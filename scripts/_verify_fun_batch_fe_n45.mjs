// 两态锁：FE-N45 太空射击深度解析算例与真实计分/道具一致（内容源修复，改 i18n 后由构建注入）
// 用法：node scripts/_verify_fun_batch_fe_n45.mjs [--head]
//   --head 用 git show HEAD:tools/fun/space-shooter.html 取修复前构建产物，验证旧算例确实还在（判别力）。
import { execSync } from 'child_process';
import fs from 'fs';

const file = 'tools/fun/space-shooter.html';
const head = process.argv.includes('--head');
const html = head ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');

let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };

// —— 1. 页面真实计分档位（源码常量）——
const types = [...html.matchAll(/(normal|fast|tough):\s*\{[^}]*score:\s*(\d+)/g)].map(m => [m[1], Number(m[2])]);
const scoreMap = Object.fromEntries(types);
assert(scoreMap.normal === 10 && scoreMap.fast === 20 && scoreMap.tough === 30,
  `敌机计分档位应为 normal=10 / fast=20 / tough=30；实际=${JSON.stringify(scoreMap)}`);

// —— 2. 页面是否真无「加速/射速翻倍」——
const hasSpeedBoost = /射速翻倍|加速道具|速度道具/.test(html);
assert(!hasSpeedBoost, `页面不得再宣称「射速翻倍/加速道具」（实际无此机制）；命中=${hasSpeedBoost}`);

// —— 3. 深度解析算例必须与真实档位一致 ——
const dd = (html.match(/<div class="dd-example">[\s\S]*?<\/div><\/div>/g) || []).join('');
const hasOldExample = /吃加速道具后射速翻倍|8 架各 15 分|累计 170 分/.test(dd);
assert(!hasOldExample, `深度解析算例不得残留旧版（加速道具 / 8 架各 15 分 / 累计 170 分）`);

const citesAllTiers = [10, 20, 30].every(n => new RegExp(`各 ${n} 分|${n} 分`).test(dd));
assert(citesAllTiers, `算例应引用真实三档分值 10/20/30；实际算例=「${dd.slice(0, 160)}」`);

const citesPowerups = /三连射/.test(dd) && /护盾/.test(dd) && /加命/.test(dd);
assert(citesPowerups, `算例应说明真实三种道具（三连射/护盾/加命）；实际算例=「${dd.slice(0, 160)}」`);

// 算例是随机连续生成中的假设击毁数量，而非固定波次。
const source = JSON.parse(head ? execSync('git show HEAD:i18n/tools/content_deepdive.json', { maxBuffer: 32 * 1024 * 1024 }).toString() : fs.readFileSync('i18n/tools/content_deepdive.json', 'utf8'))['fun/space-shooter'];
const en = JSON.parse(head ? execSync('git show HEAD:i18n/tools/en/fun/space-shooter.json').toString() : fs.readFileSync('i18n/tools/en/fun/space-shooter.json', 'utf8'));
const [method, example] = source.examples.map(item => item.body);
assert(!/波次|第\s*\d+\s*波|混编波|全清/.test(method + example), '方法与算例不得声明固定波次或清波机制');
assert(/随机/.test(method) && /持续|连续/.test(method) && /随机|假设/.test(example), '方法说明随机连续生成，算例明确为假设');
assert(/enemySpawnTimer\s*-=/.test(html) && /Math\.random\(\)/.test(html) && /Math\.floor\(score\s*\/\s*500\)/.test(html), '实际机制为计时生成随机敌机、每 500 分升级');
assert(/5 架普通/.test(example) && /2 架快速/.test(example) && /2 架厚甲/.test(example) && scoreMap.normal * 5 + scoreMap.fast * 2 + scoreMap.tough * 2 === 150 && /150 分/.test(example), '假设击毁数量与真实分值累计为 150 分');
assert([method, example].every(text => dd.includes(text) && typeof en.map[text] === 'string' && !/\bwaves?\b/i.test(en.map[text])), '构建页面与源文一致，英文翻译匹配且不引入波次');

if (failures > 0) { console.log(`\n[${head ? 'HEAD' : '当前'}] N45 锁 FAIL (${failures})`); process.exit(1); }
console.log(`\n[${head ? 'HEAD' : '当前'}] N45 锁 PASS`);
