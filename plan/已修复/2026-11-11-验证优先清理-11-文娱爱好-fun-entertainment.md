# 验证优先清理归档（仅含已验证修复记录）

来源：11-文娱爱好/fun-entertainment.md

- **复核 2026-11-07（陈旧证据，源码已正确，未改源码）**：当前 `calcPenalty(undertricks,doubled,vul)` 已实现完整阶梯——未加倍 50/100（无局/有局）；加倍无局 100/200/200/300…、有局 200/300…；再加倍整体 ×2。台账所指「有局加倍一律 200」已不存在（4♠有局加倍宕 2 = 200+300 = **500**，非 400）。补回归护栏 `scripts/_verify_chess_bridge_elo_lock.mjs`：抽取源码 `calcPenalty` 实跑 15 组标准值（含无局加倍宕4=800、有局再加倍宕2=1000、无局再加倍宕1=400）全部一致。移交：`plan/已修复/2026-11-07-FE-围棋单位与音符复制-含桥牌Elo复核.md`。
- **已修复（部分）2026-11-07**：活子输入与「缺活子不出结论」守卫此前已补（`blackStones/whiteStones` + 0/0 时拒绝计算）。本批修掉残留的**单位混用**：数子法把「贴目（目）」直接加到白方「子」数上，导致结果显示「140.0 目」而阈值行却按「180.5 + 贴目/2」判断，口径自相矛盾（极端情形直接翻转胜负：贴 7.5 目、黑 140 子对白 136.75 子，旧版判「白方胜 −0.5」）。
  - 现改为：数子法一律以「子」计——`komiZi = komi/2`（1 子 = 2 目，与页内深解「中国贴 3¾ 子 ≈ 7.5 目」一致），白方 = 活子 + 围空 + 贴子；目差 = 子差 × 2；卡片标签「黑方子数/白方子数」「贴子」，文案显示「贴子 3.75 子（= 7.5 目）」「黑方须超过 184.25 子方胜」。日本规则分支完全未动（既有 4 条 verify 契约保持 65.0/42.5/+22.5 不变）。
  - 判别力实测（`scripts/_verify_fun_batch_fe_go_note.mjs` A 节）：同一组输入 `komi=7.5 / 黑空50+活子90 / 白空48+活子85` → 当前「黑方胜、目差 +6.5、卡片=黑方子数 140.0 / 白方子数 136.8 / 贴子 3.75」（4 断言 PASS）；HEAD「白方胜、目差 −0.5、卡片=黑方总目 140.0 目 / 白方总目 140.5 目 / 贴目 7.5」（4 断言 FAIL）。移交同桥牌。
- **已修复 2026-11-07**：① 两个转换入口（`calcFreq2Note`/`calcNote2Freq`）取到 `box` 后**立即 `delete box.dataset.copyValue`**，旧结果不会跨非法输入存活；② `copyResult` 不再回退 `el.textContent`（原回退会把错误提示当调音数据复制），只在存在有效 `copyValue` 时复制，无值则静默不复制。判别力实测（`scripts/_verify_fun_batch_fe_go_note.mjs` B 节）：440 Hz 算出结果 → 清空输入再算 → 点复制——当前复制 0 次（PASS）/ HEAD 复制 1 次「A4 440.0000 Hz, 0.0 cents」（FAIL）；随后输入 880 恢复，两态均能复制到新值（守护断言）。移交同桥牌。
### FE-N5 BPM 反向时长只更新结果，数据表/历史/图表/CSV 保持旧值（低，确认源码缺陷 → **2026-11-07 已修复**）
- 描述：`calcReverse()` 只写 `#reverseResult`；历史扩展只在 `calcAll()` 外层包装里触发，改「时长/音符类型」不会记录，也不会刷新表格与图表。
- 证据：`tools/music/bpm-converter.html:658-699`（`calcReverse` 无扩展调用）、`:801-829`（`__bpm_converterExtras`）、`:838-840`（只包装 `calcAll`）、`:340`（表格/历史/图表宿主与反推结果同卡）。
- 影响：`tools/music/bpm-converter.html`；只用反推功能时历史为空、CSV 无内容、图表不更新。
- 方案：`calcReverse` 也调用同一记录函数，或把「记录」抽成两处共用的 `record()``；导出前校验表非空并提示。
- 修复（2026-11-07）：`calcReverse` 有效分支末尾调用 `__bpm_converterExtras()`（行 706 后），用 `typeof __bpm_converterExtras === 'function'` 守卫，避免页面初始化（IIFE 内行 731 首次 `calcReverse()` 时第二段脚本 `__bpm_converterExtras` 尚未定义）误调用报错；`reverseResult` 即 `.result-box`，被 `__bpm_converterResText` 采集，故反向结果会写进 `#bpm_converterTable`、历史、图表与 CSV。
- 验证说明（harness 盲区）：`scripts/verify_fun_calc.js` 的 harness **无法稳定验证本修复**——根因有二：① 页面 `calcReverse` 与 `__bpm_converterExtras` 分属两段 `<script>`，真实浏览器/JSDOM 下函数全局可见可调用；但 harness 把各段脚本隔离编译，跨段裸函数引用在 `calcReverse` 作用域内 `typeof` 为 `undefined`，守卫跳过 → 表格恒空；② 即便绕过，页面内部 1 秒节流 `now-__bpm_converter_last<1000` 与 harness 的 `FrozenDate`（`FIXED_NOW` 常量）叠加，注入后的第二次 `calcReverse` 必被节流。此属 harness 盲区，**非页面 bug**（JSDOM 真机已验证生效）。
- 实证（运行期两态，权威回归锁）：`scripts/_verify_fun_batch_fe_n5.mjs`（JSDOM 真机，等同浏览器双段同全局）。修复后：注入 `reverseMs=1000`/`quarter` → `matrix.table` 被调用、`#bpm_converterTable` 含列头 `reverseMs` 与结果 `60.00 BPM`、history 记录 1 条 ⇒ 1/1 通过；`--head` 回退旧版：表格恒空、history 0 条 ⇒ 1/1 通过。

### FE-N8 未识别后缀静默降级为大三和弦，常用降号根音被判无效（中，**2026-11-07 已修复**）
- 描述（原）：无法匹配的后缀直接回退 `[0,4,7]` 大三和弦，不报错；`Cb`/`Fb`/`E#`/`B#` 等合法根音因别名表缺失被 `indexOf` 判为 -1。
- 证据（原）：`tools/music/chord-notes.html:618-621`（默认大三）、`:474`（别名仅 Db/Eb/Gb/Ab/Bb）、`:577-590`（根音查找失败返回 null）。Node 复算：`Cfoo` → 大三 C–E–G；`Cxyz9` → 大三 C–E–G；`Cb` → `null`。
- **修复位点**：
  1. `NOTE_ALIASES`（行 474）补 `Cb:'B', Fb:'E', E#:'F', B#:'C'`，合法降号/升号根音可正常解析；
  2. 降级逻辑（行 633-641）改为仅当 `suffix===''`（如 `C`）才默认大三和弦，否则 `return null` 并提示「和弦类型无法识别」；`Cb` 经别名映射为 `B` 后正常走大三和弦。
- **判别力实测**：`scripts/verify_fun_calc.js` 增 `Cb → ["Cb · 大三和弦"]` 锁定用例 → 全量 32/32、discriminate 全量 0 逃生项；
  - 「未知后缀不再静默降级大三」子修复属 **harness 盲区**（效果为"不出现"大三和弦），改用 `scripts/_verify_fun_batch_fe_n8.mjs` JSDOM 两态脚本：注入 `Cfoo` → 修复后 `#chordTypeLabel` 清空（不含「大三和弦」）；`--head` 回退旧版 `#chordTypeLabel="<span class=\"chord-type-badge\">C · 大三和弦</span>"`（含「大三和弦」）。修复后 1/1、HEAD 1/1 通过。
- 移交文件：`plan/已修复/2026-11-07-FE-N8-降号根音无效与未知后缀静默降级.md`

### FE-N10 FEN 只校验棋盘段，缺行棋方时一律显示「黑方」且不报错（中，**2026-11-07 已修复**）
- 描述（原）：解析只要求 8 行×8 列，完全忽略行棋方、易位、吃过路兵、计数四段；缺第 2 段时 `turn=''`，三元判断落到「黑方」。FAQ 却称「缺段会解析失败」。
- 证据（原）：`tools/fun/chess-fen-viewer.html:276-298`、`tools/fun/chess-fen-viewer.html:316-320`、`tools/fun/chess-fen-viewer.html:221`。
- **修复位点**：新增 `validateFields(fen)`（`tools/fun/chess-fen-viewer.html` `render` 之前）：按 `\s+` 切 6 段，依次校验 `parts[1]∈{w,b}`、`parts[2]∈/^K?Q?k?q?$|^-$/`、`parts[3]==='-'||/^[a-h][1-8]$/`、`parts[4]/parts[5]` 为非负整数；`render` 在 `parse` 通过后调用 `validateFields`，不通过则输出 `FEN 字段缺失或非法：需 6 段（行棋方须 w/b、易位 KQkq 或 -、吃过路兵格位或 -、计数非负整数）` 并 return。`turn/castle/enPassant` 改为取自 `fv` 而非直接 `parts[1]||''`，从而缺段必由校验拦截、不再静默落「黑方」。
  - 附带修正：`默认参数` 预设 FEN 原为 `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK`（第 8 行少 3 格，本就 `parse` 失败）— 补为完整起始局面 `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`。
- **判别力实测**：`scripts/verify_fun_calc.js` 增缺段用例 `{fen:"rnbqkbnr/.../RNBQKBNR", expect:["FEN 字段缺失或非法"]}`（锚不含「白方/黑方/轮到」等默认态串，仅缺段输入下命中）；全量 `fun calc 33/33`；`discriminate_check` 已检 33 / 正确变红 33 / 仍 PASS(逃生项) 0。
- 移交文件：`plan/已修复/2026-11-07-FE-N10-FEN缺段静默显示黑方已修复字段校验.md`

### FE-N13 变速页降速时仍显示「提速 -25%」，"-"号与「提速」自相矛盾（中，**2026-11-07 已修复**）
- 描述（原）：百分比文案固定为「提速 + 数值%」，未区分加速与降速；等速时显示「提速 0%」。
- 证据（原）：`tools/music/convert-speed.html:166`（`'提速 '+((nb/ob-1)*100).toFixed(0)+'%'`）。Node 复算：180 s、120→90 → 新时长 `240.0` 秒、「提速 -25%」；120→120 → 「提速 0%」；180 s、120→140 → 「提速 17%」。
- **修复位点**：`calc()`（行 166）按 `pct=(nb/ob-1)*100` 符号分支输出「提速 X% / 降速 X% / 不变」（主显示 `toFixed(0)`、换算链 `toFixed(2)` 口径统一）；旧写死「提速 + 带符号数%」已移除。
- **判别力实测**：`scripts/verify_fun_calc.js` 增 `{nb:90}` → `["降速 25%"]`、`{nb:150}` → `["提速 25%"]`；全量 `fun calc 35/35`；`discriminate_check` 已检 35 / 正确变红 35 / 仍 PASS(逃生项) 0。
- 移交文件：`plan/已修复/2026-11-07-FE-N13-变速页降速误显提速.md`

### FE-N14 变速页宣传「对音频做变速处理、支持实时试听」，页面无音频能力（中，**2026-11-07 已修复**）
- **真源层（关键）**：meta/og/twitter/JSON-LD 描述由构建从 `i18n/tools/music.json` 的 `convert-speed.zh-CN.intro` 注入；卡片描述（`tools/music/index.html`、`json/tools.json` 的 `d` 字段）同源。直接改 `tools/music/convert-speed.html` 的 `<meta>` 是**错层**——`_build.py` 每次构建都会按 i18n 源重生成并把我之前的 HTML 编辑还原。本次修复在 `i18n/tools/music.json` 改 intro 为「输入原曲BPM与目标BPM，计算速度比例与新时长，给出提速/降速百分比…」，构建后 meta/JSON-LD/卡片全链路生效（已 grep 确认 convert-speed.html 与 index.html 卡片均收敛，0 处「对音频做变速处理/实时试听」残留）。
- 页面 `<body>` 内的简介 `<p>`（行 251，已是「用于 BPM 与新时长换算」）、功能特点/使用场景为 HTML 硬编码、不被构建重写，直接改 HTML 有效（与 i18n 文案口径一致）。
- 根因：页面只做 BPM/时长纯算术（无 `audio`/`AudioContext`/`playbackRate`），meta 却承诺音频变速与试听，属能力虚标；按「不虚标、对齐真实能力」原则收敛文案（未新增音频功能，避免伪功能）。
- 判别力：grep 复核页面自身（排除「相关工具」推荐区对其它工具的客观描述）已无「试听/音频/变速处理」字样；`verify_fun_calc.js` 该页 35/35 仍全绿、0 逃生（文案改动不影响 calc）。
- 移交文件：`plan/已修复/2026-11-07-FE-N14-变速页文案收敛去除音频虚标.md`

- 移交文件：`plan/已修复/2026-11-07-FE-N16-残局频次按单项记录.md`
### FE-N18 悔棋只撤 AI 一手，玩家可连续落两枚黑子（中，**2026-11-07 已修复**）
- 修复位点：`tools/fun/gomoku-ai.html` 的 `undo()`（行 371）。原实现只 `history.pop()` 一条并把 `turn=BLACK`，若末手是 AI 白子，则撤白留黑、玩家可立即再落一枚黑子，破坏回合制。改为：撤掉末手后，若其颜色为 WHITE 且上一手是 BLACK，则一并 `pop` 玩家那一手，回到「玩家重新落子」回合（`turn=BLACK`），从而整回合回退。
- 判别力实测：`scripts/_verify_fun_batch_fe_n18.mjs` JSDOM 真机：玩家点击落黑 → 等 AI 应手白 → `undo()` → 修复后棋盘 黑0/白0（整回合回退），旧实现会留 黑1/白0；脚本断言通过。
- 移交文件：`plan/已修复/2026-11-07-FE-N18-悔棋整回合回退.md`

- 移交文件：`plan/已修复/2026-11-07-FE-N19-战绩历史落库.md`
### FE-N21 2048「最大方块」只增不减：新局不重置、悔棋不回退，终局统计沿用历史值（中，**2026-11-07 已修复**）
- 修复：新增 `computeMaxTile()` 扫描全盘取最大值；`updateScore()` 每帧 `maxTile = computeMaxTile()`（顶部分数、scores 标签页、终局弹窗 `finalMax` 全用此值）；`newGame()` 防御性 `maxTile=0`；`loadBest()` 不再用存档 `data.maxTile` 播种（仅读 `best` 分数）。修复后：含 4 棋盘→4、undo 回退→跟随棋盘、newGame→当前棋盘最大块、刷新后新局不再残留 1024。
- 证据：`tools/fun/2048-game.html:361`（初值）、`:379-393`（newGame 重置）、`:518-528`（computeMaxTile + updateScore 每帧重算）、`:549-557`（loadBest 不读 maxTile）、`:556-560`（finalMax 用 maxTile）。
- 判别力：`scripts/_verify_fun_batch_fe_n21.mjs` JSDOM 两态锁——设含 4 棋盘→#maxTile=4 / undo 回退→2 / newGame→随棋盘重算 / loadBest(1024)→newGame 非 1024；修复后 4/4 通过，HEAD 旧版 4/4 全 FAIL（maxTile 停在 0/1024），确认 bug 真实且已修。（页面无输入框、harness 无法驱动，故用 JSDOM 两态锁，同 FE-N18/N19）
- 移交文件：`plan/已修复/2026-11-07-FE-N21-2048最大方块实时重算.md`

### FE-N22 俄罗斯方块计分口径与深度解析算例矛盾：代码 800×等级，文档 800×(等级+1)（中，**2026-11-07 已修复**）
- 修复（真源层）：deep-dive 示例串由构建从 `i18n/tools/content_deepdive.json` 的 `fun/tetris` 注入（直接改 `tools/fun/tetris.html` 是错层、会被还原，同 FE-N14）。把示例「800×(等级+1)…等级 3 得 3200」收敛为「**800×等级…等级 3 得 2400**」，对齐代码 `score += SCORE_TABLE[cleared] * level`（level 从 1 起）。同步改英文翻译源 `i18n/tools/en/fun/tetris.json`。构建后 tetris.html 示例已为「800×等级 分；等级 3 时单消 4 行得 2400 分」。
- 证据：`tools/fun/tetris.html:387`（`SCORE_TABLE=[0,100,300,500,800]`）、`:520`（`score += SCORE_TABLE[cleared]*level`）、`:414`（`level=1` 起）、行 300 计分参考表已写「multiplied by the current level」（与代码一致，无需改）。
- 判别力：grep 复核 tetris.html 示例已无「等级+1 / 3200」，改为「800×等级 / 2400」；`verify_fun_calc.js` 该页无 calc 用例受影响（纯文案口径收敛，无计算逻辑改动）。
- 移交文件：`plan/已修复/2026-11-07-FE-N22-俄罗斯方块计分口径对齐代码.md`

### FE-N24 旋转只有水平踢墙、无向上踢墙，贴底/贴顶旋转静默失败（中，**2026-11-07 已修复**）
- 修复：`rotate()` 踢墙表由纯横向标量 `[0,-1,1,-2,2]`（只改 `currentPiece.x`）扩展为含向上踢墙的偏移对表 `[[0,0],[-1,0],[1,0],[-2,0],[2,0],[0,-1],[0,-2],[-1,-1],[1,-1],[-1,-2],[1,-2]]`，循环内 `currentPiece.x += kicks[i][0]; currentPiece.y += kicks[i][1]`。先试原位/横向（保持原手感），横向均越界时再试向上踢墙 `[0,-1]/[0,-2]`（I 块贴底横转竖必需）。修复后 I 块横放最底行按 ↑ 成功转为竖向并向上踢墙 2 格（y 18→16），与参考表「允许贴墙与踢墙旋转」一致。
- 证据：`tools/fun/tetris.html:593-617`（`rotate()` 新踢墙表 + 双轴偏移）、`:459-469`（`rotateCells` 方阵旋转）、`:471-483`（`isValid` 越界即 false，`ny<0` 放过）。
- 判别力：`scripts/_verify_fun_batch_fe_n24.mjs` JSDOM 两态锁——`window.__tbTetris.setPiece('I',3,18)` 贴底 + `rotate()` → 修复后 `cells` 转竖向且 `y===16`（向上踢墙），T 块居中旋转原地形态改变；HEAD 旧版（纯横向 kick 表、无钩子）静态确认缺陷、运行期 4 项断言全 FAIL。修复版 4/4 通过，HEAD 4/4 失败，确认 bug 真实且已修。（tetris `currentPiece` 在 IIFE 闭包内，故修复版内置 `window.__tbTetris` 观测钩子；HEAD 无钩子，改用静态 kick 表差异确认，属闭包可观测性限制，已在 handoff 说明）
- 移交文件：`plan/已修复/2026-11-07-FE-N24-俄罗斯方块旋转向上踢墙.md`

### FE-N26 CPS 评级两套阈值：深度解析算例用 5 秒窗口与「很强」，代码固定 10 秒且 13.0 判「很快」（中，**2026-11-07 已修复**）
- 问题：深度解析写「慢<4、一般4~7、不错8~11、很强>12」并用「5 秒点 40 次」举例，但工具固定 10 秒、无时长选择，代码阈值为「<5 慢、<8 一般、<11 不错、<14 很快、否则神速」，同一页存在两套口径。
- 证据：`tools/fun/cps-test.html:202`（文档阈值）、`:203`（5 秒算例、13.0→很强）、`:254`（`const DURATION=10`）、`:256`（`cps<5?'慢':cps<8?'一般':cps<11?'不错':cps<14?'很快':'神速'`）、`:156`（公式框阈值与代码一致）。
- 复现：13.0 CPS 按代码 `13<14` 判「很快」，文档写「很强」；4.5 CPS 代码判「慢」，文档落在「一般 4~7」；页面无任何时长控件，「5 秒点 40 次」无法产生。
- 影响：`tools/fun/cps-test.html`；用户按算例核对评级会得到相反结论，「设定时长」暗示可调但实际固定 10 秒。
- 修复（真源层）：deep-dive 由构建从 `i18n/tools/content_deepdive.json` 的 `fun/cps-test` 注入（直接改 `tools/fun/cps-test.html` 是错层、会被还原，同 FE-N14/N20/N22/N24）。将 scenarios/example 的阈值与算例收敛为与代码一致：`慢<5/一般<8/不错<11/很快<14/神速≥14`，算例改为「10 秒点 80 次→8.0 不错、点 130 次→13.0 很快」；同步改英文翻译源 `i18n/tools/en/fun/cps-test.json`（key 即中文源串，删旧 key、补新 key，并清理一份与之重复但阈值写法不同的旧条目），确保 EN 态不退化。构建后 cps-test.html 深度解析（行 200/202/203）与公式框（行 156）、代码（行 256）三处口径一致。
- 判别力：grep 复核 cps-test.html 已无「很强 >12 / 5 秒点 40 次 / 慢 <4」；`verify_fun_calc.js` 该页无 calc 用例受影响（纯文案口径收敛）。
- 移交文件：`plan/已修复/2026-11-07-FE-N26-CPS评级阈值对齐代码.md`

### FE-N29 重置不清当前题与已找集合，界面复位后仍可继续作答（中，**2026-11-07 已修复**）
- 页面：`tools/fun/anagram-game.html`
- 问题：`reset()` 只改显示，不清 `cur`、`found`、`score`；`check()` 仅以 `!cur` 作为「未开局」守卫，而 `cur` 在重置后仍指向上局题目。
- 证据：`:298-303`（reset 仅改 DOM）、`:315`（`if(!v||!cur)return;`）、`:294-312`（start→reset→newRound 才重设 cur/found/score）。
- 复现：开始 → 答对一个词 → 点「重置」（提示回到「点击开始按钮开始」）→ 再输入上局词 → 实际仍判分并显示「已经找过这个单词」；期望重置后任何提交都不生效，直到点「开始」。
- 影响：重置语义失效，分数与已找列表可在「未开局」状态下继续累加。
- 修复（源修复）：`reset()` 头部增加 `cur=null; found=new Set(); score=0;`，使「重置」按钮与「开始」按钮语义对称——重置后 `cur` 为空、`check()` 因 `!cur` 守卫直接 return，任何提交均不生效，直到再次点「开始」。`start()` 仍先 `reset()` 再 `newRound()` 重设状态，不受影响。
- 判别力：`scripts/_verify_fun_batch_fe_n29.mjs` JSDOM 两态锁——`start()` 加载题目 → `reset()` → 提交 `'zzz'` → 修复版 `check` 因 `cur=null` 提前 return（`#output` 保持 reset 文本），HEAD 旧版 `cur` 未清空、`check` 进入判定改写 `#output`；修复后 PASS(exit 0) / HEAD FAIL(exit 1)，确认 bug 真实且已修。（`cur` 为顶层 let 不在 window，故经 DOM `#output` 间接观测）
- 移交文件：`plan/已修复/2026-11-07-FE-N29-找词游戏重置清空状态.md`

### FE-N31 重开/重置后旧的 `setTimeout(next)` 仍触发，新局第 1 题被直接跳过（中，已修复 2026-11-07）
- 页面：`tools/fun/sequence-puzzle.html`
- 问题：`choose()` 用 `setTimeout(next,1000)` 且不保存句柄，`reset()`/`start()` 均不清理；上一题遗留的定时器会在新局里执行 `next()`，题号从 1 直接跳到 2。
- 修复位点：第 321 行状态声明增 `timerId`（`let qNo,score,cur,timerId=null;`）；`reset()` 开头加 `if(timerId){clearTimeout(timerId);timerId=null;}`；`choose()` 末行改为 `timerId=setTimeout(next,o===cur.ans?1000:2200);`。
- 判别力：`scripts/_verify_fun_batch_fe_n31.mjs` JSDOM 两态锁——`start()` 开局题号=1 → 点首选项 `choose()` 安排定时器 → 1 秒内再 `start()`（reset）→ 等待 2500ms 超窗；修复版残留定时器被清理，终态题号保持 1，PASS(exit 0)；HEAD 旧版定时器触发 `next()`，终态题号跳到 2，FAIL(exit 1)，确认 bug 真实且已修。（`timerId` 为顶层 let 不在 window，故经 DOM `#qNo` 间接观测）
- 移交文件：`plan/已修复/2026-11-07-FE-N31-数列谜题重置清理定时器.md`

### FE-N32 点击速度页首屏「点击此处开始」区域点击无效，必须另点「开始」按钮（高，已修复 2026-11-07）
- 页面：`tools/fun/click-speed.html`
- 问题：`state` 只在 `start()/reset()` 中赋值，页面加载后为 `undefined`；`onClick()` 只处理 `'go'` 与 `'idle'/'done'`，`undefined` 时两个分支都不命中，主 CTA 点击区静默无响应。
- 修复位点：第 254 行状态声明由 `let duration=5,clicks,state,startTime,timer,best={5:0,10:0,30:0};` 改为 `let duration=5,clicks=0,state='idle',startTime,timer,best={5:0,10:0,30:0};` —— 加载即 `idle`，首点区域直接进入 `state==='idle'` 分支调用 `start()`。
- 判别力：`scripts/_verify_fun_batch_fe_n32.mjs` JSDOM 两态锁——首屏连点「点击此处开始」区域两次；修复版首点 `start()`（state='go'）→ 再点 `clicks++`（#counter=1），PASS(exit 0)；HEAD 旧版两次点击均因 state=undefined 无响应（#counter=0），FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N32-点击速度首屏区域点击开始.md`

### FE-N33 眨眼测试提前停止时 `elapsed` 回退为整段时长，速率被低估一个数量级（中，已修复 2026-11-07）
- 页面：`tools/fun/blink-counter.html`
- 问题：`finishTest()` 用 `total-remain` 推时长；若在第一个 1 秒 tick 之前停止（`remain` 仍等于 `total`），`elapsed<=0` 被兜底成 `total`，等于把不足 1 秒的测试按整段时长计算。
- 修复位点：新增 `startTime` 状态变量（声明 `var ...startTime=null;`，`startTest()` 内 `startTime=Date.now();`）；`finishTest()` 改为 `var elapsed=(Date.now()-startTime)/1000; if(!(elapsed>0))elapsed=0.001;`，按真实耗时计算，去掉「兜底成 total」逻辑。
- 判别力：`scripts/_verify_fun_batch_fe_n33.mjs` JSDOM 两态锁——设 60 秒 → startTest → 点 3 次眨眼 → 等 0.5s（未到首个 tick）→ stopTest(false)；修复版真实耗时≈0.5s → 每分钟眨眼≈357.9 次/分，PASS(exit 0)；HEAD 旧版兜底 60s → 3.0 次/分，FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N33-眨眼测试真实耗时计算.md`

### FE-N34 测试进行中修改「时长」会改写 remain/total，最终速率算错（中，已修复 2026-11-07）
- 页面：`tools/fun/blink-counter.html`
- 问题：时长下拉 `onchange` 直接调 `updateRing()`，该函数无条件 `total=新值; remain=total`，不判断 `running`、不重启计时；正在跑的倒计时被中途换标尺。
- 修复位点：① `updateRing()` 开头加 `if(running)return;`（测试进行中忽略时长改动）；② `startTest()` 内 `duration.disabled=true`、`stopTest()`/`resetTest()` 内 `duration.disabled=false`（进行中禁用选择，双重保险）。
- 判别力：`scripts/_verify_fun_batch_fe_n34.mjs` JSDOM 两态锁——设 60 秒 → startTest → 改 duration=30 并调 updateRing()（模拟中途改时长）；修复版 running 时 updateRing 直接 return，#tNum 保持 60，PASS(exit 0)；HEAD 旧版 remain 被改写为 30（#tNum=30），FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N34-眨眼测试进行中禁改时长.md`

### FE-N38 节拍器启动后不跟随 BPM 变更：间隔只算一次，且用 setInterval 累积漂移（中，已修复 2026-11-07）
- 页面：`tools/dance/bpm-rhythm.html`
- 问题：`toggleMetronome()` 启动时算一次 `interval=60000/bpm` 后交给 `setInterval` 固定使用；回调里只重读 `beatsPerBar`，不重读 BPM，因此运行中改 BPM 时数据区已更新、实际响拍不变。
- 修复位点：将 `setInterval` 改为递归 `setTimeout`——新增 `metroTick()`，每次 tick 末尾用 `60000/当前BPM` 重算并续排 `setTimeout(metroTick, interval)`；`toggleMetronome()` 也改用 `setTimeout(metroTimer,...)` 启动、停止分支用 `clearTimeout`。
- 判别力：`scripts/_verify_fun_batch_fe_n38.mjs` JSDOM 两态锁——桩替换 setTimeout/setInterval 仅捕获调度延迟；启动 120BPM 捕获 500ms → 改 BPM 为 240 并触发一次 tick → 修复版重算为 250ms，PASS(exit 0)；HEAD 旧版间隔恒 500ms，FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N38-节拍器跟随BPM变更.md`

- **状态：已修复 2026-11-07。** 修复位点：`tools/martial/kick-height.html` 新增 `var lvlEase=[5,3,0,-3]`（初学放宽、专业更严），评级四档门槛由 `>=100/85/70/50` 改为 `>=100-ease/85-ease/70-ease/50-ease`，`lvl` 现真实参与评级。判别力实测：`scripts/_verify_fun_batch_fe_n40n41.mjs` 运行期两态锁——输入 h=170/kh=170/前踢，切换「高级」→ 优秀、「专业」→ 良好，修复版评级随水平改变（PASS），HEAD 两态均 优秀（FAIL）。移交：`plan/已修复/2026-11-07-FE-N40-N41-踢腿评级水平与出色提示.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/martial/kick-height.html` 第 311 行「✓ 出色」触发条件由 `if(ratio>=100)` 改为 `if(ratio>=100 && grade==='优秀')`，与评级口径统一，消除「良好」与「出色」并存矛盾。判别力实测：`scripts/_verify_fun_batch_fe_n40n41.mjs` 运行期两态锁——h=170/kh=173/高踢（修正比 96.9% → 良好），修复版不显示「✓ 出色」（PASS），HEAD 仍显示（FAIL）。移交：`plan/已修复/2026-11-07-FE-N40-N41-踢腿评级水平与出色提示.md`。
### FE-N42 井字棋 AI 定时器未清理：新局/先手切换后 AI 可连下两手（高，已修复 2026-11-07）
- 页面：`tools/fun/tic-tac-toe.html`
- 问题：`newGame()` 不保存、也不 `clearTimeout()` 已排队的 AI 落子定时器；`aiMove()` 只判 `gameOver`，不校验轮次，任何残留定时器都会直接 `board[move]='O'`。两个定时器并存时同一回合 AI 连下两手。
- 修复位点：新增 `let aiTimer=null;`；`newGame()` 开头 `if(aiTimer){clearTimeout(aiTimer);aiTimer=null;}`；`makeMove()` 排 AI 前先清旧定时再 `aiTimer=setTimeout(aiMove,400)`；`aiMove()` 入口 `aiTimer=null`（定时器正在触发即清空引用）。setMode/setDifficulty 经 newGame 同样受益。
- 判别力：`scripts/_verify_fun_batch_fe_n42.mjs` JSDOM 两态锁——人机玩家先手 → makeMove(0)（排 AI 400ms）→ 立即 newGame() → 等 600ms → 修复版新棋盘 O 数=0，PASS(exit 0)；HEAD 旧版残留定时器落 1 个 O，FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N42-井字棋清理AI定时器.md`

### FE-N43 太空射击结束态不复位「开始游戏」按钮（中，**2026-11-07 已修复**）
- 页面：`tools/fun/space-shooter.html`
- 问题：`startGame()` 把 `#btnStart` 置为 `disabled` + 「游戏中...」，`gameOver()` 只切状态、不恢复按钮；只有 `restartGame()` 才复原。
- 证据：`:1205-1206`（开局禁用）、`:1061-1065`（gameOver 未触碰 btnStart）、`:1231-1232`（仅 restartGame 复原）。
- 复现：漏敌/撞机至 0 命 → 结束覆盖层出现后点「开始游戏」无任何反应，必须先点「重新开始」。
- 影响：主操作按钮在结束态永久失效，用户误判页面卡死。
- 修复位点：`gameOver()` 在 `updateHUD()` 后复原 `#btnStart`（`disabled=false`、文案回到「开始游戏」）；同步结束覆盖层提示指向「开始游戏」主按钮。`tools/fun/space-shooter.html:1065-1067`。
- 判别力：`scripts/_verify_fun_batch_fe_n43.mjs` JSDOM 两态锁——覆盖 `Math.random` 使敌机必撞玩家，真实 rAF 跑到 gameOver：当前 `disabled=false/开始游戏`（PASS），HEAD 仍 `true/游戏中...`（FAIL）。
- 移交文件：`plan/已修复/2026-11-07-FE-N43-太空射击结束复位开始按钮.md`

- **已修复 2026-11-07（改 i18n 真源 + 重建注入）**：deep-dive 是构建注入产物，直接改 HTML 会被 `_build.py` 还原，故改真源 `i18n/tools/content_deepdive.json` 的 `fun/space-shooter` → `examples[1].body`（算例），并同步英文源 `i18n/tools/en/fun/space-shooter.json` 的 map（键即中文源串——旧键删除、新键新增，否则英文态失译）。新算例：第 1 波 5 架普通机各 10 分 = 50；第 2 波混编（快速机 2×20 + 厚甲机 2×30，厚甲 3 发）= 100，累计 **150** 分；注明三种道具（三连射/护盾/加命）不直接加分、射速固定，并删掉「吃加速道具后射速翻倍」这一不存在的机制。
  - 判别力实测（`scripts/_verify_fun_batch_fe_n45.mjs`）：从构建产物抽 `normal/fast/tough` 的 score 常量断言 10/20/30，再断言页面与算例均无「射速翻倍/加速道具/8 架各 15 分/累计 170 分」、算例引用 10/20/30 与三道具、累计 150 分、英文 map 含新键——当前 7 项全 PASS；HEAD（旧构建产物）5 项 FAIL。
  - 一致性门禁：`python3 scripts/audit_deepdive_source_sync.py --check` → 扫描 4573 页、不一致 **0** 页。移交：`plan/已修复/2026-11-07-FE-N45-太空射击算例与真实计分对齐.md`。
### FE-N46 贪吃蛇把「即将腾空的尾格」判为自撞（中，**2026-11-07 已修复**）
- 页面：`tools/fun/snake-game.html`
- 问题：自撞判定在 `unshift` 前对整条蛇（含尾段）做 `some`，随后才 `pop()`；未吃到食物时尾部本会腾空，进入尾格应合法。
- 证据：`:437-470`，判定 `:456` `snake.some(s => s.x===head.x && s.y===head.y)`，`:468` 才 `snake.pop()`。
- 复现（Node 复算）：长度 4、头 (10,10)、身 (10,11)(11,11)、尾 (11,10)，向右一步进入尾格 → 判定 gameOver；按规则该格当帧腾空，应存活。该盘面可由「长度 3 蛇绕 2×2 环并在 (10,10) 吃到食物」达成。
- 影响：特定盘面下错误结束游戏（误判死亡）。
- 修复位点：`gameStep()` 先算 `willEat=(head==food)`，自撞判定 `bodyToCheck = willEat ? snake : snake.slice(0,-1)`；未吃时正常 `pop()`。`tools/fun/snake-game.html:456-469`。
- 判别力：`scripts/_verify_fun_batch_fe_n46.mjs` JSDOM 两态锁——注入脚本暴露闭包内 `snake/nextDirection/food/gameStep`，构造 2×2 环盘面、头向右一步进入尾格、food 不在尾格：当前 `gameRunning=true`、新头(11,10)、蛇长 4（PASS），HEAD `gameRunning=false`（FAIL）。
- 移交文件：`plan/已修复/2026-11-07-FE-N46-贪吃蛇尾格自撞误判.md`

### FE-N48 抛硬币重置统计后「最近结果」残留（中，已修复 2026-11-07）
- 页面：`tools/fun/coin-flip.html`
- 问题：`updateStats()` 仅在 `recent.length>0` 时重绘 `#recentResults`；`reset()` 清空数组后调用它，容器仍是旧序列。
- 修复位点：`updateStats()` 增加 `else` 分支，当 `recent.length===0` 时把 `#recentResults` 写回 `<span style="color:var(--text-muted)">暂无记录</span>`。
- 判别力：`scripts/_verify_fun_batch_fe_n48.mjs` JSDOM 两态锁——抛 3 次（每次等 1.1s）→ reset() → 修复版 #recentResults 显示「暂无记录」，PASS(exit 0)；HEAD 旧版残留「正/反」，FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N48-抛硬币重置清空最近结果.md`

### FE-N49 Pong AI 移动速率被乘 0.08，人机模式几乎无对抗（中，**2026-11-07 已修复**）
- 页面：`tools/fun/pong.html`
- 问题：`AI_REACTION` 本意是反应延迟，却被当作速度系数直接乘进每帧位移，AI 实际速度仅 0.336 px/帧。
- 证据：`:519-521`（`AI_SPEED=4.2`、`AI_ERROR=15`）、`:624-639`（`:635` `rightPaddle.y += Math.sign(diff)*AI_SPEED*AI_REACTION`）。
- 复算：4.2×0.08=0.336 px/帧 ≈ 20 px/s；球初速 `:515` 4.5 px/帧 = 270 px/s，AI 不到球速 1/13，从场地中心走到边线需约 8 s，而球横穿一次仅 2–3 s。
- 影响：AI 基本接不到球，人机模式失去对抗性（与该页「AI 有反应延迟和移动误差」的定位不符）。
- 修复位点：`:635` 位移改为 `Math.sign(diff) * AI_SPEED`（去掉 `* AI_REACTION`），并删除已无用的 `AI_REACTION` 常量（`:520`）。保留 `AI_ERROR` 抖动作为「移动误差」定位，不引入难度档位（避免范围蔓延）。`tools/fun/pong.html:519-520,635`。
- 判别力：`scripts/_verify_fun_batch_fe_n49.mjs` JSDOM 两态锁——覆盖 Math.random→0.9 使球恒向右、录制 canvas moveTo 提取右挡板 y(≈614)，跑真实循环 6s：当前右挡板 y 行程 100.8px（跟随球，PASS），HEAD 25.5px（恒近初始位，FAIL）。
- 移交文件：`plan/已修复/2026-11-07-FE-N49-Pong-AI速率修复.md`

### FE-N51 石头剪刀布「重置比分」不清最高连胜（中，已修复 2026-11-07）
- 页面：`tools/fun/rock-paper-scissors.html`
- 问题：`resetScore()` 重置 score/streak/history，却漏掉 `maxStreak`；只有「清空记录」才置 0。
- 修复位点：`resetScore()` 内 `streak = 0;` 之后新增 `maxStreak = 0;`。
- 判别力：`scripts/_verify_fun_batch_fe_n51.mjs` JSDOM 两态锁——monkeypatch Math.random→0 使 cpu 恒 rock、玩家 paper 必胜；连胜 3 次 maxStreak=3 → resetScore() → 再胜 1 次（maxStreak=max(旧值,1)）→ 修复版=1（#statsDetail「最高连胜 1」），PASS(exit 0)；HEAD 旧版=3（「最高连胜 3」），FAIL(exit 1)，确认 bug 真实且已修。
- 移交文件：`plan/已修复/2026-11-07-FE-N51-石头剪刀布重置清零最高连胜.md`
- 证据：`:442-453`（无 maxStreak 赋值）、`:496-499`（clearHistory 才 `maxStreak=0`）、`:470`（统计页直接展示 maxStreak）、`:508`（随分数一起持久化）。
- 复现：打出 3 连胜 → 点「🔄 重置比分」→ 总场次/胜率归零，统计页「最高连胜」仍显示 3。
- 影响：重置后统计自相矛盾（0 场次却有最高连胜）。
- 方案：resetScore 内加 `maxStreak = 0`。

### FE-N52 滑动拼图「自动还原」被记为胜利并写入 0 步最佳纪录（高，**2026-11-07 已修复**）
- 页面：`tools/fun/sliding-puzzle.html`
- 问题：`solveAnimation()` 反向回放结束后直接 `won=true; celebrateWin()`，而 `celebrateWin()` 经 `:1004-1005` 包裹会 `saveBest(moves, elapsed)` + `__spRecord()`；自动还原不增加 moves、也不重置计时，于是以玩家此前的步数/用时（刚开局时为 0/0）记为新纪录，并计入完成局数。
- 证据：`:887`（`window.solveAnimation`）、`:900-904`（回放完成即 `won=true; celebrateWin()`）、`:846-862`（celebrateWin→`saveBest`+弹窗）、`:1004-1005`（包裹追加 `__spRecord`）、`:700-709`（`saveBest` prev 为空即写「新纪录」）。
- 复现：重新开始后立刻点「自动还原」→ 完成后弹「🏆 新纪录」，最佳记录写成「0 步」，统计完成局数 +1；该尺寸/模式的最佳此后无法再被正常刷新（`:702` 以步数最小为优，0 步恒最优）。
- 影响：假胜利 + 永久污染最佳纪录与完成局数统计。
- 修复位点：`solveAnimation` 完成分支改为独立路径——`won=true; playing=false; stopTimer();` + 提示「演示完成，不计入对局成绩」的 toast，**不调用 celebrateWin**，从而不写最佳、不计完成局数。`tools/fun/sliding-puzzle.html:900-905`。
- 判别力：`scripts/_verify_fun_batch_fe_n52.mjs` JSDOM 两态锁——清 localStorage → `startGame()` → `solveAnimation()`，轮询 `puzzle_games_v1`：当前不写入（PASS），HEAD 写入 1 条完成记录（FAIL）。
- 移交文件：`plan/已修复/2026-11-07-FE-N52-滑动拼图自动还原不计胜利.md`

- **状态：复核（2026-11-07）：历史快照误报，当前源码已修复。** 当前 `tools/fun/random-picker.html` 的 `start()` 全程用 `result.textContent`/`output` 经 `document.createElement`+`st.textContent`/`past` 经 `sp.textContent` 渲染（:319-356），选项文本不再经任何 `innerHTML` 拼接，无注入通道。补 `scripts/_verify_fun_batch_fe_n53.mjs` 回归锁——注入 `<img onerror>` 恶意选项，当前与 HEAD 均不产生可解析 `<img>` 元素、无脚本执行（PASS），防回退。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/random-picker.html` ① `__random_pickerResText()` 过滤正则新增 `抽取中`（:419，占位串视为无结果）；② 在 `setInterval` 真实定格（`r.textContent=picked`）之后的回调末尾新增 `__random_pickerExtras()` 调用（:357），使真实抽取结果被记录。修复前同步包装器在 `start()` 返回即抓取，记到「🎲 抽取中...」。判别力实测：`scripts/_verify_fun_batch_fe_n54.mjs` 运行期两态锁——不重复模式输入 4 项、固定种子，`start()` 后等 1.5s，捕捉 `TBKit.history.record` 末条「结果」；修复版=真实项（如「苹果」，PASS），HEAD 版=「🎲 抽取中...」（FAIL）。移交：`plan/已修复/2026-11-07-FE-N54-N55-抽取记录与抽完提示.md`。
- **状态：复核（2026-11-07）：当前源码已修复，无需改源码。** 当前 `tools/fun/random-picker.html` 在 `if(unique){...}` 内、`setInterval` 之前即设有 `if(pool.length===0){ 显示「所有选项已抽完！」; return; }`（:312-315），空池不再静默重洗，与 README/FAQ 一致。`scripts/_verify_fun_batch_fe_n55.mjs` 运行期两态锁——不重复模式 2 项连抽 3 次，当前与 HEAD 末次 output 均含「所有选项已抽完！」（PASS），证实该守卫在 HEAD 已存在，台账原描述陈旧。仅补回归锁防回退，未改源码。移交：`plan/已修复/2026-11-07-FE-N54-N55-抽取记录与抽完提示.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/daily-riddle.html` `computeScore()` 去掉 `- hints*20`（与 FAQ「提示本身不减分」对齐，连击奖励保留）。判别力实测：`scripts/_verify_fun_batch_fe_n56.mjs` 从真实源码抽取 `baseScore`/`computeScore` 在隔离作用域实跑——`computeScore(true,3,1)` 修复版=100（PASS），HEAD=40（100−3×20，FAIL）。移交：`plan/已修复/2026-11-07-FE-N56-N62-N67-计分与模式与定时链.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/keyboard-heatmap.html` `onKey(e)` 开头新增 `if(e.repeat)return; // 长按自动重复产生的 keydown 不重复计数（FE-N60）`（约 291 行）。判别力实测：`scripts/_verify_fun_batch_fe_n60.mjs` 运行期两态锁——连续触发两次 `onKey`（`repeat=false` 与 `repeat=true`），读 `counts['a']`，修复版 `counts['a']=1`（忽略重复，PASS），HEAD 旧版 `counts['a']=2`（FAIL）。移交：`plan/已修复/2026-11-07-FE-N60-N73-键盘长按与生成器预设.md`。
- **已修复 2026-11-07**：① `onKey` 末尾接 `__khScheduleRecord()`——500ms 防抖后调既有 `__keyboard_heatmapExtras()`（该记录器自带 1s 节流 + 同值去重），真实打字终于落库，数据表/历史/趋势/导出有内容；② `loadSample` 保留「累加」语义（既有 verify 用例以 `loadSample();loadSample()` ⇒ 总按键 90 为契约，改动会破坏判别力），改为在结果区显式提示「示例文本已累加到当前统计：本次计入 N 次按键，当前总计 M 次。如需从 0 开始请点清空统计」（keyboard-heatmap.html ~L297-308、L382-400）。判别力实测（`scripts/_verify_fun_batch_fe_n61.mjs`）：桩 `TBKit.history.record` 捕获，真实触发 3 次 `onKey` 后等 900ms——当前记录数 1 且含 `typeArea=abc`（PASS）/ HEAD 记录数 0（FAIL）；`loadSample()` 后结果区含「累加」（当前 PASS / HEAD FAIL）。移交：`plan/已修复/2026-11-07-FE-N61-N78-热力图落库与球速帧率无关.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/sequence-memory.html` 新增 `pendingTimers` 数组 + `scheduleTimer()`/`clearPendingTimers()`，`reset()` 与 `nextRound()` 开头 `clearPendingTimers()`，全部 `setTimeout` 改为 `scheduleTimer`。判别力实测：`scripts/_verify_fun_batch_fe_n62.mjs` 运行期两态锁——`start()` 后立刻 `reset()` 再等 1.6s，修复版 `accepting` 仍为 false（链已取消，PASS），HEAD 旧链跑完设 `accepting=true`（FAIL）。移交：`plan/已修复/2026-11-07-FE-N56-N62-N67-计分与模式与定时链.md`。
- **已修复 2026-11-07**：新增 `roundTimer` + `sessionId` 局次令牌与 `clearRoundTimer()`；`start()`/`reset()` 先清定时器并 `sessionId++`；`choose()` 内 `const mySession=sessionId` 后注册定时器，回调开头 `if(mySession!==sessionId)return;` 丢弃作废局次的回调（color-guess.html ~L253-257/259-273/309-313）。判别力实测（`scripts/_verify_fun_batch_fe_n64_n82_n83.mjs` 第 1 节）：`start()`→答题→立即 `reset()`→等 1.3s，当前提示仍是「点击"开始"开始游戏」且 `round=0`（PASS）；HEAD 被旧回调推进到「第 1 轮」`round=1`（FAIL）。移交：`plan/已修复/2026-11-07-FE-N64-N82-N83-换题定时器与谜语检索去重.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/number-puzzle.html` `checkAnswer()` 在 `usedIndices.length<4` 校验后新增文法校验——相邻两个数字记号之间必须插入运算符，否则判非法（提示「相邻两个数字之间必须插入运算符，不能拼成多位数」），不再 `join('')` 拼接求值。判别力实测：`scripts/_verify_fun_batch_fe_n66.mjs` 运行期两态锁——模拟 `2 4 + 5 - 5`，修复版拦截并提示「运算符」（PASS），HEAD 拼接成 `24+5-5=24` 误判「正确」（FAIL）。移交：`plan/已修复/2026-11-07-FE-N66-N68-N69-拼数拼接与重复计分.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/number-puzzle.html` 新增「1~13 / 1~10 模式」切换按钮与 `setMode(v)`（设置 `mode13` 并 `newGame()` 重建牌面），初始化调用 `setMode(mode13)` 标记激活态。判别力实测：`scripts/_verify_fun_batch_fe_n67.mjs` 运行期两态锁——`setMode(false)` 后 `newGame()`，修复版 4 张数字全部 ≤10（PASS），HEAD 无 `setMode`（承诺未实现，FAIL）。移交：`plan/已修复/2026-11-07-FE-N56-N62-N67-计分与模式与定时链.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/word-scramble.html` 新增 `submitLocked` 状态；`submitAnswer` 答对后设 `submitLocked=true` 并 `if(submitLocked) return` 拦截窗口内二次提交，`nextWord()` 复位。判别力实测：`scripts/_verify_fun_batch_fe_n68.mjs` 运行期两态锁——开局→答对→连点两次提交，修复版 score 仅 +1 次（55→55，PASS），HEAD 翻倍（35→75，FAIL）。移交：`plan/已修复/2026-11-07-FE-N66-N68-N69-拼数拼接与重复计分.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/word-scramble.html` `endGame()` 开头加 `if(!gameActive) return;`（未开局/已结束时直接拦截，不写空局战绩）；`saveScore()` 首次判定由 `!data.bestScore` 改为 `typeof data.bestScore!=='number'`（0 分不再被当「无记录」误判新纪录）。判别力实测：`scripts/_verify_fun_batch_fe_n69.mjs` 运行期两态锁——清空历史后未开局直接 `endGame()`，修复版 `recent` 条数=0（PASS），HEAD 写入 1 条 0 分空局（FAIL）。移交：`plan/已修复/2026-11-07-FE-N66-N68-N69-拼数拼接与重复计分.md`。
- **已修复 2026-11-07**：采用前一种方案，`onTap` 改为 `const now = getAudioCtx().currentTime;`（rhythm-trainer.html ~L1011-1015），与 `startTime` 同源。判别力实测（`scripts/_verify_fun_batch_fe_n70n71.mjs`）：桩 `AudioContext.currentTime`／`performance.now` 各记一条访问日志，实跑 `startTraining()`（BPM 上限 200 → 预备拍 1.2s）等 `tapBtn` 解锁后调 `onTap`，取首条日志——当前=audio（PASS）/ HEAD=perf（FAIL）。移交：`plan/已修复/2026-11-07-FE-N70-N71-节奏评分时钟与小节号.md`。
- **已修复 2026-11-07**：`measureNum` 改用 `Math.floor((beatIdx - 1) / 4) + 1`（rhythm-trainer.html ~L1155）。判别力实测（同锁脚本）：从源码抽 3 行计算式在隔离 `new Function` 实跑，`subdivision=1 / noteIndex=3` → 当前「第1小节 第4拍」PASS / HEAD「第2小节 第4拍」FAIL。移交同 N70。
- **状态：已修复 2026-11-07（跨 5 文件统一修）。** 修复位点：`tools/fun/generator-2.html`、`tools/fun/generator-3.html`、`tools/fun/generator-24.html`、`tools/music/generator-1.html`、`tools/music/random-training-rhythm.html` 五处预设 `"cnt":"2.5"`→`"3"`、`"cnt":"7.5"`→`"8"`（同时删除无关「极端工况」模板）；`gen()` 入口由 `Math.min(+value||5,50)`（generator-1/random-training-rhythm 为 `parseInt` 取整但未钳下限）改为 `Math.max(1,Math.min(Math.floor(+value||5),50))`，确保小数与低于 1 的输入都被正确取整钳制。判别力实测：`scripts/_verify_fun_batch_fe_n73.mjs` 运行期两态锁——五文件源码均无 `"cnt":"2.5"/"7.5"`，且 `generator-2` 设 `cnt=8` 生成 8 条，修复版 PASS、HEAD 旧版仍含小数预设 FAIL。移交：`plan/已修复/2026-11-07-FE-N60-N73-键盘长按与生成器预设.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/music/sheet-music.html` 新增 `KEY_SPELLINGS`（12 调大调音阶拼写，8 项含高八度重复），`renderStaff` 与 `__staffExport` 的音名取值由 `NOTE_NAMES[noteIdx]` 改为 `KEY_SPELLINGS[currentKey/key][i]`（频率仍按 `NOTE_FREQS[noteIdx]` 不变）。判别力实测：`scripts/_verify_fun_batch_fe_n74.mjs` 运行期两态锁——`setKey('Bb')` 后读 `#staff-display`，修复版含 `Bb`/`Eb` 且不含 `A#`（PASS），HEAD 旧版无 `KEY_SPELLINGS`、Bb 调主音为 `A#`（FAIL）。移交：`plan/已修复/2026-11-07-FE-N74-N76-降号调音名与CSV唱名.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/music/sheet-music.html` `__staffExport` 第 8 级唱名由 `SOLFEGE[i]` 改为 `SOLFEGE[i === 7 ? 0 : i]`（同时音名列改用 `KEY_SPELLINGS[key][i]`）。判别力实测：`scripts/_verify_fun_batch_fe_n76.mjs` 运行期两态锁——`__staffExport()` 后读 `#staffHidden tbody` 第 8 行唱名列，修复版为 `do`（PASS），HEAD 旧版越界取 `SOLFEGE[7]` 得空/undefined（FAIL）。移交：`plan/已修复/2026-11-07-FE-N74-N76-降号调音名与CSV唱名.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/breakout.html` `togglePause()`（删除恢复时重复的 `gameLoop()` 调用，仅翻转 `state.paused`；循环在整个 running 期间只启动一次）。判别力实测：`scripts/_verify_fun_batch_fe_n77.mjs` 运行期两态锁——统计 gameLoop 的 rAF 调度次数，修复版暂停/继续前后比 =1.00（单链，PASS），HEAD 比 =2.05（双链，FAIL）。移交：`plan/已修复/2026-11-07-FE-N77-N88-N89-小游戏暂停与棋盘重建.md`。
- **已修复 2026-11-07**：`state` 新增 `lastFrame`；`gameLoop` 每帧算 `__dt = min(now - lastFrame, 50)`（首帧/恢复帧取 16.667，上限 50ms 防切后台单帧大跳）、`__k = __dt / 16.667`，并传给 `movePaddle(__k)`/`moveBall(__k)`/`updateParticles(__k)`；三函数入口统一 `kk` 钳制（非有限/≤0 退回 1），位移与挡板速度（`7*kk`）、粒子重力与寿命均按 `kk` 缩放；`startGame` 与「恢复暂停」重置 `lastFrame=0`（breakout.html ~L408-418、L499-505、L648-676、L760-780、L796/L803）。公式表「帧率无关」表述由此成立，无需改文案。判别力实测（`scripts/_verify_fun_batch_fe_n78.mjs`）：桩 canvas（记录 `arc` 读球心）+ 桩 rAF 手动逐帧 + 桩 `performance.now`，比对「33.3ms 帧位移 / 16.7ms 帧位移」——当前 8.00/4.00=**2.00**（PASS）/ HEAD 4.00/4.00=**1.00**（FAIL）。移交同 N61。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/generator-laugh.html` 预设「小规模/大规模」改 `cnt` 为 `3/8`（原 `2.5/7.5`），`gen()` 入口 `Math.max(1, Math.min(Math.floor(...), 50))`（原无 floor、无下限钳制）。判别力实测：`scripts/_verify_fun_batch_fe_n80.mjs` 运行期两态锁——抓预设配置后点「大规模」，修复版生成 8 条（PASS），HEAD 7.5 只生成 7 条（FAIL）。移交：`plan/已修复/2026-11-07-FE-N80-N87-笑声预设与冥想分段.md`。
- **已修复 2026-11-07**：新增 `resolvePool(raw)` 四级匹配——①「全部/空」= 全题库；②分类名精确；③分类名互相包含（`动`→`动物`）；④谜面文本包含；全部未命中的**回退到普通池并在结果区显式提示**（不再静默）。结果区新增「分类：X · 候选 N 条 · 本轮剩余 M 条」一行。默认输入值 `value="天气"`→`"动物"`，预设「默认参数」`topic` 同步改 `动物`（riddle-generator.html ~L129/260-320/397）。判别力实测（同锁脚本第 2 节）：默认值=`动物`、输入「天气」结果含「未命中/回退」、输入「动」结果含「分类：动物」——当前三项全 PASS，HEAD 三项全 FAIL（默认仍 `天气`、结果无任何提示/分类行）。移交同 N64。
- **已修复 2026-11-07**：新增 `usedSet`/`usedKey` 与 `pickUnique(list,key)`——池签名变化即清空集合，取「未抽过」的子集随机取一条入集合，集合耗尽自动循环清空（实现公式与深解承诺的「同一轮去重、抽完循环」）；`generate()` 改为 `pickUnique` 并显示「本轮剩余」（riddle-generator.html ~L261-300）。判别力实测（同锁脚本第 3 节）：钉死 `Math.random=()=>0` 后普通池（2 条）连抽两次——当前两条不同（PASS）；HEAD 两次都是同一条（FAIL）；第 3 次当前循环回池内。移交同 N64。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/emoji-memory.html` 维护 `pendingTimers` 数组，`reset()`/`nextLevel()` 起点 `clearPendingTimers()`；`showSeq` 起始加 `sequence.length===0` 守卫；所有 `setTimeout` 改为 `scheduleTimer()` 纳入追踪，通关延迟 `setTimeout(nextLevel,1500)` 同样纳入。判别力实测：`scripts/_verify_fun_batch_fe_n85.mjs` 运行期两态锁——「准备」阶段立即 `reset()` 后等 >1s，修复版无任何幽灵选项按钮（PASS），HEAD 出现 2 个幽灵按钮（FAIL）。移交：`plan/已修复/2026-11-07-FE-N85-记忆游戏重置定时链.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/meditation-timer.html` 分段数 `Math.round(dur/seg)`→`Math.ceil(dur/seg)`；每段「起–止」展示且止时刻 `Math.min(段末, 总时长)` 钳制（原只列起始时刻）。判别力实测：`scripts/_verify_fun_batch_fe_n87.mjs` 运行期两态锁——`dur=10,seg=3` 修复版 4 段（PASS），HEAD `round` 仅 3 段（FAIL）。移交：`plan/已修复/2026-11-07-FE-N80-N87-笑声预设与冥想分段.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/memory-game.html` winOverlay 容器补 `class="win-overlay"`（`<div id="winOverlay" class="win-overlay" style="display:none;">`）。判别力实测：`scripts/_verify_fun_batch_fe_n88.mjs` 静态结构断言——修复版命中 `id="winOverlay" class="win-overlay"`（PASS），HEAD 无 class（FAIL）。移交：`plan/已修复/2026-11-07-FE-N77-N88-N89-小游戏暂停与棋盘重建.md`。
- **状态：已修复 2026-11-07。** 修复位点：`tools/fun/memory-game.html` `setDifficulty()`/`setTheme()` 末尾调用 `startGame()` 重建棋盘并同步统计。判别力实测：`scripts/_verify_fun_batch_fe_n89.mjs` 运行期两态锁——初始 easy 12 牌，切 expert 后修复版重建为 36 牌（PASS），HEAD 仍 12 牌（FAIL）。移交：`plan/已修复/2026-11-07-FE-N77-N88-N89-小游戏暂停与棋盘重建.md`。


---

## 2026-11-11 第二批追加（11-文娱爱好/fun-entertainment.md 的 INLINE/FEATURE 验证记录）

- 处置：本批**只补锁定用例、未改源码**（符合"陈旧证据只复核、补锁定、不改源码"纪律）；视为已修复，从待处理清单移除。
