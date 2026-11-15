# 商业综合/创业 · tools/{biz,startup}（75 页）

## 2026-11-03 审计补充

### 留存优化：采购比较考虑附加费用（低，建议）
- 证据：同页 `:106,116-139,287-305` 文案提及运费及多件促销，但实际输入为两商品数量、单位和价格。
- 影响：同页；方案：按商品加入选填运费、促销总件数，展示标准单位单价和每次采购节省额，支持复制结果。

### 会议计时把一次性费用按小时计入（中，确认函数缺陷）
- 问题与证据：`tools/biz/meeting-cost-calculator.html:341-350,386-404` 常规计算将场地费直接加总，实时计时却按 `roomCost/3600*elapsed` 增长；1 人时薪 100、场地费 600、计时 30 分钟，原函数得到 350 元，按一次性费用应为 650 元。
- 影响：`tools/biz/meeting-cost-calculator.html`，计划和实时结果口径冲突。
- 方案：实时计时按一次性费用计算；若需要按时费用，另以明确单位区分。可本地保存计划与实际耗时成本对照。

### 融资稀释后复制仍是融资前股权（高，确认函数缺陷）
- 问题与证据：`tools/startup/equity-calculator.html:437-459,498-510` 展示按融资比例稀释，复制函数重新算融资前股权；一名创始人、期权池 0%、投前 5000 万、投资 1000 万，原函数展示创始人 83.33%、投资人 16.67%，复制却为创始人 100% 且缺投资人。
- 影响：`tools/startup/equity-calculator.html`，复制用于沟通时可能传播错误股权。
- 方案：展示、复制及导出使用同一最终结构并列出融资轮与投资人；可本地保存多轮融资情景对比。

### 覆盖
- 本轮核查 `tools/biz/unit-price-compare.html`、`tools/biz/meeting-cost-calculator.html`、`tools/startup/equity-calculator.html` 共 3 页；新增 2 个缺陷及 2 条建议。后两页为内存 DOM 桩执行，未实测浏览器、系统剪贴板或其他商业页。

## 2026-11-03 续查（并行批 I）

> 编号沿用本文件新启前缀 `BS-N`（与 `RE-N` / `06-F` 同批体例），互不重号；上一节 3 页不重复核查。全部结论基于源码阅读 + node 内存复算，未打开浏览器，未做 EN / 繁体 / 移动端 / 门禁验证。

### BS-N8 商业计划书实际只生成 9 板块，三处文案称 10 板块（中，确认）
- 描述：`SECTIONS` 仅 9 项，缺「竞争分析」「风险与应对」；深度解析与引据表却按 10 板块描述，简介又写「九大板块」。
- 证据：`tools/startup/business-plan.html:264-274`（9 项：summary/company/market/product/model/marketing/team/finance/funding）；`:210` 列 10 项含竞争分析与风险；`:214` 称「工具按标准 10 板块生成」；`:232` 引据表写「标准10板块」；`:150` 简介写「九大板块」。
- 影响：用户按深度解析准备竞争与风险内容却无输入框，导出的 BP 缺两个投资人常看模块，文案与产品能力不一致。
- 方案：补「竞争分析」「风险与应对」两个 textarea 并接入导出模板；或把 `:210/:214/:232` 统一降为 9 板块口径。

### BS-N9 路演大纲三处「标准 10 页」页序互不相同（低，确认）
- 描述：页面要点、深度解析、深度解析算例给出三套不同 10 页顺序，实际 `SLIDES` 与要点一致。
- 证据：`tools/startup/pitch-deck.html:188`（封面→问题→解决方案→时机→市场规模→产品→商业模式→团队→数据→融资）；`:225`（问题→解决方案→市场机会→产品演示→商业模式→竞争优势→团队→财务→融资→愿景，无封面/时机）；`:229` 算例顺序又不同；`:279-290` 实际 `SLIDES` 与 `:188` 一致。
- 影响：用户按深度解析准备时与实际生成大纲错位（导出的第 4 页是「时机」而非算例里的「产品演示」）。
- 方案：以 `SLIDES` 为唯一口径，统一 `:225`、`:229` 文字；或明确说明「10 页为标准模板，可按受众调序」。

### 留存优化
- 估值页：结果区按方法分组并标注量纲校验结论，提供「只选 2 种方法对比」与本地情景保存（避免把 5 种口径混成一个平均数）。
- 烧钱率页：一次性费用与按月费用分栏录入、按天计算耗尽日、导出本月与上月净消耗对比，而非仅累积 24 条快照。
- 文本类页面（business-plan / pitch-deck）：导出前清洗文件名（去掉 `/ : * ? " < > |`），支持 Markdown 回填导入；文本工具挂载的「历史 + 导出明细 CSV」应改为草稿版本对比。
- 质检页：加输入钳制与「未填」态提示，输出改为分维度强弱排序（先改短板）而非只给总分。

### 续查覆盖
- 本轮核查 7 页：`tools/startup/valuation-calculator.html`、`tools/startup/burn-rate.html`、`tools/startup/business-plan.html`、`tools/startup/pitch-deck.html`、`tools/startup/calc-1.html`、`tools/biz/checker-8.html`、`tools/biz/summary-rater-csat.html`；新增 12 条（高 1 / 中 8 / 低 3）。
- 上一节已覆盖的 `unit-price-compare`、`meeting-cost-calculator`、`equity-calculator` 未重复核查。
- 本轮全部为源码阅读 + node 内存复算，未打开浏览器，未验证 EN / 繁体 / 移动端 / 门禁；`tools/biz/analysis-manager`、`assessor-risk-8`、`assessor-49`、`analysis-47`、`stats-time-response` 及 `tools/startup/index.html` 分类页仍未查。

## 2026-11-03 续查（并行批 K）

> 范围：本轮实读 8 页（路径见文末覆盖行）。`tools/startup/` 除分类页外已全部覆盖，故补充 `tools/project/` 的项目管理/经营综合页。仅源码 + node 复算，未开浏览器、未做 EN / 移动端 / 门禁验证。

### BS-N22 风险排查：删光风险点后仍显示「低风险-常规管理」（中，确认）
- 描述：风险点可被全部删除，`results` 为空时 `maxRisk=0`，总体等级落到 `else` 分支「低风险-常规管理」，页面仍显示「共识别 0 个风险点」。
- 证据：`tools/biz/assessor-risk-8.html:196-199`（删除无下限）、`:216`、`:218-221`。
- 复现：点 3 次 × 删光默认风险点 → 总体「低风险-常规管理」、风险点总数 0、高/中/低均 0；期望「未录入风险点，请先添加」。
- 影响：空表被当成「零风险」绿灯，评审时可能据此放行。
- 方案：`results.length===0` 时输出中性提示并禁用评级/参考标尺；`removeRisk` 保留至少 1 项，或允许清空但明确「未知」而非「低风险」。

### BS-N23 风险排查：参考标尺永不渲染，风险名未转义会截断输入（低，确认）
- 描述：① 标尺条件 `typeof value==='number'` 引用了不存在的变量（`value` 只在 map 回调内声明），`#resRefBar` 始终为空；② 风险名未经转义写入 `value` 属性与结果表，含 `"` 时重渲染会截断名称。
- 证据：`tools/biz/assessor-risk-8.html:258`（`typeof value`）、`:180`（`value="'+r.name+'"`）、`:233`（表格 `r.name`）。
- 复现：任意输入下 `#resRefBar` 始终为空；把风险名改为 `A"B` 后点「+ 添加风险点」→ 该输入框回显 `A`（其余被当属性丢弃），表格也可能被截断。
- 影响：标尺功能缺失；名称含英文引号或 `<` 时数据丢失/布局破坏。
- 方案：标尺改用 `maxRisk`；名称渲染前 `ToolBox.escHtml`，表格同样转义。

### BS-N24 干系人分析：增删干系人会静默丢弃已编辑内容（中，确认）
- 描述：`renderSh()` 只从 `shData` 重建，而名称输入与权力/利益下拉都没有把编辑写回 `shData`；点「+ 添加干系人」或「×」会用旧值重绘。
- 证据：`tools/project/analysis-28.html:212-223`（renderSh 读 shData）、`:216-218`（输入/下拉无回写）、`:225-226`。
- 复现：把「业主/投资方」权力 5 改为 1、名称改为「甲方」，不点「分析矩阵」，直接点「+ 添加干系人」→ 业主恢复权力 5 与原名称；期望保留编辑。
- 影响：增删行会丢失已录入的干系人信息，用户需重填。
- 方案：重绘前先 `syncShFromDom()` 从当前 DOM 回写 `shData`；或给输入/下拉加 `oninput/onchange` 即时更新。

### BS-N25 干系人分析：象限与「需重点应对」用两套阈值，重点管理可落选（低，确认）
- 描述：象限按权力/利益阈值（p≥3 且 i≥3 为「重点管理」），重点清单却用 `score>=10`；两者不同源。
- 证据：`tools/project/analysis-28.html:235-240`、`:245-246`。
- 复现：只保留一名干系人权力 3、利益 3 → 结果「重点管理」，但下方无「需重点应对」提示；权力 2、利益 5 → 结果「随时告知」，却被列入「需重点应对（关注度≥10）」。
- 影响：同一页面两套优先级口径，沟通资源可能投给错误对象。
- 方案：统一以象限为主，重点清单取「重点管理」象限；或把清单标题改为「关注度≥10（不等于重点管理）」并单列象限优先级。

### BS-N26 项目风险循环：参考标尺取第 5 项风险值而非最高值（中，确认）
- 描述：标尺读取 `score`，而 `score` 是 for 循环里的 `var`，循环结束后等于第 5 项风险值，不是上方展示的 `maxScore`。
- 证据：`tools/project/assessor-risk-9.html:213-215`（`var score=p*imp`）、`:221`（maxScore）、`:240`（refBar 用 `score`）。
- 复现：前 4 项设 5×5=25，第 5 项设 1×1=1 → 上方「最高风险值 25 / 25」「整体极高风险」，参考标尺却显示 1（低风险区）。
- 影响：同一结果卡内两个风险结论互相矛盾，读者可能按标尺的低风险色放松处置。
- 方案：标尺改用 `maxScore`；若需展示逐项分布，另设数组传参，不复用循环变量。

### BS-N27 项目风险循环：10–15 档在公式框叫「较高」、结果卡叫「高风险」（低，确认）
- 描述：公式框把 10–15 称「较高」、16–25 称「高风险」，结果卡却把 10–15 标「高风险」、16–25 标「极高风险」，同一档两种叫法。
- 证据：`tools/project/assessor-risk-9.html:125`（公式框）、`:219-220`（代码分级）。
- 复现：任一项 3×4=12 → 结果「高风险」；按公式框应称「较高」。5×5=25 → 结果「极高风险」；公式框称「高风险」。
- 影响：对照公式框复核时误判等级，10–15 档容易被当成最高档。
- 方案：统一四档命名（低/中/较高/高 或 低/中/高/极高），同步公式框、结果卡、图例与 CSV。

### BS-N28 HSE 检查：关键项 0 分仍可评「优秀」，缺一票否决（高，确认）
- 描述：10 项纯加总评分，没有「关键项一票否决」；页面自己称为「一票否决/重大隐患」的特种作业持证项即使 0 分，其余 9 项满分仍得 18 分判「优秀」。
- 证据：`tools/project/checker-training-hr-1.html:208`（纯 `total+=`）、`:211-214`（仅按总分分级）、`:157`、`:164`（一票否决/即时停工表述）。
- 复现：仅「特种作业持证」选不达标（0 分），其余 9 项均达标（2 分）→ 总分 18/20、达标率 90%、等级「优秀」，建议「安全管理体系健全」；期望触发「重大隐患/停工整改」而非优秀。
- 影响：HSE 自评可能把无证上岗等重大隐患判为优秀，直接违背页面 FAQ 与法规要求，安全风险高。
- 方案：为关键项（特种作业持证、重大隐患等）设否决位：任一为 0 时整体最高只能「不合格/限期整改」并置顶红色提示；或在总分旁单列「关键项」状态。

### 续查覆盖（K 批）
- 本轮实读 8 页：`tools/biz/analysis-47.html`、`tools/biz/analysis-manager.html`、`tools/biz/stats-time-response.html`、`tools/biz/assessor-49.html`、`tools/biz/assessor-risk-8.html`、`tools/project/analysis-28.html`、`tools/project/assessor-risk-9.html`、`tools/project/checker-training-hr-1.html`；新增 16 条（高 2 / 中 9 / 低 5）。
- 未覆盖：`tools/biz` 其余文本/命名类页面、`tools/startup/index.html` 分类页；另顺带阅读 `tools/project/checker-12.html`（仅「合格/一般」命名与深度解析薄弱项映射等低优文案不一致，未单列）。

## T 批 商业文本工具覆盖（2026-11-04）

### BS-N37 文本分割：按字符数用 UTF-16 长度与 `substr`，emoji 被劈成孤立代理项（中，确认缺陷）
- 问题：`text.length` / `substr` 按码元计数，补充平面字符（emoji、生僻字、部分符号）占 2 个码元，切点落在代理对中间。
- 证据：`tools/biz/text-split.html:326-329`。
- 复现：选「按字符数」、长度填 1，输入 `😀😀ab` → 6 段，前两段分别为 `\uD83D`、`\uDE00`（node 复算），粘贴/导出显示为 `�`；期望 4 段（😀/😀/a/b）。
- 影响：社媒文案、含 emoji 的 CSV 被切坏后不可逆（复制出去即乱码），且段数与「共 N 段」全部偏大。
- 方案：用 `Array.from(text)` 或 `Intl.Segmenter('und',{granularity:'grapheme'})` 按码点/字素切分，长度也按码点计。

### BS-N38 文本分割：复制结果取 `innerText`，序号粘在内容前且段间无分隔（中，确认缺陷）
- 问题：结果区是 `<div class="result-block"><span class="idx">N</span>内容</div>`，`copyResult()` 复制 `result.innerText`，序号与内容同属一行文本。
- 证据：`tools/biz/text-split.html:341-343`（模板含 `.idx`）、`:350-351`（`document.getElementById('result').innerText`）。
- 复现：默认示例按分隔符分割 → 复制落到剪贴板的是 `1apple` / `2banana` / …（node 复算形态 `[1]apple`），期望 `apple\nbanana…` 纯内容。
- 影响：复制结果粘回输入框或其它系统时序号污染数据；用户还需手工删序号，定长切分场景尤其致命。
- 方案：维护一份 `lastParts` 数组，复制时 `join('\n')`；或在 `.idx` 上加 `user-select:none` 并额外用 `CSS.escape` 拆分文本节点，最稳是直接用数组。

### BS-N39 文本统计：英文句号不计入句子数，平均句长与阅读难度整段失真（中，确认缺陷）
- 问题：句子只认 `。！？!?`，英文 `.` 缺失；无中文标点时 `|| 1` 兜底成 1 句，于是「平均句长 = 全部词数」，难度阈值直接被击穿。
- 证据：`tools/biz/text-stats.html:303`（`/[。！？!?]+/g` 与 `|| (text.trim()?1:0)`）、`:332-336`（平均句长与 25/15 阈值）、`:157`（公式框同样只写这四类标点）。
- 复现：100 个英文单词、3 句（句号分隔）→ 输出「句子数 1、平均句长 100.0 词/句、阅读难度 困难」（node 复算）；期望 3 句、约 33 词/句、中等。
- 影响：英文/中英混排文本的「平均句长」「阅读难度」恒为困难档，是页面主打的易读性指标，结论方向性错误。
- 方案：句子切分改为 `/[。！？!?]+|[.!?]+(?=\s|$)/g`（并排除 `...`/小数点的误判），或直接按 `Intl.Segmenter('en',{granularity:'sentence'})`；公式框同步补英文句号口径。

### BS-N40 文本统计：「总行数」把末尾换行多算一行（中，确认缺陷）
- 问题：`text.split('\n').length` 在末尾有换行时返回多一个空串；`非空行` 有过滤，`总行数` 没有。
- 证据：`tools/biz/text-stats.html:300`（`text.split('\n').length`）、`:301`（同一 split 后再过滤，口径不一致）、`:333`（平均行长用该 `lines`）。
- 复现：输入 `a\nb` → 总行数 2；在编辑器末尾回车一次（`a\nb\n`）→ 总行数 3、平均行长被摊薄（node 复算 `parts=["a","b",""]`）。
- 影响：写作类用户常见的"末尾留空行"会让行数与平均行长漂移，与「非空行」并列展示时自相矛盾。
- 方案：`lines = text.replace(/\n$/,'').split('\n')`（或仅当末元素为空时 `pop()`）；`平均行长` 改用同一 `lines` 口径并注明是否含空行。

### BS-N41 注释生成器：HTML/CSS 单行注释不闭合、横幅边框不是注释、YAML 块注释非法（中，确认缺陷）
- 问题：① `line` 配置对 html 是 `<!--`、css 是 `/*`，单行模式只拼 `前缀 + 内容`，永不补 `-->` / `*/`；② banner 顶/底边线是裸 `=` 串；③ 非 html/python/ruby 的块注释统一加 `' * '`，YAML 的注释符是 `#`，混入 ` * ` 行即非法。
- 证据：`tools/biz/comment-generator.html:324-325`（html/css 的 `line`）、`:358-359`（line 分支不闭合）、`:376-385`（banner 的 `sep = '='.repeat(...)`）、`:329` + `:365-367`（YAML `#` 却走 ` * ` 分支）。
- 复现：HTML 选「单行注释」输入「说明」→ 生成 `<!-- 说明`（无 `-->`）；CSS 同理 `/* 说明`（无 `*/`），粘进样式表会吞掉后续规则；JS 选「横幅注释」→ `===================\n//  说明  //\n===================`（node 复算），首尾行是裸 `====` 语法错误；YAML 选「块注释」→ `#\n * 说明\n#`，中间行不构成注释。
- 影响：生成结果直接复制即破坏目标文件（CSS 整段失效、JS 语法报错、YAML 解析失败），属于"生成器输出不可用"。
- 方案：单行模式按语言给出成对包裹（`<!-- … -->`、`/* … */`）；banner 边线改用 `(cfg.line+' ').repeat(n)` 或行内 `//`/`#` 包裹；块注释分支按语言白名单（html/python/ruby/bash/yaml 各自单独处理），YAML 统一走 `#` 行注释。

### T 批覆盖清单（8 页）
- `tools/biz/text-replace-advanced.html`：**未发现 XSS**：替换结果走 `textContent`，匹配列表的 `match/groups` 已 `escapeHtml`。另记（未单列，低）：非正则模式下替换串仍按 `$&`/`$$` 解释，替换"原文含 `$&`"会变成插入整个匹配；复制按钮回调引用全局 `event`，Firefox 下无「已复制」反馈。
- `tools/biz/text-extract-html-tags.html`：2 条（BS-N31、BS-N32，均中）。另记（未单列，低）：清空输入时只重置 `count`，`uniqueCount` 保留上一次数字；FAQ 所称「仅正文标签」过滤与简介所称「指定标签」入口均不存在。
- `tools/biz/text-remove-duplicates-lines.html`：2 条（BS-N33、BS-N34，均中）。`trimLine`/`removeEmpty`/`sortResult` 与六种模式均真实生效，未发现 XSS（结果走 `textContent`）。
- `tools/biz/text-sort-advanced.html`：2 条（BS-N35、BS-N36，均中）。`random`/`reverse`/`natural` 与长度模式实算正常；`lex-zh` 不响应「忽略大小写」（低，未单列）。
- `tools/biz/text-merge.html`：**未发现中/高**。骨架正确：`\n` 分隔符特判、`custom` 空值回退、`skipEmpty` 为显式选项。仅记低优：`prefix`/`suffix` 输入框没有 `oninput`，改后需手动点「合并」才刷新，与同页其它输入不一致；`var currentMode` 是死变量。
- `tools/biz/text-split.html`：3 条（BS-N29 高；BS-N37、BS-N38 中）。`result.innerHTML` 对每段做 `escapeHtml`，未见注入；正则分隔符编译失败已 try/catch 提示。
- `tools/biz/text-stats.html`：2 条（BS-N39、BS-N40，均中）。统计卡片由数字与静态标签拼成，无用户文本注入；`bytes` 用 `Blob` 取 UTF-8 字节，正确。
- `tools/biz/comment-generator.html`：1 条（BS-N41，中）。12 种语言 × 5 种样式均按配置表生成；`result.textContent` 输出，无 XSS。

- 说明：本轮为**只读**审计，结论来自逐行阅读源码 + `node` 在 `/tmp` 复刻关键函数实算（脚本 `/tmp/tb_repro.js`、`/tmp/tb_repro2.js`）；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，未修改任何工具页或构建产物。新增 13 条（高 1 / 中 12）。

## U 批 · 商业文本处理（2026-11-04）

只读审计 10 页文本处理工具（`text-wrap` / `text-trim` / `justify-text` / `text-to-slug` / `text-line-numbers` / `text-compare` / `text-extract-dates` / `text-extract-urls` / `text-extract-emails` / `text-extract-numbers`），逐行读源码 + `node` 在 `/tmp` 复刻核心函数复算（含 Unicode、全半角、正则边界）。**未修改工具页/代码/构建产物，未跑 `_build.py` / `run_gates.py`，未做 git 写操作。**

### BS-N49 文本修剪：「删除空行」只认严格空串，纯空格行不删也不合并（中，确认缺陷）
- 页面：`tools/biz/text-trim.html`
- 问题：`removeDupEmpty` 与 `removeEmptyLines` 都以 `lines[i] === ''` 判空，行内只有空格/制表/全角空格的行不算空行。
- 证据：`tools/biz/text-trim.html:297`（`var isEmpty = lines[i] === ''`）、`:303`（`filter(l => l !== '')`）。
- 复现：输入 `a\n   \nb` 并勾选「删除空行」→ 仍为 3 行，`   ` 原样保留；期望 2 行（node 复算）。
- 影响：从网页/表格复制来的「看起来是空行」永远清不掉，工具核心用途打折。
- 是否假工具：否
- 方案：判空统一为 `l.trim() === ''`（如需保留全角空格语义，可用 `/[ \t\u3000\u00a0]*/` 判空）。

### BS-N50 文本修剪：全角空格能力未实现，FAQ 指向不存在的「含全角」开关（中，承诺未实现）
- 页面：`tools/biz/text-trim.html`
- 问题：简介写「可选去除全角空格」，FAQ 写「全角空格需开启『含全角』才清」，但 UI 只有「去除所有 Tab / 去除所有空格 / 合并多个空格」等，没有「含全角」控件；`trimAllSpaces` 与 `collapseSpaces` 只处理 ASCII `[ \t]`/`[ ]+`。另外 FAQ 说「普通 trim 只去半角空格与制表」也不成立，JS `trim()` 会去掉 U+3000。
- 证据：`tools/biz/text-trim.html:10`（meta 承诺）、`:163-172`（控件清单）、`:227`（FAQ）、`:288-289`（实现）。
- 复现：输入 `a\u3000\u3000b`（全角空格）勾「去除所有空格」→ 原样保留；换 NBSP 同样；期望按承诺得到 `ab`（node 复算）。
- 影响：用户按 FAQ 找不到开关，中文排版常见的全角缩进无法清理。
- 是否假工具：否（功能真实，承诺未实现）
- 方案：新增「含全角/含不间断空格」开关并把 `\u3000`、`\u00a0` 纳入字符类；或删除简介/FAQ 中的该项承诺。

### BS-N51 行号工具：「行号右对齐」复选框从未参与渲染，是死控件（中，承诺未实现）
- 页面：`tools/biz/text-line-numbers.html`
- 问题：`rightAlign` 只被读取到变量，`apply()` 的拼接逻辑完全没用它；预设示例还把 `rightAlign:true` 写进参数，但输出与关闭时一致。
- 证据：`tools/biz/text-line-numbers.html:191`（复选框）、`:308`（读取）、`:325-341`（拼接只用 `padNum` + `prefix`）、`:474`/`:476`（预设带 `rightAlign:true`）。
- 复现：任意输入（如 `a\nb`）切换该复选框 → 结果逐字节相同（node 复算两种状态一致）；期望开启后用空格把行号补到统一宽度（右对齐），关闭时左对齐/补零。
- 影响：用户勾选后看不到任何变化，误以为功能失效。
- 是否假工具：否（功能真实，控件未实现）
- 方案：`prefix` 生成后按目标宽度 `' '.repeat(width - n.length) + n`，或删除该复选框与预设字段。

### BS-N52 行号工具：负数起始值补零把符号夹在中间，输出 `0-5`（中，确认缺陷）
- 页面：`tools/biz/text-line-numbers.html`
- 问题：`padNum` 直接在 `String(num)` 前补 `0`，不区分负号；`-5` 补到 3 位得到 `0-5`。
- 证据：`tools/biz/text-line-numbers.html:294-298`（`while(s.length<width) s='0'+s`）、`:325`（调用）、`:303`（起始值允许负数）。
- 复现：起始 `-5`、步长 1、补零宽度 3 → `0-5. a`、`0-4. b`；期望 `-05. a` 或 ` -5. a`（node 复算）。
- 影响：倒计时、倒数编号的符号位置错误，看起来像非法数字。
- 是否假工具：否
- 方案：拆出符号位，对绝对值补零后再拼回 `-`。

### BS-N53 行号工具：空输入仍输出可复制的 `1. `，空格行也照常编号（中，确认缺陷）
- 页面：`tools/biz/text-line-numbers.html`
- 问题：空输入经 `''.split('\n')` 得到 `['']`，循环后 `result.join('\n')` 为 `"1. "`，非空字符串绕过 `|| '（无内容）'`；`skipEmpty` 也只判 `line === ''`，纯空格行仍编号。
- 证据：`tools/biz/text-line-numbers.html:310`（`input.split('\n')`）、`:321`（`skipEmpty && line === ''`）、`:344`（`join('\n') || '（无内容）'`）。
- 复现：清空输入框 → 结果区显示 `1. `，点复制得到 `1. `；勾「空行不编号」输入 `a\n   \nb` → `3.    ` 仍被编号（node 复算）。期望空输入显示「（无内容）」，空格行视为空行。
- 影响：清空后仍能复制出伪内容，粘贴到文档里多出一行无意义编号。
- 是否假工具：否
- 方案：`if(!input.trim())` 直接显示「（无内容）」；`skipEmpty` 判 `line.trim()===''`。

### BS-N54 文本对比：相似度把「改一行」双计为删+增，指标被系统性压低（中，确认缺陷）
- 页面：`tools/biz/text-compare.html`
- 问题：LCS 回溯把不同行拆成「左侧删除」与「右侧新增」两条，`total = same + del + add`，一次修改贡献 2 个非相同项。
- 证据：`tools/biz/text-compare.html:356-364`（`same/del/add` 统计与 `Math.round(same/total*100)`）。
- 复现：3 行文本仅第 2 行改动 → 相同 2、左独有 1、右独有 1、相似度 50%；期望 67%（2/3）。默认示例 → 38%（3/8）而非 3/6=50%（node 复算）。
- 影响：改一行就让相似度腰斩，用户会误判两份文档差异很大；「左侧独有/右侧独有」也把修改行重复计数。
- 是否假工具：否
- 方案：相似度改用 `2*same/(m+n)` 或 `1 - editDistance/max(m,n)`；统计上把相邻 del/add 行归并为「修改」。

### BS-N55 文本对比：简介承诺「逐行或按词高亮」，实现只有行级 LCS（中，承诺未实现）
- 页面：`tools/biz/text-compare.html`
- 问题：全文只有行级 LCS 与整行 same/del/add 标记，没有任何词级 diff；页面 title/meta 均写「逐行或按词高亮」。
- 证据：`tools/biz/text-compare.html:10`（meta）、`:310-349`（`getLines` + 行级 dp/回溯）。
- 复现：左右分别为 `foo bar` 与 `foo baz` → 整行被判为删除/新增，行内 `bar`→`baz` 无按词高亮；期望仅高亮发生变化的词。
- 影响：代码评审/文档校订时无法定位行内改动，标题承诺落空。
- 是否假工具：否（功能真实，承诺未实现）
- 方案：对相邻的 del/add 行再做词级 LCS（按空白分词）并渲染 `<mark>`，或把文案改为「逐行高亮」。

### BS-N56 文本对比：LCS 全矩阵无规模上限，大文本可卡死/崩溃标签页（中，崩溃风险）
- 页面：`tools/biz/text-compare.html`
- 问题：一次性分配 `(m+1)×(n+1)` 的二维数组，无行数/单元数上限，也无 try/catch 或超限提示；对比在点击时同步执行，会阻塞主线程。
- 证据：`tools/biz/text-compare.html:323`（`Array.from({length:m+1},()=>new Array(n+1).fill(0))`）、`:332-349`（回溯）。
- 复现/估算：左右各 5,000 行 → 25,000,000 个单元，仅数值就约 190MB，加上数组对象开销更高；各 10,000 行 → 10^8 单元。实际点击会长时间无响应，低内存设备易 OOM 崩溃。
- 影响：大日志/大文档对比把标签页打死，用户无法得到任何结果。
- 是否假工具：否
- 方案：先校验 `m*n` 上限并提示拆分；算法改 Myers diff 或 Hirschberg（O(min(m,n)) 内存）。

### BS-N62 Slug 生成：转拼音不处理多音字，未收录字原样混入并与拼音黏连（中，确认缺陷）
- 页面：`tools/biz/text-to-slug.html`
- 问题：`chineseToPinyin` 逐字查单字表（仅 `你好` 一个双字词条），多音字永远取表内单一读音；表外汉字不转换，直接拼进输出，和相邻拼音无分隔。
- 证据：`tools/biz/text-to-slug.html:309-311`（`PINYIN_PACKED` 构建单字表）、`:351-373`（逐字转换，未命中 `out += one`）、`:363`。
- 复现：`重庆`→`zhong-qing`（期望 `chong-qing`）、`银行`→`yin-xing`（`yin-hang`）、`音乐`→`yin-le`（`yin-yue`）、`长沙`→`zhang-sha`（`chang-sha`）；`厦门`→`厦men`（「厦」未收录，中文与 `men` 黏连）；`龘`→`龘`（node 实跑页面内嵌字典）。
- 影响：地名、机构名、人名 slug 读音错误；输出夹带中文，复制进 URL 后需再转义或 404。
- 是否假工具：否
- 方案：增加多音字词组表/先分词再注音；未收录字统一丢弃或转 `uXXXX` 并补分隔符。

### U 批覆盖清单（10 页）
- `tools/biz/text-wrap.html`：4 条（BS-N45 高；BS-N46、BS-N47、BS-N48 中）。字符模式、词模式、填充、对齐均已实跑；未发现 XSS（结果走 `textContent`）。
- `tools/biz/text-trim.html`：2 条（BS-N49、BS-N50，均中）。六类修剪顺序与公式一致；全角能力仅停留在文案。
- `tools/biz/justify-text.html`：1 条（BS-N64，中）。行宽、居中、右对齐、末行不拉伸等主体逻辑正常；未发现假工具。
- `tools/biz/text-to-slug.html`：1 条（BS-N62，中）；分隔符折叠/首尾清理、停用词、60 字符截断均可运行；拼音表实跑验证
- `tools/biz/text-line-numbers.html`：3 条（BS-N51、BS-N52、BS-N53，均中）。九种行号格式与补零宽度均真实生效。
- `tools/biz/text-compare.html`：3 条（BS-N54、BS-N55、BS-N56，均中）。LCS 行级对齐正确；`escapeHtml` 已覆盖两侧文本，未发现 XSS。
- `tools/biz/text-extract-dates.html`：1 条（BS-N57 中）；六种格式的归一化、去重、含时间丢弃逻辑与文案一致
- `tools/biz/text-extract-urls.html`：1 条（BS-N58 中）；去重、排序、仅 http、移除 query 均可运行；结果经 `escapeHtml` 输出
- `tools/biz/text-extract-emails.html`：1 条（BS-N59，中）。去重与复制正常；正则字符集受限，`innerHTML` 拼接未发现 XSS。
- `tools/biz/text-extract-numbers.html`：2 条（BS-N43 高；BS-N60 中）；重叠抑制、数值排序、平均两位小数正常

- **本批合计 23 条：高 4（BS-N42、BS-N43、BS-N44、BS-N45）/ 中 19。未发现假工具（10 页均有真实转换逻辑并可运行）。**
- 说明：本轮为**只读**审计，结论来自逐行阅读源码 + `node` 在 `/tmp` 复刻核心函数实算（脚本 `/tmp/u_biz_audit.js`、`/tmp/u_biz_audit2.js`、`/tmp/u_biz_audit3.js`）；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，未修改任何工具页或构建产物。

## V 批 · 商业文本 A（2026-11-04）

只读审计 8 页商业文本工具（`text-to-banner` / `motto-generator` / `text-box-drawing` / `barcode-generator` / `markdown-quote` / `text-reverse-lines` / `superscript-text` / `fullwidth-halfwidth`），逐行读源码 + `node` 在 `/tmp` 复刻关键函数复算（含 Unicode 码位、UTF-16 代理对、条码校验位与标准码表）。**未修改工具页/代码/构建产物，未跑 `_build.py` / `run_gates.py`，未做 git 写操作。**

### BS-N65 文字转横幅：宣称画布横幅/字体/配色/PNG 导出，实际只剩 ASCII 方框（高，确认缺陷）
- 页面：`tools/biz/text-to-banner.html`
- 问题：页面描述、公式说明英文段、深度解析与「公式与标准引据」均承诺「可调整配色与字体并导出图片」「canvas 绘制并导出 PNG」「内置 standard/banner/small 等 figlet 字体」；实际 DOM 只有样式下拉、左右/上下内边距、复制与 CSV 导出，无 canvas、无颜色/字体控件、无图片导出，也不生成 figlet 大字。
- 证据：`tools/biz/text-to-banner.html:10`（description）、`:153`（英文 formula-desc）、`:160-169`（仅 8 个边框样式）、`:184-185`（仅 CSV/复制按钮）、`:232-236`（figlet 字体与「由字符拼成的大写 HI」示例）、`:254-260`（画布绘制/PNG 引据）、`:315-345`（`generate()` 仅字符串拼框）。
- 复现：输入 `HELLO`、选「井号填充」、左右内边距 2 → 输出 `╔═════════╗` / `║  HELLO  ║` / `╚═════════╝`，仍是普通 `HELLO`；全页搜索无 `canvas` / `toDataURL` / `font` / `color` 控件。
- 影响：用户按宣传寻找字体、配色与 PNG 导出全部落空；该页与 `text-box-drawing.html` 功能重复，属名不符实。
- 是否假工具：**是**（核心的图片横幅能力未实现，仅剩文本方框）
- 方案：二选一——① 真做 canvas 横幅（字体族/字号/前景背景色/PNG 下载）；② 若保留 ASCII 方框，则同步改写 title、description、深度解析与引据表，并去掉「字体/配色/导出图片」承诺。

### BS-N71 条码生成：内容行未经转义写入 `innerHTML`，Code 128 可注入 HTML 并执行事件（高，安全）
- 页面：`tools/biz/barcode-generator.html`
- 问题：`meta()` 用字符串拼 `<b>` + `rows[i][1]` 后写 `box.innerHTML`；`buildMeta()` 第一行就是 `['条码内容', res.text]`，而 Code 128 接受全部可打印 ASCII（含 `<`、`>`、`"`），用户输入会作为 HTML 解析。
- 证据：`tools/biz/barcode-generator.html:311-319`（`h += '<div><span>' + rows[i][0] + '</span><b>' + rows[i][1] + '</b></div>'; box.innerHTML = h`）、`:353`（内容行）、`:389`（未转义原文）。
- 复现：Code 128 输入 `<img src=x onerror="window.__xss=1">` → 编码成功；jsdom 复算 `meta()` 后 `#bcMeta` 内出现 1 个真实 `<img>` 元素，页面加载即触发 `onerror`。属自 XSS（需本人粘贴），但可被“示例文本”诱导。
- 影响：与项目结果区统一 `textContent`/`escapeHtml` 的约定不符，任何未来把输入带入 URL/分享的场景会升级为可传播 XSS。
- 是否假工具：否
- 方案：`meta()` 改用 `textContent` 逐节点构建，或对 `rows[i][0]/[1]` 统一 `escapeHtml`；SVG 的 `o.text` 已有转义，可复用同一函数。

### BS-N72 条码生成：宽度缩放 0.5 被静默抬到 1，控件标称范围失效（中，确认缺陷）
- 页面：`tools/biz/barcode-generator.html`
- 问题：页面允许 `min="0.5" step="0.5"`，但渲染层 `normalizeOptions()` 用 `Math.max(1, Math.min(10, ...))`，0.5 永远变成 1；用户选最小档与选 1 输出像素完全相同。
- 证据：`tools/biz/barcode-generator.html:184`（`min="0.5"`）、`js/barcode-lib.js:332`（`scale: Math.max(1, Math.min(10, parseFloat(o.scale) || 2))`）。
- 复现：同一内容分别设缩放 `0.5` 与 `1` → canvas 宽度、模块宽度一致（node 按 `normalizeOptions` 复算）；期望 0.5 档真正减半或 UI 最小改 1。
- 影响：小尺寸标签场景以为能缩到一半，实际仍按 1 倍输出，打印排版偏差。
- 是否假工具：否
- 方案：允许 `>=0.5`（配合 `dpr` 取整），或把输入 `min` 改为 1 并删除 0.5 档文案。

### BS-N73 座右铭生成器：宣称「关键词/风格偏好」，实际只有 5 个类别下拉，FAQ 指向不存在的入口（中，确认缺陷）
- 页面：`tools/biz/motto-generator.html`
- 问题：description / og / formula-desc 均写「根据关键词或风格偏好随机生成」；UI 只有 `#cat`（中国古典/西方哲思/现代励志/人生感悟/求学修身）与数量滑块，无关键词、无风格/语气输入；深度解析还给出不存在的「专注」主题，FAQ 让用户在「主题/风格里标注严肃/活泼/古风」。
- 证据：`tools/biz/motto-generator.html:10`、`:15`、`:164`（关键词/风格承诺）、`:168-174`（仅类别下拉）、`:213`（「主题选专注」示例）、`:217`（FAQ 指向主题/风格标注）。
- 复现：页面无任何关键词/风格输入控件；`#cat` 选项无「专注」；输入不存在的风格词也无处可填。生成、去重、数量上限（min(设定, 库容量)）本身正常。
- 影响：用户按宣传无法“按关键词生成”，FAQ 给出无法执行的步骤；属承诺未实现。
- 是否假工具：否（随机抽取主逻辑真实）
- 方案：新增关键词/风格输入并参与筛选（或给每条名言打标签），否则删除相关宣传与 FAQ 表述，并把「专注」示例改为实际类别。

### BS-N79 上标文字：宣称生成 HTML `<sup>` 代码，实际只给 Unicode 字符（中，确认缺陷）
- 页面：`tools/biz/superscript-text.html`
- 问题：description、og、formula-desc 均写「生成可复制的 Unicode 或 HTML 上标代码」，但脚本只有 `toSuperscript()` 查 Unicode 映射表，全页无 `<sup>` 输出分支或 HTML 模式。
- 证据：`tools/biz/superscript-text.html:10`、`:15`、`:156`（HTML 承诺）、`:231`（FAQ 提「借助富文本/HTML <sup>」）、`:301-319`（仅 Unicode 映射）。
- 复现：输入 `x2` 任何模式 → 只有 `x²`；找不到 `<sup>2</sup>` 形式的结果或开关。
- 影响：需要 HTML 上下标的网页/邮件用户按宣传找不到输出，只能拿 Unicode 自行包裹。
- 是否假工具：否
- 方案：增加「HTML 上标 / 下标」输出（如 `x<sup>2</sup>`、`H<sub>2</sub>O`）与复制按钮，或删除 HTML 承诺及 FAQ 相关句。

### BS-N80 全角半角互转：可见「假名（仅日文）」复选框从未被读取，勾选无任何效果（中，确认缺陷）
- 页面：`tools/biz/fullwidth-halfwidth.html`
- 问题：页面提供 `#kana`「假名（仅日文）」复选框，但 `convert()` 只读 `#ascii` 与 `#space`，全页再无 `kana` 引用，也无半角/全角假名映射表（U+FF61–FF9F ↔ 平假名/片假名）。
- 证据：`tools/biz/fullwidth-halfwidth.html:168`（唯一出现 `kana` 的复选框）、`:299-330`（转换循环仅 ascii/space 分支）。
- 复现：勾选「假名」，输入半角片假名 `ｱｲｳ` 转全角 → 原样不变（期望 `アイウ`）；输入全角 `アイウ` 转半角 → 原样不变（期望 `ｱｲｳ`）。
- 影响：日文混排用户以为能一并转换假名，实际只转了 ASCII/空格，需另找工具。
- 是否假工具：否（ASCII/空格双向转换主体正常）
- 方案：实现半角片假名（U+FF61–FF9F）与全角片假名/平假名映射并接入 `kana` 开关；不做就删除该复选框。

### V 批覆盖清单（8 页）
- `tools/biz/text-to-banner.html`：3 条（BS-N65、BS-N66 高；BS-N67 中）。生成/复制/CSV 可运行，但页面身份与宣传严重不符。
- `tools/biz/motto-generator.html`：1 条（BS-N73 中）。随机抽取、去重、条数上限与 CSV 正常；未发现 XSS（结果走 `textContent`）。
- `tools/biz/text-box-drawing.html`：2 条（BS-N68 高；BS-N69 中）。视觉宽度、八种边框、对齐、预设均真实；结果走 `textContent`。
- `tools/biz/barcode-generator.html`：2 条（BS-N71 高；BS-N72 中）；EAN-13/UPC-A 随机 30 组与参考库逐位一致，Code 39 码表/校验、Code 128 校验和均正确；问题集中在元信息注入、trim 与缩放钳制
- `tools/biz/text-reverse-lines.html`：1 条（BS-N76 中）；行级倒序、跳空行、首末行保留的主体逻辑正确
- `tools/biz/superscript-text.html`：3 条（BS-N77 高；BS-N78、BS-N79 中）。数字/符号映射正确，字母 q–z 与模式分流有问题。
- `tools/biz/fullwidth-halfwidth.html`：1 条（BS-N80 中）。U+FF01–FF5E / U+3000 双向转换与开关组合实算正常，结果 `textContent` 输出。

- **本批合计 16 条：高 5（BS-N65、BS-N66、BS-N68、BS-N71、BS-N77）/ 中 11。假工具 1 个（`text-to-banner`，核心图片横幅承诺未实现）。**
- 说明：本轮为**只读**审计，结论来自逐行阅读源码 + `node` 在 `/tmp` 复刻核心函数实算（脚本 `/tmp/v_biz_text.js`、`/tmp/c39cmp2.js`、`/tmp/bccmp.js`）；条码另用 `/tmp/pylibs` 的 `python-barcode` 参考实现比对 EAN/UPC/Code39 码表；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何文件。

## V 批 · 商业文本 B（2026-11-04）

### BS-N85 随机分组：FAQ 承诺「记住种子即可复现」，页面无种子功能（中，承诺未实现）
- 页面：`tools/biz/team-roster-generator.html`
- 问题：FAQ 写「如需可复现，记住种子或导出结果即可」，但页面无种子输入/输出，洗牌直接 `Math.random()`；同页公式说明又自述「未设种子，因此同一名单每次结果不同且不可复现」，同页自相矛盾。
- 证据：`:256`（FAQ 承诺）、`:170`（公式说明自述不可复现）、`:286-293`（Math.random 洗牌）、`:195`/`:201`（仅组数/每组人数两个输入）。
- 复现：同一名单连点两次「随机分组」→ 结果不同；界面任何位置都没有 seed 可记录。
- 影响：抽签留痕场景无法按宣传方式复现。假工具：否。
- 方案：增加 seed 输入/展示（如 mulberry32），或删除 FAQ 中「记住种子」，改为「需留痕请先导出结果」。

### BS-N86 随机分组：导出 CSV / 数据表 / 历史在默认状态为空（中，确认缺陷）
- 页面：`tools/biz/team-roster-generator.html`
- 问题：历史与表格仅由 `__team_roster_generatorExtras` 生成，而该函数只挂在 `switchTab` 上，`generate()` 未被包装；页面加载即自动分组，用户直接点「导出明细 CSV」时表格无行，`exportTable` 静默 `return false`。
- 证据：`:162`（导出按钮）、`:213`（表格容器）、`:481-484`（导出读表）、`:492-495`（extras 只挂在 switchTab）、`:299-353`（generate 未挂钩）、`:386-387`（加载即 generate）；`js/tool-kit.js:221-236`。
- 复现：打开页面（已自动出 10 人 3 组）→ 直接点导出 → 无文件、无提示；先点任一标签页再导出才有内容。
- 影响：导出在默认路径下不可用。假工具：否。
- 方案：extras 同步挂到 `generate`（或 boot 调用一次），导出改为直接导出当前分组文本。

### V 批覆盖清单（6 页）
- `tools/biz/unicode-normalize.html`：2 条（BS-N81、BS-N82 中）。`String.prototype.normalize` 四范式往返实算正确（NFC/NFD 幂等、NFKC 兼容折叠），问题在结果区同步与导出。
- `tools/biz/text-filter-lines.html`：2 条（BS-N83、BS-N84 中）。8 种模式匹配、trim/去空/反选主体逻辑正确，结果走 `textContent`。
- `tools/biz/small-caps.html`：0 条。映射表 26 码位（U+1D00…U+1D22，x 保留 U+0078）与 a–z 下标一一对应，`Hello World!` → `Hᴇʟʟᴏ Wᴏʀʟᴅ!` 正确；仅「交替」示例文案与实际首字母大写不符（低，不计）。
- `tools/biz/team-roster-generator.html`：2 条（BS-N85、BS-N86 中）。Fisher–Yates 洗牌、余数平摊（22 人 4 组 = 6/6/5/5）与组数/人数校验均正确。
- `tools/biz/text-case.html`：1 条（BS-N87 中）。12 种转换主体可运行，`upper/lower/sentence/invert/trim` 实算正确；`alternate` 实为首字母大写（示例文字不符，低，不计）。
- `tools/biz/char-frequency.html`：1 条（BS-N88 高）。计数按码位、忽略大小写与中文/英文/数字/标点筛选均正确，`abracadabra` 用例（5/2/2/1/1）逐项一致。

- **本批合计 8 条：高 1（BS-N88）/ 中 7。假工具 0 个。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻核心函数实算（脚本 `/tmp/v_biz_textb.js`、`/tmp/v_biz_case.js`、`/tmp/v_biz_lines.js`、`/tmp/v_biz_freq.js`）；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何仓库文件。

## W 批 · 商业文本 C（2026-11-04）

### BS-N92 简繁转换：常用字大面积未转换，且无词级词典（高，确认缺陷）
- 页面：`tools/biz/simplified-traditional.html`
- 问题：`s2tMap` 共 2082 条，其中 936 条为「自己映射到自己」的恒等项，有效转换仅 1146 条；`发/后/干/面/只/台/系/历/尽/计/签/数/卷/周/叶/苏/蒙/朴/斗/卜` 等高频字根本不在表内。`convert()` 逐字符 `map[ch] || ch`，无词组层，故 deep-dive 承诺的「软件→軟體」不成立（实际「軟件」）。
- 证据：`tools/biz/simplified-traditional.html:262-517`（字典）、`:519-524`（反向表）、`:533-542`（逐字映射）、`:166`（「内置 2000+ 常用汉字字典，支持基础词汇转换」）、`:212`（「软件→軟體 按台湾用词词典映射」）。
- 复现（node 解析真实字典）：简→繁 `后来→后来`、`头发→头发`、`干净→干净`、`台湾→台湾`、`系统→系统`、`计划→计划`、`面条→面条`、`只有→只有`、`杂志→雜志`，均与期望繁体不符；`软件→軟件`，期望 `軟體`。
- 影响：核心转换对现代常用文本大面积失效，输出简繁混杂。假工具：否。
- 方案：补齐高频字（含一对多字），引入词级覆盖表（軟體、滑鼠、資訊等）并优先于单字映射；「2000+」宣传改为实际有效条数或补齐到真实覆盖。

### BS-N93 简繁转换：一字多义无条件映射，常用词被改错字（中，确认缺陷）
- 页面：`tools/biz/simplified-traditional.html`
- 问题：`里→裏`、`余→餘`、`丑→醜`、`云→雲` 等无条件单字映射，未按词义消歧。
- 证据：`tools/biz/simplified-traditional.html:265-275`（`云→雲`、`余→餘`、`丑→醜`、`里→裏`）、`:533-542`。
- 复现（node 复刻）：`公里→公裏`、`里程→裏程`（期望「公里/里程」保留「里」）；`余曰→餘曰`、`丑时→醜时`、`诗云→诗雲`（期望保留本字）。
- 影响：地名/度量/文言/干支文本被系统性改错。假工具：否。
- 方案：多义字改为词级规则或白名单（如「公里/里程」不转、「剩余」转「餘」、「丑时」不转）。

### BS-N94 繁→简：反向表由 s2t 反转，常用繁体不转或错转（高，确认缺陷）
- 页面：`tools/biz/simplified-traditional.html`
- 问题：`t2sMap` 仅由 `s2tMap` 反转生成（`t2sMap[s2tMap[k]] = k`），s2t 缺字则 t2s 也缺；且 `麪→麵` 等异体条目反转后把标准繁体转成异体。
- 证据：`tools/biz/simplified-traditional.html:519-524`（反转）、`:262-517`（缺 `後/臺/隻/歷/週/葉` 等 key）。
- 复现（node 复刻）：`後來→後來`、`臺灣→臺灣`、`一隻→一隻`、`歷史→歷史`、`週末→週末`、`葉子→葉子`（均未转，期望简体）；`麵條→麪條`、`麵包→麪包`、`鍾錶→锺錶`（错字，期望「面条/面包/钟表」）；`國語→國语`、`學習→學习`、`體驗→体驗`（半转）。
- 影响：繁转简输出仍是繁体或异体，不可直接发布。假工具：否。
- 方案：独立维护 t2s 对照表（或采用标准简繁字表），禁止用 s2t 反转；反转时剔除恒等与异体条目。

### W 批覆盖清单（8 页）
- `tools/biz/text-extract-ips.html`：3 条（BS-N89 高、BS-N90/BS-N91 中）。IPv4 主体、去重、RFC1918 判定正确。
- `tools/biz/simplified-traditional.html`：3 条（BS-N92 高、BS-N93 中、BS-N94 高）。字典 2082 条 / 恒等 936 条；词级缺失并入 BS-N92，未单列。
- `tools/biz/text-shuffle.html`：3 条（BS-N95/96/97 中）。Fisher–Yates 主体正确；LCG 10 箱卡方 0.62（df=9，0.05 临界 16.92），均匀性通过，不登记。
- `tools/biz/text-extract-english.html`：2 条（BS-N98、BS-N99 中）。小写去重、分隔符 `\\n`→换行转换正确。
- `tools/biz/text-extract-chinese.html`：2 条（BS-N100、BS-N101 中）。逐字/按词主体逻辑正确，输出走 `textContent`。
- `tools/biz/text-keep-only.html`：2 条（BS-N102、BS-N103 中）。反向字符类、自定义字符转义、大小写 flag 主体正确。
- `tools/biz/text-remove-numbers.html`：2 条（BS-N104 高、BS-N105 中）。
- `tools/biz/lorem-ipsum-advanced.html`：3 条（BS-N106/107/108 中）。段落/句子/单词/列表四种生成主体可运行。

- **本批合计 20 条：高 4（BS-N89、BS-N92、BS-N94、BS-N104）/ 中 16。假工具 0 个，安全条目 0 条。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻核心函数实算（脚本 `/tmp/w_biz_verify.js`）；8 页输出均走 `textContent`，无 `innerHTML` 注入，故无安全条目。**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何仓库文件。

## W 批 · 商业文本 D（2026-11-04）

> 只读审计：逐页读源码 + `node` 在 `/tmp` 复刻核心函数实算（脚本 `/tmp/w_biz_text_d.js`、`/tmp/w_biz_text_d2.js`、`/tmp/w_rand2.js`）。未开浏览器、未跑构建/门禁、未做 git 写操作。

### BS-N110 随机话术：选 12/25/40 条实际只出 10 条，预设直接触发（高，确认缺陷）
- 页面：`tools/biz/random-script.html`
- 问题：内置话术库只有 10 条，`pick` 用 `slice(0, Math.min(n, arr.length))`，n 超过库容时静默截断；而数量输入允许 1–50，且预设有「客服话术 12 条」「运营文案 25 条」「压测数据集 40 条」。
- 证据：`tools/biz/random-script.html:206`（`SCRIPTS` 10 条）、`:218`（`pick` 截断）、`:220`（数量上限 50）、`:399-401`（三条越界预设）。
- 复现（node 复刻）：点「压测数据集 40 条」→ 实际只输出 10 条，页面无任何提示；期望 40 条或明确告知库容不足。
- 影响：数量设置与预设承诺全部失真，做「压测 40 条」数据集时实际只有 10 条。假工具：否。
- 方案：扩充话术库至 ≥50 条，或把数量上限钳到库容并在超出时提示；三条预设数量改为 ≤10。

### BS-N111 随机话术：功能特点称「支持按场景筛选」，页面无该控件（中，承诺未实现）
- 页面：`tools/biz/random-script.html`
- 问题：简介功能列表写「从标准话术库随机抽取，支持按场景筛选」，但页面只有「生成数量」一个输入，无场景下拉/多选；`scene` 字段仅用于结果展示。
- 证据：`tools/biz/random-script.html:273`（功能特点）、`:124`（唯一输入 `cnt`）。
- 影响：用户无法按场景（问候/致歉/退换货）定向抽题；假工具：否。
- 方案：补场景多选并接入 `pick` 前的过滤，或删除该条功能描述。

### BS-N112 随机话术：`sort(()=>Math.random()-0.5)` 抽取概率严重不均（中，确认缺陷）
- 页面：`tools/biz/random-script.html`
- 问题：用随机比较器排序后取前 N，属已知非均匀洗牌；与其引据「同场景下各模板出现概率均等」不符。
- 证据：`tools/biz/random-script.html:218`（实现）、`:179`（引据要求等概率）、`:159`（FAQ 已自认「概率并不严格相等」）。
- 复现（node 复刻，10 万次抽 5/10）：各条目入选次数 42654–58911，最大偏差 **17.8%**；排在首位的条目 6010–19595 次，最大偏差 **96%**。
- 影响：抽检/演练的条目覆盖不均，固定几条反复被抽中；假工具：否。
- 方案：改 Fisher–Yates 洗牌后取前 N（或 `crypto.getRandomValues` 取样），并同步更新 FAQ。

### BS-N115 三页生成器描述承诺的关键词输入与释义/slogan 输出均未实现（中，承诺未实现）
- 页面：`tools/biz/app-name-generator.html`、`tools/biz/brand-name-generator.html`、`tools/biz/product-name-generator.html`
- 问题：meta 描述与英文简介承诺「结合行业关键词与命名风格」「附简短释义」「依据行业、调性与关键词」「提示可注册性思路」「结合品类、卖点与风格关键词」「附带 slogan 思路」，但三页实际只有「类别/风格/产品类型」下拉 +「数量」滑杆两个控件，输出仅有名字本身。
- 证据：`tools/biz/app-name-generator.html:10`、`:164`；控件 `:168`、`:177`。`tools/biz/brand-name-generator.html:10`、`:164`；控件 `:168`、`:177`。`tools/biz/product-name-generator.html:10`、`:162`；控件 `:166`、`:175`。
- 影响：用户按描述找不到关键词/卖点输入，也拿不到释义、可注册性提示或 slogan；搜索摘要与实际能力不一致。假工具：否（随机命名本体可用）。
- 方案：补齐关键词/卖点输入与释义/slogan 输出，或把三处描述收敛为「按类别随机组合词库」。

### BS-N126 四页「导出明细 CSV」首屏直接点击为空表、静默无文件（中，确认缺陷）
- 页面：`tools/biz/random-script.html`、`tools/biz/text-pad.html`、`tools/biz/text-indent.html`、`tools/biz/text-repeat.html`
- 问题：四页首屏结果都由脚本末尾直接调用计算（`gen()`/`pad()`/`indent()`/`repeat()`），而「记录历史 + 渲染 `#xxxTable`」的 extras 包装写在其后；boot 只注册预设、不重算，因此首屏结果从未进表。导出函数只 `try{ TBKit.util.exportTable(...) }catch(e){}`，而空表时 `exportTable` 返回 `false`（无任何提示）。
- 证据：`tools/biz/random-script.html:232`、`:403`、`:392-394`、`:407`；`tools/biz/text-pad.html:364`、`:479-481`、`:468-470`、`:483`；`tools/biz/text-indent.html:420`、`:535-537`、`:524-526`、`:539`；`tools/biz/text-repeat.html:357`、`:472-474`、`:461-463`、`:476`；`js/tool-kit.js:221-235`（空表 `return false`）。
- 复现：打开任一页（默认文本已算出并显示）→ 直接点「导出明细 CSV」→ 无文件、无 toast；先点一次「生成/填充/缩进/重复」后再导出才有内容。
- 影响：默认路径下导出不可用，用户以为浏览器拦截下载；假工具：否。
- 方案：boot 里在预设注册后重算一次（触发 extras），或导出时直接读取 `#result` 文本拼 CSV。

### W 批覆盖清单（8 页）
- `tools/biz/app-name-generator.html`：1 条（BS-N109 中）+ 共享 BS-N115。词库拼接、随机源 `crypto.getRandomValues`、转义输出主体正确。
- `tools/biz/random-script.html`：3 条（BS-N110 高、BS-N111/112 中）+ 共享 BS-N126。单次抽取不重复、数量 1–50 钳制正确，库容不足未处理。
- `tools/biz/brand-name-generator.html`：1 条（BS-N113 高）+ 共享 BS-N115。首字母大写/全小写、短名开关逻辑正确。
- `tools/biz/product-name-generator.html`：1 条（BS-N114 中）+ 共享 BS-N115。A+空格+B 拼接与公式一致。
- `tools/biz/text-pad.html`：共享 BS-N126；本页独立缺陷 0 条。左右/居中填充、按字节 2 字节模型、奇数余数分配逐例复算均达标，未发现高/中优缺陷。
- `tools/biz/text-indent.html`：3 条（BS-N116/117/118 中）。缩进字符切换、闭合括号开关主体正确。
- `tools/biz/text-repeat.html`：2 条（BS-N119/120 中）+ 共享 BS-N126。正/倒序编号、`padStart` 位数、`\n` 分隔符转换正确。
- `tools/biz/presentation-timer.html`：5 条（BS-N121 高、BS-N122/123/124 中、BS-N125 安全）。均分余数、逐页 70%/90% 配色、历史写入主体可运行。

- **本批合计 18 条：高 3（BS-N110、BS-N113、BS-N121）/ 中 14 / 安全 1（BS-N125）。假工具 0 个。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻（脚本 `/tmp/w_biz_text_d.js`、`/tmp/w_biz_text_d2.js`、`/tmp/w_rand2.js`，含 10 万次随机分布统计与 2 万条生成抽样）；生成器随机性用多次抽样统计口径，非单次结果。**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何仓库文件。

## X 批 · 商业文本收尾（2026-11-04）

> 覆盖 `tools/biz/zalgo-text.html`、`strawberry-text.html`、`fancy-text.html`、`text-case-advanced.html`、`upside-down-text.html` 共 5 页。行号为源码行号；`/tmp` Node 复刻脚本 `/tmp/xprobe.js`。

### BS-N127 装饰文字：标称「15+ / 数十种 / 含全角」，实际仅 14 种可用，另 3 张是点不动的占位卡（中，承诺未实现）
- 页面：`tools/biz/fancy-text.html`
- 问题：`styles` 共 17 项，其中 3 项值为字符串占位（区域指示符 / 颠倒 / 加点），点击只 `alert('该风格不可用')`；可真正转换的只有 14 种，少于 h2 的「15+」与 meta 的「数十种…含全角」。深解算例还宣称「全角样式输出「ＴｏｏｌＢｏｘ」」，而全页不存在全角（U+FF01–FF5E）映射。
- 证据：`tools/biz/fancy-text.html:296-298`（三张占位卡）、`:349`（`text.includes('使用')` → alert）、`:176`（h2「15+」）、`:10`/`:15`（meta「数十种…全角」）、`:208`（深解「全角样式输出ＴｏｏｌＢｏｘ」）。
- 复现：打开页面数出 17 张卡；点「🇫🇦🇳🇨🇾 区域指示符」「ɟɐuɔʎ 颠倒」「H̥e̥l̥l̥o̥ 加点」→ 一律 alert「该风格不可用」；输入 `ToolBox` 无任何全角结果可复制。
- 影响：宣称能力与实物不符，3 张卡为死功能；主体 14 种映射可用，故假工具：否。
- 方案：补全角与区域指示符映射，或删掉 3 张占位卡并把「15+/数十种/全角」文案改为实际 14 种。

### BS-N129 草莓文字：按 UTF-16 码元遍历，输入含 emoji 时输出被拆成孤立代理项（中，确认缺陷）
- 页面：`tools/biz/strawberry-text.html`
- 问题：`for(var i=0;i<input.length;i++){ var ch = input[i]; }` 按码元取字符，非 BMP 字符（emoji、部分扩展 CJK）被拆成高低代理两半，两半之间被插入装饰 emoji，拼接后成为非法代理序列，显示为 �/方框。
- 证据：`tools/biz/strawberry-text.html:308-310`（`input.length` + `input[i]`）、`:322-324`（在 `ch` 两侧拼接 emoji）。
- 复现：输入 `Hi😀`，勾选「字符前加/后加」→ 结果码位序列为 `… 1f353 48 1f353 1f353 69 1f353 1f353 d83d 1f353 1f353 de00 1f353`（`d83d`/`de00` 被拆开，孤立代理项）。
- 影响：贴 emoji 的昵称场景恰好是本工具主用途，输出直接坏字；假工具：否。
- 方案：改用 `Array.from(input)` 或 `for...of` 按码点遍历。

### BS-N130 草莓文字：深解与引据表把功能写成「叠加组合字符 / UTS #39 同形替换」，实际是拼 emoji（中，承诺未实现）
- 页面：`tools/biz/strawberry-text.html`
- 问题：方案宣传「在文字上叠加组合字符形成「草莓/带点」观感」「每字符上叠加组合标记」，引据表还给出「同形/近形字符替换，属视觉替换」「兼容归一化可部分还原」（Unicode UTS #39 / UAX #15），FAQ 也称「装饰依赖组合字符」；实现只是在字符前后拼接 emoji（U+1F353 等），与组合标记、同形替换、归一化均无关。
- 证据：`tools/biz/strawberry-text.html:232`、`:236`、`:239`、`:257-259`（引据表三行）；实现 `:312-327`（`currentEmoji + ch + currentEmoji`）。
- 复现：输入 `hello` → 输出 `🍓h🍓🍓e🍓…`（emoji 拼接），不存在任何组合标记；对结果做 NFC/NFKC 也不会还原成原词（emoji 不在兼容等价映射内，且它会作为独立字符留存）。
- 影响：用户按说明预期「可归一化还原/无副作用」，实际插入的是 emoji，平台过滤、字数与检索行为完全不同；假工具：否。
- 方案：把深解/引据表/FAQ 改为 emoji 拼接原理（或真的实现组合标记方案）。

### BS-N131 高级大小写：meta 与公式承诺「保留专有名词」，实现一律小写化，iPhone→Iphone、USA→Usa（中，承诺未实现+算错）
- 页面：`tools/biz/text-case-advanced.html`
- 问题：meta 描述（3 处）与 formula-desc 均写「按句/按标题规则智能转换…并保留专有名词」，实现中 `title` 与 `sentence` 都先 `toLowerCase()` 再首字母大写，没有任何专有名词表、缩写保留或大小写例外分支。
- 证据：`tools/biz/text-case-advanced.html:10`/`:15`/`:68`（meta「保留专有名词」）、`:164`（formula-desc "preserving proper nouns"）；实现 `:318`（title）、`:319`（sentence）。
- 复现：输入 `iPhone is from the USA` → 标题模式得 `Iphone Is From The Usa`，句首模式得 `Iphone is from the usa`（品牌名与缩写被破坏）。
- 影响：长文档排版的核心承诺落空，且输出对专有名词是错的；假工具：否。
- 方案：加专有名词/全大写缩写保留规则（或删掉「保留专有名词」文案）。

### BS-N132 高级大小写：「交替 / 交替反」两张卡的示例与真实输出正好对调（中，说明与实现相反）
- 页面：`tools/biz/text-case-advanced.html`
- 问题：「交替」卡示例写 `hElLo`，实现初值 `up=false`，首个字母即转大写 → 实际 `HeLlO`；「交替反」示例写 `HeLlO`，实现初值 `up=true`，首字母转小写 → 实际 `hElLo`。两卡示例互为对方的输出。
- 证据：`tools/biz/text-case-advanced.html:192`（交替示例 `hElLo`）、`:193`（交替反示例 `HeLlO`）、`:335-341`（`let up = false`）、`:343-349`（`let up = true`）。
- 复现：输入 `hello` 点「交替」→ `HeLlO`；点「交替反」→ `hElLo`，与卡片示例相反。
- 影响：用户按示例选模式会得到与预览不符的结果；假工具：否。
- 方案：交换两处示例文案，或把两个模式的初值对调。

### BS-N133 高级大小写：`updatePreview()` 是空函数，改输入不重算，复制会拿到上一次结果（中，确认缺陷）
- 页面：`tools/biz/text-case-advanced.html`
- 问题：textarea 绑定 `oninput="updatePreview()"`，但 `updatePreview` 函数体只有注释「保留上次结果」；页面又没有「转换」按钮（只有模式卡）。用户改完输入后预览仍是旧文本，此时点「复制结果」复制的也是旧文本。
- 证据：`tools/biz/text-case-advanced.html:169`（`oninput="updatePreview()"`）、`:367-369`（空实现）、`:171`（复制按钮）、`:175`（`#preview`）、`:493-497`（boot 也调空 `updatePreview`）、`:464-483`（每次 oninput 仍落库一条「新输入 + 旧结果」记录）、`:443`（历史回填后也只调空 `updatePreview`，预览不跟着变）。
- 复现：点「全大写」得 `HELLO WORLD` → 把输入改成 `abc`（不点任何模式）→ 预览仍显示 `HELLO WORLD` → 点「复制结果」→ 剪贴板是 `HELLO WORLD`；同时历史表新增一条「输入 abc / 结果 HELLO WORLD」的错配记录（`last<1000ms` 限流，每秒最多 1 条）。
- 影响：输出与当前输入不一致，静默复制错误结果，且把错配结果写进历史/CSV；假工具：否。
- 方案：记住 `lastMode`，在 `updatePreview` 里重跑 `convert(lastMode)`；或去掉 `oninput` 并明确提示「点模式卡才计算」。

### BS-N134 颠倒文字：末步 `split('')` 反转拆散代理对，含 emoji 输出为非法序列（中，确认缺陷）
- 页面：`tools/biz/upside-down-text.html`
- 问题：映射阶段用 `for...of`（按码点，安全），但最后 `out.split('').reverse().join('')`（按 UTF-16 码元）反转；非 BMP 字符被拆成两个代理项并倒序，产生孤立代理项。
- 证据：`tools/biz/upside-down-text.html:300-302`（按码点映射）、`:304`（`split('').reverse().join('')`）。
- 复现：输入 `a😀` → 结果码位顺序 `U+DE00 U+D83D U+0250`（高低代理倒置，浏览器显示 �）。
- 影响：贴 emoji 即坏字（中文 BMP 不受影响）；假工具：否。
- 方案：改为 `[...out].reverse().join('')`。

### BS-N135 颠倒文字：深解算例「oʅʅǝɥ」与实现输出「ollǝɥ」不符（中，算例错误）
- 页面：`tools/biz/upside-down-text.html`
- 问题：深解写「输入 hello，倒置输出 oʅʅǝɥ」，但映射表把 `l` 映射为 `l`（恒等），实际结果为 `ollǝɥ`；文档比实现多两个 `ʅ`。
- 证据：`tools/biz/upside-down-text.html:212`（算例）、`:285`（`'l':'l'`）、`:304`（反转）。
- 复现：`/tmp` Node 复刻 → `flip('hello')` = `ollǝɥ`；`flip('Hello World!')` = `¡plɹoM ollǝH`。
- 影响：算例与实物不符，用户以为映射缺字；假工具：否。
- 方案：把算例改成 `ollǝɥ`，或把 `l` 改为 `ʅ`（并同步全部含 l 的示例）。

### BS-N136 Zalgo 文字：公式称「上限放大后向下取整」，`rand(上限+1)` 未取整，轻度档可超出文档上限（中，说明与实现不符）
- 页面：`tools/biz/zalgo-text.html`
- 问题：formula-desc 明确写「上限被强度放大后再向下取整」「每字符附加数 ~ U{0, ⌊上限⌋}」，实现直接把可能带小数的 `upMax` 传给 `rand(upMax+1)`；小数时上界变 `⌈上限⌉`，轻度档也会超出文档所述最大值。
- 证据：`tools/biz/zalgo-text.html:325-327`（`parseInt(...) * intensity / 2` 未取整）、`:333-335`（`rand(upMax + 1)`）、`:531-532`（formula-eq/formula-desc「向下取整」「⌊上限⌋」）。
- 复现：上/中/下设为 3/1/3、强度「轻度」→ upMax=1.5，`rand(2.5)` 返回 0/1/2，单字符上方可出现 2 个标记（文档上限为 1）。
- 影响：按文档调参得到的强度偏强且不可预测；输出本身不算错，属说明与实现不符；假工具：否。
- 方案：`rand(Math.floor(upMax) + 1)`（三档同改），或把文档改成 `⌈上限⌉ + 1`。

### X 批覆盖清单（商业文本收尾 5 页）
- `tools/biz/zalgo-text.html`：1 条（BS-N136 中）。复核通过项：按码点叠加、空格/换行跳过、三组符号独立抽样、历史回填与预设接线正常。
- `tools/biz/strawberry-text.html`：3 条（BS-N128/129/130 中）。复核通过项：包夹/前后/跳过空白三模式与公式一致、清空与复制接线正常。
- `tools/biz/fancy-text.html`：1 条（BS-N127 中）。复核通过项：14 张映射表 `src/dst` 长度全部相等（`/tmp` 逐表校验，无 `undefined` 空洞）、未命中保留原字符、中文/emoji 按码点安全。
- `tools/biz/text-case-advanced.html`：3 条（BS-N131/132/133 中）。复核通过项：22 个模式中 camel/pascal/snake/kebab/constant/dot/path 分词与取词正确，`sentence` 句首规则正确。
- `tools/biz/upside-down-text.html`：2 条（BS-N134/135 中）。复核通过项：映射覆盖 a–z/A–Z/0–9/常用标点，未命中保留原字符，空格映射恒等。

- **X 批合计 10 条：高 0 / 中 10 / 安全 0。假工具 0 个。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻（`/tmp/xprobe.js`：fancy 17 张卡映射长度校验、`flip('hello')` 实测、草莓 emoji 码位实测、大小写各模式实测）。**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做 git 写操作**，除本文件与 `plan/categories/11-文娱爱好/fun-entertainment.md` 外未修改任何文件。

## Y 批 · 商业文本处理（2026-11-04）

- `tools/biz/text-dedup.html`：0 条 —— 保留首次/末次、忽略大小写、七种排序与反转均与说明一致（`dedup-last` 用末次下标集合过滤，输出顺序正确；`dedup-case` 以 `toLowerCase()` 建键并保留首次原样），未发现算错、崩溃或假功能。
- `tools/biz/text-extract.html`：3 条 —— 正则提取、序号列表与「无匹配项」提示可运行，但单项复制按钮存在 HTML 属性注入（高/安全），且「去重」「自定义模式」为承诺未实现，URL/IP/日期正则存在边界与取值校验缺口。
- `tools/biz/text-sort.html`：2 条 —— 八种排序模式与 `Intl.Collator`（`sensitivity`/`numeric`）开关正确，但四个辅助面板因读取 `textarea.textContent` 而恒空（假功能，高），且「去重」承诺无对应实现。

| 页面 | 问题（含 tools/&lt;dir&gt;/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/biz/text-extract.html | 匹配项经 `escapeAttr`（仅把 `'` 转成 `\'`）拼进双引号属性 `onclick="copy('…')"`：HTML 标签模式可匹配含 `"` 的标签（如 `<img src=x onerror="alert(1)">`），会提前闭合属性并注入事件属性；匹配项含 `\` 或换行时还会打断 JS 字符串（DOM 型注入/自 XSS）。:314、:323 | BS-N137 |
| tools/biz/text-extract.html | 简介、formula-desc 与引据表承诺「过滤噪声并去重」「去重后保留首次出现次序」「或自定义模式」，但 `extract()` 只做 `matches.join('\n')` 全量输出（重复项原样保留），`MODES` 也仅 16 个固定正则、无自定义模式入口（承诺未实现）。:10、:163、:247、:252 对 :301-314、:269-286 | BS-N138 |
| tools/biz/text-extract.html | URL 正则 `[^\s<>"']+` 会吞掉紧随的中文句号/右括号（`https://a.com。` 整段被当链接）；IP 与日期正则无取值校验，`999.999.999.999`、`2024-13-45` 会作为有效 IP/日期输出。:271、:274-277 | BS-N139 |
| tools/biz/text-sort.html | 结果区是 `<textarea id="output">`，而 `__text_sortResText()` 读 `textContent`（textarea 的 textContent 恒为初始空文本，不随 `.value` 变化）→ 恒返回空串，`__text_sortExtras()` 在 :408 直接返回；图表/数据表/历史/导出 CSV 全空，`__text_sortPresets()` 亦为空函数（预设页恒空）。假功能。:193、:350-357、:407-408、:429-435 | BS-N140 |
| tools/biz/text-sort.html | `meta description`、formula-desc 与引据表均称「支持去重 / optional deduplication / 合并相邻重复行」，但 `sort()` 只做排序与去空行，无任何去重逻辑，重复行原样保留（:10、:157、:254-255 对 :278-319）。 | BS-N141 |

- 统计：3 页 / 5 条（高 2 / 中 3）/ 安全 1 条（`tools/biz/text-extract.html:314`、`:323`）/ 假工具 0（`tools/biz/text-sort.html` 仅辅助面板空转、主体排序可用）/ 编号区间 BS-N137～BS-N141。
