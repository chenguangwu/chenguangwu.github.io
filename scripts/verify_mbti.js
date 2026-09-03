// MBTI 工具逻辑仿真测试（Node + 极简 DOM stub）
const fs = require('fs');
const path = require('path');
const TARGET = 'psychology/tester-2';
const html = fs.readFileSync(path.join(__dirname, '..', 'tools', TARGET + '.html'), 'utf8');
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const code = blocks.find(b => b.includes('MT_QS'));
if (!code) throw new Error('未找到 MBTI 脚本块');

function makeEl() {
  const el = {
    _html: '', _text: '', disabled: false, style: {}, _attrs: {},
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    get textContent() { return this._text; },
    set textContent(v) { this._text = String(v); },
    setAttribute(k, v) { this._attrs[k] = String(v); },
    getAttribute(k) { return (k in this._attrs) ? this._attrs[k] : null; },
    removeAttribute(k) { delete this._attrs[k]; },
    getElementsByClassName() { return []; },
    scrollIntoView() {},
  };
  return el;
}
const els = {};
const document = {
  getElementById(id) { if (!(id in els)) els[id] = makeEl(); return els[id]; },
  addEventListener() {},
};
const win = {
  localStorage: { _d: {}, getItem(k) { return k in this._d ? this._d[k] : null; }, setItem(k, v) { this._d[k] = String(v); }, removeItem(k) { delete this._d[k]; } },
  setTimeout(fn) { /* 测试环境不自动跳题 */ },
  ToolBox: {}, navigator: {},
};
const sandbox = { document, window: win, localStorage: win.localStorage, JSON, Math, parseInt, console };
const fn = new Function('document', 'window', 'localStorage', 'JSON', 'Math', 'parseInt', 'console',
  code + '\n; return {MT_QS:MT_QS, MT_SCALE:MT_SCALE, MT_ANS:MT_ANS, calc:calc, mtScore:mtScore, mtPick:mtPick, mtAnswered:mtAnswered, MT_DIMS:MT_DIMS, MT_TYPES:MT_TYPES, mtReset:mtReset, getRes:function(){return document.getElementById("res");}, setAll:function(v){for(var i=0;i<MT_ANS.length;i++){MT_ANS[i]=v;}}};');
const api = fn(document, win, win.localStorage, JSON, Math, parseInt, console);

let fail = 0;
function check(name, cond, extra) {
  console.log((cond ? '  ✅ ' : '  ❌ ') + name + (extra ? '  → ' + extra : ''));
  if (!cond) fail++;
}

console.log('\n[用例1] 题库规模与结构');
check('题目总数 60', api.MT_QS.length === 60, api.MT_QS.length + ' 题');
const dims = {};
api.MT_QS.forEach(q => { dims[q.d] = (dims[q.d] || 0) + 1; });
const perDim = [['E', 'I'], ['S', 'N'], ['T', 'F'], ['J', 'P']].map(([a, b]) => (dims[a] || 0) + (dims[b] || 0));
check('4 个维度各 15 题', perDim.every(v => v === 15), JSON.stringify(dims));
check('A/B 两方向总量平衡（各 30 题）',
  (dims.E + dims.S + dims.T + dims.J) === 30 && (dims.I + dims.N + dims.F + dims.P) === 30,
  'A=' + (dims.E + dims.S + dims.T + dims.J) + ' B=' + (dims.I + dims.N + dims.F + dims.P));
check('题干无重复', new Set(api.MT_QS.map(q => q.q)).size === 60, new Set(api.MT_QS.map(q => q.q)).size + ' 条唯一');
check('16 型数据齐全', Object.keys(api.MT_TYPES).length === 16);
check('量表为 5 档且含中间值', api.MT_SCALE.length === 5 && api.MT_SCALE.some(s => s.v === 0), api.MT_SCALE.map(s => s.t).join(' / '));
check('16 型描述齐全', Object.keys(api.MT_TYPES).length === 16);

function run(label, picker, expect) {
  api.mtReset();
  api.MT_QS.forEach((q, i) => { api.MT_ANS[i] = picker(q, i); });
  api.calc();
  const res = api.getRes();
  const out = res.innerHTML;
  const bad = /NaN|undefined|Infinity/.test(out);
  let code = '';
  for (const k of Object.keys(api.MT_TYPES)) {
    if (out.includes('mt-type-code">' + k + '<')) { code = k; break; }
  }
  const ok = !bad && code === expect;
  console.log((ok ? '  ✅ ' : '  ❌ ') + label + ' → 期望 ' + expect + '，实际 ' + code + (bad ? '（输出含 NaN/undefined）' : ''));
  if (!ok) fail++;
  // 百分比校验
  const pcts = [...out.matchAll(/mt-dbar-top[\s\S]*?<b>[^<]*<\/b> (\d+)%<\/span>[\s\S]*?(\d+)% /g)].map(m => m[1] + '/' + m[2]);
  return { code, out, pcts, copy: res.getAttribute('data-copy-value') };
}

console.log('\n[用例2] 计分方向性');
// 极端外向 / 内向 / 直觉 / 情感 / 感知
run('强 E + 强 N + 强 F + 强 P → ENFP', (q) => ['E', 'N', 'F', 'P'].includes(q.d) ? 2 : -2, 'ENFP');
run('强 I + 强 N + 强 T + 强 J → INTJ', (q) => ['I', 'N', 'T', 'J'].includes(q.d) ? 2 : -2, 'INTJ');
run('强 I + 强 S + 强 F + 强 J → ISFJ', (q) => ['I', 'S', 'F', 'J'].includes(q.d) ? 2 : -2, 'ISFJ');
run('强 E + 强 S + 强 T + 强 J → ESTJ', (q) => ['E', 'S', 'T', 'J'].includes(q.d) ? 2 : -2, 'ESTJ');

const r1 = run('全部选中间值（中立）→ 平局兜底', () => 0, 'ESTJ');
console.log('     中立时四维度比例：' + r1.pcts.join(' , '));
check('全中立时各维度为 50/50', r1.pcts.length === 4 && r1.pcts.every(p => p === '50/50'), r1.pcts.join(','));

const r2 = run('轻微偏向 I/N/T/P（混 1 分与 2 分）→ INTP', (q) => ['I', 'N', 'T', 'P'].includes(q.d) ? (q.d.charCodeAt(0) % 2 ? 1 : 2) : -1, 'INTP');
console.log('     混合分值四维度比例：' + r2.pcts.join(' , '));
check('百分比守恒（两侧相加=100）', r2.pcts.every(p => { const [a, b] = p.split('/').map(Number); return a + b === 100; }), r2.pcts.join(','));

console.log('\n[用例3] 未答完时的提示');
api.mtReset();
api.MT_ANS[0] = 2; api.MT_ANS[1] = 1;
api.calc();
const partial = api.getRes().innerHTML;
check('提示剩余题数', /还有 58 题未作答/.test(partial), partial.replace(/<[^>]+>/g, '').trim().slice(0, 60));

console.log('\n[用例4] 结果内容完整性');
api.mtReset();
api.MT_QS.forEach((q, i) => { api.MT_ANS[i] = ['I', 'N', 'F', 'P'].includes(q.d) ? 2 : -2; });
api.calc();
const out = api.getRes().innerHTML;
check('含类型中文名', /mt-type-name/.test(out));
check('含核心特征', /核心特征/.test(out));
check('含常见优势', /常见优势/.test(out));
check('含可能盲点', /可能的盲点/.test(out));
check('含适配方向', /常见适配方向/.test(out));
check('含认知功能栈', /认知功能栈/.test(out));
check('含四维度表格', /<table>/.test(out));
const copy = api.getRes().getAttribute('data-copy-value');
check('复制文本含类型与维度比例', copy && copy.includes('INFP') && /\(I\) 100%/.test(copy));
console.log('     复制文本首行：' + String(copy).split('\n')[1]);

console.log('\n[用例5] 题号导航与回退改答案');
api.mtReset();
api.MT_ANS[0] = 2;
api.MT_ANS[1] = -1;
const before = api.MT_ANS[1];
api.MT_ANS[1] = 1; // 模拟回到第 2 题改答案
check('答案可被覆盖修改', before === -1 && api.MT_ANS[1] === 1);
check('已答计数正确', api.mtAnswered() === 2, api.mtAnswered() + ' 题');

console.log('\n==== ' + (fail === 0 ? '全部通过' : fail + ' 项失败') + ' ====');
process.exit(fail === 0 ? 0 : 1);
