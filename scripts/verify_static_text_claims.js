#!/usr/bin/env node
/**
 * 静态文案与实现口径一致性检查（无头门禁只跑 JS，覆盖不到纯说明文字）。
 *
 * 用法：node scripts/verify_static_text_claims.js
 * 新增规则：{ file, include: [...], exclude: [...] }
 */
const fs = require('fs');
const path = require('path');

const CHECKS = [
  {
    name: 'PCR Ct 判读说明与实现半开区间一致（785 复核失败重做）',
    file: 'tools/clinical-lab/pcr-ct-interpretation.html',
    include: ['30≤Ct&lt;38', '38≤Ct&lt;cutoff', '未填 Ct：视为未完成检测'],
    exclude: ['Ct 30–37', '无 Ct：阴性'],
  },
  {
    name: '稀释比例标签口径对照与算例一致（532 复核失败重做）',
    file: 'tools/cleaning/dilution-ratio.html',
    include: ['产品标签的「1:X」和本页的「1:N」是同一种口径吗？', '原液约 9.9 mL', '1/101'],
    exclude: ['原液约 10 mL、加水约 990 mL'],
  },
];

let pass = 0;
const fails = [];
for (const c of CHECKS) {
  const abs = path.join(__dirname, '..', c.file);
  const html = fs.readFileSync(abs, 'utf8');
  const missing = (c.include || []).filter((s) => html.indexOf(s) === -1);
  const stale = (c.exclude || []).filter((s) => html.indexOf(s) !== -1);
  if (missing.length || stale.length) {
    fails.push(c.name);
    console.log(`FAIL ${c.name}`);
    if (missing.length) console.log(`  缺少：${missing.join(' / ')}`);
    if (stale.length) console.log(`  残留旧文案：${stale.join(' / ')}`);
  } else {
    pass++;
    console.log(`PASS ${c.name}`);
  }
}

console.log(`\n静态文案一致性：${pass}/${CHECKS.length}`);
if (fails.length) process.exit(1);
