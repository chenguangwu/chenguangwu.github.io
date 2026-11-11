// 第228批 · IT-N217~N221（markdown-table 1 条 + wifi-qr 4 条，JSDOM 真机）
//  N217 md-table 行列含逗号被拆列（真修：CSV 双引号包裹）
//  N218 WiFi 字符串未按 ZXing 转义（进批探测：已修，补证据）
//  N219 隐藏网络字段顺序/结尾分号（进批探测：已修，补证据）
//  N220 名为二维码生成器却只产字符串（真修：改名 WiFi 配网字符串生成器，URL 不变）
//  N221 两处 </div 缺 >（进批探测：已修，补证据）
// 用法：node scripts/_verify_it_batch228.mjs [旧页目录；提供时对两页做差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 150) : '')); }

function makeDom(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  let history = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {} };
      w.i18nText = (k, f) => (k == null || k === '') ? (f != null ? f : '') : (f || String(k));
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return history.slice(); }, last() { return history.length ? history[history.length - 1] : null; },
          record(r) { history.push(r); }, mount() {}, clear() { history = []; } }
      };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html };
}

const MDT = OLD_DIR ? OLD_DIR + '/mdtable.orig.html' : 'tools/it/markdown-table-generator.html';
const WIFI = OLD_DIR ? OLD_DIR + '/wifi.orig.html' : 'tools/it/wifi-qr-generator.html';

// ══════════════ N217 md-table CSV 引号解析 ══════════════
const M = makeDom(MDT), mw = M.w, md = M.d;
function parseRow(line) { return mw.eval('parseRow(' + JSON.stringify(line) + ')'); }
check('N217 "a,b",c 解析为 2 列 ["a,b","c"]', JSON.stringify(parseRow('"a,b",c')) === '["a,b","c"]', JSON.stringify(parseRow('"a,b",c')));
check('N217 普通逗号分隔仍是 3 列', JSON.stringify(parseRow('a,b,c')) === '["a","b","c"]', JSON.stringify(parseRow('a,b,c')));
check('N217 引号内 "" 还原为字面引号', JSON.stringify(parseRow('"a""b",c')) === '["a\\"b","c"]', JSON.stringify(parseRow('"a""b",c')));
check('N217 未闭合引号不丢字符', JSON.stringify(parseRow('"a,b')).includes('a,b'), JSON.stringify(parseRow('"a,b')));
// 端到端：含逗号单元格产出 1 列（竖线不增加）
md.getElementById('cols').value = '2'; md.getElementById('rows').value = '1'; md.getElementById('align').value = 'left';
md.getElementById('headerLine').value = '"a,b",c';
md.getElementById('bodyLine').value = '"x,y",z';
mw.renderPreview();
const mdOut = md.getElementById('output').value;
check('N217 端到端：含逗号单元格不被拆成额外列', /a,b/.test(mdOut) && /\| a,b \| c \|/.test(mdOut), JSON.stringify(mdOut.split('\n')[0]));

// ══════════════ wifi N218/N219/N220/N221 ══════════════
const W = makeDom(WIFI), ww = W.w, wd = W.d;
function wifiCalc(ssid, pass, enc, hidden) {
  wd.getElementById('ssid').value = ssid;
  wd.getElementById('pass').value = pass;
  wd.getElementById('enc').value = enc;
  wd.getElementById('hidden').value = hidden;
  ww.calcTool();
  return wd.getElementById('result').textContent + ' ' + wd.getElementById('result').innerHTML;
}
// N218 转义（补证据）
const rEsc = wifiCalc('My;AP', 'pw;x', 'WPA', 'false');
check('N218 SSID/密码分号转义为 \\;', /My\\;AP/.test(rEsc) && /pw\\;x/.test(rEsc), rEsc.slice(0, 180));
const rColon = wifiCalc('a,b:c"d\\e', 'p', 'WPA', 'false');
check('N218 , : " \\ 均按 ZXing 规则转义', /a\\,b\\:c\\"d\\\\e/.test(rColon), rColon.slice(0, 180));
// N219 字段顺序/结尾（补证据）
const rPlain = wifiCalc('MyHomeAP', 'secret123', 'WPA', 'false');
check('N219 普通网络字符串 WIFI:T:WPA;S:…;P:…;;', /WIFI:T:WPA;S:MyHomeAP;P:secret123;;/.test(rPlain), rPlain.slice(0, 180));
const rHidden = wifiCalc('MyHomeAP', 'secret123', 'WPA', 'true');
check('N219 隐藏网络 H:true 在 P 后、结尾双分号，无多余空字段', /;P:secret123;H:true;;/.test(rHidden) && !/;;H:true/.test(rHidden), rHidden.slice(0, 200));
const rNopass = wifiCalc('Guest', '', 'nopass', 'true');
check('N219 nopass 隐藏网络无 P 字段且 H:true 结尾', /WIFI:T:nopass;S:Guest;H:true;;/.test(rNopass) && !/P:/.test(rNopass), rNopass.slice(0, 180));
// N220 改名（真修）
const html = W.html;
check('N220 title/H1/面包屑/JSON-LD 不再宣称「二维码生成器」', (html.match(/WiFi 配网二维码生成器/g) || []).length <= 1, 'count=' + (html.match(/WiFi 配网二维码生成器/g) || []).length);
check('N220 显示名改为「WiFi 配网字符串生成器」', /<title>WiFi 配网字符串生成器/.test(html) && /<h1 class="sr-only">WiFi 配网字符串生成器<\/h1>/.test(html), '');
check('N220 仍保留「交给二维码工具」的正确指引', /复制后交给二维码工具/.test(html) && /交给任意二维码生成工具/.test(wifiCalc('A', 'B', 'WPA', 'false')), '');
check('N220 URL/slug 未变（无死链风险）', /wifi-qr-generator\.html/.test(html) && !/wifi-string-generator/.test(html), '');
// N221 残缺 div（补证据）
check('N221 无未闭合的 </div（缺 >）', (() => {
  const bad = html.split('\n').filter(l => /<\/div(?!>)/.test(l));
  return bad.length === 0;
})(), '');

// ══════════════ 公式 / i18n 三源（仅修好版）══════════════
if (!OLD_DIR) {
  const enM = JSON.parse(fs.readFileSync('i18n/tools/en/it/markdown-table-generator.json', 'utf8'));
  const enW = JSON.parse(fs.readFileSync('i18n/tools/en/it/wifi-qr-generator.json', 'utf8'));
  check('i18n md-table 公式含 CSV 双引号规则且 en 同键', (() => {
    const k = Object.keys(enM.map).find(x => x.startsWith('行数取输入值'));
    return !!k && /双引号/.test(k) && /CSV rules/.test(enM.map[k]);
  })(), '');
  check('i18n wifi 已改名且无旧「二维码生成器」键（指南链接键保留）', (() => {
    const keys = Object.keys(enW.map);
    return keys.some(k => k.includes('WiFi 配网字符串生成器')) && !keys.some(k => k.includes('WiFi 配网二维码生成器') && !k.includes('使用指南'));
  })(), '');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
