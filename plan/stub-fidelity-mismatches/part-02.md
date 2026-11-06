## 7. 弱用例与解析缺口工单

> 判据来自 `TB_DISCRIM_REPORT=1` 的逐条导出（fidelity 模式，207 个 verify 全跑）。
> 三类处置不同：**all_default** 改用例输入；**无法静态解析** 补 verify 侧桩（控件由页面脚本运行时生成）；
> **无注入** 本就不适用，无需处理。

### 7.1 all_default 弱用例工单（36 条）

| 行业 | slug | 用例 ref | 默认值 = 注入值 | 建议改成什么输入 |
|---|---|---|---|---|
| acupuncture | `acupuncture/needle-retention` | auto-restore | `age`=`adult` | 改用下拉另一项 `child`（默认 `adult`） |
| acupuncture | `acupuncture/needling-depth` | auto-restore | `bodyType`=`medium` | 改用下拉另一项 `thin`（默认 `medium`） |
| audio | `audio/audio-cut` | 结构性不可改造（保留 all_default，勿重复评估）： | `startInput`=`0`、`endInput`=`0` | 改用 `5`（默认 `0`，翻倍/避开默认） |
| beauty | `beauty/calc-2` | auto-restore | `tone`=`light` | 改用下拉另一项 `fair`（默认 `light`） |
| beauty | `beauty/skincare-routine` | auto-restore | `ageGroup`=`25` | 改用下拉另一项 `20`（默认 `25`） |
| chinese-cook | `chinese-cook/wok-heat` | auto-restore | `heat`=`zhong` | 改用下拉另一项 `wang`（默认 `zhong`） |
| cognition | `cognition/human-benchmark` | 结构性不可改造（保留 all_default，勿重复评估）： | `tArea`=`空` | 改用非空值（默认空串，注入空值等于没注入） |
| cognition | `cognition/time-perception` | auto-restore | `bSel`=`90` | 改用下拉另一项 `60`（默认 `90`） |
| dentistry | `dentistry/tongue-oral-health` | auto-restore | `color`=`normal` | 改用下拉另一项 `pale`（默认 `normal`） |
| dentistry | `dentistry/wisdom-tooth` | auto-restore | `winter`=`mesioangular` | 改用下拉另一项 `vertical`（默认 `mesioangular`） |
| design | `design/photo-print-size` | 冲印尺寸 = 像素 ÷ DPI × 2.54cm：4000/ | `pw`=`4000`、`ph`=`3000`、`dpi`=`300` | 改用 `8000`（默认 `4000`，翻倍/避开默认） |
| design | `design/spacing-scale` | 等比数列 size_i = round(base × rat | `baseSize`=`4`、`ratio`=`1.25`、`levels`=`10` | 改用 `8`（默认 `4`，翻倍/避开默认） |
| electromagnetism | `electromagnetism/free-space-impedance` | Z₀=√(μ₀/ε₀)=376.73 Ω（常数页，页面无有效 | `x`=`0` | 改用 `5`（默认 `0`，翻倍/避开默认） |
| forensic-medicine | `forensic-medicine/drowning-diatom` | auto-restore | `waterDiatom`=`medium` | 改用下拉另一项 `high`（默认 `medium`） |
| gastroenterology | `gastroenterology/esophageal-varices` | auto-restore | `size`=`2` | 改用下拉另一项 `1`（默认 `2`） |
| health | `health/protein-needs` | 蛋白质 = 体重 × 活动系数 = 65 × 1.4 = 9 | `weight`=`65`、`age`=`30`、`activity`=`1.4` | 改用 `130`（默认 `65`，翻倍/避开默认） |
| health | `health/calc-2` | 总分 = 时长20(7–9h) + 潜伏期10 + 觉醒10 | `duration`=`7`、`latency`=`10`、`wakings`=`10`、`depth`=`15`、`alertness`=`15`、`breathing`=`0` | 改用 `14`（默认 `7`，翻倍/避开默认） |
| it | `it/calc-2` | format(255,'X') = FF | `numInput`=`255`、`fromBase`=`10` | 改用 `510`（默认 `255`，翻倍/避开默认） |
| it | `it/vector-dot-product` | 自动补强（B类零用例）：注入非默认输入{"dim":"3"} | `dim`=`3` | 改用下拉另一项 `2`（默认 `3`） |
| it | `it/vector-magnitude` | 自动补强（B类零用例）：注入非默认输入{"dim":"3"} | `dim`=`3` | 改用下拉另一项 `2`（默认 `3`） |
| kids | `kids/stroke-order` | auto-restore | `charInput`=`永`、`speedSel`=`900` | 改用 `永-x` 或语义不同的合法值（默认 `永`） |
| language | `language/idiom-solitaire` | auto-restore | `timeLimit`=`20` | 改用下拉另一项 `15`（默认 `20`） |
| mechanical | `mechanical/spring-rate` |  | `d`=`5`、`D`=`30`、`n`=`6`、`G`=`79` | 改用 `10`（默认 `5`，翻倍/避开默认） |
| travel | `travel/luggage-size` | auto-restore | `size`=`20` | 改用下拉另一项 `18`（默认 `20`） |
| music | `music/web-tuner` | auto-restore | `refFreq`=`440` | 改用下拉另一项 `432`（默认 `440`） |
| office | `office/mindmap` | 结构性不可改造（保留 all_default，勿重复评估）： | `editor`=`空` | 改用非空值（默认空串，注入空值等于没注入） |
| ophthalmology | `ophthalmology/amblyopia-stereopsis` | auto-restore | `age`=`5`、`stereoLevel`=`60` | 改用 `10`（默认 `5`，翻倍/避开默认） |
| pet | `pet/training-planner` | auto-restore | `age`=`junior` | 改用下拉另一项 `puppy`（默认 `junior`） |
| rheumatology | `rheumatology/anca-classification` | auto-restore | `iif`=`canca` | 改用下拉另一项 `neg`（默认 `canca`） |
| rheumatology | `rheumatology/behcet-hla` | auto-restore | `age`=`middle` | 改用下拉另一项 `young`（默认 `middle`） |
| rheumatology | `rheumatology/ssa-ssb` | auto-restore | `ssa`=`ro60` | 改用下拉另一项 `neg`（默认 `ro60`） |
| science | `science/convert-power` | 1 N = 0.2248089 lbf（1 lbf = 4. | `val`=`1`、`from`=`N`、`to`=`lbf` | 改用 `2`（默认 `1`，翻倍/避开默认） |
| startup | `startup/equity-calculator` | auto-restore | `w_idea`=`3`、`w_money`=`1`、`w_time`=`2`、`w_res`=`2`、`pool`=`15`、`mode`=`weighted` | 改用 `6`（默认 `3`，翻倍/避开默认） |
| stats | `stats/sample-size` | auto-restore | `e`=`5`、`p`=`0.5`、`n`=`0`、`conf`=`0.95` | 改用 `10`（默认 `5`，翻倍/避开默认） |
| text | `text/convert-6` | auto-restore | `val`=`Hello World`、`to`=`lower` | 改用 `Hello World-x` 或语义不同的合法值（默认 `Hello World |
| wedding | `wedding/wedding-banquet` | 主桌 ceil(120/10)=12；备桌 mid=2；合计 | `guests`=`120`、`type`=`round10`、`backup`=`mid` | 改用 `240`（默认 `120`，翻倍/避开默认） |

**按行业**：it 3、rheumatology 3、acupuncture 2、beauty 2、cognition 2、dentistry 2、design 2、health 2、audio 1、chinese-cook 1、electromagnetism 1、forensic-medicine 1、gastroenterology 1、kids 1、language 1、mechanical 1、travel 1、music 1、office 1、ophthalmology 1、pet 1、science 1、startup 1、stats 1、text 1、wedding 1。

### 7.2 无法静态解析（40 条，页面控件运行时生成）

| 行业 | slug | 用例 ref | 解析不到的 id |
|---|---|---|---|
| chemical | `chemical/checker-15` | 去默认化（原 expect「0/10」＝全零默认态即命中）： | `m0_0`、`m0_1`、`m0_2`、`m0_3`、`m0_4`、`m1_0`、`m1_1`、`m1_2`、`m1_3`、`m1_4`、`m1_5`、`m2_0`、`m2_1`、`m2_2`、`m2_3`、`m2_4` |
| cleaning | `cleaning/checker-10` | 去默认化（16 项打分全部非默认）：地面 4 项全 5 →  | `a0_0`、`a0_1`、`a0_2`、`a0_3`、`a1_0`、`a1_1`、`a1_2`、`a1_3`、`a1_4`、`a2_0`、`a2_1`、`a2_2`、`a3_0`、`a3_1`、`a3_2`、`a3_3` |
| cleaning | `cleaning/checker-9` | 去默认化（15 项评级全部非默认）：一、SOP 5 项全「已 | `m0_0`、`m0_1`、`m0_2`、`m0_3`、`m0_4`、`m1_0`、`m1_1`、`m1_2`、`m1_3`、`m1_4`、`m2_0`、`m2_1`、`m2_2`、`m2_3`、`m2_4` |
| clinical-lab | `clinical-lab/urinalysis-interpretation` | LEU 3+(500) 且 NIT 阳性 → 满足「(leu | `ua_leu`、`ua_nit`、`ua_pro`、`ua_glu`、`ua_ket`、`ua_ery`、`ua_bil`、`ua_ubg`、`ua_vc` |
| decor | `decor/curtain-fabric` | 2026-10-27 新增「遮光+纱帘双层组合估算」：注入杆 | `dblRod`、`dblH`、`dblFullA`、`dblFabA`、`dblFullB`、`dblFabB` |
| dentistry | `dentistry/gingival-index` | 6 牙 × 4 位点全部显式注入（动态 id `<tooth | `t16_0`、`t16_1`、`t16_2`、`t16_3`、`t16_bop`、`t21_0`、`t21_1`、`t21_2`、`t21_3`、`t21_bop`、`t24_0`、`t24_1`、`t24_2`、`t24_3`、`t24_bop`、`t36_0`、`t36_1`、`t36_2`、`t36_3`、`t36_bop`、`t41_0`、`t41_1`、`t41_2`、`t41_3`、`t41_bop`、`t44_0`、`t44_1`、`t44_2`、`t44_3`、`t44_bop` |
| dentistry | `dentistry/rater-risk-2` | 7 维（exp/ms/diet/plaque/fluorid | `d_exp`、`d_ms`、`d_diet`、`d_plaque`、`d_fluoride`、`d_flow`、`d_buffer` |
| electrical | `electrical/load-curve` | auto-restore | `h'+h+'` |
| endocrinology | `endocrinology/catecholamine-test` | 注入血浆游离 MN/NMN（默认页签 plasma）→ 结果 | `mn`、`nmn` |
| fitness | `fitness/bodyfat-caliper` | 注入非默认（默认 gender=male/sites=3 但 | `site_chest`、`site_abdomen`、`site_thigh` |
| forensic-medicine | `forensic-medicine/bone-age-estimation` | auto-restore | `femurLen`、`crl`、`carpalNum`、`metaNum`、`radiusGrade`、`metaGrade`、`phalGrade` |
| futures | `futures/option-greeks` | auto-restore | `marketPrice` |
| hydraulic | `hydraulic/pressure-drop` | v0=1.6,v1=137 → 计算壁厚 δ=1.6×200 | `v0`、`v1` |
| hydraulic | `hydraulic/qudao-buchong-buyu-liusu` | v0=0.8,v1=0.0005 → 谢才 v=(1/0.0 | `v0`、`v1` |
| hydraulic | `hydraulic/daohongxi-shuitousunshi-maishen` | v0=2.0,v1=50 → 沿程损失 h_f=0.025× | `v0`、`v1` |
| it | `it/vector-dot-product` | 注入非默认(默认 2D a=(1,0)/b=(0,1)点积  | `a0`、`a1`、`b0`、`b1` |
| legal | `legal/court-fee` | 财产案件10万：100000×2.5%−200=2300（分 | `hasPropertySplit`、`simplified` |
| library | `library/citation-format` | auto-restore | `edition`、`place`、`publisher`、`year`、`pages`、`journal`、`volissue`、`degree`、`school`、`conf`、`stdno`、`patno`、`paper`、`date`、`url`、`cited` |
| project | `project/analysis-28` | auto-restore | `sn'+idx+'` |
| property | `property/cycle-elevator` | auto-restore | `logDate_'+el.id+'` |
| psychiatry | `psychiatry/assessor-risk-5` | C-SSRS 自杀意念第3项=是（其余=否）→ maxIde | `ide0`、`ide1`、`ide2`、`ide3`、`ide4`、`beh0`、`beh1`、`beh2` |
| psychiatry | `psychiatry/calc-1` | PHQ-9 九项=3,3,2,2,1,2,2,1,2 → 总 | `q0`、`q1`、`q2`、`q3`、`q4`、`q5`、`q6`、`q7`、`q8` |
| psychiatry | `psychiatry/mmpi2-personality` | MMPI-2 十量表 T 分（动态 id sc0..sc9  | `sc0`、`sc1` |
| psychiatry | `psychiatry/rater-23` | LSAS 24 项（表演型 13 + 社交互动型 11，动态 | `f0`、`f1`、`f2`、`f3`、`f4`、`f5`、`f6`、`f7`、`f8`、`f9`、`f10`、`f11`、`f12`、`f13`、`f14`、`f15`、`f16`、`f17`、`f18`、`f19`、`f20`、`f21`、`f22`、`f23`、`a0`、`a1`、`a2`、`a3`、`a4`、`a5`、`a6`、`a7`、`a8`、`a9`、`a10`、`a11`、`a12`、`a13`、`a14`、`a15`、`a16`、`a17`、`a18`、`a19`、`a20`、`a21`、`a22`、`a23` |
| psychiatry | `psychiatry/rater-24` | CD-RISC 25 项（动态 id q0..q24 由 b | `q0`、`q1`、`q2`、`q3`、`q4`、`q5`、`q6`、`q7`、`q8`、`q9`、`q10`、`q11`、`q12`、`q13`、`q14`、`q15`、`q16`、`q17`、`q18`、`q19`、`q20`、`q21`、`q22`、`q23`、`q24` |
| psychiatry | `psychiatry/self-assess-4` | ASRS-v1.1 六项（动态 id q0..q5，posi | `q0`、`q1`、`q2`、`q3`、`q4`、`q5` |
| psychology | `psychology/attachment-style-test` | auto-restore | `at' + i + '_' + l.v + '` |
| psychology | `psychology/calc-12` | inputs 写 10 个滑杆（id=s-<维度键>）：li | `s-life`、`s-health`、`s-relation`、`s-work`、`s-finance`、`s-growth`、`s-leisure`、`s-safety`、`s-self`、`s-mood` |
| psychology | `psychology/holland-career-test` | auto-restore | `hl' + i + '_' + val + '` |
| pulmonology | `pulmonology/copd-cat` | auto-restore | `q0`、`q1`、`q2`、`q3`、`q4`、`q5`、`q6`、`q7` |
| pulmonology | `pulmonology/rater-13` | auto-restore | `q0`、`q1`、`q2`、`q3`、`q4`、`q5`、`q6` |
| pulmonology | `pulmonology/self-assess-3` | auto-restore | `q0`、`q1`、`q2`、`q3`、`q4`、`q5` |
| rehabilitation | `rehabilitation/asia-impairment-scale` | 门诊记录：全量注入 28 皮节×4 位点（sens_*_lt | `sens_C2_lt_l`、`sens_C2_lt_r`、`sens_C2_pp_l`、`sens_C2_pp_r`、`sens_C3_lt_l`、`sens_C3_lt_r`、`sens_C3_pp_l`、`sens_C3_pp_r`、`sens_C4_lt_l`、`sens_C4_lt_r`、`sens_C4_pp_l`、`sens_C4_pp_r`、`sens_C5_lt_l`、`sens_C5_lt_r`、`sens_C5_pp_l`、`sens_C5_pp_r`、`sens_C6_lt_l`、`sens_C6_lt_r`、`sens_C6_pp_l`、`sens_C6_pp_r`、`sens_C7_lt_l`、`sens_C7_lt_r`、`sens_C7_pp_l`、`sens_C7_pp_r`、`sens_C8_lt_l`、`sens_C8_lt_r`、`sens_C8_pp_l`、`sens_C8_pp_r`、`sens_T1_lt_l`、`sens_T1_lt_r`、`sens_T1_pp_l`、`sens_T1_pp_r`、`sens_T2_lt_l`、`sens_T2_lt_r`、`sens_T2_pp_l`、`sens_T2_pp_r`、`sens_T3_lt_l`、`sens_T3_lt_r`、`sens_T3_pp_l`、`sens_T3_pp_r`、`sens_T4_lt_l`、`sens_T4_lt_r`、`sens_T4_pp_l`、`sens_T4_pp_r`、`sens_T5_lt_l`、`sens_T5_lt_r`、`sens_T5_pp_l`、`sens_T5_pp_r`、`sens_T6_lt_l`、`sens_T6_lt_r`、`sens_T6_pp_l`、`sens_T6_pp_r`、`sens_T7_lt_l`、`sens_T7_lt_r`、`sens_T7_pp_l`、`sens_T7_pp_r`、`sens_T8_lt_l`、`sens_T8_lt_r`、`sens_T8_pp_l`、`sens_T8_pp_r`、`sens_T9_lt_l`、`sens_T9_lt_r`、`sens_T9_pp_l`、`sens_T9_pp_r`、`sens_T10_lt_l`、`sens_T10_lt_r`、`sens_T10_pp_l`、`sens_T10_pp_r`、`sens_T11_lt_l`、`sens_T11_lt_r`、`sens_T11_pp_l`、`sens_T11_pp_r`、`sens_T12_lt_l`、`sens_T12_lt_r`、`sens_T12_pp_l`、`sens_T12_pp_r`、`sens_L1_lt_l`、`sens_L1_lt_r`、`sens_L1_pp_l`、`sens_L1_pp_r`、`sens_L2_lt_l`、`sens_L2_lt_r`、`sens_L2_pp_l`、`sens_L2_pp_r`、`sens_L3_lt_l`、`sens_L3_lt_r`、`sens_L3_pp_l`、`sens_L3_pp_r`、`sens_L4_lt_l`、`sens_L4_lt_r`、`sens_L4_pp_l`、`sens_L4_pp_r`、`sens_L5_lt_l`、`sens_L5_lt_r`、`sens_L5_pp_l`、`sens_L5_pp_r`、`sens_S1_lt_l`、`sens_S1_lt_r`、`sens_S1_pp_l`、`sens_S1_pp_r`、`sens_S2_lt_l`、`sens_S2_lt_r`、`sens_S2_pp_l`、`sens_S2_pp_r`、`sens_S3_lt_l`、`sens_S3_lt_r`、`sens_S3_pp_l`、`sens_S3_pp_r`、`sens_S4-S5_lt_l`、`sens_S4-S5_lt_r`、`sens_S4-S5_pp_l`、`sens_S4-S5_pp_r`、`motor_0_l`、`motor_0_r`、`motor_1_l`、`motor_1_r`、`motor_2_l`、`motor_2_r`、`motor_3_l`、`motor_3_r`、`motor_4_l`、`motor_4_r`、`motor_5_l`、`motor_5_r`、`motor_6_l`、`motor_6_r`、`motor_7_l`、`motor_7_r`、`motor_8_l`、`motor_8_r`、`motor_9_l`、`motor_9_r` |
| rheumatology | `rheumatology/assessor-10` | 各域取本域最高档：全身/腺体/生化只有 0–2 档，其余取  | `d0`、`d1`、`d2`、`d3`、`d4`、`d5`、`d6`、`d7`、`d8`、`d9`、`d10`、`d11` |
| rheumatology | `rheumatology/assessor-10` | 切点回归：腺体低 2×2=4 + 生化低 1×1=1 = 5 | `d2`、`d11` |
| rheumatology | `rheumatology/guguanjieyan-womac-zhishu` | auto-restore | `' + name + '_' + v + '` |
| rheumatology | `rheumatology/womac` | WOMAC：疼痛 Σ14/20、僵硬 Σ4/8、功能 Σ34 | `p0`、`p1`、`p2`、`p3`、`p4`、`s0`、`s1`、`f0`、`f1`、`f2`、`f3`、`f4`、`f5`、`f6`、`f7`、`f8`、`f9`、`f10`、`f11`、`f12`、`f13`、`f14`、`f15`、`f16` |
| surveying | `surveying/calc-1` | SV-5 新增：注入 4 测段高差 Σh=1.256+2.3 | `dh-1`、`dh-2`、`dh-3`、`dh-4`、`fc-1`、`fc-2`、`fc-3`、`fc-4` |
| urology | `urology/calc-1` | fix broken template: q0-6=3→总分 | `q0`、`q1`、`q2`、`q3`、`q4`、`q5`、`q6` |
| urology | `urology/iief5-score` | fix broken template: q0-4=3→总分 | `q0`、`q1`、`q2`、`q3`、`q4` |

**按行业**：psychiatry 6、rheumatology 4、hydraulic 3、psychology 3、pulmonology 3、cleaning 2、dentistry 2、urology 2、chemical 1、clinical-lab 1、decor 1、electrical 1、endocrinology 1、fitness 1、forensic-medicine 1、futures 1、it 1、legal 1、library 1、project 1、property 1、rehabilitation 1、surveying 1。

### 7.3 无注入用例（10 条，本来就不适用判别力）

| 行业 | slug | 用例 ref |
|---|---|---|
| admin | `admin/detector-time` | 结构性不可注入（沿用 tcm-diagnosis/etiology-tree 的 |
| ceramics | `ceramics/glaze-temp` | 结构性不可注入（2026-10-10 复核，原 ref 为 auto-resto |
| chess | `chess/xiangqi-endgame` | 结构性不可注入（沿用 tcm-diagnosis/etiology-tree 口 |
| film | `film/color-grading` | 结构性不可注入（2026-09-26 复核，原 ref 为 auto-resto |
| gardening2 | `gardening2/pest-control` | 结构性不可注入（2026-09-26 复核，原 ref 为 auto-resto |
| image | `image/nine-grid-cutter` | 结构性不可注入（2026-10-10 复核，原 ref 为 auto-resto |
| science | `science/physics-constants` | auto-restore(default)；**2026-09-26 复核判死（ |
| music | `music/ear-trainer` | auto-restore(default)；**2026-09-26 复核判死（ |
| paper | `paper/paper-grade` | 结构性不可注入（2026-09-26 复核，原 ref 为 auto-resto |
| tcm-diagnosis | `tcm-diagnosis/etiology-tree` | 结构性不可注入：页面仅 treeContainer 一个容器，节点由 build |
