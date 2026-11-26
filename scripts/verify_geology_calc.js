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
  { slug: "civil/dijichengzailijisuan", inputs: { c: "20", phi: "25", gamma: "19", B: "3", Df: "2", K: "2.5" }, expect: ["451.82"], ref: "Terzaghi：Nq=e^(π·tan25°)·tan²(45°+12.5°)=10.66，Nc=(Nq−1)/tan25°=20.72，Nγ=2(Nq+1)tan25°=10.88；qu=20×20.72+19×2×10.66+0.5×19×3×10.88=1129.55；fa=qu/2.5=451.82 kPa（默认 c=15/φ=20/K=2 避开）" },
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
  { slug: "geology/dip-strike", inputs: { x1: "0", y1: "0", z1: "0", x2: "10", y2: "0", z2: "0", x3: "0", y3: "0", z3: "10" }, expect: ["270.0°", "90.0°", "直立面"], ref: "P1(0,0,0)、P2(10,0,0)、P3(0,0,10)：C=v1x·v2y−v1y·v2x=0 ⇒ C/|n|=0 判直立面，倾角 90.0°、倾向「不确定」、走向 atan2(0,−100)+90=270.0°；原实现误报「水平面、倾角 0°」" },
  { slug: "geology/dip-strike", inputs: { x1: "0", y1: "0", z1: "100", x2: "50", y2: "0", z2: "100", x3: "0", y3: "40", z3: "100" }, expect: ["0.0°", "不确定"], ref: "P1/P2/P3 同 z=100：C=2000、|n|=2000 ⇒ |C|/|n|=1 判水平面，倾角 0.0°、走向/倾向均「不确定」；原实现会输出走向 270.0°/倾向 0.0° 的伪确定值。锚点不取「水平面」——该词在页面静态文案（图例/说明）中恒存在，属逃生项。" },
  { slug: "geology/dip-strike", inputs: { x1: "0", y1: "0", z1: "100", x2: "50", y2: "0", z2: "100", x3: "0", y3: "40", z3: "100" }, expect: ["产状结果：倾角 0.0°（水平面"], ref: "水平面结果可复制：copyResult() 要求 detail 含「产状」且能匹配 `产状结果：`，旧实现水平面分支只写「三点构成水平面…」故复制按钮恒提示无结果；现补一行产状结果。默认输入非水平面 ⇒ 不命中。" },
  { slug: "geology/dip-strike", inputs: { x1: "0", y1: "0", z1: "0", x2: "10", y2: "0", z2: "0", x3: "0", y3: "0", z3: "10" }, expect: ["产状结果：走向 270.0°∠倾角 90.0°（直立面"], ref: "直立面结果可复制：旧实现直立面分支无「产状结果：」行，copyResult() 匹配不到任何内容（复制空串）。现补「走向 270.0°∠倾角 90.0°（直立面，倾向不确定）」。默认输入不命中。" },
  { slug: "geology/dizhiyijipinggu", inputs: { rtype: "4", scale: "0.5", comp: "80", sci: "4" }, expect: ["3.80"], ref: "综合评分=类型×0.3+规模×0.2+完整度×0.2+科学价值×0.3；类型4=1.2、规模0.5→3×0.2=0.6、完整度80/20=4×0.2=0.8、科学价值4×0.3=1.2，合计3.80（二级省级保护；默认 scale=2.5 避开）" },
    {
    "slug": "geology/duanceng-xingzhi-weiyi-huodongxing-panding",
    "inputs": { "v0": "3", "v1": "8000" },
    "expect": ["0.0004 mm/年", "稳定断层", "工程风险低"],
    "ref": "年均=3/8000=0.0004mm/年<0.001稳定断层、风险低（默认50/10000→0.0050/疑似活动/中；swapValues 50/10000→10000/50 输出活动断层/高风险，注入失败均不命中 0.0004/稳定/低）"
  },
    {
    "slug": "geology/kengtan-chuanmai-yanmai-quyang-fangshi",
    "inputs": { "v0": "80", "v1": "6" },
    "expect": ["480.0 m³", "624.0 m³", "391.9 m²"],
    "ref": "开挖=80×6=480.0m³；出渣=480×1.3=624.0；支护=80×2×√6=391.9m²（默认50/4→200.0/260.0/200.0，注入失败即不命中）"
  },
    {
    "slug": "geology/sample-1",
    "inputs": { "v0": "32", "v1": "4" },
    "expect": ["16"],
    "ref": "采样段数=长度/2=32/2=16（默认20/3→10；swap 32/4→4/32→采样=2；hint 含150子串但无独立16；注入失败均不命中 16）"
  },
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
},
{
  "slug": "geology/analysis-33",
  "inputs": {
    "data": "S-01,12.5,12.1\n坏行\nS-03,abc,19.2\nS-04,10,10.5",
    "lim": "5"
  },
  "clicks": [
    "calc();var r=String(document.getElementById('res').innerHTML),t=String(document.getElementById('analysis_33Table').innerHTML);document.getElementById('__tbProbe').textContent='AQ33 '+((r.indexOf('已接受 2 行、拒绝 2 行')>=0&&r.indexOf('批次判定')<0&&t==='')?'OK':'BAD');"
  ],
  "expect": [
    "AQ33 OK"
  ],
  "ref": "混合无效行：第 2 行列数不足、第 3 行分析值非数字，旧代码静默跳过并按剩余行给出合格率；现报告拒绝行数与逐行原因、清空数据表且不输出批次合格结论，直到用户修正。"
},
{
  "slug": "geology/analysis-32",
  "inputs": { "data": "西翼,270,30\n东翼,90,60" },
  "expect": [
    "翼间角： 90.0°",
    "轴面倾角： 75.0°",
    "褶皱对称性： 不对称"
  ],
  "ref": "两翼法向 n₁(270/30)、n₂(90/60)：翼间角=180−arccos(n₁·n₂)=180−90=90.0°；轴面法向=n₁−n₂ 对枢纽正交化后倾角 75.0°、倾向 90.0°；两翼倾角差 30°>10° 判不对称（默认 40/40 对称、翼间角 100.0°、轴面倾角 90.0°，避开）"
},
{
  "slug": "geology/spacing-4",
  "inputs": {
    "v0": "2000000",
    "v1": "200"
  },
  "expect": [
    "50",
    "40000 m²",
    "0.25 工程/万m²"
  ],
  "ref": "工程数≈面积/间距²=2000000/40000=50；网度单元=200²=40000 m²；密度=10000/40000=0.25（默认 1000000/100 得 100，注入失败即不命中）"
},

// ── 零用例加固（2026-10-06）──────────────────────────
{
  "slug": "geology/tester-16",
  "inputs": { "ucs_p": "180", "ucs_d": "90", "den_md": "260.0", "den_ms": "268.0", "den_mw": "162.0", "sof_cd": "95", "sof_cw": "62" },
  "expect": ["软化系数 K： 0.653", "K = σcw/σcd = 62/95 = 0.653"],
  "ref": "注入非默认(默认 σp=120/σd=50/σcd=85/σcw=55)：软化系数 K = 天然/饱和抗压强度 = 62/95 = 0.6526 → 0.653（0.5<K<0.65 ⇒ 弱软化岩石）；页面算式串随注入值变化。默认态 55/85 = 0.647，两条均不命中。"
},
{
  "slug": "geology/analysis-grade-ore",
  "inputs": { "cutoff": "1.8", "ind": "2.4" },
  "expect": ["边界品位： 1.80 % ｜ 工业品位： 2.40 %", "≥ 工业品位（矿石）： 0 个（占比 0.0%）", "≥ 边界品位总样数： 2 / 10（占比 20.0%）", "≥ 边界品位子集平均品位： 1.950 %"],
  "ref": "注入非默认(默认 cutoff=1.0/ind=1.5)：内置 10 个样品(1.3,0.8,1.6,1.1,1.4 等，均值 1.370)⇒ 边界品位提到 1.80 后仅 2 个样(1.95 的两个)≥ 边界品位、0 个达工业品位 2.40；子集均值 1.950%。默认态边界 1.00/工业 1.50 → 8/10(80%)、矿石 4 个，四条均不命中。"
},

{
    "slug": "geology/richter-scale",
    "inputs": {
      "mag": "5"
    },
    "expect": [
      "2.00e+12 能量 J"
    ],
    "ref": "里氏震级能量公式 E = 10^(1.5M + 4.8) J；M=5 → 10^(7.5+4.8) = 10^12.3 = 1.995e12 ≈ 2.00e+12 J。页面输出 '2.00e+12 能量 J'。HTML 默认 mag=6 → 6.31e+13，默认态不产生该值。"
  },

{
    "slug": "geology/mineral-hardness",
    "inputs": {
      "h": "7"
    },
    "expect": [
      "最接近的标准矿物： 石英（莫氏 7）"
    ],
    "ref": "莫氏硬度标准表：7 对应石英（SiO₂）。输入h=7 查表得最接近标准矿物 = 石英。HTML 默认 h=6 → 正长石，默认态不出现'石英（莫氏 7）'。"
  },

// ── 零用例加固（2026-10-09）──────────────────────────
{
    "slug": "geology/dizhibianlujilubiao",
    "inputs": { "holeId": "ZK205", "run": "5", "dFrom": "20.00", "dTo": "25.50", "litho": "中风化灰岩", "color": "青灰色", "struct": "中细粒结构", "desc": "完整" },
    "expect": [
      "厚 5.50 m"
    ],
    "ref": "地质编录分层厚度 = dTo − dFrom = 25.50 − 20.00 = 5.50 m。注入非默认(默认 ZK101/3/12.50/15.80 → 厚 3.30 m)，输出'（厚 5.50 m）'，默认态不出现 5.50。"
  },
{
    "slug": "geology/dizhishujutongji",
    "inputs": { "data": "10\n12\n11\n13\n12\n14\n11\n13", "conf": "0.95", "dtype": "sample" },
    "expect": [
      "10.9052 , 13.0948"
    ],
    "ref": "8 个样本：均值=96/8=12，样本方差=Σ(x−12)²/(n−1)=12/7=1.7143，s=1.3093，SE=1.3093/√8=0.4630，t(7,0.975)=2.365，边际=2.365×0.4630=1.0948 → 95% CI=[12−1.0948, 12+1.0948]=[10.9052, 13.0948]。注入非默认(默认内置样本为不同值)，默认态不出现该区间。"
  },
{
    "slug": "geology/wutanyichangjieyi",
    "inputs": { "amp": "800", "width": "120", "grad": "10", "atype": "grav" },
    "expect": [
      "估算埋深 ≈ 91.6 m"
    ],
    "ref": "Peters 半宽法埋深 ≈ 半宽 W / 1.31 = 120 / 1.31 = 91.603 → 91.6 m。注入非默认(默认 amp=500/width=80/grad=6 → 80/1.31=61.1 m)，默认态不出现 91.6。"
  },
  // ── 零用例收敛（2026-10-09）────────────────────────────
  {
    "slug": "geology/stats-density-1",
    "inputs": { "lines": "14,32\n9,21\n11,28" },
    "expect": [
      "测线 1：长 14.0 m / 32 条",
      "测线 3：长 11.0 m / 28 条",
      "节理总数 81 条",
      "总体平均间距： 0.42 m/条"
    ],
    "ref": "注入非默认三测线数据（默认 10,25 / 8,19 / 12,31，换行分隔）。独立复算：测线1 = 32/14 = 2.2857 → 2.29 条/m、平均间距 14/32 = 0.4375 → 0.44 m/条；测线2 = 21/9 = 2.333 → 2.33、9/21 = 0.4286 → 0.43；测线3 = 28/11 = 2.545 → 2.55、11/28 = 0.3929 → 0.39。合计总长 14+9+11 = 34.0 m、节理总数 32+21+28 = 81 条；总体线密度 81/34 = 2.382 → 2.38 条/m；总体平均间距 34/81 = 0.4198 → 0.42 m/条。⚠ 页面解析按【换行】分行、用逗号分隔长度与条数；同一行内用空格分隔只会被识别成一条测线（实测）。默认态输出 30.0 m / 75 条 / 0.40，四条均不命中。⚠ 页面 fmt() 用 toLocaleString 在 harness 桩下抛错但不影响统计链产出（实测通过）。"
  },
  {
    "slug": "geology/stratum-correlation",
    "inputs": { "search": "qqx7" },
    "expect": [
      "未找到匹配"
    ],
    "ref": "空结果路径用例（负向断言），与 rock-identify 同型。注入无匹配检索词 qqx7 ⇒ 页面空态文案『未找到匹配』出现；默认态渲染全部地层卡片（第四系…前寒武系），不含该串。独立依据：页面源码的 cnt===0 分支输出『未找到匹配』。"
  },
  {
    "slug": "geology/rock-identify",
    "inputs": { "search": "qqx7" },
    "expect": ["未找到匹配的岩石"],
    "ref": "空结果路径用例（负向断言）。该页是岩石检索表：默认 search 为空 + grpFilter=all ⇒ 渲染全部岩石卡片（花岗岩/闪长岩/辉长岩/玄武岩/流纹岩…），任何具体岩性串在默认态都出现 ⇒ 正向锚必然是逃生项。注入无匹配检索词 qqx7 ⇒ 命中页面 cnt===0 分支输出『未找到匹配的岩石』，默认态不含该串。注入失败（回退空 search）即恢复全列表 ⇒ 判别力成立。"
  },
  {
    "slug": "geology/diqiuwuliyingyong",
    "inputs": { "AB": "200", "a": "20" },
    "expect": ["100.00 探测深度 (m)", "20.00 垂直分辨率 (m)", "5.00 深径比"],
    "ref": "注入非默认（页面 input 由 JS 用 '+d.AB+' 模板填充，harness 下默认值为字面串 ⇒ 默认态报『请输入有效极距（>0）』，与注入态截然不同）。电法口径：探测深度 ≈ AB/2 = 200/2 = 100.00 m；垂直分辨率 = a = 20.00 m；深径比 = AB/a = 200/20 = 5.00。三项均只在注入态出现。"
  },
  {
    "slug": "geology/calc-25",
    "inputs": {
      "dt": "42",
      "vp": "42",
      "vs": "42"
    },
    "expect": [
      "42\n42\n42\n请输入有效参数（Δt&gt;0、Vp&gt;Vs&gt;0）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dt\":\"42\",\"vp\":\"42\",\"vs\":\"42\"}，输出区含「42\n42\n42\n请输入有效参数（Δt&gt;0、Vp&gt;Vs&gt;0）\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/calc-87",
    "inputs": {
      "bg": "42",
      "an": "42",
      "sd": "42"
    },
    "expect": [
      "强度 判定结论： 无明显异常 · 背景范围\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bg\":\"42\",\"an\":\"42\",\"sd\":\"42\"}，输出区含「强度 判定结论： 无明显异常 · 背景范围\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/analysis-cost-2",
    "inputs": {
      "holes": "42",
      "meter": "42",
      "waste": "42",
      "shifts": "42",
      "rate": "42",
      "move": "42",
      "other": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n报废进尺不能超过总进尺，请核对。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"holes\":\"42\",\"meter\":\"42\",\"waste\":\"42\",\"shifts\":\"42\",\"rate\":\"42\",\"move\":\"42\",\"other\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n报废进尺不能超过总进尺，请核对。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "civil/dijichengzailijisuan",
    "inputs": {
      "c": "42",
      "phi": "42",
      "gamma": "42",
      "B": "42",
      "Df": "42",
      "K": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n93.71"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"phi\":\"42\",\"gamma\":\"42\",\"B\":\"42\",\"Df\":\"42\",\"K\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n93.71」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/dip-strike",
    "inputs": {
      "x1": "42",
      "y1": "42",
      "z1": "42",
      "x2": "42",
      "y2": "42",
      "z2": "42",
      "x3": "42",
      "y3": "42",
      "z3": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n42\n三点共线或重合，无法确定平面，请检查输入。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x1\":\"42\",\"y1\":\"42\",\"z1\":\"42\",\"x2\":\"42\",\"y2\":\"42\",\"z2\":\"42\",\"x3\":\"42\",\"y3\":\"42\",\"z3\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n42\n42\n三点共线或重合，无法确定平…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/diqiuwulishujujisuan",
    "inputs": {
      "rho": "42",
      "h": "42",
      "k": "42",
      "H": "42",
      "V": "42",
      "z": "42",
      "I": "42",
      "dV": "42",
      "a": "42",
      "d": "42",
      "t": "42",
      "method": "magnetic"
    },
    "expect": [
      "暂无计算记录\nmagnetic\n磁化率 κ (SI) 磁化场 H (A/m) 体积 V (m³) 埋深 z (m)\n💡 磁法球体正上方：ΔT = 200 × κ × H × V / z³ (nT)，κ 为磁化率，H 为磁化场，V 为体积，"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"h\":\"42\",\"k\":\"42\",\"H\":\"42\",\"V\":\"42\",\"z\":\"42\",\"I\":\"42\",\"dV\":\"42\",\"a\":\"42\",\"d\":\"42\",\"t\":\"42\",\"method\":\"magnetic\"}，输出区含「暂无计算记录\nmagnetic\n磁化率 κ (SI) 磁化场 H (A/m) 体…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/diqiuhuaxueyichangjieshi",
    "inputs": {
      "ename": "abc123测试",
      "c": "42",
      "b": "42",
      "sd": "42"
    },
    "expect": [
      "00 绝对异常量 负异常 异常性质 abc123测试 异常类别： 背景范围 · 无明显富集\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ename\":\"abc123测试\",\"c\":\"42\",\"b\":\"42\",\"sd\":\"42\"}，输出区含「00 绝对异常量 负异常 异常性质 abc123测试 异常类别： 背景范围 · …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/dizhiwurandiaochapinggu",
    "inputs": {
      "pname": "abc123测试",
      "Cn": "42",
      "Bn": "42",
      "Sn": "42"
    },
    "expect": [
      "系数 Cn/Bn abc123测试 污染程度： 无污染\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pname\":\"abc123测试\",\"Cn\":\"42\",\"Bn\":\"42\",\"Sn\":\"42\"}，输出区含「系数 Cn/Bn abc123测试 污染程度： 无污染\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/dizhiyijipinggu",
    "inputs": {
      "scale": "42",
      "comp": "42",
      "sci": "42",
      "rtype": "4"
    },
    "expect": [
      "一级 国家级保护 5.0 规模评分 2.1 完整度评分 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"scale\":\"42\",\"comp\":\"42\",\"sci\":\"42\",\"rtype\":\"4\"}，输出区含「一级 国家级保护 5.0 规模评分 2.1 完整度评分 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/estimate-grade-reserve",
    "inputs": {
      "area": "42",
      "thick": "42",
      "dens": "42",
      "grade": "2.5"
    },
    "expect": [
      "2.500% 平均品位 25.00 金属品位 (kg/t)"
    ],
    "ref": "自动补强（B类零用例）：原注入 grade=42 已按 0–100% 上限拒绝，改为 2.5% 后输出「0.1852 金属量 (万吨) 2.500% 平均品位 25.00 金属品位 (kg/t)」；V=42×42=1764、Q=1764×42=74088、P=Q×2.5%=1852.2、P/Q×1000=25.00 与页面一致，默认态（1.2%）不含 2.500/25.00 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/estimate-grade-reserve",
    "inputs": { "area": "50000", "thick": "3.5", "dens": "2.7", "grade": "150" },
    "expect": [
      "品位 0–100%）"
    ],
    "ref": "品位上限于 100%：C=150 时金属量会大于矿石量，须报错而非输出「平均品位 150.000%」；默认 1.2% 不含该提示 ⇒ 零逃生。"
  },
  {
    "slug": "geology/estimate-grade-reserve",
    "clicks": [
      "calc();document.getElementById('grade').value='150';calc();document.getElementById('__tbProbe').textContent='STALE '+(lastResult===''?'0':'1');"
    ],
    "expect": ["STALE 0"],
    "ref": "错误态须清空 lastResult：先以默认值算出合法结果，再输入 150% 触发校验失败；旧实现只替换提示文字，lastResult 仍为上一组数据 ⇒ 复制按钮可复制过期结果（探针 1）。默认态无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "geology/estimate-reserve-1",
    "inputs": {
      "s1": "42",
      "s2": "42",
      "L": "42",
      "dens": "42",
      "grade": "42"
    },
    "expect": [
      " 金属量 P = 31116.96 t （3.1117"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"s1\":\"42\",\"s2\":\"42\",\"L\":\"42\",\"dens\":\"42\",\"grade\":\"42\"}，输出区含「 金属量 P = 31116.96 t （3.1117」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/generator-37",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      " 厚 14m 262-264m 页岩 厚 2m 264-277m 细砂岩 厚 13m 277-281m 粗砂岩 厚 4m 281-286m 泥岩 厚 5m 286-288m 粉砂岩 厚 2m 288-303m 粗砂岩 厚 15m 303-3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「 厚 14m 262-264m 页岩 厚 2m 264-277m 细砂岩 厚 1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/hazard",
    "inputs": {
      "slope": "42",
      "height": "42",
      "rain": "42",
      "litho": "2"
    },
    "expect": [
      "分 3 坡高评分 42° 坡度 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"slope\":\"42\",\"height\":\"42\",\"rain\":\"42\",\"litho\":\"2\"}，输出区含「分 3 坡高评分 42° 坡度 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/huanjingdizhipingjia",
    "inputs": {
      "n": "abc123测试",
      "c": "42",
      "s": "42"
    },
    "expect": [
      "i 标准值 Si\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"abc123测试\",\"c\":\"42\",\"s\":\"42\"}，输出区含「i 标准值 Si\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/sanweidizhijianmocanshu",
    "inputs": {
      "h": "42",
      "dip": "42",
      "L": "42",
      "S": "42",
      "dens": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n31.21"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h\":\"42\",\"dip\":\"42\",\"L\":\"42\",\"S\":\"42\",\"dens\":\"42\"}，输出区含「42\n42\n42\n42\n42\n31.21」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/soil-sample",
    "inputs": {
      "area": "42",
      "dens": "42",
      "cost": "42",
      "scale": "1"
    },
    "expect": [
      "距 ≈ 点距 ≈ 816.5 m ，总点数 63 个 ，覆盖 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"area\":\"42\",\"dens\":\"42\",\"cost\":\"42\",\"scale\":\"1\"}，输出区含「距 ≈ 点距 ≈ 816.5 m ，总点数 63 个 ，覆盖 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/soil-sample",
    "inputs": { "area": "20", "dens": "4", "cost": "-100" },
    "expect": [
      "每点成本（≥0，免费采样填 0）"
    ],
    "ref": "成本须 ≥0：cost=-100 时旧实现输出估算成本 −8000 元；现于校验阶段报错。默认 cost=80 不含该提示 ⇒ 零逃生。"
  },
  {
    "slug": "geology/soil-sample",
    "inputs": { "area": "30", "dens": "9", "cost": "0" },
    "expect": ["9.00 密度 (点/km²) 0 估算成本 (元)"],
    "ref": "642 批复核失败回归：免费采样 0 元是合法金额，旧 `cost<=0` 拒绝计算；现仅拒绝空值/非有限/负数。注入 area=30/dens=9/cost=0（默认 dens=4、cost=80）；短锚「0 估算成本 (元)」会被默认 6400 的尾零命中，故改用绑定密度 9.00 与成本 0 的组合锚。"
  },
  {
    "slug": "geology/soil-sample",
    "inputs": { "area": "20", "dens": "4", "cost": "" },
    "expect": ["每点成本（≥0，免费采样填 0）"],
    "ref": "642 批复核失败回归：成本留空旧实现 `parseFloat('')` 得 NaN 后虽被拒，但公式说明误称「空值按 0」；现文案与校验统一为「0 合法、空值拒绝」。空串与默认 80 均不含该文案在注入态的字段级锚。"
  },
  {
    "slug": "geology/soil-sample",
    "clicks": [
      "calc();document.getElementById('cost').value='-100';calc();document.getElementById('__tbProbe').textContent='STALE '+(lastResult===''?'0':'1');"
    ],
    "expect": ["STALE 0"],
    "ref": "错误态须清空 lastResult：先默认参数算出合法结果，再把每点成本改 −100 触发失败；旧实现不清 lastResult，复制按钮仍输出上一组数据（探针 1）。默认态无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "geology/mineral-hardness",
    "inputs": { "h": "15" },
    "expect": [
      "莫氏硬度有效范围 1–10，已按 10 级计算"
    ],
    "ref": "输入上限：h=15 超出莫氏 1–10，须提示并回落 10 级；旧实现不校验，15 直接参与比较并给出「可划全部参照物」。默认 h=6 不含该提示 ⇒ 零逃生。"
  },
  {
    "slug": "geology/mineral-hardness",
    "inputs": { "h": "0" },
    "expect": ["莫氏硬度有效范围 1–10，已按 1 级计算"],
    "ref": "642 批复核失败回归：旧实现把 h<0 钳到 0 却提示「范围 1–10，已按 0 级计算」，下界自相矛盾；现统一钳到有效下界 1。默认 h=6 不出现该提示。"
  },
  {
    "slug": "geology/mineral-hardness",
    "inputs": { "h": "-3" },
    "expect": ["莫氏硬度有效范围 1–10，已按 1 级计算"],
    "ref": "642 批复核失败回归：负值同样钳到 1 级而非 0 级，提示与有效范围一致；默认 h=6 不出现该提示。"
  },
  {
    "slug": "geology/shuiwendizhishentoushiyan",
    "inputs": {
      "Q": "42",
      "s": "42",
      "r0": "42",
      "M": "42",
      "R": "42",
      "type": "unconfined"
    },
    "expect": [
      "n(R/r₀)/(π·(2H−s)·s)。\n请输入有效参数（降深、井半径、含水层厚&gt;0，R&gt;r₀）\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"Q\":\"42\",\"s\":\"42\",\"r0\":\"42\",\"M\":\"42\",\"R\":\"42\",\"type\":\"unconfined\"}，输出区含「n(R/r₀)/(π·(2H−s)·s)。\n请输入有效参数（降深、井半径、含水层…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/weight-sample",
    "inputs": {
      "d": "42",
      "m": "42",
      "w": "42",
      "cval": "42",
      "tol": "42",
      "mat": "0.25"
    },
    "expect": [
      "最小样重 (g) 289.66 样重/最小样重 6.090e-4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"d\":\"42\",\"m\":\"42\",\"w\":\"42\",\"cval\":\"42\",\"tol\":\"42\",\"mat\":\"0.25\"}，输出区含「最小样重 (g) 289.66 样重/最小样重 6.090e-4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "geology/calc-1",
    "inputs": { "drillLen": "2", "threshold": "100", "unit": "mm" },
    "clicks": ["document.querySelectorAll=function(){return [{value:'120'},{value:'85'},{value:'250'},{value:'60'},{value:'180'},{value:'95'},{value:'310'},{value:'40'},{value:'150'}];};calcRQD()"],
    "expect": ["50.5%", "1.010"],
    "ref": "段长(mm)=120/85/250/60/180/95/310/40/150、阈值 100 mm ⇒ 有效段 120+250+180+310+150=1010 mm=1.010 m（5/9 段）；钻孔总长 2 m ⇒ RQD=1010/(2×1000)×100=50.5%（≥50 → 一般 Fair）。harness 不解析 addSegment() 动态生成的输入，故 clicks 以同值数组替换 querySelectorAll('#segments .seg-val') 的返回值后调用真实 calcRQD()，阈值比较/求和/分级仍全部走页面实现；默认态 0 段 ⇒ RQD 0.0%、有效岩芯总长 0.000，两锚均不命中（判别时清空 clicks 即回该默认态）。"
  }

,
{
  "slug": "geology/calc-1",
  "inputs": {"drillLen":"2","threshold":"0","unit":"mm"},
  "clicks": ["document.querySelectorAll=function(){return [{value:'120'},{value:'85'},{value:'250'}];};calcRQD()"],
  "expect": ["有效岩芯长度阈值必须大于 0；常用 100 mm"],
  "ref": "阈值 0 不按 100 兜底，显式拒绝并说明常用 100 mm；旧 `||100` 会把 0 静默当 100 算出 RQD。默认阈值 100 不含该提示。"
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

  console.log("==== geology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();