#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
// ─────────────────────────────────────────────────────────────
// 第十五批弱用例去默认化（tcm-pharmacy 22 例）
//   ① 8 例 all_default：原 inputs 逐字等于页面默认值 → 全部换非默认输入 + 独立复算期望
//   ② 9 例 no_inputs：8 例转真输入；five-flavors 页面无可注入控件，保留 no_inputs（见该例 ref）
//   ③ 5 例「真但无效」：expect 为注入值原样回显 / JS 模板残骸键 → 改真键 + 真结果
//   所有数值期望均由 Python（IEEE754 double，toFixed 用 Decimal 精确二进制 + HALF_UP 模拟）独立复算
// ─────────────────────────────────────────────────────────────
{
  // 药酒浸泡浓度/时间：cat=animal（浸出率 0.18、建议 45~60 天）150g/800mL/60%vol、目标 0.15 g/mL
  // 复算：conc=150/800=0.1875→0.188；1:5；extConc=27*1000/800=33.8；finalAbv=60*800/807.5=59.4%
  //       dose=15mL（0.1≤conc<0.2）；doseHerb=15*0.1875=2.81；target 0.15 → 已达标、达标需 120.0g
  "slug": "tcm-pharmacy/calc-time-concentration",
  "inputs": {
    "herb": "150",
    "vol": "800",
    "abv": "60",
    "target": "0.15",
    "cat": "animal"
  },
  "expect": [
    "目标生药浓度 0.150 g/mL：当前已达标。",
    "1:5 药酒比",
    "33.8"
  ],
  "ref": "独立复算：conc=150/800=0.1875→toFixed(3) 0.188；ratio=800/150→1:5；extConc=150*0.18*1000/800=33.75→33.8；finalAbv=60*800/(800+150*0.05)=59.4427→59.4%；needHerb=0.15*800=120.0。默认（root/100/1000/50/0.1）conc=0.100、1:10、目标已达标，故本例须靠 0.150/1:5/33.8 三分支差异判定（原 expect「暂无计算记录」取自 historyBox 空态，与计算无关）"
},
{
  // 汤剂煎煮时间表：herbCount=6、avgDose=12（总药量 72g）、三煎、含先煎(石膏/附子)+后下(薄荷)+冲服(三七粉)
  // 复算：头煎 720、二煎 576、三煎 432；得汁 216/173/130 → 合汁 519；特殊煎法 4 味
  "slug": "tcm-pharmacy/decoction-time",
  "inputs": {
    "herbInput": "石膏,附子,薄荷,三七粉",
    "herbCount": "6",
    "avgDose": "12",
    "decoctTimes": "3"
  },
  "expect": [
    "总量约 519ml",
    "步骤4 - 三煎",
    "分3次温服"
  ],
  "ref": "独立复算：totalWeight=6*12=72；waterFirst=ceil(72*10)=720、Second=ceil(72*8)=576、Third=ceil(72*6)=432；得汁 ceil(720*0.3)=216、ceil(576*0.3)=173、ceil(432*0.3)=130 → totalJuice=519ml；先煎 石膏/附子、后下 薄荷、冲服 三七粉 → 特殊煎法 4。默认（5/10/两煎）totalJuice=270 → 「总量约 270ml」，且兜底 loadExample 会把药材设为「石膏，知母，薄荷，甘草，粳米，附子」得「步骤2 - 头煎（知母、甘草、粳米）」，故**不可**用「步骤1 - 先煎（石膏、附子）」作锚点（默认态经 loadExample 同样命中，实测逃生项）；改锚 519ml / 步骤4-三煎 / 分3次温服（默认两煎 → 分2次温服）三个仅注入态成立的串（原 expect「每日一剂」为注意事项固定文案，恒命中）"
},
{
  // 药酒配制方案：红花酒（当量比 1:8、建议 10~20 天）、100g/800mL/45%vol、成人 70kg
  // 复算：herbConc=100/800*100=12.50%；ratio=800/100=8.0（|8.0-8|≤2 → 比例合适）；纯酒精 360mL
  //       soakDays=(10+20)/2=15；recommended=min(20, 70*0.4=28)=20 → 每次 10mL；每日酒精 9.0g；可服 40 天
  "slug": "tcm-pharmacy/medicinal-wine",
  "inputs": {
    "wineType": "红花酒",
    "herbWeight": "100",
    "wineVolume": "800",
    "alcoholPct": "45",
    "patient": "adult2"
  },
  "expect": [
    "药酒比例(1:8.0)",
    "药酒比例合适，符合该类药酒的标准配比",
    "12.50%"
  ],
  "ref": "独立复算：herbConc=100/800*100=12.50；ratio=(800/100).toFixed(1)=8.0；ratioEval 因 8.0∈[6,10] 落「合适」；soakDays=(10+20)/2=15；weightMap.adult2=70 → recommendedDose=min(20,28)=20 → perDose=10；dailyAlcohol=20*45/100=9.0≤25（不触发超量提醒）；totalDays=round(800/20)=40。wineVolume 取 800 与 loadType() 对 herbWeight=100 的推荐值一致，故 wineType 的 change 顺序不影响结果。默认 wineType 为空串 → calc() 直接 return（result 为空），本例任何分支文案均非默认态（原 expect「散瘀止痛」取自配方列表静态文案）"
},
{
  // 中药剂量换算：成人 9g、6 岁、20kg、有毒中药（×0.5）
  // 复算：ageDose=9*0.33=2.97；Young=9*6/18=3；Clark=9*20/60=3；bsa=20*0.035+0.1=0.80 → bsaDose=9*0.8/1.73=4.16
  //       四法均值 3.2829…×0.5=1.6415 → 推荐 1.64g
  "slug": "tcm-pharmacy/tcm-dosage",
  "inputs": {
    "adultDose": "9",
    "age": "6",
    "weight": "20",
    "drugType": "toxic"
  },
  "expect": [
    "推荐儿童剂量：1.64g",
    "有毒中药，剂量减半",
    "2.97g ~ 4.16g"
  ],
  "ref": "独立复算：age≤6 → ageRatio=0.33 → ageDose=2.97；youngDose=9*6/(6+12)=3.00；clarkDose=9*20/60=3.00；bsa=0.80、bsaDose=9*0.8/1.73=4.1618→4.16；avg=(2.97+3+3+4.1618)/4=3.28296×adjustFactor 0.5=1.6415→推荐 1.64g；区间 2.97g~4.16g。默认（10g/5岁/18kg/普通）推荐 3.37g、无减半提示，故 1.64g 与「剂量减半」均只在注入态成立（原 expect「推荐儿童剂量」为固定标签，恒命中）"
},
{
  // 中成药经济学：补中益气丸 36 元/200 粒、每次 8 粒、每日 3 次、疗程 14 天
  // 复算：unitPrice=36/200=0.180；ddc=0.18*8*3=4.32 元/日；totalCost=4.32*14=60.48 元；性价比 100%
  "slug": "tcm-pharmacy/tcm-pharmacoeconomics",
  "inputs": {
    "drugName": "补中益气丸",
    "drugPrice": "36",
    "drugPkgQty": "200",
    "drugSingleDose": "8",
    "drugFreq": "3",
    "drugDays": "14"
  },
  "expect": [
    "日治疗费用仅 4.32 元，疗程费用 60.48 元。",
    "0.180"
  ],
  "ref": "独立复算：unitPrice=36/200=0.18→toFixed(3) 0.180；ddc=0.18*8*3=4.32；totalCost=4.32*14=60.48；ratio=round(4.32/4.32*100)=100%。drugName 默认空 → addDrug() 提前 return、drugList 恒空、仅渲染「请添加药品进行比较」，故 4.32/60.48 只在注入态出现（原 expect 即该空态文案，与计算无关；参考药品列表含 25/100 等数字，均与 4.32/60.48 不同）"
},
{
  // 方歌生成：银翘散 + 十味药 + 功效「辛凉透表，清热解毒」
  // 复算：namePart=「银翘」；line1=substr7(银翘方中用银花连翘)=银翘方中用银花；line2=substr7(竹叶荆芥牛共成方)=竹叶荆芥牛共成
  //       line3=pad7(辛凉透表功独擅)=7 字原样；line4=临证加减效堪夸
  "slug": "tcm-pharmacy/formula-song",
  "inputs": {
    "formulaName": "银翘散",
    "herbInput": "银花,连翘,竹叶,荆芥,牛蒡子,豆豉,薄荷,甘草,桔梗,芦根",
    "effectInput": "辛凉透表，清热解毒"
  },
  "expect": [
    "银翘方中用银花",
    "辛凉透表功独擅",
    "组成药材： 银花、连翘、竹叶、荆芥、牛蒡子、豆豉、薄荷、甘草、桔梗、芦根"
  ],
  "ref": "独立复算（padTo7 七言凑字）：name.replace([汤丸散丹饮方],'')=「银翘」→ line1=substring(0,7)(银翘方中用银花连翘)=银翘方中用银花；remaining 拼接前 5 字=竹叶荆芥牛 → line2=竹叶荆芥牛共成；effect 前 4 字+功独擅=辛凉透表功独擅（恰 7 字）。默认（补气养血汤/黄芪,…）生成「补气养方中用黄」「补气养血功独擅」；另 loadCustomExample 会以 customExamples[1]（清热泻火方）覆盖重算，得「清热泻方中用石」，均与本例锚点不同（原 expect「推荐优先背诵经典方歌」为提示框固定文案，恒命中）"
},
{
  // 配方颗粒当量折算：石膏（当量比 1:10、每袋 3g 相当于饮片 30g）饮片 45g
  // 复算：granuleDose=45/10=4.50g；bags=4.5/3=1.5 袋
  "slug": "tcm-pharmacy/granule-equivalent",
  "inputs": {
    "herbSelect": "石膏",
    "decoctionDose": "45"
  },
  "expect": [
    "45g ÷ 10 = 4.50g",
    "4.50g"
  ],
  "ref": "独立复算：granuleDose=45/10=4.50（toFixed(2)）；bagG 取自规格「每袋装3g」=3 → bags=4.5/3=1.5。默认 herbSelect 为空 → calcSingle 仅输出「请选择药材」；兜底会调 loadFormulaExample（黄芪:30 → 6.00g），全串「45g ÷ 10 = 4.50g」仅注入态出现（原 expect「加开水150-200ml…」仅由 loadFormulaExample 的处方折算分支产生，与注入值无关）"
},
{
  // 配伍禁忌核对：硫黄+朴硝（十九畏）、甘草+海藻（十八反甘草组）
  // 复算：十九畏命中 1 组（硫黄/朴硝）、十八反命中 1 组（甘草反海藻）→ 共 2 项；四味药均不在妊娠禁用/慎用表 → 无妊娠提示
  "slug": "tcm-pharmacy/incompatibility-check",
  "inputs": {
    "herbInput": "硫黄，朴硝，甘草，海藻"
  },
  "expect": [
    "发现 2 项配伍禁忌",
    "甘草 与 海藻 不可同用",
    "共 4 味药"
  ],
  "ref": "独立复算（双循环双向匹配 + key 去重）：十九畏仅硫黄↔朴硝命中 → 1 项；十八反甘草组 aParts=[甘草]、bParts=[京大戟,芫花,甘遂,海藻] → 甘草↔海藻命中 → 1 项；其余七组十九畏与乌头/藜芦两组均无交集 → conflicts=2。妊娠表比对：硫黄/朴硝/甘草/海藻均不在 pregnancyForbidden/Caution → 无妊娠段。默认 herbInput 为空 → checkCompat 提前 return，仅渲染两张参考表（表内含「甘草 反 …海藻」，但无「与 海藻 不可同用」与「发现 2 项」措辞）（原 expect「以下药物对孕妇有风险」仅由兜底 loadExample 触发，与注入值无关）"
},
  // 注：tcm-pharmacy/analysis-ratio-prescription 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  // 药材质量评分：人参 8 项（权重 15/15/15/15/10/10/10/10）分别 90/85/80/95/70/60/100/90
  // 复算：Σ 评分×权重% = 13.5+12.75+12+14.25+7+6+10+9 = 84.5 → 「合格品」（≥80）
  "slug": "tcm-pharmacy/herb-quality",
  "inputs": {
    "herbSelect": "人参",
    "score_0": "90",
    "score_1": "85",
    "score_2": "80",
    "score_3": "95",
    "score_4": "70",
    "score_5": "60",
    "score_6": "100",
    "score_7": "90"
  },
  "expect": [
    "84.5 分",
    "质量良好，符合药典标准，可入药使用",
    "合格品"
  ],
  "ref": "独立复算：totalScore=Σ score_i×weight_i/100=90*.15+85*.15+80*.15+95*.15+70*.1+60*.1+100*.1+90*.1=84.5→toFixed(1) 84.5，落 [80,90) → 合格品 + 「质量良好，符合药典标准，可入药使用」。原 inputs 键为脚本模板字面量 score_'+i+'（页面真实键是 renderScoreForm 生成的 score_0…score_7），注入从未生效、expect「120」只是那个幻影元素的 value 回显，属无效用例。注：本例键含动态 id，selfcheck/discriminate 两道静态校验均取不到默认值（判 null / 跳过），判别力已由自建同口径探针补验（注入 PASS + 回退默认 FAIL）"
},
{
  // 药膳配方折算：杜仲猪腰汤、3 人份（基准 2 人份 → ×1.5）、气虚质（药材 ×1.3）
  // 复算：猪腰 2*1*1.5=3 只、杜仲 15*1.3*1.5=29g、生姜 10*1*1.5=15g、枸杞子 10*1.3*1.5=20g
  //       foodTotal=18g、herbTotal=48.75→49g、药食比例 1:(18/48.75)=1:0.4
  "slug": "tcm-pharmacy/medicated-diet",
  "inputs": {
    "recipeSelect": "杜仲猪腰汤",
    "servingSize": "3",
    "constitution": "qi"
  },
  "expect": [
    "药食比例(1:0.4)",
    "气虚质：补气药量增加30%",
    "18g"
  ],
  "ref": "独立复算：servingFactor=3/2=1.5；qi 体质 herbFactor=1.3、foodFactor=1；猪腰(食,2,只)→3 只；杜仲(药,15)→29g；生姜(食,10)→15g；枸杞子(药,10)→20g；foodTotal=3+15=18→「18g 食材总量」；herbTotal=29.25+19.5=48.75→49g；ratio=(18/48.75).toFixed(1)=0.4→「药食比例(1:0.4)」；qi 提示「气虚质：补气药量增加30%」。默认 recipeSelect 为空 → calc 提前 return（result 为空）；normal 体质 note 为空串，故体质提示也只在注入态出现。原 expect「qi」是 select value 的回显，属无效用例"
},
{
  // 服药时间建议：驱虫药（本应空腹服）+ 日常调养 + 胃肠敏感 → 改为饭后服
  "slug": "tcm-pharmacy/medication-timing",
  "inputs": {
    "drugType": "驱虫药",
    "purpose": "supplement",
    "stomach": "sensitive"
  },
  "expect": [
    "饭后服（调整建议）",
    "您的胃肠较敏感，建议改为饭后30分钟服用以减少刺激，或遵医嘱",
    "日常调养服用建议从小剂量开始"
  ],
  "ref": "规则核对：驱虫药 timing=空腹服、timeDetail=清晨空腹；stomach=sensitive 且 timing∈{空腹服,饭前服} → timing 改写为「饭后服（调整建议）」、timeDetail 改「饭后30分钟」、adjustedNote 输出「您的胃肠较敏感，建议改为饭后30分钟服用以减少刺激，或遵医嘱」；purpose=supplement → purposeNote「日常调养服用建议从小剂量开始…」。默认 drugType 为空 → recommend 提前 return，仅渲染全量时间表（表内驱虫药为「空腹服」，绝无「饭后服（调整建议）」）。原 expect「supplement」是 select value 回显，属无效用例"
},
{
  // 药引用量：大枣（baseDose 3 枚/baseGram 10g/maxDose 12/maxGram 40）、15 味药（>12 → ×1.3）、儿童（×0.5）、补益方（大枣 → ×1.3）
  // 复算：totalFactor=1.3*0.5*1.3=0.845；unitDose=ceil(3*0.845)=3 枚；gramDose=(10*0.845).toFixed(1)=8.5g
  //       maxUnit=ceil(12*0.5)=6 枚、maxGram=20.0g（均未越界）
  "slug": "tcm-pharmacy/medicinal-guide",
  "inputs": {
    "guideSelect": "大枣",
    "herbCount": "15",
    "patient": "child",
    "formulaType": "supplement"
  },
  "expect": [
    "儿童用药引减半",
    "补益方，大枣适当加量增强补益",
    "8.5g",
    "×0.85"
  ],
  "ref": "独立复算：herbFactor=1.3（herbCount 15>12）；patientFactor=0.5（child）→ patientNote「儿童用药引减半」；typeFactor=1.3（supplement 且 guide=大枣）→ typeNote「补益方，大枣适当加量增强补益」；totalFactor=0.845→toFixed(2) 0.85（表格「×0.85」）；unitDose=ceil(3*0.845)=3 枚；gramDose=(10*0.845).toFixed(1)=8.5g；maxUnit=6 枚、maxGram=20.0g。默认 guideSelect 为空 → calc 提前 return；药引列表里大枣用法为「劈开3-12枚（约10-40g）」，不含「8.5g」，故锚点均非默认态。原 expect「child」是 select value 回显，属无效用例"
},
{
  // 药材图鉴检索（过滤型）：q=化痰 命中陈皮/半夏/冬虫夏草 3 条
  // 判别力要点：过滤结果是全量子集，单卡片内文本在默认全量态同样存在 → 只能用「仅过滤态成立的跨卡片相邻串」
  "slug": "tcm-pharmacy/herb-properties",
  "inputs": {
    "searchInput": "化痰"
  },
  "expect": [
    "消痞散结 🌿 冬虫夏草"
  ],
  "ref": "跨卡片相邻串：q=化痰 命中 陈皮→半夏→冬虫夏草（3 条）；其中「半夏」在全量库中的下一条是阿胶（冬虫夏草的前一条是阿胶），故「消痞散结」（半夏功效末句）紧接「🌿 冬虫夏草」的组合**仅过滤态成立**，默认全量态为「消痞散结 🌿 <半夏之后的那味>」。全量卡数 119 与过滤后 3 条亦不同（原 expect「119」即 countText 默认全量数，属默认态逃生项）"
},
{
  // 药性（四气）查询：葶苈子 → 精确命中「大寒」
  "slug": "tcm-pharmacy/four-qi-nature",
  "inputs": {
    "herbInput": "葶苈子"
  },
  "expect": [
    "大寒性",
    "清热泻火力强。适用于实热重证。不宜久服。"
  ],
  "ref": "精确匹配分支：herbQiDB['葶苈子']='大寒' → 渲染「大寒性」徽章 + qiDesc['大寒']「清热泻火力强。适用于实热重证。不宜久服。」。默认 herbInput 为空 → queryQi 仅输出「请输入药材名称」（原 expect 即该空态文案，恒命中）。「大寒」同时区别于模糊匹配分支（模糊结果不含「大寒性」徽章措辞）"
},
{
  // 炮制规格检索（过滤型）：q=炭 命中大黄炭/生地炭/黄柏炭/当归炭/香附炭 5 条
  "slug": "tcm-pharmacy/herb-processing",
  "inputs": {
    "searchInput": "炭"
  },
  "expect": [
    "止血止泻 🔬 地黄 · 生地炭",
    "止血和血 🔬 香附 · 香附炭"
  ],
  "ref": "跨卡片相邻串：q=炭 命中 5 条（大黄炭→生地炭→黄柏炭→当归炭→香附炭）。全量库中大黄炭的下一条是生地黄（非生地炭）、当归炭的下一条是生白芍（非香附炭），故「止血止泻 🔬 地黄 · 生地炭」与「止血和血 🔬 香附 · 香附炭」仅过滤态成立（原 expect「55」为 countText 默认全量数，属默认态逃生项；全量实为 57）"
},
{
  // 贮藏养护检索（过滤型）：q=参 命中人参/西洋参/党参 3 条
  "slug": "tcm-pharmacy/herb-storage",
  "inputs": {
    "searchInput": "参"
  },
  "expect": [
    "易虫蛀、霉变 📦 党参"
  ],
  "ref": "跨卡片相邻串：q=参 命中 3 条（人参→西洋参→党参）。全量库中西洋参的下一条是甘草（非党参），故「易虫蛀、霉变（西洋参主要风险）📦 党参」仅过滤态成立；另「易虫蛀、泛油」为人参风险，可区分两者（原 expect「45-65%」取自甘草/黄芪的湿度字段，默认全量态即存在，属逃生项）"
},
{
  // 君臣佐使分析：四物汤（熟地黄 12 君 / 当归 9 臣 / 白芍 9 佐 / 川芎 6 使，总量 36g）
  // 复算：以最小药量 6g 为 1 → 君:2.0 臣:1.5 佐:1.5 使:1.0；君药占比 12/36=33.3%≥25% → 符合「君药为主」
  "slug": "tcm-pharmacy/jun-chen-zuo-shi",
  "inputs": {
    "formulaSelect": "siwutang"
  },
  "expect": [
    "君:2.0 臣:1.5 佐:1.5 使:1.0",
    "君药剂量占比 33.3%，符合"
  ],
  "ref": "独立复算：totalDose=12+9+9+6=36g；minDose=6 → 比例串「君:2.0  臣:1.5  佐:1.5  使:1.0」（join 用双空格，blob 归一为单空格）；junPct=12/36*100=33.333→toFixed(1) 33.3 ≥25 → 「君药剂量占比 33.3%，符合“君药为主”的组方原则」。默认 formulaSelect 为空 → analyzeClassic 提前 return；select 的 innerHTML 仅含各方名（含《太平惠民和剂局方》），无比例串（原 expect「太平惠民和剂局方」取自 select 选项文本，属逃生项）"
},
{
  // 中成药检索（过滤型）：q=失眠 命中归脾丸/天王补心丸/柏子养心丸/血府逐瘀丸 4 条
  "slug": "tcm-pharmacy/patent-medicine",
  "inputs": {
    "searchInput": "失眠"
  },
  "expect": [
    "食欲不振 🧧 天王补心丸"
  ],
  "ref": "跨卡片相邻串：q=失眠 命中 4 条（归脾丸→天王补心丸→柏子养心丸→血府逐瘀丸）。全量库中归脾丸的下一条是逍遥丸（非天王补心丸），故「食欲不振（归脾丸主治末句）🧧 天王补心丸」仅过滤态成立；后两对在全量库中本就相邻，故意不用（原 expect「30」为 countText 默认全量数，属逃生项）"
},
{
  // 妊娠禁忌检索（过滤型）：q=攻毒杀虫药 命中雄黄/轻粉/砒石/硫黄 4 条
  "slug": "tcm-pharmacy/pregnancy-contraindication",
  "inputs": {
    "searchInput": "攻毒杀虫药"
  },
  "expect": [
    "大毒，蚀疮去腐 🤰 硫黄"
  ],
  "ref": "跨卡片相邻串：q=攻毒杀虫药 命中 4 条（雄黄/轻粉/砒石 禁用 → 硫黄 忌用）。全量库中砒石的下一条是蛇蜕（非硫黄），故「大毒，蚀疮去腐（砒石原因）🤰 硫黄」仅过滤态成立。注意**不能**用「🤰 硫黄 忌用」单卡片串作锚点——硫黄在全量列表中本就存在该串，实测为逃生项；亦不用雄黄→轻粉、轻粉→砒石（二者在全量库中就相邻）（原 expect「63」为 countText 默认全量数，属逃生项）"
},
{
  // ADR 关联性评价（Naranjo 10 题）：checks 声明 10 题均选 value=2 的选项 → 总分 20 → 「肯定」
  // 复算：score=Σ2×10=20 ≥9 → 肯定 + 「该不良反应与药物存在明确的因果关系，建议立即停药并上报」
  "slug": "tcm-pharmacy/tcm-adr-assessment",
  "inputs": {
    "drugName": "雷公藤多苷片",
    "adrDesc": "肝功能异常"
  },
  "checks": [
    "2"
  ],
  "expect": [
    "该不良反应与药物存在明确的因果关系，建议立即停药并上报",
    "可疑药品：雷公藤多苷片",
    "不良反应：肝功能异常"
  ],
  "ref": "独立复算：Naranjo 十题均取 value=2 的选项（第2/4/5题「否」=+2，其余题「是」=+1 之外仅有 0/-1/-2 档；统一取题面 value=2 的选项）→ score=2*10=20 ≥9 → 等级「肯定」+ 结论「该不良反应与药物存在明确的因果关系，建议立即停药并上报」。默认无 checks → 10 题全部未作答 → score=0 → 「可疑」，与本例结论不同；drugName/adrDesc 默认空串故两处回显段也不出现。注：答题读取路径为 querySelector(『input[name=q_i]:checked』)，harness 的 :checked 桩本批补了 parentElement（页面会读 checked.parentElement.textContent 取选项标签），否则该例无法验证。另：assess() 末尾会调 #resultCard.scrollIntoView()（harness 未桩此方法）而抛错，但 #result 的 innerHTML 已在抛错前写入，故断言在下一个候选（copyReport）处命中——结果内容确由 assess() 依 checks 计算得出，不受影响"
},
{
  // 五味（酸苦甘辛咸淡涩）：纯点击答题/标签页，整页无 <input>/<select>/<textarea>，门禁无法注入
  "slug": "tcm-pharmacy/five-flavors",
  "inputs": {},
  "expect": [
    "酸走筋——多食酸则筋脉拘急"
  ],
  "ref": "结构性弱用例（同 DEV-PLAN §10.6 缺陷 G 类）：页面为 7 个 tab 按钮 onclick=selectFlavor(...)，静态 HTML 中不存在任何表单控件（也无 id 可供 harness 建元素触发），门禁只能跑顶层 renderFlavor('酸')。故断言锁定默认「酸」味的确定性内容（五味所走），判别力天然为 0，保留 no_inputs 登记在基线中"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug + " :: " + r.why); }
    catch (e) { fails.push(c.slug + " :: " + e.message); }
  }
  console.log("==== tcm-pharmacy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) { fails.forEach((f) => console.log("  ❌ " + f)); process.exit(1); }
}
if (require.main === module) main();
