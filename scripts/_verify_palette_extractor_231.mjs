// 证据脚本：palette-extractor D-N231/D-N232 真假判别
// 从页面真源码提取 medianCut 复算，验证「截簇后占比合计」与「单像素空簇」两条修复
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PAGE = path.join(ROOT, 'tools/design/palette-extractor.html');
const src = fs.readFileSync(PAGE, 'utf8');

let pass = 0, fail = 0;
function ok(cond, msg) {
  if (cond) { pass++; console.log('PASS ' + msg); }
  else { fail++; console.log('FAIL ' + msg); }
}

// 提取页面真源码 medianCut（到函数结束的两个空格缩进右括号）
const mm = src.match(/function medianCut\(pixels, depth, maxDepth\)\s*\{[\s\S]*?\n  \}/);
ok(!!mm, '从页面源码提取 medianCut 函数');
if (!mm) process.exit(1);
const medianCut = new Function(mm[0] + '; return medianCut;')();

// 构造 8 色 × 2 像素 = 16 像素，count=5 → maxDepth=3 → 切 8 簇再截到 5 簇
const pixels = [];
for (let c = 0; c < 8; c++) {
  for (let k = 0; k < 2; k++) pixels.push([c * 32, c * 16, 255 - c * 32]);
}
const count = 5;
const maxDepth = Math.ceil(Math.log2(count));
const raw = medianCut(pixels.slice(), 0, maxDepth)
  .sort((a, b) => b.count - a.count).slice(0, count);
const keptTotal = raw.reduce((s, c) => s + c.count, 0);
const totalPixels = pixels.length;

// 旧口径：截簇后仍除以全部像素；新口径：按保留簇归一
const sumOld = raw.reduce((s, c) => s + c.count / totalPixels * 100, 0);
const sumNew = raw.reduce((s, c) => s + c.count / keptTotal * 100, 0);
ok(keptTotal < totalPixels, `截簇确实丢像素：保留 ${keptTotal}/${totalPixels} 像素`);
ok(sumOld < 99, `旧口径占比合计 ${sumOld.toFixed(1)}% < 100%（D-N231 缺陷成立）`);
ok(Math.abs(sumNew - 100) < 0.01, `新口径占比合计 ${sumNew.toFixed(1)}% = 100%`);

// D-N232：单像素簇继续切会 mid=0 → 空簇 n=0 → NaN → rgbToHex 得 #000000 0.0%
const single = medianCut([[10, 20, 30]], 0, 3);
const hasNaN = single.some(c => !isFinite(c.r) || !isFinite(c.g) || !isFinite(c.b) || c.count === 0);
ok(!hasNaN && single.length === 1 && single[0].count === 1,
  '单像素簇直接聚合，无 NaN 空簇（D-N232 缺陷已消解）');

// 源码修复特征（判别核心：旧源码此处必然 FAIL）
ok(/var keptTotal\s*=/.test(src) && /c\.count \/ keptTotal/.test(src),
  '源码已按保留簇归一 percent');
ok(/pixels\.length === 0\) return \[\]/.test(src) && /depth >= maxDepth \|\| pixels\.length === 1/.test(src),
  '源码已防单像素簇递归切出空簇');

console.log(`\n合计 ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
