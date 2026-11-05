# tools-audit-84 逐页处置台账

> 对象：`wip/tools-audit-84` = `12c22fba9f` 的批量改写（65 文件）。`tools/ecommerce/analysis-cost-8.html` 已在 master 由 `54797f1927` 修好，不在此列 ⇒ 应处置 64 页。
> 判档：**A** = 改写除数字错外有实质提升（结构/算例/依据/口径）且内容正确 ⇒ 修正数字后保留；**B** = 改写只是把正确内容改成错的 ⇒ 整页回退，最终与 HEAD 原版完全一致。
> 判定依据：页面 `calc()` 实际表达式 + 常量表 + node 实跑。
>
> **回退前置条件（2026-11-05 新增，后续 34 页必须遵守）**：「B 整页回退」只在**HEAD 原版本身正确**时成立。判定顺序固定为：先读页面 `calc()` 真实表达式 → 按默认输入 node 实跑 → 与 HEAD 页面文字值比对；**若 HEAD 文字值与实现不符 ⇒ 该页不算 B，必须修页面（修缺陷），不能整页回退**；只有「HEAD 值对 + 存档值错」才判 B 并回退。
> 已按此口径复核 `edu/calc-4`、`dermatology/vasi-vitiligo`、`obstetrics/fetal-weight-hadlock`、`fishery/feed-protein-fat` 四页：HEAD 值与实现逐项吻合（95.0 / 16.75 / 2892 g / 11.45 kJ/g），存档值（91.7 / 28 / 3100 / 1.14）均无法由实现公式导出 ⇒ 维持 B，无需修缺陷。

| 路径 | 档 | 处置 | 关键依据 | commit |
|---|---|---|---|---|
| tools/edu/calc-4.html | B | 整页回退 | 算例 (85−70×0.4)/0.6=95.0，改写写 91.7 | `129436b5ef` |
| tools/dermatology/vasi-vitiligo.html | B | 整页回退 | 5×0.95+20×0.60=16.75，改写写 16+12=28 | `129436b5ef` |
| tools/obstetrics/fetal-weight-hadlock.html | B | 整页回退 | log₁₀ 3.4612→2892g，改写写 3.49→3100g | `129436b5ef` |
| tools/fishery/feed-protein-fat.html | B | 整页回退 | 可消化能 11.45 kJ/g，改写写 1.14 kJ/g | `129436b5ef` |
| tools/healthcare/ibw.html | B | 整页回退 | 实现含 ABW=IBW+0.4×超出部分，改写删掉该功能点 | `c6695142a2` |
| tools/healthcare/egfr.html | B | 整页回退 | 实现为 CKD-EPI 2009 含种族系数 1.159，改写弱化为「完整公式」 | `c6695142a2` |
| tools/obstetrics/kupperman-score.html | B | 整页回退 | 20 分→中度(16–30)、5 分→基本正常(≤6)、13 项满分 63 | `c6695142a2` |
| tools/urology/iief5-score.html | B | 整页回退 | 14 分→轻中度(12–16)、22→正常下限 | `c6695142a2` |
| tools/cardiology/coronary-calcium.html | A | 修正保留 | 系数 1/2/3/4、40×3+15×1+20×2=175；保留「本页直接输入积分、不逐血管计算」范围说明 | `c6695142a2` |
| tools/obstetrics/gdm-ogtt.html | B | 整页回退 | 诊断切点 5.1/10.0/8.5；5.3/7.8/6.7 为治疗后目标 | `ceb36d94e9` |
| tools/pediatrics/pediatric-anemia.html | B | 整页回退 | 日总量上限 200 mg 元素铁（实现 Math.min） | `ceb36d94e9` |
| tools/pediatrics/pediatric-asthma.html | B | 整页回退 | C-ACT 满分 27、部分控制 20–22 | `ceb36d94e9` |
| tools/pulmonology/anti-tb-dosing.html | B | 整页回退 | PZA/EMB 50–70kg；55kg→1750/1000 mg | `ceb36d94e9` |
| tools/rheumatology/essdai.html | B | 整页回退 | 12 域 2+4+3+2+1=12，12 大系统 | `ceb36d94e9` |
| tools/agriculture/irrigation-uniformity.html | B | 整页回退 | 实现 cu>=90/80/70；改写写 0.85/0.75（单位+档位双错） | `51af32defb` |
| tools/civil/slope-stability-fos.html | B | 整页回退 | 固定 Fs>=1.3（二级）；改写写 1.3~1.5 | `51af32defb` |
| tools/food/convert-concentration.html | B | 整页回退 | SG=1+Bx÷[258.6−(Bx÷258.2)×227.1]=1.0830；改写写 1.0713 | `51af32defb` |
| tools/fitness/generator.html | B | 整页回退 | title-en/desc-en 被退化成占位符，无实质提升 | `51af32defb` |
| tools/hematology/generator-analysis.html | B | 整页回退 | title-en/desc-en 被退化成占位符，无实质提升 | `51af32defb` |
| tools/agriculture/assessor-1.html | A | 修正保留 | 保留真实 title-en/desc-en、参考值（机收 3.0/人工 2.0、不判定合格）表述；恢复四输入描述与样框说明 | `51af32defb` |
| tools/fishery/calc-power.html | B | 整页回退 | 实现 Q=1.163×V×ΔT÷η（1368.2 kWh/57.01 kW/68.41 kW）；改写换成 P=V×I | `51af32defb` |
| tools/construction/ac-size-guide.html | B | 整页回退 | 实现 ÷2500（4400W→1.8 匹）；改写写 2324W | `51af32defb` |
| tools/biz/text-merge.html | B | 整页回退 | 实现 `split('\\n')`+`join(sep)` 按行拼接；改写宣称两列配对合并 | `c1c2f4d76c` |
| tools/biz/text-to-banner.html | B | 整页回退 | 实现 8 种字符边框、仅导出 .txt；改写宣称 figlet 字体与图片导出 | `c1c2f4d76c` |
| tools/cardiology/ckd-epi.html | B | 整页回退 | 实现仅 Scr 版 CKD-EPI 2021（女65/Scr1.3→45.6）；改写虚构胱抑素 C 输入 | `c1c2f4d76c` |
| tools/cardiology/hypertension-jnc.html | B | 整页回退 | 实现含「平均风险」档；152/94+糖尿病(1级,rf≥1)→中危，改写写很高危 | `c1c2f4d76c` |
| tools/chess/xiangqi-endgame.html | B | 整页回退 | 实现为杀法条件卡（无棋盘输入/不着法）；改写宣称给着法序列 | `c1c2f4d76c` |
| tools/clinical-lab/convert-39.html | B | 整页回退 | 实现为 INR=(PT/对照)^ISI（18/12,1.1→1.56）；改写换成胆固醇换算 | `c1c2f4d76c` |
| tools/clinical-lab/vaginal-discharge-grading.html | B | 整页回退 | 实现为清洁度 Ⅰ–Ⅳ（杆菌/球菌/上皮/WBC）；改写换成 Nugent 评分 | `c1c2f4d76c` |
| tools/clinical-nursing/assessor-rater-risk.html | B | 整页回退 | Morse 25+15+20+10=70；改写写 55 | `c1c2f4d76c` |
| tools/construction/calc-1.html | B | 整页回退 | 实现 φ 表实跑 λ≈195.6、φ≈0.196、Nrd≈17.0 kN；改写写 30–40 kN 无算式来源 | `d8d05b94ec` |
| tools/data/generator-35.html | A | 修正保留 | 保留「组数留空时按 Sturges ceil」标题口径（与 formula-eq 一致）；恢复真实 title-en/desc-en | `d8d05b94ec` |
| tools/design/mesh-gradient.html | B | 整页回退 | 改写把算例换成转义 HTML 垃圾与虚假 SVG/滤镜说法，无实质提升 | `d8d05b94ec` |
| tools/design/pixel-art-generator.html | A | 修正保留 | 保留真实 desc-en（4–24 网格/6 色/字符画与 box-shadow）；回退「照片像素化/32 色」错误深解与 FAQ | `d8d05b94ec` |
| tools/ecommerce/report.html | B | 整页回退 | 实现为「指标,本期,上期」环比看板；改写虚构筛选/汇总 BI 图表 | `d8d05b94ec` |
| tools/finance/generator-report-1.html | B | 整页回退 | title-en/desc-en 退化为「Finance」占位；英文元数据退化，归英文元数据线处理 | `d8d05b94ec` |
| tools/fire-rescue/smoke-management.html | B | 整页回退 | 实现 V 含 1.2 安全系数：m=35.38 kg/s、V=47.3 m³/s、170368 m³/h、12 口；改写删 1.2 得 39.4/141972 | `d8d05b94ec` |
| tools/fire-rescue/sprinkler-design.html | B | 整页回退 | 1040 L/min=17.3 L/s → 水池 62.4 m³(1h)/124.8 m³(2h)；改写写 1040–2080 L（差 1000 倍） | `d8d05b94ec` |
| tools/fishery/drug-withdrawal-fish.html | B | 修正权威源，待构建复核 | 实际采用 ceil；示例向上取整为 9/47 天，明确模型不能保证残留达标，应遵守说明书及法规 | 未提交 |
| tools/fishery/pond-desilting.html | B | 修正权威源，待构建复核 | 默认 5 亩、保留 5 cm：5×666.67×15/100≈500 m³，费用 7500 元；存档漏扣保留层写 667 m³ | 未提交 |
| tools/fishery/stocking-density.html | B | 修正权威源，待构建复核 | 半精养 360÷(15/1000)÷0.75=32000 尾/亩、总 160000 尾；存档错将克除以 100。半精养并非页面默认精养，已澄清 | 未提交 |
| tools/fun/coin-toss-streak.html | B | 修正权威源，待构建复核 | 实现统计正反同面；18 次序列最长连正 5，存档误写 20 次及 6 连；区分固定序列与多次试验概率 | 未提交 |
| tools/fun/color-guess.html | B | 修正权威源，待构建复核 | 实际四选一且色值严格相等、10 轮；存档误称输入色名及容差判分 | 未提交 |
| tools/fun/daily-riddle.html | B | 修正权威源，待构建复核 | 评分基础 180、提示每级扣 20、连击加分非倍数；示例 1 级提示/3 连击得 190 | 未提交 |
| tools/gardening/balcony-sunlight.html | B | 修正权威源，待构建复核 | 南向中层夏 8/冬 4 小时，西向低层夏 5 小时，高层加 0.5 小时 | 未提交 |
| tools/healthcare/antipyretic-dose.html | B | 修正标题生成数据，待构建复核 | 存档及当前构建标题截断 60 mg/kg 为 60 mg；调整介绍避免错误剂量出现在标题 | 未提交 |
| tools/hr/analysis-29.html | B | 修正权威源，待构建复核 | 平均在职人数 (220+200)/2，离职率 18/210=8.57% | 未提交 |
| tools/hr/assessor-training-hr.html | B | 修正权威源，待构建复核 | 实际仅评柯氏前两层，90/92/66.7 平均 82.9，非存档虚构加权 ROI | 未提交 |
| tools/hr/attendance-stats.html | B | 修正权威源，待构建复核 | 95.5% 存在迟到请假时评级封顶良好，而非优秀 | 未提交 |
| tools/hr/calc-81.html | B | 修正权威源，待构建复核 | 两岗位 5500 元、ROI 1354.55%；不自动统计过保人数，消除虚构自动分档 | 未提交 |
| tools/it/whitespace.html | B | 修正权威源，待构建复核 | 合并连续空格会压缩缩进；压成一行是独立选项 | 未提交 |
| tools/it/xml-validator.html | B | 保留主线 | 存档仅调整 deep-dive 标记位置和空行，无独有功能 | — |
| tools/leather/xueyunhoudukongzhi.html | B | 修正权威源与介绍，待构建复核 | 实际按刀痕间距分档、切除量独立计算，不预测厚度偏差或保证合格 | 未提交 |
| tools/life/generator-price.html | B | 修正权威源，待构建复核 | 金额按输入计算，数量不在 1–50 直接报错，非静默截断 | 未提交 |
| tools/marketing/email-subject-line-tester.html | 待 | 待处置 | — | — |
| tools/marketing/marketing-discount-rate.html | B | 修正权威源，待构建复核 | 页面只算单次折扣，不含优惠券 | 未提交 |
| tools/pediatrics/ddst-screening.html | 待 | 待处置 | — | — |
| tools/psychiatry/cdrisc-resilience.html | 待 | 待处置 | — | — |
| tools/realestate/generator-assessor.html | 待 | 待处置 | — | — |
| tools/rehabilitation/berg-balance-scale.html | 待 | 待处置 | — | — |
| tools/rehabilitation/fim-scale.html | 待 | 待处置 | — | — |
| tools/tcm-pharmacy/tcm-adr-assessment.html | 待 | 待处置 | — | — |
| tools/tcm-pharmacy/tcm-dosage.html | 待 | 待处置 | — | — |
| tools/urban/building-height.html | 待 | 待处置 | — | — |

**进度（2026-11-05 晚复核）**：表内 64 页状态分布 = B 整页回退 34 / A 修正保留 4 / B 修正权威源待复核 15 / 待处置 9 / 保留主线 1 / 修正标题生成数据 1。

- 集成 merge `72e4990707` 曾把 27 页 B 档错值覆盖回 master；已由 `4f6b06e4d2`（27 页整页回退 + `content_deepdive.json` 等 12 个源同步）与 `db8786ea78`（3 个 `zh-CN.intro` + 1 个 `_en_override.ed` 补齐，重跑 `_build.py` 幂等）修复，两次均 `All 229 quality gates passed.`。
- 抽验回退结果在 HEAD 仍有效：`dermatology/vasi-vitiligo` = 16.75、`obstetrics/fetal-weight-hadlock` = 2892 g、`edu/calc-4` = 95.0。
- **仍未收口**：15 条「修正权威源，待构建复核」需逐页确认是否已落盘并随 build 生效；9 条「待处置」需逐页判档。禁止据此宣布 84 页专项完成。
