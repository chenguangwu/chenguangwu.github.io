# 科研/图书馆 · tools/{research,library,archive}（~20 页）

## 功能缺陷
- 缺「样本量计算器」统一入口（alpha/效力/效应量三参数，各学科预设）。
- 缺「期刊分区速查」（静态 CAS/JCR 数据模块）。

## 优化点
- S7 引据：统计页标方法出处（Cohen 1988 等）。

## 受影响范围
- tools/research/、tools/library/、tools/archive/

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 逾期罚款封顶与倒序日期（中，确认函数缺陷）
- 证据：`tools/library/overdue-fine.html:265-302` 已启用封顶但 cap=0 时 `cap>0` 不成立，原函数 10 天、每本每日 0.5 元仍收费 5 元；归还早于借阅时输出负借阅天数而未拒绝。
- 影响：`tools/library/overdue-fine.html`，封顶语义和日期状态不可靠。
- 方案：明确零元封顶是支持还是非法并对应处理；校验日期先后，不输出正常罚单。

### 专著页码标点与页面示例不一致（中，确认源码冲突）
- 证据：`tools/library/citation-format.html:201-204,358-364` 出版年后拼接 `.100-150.`，同页示例用 `:100-150.`。
- 影响：`tools/library/citation-format.html`，引用复制结果与页面示例不一致；未独立审核全部著录标准。
- 方案：核对所用标准版本并统一示例与生成逻辑，增加页码有无及版本的用例。可加入用户主动维护的本地文献草稿与逐条编辑、批量复制。

### 覆盖与目录冲突
- 本次仅抽查上述 4 页；前三项使用内存 DOM 桩，未验证真实浏览器、专业规范、线上及其余页面。旧范围列 `tools/archive/`，当前目录不存在，须核对分类映射，不应算已覆盖。

## 2026-11-03 续查（并行批 H）

> 编号说明：首轮 4 条结论无编号，保留原文不动；本批新增 `RL-H` 系列，不与其重号。以下结论均为源码阅读 + node 内存复算，未做真实浏览器、英文态、移动端、门禁或线上验证。本批覆盖 8 页：`analysis-50/51/52/54`、`assessor-50`、`tester-17`、`clc-classifier`、`shelf-capacity`。

### RL-H20 中图法：R76 标为「眼科学」且 R77 缺失（中，待验证）
- 描述：R 大类中 `R76` 写成「眼科学」，全表无 `R77`，也没有耳鼻咽喉科学。按通行《中国图书馆分类法》分类表，R76 为耳鼻咽喉科学、R77 为眼科学。
- 证据：`tools/library/clc-classifier.html:387-401`（R 子类数据）。node 复算 `search('眼科学')` → 1 条 `R76 眼科学`，`search('R77')` → 0 条。仓库内无权威原表可比对，故列为待验证。
- 影响：`tools/library/clc-classifier.html`。按此表编目会把眼科学书籍错分到耳鼻咽喉类号。
- 方案：对照《中图法》第五版 R 类原表逐条校核，修正 R76 并补 R77；同时补一条类号唯一性/连续性测试。

### 留存优化
- `analysis-50` 的「预设」为空实现（`tools/research/analysis-50.html:409-411`，`analysis-51` 同名区域同样为空），可各补 3 组行业示例；两页解析逻辑近乎同构，建议抽公共解析器，避免同名分隔符缺陷各自复制。
- `analysis-52` / `analysis-54` 建议输出「坏行清单」（行号 + 原文），而不是只给条数，便于研究者修数据。
- `assessor-50` 结果卡建议并列「每触达人次成本」与「CPM(元/千次)」，并在卡片上直接标注单位，避免再次混淆。
- `tester-17` 可增加「四价单调性提示/曲线顺序图」，让倒序输入在提交前即可见；`clc-classifier` 建议提供「复制索书号」而非仅分类号，并在搜索无结果时给出相近类目。
- `shelf-capacity` 建议把单面/双面并排成一表，并输出 80%/85%/90% 三档填充率敏感度，替代单一估算。

### 续查覆盖
- 本批覆盖 8 页：`tools/research/analysis-50.html`、`tools/research/analysis-51.html`、`tools/research/analysis-52.html`、`tools/research/analysis-54.html`、`tools/research/assessor-50.html`、`tools/research/tester-17.html`、`tools/library/clc-classifier.html`、`tools/library/shelf-capacity.html`。
- 首轮已覆盖 4 页（`analysis-49`、`calc-97`、`overdue-fine`、`citation-format`），本批不重复。
- 未覆盖：`tools/library/archive-label.html`、`generator-label.html`、`stats-report.html` 及 `tools/research/index.html`、`tools/library/index.html`；`tools/archive/` 仍不存在，首轮目录疑问保留。
- 方法边界：全部结论基于静态源码 + node 内存复算，未做真实浏览器、英文态、移动端、门禁与线上验证；`RL-H20` 需按专业类表复核后方可定级。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页（`tools/library/archive-label.html`、`tools/library/generator-label.html`、`tools/library/stats-report.html`、`tools/cognition/digit-span-test.html`、`tools/cognition/schulte-table.html`、`tools/cognition/stroop-test.html`、`tools/museum/lighting-lux.html`、`tools/museum/era-comparator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/cognition/cognitive-assessment.html`、`tools/cognition/corsi-block-test.html`、`tools/cognition/nback-training.html`、`tools/cognition/time-perception.html`、`tools/museum/audio-guide-timer.html`、`tools/museum/exhibit-spacing.html`、`tools/museum/historical-calendar.html`、`tools/museum/showcase-monitor.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。
> 编号说明：文件实际最大编号为 K 批末尾 RL-K21（非提示中的 K16），为避免重号，本轮从 **RL-K22** 起续编。

### RL-K35 历史日历：节气用固定月-日表，2024 冬至等年份错位/漏标（中，确认）
- 描述：`TERM_DATES` 是固定「月-日」表（如冬至 12-22），不随年份变化；节气实际每年漂移 1–2 天。
- 证据：`tools/museum/historical-calendar.html:300`、`:379-393`。
- 复现：选 2024-12-21（2024 年冬至，北京时间 12-21）→ 节气行缺失（期望「冬至」）；选 2024-12-22 → 显示「冬至」（错误）。另 2024 处暑为 08-22，表给 08-23。
- 影响：节气标注在多数年份错位或漏标，历史日期解读失真。
- 方案：内置 1900–2100 逐年节气表，或用太阳黄经近似公式按年份计算。

- 本轮实读 8 页：`tools/cognition/cognitive-assessment.html`、`tools/cognition/corsi-block-test.html`、`tools/cognition/nback-training.html`、`tools/cognition/time-perception.html`、`tools/museum/audio-guide-timer.html`、`tools/museum/exhibit-spacing.html`、`tools/museum/historical-calendar.html`、`tools/museum/showcase-monitor.html`；新增 18 条（高 4 / 中 10 / 低 4）。
- 与既有条目无重复页面：research 非索引页（`analysis-49/50/51/52/54`、`assessor-50`、`calc-97`、`tester-17`）与 library 非索引页（`archive-label`、`citation-format`、`clc-classifier`、`generator-label`、`overdue-fine`、`shelf-capacity`、`stats-report`）已由前序批次全覆盖，本轮无剩余可读页，故转向 cognition/museum 未覆盖页。
- 未覆盖：`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`（分类索引页，无工具逻辑）；`tools/cognition/human-benchmark.html`；`tools/museum/timeline-viewer.html`、`tools/museum/visitor-route.html`。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 7 页（`tools/cognition/human-benchmark.html`、`tools/museum/visitor-route.html`、`tools/museum/timeline-viewer.html`、`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`）。**说明：四目录仅剩这 7 个未覆盖页（3 个工具页 + 4 个索引页），不足以凑满 8 页；未跨目录外扩，以免与 edu-language 批重复。** 仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 本轮实读 7 页：`tools/cognition/human-benchmark.html`、`tools/museum/visitor-route.html`、`tools/museum/timeline-viewer.html`、`tools/research/index.html`、`tools/library/index.html`、`tools/cognition/index.html`、`tools/museum/index.html`；新增 19 条（高 2 / 中 10 / 低 7）。
- 重复说明：本批无重读页面；RL-K51 是索引页文案问题（analysis-49/52/54 页面本身由前序批次覆盖，但该三处「卡片承诺未实现」此前未记录），RL-K57 为四个索引页共有模板问题。
- 四目录 35 个 HTML（31 个工具页 + 4 个索引页）至此全部覆盖；未覆盖：无。**本批范围内只剩上述 7 个未覆盖页，无法凑满 8 页，特此说明。**
