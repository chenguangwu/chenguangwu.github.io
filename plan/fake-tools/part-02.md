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

