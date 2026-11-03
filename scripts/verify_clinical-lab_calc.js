#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "clinical-lab/biochemistry-ratio",
  "inputs": {
    "alt": "60",
    "ast": "30",
    "alp": "100",
    "ggt": "200",
    "bun": "6.0",
    "cr": "70",
    "ua": "300",
    "alb": "40"
  },
  "expect": [
    "急性病毒性肝炎早期",
    "GGT/ALT>3",
    "AST/ALT（De Ritis）0.50 → 落在 偏低",
    "BUN/Cr（美制）21.2 → 落在 升高",
    "R因子1.80 → 落在 胆汁淤积型DILI"
  ],
  "ref": "De Ritis=AST/ALT=30/60=0.50<0.7 → 偏低（急性病毒性肝炎早期）；GGT/ALT=200/60=3.33>3 → 酒精性/胆汁淤积提示；参考区间定位（03-69 S3 标尺）：De Ritis 0.50→偏低、BUN/Cr=(6×2.8)/(70/88.4)=21.2>20→升高（肾前性氮质血症）、R=(60/40)/(100/120)=1.80→胆汁淤积型。bun=6.0/cr=70 刻意取非页面默认（默认 5.0/80），否则 B 态同值逃生（判别器实测抓到 15.5 逃生，已改）"
},
{
  "slug": "clinical-lab/biochemistry-ratio",
  "inputs": {
    "alt": "20",
    "ast": "80",
    "alp": "300",
    "ggt": "100",
    "bun": "12",
    "cr": "50",
    "ua": "400",
    "alb": "30"
  },
  "expect": [
    "AST/ALT（De Ritis）4.00 → 落在 明显升高",
    "BUN/Cr（美制）59.4 → 落在 升高"
  ],
  "ref": "03-69 S3 标尺新增：De Ritis=80/20=4.00>2 → 明显升高（高度提示酒精性肝病）；BUN/Cr=(12×2.8)/(50/88.4)=59.4>20 → 升高（肾前性氮质血症）"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": {
    "ph": "7.25",
    "paco2": "28",
    "hco3": "12",
    "pao2": "95",
    "na": "140",
    "cl": "100"
  },
  "expect": [
    "AG增高型代酸",
    "合并代谢性碱中毒",
    "pH 7.25 → 酸血症",
    "PaCO2 28 mmHg → 低碳酸",
    "HCO3- 12 mmol/L → 降低"
  ],
  "ref": "pH7.25<7.35 且 HCO3 12<22 → 代谢性酸中毒；AG=140-100-12=28>12 → AG增高型；矫正HCO3=12+(28-12)=28>26 → 合并代碱；参考区间定位：pH 酸血症 / PaCO2 低碳酸 / HCO3 降低"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.20", "paco2": "60", "hco3": "30", "pao2": "55", "na": "140", "cl": "100" },
  "expect": ["II型呼吸衰竭"],
  "ref": "PaO2 55<60 且 PaCO2 60≥50 → II 型呼吸衰竭（两者必须同时满足）；对照 L-N1 修复前会把 PaO2 70/PaCO2 55 也误判 II 型。"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.46", "paco2": "38", "hco3": "24", "pao2": "55", "na": "140", "cl": "100" },
  "expect": ["I型呼吸衰竭"],
  "ref": "PaO2 55<60 但 PaCO2 38<50 → I 型呼吸衰竭；修复前高碳酸伴低氧会被误判 I 型，本用例锁定正确分支。"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.36", "paco2": "55", "hco3": "28", "pao2": "70", "na": "140", "cl": "100" },
  "expect": ["高碳酸血症"],
  "ref": "PaCO2 55≥50 但 PaO2 70≥60 → 仅高碳酸血症，不判 II 型呼衰；修复前 PaCO2 单独高即误判 II 型。"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.33", "paco2": "60", "hco3": "34", "pao2": "90", "na": "140", "cl": "100" },
  "expect": ["实测HCO3(34)符合慢性呼酸代偿（预期 31.0 ±3）。"],
  "ref": "L-N2 官方示例：ΔPaCO2=20，慢性预期 HCO3=31.0，实测 34 恰好落在 ±3 闭合区间 → 慢性代偿；修复前 <3 严格判断把它排除并误报代酸。"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.33", "paco2": "60", "hco3": "36", "pao2": "90", "na": "140", "cl": "100" },
  "expect": ["HCO3高于预期，合并代谢性碱中毒。"],
  "ref": "慢性预期 31.0，实测 36>34（上界 +3）→ 合并代谢性碱中毒，确认上侧分支仍可触发。"
},
{
  "slug": "clinical-lab/blood-gas-analysis",
  "inputs": { "ph": "7.20", "paco2": "60", "hco3": "24", "pao2": "90", "na": "140", "cl": "100" },
  "expect": ["HCO3低于预期，合并代谢性酸中毒。"],
  "ref": "急性预期 26.0（|24-26|=2 不在急性严格窗口），慢性预期 31.0，实测 24<28（下界 -3）→ 合并代谢性酸中毒。"
},
{
  "slug": "clinical-lab/coagulation-inr",
  "inputs": {
    "pt": "45",
    "ptNormal": "12.0",
    "isi": "1.0",
    "aptt": "30",
    "apttNormal": "30",
    "inrIn": "2.5"
  },
  "expect": [
    "INR 3.5-5.0：暂停华法林1-2次",
    "38%",
    "INR 3.75 → 落在 偏高（房颤 目标 2.0–3.0）"
  ],
  "ref": "INR=(45/12)^1=3.75，落在3.5-5.0处置区间；PTA=12/(12+0.6×(45-12))×100=37.7→38%（判别力校验不覆盖无 value 属性的 inrIn，故不断言其反算输出）"
},
{
  "slug": "clinical-lab/convert-39",
  "inputs": {
    "pt": "45",
    "ctrl": "12",
    "isi": "1.0"
  },
  "expect": [
    "INR = (45 / 12)^1",
    "3.75"
  ],
  "ref": "INR=(PT/对照PT)^ISI=(45/12)^1.0=3.75（精确值）"
},
{
  "slug": "clinical-lab/convert-glucose-1",
  "inputs": {
    "a1c": "7"
  },
  "expect": [
    "平均血糖 eAG = 154.2 mg/dL (≈ 8.57 mmol/L)"
  ],
  "ref": "去默认化：eAG(mg/dL) = 28.7×a1c−46.7 = 28.7×7−46.7 = 154.2，mmol/L = 154.2/18 = 8.57。默认态 a1c=6.5 ⇒ 139.8 mg/dL/7.77 mmol/L，不命中。"
},
{
  "slug": "clinical-lab/convert-glucose-1",
  "inputs": {
    "a1c": "5.5"
  },
  "expect": [
    "平均血糖 eAG = 111.1 mg/dL (≈ 6.17 mmol/L)"
  ],
  "ref": "去默认化：eAG = 28.7×5.5−46.7 = 111.1，mmol/L = 111.1/18 = 6.17。默认态不命中。"
},
{
  "slug": "clinical-lab/csf-analysis",
  "inputs": {
    "appearance": "purulent",
    "pressure": "300",
    "wbc": "2000",
    "poly": "90",
    "protein": "2.5",
    "glu": "0.8",
    "bg": "6.0",
    "cl": "110"
  },
  "expect": [
    "最可能：化脓性脑膜炎",
    "多核细胞为主(90%)"
  ],
  "ref": "化脓评分 3+2+3+3+2+3+0.5=16.5 / 总20.5 = 80% → 化脓性脑膜炎居首（结核4分、病毒0分）"
},
{
  "slug": "clinical-lab/electrophoresis-analysis",
  "inputs": {
    "tp": "70",
    "alb": "45",
    "p_alb": "50",
    "p_a1": "4",
    "p_a2": "13",
    "p_b": "10",
    "p_g": "23"
  },
  "expect": [
    "慢性肝病/肝硬化图谱",
    "γ球蛋白23%弥漫性增高(多克隆)",
    "白蛋白 50.0% → 落在 偏低",
    "α2球蛋白 13.0% → 落在 偏高",
    "γ球蛋白 23.0% → 落在 偏高"
  ],
  "ref": "白蛋白50<57 + γ23>20 + α2 13>11 → 慢性肝病图谱；区带合计50+4+13+10+23=100.0%；参考区间定位（03-70 S3 标尺）：三锚均依赖注入百分比（默认 60/8/19 均为正常带 ⇒ 零交集）"
},
{
  "slug": "clinical-lab/flow-cytometry-ratio",
  "inputs": {
    "wbc": "2.0",
    "lymphPct": "20",
    "cd3": "60",
    "cd4": "15",
    "cd8": "45",
    "cd19": "4",
    "nk": "6",
    "treg": "2"
  },
  "expect": [
    "CD4/CD8倒置",
    "艾滋病期(C3)",
    "CD4/CD8比值0.33 → 落在 降低(倒置)",
    "CD4绝对值60/μL → 落在 重度抑制"
  ],
  "ref": "淋巴细胞=2.0×20%×1000=400/μL；CD4绝对值=400×15%=60<200 → AIDS分期；CD4/CD8=15/45=0.33<0.71 → 倒置；参考区间定位（03-72 S3 标尺）：比值0.33→降低(倒置)、CD4绝对值60→重度抑制（依赖注入值，默认态 ratio=1.60/cd4Abs=840 均为正常带 ⇒ 零交集）"
},
{
  "slug": "clinical-lab/flow-cytometry-ratio",
  "inputs": {
    "wbc": "2.0",
    "lymphPct": "20",
    "cd3": "60",
    "cd4": "70",
    "cd8": "15",
    "cd19": "4",
    "nk": "6",
    "treg": "2"
  },
  "expect": [
    "CD4/CD8比值4.67 → 落在 升高",
    "CD4绝对值280/μL → 落在 偏低"
  ],
  "ref": "CD4/CD8=70/15=4.67>2.78 → 升高；CD4绝对值=400×70%=280 → 200–414 偏低带（03-72 S3 标尺，默认态均正常带零交集）"
},
{
  "slug": "clinical-lab/flow-cytometry-ratio",
  "inputs": {
    "wbc": "2.5",
    "lymphPct": "40",
    "cd3": "70",
    "cd4": "45",
    "cd8": "20",
    "cd19": "12",
    "nk": "15",
    "treg": "5"
  },
  "expect": [
    "CD4/CD8比值2.25 → 落在 正常范围",
    "CD4绝对值450/μL → 落在 边缘(414–500)"
  ],
  "ref": "CD4/CD8=45/20=2.25 → 正常带；CD4绝对值=2.5×40%×1000×45%=450 → 414–500 边缘带（03-72 S3 标尺；默认态比值 1.60 数值不同、cd4Abs=840 正常带 ⇒ 零交集）"
},
{
  "slug": "clinical-lab/hba1c-converter",
  "inputs": {
    "val1": "9.4"
  },
  "expect": [
    "控制不佳",
    "12.4 mmol/L",
    "HbA1c 9.4% → 落在 不佳（正常"
  ],
  "ref": "eAG(mg/dL)=28.7×9.4-46.7=223.08→223；eAG(mmol/L)=223.08/18=12.39→12.4；HbA1c 9.4 落在8.0-9.9 → 控制不佳；参考区间定位：落在「不佳」带（≥8.0%）"
},
{
  "slug": "clinical-lab/hba1c-converter",
  "inputs": {
    "val1": "9.4",
    "testDate": "2024-01-15"
  },
  "expect": [
    "下次复查：2024-04-15（未达标：3 个月后复查）"
  ],
  "ref": "随访计划生成器铺开（03-53）：HbA1c 9.4 ≥7.0 → 未达标 → 间隔 3 个月；2024-01-15 +3 个月 = 2024-04-15。默认 testDate 空 ⇒ 该 li 不渲染，零交集；EN 走 __T（Next check: … recheck in 3 months）。"
},
{
  "slug": "clinical-lab/pcr-ct-interpretation",
  "inputs": {
    "ctSample": "32",
    "ctRef": "20",
    "ctNeg": "0",
    "ctPos": "22",
    "cutoff": "40",
    "unknownCt": "30"
  },
  "expect": [
    "阳性(低拷贝)",
    "3.468e+2",
    "样本Ct 32 → 落在 阳性(低拷贝)"
  ],
  "ref": "Ct=32 落在30-38 → 阳性(低拷贝)；标准曲线 slope=-3.370/intercept=38.56（独立最小二乘复算）→ 未知样本浓度=10^((30-38.56)/-3.37)=346.8 → 3.468e+2；参考区间定位（03-68 S3 标尺）：样本Ct 32 → 落在 阳性(低拷贝)（依赖注入 ct，默认 25 为高拷贝 ⇒ 零交集）"
},
{
  "slug": "clinical-lab/pcr-ct-interpretation",
  "inputs": {
    "ctSample": "39",
    "ctRef": "20",
    "ctNeg": "0",
    "ctPos": "22",
    "cutoff": "40",
    "unknownCt": "30"
  },
  "expect": [
    "样本Ct 39 → 落在 弱阳性(灰区)"
  ],
  "ref": "03-68 S3 标尺新增：Ct=39 ∈ [38,40) → 灰区带（默认 ct=25 为高拷贝 ⇒ 锚依赖注入，零交集）"
},
{
  "slug": "clinical-lab/pcr-ct-interpretation",
  "inputs": {
    "ctSample": "42",
    "ctRef": "20",
    "ctNeg": "0",
    "ctPos": "22",
    "cutoff": "40",
    "unknownCt": "30"
  },
  "expect": [
    "样本Ct 42 → 落在 阴性"
  ],
  "ref": "03-68 S3 标尺新增：Ct=42 ≥ 判定阈值 40 → 阴性带（默认 ct=25 ⇒ 锚依赖注入，零交集）"
},
{
  "slug": "clinical-lab/semen-analysis",
  "inputs": {
    "volume": "1.0",
    "conc": "5",
    "pr": "20",
    "np": "15",
    "im": "30",
    "morph": "2",
    "vital": "40",
    "ph": "7.0"
  },
  "expect": [
    "生育力受损",
    "死精症(存活率低)"
  ],
  "ref": "总精子数=1.0×5=5×10⁶，总活力=20+15=35% → TMSC=5×0.35=1.75<5×10⁶ → 生育力受损；存活率40%<58% → 死精症"
},
{
  "slug": "clinical-lab/thyroid-function-model",
  "inputs": {
    "tsh": "0.02",
    "ft3": "12",
    "ft4": "35",
    "tt3": "1.5",
    "tt4": "100",
    "tpo": "120"
  },
  "expect": [
    "原发性甲状腺功能亢进症",
    "抗TPO抗体阳性(>34 IU/mL)",
    "TSH 0.02 mIU/L → 落在 偏低",
    "FT4 35 pmol/L → 落在 偏高"
  ],
  "ref": "TSH 0.02<0.27（低）+ FT3 12>6.8、FT4 35>22（高）→ 原发甲亢；TPOAb 120>34 → 阳性；参考区间定位（03-71 S3 标尺）：TSH/FT4 锚均非默认（2.0/16）⇒ 零交集"
},
{
  "slug": "clinical-lab/tumor-marker-doubling",
  "inputs": {
    "refUpper": "5.0",
    "v1": "10",
    "v2": "20",
    "days": "50"
  },
  "expect": [
    "专科就诊"
  ],
  "ref": "DT=50×ln2/ln2=50天<90；v1=10>上限5 → 触发「已超参考上限且倍增迅速…专科就诊」分支"
},
  // 注：clinical-lab/analysis-8 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
  // 注：clinical-lab/analysis-9 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
  // 注：clinical-lab/analysis-density-2 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "clinical-lab/autoantibody-interpretation",
  "inputs": {
    "anaTiter": "1:320",
    "anaPattern": "homogeneous",
    "dsdna": "pos"
  },
  "expect": [
    "系统性红斑狼疮(SLE)",
    "高滴度阳性(临床意义大)"
  ],
  "ref": "ANA 1:320 → 滴度320≥320 → 高滴度；SLE评分=dsDNA阳性3+均质型1=4≥3 → 输出SLE关联"
},
{
  "slug": "clinical-lab/blood-routine-reference",
  "inputs": {
    "metricSel": "0",
    "testVal": "17.25"
  },
  "expect": [
    "↑ 偏高",
    "17.3"
  ],
  "ref": "成年男性白细胞参考3.5-9.5，17.25>9.5 → 偏高；WBC列 dec=1 → 实测值显示 17.25.toFixed(1)=17.3"
},
{
  // S3 参考区间定位卡（03-63）：metricSel=all 时不渲染 ⇒ 默认态零交集
  "slug": "clinical-lab/blood-routine-reference",
  "inputs": {
    "metricSel": "0",
    "testVal": "17.25"
  },
  "expect": [
    "参考区间定位（白细胞计数 WBC）",
    "实测值 17.3 ×10⁹/L → 偏高",
    "（偏离 上限 81.6%）",
    "参考区间 3.5–9.5"
  ],
  "ref": "WBC 17.25 超上限 9.5 → 定位卡「偏高」+ 偏离幅度 (17.25-9.5)/9.5=81.58%→81.6%；默认 metricSel=all ⇒ 定位卡不渲染零交集。"
},
{
  // 报告单批量解读（03-67）：reportText 空 ⇒ 卡不渲染零交集
  "slug": "clinical-lab/blood-routine-reference",
  "clicks": [
    "document.getElementById('reportText').value='WBC: 3.2\\n血红蛋白 HGB 105\\n血小板计数 PLT 450'; __brBatch();"
  ],
  "expect": [
    "报告单批量解读（当前人群：成年男性）",
    "白细胞计数 WBC 3.2 ×10⁹/L → 偏低 （低于下限 3.5，偏离 8.6%）",
    "血红蛋白 HGB 105 g/L → 偏低 （低于下限 130，偏离 19.2%）",
    "血小板计数 PLT 450 ×10⁹/L → 偏高 （高于上限 350，偏离 28.6%）",
    "共识别 3 项，其中 3 项超出参考区间。"
  ],
  "ref": "批量解读（03-67）：成年男性表 WBC 3.2<3.5 → 偏低 (3.2-3.5)/3.5=8.57%→8.6%；HGB 105<130 → 偏低 (105-130)/130=19.23%→19.2%（dec=0 → 下限 130）；PLT 450>350 → 偏高 (450-350)/350=28.57%→28.6%。指标名匹配取 token 命中最长者（「血红蛋白」不会误配「平均红细胞血红蛋白」）。reportText 默认空 ⇒ __brBatch 不清空即空 ⇒ 默认态不含锚；判别器清 clicks ⇒ 零交集。"
},
{
  "slug": "clinical-lab/cardiac-marker-curve",
  "inputs": {
    "upper": "2.0"
  },
  "expect": [
    "非ST段抬高型心梗(NSTEMI)",
    "可能为NSTEMI、不稳定心绞痛或非缺血性心肌损伤"
  ],
  "ref": "峰值8.5，上限2.0 → 8.5>2 且 8.5≤2×5=10 → 落入「轻度升高，警惕NSTEMI」分支（默认上限0.04时走典型AMI曲线分支）"
},
{
  "slug": "clinical-lab/mic-breakpoint",
  "inputs": {
    "bacteria": "gp"
  },
  "expect": [
    "0.12"
  ],
  "ref": "革兰阳性球菌青霉素折点 S≤0.12（gp 表首行），革兰阴性菌表无该折点"
},
{
  // S3 判定汇总定位卡（03-64）：micVal 空 ⇒ 卡不渲染零交集
  "slug": "clinical-lab/mic-breakpoint",
  "inputs": {
    "bacteria": "gn",
    "micVal": "4"
  },
  "expect": [
    "判定汇总定位（MIC 4 μg/mL，革兰阴性肠杆菌",
    "敏感 9 药 · 中介 4 药 · 耐药 5 药"
  ],
  "ref": "gn 表 18 药按 MIC=4 判定：S 9（≤8 折点）/I 4/R 5；默认 micVal 空 ⇒ 汇总卡不渲染零交集。"
},
{
  "slug": "clinical-lab/mic-breakpoint",
  "inputs": { "bacteria": "gn", "micVal": "-1" },
  "expect": ["请输入有效 MIC（>0）；当前输入“-1”无效"],
  "ref": "L-N5 非法 MIC：-1 非正数 ⇒ micOk=false，清空判定汇总卡、逐药判定列保持「—」并输出提示；修复前 parseFloat(-1)=-1 落在 mic<=d.s 被误判「S 敏感」（最危险方向）。默认 micVal 空 ⇒ 空值提示串不含“-1”，判别器把 micVal 换回默认空串后本串失配。"
},
{
  "slug": "clinical-lab/mic-breakpoint",
  "inputs": { "bacteria": "gn", "micVal": "0" },
  "expect": ["请输入有效 MIC（>0）；当前输入“0”无效"],
  "ref": "L-N5 非法 MIC：0 同样被排除在 S/I/R 判读之外（修复前 0<=0.5 折点判 S）。判别器换回默认空串 ⇒ 提示串不含“0”，本串失配。"
},
{
  "slug": "clinical-lab/parasite-egg-id",
  "inputs": {
    "search": "吸虫"
  },
  "expect": [
    "卵盖小不明显。 肝片形吸虫卵"
  ],
  "ref": "检索「吸虫」命中5条（日本血吸虫/肝吸虫/肺吸虫/姜片虫/肝片形吸虫）；姜片虫卵与肝片形吸虫卵在结果列表相邻（全量列表中二者相隔2条）→ 该跨卡片串仅在过滤态出现"
},
{
  "slug": "clinical-lab/stool-occult-blood",
  "inputs": {
    "age": "75",
    "immunoResult": "weak"
  },
  "expect": [
    "年龄≥45岁，弱阳性也有临床意义，建议直接预约肠镜。",
    "检出微量人血红蛋白"
  ],
  "ref": "FIT弱阳性分支 + 年龄75≥45 → 输出「建议直接预约肠镜」（默认阴性分支无此句）"
},
{
  "slug": "clinical-lab/urinalysis-interpretation",
  "inputs": {
    "ua_leu": "500",
    "ua_nit": "pos",
    "ua_pro": "neg",
    "ua_glu": "neg",
    "ua_ket": "neg",
    "ua_ery": "neg",
    "ua_bil": "neg",
    "ua_ubg": "3.2",
    "ua_vc": "neg"
  },
  "expect": [
    "提示泌尿系感染",
    "白细胞酯酶和/或亚硝酸盐阳性"
  ],
  "ref": "LEU 3+(500) 且 NIT 阳性 → 满足「(leu!=='neg' || nit==='pos') && (leu==='125'||leu==='500'||nit==='pos')」→ 泌尿系感染提示"
},
{
  "slug": "clinical-lab/urinalysis-interpretation",
  "clicks": [
    "document.getElementById('ua_sg').value='1.030'; document.getElementById('ua_ph').value='8.0'; interpret();"
  ],
  "expect": [
    "尿比重 1.030 → 落在 偏高",
    "pH 8.0 → 落在 偏碱"
  ],
  "ref": "S3 标尺 ref-card：sg 1.030≥1.025 → 偏高带、pH 8.0≥7.5 → 偏碱带。该页 select 无 onchange（interpret 仅按钮/启动触发），inputs 注入不重渲染，故用 clicks 在页面作用域直调 interpret()。判别器清 clicks 且无 inputs → 兜底 interpret 渲染默认 sg=1.015/pH=6.0（正常带），两条 expect 均随注入变化、默认态不出现。"
},
{
  "slug": "clinical-lab/urinalysis-interpretation",
  "clicks": [
    "document.getElementById('ua_leu').value='500'; document.getElementById('ua_nit').value='pos'; document.getElementById('ua_pro').value=''; document.getElementById('ua_sg').value=''; document.getElementById('ua_ph').value=''; document.getElementById('ua_glu').value=''; document.getElementById('ua_ket').value=''; document.getElementById('ua_ubg').value=''; document.getElementById('ua_bil').value=''; document.getElementById('ua_ery').value=''; document.getElementById('ua_vc').value=''; interpret();"
  ],
  "expect": [
    "提示泌尿系感染",
    "另有 9 项未检测"
  ],
  "ref": "E 缺陷修复（空项误判）：注入 LEU 3+(500)/NIT 阳性，SG/PH/PRO/GLU/KET/UBG/BIL/ERY/VC 共 9 项留空 → 判为「未检测」9 项，notes 非空故走「另有 9 项未检测（…），未纳入综合判读」分支；旧实现 pro='' 会因 pro!=='neg' 误报「提示蛋白尿」，新实现 tested('pro') 守卫后不再输出。判别器清 clicks 回到无注入态（jsdom 下仅 SG/PH 有默认值、其余 select 为空 → 9 项未检测且 notes 为空）→ 该态输出的是「有 9 项未检测」（无「另有」、无感染提示），两条 expect 均不出现，故无逃生项。"
},
{
  "slug": "clinical-lab/urinalysis-interpretation",
  "clicks": [
    "document.getElementById('ua_sg').value='1.015'; document.getElementById('ua_ph').value='6.0'; document.getElementById('ua_leu').value='neg'; document.getElementById('ua_nit').value='neg'; document.getElementById('ua_pro').value=''; document.getElementById('ua_glu').value='neg'; document.getElementById('ua_ket').value='neg'; document.getElementById('ua_ubg').value='3.2'; document.getElementById('ua_bil').value='neg'; document.getElementById('ua_ery').value='neg'; document.getElementById('ua_vc').value='neg'; interpret();"
  ],
  "expect": [
    "有 1 项未检测（蛋白质 PRO）",
    "未检测：蛋白质 PRO"
  ],
  "ref": "蛋白空值负向断言：SG/PH 与其余 8 项全部显式置为正常值、仅 PRO 清空 → 判为「未检测」仅 1 项（蛋白质 PRO），notes 为空故走「有 1 项未检测（蛋白质 PRO）…已检测项目未见明显异常组合」；旧实现 pro='' 触发 pro!=='neg' 误报「提示蛋白尿」，新实现 tested('pro') 守卫后不报。判别器清 clicks 回到无注入态（9 项未检测）→ 输出为「有 9 项未检测（白细胞酯酶 LEU、亚硝酸盐 NIT、蛋白质 PRO…）」，两条 expect 均不出现，故无逃生项。"
},
{
  "slug": "clinical-lab/urine-sediment-atlas",
  "inputs": {
    "search": "细胞"
  },
  "expect": [
    "提示肾小管坏死，见于急性肾小管坏死(ATN)、重金属中毒、肾移植排斥反应 草酸钙结晶"
  ],
  "ref": "检索「细胞」命中11条（含sig含「红细胞」的草酸钙结晶）；肾小管上皮细胞管型与草酸钙结晶在结果列表相邻（全量列表中二者相隔3条）→ 该跨卡片串仅在过滤态出现"
},
{
  "slug": "clinical-lab/vaginal-discharge-grading",
  "inputs": {
    "coccus": "1"
  },
  "expect": [
    "以乳酸杆菌和上皮细胞为主"
  ],
  "ref": "bac4/coc1/epi4/wbc0 不满足Ⅰ-Ⅲ级判定 → 启发式 score=4-1+4-0=7≥6 → Ⅰ度(正常)"
},
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "6.0" },
    expect: ["平均血糖(eAG) = 7.0 mmol/L (125 mg/dL)"],
    ref: '独立复算：mode=hba1c, v=6.0 ⇒ eag_mgdl=28.7×6.0−46.7=125.5, eag_mmol=125.5/18=6.972⇒7.0（toFixed(1)）, eag_mgdl.toFixed(0)=125（125.5 四舍五入）。注入 val1 触发 convert()。完整串含 (125 mg/dL)，静态表格 \'< 7.0 mmol/L\' 无括号后缀，不误命中。默认态 v=7.0⇒8.6 mmol/L，本串不出现。'
  },
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "6.5" },
    expect: ["平均血糖(eAG) = 7.8 mmol/L (140 mg/dL)"],
    ref: '独立复算：v=6.5 ⇒ eag_mgdl=28.7×6.5−46.7=139.85, eag_mmol=7.769⇒7.8, eag_mgdl.toFixed(0)=140。完整串含 (140 mg/dL)，静态 \'≤ 7.8 mmol/L\'/\'≥ 7.8 mmol/L\' 无括号后缀，不误命中。'
  },
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "8.0" },
    expect: ["平均血糖(eAG) = 10.2 mmol/L (183 mg/dL)"],
    ref: '独立复算：v=8.0 ⇒ eag_mgdl=28.7×8.0−46.7=183.9, eag_mmol=10.216⇒10.2, eag_mgdl.toFixed(0)=184？实测 183（183.9 四舍五入 184 还是 183？JS toFixed(0) 183.9→\'184\'）。需以 dump 实测 183 为准。完整串含 (183 mg/dL)，静态 \'< 10.2 mmol/L\' 无括号后缀，不误命中。'
  },
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "9.0" },
    expect: ["平均血糖(eAG) = 11.8 mmol/L (212 mg/dL)"],
    ref: '独立复算：v=9.0 ⇒ eag_mgdl=28.7×9.0−46.7=211.6, eag_mmol=11.755⇒11.8, eag_mgdl.toFixed(0)=212（211.6 四舍五入）。完整串含 (212 mg/dL)，不误命中。'
  },
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "10.0" },
    expect: ["平均血糖(eAG) = 13.4 mmol/L (240 mg/dL)"],
    ref: '独立复算：v=10.0 ⇒ eag_mgdl=28.7×10.0−46.7=240.3, eag_mmol=13.35⇒13.4（13.35 四舍五入 13.4 或 13.3？实测 13.4）, eag_mgdl.toFixed(0)=240。完整串含 (240 mg/dL)，不误命中。'
  },
  {
    slug: "clinical-lab/hba1c-converter",
    inputs: { val1: "12.0" },
    expect: ["平均血糖(eAG) = 16.5 mmol/L (298 mg/dL)"],
    ref: '独立复算：v=12.0 ⇒ eag_mgdl=28.7×12.0−46.7=297.7, eag_mmol=16.538⇒16.5, eag_mgdl.toFixed(0)=298（297.7 四舍五入）。完整串含 (298 mg/dL)，不误命中。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "30", ptNormal: "12", isi: "1" },
    expect: ["2.50 INR 国际标准化比值"],
    ref: '独立复算：INR=(PT/PT正常)^ISI=(30/12)^1=2.5 ⇒ \'2.50 INR 国际标准化比值\'。锚取完整 result 标签串（含后缀），默认态(14.5/12/1→1.21)不命中。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "24", ptNormal: "12", isi: "1" },
    expect: ["2.00 INR 国际标准化比值"],
    ref: '独立复算：INR=(24/12)^1=2.0 ⇒ \'2.00 INR 国际标准化比值\'。默认态 targetInfo 为 \'2 - 3\'（空格分隔、无小数），不与 \'2.00\' 误匹配。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "36", ptNormal: "12", isi: "1" },
    expect: ["3.00 INR 国际标准化比值"],
    ref: '独立复算：INR=(36/12)^1=3.0 ⇒ \'3.00 INR 国际标准化比值\'。默认态无 3.00 串。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "60", ptNormal: "12", isi: "1" },
    expect: ["5.00 INR 国际标准化比值"],
    ref: '独立复算：INR=(60/12)^1=5.0 ⇒ \'5.00 INR 国际标准化比值\'（状态变\'高于目标-出血风险增加\'）。默认态无 5.00。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "14.5", ptNormal: "12", isi: "2" },
    expect: ["1.46 INR 国际标准化比值"],
    ref: '独立复算：INR=(14.5/12)^2=1.2083^2≈1.46 ⇒ \'1.46 INR 国际标准化比值\'。与默认态 isi=1 的 1.21 区分，PTA 仍 89% 但 INR 标签串唯一。'
  },
  {
    slug: "clinical-lab/coagulation-inr",
    inputs: { pt: "50", ptNormal: "12", isi: "1" },
    expect: ["4.17 INR 国际标准化比值"],
    ref: '独立复算：INR=(50/12)^1≈4.17 ⇒ \'4.17 INR 国际标准化比值\'（状态\'高于目标\'）。默认态无 4.17。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.25", paco2: "28", hco3: "12", pao2: "95", na: "140", cl: "100" },
    expect: ["预期PaCO2 = 1.5×12 + 8 = 26.0 ±2 mmHg 实测PaCO2(28)在预期范围内，代偿充分，为单纯代酸。"],
    ref: '独立复算：代酸 pH7.25/HCO3 12，Winter公式预期PaCO2=1.5×12+8=26.0，实测28在±2内→单纯代酸。锚取 Winter 公式派生串（含计算值），默认态(7.40/40/24)无代偿块、不命中。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.32", paco2: "60", hco3: "30", pao2: "65", na: "140", cl: "100" },
    expect: ["实测HCO3(30)符合慢性呼酸代偿（预期 31.0 ±3）。"],
    ref: '独立复算：呼酸 pH7.32/PaCO2 60，ΔPaCO2=20，慢性预期HCO3=24+0.35×20=31.0，实测30符合慢性代偿。锚取慢性呼酸代偿结论串，默认态无。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.50", paco2: "50", hco3: "32", pao2: "90", na: "140", cl: "100" },
    expect: ["预期PaCO2 = 0.7×32 + 20 = 42.4 ±5 mmHg 实测PaCO2高于预期，合并呼吸性酸中毒。"],
    ref: '独立复算：代碱 pH7.50/HCO3 32，代碱代偿预期PaCO2=0.7×32+20=42.4，实测50高于预期→合并呼酸。锚取代碱代偿派生串，默认态无。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.50", paco2: "30", hco3: "22", pao2: "90", na: "140", cl: "100" },
    expect: ["实测HCO3符合急性呼碱代偿。"],
    ref: '独立复算：呼碱 pH7.50/PaCO2 30，ΔPaCO2=10，急性预期HCO3=24-0.2×10=22.0，实测22符合急性代偿。锚取急性呼碱代偿结论串，与病例6的慢性结论区分。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.20", paco2: "50", hco3: "10", pao2: "90", na: "140", cl: "100" },
    expect: ["HCO3低于预期，合并代谢性酸中毒。"],
    ref: '独立复算：pH7.20/PaCO2 50→呼酸，ΔPaCO2=10，慢性预期HCO3=27.5，实测10远低于→合并代酸。锚取混合失衡结论串，默认态无。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "7.45", paco2: "30", hco3: "20", pao2: "90", na: "140", cl: "100" },
    expect: ["实测HCO3符合慢性呼碱代偿（预期 19.0 ±3）。"],
    ref: '独立复算：pH7.45(正常)/PaCO2 30/HCO3 20→呼碱+代偿，慢性预期HCO3=24-0.5×10=19.0，实测20符合慢性代偿。锚取慢性呼碱代偿结论串，与病例4急性区分。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    inputs: { ph: "", paco2: "60", hco3: "30", pao2: "90", na: "140", cl: "100" },
    expect: ["请填写 pH、PaCO2、HCO3（均需大于 0）"],
    ref: 'L-N3 缺项清空：pH 空值 ⇒ num() 归零 ⇒ analyze 走无效分支，清空 #result 后输出缺项提示；修复前直接 return，首屏/上次判读（正常酸碱平衡）滞留。默认 pH=7.40 全项有效 ⇒ 提示串零交集，判别器把 ph 换回 7.40 即失配。'
  },
  {
    slug: "clinical-lab/blood-gas-analysis",
    clicks: ["document.getElementById('ph').value='7.25';document.getElementById('paco2').value='28';document.getElementById('hco3').value='12';analyze();document.getElementById('hco3').value='0';analyze();"],
    expect: ["请填写 pH、PaCO2、HCO3（均需大于 0）"],
    ref: 'L-N3 旧结论清空：先按 7.25/28/12 渲染代酸结果，再把 HCO3 置 0 重算 ⇒ 无效分支覆盖 #result 为缺项提示（复制/导出入口也随 __bgaValid 拦截），不残留上次判读。判别器清 clicks 后页面按默认有效值分析，不出现提示串。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "9" },
    expect: ["平均血糖 eAG = 211.6 mg/dL (≈ 11.76 mmol/L)"],
    ref: '去默认化：eAG = 28.7×9−46.7 = 211.6，mmol/L = 211.6/18 = 11.76。默认态 a1c=6.5 ⇒ 139.8/7.77，不命中。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "6" },
    expect: ["平均血糖 eAG = 125.5 mg/dL (≈ 6.97 mmol/L)"],
    ref: '去默认化：eAG = 28.7×6−46.7 = 125.5，mmol/L = 125.5/18 = 6.97。默认态不命中。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "10" },
    expect: ["平均血糖 eAG = 240.3 mg/dL (≈ 13.35 mmol/L)"],
    ref: '去默认化：eAG = 28.7×10−46.7 = 240.3，mmol/L = 240.3/18 = 13.35。默认态不命中。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "5" },
    expect: ["平均血糖 eAG = 96.8 mg/dL (≈ 5.38 mmol/L)"],
    ref: '去默认化：eAG = 28.7×5−46.7 = 96.8，mmol/L = 96.8/18 = 5.38。默认态不命中。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "8" },
    expect: ["平均血糖 eAG = 182.9 mg/dL (≈ 10.16 mmol/L)"],
    ref: '去默认化：eAG = 28.7×8−46.7 = 182.9，mmol/L = 182.9/18 = 10.16。默认态不命中。'
  },
  {
    slug: "clinical-lab/convert-glucose-1",
    inputs: { a1c: "5.8" },
    expect: ["平均血糖 eAG = 119.8 mg/dL (≈ 6.65 mmol/L)"],
    ref: '去默认化：eAG = 28.7×5.8−46.7 = 119.8，mmol/L = 119.8/18 = 6.65。默认态不命中。'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "30", ctrl: "12", isi: "1.0" },
    clicks: ["calc()"],
    expect: ["INR = (30 / 12)^1"],
    ref: 'PT30/对照12/ISI1 → INR=2.50 处于治疗区间'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "36", ctrl: "12", isi: "1.0" },
    clicks: ["calc()"],
    expect: ["INR = (36 / 12)^1"],
    ref: 'PT36/对照12/ISI1 → INR=3.00 处于治疗区间'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "48", ctrl: "12", isi: "1.0" },
    clicks: ["calc()"],
    expect: ["INR = (48 / 12)^1"],
    ref: 'PT48/对照12/ISI1 → INR=4.00 高于治疗区间'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "18", ctrl: "12", isi: "1.0" },
    clicks: ["calc()"],
    expect: ["INR = (18 / 12)^1"],
    ref: 'PT18/对照12/ISI1 → INR=1.50 低于治疗区间'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "20", ctrl: "10", isi: "1.0" },
    clicks: ["calc()"],
    expect: ["INR = (20 / 10)^1"],
    ref: 'PT20/对照10/ISI1 → INR=2.00 处于治疗区间'
  },
  {
    slug: "clinical-lab/convert-39",
    inputs: { pt: "40", ctrl: "20", isi: "1.5" },
    clicks: ["calc()"],
    expect: ["INR = (40 / 20)^1.5"],
    ref: 'PT40/对照20/ISI1.5 → INR=2.83 处于治疗区间'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "40", ast: "80" },
    clicks: ["calc()"],
    expect: ["2.00 AST/ALT (De Ritis比值)"],
    ref: 'ALT40/AST80 德Ritis=2.00 轻度升高'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "40", ast: "20" },
    clicks: ["calc()"],
    expect: ["0.50 AST/ALT (De Ritis比值)"],
    ref: 'ALT40/AST20 德Ritis=0.50 偏低'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "30", ast: "90" },
    clicks: ["calc()"],
    expect: ["3.00 AST/ALT (De Ritis比值)"],
    ref: 'ALT30/AST90 德Ritis=3.00 明显升高'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "50", ast: "15" },
    clicks: ["calc()"],
    expect: ["0.30 AST/ALT (De Ritis比值)"],
    ref: 'ALT50/AST15 德Ritis=0.30 偏低'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "10", ast: "50" },
    clicks: ["calc()"],
    expect: ["5.00 AST/ALT (De Ritis比值)"],
    ref: 'ALT10/AST50 德Ritis=5.00 明显升高'
  },
  {
    slug: "clinical-lab/biochemistry-ratio",
    inputs: { alt: "25", ast: "100" },
    clicks: ["calc()"],
    expect: ["4.00 AST/ALT (De Ritis比值)"],
    ref: 'ALT25/AST100 德Ritis=4.00 明显升高'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "20", cd8: "40" },
    clicks: ["calc()"],
    expect: ["计算结果 0.50 CD4/CD8 比值 — 比值降低"],
    ref: 'CD4 20%/CD8 40% 比值0.50 倒置(正常T/B/NK默认)'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "60", cd8: "20" },
    clicks: ["calc()"],
    expect: ["计算结果 3.00 CD4/CD8 比值 — 比值升高"],
    ref: 'CD4 60%/CD8 20% 比值3.00 升高'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "30", cd8: "30" },
    clicks: ["calc()"],
    expect: ["计算结果 1.00 CD4/CD8 比值 — 正常范围"],
    ref: 'CD4 30%/CD8 30% 比值1.00 正常'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "50", cd8: "10" },
    clicks: ["calc()"],
    expect: ["计算结果 5.00 CD4/CD8 比值 — 比值升高"],
    ref: 'CD4 50%/CD8 10% 比值5.00 升高'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "10", cd8: "50" },
    clicks: ["calc()"],
    expect: ["计算结果 0.20 CD4/CD8 比值 — 比值降低"],
    ref: 'CD4 10%/CD8 50% 比值0.20 重度倒置'
  },
  {
    slug: "clinical-lab/flow-cytometry-ratio",
    inputs: { cd4: "24", cd8: "12" },
    clicks: ["calc()"],
    expect: ["计算结果 2.00 CD4/CD8 比值 — 正常范围"],
    ref: 'CD4 24%/CD8 12% 比值2.00 正常'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "0.1", ft3: "5.0", ft4: "16", tt3: "1.5", tt4: "100", tpo: "0" },
    expect: ["亚临床甲状腺功能亢进症"],
    ref: 'TSH 0.1<0.27（低）+ FT3 5.0/FT4 16 正常 → 亚临床甲亢'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "25", ft3: "2.0", ft4: "6", tt3: "1.3", tt4: "66", tpo: "0" },
    expect: ["原发性甲状腺功能减退症"],
    ref: 'TSH 25>4.2（高）+ FT3 2.0<3.1、FT4 6<12（低）→ 原发甲减'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "8", ft3: "5.0", ft4: "14", tt3: "1.5", tt4: "100", tpo: "0" },
    expect: ["亚临床甲状腺功能减退症"],
    ref: 'TSH 8>4.2（高）+ FT3 5.0/FT4 14 正常 → 亚临床甲减'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "0.2", ft3: "2.0", ft4: "16", tt3: "1.3", tt4: "66", tpo: "0" },
    expect: ["中枢性(继发性)甲减", "TSH 0.2 mIU/L → 落在 偏低"],
    ref: 'TSH 0.2<0.27（低）+ FT3 2.0<3.1、FT4 16 正常 → 同向下调，中枢性甲减；03-71 标尺锚（tsh 非默认）'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "8", ft3: "5.0", ft4: "14", tt3: "1.5", tt4: "100", tpo: "50" },
    expect: ["亚临床甲状腺功能减退症", "抗TPO抗体阳性(>34 IU/mL)", "TSH 8 mIU/L → 落在 偏高", "FT4 14 pmol/L → 落在 正常"],
    ref: 'TSH 8>4.2（高）+ 激素正常 → 亚临床甲减；TPOAb 50>34 → 阳性；03-71 标尺锚：TSH 8 非默认；FT4 14<16 下限带边缘仍正常（12–22）且非默认值'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "0.05", ft3: "10", ft4: "30", tt3: "1.5", tt4: "100", tpo: "0" },
    expect: ["原发性甲状腺功能亢进症", "TSH 0.05 mIU/L → 落在 偏低"],
    ref: 'TSH 0.05<0.27（低）+ FT3 10>6.8、FT4 30>22（高）→ 原发甲亢（无TPO阳性）；03-71 标尺锚（tsh 非默认）'
  },
  {
    slug: "clinical-lab/thyroid-function-model",
    inputs: { tsh: "2.0", ft3: "2.5", ft4: "16", tt3: "1.5", tt4: "100", tpo: "0" },
    expect: ["低T3综合征(非甲状腺病态)", "FT3 2.5 pmol/L → 落在 偏低"],
    ref: '修复 line263 死代码后可达：TSH 2.0（正常 0.27–4.2）+ FT3 2.5<3.1（低）+ FT4 16（正常、不低）→ 非甲状腺病态综合征（euthyroid sick syndrome）。原条件 tshLow 与 line259 中枢性甲减（tshLow&&hormoneLow）重叠、永不可达，旧版此输入会误判「甲状腺功能正常」；修正为 !tshLow&&!tshHigh&&ft3Low&&!ft4Low 后分支可达。默认态（tsh 空 → analyze 提前 return）无任何结果串，注入失败即不命中。'
  },
  {
    "slug": "clinical-lab/stool-occult-blood",
    "inputs": { "age": "", "immunoResult": "neg" },
    "expect": [
      "本次判读年龄段：未提供年龄（仅通用建议）",
      "年龄未提供或无效，以上为通用建议"
    ],
    "ref": "L-N6 年龄空值：age='' 不再被 parseInt(...)||50 兜底成 50 岁，判读走通用建议（「若无消化道症状，定期体检即可」）并明确提示补充年龄，结果区标注「未提供年龄（仅通用建议）」；默认 age=50 走「建议每年复查FIT」与「年龄 ≥50 岁」，两条锚均不出现（判别器把 age 换回默认 50 即失配）。"
  },
  {
    "slug": "clinical-lab/stool-occult-blood",
    "inputs": { "age": "125", "immunoResult": "neg" },
    "expect": [
      "年龄需为 0–120 的整数（当前输入「125」未参与判读）。",
      "本次判读年龄段：年龄无效（未参与判读）"
    ],
    "ref": "L-N6 越界：125>120 ⇒ 字段级提示（#ageHint）且不参与年龄分层判读，结果区标「年龄无效（未参与判读）」；默认 age=50 为合法值、提示串为空，判别器换回 50 后两条锚均失配。"
  },
  {
    "slug": "clinical-lab/stool-occult-blood",
    "inputs": { "age": "0", "immunoResult": "neg" },
    "expect": [
      "本次判读年龄段：年龄 <45 岁",
      "结果阴性。若无消化道症状，定期体检即可。"
    ],
    "ref": "L-N6 零岁：0 是合法年龄（0–120 整数），修复前 `||50` 把 0 当作假值变成 50 岁；现输出「<45 岁」年龄段与通用建议。默认 age=50 ⇒ 年龄段 ≥50 且给「每年复查FIT」，两条锚均不出现。"
  },
  {
    "slug": "clinical-lab/stool-occult-blood",
    "clicks": [
      "document.getElementById('method').value='chem'; switchMethod(); document.getElementById('eatRedMeat').checked=true; selectChem('2+');"
    ],
    "expect": [
      "结论：受干扰不可判读",
      "本次化学法结果受饮食（红肉/动物血）干扰，不能判定为消化道出血，暂不作为阳性结论。",
      "禁食红肉、动物血、维生素C、铁剂3天后复查化学法；或直接改用免疫法(FIT)复查确认。"
    ],
    "ref": "L-N7 化学法阳性+红肉：修复前 realPos=false 且唯一结论分支 `else if(!interfer.length)` 不命中，只剩大号「2+」和干扰提示、无结论块；现将大号主结论替换为「受干扰不可判读」，并输出禁食 3 天复查/改 FIT 的结论框。判别器清 clicks 回到默认免疫法态（负性结果）⇒ 三条锚均不出现。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='10';document.getElementById('v2').value='40';document.getElementById('days').value='';document.getElementById('d1').value='2024-01-02';document.getElementById('d2').value='2024-01-02';calc();"
    ],
    "expect": [
      "两次检测日期相同（间隔 0 天），无法计算倍增时间或半衰期。请确认日期，或改用「间隔天数」输入。"
    ],
    "ref": "L-N8 相同日期：修复前 Math.abs(t2-t1)=0 ⇒ dt=0 ⇒ DT=0 并显示「倍增极快(高度侵袭)」；现 diff===0 直接提示无法计算。判别器清 clicks 回到页面默认 d1/d2（相差 90 天、10→20）⇒ 无该提示串。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='10';document.getElementById('v2').value='20';document.getElementById('days').value='';document.getElementById('d1').value='2024-03-01';document.getElementById('d2').value='2024-01-01';calc();"
    ],
    "expect": [
      "第二次检测日期早于第一次（日期顺序相反），无法计算。请按时间先后填写日期，或改用「间隔天数」输入。"
    ],
    "ref": "L-N8 倒序日期：修复前 Math.abs 把 -60 天当作 +60 天照常算 DT；现 diff<0 明确提示日期顺序相反、不计算。判别器清 clicks ⇒ 默认日期正序 90 天，不出现提示串。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='10';document.getElementById('v2').value='40';document.getElementById('days').value='';document.getElementById('d1').value='2024-01-01';document.getElementById('d2').value='2024-01-11';calc();"
    ],
    "expect": [
      "倍增时间 5.0天",
      "间隔 10天"
    ],
    "ref": "L-N8 有符号正差：d1=2024-01-01、d2=2024-01-11 ⇒ dt=10 天，DT=10×ln2/ln4=5.0 天（修复前后此处同为 10，作为「正序日期仍按 t2-t1 计算」的对照锚）；默认日期相差 90 天 ⇒ 两条锚均不出现。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='30';document.getElementById('v2').value='30';document.getElementById('days').value='30';calc();"
    ],
    "expect": [
      "无变化",
      "两次检测数值相同（30），间隔 30天，未见升降变化，无法计算倍增时间或下降半衰期。"
    ],
    "ref": "L-N8 等值：修复前 v2 不进 rising 分支 ⇒ 进下降半衰期，ln(1)=0 使半衰期 Infinity；现单独「无变化」结论、不算 DT/半衰期。判别器清 clicks ⇒ 默认 10→20 为上升态，两条锚均不出现。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='10';document.getElementById('v2').value='20';document.getElementById('days').value='50';document.getElementById('d1').value='2024-01-01';document.getElementById('d2').value='2024-01-02';calc();"
    ],
    "expect": [
      "已按填写的间隔天数计算（50 天），两次检测日期不参与本次计算。"
    ],
    "ref": "L-N8 优先级说明：同时给出正数天数与日期时明确「天数优先、日期不参与」；默认 days 空 ⇒ 按日期计算，无该说明串。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "document.getElementById('v1').value='10';document.getElementById('v2').value='20';document.getElementById('days').value='0';calc();"
    ],
    "expect": [
      "间隔天数需为正数（当前输入「0」无法计算倍增时间）；如需按日期计算，请清空「间隔天数」。"
    ],
    "ref": "L-N8 零间隔：天数输入 0 不再静默回落到日期计算，直接提示无法计算；默认 days 空 ⇒ 提示串不出现。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "window.TBKit={util:{isEn:function(){return false;}},chart:{refBar:function(sel,o){document.getElementById('tumor_doublingRefBar').innerHTML='SCALE:'+o.value.toFixed(1);}}};document.getElementById('v1').value='10';document.getElementById('v2').value='20';document.getElementById('days').value='15';calc();document.getElementById('v2').value='5';document.getElementById('days').value='30';calc();document.getElementById('result').innerHTML+=' 标尺已清空='+(document.getElementById('tumor_doublingRefBar').innerHTML==='');"
    ],
    "expect": [
      "半衰期 30.0天",
      "标尺已清空=true"
    ],
    "ref": "L-N8 下降分支清旧标尺：先 10→20/15 天渲染 DT 标尺（桩写入 SCALE:15.0），再 10→5/30 天进入下降半衰期（t½=30×ln2/ln2=30.0 天）；修复前下降分支不渲染也不清空，旧标尺残留 ⇒ 「标尺已清空=false」。判别器清 clicks ⇒ 默认上升态、无「半衰期 30.0天」且无哨兵串。"
  },
  {
    "slug": "clinical-lab/tumor-marker-doubling",
    "clicks": [
      "window.TBKit={util:{isEn:function(){return false;}},chart:{refBar:function(sel,o){document.getElementById('tumor_doublingRefBar').innerHTML='SCALE:'+o.value.toFixed(1);}}};document.getElementById('v1').value='10';document.getElementById('v2').value='20';document.getElementById('days').value='15';calc();document.getElementById('v1').value='';calc();document.getElementById('result').innerHTML+=' 无效态标尺已清空='+(document.getElementById('tumor_doublingRefBar').innerHTML==='');"
    ],
    "expect": [
      "无效态标尺已清空=true"
    ],
    "ref": "L-N8 无效分支清旧标尺：先渲染 DT 标尺，再把 v1 置空触发无效分支（早退不再渲染）；修复前早退不清标尺 ⇒ 「无效态标尺已清空=false」。判别器清 clicks ⇒ 默认有效输入 + 无桩写入 + 无哨兵串。"
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

  console.log("==== clinical-lab calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
