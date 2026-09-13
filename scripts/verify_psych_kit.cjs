/* verify_psych_kit.cjs — 心理量表页面增强的行为验证（jsdom）
 * 覆盖：说明卡、进度条、未答确认、分级徽章、高危热线横幅、娱乐标识、本地暂存。
 */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const ROOT = path.resolve(__dirname, '..');
const KIT = fs.readFileSync(path.join(ROOT, 'js', 'psych-kit.js'), 'utf8');

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ✅ ' + name); }
  else { fail++; console.log('  ❌ ' + name + (extra ? ' — ' + extra : '')); }
}

function load(rel) {
  const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => { });
  const dom = new JSDOM(html, {
    url: 'https://chenguangwu.github.io/' + rel,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc
  });
  const d = dom.window.document;
  const s = d.createElement('script');
  s.textContent = KIT;
  const cfg = (html.match(/data-psych='([^']*)'/) || [])[1] || '{}';
  s.setAttribute('data-psych', cfg);
  d.body.appendChild(s);
  return dom;
}

function ready() {
  return new Promise(resolve => setTimeout(resolve, 60));
}

function click(win, el) {
  el.dispatchEvent(new win.MouseEvent('click', { bubbles: true, cancelable: true }));
}

function answerRows(win, d, fn) {
  Array.from(d.querySelectorAll('.q-opts')).forEach((row, i) => {
    const opts = Array.from(row.querySelectorAll('.q-opt'));
    const idx = fn(i, opts.length);
    if (opts[idx]) click(win, opts[idx]);
  });
}

(async function main() {
  console.log('== 1. PHQ-9 高危路径 ==');
  {
    const dom = load('tools/psychiatry/phq9-depression.html');
    const w = dom.window, d = w.document;
    await ready();
    ok('说明卡已注入', !!d.getElementById('pk-intro'));
    ok('进度条已注入', !!d.getElementById('pk-progress'));
    const head = d.querySelector('.pk-progress-head');
    ok('题数显示 9', !!head && /\/ 9 题/.test(head.textContent), head ? head.textContent : '');
    const quiz = d.getElementById('quiz');
    ok('未开始则题目区隐藏', quiz.classList.contains('pk-hidden'));
    click(w, d.getElementById('pk-start'));
    ok('点击开始后题目区显示', !quiz.classList.contains('pk-hidden'));

    answerRows(w, d, () => 3);   // 全选最高分 3 → 总分 27，第9题=3
    await ready();
    const res = d.getElementById('result');
    ok('进度显示已答 9 题', /已答 9 题/.test((d.getElementById('pk-done') || {}).textContent || ''));
    const hot = res.querySelector('.pk-hotline');
    ok('高危结果出现热线横幅', !!hot);
    ok('热线含 3 个可拨号链接', !!hot && hot.querySelectorAll('a[href^="tel:"]').length >= 3);
    ok('热线号码完整', !!hot && hot.textContent.includes('400-161-9995') && hot.textContent.includes('010-82951332') && hot.textContent.includes('400-821-1215'));
    ok('tel 链接为纯数字', !!hot && Array.from(hot.querySelectorAll('a[href^="tel:"]')).every(a => /^tel:\d+$/.test(a.getAttribute('href'))));
    ok('分级徽章存在', !!res.querySelector('.pk-badge'));
    ok('重度徽章为红色', !!res.querySelector('.pk-badge') && res.querySelector('.pk-badge').style.background.replace(/\s/g, '') === 'rgb(220,38,38)');
    ok('大号总分显示 27', !!res.querySelector('.pk-score') && res.querySelector('.pk-score').textContent === '27');
    ok('操作条含复制/存图', !!d.getElementById('pk-copy') && !!d.getElementById('pk-img'));
    ok('本地暂存已写入', !!w.localStorage.getItem('pk:ans:phq9-depression'));
    dom.window.close();
  }

  console.log('== 2. PHQ-9 低危路径（全选 0 分）==');
  {
    const dom = load('tools/psychiatry/phq9-depression.html');
    const w = dom.window, d = w.document;
    await ready();
    click(w, d.getElementById('pk-start'));
    answerRows(w, d, () => 0);
    await ready();
    const res = d.getElementById('result');
    ok('低危无热线横幅', !res.querySelector('.pk-hotline'));
    const badge = res.querySelector('.pk-badge');
    ok('低危徽章为绿色', !!badge && badge.style.background.replace(/\s/g, '') === 'rgb(22,163,74)', badge ? badge.style.background : '无徽章');
    dom.window.close();
  }

  console.log('== 3. 未答完提交确认 ==');
  {
    const dom = load('tools/psychiatry/gad7-anxiety.html');
    const w = dom.window, d = w.document;
    await ready();
    click(w, d.getElementById('pk-start'));
    const rows = Array.from(d.querySelectorAll('.q-opts'));
    rows.slice(0, 3).forEach(row => click(w, row.querySelectorAll('.q-opt')[1]));
    await ready();
    const btn = Array.from(d.querySelectorAll('button')).find(b => (b.getAttribute('onclick') || '').indexOf('calc(') >= 0);
    ok('找到计算按钮', !!btn);
    click(w, btn);
    await ready();
    const modal = d.querySelector('.pk-modal');
    ok('弹出未答确认框', !!modal);
    ok('提示未答题数（7 题中剩 4 题）', !!modal && /还有 4 题未作答/.test(modal.textContent), modal ? modal.textContent.slice(0, 70) : '未弹出');
    ok('列出未答题号', !!modal && !!modal.querySelector('.pk-modal-nums'));
    click(w, d.getElementById('pk-ok'));
    ok('确认后关闭弹窗', !d.querySelector('.pk-modal'));
    dom.window.close();
  }

  console.log('== 4. GAD-7 高危阈值（≥15）==');
  {
    const dom = load('tools/psychiatry/gad7-anxiety.html');
    const w = dom.window, d = w.document;
    await ready();
    click(w, d.getElementById('pk-start'));
    answerRows(w, d, () => 3);   // 7×3 = 21 ≥ 15
    await ready();
    ok('GAD-7 满分触发热线', !!d.getElementById('result').querySelector('.pk-hotline'));
    dom.window.close();
  }

  console.log('== 5. CAGE 阳性阈值（≥2）==');
  {
    const dom = load('tools/psychiatry/cage-substance.html');
    const w = dom.window, d = w.document;
    await ready();
    click(w, d.getElementById('pk-start'));
    const rows = Array.from(d.querySelectorAll('.q-opts'));
    rows.slice(0, 2).forEach(r => click(w, r.querySelectorAll('.q-opt')[0]));
    rows.slice(2).forEach(r => click(w, r.querySelectorAll('.q-opt')[1]));
    await ready();
    ok('CAGE 2 项"是"触发热线', !!d.getElementById('result').querySelector('.pk-hotline'),
      d.getElementById('result').textContent.slice(0, 60));
    dom.window.close();
  }

  console.log('== 6. MDQ 阳性（文本判定）==');
  {
    const dom = load('tools/psychiatry/mdq-bipolar.html');
    const w = dom.window, d = w.document;
    await ready();
    click(w, d.getElementById('pk-start'));
    answerRows(w, d, () => 0);
    await ready();
    const res = d.getElementById('result');
    const hotline = !!res.querySelector('.pk-hotline');
    ok('MDQ 阳性判定与热线一致', (res.textContent.indexOf('筛查阳性') >= 0) ? hotline : !hotline,
      res.textContent.slice(0, 60));
    dom.window.close();
  }

  console.log('== 7. 娱乐类标识（不加热线）==');
  {
    const dom = load('tools/psychology/tester-2.html');
    const d = dom.window.document;
    await ready();
    const tag = d.querySelector('.pk-tag');
    ok('MBTI 页有娱乐标识', !!tag && tag.textContent.includes('娱乐测试'), tag ? tag.textContent : '无标识');
    ok('娱乐页无热线横幅', !d.querySelector('.pk-hotline'));
    dom.window.close();
  }
  {
    const dom = load('tools/psychology/holland-career-test.html');
    const d = dom.window.document;
    await ready();
    const tag = d.querySelector('.pk-tag');
    ok('霍兰德页有职业参考标识', !!tag && tag.textContent.includes('职业方向参考'), tag ? tag.textContent : '无标识');
    dom.window.close();
  }
  {
    const dom = load('tools/psychology/random-12.html');
    const d = dom.window.document;
    await ready();
    ok('认知偏差卡片页未注入 kit', !d.querySelector('.pk-tag') && !d.getElementById('pk-progress'));
    dom.window.close();
  }

  console.log('== 8. 纯前端自检 ==');
  {
    const src = fs.readFileSync(path.join(ROOT, 'js', 'psych-kit.js'), 'utf8');
    ok('无 fetch/XMLHttpRequest', !/\bfetch\s*\(|XMLHttpRequest/.test(src));
    ok('仅使用 localStorage 存储', !/sessionStorage|indexedDB|document\.cookie/i.test(src));
    let injected = 0;
    for (const ind of ['psychiatry', 'psychology']) {
      for (const f of fs.readdirSync(path.join(ROOT, 'tools', ind))) {
        if (!f.endsWith('.html')) continue;
        try { if (/psych-kit\.js/.test(fs.readFileSync(path.join(ROOT, 'tools', ind, f), 'utf8'))) injected++; } catch (e) { }
      }
    }
    ok('注入页面数 >= 40', injected >= 40, '实际 ' + injected);
  }

  console.log('\n结果：' + pass + ' 通过 / ' + fail + ' 失败');
  process.exit(fail ? 1 : 0);
})();
