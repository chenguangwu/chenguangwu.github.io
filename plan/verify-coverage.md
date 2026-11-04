# verify 用例覆盖台账

> 生成日期：2026-11-05（口径修正版）| 口径：工具页 = `tools/<dir>/*.html` **排除各行业 `index.html`**（分类落地页不含 calc 逻辑）；已覆盖 = 该页 slug 出现在 `scripts/` 下任一 `verify_*` 文件的 `slug` 键中（`"slug"` 与 `slug` 两种写法均计）。

## 总览

| 指标 | 数值 |
|---|---|
| 工具页总数（排除 index） | 4705 |
| 至少 1 条用例覆盖 | 4563（97.0%） |
| 零用例页 | 142（3.0%） |
| 存在零用例页的目录 | 36 |

## 零用例页按目录（页数降序）

| 目录 | 零用例页数 | 目录总页数 | slug |
|---|---|---|---|
| `fun` | 39 | 54 | 1a2b-guess, zodiac-match, othello, daily-riddle, tic-tac-toe, space-shooter, breakout, tongue-twister, sequence-puzzle, snake-game, blood-type-personality, generator-laugh, keyboard-heatmap, sequence-memory, color-guess, hangman, coin-flip, pong, riddle-generator, number-puzzle, rock-paper-scissors, gomoku-ai, emoji-memory, bingo-generator, tetris, word-scramble, memory-game, solitaire, sliding-puzzle, gomoku, generator-2, 2048-game, pattern-memory, minesweeper, shape-memory, generator-3, color-memory, random-name-gen, fingerprint-types |
| `it` | 24 | 338 | ksuid-generator, regex, device-info, pdf-signature-checker, ulid-generator, generator-16, gamertag-generator, ecdsa, tiny-url, less-compiler, benchmark-builder, aes-encryptor, uuid-v7-generator, random-port-generator, typing-test, token-generator, nickname-generator, short-link-generator, team-name-generator, html-to-markdown, keycode-info, uuid-v4-generator, camera-recorder, typescript-compiler |
| `edu` | 11 | 44 | color-quiz, capital-quiz, math-quiz, reminder-1, multiplication-table, country-quiz, flashcards, number-memory, typing-game, flag-quiz, countdown-5 |
| `ai` | 6 | 64 | speech-to-text, text-summarization, sentiment-analysis, ai-text-summarizer, image-classification, ocr |
| `psychology` | 6 | 20 | enneagram-test, analysis-2, bigfive-personality-test, bubble-tea-personality-quiz, tester-3, scl90-assessment |
| `audio` | 4 | 8 | audio-speed, audio-recorder, audio-echo, audio-volume |
| `biz` | 4 | 69 | motto-generator, app-name-generator, brand-name-generator, product-name-generator |
| `design` | 4 | 108 | image-rotator, font-pairing, image-color-picker, palette-extractor |
| `health` | 4 | 40 | stretch-generator, dysphagia-food-guide, symptom-checker, rehab-timer |
| `marketing` | 4 | 45 | funnel-calculator, tagline-generator, hashtag-generator, slogan-generator |
| `ophthalmology` | 3 | 31 | ishihara-test, astigmatism-chart, pupil-reflex |
| `science` | 3 | 92 | logic-gate-simulator, periodic-table, calculator |
| `agriculture` | 2 | 64 | countdown-4, countdown-cycle |
| `food` | 2 | 24 | cooking-converter, beer-gravity-estimator |
| `language` | 2 | 17 | ipa-practice, riyuwushiyintulianxi-dianjifayin |
| `life` | 2 | 70 | holiday-calendar, event-countdown |
| `office` | 2 | 6 | pdf-merge, flowchart |
| `usedcar` | 2 | 12 | checker-3, rater-37 |
| `accessibility` | 1 | 5 | accessible-restroom |
| `acupuncture` | 1 | 22 | acupoint-combination |
| `aerospace` | 1 | 37 | weight-balance |
| `astronomy` | 1 | 23 | solar-elevation |
| `eco` | 1 | 39 | noise-superposition |
| `finance` | 1 | 115 | word-search |
| `geology` | 1 | 36 | calc-1 |
| `image` | 1 | 14 | image-converter |
| `legal` | 1 | 48 | calendar |
| `metalwork` | 1 | 39 | detector-55 |
| `music` | 1 | 20 | detector |
| `obstetrics` | 1 | 27 | pcos-rotterdam |
| `optical` | 1 | 40 | driving-lens |
| `reproductive-medicine` | 1 | 25 | assessor-15 |
| `safety` | 1 | 15 | self-test |
| `security` | 1 | 11 | passphrase-generator |
| `wedding` | 1 | 9 | countdown-time |
| `yi` | 1 | 5 | gua-interpretation |

## 说明

- 旧版台账把 `index.html` 计入分母、且 slug 匹配未归一，导致「117 目录整目录零覆盖 1492 页」的结论失真（实际 0 个整目录零覆盖，零用例最集中的目录也只有少量页）。
- `clinical-nursing/**` 由临床线在途，本台账只统计、不在本线改动。

## 用例期望值标准（2026-11-05 定稿）

> **用例的期望值必须能被第三个人手算复现。** 只有页面自己算得出来的“期望值”不是用例，是快照——页面错了快照跟着错，永远绿。

- 写法：先在 `ref` 里写独立复算式，再取页面同口径输出比对；`ref` 必须给出输入、公式、中间量、结果与默认态差异。
- 示例（本批已落地）：`beer-gravity-estimator` OG = 1 + 37×8×2.20462×0.75/5.28344/1000 = 1.093；`solar-elevation` sin h = sin40°sin23.45° + cos40°cos23.45°cos(-4.5°) = 0.9563 ⇒ 73.03°；`noise-superposition` 10·lg(10^9 + 10^7) = 100.04 ⇒ 100.0 dB；`calc-1` RQD = 1010/(2×1000)×100 = 50.5%。
- 动态 `innerHTML` 生成的输入：允许「真实公式 + 显式注入 + `ref` 写明桩不解析 innerHTML 的原因」，不得硬凑一个“能跑通”的假输入。

## 工作量归因（2026-11-05）

- `general` / `fun` / `agriculture` / `geology` / `metalwork` 5 个分类红已由他线修复；本线仅复核全绿（361/361、19/19、177/177、55/55、71/71，逃生 0），**归因他线，本线未重复动**。

## fun 39 个零用例页三分类（2026-11-05）

口径：满足任一豁免条件才可豁免，且须在用例 `ref` 写明编号——① 输出无确定性锚（仅 `Math.random`/`Date.now`/外部文件，且无“固定输入→固定输出”路径）；② 纯媒体输出（仅 canvas/audio，无稳定文本数值；**有元数据则必须测**）；③ 纯静态内容页（无计算，应从覆盖率统计剔除）。**有分数/步数/计时/生成数量/词数等确定性输出者一律不得豁免。**

| 类别 | 页数 | 清单 |
|---|---|---|
| 可正常测 | 5 | `keyboard-heatmap`（`loadSample()` 两次 ⇒ 总按键 90；单次 45 = 字母 35 + 空格 9 + 句点 1，唯一 28）、`coin-flip`（钉随机后掷 3 次 ⇒ 正面率 33.3%）、`generator-2`（cnt=10 ⇒ `#10 数独`）、`generator-3`（cnt=10 ⇒ `#10 迷宫`）、`generator-laugh`（cnt=10 ⇒ 第 10 条笑声文本） |
| 该测但难注入 | 30 | `1a2b-guess`、`zodiac-match`、`othello`、`daily-riddle`、`tic-tac-toe`、`space-shooter`、`breakout`、`tongue-twister`、`sequence-puzzle`、`snake-game`、`sequence-memory`、`color-guess`、`hangman`、`pong`、`number-puzzle`、`rock-paper-scissors`、`gomoku-ai`、`emoji-memory`、`tetris`、`word-scramble`、`memory-game`、`solitaire`、`sliding-puzzle`、`gomoku`、`2048-game`、`pattern-memory`、`minesweeper`、`shape-memory`、`color-memory`、`random-name-gen` |
| 豁免 | 4 | ① `riddle-generator`（题库纯随机、无计数/数值文本）、`bingo-generator`（随机号码卡、无尺寸/数量文本）；③ `blood-type-personality`、`fingerprint-types`（纯静态内容页，无计算） |

- 上表“可正常测”5 页已补进 `scripts/verify_fun_calc.js`（2026-11-05，见下节）；C 类 5 条全部为 click/inputs 驱动，默认态不命中。
- 其余 30 页均有分数/步数/计时/胜负数等确定性语义，只因棋盘 canvas、随机对手或动态棋盘点击在现有桩中难以注入而暂列 B 类，**不得整类豁免**。

## 2026-11-05 红 1 修复 + C 类 5 页落地

### `anti-regression: case discrimination` 跳过 54 > 基线 51

| 用例 | 根因 | 修法 |
|---|---|---|
| `metalwork/detector-55` | 18 个 `m{m}_{i}` 下拉由 `innerHTML` 运行期生成，`pageDefaults` 取不到 ⇒ `unresolved` ⇒ 跳过 | 改为 **clicks-only**：在页面作用域内逐个置「完全执行(2)」后调 `calc()`，expect 只认 100%/优秀 |
| `usedcar/checker-3` | 同上，`ck_<key>` 运行期生成；且页面 init 末尾直接 `calc()`，空值会 `statusOpts.find()` 返回 undefined 抛错 | **inputs 注入全部 `ck_*`（合法档位、让 boot calc 不抛错）+ clicks 改档重算**；expect 只认 click 后的分数（86 分 / 严重问题 1 项），判别器清空 clicks 后只能复现注入态全优分 100 ⇒ 失配 |
| `usedcar/rater-37` | 同上 | 同上：注入全「优秀(5)」让 boot 得 100 分，clicks 把 4 项改「严重(1)」⇒ 1540/27 = 57 分「一般」、发现 4 项问题；清空 clicks 后仍为 100 分 ⇒ 失配 |

- 结果：全站 `node scripts/discriminate_check.js` ⇒ **已检 9145 / 正确变红 9145 / 逃生 0 / 跳过 51 = 基线 51**（未上调基线）。
- 结论：动态 `innerHTML` 页不能只靠 `inputs`（会 skip），也不能只靠 `clicks` 写注入值（会是逃生项）；正确姿势是「inputs 保证 boot 可运行 + clicks 产生默认态无法复现的派生量」。

### C 类 5 页（`fun`）

- `keyboard-heatmap`：`loadSample();loadSample()` ⇒ 总按键 90（单次 45，累加函数；唯一 28 作锚会被兜底单次调用复现，已弃用）。
- `coin-flip`：`Math.random` 依次钉 0.1 / 0.9 / 0.9 掷 3 次 ⇒ 正面率 33.3%（兜底按种子序列掷 11 次得 72.7%，不命中）。**必须在 clicks 内保存并还原 `Math.random`**：harness 用全局种子 PRNG，钉成常量后不还原会让同进程后续随机类用例死循环（实测 4 个 verify 进程 100% CPU 空转）。
- `generator-2` / `generator-3` / `generator-laugh`：`cnt=10` ⇒ `#10 数独` / `#10 迷宫` / 第 10 条笑声。
- 判别结果：`verify_fun_calc.js` 24/24 正确变红、0 逃生、0 跳过。

### `verify input ids` 存疑 48 条（只读排查，未改）

- 由 49 降至 48：`metalwork/detector-55` 改为 clicks-only 后不再注入动态 id。
- **真·注入落空（3 条，待批后处理）**：
  - `agriculture/irrigation-uniformity` 的 `pt`：页面只生成 `pt0..ptN` 并读 `pt'+k`，裸 `pt` 从不被读取（该条为“自动补强”生成）；
  - `design/tester-assessor` 的 `sus`：页面生成 `sus0..sus9`，无 `sus` 元素（同属“自动补强”）；
  - `gastroenterology/ercp-success` 的 `cbd`：页面根本没有 CBD 字段（仅有 stoneSize/stoneCount/stonePos/purpose/surgery/priorEst/diverticulum），预设与用例都写 `cbd` 属空注入。
- 其余 45 条均为**运行期按模式生成、键名正确**（如 `id="tmax'+i+'"`、`id='m'+mi+'_'+ii`、`id="q${i}"`、`id="ck_'+it.key+'"`、`id="s-'+d.k+'"`、`id="${t.id}_${si}"`），属审计口径的“存疑”而非缺陷；已在生成语句逐条核对。
