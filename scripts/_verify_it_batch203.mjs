// 第203批 · IT-N255 device-info 状态徽章不被转义（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/device-info.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

function makeDom(onLine) {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.com/tools/it/device-info.html',
    beforeParse(w) {
      w.alert = () => {};
      w.i18nText = (k, fb) => (fb != null ? fb : '');
      w.ToolBox = { copyText() {}, showToast() {}, toggleToolTheme() {}, downloadText() {} };
      Object.defineProperty(w.navigator, 'onLine', { configurable: true, value: onLine });
      w.TBKit = { util: { isEn: () => false, exportTable() {} } };
      w.console = { warn() {}, log() {}, error() {} };
    }
  });
  return dom.window.document;
}

// 在线态
{
  const d = makeDom(true);
  const bi = d.getElementById('browserInfo');
  const ds = d.getElementById('deviceStatus');
  // 真实 DOM 节点存在 = 未转义；转义时会是文本 "&lt;span..."
  check('在线态 browserInfo 有真实 badge 元素', bi.querySelector('.status-badge.ok') !== null, bi.textContent.slice(0, 60));
  check('在线态 deviceStatus 有真实 badge 元素', ds.querySelector('.status-badge.ok') !== null, ds.textContent.slice(0, 60));
  check('badge 文本为「在线」', bi.querySelector('.status-badge') && bi.querySelector('.status-badge').textContent === '在线');
  check('页面无裸转义标签文本', bi.innerHTML.indexOf('&lt;span') < 0 && ds.innerHTML.indexOf('&lt;span') < 0);
}

// 离线态
{
  const d = makeDom(false);
  const bi = d.getElementById('browserInfo');
  check('离线态 badge 为 err 样式', bi.querySelector('.status-badge.err') !== null, bi.textContent.slice(0, 60));
  check('离线态 badge 文本为「离线」', bi.querySelector('.status-badge') && bi.querySelector('.status-badge').textContent === '离线');
}

// 安全性：普通值仍被转义（item raw 仅用于内部 badge）
{
  const d = makeDom(true);
  // 直接调 item（顶层函数）验证默认仍转义
  const out = d.defaultView.item('XSS', '<img src=x onerror=alert(1)>');
  check('item 默认仍转义外部值', out.indexOf('&lt;img') >= 0 && out.indexOf('<img') < 0, out.slice(0, 100));
  const rawOut = d.defaultView.item('badge', '<span class="status-badge ok">OK</span>', false, true);
  check('item raw=true 仅可信串不转义', rawOut.indexOf('<span class="status-badge ok">OK</span>') >= 0);
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
