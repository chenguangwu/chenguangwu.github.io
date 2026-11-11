// 第208批 · IT-N261/N262/N263 hex-encode 多行0x / 历史链 / 严格UTF-8（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/hex-encode.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 180) : '')); }

let isEn = false;
const alerts = [];
const hist = [];   // [{t, d}, ...] 与页面 TBKit.history.list() 形态一致

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/hex-encode.html',
  beforeParse(w) {
    w.alert = m => { alerts.push(String(m)); };
    w.i18nText = k => k;
    w.TextDecoder = TextDecoder;
    w.TextEncoder = TextEncoder;
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {} };
    Object.defineProperty(w.navigator, 'clipboard', {
      configurable: true,
      value: { writeText() { return Promise.resolve(); } }
    });
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar() {} },
      history: {
        list() { return hist.slice(); },
        record(d) { hist.unshift({ t: Date.now(), d: Object.assign({}, d) }); },
        last() { return hist.length ? hist[0].d : null; },
        mount(sel, fn) { w.__hexReplay = fn; },
        clear() { hist.length = 0; }
      }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

const input = d.getElementById('input');
const output = d.getElementById('output');
const prefix = d.getElementById('prefix');
const upper = d.getElementById('upper');
const sep = d.getElementById('sep');

function encode(s) {
  input.value = s;
  w.eval('__hex_encode_last = 0;');
  w.eval('enc()');
  return output.value;
}
function decode(s) {
  input.value = s;
  w.eval('__hex_encode_last = 0;');
  w.eval('dec()');
  return output.value;
}
function clearHist() { hist.length = 0; }

// ── IT-N261 编码侧 prefix 逐字节加 ──
sep.value = ' ';
prefix.checked = true;
upper.checked = false;
check('编码 prefix 逐字节 0x48 0x69', encode('Hi') === '0x48 0x69', JSON.stringify(output.value));
prefix.checked = false;
check('编码无 prefix 仍为 48 69', encode('Hi') === '48 69', JSON.stringify(output.value));
prefix.checked = true;
upper.checked = true;
check('编码 uppercase + 逐字节 prefix', encode('j') === '0x6A', JSON.stringify(output.value));
upper.checked = false;
sep.value = '';

// ── IT-N261 解码侧：多行/每字节 0x 的 hexdump 与内存 dump ──
check('解码每字节 0x（空格分隔）', decode('0x48 0x69 0x6f') === 'Hio', JSON.stringify(output.value));
check('解码多行 hexdump（每行带 0x）', decode('0x48\n0x69\n0x6f') === 'Hio', JSON.stringify(output.value));
check('解码混合写法（首字节 0x + 后续裸 hex）', decode('0x48 69 6f') === 'Hio', JSON.stringify(output.value));
check('解码标准连续 hex 不回退', decode('4869') === 'Hi', JSON.stringify(output.value));
check('解码冒号/短横线分隔符', decode('48:69-6f') === 'Hio', JSON.stringify(output.value));
check('解码大小写前缀 0X 兼容', decode('0X48 0X69') === 'Hi', JSON.stringify(output.value));

// ── IT-N262 评分启发式清除 + 历史链不再恒空 ──
check('score(Error 404)=1', w.eval("__hex_encodeScore('Error 404')") === 1);
check('score(中文「错误」)=1', w.eval("__hex_encodeScore('页面显示：错误')") === 1);
check('score(严格解码告警 ⚠)=1', w.eval("__hex_encodeScore('⚠ 含 1 个非法 UTF-8 字节')") === 1);
clearHist(); encode('Hi');
check('编码进历史且不恒空', hist.length >= 1, 'n=' + hist.length);
check('历史 __tbScore=1', hist.length >= 1 && hist[0].d.__tbScore === 1, JSON.stringify(hist[0] && hist[0].d));

// ── IT-N263 严格 UTF-8：非法字节明确报错 + Latin-1 对照 ──
const bad = decode('FF');
check('非法字节不再静默替换成 U+FFFD', bad.indexOf('\uFFFD') < 0, JSON.stringify(bad.slice(0, 60)));
check('非法字节明确告警', /非法 UTF-8|invalid UTF-8/.test(bad), bad.slice(0, 60));
check('非法字节给 Latin-1 对照', bad.indexOf('Latin-1') >= 0 && bad.indexOf('\u00FF') >= 0);
check('非法字节给原始字节 0xFF', bad.indexOf('0xFF') >= 0);
check('合法中文 UTF-8 正常解码', decode('E4 B8 AD') === '中', JSON.stringify(output.value));

// ── IT-N263 解码接入历史 + 方向字段 + 回放按方向 ──
clearHist(); decode('4869');
check('解码也进历史（原版只包 enc）', hist.length >= 1, 'n=' + hist.length);
check('解码记录含方向=解码', hist.length >= 1 && hist[0].d['模式'] === '解码', JSON.stringify(hist[0] && hist[0].d));
const decRec = hist[0] && hist[0].d;
clearHist(); encode('Hi');
check('编码记录含方向=编码', hist.length >= 1 && hist[0].d['模式'] === '编码', JSON.stringify(hist[0] && hist[0].d));
if (decRec && typeof w.__hexReplay === 'function') {
  input.value = ''; output.value = '';
  try { w.__hexReplay(decRec); } catch (e) { console.log('replay err ' + e.message); }
  check('回放解码记录走 dec() 还原文本', output.value === 'Hi', JSON.stringify(output.value));
} else {
  check('回放解码记录走 dec() 还原文本', false, 'no replay hook');
}

// ── IT-N263 EN 态无中文泄漏 ──
isEn = true;
const badEn = decode('FF');
check('EN 态严格解码提示为英文', /invalid UTF-8/i.test(badEn) && !/非法/.test(badEn), badEn.slice(0, 80));
alerts.length = 0; decode('GG');
check('EN 态非法字符 alert 英文化', alerts.some(a => /Invalid hexadecimal/i.test(a)), JSON.stringify(alerts));
isEn = false;

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
