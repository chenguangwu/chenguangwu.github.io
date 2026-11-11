import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/user-agent-parser.html', 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + x : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/user-agent-parser.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => false },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const b = ua => w.parseBrowser(ua);

// IT-D41 微信
{
  const ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x1800282a) NetType/WIFI Language/zh_CN';
  const r = b(ua);
  check('微信 UA → WeChat', r.name === 'WeChat' && r.version === '8.0.40', JSON.stringify(r));
}
{
  // 微信桌面版 UA 同时含 Chrome/，必须优先识别为微信而非 Chrome
  const ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.28';
  const r = b(ua);
  check('微信含 Chrome 时优先微信', r.name === 'WeChat' && r.version === '7.0.28', JSON.stringify(r));
}
// IT-D41 百度爬虫
{
  const r = b('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)');
  check('百度爬虫 → Baiduspider', r.name === 'Baiduspider' && r.version === '2.0', JSON.stringify(r));
}
{
  const r = b('Mozilla/5.0 (compatible; Baiduspider; +http://www.baidu.com/search/spider.html)');
  check('百度爬虫无版本不报错', r.name === 'Baiduspider' && r.version === '', JSON.stringify(r));
}
// 既有规则回归
{
  const r = b('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36');
  check('Chrome 回归', r.name === 'Google Chrome' && r.version === '120.0.0.0', JSON.stringify(r));
}
{
  const r = b('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0');
  check('Edge 回归', r.name === 'Microsoft Edge' && r.version === '120.0.0.0', JSON.stringify(r));
}
{
  const r = b('Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1');
  check('CriOS 回归', r.name === 'Google Chrome' && r.version === '120.0.6099.119', JSON.stringify(r));
}
{
  const r = b('Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 SamsungBrowser/23.0.1.1 Chrome/115.0.0.0 Mobile Safari/537.36');
  check('Samsung 回归', r.name === 'Samsung Internet' && r.version === '23.0.1.1', JSON.stringify(r));
}
// 完整链路：parse() 输出含新识别结果与爬虫设备
{
  const inp = w.document.getElementById('uaInput');
  inp.value = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)';
  w.parse();
  const out = w.document.getElementById('result').textContent;
  check('parse() 输出含 Baiduspider 与爬虫设备', out.includes('Baiduspider 2.0') && /爬虫|bot|spider/i.test(out), out.slice(0, 130));
}

const pass = checks.filter(c => c[1]).length;
console.log(`\n==== batch172 ${pass}/${checks.length} ====`);
if (pass !== checks.length) process.exit(1);
