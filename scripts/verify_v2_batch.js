// V2 新增工具批量冒烟测试（jsdom）：加载无 JS 报错 + 关键元素存在 + 触发主按钮后仍无报错
// 用法：NODE_PATH=/Users/cgw/.workbuddy/binaries/node/workspace/node_modules node scripts/verify_v2_batch.js
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const ROOT = path.join(__dirname, '..');

const TARGETS = [
  ['cognition', 'cognitive-assessment'], ['cognition', 'corsi-block-test'],
  ['cognition', 'digit-span-test'], ['cognition', 'human-benchmark'],
  ['cognition', 'nback-training'], ['cognition', 'schulte-table'],
  ['cognition', 'stroop-test'], ['cognition', 'time-perception'],
  ['colorvision', 'colorblind-simulator'], ['colorvision', 'cvd-safe-palette'],
  ['colorvision', 'farnsworth-d15-test'], ['colorvision', 'palette-cvd-checker'],
  ['ophthalmology', 'amsler-grid-test'], ['ophthalmology', 'astigmatism-chart'],
  ['ophthalmology', 'eye-chart-toolkit'], ['ophthalmology', 'ishihara-test'],
  ['ent', 'calc-1'], ['ent', 'analysis-13'],
  ['fun', 'riddle-generator'], ['fun', 'sudoku-generator'],
];

// jsdom 未实现 canvas / WebAudio 等，这类告警不算页面缺陷
const IGNORE = /Not implemented|Could not parse CSS|Error: Not implemented/i;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function probe(ind, slug) {
  const file = path.join(ROOT, 'tools', ind, slug + '.html');
  if (!fs.existsSync(file)) return { ind, slug, fatal: '文件不存在' };
  const html = fs.readFileSync(file, 'utf8');
  const errs = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { if (!IGNORE.test(String(e.message))) errs.push(e.message.split('\n')[0]); });
  vc.on('error', (...a) => { const m = String(a[0]); if (!IGNORE.test(m)) errs.push(m); });

  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'http://localhost/tools/' + ind + '/' + slug + '.html',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(window) {
      // ToolBox / i18nText 由 /js/common.js 提供，测试环境不加载外部脚本，这里给替身
      window.ToolBox = new Proxy({}, { get: () => function () { return undefined; } });
      window.i18nText = (k, fb) => (fb === undefined ? String(k) : fb);
      // jsdom 未实现 canvas：给一个 noop 2D 上下文，避免绘图调用被误判为页面缺陷
      const noopCtx = new Proxy({}, {
        get(_t, k) {
          if (k === 'canvas') return undefined;
          if (k === 'measureText') return () => ({ width: 10 });
          if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop() {} });
          if (k === 'getImageData') return (x, y, w, h) => ({ data: new Uint8ClampedArray(Math.max(4, (w || 1) * (h || 1) * 4)) });
          if (k === 'createPattern') return () => ({});
          return function () { return undefined; };
        },
        set() { return true; },
      });
      window.HTMLCanvasElement.prototype.getContext = function () { return noopCtx; };
      window.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/png;base64,'; };
      // jsdom 未实现 scrollIntoView / scrollTo，真实浏览器原生支持，补空实现避免误报
      window.Element.prototype.scrollIntoView = function () {};
      window.HTMLElement.prototype.scrollIntoView = function () {};
      window.scrollTo = function () {};
      window.scrollBy = function () {};
    },
  });
  const doc = dom.window.document;
  await sleep(400);

  const r = { ind, slug, errs, info: {}, checks: [] };
  const ok = (n, c, x) => r.checks.push([n, !!c, x === undefined ? '' : String(x)]);

  const h = doc.querySelector('h2') || doc.querySelector('h1');
  const title = (h ? h.textContent : '').replace(/\s+/g, ' ').trim();
  ok('标题非空', title.length > 3, title.slice(0, 30));

  const inputs = doc.querySelectorAll('input,select,textarea').length;
  const buttons = doc.querySelectorAll('button').length;
  const canvas = doc.querySelectorAll('canvas').length;
  r.info = { inputs, buttons, canvas };
  ok('有交互元素', buttons > 0 || inputs > 0, 'btn=' + buttons + ' input=' + inputs);

  // 触发主按钮（最多前 3 个），观察是否抛错、页面是否产出内容
  const primary = [].slice.call(doc.querySelectorAll('button.btn.primary, button.primary, button'))
    .slice(0, 3);
  const textBefore = (doc.body.textContent || '').replace(/\s+/g, ' ').trim().length;
  let clicked = 0;
  for (const b of primary) {
    try { b.click(); clicked++; } catch (e) { errs.push('click: ' + e.message); }
  }
  await sleep(500);
  const textAfter = (doc.body.textContent || '').replace(/\s+/g, ' ').trim().length;

  ok('点击主按钮无报错', errs.length === 0, errs.slice(0, 2).join(' ; ') || 'clean');
  // 页面至少要有实质内容（不是空壳）
  ok('页面有实质内容', textAfter > 400, textAfter + ' 字符');
  // 游戏/测试类点击后通常会有状态变化（文本增长或出现结果区）
  const hasOut = !!doc.querySelector('table,.result-box,canvas,[id*="grid"],[id*="board"],[id*="res"],[id*="result"],[id*="out"],[id*="chart"],[id*="stage"],[id*="matrix"]');
  ok('存在输出载体', hasOut, '');
  r.clicked = clicked;
  r.textAfter = textAfter;
  dom.window.close();
  return r;
}

(async function () {
  let bad = 0;
  for (const [ind, slug] of TARGETS) {
    const r = await probe(ind, slug);
    if (r.fatal) { console.log('❌ ' + ind + '/' + slug + ' — ' + r.fatal); bad++; continue; }
    const failed = r.checks.filter(c => !c[1]);
    const tag = failed.length === 0 ? '✅' : '⚠️ ';
    if (failed.length) bad++;
    console.log(tag + ' ' + (ind + '/' + slug).padEnd(34) +
      ' btn=' + String(r.info.buttons).padEnd(3) +
      ' input=' + String(r.info.inputs).padEnd(3) +
      ' canvas=' + String(r.info.canvas).padEnd(2) +
      ' 文本=' + String(r.textAfter).padEnd(6) +
      (failed.length ? '｜失败: ' + failed.map(f => f[0] + (f[2] ? '(' + f[2].slice(0, 40) + ')' : '')).join(', ')
                     : '｜全部通过'));
  }
  console.log('\n==== ' + (bad === 0 ? '全部通过' : bad + ' 个工具存在问题') + ' ====');
  process.exit(0);
})();
