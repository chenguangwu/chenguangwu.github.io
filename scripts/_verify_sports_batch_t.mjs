// scripts/_verify_sports_batch_t.mjs — SF-N119/120/121 网球得分率分析 T 批运行期证据
//
// SF-N119（高）：原校验只标红不中止，指数可破 100。复现：总发球分 100/ACE 8/双误 4/一发 65%/面对 2/挽救 10
//            ⇒ 挽救率 500%、效率 193.5、判「优秀」；ACE 填 100（总 10）⇒ ACE 率 1000%。
//            修复：valid 含 ace<=total、df<=total、bs<=bf，不通过即中止、不输出指数。
// SF-N120（承诺未实现）：标题「得分率」无任何输入/输出。原仅读 total/ace/df/firstIn/bpFace/bpSave 六项。
//            修复：新增一发得分 p1w、二发得分 p2w、全场总得分 rt、本方全场得分 rw，输出一发/二发/总 得分率。
// SF-N121（中）：破发点面对 0 记 100%、0/0 白送 30 分。原 bf>0?bs/bf*100:100 占 0.30 权重。
//            修复：bf=0 时挽救率显示「—」并从综合指数剔除、其余权重按比例归一。
// 用法：node scripts/_verify_sports_batch_t.mjs [--head]（--head 读 HEAD 版做回退判别）
import { readFileSync } from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM, VirtualConsole } from 'jsdom';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HEAD = process.argv.includes('--head');
const read = (rel) => HEAD
  ? execFileSync('git', ['show', 'HEAD:' + rel], { cwd: ROOT, encoding: 'utf8', maxBuffer: 30e6 })
  : readFileSync(path.join(ROOT, rel), 'utf8');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + detail : '')); }
}

async function loadPage(rel) {
  const html = read(rel);
  const vc = new VirtualConsole();
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'https://x.test/' + rel,
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(w) {
      const noop = () => {};
      const kit = {
        util: { isEn: () => false, diffBox: noop, exportTable: noop, showToast: noop, copyText: noop, downloadText: noop,
          setResult: (id, v) => { const e = w.document.getElementById(id); if (e) e.innerHTML = v; } },
        history: { list: () => [], last: () => null, record: noop, mount: noop, clear: noop },
        preset: { bar: noop },
        chart: { line: noop, bar: noop, pie: noop, gauge: noop, scatter: noop, timeline: noop, bell: noop, histogram: noop, rangeBar: noop, refBar: noop },
        matrix: { table: noop }, copyText: noop, downloadText: noop, showToast: noop,
      };
      w.TBKit = kit; w.ToolBox = kit;
      w.i18nText = (k) => (typeof k === 'string' ? k : '');
      try { w.alert = noop; w.confirm = () => true; } catch (e) {}
    },
  });
  await new Promise((r) => setTimeout(r, 200));
  return dom.window;
}

// ── SF-N119 / N120 / N121：wangqiudefenlvfenxi ──
{
  const REL = 'tools/sports/wangqiudefenlvfenxi.html';
  const w = await loadPage(REL);
  const doc = w.document;
  const txt = () => doc.getElementById('res').textContent.replace(/\s+/g, ' ').trim();
  const has = (id) => !!doc.getElementById(id);
  const setIn = (o) => {
    for (const k of ['total', 'ace', 'df', 'firstIn', 'p1w', 'p2w', 'rt', 'rw', 'bpFace', 'bpSave']) {
      if (o[k] !== undefined && has(k)) doc.getElementById(k).value = o[k];
    }
    if (w.calc) w.calc();
  };

  // SF-N119：ACE 超过总发球分 ⇒ 必须中止（HEAD 无此校验，会算出破百指数）
  setIn({ total: '10', ace: '100', df: '4', firstIn: '65', p1w: '5', p2w: '2', rt: '10', rw: '5', bpFace: '2', bpSave: '1' });
  check('SF-N119 ACE=100/总10（原 ACE 率 1000%、指数破百）⇒ 中止提示，不输出指数',
    /请填写有效数据/.test(txt()) && !/发球表现：/.test(txt()), txt().slice(0, 160));

  // SF-N119：挽救超过面对 ⇒ 必须中止（原 500% 挽救率、193.5 指数）
  setIn({ total: '100', ace: '8', df: '4', firstIn: '65', p1w: '45', p2w: '18', rt: '140', rw: '63', bpFace: '2', bpSave: '10' });
  check('SF-N119 挽救10/面对2（原 500% 挽救率、193.5 指数）⇒ 中止提示',
    /请填写有效数据/.test(txt()), txt().slice(0, 160));

  // SF-N120：一发/二发得分率应算出（HEAD 无 p1w/p2w 字段，--head 下 skip）
  if (has('p1w') && has('p2w')) {
    setIn({ total: '100', ace: '8', df: '4', firstIn: '60', p1w: '50', p2w: '18', rt: '140', rw: '63', bpFace: '6', bpSave: '4' });
    check('SF-N120 一发得分率 = 50/60 ⇒ 83.3%、二发得分率 = 18/40 ⇒ 45.0%',
      /83\.3%一发得分率/.test(txt()) && /45\.0%二发得分率/.test(txt()), txt().slice(0, 200));
    // 总得分率：本方 63 / 全场 140 ⇒ 45.0%
    check('SF-N120 总得分率 = 63/140 ⇒ 45.0%', /45\.0%总得分率/.test(txt()), txt().slice(0, 200));
  } else {
    check('SF-N120（HEAD 无 p1w/p2w 字段，跳过）', false, 'HEAD 版无得分率字段');
  }

  // SF-N121：破发点面对 0 ⇒ 挽救率「—」且从指数剔除
  setIn({ total: '100', ace: '8', df: '4', firstIn: '65', p1w: '45', p2w: '18', rt: '140', rw: '63', bpFace: '0', bpSave: '0' });
  check('SF-N121 面对0（原记 100% 白送 30 分）⇒ 挽救率「—」且「已从综合指数中剔除」',
    /—破发点挽救率/.test(txt()) && /已从综合指数中剔除/.test(txt()), txt().slice(0, 200));

  // SF-N121 对照：有破发点样本时不出现「剔除」文案
  setIn({ total: '100', ace: '8', df: '4', firstIn: '65', p1w: '45', p2w: '18', rt: '140', rw: '63', bpFace: '6', bpSave: '4' });
  check('SF-N121 对照（面对6/挽救4）⇒ 不出现「剔除」、挽救率非「—」',
    !/已从综合指数中剔除/.test(txt()) && !/— 破发点挽救率/.test(txt()), txt().slice(0, 200));
}

console.log(`\n==== batch_t ${HEAD ? '(HEAD 回退)' : '(当前)'} ==== ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
