// 第247批探测 · IT-N101/N102/N103（http-status）
//  N101 补齐常用标准码（203/451/428/431 等），meta 口径改「常用」
//  N102 401 描述统一为「未认证」
//  N103 无结果时空表格保持隐藏（复核已修）
// 用法：node scripts/_verify_it_batch247.mjs [旧页目录]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok]);
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail ? ' | ' + String(detail).slice(0, 220) : ''));
}
function stub(w) {
  w.alert = () => {};
  w.ToolBox = { showToast() {}, copyText() {}, toggleToolTheme() {}, escHtml: s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
    history: { list() { return []; }, last() { return null; }, record() {}, mount() {}, clear() {} }
  };
}
function makeDom(file) {
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/' + file.split('/').pop(),
    beforeParse: stub, pretendToBeVisual: true
  });
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch (e) {}
  return dom;
}
const page = () => OLD_DIR ? OLD_DIR + '/http-status.html' : 'tools/it/http-status.html';

// ══════════════ N101 状态码补齐 + meta 口径 ══════════════
{
  const dom = makeDom(page());
  const w = dom.window, d = w.document;
  const codes = w.eval('statusCodes.map(function(s){return s.code;})');
  const need = [103,203,205,300,303,305,411,412,414,416,417,418,421,425,426,428,431,451,506,507,508,510];
  const missing = need.filter(c => !codes.includes(c));
  check('N101 补齐 22 个常用标准码', missing.length === 0, missing.length ? 'missing=' + missing.join(',') : 'all present');
  check('N101 数据规模 >= 50 条', codes.length >= 50, 'count=' + codes.length);
  // 搜索 203/451 能命中
  const input = d.getElementById('search');
  input.value = '451';
  w.filterStatus();
  const listHtml = d.getElementById('statusList').innerHTML;
  check('N101 搜索 451 有结果', /451/.test(listHtml) && /无匹配|No matching/.test(listHtml) === false, listHtml.slice(0, 120));
  // meta 口径
  const html = fs.readFileSync(page(),'utf8');
  check('N101 meta 改「常用标准状态码」', /常用标准状态码/.test(html) && !/全部标准状态码/.test(html), 'checked');
  const itJsonPath = OLD_DIR ? OLD_DIR + '/it.json' : 'i18n/tools/it.json';
  const itJson = fs.readFileSync(itJsonPath,'utf8');
  check('N101 it.json SEO 源同步', /HTTP 状态码速查表汇总 1xx~5xx 常用标准状态码/.test(itJson), 'checked');
  // 新增状态码的中文说明必须有英文映射，避免英文态新增 CJK 残留。
  const enMap = JSON.parse(fs.readFileSync(OLD_DIR ? OLD_DIR + '/http-status.en.json' : 'i18n/tools/en/it/http-status.json','utf8')).map;
  const addedPairs = w.eval("statusCodes.filter(function(s){return [" + need.join(',') + "].indexOf(s.code)>=0;}).map(function(s){return [s.desc,s.detail];})");
  const untranslated = [].concat.apply([], addedPairs).filter(s => /[\u4e00-\u9fff]/.test(s) && !enMap[s]);
  check('N101 新增状态码英文映射齐全', untranslated.length === 0, untranslated.length ? untranslated.join(' | ') : 'all mapped');
}

// ══════════════ N102 401 描述统一 ══════════════
{
  const dom = makeDom(page());
  const s401 = dom.window.eval("statusCodes.find(function(s){return s.code===401;})");
  check('N102 401 desc 为「未认证」', s401 && s401.desc === '未认证', s401 ? s401.desc : 'missing');
  check('N102 401 detail 含 403 区分说明', s401 && /403/.test(s401.detail), s401 ? s401.detail.slice(0, 80) : '');
  const enMap = JSON.parse(fs.readFileSync(OLD_DIR ? OLD_DIR + '/http-status.en.json' : 'i18n/tools/en/it/http-status.json','utf8')).map;
  check('N102 401 新口径英文映射', enMap['未认证'] === 'Not authenticated', enMap['未认证'] || 'missing');
}

// ══════════════ N103 空结果表格隐藏（复核） ══════════════
{
  const dom = makeDom(page());
  const w = dom.window, d = w.document;
  const input = d.getElementById('search');
  input.value = 'zzz';
  w.filterStatus();
  const t = d.getElementById('httpTable');
  check('N103 无结果时表格保持隐藏', t && t.style.display === 'none', t ? 'display=' + t.style.display : 'no table');
  check('N103 无结果时不残留表头', t && (!t.querySelector('thead') || t.querySelector('thead').innerHTML.trim() === ''), t ? 'thead=' + (t.querySelector('thead') ? t.querySelector('thead').innerHTML.trim() : 'none') : 'no table');
}

const pass = checks.filter(c => c[1]).length;
console.log('\nRESULT ' + pass + '/' + checks.length + (OLD_DIR ? ' [OLD ' + OLD_DIR + ']' : ' [NEW]'));
if (pass !== checks.length) process.exitCode = 1;
