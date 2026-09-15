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
    expect: ["25.1327", "8.0000"],
    ref: "C=2π·4=25.1327 m；直径=C/π=8.0000 m" },

  { slug: "geometry/sector-area",
    inputs: { r: "4", deg: "60" },
    expect: ["8.3776", "8.3776"],
    ref: "θ=π/3；A=r²θ/2=16·(π/3)/2=8.3776 m²；整圆比项同值" },

  // ---- 多边形 ----
  { slug: "geometry/polygon-interior-angle",
    inputs: { n: "5" },
    expect: ["108.00", "540"],
    ref: "θ=(5−2)·180/5=108.00°；内角和=(5−2)·180=540°" },

  { slug: "geometry/regular-polygon-area",
    inputs: { n: "5", s: "2" },
    expect: ["6.8819", "1.3764"],
    ref: "A=5·4/(4·tan36°)=6.8819 m²；内切圆半径=2/(2·tan36°)=1.3764 m" },

  { slug: "geometry/trapezoid-area",
    inputs: { a: "2", b: "7", h: "3" },
    expect: ["13.5000", "18.0000"],
    ref: "A=(2+7)·3/2=13.5000 m²；中位线×2=(2+7)·2=18.0000 m（须避开默认结果的 16.0000）" },

  { slug: "geometry/triangle-heron",
    inputs: { a: "5", b: "6", c: "7" },
    expect: ["14.6969", "9.0000"],
    ref: "s=9.0000；A=√(9·4·3·2)=√216=14.6969 m²" },

  { slug: "geometry/pythagorean",
    inputs: { a: "5", b: "12" },
    expect: ["13.0000", "67.38"],
    ref: "c=√(25+144)=13.0000 m；∠A=atan2(12,5)=67.38°" },

  { slug: "geometry/rectangle-diagonal",
    inputs: { w: "6", h: "8" },
    expect: ["10.0000", "48.0000"],
    ref: "d=√(36+64)=10.0000 m；面积=6·8=48.0000 m²" },

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
    expect: ["60.000", "94.000"],
    ref: "V=5·4·3=60.000 m³；A=2·(20+12+15)=94.000 m²" },

  { slug: "geometry/sphere-surface-area",
    inputs: { r: "2" },
    expect: ["50.265"],
    ref: "A=4π·4=50.265 m²" },

  { slug: "geometry/sphere-volume",
    inputs: { r: "6" },
    expect: ["904.779"],
    ref: "V=4/3·π·216=904.779 m³" },

  { slug: "geometry/torus-volume",
    inputs: { R: "4", r: "2" },
    expect: ["315.827"],
    ref: "V=2π²·4·4=315.827 m³" },

  { slug: "geometry/ellipse-area",
    inputs: { a: "4", b: "2" },
    expect: ["25.133"],
    ref: "A=π·4·2=25.133 m²" },
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