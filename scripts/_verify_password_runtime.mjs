#!/usr/bin/env node
/**
 * IT-N536～N538 密码强度页运行期回归 + 英文态动态串零残留。
 *
 * 为什么不用 verify_it_calc.js：该 harness 是简化桩、不注入 TBKit，无法覆盖
 * ① 英文态（TBKit.util.isEn()=true）下动态结果串是否漏中文；
 * ② formatTime() 的「天/年/千年」等长单位是否随语言切换。
 * 这里用 jsdom 真机执行页面内联脚本，与线上同一份源码。
 *
 * 用法：
 *   node scripts/_verify_password_runtime.mjs                  # 当前工作区
 *   git show HEAD:tools/it/password-strength.html > /tmp/head.html
 *   node scripts/_verify_password_runtime.mjs /tmp/head.html   # 回退源码判别力实测
 * 退出码：0 全通过；1 有失败项。
 */
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = resolve(process.argv[2] || resolve(ROOT, 'tools/it/password-strength.html'));
const CJK = /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/g;
const HAS_CJK = /[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/;
function noCJK(t) { return !HAS_CJK.test(t); }
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  —  ' + detail : ''}`);
}

async function load(lang, pwd) {
  const dom = new JSDOM(readFileSync(SRC, 'utf8'), {
    url: `https://toolbox.local/tools/it/password-strength.html?lang=${lang}`,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(w) {
      w.TBKit = { util: { isEn: () => lang === 'en-US' }, chart: {}, showToast: () => {} };
      w.ToolBox = { showToast: () => {} };
    },
  });
  const w = dom.window;
  await new Promise((r) => {
    if (w.document.readyState !== 'loading') return r();
    w.addEventListener('DOMContentLoaded', r);
    setTimeout(r, 1500);
  });
  await new Promise((r) => setTimeout(r, 250));
  w.document.getElementById('pwd').value = pwd;
  try { w.check(); } catch (e) { console.log('  check() threw: ' + e.message); }
  const text = (id) => (w.document.getElementById(id)?.textContent || '');
  return { crack: text('crackText'), feedback: text('feedback'), table: text('pwdTable'), label: text('label') };
}

// ---- N536：三档标签与除数一致；长单位也须双语 ----
{
  const zh = await load('zh-CN', 'abc123测试');
  check('N536 在线档 10 亿次/秒 ⇒ 48 bit 约 3 天', zh.crack.includes('在线破解（10亿次/秒）：') && zh.crack.includes('3 天'), zh.crack.slice(0, 60));
  check('N536 离线/超算档分别快 100 / 1000 倍', zh.crack.includes('46 min') || zh.crack.includes('46 分钟') || zh.crack.includes('46 分'), zh.crack.slice(0, 140));
  const en = await load('en-US', 'abc123测试');
  check('N536 英文态长单位无中文（天/年/千年）', noCJK(en.crack) && noCJK(en.feedback) && noCJK(en.table) && noCJK(en.label),
    `crack=${JSON.stringify(en.crack.slice(0, 90))}`);
  check('N536 英文态三档标签齐备', en.crack.includes('Online crack (1e9 guesses/s)') && en.crack.includes('Offline GPU (1e11 guesses/s)') && en.crack.includes('Supercomputer (1e12 guesses/s)'));
}
// ---- N537：公式承诺的熵判读必须单列输出 ----
{
  const zh = await load('zh-CN', 'a'.repeat(32));
  check('N537 32 个 a（150 bits）⇒ 熵判读「极强」单列', zh.crack.includes('熵判读（150 bits）：') && zh.crack.includes('极强'), zh.crack.slice(-60));
  const en = await load('en-US', 'a'.repeat(32));
  check('N537 英文态熵判读无中文', en.crack.includes('Entropy verdict (150 bits): Very strong'));
}
// ---- N538：中段键盘序列也要命中 ----
{
  const zh = await load('zh-CN', 'xxqwe123');
  check('N538 中段 qwe 命中风险提示（中文态）', zh.feedback.includes('⚠️ 包含键盘连续序列（如123、abc、qwe）'));
  const en = await load('en-US', 'xxqwe123');
  check('N538 中段 qwe 命中风险提示（英文态）', en.feedback.includes('Keyboard sequence (e.g. 123, abc, qwe)'));
}
// ---- 英文态全容器零 CJK ----
{
  const en = await load('en-US', 'ToolBox@2026');
  for (const [k, t] of Object.entries(en)) {
    const hits = [...new Set(t.match(CJK) || [])].join('');
    check(`EN 零 CJK：${k}`, !hits, hits);
  }
}

const pass = results.filter((r) => r.ok).length;
console.log(`\n==== ${pass}/${results.length} 通过 ====`);
process.exit(pass === results.length ? 0 : 1);
