#!/usr/bin/env node
/**
 * 第 40 道门禁：obstetrics 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除：
 *   - gestational / gestational-age：计算依赖 new Date()（今日孕周），stub 无法还原 → 无验证意义；
 *   - 其余 16 个计算类页面除本表 13 个外，多为纯展示/模板类或单位换算，已并入对应确定性函数。
 * 用法: node scripts/verify_obstetrics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "obstetrics/afi-normal",
    inputs: { ruq: "2", luq: "2", rlq: "2", llq: "2" },
    expect: ["8.0", "偏少"],
    ref: "AFI=2+2+2+2=8.0cm，落入 ≤8 → 偏少(临界)（默认示例=12→正常，避开）" },

  { slug: "obstetrics/ectopic-hcg",
    inputs: { hcg1: "1000", hcg2: "2000", interval: "48" },
    expect: ["+100.0%", "48.0小时"],
    ref: "变化率=(2000-1000)/1000×100=+100.0%；DT=48×0.693/ln2=48.0h（默认示例值不同，避开）" },

  { slug: "obstetrics/fetal-weight-hadlock",
    inputs: { bpd: "9", hc: "32", ac: "30", fl: "7" },
    expect: ["2562", "2.56", "正常体重"],
    ref: "Hadlock四参数 log10w=1.3596-0.00386·30·7+0.0064·32+0.00061·9·30+0.0424·30+0.174·7=3.4085→EFW=10^3.4085=2562g=2.56kg（默认空→请至少输入一个参数，避开）" },

  { slug: "obstetrics/fetal-weight-hadlock",
    inputs: { bpd: "9.2", hc: "", ac: "33", fl: "7.2" },
    expect: ["Shepard两参数(BPD+AC)修正", "3109"],
    ref: "缺 HC、保留 BPD+AC+FL ⇒ 退化 Shepard 两参数（该式原单位为 kg）：log10=-1.7492+0.166·9.2+0.046·33-2.646·(9.2·33)/1000=0.492674→10^=3.1094kg→×1000=3109g。"
       + "默认态（8.8/32/30.5/6.6 四参数）走 Hadlock 四参数、不含该串 ⇒ 强判别。此前该分支误用 +1.7492 且未换算 g（显示约 9.8kg），已修正。" },

  { slug: "obstetrics/fetal-weight-hadlock",
    inputs: { bpd: "", hc: "", ac: "33", fl: "7.2" },
    expect: ["Hadlock两参数(AC+FL)", "3102"],
    ref: "仅 AC+FL ⇒ Hadlock 两参数：log10=1.304+0.05281·33+0.1938·7.2-0.004·33·7.2=3.49169→EFW=10^3.49169=3102g。"
       + "默认态走四参数，不含该串；单参数分支也不会命中 3102 ⇒ 强判别。" },

  { slug: "obstetrics/fetal-weight-hadlock",
    inputs: { sfh: "30", ac2: "90" },
    expect: ["810", "2790"],
    ref: "宫高腹围页签：宫高×腹围×0.3=30·90·0.3=810g；Johnson 法 (30−12)·155=2790g。"
       + "默认态（32/95）为 912g / 3100g，与本例两值均不同 ⇒ 强判别。" },

  { slug: "obstetrics/postpartum-hemorrhage",
    inputs: { wetWeight: "2000", dryWeight: "1000", preWeight: "60", hr: "100", sbp: "100" },
    expect: ["952", "1.00"],
    ref: "失血量=(2000-1000)/1.05=952mL（calcWeight）；SI=100/100=1.00（calcShock→轻度休克）（默认空→返回，避开）" },

  { slug: "obstetrics/preeclampsia-prediction",
    inputs: { sflt: "6000", pigf: "50", onset: "late" },
    expect: ["120.00", "确诊子痫前期"],
    ref: "比值=6000/50=120.00；晚发确诊界值110，120≥110→确诊（默认空→请输入有效数值，避开）" },

  { slug: "obstetrics/ovarian-reserve",
    inputs: { amh: "7.0", fsh: "6", e2: "35", afc: "12", age: "30" },
    expect: ["7.00", "卵巢高反应(可能PCOS)"],
    ref: "amh=7.0≥6→amhLevel极高且score-=1→总分-1；其余0分→amh>6分支→卵巢高反应(可能PCOS)；AMH显示7.00（默认/示例=0.6→DOR、2.5→正常，均不命中，避开） ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。" },

  { slug: "obstetrics/endometrial-thickness",
    inputs: { cycleDay: "20", thickness: "5" },
    expect: ["偏薄"],
    ref: "育龄期 D20→分泌期(10–14mm)，实测5mm<minT-1=9→偏薄（默认周期类型非绝经后，避开绝经后分支）" },

  { slug: "obstetrics/fetal-movement-count",
    inputs: { morn: "1", noon: "1", even: "1", h1: "1" },
    expect: ["异常(减少)"],
    ref: "12h胎动=(1+1+1)×4=12<20→异常(减少)（避开 '12' 命中默认标签 '12小时胎动'；默认示例=5/4/6/6→36正常）" },

  { slug: "obstetrics/ctg-fhr",
    inputs: { baseline: "105", variability: "10", accel: "present", decel: "none", contractions: "4" },
    expect: ["可疑", "105"],
    ref: "基线105→可疑(100–110)；变异10→正常；加速present；无减速；宫缩4→正常；abnCount=0,susCount=1→可疑CTG（默认140/10→正常、示例95/3/late→异常，均不命中，避开） ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。" },

  { slug: "obstetrics/heart-rate",
    inputs: { baseline: "95", variability: "10", accel: "2", decel: "none" },
    expect: ["病理性 CTG（Pathological）"],
    ref: "基线95<100→病理性（其余正常：变异10、加速2、无减速）；原用例 decel=late 是 select 无默认值，注入失败仍留 late → 结果恒为病理性 → 逃生项" },

  { slug: "obstetrics/yangshuizhishu-afi-zhengchangfanwei",
    inputs: { q1: "2", q2: "3", q3: "3", q4: "3" },
    expect: ["11.0"],
    ref: "AFI=2+3+3+3=11.0cm→羊水量正常（默认4/3/3/3=13.0，避开）" },

  { slug: "obstetrics/down-screening",
    inputs: { age: "28", afp: "0.75", bhcg: "1.7", ue3: "0.75" },
    expect: ["1/90"],
    ref: "年龄先验1/(1300·e^-0.18)=1/1085.9；afpLR(0.75<0.8→3)×hcgLR(1.7>1.5→2)×ue3LR(0.75<0.8→2)=12；调整后→riskN=round(1/(12/1085.9))=90→1/90,<1/270高风险（默认=25/1/1/1→1/1300；预设loadHigh=38/0.65/2.8/0.65→1/25，避开）" },

  { slug: "obstetrics/calc-risk",
    inputs: { age: "40", weight: "60", ga: "16", afp: "0.6", bhCG: "2.5" },
    expect: ["1:28", "高风险"],
    ref: "先验1/100×afpLR(0.6→1.6)×hcgLR(2.5→2.2)=0.0352→1/28；≥1/270→高风险（weight/ga仅作非空校验，默认空→请完整输入，避开）" },
  // ── §7.4 零用例加固：obstetrics 确定性数值页（注入非默认 + harness 实测锚）──
  { slug: "obstetrics/pearl-index",
    inputs: { preg: "5", wm: "15000" },
    expect: ["0.40 Pearl指数", "(=1250 妇女年)", "0.4 人意外妊娠"],
    ref: "注入非默认(默认 2/12000)：Pearl 指数 = 意外妊娠数×1200 / 使用妇女月 = 5×1200/15000 = 0.40（/100 妇女年 ⇒ 1 年失败率 0.40%，评级「极高效」）；15000 月 = 1250 妇女年。默认态 0.20/(1000 妇女年)/0.2 人 均不命中。" },
  { slug: "obstetrics/labor-curve",
    inputs: { dilation: "9", hours: "14" },
    expect: ["14 h 临产时长", "9 cm 宫口扩张"],
    ref: "注入非默认(默认 dilation=8/hours=10)：初产妇按 ACOG/WHO（活跃期 6 cm 起）⇒ 9 cm 处判定为活跃期；临产 14 h、潜伏期上限 20 h、扩张速率 ≥1 cm/h ⇒ 产程进展正常。⚠ 「活跃期」「产程进展正常」等结论文案在默认态同样成立（8 cm/10 h 也判正常）⇒ 不可作锚，只取含注入值的两串。" },
  { slug: "obstetrics/biyun-pearlzhishu-shibailv",
    inputs: { women: "150", months: "1800", pregnancies: "12" },
    expect: ["0.05 Pearl 指数", "12 意外妊娠数", "150 使用人数"],
    ref: "注入非默认(默认 100/1200/6)：按页面 Pearl 指数口径 ⇒ 0.05；并回显使用人数 150、总使用月数 1800、意外妊娠数 12。默认态 0.10/100/6 均不命中。" },
  { slug: "obstetrics/calc-50",
    inputs: { height: "165", weight: "78", preWeight: "62", hctBefore: "34", hctAfter: "27" },
    expect: ["4363 估算血容量（mL）", "898 估算失血量（mL）", "20.6%"],
    ref: "注入非默认(默认 160/70/58/36/28)：估算血容量 ≈ 4,363 mL；按分娩前后血细胞比容差（34 → 27）与体重差 ⇒ 估算失血量 ≈ 898 mL，占血容量 20.6% ⇒ PPH 分级「PPH（500~1500 mL）」。默认态 3,994 mL/… 均不命中。" },

  // ── 零用例收敛（2026-10-09）：obstetrics 8 页中 4 页可收敛 ──
  { slug: "obstetrics/bishop-score",
    inputs: { dilation: "3", effacement: "3", station: "3", position: "2", consistency: "2" },
    expect: ["13/13", "Bishop 13分", "宫口扩张：3分", "宫颈质地：2分"],
    ref: "注入五项 Bishop 项（默认 2/2/2/1/1 ⇒ 8 分）。独立复算：宫口扩张 3cm=3、宫颈消退 3cm=3、胎头位置 station=3 得 3 分、宫颈位置 2、宫颈质地 2 ⇒ 总分 3+3+3+2+2 = 13。原锚「11/13」与「可直接用缩宫素引产」均为页面静态文案（示例/阈值表，默认态即含）⇒ 逃生；改锚动态结果「13/13」「Bishop 13分」与明细「宫口扩张：3分」「宫颈质地：2分」。默认 8 分 ⇒「8/13」「Bishop 8分」「宫口扩张：2分」「宫颈质地：1分」，四条均不命中。" },
  { slug: "obstetrics/placenta-grading",
    inputs: { gw: "30", grade: "3" },
    expect: ["孕30周出现III级", "30周 当前孕周"],
    ref: "注入孕周 30 周 + Grannum 3 级（默认 36 周 + 2 级）。独立复算：g==='3' && gw<36 ⇒ 触发过早老化分支，输出「孕30周出现III级，提示胎盘过早老化…」；结果卡片结构串「30周 当前孕周」。原锚「II级(成熟)」「32–36周」「绒毛板切迹…」「基本相符」均为注入默认 2 级即可命中的静态/分级文案 ⇒ 逃生。默认 36 周 + 2 级 ⇒「36周 当前孕周」且无过早老化提示，两条均不命中。" },
  { slug: "obstetrics/rater-26",
    inputs: { k1: "3", k2: "2", k3: "3", k4: "1", k5: "2", k6: "3", k7: "1", k8: "2", k9: "3", k10: "1", k11: "2" },
    expect: ["Kupperman总分： 38", "症状原始分23", "更年期症状重度", "潮热出汗 ×4 3分 12分", "阴道干涩 ×1 2分 2分"],
    ref: "注入 11 项症状评分（默认全 0）。独立复算（页面 Kupperman 权重表）：潮热出汗 3×4=12、感觉异常 2×2=4、失眠 3×2=6、易激动 1×2=2、抑郁疑心 2×1=2、眩晕 3×1=3、疲乏 1×1=1、骨关节痛 2×1=2、头痛 3×1=3、心悸 1×1=1、阴道干涩 2×1=2 ⇒ 加权总分 12+4+6+2+2+3+1+2+3+1+2 = 38；原始分 3+2+3+1+2+3+1+2+3+1+2 = 23。总分 ≥31 判「重度」（页面阈值表）⇒ 建议就诊妇科内分泌评估激素替代。默认态 0 分输出「更年期症状轻微，建议生活调理」，五条均不命中。" },
  { slug: "obstetrics/due-date",
    inputs: { cycle: "30" },
    expect: ["2024-11-18", "Naegele预产期：2024-11-18 (LMP + 280天 + 2天)", "月经周期：30天", "156 距预产期(天)"],
    ref: "注入月经周期 30 天（默认 28）。harness 的 new Date() 冻结在 2024-06-15（verify_it_calc.js FIXED_NOW），页面 init 的 loadExample() 把 LMP 设为 今天−126 天 = 2024-02-10，故今日=2024-06-15 恒定 ⇒ 日期型结果在门禁中完全确定。独立复算：周期修正量 = 30 − 28 = +2 天；Naegele EDD = LMP + 280 + 修正 = 2024-02-10 + 282 天 = 2024-11-18；距预产期天数 = 2024-11-18 − 2024-06-15 = 156 天。⚠ 不注入 lmpDate：判别器会点『加载示例』把 lmpDate 重设为 2024-02-10（= 今天−126），若用默认 28 天则 EDD 恒为 2024-11-16 无论注入是否失败 ⇒ 假逃生项（判别器实测 via=loadExample 报出）。改用周期作注入点，EDD 随周期线性平移，翻转可靠。" },
  { slug: "obstetrics/gdm-ogtt",
    inputs: { fpg: "7.5", h1: "11.0", h2: "9.5" },
    expect: ["糖尿病合并妊娠(孕前糖尿病)", "血糖达到糖尿病诊断标准(空腹≥7.0或2h≥11.1)，应按孕前糖尿病管理，建议内分泌科会诊。"],
    ref: "注入非默认（HTML 默认 5.3/9.8/8.2；页面 init 调 loadGDM 载入 5.3/10.5/8.2 样例）：fpg=7.5 ≥ 7.0 ⇒ isPreDM 优先分支 ⇒ 诊断「糖尿病合并妊娠(孕前糖尿病)」，而非 GDM 分支。⚠ 该页有 loadNormal()（4.5/8.0/7.0 → 糖耐量正常）与 loadGDM()（→ GDM）两个样例载入函数，harness step-3 兜底会依次调用 ⇒ 若 expect 取「糖耐量正常」或「妊娠糖尿病(GDM)」会被兜底调出的同态命中 ⇒ 假逃生项；取两者都不产生的孕前糖尿病分支才安全。" },
  { slug: "obstetrics/taipanchengshudu-grannumfenji",
    inputs: { gaWeek: "38", chorion: "3", substance: "3", basal: "3" },
    expect: ["Grannum III 级", "提示胎盘老化；37 周后出现多属正常"],
    ref: "注入非默认（默认 gaWeek=32 且三项分级 select 均取首项 0）：Grannum 三项评分合计 = 3+3+3 = 9，"
      + "scoreToGrade 档位 ≤8 ⇒ 2 级、>8 ⇒ 3 级（修复前档位 ≤9 仍返 2，导致 3/3/3 与预设「III 级 38 周」都算成 II 级）；"
      + "对应描述「胎盘老化…37 周后出现多属正常」。默认态合计 0 ⇒ 0 级（Grannum 0 级 / 胎盘未成熟），两串均不出现。"
      + "38 周 + III 级不触发 concern（仅 grade===3 && ga<37 提示早熟）。" },
  { slug: "obstetrics/gestational-age",
    inputs: { lmpDate: "2024-01-01", cycleLen: "30" },
    expect: ["23+5 当前孕周", "2024-10-09 预产期(EDD)"],
    ref: "注入 LMP=2024-01-01 + 周期 30 天（默认 LMP 由 init 填为 今天−140 天、周期 28）。harness now 冻结 2024-06-15 ⇒ 结果完全确定：周期修正 = 30−28 = +2 天；EDD = LMP + 280 + 2 = 2024-01-01 + 282 天 = 2024-10-09（2024 闰年：1月30+2月29+3月31+4月30+5月31+6月30+7月31+8月31+9月30=273，余 9 天 ⇒ 10月9日）；距末次月经 = 2024-06-15 − 2024-01-01 = 166 日历天 = 23 周+5 天（页面输出一致）。"
       + "⚠ 原断言「23+4」是旧实现按毫秒差 + Math.floor 计日、跨夏令时被 1 小时蚀掉一天的产物；改为按日历日差（Date.UTC 组件相减）后应为 23+5。LMP 必须早于冻结 today（2024-06-15），晚于则页面报『末次月经日期不能晚于今天』。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "20", usType: "bpd" },
    expect: ["13+1 B超孕周", "2026-12-06 校正预产期"],
    ref: "Hadlock 1984 BPD：BPD 20mm=2.0cm ⇒ GA=9.54+1.482×2.0+0.1676×2.0²=13.1744 周=13+1；扫描日 2026-06-01 ⇒ EDD=+280−round(92.22)=+188 天=2026-12-06。旧线性近似 (2.11+2.0×1.942)×7=41.3 天=5+6 周、EDD 2027-02-05，两串均不命中。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "45", usType: "bpd" },
    expect: ["19+4 B超孕周", "2026-10-22 校正预产期"],
    ref: "Hadlock 1984 BPD：45mm=4.5cm ⇒ GA=9.54+1.482×4.5+0.1676×4.5²=19.6029 周=19+4；EDD=2026-06-01+(280−round(137.22))=+143 天=2026-10-22。旧线性近似 (2.11+4.5×1.942)×7=75.9 天=10+6 周、EDD 2026-12-22（差 2 个月），两串均不命中。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "78", usType: "bpd" },
    expect: ["31+2 B超孕周", "2026-08-01 校正预产期"],
    ref: "Hadlock 1984 BPD：78mm=7.8cm ⇒ GA=9.54+1.482×7.8+0.1676×7.8²=31.2964 周=31+2；EDD=2026-06-01+(280−round(219.07))=+61 天=2026-08-01。旧线性近似 (2.11+7.8×1.942)×7=120.8 天=17+2 周、EDD 2026-12-25，两串均不命中。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "176", usType: "hc" },
    expect: ["20+1 B超孕周", "2026-10-18 校正预产期"],
    ref: "Hadlock 1984 HC：17.6cm ⇒ GA=8.96+0.540×17.6+0.0003×17.6³=20.0995 周=20+1；EDD=2026-06-01+(280−round(140.70))=+139 天=2026-10-18。默认 CRL 60mm 输出 12+3 周/2026-10-14，两串均不命中。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "154", usType: "ac" },
    expect: ["20+4 B超孕周", "2026-10-15 校正预产期"],
    ref: "Hadlock 1984 AC：15.4cm ⇒ GA=8.14+0.753×15.4+0.0036×15.4²=20.5900 周=20+4；EDD=2026-06-01+(280−round(144.13))=+136 天=2026-10-15。默认 CRL 60mm 输出 12+3 周/2026-10-14，两串均不命中。" },
  { slug: "obstetrics/gestational-age",
    inputs: { usDate: "2026-06-01", usValue: "33", usType: "fl" },
    expect: ["20+2 B超孕周", "2026-10-17 校正预产期"],
    ref: "Hadlock 1984 FL：3.3cm ⇒ GA=10.35+2.460×3.3+0.170×3.3²=20.3193 周=20+2；EDD=2026-06-01+(280−round(142.24))=+138 天=2026-10-17。默认 CRL 60mm 输出 12+3 周/2026-10-14，两串均不命中。" },
  { slug: "obstetrics/cycle-8",
    inputs: { cycleDay: "14", thickness: "8", measureDate: "2024-06-01" },
    expect: ["8.0 最新厚度 (第14天)", "排卵期 (2024-06-01)"],
    ref: "三个输入 HTML 默认均为空串，注入后才有记录：周期第 14 天 ⇒ 分期「排卵期」（页面分期表：卵泡期 0–13、排卵期 14–16、黄体期 17+），厚度 8.0 mm；该期参考区间 9–14 mm ⇒ 判读「内膜偏薄」（输出中『临床解读（第14天，排卵期）』一句）。默认空态输出空列表/提示，两串均不出现。锚带天数与日期的合成串，避开纯标签「最新厚度」。⚠ harness 未建模 confirm（errs 有 delMeas: confirm is not defined），但只影响删除按钮，不影响注入态计算。" },
  {
    "slug": "obstetrics/afi-normal",
    "inputs": {
      "ruq": "42",
      "luq": "42",
      "rlq": "42",
      "llq": "42",
      "sdp": "42"
    },
    "expect": [
      "0 右下 RLQ 42.0 左下 LLQ 42.0 羊水过多 AFI≥25cm，羊水过多。需排查GDM、胎儿消化道畸形、染色体异常。症状明显可考虑羊膜腔穿刺放液。\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ruq\":\"42\",\"luq\":\"42\",\"rlq\":\"42\",\"llq\":\"42\",\"sdp\":\"42\"}，输出区含「0 右下 RLQ 42.0 左下 LLQ 42.0 羊水过多 AFI≥25cm，…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/bishop-score",
    "inputs": {
      "dilation": "1",
      "effacement": "1",
      "station": "1",
      "position": "1",
      "consistency": "1"
    },
    "expect": [
      "分明细 宫口扩张：1分 宫颈消退：1分 先露位置：1分 宫颈位置：1分 宫颈质地：1分 总分 = 5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dilation\":\"1\",\"effacement\":\"1\",\"station\":\"1\",\"position\":\"1\",\"consistency\":\"1\"}，输出区含「分明细 宫口扩张：1分 宫颈消退：1分 先露位置：1分 宫颈位置：1分 宫颈质地…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/calc-50",
    "inputs": {
      "height": "42",
      "weight": "42",
      "preWeight": "42",
      "hctBefore": "42",
      "hctAfter": "42",
      "mode": "cesarean"
    },
    "expect": [
      "42\n42\n42\n42\n42\ncesarean\n产后 Hct 应低于产前 Hct，请检查输入。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"height\":\"42\",\"weight\":\"42\",\"preWeight\":\"42\",\"hctBefore\":\"42\",\"hctAfter\":\"42\",\"mode\":\"cesarean\"}，输出区含「42\n42\n42\n42\n42\ncesarean\n产后 Hct 应低于产前 Hct…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/biyun-pearlzhishu-shibailv",
    "inputs": {
      "women": "42",
      "months": "42",
      "pregnancies": "42",
      "method": "pill"
    },
    "expect": [
      "Pearl 指数 28.57 典型使用失败率（复方口服避孕药） 7 完美使用失败率（复方口服避孕药） 0.3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"women\":\"42\",\"months\":\"42\",\"pregnancies\":\"42\",\"method\":\"pill\"}，输出区含「Pearl 指数 28.57 典型使用失败率（复方口服避孕药） 7 完美使用失败…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/cycle-8",
    "inputs": {
      "cycleDay": "42",
      "thickness": "42",
      "measureDate": "abc123测试",
      "measureNote": "abc123测试"
    },
    "expect": [
      "测量记录\n暂无记录\n42\n当前周期天数： 第42天 ，属于 黄体后期 ，参考范围： 7-14mm\n42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cycleDay\":\"42\",\"thickness\":\"42\",\"measureDate\":\"abc123测试\",\"measureNote\":\"abc123测试\"}，输出区含「测量记录\n暂无记录\n42\n当前周期天数： 第42天 ，属于 黄体后期 ，参考范围…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/calc-risk",
    "inputs": {
      "age": "42",
      "weight": "42",
      "ga": "42",
      "afp": "42",
      "bhCG": "42"
    },
    "expect": [
      "70） 风险分层 1.6239% 年龄先验风险 0.88 综合似然比"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"weight\":\"42\",\"ga\":\"42\",\"afp\":\"42\",\"bhCG\":\"42\"}，输出区含「70） 风险分层 1.6239% 年龄先验风险 0.88 综合似然比」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/down-screening",
    "inputs": {
      "age": "42",
      "gw": "42",
      "weight": "42",
      "afp": "42",
      "bhcg": "42",
      "ue3": "42"
    },
    "expect": [
      "诊断(羊水穿刺)。\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"gw\":\"42\",\"weight\":\"42\",\"afp\":\"42\",\"bhcg\":\"42\",\"ue3\":\"42\"}，输出区含「诊断(羊水穿刺)。\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/due-date",
    "inputs": {
      "lmpDate": "abc123测试",
      "cycle": "42",
      "eddDate": "abc123测试"
    },
    "expect": [
      "MP + 280天 + 14"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lmpDate\":\"abc123测试\",\"cycle\":\"42\",\"eddDate\":\"abc123测试\"}，输出区含「MP + 280天 + 14」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    // S2 产检逐次排程表（03-68）：日期随注入 lmp 平移 ⇒ 可判别
    "slug": "obstetrics/due-date",
    "inputs": {
      "lmpDate": "2024-01-15",
      "cycle": "28"
    },
    "expect": [
      "第1次：孕12周 2024-04-08 · NT 预约/建档化验",
      "第13次：孕40周 2024-10-21 · 预产期评估"
    ],
    "ref": "产检逐次排程表（03-68）：lmp=2024-01-15 +84 天（1月余16+2月29+3月31=76，余8 → 4/8）= 孕12周建档日 2024-04-08；+280 天 = 孕40周 2024-10-21（恰为 EDD，自洽）。⚠ 判别器 B 态走 loadExample（lmp=2024-02-10，FIXED_NOW=2024-06-15 −126 天）→ 第1次=2024-05-04，与注入态 2024-04-08 零交集；且 B 态 cycle=28 排程仍渲染但日期不同 ⇒ 锚依赖注入 lmp、判别可靠。日期由 lmp 平移、与运行日无关（铁律④）。"
  },
  {
    "slug": "obstetrics/fetal-movement-count",
    "inputs": {
      "morn": "42",
      "noon": "42",
      "even": "42",
      "h1": "42"
    },
    "expect": [
      " 正常 评估结果 42 早段/h 42 中段/h 42 晚段/h 126 3h合计 504"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"morn\":\"42\",\"noon\":\"42\",\"even\":\"42\",\"h1\":\"42\"}，输出区含「 正常 评估结果 42 早段/h 42 中段/h 42 晚段/h 126 3h合…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/endometrial-thickness",
    "inputs": {
      "cycleDay": "42",
      "thickness": "42",
      "cycleType": "ivf",
      "bleeding": "yes"
    },
    "expect": [
      "详情 月经周期：第42天 当前阶段：黄体期延长 该阶段参考厚度：10–14mm 实测厚度：42mm — 偏厚"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cycleDay\":\"42\",\"thickness\":\"42\",\"cycleType\":\"ivf\",\"bleeding\":\"yes\"}，输出区含「详情 月经周期：第42天 当前阶段：黄体期延长 该阶段参考厚度：10–14mm …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/fetal-weight-hadlock",
    "inputs": {
      "bpd": "42",
      "hc": "42",
      "ac": "42",
      "fl": "42",
      "sfh": "42",
      "ac2": "42"
    },
    "expect": [
      "C+AC+FL) 巨大儿 提示巨大儿。需评估糖尿病、肩难产风险，酌情计划分娩方式。\n42\n42\n529"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bpd\":\"42\",\"hc\":\"42\",\"ac\":\"42\",\"fl\":\"42\",\"sfh\":\"42\",\"ac2\":\"42\"}，输出区含「C+AC+FL) 巨大儿 提示巨大儿。需评估糖尿病、肩难产风险，酌情计划分娩方式…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/gestational-age",
    "inputs": {
      "lmpDate": "abc123测试",
      "cycleLen": "42",
      "usDate": "abc123测试",
      "usValue": "42",
      "lmpDate2": "abc123测试",
      "usType": "bpd"
    },
    "expect": [
      "abc123测试\n42\n⚠ 计算结果含无效值，请检查输入是否为有效正数。\nabc123测试\nbpd\n42\nabc123测试\nBPD 值 (mm)\n⚠ 计算结果含无效值，请检查输入是否为有效正数。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lmpDate\":\"abc123测试\",\"cycleLen\":\"42\",\"usDate\":\"abc123测试\",\"usValue\":\"42\",\"lmpDate2\":\"abc123测试\",\"usType\":\"bpd\"}，输出区含「abc123测试\n42\n⚠ 计算结果含无效值，请检查输入是否为有效正数。\nabc…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/heart-rate",
    "inputs": {
      "baseline": "42",
      "variability": "42",
      "accel": "42",
      "decel": "variable"
    },
    "expect": [
      "in 正常 减速 变异减速 处理建议： 建议立即评估母胎状况：左侧卧位、吸氧、纠正低血压、寻找病因（胎盘早剥、脐带脱垂、子宫破裂等），必要时紧急终止妊娠。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseline\":\"42\",\"variability\":\"42\",\"accel\":\"42\",\"decel\":\"variable\"}，输出区含「in 正常 减速 变异减速 处理建议： 建议立即评估母胎状况：左侧卧位、吸氧、纠…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/labor-curve",
    "inputs": {
      "dilation": "42",
      "hours": "42",
      "parity": "multip",
      "standard": "friedman"
    },
    "expect": [
      "multip\nfriedman\n42\n42\n42 cm 宫口扩张 42 h 临产时长 第二产程(宫口开全)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dilation\":\"42\",\"hours\":\"42\",\"parity\":\"multip\",\"standard\":\"friedman\"}，输出区含「multip\nfriedman\n42\n42\n42 cm 宫口扩张 42 h 临产…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/pearl-index",
    "inputs": {
      "preg": "42",
      "wm": "42"
    },
    "expect": [
      "用该方法1年约有 1200.0 人意外妊娠 低效 Pearl指数>10，避孕效果较低，1年内意外妊娠率>10%，建议改用更可靠方法。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"preg\":\"42\",\"wm\":\"42\"}，输出区含「用该方法1年约有 1200.0 人意外妊娠 低效 Pearl指数>10，避孕效果…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/placenta-grading",
    "inputs": {
      "gw": "42",
      "grade": "1"
    },
    "expect": [
      " 影像特征 绒毛板轻微波浪状，实质散在强回声点，基底板无改变。胎盘开始成熟。 孕42周仍为I级，可能胎盘成熟延迟，关注胎儿生长。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gw\":\"42\",\"grade\":\"1\"}，输出区含「 影像特征 绒毛板轻微波浪状，实质散在强回声点，基底板无改变。胎盘开始成熟。 孕…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/postpartum-hemorrhage",
    "inputs": {
      "wetWeight": "42",
      "dryWeight": "42",
      "preWeight": "42",
      "bloodFactor": "42",
      "hr": "42",
      "sbp": "42"
    },
    "expect": [
      "g 休克指数 = 42 ÷ 42 = 1.00 估计失血量：500–1000mL 轻度休克 轻度失血。监测生命体征，查明出血原因，备血。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wetWeight\":\"42\",\"dryWeight\":\"42\",\"preWeight\":\"42\",\"bloodFactor\":\"42\",\"hr\":\"42\",\"sbp\":\"42\"}，输出区含「g 休克指数 = 42 ÷ 42 = 1.00 估计失血量：500–1000mL…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/preeclampsia-prediction",
    "inputs": {
      "sflt": "42",
      "pigf": "42",
      "gw": "42",
      "onset": "late"
    },
    "expect": [
      "sFlt-1/PIGF = 42 / 42 = 1.00"
    ],
    "ref": "自动补强后收紧：注入 sFlt-1=42、PIGF=42、晚发型 ⇒ 比值 1.00，输出明细「sFlt-1/PIGF = 42 / 42 = 1.00」与「排除子痫前期」。原锚「确诊界值：≥110（晚」由 onset 单值决定、与 sflt/pigf 注入无关，默认态（1500/100/晚发）同样出现 ⇒ 逃生；改锚含两个注入值的比值明细。默认 15.00 ⇒ 不命中。"
  },
  {
    "slug": "obstetrics/rater-26",
    "inputs": {
      "k1": "1",
      "k2": "1",
      "k3": "1",
      "k4": "1",
      "k5": "1",
      "k6": "1",
      "k7": "1",
      "k8": "1",
      "k9": "1",
      "k10": "1",
      "k11": "1"
    },
    "expect": [
      " 阴道干涩 ×1 1分 1分 更年期症状中度，建议就医评估，可考虑植物药或低剂量激素替代治疗。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k1\":\"1\",\"k2\":\"1\",\"k3\":\"1\",\"k4\":\"1\",\"k5\":\"1\",\"k6\":\"1\",\"k7\":\"1\",\"k8\":\"1\",\"k9\":\"1\",\"k10\":\"1\",\"k11\":\"1\"}，输出区含「 阴道干涩 ×1 1分 1分 更年期症状中度，建议就医评估，可考虑植物药或低剂量…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/taipanchengshudu-grannumfenji",
    "inputs": {
      "gaWeek": "42",
      "chorion": "1",
      "substance": "1",
      "basal": "1"
    },
    "expect": [
      "annum 0 级，虽可见于正常妊娠，建议随访胎盘功能。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gaWeek\":\"42\",\"chorion\":\"1\",\"substance\":\"1\",\"basal\":\"1\"}，输出区含「annum 0 级，虽可见于正常妊娠，建议随访胎盘功能。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/yangshuizhishu-afi-zhengchangfanwei",
    "inputs": {
      "q1": "42",
      "q2": "42",
      "q3": "42",
      "q4": "42",
      "mvp": "42"
    },
    "expect": [
      "判读结果 建议： 建议排查妊娠期糖尿病、胎儿消化道畸形、双胎输血综合征等，必要时进一步检查。\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q1\":\"42\",\"q2\":\"42\",\"q3\":\"42\",\"q4\":\"42\",\"mvp\":\"42\"}，输出区含「判读结果 建议： 建议排查妊娠期糖尿病、胎儿消化道畸形、双胎输血综合征等，必要时…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "obstetrics/kupperman-score",
    "clicks": [
      "document.querySelectorAll('.symptom-row').forEach(function(r){r.dataset.sev='3';});calc()"
    ],
    "expect": [
      "总分 = 63",
      "重度症状，明显影响生活"
    ],
    "ref": "改良 Kupperman 原版 13 项、权重合计 21（潮热出汗 ×4，泌尿系统症状与性生活困难各 ×2），各症状程度 0–3 ⇒ 满分 63。clicks 把 13 行全部置「重(3)」⇒ 21×3=63 落 ≥31「重度」；默认态 13 行程度全 0 ⇒ 总分 0「基本正常」，零交集。"
  },
  { slug: "obstetrics/afi-normal",
    inputs: { ruq: "", luq: "", rlq: "", llq: "" },
    expect: ["请填写四个象限羊水暗区（cm）后再判读。"],
    ref: "空态守卫：四象限全清空时不再按 0 计算（旧实现 → AFI 0.0cm 直接判「羊水过少」），改为只输出填写提示，不给临床分级。默认态 4.5/5.0/3.8/4.2 有值 ⇒ 提示串不出现。" }
];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== obstetrics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();