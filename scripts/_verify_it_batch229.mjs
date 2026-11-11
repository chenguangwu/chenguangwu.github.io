// 第229批 · IT-N222~N226（phone-screen-sizes 3 条 + rabbit 2 条，JSDOM 真机）
//  N222 图表页签默认隐藏结果区（真修：结果始终可见，页签只切换曲线）
//  N223 宣称可查 DPR 却无 DPR/CSS 视口列、分辨率顺序不一（真修：统一宽×高并补列）
//  N224 meta/og/twitter/JSON-LD 描述重复（真修：去重为单句）
//  N225 Rabbit 进位与整套 RFC 4503 实现偏离（真修：密钥/IV/计数器/提取全量对齐）
//  N226 32 hex 密钥被按文本截断（真修：hex 按字节装入，文本补齐/超长报错）
// 用法：node scripts/_verify_it_batch229.mjs [旧页目录；提供时做旧源码差分]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD_DIR = process.argv[2] || '';
const checks = [];
function check(n, ok, x) { checks.push([n, !!ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

function makeDom(htmlPath, en) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const history = [];
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://example.com/tools/it/x.html',
    beforeParse(w) {
      w.alert = () => {};
      w.ToolBox = { showToast() {}, copyText() {}, setResult(id, v) { const e = w.document.getElementById(id); if (e) e.innerHTML = v; }, toggleToolTheme() {} };
      w.TBKit = {
        util: { isEn: () => !!en, exportTable() {}, diffBox() {} },
        chart: { line() {}, bar() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list() { return history.slice(); }, last() { return history.length ? history[history.length - 1] : null; },
          record(r) { history.push(r); }, mount() {}, clear() { history = []; } }
      };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, html };
}

const PSS = OLD_DIR ? OLD_DIR + '/pss.orig.html' : 'tools/it/phone-screen-sizes.html';
const RAB = OLD_DIR ? OLD_DIR + '/rabbit.orig.html' : 'tools/it/rabbit.html';

// ══════════════ N222~N224 phone-screen-sizes ══════════════
const P = makeDom(PSS), pw = P.w, pd = P.d;
check('N224 描述不再重复「是一款免费的在线IT 开发工具」', (P.html.match(/手机屏幕尺寸速查是一款免费的在线IT 开发工具/g) || []).length === 0,
  'count=' + (P.html.match(/手机屏幕尺寸速查是一款免费的在线IT 开发工具/g) || []).length);
check('N224 meta/og/twitter/JSON-LD 使用去重后的同一句', (P.html.match(/手机屏幕尺寸速查：按英寸与分辨率反算 PPI/g) || []).length === 4,
  'count=' + (P.html.match(/手机屏幕尺寸速查：按英寸与分辨率反算 PPI/g) || []).length);
check('N222 首屏结果区未被页签隐藏', pd.getElementById('result').style.display !== 'none', 'display=' + pd.getElementById('result').style.display);
check('N222 结果含 PPI 数据', /PPI/.test(pd.getElementById('result').textContent), pd.getElementById('result').textContent.slice(0, 80));
const pBtnResult = pd.querySelector('.tab-btn[data-pane="result"]'), pBtnBoth = pd.querySelector('.tab-btn[data-pane="both"]');
check('N222 页签语义改为「结果 + 图表 / 仅结果」',
  !!pBtnResult && /仅结果/.test(pBtnResult.textContent) && !!pBtnBoth && /结果 \+ 图表/.test(pBtnBoth.textContent), '');
if (pBtnResult && pBtnBoth) {
  pBtnResult.click();
  check('N222 点「仅结果」只藏曲线不藏结果', pd.getElementById('pssChart').style.display === 'none' && pd.getElementById('result').style.display !== 'none',
    'chart=' + pd.getElementById('pssChart').style.display + ',result=' + pd.getElementById('result').style.display);
  pBtnBoth.click();
  check('N222 点「结果 + 图表」恢复曲线与结果', pd.getElementById('pssChart').style.display !== 'none' && pd.getElementById('result').style.display !== 'none', '');
}
const pTable = pd.getElementById('result').innerHTML;
check('N223 机型表新增 DPR 与 CSS 视口列', /DPR（典型）/.test(pTable) && /CSS 视口（宽×高）/.test(pTable), pTable.slice(0, 200));
check('N223 分辨率统一为宽×高（1179×2556，不再 2556×1179）', /1179×2556/.test(pTable) && !/2556×1179/.test(pTable), '');
check('N223 iPhone 15 Pro 的 CSS 视口 393×852 可见', /393×852/.test(pTable), '');
check('N223 机型表仍为 10 款', (pTable.match(/<tr>/g) || []).length === 11, 'rows=' + (pTable.match(/<tr>/g) || []).length);
const PE = makeDom(PSS, true);
let enTable = '';
try { enTable = PE.w.eval('pssPhoneTable()'); } catch (e) { enTable = 'NOT_DEFINED'; }
check('N223 英文态机型表表头/提示无汉字', enTable !== 'NOT_DEFINED' && !/[\u4e00-\u9fff]/.test(enTable) && /CSS viewport \(W×H\)/.test(enTable), enTable.slice(0, 180));

// ══════════════ N225/N226 rabbit ══════════════
const R = makeDom(RAB), rw = R.w, rd = R.d;
function vector(key, iv) {
  const ivArg = iv ? "hexToBytes('" + iv + "')" : 'null';
  return rw.eval("(function(){var b=new Uint8Array(16);new Rabbit(hexToBytes('" + key + "')," + ivArg + ").keystream(b,0,16);return bytesToHex(b);})()");
}
const V = [
  ['00000000000000000000000000000000', '0000000000000000', 'c6a7275ef85495d87ccd5d376705b7ed', 'RFC A.2 #1 全零密钥+全零 IV'],
  ['00000000000000000000000000000000', 'c373f575c1267e59', '1fcd4eb9580012e2e0dccc9222017d6d', 'RFC A.2 #2 全零密钥+非零 IV'],
  ['912813292e3d36fe3bfc62f1dc51c3ac', null, '3d2df3c83ef627a1e97fc38487e2519c', 'RFC A.1 #2 非零密钥无 IV'],
  ['8395741587e0c733e9e9ab01c09b0043', null, '0cb10dcda041cdac32eb5cfd02d0609b', 'RFC A.1 #3 非零密钥无 IV'],
];
for (const [k, iv, want, name] of V) {
  const got = vector(k, iv);
  check('N225 ' + name + ' 首块密钥流对齐官方向量', got === want, got + ' / want ' + want);
}
check('N225 源码不再有 t>>>32 或把进位加回 C0 后清零', !/>>>\s*32/.test(R.html) && !/C\[0\]=\(C\[0\]\+carry\)/.test(R.html), '');
rd.getElementById('key').value = '00112233445566778899aabbccddeeff';
check('N226 32 hex 密钥按字节装入而非按 ASCII 文本截断', rw.eval('bytesToHex(getKey())') === '00112233445566778899aabbccddeeff', rw.eval('bytesToHex(getKey())'));
rd.getElementById('key').value = '';
const defKey = rw.eval('bytesToHex(getKey())');
check('N226 空密钥回退为整整 16 字节默认值', defKey.length === 32, defKey + ' (' + defKey.length / 2 + ' bytes)');
rd.getElementById('key').value = 'this-key-is-way-too-long-12345';
let overErr = '';
try { rw.eval('getKey()'); } catch (e) { overErr = String(e.message || e); }
check('N226 超长文本密钥明确报错而非静默截断', /16/.test(overErr), overErr);
check('N226 随机 IV 按钮按 8 字节生成', /randomHex\(8\)/.test(R.html) && !/randomHex\(16\)/.test(R.html), '');
// 端到端：RFC 官方向量作为密文解密，得到 16 个 NUL 字节
rd.getElementById('key').value = '00000000000000000000000000000000';
rd.getElementById('iv').value = '0000000000000000';
rd.getElementById('outputFormat').value = 'hex';
rd.getElementById('input').value = 'c6a7275ef85495d87ccd5d376705b7ed';
rw.decrypt();
const dec = rd.getElementById('output').value;
check('N225 端到端解密：官方向量密文 → 16 个 NUL 明文', dec.length === 16 && [...dec].every(c => c.charCodeAt(0) === 0), 'len=' + dec.length);
// 失败态清空旧结果，避免 G10 旧结果残留
rd.getElementById('key').value = 'overlong-key-that-exceeds-16-bytes';
rd.getElementById('input').value = '616263';
rw.encrypt();
check('N226 非法密钥时清空旧输出', rd.getElementById('output').value === '', JSON.stringify(rd.getElementById('output').value));
const rbHtml = R.html;
check('N226 密钥/IV 标签与 deep-dive 声明 RFC 向量', /32 hex 字符/.test(rbHtml) && /C6 A7 27 5E/.test(rbHtml), '');
if (!OLD_DIR) {
  const enR = JSON.parse(fs.readFileSync('i18n/tools/en/it/rabbit.json', 'utf8'));
  const dd = JSON.parse(fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'));
  check('i18n rabbit 英文映射同步新公式/标签/deep-dive', Object.keys(enR.map).some(k => k.startsWith('按 RFC 4503 实现')) &&
    Object.values(enR.map).some(v => /RFC 4503 vector/.test(v)), '');
  check('i18n deep-dive 两页源与页面示例一致', /C6 A7 27 5E/.test(dd['it/rabbit'].examples[0].body) &&
    /393×852/.test(dd['it/phone-screen-sizes'].examples[0].body), '');
}

const pass = checks.filter(c => c[1]).length;
console.log('\n==== ' + pass + '/' + checks.length + ' 通过 ====');
if (pass !== checks.length) { console.log('FAILED: ' + checks.filter(c => !c[1]).map(c => c[0]).join(' | ')); process.exit(1); }
