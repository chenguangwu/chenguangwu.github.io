// 第 119 批真机回归：F-N160/161/162/163（word-wrap）、F-N146（swift-bic）、
// F-N152（aadhaar），并核实 F-N141（currency-symbol 导出后表格隐藏）已修。
// JSDOM runScripts:'dangerously' + 真实 js/tool-kit.js + 自建 TBKit/ToolBox 桩。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
let failed = false;
const bad = [];

function load(slug) {
  const html = readFileSync(`${ROOT}/tools/finance/${slug}.html`, 'utf8');
  const downloads = [];
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 160) + ' | '; });
  const dom = new JSDOM(html, {
    url: `https://x.test/tools/finance/${slug}.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      w.ToolBox = {
        showToast() {}, escHtml: s => String(s), copyText() {}, downloadText() {}, toggleToolTheme() {},
        formatNumber: (v, d) => { const n = Number(v); return isFinite(n) ? n.toFixed(typeof d === 'number' ? d : 2) : String(v); },
        setResult: (id, s) => { const e = w.document.getElementById(id); if (e) e.innerHTML = s; },
        createTable: () => '',
      };
      w.i18nText = k => k;
      w.resolveCanvasColor = () => '#333';
      w.Blob = class { constructor(parts) { this.text = parts.join(''); } };
      w.URL.createObjectURL = b => { downloads.push(b.text); return 'blob:test'; };
      w.URL.revokeObjectURL = () => {};
      w.HTMLAnchorElement.prototype.click = function () {};
      w.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (_, k) => k === 'createLinearGradient' ? () => ({ addColorStop() {} }) : () => {},
      });
      w.eval(readFileSync(`${ROOT}/js/tool-kit.js`, 'utf8'));
    }
  });
  return { dom, w: dom.window, doc: dom.window.document, downloads, get jsErr() { return jsErr; } };
}
const check = (label, ok, diag) => {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${label}`);
  if (!ok) { failed = true; bad.push(label); if (diag) console.log('  DIAG ' + diag); }
};

// ---------------------------------------------------------------- word-wrap
{
  const { w, doc, downloads, jsErr } = load('word-wrap');
  await new Promise(r => w.addEventListener('load', r));
  check('word-wrap 加载无脚本异常', !jsErr, jsErr);

  const bytes = doc.getElementById('countBytes');
  bytes.checked = true;
  check('F-N161 中文按 UTF-8 3 字节计', w.eval("visualLen('中文测试')") === 12, String(w.eval("visualLen('中文测试')")));
  check('F-N161 emoji 按 4 字节计', w.eval("visualLen('😀')") === 4, String(w.eval("visualLen('😀')")));
  const tk = w.eval("JSON.stringify(takeByLen('😀ABC',4))");
  check('F-N161 takeByLen 不拆 emoji 代理项', JSON.parse(tk).text === '😀', tk);
  bytes.checked = false;

  // F-N160：按单词模式 + 悬挂缩进，续行必须有 2 空格且总宽不超 width
  doc.getElementById('width').value = '20';
  doc.getElementById('mode').value = 'word';
  doc.getElementById('indent').checked = false;
  doc.getElementById('hanging').checked = true;
  doc.getElementById('keepExisting').checked = false;
  doc.getElementById('input').value = 'This is a fairly long English clause that must wrap onto several lines for the hanging indent to become visible';
  w.eval('wrap()');
  const wlines = doc.getElementById('result').textContent.split('\n');
  const wrapOk = wlines.length >= 3 && wlines.slice(1).every(l => l.startsWith('  ')) && wlines.every(l => l.length <= 20);
  check('F-N160 word 模式悬挂缩进生效且不超宽', wrapOk, JSON.stringify(wlines.map(l => [l.length, l.slice(0, 26)])));

  // F-N162：无标点超长中文句必须强折，不能整段压成一行
  doc.getElementById('mode').value = 'chinese';
  doc.getElementById('hanging').checked = false;
  const longZh = '这是一个没有任何标点的超长连续中文句子用于测试按中文断句模式是否会在宽度不足时继续强行折行';
  doc.getElementById('input').value = longZh;
  w.eval('wrap()');
  const zlines = doc.getElementById('result').textContent.split('\n');
  const zhOk = zlines.length >= 3 && zlines.every(l => l.length <= 20) && zlines.join('') === longZh;
  check('F-N162 中文超长 token 强折且不丢字', zhOk, JSON.stringify(zlines.map(l => l.length)));

  // F-N163：导出必须含当前折行结果，而非空历史表
  doc.querySelector('[onclick="__word_wrapExport()"]').click();
  const csv = downloads.map(d => String(d)).join('\n');
  check('F-N163 导出含折行结果明细', csv.includes('折行后文本') && csv.includes(zlines[0]) && csv.includes('UTF-8'), csv.slice(0, 160));
  const guide = doc.querySelector('.opt-guide')?.textContent || '';
  const faq = doc.querySelector('.opt-faq')?.textContent || '';
  check('F-N163 操作文案改为「换行」且去掉理财套话',
    !guide.includes('点击「计算」或「生成」') && guide.includes('换行') && !guide.includes('贷款与投资收益测算') && !faq.includes('贷款与投资收益测算'),
    guide.slice(0, 160));
  check('F-N163 删除无面板的「预设」页签', !doc.querySelector('[data-pane="pre"]') && doc.querySelectorAll('.tbk-tab').length === 3,
    String(doc.querySelectorAll('.tbk-tab').length));
  // 既有行为回归：默认 word 模式的输入拼接仍正常
  doc.getElementById('mode').value = 'word';
  doc.getElementById('width').value = '42';
  doc.getElementById('keepExisting').checked = true;
  doc.getElementById('input').value = '1\n2\n3';
  w.eval('wrap()');
  const folded = doc.getElementById('result').textContent.replace(/\s+/g, ' ').trim();
  check('word-wrap 既有 word 模式回归', folded === '1 2 3', folded);
  w.close();
}

// ---------------------------------------------------------------- swift-bic
{
  const { w, doc, jsErr } = load('swift-bic-validator');
  await new Promise(r => w.addEventListener('load', r));
  check('swift-bic 加载无脚本异常', !jsErr, jsErr);
  doc.getElementById('input').value = 'DEUT DE FF 500';
  w.eval('validate()');
  const o1 = doc.getElementById('output').innerHTML;
  check('F-N146 分组书写归一化并通过校验',
    o1.includes('长度：</strong>11 字符') && o1.includes('已忽略 3 个') && o1.includes('银行代码：</strong>DEUT') && o1.includes('格式有效') && !o1.includes('❌ 长度必须为 8 或 11'),
    o1.slice(0, 260));
  doc.getElementById('input').value = '<img src=x onerror=alert(1)>';
  w.eval('validate()');
  const o2 = doc.getElementById('output').innerHTML;
  check('F-N146 非法输入回显转义且拒绝', !/<img/i.test(o2) && o2.includes('&lt;IMG') && o2.includes('仅允许字母、数字') && !o2.includes('已忽略'), o2.slice(0, 260));
  w.close();
}

// ---------------------------------------------------------------- aadhaar
{
  const { w, doc, jsErr } = load('aadhaar-validator');
  await new Promise(r => w.addEventListener('load', r));
  check('aadhaar 加载无脚本异常', !jsErr, jsErr);
  doc.getElementById('input').value = '00-0000-0000-00';
  w.eval('validate()');
  const o = doc.getElementById('output').innerHTML;
  check('F-N152 首位 0/1 分支补齐输入/格式化/长度上下文',
    o.includes('00-0000-0000-00') && o.includes('格式化：</strong>0000 0000 0000') && o.includes('长度：</strong>12 位') && o.includes('不能以 0 或 1 开头'),
    o.slice(0, 300));
  w.close();
}

// ---------------------------------------------------------------- currency-symbol（F-N141 核实已修）
{
  const { w, doc, downloads, jsErr } = load('currency-symbol');
  await new Promise(r => w.addEventListener('load', r));
  check('currency-symbol 加载无脚本异常', !jsErr, jsErr);
  const t = doc.getElementById('curTable');
  const before = t?.style.display;
  doc.querySelector('[onclick="__curExport()"]')?.click();
  check('F-N141 导出后 153 行表格恢复隐藏',
    !!t && t.style.display === 'none' && downloads.length > 0 && String(downloads[0]).length > 0,
    JSON.stringify({ before, after: t?.style.display, dl: downloads.length }));
  w.close();
}

console.log(`\n=== BATCH119 ${failed ? 'FAILED' : 'ALL PASS'} | failed=${bad.length} ===`);
if (bad.length) console.log(bad.join('\n'));
process.exit(failed ? 1 : 0);
