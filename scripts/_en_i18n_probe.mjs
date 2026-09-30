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
 *   node scripts/_en_i18n_probe.mjs --keysrc <industry>/<slug>        EN 残留 ↔ zh 源文按 DOM 路径配对（坑 23 半译键自查）
 *   node scripts/_en_i18n_probe.mjs --check <industry>[/<slug>]       验收：英文态残留必须为 0
 *   node scripts/_en_i18n_probe.mjs --roundtrip <industry>[/<slug>]   往返回归：zh-CN→en-US→zh-CN 文本必须逐条一致
 *   node scripts/_en_i18n_probe.mjs --reindex <industry>              重建 i18n/tools/en/<ind>/_index.json
 *   node scripts/_en_i18n_probe.mjs --done <industry>/<slug>           单工具验收通过后从 pending 清单移除（逐工具记账）
 *   node scripts/_en_i18n_probe.mjs --promote <industry>              行业全绿后从 _en-i18n/industries.md 删行
 *   node scripts/_en_i18n_probe.mjs --smoke <industry>[/<slug>] [--en] 功能烟测：页面 JS 无报错 + 主流程可运行（--en 为英文态）
 *
 * 退出码：0 = 通过；1 = 有残留 / 不一致 / 报错（列出明细）。
 */
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';
import { webcrypto } from 'node:crypto';
import { JSDOM, VirtualConsole } from 'jsdom';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const STATE = path.join(ROOT, '_en-i18n');
const PENDING = path.join(STATE, 'pending');
const WORK = path.join(STATE, 'work');
const EN_DIR = path.join(ROOT, 'i18n', 'tools', 'en');
const CJK = /[\u4e00-\u9fff]/;
// 英文态残留判定口径：汉字 + 中文专属标点（全角标点、中文引号、书名号）。
// 中文专属标点常以「孤立文本节点」形式存在（如 `<b>加密</b>：<code>x</code>` 的「：」、`<code>x</code>。</p>` 的「。」），
// 不含汉字 ⇒ extract 不收集、per-tool 字典也覆盖不到，必须由 en/_common.json 全局映射兜底；
// 若 check 沿用纯汉字口径就会漏报，故此处单列更宽的正则。
const RESIDUAL_RE = /[\u4e00-\u9fff\u3002\uFF0C\u3001\uFF1B\uFF1A\uFF01\uFF1F\u300C\u300D\uFF08\uFF09]/;
const PUNCT_ONLY = /^[\u3002\uFF0C\u3001\uFF1B\uFF1A\uFF01\uFF1F\u300C\u300D\uFF08\uFF09]+$/;

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

// 全页快照（文本节点 + 表单控件 value）——判断「主流程是否真的产出了内容」。
// 必须含表单 value：大量工具把结果写进 `<textarea readonly id="output">` 的 value（不在文本节点里）。
function snapText(w) {
  let s = '';
  const k = w.document.createTreeWalker(w.document.body, w.NodeFilter.SHOW_TEXT, null, false);
  let n;
  while ((n = k.nextNode())) s += (n.nodeValue || '') + '\u0001';
  for (const el of w.document.querySelectorAll('input, textarea, select')) s += '#' + (el.value || '') + '\u0001';
  return s;
}
// 读取输出元素的值（表单控件读 value，其余读 textContent）
function readOut(el) {
  if (!el) return '';
  const tag = (el.tagName || '').toUpperCase();
  if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT') return el.value || '';
  return el.textContent || '';
}

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
    if (t && RESIDUAL_RE.test(t)) out.push(t);
  }
  return out;
}

// 属性残留：placeholder / title / aria-label / alt —— 与 js/tool-i18n.js 第三层 applyEnDict
// 翻译的属性集合一致。此前的 --check 只查文本节点，对属性里的汉字完全失明，
// 导致全站英文态输入框 placeholder、面包屑 nav aria-label 等长期漏翻却门禁 0 残留。
// 现纳入校验：精确匹配运行时翻译的属性范围，避免误报（不含 value，表单逻辑值不翻译）。
function collectCJKAttr(w) {
  const out = [];
  for (const el of w.document.querySelectorAll('[placeholder],[title],[aria-label],[alt]')) {
    if (isExcluded({ parentNode: el })) continue;
    for (const a of ['placeholder', 'title', 'aria-label', 'alt']) {
      const v = el.getAttribute(a);
      if (v && RESIDUAL_RE.test(v)) out.push(a + '="' + v + '"');
    }
  }
  return out;
}

// 校验口径（文本节点 + 属性）合集，供 --check / --scan 使用
function collectCJKFull(w) {
  return collectCJK(w).concat(collectCJKAttr(w));
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
    const res = collectCJKFull(w);
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
        if (PUNCT_ONLY.test(r)) continue;       // 纯标点节点：由 en/_common.json 统一映射，不进 per-tool 候选
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
  // 英文态抽取：collectCJK/collectCJKAttr 的「残留」口径与 --check 完全一致
  // （运行时已处理过的节点不会残留 ⇒ 天然排除 applyChrome/chrome 层与已译项）。
  // 注意：极少数节点已被 _common/_prefix 半翻译（变异系数→Coefficient of variation），
  // 其 EN 残留形态≠源文，须以 zh 态源文为键 —— 由 --check 兜底暴露，再查 _dbg/zh 抽取。
  const { w, getPending } = probePage(file, process.env.EXTRACT_LANG || 'en-US');
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
    items.push({ kind: 'text', loc: locOf(n), zh: t, path: 'T:' + nodePath(n) });
  }
  // 属性残留（placeholder/title/aria-label/alt）——与 --check 的 collectCJKAttr 口径一致。
  // 修复坑 9：此前 extract 只收 [data-zh] 与文本节点，属性（输入框 placeholder 等）
  // 完全不在待译清单里，导致「按 extract 清单译完、--check 仍报残留」。
  for (const el of w.document.querySelectorAll('[placeholder],[title],[aria-label],[alt]')) {
    if (isExcluded({ parentNode: el })) continue;
    for (const a of ['placeholder', 'title', 'aria-label', 'alt']) {
      const v = el.getAttribute(a);
      if (!v || !RESIDUAL_RE.test(v)) continue;
      const key = a + '\u0000' + v;
      if (seen.has(key)) continue;
      seen.add(key);
      items.push({ kind: 'attr:' + a, loc: locOfEl(el) + ' [' + a + ']', zh: v, path: 'A:' + a + ':' + nodePath(el) });
    }
  }
  w.close();
  // 源文配对（治坑 23）：同页再渲染 zh-CN，按 DOM 路径把每条「EN 残留」对回「中文源文」。
  // 极少数 EN 残留是 _prefix/_common 的「半翻译形态」（`Epley 公式：`→`Epley Formula:`），
  // 形态 ≠ 源文 ⇒ 直接当键永不命中。这里给每条 text/attr 项补 zh_src，并以 src_diff 标出差异项。
  try {
    const z = probePage(file, 'zh-CN');
    await settle(z.getPending);
    const zhMap = collectWithPaths(z.w);
    z.w.close();
    for (const it of items) {
      if (!it.path) continue;                       // data-zh 项：源文已在属性里，无需配对
      it.zh_src = zhMap.has(it.path) ? zhMap.get(it.path) : null;
      it.src_diff = it.zh_src !== null && it.zh_src !== it.zh;
    }
  } catch (e) { /* zh 态渲染失败不阻断 extract，仅缺 zh_src */ }
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
  const diffs = items.filter((x) => x.src_diff);
  console.log('[extract] ' + ind + '/' + slug + ' (' + meta.name + '): 待译 ' + items.length + ' 条'
    + (diffs.length ? '，形态≠源文 ' + diffs.length + ' 条（须以 zh_src 为键）' : ''));
  for (const it of items.slice(0, 14)) {
    console.log('   [' + (it.kind + ' ' + it.loc).slice(0, 26).padEnd(26) + '] ' + it.zh.slice(0, 74));
  }
  for (const it of diffs) {
    console.log('   ≠ EN: ' + it.zh.slice(0, 78));
    console.log('     ZH: ' + (it.zh_src === null ? '<无对应源节点>' : it.zh_src.slice(0, 78)));
  }
}

// ---------- 模式：keysrc（EN 残留 ↔ zh 源文 按 DOM 路径精确配对） ----------
// 解决坑 23：极少数 EN 残留是 _prefix/_common 的「半翻译形态」（如 `Epley 公式：`→`Epley Formula:`），
// 其形态 ≠ per-tool 字典所需的「运行时中文源文」。EN 态抽取拿到的是半译形态，直接当键永不命中。
// 做法：同页分别渲染 EN 与 zh-CN，按「节点 DOM 路径」（自 body 起的 childNodes 下标链）配对；
// 结构在两种语言态下一致（EN 只改文本值不改结构），故路径可精确对齐 ⇒ 直接拿到源文键。
function nodePath(n) {
  const parts = [];
  let cur = n;
  while (cur && cur.parentNode && cur.nodeName && cur.nodeName.toLowerCase() !== 'body') {
    parts.unshift(Array.prototype.indexOf.call(cur.parentNode.childNodes, cur));
    cur = cur.parentNode;
  }
  return parts.join('/');
}
function collectWithPaths(w) {
  const map = new Map();
  for (const n of textNodes(w)) {
    const t = (n.nodeValue || '').trim();
    if (!t) continue;
    map.set('T:' + nodePath(n), t);
  }
  for (const el of w.document.querySelectorAll('[placeholder],[title],[aria-label],[alt]')) {
    if (isExcluded({ parentNode: el })) continue;
    for (const a of ['placeholder', 'title', 'aria-label', 'alt']) {
      const v = (el.getAttribute(a) || '').trim();
      if (!v) continue;
      map.set('A:' + a + ':' + nodePath(el), v);
    }
  }
  return map;
}
async function keysrc(target) {
  const [ind, slug] = target.split('/');
  const file = path.join(ROOT, BASE, ind, slug + '.html');
  if (!fs.existsSync(file)) { console.error('工具页不存在: ' + file); process.exit(1); }
  const en = probePage(file, 'en-US');
  await settle(en.getPending);
  const enMap = collectWithPaths(en.w);
  en.w.close();
  const zh = probePage(file, 'zh-CN');
  await settle(zh.getPending);
  const zhMap = collectWithPaths(zh.w);
  zh.w.close();
  const rows = [];
  for (const [k, v] of enMap) {
    if (!RESIDUAL_RE.test(v)) continue;          // 只关心 EN 态残留
    const src = zhMap.has(k) ? zhMap.get(k) : null;
    rows.push({ path: k, en: v, zh: src, same: src === v });
  }
  rows.sort((a, b) => (a.same === b.same ? 0 : (a.same ? 1 : -1)));
  fs.mkdirSync(path.join(WORK, ind), { recursive: true });
  fs.writeFileSync(path.join(WORK, ind, slug + '.keysrc.json'),
    JSON.stringify({ industry: ind, slug, count: rows.length, rows }, null, 1) + '\n');
  const diff = rows.filter((r) => !r.same).length;
  console.log('[keysrc] ' + ind + '/' + slug + ': EN 残留 ' + rows.length
    + ' 条，其中形态≠源文 ' + diff + ' 条（须以 zh 为键）');
  for (const r of rows) {
    if (r.same) continue;
    console.log('  ≠ EN: ' + r.en.slice(0, 90));
    console.log('    ZH: ' + (r.zh === null ? '<无对应源节点：动态插入/结构差异>' : r.zh.slice(0, 90)));
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
      const res = collectCJKFull(w);
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

// ---------- 模式：smoke（功能烟测：JS 无报错 + 主流程可运行） ----------
// 与 --check 互补：--check 只看「文本是否残留中文」，本模式看「页面还跑不跑得动」。
// 用 runScripts:'dangerously' 真实执行页面内联脚本（外部 CDN/JS 不加载，需 i18n 层时手动 eval 模拟），
// 捕获 jsdomError / window.error / unhandledrejection，再点击主流程按钮检查输出。
const SMOKE_BTN_SKIP = /copy|clear|reset|theme|toggle|download|share|print|save|delete|remove|upload|paste/i;
async function smoke(targets, opts) {
  let bad = 0;
  let total = 0;
  for (const target of targets) {
    const seg = target.split('/');
    const ind = seg[0];
    const tools = seg[1] ? [{ slug: seg[1], file: path.join(ROOT, BASE, ind, seg[1] + '.html') }] : industryTools(ind);
    for (const t of tools) {
      if (!fs.existsSync(t.file)) { console.error('缺失: ' + t.file); bad++; continue; }
      total++;
      const errors = [];
      const envNotes = [];
      const vc = new VirtualConsole();
      vc.on('jsdomError', (e) => {
        const msg = 'jsdomError: ' + ((e && e.message) || String(e));
        // 「Not implemented: …」= jsdom 未实现的原生 API（alert/clipboard/canvas 等），属环境限制、非页面缺陷
        if (/Not implemented/.test(msg)) envNotes.push(msg); else errors.push(msg);
      });
      const dom = new JSDOM(fs.readFileSync(t.file, 'utf8'), {
        url: 'https://toolbox.local/' + BASE + '/' + ind + '/' + t.slug + '.html?lang=' + (opts.en ? 'en-US' : 'zh-CN'),
        runScripts: 'dangerously',
        pretendToBeVisual: true,
        virtualConsole: vc,
        beforeParse(w2) {
          w2.lucide = { createIcons() {} };
          w2.scrollTo = () => {};
          // jsdom 未实现 Element.scrollIntoView（真实浏览器有）⇒ 结果页自动滚动类页面会误报
          // 「scrollIntoView is not a function」，属环境限制、非页面缺陷，故补 no-op 存根。
          try { w2.Element.prototype.scrollIntoView = () => {}; } catch (e) {}
          try { w2.HTMLElement.prototype.scrollIntoView = () => {}; } catch (e) {}
          w2.alert = () => {};
          w2.confirm = () => true;
          w2.prompt = () => '';
          try { w2.navigator.clipboard = { writeText: () => Promise.resolve(), readText: () => Promise.resolve('') }; } catch (e) {}
          // canvas 2D 桩：jsdom 无 canvas 实现（getContext 返回 null），会让条形码/绘图类页面误报 TypeError。
          // 真实浏览器有 canvas ⇒ 此处只补环境能力，不做逻辑替换。所有绘图方法 no-op、属性可读可写。
          try {
            const mkCtx = () => new Proxy({}, {
              get(t, k) {
                if (k === 'canvas') return { width: 300, height: 150 };
                if (k === 'measureText') return () => ({ width: 0 });
                if (k === 'getImageData') return (x, y, wd, ht) => ({ data: new Uint8ClampedArray(Math.max(4, wd * ht * 4)), width: wd, height: ht });
                if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
                if (k === 'getContextAttributes') return () => ({});
                if (k in t) return t[k];
                return typeof k === 'string' ? () => {} : undefined;
              },
              set(t, k, v) { t[k] = v; return true; },
            });
            w2.HTMLCanvasElement.prototype.getContext = function () { return mkCtx(); };
            w2.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/png;base64,'; };
            w2.HTMLCanvasElement.prototype.toBlob = function (cb) { if (cb) cb(new w2.Blob([], { type: 'image/png' })); };
          } catch (e) {}
          w2.matchMedia = w2.matchMedia || (() => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }));
          // Web Audio API 能力补齐（环境限制，非页面缺陷）：
          // jsdom 未实现 AudioContext / webkitAudioContext，纯前端音频合成类页面（笑声音效生成器等）
          // 因此抛 "(window.AudioContext || window.webkitAudioContext) is not a constructor"，与 i18n 无关。
          // 真实浏览器完整支持 ⇒ 此处补齐最小可用桩（不真正发声，保证不抛错）。
          try {
            if (typeof w2.AudioContext === 'undefined' && typeof w2.webkitAudioContext === 'undefined') {
              const audioParam = () => ({ value: 0, setValueAtTime() {}, linearRampToValueAtTime() {}, exponentialRampToValueAtTime() {}, setTargetAtTime() {}, cancelScheduledValues() {}, setValueCurveAtTime() {} });
              const AudioCtxStub = function () {
                this.currentTime = 0;
                this.destination = {};
                this.sampleRate = 44100;
                this.state = 'running';
                this.createOscillator = () => ({ frequency: audioParam(), detune: audioParam(), type: 'sine', connect() {}, disconnect() {}, start() {}, stop() {} });
                this.createGain = () => ({ gain: audioParam(), connect() {}, disconnect() {} });
                this.createBiquadFilter = () => ({ type: 'lowpass', frequency: audioParam(), Q: audioParam(), connect() {}, disconnect() {} });
                this.createAnalyser = () => ({ fftSize: 2048, frequencyBinCount: 1024, connect() {}, disconnect() {}, getByteTimeDomainData() {}, getByteFrequencyData() {} });
                this.createBuffer = () => ({ getChannelData: () => new Float32Array(8) });
                this.createBufferSource = () => ({ buffer: null, loop: false, connect() {}, disconnect() {}, start() {}, stop() {} });
                this.resume = () => Promise.resolve();
                this.suspend = () => Promise.resolve();
                this.close = () => Promise.resolve();
              };
              w2.AudioContext = AudioCtxStub;
              w2.webkitAudioContext = AudioCtxStub;
            }
          } catch (e) {}
          // WebCrypto / TextEncoder 能力补齐（环境限制，非页面缺陷）：
          // jsdom 只实现 crypto.getRandomValues / randomUUID，未实现 crypto.subtle，也未提供全局 TextEncoder。
          // 加密类页面（ECDSA/RSA/AES/PBKDF2/HMAC/JWT…）因此抛 TypeError，并把异常文本渲染进 #output，
          // 被后面的 suspicious 正则误判为「输出异常值」。真实浏览器（HTTPS secure context）完整支持 ⇒ 此处补齐环境能力。
          // 优先注入 Node 内置真实实现（密码学主流程可真正跑通、产出真实值），失败时退回最小可用桩（保证不抛错）。
          try { if (typeof w2.TextEncoder === 'undefined') w2.TextEncoder = TextEncoder; } catch (e) {}
          try { if (typeof w2.TextDecoder === 'undefined') w2.TextDecoder = TextDecoder; } catch (e) {}
          try {
            if (w2.crypto && !w2.crypto.subtle) {
              let real = null;
              try { real = webcrypto.subtle; } catch (e) {}
              if (real) {
                Object.defineProperty(w2.crypto, 'subtle', { value: real, configurable: true });
              } else {
                const buf = (n) => new ArrayBuffer(n);
                const keyObj = (type) => ({ type, algorithm: { name: 'ECDSA' }, extractable: true, usages: [] });
                Object.defineProperty(w2.crypto, 'subtle', {
                  configurable: true,
                  value: {
                    async generateKey() { return { publicKey: keyObj('public'), privateKey: keyObj('private') }; },
                    async importKey() { return keyObj('private'); },
                    async exportKey() { return buf(64); },
                    async sign() { return buf(64); },
                    async verify() { return true; },
                    async digest() { return buf(32); },
                    async encrypt() { return buf(32); },
                    async decrypt() { return buf(32); },
                    async deriveBits() { return buf(32); },
                    async deriveKey() { return keyObj('secret'); },
                    async wrapKey() { return buf(32); },
                    async unwrapKey() { return keyObj('secret'); },
                  },
                });
              }
            }
          } catch (e) {}
          w2.fetch = (u) => {
            try {
              const clean = decodeURIComponent(String(u).split('?')[0].split('#')[0]).replace(/^\/+/, '');
              const data = fs.readFileSync(path.join(ROOT, clean), 'utf8');
              return Promise.resolve({ ok: true, status: 200, json: async () => JSON.parse(data), text: async () => data });
            } catch (e) {
              return Promise.resolve({ ok: false, status: 404, json: async () => null, text: async () => '' });
            }
          };
          w2.addEventListener('error', (e) => errors.push('window.error: ' + ((e && (e.message || (e.error && e.error.message))) || 'unknown')));
          w2.addEventListener('unhandledrejection', (e) => errors.push('unhandledrejection: ' + String((e && e.reason) || '')));
        },
      });
      const w = dom.window;
      await tick(30);
      if (opts.en) {
        try { w.__TI18N_EN = enData(); w.eval(I18N_SRC()); w.eval(TI18N_SRC()); } catch (e) { errors.push('en-eval: ' + e.message); }
        await tick(20);
      }
      // 空输入补样本值：让主流程真正跑起来（只填空值，不覆盖页面预设）；
      // 数字类输入喂纯数字（条形码/编码类对字符集敏感），其余喂混合样本。
      let filled = 0;
      for (const el of w.document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=button]):not([type=submit]):not([type=file]):not([type=range]):not([type=color]), textarea')) {
        if (el.disabled || el.readOnly) continue;
        if ((el.value || '') !== '') continue;
        const hint = ((el.getAttribute('placeholder') || '') + (el.getAttribute('aria-label') || '') + (el.getAttribute('id') || '')).toLowerCase();
        try {
          const numLike = /数字|number|digit|numeric/.test(hint) && !/文本|文字|字母|明文|密文|text|letter|word/.test(hint);
          el.value = numLike ? '12345678' : 'Hello World 123';
          el.dispatchEvent(new w.Event('input', { bubbles: true }));
          el.dispatchEvent(new w.Event('change', { bubbles: true }));
          filled++;
        } catch (e) {}
        if (filled >= 3) break;
      }
      const outEl = w.document.querySelector('#output, #result, .result, .tool-output, output, pre');
      let clicked = 0;
      let produced = false;
      const btns = [...w.document.querySelectorAll('button[onclick]')]
        .filter((b) => !SMOKE_BTN_SKIP.test(b.getAttribute('onclick') || ''));
      // 逐按钮独立判定产出：连点两个按钮时，后一个（如「解码」）常会覆盖/清空前一个的产出，
      // 若只在末尾比对终态就会误判为「无产出」。
      for (const b of btns.slice(0, 3)) {
        const s0 = snapText(w);
        try { b.click(); clicked++; } catch (e) { errors.push('click: ' + e.message); }
        await tick(35);
        if (snapText(w) !== s0) produced = true;
      }
      const afterOut = readOut(outEl);
      const suspicious = /(^|[^A-Za-z])(NaN|undefined|Infinity)($|[^A-Za-z])/.test(afterOut);
      w.close();
      if (errors.length || suspicious) {
        bad++;
        console.log('❌ ' + ind + '/' + t.slug + (opts.en ? ' [en]' : '')
          + (errors.length ? '  报错 ' + errors.length : '') + (suspicious ? '  输出异常值' : ''));
        for (const e of errors.slice(0, 5)) console.log('     · ' + e.slice(0, 150));
        if (suspicious) console.log('     · 输出含 NaN/undefined/Infinity: ' + afterOut.slice(0, 100));
      } else if (!clicked) {
        console.log('ℹ️  ' + ind + '/' + t.slug + (opts.en ? ' [en]' : '') + ' 无主流程按钮（查询/展示类）');
      } else if (!produced) {
        console.log('⚠️  ' + ind + '/' + t.slug + (opts.en ? ' [en]' : '')
          + '  点击了 ' + clicked + ' 个按钮但无输出变化'
          + (envNotes.length ? '（jsdom 未实现 ' + envNotes.length + ' 项）' : ''));
      } else if (envNotes.length) {
        console.log('ℹ️  ' + ind + '/' + t.slug + (opts.en ? ' [en]' : '') + ' OK（jsdom 未实现提示 ' + envNotes.length + ' 项）');
      }
    }
  }
  console.log('\n[smoke] 共 ' + total + ' 页，异常 ' + bad + ' 页');
  process.exitCode = bad ? 1 : 0;
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
const mode = argv.find((a) => a.startsWith('--') && a !== '--tw' && a !== '--en');
const args = argv.filter((a) => !a.startsWith('--'));
if (argv.indexOf('--tw') > -1) BASE = 'zh-tw/tools';   // 校验繁体构建产物（中文态还原、英文态同形受益）

(async () => {
  fs.mkdirSync(STATE, { recursive: true });
  switch (mode) {
    case '--scan': await scan(args[0]); break;
    case '--mine': await mine(args); break;
    case '--extract': await extract(args[0]); break;
    case '--keysrc': await keysrc(args[0]); break;
    case '--check': await check(args); break;
    case '--roundtrip': await roundtrip(args); break;
    case '--smoke': await smoke(args, { en: argv.indexOf('--en') > -1 }); break;
    case '--reindex': reindex(args[0]); break;
    case '--done': done(args[0]); break;
    case '--promote': promote(args[0]); break;
    default:
      console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('*/')[0]);
      process.exit(1);
  }
})();
