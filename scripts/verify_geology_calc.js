#!/usr/bin/env node
/**
 * 第 32 道门禁：geology 分类计算正确性验证（20 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：calc-1（RQD 依赖动态增删的岩芯段行，非纯输入驱动）、
 *       diqiuwulishujujisuan/magnetic（多分支表单，仅覆盖 gravity 分支）、
 *       analysis-grade-ore / analysis-32 / generator-37（文本/文件输入类）、
 *       analysis-33 / spacing-4（多指标行动态表单）。
 * 用法: node scripts/verify_geology_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "geology/dijichengzailijisuan", inputs: { c: "20", phi: "25", gamma: "19", B: "3", Df: "2", K: "2.5" }, expect: ["451.82"], ref: "Terzaghi：Nq=e^(π·tan25°)·tan²(45°+12.5°)=10.66，Nc=(Nq−1)/tan25°=20.72，Nγ=2(Nq+1)tan25°=10.88；qu=20×20.72+19×2×10.66+0.5×19×3×10.88=1129.55；fa=qu/2.5=451.82 kPa（默认 c=15/φ=20/K=2 避开）" },
  { slug: "geology/estimate-grade-reserve", inputs: { area: "80000", thick: "5", dens: "2.6", grade: "1.5" }, expect: ["15600.00"], ref: "V=S·M=80000×5=400000 m³；Q=V·D=400000×2.6=1040000 t；P=Q·C/100=1040000×1.5/100=15600.00 t（默认 area=50000/thick=3.5 避开）" },
  { slug: "geology/estimate-reserve-1", inputs: { s1: "1200", s2: "800", L: "60", dens: "2.6", grade: "1.2" }, expect: ["1872.00"], ref: "断面法：avgS=(1200+800)/2=1000；V=1000×60=60000；Q=60000×2.6=156000；P=156000×1.2/100=1872.00 t（默认 s1=800/s2=600 避开）" },
  { slug: "geology/soil-sample", inputs: { area: "30", dens: "9", cost: "60" }, expect: ["333.3"], ref: "N=A·D=30×9=270 点；网格间距 L=√(1/D)×1000=√(1/9)×1000=333.3 m；成本=270×60=16200 元（默认 area=20/dens=4 避开）" },
  { slug: "geology/calc-25", inputs: { dt: "12", vp: "6.2", vs: "3.6" }, expect: ["103.02"], ref: "震中距 D=Δt·Vp·Vs/(Vp−Vs)=12×6.2×3.6/(6.2−3.6)=267.84/2.6=103.02 km（默认 dt=20 避开）" },
  { slug: "geology/calc-87", inputs: { bg: "30", an: "90", sd: "8" }, expect: ["46.00"], ref: "异常下限 T=背景+2σ=30+2×8=46.00（衬度 Ac=90/30=3.000；默认 bg=40/an=120 避开）" },
  { slug: "geology/dizhiwurandiaochapinggu", inputs: { Cn: "1.2", Bn: "0.2", Sn: "0.5" }, expect: ["2.400"], ref: "单因子污染指数 Pi=Cn/Sn=1.2/0.5=2.400（超標倍数=1.400；Igeo=log₂(1.2/(1.5×0.2))=2.000；默认 Cn=0.6/Sn=0.3 避开）" },
  { slug: "geology/sanweidizhijianmocanshu", inputs: { h: "12", dip: "30", L: "400", S: "250", dens: "2.8" }, expect: ["10.392"], ref: "真厚度 t=h·cos30°=12×0.866025=10.392 m（A=L·S=100000 m²；V=A·t=1039230.48；默认 h=5/dip=25 避开）" },
  { slug: "geology/shuiwendizhishentoushiyan", inputs: { type: "confined", Q: "800", s: "4", r0: "0.2", M: "25", R: "300" }, expect: ["9.3115"], ref: "承压完整井 K=Q·ln(R/r₀)/(2π·M·s)=800×ln(1500)/(2π×25×4)=800×7.3133/628.3185=9.3115 m/d（默认 Q=500/M=20 避开）" },
  { slug: "geology/shuiwendizhishentoushiyan", inputs: { type: "unconfined", Q: "600", s: "2.5", r0: "0.2", M: "15", R: "250" }, expect: ["39.6189"], ref: "潜水完整井 K=2Q·ln(R/r₀)/(π(2H−s)·s)=1200×ln(1250)/(π×(30−2.5)×2.5)=1200×7.1309/215.9845=39.6189 m/d（默认 Q=500 避开）" },
  { slug: "geology/hazard", inputs: { slope: "50", height: "60", rain: "120", litho: "5" }, expect: ["4.25"], ref: "危险指数=ss×0.35+sl×0.25+sr×0.25+sh×0.15；slope50→4、height60→4、rain120→4、litho5=5：4×0.35+5×0.25+4×0.25+4×0.15=4.25（Ⅳ级极高危险；默认 slope=35/litho=3 避开）" },
  { slug: "geology/diqiuhuaxueyichangjieshi", inputs: { c: "150", b: "40", sd: "20" }, expect: ["5.500"], ref: "标准化异常值 Z=(C−B)/σ=(150−40)/20=5.500（衬度 Ac=150/40=3.750；默认 c=80/b=30 避开）" },
  { slug: "geology/diqiuwulishujujisuan", inputs: { method: "gravity", rho: "2.5", h: "100" }, expect: ["10.475"], ref: "重力异常 Δg=0.0419·Δρ·h=0.0419×2.5×100=10.475 mGal（g.u.=Δg×10=104.75）" },
  { slug: "geology/dip-strike", inputs: { x1: "0", y1: "0", z1: "0", x2: "1", y2: "0", z2: "-0.5", x3: "0", y3: "1", z3: "-0.5" }, expect: ["315.0"], ref: "三点定面：法向量n=(0.5,0.5,1)（东,北,上），|n|=√1.5；倾角=acos(C/|n|)=35.3°；倾向=atan2(0.5,0.5)=45.0°；走向=(45−90+360)%360=315.0°（默认 z1=100 平面且水平，避开）" },
  { slug: "geology/dizhiyijipinggu", inputs: { rtype: "4", scale: "0.5", comp: "80", sci: "4" }, expect: ["3.80"], ref: "综合评分=类型×0.3+规模×0.2+完整度×0.2+科学价值×0.3；类型4=1.2、规模0.5→3×0.2=0.6、完整度80/20=4×0.2=0.8、科学价值4×0.3=1.2，合计3.80（二级省级保护；默认 scale=2.5 避开）" },
  { slug: "geology/duanceng-xingzhi-weiyi-huodongxing-panding", inputs: { v0: "30", v1: "40" }, expect: ["35.0"], ref: "通用判读页：综合评分=(a+b)/2=(30+40)/2=35.0 → 轻度（默认 100/50=75 避开）" },
  { slug: "geology/kengtan-chuanmai-yanmai-quyang-fangshi", inputs: { v0: "60", v1: "80" }, expect: ["70.0"], ref: "通用判读页：综合评分=(60+80)/2=70.0 → 中度（默认 100/50=75 避开）" },
  { slug: "geology/sample-1", inputs: { v0: "90", v1: "95" }, expect: ["92.5"], ref: "通用判读页：综合评分=(90+95)/2=92.5 → 重度（默认 100/50=75 避开）" },
  { slug: "geology/weight-sample", inputs: { d: "3", m: "8", w: "2", tol: "15", mat: "0.25" }, expect: ["14.70"], ref: "Gy 采样：dCm=0.3、mG=8000、富集因子(1/w−1)=49；最小样重 m_min=C·d³·(1/w−1)/tol_rel²=0.25×0.027×49/0.15²=0.33075/0.0225=14.70 g（默认 d=2/m=5/w=1.5/tol=10/C=0.5 避开）" },
  { slug: "geology/analysis-cost-2", inputs: { holes: "8", meter: "2400", waste: "240", shifts: "60", rate: "2800", move: "72000", other: "108000" }, expect: ["161.11", "36.00", "43,500.00"], ref: "勘探成本效率：有效进尺=2400−240=2160 m，总费用=60×2800+72000+108000=348000 元 → 单位成本=348000÷2160=161.11 元/m，纯钻效率=2160÷60=36.00 m/台班，单孔成本=348000÷8=43,500.00 元（独立复算；默认组为 158.79/36.67/43,666.67，注入失败即不命中）" },
  {
    "slug": "geology/stats-analysis-2",
    "inputs": {
      "data": "20.4\n18.6\n22.1\n19.3\n21.5"
    },
    "expect": [
      "平均值： 20.38",
      "变异系数： 7.17%",
      "标准值： 18.99"
    ],
    "ref": "均值=101.9/5=20.38；样本标准差=√(8.548/4)=1.462 → 变异系数=1.462/20.38=7.17%；γs=1−(1.704/√5+4.678/25)×0.0717=0.9319 → 标准值=0.9319×20.38=18.99（独立复算；默认 T1..T6 共6组 → 均值13.03、CV6.54%、标准值12.33，注入失败即不命中）"
  },
{
  "slug": "geology/analysis-33",
  "inputs": {
    "data": "S-01,12.5,12.1\nS-02,8.4,8.9\nS-03,20.0,19.2",
    "lim": "5"
  },
  "expect": [
    "平均相对偏差： 4.37%",
    "超差项数： 1",
    "内检合格率： 66.67%"
  ],
  "ref": "RD=3.2520/5.7803/4.0816，均值4.37%；仅S-02超5%，合格率2/3=66.67%"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== geology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();