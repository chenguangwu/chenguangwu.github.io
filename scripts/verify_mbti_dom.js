// MBTI 工具真实 DOM 交互测试（jsdom）
// 用法：NODE_PATH=/Users/cgw/.workbuddy/binaries/node/workspace/node_modules node scripts/verify_mbti_dom.js
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const TARGET = 'psychology/tester-2';
const file = path.join(__dirname, '..', 'tools', TARGET + '.html');
const html = fs.readFileSync(file, 'utf8');

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'http://localhost/tools/psychology/tester-2.html',
  pretendToBeVisual: true,
});
const { window } = dom;
const doc = window.document;

const log = [];
let fail = 0;
function ok(name, cond, extra) {
  log.push((cond ? '  ✅ ' : '  ❌ ') + name + (extra ? '  → ' + extra : ''));
  if (!cond) fail++;
}
function info(name, v) { log.push('  ℹ️  ' + name + '：' + v); }
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async function () {
  await sleep(300); // 等待脚本执行完毕

  const w = window;
  const $ = (id) => doc.getElementById(id);
  const opts = () => doc.getElementById('mtOpts').getElementsByClassName('mt-opt');
  const cells = () => doc.getElementById('mtGrid').getElementsByClassName('mt-cell');

  console.log('\n【A. 首屏渲染】');
  ok('题库已装载 60 题', w.MT_QS && w.MT_QS.length === 60, (w.MT_QS || []).length + ' 题');
  ok('题号显示 Q1', $('mtQNum').textContent === 'Q1', $('mtQNum').textContent);
  ok('题干已渲染', $('mtQText').textContent.length > 5, $('mtQText').textContent.slice(0, 28) + '…');
  ok('计数显示 60 题', /\/ 60 题/.test($('mtCount').textContent), $('mtCount').textContent);
  ok('维度标签已渲染', $('mtDimTag').textContent.length > 2, $('mtDimTag').textContent);

  console.log('\n【B. 选项形态（对应问题 3：不要原生单选按钮）】');
  ok('渲染出 5 个选项', opts().length === 5, opts().length + ' 个');
  ok('选项是 button 而非 input', opts()[0].tagName === 'BUTTON', opts()[0].tagName);
  ok('页面零原生 radio', doc.querySelectorAll('input[type=radio]').length === 0,
    'radio 数=' + doc.querySelectorAll('input[type=radio]').length);
  ok('第 3 档为中立（对应问题 2）', /中立/.test(opts()[2].textContent), opts()[2].textContent.trim());
  info('五档选项', Array.from(opts()).map(o => o.textContent.trim()).join(' / '));

  console.log('\n【C. 点文字即选中】');
  const label = opts()[2].getElementsByClassName('mt-opt-label')[0];
  label.click();
  ok('点内层文字即选中（事件冒泡）', opts()[2].className.indexOf('on') >= 0, opts()[2].className);
  ok('aria-pressed 同步为 true', opts()[2].getAttribute('aria-pressed') === 'true');
  ok('其余选项保持未选中', opts()[0].className.indexOf('on') < 0 && opts()[4].className.indexOf('on') < 0);
  ok('进度条已推进', parseFloat($('mtBarFill').style.width) > 0, $('mtBarFill').style.width);
  await sleep(280); // 等待自动跳到下一题

  console.log('\n【D. 顺序作答与回退（对应问题 4）】');
  ok('答完自动跳到第 2 题', $('mtQNum').textContent === 'Q2', $('mtQNum').textContent);
  ok('题号网格共 60 格', cells().length === 60, cells().length + ' 格');
  ok('已答格高亮', cells()[0].className.indexOf('done') >= 0, cells()[0].className);
  cells()[19].click();
  ok('点题号直接跳到第 20 题', $('mtQNum').textContent === 'Q20', $('mtQNum').textContent);
  $('mtPrev').click();
  ok('上一题回到 Q19', $('mtQNum').textContent === 'Q19', $('mtQNum').textContent);
  cells()[0].click();
  ok('跳回第 1 题原答案仍在', opts()[2].className.indexOf('on') >= 0, opts()[2].className);
  opts()[4].click();
  ok('可以把答案改成另一档', opts()[4].className.indexOf('on') >= 0 && opts()[2].className.indexOf('on') < 0);
  await sleep(280);

  console.log('\n【E. 键盘操作】');
  const cur = $('mtQNum').textContent;
  doc.dispatchEvent(new window.KeyboardEvent('keydown', { key: '3', bubbles: true }));
  ok('数字键 3 选中中立档', opts()[2].className.indexOf('on') >= 0, cur + ' → ' + opts()[2].className);
  const before = $('mtQNum').textContent;
  doc.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
  ok('方向键 → 翻到下一题', $('mtQNum').textContent !== before, before + ' → ' + $('mtQNum').textContent);

  console.log('\n【F. 完整结果输出】');
  for (let i = 0; i < 60; i++) w.MT_ANS[i] = (i % 3 === 0 ? -2 : (i % 3 === 1 ? 1 : 0));
  w.calc();
  const res = doc.getElementById('res').innerHTML;
  ok('结果已生成', res.length > 500, res.length + ' 字符');
  const code = (res.match(/mt-type-code">([A-Z]{4})</) || [])[1] || '';
  ok('输出 4 字母类型码', /^[EIN][SN][TF][JP]$/.test(code), code);
  ok('4 条维度百分比条', (res.match(/mt-dbar-top/g) || []).length === 4, (res.match(/mt-dbar-top/g) || []).length + ' 条');
  ok('含类型中文名', /mt-type-name/.test(res));
  ok('含核心特征', /核心特征/.test(res));
  ok('含常见优势', /常见优势/.test(res));
  ok('含可能盲点', /可能的盲点/.test(res));
  ok('含适配方向', /常见适配方向/.test(res));
  ok('含认知功能栈', /认知功能栈/.test(res));
  ok('结果无 NaN/undefined', !/NaN|undefined|Infinity/.test(res));
  const cv = doc.getElementById('res').getAttribute('data-copy-value') || '';
  ok('复制文本就绪', cv.length > 80, cv.split('\n')[1] || '');
  info('结果类型', code + '（' + cv.split('\n')[1] + '）');

  console.log('\n【G. 边界与重置】');
  w.mtReset();
  ok('重置后进度归零', parseFloat($('mtBarFill').style.width) === 0, $('mtBarFill').style.width);
  ok('重置后回到第 1 题', $('mtQNum').textContent === 'Q1', $('mtQNum').textContent);
  w.MT_ANS[0] = 1;
  w.calc();
  ok('未答完时提示剩余题数', /未作答/.test(doc.getElementById('res').innerHTML),
    doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim().slice(0, 34));

  console.log('\n' + log.join('\n'));
  console.log('\n==== ' + (fail === 0 ? '全部通过' : fail + ' 项失败') + ' ====');
  dom.window.close();
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('运行异常：', e); process.exit(1); });
