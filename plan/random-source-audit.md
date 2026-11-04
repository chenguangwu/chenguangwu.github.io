# 全站随机数源审计（2026-11-05）

## 口径与范围

- **扫描对象**：`tools/**/*.html` + 运行时共享脚本 `js/tools/*.js`，不含 `zh-tw/`（构建产物）、`js/i18n.js`、`sw.js`。
- **基线**：审计开始时 **232 个工具页**含 `Math.random()`，共 **525 处**；共享脚本另 **2 个文件 / 9 处**（`js/tools/chinese-culture.js` 7 处、`js/tools/cognitive-assessment.js` 1 处 + 辅助 1 处）。
- **分档判据按页面用途，不按工具名**；一页同时存在多种用途时，按最高风险档归档（B > C > A > D）。
- **计数口径**：四档按**审计基线 232 页**计（A=183 / B=16 / C=8 / D=25）。修复后仍含 `Math.random` 的页面为 224 页（B 中 7 页已彻底移除随机、A 中 1 页改为确定性），因此「当前仍含随机」口径为 A=182 / B=9 / C=8 / D=25。
- 共享脚本 2 文件均为 **A 类**（随机取诗句/题目顺序），未改。

## 四档计数

| 档位 | 含义 | 页数 | 处置 |
|---|---|---|---|
| **A** | 功能必需随机（游戏、洗牌、抽取、随机出题、随机生成） | **183** | 保持 `Math.random`；凡声明「可复现/公开可复算」的页面逐页核对（见 §A 声明修正） |
| **B** | 密码学用途（密码、令牌、盐、验证码、UUIDv4、抽奖防预测） | **16** | **全部改为 `crypto.getRandomValues`**，无模偏差；不支持时显式提示，禁止回落 |
| **C** | 伪装随机（用随机数「生成」本应确定的数值） | **8** | 登记为假工具，给出重做/降级建议，本批未改 |
| **D** | 无害（本地唯一 ID、装饰抖动、示例初始化） | **25** | 不改 |
| 合计 | | **232** | |

## B 类：16 页（已全部修复）

统一实现：优先取 `crypto` / `window.crypto`；整数走**拒绝采样**（`limit = floor(2^32/max) * max`，`getRandomValues(Uint32Array(1))` 直到 `< limit`，再 `% max`），浮点走 `Uint32Array/2^32`；无 `crypto` 时写显式提示并停止（**不回落 `Math.random`**）。

| 页面 | 用途 | 当前源（修复前 → 修复后） | 档位 | 处置 |
|---|---|---|---|---|
| `tools/it/cuid-generator.html` | CUID 标识 | Math.random → `crypto.getRandomValues` | B | 已修；`generate()` 无 crypto 显式提示 |
| `tools/it/invite-code-generator.html` | 邀请码 | 同上 | B | 已修；保留装饰性 random（D） |
| `tools/it/pin-generator.html` | PIN 码 | 同上 | B | 已修 |
| `tools/it/nanoid-generator.html` | 短 ID / token | 同上 | B | 已修；`nanoid()` 直接 `getRandomValues(bytes)` |
| `tools/it/uuid-generator.html` | UUIDv4 | Math.random → `crypto` | B | 已修；移除随机回退，无 crypto 返回空并提示 |
| `tools/it/random-string.html` | 随机口令串 | Math.random → `crypto` + 逐字符拒绝采样 | B | 已修；同步更正说明与 en 字典 |
| `tools/it/password-generator.html` | 密码生成 | Math.random → `crypto` | B | 已修；`generateRandomPassword` 无 crypto 返回 `''` |
| `tools/it/captcha-generator.html` | 图形/批量验证码 | Math.random（含取字符）→ `crypto` | B | 已修；`generate()`/`batchGenerate()` 均加降级提示；噪点/弧线随机保留（D） |
| `tools/safety/manager.html` | 保险箱密码 | Math.random → `crypto` | B | 已修；`genPassword()` 提示 |
| `tools/safety/detector-strength.html` | 强度检测附带生成 | Math.random → `crypto`；`sort(()=>Math.random()-0.5)` → Fisher-Yates | B | 已修 |
| `tools/data/random-3.html` | 强密码批量生成 | Math.random → `crypto` + 拒绝采样 | B | 已修；**另修**：字符集含 `& < >`，原样拼 `innerHTML` 会被解析成标签，现统一 `escHtml` 转义 |
| `tools/data/random-4.html` | 验证码（数字/字母/混合） | Math.random → `crypto` | B | 已修（本批新发现） |
| `tools/security/virtual-safe.html` | 加盐 | Math.random → `crypto` | B | 已修；`genSalt()` 无 crypto 返回 `null`，调用处 toast 中止 |
| `tools/life/generator-strength.html` | 密码生成 | Math.random → `crypto` | B | 已修（本批新发现）；无 crypto 时结果区显式提示 |
| `tools/fun/raffle-picker.html` | 抽奖防预测 / 公开抽取 | Math.random 种子 → `crypto` 自动种子 | B | 已修；保留用户可填种子（可复算），留空时 crypto 生成；失败显式提示 |
| `tools/fun/random-picker.html` | 抽签防预测 | Math.random 种子 → `crypto` 自动种子 | B | 已修；同上 |

> **B 页残留 `Math.random` 说明**：`captcha`（17 处）、`random-string`（4）、`nanoid`（3）、`raffle`/`random-picker`（各 2）、`invite`/`pin`/`manager`/`virtual-safe`（各 1）仍有残留，但均为**装饰动画/噪点/唯一 ID 后缀**（D 类用途），不生成任何安全凭证。`cuid`/`uuid`/`password`/`detector`/`random-3`/`random-4`/`generator-strength` 已 0 残留。

## C 类：8 页（假工具，本批未改，仅登记）

| 页面 | 用途 | 当前源 | 档位 | 处置建议 |
|---|---|---|---|---|
| `tools/urban/building-height.html` | 建筑高度示意 | `Math.round(30+Math.random()*0)` 恒为 30 且未参与渲染（死随机） | C | 删死随机，改静态示例或接真实输入 |
| `tools/fitness/generator.html` | 训练计划「生成」 | 随机目标重量/组次/器械 | C | 改为按输入计算；或明示「示例数据」并去掉「生成」承诺 |
| `tools/food-testing/generator-27.html` | 微生物检验示例 | 随机样本/稀释度/菌落数 | C | 加样本/稀释度输入后计算，或标注示例 |
| `tools/electrical/generator-23.html` | 逻辑表达式化简 | 无表达式控件，随机抽 8 个预设真值表 | C | 补表达式输入并真实化简；否则改标题为「真值表速查」 |
| `tools/hematology/generator-analysis.html` | 血栓弹力图（TG）分析 | 随机 lag/TTP/peak/ETP | C | 接曲线数据输入后计算，或标注「模拟示例」 |
| `tools/finance/generator-report-1.html` | 三表生成 | 随机营收/成本/资产负债/现金流 | C | 按输入科目计算，或明确为演示数据 |
| `tools/realestate/generator-assessor.html` | 房产评估 | 随机评估价/面积/方法/因素 | C | 接可比案例/参数输入后计算 |
| `tools/data/generator-35.html` | 直方图生成 | 无数据输入，随机频数 | C | 接数据输入；或改「示例直方图」 |

## D 类：25 页（无害，不改）

用途均为**本地唯一 ID / 时间戳后缀 / 初始抖动 / 示例状态**，不参与对外结果。

`edu/exam-study-planner`、`edu/reminder-1`、`home/renovation-budget`、`home/furniture-layout`、`rental/reminder-4`、`ecommerce/cycle-15`、`usedcar/recorder-maintenance`、`office/pdf-merge`、`it/env-generator`、`it/json-formatter`、`property/cycle-elevator`、`edu2/wrong-book`、`wedding/seating-chart`、`life/countdown-timer`、`automotive/cycle-13`、`automotive/cycle-belt`、`safety/reminder-cycle-protection`、`pr/media-invite`、`pr/risk-assessment`、`pet/reminder-vaccine-deworming`、`funeral/ceremony-timeline`、`finance/register-depreciation`、`fitness/cycle-5`、`medical2/drug-expiry`、`decor/scheduler`。

## A 类：183 页（保持）+ 声明修正

### A 类页面分组清单（按行业，合计 183）

| 行业 | 页数 | 典型用途 | 页面（slug） |
|---|---|---|---|
| fun | 40 | 游戏、猜谜、随机出题、抽签动画 | 1a2b-guess, 2048-game, anagram-game, bingo-generator, breakout, coin-flip, coin-toss-streak, color-guess, color-memory, emoji-memory, generator-2, generator-24, generator-3, generator-laugh, gomoku, hangman, memory-game, minesweeper, number-guess, number-puzzle, pattern-memory, pong, random-name-gen, reaction-tester, riddle-generator, rock-paper-scissors, sequence-memory, sequence-puzzle, shape-memory, sliding-puzzle, snake-game, solitaire, space-shooter, tetris, tic-tac-toe, tongue-twister, typing-rhythm, whack-a-mole, word-scramble, zodiac-match |
| design | 14 | 配色/渐变/粒子随机生成 | color-palette, color-palette-generator, color-picker, farnsworth-d15-test, generator-10, generator-11, generator-12, generator-6, generator-7, generator-8, generator-9, gradient, mesh-gradient, particle-effect-generator |
| it | 14 | 随机串/名称/MAC/ULA/Lorem/混淆 | calc-3, chinese-name-generator, domain-name-generator, generator-16, hash-id-generator, ipv6-ula, js-obfuscator, lorem, mac-generator, mac-lookup, random, team-name-generator, typing-test, username-generator |
| edu | 13 | 题库顺序、单词/速记训练 | capital-quiz, color-quiz, country-quiz, english-vocabulary, flag-quiz, flashcards, generator-26, math-quiz, multiplication-table, number-memory, pinyin-typing-practice, typing-game, word-memory |
| biz | 9 | 文本打乱/Lorem/名称生成 | lorem-ipsum-advanced, name-generator, random-script, team-roster-generator, text-case-advanced, text-shuffle, text-sort, text-sort-advanced, zalgo-text |
| data | 9 | 随机数据集/图表样例 | chart-generator, data-cleaner, generator-14, generator-report, random-1, random-5, random-6, random-7, random-9 |
| music | 6 | 和弦/节奏随机练习 | chord-progression, ear-trainer, generator-1, music-player, random-training-rhythm, rhythm-trainer |
| language | 6 | 语言测验/发音练习 | german-gender-quiz, idiom-solitaire, ipa-practice, language-toolkit, riyuwushiyintulianxi-dianjifayin, vocabulary-builder |
| cognition | 5 | 认知测试题目顺序 | corsi-block-test, digit-span-test, nback-training, schulte-table, stroop-test |
| safety | 5 | 安全题库/随机场景 | generator-21, generator-hazard, random-13, safety-quiz, self-test |
| life | 4 | 随机价格/推荐 | generator-price, generator-random-1, number-to-chinese, recommender-8 |
| sports | 4 | 模拟/随机推荐 | generator-random-3, simulator-18, sports-reference, yoga-pose-generator |
| nutrition | 4 | 随机推荐/血糖负荷 | generator-glucose-load, recommender-2, recommender-3, recommender-4 |
| travel | 4 | 名称/推荐/瞄准训练 | aim-trainer, business-name-generator, recommender-10, recommender-9 |
| beauty | 3 | 配色/推荐 | nail-color-harmony, recommender-cycle, recommender-face-shape |
| rental | 2 | 生成器/推荐 | generator-32, recommender-5 |
| security | 2 | 卡片顺序/擦除模拟 | anti-fraud-cards, data-erase-simulator |
| acupuncture | 2 | 穴位/时辰推荐 | recommender-acupoint, recommender-time |
| psychology | 2 | 随机量表/题目 | generator-20, random-12 |
| food-testing | 2 | 生成器/排序 | generator-31, ingredient-sorter |
| yi | 2 | 起卦/解卦 | gua-interpretation, yi-divination |
| advertising | 2 | 颜色/时间生成 | color-convert, generator-time |
| ophthalmology | 2 | 视力表/色盲测试 | eye-chart-toolkit, ishihara-test |
| kids | 2 | 镜像字母/乘法练习 | mirror-letter, multiplication-practice |
| stats | 2 | 数据分布/回归示例 | data-distribution, regression-analysis |
| 其余 23 个单页行业 | 各 1 | 单页随机生成/推荐 | securities/technical-indicator, ent/temporal-resolution-hearing, meteorology/generator-30, quality/control-chart, energy/wind-power-estimator, general/recommender-24, health/stretch-generator, pet-training/clicker-timing, image/generator-15, geology/generator-37, tcm-diagnosis/generator-29, audio/audio-echo, fire/response-drill, ai/ai-prompt-generator, food/recipe-generator, finance/word-search, chinese/chinese-character, gardening/recommender, clinical-nursing/generator-pressure, text/lorem-ipsum-generator, service/script-template, legal/generator-17, seismology/generator-drill |

> 合计校验：40+14+14+13+9+9+6+6+5+5+4×4+3+2×10+23 = **183**。

### A 类声明修正（本批共 6 页）

| 页面 | 原声明 | 实际实现 | 处置 |
|---|---|---|---|
| `tools/it/hash-id-generator.html` | Hashids 为确定性编码 | `lottery` 取 `Math.random`，同输入每次不同 | **改为确定性**：`lottery` 由 `salt+输入` 的 FNV/31 乘哈希派生；verify 期望同步改为 `JKoJLgdr` |
| `tools/it/random.html` | 「可设种子复现」「密码学安全伪随机，不可预测」 | `Math.random`，无种子控件 | 更正为「每次结果独立随机、不可复现」「Math.random 伪随机、可预测，不可用于口令/令牌/密钥」；同步 `i18n/tools/it.json` |
| `tools/biz/text-shuffle.html` | 「可设随机种子复现」「记下种子」 | 有「固定种子（可复现）」勾选，但种子固定 12345 且不展示 | 更正为「可切换固定种子复现」；说明「固定种子不展示，需留档请导出结果」；同步 `i18n/tools/biz.json` |
| `tools/biz/team-roster-generator.html` | 「记住种子或导出结果即可复现」 | 无种子、不可复现 | 改为「每次结果不同且不可复现；如需留档请导出结果」 |
| `tools/fun/bingo-generator.html` | 「过程公开可复现、结果随机」 | 无种子、每次不同 | 改为「过程公开、结果随机且每次不同（不可复现，需留档请导出结果）」 |
| `tools/life/generator-random-1.html` | 「如 42（密码学安全随机）」 | `Math.random` | 改为「基于浏览器 Math.random，非密码学强度」 |

### A 类其他观察（未改）

- `tools/edu/generator-26.html` 定义了 `randInt()` 但 `gen()` 从未调用（死代码），页面实际确是「同输入同输出」；建议后续删除死函数，不影响功能。
- `tools/biz/text-shuffle.html` 的固定种子仅 12345，无法自定义；如需「公开种子抽签」应改为可输入/展示种子（当前已按事实降级描述）。
- 共享脚本 `js/tools/chinese-culture.js`（诗句/题目随机取用）与 `js/tools/cognitive-assessment.js`（题序随机）均为 A 类，无安全用途，保持不变。

## 验证与门禁

| 项目 | 结果 |
|---|---|
| `node scripts/verify_data_calc.js` | **27/27**（`data/random-3`、`random-4` 已改为格式/长度/字符集断言） |
| `scripts/discriminate_check.js verify_data_calc.js`（fidelity=1） | 已检 27 / 逃生 **0** |
| `verify_life_calc.js` | 提交版 315/315；工作树（含别线新增温度边界用例）322/322 |
| `verify_safety_calc.js` | 14/14 |
| `verify_security_calc.js` | 14/14 |
| `verify_fun_calc.js` | 19/19 |
| `verify_it_calc.js` | **提交版 985/985 全绿**；工作树另有别线未提交的 `DESTRUCTIVE` 正则改动，导致 `it/morse`、`it/rc4`、`it/xxtea` 3 条瞬时失败（HEAD 版 harness 跑同页全绿），与本批无关，未纳入提交 |
| `python3 _test_static.py` | 4705 通过 / 0 失败 / 0 告警 |
| 本批涉及 suite 的 scoped fidelity | **0 逃生**（data 27/27、life 322/322、safety/security/fun 全绿） |
| 全局 fidelity（`TB_STUB_FIDELITY=1`） | **8872 已检 / 0 逃生**（`verify_office_calc.js` 子进程静默退出，属既有隔离项，未计入） |
| `selfcheck_false_pass.js` | all_default 4 / baseline 4（无新增） |

## 交付与后续

- **已修改工具页 22 个**：B 类 16 + A 类声明/确定性 6（`hash-id-generator`、`random`、`text-shuffle`、`team-roster-generator`、`bingo-generator`、`generator-random-1`）。
- **mutation 边界**：B 类 16 页全部无 crypto 时显式提示，未静默回落。
- **i18n**：同步修改 `i18n/tools/it.json`、`i18n/tools/biz.json`、`i18n/tools/en/it/random-string.json`。按本次纪律**未跑 `_build.py`**，因此：
  1. 页面 `meta description` 与 `json/tools.json` 构建产物仍是旧文案，需下次构建刷新；
  2. `i18n/tools/en/**` 子树已改而 SW 版本戳未变，**下次上线前必须重跑 `python3 _build.py`**。
- **verify 期望**：B 类随机页一律改为「格式/长度/字符集/条数」结构断言，不再钉死具体随机值。
- **未处理**：C 类 8 页为假工具，按任务要求仅登记；建议优先处理 `electrical/generator-23`（名不副实）与 `data/generator-35`（无数据输入）。
