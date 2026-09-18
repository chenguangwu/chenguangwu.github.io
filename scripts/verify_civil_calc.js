#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "civil/active-earth-rankine", inputs: {"gamma":"20","H":"6","phi":"32","c":"5"}, expect: ["77.4"], ref: "K_a = tan²(45°−32°/2) = 0.3073；z₀ = 2c/(√K_a·γ) = 0.90 m；E_a = ½γH²K_a − 2cH√K_a = 110.63 − 33.27 = 77.4 kN/m（避开默认 18/5/30/0）" },
  { slug: "civil/beam-udl", inputs: {"L":"8","q":"25","E":"30","I":"8000","b":"250","h":"500"}, expect: ["19.20"], ref: "M_max = qL²/8 = 25×64/8 = 200 kN·m；W = bh²/6 = 250×500²/6 = 1.0417×10⁷ mm³；σ = M/W = 200×10⁶/1.0417×10⁷ = 19.20 MPa（避开默认 6/20/200/400）" },
  { slug: "civil/calc-1", inputs: {"fcuk":"40","sigma":"5.0","wc":"0.45","mw":"185","beta":"40","rhoC":"3100","rhoS":"2650","rhoG":"2700","air":"1.0"}, expect: ["1.75 : 2.63 : 0.45"], ref: "f_cu,0 = 40 + 1.645×5 = 48.2 MPa；m_c = m_w/(W/C) = 185/0.45 = 411.1 kg；绝对体积法解得 m_g = 1081.1、m_s = 720.7 kg；质量比 水泥:砂:石:水 = 1 : 1.75 : 2.63 : 0.45（避开默认 C30/W=0.50/β=38）" },
  { slug: "civil/calc-2", inputs: {"straight1":"2500","straight2":"1200","diameter":"25","angle1":"90","angle2":"45","bendFactor":"2.5","cover":"25","num":"3"}, expect: ["3690.1"], ref: "D = 2.5d = 62.5 mm，R = D/2 + d = 56.25；Δ₁(90°) = R·π/2 − 2R·sin45° = 8.81；Δ₂(45°) = R·0.7854 − 2R·sin22.5° = 1.13；无弯钩 → 单根 = 2500 + 1200 − 8.81 − 1.13 = 3690.1 mm（避开默认 3000/0/20/90/0）" },
  { slug: "civil/carbonation-depth", inputs: {"K":"2.5","t":"45"}, expect: ["42.9"], ref: "x = 2.56·K·√t = 2.56 × 2.5 × √45 = 2.56×2.5×6.7082 = 42.9 mm（避开默认 K=2.0/t=30）" },
  { slug: "civil/cft-capacity", inputs: {"D":"500","t":"12","fc":"50","fy":"390"}, expect: ["17852"], ref: "A_c = π(500−24)²/4 = 177952 mm²；A_s = π(500²−476²)/4 = 18397 mm²；N = A_s·f_y + 1.2·A_c·f_c = 7174892 + 10677143 = 17852 kN（避开默认 400/10/40/345）" },
  { slug: "civil/concrete-volume", inputs: {"a":"5","b":"0.5","c":"0.6","rho":"2500"}, expect: ["3.75"], ref: "V = 5 × 0.5 × 0.6 = 1.500 m³；重量 = V·ρ/1000 = 1.5×2500/1000 = 3.75 t（避开默认 4/0.4/0.5/2400）" },
  { slug: "civil/concrete-wb-ratio", inputs: {"fcu":"45","fb":"50","aa":"0.53","ab":"0.20"}, expect: ["0.527"], ref: "W/B = α_a·f_b/(f_cu,0 + α_a·α_b·f_b) = 0.53×50/(45 + 0.53×0.20×50) = 26.5/50.3 = 0.527（避开默认 38.2/45）" },
  { slug: "civil/excavation-earth", inputs: {"gamma":"20","H":"7","phi":"32","q":"15"}, expect: ["182.8"], ref: "K_a = tan²(45°−16°) = 0.3073；E_a = ½γH²K_a + qHK_a = 150.56 + 32.26 = 182.8 kN/m（避开默认 19/8/30/10）" },
  { slug: "civil/isolated-footing", inputs: {"N":"1000","M":"120","fa":"220","gamma":"20","d":"1.8","B":"3.0"}, expect: ["173.8"], ref: "A = 9 m²；p_avg = (N + γAd)/A = (1000+324)/9 = 147.1 kPa；p_max = p_avg + M/(B³/6) = 147.1 + 120/4.5 = 173.8 kPa ≤ 1.2f_a（避开默认 800/80/200/1.5/2.5）" },
  { slug: "civil/load-combination", inputs: {"Sg":"60","Sq":"40","gG":"1.3","gQ":"1.5"}, expect: ["138.0"], ref: "S = γ_G·S_Gk + γ_Q·S_Qk = 1.3×60 + 1.5×40 = 78 + 60 = 138.0 kN·m（避开默认 50/30）" },
  { slug: "civil/masonry-bearing", inputs: {"f":"3.0","b":"370","L":"4000","phi":"1.0"}, expect: ["4440"], ref: "A = 370 × 4000 = 1.48×10⁶ mm²；N = φ·f·A/1000 = 1.0×3.0×1.48×10⁶/1000 = 4440 kN（避开默认 2.5/240/3000）" },
  { slug: "civil/one-way-slab", inputs: {"M":"12","h":"150","fc":"14.3","fy":"360","as":"20"}, expect: ["263 每米配筋"], ref: "h₀ = 150 − 20 = 130 mm；α_s = M/(α₁f_c b h₀²) = 12×10⁶/(14.3×1000×130²) = 0.0497；ξ = 1−√(1−2α_s) = 0.0510；A_s = ξf_c b h₀/f_y = 263 mm²/m（避开默认 8/120）" },
  { slug: "civil/pile-capacity", inputs: {"d":"0.8","L":"20","qs":"50","qp":"2500","K":"2"}, expect: ["1885"], ref: "A_p = πd²/4 = 0.5027 m²；u = πd = 2.513 m；R_a = (q_p·A_p + u·q_s·L)/K = (1257 + 2513)/2 = 1885 kN（避开默认 0.6/15/40/2000）" },
  { slug: "civil/rc-beam-rebar", inputs: {"M":"200","b":"300","h":"600","fc":"14.3","fy":"360","as":"40"}, expect: ["0.64 配筋率"], ref: "h₀ = 560 mm；α_s = 200×10⁶/(14.3×300×560²) = 0.1487；ξ = 1−√(1−2α_s) = 0.1617；A_s = ξf_c b h₀/f_y = 1080 mm²；ρ = A_s/(bh₀) = 0.64%（避开默认 150/250/500）" },
  { slug: "civil/rebar-anchorage", inputs: {"fy":"400","ft":"1.71","d":"25","za":"1.0"}, expect: ["819"], ref: "l_ab = 0.14·α·(f_y/f_t)·d = 0.14 × 1.0 × (400/1.71) × 25 = 819 mm（避开默认 360/1.43/20）" },
  { slug: "civil/rebar-weight", inputs: {"d":"25","L":"12","n":"8"}, expect: ["370.2"], ref: "每米重 = 0.00617d² = 0.00617×625 = 3.856 kg/m；总重 = 3.856 × 12 × 8 = 370.2 kg（避开默认 20/9/10）" },
  { slug: "civil/rock-mass-rating", inputs: {"s1":"15","s2":"15","s3":"12","s4":"25","s5":"12"}, expect: ["79 RMR"], ref: "RMR = 15+15+12+25+12 = 79 → II 级（好）（避开默认 12/13/10/20/10 = 65；两者同为 II 级，故断言总分而非级别）" },
  { slug: "civil/slope-stability-fos", inputs: {"gamma":"20","z":"4","alpha":"25","c":"15","phi":"30"}, expect: ["1.73"], ref: "F_s = (c + γz·cos²α·tanφ)/(γz·sinα·cosα) = (15 + 20×4×0.8214×0.5774)/(20×4×0.4226×0.9063) = 52.94/30.64 = 1.73（避开默认 19/3/30/10/28）" },
  { slug: "civil/two-way-slab", inputs: {"q":"12","lx":"5","ly":"6"}, expect: ["1.16"], ref: "l_x ≤ l_y → α_x = 0.10，α_y = 0.06；M_x = 0.10×12×25 = 30.00，M_y = 0.06×12×36 = 25.92；比值 = 1.16（避开默认 10/4/5）" },
  { slug: "civil/wind-load", inputs: {"w0":"0.6","mz":"1.3","ms":"1.3","bz":"1.7"}, expect: ["1.724"], ref: "w_k = β_z·μ_s·μ_z·w_0 = 1.7 × 1.3 × 1.3 × 0.6 = 1.724 kN/m²（避开默认 0.5/1.0/1.3/1.5）" },
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
  console.log("==== civil calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();