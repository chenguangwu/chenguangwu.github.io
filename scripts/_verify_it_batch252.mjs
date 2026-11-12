// 第252批 JSDOM 验证：IT-N136 ascii-table 点击复制 / N137 Latin-1 口径 / N138 区间边界
// 用法: node scripts/_verify_it_batch252.mjs [OLD_DIR]
// 传入 OLD_DIR 时读取备份源码，验证旧态缺陷存在（判别力证据）。
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const dir = (p) => OLD ? `${OLD}/${p}` : p;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function loadPage() {
  return fs.readFileSync(dir('tools/it/ascii-table.html'), 'utf8');
}
function makeDom(html) {
  const copied = [];
  const domain = { runScripts: 'dangerously', url: 'https://example.com/ascii-table.html', beforeParse(w) {
    w.alert = () => {};
    w.__toasts = [];
    w.ToolBox = { showToast: (m) => w.__toasts.push(String(m)), copyText: (v) => copied.push(String(v)), toggleToolTheme() {} };
    w.TBKit = { util: { isEn: () => false } };
    Object.defineProperty(w.navigator, 'clipboard', {
      configurable: true,
      value: { writeText: (v) => { copied.push(String(v)); return Promise.resolve(); } }
    });
  }};
  const dom = new JSDOM(html, domain);
  return { dom, copied };
}
function cards(d) { return Array.from(d.querySelectorAll('.ascii-card')).map(c => c.querySelector('.dec').textContent); }

const html = loadPage();
const { dom, copied } = makeDom(html);
const w = dom.window, d = w.document;

// ---- N138 区间边界（真机实测：ctrl 0-31 / print 应为 32-126 / extended 128-255）----
w.setCat('ctrl', { classList: { add() {}, remove() {} } });
let c = cards(d);
check('N138 ctrl=0-31', c.length === 32 && c[0] === '0' && c[c.length - 1] === '31', `n=${c.length} last=${c[c.length - 1]}`);
w.setCat('print', { classList: { add() {}, remove() {} } });
c = cards(d);
check('N138 print=32-126（不含DEL 127）', c.length === 95 && c[0] === '32' && c[c.length - 1] === '126', `n=${c.length} last=${c[c.length - 1]}`);
w.setCat('extended', { classList: { add() {}, remove() {} } });
c = cards(d);
check('N138 extended=128-255', c.length === 128 && c[0] === '128' && c[c.length - 1] === '255', `n=${c.length}`);
check('N138 页签标签改 32-126', /可打印 \(32-126\)/.test(html) && !/可打印 \(32-127\)/.test(html), 'label');

// ---- N137 Latin-1 口径 ----
check('N137 页签改 Latin-1', /Latin-1 \(128-255\)/.test(html) && !/>扩展 \(128-255\)</.test(html), 'tab');
w.showDetail(128);
const detail = d.getElementById('detail').textContent;
check('N137 详情分类=Latin-1', /Latin-1 \(ISO-8859-1\)/.test(detail) && !/扩展 ASCII/.test(detail), detail.replace(/\s+/g, ' ').slice(-60));
const enMap = JSON.parse(fs.readFileSync(dir('i18n/tools/en/it/ascii-table.json'), 'utf8')).map;
check('N137 英文映射含 Latin-1 标签', enMap['Latin-1 (128-255)'] === 'Latin-1 (128–255)' && !enMap['扩展 (128-255)'], 'checked');

// ---- N136 点击自动复制十进制编码 ----
copied.length = 0;
w.__toasts.length = 0;
w.showDetail(65);
await new Promise(r => setTimeout(r, 0)); // 等待 clipboard.writeText().then() 微任务执行
check('N136 点击复制十进制编码 65', copied.includes('65'), 'copied=' + JSON.stringify(copied));
check('N136 toast 提示已复制', w.__toasts.some(m => /已复制|Copied/.test(m)), JSON.stringify(w.__toasts));
check('N136 详情含复制编码值', /asciiCopyVal|>65</.test(d.getElementById('detail').innerHTML), 'copy row');
check('N136 meta SEO 仍承诺点击复制（功能已兑现）', /点击即可复制对应编码/.test(html), 'meta');

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
