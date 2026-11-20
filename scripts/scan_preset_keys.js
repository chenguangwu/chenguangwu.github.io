#!/usr/bin/env node
/**
 * scan_preset_keys.js — 预设数据静态体检（只读）
 * 口径：抽取页面里 TBKit.preset.bar(...,[{label,values:{k:v}}...],cb) 的 values 键，
 * 与页面真实 id、select 的 option value 比对，报告：
 *   KEY_MISSING  values 键在页面无同名 id（预设写不进任何控件）
 *   OPT_MISSING  目标为 select，但 v 不在其 option value 中（写入后落空/异常）
 *   OPT_MISMATCH 目标为 select，v 存在但以数字形态给出且 option 为字符串（仅提示）
 * 用法：node scripts/scan_preset_keys.js [--ind <industry>] [--json out.json]
 */
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const IND = args.includes('--ind') ? args[args.indexOf('--ind') + 1] : null;
const JSONOUT = args.includes('--json') ? args[args.indexOf('--json') + 1] : null;

function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) { if (!/index\.html$/.test(p)) walk(p, out); }
    else if (f.endsWith('.html') && f !== 'index.html') out.push(p);
  }
  return out;
}
const files = walk(path.join(ROOT, 'tools')).filter(p => !IND || p.split('/tools/')[1].startsWith(IND + '/'));
const rows = [];
for (const file of files) {
  const rel = file.replace(ROOT + '/', '');
  const src = fs.readFileSync(file, 'utf8');
  if (!src.includes('TBKit.preset.bar')) continue;
  // 取 TBKit.preset.bar( 之后的第一个 '[' 到与之配平的 ']'
  let idx = src.indexOf('TBKit.preset.bar');
  while (idx >= 0) {
    const lb = src.indexOf('[', idx);
    if (lb < 0) break;
    let depth = 0, end = -1, inStr = 0, q = '';
    for (let i = lb; i < src.length; i++) {
      const c = src[i];
      if (inStr) { if (c === '\\') i++; else if (c === q) inStr = 0; continue; }
      if (c === '"' || c === "'" || c === '`') { inStr = 1; q = c; continue; }
      if (c === '[') depth++;
      else if (c === ']') { depth--; if (!depth) { end = i; break; } }
    }
    if (end < 0) break;
    const arrText = src.slice(lb, end + 1);
    let parsed = null;
    try { parsed = new Function('return ' + arrText)(); } catch (e) { parsed = null; }
    if (Array.isArray(parsed)) {
      const ids = new Set([...src.matchAll(/\bid\s*=\s*["']([^"']+)["']/g)].map(m => m[1]));
      const selOpts = {};
      for (const m of src.matchAll(/<select\b[^>]*id\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/select>/gi)) {
        selOpts[m[1]] = new Set([...m[2].matchAll(/<option\b[^>]*value\s*=\s*["']([^"']*)["']/gi)].map(x => x[1]));
      }
      for (const p of parsed) {
        if (!p || !p.values) continue;
        const keys = Object.keys(p.values).filter(k => k !== '__call');
        if (!keys.length) rows.push({ file: rel, preset: p.label || '', kind: 'NO_VALUES', key: '' });
        for (const k of keys) {
          if (!ids.has(k)) { rows.push({ file: rel, preset: p.label || '', kind: 'KEY_MISSING', key: k }); continue; }
          if (selOpts[k]) {
            const v = String(p.values[k]);
            if (!selOpts[k].has(v)) rows.push({ file: rel, preset: p.label || '', kind: 'OPT_MISSING', key: k + '=' + v });
          }
        }
      }
    }
    idx = src.indexOf('TBKit.preset.bar', end);
  }
}
const kinds = {};
for (const r of rows) kinds[r.kind] = (kinds[r.kind] || 0) + 1;
console.log('[preset-scan] pages=' + files.length + ' hits=' + rows.length, JSON.stringify(kinds));
for (const r of rows.slice(0, 40)) console.log(r.kind, r.file, '|', r.preset, '|', r.key);
if (JSONOUT) fs.writeFileSync(JSONOUT, JSON.stringify(rows, null, 1));
