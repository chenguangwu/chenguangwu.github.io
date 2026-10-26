#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pediatrics/assessor-13",
  "inputs": {
    "ageMonth": "24",
    "weight": "12",
    "prevWeight": "13.2",
    "diarrheaDays": "3"
  },
  "clicks": [
    "var __m={};for(var i=0;i<8;i++)__m['sg'+i]='2';__m.sg0='0';__m.sg1='1';var __g=document.getElementById;document.getElementById=function(id){if(__m[id]!==undefined)return {value:__m[id],checked:false};return __g.call(document,id);};calc()"
  ],
  "expect": [
    "【WHO 儿童脱水评估（8 项体征 + 液体缺失量）】 结果：月龄 24 月 · 体重 12 kg → 重度体征 1 项、轻/中度体征 1 项，分级：轻度脱水",
    "估计液体缺失量 360 mL（3% × 体重）；腹泻 3 天"
  ],
  "ref": "门诊记录：8 个体征下拉在 harness 里由 buildList() 动态生成、stub 中不存在，故 clicks 覆写 getElementById 直接给 sg0=0（重度）、sg1=1（轻中度）、其余 sg2-7=2（正常）⇒ 重度 1 项 + 轻中 1 项 ⇒ 按「severe+some>=1」落「轻度脱水」；3% × 12 kg = 360 mL（原实现漏 ×1000，只给 1 mL，本次已修）。默认态 8 项全取首档(idx 0)=重度 ⇒「重度体征 8 项…重度脱水」，与该用例零交集。另：病前体重 13.2→12 kg 给出 9.1% 体重丢失（与体征分级不一致属预期，页面已在提示里指出需结合体征判断）。"
},
{
  "slug": "pediatrics/assessor-spo2",
  "inputs": {
    "ageDay": "1",
    "rhSpO2": "85",
    "footSpO2": "80"
  },
  "expect": [
    "CCHD脉搏血氧筛查：CCHD筛查阳性（SpO2＜90%）",
    "综合风险：中风险"
  ],
  "ref": "新生儿 CCHD 脉搏血氧筛查（门诊记录）：右手 85% / 足部 80% / 差值 5% → 综合风险中风险、筛查阳性（默认 98/97/1% → 低风险、阴性）。原用例 expect 含「85%」属输入回显（逃生项类型②），已改为门诊记录强串「CCHD脉搏血氧筛查：CCHD筛查阳性（SpO2＜90%）」+「综合风险：中风险」，二者均随输入变化、默认态（阴性/低风险）不出现，零交集。钩子捕获 minS/diff/cchd/urg/lvl/sign/risk 等已算变量，EN 态走 cchdMap/urgMap/lvlMap + resultEn/extraEn/hintEn 纯英文映射，零 CJK。"
},
{"slug":"pediatrics/chd-assessment","inputs":{"age":"2","rhSpo2":"85","llSpo2":"78"},"checkIds":["cyanosis"],"expect":["结果：右上肢 SpO₂ 85% / 下肢 78%（差值 7%）→ 血氧筛查 阳性(转诊)；风险评分 8 分，分级：高风险","危险因素 3 项（血氧筛查阳性、中心性紫绀、上下肢SpO2差值≥5%(导管依赖)）"],"ref":"门诊记录（EMR note）：右上肢 85%、下肢 78% 均 <90 ⇒ 血氧阳性 +3；差值 7% ≥5 ⇒ 再 +2；勾选中心性紫绀 +3 ⇒ 风险评分 8 ≥5 落「高风险」。默认态 97/96（差值 1%、阴性）且无勾选 ⇒「风险评分 0 分，分级：极低风险」，零交集。原用例 expect 仅 85%/高风险 两个碎片。"},
{
  "slug": "pediatrics/ddst-screening",
  "inputs": {
    "age": "18"
  },
  "clicks": [
    "var d=domains[0];getAgeGroups(18).forEach(function(g){var it=d.items[g]||[];it.forEach(function(x,idx){testResults[d.key+'_'+g+'_'+idx]='fail';});});calc()"
  ],
  "expect": [
    "【DDST 丹佛发育筛查（4 能区）】 结果：年龄 18 月龄 → 4 个能区筛查：个人-社会异常(0/18)",
    "总体结果：异常 异常能区 1 个、可疑能区 0 个"
  ],
  "ref": "门诊记录：把「个人-社会」能区 18 月龄及以前的条目全部标记 fail（clicks 直接写 testResults），其余能区未测 ⇒ 1 个能区异常、0 个可疑 ⇒ 总体「异常」。默认态 testResults 为空 ⇒ 4 能区全「未测」、总体「正常」，与本用例零交集。"
},
{"slug":"pediatrics/dehydration-assessment","inputs":{"weight":"8","prevWeight":"8.8"},"checkIds":["s3","s4","s8"],"expect":["结果：分度：中度脱水（估计体液丢失 5-10%）· Gorelick 评分 3/10","体重丢失法算得 9.1%"],"ref":"门诊记录：勾选 s3 黏膜干燥 + s4 眼窝凹陷 + s8 尿量减少 ⇒ Gorelick 3/10 落 3–6 段「中度脱水」（5-10%）；病前 8.8 kg → 现 8 kg，体重丢失 (0.8/8.8)=9.1% ⇒ 累计丢失量按体重丢失法算得约 727 mL。默认态 10 kg、未勾选、无病前体重 ⇒「轻度脱水」「Gorelick 0/10」，零交集。"},
{"slug":"pediatrics/diarrhea-dehydration","inputs":{"age":"18","weight":"10","stoolFreq":"8","duration":"3","stoolType":"watery"},"checkIds":["s1","s4","s5","s8"],"expect":["结果：分度：中度脱水（体液丢失 8%）· 腹泻 8 次/日 · 病程 3 天 · 大便性状 水样便","重度体征 0 项、中度体征 4 项、轻度体征 0 项（共 4 项）"],"ref":"门诊记录：勾选 s1 眼窝凹陷 + s4 皮肤弹性差 + s5 尿量减少 + s8 前囟凹陷，全属中度体征 4 项 ⇒ 中度脱水（7.5%→显示 8%）；水样便。默认态 12 月/10 kg/6 次/日、未勾选 ⇒「无脱水（体液丢失 0%）」，零交集。"},
{"slug":"pediatrics/enuresis-age","inputs":{"age":"8","freq":"6"},"expect":["结果：年龄 8 岁 · 每周遗尿 6 次 → 严重度 中度(4-6次/周)；原发性遗尿 / 单症状性遗尿(仅夜间)（符合诊断）；同龄自然控尿率约 93%"],"ref":"门诊记录：8 岁、每周 6 次 ⇒ 4–6 段「中度」、≥5 岁且 ≥2 次/周「符合诊断」、8 岁档自然控尿率 93%；本题未勾选任何伴随症状 ⇒ 需排查 0 项。默认态 7 岁/4 次 ⇒「每周遗尿 4 次」「同龄自然控尿率约 85%」，零交集。原用例 expect 仅「10岁」年龄回显。"},
{"slug":"pediatrics/growth-curve-zscore","inputs":{"gender":"girl","age":"24","ageUnit":"month","height":"82","weight":"10.5","head":"46"},"expect":["结果：年龄 24 月（女）· 身高 82 cm → Z -1.16（正常）；体重 10.5 kg → Z -1.28（正常）；头围 46 cm → Z -0.92（正常）","参考中位数：身高中位 85.7、体重中位 12.3、头围中位 47.2"],"ref":"门诊记录（EMR note）：24 月女童 WHO 身高中位 85.7 cm、SD 3.2 ⇒ Z=(82-85.7)/3.2=-1.16；体重中位 12.3、SD 1.42 ⇒ -1.28；头围中位 47.2 ⇒ -0.92。默认态男童 87/12.5/48 ⇒「身高 87 cm → Z -0.03」，零交集。本批同时修 whoRef 身高中位数模型：旧实现 49+2.1×月龄 线性外推，24 月女童给到 99.4 cm（正确 85.7），正常儿童被判「Z -7.47 重度生长迟缓」；改为 WHO 生长标准分月龄中位数/SD 表（0–60 月 Child Growth Standards，61 月起 2007 生长参考）+ 线性插值。"},
{"slug":"pediatrics/hfmd-course","inputs":{"age":"18","day":"3","temp":"39.2"},"checkIds":["s2","s3"],"expect":["结果：年龄 18 月 · 病程第 3 天 · 体温 39.2°C → 分期：第2期：神经系统受累期；皮疹 0 处、分布典型：否","重症预警征象 2 项（神经系统 2 项、心肺 0 项）；处置：住院治疗+降颅压"],"ref":"门诊记录：勾选 s2 精神差/嗜睡 + s3 肢体抖动/肌阵挛（均属神经系统预警征）⇒ 神经 2 项、心肺 0 项 ⇒ 落「第 2 期：神经系统受累期」，处置「住院治疗+降颅压」。默认态 24 月/第 2 天/38.5°C 且无勾选 ⇒「疑似(皮疹不典型)」，零交集。原用例 expect 仅「40°C」体温回显。"},
{"slug":"pediatrics/hirschberg-test","inputs":{"fixing":"left","reflex":"nasal","offset":"3","pupil":"6"},"expect":["结果：注视眼：左眼 → 非注视眼：右眼；光反射位置 偏鼻侧、偏移 3 mm（约 45°）→ 重度外斜视(Exotropia)","经验换算：角膜光反射每偏移 1 mm 约对应 15°（≈7 三棱镜度）；瞳孔直径 6 mm"],"ref":"门诊记录：左眼注视、光反射偏鼻侧（眼球外转）⇒ 外斜；偏移 3 mm × 15° = 45°；≥3.5 mm 段为「极重度」、2.5–3.5 mm 为「重度」⇒ 3 mm 落「重度外斜视」。默认态 reflex=center、offset=2 ⇒「正位(无斜视)」「光反射位置 居中」，零交集。原用例注入 reflex=exo（页面并无该选项值）导致结论含 undefined，属非法输入，已改为合法值 nasal。"},
{"slug":"pediatrics/neonatal-jaundice","inputs":{"hours":"72","tsb":"15","ga":"39","bw":"3200"},"expect":["结果：TSB 15 mg/dL @ 出生 72 小时 → 高危险区；光疗阈值 17、换血阈值 22 → 未达光疗阈值","小时龄百分位 P40 11.5 / P75 14.5 / P95 15.0 mg/dL；高危因素：无"],"ref":"门诊记录：Bhutani 1999 小时龄百分位表 72 h 为 P40 11.5 / P75 14.5 / P95 15.0 mg/dL（AAP 2004/2009 沿用），TSB 15 ≥ P95 ⇒「高危险区」；39 周足月低危儿 72–96 h 光疗阈值 17、换血 22（页面 getThresholds）⇒ 未达光疗阈值。默认态 48 h/TSB 14 ⇒「TSB 14 mg/dL @ 出生 48 小时」「P95 12.0」，零交集。本用例同时锁住「百分位表口径」（原实现用二次多项式近似，72 h 给出 P95 56.8 mg/dL 的荒谬值，已改为权威表插值）。"},
{"slug":"pediatrics/pediatric-anemia","inputs":{"age":"12","ageUnit":"month","weight":"10","hb":"95","sf":"8","mcv":"70"},"expect":["结果：年龄 12 月（6-59月）· Hb 95 g/L（阈值 ≥110）→ 中度贫血；MCV 70 fL（阈值 ≥75）、SF 8 μg/L → 缺铁性贫血(IDA,Stage 3)","元素铁补充量 40.0 mg/日；SF 偏低：是；MCV 偏低：是"],"ref":"门诊记录：12 月龄属 6-59 月组，Hb 阈值 110 g/L，实测 95 ⇒ 中度贫血；MCV 70 < 75、SF 8 < 12 ⇒ IDA Stage 3；10 kg × 4 mg/kg/日 = 40.0 mg/日元素铁。默认态 Hb 100/MCV 72/SF 12 ⇒「轻度贫血」「铁储存不足」，零交集。"},
{"slug":"pediatrics/pediatric-fever","inputs":{"temp":"39.2","age":"8"},"clicks":["var e=document.getElementById('fever3d');if(e){e.checked=true;}calc()"],"expect":["结果：体温 39.2°C（腋温）→ 腋温等效 39.2°C，分度：高热","月龄 8 月；危险信号 1 条"],"ref":"门诊记录（EMR note）：体温 39.2°C（腋温）落 39.0–41.0 段「高热」；勾选发热>3 天 ⇒ 危险信号 1 条。默认态 38.5°C/24 月、未勾选 ⇒「分度：中度发热」「危险信号 0 条」，零交集。原用例只锚 39.5°C 单值（输入回显式弱锚）。"},
{"slug":"pediatrics/pediatric-pneumonia","inputs":{"age":"10","rr":"52","spo2":"95"},"checkIds":["s1","s2"],"expect":["结果：分度：重症肺炎，呼吸 52 次/分（该年龄增快阈值 50）· SpO₂ 95% → 处置：住院治疗","极重症体征 0 项、重症体征 2 项；记录体征共 2 项"],"ref":"门诊记录：10 月龄 WHO 呼吸增快阈值 50，RR 52 达增快；勾选 s1 胸凹陷 + s2 鼻翼扇动 = 2 项重症体征、0 项极重症 ⇒ 落「重症肺炎」/「住院治疗」。默认态 12 月/RR 55/SpO₂ 92 且无勾选 ⇒「肺炎」/「门诊治疗」，零交集。"},
{
  "slug": "pediatrics/rater-27",
  "inputs": {
    "gender": "girl",
    "ageMonth": "24",
    "weight": "8.2",
    "height": "80",
    "headCirc": "45"
  },
  "clicks": [
    "calc()"
  ],
  "ref": "女 24 月龄：体重 8.2 kg ⇒ Z=-2.73（中度偏低，超 -2SD）；身长 80 cm ⇒ Z=-1.96；头围 45 cm ⇒ Z=-1.74；BMI 8.2/0.8²=12.8。阳性条目仅体重/年龄一项，提示语走 |Z|>2 分支而非 Z<-3 分支。默认态 ageMonth 空 ⇒ Z 全为「—」，与本用例零交集。",
  "expect": [
    "【儿童生长发育 Z 评分评估（WHO 标准）】 结果：女 2.0 岁（24 月龄）· 体重 8.2 kg（Z -2.73）· 身长/高 80 cm（Z -1.96）· 头围 45 cm（Z -1.74） · BMI 12.8 阳性条目（共 1 项）：Q1 体重/年龄 Z -2.73（超出 ±2SD：中度偏低） 判读口径：以 WHO 儿童生长标准（按月龄插值取中位数与 SD）计算 Z 评分；|Z|&gt;2 为超出正常范围、|Z|&gt;3 为重度异常；单次测量不替代纵向生长曲线 临床提示：存在超出 ±2SD 的指标：结合生长曲线趋势（是否跨越主要百分位线）判断，单次测量异常需 4 周内复测确认，同时记录喂养与近期疾病史。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{"slug":"pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian","inputs":{"age":"48","bili":"20"},"expect":["结果：日龄 48 小时，TSB 20 mg/dL → 光疗阈值区；光疗阈值 13.5、换血阈值 21.0 mg/dL；Bhutani 百分位 ≥95th","胎龄 38 周（低危曲线）· 危险因素：无；距换血阈值余 1.0 mg/dL"],"ref":"门诊记录：48 h、TSB 20 mg/dL，胎龄 38 周无危险因素 ⇒ 走低危阈值（光疗 13.5、换血 21.0）⇒ 20 ≥13.5 且 <21 落「光疗阈值区」，距换血余 1.0 mg/dL；Bhutani 表 P95(48h)=12 ⇒ 20 ≥ P95 落 ≥95th。默认态 TSB 14 ⇒「TSB 14 mg/dL」「距换血阈值余 7.0 mg/dL」，零交集。本批同时把本页旧百分位表（P95 48h=14.0/P75=9.5/P40=6.0，较 AAP 口径系统性偏高约 2 mg/dL）统一为 Bhutani/Maisels 表值，与 neonatal-jaundice 页同源。"},
{
  "slug": "pediatrics/vaccine-schedule",
  "inputs": {
    "vaccinatedMonth": "6"
  },
  "expect": [
    "预防：乙型肝炎 已接种"
  ],
  "ref": "疫苗接种时间表：vaccinatedMonth=6 表示已接种至 6 月龄 → 0~6 月龄疫苗行的状态变为「已接种」（默认空 → 全部「逾期，尽快补种」）。锚点取随输入变化的具体行串「预防：乙型肝炎 已接种」（仅当该行状态为已接种时出现），避开页面恒定图例「绿色=已接种…」(含「已接种」三字，裸「已接种」会恒命中导致逃生项)。回退默认(空)该行为「逾期，尽快补种」→ 失配。"
},
{"slug":"pediatrics/developmental-milestones","inputs":{"age":"27"},"expect":["月龄 27 月，总体达成 0/8（0%）→ 多能区明显落后","说2-3字句"],"ref":"门诊记录：age=27 取出 27 月龄里程碑条目集（4 能区各 2 条 = 8 条）⇒「0/8（0%）」；达到率 0 落「多能区明显落后」段。默认 18 月龄 ⇒「月龄 18 月，总体达成 0/6」，与「0/8」零交集；「说2-3字句」为 27 月龄条目正文，默认 18 月龄不出现。注：里程碑勾选框由 renderMilestones 动态生成，stub DOM 无法勾选，故达成数恒 0；此处只锚「月龄→条目数」的映射。"},
{
  "slug": "pediatrics/hearing-screening",
  "inputs": {
    "age": "2",
    "ageUnit": "month",
    "method": "aabr",
    "leftResult": "refer",
    "rightResult": "pass"
  },
  "checkIds": [
    "riskFactor"
  ],
  "expect": [
    "【新生儿听力筛查（UNHS）】 结果：筛查方式 AABR 自动听性脑干反应 · 月龄 2 月（折合约 60 天）→ 左耳 未通过（转诊）、右耳 通过；结论：单侧未通过（转诊）",
    "下一步随访：42天内复查/3月龄诊断；听力高危因素：有"
  ],
  "ref": "门诊记录（EMR note）：AABR + 2 月龄 + 左耳转诊/右耳通过 + 勾选高危因素 ⇒ 综合判定「单侧未通过(转诊)」，随访 42 天内复查/3 月龄诊断。默认态为 OAE + 3 天龄 + 双耳通过 + 无高危 ⇒「结论：通过」「听力高危因素：无」，与本用例零交集。"
},
{"slug":"pediatrics/mchat-autism","clicks":["for(var i=0;i<20;i++){answers[i]=true;}answers[1]=false;answers[4]=false;answers[11]=false;calc()"],"expect":["结果：未通过 5/20 题，分级：中风险","关键题未通过 3 项（第2、5、12题）"],"ref":"门诊记录：20 题全答「是」后把第 2、5、12 题（0-based 1/4/11）改答「否」⇒ 这 3 题为关键未通过；另 17、19 题答「是」按页面 failOnYes 口径记未通过 ⇒ 共 5 题 >2 且 ≤7 落「中风险」。默认态未作答 ⇒ calc 直接 return、不渲染门诊记录，零交集。原用例 expect 仅年龄回显「27」（零判别力，auto-restore 残留）。"},
{
  "slug": "pediatrics/pediatric-asthma",
  "inputs": {
    "age": "8"
  },
  "clicks": [
    "answers={c1:1,c2:1,c3:1,c4:1,p1:2,p2:2,p3:2};calc()"
  ],
  "expect": [
    "C-ACT（儿童哮喘控制测试，4–11 岁，儿童 4 题 0–3 + 家长 3 题 0–5，满分 27） → 总分 10/27，分级：未控制",
    "作答 7 题；分级界值：≤19 未控制、20–22 部分控制、≥23 完全控制"
  ],
  "ref": "门诊记录：年龄 8 岁 ⇒ C-ACT 7 题（儿童 4 题 0–3 + 家长 3 题 0–5，满分 27，原实现按 5 档累加得 25 且界值套用成人 ACT 的 20/16，本次按官方口径修正为 ≥23/20–22/≤19）；clicks 直接写 answers ⇒ 总分 1+1+1+1+2+2+2=10 ≤19 ⇒「未控制」。默认态 answers 为空 ⇒ answered<7 直接 return、不渲染门诊记录，零交集。"
},
{
  "slug": "pediatrics/pediatric-fracture",
  "inputs": {
    "age": "9",
    "site": "distal_femur",
    "open": "1"
  },
  "clicks": [
    "calc()"
  ],
  "ref": "9 岁 + 股骨远端 + 开放性骨折 ⇒ 分型默认 Salter-Harris I 型、预后良好、生长障碍风险低(<1%)，但开放骨折强制走「急诊优先」分支（清创+抗生素+破伤风），并在阳性条目列出「开放性骨折」。默认态 site=distal_radius 且无开放性 ⇒ 走 I–II 型常规分支、无「开放性骨折」条目，与本用例零交集。",
  "expect": [
    "【儿童骨骺损伤（Salter-Harris 分型）评估】 结果：年龄 9 岁 · 部位 股骨远端 · 分型 Salter-Harris I 型 · 预后 良好、生长障碍风险 低(&lt;1%) 阳性条目：无 分型口径（Salter-Harris）：I 骺板分离、II 骺板+干骺端、III 骺板+骨骺（关节内）、IV 贯通干骺端-骺板-骨骺、V 骺板挤压伤（早期 X 线常阴性）；本部位要点：股骨远端骺板占下肢生长70%，损伤后果严重，IV型几乎必发生生长障碍 临床提示：Salter-Harris I–II 型：以闭合复位加石膏固定为主，复位后 1 周、2 周复查 X 线；告知家长观察末梢血运、肿胀与疼痛变化，出现剧痛或麻木需即刻返院。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
},
{"slug":"pediatrics/seizure-classification","inputs":{"age":"24"},"clicks":["opts.duration='prolonged';opts.type='focal';calc()"],"expect":["结果：年龄 24 月 · 发热 有 · 发作时长 ≥15 分钟 · 发作形式 局灶性 · 次数 单次 → 复杂型热性惊厥（复发风险 50-60%）","复发危险因素 2 项（长时程发作、局灶性发作）；家族史：阴性；既往惊厥史：无"],"ref":"门诊记录：24 月龄在 6–60 月范围内且发热 ⇒ 属热性惊厥；clicks 置 duration=prolonged、type=focal ⇒ 非「短+全面+单次」组合 ⇒ 落「复杂型热性惊厥」（复发 50-60%）；危险因素计 2 项。默认态 brief/generalized/single ⇒「单纯型热性惊厥（复发风险 ~30%）」「危险因素 0 项」，零交集。原用例 expect 仅「30月」年龄回显（auto-restore 残留）。"},
{
  "slug": "pediatrics/vanderbilt-adhd",
  "inputs": {
    "age": "9",
    "rater": "teacher"
  },
  "clicks": [
    "for(var i=0;i<9;i++){answers['inatt_'+i]=3;answers['hyper_'+i]=3;}for(var j=0;j<8;j++){answers['behav_'+j]=3;}for(var k=0;k<7;k++){answers['anx_'+k]=3;}calc()"
  ],
  "ref": "9 岁（≥6 岁）+ 教师版：attention 9 题全 3 分 ⇒ 9/9 阳性、总分 27/36；hyper 同 ⇒ 9/9、27/36；behav 8 题全 3 分 ⇒ 8/8；anx 7 题全 3 分 ⇒ 7/7 ⇒ 混合型 + 共病 ⇒「ADHD阳性(伴共病)」。默认态 answers 为空 ⇒ 全 0、走阴性分支，与本用例零交集。",
  "expect": [
    "【Vanderbilt ADHD 诊断量表（教师版）】 结果：年龄 9 岁 · ADHD阳性(伴共病)（混合型） · 注意缺陷 9/9（总分 27/36）、多动冲动 9/9（总分 27/36）、行为问题 8/8、焦虑抑郁 7/7 阳性条目（共 4 项）：Q1 注意缺陷 9/9 条阳性（总分 27/36）；Q2 多动冲动 9/9 条阳性（总分 27/36）；Q3 行为/对立违抗 8/8 条阳性（共病筛查阳性）；Q4 焦虑/抑郁 7/7 条阳性（共病筛查阳性） 阳性界值：注意缺陷或多动冲动 ≥6 条（评分≥2 计为阳性）、行为问题 ≥3/8、焦虑抑郁 ≥3/7；量表仅作筛查，诊断需结合跨场景信息、病程与功能损害 临床提示：筛查阳性且伴共病：建议儿童精神科/发育行为儿科评估，同时评估对立违抗、焦虑抑郁、睡眠与学习功能；行为治疗与家长培训为一线，药物需专科处方与随访。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）"
  ]
}
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

  console.log("==== pediatrics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
