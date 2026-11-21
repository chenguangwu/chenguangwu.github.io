# 商业综合/创业 · tools/{biz,startup}（75 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 2026-11-03 审计补充

### 留存优化：采购比较考虑附加费用（低，建议）
- 证据：同页 `:106,116-139,287-305` 文案提及运费及多件促销，但实际输入为两商品数量、单位和价格。
- 影响：同页；方案：按商品加入选填运费、促销总件数，展示标准单位单价和每次采购节省额，支持复制结果。

### 覆盖
- 本轮核查 `tools/biz/unit-price-compare.html`、`tools/biz/meeting-cost-calculator.html`、`tools/startup/equity-calculator.html` 共 3 页；新增 2 个缺陷及 2 条建议。后两页为内存 DOM 桩执行，未实测浏览器、系统剪贴板或其他商业页。

## 2026-11-03 续查（并行批 I）

> 编号沿用本文件新启前缀 `BS-N`（与 `RE-N` / `06-F` 同批体例），互不重号；上一节 3 页不重复核查。全部结论基于源码阅读 + node 内存复算，未打开浏览器，未做 EN / 繁体 / 移动端 / 门禁验证。

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

### 续查覆盖（K 批）
- 本轮实读 8 页：`tools/biz/analysis-47.html`、`tools/biz/analysis-manager.html`、`tools/biz/stats-time-response.html`、`tools/biz/assessor-49.html`、`tools/biz/assessor-risk-8.html`、`tools/project/analysis-28.html`、`tools/project/assessor-risk-9.html`、`tools/project/checker-training-hr-1.html`；新增 16 条（高 2 / 中 9 / 低 5）。
- 未覆盖：`tools/biz` 其余文本/命名类页面、`tools/startup/index.html` 分类页；另顺带阅读 `tools/project/checker-12.html`（仅「合格/一般」命名与深度解析薄弱项映射等低优文案不一致，未单列）。

## T 批 商业文本工具覆盖（2026-11-04）

### T 批覆盖清单（8 页）
- `tools/biz/text-replace-advanced.html`：**未发现 XSS**：替换结果走 `textContent`，匹配列表的 `match/groups` 已 `escapeHtml`。另记（未单列，低）：非正则模式下替换串仍按 `$&`/`$$` 解释，替换"原文含 `$&`"会变成插入整个匹配；复制按钮回调引用全局 `event`，Firefox 下无「已复制」反馈。
- `tools/biz/text-extract-html-tags.html`：2 条（BS-N31、BS-N32，均中）。另记（未单列，低）：清空输入时只重置 `count`，`uniqueCount` 保留上一次数字；FAQ 所称「仅正文标签」过滤与简介所称「指定标签」入口均不存在。
- `tools/biz/text-remove-duplicates-lines.html`：2 条（BS-N33、BS-N34，均中）。`trimLine`/`removeEmpty`/`sortResult` 与六种模式均真实生效，未发现 XSS（结果走 `textContent`）。
- `tools/biz/text-sort-advanced.html`：2 条（BS-N35、BS-N36，均中）。`random`/`reverse`/`natural` 与长度模式实算正常；`lex-zh` 不响应「忽略大小写」（低，未单列）。
- `tools/biz/text-merge.html`：**未发现中/高**。骨架正确：`\n` 分隔符特判、`custom` 空值回退、`skipEmpty` 为显式选项。仅记低优：`prefix`/`suffix` 输入框没有 `oninput`，改后需手动点「合并」才刷新，与同页其它输入不一致；`var currentMode` 是死变量。
- `tools/biz/text-split.html`：1 条（BS-N29 高）。`result.innerHTML` 对每段做 `escapeHtml`，未见注入；正则分隔符编译失败已 try/catch 提示。

- 说明：本轮为**只读**审计，结论来自逐行阅读源码 + `node` 在 `/tmp` 复刻关键函数实算（脚本 `/tmp/tb_repro.js`、`/tmp/tb_repro2.js`）；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，未修改任何工具页或构建产物。新增 13 条（高 1 / 中 12）。

## U 批 · 商业文本处理（2026-11-04）

只读审计 10 页文本处理工具（`text-wrap` / `text-trim` / `justify-text` / `text-to-slug` / `text-line-numbers` / `text-compare` / `text-extract-dates` / `text-extract-urls` / `text-extract-emails` / `text-extract-numbers`），逐行读源码 + `node` 在 `/tmp` 复刻核心函数复算（含 Unicode、全半角、正则边界）。**未修改工具页/代码/构建产物，未跑 `_build.py` / `run_gates.py`，未做 git 写操作。**

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

### V 批覆盖清单（8 页）
- `tools/biz/text-to-banner.html`：3 条（BS-N65、BS-N66 高；BS-N67 中）。生成/复制/CSV 可运行，但页面身份与宣传严重不符。
- `tools/biz/motto-generator.html`：1 条（BS-N73 中）。随机抽取、去重、条数上限与 CSV 正常；未发现 XSS（结果走 `textContent`）。
- `tools/biz/text-box-drawing.html`：2 条（BS-N68 高；BS-N69 中）。视觉宽度、八种边框、对齐、预设均真实；结果走 `textContent`。
- `tools/biz/barcode-generator.html`：1 条（BS-N72 中）；EAN-13/UPC-A 随机 30 组与参考库逐位一致，Code 39 码表/校验、Code 128 校验和均正确；原元信息注入已改 `textContent` 渲染，第 953 批清账，剩余问题为 trim 与缩放钳制
- `tools/biz/text-reverse-lines.html`：1 条（BS-N76 中）；行级倒序、跳空行、首末行保留的主体逻辑正确
- `tools/biz/superscript-text.html`：3 条（BS-N77 高；BS-N78、BS-N79 中）。数字/符号映射正确，字母 q–z 与模式分流有问题。
- `tools/biz/fullwidth-halfwidth.html`：1 条（BS-N80 中）。U+FF01–FF5E / U+3000 双向转换与开关组合实算正常，结果 `textContent` 输出。

- **本批合计 15 条：高 4（BS-N65、BS-N66、BS-N68、BS-N77）/ 中 11（BS-N71 已修复销账）。假工具 1 个（`text-to-banner`，核心图片横幅承诺未实现）。**
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

### W 批覆盖清单（8 页）
- `tools/biz/app-name-generator.html`：1 条（BS-N109 中）+ 共享 BS-N115。词库拼接、随机源 `crypto.getRandomValues`、转义输出主体正确。
- `tools/biz/random-script.html`：1 条（BS-N111 中）。单次抽取不重复、数量 1–50 钳制正确，库容不足已有明确提示。
- `tools/biz/brand-name-generator.html`：1 条（BS-N113 高）+ 共享 BS-N115。首字母大写/全小写、短名开关逻辑正确。
- `tools/biz/product-name-generator.html`：1 条（BS-N114 中）+ 共享 BS-N115。A+空格+B 拼接与公式一致。
- `tools/biz/text-pad.html`：本页独立缺陷 0 条。左右/居中填充、按字节 2 字节模型、奇数余数分配逐例复算均达标，未发现高/中优缺陷。
- `tools/biz/text-indent.html`：3 条（BS-N116/117/118 中）。缩进字符切换、闭合括号开关主体正确。
- `tools/biz/text-repeat.html`：2 条（BS-N119/120 中）。正/倒序编号、`padStart` 位数、`\n` 分隔符转换正确。
- `tools/biz/presentation-timer.html`：5 条（BS-N121 高、BS-N122/123/124 中、BS-N125 安全）。均分余数、逐页 70%/90% 配色、历史写入主体可运行。

- **本批合计 18 条：高 3（BS-N110、BS-N113、BS-N121）/ 中 14 / 安全 1（BS-N125）。假工具 0 个。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻（脚本 `/tmp/w_biz_text_d.js`、`/tmp/w_biz_text_d2.js`、`/tmp/w_rand2.js`，含 10 万次随机分布统计与 2 万条生成抽样）；生成器随机性用多次抽样统计口径，非单次结果。**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何仓库文件。

## X 批 · 商业文本收尾（2026-11-04）

> 覆盖 `tools/biz/zalgo-text.html`、`strawberry-text.html`、`fancy-text.html`、`text-case-advanced.html`、`upside-down-text.html` 共 5 页。行号为源码行号；`/tmp` Node 复刻脚本 `/tmp/xprobe.js`。

### X 批覆盖清单（商业文本收尾 5 页）
- `tools/biz/strawberry-text.html`：2 条（BS-N128/130 中）。复核通过项：包夹/前后/跳过空白三模式与公式一致、清空与复制接线正常。
- `tools/biz/fancy-text.html`：1 条（BS-N127 中）。复核通过项：14 张映射表 `src/dst` 长度全部相等（`/tmp` 逐表校验，无 `undefined` 空洞）、未命中保留原字符、中文/emoji 按码点安全。
- `tools/biz/text-case-advanced.html`：1 条（BS-N131 中）。复核通过项：22 个模式中 camel/pascal/snake/kebab/constant/dot/path 分词与取词正确，`sentence` 句首规则正确。

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
