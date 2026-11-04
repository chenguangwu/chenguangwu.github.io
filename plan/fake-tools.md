# 假实现与纯展示工具清单（截至 Q 批 · 44 页复核版）

## 口径与局限

- **数据来源**：`plan/categories/**/*.md`、`plan/G*.md` 中含「假 / 名不副实 / 纯展示 / 未实现 / 硬编码 / 回显 / 固定 / 承诺 / 无实际 / 演示 / 占位 / 模板页 / 不参与 / 装饰性」等关键词的条目，按页面路径去重后逐一核对源码。另有全站静态扫描作为规模参考。
- **两轮均为只读专项**：未改代码、未构建、未跑门禁、未开浏览器；临时脚本均在 `/tmp`。
- **本轮（2026-11-04）新增**：对主表 44 条「待验证」逐页复读**当前工作树**源码并给出结论；原「证据（行号）」列中大量数字实为 **plan 文档行号**（如 `drug-dosing.md:876`），已全部重锚为**页面当前行号**。原有 27 条「已确认」的行号未重核，保留原记录。
- **「已确认（真）」**：本轮实际读过源码关键行，并确认实现与宣称不符（静态证据即可复现，例如控件从未被读取、容器为空、公式与引用表口径冲突）。**「已否定」**：复核后该记录不成立或已被工作区改动修复。**「部分成立」**：一条记录内只有部分子项仍成立，需修但非整体重做。
- **静态判定局限**：未开浏览器，未验证运行时行为（如事件是否真正绑定、`TBKit` 运行时渲染、CSS 隐藏态）；结论只覆盖「源码中是否存在对应实现」。凡运行时才可判定的项，均标注「静态不可判」。
- **未做全站穷举**：全站 4705 个工具页（不含各行业 `index.html`），本轮覆盖的是「plan 已点名 + 抽检复核」的样本，**不代表只有这些页有问题**。
- **静态扫描口径**：`tools/*/*.html` 中不含任何 `<input|select|textarea` 的页面共 **147 页（3.1%）**。其中大量是**运行时由 JS 生成单选/输入的心理量表、测验、小游戏**（如 `psychology/*`、`clinical-nursing/morse-score.html`、`science/calculator.html`），并非纯展示缺陷；真正可疑的是「宣称计算/生成/识别却无任何交互入口」的页（见下表 B 类）。静态扫描只作规模参考，**不能直接当作缺陷数**。

## 汇总统计

| 指标 | 数值 |
|---|---|
| 清单原始去重页数 | **71** |
| 本轮复核页数 | **44** |
| 复核后仍成立页数 | **61**（原 27 + 本轮 34） |
| 已确认（真） | **58**（原 27 + 本轮 31） |
| 部分成立 | **3** |
| 已否定 | **10** |
| 待验证 | **0** |
| **最终「必须重做」页数** | **61**（真 58 + 部分 3，纯展示 B 类 3 页已计入） |
| 复核后 A（有输入但输出与输入无关/死输入/随机/回显/硬编码） | **20** |
| 复核后 B（无输入/无交互仍宣称计算·生成·检测·换算） | **3** |
| 复核后 C（名不副实：宣称功能未实现） | **35** |
| 复核后 D（占位/模板/通用套话） | **3** |
| 大分类分布（61 页）：医疗健康 13 / 商业运营 16 / 教育学习 10 / IT开发 4 / 设计创意 4 / 生活消费 3 / 金融财务 3 / 语言翻译 2 / 文娱爱好 2 / 图书档案 1 / 工程制造 1 / 长尾行业 1 / 自然科学 1 | 61 |

> 计数口径：每页只记一个「主类型」；含多种成分的页在证据列标注次要类型。已否定的 10 页不再计入类型分布与「必须重做」。

## 清单表

按留存影响从高到低排序。`置信度` 列：**已确认（真）**＝记录成立；**部分成立**＝仅部分子项成立；**已否定**＝记录不成立或已修复。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 置信度 | 留存影响 |
|---|---|---|---|---|---|---|
| 医疗健康 | `tools/pulmonology/tb-resistance.html` | A（+C） | `:271-272` 读取 PZA/EMB 耐药后**从未参与** `:276-287` 方案分支；DS-TB 仍给含 Z/E 的 `2HRZE/4HR`，勾选耐药不改变方案 | `plan/categories/03-医疗健康/specialties.md:417` | 已确认（真） | 高（用药建议与实际耐药谱冲突） |
| 医疗健康 | `tools/cardiology/calc-3.html` | C | `:180-193` 引据表写「7 项各 1 分、0-2/3-4/5-7、NSTEMI」，页内实现为 STEMI 10 项加权 0-14 | `plan/categories/03-医疗健康/specialties.md:417` | 已确认（真） | 高（评分口径自相矛盾） |
| 医疗健康 | `tools/pediatrics/ddst-screening.html` | A（+C） | `:143` 矫正胎龄输入存在但 JS 从不读取；`:659-661` 仅写入预设；`:130` 引据称 125 项/20 分钟 | `plan/categories/12-长尾行业/_others.md:1160` | 已确认（真） | 高（早产儿筛查结论失真） |
| 设计创意 | `tools/design/spectrum-visualizer.html` | A（+C） | 工作区 meta 已改为「不执行真实 FFT」，但 `:155` 公式框仍写「AnalyserNode 做 FFT」、`:202/:209` FAQ 仍称「教学 FFT」；全文无 `getUserMedia/Analyser`，实为正弦动画 | `plan/categories/04-设计创意/design.md:1126` | 已确认（真） | 高（残留虚构 FFT 说明） |
| 文娱爱好 | `tools/chess/xiangqi-endgame.html` | B | 0 个表单控件；`:329` 仅相关工具区，无棋盘/落子/判杀入口 | `plan/categories/11-文娱爱好/fun-entertainment.md:154` | 已确认（真） | 高（宣称输入残局判一步杀，实际静态题库） |
| 医疗健康 | `tools/tcm-chemistry/metabolite-prediction.html` | A | `:343` 只把品种写入 `<option>`，全文无读取 `compound` 值；仅 `mw` 参与 | `plan/categories/12-长尾行业/_others.md:1285` | 已确认（真） | 高（核心下拉是死输入） |
| 商业运营 | `tools/ecommerce/estimate-ranking.html` | A | `:130,132` 仅搜索量+权重 2 个输入；`:552` 计算只由这两值推出 | `plan/categories/06-商业运营/ecommerce-logistics.md:438` | 已确认（真） | 高（简介宣称销量/评价/点击/转化） |
| 商业运营 | `tools/hr/calc-81.html` | A | `:130,132` 仅「内推基数×达成系数」；`:304` 起算无人数/奖励/转化/ROI | `plan/categories/06-商业运营/hr-legal.md:418` | 已确认（真） | 高（深解承诺分岗位明细/自动分档/滚动统计） |
| 商业运营 | `tools/ecommerce/report.html` | C | `:124` 唯一输入是一个 textarea；`:203` 仅按逗号分行取数 | `plan/categories/06-商业运营/ecommerce-logistics.md:501` | 已确认（真） | 高（宣称拖拽上传/筛选/汇总报表） |
| 文娱爱好 | `tools/chess/gomoku-forbidden.html` | C | `:149-162` 只有「棋型/连子数/活口数」3 个数字输入，无棋盘坐标 | `plan/categories/11-文娱爱好/fun-entertainment.md:130` | 已确认（真） | 中高（宣称自动识别活三/冲四/连五） |
| 医疗健康 | `tools/clinical-lab/parasite-egg-id.html` | B | `:139` 仅一个搜索框；全文 0 个 `<img>/<svg>`，`.egg-svg` 容器为空 | `plan/categories/03-医疗健康/lab-diagnosis.md:357` | 已确认（真） | 中高（「形态识别」无图可看） |
| 医疗健康 | `tools/clinical-lab/urine-sediment-atlas.html` | B | `:144` 仅搜索框；`:289-292` 只输出文字字段；全文 0 个 `<img>/<svg>` | `plan/categories/03-医疗健康/lab-diagnosis.md:443` | 已确认（真） | 中高（「图谱查询」无图谱） |
| 医疗健康 | `tools/pulmonology/pulmonary-function.html` | C | `:139-142` cutoff 仅 0.70/0.75；`:179,211` 却称「LLN 可自定」 | `plan/categories/03-医疗健康/specialties.md:417` | 已确认（真） | 中高（LLN 未实现，老年判读偏差） |
| 医疗健康 | `tools/nephrology/aki-kdigo.html` | C | `:130-146` 仅基线/当前肌酐/尿量/时长 4 项；`:249` 起无 48h/7d 窗与 RRT | `plan/categories/12-长尾行业/_others.md:1403` | 已确认（真） | 中高（KDIGO 时间窗缺失） |
| 商业运营 | `tools/hr/stats-funnel-recruit.html` | A | `:123-126` 仅 4 个环节人数；`:258` 起无渠道花费/单聘成本字段 | `plan/categories/06-商业运营/hr-legal.md:383` | 已确认（真） | 中高（标题/meta 宣称渠道成本） |
| 商业运营 | `tools/marketing/email-subject-line-tester.html` | C | `:191,194` 标题+预览正文；`:270` 图表容器；`:436` 只画关键词权重饼图 | `plan/categories/06-商业运营/marketing-sales.md:433` | 已确认（真） | 中高（无打开率/送达率/垃圾度模型，预览正文不参评） |
| 商业运营 | `tools/hr/eap-xinli-zixun-weiji-ziyuan.html` | C | `:130,132` 仅员工规模+需求强度；全文无热线号码/转介资源链接 | `plan/categories/06-商业运营/hr-legal.md:545` | 已确认（真） | 中（EAP「资源」名不副实） |
| 商业运营 | `tools/marketing/marketing-utm-builder.html` | C | `:152-157` 单条链接 6 字段；`:240` 只拼一条 URL | `plan/categories/06-商业运营/marketing-sales.md:461` | 已确认（真） | 中（宣称批量生成，且必填规则与 FAQ 冲突） |
| 教育学习 | `tools/edu/word-memory.html` | A | `:572-575` `lastReview=Date.now()` 只写不读；无到期调度/复习队列 | `plan/categories/07-教育学习/edu-language.md:1117` | 已确认（真） | 中（「艾宾浩斯」未真正驱动复习） |
| 设计创意 | `tools/design/pixel-art-generator.html` | C（+D） | `:145,427-429` 导出按钮实为矩阵 CSV；`:75` FAQ 称导出字符画/CSS | `plan/categories/04-设计创意/design.md:788` | 已确认（真） | 中（导出承诺与实现不符） |
| 语言翻译 | `tools/language/text-polisher.html` | C（+D） | `:153-170` 仅空格/空行/标点/全半角 6 个格式化开关 | `plan/categories/07-教育学习/edu-language.md:380` | 已确认（真） | 中（「润色/改写/同义替换」未实现） |
| 图书档案 | `tools/library/generator-label.html` | C | `:146` 称「可批量打印」；`:249-262` 仅生成单张标签 + `window.print` | `plan/categories/07-教育学习/research-library.md:210` | 已确认（真） | 中（无批量条数/多盒循环） |
| IT开发 | `tools/it/md5.html` | C（+D） | `:47,606` 称「支持批量生成、碰撞检测参考」；`:403` 仅单条 `md5(text)` | `plan/categories/01-IT开发/it.md:1957` | 已确认（真） | 中（JSON-LD/介绍夸大） |
| 医疗健康 | `tools/healthcare/ideal-weight.html` | A | `:238-240` 读取 `age` 后未进入公式，仅 Devine 一路 | `plan/categories/03-医疗健康/drug-dosing.md:319` | 已确认（真） | 中（年龄是死输入） |
| 商业运营 | `tools/ecommerce/analysis-cost-8.html` | C | `:10` 称分项成本/费用效益比；`:125-129` 仅固定成本/单位变动成本/单价；`:210-225` 只算 CVP 保本 | `plan/categories/06-商业运营/ecommerce-logistics.md:394` | 已确认（真） | 中（名实不符） |
| 商业运营 | `tools/ecommerce/analysis-70.html` | A | `:126` 每行含「订单数」；`:205` 起 calc 全程未引用该列 | `plan/categories/06-商业运营/ecommerce-logistics.md:373` | 已确认（真） | 中（死输入） |
| 商业运营 | `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | C | `:130,132` 仅 HRIS/AI 两个成熟度分；`:304` 起只比较两分 | `plan/categories/06-商业运营/hr-legal.md:441` | 已确认（真） | 中（宣称对比成本与效率） |
| 医疗健康 | `tools/clinical-nursing/suction-pressure.html` | A | `:148` 压力输入；`:276-279` 区间已改为 80-120/80-100/60-80/40-60，**原「成人硬编码 150-200」已不成立**；残留默认值 `value="150"` 越界，首屏即提示「过高」 | `plan/categories/03-医疗健康/drug-dosing.md:333` | 已否定 | —（仅建议把默认值改为 100） |
| 医疗健康 | `tools/pulmonology/lung-rads.html` | A | `:142` 已有「实性成分(mm)」输入，`:266-271` 读入 `solidSize`；实性成分 ≥8mm→4B 分支可达，原「≥15mm 恒判 4A/4B 不可达」不成立 | `plan/categories/03-医疗健康/drug-dosing.md:876` | 已否定 | —（已修复） |
| 医疗健康 | `tools/clinical-lab/flow-cytometry-ratio.html` | A | `:154` Treg 输入、`:260` 读入后**全文未再使用**；`:302` 仅显示 NK 绝对值，`:316-330` 异常 flags 无 NK 低值判定，NK 偏低仍落「各项指标在参考范围内」 | `plan/categories/03-医疗健康/lab-diagnosis.md:291` | 已确认（真） | 中高（正向误判） |
| 医疗健康 | `tools/clinical-lab/semen-analysis.html` | A | `:148` IM 输入、`:261` 读入；`:262` 必填校验**不含 im**；`:267` 总活力只算 PR+NP；`:274` `setInterp('im',true,'')` 恒显 ✓ 正常 | `plan/categories/03-医疗健康/lab-diagnosis.md:398` | 已确认（真） | 中（IM 死输入 + 假正常） |
| 医疗健康 | `tools/clinical-nursing/bag-valve-mask.html` | A | `:153` 球囊下拉、`:323` 读入仅用于 `bagWarnText` 告警，不改变频率/潮气量；`:257` 写「高级气道后 8~10 次/分」，`:282-283` 婴儿 CPR 又写 20-30 次/分，页面口径冲突 | `plan/categories/03-医疗健康/drug-dosing.md:262` | 部分成立 | 中（告警已接线；频率口径需统一） |
| 医疗健康 | `tools/clinical-nursing/ostomy-bag-timing.html` | C | `:379` 已实现 `warnAt = interval*0.7`，`:382-396` 倒计时按 70% 进入预警；原「0.7 未实现、按 100%」不成立 | `plan/categories/03-医疗健康/drug-dosing.md:412` | 已否定 | —（已修复） |
| 医疗健康 | `tools/healthcare/map.html` | A | `:242-257` 已有四重输入守卫（收缩压/舒张压非正、超范围、舒张压>收缩压均拦截并提示），原「无守卫仍判正常」不成立 | `plan/categories/03-医疗健康/drug-dosing.md:312` | 已否定 | —（已修复） |
| 医疗健康 | `tools/healthcare/healthcare.html` | C | `:121` 英文简介已改为「按体重折算 + 上限倍数」，不再提 Clark/Young/BSA；`:163-165` 引据表仅列体表面积法作参考，`:464` FAQ 也只作局限说明 | `plan/categories/03-医疗健康/drug-dosing.md:81` | 已否定 | —（原记录已过期） |
| 医疗健康 | `tools/nephrology/edema-grading.html` | A | `:288` 读入 recovery，`:299-300` `recoveryGrade` 与 `depthGrade` 取 `Math.max` 参与最终分级，原「完全不参与」不成立 | `plan/categories/12-长尾行业/_others.md:1464` | 已否定 | —（已修复） |
| 医疗健康 | `tools/cardiology/coronary-calcium.html` | C | `:262-267` 原始 Agatston 分段（0/<100/<400/<1000/≥1000）已实现；`:271-285` MESA 简化百分位（<50/50–75/≥75）已实现 | `plan/categories/03-医疗健康/specialties.md:417` | 已否定 | —（已修复） |
| 金融财务 | `tools/finance/housing-fund-loan.html` | A | `:292` `var RATE = 0.031` 写死；`:205,233,366` 正文与结果均按 3.1% 输出，且标注「2024 年参考」；无利率可调输入 | `plan/categories/02-金融财务/finance.md:729` | 已确认（真） | 中高（利率口径过期） |
| 金融财务 | `tools/finance/salary-after-tax.html` | A | `:261` 读入 `months` 后仅用于 `:262` 合法性守卫，税费计算全程未用；`:266` brackets 有 7 档，`:294-298` 展示表只列 5 档（45%/35% 两档缺失） | `plan/categories/02-金融财务/finance.md:269` | 已确认（真） | 中（死输入 + 税率表不全） |
| 商业运营 | `tools/marketing/marketing-ltv-calculator.html` | A | `:457` 计算 `payback = cac/(ltv/(lifespanYears 或 3)/12)` 后**从未渲染**；`:461` 只展示 LTV:CAC 比率；简单模式无 lifespanYears 时回退 3 年 | `plan/categories/06-商业运营/marketing-sales.md:361` | 已确认（真） | 中（回本周期结果被丢弃） |
| 商业运营 | `tools/hr/bandwidth-1.html` | C | `:304-352` calc 为通用模板：按标题正则匹配后算 `(a+b)/2` 或 `a*b`，输入 v0/v1 被当作任意 A/B；meta `:10-11` 承诺的「分位值/内部公平性」无对应实现 | `plan/categories/06-商业运营/hr-legal.md:483` | 已确认（真） | 中低（整页模板化） |
| 商业运营 | `tools/hr/attendance-stats.html` | C | `:137` 公式明写「加班不参与计算」；`:142-152` 仅应出勤/三类扣款 + 员工行，无文件导入、无加班时长、无全勤奖 | `plan/categories/06-商业运营/hr-legal.md:309` | 已确认（真） | 中（三项承诺未实现） |
| 商业运营 | `tools/legal/child-support.html` | A | `:320` 读入 `childCount` 后，`:326-360` 计算全程未使用；抚养费比例不随子女数调整 | `plan/categories/06-商业运营/hr-legal.md:116` | 已确认（真） | 中（死输入，金额失真） |
| 商业运营 | `tools/legal/court-fee.html` | C | `:320-323` IP 案件无金额 500、有金额仍 `Math.min(500+amount*1%, 1000)`；文案却写「有金额按财产案件」，实际统一封顶 1000 | `plan/categories/06-商业运营/hr-legal.md:92` | 已确认（真） | 中高（受理费算错） |
| 商业运营 | `tools/biz/stats-time-response.html` | C | `:200-211` 仅条数/均值/中位数/最短最长/达标率；无 P90、无 FCR、无分组 | `plan/categories/06-商业运营/biz-startup.md:163` | 已确认（真） | 低 |
| 教育学习 | `tools/edu/flag-quiz.html` | C | `:158` 英文简介称 `timed multiple-choice quiz`；全文无 `setInterval`/计时状态；`:200` 深解又承诺「错题库」，无错题存储 | `plan/categories/07-教育学习/edu-language.md:1186` | 已确认（真） | 中（限时/错题双双落空） |
| 教育学习 | `tools/edu/typing-game.html` | C | `:10` meta 称「错题回看」、`:212` FAQ 称「成绩存本地」；全文 localStorage 仅 `:359-363` 存主题，无错题/成绩/排行 | `plan/categories/07-教育学习/edu-language.md:994` | 已确认（真） | 低 |
| 教育学习 | `tools/edu/chinese-zodiac.html` | C | `:353-355` 只读 `year` 后 `getZodiac(y)` 按公历年取模；无日期输入、无春节边界判断，FAQ 的「春节前按上一年」无法执行 | `plan/categories/07-教育学习/edu-language.md:165` | 已确认（真） | 中 |
| 教育学习 | `tools/edu/study-planner.html` | C | `:189-196` 两个 `formula-box` 完全重复；`:191/195` 仅文字承诺「完成率/按优先级排序」，`:246` 只统计完成任务数，无完成率/优先级 | `plan/categories/07-教育学习/edu-language.md:638` | 已确认（真） | 低 |
| 教育学习 | `tools/research/analysis-49.html` | C | `:230-250` 只计算 Cronbach α；全文无 KMO/Bartlett 实现（仅引据/卡片提到） | `plan/categories/07-教育学习/research-library.md:577` | 已确认（真） | 中 |
| 教育学习 | `tools/cognition/human-benchmark.html` | C | `:758` 样本恰 84 字；`:761` `textarea` 无 `onpaste` 拦截，`:767-775` WPM 按已输入字符计，粘贴即可刷分 | `plan/categories/07-教育学习/research-library.md:528` | 已确认（真） | 中低（基准可被粘贴作弊） |
| 教育学习 | `tools/museum/visitor-route.html` | C | `:342-347` 环路护栏已实现（原「负权无限循环」已否定）；但 `:183` 承诺「必看节点」，页面仅有起点/终点选择，无途经点/通行时间面板 | `plan/categories/07-教育学习/research-library.md:598` | 部分成立 | 中低（多目标路线未实现） |
| 教育学习 | `tools/museum/index.html` | C | `:88,90,93` 等 **4 张**卡片共用同一句「历史人文工具，帮助查询与了解历史文化知识」模板文案（非 3 张） | `plan/categories/07-教育学习/research-library.md:626` | 已确认（真） | 中低（分类页文案模板化） |
| 语言翻译 | `tools/language/translator.html` | C | `:185` 仅称「支持常用词与问候短句（本地词表）」；`:281` 明示「实际条数显示在输入框下方」；`:625` 运行时显示词表条数；全文无「100+」与语种自动检测承诺 | `plan/categories/07-教育学习/edu-language.md:394` | 已否定 | —（原记录与当前文案不符） |
| 语言翻译 | `tools/language/grammar-checker.html` | C | `:264-275` RULES 为字面正则（i/teh/recieve 等）；`:335` 仅收集命中项，无「问题密度分级」、无最小编辑距离 | `plan/categories/07-教育学习/edu-language.md:269` | 已确认（真） | 中 |
| IT开发 | `tools/it/http-cookies.html` | C | `:169` 英文简介称 `Parse and build ... headers`；实为 `:165` 分类聚合速查 + `:171` 搜索 + `:177-185` 图表/表格，无解析或构造入口 | `plan/categories/01-IT开发/it.md:1380` | 已确认（真） | 低（英文简介夸大） |
| IT开发 | `tools/it/markdown-to-html.html` | C | `:313-316` 图片规则已实现且置于链接规则之前，`![alt](url)` 输出 `<img>`；原「输出字面 ! + 链接」不成立 | `plan/categories/01-IT开发/it.md:207` | 已否定 | —（已修复） |
| IT开发 | `tools/it/whitespace.html` | C | `:219-228` 仅去首尾/删空行/合并行内空格/末尾单换行；无「全压成一行」，但 `:407` FAQ 承诺「可选全压成一行」；`:250-256` 预览按同一索引比较 `rawLines[pi]` 与 `lines[pi]`，删空行后错位 | `plan/categories/01-IT开发/it.md:219` | 已确认（真） | 低 |
| IT开发 | `tools/it/timestamp-converter.html` | C | `:416-426` 时区表为固定 offset（悉尼 +11、纽约 -5、洛杉矶 -8），无 DST 计算；夏令时期间纽约/悉尼显示偏差 1 小时 | `plan/categories/01-IT开发/it.md:347` | 已确认（真） | 中低 |
| 设计创意 | `tools/design/gradient.html` | C | `:241` FAQ 称「按 WCAG 算对比度并标红」；全文无 WCAG/contrast 计算代码 | `plan/categories/04-设计创意/design.md:396` | 已确认（真） | 低 |
| 设计创意 | `tools/design/mesh-gradient.html` | C | `:252-256` 仅颜色选择器 + 重新生成；无拖拽控制点、无图片/CSS 导出（仅 CSV 导出）、`:204` FAQ 的 WCAG 校验未实现 | `plan/categories/04-设计创意/design.md:487` | 已确认（真） | 低 |
| 金融财务 | `tools/finance/word-wrap.html` | C | `:489-491` CSV 导出仅导 `#word_wrapTable`，不含换行结果；`:183-189` 4 个页签只映射到分散元素（`:571-583`），无独立「预设/历史」面板，切页签仍停留在同一卡片 | `plan/categories/02-金融财务/finance.md:1246` | 部分成立 | 低 |
| 工程制造 | `tools/electronics/capacitor-calculator.html` | A | `:352-354` 注释「假设 5τ 内完成」后写死 `tau = 0.001`，`P = E/(5*tau)`；充电时间常数与 R/C 输入无关 | `plan/categories/08-工程制造/electrical-electronics.md:71` | 已确认（真） | 中 |
| 长尾行业 | `tools/acupuncture/acupoint-location.html` | A | `:399` `revCun = realCm ? 0 : 0` 为死变量；`:400` 反算提示用 `targetCun.toFixed(1)`（目标寸数）而非 X，公式自相矛盾 | `plan/categories/12-长尾行业/_others.md:827` | 已确认（真） | 低 |
| 自然科学 | `tools/quantum/pair-production-threshold.html` | A | `:128-129` 「（常量计算）」`dummy` 输入不参与任何输出；`:215-219` 结果为 2mₑc² 常量；`:221` 重置只把 dummy 置 1；预设为空 | `plan/categories/09-自然科学/physics-optics-quantum.md:94` | 已确认（真） | 低 |
| 生活消费 | `tools/life/countdown-timer.html` | A | `:514-521` `addPreset(...,isLunar=true)` 走 `SPRING_FESTIVAL_DATES` 逐年取春节日期（2025-01-29/2026-02-17…），原「硬编码 1 月 29 日、isLunar 未使用」不成立 | `plan/categories/05-生活消费/life.md:596` | 已否定 | —（已修复） |
| 生活消费 | `tools/life/stats-13.html` | C | `:291-293` 简介承诺「转化漏斗/时段峰值/报名付款聚合」，`:218-251` 只算人数/份数/均值/最多最少/金额，无占比、分档、漏斗、峰值 | `plan/categories/05-生活消费/life.md:908` | 已确认（真） | 中低 |
| 生活消费 | `tools/life/analysis-cost-9.html` | C | `:231-234` 仅合计/项均/最大项/占比表/极差；无固定-变动拆分、无单位成本、无盈亏平衡、无降本优先级排序（`:188/:193` 公式不可用） | `plan/categories/05-生活消费/life.md:750` | 已确认（真） | 低 |
| 生活消费 | `tools/life/assessor-target.html` | D | `:427` `opt-guide` 仍是「填写参数→点击计算/生成→查看输出」通用套话；`shopArea` `:226` 读入后未参与 `:232` 加权 | `plan/categories/05-生活消费/life.md:955` | 已确认（真） | 低（模板套话 + 面积死输入） |
| 教育学习 | `tools/edu/math-quiz.html` | D | `:513` `opt-guide` 仍是「点击计算/生成」套话（实际无该按钮，靠选项点击作答）；计时/题量/难度 `:363/:283-285` 已实现 | `plan/categories/07-教育学习/edu-language.md:972` | 已确认（真） | 低（仅文案套话） |
| 医疗健康 | `tools/rehabilitation/fim-scale.html` | D | `:576` `opt-guide` 仍是「填写参数→点击计算/生成→查看输出」通用套话，与实际 18 项下拉即时汇总流程不符 | `plan/categories/12-长尾行业/_others.md:1078` | 已确认（真） | 低（仅文案套话） |

## 44 页待验证复核结果

结论口径：`真` = 原记录成立、必须修（计入必须重做）；`部分` = 记录仅部分成立、需修但非整体重做（计入必须重做）；`假` = 记录不成立/已修复（不计入）。

| 页面 | 结论 | 证据行号（当前源码） | 判定说明 |
|---|---|---|---|
| `tools/clinical-nursing/suction-pressure.html` | 假 | `:148,276-279` | 压力输入→分级正常；四档区间已改为 80-120/80-100/60-80/40-60，原「成人 150-200 冲突」已修复。残留：默认值 150 越界，首屏即红（建议改 100）。 |
| `tools/pulmonology/lung-rads.html` | 假 | `:142,266-271` | 已有「实性成分」输入并读入；实性成分 ≥8mm→4B 分支可达，4A/4B 判定完整，「≥15mm 恒判 4A」不成立。 |
| `tools/clinical-lab/flow-cytometry-ratio.html` | 真 | `:154,260,302,316-330` | Treg 读入后全文未用（死输入）；NK 仅显示绝对值，异常 flags 无 NK 低值，NK 偏低仍报「各项指标在参考范围内」。 |
| `tools/clinical-lab/semen-analysis.html` | 真 | `:148,261-267,274` | IM 不在必填校验、不参与总活力；`setInterp('im',true,'')` 恒显 ✓ 正常。 |
| `tools/clinical-nursing/bag-valve-mask.html` | 部分 | `:153,323,189,257,282-283` | 球囊容量已接入但只驱动告警、不改变主参数（「不参算」部分成立）；`257` 的 8-10 次/分 与 `282-283` 婴儿 20-30 次/分 页面内冲突。 |
| `tools/clinical-nursing/ostomy-bag-timing.html` | 假 | `:379,382-396` | `warnAt=interval*0.7` 已实现，倒计时在 70% 处预警；原「0.7 未实现」不成立。 |
| `tools/healthcare/map.html` | 假 | `:242-257` | 已有非正、超范围、舒张压>收缩压三类守卫，均拦截并给出红色提示。 |
| `tools/healthcare/healthcare.html` | 假 | `:121,163-165,464` | 英文简介已改为体重折算+上限倍数；Clark/BSA 仅出现在引据表与「局限」FAQ，不再宣称三法实现。 |
| `tools/nephrology/edema-grading.html` | 假 | `:288,299-300` | 回弹时间与凹陷深度分别分级后取 `Math.max`，恢复时间真实参与分级。 |
| `tools/cardiology/coronary-calcium.html` | 假 | `:262-267,271-285` | 原始 Agatston 分段与 MESA 简化百分位重分类均已实现。 |
| `tools/finance/housing-fund-loan.html` | 真 | `:205,292,366` | 利率 `RATE=0.031` 写死，无利率输入；正文/结果都按 3.1%（2024 参考）输出。 |
| `tools/finance/salary-after-tax.html` | 真 | `:261,266,294-298` | `months` 仅做守卫、不参算；brackets 7 档但展示表仅 5 档。 |
| `tools/marketing/marketing-ltv-calculator.html` | 真 | `:448-457,461` | `payback` 计算后未渲染；只展示 LTV:CAC 比率；简单模式回退 3 年。 |
| `tools/hr/bandwidth-1.html` | 真 | `:304-352` | calc 为通用模板（按标题正则算 `(a+b)/2`/`a*b`），与薪酬带宽/分位/Compa-ratio 无关。 |
| `tools/hr/attendance-stats.html` | 真 | `:137,142-152` | 无文件导入、无加班时长、无全勤奖；公式还明写「加班不参与计算」。 |
| `tools/legal/child-support.html` | 真 | `:320` | `childCount` 读入后未参与比例/金额计算，抚养费不随子女数变化。 |
| `tools/legal/court-fee.html` | 真 | `:320-323` | IP 案件有金额时仍 `min(500+1%,1000)` 封顶，未按财产案件累进。 |
| `tools/biz/stats-time-response.html` | 真 | `:200-211` | 仅均值/中位数/达标率，无 P90/FCR/分组。 |
| `tools/edu/flag-quiz.html` | 真 | `:158,200` | 英文简介称 timed quiz，但无计时器；深解承诺「错题库」，无存储。 |
| `tools/edu/typing-game.html` | 真 | `:10,212,359-363` | 宣称错题回看、成绩存本地；localStorage 仅存主题。 |
| `tools/edu/chinese-zodiac.html` | 真 | `:353-355` | 只吃公历年取模，无日期/春节边界处理。 |
| `tools/edu/study-planner.html` | 真 | `:189-196,246` | 两个公式框重复；完成率/优先级仅文字，页面只统计完成任务数。 |
| `tools/research/analysis-49.html` | 真 | `:230-250` | 仅 Cronbach α；KMO/Bartlett 无实现。 |
| `tools/cognition/human-benchmark.html` | 真 | `:758,761,767-775` | 样本恰 84 字；textarea 无粘贴拦截，粘贴即可刷 WPM。 |
| `tools/museum/visitor-route.html` | 部分 | `:342-347,183` | 环路护栏已实现（原负权死循环已否定）；「必看节点/通行时间」仍无输入。 |
| `tools/museum/index.html` | 真 | `:88,90,93` | 4 张卡片共用同一段「历史人文工具」模板文案（原记录写 3 张，实为 4 张）。 |
| `tools/language/translator.html` | 假 | `:185,281,625` | 当前文案只称「本地词表」，运行时显示实际条数；无「100+」与语种检测承诺。 |
| `tools/language/grammar-checker.html` | 真 | `:264-275,335` | 纯字面正则匹配；无问题密度分级、无最小编辑距离。 |
| `tools/it/http-cookies.html` | 真 | `:165,169-171,177-185` | 英文简介称 Parse and build，实为静态速查+搜索+图表，无解析/构造入口。 |
| `tools/it/markdown-to-html.html` | 假 | `:313-316` | 图片规则已实现且在链接规则前，输出 `<img>`。 |
| `tools/it/whitespace.html` | 真 | `:219-228,250-256,407` | 无「全压成一行」选项但 FAQ 承诺；删空行后逐行预览按索引比较导致错位。 |
| `tools/it/timestamp-converter.html` | 真 | `:416-426` | 固定 offset 表，无夏令时处理。 |
| `tools/design/gradient.html` | 真 | `:241` | FAQ 称计算 WCAG 对比度并标红，全文无对应代码。 |
| `tools/design/mesh-gradient.html` | 真 | `:204,252-256` | 无拖拽控制点、无图片/CSS 导出、无 WCAG 校验。 |
| `tools/finance/word-wrap.html` | 部分 | `:183-189,489-491,571-583` | CSV 只导表格不含换行结果（成立）；页签映射到分散元素、无独立面板（部分成立）。 |
| `tools/electronics/capacitor-calculator.html` | 真 | `:352-354` | 时间常数写死 `tau=0.001`（5ms 假设），功率与 R/C 无关。 |
| `tools/acupuncture/acupoint-location.html` | 真 | `:399-400` | `revCun` 死变量；反算提示用目标寸数而非 X，公式错误。 |
| `tools/quantum/pair-production-threshold.html` | 真 | `:128-129,215-219,221` | `dummy` 假输入；输出为常量 2mₑc²；预设为空。 |
| `tools/life/countdown-timer.html` | 假 | `:514-521` | 春节预设走农历日期表逐年取值，`isLunar` 已使用。 |
| `tools/life/stats-13.html` | 真 | `:291-293,218-251` | 承诺漏斗/时段峰值/占比，实际仅人数/份数/均值/金额。 |
| `tools/life/analysis-cost-9.html` | 真 | `:231-234` | 仅合计/均值/占比/极差；无固定-变动拆分与降本排序。 |
| `tools/life/assessor-target.html` | 真 | `:427,226,232` | `opt-guide` 通用套话；面积 `shopArea` 读入但未参与加权。 |
| `tools/edu/math-quiz.html` | 真 | `:513,363` | `opt-guide` 仍是「点击计算/生成」套话（计时功能已实现，问题只在文案）。 |
| `tools/rehabilitation/fim-scale.html` | 真 | `:576` | `opt-guide` 通用套话与实际下拉即时汇总流程不符。 |

## Top 20 简析

> 本节为原批次留存简析，仅对第 5 条按本轮复核结果做了更正；其余条目对应页面仍成立。

1. **`tools/pulmonology/tb-resistance.html:271-287`**：吡嗪酰胺/乙胺丁醇耐药被勾选后，`dPza/dEmb` 虽被读取却从未进入方案分支；DS-TB 仍输出含 Z/E 的 `2HRZE/4HR`。这是本批风险最高的一条——用户会据此得到与实际耐药谱冲突的用药方案，属安全级问题，应优先修或强制加免责声明。
2. **`tools/cardiology/calc-3.html:180-193`**：页面引用表明确写 TIMI **7 项、0-2/3-4/5-7、NSTEMI**，实现却是 STEMI 的 10 项加权 0-14。同一页两套口径，临床评分可信度直接归零。
3. **`tools/pediatrics/ddst-screening.html:143`**：矫正胎龄输入存在、预设也写入，但 JS 从未读取；早产儿按实际月龄判项会系统性偏严。引据的 125 项与实现一致（32/31/29/33），说明缺陷集中在死输入而非项数。
4. **`tools/design/spectrum-visualizer.html:155`**：文案写 AnalyserNode + FFT + 峰值查看，代码里没有 `getUserMedia`/`AnalyserNode`，画面是正弦动画。设计类工具靠「看起来专业」留存，这类假实现最伤复访。
5. **`tools/pulmonology/lung-rads.html:142,266-271`（本轮更正）**：复核发现页面已有「实性成分(mm)」输入并参与 4A/4B 判定，实性成分 ≥8mm→4B 分支可达；**原记录「≥15mm 恒判 4A、4B 不可达」已否定**，不再列入修复。
6. **`tools/chess/xiangqi-endgame.html`**：0 个控件、无棋盘、无落子，只有静态题库。标题「残局提示」与「输入残局判一步杀」完全落空。
7. **`tools/tcm-chemistry/metabolite-prediction.html:343`**：核心「选择成分」下拉只负责渲染选项，`predict()` 从不读取它的值；用户换成分结果不变，是典型 A 类死输入。
8. **`tools/ecommerce/estimate-ranking.html:130-132`**：简介宣称搜索量/销量/评价/点击/转化多维建模，实际只有 2 个数字输入，结果由权重×搜索量直接推出。运营类用户一次就能识破。
9. **`tools/hr/calc-81.html:130-132`**：内推计算只有「基数×系数」，深解承诺的分岗位明细、自动分档、按过保人数滚动统计全未实现，ROI 无从谈起。
10. **`tools/ecommerce/report.html:124`**：整页唯一输入是一个 textarea，简介却写拖拽上传、筛选、汇总报表。交互承诺与实现差一个量级。
11. **`tools/clinical-lab/flow-cytometry-ratio.html:154,260,316-330`**：Treg 输入不参算；NK 只有绝对值展示、无低值告警，NK 42/μL、CD4 60% 仍可能统一报「各项指标在参考范围内」，属危险的正向误判。
12. **`tools/chess/gomoku-forbidden.html:149-162`**：用「棋型/连子数/活口数」三个抽象参数代替棋盘，用户无法还原自己的局面，判禁手失去意义。
13. **`tools/clinical-lab/parasite-egg-id.html:139`**：整页 0 张图，`.egg-svg` 是空容器。「形态识别」只剩文字表，检索价值大打折扣。
14. **`tools/clinical-lab/urine-sediment-atlas.html:144,289-292`**：同上，0 张图，只输出大小/形态/外观文字，「图谱」名不副实。
15. **`tools/pulmonology/pulmonary-function.html:139-142`**：FAQ 明确说「老年建议按 LLN」，但下拉只有 0.70/0.75，无法输入 LLN 值，老年阻塞判读会偏差。
16. **`tools/nephrology/aki-kdigo.html:130-146`**：KDIGO 依赖 48h/7d 时间窗与 RRT 状态，页面只有 4 个字段，分期的核心判据缺失。
17. **`tools/hr/stats-funnel-recruit.html:123-126`**：标题/meta 讲渠道花费与单聘成本，页面只有 4 个环节人数，成本维度全部缺失。
18. **`tools/marketing/email-subject-line-tester.html:191,436`**：只按关键词权重画饼图，无打开率/送达率/垃圾度模型；预览正文输入不参与评分，且自带示例标题得 85 分「优秀」。
19. **`tools/edu/word-memory.html:572-575`**：`lastReview` 只写不读，所谓艾宾浩斯调度没有到期队列，复习节点实际由用户手动决定。
20. **`tools/design/pixel-art-generator.html:145,427-429`**：导出按钮实际导出矩阵 CSV，而不是宣称的字符画/CSS；调色板仅 6 色而非文案的 8 色。

## 建议修复顺序

**P0｜安全与错误输出（先止血，1 周内）**
1. `tools/pulmonology/tb-resistance.html` —— 耐药输入必须进入方案分支，或直接下架方案文本只保留宣教。
2. `tools/cardiology/calc-3.html` —— 引据表与实现二选一；若保留 STEMI 评分，删除 NSTEMI 引用行。
3. `tools/pediatrics/ddst-screening.html` —— 接通 `correctGA` 或删除该输入，避免早产儿误判。
4. `tools/clinical-lab/flow-cytometry-ratio.html` —— Treg 接通或删除；补 NK 绝对值低值告警（`<100/μL` 量级按实验室参考区间），避免「全部正常」误判。
5. `tools/pulmonology/pulmonary-function.html`、`tools/nephrology/aki-kdigo.html` —— 补 LLN/时间窗判据或明确标注「不含 X 判据」。
6. `tools/clinical-lab/semen-analysis.html` —— IM 与 PR+NP+IM=100 一致性校验接通，或删除该行，避免恒 ✓ 假正常。

**P1｜金额/法规类算错（直接误导用户，2 周内）**
7. `tools/finance/housing-fund-loan.html` —— 把 `RATE` 改为可输入（默认 2.85% 或标注「按最新政策填写」），并同步正文/示例。
8. `tools/finance/salary-after-tax.html` —— `months` 接入累计预扣或删除；补 35%/45% 两档，避免高收入税负偏低。
9. `tools/legal/court-fee.html` —— 知识产权有金额时按财产案件累进，或删掉该文案。
10. `tools/legal/child-support.html` —— `childCount` 进入比例/金额公式（多子女分摊/上浮），或删除该控件。
11. `tools/marketing/marketing-ltv-calculator.html` —— 渲染 `payback`，并把 `lifespanYears` 改为显式输入，去掉回退 3 年。

**P2｜名不副实/模板重做（3 周内）**
12. `tools/hr/bandwidth-1.html`、`tools/hr/attendance-stats.html`、`tools/life/stats-13.html`、`tools/life/analysis-cost-9.html` —— 重写为真实业务模型，或把标题/meta/深解降级为「通用统计」。
13. `tools/hr/attendance-stats.html`、`tools/edu/study-planner.html`、`tools/research/analysis-49.html`、`tools/language/grammar-checker.html` —— 补齐承诺字段（导入/加班/全勤、完成率/优先级、KMO/Bartlett、密度/编辑距离）或删除承诺。
14. `tools/design/mesh-gradient.html`、`tools/design/gradient.html`、`tools/finance/word-wrap.html`、`tools/electronics/capacitor-calculator.html` —— 补导出/WCAG/时间常数输入，或删掉对应文案。

**P3｜文案与交互对齐（4 周内，成本最低）**
15. `tools/edu/flag-quiz.html`、`tools/edu/typing-game.html`、`tools/cognition/human-benchmark.html`、`tools/it/http-cookies.html`、`tools/it/whitespace.html`、`tools/it/timestamp-converter.html`、`tools/museum/index.html`、`tools/life/assessor-target.html`、`tools/edu/math-quiz.html`、`tools/rehabilitation/fim-scale.html`、`tools/quantum/pair-production-threshold.html`、`tools/acupuncture/acupoint-location.html` —— 优先改 meta/FAQ/深解与 `opt-guide`，能删控件就删，避免「搜索承诺」与「页面能力」继续错位。
16. `tools/clinical-nursing/bag-valve-mask.html`、`tools/museum/visitor-route.html`、`tools/finance/word-wrap.html` —— 统一页面内口径（婴儿通气频率、必看节点、页签面板）。

**P4｜已否定，不再投入（从待修清单移除）**
17. `suction-pressure`、`lung-rads`、`ostomy-bag-timing`、`map`、`healthcare`、`edema-grading`、`coronary-calcium`、`translator`、`markdown-to-html`、`countdown-timer` —— 记录已不成立/已修复，仅需回归时复测。

## 待验证补充清单

主表 **44 条「待验证」已全部复核完毕，待验证剩余 0**。原先「主表未展开、仅 plan 点名」的 4 页已顺手抽查（**不计入 44 页统计，也不计入 61 页必须重做**）：

| 页面 | 抽查结论 | 证据行号 | 说明 |
|---|---|---|---|
| `tools/marketing/marketing-ltv-cac-ratio.html` | 部分成立 | `:430,456,476` | 回本周期仍按固定 36 个月摊算，但已展示在表格与指标卡，不再算「未展示」。 |
| `tools/marketing/marketing-cac-calculator.html` | 已否定 | `:329,419` | 回收期已按 `cac/(ltv/36)` 计算并在明细表展示，原「不展示」不成立。 |
| `tools/design/base64-to-image.html` | 真 | `:202,233` | FAQ 称按 data URI MIME 识别；魔数字节校验只出现在引据表，代码层无嗅探。 |
| `tools/edu/number-memory.html` | 真 | `:412` | 记录时间用 `toLocaleString('zh-CN')`，中英混排，原记录成立。 |

### 复核反例（计划记录已过期，不计入清单）

| 页面 | plan 原记录 | 本轮复核结果 |
|---|---|---|
| `tools/healthcare/bsa-calculator.html` | `drug-dosing.md:269`「年龄完全不参与计算」 | **不成立**：`:305-311` 读取 `age`，`<18` 走 Haycock、`≥18` 走 DuBois |
| `tools/chinese/chinese-character.html` | `edu-language.md:281`「字库仅 20 字，曦查不到」 | **不成立**：`:285` `charDB` 实际 45+ 字，含「曦」 |
| `tools/museum/visitor-route.html` | `research-library.md:507`「负权通道导致无限循环」 | **已修复**：`:342` 已有 `seen[cur]` 与 `steps <= nodes.length` 双重护栏（本页另一条「必看节点未实现」仍为部分成立） |
| `tools/finance/word-search.html` | `finance.md:1255`「宣称自定义词表/网格/可打印」 | **文案已对齐**：工作区 meta/正文/FAQ 已改为「固定 12×12、不支持自定义/打印」，仅剩功能受限，不再算虚假承诺 |
| `tools/edu/country-quiz.html` | `edu-language.md:1167`「宣称限时作答」 | **文案已对齐**：工作区 meta 已改为「共 10 题、无计时模式」，不再算名不副实 |

**本轮新增否定 10 条**（详见「44 页待验证复核结果」及主表 `已否定` 行）：

| 页面 | 原记录要点 | 否定依据 |
|---|---|---|
| `tools/clinical-nursing/suction-pressure.html` | 成人区间硬编码 150-200 | `:276-279` 已改为 80-120 等四档；仅默认值 150 越界 |
| `tools/pulmonology/lung-rads.html` | 部分实性 ≥15mm 恒判 4A、无实性成分输入 | `:142` 有输入，`:266-271` 4B 分支可达 |
| `tools/clinical-nursing/ostomy-bag-timing.html` | 间隔×0.7 预警未实现 | `:379,382-396` 已按 70% 预警 |
| `tools/healthcare/map.html` | 无输入守卫，舒张压>收缩压仍正常 | `:242-257` 四重守卫齐全 |
| `tools/healthcare/healthcare.html` | 英文简介称 Clark/Young/BSA 三法 | `:121` 已改为体重折算；Clark/BSA 仅作引据与局限说明 |
| `tools/nephrology/edema-grading.html` | 恢复时间不参与分级 | `:288,299-300` 已取 `max(depthGrade, recoveryGrade)` |
| `tools/cardiology/coronary-calcium.html` | 百分位与 Agatston 分段未实现 | `:262-267,271-285` 两者均实现 |
| `tools/language/translator.html` | 称 100+ 词汇、缺语种检测 | `:185,281,625` 当前文案只称本地词表并显示实际条数，无 100+/检测承诺 |
| `tools/it/markdown-to-html.html` | 图片语法未实现 | `:313-316` 已实现且在链接规则前 |
| `tools/life/countdown-timer.html` | 春节写死 1 月 29 日、isLunar 未用 | `:514-521` 已按农历日期表逐年取值 |

## T 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均已读当前源码并可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| 生活消费 | `tools/sports/rehab-motion.html` | C（+A） | `:118-131`（仅体重/次数等输入）、`:559-575`（输出为体重×次数） | `plan/categories/05-生活消费/sports-fitness.md` SF-N28（高） | 标题/英文简介承诺「按损伤部位给出动作库」，实际无动作库、无部位选择，并把体重×次数当训练负荷（840kg 伪负荷） |
| 生活消费 | `tools/sports/training-planner.html` | C | 模板固定 4 条训练日；选 5/6 天仍只生成 4 天 | `plan/categories/05-生活消费/sports-fitness.md` SF-N24（高） | 宣称按每周天数生成计划，天数选项不参与模板条数；同日核心分化动作整组重复（SF-N25） |
| 商业运营 | `tools/biz/text-extract-html-tags.html` | A | `:166-170`（五个开关中两个默认勾选）、`:313-315`（仅取三个）、`:326-332`（「含属性」未勾仍剥属性） | `plan/categories/06-商业运营/biz-startup.md` BS-N31/BS-N32（中） | 宣称「指定标签/仅正文」筛选，实际开关未参与过滤；`uniqueCount` 在清空输入后保留上次值 |

## U 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均读当前源码、可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| IT开发 | `tools/it/phone-parser.html` | C | `:329-345` 输入框为 `type="number"` 无法粘贴示例号码；解析结果仅做分段拼接，无运营商/归属地解析 | `plan/categories/01-IT开发/it.md` IT-N412/IT-N413 | 宣称「手机号归属地/运营商解析」，实际只按长度切分并回显 |
| 医疗健康 | `tools/gastroenterology/ercp-success.html` | B（局部） | 关键成功率输入未进入最终判定，仅按固定基线输出「可成功」 | `plan/categories/03-医疗健康/specialties.md` 03-17x | 名不副实；需临床复核 |
| 生活消费 | `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` | C | 仅两个通用数值输入，按模板算比值；页面承诺的得分率/关键分统计未实现 | `plan/categories/05-生活消费/sports-fitness.md` SF-N43 | 通用两参模板套体育标题 |
| 文娱爱好 | `tools/fun/anagram-game.html` | A | `:15-24` 5 套固定字母题 + 每条硬编码 `valid` 词表，判定 `cur.valid.includes(v)`，无字母多重集校验、无词典、不可换题 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N27 | 合法词 SILT 判错、不可拼的 ICE 判对 |
| 文娱爱好 | `tools/fun/sequence-puzzle.html` | C | 仅 6 类数字序列；承诺的质数/阶乘/图形序列与「做错有解析」均无实现 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N30 | 教学价值落空 |

## V 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均已读当前源码、可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| IT开发 | `tools/it/morse-decode-advanced.html` | C | `:3669-3677` 「增强版/自动推断时间单位/容错」无实现，无分隔电码一律解成 `?` | `plan/categories/01-IT开发/it.md` IT-N440 | 名不副实 |
| 生活消费 | `tools/sports/baofali-zongtiao-lidingtiaoyuan.html` | C（+A） | `:398-405` 仅「初速度→跳高」换算；meta 承诺的体重/远度/功率/爆发力指数均无输入输出 | `plan/categories/05-生活消费/sports-fitness.md` SF-N45 | 承诺未实现 |
| 长尾行业 | `tools/gardening/balcony-sunlight.html` | B（半假） | `:120/:124/:128` 三个下拉无 `option`；`:262/:306/:339-343` 查表恒按南向·春 6.0h | `plan/categories/12-长尾行业/_others.md` 12-N206 | 核心三维度输入不可选，结果恒定 |
| 商业运营 | `tools/biz/text-to-banner.html` | C | `:10/:153` 宣称画布横幅/字体/配色/PNG；`:160-169` 仅 8 种边框、`:315-345` 仅字符串拼框 | `plan/categories/06-商业运营/biz-startup.md` BS-N65 | 实际只剩 ASCII 方框 |

## W 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均已读当前源码、可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| IT开发 | `tools/it/url-qr.html` | A | `:247-267` 只画三个定位图形与时序图案，其余由 `pseudoRandom(strHash(text))` 随机填充（核心 `:260`）；无数据位/格式信息/掩码/纠错码，尺寸恒 29×29 | `plan/categories/01-IT开发/it.md` IT-N456 | 产出不可扫码，属装饰图 |
| 长尾行业 | `tools/nutrition/generator-nutrition-label.html` | A | `:120` 唯一输入是「生成数量」；`:203-209` 能量/蛋白/脂肪/碳水/钠全部 `Math.random()` 独立生成，能量与宏量营养素不符（Atwater 核算应 28.5–403.5 kcal，页面只 80–379 kcal） | `plan/categories/12-长尾行业/_others.md` 12-N215 | 宣称「适合预包装食品合规」 |
| 生活消费 | `tools/sports/analysis-19.html` | C | `:120-121` 仅一个「回合,攻/防,成/败」文本框；`:210-245` 只做计数与百分比，无视频上传/播放/时间轴/标注 | `plan/categories/05-生活消费/sports-fitness.md` SF-N65 | 标题称「视频分析」 |
| 工程制造 | `tools/machinery/detector-159.html` | C | `:136-138`、`:221` 三项自定义阈值（刚度≥100 N/mm、载荷≥50 kN、疲劳≥1×10⁶）被标为 GB/T 1448 / GB/T 307 要求；`:240` 称「可用于质量验收」 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H56 | 冒用国标验收口径 |
| 文娱爱好 | `tools/fun/tongue-twister.html` | C | `:275` `function start(){next();}`；全页无计时状态/停止按钮/用时显示，`:199-204` 算例与 FAQ 却称 performance 计时 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N59 | 「跟读计时」完全未实现 |

## X 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均已读当前源码、可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| 长尾行业 | `tools/leather/xueyunhoudukongzhi.html` | A | 削匀评分恒 100，目标厚度输入不参与判定 | `plan/categories/12-长尾行业/_others.md` 12-N222 | 评分与输入无关 |
| 生活消费 | `tools/sports/calc-angle-slope.html` | C | 实为百分比计算器，无坡度换算/角度制换算 | `plan/categories/05-生活消费/sports-fitness.md` SF-N74 | 名不副实 |
| 工程制造 | `tools/machinery/detector-134.html`、`detector-hardness-torque.html`、`detector-155.html` | C | 三页共用模板，`stdItems` 硬编码阈值标注为 GB/T 528/1689/16823/230/1800/24600/4604/307 要求，并输出「可用于质量验收」；`formula-desc` 仍是「合法性校验」模板残留 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H63 | 与 MM-H56 同源蔓延 3 页 |
| 文娱爱好 | `tools/music/random-training-rhythm.html` | C | 唯一输入「生成数量」，`gen()` 只拼文本；无 `AudioContext`、无敲击采集/命中判定/准确率 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N72 | 宣称节拍训练与准确率统计 |
| IT开发 | `tools/it/charset-detector.html` | C | 「编码识别器」仅做 6 条固定替换，非真实检测 | `plan/categories/01-IT开发/it.md` IT-N49x | 名不副实 |
| 文娱爱好 | `tools/fun/generator-laugh.html` | C | `:232-241` `gen()` 只输出文字方案；全文无 `AudioContext`/`OscillatorNode`，无播放与 wav 导出 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N79 | 宣称实时合成并可导出 wav |
| 文娱爱好 | `tools/fun/meditation-timer.html` | C | `:275-320` 只生成静态时刻表；无开始/暂停、无 `setInterval`、无 `AudioContext`，历史不记实际时长 | `plan/categories/11-文娱爱好/fun-entertainment.md` FE-N86 | 无法用于计时 |

## Y 批新增假工具候选（2026-11-04）

> 本轮 10 个只读子 agent 的增量产出，均已读当前源码、可由静态证据复现；**不计入上表 61 页统计**，待修复线复核后并入主表。

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| IT开发 | `tools/it/email-qr.html` | B | `:262-282` `renderQR` 只画三个定位符与时序线，其余 29×29 模块由 `:275-280` FNV 种子伪随机填充；无数据编码、Reed-Solomon、格式/版本信息，扫码得不到 `mailto:` | `plan/categories/01-IT开发/it.md` IT-N520 | 伪二维码（与 `location-qr` 同源） |
| IT开发 | `tools/it/location-qr.html` | B | `:264-283` 固定 25×25 网格，仅画定位角/定时线，其余用 `strHash`+LCG 填 0/1；无数据位/纠错/掩码，扫码无法还原 `geo:` 载荷 | `plan/categories/01-IT开发/it.md` IT-N521 | 伪二维码 |
| 工程制造 | `tools/machinery/detector-stretch.html` | C | `:213,232` 阈值 0.08 g、20 MPa、1×10⁶ 次写死，却称依据 GB/T 1689、GB/T 528、GB/T 1688（均为试验方法标准，不规定该合格线）判定合格，并称「可用于质量验收」；`:125` 仍为「合法性校验」模板 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H81 | 写死阈值冒充国标 |
| 农业养殖 | `tools/agriculture/assessor-1.html` | A | `:126,220-228` 总损失率只用「理论产量−实际收获」，田间落粒与脱粒清选两项输入不参与主结果；公式框分母「理论−实际+损失」与代码 `totalLoss/ty` 不符 | `plan/categories/10-农业养殖/agriculture.md` 10-64 | 分项损失死输入 |
| 农业养殖 | `tools/agriculture/calc-6.html` | A | `:126-127,278-281` 饲养周期仅参与 `cycle<=0` 校验，不进入任何算式；45 天与 120 天结果相同，公式说明「年批次数=365÷饲养周期×批次数」未实现 | `plan/categories/10-农业养殖/agriculture.md` 10-67 | 饲养周期死输入 |

> 说明：`tools/biz/text-sort.html`（BS-N140）主体排序可用，仅图表/数据表/历史/导出因 `textarea.textContent` 恒空而全失效，按「部分成立」留待修复线复核，暂不计入假工具页数。
