#!/usr/bin/env node
/**
 * _en_i18n_probe.mjs — 英文态「内容区全量英文化」专项·统一探针
 *
 * 真机（jsdom）模拟：直接加载页面并执行真实 js/i18n.js + js/tool-i18n.js，
 * 与运行时共用同一套代码 ⇒ 零口径偏差（不做静态复刻，避免第二套匹配逻辑）。
 *
 * 用法：
 *   node scripts/_en_i18n_probe.mjs --scan <industry>                 生成 _en-i18n/pending/<ind>.json
 *   node scripts/_en_i18n_probe.mjs --extract <industry>/<slug>       输出待译明细 _en-i18n/work/<ind>/<slug>.json
 *   node scripts/_en_i18n_probe.mjs --check <industry>[/<slug>]       验收：英文态残留必须为 0
 *   node scripts/_en_i18n_probe.mjs --roundtrip <industry>[/<slug>]   往返回归：zh-CN→en-US→zh-CN 文本必须逐条一致
 *   node scripts/_en_i18n_probe.mjs --reindex <industry>              重建 i18n/tools/en/<ind>/_index.json
 *   node scripts/_en_i18n_probe.mjs --done <industry>/<slug>           单工具验收通过后从 pending 清单移除（逐工具记账）
 *   node scripts/_en_i18n_probe.mjs --promote <industry>              行业全绿后从 _en-i18n/industries.md 删行
 *
 * 退出码：0 = 通过；1 = 有残留 / 不一致（列出明细）。
 */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const STATE = path.join(ROOT, '_en-i18n');
const PENDING = path.join(STATE, 'pending');
const WORK = path.join(STATE, 'work');
const EN_DIR = path.join(ROOT, 'i18n', 'tools', 'en');
const CJK = /[\u4e00-\u9fff]/;

// ---------- 只读一次的数据（进程内缓存） ----------
let EN_DATA = null;
function enData() {
  if (EN_DATA) return EN_DATA;
  const ctx = { window: {} };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n-en.js'), 'utf8'), ctx);
  EN_DATA = ctx.window.__TI18N_EN || {};
  return EN_DATA;
}
const I18N_SRC = () => fs.readFileSync(path.join(ROOT, 'js', 'i18n.js'), 'utf8');
const TI18N_SRC = () => fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n.js'), 'utf8');

// ---------- 单页探针 ----------
function probePage(htmlPath, lang) {
  const rel = path.relative(ROOT, htmlPath).split(path.sep).join('/');
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, {
    url: 'https://toolbox.local/' + rel + '?lang=' + lang,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
  });
  const w = dom.window;
  let pending = 0;
  if (lang !== 'zh-CN') w.__TI18N_EN = enData();
  w.fetch = (u) => {
    const clean = decodeURIComponent(String(u).split('?')[0].split('#')[0]).replace(/^\/+/, '');
    const fp = path.join(ROOT, clean);
    pending++;
    return new Promise((resolve) => {
      fs.readFile(fp, 'utf8', (err, data) => {
        pending--;
        if (err) {
          resolve({ ok: false, status: 404, json: async () => null, text: async () => '' });
        } else {
          resolve({ ok: true, status: 200, json: async () => JSON.parse(data), text: async () => data });
        }
      });
    });
  };
  w.eval(I18N_SRC());
  w.eval(TI18N_SRC());
  return { w, getPending: () => pending };
}

const tick = (ms = 4) => new Promise((r) => setTimeout(r, ms));

async function settle(getPending, rounds = 60) {
  for (let i = 0; i < rounds; i++) {
    await tick();
    if (getPending() === 0) {
      await tick();
      if (getPending() === 0) return;
    }
  }
}

// 系统 UI 白名单：语言切换器内的语言名（简体中文 / 繁體中文 / English）是语言选择器自身，
// 按惯例用本语言显示，不参与翻译，也不计入残留。
function isExcluded(n) {
  let el = n.parentNode;
  while (el && el.nodeName && el.nodeName.toLowerCase() !== 'body') {
    const cls = (el.getAttribute && el.getAttribute('class')) || '';
    if (/(^|\s)lang-switcher(\s|$)/.test(cls)) return true;
    el = el.parentNode;
  }
  return false;
}

// 可见文本节点（排除 script/style/noscript 与系统 UI 白名单）
function* textNodes(w) {
  const walker = w.document.createTreeWalker(w.document.body, w.NodeFilter.SHOW_TEXT, null, false);
  let n;
  while ((n = walker.nextNode())) {
    const p = n.parentNode;
    if (!p) continue;
    const tag = (p.nodeName || '').toUpperCase();
    if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
    if (isExcluded(n)) continue;
    yield n;
  }
}

function collectCJK(w) {
  const out = [];
  for (const n of textNodes(w)) {
    const t = (n.nodeValue || '').trim();
    if (t && CJK.test(t)) out.push(t);
  }
  return out;
}

function collectAll(w) {
  const out = [];
  for (const n of textNodes(w)) {
    const t = (n.nodeValue || '').trim();
    if (t) out.push(t);
  }
  return out;
}

// 定位路径：祖先标签 + class（供翻译时判断上下文）
function locOfEl(el) {
  const parts = [];
  let cur = el;
  while (cur && cur.nodeName && cur.nodeName.toLowerCase() !== 'body') {
    const tag = cur.nodeName.toLowerCase();
    const cls = (cur.getAttribute && cur.getAttribute('class')) || '';
    parts.unshift(cls ? tag + '.' + cls.split(/\s+/)[0] : tag);
    cur = cur.parentNode;
    if (parts.length >= 4) break;
  }
  return parts.join(' > ');
}
const locOf = (n) => locOfEl(n.parentNode);

// ---------- 工具清单 ----------
// BASE = 'tools'（简体源）或 'zh-tw/tools'（繁体构建产物）
let BASE = 'tools';
function industryTools(ind) {
  const dir = path.join(ROOT, BASE, ind);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.html') && f !== 'index.html')
    .sort()
    .map((f) => ({ slug: f.replace(/\.html$/, ''), file: path.join(dir, f) }));
}

let SI = null;
function toolMeta(ind, slug) {
  if (!SI) { try { SI = JSON.parse(fs.readFileSync(path.join(ROOT, 'json', 'tools.json'), 'utf8')); } catch (e) { SI = []; } }
  for (const t of SI) {
    const u = t.url || t.u || '';
    if (u.endsWith('/' + slug + '.html') && (!ind || u.indexOf('/' + ind + '/') > -1)) {
      return { name: t.name || t.n || '', en: t.en || '', ed: t.ed || '', desc: t.desc || t.d || '' };
    }
  }
  return { name: '', en: '', ed: '', desc: '' };
}

// ---------- 模式：scan ----------
async function scan(ind) {
  const tools = industryTools(ind);
  if (!tools.length) { console.error('行业不存在或无工具页: ' + ind); process.exit(1); }
  const out = [];
  let totalResidual = 0;
  for (const t of tools) {
    const { w, getPending } = probePage(t.file, 'en-US');
    await settle(getPending);
    const res = collectCJK(w);
    w.close();
    totalResidual += res.length;
    if (res.length) out.push({ slug: t.slug, residual: res.length, samples: res.slice(0, 3) });
  }
  fs.mkdirSync(PENDING, { recursive: true });
  const payload = {
    industry: ind,
    scanned_at: new Date().toISOString().slice(0, 10),
    baseline: { tools: tools.length, residual_nodes: totalResidual },
    tools: out,
  };
  fs.writeFileSync(path.join(PENDING, ind + '.json'), JSON.stringify(payload, null, 1) + '\n');
  console.log('[scan] ' + ind + ': 工具 ' + tools.length + '，有问题 ' + out.length + '，残留节点 ' + totalResidual);
  for (const o of out.slice(0, 12)) {
    console.log('   ' + String(o.slug).padEnd(28) + ' residual=' + String(o.residual).padEnd(4) + o.samples.join(' | ').slice(0, 88));
  }
}

// ---------- 模式：mine（跨行业挖掘全站通用句，供 i18n/tools/en/_common.json 使用） ----------
async function mine(industries) {
  const freq = new Map();
  const where = new Map();
  let pages = 0;
  for (const ind of industries) {
    for (const t of industryTools(ind)) {
      const { w, getPending } = probePage(t.file, 'en-US');
      await settle(getPending);
      for (const r of collectCJK(w)) {
        if (/\|\s*ToolBox/.test(r)) continue;   // 相关工具卡片 SEO 名称：由 slug-en.json 机制负责，不属本层
        freq.set(r, (freq.get(r) || 0) + 1);
        if (!where.has(r)) where.set(r, ind + '/' + t.slug);
      }
      w.close();
      pages++;
    }
  }
  const cand = [...freq.entries()].filter(([, c]) => c >= 3).sort((a, b) => b[1] - a[1]);
  const payload = {
    generated: new Date().toISOString().slice(0, 10),
    pages,
    industries,
    candidates: cand.map(([text, count]) => ({ text, count, sample: where.get(text) })),
  };
  fs.writeFileSync(path.join(STATE, 'common-candidates.json'), JSON.stringify(payload, null, 1) + '\n');
  console.log('[mine] ' + pages + ' 页，唯一残留 ' + freq.size + ' 条，复现≥3 的 ' + cand.length + ' 条');
  for (const [t, c] of cand.slice(0, 60)) console.log(String(c).padStart(5) + '  ' + t.slice(0, 96));
}

// ---------- 模式：extract ----------
async function extract(target) {
  const [ind, slug] = target.split('/');
  const file = path.join(ROOT, 'tools', ind, slug + '.html');
  if (!fs.existsSync(file)) { console.error('工具页不存在: ' + file); process.exit(1); }
  const { w, getPending } = probePage(file, 'en-US');
  await settle(getPending);
  const meta = toolMeta(ind, slug);
  const items = [];
  const seen = new Set();
  // [data-zh] 优先（h2 / 首 p：英文态静态文本是构建期预渲染值，中文原文在 data-zh）
  for (const el of w.document.querySelectorAll('[data-zh]')) {
    if (el.children && el.children.length) continue;
    const dz = el.getAttribute('data-zh');
    if (!dz || !CJK.test(dz) || seen.has(dz)) continue;
    seen.add(dz);
    items.push({ kind: 'data-zh', loc: locOfEl(el), zh: dz, current_en: (el.textContent || '').trim() });
  }
  for (const n of textNodes(w)) {
    const t = (n.nodeValue || '').trim();
    if (!t || !CJK.test(t) || seen.has(t)) continue;
    seen.add(t);
    items.push({ kind: 'text', loc: locOf(n), zh: t });
  }
  w.close();
  fs.mkdirSync(path.join(WORK, ind), { recursive: true });
  const payload = {
    industry: ind,
    slug,
    name: meta.name,
    exist_en: meta.en,
    exist_ed: meta.ed,
    count: items.length,
    items,
  };
  fs.writeFileSync(path.join(WORK, ind, slug + '.json'), JSON.stringify(payload, null, 1) + '\n');
  console.log('[extract] ' + ind + '/' + slug + ' (' + meta.name + '): 待译 ' + items.length + ' 条');
  for (const it of items.slice(0, 14)) {
    console.log('   [' + (it.kind + ' ' + it.loc).slice(0, 26).padEnd(26) + '] ' + it.zh.slice(0, 74));
  }
}

// ---------- 模式：check ----------
async function check(targets) {
  let bad = 0;
  let total = 0;
  for (const target of targets) {
    const seg = target.split('/');
    const ind = seg[0];
    const tools = seg[1] ? [{ slug: seg[1], file: path.join(ROOT, BASE, ind, seg[1] + '.html') }] : industryTools(ind);
    for (const t of tools) {
      if (!fs.existsSync(t.file)) { console.error('缺失: ' + t.file); bad++; continue; }
      total++;
      const { w, getPending } = probePage(t.file, 'en-US');
      await settle(getPending);
      const res = collectCJK(w);
      w.close();
      if (res.length) {
        bad++;
        console.log('❌ ' + ind + '/' + t.slug + '  残留 ' + res.length);
        for (const r of res.slice(0, 8)) console.log('     · ' + r.slice(0, 100));
      }
    }
  }
  console.log('\n[check] 共 ' + total + ' 页，有残留 ' + bad + ' 页');
  process.exitCode = bad ? 1 : 0;
}

// ---------- 模式：roundtrip（中文态还原性回归） ----------
async function roundtrip(targets) {
  let bad = 0;
  let total = 0;
  for (const target of targets) {
    const seg = target.split('/');
    const ind = seg[0];
    const tools = seg[1] ? [{ slug: seg[1], file: path.join(ROOT, BASE, ind, seg[1] + '.html') }] : industryTools(ind);
    for (const t of tools) {
      if (!fs.existsSync(t.file)) { bad++; continue; }
      total++;
      const { w, getPending } = probePage(t.file, 'zh-CN');
      await settle(getPending);
      const before = collectAll(w);
      const origin = w.I18n.get();          // 简体源 = zh-CN；繁体产物 = zh-TW
      w.I18n.set('en-US', { persist: false });
      await settle(getPending);
      w.I18n.set(origin, { persist: false });   // 按页面原始语言还原（繁体页回 zh-TW）
      await settle(getPending);
      const after = collectAll(w);
      const diff = [];
      const n = Math.max(before.length, after.length);
      for (let i = 0; i < n; i++) if (before[i] !== after[i]) diff.push({ i, b: before[i], a: after[i] });
      w.close();
      if (diff.length) {
        bad++;
        console.log('❌ ' + ind + '/' + t.slug + '  往返不一致 ' + diff.length + ' 处');
        for (const d of diff.slice(0, 5)) {
          console.log('     · #' + d.i + ' 「' + String(d.b).slice(0, 46) + '」 → 「' + String(d.a).slice(0, 46) + '」');
        }
      }
    }
  }
  console.log('\n[roundtrip] 共 ' + total + ' 页，不一致 ' + bad + ' 页');
  process.exitCode = bad ? 1 : 0;
}

// ---------- 模式：done（单工具完成后从 pending 清单移除，逐工具记账） ----------
function done(target) {
  const [ind, slug] = target.split('/');
  const p = path.join(PENDING, ind + '.json');
  if (!fs.existsSync(p)) { console.log('[done] ' + ind + ' 无待处理清单（可能已完成）'); return; }
  const data = JSON.parse(fs.readFileSync(p, 'utf8'));
  const before = data.tools.length;
  data.tools = data.tools.filter((t) => t.slug !== slug);
  const removed = before - data.tools.length;
  if (removed) {
    data.baseline.residual_nodes = data.tools.reduce((s, t) => s + (t.residual || 0), 0);
    fs.writeFileSync(p, JSON.stringify(data, null, 1) + '\n');
  }
  console.log('[done] ' + ind + '/' + slug + (removed ? ' 已移除' : ' 不在清单中')
    + '；剩余 ' + data.tools.length + ' 个工具'
    + (data.tools.length === 0 ? '（行业已全绿，可 --promote ' + ind + '）' : ''));
}

// ---------- 模式：reindex ----------
function reindex(ind) {
  const dir = path.join(EN_DIR, ind);
  const tools = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((f) => f.endsWith('.json') && f !== '_index.json').map((f) => f.replace(/\.json$/, '')).sort()
    : [];
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, '_index.json'), JSON.stringify({ industry: ind, tools }, null, 1) + '\n');
  console.log('[reindex] ' + ind + ': ' + tools.length + ' 个字典');
}

// ---------- 模式：promote ----------
function promote(ind) {
  const p = path.join(STATE, 'industries.md');
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  const re = new RegExp('\\|\\s*`' + ind + '`\\s*\\|');
  const kept = lines.filter((l) => !re.test(l));
  const removed = lines.length - kept.length;
  if (!removed) { console.log('[promote] ' + ind + ' 不在清单中（可能已完成）'); return; }
  let seq = 0;
  const out = kept.map((l) => {
    if (/^\|\s*\d+\s*\|/.test(l)) { seq++; return l.replace(/^\|\s*\d+\s*\|/, '| ' + seq + ' |'); }
    return l;
  });
  fs.writeFileSync(p, out.join('\n'));
  const pend = path.join(PENDING, ind + '.json');
  if (fs.existsSync(pend)) fs.unlinkSync(pend);
  const remain = out.filter((l) => /^\|\s*\d+\s*\|/.test(l)).length;
  console.log('[promote] ' + ind + ' 已移除，清单剩余 ' + remain + ' 个行业');
}

// ---------- CLI ----------
const argv = process.argv.slice(2);
const mode = argv.find((a) => a.startsWith('--') && a !== '--tw');
const args = argv.filter((a) => !a.startsWith('--'));
if (argv.indexOf('--tw') > -1) BASE = 'zh-tw/tools';   // 校验繁体构建产物（中文态还原、英文态同形受益）

(async () => {
  fs.mkdirSync(STATE, { recursive: true });
  switch (mode) {
    case '--scan': await scan(args[0]); break;
    case '--mine': await mine(args); break;
    case '--extract': await extract(args[0]); break;
    case '--check': await check(args); break;
    case '--roundtrip': await roundtrip(args); break;
    case '--reindex': reindex(args[0]); break;
    case '--done': done(args[0]); break;
    case '--promote': promote(args[0]); break;
    default:
      console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0]);
      process.exit(1);
  }
})();
