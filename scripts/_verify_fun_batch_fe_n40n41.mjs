// FE-N40 + FE-N41 运行期两态锁（kick-height.html）
// N40: level 下拉原先不参与任何计算 → 现在应影响评级（初学放宽/专业更严）
// N41: 「✓ 出色」原用原始 ratio>=100 触发，与「良好」评级并存 → 改为仅当 grade==='优秀' 时显示
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import process from 'process';
import fs from 'fs';

const file = 'tools/martial/kick-height.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');

function load() {
  return new JSDOM(html, {
    runScripts: 'dangerously',
    beforeParse(w) {
      w.TBKit = { util: { isEn: () => false }, chart: { refBar() {} } };
    },
  });
}

function calcWith(dom, { h, kh, kt, lvl, ll = 0 }) {
  const d = dom.window.document;
  d.getElementById('height').value = String(h);
  d.getElementById('kickHeight').value = String(kh);
  d.getElementById('kickType').value = kt;
  d.getElementById('level').value = String(lvl);
  if (ll) d.getElementById('legLen').value = String(ll);
  dom.window.calc();
  return d.getElementById('result').innerHTML;
}

function gradeOf(s) { const m = s.match(/<span class="grade-tag[^"]*">([^<]+)<\/span>/); return m ? m[1] : '(none)'; }

let pass = true;
const notes = [];

// ---- N40: level 影响评级 ----
{
  const cur = load();
  const gL2 = gradeOf(calcWith(cur, { h: 170, kh: 170, kt: 'front', lvl: 2 })); // 高级
  const gL3 = gradeOf(calcWith(cur, { h: 170, kh: 170, kt: 'front', lvl: 3 })); // 专业
  const n40 = gL2 !== gL3; // 同一身高/踢高，仅切换训练水平 → 评级应改变
  notes.push(`[N40] h=170 kh=170 front | 高级=${gL2} 专业=${gL3} → ${n40 ? 'PASS(水平参与评级)' : 'FAIL(水平无效)'}`);
  pass = pass && n40;
}

// ---- N41: 「✓ 出色」不再与「良好」并存 ----
{
  const cur = load();
  const s = calcWith(cur, { h: 170, kh: 173, kt: 'high', lvl: 2 }); // ratio=101.8 但高踢修正比=96.9 → 良好
  const hasExcellent = s.includes('✓ 出色');
  const g = gradeOf(s);
  const n41 = !hasExcellent && g === '良好';
  notes.push(`[N41] h=170 kh=173 high | grade=${g} ✓出色=${hasExcellent} → ${n41 ? 'PASS(无矛盾)' : 'FAIL(出色与良好并存)'}`);
  pass = pass && n41;
}

console.log(notes.join('\n'));
console.log(pass ? 'ALL PASS' : 'FAIL');
process.exit(pass ? 0 : 1);
