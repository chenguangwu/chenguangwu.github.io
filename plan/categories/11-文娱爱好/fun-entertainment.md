# 娱乐 · tools/{fun,music,film,media,dance,martial,chess,games 类}（~80 页）

## 已知问题

## 功能缺陷
- 音乐页缺「和弦进行速查」（常用 1645/4536 试听）。
- fun 类「看一眼就走」重灾区：优先接 G06-S1/S4（结果生成即分享）。

## 受影响范围
- tools/fun/（62）、tools/music/、tools/film/、tools/media/、tools/dance/、tools/martial/、tools/chess/

## 进度
- 🔴 待开发

## 2026-11-03 审计补充

### 删除输入后节奏评分残留（中，确认缺陷）
- 问题：输入至少三个字符形成分析后全选删除，输入已空但之前的评分、等级及分析仍显示。
- 证据：`tools/fun/typing-rhythm.html:155-170,270-281,294-317,352-357`：Backspace 只 pop 一次并画图，input 只保存文本；只有 `clearAll()` 重置分数及结果。浏览器未实测。
- 影响：`tools/fun/typing-rhythm.html`；可能把上一次成绩误认为当前练习结果。
- 方案：处理选区删除、粘贴和输入法事件，文本清空时重置计时与结果；测试全选删除与重新输入。

### 留存优化：同题个人进步对比（低，建议）
- 证据：同页 `:294-317` 已计算间隔均值、变异系数及等级，`:266-268` 可切换样文。
- 影响：同页；方案：提供重复同一段文本的历次成绩对比，明确评分与输入长度局限；仅本地记录指标，不存练习文本。

### 桥牌有局加倍宕墩罚分错误（高，确认源码缺陷）
- 证据：`tools/chess/bridge-scoring.html:291-298,344-346,363-380` 有局加倍每墩一律算 200；4♠有局加倍实得 8 墩（宕 2）算 400，按首墩 200、后每墩 300 应为 500，再加倍同受影响。
- 影响：`tools/chess/bridge-scoring.html`，错误赛局积分。
- 方案：分别实现有局/无局逐墩阶梯及再加倍；增加宕 1、2、3 墩用例，允许按定约保存可核对明细。

### 中国围棋数子法实际沿用数目法（高，确认源码缺陷）
- 证据：`tools/chess/go-territory.html:143-175,223-228,279-307` 中国和日本两分支均用围空加提子，缺盘上活子输入，却标为中国数子法；黑空 50、提 3、白空 48、提 5、贴目 6.5，两模式均输出 53 比 59.5。
- 影响：`tools/chess/go-territory.html`，中国规则数据不足仍给出可能误导的胜负。
- 方案：按选择的规则引入必要活子、空点及死子处理，注明贴目或贴子单位，不足时不出结论；可本地保存规则口径和棋局复盘明细。

### 节拍细分格数与拍号音值矛盾（中，确认源码缺陷）
- 证据：`tools/music/beat-subdivision.html:219-228,518-550,580-585,698-757` 7/8 汇总 7/3 拍却绘 3 拍组；6/8、120 BPM、四分音符显示 1.5 秒小节但绘 2 格各 750 ms；4/4 全音符汇总 1 格却绘 4 格。
- 影响：`tools/music/beat-subdivision.html`，节拍练习图与音值不一致。
- 方案：明确 BPM 基准、复拍及不规则重音分组，按音值和小节长度生成格子；本地保存拍号、分组及速度练习预设。

### 音符转换错误后复制旧结果（中，确认源码缺陷）
- 证据：`tools/music/freq-note-converter.html:230-267,520-525,554-566,581-590` 先计算 440 Hz，再清空输入；错误分支未清除上次 `dataset.copyValue`，复制仍优先读取旧结果。
- 影响：`tools/music/freq-note-converter.html`，错误状态下复制过时调音数据。
- 方案：无效时清空复制值、禁用复制和试听；恢复有效后启用并在本地预设注明 A4 参考频率。

### 硬币连胜名称与定义冲突（低，确认源码缺陷）
- 证据：`tools/fun/coin-toss-streak.html:158-172,200-208,275-294` 正、反、反、反的状态更新将任意同面最长连续次数记为 3，但解释称最长连胜为连续正面，按该定义为 1。
- 影响：`tools/fun/coin-toss-streak.html`，概率演示口径不一致。
- 方案：区分最长同面与最长正面，并注明对应概率；可本地保存次数与个人纪录。

### 宾果宣称词库和可复现但缺入口（中，确认源码缺陷）
- 证据：`tools/fun/bingo-generator.html:154-170,193-205,252-275` 文案提词库抽样与公开可复现，界面只生成/重置，固定数值范围使用 `Math.random()`，没有词库或随机种子输入。
- 影响：`tools/fun/bingo-generator.html`，用户无法依说明准备词卡或复现卡片。
- 方案：补词库及去重校验与可分享种子，或删除不支持的承诺；本地保存卡片，分享由用户主动选择。

### 覆盖
- 本轮核查打字节奏及上述娱乐、音乐、棋类 6 页，共 7 页；源码推导未实测浏览器，其他文娱工具未逐页覆盖。

## 2026-11-03 续查（并行批 H）

本批续查 7 页（棋类 3 页、音乐 3 页、娱乐 1 页），均先读源码再用 Node 内存复算页面自身函数取证；未改动任何工具文件，未做浏览器、英文态、移动端、门禁或线上验证。

### FE-N1 Elo 复制结果与历史「结果」列读的是对局结果下拉框（中，确认源码缺陷）
- 描述：复制按钮与历史记录取 `#result` 的文本，但 `#result` 是「胜利/和棋/失败」下拉框，真正的计算输出在 `#resultBox` 与 `#ratingChange`；复制得到的是选项文字，历史「结果」列恒为同一串选项文本。
- 证据：`tools/chess/elo-rating.html:152-155`（`<select id="result">` 三个选项）、`:183`（输出容器 `id="resultBox"`）、`:319`（`ToolBox.copyText($('result').innerText, …)`）、`:406-412`（`__elo_ratingResText` 读取 `document.getElementById('result').textContent`）。全文件仅 `:152` 一处 `id="result"`（检索确认）。源码推导：select 文本为「胜利（1分）和棋（0.5分）失败（0分）」。
- 影响：`tools/chess/elo-rating.html`；复制结果不可用，历史记录无法区分胜负与分数变化。
- 方案：复制改读 `#resultBox`/`#ratingChange`；历史「结果」列改为新等级分或「胜/和/负 + Δ」。

### FE-N2 Elo 深度解析算例与页面公式不符，K=32 不在可选项（中，确认内容缺陷）
- 描述：算例称 1500 vs 1600、胜、K=32 输出「预期胜率约 36.4%」「ΔE≈+22.7」「新分≈1522.7」；按页面公式实际为 36.0%、`Δ=+20.48`、新分 `1520.48`，且 K 下拉只有 40/20/10，没有 32。
- 证据：`tools/chess/elo-rating.html:230`（算例）、`:163-167`（K 选项 40/20/10）。Node 复算（输入 1500、1600、得分 1）：预期得分率 `0.359935`（36.0%，非 36.4%），K=32 → 每局 `+20.4821`、新分 `1520.4821`；K=20（默认）→ `+12.8013`、新分 `1512.8013`。`22.7` 对应 K≈35.5。
- 影响：`tools/chess/elo-rating.html`；用户按算例复现得不到页面结果，示例本身不可信。
- 方案：用页面实跑值重写算例并向算例标注所用 K；若要保留 K=32，应在下拉中新增该档。

### FE-N3 Elo「胜率/败率」实为预期得分率及其补数，drawProb 为死代码（中，确认口径缺陷）
- 描述：页面把 `expectedA` 标为「预期胜率/胜率」、`1-expectedA` 标为「败率」，两者恒互补，等于宣称和棋概率为 0；`drawProb` 已计算却从未渲染。
- 证据：`tools/chess/elo-rating.html:291-293`（`winProb=expectedA*100`、`drawProb=(1-Math.abs(expectedA-expectedB))*50`、`lossProb=(1-expectedA)*100`）、`:299`（「预期胜率」卡）、`:309-312`（「胜率/败率」两条并只画两条进度条）。Node 复算：1500 vs 1500 → 胜率 50、败率 50、drawProb 50（三者合计 150）；1500 vs 1600 → 36.0/64.0，drawProb 36.0。
- 影响：`tools/chess/elo-rating.html`；概率区误导用户，尤其对和棋常见的棋类。
- 方案：改标「预期得分率」并说明含和棋；或引入可输入的历史和棋率再拆分胜/和/负，删除或启用 `drawProb`。

### FE-N4 BPM 超出 40–300 被静默钳制，输入框仍显示原值（中，确认源码缺陷）
- 描述：`getBpm()` 把小于 40 或大于 300 的值钳到边界后直接计算，但只同步滑块、不回写输入框，用户看到的数值与实际计算值不一致；预设「小规模」只改输入 60、滑块仍为 120。
- 证据：`tools/music/bpm-converter.html:495-500`（钳制）、`:503-508`（仅滑块 `value=val`）、`:261`（输入框）、`:836`（预设只写 `bpmInput`）。Node 复算：输入 500 → 按 300 算，四分音符 `200.00 ms`（按 500 应为 `120.00 ms`）；输入 10 → 按 40 算，`1500.00 ms`（按 10 应为 `6000.00 ms`）。
- 影响：`tools/music/bpm-converter.html`；超出范围的 BPM 结果与页面显示的 BPM 不一致，误差可达 4 倍以上。
- 方案：越界时提示并回写输入框，或按实际输入值计算；预设同时同步滑块与输入。

### FE-N5 BPM 反向时长只更新结果，数据表/历史/图表/CSV 保持旧值（低，确认源码缺陷）
- 描述：`calcReverse()` 只写 `#reverseResult`；历史扩展只在 `calcAll()` 外层包装里触发，改「时长/音符类型」不会记录，也不会刷新表格与图表。
- 证据：`tools/music/bpm-converter.html:658-699`（`calcReverse` 无扩展调用）、`:801-829`（`__bpm_converterExtras`）、`:838-840`（只包装 `calcAll`）、`:340`（表格/历史/图表宿主与反推结果同卡）。
- 影响：`tools/music/bpm-converter.html`；只用反推功能时历史为空、CSV 无内容、图表不更新。
- 方案：`calcReverse` 也调用同一记录函数，或把「记录」抽成两处共用的 `record()`；导出前校验表非空并提示。

### FE-N6 和弦解析把 `Cmaj`/`Cmajor` 判成小三和弦（高，确认函数缺陷）
- 描述：后缀匹配在归一化之前用 `suffix.startsWith(s)`，`maj`/`major` 先命中单字符 `m`（小三），永远走不到 `maj→M` 的归一化分支；`Cmaj` 输出 C–D♯–G。
- 证据：`tools/music/chord-notes.html:478-512`（类型表）、`:593-600`（首轮前缀匹配）、`:602-616`（归一化仅在未匹配时执行）。Node 直接执行页面 `parseChord`：`Cmaj` → 类型 `m`、音符 C/D#/G；`Cmajor` → 类型 `m`、C/D#/G；`Cmaj7` → 类型 `maj7`、C/E/G/B（因四字符精确命中而侥幸正确）。
- 影响：`tools/music/chord-notes.html`；常见写法 `Cmaj` 得到错误和弦，音符、频率、播放与复制结果全部错误。
- 方案：先做全等匹配，再做「最长后缀」匹配且优先匹配大写 `M`/已归一化后缀；补 `Cmaj`、`Cmajor`、`Cmin`、`Cminor` 回归用例。

### FE-N7 扩展和弦的九音被标成「二音」，与页内速查表矛盾（中，确认源码缺陷）
- 描述：音程标签用 `semitone % 12` 取名称，`add9` 的 +2 与 `9`/`m9` 的 +14 都落到索引 2「二音」；同页规则表却写「加九和弦 = 大三+九音」。
- 证据：`tools/music/chord-notes.html:475`（`DEGREE_NAMES`，索引 1 为「九音」、索引 2 为「二音」）、`:664-668`（渲染取 `DEGREE_NAMES[note.semitone % 12]`）、`:321`（速查表「大三+九音」）。Node 直接执行页面 `parseChord`：`Cadd9` → 最高音 D 的 `semitone=2`；`C9`、`Cm9` → D 的 `semitone=14`；两值经 `%12` 均取到「二音」。
- 影响：`tools/music/chord-notes.html`；和弦构成说明与自身规则表冲突，学习者会被误导。
- 方案：按原始半音数映射扩展音（2→九音、14→九音，或区分 add9/9），补 `add9`、`9`、`m9` 断言用例。

### FE-N8 未识别后缀静默降级为大三和弦，常用降号根音被判无效（中，确认源码缺陷）
- 描述：无法匹配的后缀直接回退 `[0,4,7]` 大三和弦，不报错；`Cb`/`Fb`/`E#`/`B#` 等合法根音因别名表缺失被 `indexOf` 判为 -1。
- 证据：`tools/music/chord-notes.html:618-621`（默认大三）、`:474`（别名仅 Db/Eb/Gb/Ab/Bb）、`:577-590`（根音查找失败返回 null）。Node 复算：`Cfoo` → 大三 C–E–G；`Cxyz9` → 大三 C–E–G；`Cb` → `null`。
- 影响：`tools/music/chord-notes.html`；拼错或未支持的和弦被当成大三和弦安静输出，降号调根音直接无结果。
- 方案：未识别后缀返回 null 并提示支持列表；补齐 Cb/Fb/E#/B# 及重升重降根音。

### FE-N9 FEN 历史回填调用无参 `loadPreset()`，输入框被写成字符串 `undefined`（高，确认源码缺陷）
- 描述：历史「恢复」回调末尾调用 `loadPreset()` 而不传记录中的 FEN，`presets[undefined]` 为 `undefined`，被写进输入框并渲染为无效局面。
- 证据：`tools/fun/chess-fen-viewer.html:405-418`（回调先按 `rec` 正确回填 `:408-414`，随后 `:416` 调用 `loadPreset();`）、`:329-332`（`value=presets[k]`、`render(presets[k])`）、`:270-274`（presets 仅有 start/mate/endgame）。Node 直接执行页面 `parse`：`parse('undefined')` 返回 `null`，`presets[undefined] === undefined`。
- 影响：`tools/fun/chess-fen-viewer.html`；点击任一条历史记录后输入框显示 `undefined`、棋盘清空、结果变为「无效的 FEN」，历史功能反而破坏当前局面。
- 方案：从 `rec.fen` 取记录值直接 `render(fen)`，空值不覆盖现有局面；补「解析两次 → 点历史第一条 → 局面还原」用例。

### FE-N10 FEN 只校验棋盘段，缺行棋方时一律显示「黑方」且不报错（中，确认源码缺陷）
- 描述：解析只要求 8 行×8 列，完全忽略行棋方、易位、吃过路兵、计数四段；缺第 2 段时 `turn=''`，三元判断落到「黑方」。FAQ 却称「缺段会解析失败」。
- 证据：`tools/fun/chess-fen-viewer.html:276-298`（`parse` 只读 `fen.split(' ')[0]`）、`:316-320`（`turn=parts[1]||''`，非 `w` 即黑方）、`:221`（FAQ 承诺）。Node 直接执行页面 `parse`：仅棋盘段的 FEN、`8/8/8/8/8/8/8/8` 空棋盘、`8/8/8/8/8/8/k7/K7` 双王残局均被接受；`r9/8/…` 因列数超 8 被拒。
- 影响：`tools/fun/chess-fen-viewer.html`；残缺或非法 FEN 得到看似正常的「黑方先走」结论，用户无法察觉输入错误。
- 方案：校验 6 段及字段取值（`w|b`、`KQkq|-`、格位、半回合/回合数），缺段或非法时报错；无王/多王局面给出警告。

### FE-N11 五子棋禁手判定顺序错误，三三/四四分支忽略连子数（高，确认源码缺陷）
- 描述：`three_three`/`four_four` 分支只看 `liveCount`，完全不读 `stoneCount`，长连与五连被误判；`custom` 分支又要求 `stones===5 && live<2` 才判五连，导致「恰好五连同时含活三」被判禁手。
- 证据：`tools/chess/gomoku-forbidden.html:287-296`（只判 `live>=2`）、`:304-309`（`stones===5&&live<2` 优先于 `live>=2`）、`:315-316`（只要 `badge` 含 ok 且 `stones===5` 就追加「五连胜利」提示）。Node 直接执行页面 `analyze()`：`three_three, stones=6, live=2` → 「三三禁手」（应为长连禁手）；`three_three, stones=5, live=1` → 结果栏「非禁手/合法」同时追加「✅ 五连胜利」提示（同一弹窗自相矛盾）；`four_four, stones=6, live=2` → 「四四禁手」；`custom, stones=5, live=2` → 「三三/四四禁手」（五连应优先判胜）。
- 影响：`tools/chess/gomoku-forbidden.html`；黑棋长连、五连等核心规则判定错误，用户按结果对局会判错胜负。
- 方案：按「长连（≥6）→ 五连（=5）胜利 → 三三/四四」统一顺序判定，三三/四四分支也读取连子数；补上述三组回归用例。

### FE-N12 五子棋禁手页宣称自动识别活三/冲四/连五，实际无棋盘与落子输入（中，确认功能缺失）
- 描述：说明写「落子后自动识别活三、冲四与连五」，但页面只有「棋型类型」下拉和两个数字框，没有棋盘、没有落子坐标，判定完全依赖用户自报的活子数；预设还把 `liveCount` 设为 6，超过输入框 `max=4`。
- 证据：`tools/chess/gomoku-forbidden.html:142`（公式说明）、`:146-163`（仅 select + 两个 number 输入）、`:282-310`（`analyze` 只读这三项）、`:496`（预设 `liveCount:'6'`）与 `:162`（`max="4"`）。
- 影响：`tools/chess/gomoku-forbidden.html`；用户无法输入真实棋局，「判断器」名不符实，宣传能力高于实际。
- 方案：提供 15×15 棋盘落子并按四方向扫描活三/四/五，或删除自动识别承诺并把标题改为「禁手规则速查/参数演示」；修正越界预设。

### FE-N13 变速页降速时仍显示「提速 -25%」，“-”号与「提速」自相矛盾（中，确认源码缺陷）
- 描述：百分比文案固定为「提速 + 数值%」，未区分加速与降速；等速时显示「提速 0%」。
- 证据：`tools/music/convert-speed.html:166`（`'提速 '+((nb/ob-1)*100).toFixed(0)+'%'`）。Node 复算：180 s、120→90 → 新时长 `240.0` 秒、「提速 -25%」；120→120 → 「提速 0%」；180 s、120→140 → 「提速 17%」。
- 影响：`tools/music/convert-speed.html`；降速场景文案方向错误，用户容易误读为加速。
- 方案：按比值分支输出「提速 +X%」「降速 X%」「不变」，并与第二段换算链保留两位小数的口径统一。

### FE-N14 变速页宣传「对音频做变速处理、支持实时试听」，页面无音频能力（中，确认内容缺陷）
- 描述：meta、工具简介与功能特点均承诺音频变速与实时试听，实际只有三个数字输入与纯算术输出，没有任何音频元素、Web Audio 或文件读取代码；参考表列出的 cents 音高偏移也未实现。
- 证据：`tools/music/convert-speed.html:10`、`:14`、`:31`（meta 描述）、`:251`、`:256`（简介与「即时试听」）、`:124-127`（仅 `dur/ob/nb` 数字框）、`:166`（纯计算）、`:142-144`（列 cents 公式但无对应计算）。全文检索无 `audio`/`play`/`AudioContext`。
- 影响：`tools/music/convert-speed.html`；用户按文案寻找试听或音频处理功能而找不到，属于能力虚标。
- 方案：删除试听/音频处理承诺并把页面定位为「BPM 与时长换算」；若确需音频，补文件选择、`AudioBufferSourceNode.playbackRate` 与音高提示，并另行做真机验证。

### FE-N15 象棋残局「一步杀」5 条中 4 条含两步红方着法（中，确认内容缺陷）
- 描述：「一步杀」分类的解法普遍出现两着红棋，甚至把「红帅镇守」这种非着法写成第 2 步，与「一步杀」定义不符。
- 证据：`tools/chess/xiangqi-endgame.html:250-254`（one 列表）。Node 读取页面 `ENDGAMES` 统计红方着法：重炮绝杀 2 着、白脸将 2 着、双车错 2 着、大刀剜心 2 着、闷宫杀 1 着（5 条中 4 条 >1 着）。
- 影响：`tools/chess/xiangqi-endgame.html`；训练分类失真，用户按「一步杀」练习会得到两步杀题。
- 方案：把这 4 条迁入「两步杀」或改写为真正的单着绝杀；渲染前按红方着法数断言分类。

### FE-N16 残局页面称「输入某残局并判一步杀」，实际只有静态题库；查阅频次按卡片标题串统计（中，确认内容/功能缺陷）
- 描述：深度解析演示「输入某残局，工具展示着法序列并判一步杀」，页面没有任何输入控件或判定逻辑；历史频次记录的是当前所有展开卡片的标题拼接串，开两张卡就记成「A + B」一条，频次图不可解释。
- 证据：`tools/chess/xiangqi-endgame.html:199`（输入并判定的描述）、`:137-152`（仅 tab 按钮、导出按钮、隐藏表格，无 input）、`:390-408`（`lab` 为 `.endgame-card.open` 标题 join，`hist.push({l:lab})`，按 `l` 计数）。源码推导：依次展开 A、B 后条目为「A + B」，再关 A 展开 C 变为「B + C」。
- 影响：`tools/chess/xiangqi-endgame.html`；宣传的交互判定不存在；历史/CSV 中的「条目」不是单个残局，频次统计失真。
- 方案：删除「输入/判定」表述并改为「残局题库速查」；`toggleCard` 只记录被点击的单个残局标题（去重计数），历史表增加分类与步数列。

### 留存优化
- `tools/chess/elo-rating.html`：本地保存常用「我的分/对手分/K/局数」组合与最近对局序列，便于赛后连续估算；仅存本机、可一键清空。
- `tools/music/chord-notes.html`：复用已有本地历史，增加「收藏和弦清单/最近 10 个和弦」与一键生成和弦卡文本，方便练习复盘。
- `tools/music/bpm-converter.html`、`tools/music/convert-speed.html`：本地保存常用 BPM、采样率与「原 BPM→目标 BPM」对照表，支持多曲目批量换算。
- `tools/fun/chess-fen-viewer.html`、`tools/chess/xiangqi-endgame.html`：本地收藏 FEN 局面与残局学习进度（已会/待复习），历史改为按单项记录，避免组合标题污染频次。

### 续查覆盖
- 本批覆盖 `tools/chess/elo-rating.html`、`tools/chess/gomoku-forbidden.html`、`tools/chess/xiangqi-endgame.html`、`tools/music/bpm-converter.html`、`tools/music/convert-speed.html`、`tools/music/chord-notes.html`、`tools/fun/chess-fen-viewer.html` 共 7 页，新增 16 条（高优 3 条：FE-N6、FE-N9、FE-N11）；均为源码与 Node 内存复算证据，未做真实浏览器、英文态、移动端、门禁或线上验证。
- 已覆盖页与既有记录不重复：本文件前述已查 `typing-rhythm`、`coin-toss-streak`、`bingo-generator`、`bridge-scoring`、`go-territory`、`beat-subdivision`、`freq-note-converter`，本批未重复审计。
