#!/usr/bin/env node
/**
 * 794 复核失败重做：冷敷计时页的部位按钮必须带 data-part，历史回放才能恢复高亮。
 *
 * 规则：每个 `onclick="selectPart('<key>',this)"` 的按钮，同标签内必须有 data-part="<key>"。
 * 用法：node scripts/verify_cold_part_attrs.js
 */
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'tools', 'clinical-nursing', 'cold-compress-timer.html');
const html = fs.readFileSync(file, 'utf8');
const PARTS = ['joint', 'muscle', 'face', 'limb', 'postop'];

let pass = 0;
const fails = [];
for (const p of PARTS) {
  const re = new RegExp(`<button[^>]*onclick="selectPart\\('${p}',this\\)"[^>]*>`);
  const m = html.match(re);
  if (!m) {
    fails.push(`${p}: 未找到按钮`);
    console.log(`FAIL ${p}: 未找到 selectPart('${p}',this) 按钮`);
    continue;
  }
  if (m[0].indexOf(`data-part="${p}"`) === -1) {
    fails.push(`${p}: 缺 data-part`);
    console.log(`FAIL ${p}: 按钮缺 data-part="${p}"  →  ${m[0]}`);
    continue;
  }
  pass++;
  console.log(`PASS ${p}: data-part 与 selectPart 键一致`);
}

console.log(`\n冷敷部位按钮 data-part：${pass}/${PARTS.length}`);
if (fails.length) process.exit(1);
