#!/usr/bin/env node
/*
 * 指南页 EN i18n 探针（与 js/guide-i18n.js 运行时同口径）
 *   node scripts/_en_i18n_guide_probe.mjs --extract <slug>     抽取待译中文文本节点 → _en-i18n/work/guides/<slug>.json
 *   node scripts/_en_i18n_guide_probe.mjs --check   <slug>     验收：应用词典后残留 CJK 必须为 0
 *   node scripts/_en_i18n_guide_probe.mjs --promote <slug>     从 _en-i18n/guides_todo.txt 删除该行
 *
 * 口径：main + .breadcrumb 的可见文本节点（跳过 script/style），精确整串匹配替换，保留首尾空白。
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const GUIDES_DIR = path.join(ROOT, 'guides');
const I18N_GUIDES_DIR = path.join(ROOT, 'i18n', 'guides');
const WORK_DIR = path.join(ROOT, '_en-i18n', 'work', 'guides');
const TODO = path.join(ROOT, '_en-i18n', 'guides_todo.txt');

const CJK = /[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]/;

function loadDict(slug) {
  const map = {};
  const commonPath = path.join(I18N_GUIDES_DIR, '_common.json');
  if (fs.existsSync(commonPath)) {
    try { Object.assign(map, JSON.parse(fs.readFileSync(commonPath, 'utf-8'))); } catch (e) {}
  }
  const dictPath = path.join(I18N_GUIDES_DIR, slug + '.json');
  if (fs.existsSync(dictPath)) {
    try {
      const d = JSON.parse(fs.readFileSync(dictPath, 'utf-8'));
      if (d && d.map) Object.assign(map, d.map);
    } catch (e) {}
  }
  return map;
}

function getRoots(doc) {
  const roots = [];
  const main = doc.querySelector('main'); if (main) roots.push(main);
  const bc = doc.querySelector('.breadcrumb'); if (bc) roots.push(bc);
  const faq = doc.querySelector('.faq'); if (faq) roots.push(faq);
  const rel = doc.querySelector('.related'); if (rel) roots.push(rel);
  const back = doc.querySelector('.back'); if (back) roots.push(back);
  return roots;
}

function collectCJKStrings(doc) {
  const out = [];
  for (const root of getRoots(doc)) {
    const NF = root.ownerDocument.defaultView.NodeFilter;
    const walker = root.ownerDocument.createTreeWalker(root, NF.SHOW_TEXT, null, false);
    let n;
    while ((n = walker.nextNode())) {
      const parent = n.parentNode;
      if (!parent) continue;
      const tag = (parent.nodeName || '').toUpperCase();
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
      const raw = n.nodeValue;
      if (!raw) continue;
      const k = raw.trim();
      if (!k || !CJK.test(k)) continue;
      out.push(k);
    }
  }
  return out;
}

function applyReplacement(doc, map) {
  for (const root of getRoots(doc)) {
    const NF = root.ownerDocument.defaultView.NodeFilter;
    const walker = root.ownerDocument.createTreeWalker(root, NF.SHOW_TEXT, null, false);
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);
    for (const node of nodes) {
      const parent = node.parentNode;
      if (!parent) continue;
      const tag = (parent.nodeName || '').toUpperCase();
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
      const raw = node.nodeValue;
      if (!raw) continue;
      const k = raw.trim();
      if (!k || !CJK.test(k)) continue;
      const en = map[k];
      if (!en || en === k) continue;
      const idx = raw.indexOf(k);
      if (idx < 0) continue;
      node.nodeValue = raw.slice(0, idx) + en + raw.slice(idx + k.length);
    }
  }
  // chrome
  const bcLinks = doc.querySelectorAll('.breadcrumb a');
  if (bcLinks[0] && bcLinks[0].textContent.trim() === '首页') bcLinks[0].textContent = 'Home';
  if (bcLinks[1] && bcLinks[1].textContent.trim() === '使用指南') bcLinks[1].textContent = 'User Guide';
  const rt = doc.querySelector('.related h3'); if (rt) rt.textContent = 'Related Tools';
  const back = doc.querySelector('.back a');
  if (back) back.textContent = back.textContent.replace('→ 打开', '→ Open').replace(/工具$/, 'Tool');
}

function loadGuide(slug) {
  const file = path.join(GUIDES_DIR, slug + '.html');
  if (!fs.existsSync(file)) throw new Error('guide not found: ' + slug);
  const html = fs.readFileSync(file, 'utf-8');
  const dom = new JSDOM(html, { runScripts: undefined });
  return dom.window.document;
}

let mode = null, target = null;
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a === '--extract' || a === '--check' || a === '--promote') { mode = a.slice(2); target = process.argv[++i]; }
}

if (!mode || !target) {
  console.error('usage: --extract|--check|--promote <slug>');
  process.exit(2);
}

if (mode === 'extract') {
  const doc = loadGuide(target);
  const strings = collectCJKStrings(doc);
  const uniq = Array.from(new Set(strings));
  fs.mkdirSync(WORK_DIR, { recursive: true });
  fs.writeFileSync(path.join(WORK_DIR, target + '.json'), JSON.stringify({ slug: target, strings: uniq }, null, 2));
  console.log('extracted', uniq.length, 'unique CJK strings for', target);
  uniq.forEach((s) => console.log('  - ' + s));
} else if (mode === 'check') {
  const doc = loadGuide(target);
  const map = loadDict(target);
  applyReplacement(doc, map);
  const residual = [];
  for (const root of getRoots(doc)) {
    const NF = root.ownerDocument.defaultView.NodeFilter;
    const walker = root.ownerDocument.createTreeWalker(root, NF.SHOW_TEXT, null, false);
    let n;
    while ((n = walker.nextNode())) {
      const parent = n.parentNode;
      if (!parent) continue;
      const tag = (parent.nodeName || '').toUpperCase();
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') continue;
      const raw = n.nodeValue;
      if (!raw) continue;
      const k = raw.trim();
      if (k && CJK.test(k)) residual.push(k);
    }
  }
  const uniq = Array.from(new Set(residual));
  console.log('RESIDUAL_COUNT=' + uniq.length + ' for ' + target);
  uniq.slice(0, 30).forEach((s) => console.log('  RESIDUAL: ' + s));
  process.exit(uniq.length === 0 ? 0 : 1);
} else if (mode === 'promote') {
  if (!fs.existsSync(TODO)) { console.error('todo missing'); process.exit(1); }
  const lines = fs.readFileSync(TODO, 'utf-8').split('\n');
  const before = lines.length;
  const after = lines.filter((l) => {
    const t = l.trim();
    return t !== '' && t !== (target + '.html') && t !== target;
  });
  fs.writeFileSync(TODO, after.join('\n') + (after.length ? '\n' : ''));
  console.log('promoted', target, 'remaining', after.filter((l) => l.trim()).length);
}
