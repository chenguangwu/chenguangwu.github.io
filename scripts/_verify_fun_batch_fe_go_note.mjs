// 两态锁：围棋数子法「目/子」单位混用（go-territory）+ 音符转换非法输入后仍复制旧结果（freq-note-converter）
// 用法：node scripts/_verify_fun_batch_fe_go_note.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const loadHtml = (f) => head ? execSync(`git show HEAD:${f}`).toString() : fs.readFileSync(f, 'utf8');

function boot(html, beforeParse) {
  return new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://example.test/',
    beforeParse(w) {
      w.__copied = [];
      w.ToolBox = {
        copyText: (t) => w.__copied.push(String(t)),
        showToast() {}, downloadText() {}, showError() {}, toggleToolTheme() {}
      };
      w.i18nText = (k) => String(k);
      w.TBKit = { util: { isEn: () => false }, history: { record() {}, last: () => null, list: () => [], mount() {} }, matrix: { table() {} }, chart: { line() {} } };
      if (beforeParse) beforeParse(w);
    }
  });
}

// ============ A. 围棋：中国规则贴子单位 ============
{
  const dom = boot(loadHtml('tools/chess/go-territory.html'));
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  const $ = (id) => w.document.getElementById(id);
  if (typeof w.calc !== 'function') {
    console.log('  ✗ calc 不可见，围棋锁无法判定'); failures++;
  } else {
    // 切到中国规则（数子法）并填入活子
    $('method').value = 'chinese';
    w.toggleMethod();
    $('komi').value = '7.5';        // 贴 7.5 目 = 3.75 子
    $('blackTerritory').value = '50';
    $('blackStones').value = '90';  // 黑 = 50 + 90 = 140 子
    $('whiteTerritory').value = '48';
    $('whiteStones').value = '85';  // 白 = 48 + 85 + 3.75 = 136.75 子
    w.calc();

    const res = ($('result').textContent || '').replace(/\s+/g, ' ');
    const grid = ($('dataGrid').textContent || '').replace(/\s+/g, ' ');

    assert(/黑方胜/.test(res), `贴 7.5 目时黑 140 子 vs 白 136.75 子应判黑胜；实际结果=「${res.slice(0, 90)}」`);
    assert(/6\.5/.test(res) && /目差/.test(res),
      `子差 3.25 应折算为目差 6.5 目；实际结果=「${res.slice(0, 90)}」`);
    assert(/黑方子数/.test(grid) && /贴子/.test(grid),
      `中国规则卡片应标「黑方子数/贴子」而非「黑方总目/贴目」；实际卡片=「${grid}」`);
    assert(/3\.75 ?子/.test(res) || /3\.75 ?子/.test(grid),
      `贴子应显示为 3.75 子（= 7.5 目）；实际结果=「${res.slice(0, 120)}」`);
  }
  dom.window.close();
}

// ============ B. 音符转换：非法输入不得复制旧结果 ============
{
  const dom = boot(loadHtml('tools/music/freq-note-converter.html'));
  const w = dom.window;
  await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await sleep(60);

  const $ = (id) => w.document.getElementById(id);
  if (typeof w.calcFreq2Note !== 'function' || typeof w.copyResult !== 'function') {
    console.log('  ✗ calcFreq2Note/copyResult 不可见，音符锁无法判定'); failures++;
  } else {
    // 先算出有效结果（440 Hz），再清空输入触发错误分支
    $('freqInput').value = '440';
    w.calcFreq2Note();
    const firstCopy = $('freq2note').dataset.copyValue || '';
    assert(/440/.test(firstCopy), `440 Hz 应写入复制值；实际=「${firstCopy}」`);

    $('freqInput').value = '';
    w.calcFreq2Note();
    w.__copied.length = 0;
    w.copyResult('freq2note');
    assert(w.__copied.length === 0,
      `输入非法后再点复制不应复制任何内容（旧值已失效）；实际复制了 ${w.__copied.length} 次：「${w.__copied[0] || ''}」`);

    // 恢复有效输入后应可正常复制新值
    $('freqInput').value = '880';
    w.calcFreq2Note();
    w.__copied.length = 0;
    w.copyResult('freq2note');
    assert(w.__copied.length === 1 && /880/.test(w.__copied[0]),
      `恢复有效输入后复制应得到新值（880）；实际=「${w.__copied[0] || ''}」`);
  }
  dom.window.close();
}

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] 围棋/音符 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] 围棋/音符 锁 PASS`);
