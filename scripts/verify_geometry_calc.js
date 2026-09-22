#!/usr/bin node
/**
 * geometry 分类计算正确性验证（覆盖 tools/geometry/ 全部 28 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_geometry_calc.js
 *   —— 目标：默认态 0 命中（该项由 CI 与人工双重确认）。
 *
 * 跑法:
 *   node scripts/verify_geometry_calc.js              # 全部
 *   node scripts/verify_geometry_calc.js pythagorean  # 单页
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---- 向量与坐标 ----
  { slug: "geometry/angle-between-vectors",
    inputs: { ax: "2", ay: "1", bx: "1", by: "3" },
    expect: ["45.000", "5.000"],
    ref: "a·b=2·1+1·3=5.000；cos θ=5/(√5·√10)=1/√2 → θ=45.000°" },

  { slug: "geometry/midpoint-2d",
    inputs: { x1: "-3", y1: "7", x2: "11", y2: "-2" },
    expect: ["4.000", "2.500"],
    ref: "((−3+11)/2=4.000；(7+(−2))/2=2.500" },

  { slug: "geometry/distance-3d",
    inputs: { x1: "1", y1: "1", z1: "1", x2: "4", y2: "6", z2: "3" },
    expect: ["6.164"],
    ref: "√(3²+5²+2²)=√38=6.164（位移须避开默认 3,4,12，否则 d=13 与默认态雷同）" },

  { slug: "geometry/dot-product-2d",
    inputs: { ax: "2", ay: "5", bx: "3", by: "4" },
    expect: ["26.000", "5.200"],
    ref: "a·b=2·3+5·4=26.000；|b|=5 → 投影=26/5=5.200" },

  { slug: "geometry/point-line-distance",
    inputs: { A: "3", B: "4", C: "-2", x0: "1", y0: "2" },
    expect: ["1.8000", "5.0000"],
    ref: "d=|3·1+4·2−2|/√(9+16)=9/5=1.8000；√(A²+B²)=5.0000" },

  { slug: "geometry/parabola-vertex",
    inputs: { a: "2", b: "-6", c: "1" },
    expect: ["1.5000", "-3.5000"],
    ref: "x_v=6/(2·2)=1.5000；y_v=2·2.25−6·1.5+1=−3.5000（须避开默认 x_v=2.0000）" },

  // ---- 圆、弧、扇形 ----
  { slug: "geometry/arc-length",
    inputs: { r: "7", deg: "45" },
    expect: ["5.4978", "0.7854"],
    ref: "θ=45°=0.7854 rad；L=7·0.7854=5.4978 m" },

  { slug: "geometry/chord-length",
    inputs: { r: "6", deg: "60" },
    expect: ["6.0000", "3.0000"],
    ref: "c=2·6·sin(30°)=6.0000 m；半弦长=3.0000 m" },

  { slug: "geometry/circle-area",
    inputs: { r: "2.5" },
    expect: ["19.6350", "15.7080"],
    ref: "A=π·2.5²=19.6350 m²；周长=2π·2.5=15.7080 m" },

  { slug: "geometry/circle-circumference",
    inputs: { r: "4" },
    expect: ["25.1327", "8.0000", "32.0000"],
    ref: "C=2π·4=25.1327 m；直径=C/π=8.0000 m；圆内接正方形对角线=2r ⇒ 面积=2r²=32.0000 m²（原式误用 πr²/4=12.566）" },

  { slug: "geometry/sector-area",
    inputs: { r: "4", deg: "60" },
    expect: ["8.3776", "16.667"],
    ref: "θ=π/3；A=r²θ/2=16·(π/3)/2=8.3776 m²；占整圆 60/360=16.667%（已删除与扇形面积同值的重复卡片）" },

  // ---- 多边形 ----
  { slug: "geometry/polygon-interior-angle",
    inputs: { n: "5" },
    expect: ["108.00", "540", "72.0000"],
    ref: "θ=(5−2)·180/5=108.00°；内角和=(5−2)·180=540°；中心角=360/5=72.0000°（原式第五张卡标「内角和与边数之比」却算 (n−2)/n=0.6，无几何意义，已换成中心角）" },

  { slug: "geometry/regular-polygon-area",
    inputs: { n: "5", s: "2" },
    expect: ["6.8819", "1.3764"],
    ref: "A=5·4/(4·tan36°)=6.8819 m²；内切圆半径=2/(2·tan36°)=1.3764 m" },

  { slug: "geometry/trapezoid-area",
    inputs: { a: "2", b: "7", h: "3" },
    expect: ["13.5000", "9.0000"],
    ref: "A=(2+7)·3/2=13.5000 m²；中位线=(2+7)/2=4.5 ⇒ 中位线×2=上下底之和=9.0000 m（原式算 (a+b)·2=18，把「×2」错做成「×4」）" },

  { slug: "geometry/triangle-heron",
    inputs: { a: "5", b: "6", c: "7" },
    expect: ["14.6969", "9.0000"],
    ref: "s=9.0000；A=√(9·4·3·2)=√216=14.6969 m²" },

  { slug: "geometry/pythagorean",
    inputs: { a: "5", b: "12" },
    expect: ["13.0000", "22.62"],
    ref: "c=√(25+144)=13.0000 m；∠A 的对边是 a=5 ⇒ tanA=a/b ⇒ ∠A=atan2(5,12)=22.62°（原式用 atan2(b,a)=67.38°，那是 ∠B，A、B 标反）" },

  { slug: "geometry/rectangle-diagonal",
    inputs: { w: "5", h: "12" },
    expect: ["13.0000", "60.0000", "45.240"],
    ref: "d=√(25+144)=13.0000 m；面积=5·12=60.0000 m²；两条对角线方向 (w,h) 与 (w,−h) ⇒ cosθ=(w²−h²)/(w²+h²)=−119/169 ⇒ θ=2·arctan(5/12)=45.240°（原式 atan(h/w)=67.38° 只是对角线与长边的夹角，不是两对角线夹角）" },

  // ---- 立体图形 ----
  { slug: "geometry/cone-frustum-volume",
    inputs: { R: "5", r: "2", h: "6" },
    expect: ["245.044"],
    ref: "V=π·6/3·(25+10+4)=2π·39=245.044 m³" },

  { slug: "geometry/cone-volume",
    inputs: { r: "2", h: "7" },
    expect: ["29.3215", "12.5664"],
    ref: "V=π·4·7/3=29.3215 m³；底面积=π·4=12.5664 m²" },

  { slug: "geometry/cube-properties",
    inputs: { a: "3" },
    expect: ["27.000", "54.000", "5.196"],
    ref: "V=3³=27.000；A=6·9=54.000；d=3√3=5.196" },

  { slug: "geometry/cylinder-volume",
    inputs: { r: "3", h: "4" },
    expect: ["113.0973", "75.3982"],
    ref: "V=π·9·4=113.0973 m³；侧面积=2π·3·4=75.3982 m²" },

  { slug: "geometry/ellipsoid-volume",
    inputs: { a: "2", b: "4", c: "5" },
    expect: ["167.552"],
    ref: "V=4/3·π·2·4·5=167.552 m³" },

  { slug: "geometry/pyramid-volume",
    inputs: { A: "12", h: "5" },
    expect: ["20.000"],
    ref: "V=12·5/3=20.000 m³" },

  { slug: "geometry/rectangular-prism-volume",
    inputs: { l: "5", w: "4", h: "3" },
    expect: ["60.000", "94.000", "48.000"],
    ref: "V=5·4·3=60.000 m³；A=2·(20+12+15)=94.000 m²；长方体有 12 条棱 ⇒ 棱长总和=4(l+w+h)=48.000 m（原式用 2(l+w+h)=24，少算一半）" },

  { slug: "geometry/sphere-surface-area",
    inputs: { r: "2" },
    expect: ["50.265"],
    ref: "A=4π·4=50.265 m²" },

  { slug: "geometry/sphere-volume",
    inputs: { r: "6" },
    expect: ["904.779", "904778.684"],
    ref: "V=4/3·π·216=904.779 m³；1 m³=1000 L ⇒ 904778.684 L（原式除以 1000 写成 0.904779 L，差 10⁶ 倍）" },

  { slug: "geometry/torus-volume",
    inputs: { R: "4", r: "2" },
    expect: ["315.827"],
    ref: "V=2π²·4·4=315.827 m³" },

  { slug: "geometry/ellipse-area",
    inputs: { a: "4", b: "2" },
    expect: ["25.133"],
    ref: "A=π·4·2=25.133 m²" },

  // ---- BATCH51 新增：定义域/退化输入的提示分支 ----
  { slug: "geometry/triangle-heron",
    inputs: { a: "1", b: "2", c: "10" },
    expect: ["不能构成三角形"],
    ref: "1+2<10 不满足三角不等式 ⇒ s(s−a)(s−b)(s−c)<0 开方得 NaN；正确应提示（默认 3,4,5 合法，避开）" },
  { slug: "geometry/parabola-vertex",
    inputs: { a: "0", b: "2", c: "3" },
    expect: ["二次项系数 a 不能为 0"],
    ref: "a=0 时 −b/(2a) 为 ±Infinity，且原函数是一次函数本无顶点（默认 2,−6,1 避开）" },
  { slug: "geometry/dot-product-2d",
    inputs: { ax: "1", ay: "2", bx: "0", by: "0" },
    expect: ["零向量"],
    ref: "投影长度 = a·b/|b|，b 为零向量时 |b|=0 ⇒ 除零得 Infinity（默认 (1,2)·(1,0) 之类避开）" },
  { slug: "geometry/angle-between-vectors",
    inputs: { ax: "0", ay: "0", bx: "1", by: "2" },
    expect: ["零向量"],
    ref: "零向量无方向，dot/(na·nb)=0/0 ⇒ NaN（默认 (1,1) 与 (0,1) 避开）" },
  { slug: "geometry/regular-polygon-area",
    inputs: { n: "2", s: "3" },
    expect: ["至少为 3"],
    ref: "n<3 时 tan(π/n) 退化（n=2 → tan90° 发散）⇒ 面积无意义（默认 n=6 避开）" },
  { slug: "geometry/point-line-distance",
    inputs: { A: "0", B: "0", C: "1", x0: "2", y0: "3" },
    expect: ["不构成一条直线"],
    ref: "A=B=0 时 √(A²+B²)=0 ⇒ 除零得 Infinity（默认 3,4,−2 避开）" },
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
  console.log("==== geometry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();