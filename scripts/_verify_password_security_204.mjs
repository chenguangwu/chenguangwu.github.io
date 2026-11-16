#!/usr/bin/env node
/**
 * _verify_password_security_204.mjs — 204 批复核失败裁断的安全口径证据脚本（独立专项，不入全量门禁 ratchet）。
 *
 * 裁断结论：password.html 明文密码写历史/趋势/导出的旧要求正式作废——
 *   ① 旧页已合并重定向至 life/generator-strength.html（提交 d58e5d690f），无 pwLen 等原入口；
 *   ② 目标页「关闭页面即清除密码」是正确安全口径，localStorage 只存选项配置、不存明文密码；
 *   ③ 等效安全功能由 finance/password-generator-advanced 提供：历史只存参数与掩码「未保存明文」。
 * 本脚本用静态源码断言锁定上述事实，防止后续改动把明文密码重新写回历史/趋势/导出。
 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(resolve(ROOT, p), 'utf8');

let pass = 0, fail = 0;
const check = (label, ok) => {
  if (ok) { pass++; console.log('PASS ' + label); }
  else { fail++; console.log('FAIL ' + label); }
};

// ① 旧页为重定向桩
const old = read('tools/finance/password.html');
check('旧页含 TOOLBOX-REDIRECT 桩标记', /TOOLBOX-REDIRECT/.test(old));
check('旧页 noindex 且 canonical 指向新页', /noindex/.test(old) && /generator-strength\.html/.test(old));
check('旧页无原 generatePW/pwLen 入口', !/function\s+generatePW|id=["']pwLen["']/.test(old));

// ② 目标页不持久化明文密码
const dst = read('tools/life/generator-strength.html');
check('目标页明示关闭页面即清除', /关闭页面即清除/.test(dst));
check('目标页 localStorage 仅存选项配置(键由 el.id 派生)', /localStorage\.setItem\(k\(el\.id\)/.test(dst));
check('目标页无 history.record 写明文密码', !/history\.record\s*\(/.test(dst));

// ③ 高级页历史只存参数与掩码
const adv = read('tools/finance/password-generator-advanced.html');
check('高级页历史掩码声明', /未保存明文/.test(adv) && /绝不写入生成的密码明文/.test(adv));
check('高级页无把密码明文写入 rec 的语句', !/rec\[rk\]\s*=\s*(allPwds|pwds|password|generatedPwd)/i.test(adv));

// ④ 验证脚本已移除失效用例、ROOT 可移植
const ver = read('scripts/_verify_finance_history_batch118.mjs');
check('batch118 已移除 password 失效用例', !/slug:\s*['"]password['"]/.test(ver));
check('batch118 ROOT 可移植推导', /fileURLToPath\(import\.meta\.url\)/.test(ver) && !/ROOT\s*=\s*['"]\/Users\//.test(ver));

console.log(`\n=== 204 安全口径证据 ${pass}/${pass + fail} | fail=${fail} ===`);
process.exit(fail ? 1 : 0);
