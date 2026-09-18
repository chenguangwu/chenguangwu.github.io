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
    "bun": "5.0",
    "cr": "80",
    "ua": "300",
    "alb": "40"
  },
  "expect": [
    "急性病毒性肝炎早期",
    "GGT/ALT>3"
  ],
  "ref": "De Ritis=AST/ALT=30/60=0.50<0.7 → 偏低（急性病毒性肝炎早期）；GGT/ALT=200/60=3.33>3 → 酒精性/胆汁淤积提示"
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
    "合并代谢性碱中毒"
  ],
  "ref": "pH7.25<7.35 且 HCO3 12<22 → 代谢性酸中毒；AG=140-100-12=28>12 → AG增高型；矫正HCO3=12+(28-12)=28>26 → 合并代碱"
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
    "38%"
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
    "val": "7.5",
    "rate": "2.5"
  },
  "expect": [
    "18.750000",
    "系数: 2.5"
  ],
  "ref": "r=val×rate×from/to=7.5×2.5×1/1=18.75 → toFixed(6)=18.750000"
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
    "γ球蛋白23%弥漫性增高(多克隆)"
  ],
  "ref": "白蛋白50<57 + γ23>20 + α2 13>11 → 慢性肝病图谱；区带合计50+4+13+10+23=100.0%"
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
    "艾滋病期(C3)"
  ],
  "ref": "淋巴细胞=2.0×20%×1000=400/μL；CD4绝对值=400×15%=60<200 → AIDS分期；CD4/CD8=15/45=0.33<0.71 → 倒置"
},
{
  "slug": "clinical-lab/hba1c-converter",
  "inputs": {
    "val1": "9.4"
  },
  "expect": [
    "控制不佳",
    "12.4 mmol/L"
  ],
  "ref": "eAG(mg/dL)=28.7×9.4-46.7=223.08→223；eAG(mmol/L)=223.08/18=12.39→12.4；HbA1c 9.4 落在8.0-9.9 → 控制不佳"
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
    "3.468e+2"
  ],
  "ref": "Ct=32 落在30-38 → 阳性(低拷贝)；标准曲线 slope=-3.370/intercept=38.56（独立最小二乘复算）→ 未知样本浓度=10^((30-38.56)/-3.37)=346.8 → 3.468e+2"
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
    "抗TPO抗体阳性(>34 IU/mL)"
  ],
  "ref": "TSH 0.02<0.27（低）+ FT3 12>6.8、FT4 35>22（高）→ 原发甲亢；TPOAb 120>34 → 阳性"
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
{
  "slug": "clinical-lab/analysis-8",
  "inputs": {
    "data": "3,7,11,19,23"
  },
  "expect": [
    "55.04",
    "12.60"
  ],
  "ref": "n=5, 和=63, 均值=12.60, 总体方差=((9.6²+5.6²+1.6²+6.4²+10.4²)/5)=55.04（Python Decimal 高精度复算）"
},
{
  "slug": "clinical-lab/analysis-9",
  "inputs": {
    "data": "3,7,11,19,23"
  },
  "expect": [
    "55.04",
    "12.60"
  ],
  "ref": "n=5, 和=63, 均值=12.60, 总体方差=55.04（Python Decimal 高精度复算）"
},
{
  "slug": "clinical-lab/analysis-density-2",
  "inputs": {
    "data": "3,7,11,19,23"
  },
  "expect": [
    "55.04",
    "12.60"
  ],
  "ref": "n=5, 和=63, 均值=12.60, 总体方差=55.04（Python Decimal 高精度复算）"
},
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
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== clinical-lab calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
