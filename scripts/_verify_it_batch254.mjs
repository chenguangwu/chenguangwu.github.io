// 第254批 JSDOM 验证：IT-N143 往返（已修证据）/ N144 补位剥离 / N145 预设密钥与状态提示
// 用法: node scripts/_verify_it_batch254.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = () => OLD ? `${OLD}/tools/it/adfgvx-cipher.html` : 'tools/it/adfgvx-cipher.html';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const html = fs.readFileSync(page(), 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://x.com/adfgvx.html', beforeParse(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {} };
  w.TBKit = { util: { isEn: () => false, exportTable() {}, diffBox() {} }, chart: { bar() {}, line() {} },
    matrix: { table() {} }, preset: { bar() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} } };
}});
const w = dom.window, d = w.document;
function roundtrip(key, trans, txt) {
  d.getElementById('key').value = key;
  d.getElementById('transKey').value = trans;
  d.getElementById('input').value = txt;
  w.enc(); const cipher = d.getElementById('output').value;
  d.getElementById('input').value = cipher;
  w.dec(); return { cipher, back: d.getElementById('output').value };
}

// N143（已修）：CIPHER / FRANCE 非对合密钥往返
let r = roundtrip('', 'CIPHER', 'ATTACKATDAWN');
check('N143 CIPHER 往返（去标记后对齐）', r.back.replace(/~P\d+$/, '') === 'ATTACKATDAWN', `back=${r.back}`);
r = roundtrip('', 'FRANCE', 'HELLO');
check('N143 FRANCE 往返', r.back.replace(/~P\d+$/, '') === 'HELLO', `back=${r.back}`);

// N144：补位剥离
r = roundtrip('', 'LEMON', 'HIJ');
check('N144 HIJ 补位剥离（无多余 YY）', r.back.replace(/~P\d+$/, '') === 'HIJ', `cipher=${r.cipher} back=${r.back}`);
r = roundtrip('', 'FRANCE', 'HELLO');
check('N144 HELLO 补位剥离（无多余 Y）', r.back.replace(/~P\d+$/, '') === 'HELLO', `back=${r.back}`);
r = roundtrip('', 'LEMON', 'A');
check('N144 单字符补位剥离', r.back.replace(/~P\d+$/, '') === 'A', `back=${r.back}`);
check('N144 密文含补位标记', /~P\d+$/.test(roundtrip('', 'LEMON', 'HIJ').cipher), 'marker');

// N145：预设 36 字符 key + 状态提示
check('N145 预设均为 36 字符置换',
  /key':'HCJ8R3OYK14B9PD7U2TE5IVFZASXM06LQGWN/.test(html) &&
  /key':'DLH4A39NQ2PE8W76VI01CXOTZBYUKJ5SMFRG/.test(html) &&
  /key':'J5PYR86C2ELF7D1S3H4NIUXTAKQOG0VMB9ZW/.test(html) &&
  !/key':'KEY'/.test(html) && !/key':'SECRET'/.test(html) && !/key':'BREAK'/.test(html), 'presets');
d.getElementById('key').value = '';
w.renderGrid();
const ks1 = d.getElementById('keyStatus');
const s1 = ks1 ? ks1.textContent : '(no keyStatus)';
check('N145 非法长度提示回退默认', /回退默认方阵|Using default/.test(s1), s1);
d.getElementById('key').value = 'HCJ8R3OYK14B9PD7U2TE5IVFZASXM06LQGWN';
w.renderGrid();
const ks2 = d.getElementById('keyStatus');
const s2 = ks2 ? ks2.textContent : '(no keyStatus)';
check('N145 合法长度提示已生效', /已生效|active/.test(s2), s2);

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
