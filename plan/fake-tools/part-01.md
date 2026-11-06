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

