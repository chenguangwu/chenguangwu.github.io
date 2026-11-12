// 第269批 JSDOM 验证：IT-N270 .gitignore 模板安全规则（.env 承诺落地）
// 用法: node scripts/_verify_it_batch269.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/gitignore-generator.html` : 'tools/it/gitignore-generator.html';
const html = fs.readFileSync(page(), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/gitignore.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {}, copyText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { list: () => [], last: () => null, record() {}, mount() {} },
    };
    w.i18nText = (zh) => zh;
  },
});
const w = dom.window, d = w.document;
// 页面 calcTool 用 escH(createElement.textContent) 产生 <pre>，JSDOM 真机可正常渲染，直接读 innerHTML
const stacks = ['py', 'node', 'go', 'rust', 'java', 'dotnet', 'c', 'ide'];
const ids = { py: 'top_py', node: 'top_node', go: 'top_go', rust: 'top_rust', java: 'top_java', dotnet: 'top_dotnet', c: 'top_c', ide: 'top_ide' };

function selectOnly(stack) {
  for (const s of stacks) { const e = d.getElementById(ids[s]); if (e) e.checked = (s === stack); }
  w.calcTool();
}
function resultText() { return d.getElementById('result').textContent || ''; }

// ---------- 每个模板都应含 .env 三件套 ----------
let allHave = true, missing = [];
for (const s of stacks) {
  selectOnly(s);
  const t = resultText();
  const ok = t.includes('.env') && t.includes('.env.*') && t.includes('!.env.example');
  if (!ok) { allHave = false; missing.push(s); }
}
check('N270 8 个模板全部含 .env/.env.*/!.env.example', allHave, 'missing=' + missing.join(','));

// ---------- Node 模板具体规则（示例承诺） ----------
selectOnly('node');
const nodeOut = resultText();
check('N270 Node 输出含 node_modules/', nodeOut.includes('node_modules/'));
check('N270 Node 输出含 dist/', nodeOut.includes('dist/'));
check('N270 Node 输出含 .env', nodeOut.includes('.env'));
check('N270 Node 保留 .env.example 样例（!.env.example 取反）', nodeOut.includes('!.env.example'));

// ---------- 全 29+ 条规则汇总含 .env ----------
for (const s of stacks) { const e = d.getElementById(ids[s]); if (e) e.checked = true; }
w.calcTool();
const allOut = resultText();
check('N270 全选输出含 .env 规则', allOut.includes('.env') && allOut.includes('.env.*'));
check('N270 全选输出仍含各栈代表规则', allOut.includes('__pycache__/') && allOut.includes('target/') && allOut.includes('node_modules/'));

// ---------- 承诺文案与输出一致 ----------
const bodyText = d.body.textContent || '';
check('N270 深度解析示例声称输出 .env', bodyText.includes('选 Node') && bodyText.includes('.env'), 'claim present');
check('N270 示例承诺与实际输出一致（不再落空）', /选 Node[\s\S]{0,80}\.env/.test(bodyText) && nodeOut.includes('.env'));

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
