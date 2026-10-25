# 图表/预设扩补专项 · 甄别裁断清单（交接文档）

> 专项状态：93 页全部处置完毕，专项闭环。

> 日期：2026-10-25。本文件为「dev-plan 第四章方向①/②：图表/预设扩补」专项的一次性交接文档，
> 记录对 93 页真缺池的最终处置，供裁断与收口核对；后续勿在此文件追加日常改动。

## 方法

- **真机探针**：puppeteer-core + Chrome headless，逐页真实交互（填表单/点预设按钮/播种 localStorage 历史后）验证 live svg / preset children 与 EN 态（`?lang=en-US`）零汉字，产物 `/tmp/probe_batch10*.json`（第七批为 `probe_batch10g.json`，3/3 通过）。
- **逐页读 calc**：每页先读 `calc()`/生成函数钉死数据源（真实全局变量、localStorage 记录结构或页内 DOM 字段），冲突或无信息量则跳过注入并写明理由，禁止硬凑。

## 已注入 60 页（第一~六批，commit 一览）

`3be9a86eac`（第一批 10 页）→ `115d21ef18`（第二批 10 页）→ `46efef24f4`（第三批 10 页）→ `f550235429`（第四批 10 页）→ `2d31f0c50f`（第五批 10 页）→ `69e0aac8a0`（第六批 10 页）。
数据源全部取自各页 calc/渲染函数真实变量，TBKit.chart/preset 按页接线，EN 态零中文，真机探针复测通过。

## 第七批注入 3 页（commit：`2f35e4073d`）

（hash 已回填：第七批提交为 `2f35e4073d`，即本收尾批的直接前驱。）

1. **tools/edu/countdown-5.html** — 图表：按日志日期升序的累计学习小时 vs 目标总时长双系列 line（数据源：全局 `state.logs[{date,hours}]` + `state.targetHours`，照 `render()` 的 totalH/pct 口径），标题含目标完成率%；preset：高考（6月7日）/考研（12月下旬）/四六级（6·12月）/公务员国考（11月底）4 组目标日期场景，填 `examName/examDate/targetHours` 真实字段并 `saveExam()` 持久化。
2. **tools/safety/self-test.html** — 页内已有 `tbHistChart` 历史得分趋势 line（数据源：TBKit.history，localStorage key=`tbk_hist_<pathname>`，记录结构 `{t,d:{时间,得分,答对,评级,__v}}`）；本批包装 `__tbHistRender` 给标题补「最近得分 · 最高分」，无记录回退原标题，langchange 全量重渲染。
3. **tools/pet/training-planner.html** — preset：幼犬社会化/成犬服从/行为矫正/高级技能 4 组（页内真实字段：`#age`、`#dailyTime`、全局 `currentPet/selectedGoals` + `renderGoalGrid()/generate()`）。7 天分布图分支**不触发**：每日任务数 = min(时段数+1, 项目总数) 恒定、每日时长恒定，画图必为 7 根等高柱无信息量，且页面有真实参数字段（「纯查表无参数」条件不成立）。

## 已注入（收尾批，原报裁断 2 页）

（老板裁断：边际增益虽低但可做，做后 93 页真缺池全闭环。本节随收尾批提交，commit hash 由维护者提交后补写于此——同第七批自引用处理。）

1. **tools/finance/word-counter.html** — 图表：词频 Top-10 条形图（`TBKit.chart.bar`；数据源：页内 `showDensity()` 同口径词频——文本小写 `[a-z]+` 切词、剔除单字母、频次降序取前 10）；容器 `#wcChart` 置于 `#densitySection` 内（勾选「显示词频」后随列表一起展示，图给 top-N 直观对比、补列表全文滚动之短）；接线：`__wc_fn0` 链包装全局 `analyze`（覆盖「分析」按钮 / textarea 内联 oninput / 粘贴），空文本或无 ≥2 字母词静默跳过。注：TBKit.chart.bar 为纵向柱状（工具箱无横向分类条形分支），逐柱 tooltip 补全每词频次。
2. **tools/edu/multiplication-table.html** — 页内 localStorage 仅 `mult-best` 单值（无历次挑战记录数组，得分/用时趋势线无数据源），且页面无范围参数字段可挂 preset，按裁断备选项落「本次答题正确率 bar」：正确/错误双柱（数据源：全局 `pCorrect`/`pWrong`，照 `updatePScore()` 的正确率口径，标题含实时正确率%）；容器 `#mtChart` 置于随机练习 tab 末尾；接线：`__mt_fn0` 链包装 `updatePScore()`，每答一题实时重绘。

## 天然不需要（B 类，逐页一句依据）

> 逐行清点为 **28 页**（原甄别底稿 `/tmp/screening33.md` 统计块写「B：18」为笔误，以本清单为准；口径核对见下方结论）。

- tools/ai/ocr.html — AI 识别：图片→文本输出，无连续量、无参数场景
- tools/ai/speech-to-text.html — AI 转写：音频→文本，无序列价值
- tools/biz/markdown.html — 文本编辑+实时预览，统计仅字符数单值
- tools/biz/name-generator.html — 随机名字生成器，已有 applyNamePreset；输出为离散名字列表，无可画系列
- tools/chinese/chinese-culture.html — 静态文化资料查表（save/restore 仅偏好），无计算
- tools/chinese/lunar-calendar.html — 日期↔农历一一对应转换，星座/宜忌为查表单值
- tools/design/colorblind-simulator.html — 图像/颜色模拟器，输出为视觉效果非数据
- tools/design/shadow-generator.html — CSS 效果生成器，已有 applyPreset/预设网格，无可画系列
- tools/fengshui/fengshui-guide.html — 静态资料查表，已有 applyFengshuiPreset，无计算序列
- tools/image/image-converter.html — 批量格式转换器，输出为文件非数据
- tools/it/ast-viewer.html — 代码→树形查看器，stats 为单值计数
- tools/it/color-converter.html — 颜色格式一一对应转换，对比度为单值输出
- tools/it/css-properties.html — 属性速查表，勾选收藏，无计算
- tools/it/csv-to-json.html — 双向格式转换器，一一映射
- tools/it/html-entity-encoder.html — 编解码器，一一映射（附查表）
- tools/it/html-tags.html — 标签速查表，无计算
- tools/it/json-to-tsv.html — 双向格式转换器，一一映射
- tools/it/pdf-signature-checker.html — 签名状态为布尔/状态非序列
- tools/it/sha.html — 哈希计算器，输入→摘要单值
- tools/it/text-diff.html — LCS 文本对比，stats（增/删行数）单值，无多维系列
- tools/legal/contract-templates.html — 模板库筛选/收藏，已有 applyContractPreset，无计算
- tools/library/archive-label.html — 标签批量生成器，输出为打印标签非数据
- tools/life/base-convert.html — 进制转换一一对应
- tools/life/countdown-1.html — 秒表计时器属实时场景（laps 可画但增益边际），已有 applyTimerPreset
- tools/medical/drug-info.html — 药物速查表+收藏，无计算
- tools/safety/manager.html — 口令管理器，strength 为单值仪表；本地加密存储工具
- tools/security/virtual-safe.html — 本地加密保险箱，强度为单值
- tools/travel/currency-cheat-sheet.html — 多档换算网格本身即「多档对比」输出形态，画图无增益

## 结论（93 页真缺池处置核对）

- **注入 65**（六批 60 + 第七批 3 + 收尾批 2）＋ **天然不需要 28**（B 类）＝ **93，精确闭合**。
- C 类存疑 4 页全部有去向：training-planner、self-test 并入第七批注入；multiplication-table、word-counter 老板裁断可做，已随收尾批注入（见上节）。
- 「已注入前批重叠」说明：第六批 10 页（detector-time、checker-assessor-1/2、detector-20、checker-7、cycle-11、rater-17、physics-calculator、data-erase-simulator、smoke-alarm-test）在剩余池甄别时被标「已注入」，该 10 页即第六批本身、已含在「注入 60」内，**不重复计数**；若按「18＋重叠 10」口径列式则与第六批重复计数且无法闭合，故以本清单 28 页口径为准。
- 专项状态：93 页全部处置完毕（注入 65 + 天然不需要 28），专项闭环（2026-10-25 收尾批收口）。
