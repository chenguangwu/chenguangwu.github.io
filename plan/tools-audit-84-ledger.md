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
| tools/construction/calc-1.html | 待 | 待处置 | — | — |
| tools/data/generator-35.html | 待 | 待处置 | — | — |
| tools/design/mesh-gradient.html | 待 | 待处置 | — | — |
| tools/design/pixel-art-generator.html | 待 | 待处置 | — | — |
| tools/ecommerce/report.html | 待 | 待处置 | — | — |
| tools/finance/generator-report-1.html | 待 | 待处置 | — | — |
| tools/fire-rescue/smoke-management.html | 待 | 待处置 | — | — |
| tools/fire-rescue/sprinkler-design.html | 待 | 待处置 | — | — |
| tools/fishery/drug-withdrawal-fish.html | 待 | 待处置 | — | — |
| tools/fishery/pond-desilting.html | 待 | 待处置 | — | — |
| tools/fishery/stocking-density.html | 待 | 待处置 | — | — |
| tools/fun/coin-toss-streak.html | 待 | 待处置 | — | — |
| tools/fun/color-guess.html | 待 | 待处置 | — | — |
| tools/fun/daily-riddle.html | 待 | 待处置 | — | — |
| tools/gardening/balcony-sunlight.html | 待 | 待处置 | — | — |
| tools/healthcare/antipyretic-dose.html | 待 | 待处置 | — | — |
| tools/hr/analysis-29.html | 待 | 待处置 | — | — |
| tools/hr/assessor-training-hr.html | 待 | 待处置 | — | — |
| tools/hr/attendance-stats.html | 待 | 待处置 | — | — |
| tools/hr/calc-81.html | 待 | 待处置 | — | — |
| tools/it/whitespace.html | 待 | 待处置 | — | — |
| tools/it/xml-validator.html | 待 | 待处置 | — | — |
| tools/leather/xueyunhoudukongzhi.html | 待 | 待处置 | — | — |
| tools/life/generator-price.html | 待 | 待处置 | — | — |
| tools/marketing/email-subject-line-tester.html | 待 | 待处置 | — | — |
| tools/marketing/marketing-discount-rate.html | 待 | 待处置 | — | — |
| tools/pediatrics/ddst-screening.html | 待 | 待处置 | — | — |
| tools/psychiatry/cdrisc-resilience.html | 待 | 待处置 | — | — |
| tools/realestate/generator-assessor.html | 待 | 待处置 | — | — |
| tools/rehabilitation/berg-balance-scale.html | 待 | 待处置 | — | — |
| tools/rehabilitation/fim-scale.html | 待 | 待处置 | — | — |
| tools/tcm-pharmacy/tcm-adr-assessment.html | 待 | 待处置 | — | — |
| tools/tcm-pharmacy/tcm-dosage.html | 待 | 待处置 | — | — |
| tools/urban/building-height.html | 待 | 待处置 | — | — |

进度：已处置 30 / 64（A 2 页、B 28 页），剩余 34 页。
