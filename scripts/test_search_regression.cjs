/**
 * B5-01 Search regression harness.
 *
 * Mirrors js/app.js toolboxScore + toolboxSearch (hybrid exact/pinyin/alias
 * ranker + Fuse fuzzy fallback) and asserts quality targets using cases
 * generated from the real index.
 *
 * Run: node scripts/test_search_regression.cjs
 * Exit code 0 = pass, 1 = below target.
 */
const path = require('path');
const fs = require('fs');
const Fuse = require(path.join(__dirname, '..', 'vendor', 'fuse.min.js'));

const ROOT = path.join(__dirname, '..');
const index = JSON.parse(fs.readFileSync(path.join(ROOT, 'json', 'search-index.json'), 'utf-8'));
const PINYIN = JSON.parse(fs.readFileSync(path.join(ROOT, 'scripts', '_pinyin_map.json'), 'utf-8'));

const fuse = new Fuse(index, {
  keys: [
    { name: 'n', weight: 0.42 },
    { name: 's', weight: 0.28 },
    { name: 'al', weight: 0.30 },
    { name: 'd', weight: 0.13 },
    { name: 'i', weight: 0.05 },
    { name: 'c', weight: 0.05 },
  ],
  threshold: 0.38,
  ignoreLocation: true,
  minMatchCharLength: 1,
  includeScore: true,
});

function toolboxScore(t, q) {
  const name = (t.n || '').toLowerCase();
  const slug = (t.s || '').toLowerCase();
  const alias = (t.al || []).join(' ').toLowerCase();
  const py = (t.py || '').toLowerCase();
  if (name === q) return 1000;
  if (name.startsWith(q)) return 920 - name.length;
  if (name.indexOf(q) >= 0) return 820 - name.indexOf(q);
  if (py && py.indexOf(q) >= 0) return 600 - py.indexOf(q) * 0.5;
  if (slug.indexOf(q) >= 0) return 560 - slug.indexOf(q) * 0.5;
  if (alias.indexOf(q) >= 0) return 520;
  return -1;
}

function toolboxSearch(query, limit) {
  const q = (query || '').toLowerCase().trim();
  if (!q) return [];
  const direct = index
    .filter(t => toolboxScore(t, q) >= 0)
    .sort((a, b) => toolboxScore(b, q) - toolboxScore(a, q));
  const fz = fuse.search(q, { limit: 300 });
  const seen = new Set(direct.map(t => t.u));
  const fuzzy = fz
    .filter(r => !seen.has(r.item.u))
    .map(r => ({ t: r.item, s: 300 - (r.score || 0) * 300 }))
    .sort((a, b) => b.s - a.s)
    .map(x => x.t);
  return direct.concat(fuzzy).slice(0, limit || 20);
}

function pinyinOf(name) {
  let s = '';
  for (const ch of name) s += PINYIN[ch] || '';
  return s.toLowerCase();
}

// ---- Generate cases from the real index ----
function buildCases() {
  const cases = [];
  const byUrl = {};
  const chinese = index.filter(t => /[一-鿿]/.test(t.n));
  // 1) Chinese exact-name (expect first hit)
  let cn = 0;
  for (const t of chinese) {
    if (cn >= 40) break;
    if (t.n.length < 3) continue;
    cases.push({ group: 'cn', q: t.n, expect: t.u, exact: true });
    cn++;
  }
  // 2) Pinyin (expect in top 10)
  let py = 0;
  for (const t of chinese) {
    if (py >= 40) break;
    const p = pinyinOf(t.n);
    if (p.length < 4) continue;
    cases.push({ group: 'py', q: p, expect: t.u });
    py++;
  }
  // 3) English/slug alias (expect in top 10)
  let en = 0;
  for (const t of index) {
    if (en >= 40) break;
    const toks = (t.s || '').split('-').filter(x => x.length >= 3 && /[a-z]/.test(x));
    if (!toks.length) continue;
    cases.push({ group: 'en', q: toks[0], expect: t.u });
    en++;
  }
  // 4) Typo / truncated Chinese (expect in top 10, fuzzy)
  let tp = 0;
  for (const t of chinese) {
    if (tp >= 40) break;
    if (t.n.length < 5) continue;
    const q = t.n.slice(0, t.n.length - 1); // drop last char (common typo)
    cases.push({ group: 'tp', q, expect: t.u });
    tp++;
  }
  return cases;
}

const CASES = buildCases();
const TOP = 10;
const groups = {};
for (const c of CASES) (groups[c.group] = groups[c.group] || []).push(c);

function evalGroup(list, exactRequired) {
  let pass = 0;
  const fails = [];
  for (const c of list) {
    const res = toolboxSearch(c.q, TOP);
    const urls = res.map(r => r.u);
    let ok = false;
    if (exactRequired) ok = urls.length > 0 && urls[0] === c.expect;
    else ok = urls.some(u => u === c.expect);
    if (ok) pass++;
    else fails.push({ q: c.q, expect: c.expect, top: urls.slice(0, 3) });
  }
  return { pass, total: list.length, rate: pass / list.length, fails };
}

let allPass = 0;
for (const g of ['cn', 'py', 'en', 'tp']) {
  const r = evalGroup(groups[g], g === 'cn');
  allPass += r.pass;
  console.log(`${g}: ${r.pass}/${r.total} (${(r.rate * 100).toFixed(1)}%)`);
  for (const f of r.fails.slice(0, 5)) {
    console.log(`   FAIL "${f.q}" expect ${f.expect} top=${JSON.stringify(f.top)}`);
  }
}

const total = CASES.length;
const rate = allPass / total;
const cnRate = evalGroup(groups.cn, true).rate;
console.log(`\nOverall: ${allPass}/${total} (${(rate * 100).toFixed(1)}%) | cn-exact-first: ${(cnRate * 100).toFixed(1)}%`);

if (rate < 0.95 || cnRate < 1) {
  console.log('FAIL: B5-01 target not met (need overall>=95%, cn-exact-first=100%)');
  process.exit(1);
}
console.log('PASS: B5-01 search quality targets met');
