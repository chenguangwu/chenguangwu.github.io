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
      w.TBKit = { util: { isEn: () => false }, chart: { refBar(_host, cfg) { w.lastBar = cfg; } } };
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

// 评级和标尺必须使用同一阈值，精确覆盖每个级别的边界两侧。
{
  const cur = load();
  const levels = [5, 3, 0, -3];
  const names = ['优秀', '良好', '及格', '一般', '较弱'];
  let errors = [];
  for (let lvl = 0; lvl < levels.length; lvl++) {
    for (const factor of [['front', 1], ['side', 0.95], ['round', 0.92], ['back', 0.88], ['high', 1.05]]) {
      for (const threshold of [50, 70, 85, 100]) {
        for (const delta of [-0.01, 0, 0.01]) {
          const target = threshold - levels[lvl] + delta;
          const s = calcWith(cur, { h: 200, kh: target * 2 * factor[1], kt: factor[0], lvl });
          const bar = cur.window.lastBar;
          const adjusted = target;
          const expected = names[[100, 85, 70, 50].findIndex(v => adjusted >= v - levels[lvl] - 1e-10)];
          const expectedGrade = expected || '较弱';
          const actual = gradeOf(s);
          const band = bar?.bands.find(b => bar.value >= (b.lo ?? -Infinity) && bar.value < (b.hi ?? Infinity));
          if (Math.abs(delta) > 0 && (actual !== expectedGrade || band?.label.zh !== actual)) errors.push(`${lvl}/${factor[0]}/${target}: ${actual}/${band?.label.zh} != ${expectedGrade}`);
          if (Math.abs(delta) < 1e-10 && band?.label.zh !== actual) errors.push(`边界 ${lvl}/${factor[0]}/${target}: ${actual}/${band?.label.zh}`);
        }
      }
    }
  }
  notes.push(`[阈值] ${errors.length ? 'FAIL ' + errors.slice(0, 5).join('; ') : 'PASS 各水平、类型及边界的标尺与评级一致'}`);
  pass = pass && errors.length === 0;
  cur.window.close();
}
{
  const cur = load();
  const below = calcWith(cur, { h: 170, kh: 165, kt: 'front', lvl: 0 });
  const at = calcWith(cur, { h: 170, kh: 170, kt: 'front', lvl: 3 });
  const ok = gradeOf(below) === '优秀' && !/过头顶|头顶以上/.test(below) && /低于身高/.test(below) && /达到身高/.test(at);
  notes.push(`[实际高度] ${ok ? 'PASS' : 'FAIL 初学优秀不得误称超过头顶，等高应如实说明'}`);
  pass = pass && ok;
  cur.window.close();
}
{
  const source = JSON.parse(fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'));
  const dict = JSON.parse(fs.readFileSync('i18n/tools/en/martial/kick-height.json', 'utf8')).map;
  const dom = load();
  const example = dom.window.document.querySelector('.dd-ex-body').textContent.trim();
  const sourceText = JSON.stringify(source);
  const en = dict[example];
  const table = dom.window.document.querySelector('.card table').textContent;
  const formula = dom.window.document.querySelector('.formula-eq').textContent;
  const ok = sourceText.includes(example.replaceAll('\n', '\\n')) && /初学/.test(example) && /优秀/.test(example) && /低于身高/.test(example) && en && /beginner/i.test(en) && /excellent/i.test(en) && /below.*height/i.test(en) && /修正比/.test(table) && /训练水平/.test(table) && /初学/.test(formula) && /专业/.test(formula);
  notes.push(`[文案及英文] ${ok ? 'PASS' : 'FAIL 表格、公式或算例的源数据/翻译仍不一致'}`);
  pass = pass && !!ok;
  dom.window.close();
}
console.log(notes.join('\n'));
console.log(pass ? 'ALL PASS' : 'FAIL');
process.exit(pass ? 0 : 1);
