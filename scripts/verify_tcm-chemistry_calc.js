#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "tcm-chemistry/calc-44",
  "inputs": {
    "K": "7",
    "v0": "100",
    "v": "25",
    "target": "99"
  },
  "expect": ["4.552358675"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/capsule-filling",
  "inputs": {
    "height": "45",
    "diameter": "80",
    "bulkDensity": "0.5",
    "tapDensity": "0.7",
    "targetWeight": "300",
    "fillDensity": "0.5",
    "moisture": "5"
  },
  "expect": [
    "arctan(45/40.0)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/chromatography-gradient",
  "inputs": {
    "colDiameter": "6",
    "sampleWeight": "2"
  },
  "expect": ["alkaloid\n1:50\n6\n2\n硅胶柱层析方案 6 柱径(cm) 7.1 装柱高度(cm) 200 柱体积BV(mL) 100 硅胶用量(g) 装柱参数： 1:50 硅胶（100g），柱径6cm，装柱高度约7.1cm，柱体积约200mL（1BV）。 注意： 柱高/柱径比建议≥10:1，当前为1.2:1，建议减小柱径或增加硅胶量。 梯度洗脱方案（生物碱） 洗脱体系：石油醚 → 乙酸乙酯 1 2 3 4 5 6 7 1 石油醚 : 乙酸乙酯 = 100:0 洗脱体积：2-3BV（约400 mL）| 目标：极性杂质/色素 2 石油醚 : 乙酸乙酯 = 90:10 洗脱体积：2BV（约400 mL）| 目标：低极性生物碱 3 石油醚 : 乙酸乙酯 = 80:20 洗脱体积：2BV（约400 mL）| 目标：中等极性生物碱 4 石油醚 : 乙酸乙酯 = 70:30 洗脱体积：2BV（约400 mL）| 目标：中等极性生物碱 5 石油醚 : 乙酸乙酯 = 50:50 洗脱体积：3BV（约600 mL）| 目标：高极性生物碱 6 石油醚 : 乙酸乙酯 = 0:100 洗脱体积：3BV（约600 mL）| 目标：强极性生物碱 7 石油醚 : 乙酸乙酯 = MeOH冲洗 洗脱体积：2BV（约400 mL）| 目标：残留强极性成分 改性建议： 可加0.5%-1%二乙胺改性 操作要点： 1. 硅胶活化：105°C活化30min 2. 干法/湿法装柱，确保无气泡、无裂痕 3. 上样浓度10%-20%，尽量薄层 4. 流速控制：1-2 BV/h 5. 每BV收集1管，TLC监控合并"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/concentration-calc",
  "inputs": {
    "targetTemp": "75",
    "vacuum": "",
    "atm": "760"
  },
  "expect": [
    "288.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/content-assay",
  "inputs": {
    "stdMass": "15",
    "stdConc": "0.50",
    "isMass": "8.00",
    "isConc": "0.40",
    "stdArea": "500000",
    "isArea": "450000",
    "factor": "0.889",
    "sampleMass": "500",
    "sampleIS": "8.00",
    "sampleVol": "25",
    "sampleArea": "480000",
    "sampleISArea": "440000",
    "lossOnDrying": "0"
  },
  "expect": [
    "15"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "tcm-chemistry/crystallization-yield",
  "inputs": {
    "feedAmount": "15",
    "dissolveTemp": "70",
    "crystalTemp": "10",
    "solHigh": "8.5",
    "solLow": "0.8",
    "solventVol": "120",
    "lossRate": "5"
  },
  "expect": [
    "120mL溶剂在70°C仅能溶10.20g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/detector-4",
  "inputs": {
    "herb1": "甘草_X",
    "herb2": "甘遂"
  },
  "expect": [
    "甘草_X"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "tcm-chemistry/extraction-counts",
  "inputs": {
    "K": "8",
    "ratio": "0.5",
    "target": "95",
    "total": "100"
  },
  "expect": [
    "1/(1+8×0.5)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/extraction-solvent",
  "inputs": {
    "compoundType": "alkaloid_salt"
  },
  "expect": [
    "可用0.5%-1%盐酸/硫酸乙醇溶液提取"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/fingerprint-similarity",
  "inputs": {
    "refData": "80,120,60,40,25",
    "s1": "82,118,62,38,26",
    "s2": "70,140,50,55,20",
    "s3": "95,100,80,30,35",
    "s4": "60,150,45,60,15"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.9547",
    "0.8863",
    "0.9380 平均相关系数"
  ],
  "ref": "独立复算 Pearson：ref 均值 65（dx=15,55,−5,−25,−40，Σdx²=5500）；"
     + "s2 均值 67（dy=3,73,−17,−12,−47，Σdy²=7980），Σdxdy=6325 ⇒ r=6325/√(5500×7980)=0.9547；"
     + "s3 均值 68（dy=27,32,12,−38,−33，Σdy²=4430），Σdxdy=4375 ⇒ r=4375/√(5500×4430)=0.8863；"
     + "四样平均=(0.9985+0.9547+0.8863+0.9126)/4=0.9380。原 7 峰数据为页面默认态。",
},
{
  "slug": "tcm-chemistry/granule-quality",
  "inputs": {
    "totalWt": "150",
    "s1": "2",
    "s2": "15",
    "s3": "55",
    "s4": "20",
    "s5": "5",
    "s6": "3",
    "moisture": "4.0",
    "rsd": "3.0",
    "assay": "98",
    "sizeScore": "5"
  },
  "expect": [
    "2680"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "inputs": {
    "colLength": "375",
    "colID": "4.6",
    "flowRate": "1.0",
    "t0": "2.5",
    "kPrime": "3.0",
    "gradSlope": "0",
    "rt_plate": "10.5",
    "peakWidth": "0.5",
    "t0_plate": "2.5",
    "L_plate": "250",
    "tr1": "8.5",
    "tr2": "10.2",
    "w1": "0.4",
    "w2": "0.5"
  },
  "expect": [
    "6.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/impurity-limit",
  "inputs": {
    "sampleWt": "150",
    "sampleVol": "10",
    "stdWt": "1",
    "stdVol": "10",
    "sampleSpot": "10",
    "stdSpot": "10",
    "sampleSpotIntensity": "3",
    "stdSpotIntensity": "5",
    "stdConcSemi": "0.1",
    "sampleAmount": "100"
  },
  "expect": [
    "0.150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/metabolite-prediction",
  "inputs": {
    "mw": "405"
  },
  "expect": [ "243 脱糖基", "421 羟基化", "581 葡萄糖醛酸化" ],
  "ref": "MW=405（黄芩苷）按官能团质量差独立复算：脱糖基 −162（葡萄糖基 C₆H₁₀O₅）⇒ 243；羟基化 +16 ⇒ 421；葡萄糖醛酸化 +176 ⇒ 581。默认态 MW=270 ⇒ 108 / 286 / 446，三串均不命中。旧断言 229 为误用 −176（那是葡萄糖醛酸加合的质量差）所致。"
},
{
  "slug": "tcm-chemistry/metabolite-prediction",
  "inputs": {
    "mw": "10"
  },
  "expect": [ "— 去甲基" ],
  "ref": "MW=10：旧实现去甲基直接算 10−14=−4 并显示负分子量；现与脱糖基/脱水一致，非正值显示「—」。默认 MW=270 ⇒ 256，不命中。"
},
{
  "slug": "tcm-chemistry/ointment-release",
  "inputs": {
    "concA": "30",
    "solCs": "5",
    "diffD": "0.001",
    "time": "6",
    "thickness": "0.1"
  },
  "expect": [
    "((2×30-5)×5×0.00050×6)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/pharmacokinetics",
  "inputs": {
    "dose": "150",
    "bio": "50",
    "vd": "50",
    "cl": "5",
    "ka": "1.0",
    "tau": "12",
    "weight": "60"
  },
  "expect": [
    "(75.00×1)/(50×0.9000)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/response-factor",
  "inputs": {
    "refName": "黄芩苷",
    "refConc": "3.1",
    "refArea": "500000",
    "cn${i}": "${d.name}",
    "cc${i}": "${d.conc}",
    "ca${i}": "${d.area}",
    "cq${i}": "${(d.conc*10).toFixed(2)}"
  },
  "expect": [
    "161290"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/solubility-guide",
  "inputs": {
    "searchBox": "zzz"
  },
  "expect": [
    "未找到匹配成分"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部成分，不产此串）"
},
{
  "slug": "tcm-chemistry/stability-test",
  "inputs": {
    "ea": "125.14",
    "accelTemp": "40",
    "accelTime": "6",
    "storageTemp": "25",
    "accelDeg": "2.5",
    "accelMonths": "6",
    "interDeg": "1.0",
    "interMonths": "12",
    "specLimit": "10"
  },
  "expect": [
    "125.1×1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/structure-identification",
  "inputs": {
    "irInput": "3420, 2925, 1710, 1610, 1510, 1455, 1275, 1075",
    "uvInput": "228, 268, 305",
    "nmrInput": "12.6, 9.9, 7.6, 7.2, 6.8, 6.4, 3.9",
    "msM": "406",
    "msFrag": "243, 225, 153, 125, 97"
  },
  "expect": [
    "输入8个吸收峰，识别出10个特征基团 📊 特征峰归属 3420 cm⁻¹ → O-H 伸缩振动（羟基/酚羟基） 宽峰为缔合OH，尖峰为游离OH 3420 cm⁻¹ → N-H 伸缩振动（胺/酰胺）",
    "228 nm → 共轭二烯/α,β-不饱和酮 共轭体系强吸收",
    "δ 12.6 ppm → 羧基 -COOH / 酚OH(分子内氢键)（活泼氢）",
    "含芳环（3个芳氢）",
    "406 分子离子峰[M]⁺ 5 碎片峰数 163 最大中性丢失"
  ],
  "ref": "去默认化：inputs 全组换成非默认值（默认为 3400/220/12.5/270）。3420 命中 O-H 伸缩，锁定 range 降序归一化修复——修复前 [3600,3200] 等降序项永不匹配，只识别出 2 个基团；修复后识别出 10 个（默认组 11 个，数量与峰位双维度均可判）"
},
{
  "slug": "tcm-chemistry/toxicity-dose",
  "inputs": {
    "dose": "750",
    "humanWeight": "60",
    "ld50": "500"
  },
  "expect": ["mouse\nhuman\n750\nbsa\n60\n100\n等效剂量换算 750 小鼠 LD50(mg/kg) 60.81 人等效(mg/kg) 60.81 人等效剂量(mg/kg) 0.6081 安全起始剂量(mg/kg) 换算结果： 小鼠 LD50 = 750 mg/kg 体表面积法：Dose₂ = Dose₁ × (Km₁/Km₂) = 750 × (3/37) 人 等效剂量 = 60.81 mg/kg 人体等效剂量(HED)估算： HED = 动物剂量 × (Km动物 / Km人) = 750 × (3/37) = 60.81 mg/kg 安全起始剂量(MRD) = HED / 安全系数 = 60.81 / 100 = 0.6081 mg/kg 60kg成人总剂量 = 0.6081 × 60 = 36.49 mg 安全系数说明： ×10：同种动物重复实验，毒性明确 ×100：常规新药研究（默认） ×1000：毒性未知或高毒性物质 注意：实际临床起始剂量还需考虑药效学、药代学数据 常用Km值参考： 小鼠Km=3 (20g) | 大鼠Km=5.9 (150g) | 豚鼠Km=8 (400g) 家兔Km=12 (1.8kg) | 犬Km=20 (10kg) | 人Km=37 (60kg)\n500\noral\n毒性分级结果 500 LD50(mg/kg) 口服 给药途径 中等毒 毒性等级 毒性分级： 中等毒 需较大剂量才致命，如小檗碱(LD50约~400mg/kg) WHO经口急性毒性分级表 分级 LD50(mg/kg) 说明 剧毒 ≤1 极微量致命 高毒 1-50 少量致命 中等毒 50-500 较大剂量致命 低毒 500-5000 相对安全 微毒/无毒 >5000 基本无毒 中药常见毒性成分参考： 乌头碱 LD50≈0.3mg/kg(剧毒) | 士的宁 LD50≈2mg/kg(高毒) 马钱子碱 LD50≈50mg/kg(高毒) | 苦参碱 LD50≈150mg/kg(中等毒) 小檗碱 LD50≈400mg/kg(中等毒) | 黄芩苷 LD50>5000mg/kg(无毒)"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/compatibility-taboo",
  "clicks": ["document.getElementById('herbA').value='乌头';document.getElementById('herbB').value='半夏';checkClassic()"],
  "expect": ["乌头 与 半夏", "乌头组"],
  "ref": "⚠ 该页两个 select 的选项由 initHerbs() 在 DOMContentLoaded 时填充，而 harness step-3 兜底会再调 initHerbs ⇒ inputs 字段注入会被冲回默认（甘草/甘遂）。改用 clicks 在页面作用域设值并直接调 checkClassic()（step-2.5 立即判定，不等 step-3）。注入「乌头 + 半夏」命中十八反乌头组（乌头反半夏/瓜蒌/贝母/白蔹/白及）⇒ 输出『禁止配伍！乌头 与 半夏 属于 十八反』。⚠ expect 只取『乌头 与 半夏』+『十八反』：默认态（甘草/甘遂）虽也含『十八反』，但不含『乌头 与 半夏』，判别器实测两条均会变红（OR 语义下同态需全部命中才逃生）。"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "clicks": ["document.getElementById('t0').value='1.2';document.getElementById('kPrime').value='5';document.getElementById('gradSlope').value='2';calcRT();"],
  "expect": ["梯度参数不适用", "早于死时间"],
  "ref": "第1071批 N145：短柱梯度预设 t0=1.2/k=5/slope=2 ⇒ tR_grad=1.2×6/7=1.03 < t0=1.2，物理上不可能。旧版照常渲染「梯度保留时间 1.03 min」无警示；新版 tR_grad<t0 时输出「⚠️ 梯度参数不适用…早于死时间 t₀」警示。默认 slope=0 走等度不触发 ⇒ 依赖 inputs 注入，强判别零逃生。"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "clicks": ["document.getElementById('rt_plate').value='2';document.getElementById('t0_plate').value='2.5';document.getElementById('peakWidth').value='0.5';calcPlate();"],
  "expect": ["保留时间 tR 须大于死时间"],
  "ref": "第1071批 N147：tR=2 < t0=2.5 ⇒ k′=(2−2.5)/2.5=−0.2 无物理意义。旧版仍渲染「有效塔板数 16」；新版 calcPlate 开头校验 tR>t0>0&&W>0&&L>0，不满足则提示「保留时间 tR 须大于死时间 t₀」并停算。默认 tR=2.5/t0=2.5 相等也不满足（须严格大于），但默认实际值不同 ⇒ 依赖 clicks 注入，强判别。"
},
{
  "slug": "tcm-chemistry/solubility-guide",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-chemistry/solubility-guide.html','utf8');var n=h.split('let rows = filterRows();').length-1;var ok=h.indexOf('function filterRows()')>=0&&n===2&&h.indexOf('导出明细 CSV')<0;document.getElementById('__tbProbe').textContent='SOLFILTER '+(ok?'OK':'BAD');"],
  "expect": ["SOLFILTER OK"],
  "ref": "12-N110 表格/导出筛选口径统一：filterRows 同时匹配名称/来源/类别，renderTable 与 exportData 各复用一次；空结果态误导性的历史导出按钮移除。旧版 exportData 只按名称且空态按钮存在 ⇒ 变红。默认态不产生该串，零逃生。"
},
{
  "slug": "tcm-chemistry/solubility-guide",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-chemistry/solubility-guide.html','utf8');var deep=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/tcm-chemistry/solubility-guide.json','utf8');var parts=h.split('<script');var fb='';for(var k=1;k<parts.length;k++){var seg=parts[k].split('</script>')[0];if(seg.indexOf('FAQPage')>=0){fb=seg.slice(seg.indexOf('{'),seg.lastIndexOf('}')+1);break;}}var q=null;try{q=JSON.parse(fb);}catch(e){}var ans=q&&q.mainEntity&&q.mainEntity[0]?q.mainEntity[0].acceptedAnswer.text:'';var vis=h.indexOf('易溶/溶解/微溶/难溶/不溶五级')<0&&h.indexOf('本页按四级简化')>=0;var src=deep.indexOf('易溶/溶解/微溶/难溶/不溶五级')<0&&deep.indexOf('本页按四级简化')>=0;var enok=en.indexOf('Five grades: freely soluble')<0&&en.indexOf('four simplified grades')>=0;var ok=ans.indexOf('四级')>=0&&ans.indexOf('七级')>=0&&ans.indexOf('五级')<0&&vis&&src&&enok;document.getElementById('__tbProbe').textContent='SOLFAQ '+(ok?'OK':'BAD');"],
  "expect": ["SOLFAQ OK"],
  "ref": "第283批：页面正文、可见 FAQ、FAQPage、深解数据源与英文词典必须统一为“本页四级简化 vs 药典七级”，不得再出现“易溶/溶解/微溶/难溶/不溶五级”。旧版 FAQ/LD/源 JSON/英文均写五级 ⇒ BAD。"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-chemistry/hplc-optimization.html','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/tcm-chemistry/hplc-optimization.json','utf8');var ok=h.indexOf('基于权威医学标准')<0&&h.indexOf('支持多种临床参数')<0&&h.indexOf('医疗数据不上传，保护隐私')<0&&h.indexOf('临床计算与评估辅助')<0&&h.indexOf('医学学习与考试备考')<0&&h.indexOf('健康监测参考')<0&&h.indexOf('按 HPLC 参数计算保留时间、柱效与分离度')>=0&&h.indexOf('支持等度与梯度洗脱条件评估')>=0&&h.indexOf('分析方法开发与色谱条件筛选')>=0&&h.indexOf('实验结果复核与方案比较')>=0&&en.indexOf('Compute retention time, column efficiency and resolution from HPLC parameters')>=0&&en.indexOf('Supports isocratic and gradient elution evaluation')>=0&&en.indexOf('Parameters are processed only in the browser and are never uploaded')>=0;document.getElementById('__tbProbe').textContent='HPLCINTRO '+(ok?'OK':'BAD');"],
  "expect": ["HPLCINTRO OK"],
  "ref": "12-N146：HPLC 工具简介残留医疗/临床话术（基于权威医学标准、临床参数、医疗数据、健康监测等），与分析化学定位不符。修复后功能特点与使用场景全部改为色谱方法开发口径，并在本页 en map 补齐新键避免英文态 CJK 残留；旧版任一医疗串命中即红。"
},
{
  "slug": "tcm-chemistry/metabolite-prediction",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tcm-chemistry/metabolite-prediction.html','utf8');var zh=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/tcm-chemistry.json','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/tcm-chemistry/metabolite-prediction.json','utf8');var ok=h.indexOf('预测 I 相与 II 相代谢产物')>=0&&h.indexOf('输入中药成分结构')<0&&h.indexOf('外用给药代谢特点')>=0&&h.indexOf('给药途径只影响以上提示；下方 I/II 相反应按化合物类别给出，不随途径变化。')>=0&&zh.indexOf('不解析结构式，结果需实验验证')>=0&&en.indexOf('Topical route:')>=0&&en.indexOf('The route only affects the note above')>=0;document.getElementById('__tbProbe').textContent='METABI '+(ok?'OK':'BAD');"],
  "expect": ["METABI OK"],
  "ref": "12-N92/N94/N95：meta/标题不再承诺结构输入（页面说明与公式框均声明不解析结构式），标题补全 I 相与 II 相；给药途径补外用分支并明示下方类别模板不随途径变化，中英源同步。旧版旧结构输入串命中、标题截断、无外用提示 ⇒ 变红；默认态不产生该哨兵，零逃生。"
},
{
  "slug": 'tcm-chemistry/compatibility-taboo',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/tcm-chemistry/compatibility-taboo.html\',\'utf8\');var i=h.indexOf(\'function switchTab(name, btn){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!name||!btn)\')>=0&&seg.indexOf(\'checkClassic(); checkPhyschem(); return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'TMCCF0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['TMCCF0 OK'],
  "ref": "第1336批·历史恢复无参切换函数抛错修复源码形态强锚：旧版 function switchTab(name, btn){ 无参调用解引用参数抛错被 catch 吞、结果不重算；修复后无参分支安全重算本页主结果并 return。旧版无 ⇒ BAD。"
},
{
  "slug": 'tcm-chemistry/structure-identification',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/tcm-chemistry/structure-identification.html\',\'utf8\');var i=h.indexOf(\'function switchTab(name, btn){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!name||!btn)\')>=0&&seg.indexOf(\'parseIR(); parseNMR(); parseMS(); parseUV(); return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'TMCSI0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['TMCSI0 OK'],
  "ref": "第1336批·历史恢复无参切换函数抛错修复源码形态强锚：旧版 function switchTab(name, btn){ 无参调用解引用参数抛错被 catch 吞、结果不重算；修复后无参分支安全重算本页主结果并 return。旧版无 ⇒ BAD。"
},
{
  "slug": 'tcm-chemistry/toxicity-dose',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/tcm-chemistry/toxicity-dose.html\',\'utf8\');var i=h.indexOf(\'function switchTab(name, btn){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!name||!btn)\')>=0&&seg.indexOf(\'convert(); classify(); return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'TMCTD0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['TMCTD0 OK'],
  "ref": "第1336批·历史恢复无参切换函数抛错修复源码形态强锚：旧版 function switchTab(name, btn){ 无参调用解引用参数抛错被 catch 吞、结果不重算；修复后无参分支安全重算本页主结果并 return。旧版无 ⇒ BAD。"
},
{
  "slug": "tcm-chemistry/granule-quality",
  "inputs": {
    "totalWt": "0"
  },
  "expect": [
    "请填写大于 0 的总质量"
  ],
  "ref": "总质量为 0 时清空粒度分布分析（TCMGRNCLR）"
},
{
  "slug": "tcm-chemistry/ointment-release",
  "inputs": {
    "time": "0"
  },
  "expect": [
    "请填写大于 0 的初始浓度"
  ],
  "ref": "时间=0 时清空释放度曲线（TCMOINTCLR）"
},
{
  "slug": "tcm-chemistry/extraction-counts",
  "inputs": {
    "K": "0"
  },
  "expect": [
    "请填写大于 0 的分配系数"
  ],
  "ref": "K=0 时清空萃取次数结论（TCMEXTRCLR）"
},
{
  "slug": "tcm-chemistry/capsule-filling",
  "inputs": {
    "height": "0"
  },
  "expect": [
    "请填写大于 0 的堆高"
  ],
  "ref": "堆高=0 时清空流动性评价（TCMCAPCLR）"
},
{
  "slug": "tcm-chemistry/toxicity-dose",
  "inputs": {
    "dose": "0"
  },
  "expect": [
    "请填写大于 0 的剂量"
  ],
  "ref": "剂量=0 时清空等效剂量换算（TCMTOXCLR）"
},
{
  "slug": "tcm-chemistry/pharmacokinetics",
  "inputs": {
    "dose": "0"
  },
  "expect": [
    "请填写大于 0 的剂量"
  ],
  "ref": "剂量=0 时清空药代参数（TCMPKCLR）"
},
{
  "slug": "tcm-chemistry/structure-identification",
  "inputs": {
    "irInput": ""
  },
  "expect": [
    "请填写 IR 吸收峰"
  ],
  "ref": "IR 峰为空时清空结构解析结果（TCMIRCLR）"
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

  console.log("==== tcm-chemistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
