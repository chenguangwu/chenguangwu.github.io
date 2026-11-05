#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "clinical-nursing/assessor-pressure-risk",
  "inputs": {
    "position": "5",
    "duration": "5",
    "bmi": "17",
    "age": "78"
  },
  "checkIds": [
    "diabetes",
    "edema"
  ],
  "expect": [
    "【手术体位相关压力性损伤风险评估】 结果：体位 头低脚高位 · 手术时长 5 h · BMI 17 · 年龄 78 岁 → 风险评分 18 分，分级：高风险",
    "重点受压部位：肩部、背部；风险因素：头低脚高位压力集中、手术时长"
  ],
  "ref": "门诊记录：头低脚高位 4 + 时长>4h 4 + 消瘦(BMI<18.5) 3 + 高龄(>70) 3 + 糖尿病 2 + 水肿 2 = 18 分 ⇒ ≥10 高风险；该体位重点受压部位为肩部/背部。默认态仰卧位（1 分）、无勾选 ⇒ 评分远低于 10、分级低风险，与本用例零交集。（风险因素串在「手术时长>5h」处含被 __emrEsc 转义的 &gt;，故 expect 只截到「手术时长」为止。）"
},
{
  "slug": "clinical-nursing/assessor-rater-risk",
  "inputs": {
    "m1": "25",
    "m2": "15",
    "m3": "30",
    "m4": "20",
    "m5": "20",
    "m6": "15"
  },
  "expect": [
    "【Morse 跌倒风险评估（6 项 · 满分 125）】 结果：Morse 总分 125/125 → 分级：高风险",
      ],
  "ref": "门诊记录：6 项全取最高档 25+15+30+20+20+15 = 125 > 50 ⇒「高风险」。默认态 6 项全 0 ⇒「Morse 总分 0/125 → 分级：低风险」，与本用例零交集。"
},
{
  "slug": "clinical-nursing/bag-valve-mask",
  "inputs": {
    "ageGroup": "infant"
  },
  "expect": [
    "【简易呼吸器（球囊-面罩）通气参数】 结果：心肺复苏（CPR） · 婴儿 → 通气频率 20-30 次/分、潮气量 100-150 mL、送气时间 1 秒、送气间隔 2 秒、按压通气比 30:2、球囊 成人型 1500 mL"
      ],
  "ref": "门诊记录：场景默认 CPR、年龄组切婴儿 ⇒ 20-30 次/分（每 2-3 秒 1 次）、潮气量 100-150 mL、间隔 2 秒、按压通气比 30:2，记录附带所选框定球囊容量。默认态为成人 ⇒ 10 次/分、400-600 mL、间隔 6 秒，与本用例零交集。"
},
{
  "slug": "clinical-nursing/bag-valve-mask",
  "inputs": {
    "ageGroup": "infant",
    "bagSize": "adult"
  },
  "expect": [
    "球囊过大：婴儿应选婴儿型(240mL)"
  ],
  "ref": "D-N29 球囊容量参与校验：旧实现完全不读 bagSize，婴儿选成人型(1500mL) 仍静默给出婴儿参数；修复后按年龄与球囊比对给出红字不匹配提示。默认成人+成人型为匹配态，不含该串 ⇒ 强判别、零逃生。"
},
{
  "slug": "clinical-nursing/barthel-index",
  "clicks": [
    "scores.eating=0;scores.bathing=0;scores.grooming=0;scores.dressing=0;scores.bowels=5;scores.bladder=5;scores.toilet=5;scores.transfer=10;scores.walking=10;scores.stairs=5;renderItems();calc()"
  ],
  "expect": [
    "40",
    "大部分ADL需他人帮助，建议加强护理，预防并发症"
  ],
  "ref": "静态量表页(无input)：clicks 页面作用域直写 scores 十项=40 分，落「≥25 重度依赖」分支专属 desc（默认 100 分走「完全自理」、零参兜底 scores[undefined]=undefined→total=NaN 走 else 亦为另一分支，两者均不含该串）。"
},
{
  "slug": "clinical-nursing/braden-score",
  "clicks": [
    "selectScore('sensory',2);selectScore('moisture',2);selectScore('activity',2);selectScore('mobility',2);selectScore('nutrition',2);selectScore('friction',3)"
  ],
  "expect": [
    "每2小时翻身一次"
  ],
  "ref": "静态按钮量表页：逐维 selectScore 到 total=2*5+3=13 落「中度风险(13-14)」分支，其 desc 独有串「每2小时翻身一次」。默认 total=23 走「无风险」；零参兜底 scores[undefined]=undefined→total=NaN 走 else「极度风险」(每1小时翻身)，两态均不含该串（故非逃生项）。"
},
{
  "slug": "clinical-nursing/calc-rater-risk",
  "inputs": {
    "b1": "1",
    "b2": "1",
    "b3": "1",
    "b4": "1",
    "b5": "1",
    "b6": "1"
  },
  "expect": [
    "【Braden 压疮风险评估（6 维度 · 满分 23）】 结果：Braden 总分 6/23 → 分级：极高风险"
      ],
  "ref": "方向敏感（最差态）：6 维全取最低档 1 分 ⇒ 总分 6 ≤9 ⇒「极高风险」。只锚总分结论串，不锚任何单项选项文案（选项文案在静态 HTML 中恒存在，会退化成逃生项）。页面首屏默认感知 3 分、摩擦剪切 2 分（21/23 无风险），兜底回填不会得到 6/23。"
},
{
  "slug": "clinical-nursing/calc-rater-risk",
  "inputs": {
    "b1": "4",
    "b2": "4",
    "b3": "4",
    "b4": "4",
    "b5": "4",
    "b6": "3"
  },
  "expect": [
    "【Braden 压疮风险评估（6 维度 · 满分 23）】 结果：Braden 总分 23/23 → 分级：无风险"
      ],
  "ref": "方向敏感（最好态）：前五项各 4 分、摩擦剪切 3 分 ⇒ 总分 4*5+3=23 ⇒「无风险」，与最差态 6 分/极高风险互斥。只锚总分结论串，不锚单项选项文案；页面首屏默认 21/23，兜底回填（首个选项值）也只得 20/23，均不会命中 23/23。"
},
{
  "slug": "clinical-nursing/chest-compression-depth",
  "inputs": {
    "bodyType": "obese"
  },
  "clicks": [
    "selectAge('child')"
  ],
  "expect": [
    "【胸外按压深度与参数（按年龄）】 结果：对象：儿童（肥胖） → 按压深度 5 cm、频率 100-120 次/分、按压通气比 30:2、回弹要求「完全回弹」、中断 ＜10s",
    "说明：按压深度：约5cm（胸廓前后径1/3）（肥胖患者需加大力度确保达到深度）"
  ],
  "ref": "门诊记录：clicks 调 selectAge('child') 切到儿童（AHA 2020 至少 5 cm，页面统一为 5 cm），inputs 选肥胖体型 ⇒ 追加「肥胖患者需加大力度」。默认态 currentAge='adult'、bodyType='normal' ⇒「对象：成人 → 按压深度 5-6 cm」，与本用例零交集。旧实现输出「4–5 cm」，与同页 desc「约5cm」及 AHA 至少 5 cm 矛盾，已修正。"
},
{
  "slug": "clinical-nursing/chest-compression-depth",
  "clicks": [
    "selectAge('infant')"
  ],
  "expect": [
    "对象：婴儿 → 按压深度 4 cm"
  ],
  "ref": "婴儿按压深度：AHA 2020 至少 4 cm，页面统一为 4 cm（旧实现输出 3–4 cm，与同页 desc「约4cm」矛盾）。clicks 切 infant；默认态成人 5-6 cm ⇒「对象：婴儿 → 按压深度 4 cm」不命中，注入/点击失败即变红。"
},
{
  "slug": "clinical-nursing/cold-compress-timer",
  "inputs": {
    "sensitivity": "diabetic"
  },
  "clicks": [
    "calc()"
  ],
  "ref": "冷敷时长 = 关节基准 20 分钟 × 糖尿病敏感系数 0.5 = 10 分钟；间隔 30 分钟、每日 4–6 次、每 2 分钟查皮肤。默认态 sensitivity=normal ⇒ 20 分钟且走「皮肤耐受正常」提示，与本用例零交集。",
  "expect": [
    "【冷敷时长与皮肤安全评估（关节）】 结果：关节冷敷 · 皮肤条件 糖尿病/感觉减退 → 单次 10 分钟 / 间隔 30 分钟 / 每日 4-6次 / 每2分钟检查皮肤 计算口径：单次时长 = 部位基准（关节/肌肉/四肢/术后 20 分钟、面部 15 分钟）× 皮肤敏感系数（正常 1.0、敏感与老年 0.7、糖尿病 0.5），四舍五入取整 临床提示：皮肤敏感/感觉减退人群：单次冷敷缩短至 10 分钟，结束后必须间隔 30 分钟并检查皮肤；因痛觉与温度觉迟钝，禁止凭主观感觉延长冷敷，出现苍白、发绀、麻木立即停止。 评估日期：__________ 评估者：__________ （自评/筛查量表，结果仅供临床沟通参考，不作为诊断依据）\n"
  ]
},
{
  "slug": "clinical-nursing/convert-flow-concentration",
  "inputs": {
    "mode": "o2f",
    "val": "40"
  },
  "expect": [
    "【氧流量与吸入氧浓度换算】 结果：FiO₂ 40% → 等效氧流量 ≈ 4.75 L/min",
    "较空气（21%）增氧 19.0 个百分点；换算仅适用于鼻导管低流量给氧"
  ],
  "ref": "门诊记录：反算模式 FiO₂ 40% ⇒ (40-21)/4 = 4.75 L/min，增氧 19.0 个百分点。默认态为正向模式（流量 2 L/min ⇒ 29%、增氧 8.0 个百分点），与本用例零交集。"
},
{
  "slug": "clinical-nursing/convert-flow-concentration",
  "inputs": {
    "mode": "f2o",
    "val": "10"
  },
  "expect": [
    "FiO2 ≈ 61.0%（流量 10 L/min）"
  ],
  "ref": "去默认化：FiO2 = 21+4×10 = 61.0%。默认态不命中。"
},
{
  "slug": "clinical-nursing/convert-flow-concentration",
  "inputs": {
    "mode": "o2f",
    "val": "40"
  },
  "expect": [
    "氧流量 ≈ 4.75 L/min（FiO2 40%）"
  ],
  "ref": "去默认化：FiO2 40% ⇒ 流量 = (40−21)/4 = 4.75 L/min。默认态不命中。"
},
{
  "slug": "clinical-nursing/cvc-maintenance",
  "inputs": {
    "lumens": "3",
    "flushType": "heparin100",
    "cathVol": "1.5",
    "extraFlush": "2"
  },
  "expect": [
    "【中心静脉导管（CVC）冲封管方案】 结果：CVC中心静脉导管 · 3 腔 · 封管液 肝素盐水 100 U/mL → 每腔冲管 3.5 mL、总冲管 10.5 mL、总封管 5.4 mL、肝素总量 540 U",
      ],
  "ref": "门诊记录：每腔冲管 = 1.5 + 2 = 3.5 mL，3 腔 ⇒ 总冲管 10.5 mL；封管每腔 1.5×1.2 = 1.8 ⇒ 总封管 5.4 mL；肝素 5.4×100 = 540 U。默认态 1 腔、生理盐水 ⇒ 每腔 3.5、总冲管 3.5、总封管 3.5、无肝素，与本用例零交集。"
},
{
  "slug": "clinical-nursing/cvc-maintenance",
  "inputs": {
    "lumens": "2",
    "flushType": "saline",
    "cathVol": "2",
    "extraFlush": "1"
  },
  "clicks": [
    "currentType='dialysis';calc()"
  ],
  "expect": [
    "封管液 高浓度肝素盐水 1000 U/mL",
    "肝素总量 4,800 U"
  ],
  "ref": "B3 回归：透析导管 + 注入生理盐水封管液（旧实现按 saline 算 ⇒ 肝素 0，错误）。修正后导管类型强制高浓度肝素 1000 U/mL：每腔冲管 2+1=3.0 mL、总冲管 6.0 mL；封管每腔 2×1.2=2.4 ⇒ 总封管 4.8 mL；肝素 4.8×1000=4800 U。默认态 CVC+生理盐水 ⇒ 无肝素，零交集。"
},
{
  "slug": "clinical-nursing/cycle-7",
  "inputs": {
    "ptInput": "12床 李四",
    "startInput": "2026-09-24T08:30"
  },
  "clicks": [
    "selectedType='腕部约束'; selectedSkin='正常'; startRestraint()"
  ],
  "expect": [
    "约束类型：腕部约束 · 皮肤状态：正常"
  ],
  "ref": "门诊记录：clicks 注入 selectedType='腕部约束'（覆盖默认'约束带'）+ selectedSkin='正常' 后 startRestraint() 触发 __cycleEmr，渲染『约束类型：腕部约束 · 皮肤状态：正常』。默认态兜底循环调 __cycleEmr 用页面默认 selectedType='约束带' → 渲染『约束类型：约束带』，与本用例零交集。"
},
{
  "slug": "clinical-nursing/fall-emergency-flow",
  "clicks": [
    "window.__fallSnap=[0,1,2,4,7]; window.__fallEmr()"
  ],
  "expect": [
    "已完成 5/8 关键步骤"
  ],
  "ref": "门诊记录：clicks 注入 window.__fallSnap=[0,1,2,4,7]（完成的步骤索引）后 window.__fallEmr() 渲染『已完成 5/8 关键步骤 + 步骤序号 1,2,3,5,8』。__fallEmr 渲染后 delete window.__fallSnap，兜底循环即便调用也 return；默认态无 __fallSnap → 无任何门诊记录块，零交集。"
},
{
  "slug": "clinical-nursing/gastric-tube-depth",
  "inputs": {
    "noseEar": "14",
    "earXiphoid": "28",
    "extraDepth": "10"
  },
  "expect": [
    "【胃管置入深度测算】 结果：方法：NEX 测量法（鼻尖→耳垂 14 cm + 耳垂→剑突 28 cm + 追加 10 cm）→ 预计置入深度 52 cm",
    "鼻尖→耳垂 14 cm + 耳垂→剑突 28 cm + 追加 10 cm）→ 预计置入深度 52 cm"
  ],
  "ref": "门诊记录：NEX 法 14 + 28 + 10 = 52 cm。默认态 18 + 25 + 10 = 53 cm，与本用例零交集（整串含分段数值，非只差 1 的数字）。"
},
{
  "slug": "clinical-nursing/gastric-tube-depth",
  "inputs": {
    "height": "182",
    "noseXiphoid": "37"
  },
  "clicks": [
    "currentMethod='formula';calc()"
  ],
  "expect": [
    "鼻尖→剑突实测 37 cm + 10 cm",
    "预计置入深度 47 cm"
  ],
  "ref": "B2 回归：身高公式法有实测 NEX 时应按 NEX+10 计算。旧实现 182×0.2+37=73.4 → 73 cm；修正后 37+10=47 cm。默认态（NEX 测量法）18+25+10=53 cm，零交集。"
},
{
  "slug": "clinical-nursing/gastric-tube-depth",
  "inputs": {
    "height": "182",
    "noseXiphoid": ""
  },
  "clicks": [
    "currentMethod='formula';calc()"
  ],
  "expect": [
    "身高 182 cm × 0.25 + 10 cm",
    "预计置入深度 56 cm"
  ],
  "ref": "B2 回归：清空实测 NEX 时不得把空值当 0 或默认 77 混算。旧实现 182×0.2+0=36 cm；修正后身高估算 182×0.25+10=55.5 → 56 cm。默认态 53 cm，零交集。"
},
{
  "slug": "clinical-nursing/generator-pressure",
  "inputs": {
    "cnt": "10"
  },
  "expect": [
    "生成结果：共 6 条"
  ],
  "ref": "上限封顶：cnt=10 只允许 6 个分期各 1 条，输出「共 6 条」；默认 cnt=5 输出「共 5 条」，判别器清空 inputs 亦为 5 条 ⇒ 非逃生项，且不抓 Math.random 随机内容。"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "250",
    "hours": "3",
    "minutes": "45",
    "dropFactor": "20"
  },
  "expect": [
    "【静脉输液滴速推算】 结果：总量 250 mL / 滴系数 20 滴/mL，输注时间 3 小时 45 分（共 225 分钟）→ 滴速 22 滴/分、输液泵 66.7 mL/h、总滴数 5,000 滴（每秒约 0.4 滴）",
    "总滴数 5,000 滴（每秒约 0.4 滴）"
  ],
  "ref": "门诊记录：250 mL × 20 滴/mL ÷ 225 分钟 = 22.2 → 22 滴/分；泵速 250/225×60 = 66.7 mL/h；总滴数 5000。默认态 500 mL / 4 h / 20 滴/mL ⇒ 42 滴/分、125.0 mL/h、10,000 滴，与本用例零交集。"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "500",
    "hours": "",
    "minutes": "",
    "dropFactor": "20"
  },
  "expect": ["【静脉输液滴速推算】 结果：参数不完整"],
  "ref": "D-N11 清空时间：totalMinutes = 0×60+0 = 0 ⇒ 旧实现结果区置 --，但 window.__EMR_SUM 未清空，EMR 记录继续沿用上一次「125.0 mL/h / 10,000 滴」；修复后置空并写入「参数不完整」新记录，旧滴速不再沿用。默认 hours=4/minutes=0 有效，不含该串 ⇒ 判别力成立。"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "500",
    "hours": "4",
    "minutes": "0",
    "dropFactor": "60"
  },
  "expect": ["结果：总量 500 mL / 滴系数 60 滴/mL", "当前 125 滴/分、泵速 125 mL/h 在常规范围"],
  "ref": "D-N11 阈值随滴系数失真：500 mL/4 h、60 滴/mL ⇒ 125 mL/h、125 滴/分。旧实现按 dr>60 判「偏快」（125 滴/分），但泵速 125 mL/h 属常规（20 滴/mL 换算约 42 滴/分）。修复后按泵速 mL/h 判定 ⇒ 常规范围；默认 df=20 时记录为「滴系数 20 滴/mL」，不含 60 串 ⇒ 判别力成立。"
},
{
  "slug": "clinical-nursing/iv-drip-rate",
  "inputs": {
    "volume": "300",
    "hours": "1",
    "minutes": "0",
    "dropFactor": "20"
  },
  "expect": ["约合 20 滴/mL 输液器 60 滴/分以上"],
  "ref": "D-N11 上阈值复核：300 mL/1 h ⇒ 泵速 300 mL/h > 180，判偏快（旧实现按 300 滴/分 > 60 也判偏快，结论一致，用于锁定新口径不丢偏快分支）。默认 125 mL/h 不命中。"
},
{
  "slug": "clinical-nursing/morse-score",
  "clicks": [
    "selectScore('history',25);selectScore('gait',10)"
  ],
  "expect": [
    "保持病区环境安全"
  ],
  "ref": "静态按钮量表页：selectScore 到 total=25+10=35 落「低度跌倒风险(25-44)」分支，其 desc 独有串「保持病区环境安全」。默认全 0 走「无跌倒风险」；零参兜底 total=NaN 落 else「高度跌倒风险」，两态均不含该串。"
},
{
  "slug": "clinical-nursing/morse-score",
  "clicks": [
    "selectScore('history',25);selectScore('gait',20)"
  ],
  "expect": [
    "45"
  ],
  "ref": "Morse 1989 原版切点 ≥45 为高度风险：25+20=45 必须落「高度跌倒风险」；旧实现以 >50 为高危会把 45 误判为低危。锚定 totalNum=45（注入失败时默认 0 或兜底 NaN→—，均不含 45），与高危 desc 的 NaN 兜底不可分，故不用 desc。"
},
{
  "slug": "clinical-nursing/ostomy-bag-timing",
  "inputs": {
    "stomaType": "ileostomy",
    "outputType": "liquid",
    "baseStatus": "leak"
  },
  "clicks": ["calc()"],
  "expect": [
    "造口类型：回肠造口 · 内容物：稀便 · 当前状态：已渗漏 · 建议更换间隔：立即"
  ],
  "ref": "双态零交集：expect 锚定注入的造口类型/内容物/状态组合（leak→间隔立即）。判别器清空 inputs（默认 colostomy/formed/intact → 间隔 7 天）→ 不命中 ⇒ 非逃生项。不抓 new Date() 动态倒计时。"
},
{
  "slug": "clinical-nursing/oxygen-concentration",
  "inputs": {
    "flowRate": "5"
  },
  "expect": [
    "【吸氧装置与浓度换算】 结果：装置：鼻导管 · 流量 5 L/min → FiO₂ 约 41%（鼻导管5L/min对应FiO2约41%）",
    "该装置适用流量 1–6 L/min、最高 FiO₂ 44%；湿化：≤4L不需，＞4L需湿化；估算 PaO₂ 约 205 mmHg"
  ],
  "ref": "门诊记录：鼻导管 FiO₂ = 21 + 4×5 = 41%（上限 44% 未触发）；PaO₂ 估算 41×5 = 205 mmHg。默认态 flowRate=2 ⇒ 29%、PaO₂ 145，与本用例零交集。注：原实现把 `pao2` 暴露给记录钩子时该变量尚未定义（null），已改为在钩子里按 fio2×5 直接计算。"
},
{
  "slug": "clinical-nursing/oxygen-concentration",
  "inputs": {
    "flowRate": "12"
  },
  "expect": [
    "鼻导管12L/min对应FiO2约69%",
    "＞6L/min 超出鼻导管可靠范围",
    "建议改用普通面罩或高流量鼻导管"
  ],
  "ref": "鼻导管不再静默封顶 44%：FiO₂ = 21 + 4×12 = 69%（原实现显示 44%）；流量＞6 L/min 触发警示并建议改面罩。默认态 flowRate=2 ⇒ 28% 且无警示，三串均不命中。"
},
{
  "slug": "clinical-nursing/pain-nrs",
  "clicks": [
    "selectPain(7)"
  ],
  "expect": [
    "NRS 7/10 → 疼痛等级：重度疼痛"
  ],
  "ref": "门诊记录：clicks 调 selectPain(7)（页面 selectPain 被 wrapper 包住，finally 触发 __emrData 渲染），REC 内 typeof score==='number' 守卫挡住兜底无参调用覆盖，输出「NRS 7/10 → 重度疼痛」。默认态 __EMR_S 未赋值 ⇒「NRS 0/10 → 无痛」，零交集。"
},
{
  "slug": "clinical-nursing/pressure-injury-description",
  "inputs": {
    "woundL": "6",
    "woundW": "2",
    "woundD": "0.5",
    "exudate": "中等量浆液性",
    "surrounding": "红斑"
  },
  "clicks": [
    "selectStage(\"3\",{classList:{add:function(){}}})"
  ],
  "expect": [
    "3期压力性损伤 · 创面 6×2×0.5cm · 渗出液 中等量浆液性 · 周围皮肤 红斑"
  ],
  "ref": "门诊记录：clicks 调 selectStage('3', 哑 btn)（第二参需 classList.add），REC 内 typeof st==='string' 守卫；创面尺寸由 woundL/W/D 拼出 6×2×0.5cm，3 期才输出渗出液与周围皮肤。默认态 currentStage='1' 且页面末尾 generate() 时 __EMR_S 未赋值 ⇒ guard 直接 return、不产生门诊记录，零交集。原 expect「6cm」属输入回显（零判别力），已废弃。注：本页部位来自 querySelectorAll('#locationCheck input:checked')，stub 下会误返回全部 select 默认值，故门诊记录不含部位、留「损伤部位：____」手填。"
},
{
  "slug": "clinical-nursing/reminder-time-1",
  "inputs": {
    "coldDur": "15",
    "restDur": "45",
    "checkDur": "8"
  },
  "clicks": [
    "selectedArea='踝关节'; __reminderEmr()"
  ],
  "expect": [
    "部位：踝关节"
  ],
  "ref": "门诊记录：clicks 注入 selectedArea='踝关节'（覆盖默认'额头'）后 __reminderEmr() 渲染『部位：踝关节』。默认态兜底循环调 __reminderEmr 用页面默认 selectedArea='额头' → 渲染『部位：额头』，与本用例零交集。"
},
{
  "slug": "clinical-nursing/restraint-check",
  "clicks": [
    "checkedState[\"wrist\"]={0:true,1:true,2:true,3:true,4:true};updateResult();"
  ],
  "expect": [
    "已完成 5/7 项检查 → 未完成，不得视为安全"
  ],
  "ref": "门诊记录：clicks 直接写 checkedState.wrist 前 5 项为 true 后调 updateResult()，REC 就地统计已勾选数（原写法读函数内 checkedCount 因 var 提升恒为 undefined，已改为按 checkedState 现算），输出「已完成 5/7 项检查 → 未完成」。默认态 0/7 ⇒「已完成 0/7 项检查」，零交集。"
},
{
  "slug": "clinical-nursing/restraint-duration",
  "inputs": {
    "startTime": "08:00",
    "totalHours": "4"
  },
  "clicks": ["currentType='chest'; calc();"],
  "expect": [
    "约束类型：胸衣约束 · 松解间隔：每 2 小时"
  ],
  "ref": "双态零交集：expect 锚定注入的约束类型 chest（胸衣约束）。判别器清空 clicks（默认 currentType=wrist → 手腕约束）→ 不命中 ⇒ 非逃生项。不抓 new Date() 动态时刻。"
},
{
  "slug": "clinical-nursing/suction-pressure",
  "inputs": {
    "currentPressure": "260"
  },
  "expect": [
    "当前负压 260 mmHg（≈34.6 kPa）→ 超过安全范围"
  ],
  "ref": "门诊记录：inputs 写 260 mmHg（页面默认 150，已非安全值），REC 在 evaluate(p) 处捕获 typeof p==='number' 守卫后的压力值与患者类别，输出「成人 · 安全范围 80–120 · 当前负压 260 mmHg（≈34.6 kPa）→ 超过安全范围」并给出黏膜损伤临床提示。默认态 150 mmHg（≈20.0 kPa）数值串不同，零交集。"
},
{
  "slug": "clinical-nursing/suction-pressure",
  "inputs": {
    "currentPressure": "130"
  },
  "expect": [
    "患者类别 成人 · 安全范围 80–120 mmHg · 当前负压 130 mmHg（≈17.3 kPa）→ 超过安全范围（黏膜损伤风险）"
  ],
  "ref": "W1-B 回归：AARC 成人推荐 80–120 mmHg，130 mmHg 属过高。输入 130 非默认（150）；旧实现成人区间 150–200 ⇒ 判「在安全范围内」，本串不命中。"
},
{
  "slug": "clinical-nursing/suction-pressure",
  "inputs": {
    "currentPressure": "110"
  },
  "clicks": [
    "selectAge('child',{classList:{add:function(){}}})"
  ],
  "expect": [
    "患者类别 儿童 · 安全范围 80–100 mmHg · 当前负压 110 mmHg（≈14.6 kPa）→ 超过安全范围（黏膜损伤风险）"
  ],
  "ref": "W1-B 回归：年龄选择必须真正改变区间。clicks 切儿童（80–100 mmHg）后 110 mmHg 属过高；旧实现儿童 100–150 ⇒ 判「在安全范围内」，本串不命中。输入 110 非默认（150）。"
},
{
  "slug": "clinical-nursing/surgical-position-risk",
  "clicks": [
    "selectPosition(\"lithotomy\",{classList:{add:function(){}}})"
  ],
  "expect": [
    "体位 截石位压力点评估 · 压力点共 4 处（高 2 / 中 1 / 低 1）"
  ],
  "ref": "门诊记录：clicks 调 selectPosition('lithotomy', 哑 btn)（第二参需 classList 否则抛错），REC 内 typeof pos==='string' 守卫，输出截石位 4 个压力点的高/中/低分布。默认 supine ⇒「仰卧位压力点评估 · 压力点共 5 处（高 3 / 中 2 / 低 0）」，零交集。"
},
{
  "slug": "clinical-nursing/tracheostomy-dressing",
  "inputs": {
    "firstDressing": "08:00"
  },
  "clicks": ["currentLevel='heavy'; calc();"],
  "expect": [
    "分泌物评估：大量分泌物 · 换药间隔：每 4 小时"
  ],
  "ref": "双态零交集：expect 锚定注入的分级 heavy（大量分泌物）。判别器清空 clicks（默认 currentLevel=minimal → 微量分泌物）→ 不命中 ⇒ 非逃生项。不抓 new Date() 动态时刻，只锚分级/间隔/次数。"
}
  ,{
    "slug": "clinical-nursing/braden-score",
    "clicks": ["selectScore('sensory',1);selectScore('moisture',1);selectScore('activity',1);selectScore('mobility',1);selectScore('nutrition',1);selectScore('friction',1);calc()"],
    "expect": [
      "【Braden 压疮风险评估（6 维度）】 结果：总分 6/23，分级：极度风险",
      "满分（各条目最高分之和）23；得分率 26%；条目明细见上"
    ],
    "ref": "门诊记录（EMR note）：6 个维度各取最低档 1 分 ⇒ 总分 6 <10 落「极度风险」；满分 23 = 4+4+4+4+4+3，得分率 6/23≈26% ⇒ 建议每 1 小时翻身。默认态各维度取最高档（4/4/4/4/4/3=23）⇒「总分 23/23，分级：无风险」「得分率 100%」，与本用例零交集。"
  }
  ,{
    "slug": "clinical-nursing/morse-score",
    "clicks": ["selectScore('history',25);selectScore('diagnosis',15);selectScore('aid',30);selectScore('iv',20);selectScore('gait',20);selectScore('cognition',15);calc()"],
    "expect": [
      "【Morse 跌倒风险评估（6 维度）】 结果：总分 125/125，分级：高度跌倒风险",
      "满分（各条目最高分之和）125；得分率 100%；条目明细见上"
    ],
    "ref": "门诊记录：6 维度全取最高档 25+15+30+20+20+15=125 ⇒ >50 落「高度跌倒风险」；满分 125、得分率 100%。默认态全 0 ⇒「总分 0/125，分级：无跌倒风险」「得分率 0%」，零交集。"
  }
  ,{
    "slug": "clinical-nursing/barthel-index",
    "clicks": ["selectScore('eating',0);selectScore('bathing',0);selectScore('grooming',0);selectScore('dressing',0);selectScore('bowels',0);selectScore('bladder',0);selectScore('toilet',0);selectScore('transfer',0);selectScore('walking',0);selectScore('stairs',0);calc()"],
    "expect": [
      "【Barthel 指数（ADL · 10 项 · 满分 100）】 结果：总分 0/100，分级：完全依赖",
      "满分（各条目最高分之和）100；得分率 0%；条目明细见上"
    ],
    "ref": "门诊记录：10 项全取最低档 0 分 ⇒ 总分 0 <25 落「完全依赖」；满分 100 = 10+5+5+10+10+10+10+15+15+10。默认态为各维度最高档（满分 100）⇒「总分 100/100，分级：完全自理」「得分率 100%」，零交集。"
  },
  {
    "slug": "clinical-nursing/reminder-time-1",
    "inputs": { "restDur": "45" },
    "expect": ["休息 45 分钟"],
    "ref": "单字段注入（2026-11-05 补 oninput）：冷敷方案预览默认「休息 30 分钟」，仅改休息间隔 45 分即实时刷新为「休息 45 分钟」；默认态不含该串 ⇒ 强判别。计时开始后（state.running）预览不覆盖运行中状态。"
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

  console.log("==== clinical-nursing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
