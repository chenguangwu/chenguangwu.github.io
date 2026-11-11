// 第 136 批真机回归：finance.md F-N17（六页英文结果标签缺键）。
// 清单证据为「疑似英文态残留中文，待探针」——本批用权威 EN i18n 探针逐页核实：
//   --check    英文态残留必须为 0（文本节点 + placeholder/title/aria-label/alt，排除 __tbL 运行时本地化串）
//   --roundtrip zh→en→zh 文本逐条一致（证明标签是正确翻译而非被删/误译）
// 探针与运行时共用 js/i18n.js + js/tool-i18n.js，零口径偏差。
// 结论：6 页均已是「已修未删条目」，不改源码、不重复加锁。
// 注：--smoke 的 ToolBox/resolveCanvasColor 报错系 jsdom 不加载外部 tool-kit.js，
//     zh/en 两态同形（各 5 页、同类错），与 i18n 无关，故不作为 PASS 判据。
import { execFileSync } from 'child_process';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const PROBE = 'scripts/_en_i18n_probe.mjs';
const SLUGS = [
  'housing-fund-loan', 'lease-payment-calculator', 'calc-2',
  'irr-calculator', 'investment-roi', 'dca-calculator',
];
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 240) : '')); }
}
function probe(args) {
  return execFileSync('node', [PROBE, ...args], { cwd: ROOT, encoding: 'utf8', env: { ...process.env, NODE_OPTIONS: '' } });
}

function main() {
  console.log('== F-N17 ① EN 态零残留 ==');
  for (const slug of SLUGS) {
    const out = probe(['--check', 'finance/' + slug]);
    const m = out.match(/有残留\s+(\d+)\s+页/);
    const bad = m ? Number(m[1]) : -1;
    check(slug + ' EN 零残留', bad === 0, out.trim().split('\n').slice(-3).join(' / '));
  }
  console.log('== F-N17 ② 往返一致（翻译非删除）==');
  for (const slug of SLUGS) {
    const out = probe(['--roundtrip', 'finance/' + slug]);
    const m = out.match(/不一致\s+(\d+)\s+页/);
    const bad = m ? Number(m[1]) : -1;
    check(slug + ' zh→en→zh 往返一致', bad === 0, out.trim().split('\n').slice(-3).join(' / '));
  }
  console.log(`\nBATCH136 ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main();
