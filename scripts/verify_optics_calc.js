#!/usr/bin node
/**
 * optics 分类计算正确性验证（覆盖 tools/optics/ 全部 21 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_optics_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 注意（nuclear 分类教训）：文本型分支断言必须选「默认态不会走到」的那一支，
 *   否则默认态即命中形成假通过。本文件 3 处已按此处理：
 *   - magnification-optics 默认 M<0（倒立） → 用例取正像距得「正立」
 *   - thin-lens-equation  默认 dᵢ>0（实像）→ 用例取 dₒ<f 得「虚像」
 *   - snells-law          默认折射分支     → 用例取全反射分支
 *
 * 跑法:
 *   node scripts/verify_optics_calc.js                # 全部
 *   node scripts/verify_optics_calc.js snells-law     # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "optics/angular-magnification",
    inputs: { N: "200", f: "8" },
    expect: ["25.00"],
    ref: "M=N/f=200/8=25.00（8 cm 焦距放大镜约放大 25 倍）" },

  { slug: "optics/brewster-angle",
    inputs: { n1: "1.0", n2: "1.6" },
    expect: ["57.995 布儒斯特角"],
    ref: "θ_B=arctan(n₂/n₁)=arctan(1.6)=57.995°" },

  { slug: "optics/combined-lens-focal",
    inputs: { f1: "0.15", f2: "0.25" },
    expect: ["0.0937"],
    ref: "1/F=1/0.15+1/0.25=10.6667 → F=0.0937 m" },

  { slug: "optics/doppler-optical",
    inputs: { f: "4.5e14", v: "1.2e6", c: "3e8" },
    expect: ["4.518e+14"],
    ref: "f′=f(1+v/c)=4.5e14×1.004=4.518e+14 Hz（蓝移）" },

  { slug: "optics/focal-length-mirror",
    inputs: { R: "35" },
    expect: ["17.50"],
    ref: "f=R/2=35/2=17.50 cm" },

  { slug: "optics/fresnel-reflectance",
    inputs: { n1: "1.0", n2: "1.7" },
    expect: ["6.72 反射率", "93.28 透射率 (%)"],
    ref: "R=((1−1.7)/(1+1.7))²=(−0.2593)²=0.0672→6.72%；透射 93.28%" },

  // 默认态 do>0/di>0 → M<0「倒立」；此处取负像距走「正立」分支，避免默认态命中
  { slug: "optics/magnification-optics",
    inputs: { do: "0.5", di: "-0.2" },
    expect: ["0.400", "正立"],
    ref: "M=−dᵢ/dₒ=−(−0.2)/0.5=0.400，M>0 故为正立（虚像情形）" },

  { slug: "optics/malus-law",
    inputs: { I0: "200", th: "30" },
    expect: ["150.00"],
    ref: "I=I₀cos²θ=200×cos²30°=200×0.75=150.00" },

  { slug: "optics/mirror-equation",
    inputs: { f: "0.3", do: "0.8" },
    expect: ["0.4800"],
    ref: "1/dᵢ=1/f−1/dₒ=3.3333−1.25=2.0833 → dᵢ=0.4800 m" },
  { slug: "optics/mirror-equation",
    inputs: { f: "-0.2", do: "0.5" },
    expect: ["-0.1429"],
    ref: "凸面镜成像（f 为有符号量，凹正凸负）：f=-0.2 m、dₒ=0.5 m → 1/dᵢ=1/f−1/dₒ=-5−2=-7 → dᵢ=-0.1429 m（虚像、缩小、正立）；旧版把 f 列入「不能为负」拦截，页面文案/算例承诺的凸面镜功能被屏蔽。-0.1429 非默认 ⇒ 零逃生。" },
  { slug: "optics/mirror-equation",
    clicks: ["document.getElementById('f').value='0';document.getElementById('do').value='0.5';calcTool();var h=String(document.getElementById('result').textContent||document.getElementById('result').innerHTML);document.getElementById('f').value='FZERO_'+(h.indexOf('不能为 0')>=0?'OK':'BAD');"],
    expect: ["FZERO_OK"],
    ref: "PQ-20 清账（f=0 分母守卫）：f=0、dₒ=0.5 时 1/f 发散、dᵢ=1/(∞−2) 收敛成 0，旧版输出「像距 0、放大率 0」伪结果；现 __D 含 f，f=0 提示「焦距不能为 0」。探针断言结果含「不能为 0」，旧版 ⇒ FZERO_BAD，零逃生。" },

  { slug: "optics/optical-power-diopter",
    inputs: { f: "0.25" },
    expect: ["4.00"],
    ref: "P=1/f=1/0.25=4.00 D" },

  { slug: "optics/prism-deviation",
    inputs: { n: "1.6", A: "15" },
    expect: ["9.00"],
    ref: "δ≈(n−1)·A=0.6×15=9.00°（小角度近似）" },

  { slug: "optics/snells-law",
    inputs: { n1: "1", n2: "1", t1: "120" },
    expect: ["入射角 θ₁ 为相对法线的角度"],
    ref: "折射率相等时 120° 仍会被反正弦压回 60°，看似有效；新增 0≤θ₁<90 校验后必须直接提示越界。" },

  { slug: "optics/fresnel-reflectance",
    inputs: { n1: "1", n2: "-0.5" },
    expect: ["均必须 &gt; 0"],
    ref: "n₂=-0.5 旧版会输出 R=900%、T=-800%；新增正折射率校验后拒绝计算。" },

  { slug: "optics/optical-power-diopter",
    inputs: { f: "-0.5" },
    expect: ["-500.0000 焦距 (mm，带符号)", "-2.00"],
    ref: "发散透镜 f=-0.5 m：P=-2.00 D，毫米焦距应为 -500.0000 mm，不能丢符号显示 500。" },

  { slug: "optics/prism-deviation",
    inputs: { n: "1.5", A: "60" },
    expect: ["37.181", "30.00"],
    ref: "精确最小偏向角 δ_min=2arcsin(1.5·sin30°)-60=37.181°；小角近似 (1.5-1)×60=30.00°，两者并列展示。" },

  { slug: "optics/rayleigh-criterion",
    inputs: { lam: "600e-9", D: "0.2" },
    expect: ["3.6600", "7.549e-1"],
    ref: "θ=1.22λ/D=1.22×600e-9/0.2=3.66e-6 rad=3.6600 µrad=7.549e-1 角秒" },

  { slug: "optics/refractive-index-speed",
    inputs: { v: "1.5e8", c: "3e8" },
    expect: ["2.0000"],
    ref: "n=c/v=3e8/1.5e8=2.0000" },

  { slug: "optics/resolving-power",
    inputs: { D: "0.25", lam: "500" },
    expect: ["409836"],
    ref: "R=D/(1.22λ)=0.25/(1.22×500e-9)=409836 m⁻¹" },

  { slug: "optics/separated-lenses-focal",
    inputs: { f1: "12", f2: "18", d: "3" },
    expect: ["8.000"],
    ref: "1/F=1/12+1/18−3/(12×18)=0.0833+0.0556−0.01389=0.125 → F=8.000 cm" },

  { slug: "optics/single-slit-diffraction",
    inputs: { a: "2e-4", lam: "450e-9", m: "1" },
    expect: ["0.1289"],
    ref: "sinθ=mλ/a=450e-9/2e-4=2.25e-3 → θ=arcsin(2.25e-3)=0.1289°" },

  // 默认态（1.0→1.5，30°）为折射分支；此处取全反射分支，避免默认态命中折射角文本
  { slug: "optics/snells-law",
    inputs: { n1: "1.5", n2: "1.0", t1: "60" },
    expect: ["发生全反射（无折射）"],
    ref: "n₁sinθ₁/n₂=1.5×sin60°=1.299>1，超过临界角，发生全反射" },

  { slug: "optics/thin-film-max",
    inputs: { n: "1.4", t: "350", m: "1" },
    expect: ["980.0"],
    ref: "λ=2nt/m=2×1.4×350/1=980.0 nm（相长干涉，近红外）" },

  { slug: "optics/thin-film-min",
    inputs: { n: "1.4", t: "350", m: "1" },
    expect: ["653.3"],
    ref: "λ=2nt/(m+0.5)=2×1.4×350/1.5=653.3 nm（相消干涉，红光）" },

  // 默认态 dₒ>f（0.3>0.1）为实像；此处取 dₒ<f 走虚像分支
  { slug: "optics/thin-lens-equation",
    inputs: { f: "0.3", do: "0.2" },
    expect: ["-0.6000", "虚像"],
    ref: "1/dᵢ=1/0.3−1/0.2=3.3333−5=−1.6667 → dᵢ=−0.6000 m<0，故为虚像" },

  { slug: "optics/thin-lens-equation",
    inputs: { f: "0.25", do: "0.5" },
    expect: ["像距 d_i = 0.5000 m（正）", "放大率 m = -1.0000"],
    ref: "1/dᵢ=1/0.25−1/0.5=4−2=2 → dᵢ=0.5000 m（实像）；m=−dᵢ/d_o=−1.0000（倒立等大）。默认 f0.1/do0.3→dᵢ0.1500/m−0.5000，避开 A===B。注意 expect 为「或」匹配：裸串『0.5000』会被默认态『-0.5000』子串命中而变逃生项，故必须带『像距 d_i = 』上下文。" },

  {
    slug: "optics/thin-lens-equation",
    clicks: ["var e=function(id){return document.getElementById(id);};e('f').value='0.1';e('do').value='0.1';calcTool();var r=String(e('result').innerHTML||'')+'|'+String(e('result').textContent||'');var b=String(e('thinLensNature').innerHTML||'');var s=String(e('thinLensRay').innerHTML||'');document.getElementById('__tbProbe').textContent='LENSFOC svgEmpty='+(s===''?1:0)+' svgInf='+(s.indexOf('Infinity')>=0?1:0)+' msg='+(r.indexOf('像在无穷远')>=0?1:0)+' nat='+(b.indexOf('出射光平行')>=0?1:0);"],
    expect: ["LENSFOC svgEmpty=1 svgInf=0 msg=1 nat=1"],
    ref: "复核失败重做·薄透镜 1/3（焦点边界）：f=0.1m、d_o=0.1m 时 1/dᵢ=0，dᵢ 与 m 发散。修复前 calcRay 仍判「实像·倒立·放大」并把 Infinity 写进 SVG 坐标（svgEmpty=0 svgInf=1）；修复后结果区明确「像在无穷远」、结论区写「出射光平行」、清空错误光路图 ⇒ LENSFOC svgEmpty=1 svgInf=0 msg=1 nat=1。"
  },
  {
    slug: "optics/thin-lens-equation",
    clicks: ["var e=function(id){return document.getElementById(id);};e('f').value='0.1';e('do').value='0.3';calcTool();var s1=String(e('thinLensRay').innerHTML||''),b1=String(e('thinLensNature').innerHTML||'');e('f').value='';calcTool();var s2=String(e('thinLensRay').innerHTML||''),b2=String(e('thinLensNature').innerHTML||'');e('f').value='0.1';calcTool();var s3=String(e('thinLensRay').innerHTML||'');document.getElementById('__tbProbe').textContent='LENSCLR first='+(s1.indexOf('<svg')>=0?1:0)+' empty='+((s2===''&&b2==='')?1:0)+' restore='+(s3.indexOf('<svg')>=0?1:0);"],
    expect: ["LENSCLR first=1 empty=1 restore=1"],
    ref: "复核失败重做·薄透镜 2/3（有效→空→恢复）：清空焦距后 __tbInputGuard 早退，旧实现不调 calcRay ⇒ #thinLensNature / #thinLensRay 保留旧图和旧结论（empty=0）；修复后早退同样走 calcRay 清空，恢复有效输入后重新出图 ⇒ LENSCLR first=1 empty=1 restore=1。"
  },
  {
    slug: "optics/thin-lens-equation",
    clicks: ["var e=function(id){return document.getElementById(id);};e('f').value='0.1';e('do').value='0.09';calcTool();var sv=String(e('thinLensRay').innerHTML||''),bv=String(e('thinLensNature').innerHTML||'');e('do').value='0.11';calcTool();var sr=String(e('thinLensRay').innerHTML||''),br=String(e('thinLensNature').innerHTML||'');document.getElementById('__tbProbe').textContent='LENSSIDE virt='+((bv.indexOf('虚像')>=0&&sv.indexOf('<svg')>=0&&sv.indexOf('Infinity')<0)?1:0)+' real='+((br.indexOf('实像')>=0&&sr.indexOf('<svg')>=0&&sr.indexOf('Infinity')<0)?1:0);"],
    expect: ["LENSSIDE virt=1 real=1"],
    ref: "复核失败重做·薄透镜 3/3（焦点两侧护栏）：d_o=0.09（虚像）与 0.11（实像）都应正常出 SVG、结论分别为虚像/实像且不含 Infinity。本例修复前后都应 PASS，证明焦点分支没有误伤两侧。"
  },
  {
    slug: "optics/thin-lens-equation",
    clicks: ["globalThis.TBKit={util:{isEn:function(){return false;}},matrix:{table:function(){}},history:{record:function(){throw Error('invalid input recorded');}}};var e=function(id){return document.getElementById(id);};e('f').value='';e('do').value='0.4';e('thin_lens_equationDiff').textContent='OLD COMPARISON';__thin_lens_equationExtras();document.getElementById('__tbProbe').textContent='LENSINVALID diffCleared='+(e('thin_lens_equationDiff').textContent===''?1:0);"],
    expect: ["LENSINVALID diffCleared=1"],
    ref: "真实页面连续计算两个有效值后清空焦距，旧结果对比条必须清除；探针模拟已有对比条并走真实 extras 的无效输入分支，不能残留旧计算结论。"
  },
  { slug: "optics/young-fringe",
    inputs: { lam: "480", L: "2", d: "0.4" },
    expect: ["2.400"],
    ref: "Δy=λL/d=480e-9×2/(0.4e-3)=2.4e-3 m=2.400 mm" },
  { slug: "optics/young-fringe",
    inputs: { lam: "0", L: "2", d: "0.4" },
    expect: ["波长 λ、屏距 L、缝距 d 均必须 > 0"],
    ref: "998 分母误标修复（PQ-04）：λ=0 旧版被误标「波长 λ 是本计算的分母，不能为 0」，实际 λ 在分子；修复后只把 d 当分母，零值走统一正性提示。" },
  {
    "slug": "optics/angular-magnification",
    "inputs": {
      "N": "42",
      "f": "42"
    },
    "expect": [
      "与两倍焦距之比 1.00 放大率平方"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"N\":\"42\",\"f\":\"42\"}，输出区含「与两倍焦距之比 1.00 放大率平方」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/combined-lens-focal",
    "inputs": {
      "f1": "42",
      "f2": "42"
    },
    "expect": [
      "焦度 (屈光度) 21000.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f1\":\"42\",\"f2\":\"42\"}，输出区含「焦度 (屈光度) 21000.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/brewster-angle",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "率比 n2/n1 45.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「率比 n2/n1 45.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/focal-length-mirror",
    "inputs": {
      "R": "42"
    },
    "expect": [
      "数 (1/cm) 2.380952"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\"}，输出区含「数 (1/cm) 2.380952」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/magnification-optics",
    "inputs": {
      "do": "42",
      "di": "42"
    },
    "expect": [
      "焦距 f (m) 1.000 放大率绝对值"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"do\":\"42\",\"di\":\"42\"}，输出区含「焦距 f (m) 1.000 放大率绝对值」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/doppler-optical",
    "inputs": {
      "f": "42",
      "v": "42",
      "c": "42"
    },
    "expect": [
      "|v/c| 必须小于 1"
    ],
    "ref": "f=42,v=42,c=42 ⇒ v/c=1，相对速度达到光速，页面应拒绝而不是给出有限频移；默认态不含该提示。"
  },
  {
    "slug": "optics/fresnel-reflectance",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "射率 R (%) 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「射率 R (%) 100」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/malus-law",
    "inputs": {
      "I0": "42",
      "th": "42"
    },
    "expect": [
      "42\n42\n23.20 透射光强 I 18.805 被吸收光强 44.77"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I0\":\"42\",\"th\":\"42\"}，输出区含「42\n42\n23.20 透射光强 I 18.805 被吸收光强 44.77」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/optical-power-diopter",
    "inputs": {
      "f": "42"
    },
    "expect": [
      "42000.0000 焦距 (mm，带符号)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\"}，输出区含「42000.0000 焦距 (mm，带符号)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/mirror-equation",
    "inputs": {
      "f": "42",
      "do": "42"
    },
    "expect": [
      "距减焦距 (m) 84.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"do\":\"42\"}，输出区含「距减焦距 (m) 84.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/prism-deviation",
    "inputs": {
      "n": "42",
      "A": "42"
    },
    "expect": [
      "1722.00 小角近似"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"A\":\"42\"}，输出区含「1722.00 小角近似」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/refractive-index-speed",
    "inputs": {
      "v": "42",
      "c": "42"
    },
    "expect": [
      "00 折射率 n 1.000000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"c\":\"42\"}，输出区含「00 折射率 n 1.000000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/rayleigh-criterion",
    "inputs": {
      "lam": "42",
      "D": "42"
    },
    "expect": [
      "角 (µrad) 2.516e+5 θ (角秒) 1.220e+0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\",\"D\":\"42\"}，输出区含「角 (µrad) 2.516e+5 θ (角秒) 1.220e+0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/separated-lenses-focal",
    "inputs": {
      "f1": "42",
      "f2": "42",
      "d": "42"
    },
    "expect": [
      "42\n42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f1\":\"42\",\"f2\":\"42\",\"d\":\"42\"}，输出区含「42\n42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/resolving-power",
    "inputs": {
      "D": "42",
      "lam": "42"
    },
    "expect": [
      "1.220e-9 最小分辨角 θ_min (rad)"
    ],
    "ref": "D=42m、λ=42nm ⇒ θ_min=1.22×42e-9/42=1.220e-9 rad；页面按角分辨极限输出，不再标成 1/m 的 R。"
  },
  {
    "slug": "optics/single-slit-diffraction",
    "inputs": {
      "a": "1e-4",
      "lam": "600e-9",
      "m": "2"
    },
    "expect": [
      "0.6876 暗纹角 θ (°)",
      "0.3438 第一暗纹角 θ₁ (°)"
    ],
    "ref": "单缝暗纹条件 a·sinθ=mλ：m=2、λ=600nm、a=0.1mm ⇒ sinθ=0.012，θ=arcsin(0.012)=0.6876°；第一暗纹 θ₁=arcsin(600e-9/1e-4)=0.3438°。原自动补强用例 a=λ=m=42 ⇒ sinθ=42>1，asin 越界被页面校验拦截，期望串恒不成立，已改为合法物理输入。"
  },
  {
    "slug": "optics/snells-law",
    "inputs": {
      "n1": "42",
      "n2": "42",
      "t1": "42"
    },
    "expect": [
      "42\n42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\",\"t1\":\"42\"}，输出区含「42\n42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/thin-film-max",
    "inputs": {
      "n": "42",
      "t": "42",
      "m": "42"
    },
    "expect": [
      "长 λ (nm) 3528"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"t\":\"42\",\"m\":\"42\"}，输出区含「长 λ (nm) 3528」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/thin-film-min",
    "inputs": {
      "n": "42",
      "t": "42",
      "m": "42"
    },
    "expect": [
      "82.0"
    ],
    "ref": "第967批复核：n=n1? 默认 n1=1、n2=1.5，n=42 时只有第一界面发生 π 跃变，相消分母=m+0.5+0.5=43 ⇒ 2×42×42/43=82.0。原 83.0 假设两界面相位相同，未计 n2=1.5<n 的单侧跃变。"
  },
  {
    "slug": "optics/young-fringe",
    "inputs": {
      "lam": "42",
      "L": "42",
      "d": "42"
    },
    "expect": [
      "23.8095 条纹密度"
    ],
    "ref": "λ=42nm、L=42m、d=42mm ⇒ Δy=0.042mm，条纹密度=1/Δy=23.8095 1/mm；不再用屏距冒充视场宽度。"
  },
  {
    "slug": "optics/thin-lens-equation",
    "inputs": {
      "f": "42",
      "do": "43"
    },
    "expect": [
      "1806.0000", "-42.0000"
    ],
    "ref": "焦点边界重做同批同步：原自动补强用例用 f=42 / d_o=42 恰好落在焦点上，修复后该输入改走「出射光平行、像在无穷远」分支，旧的 dataGrid 断言必然漂移 ⇒ inputs 改为非焦点的 42/43。1/dᵢ=1/42−1/43 ⇒ dᵢ=1806.0000 m、m=−42.0000，expect 取真实派生结论串（依赖两个注入值；默认态 f0.1/d_o0.3 不含）⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/malus-law",
    "inputs": { "I0": "0", "th": "60" },
    "expect": ["— 吸收光强占比 (%)"],
    "ref": "1000 I₀=0 时吸收占比不再用 1e-9 兜底伪造巨大百分比（PQ-01）；旧版显示 1000000000.00，修复后显示「—」。默认 I₀=100 不含该串。"
  },
  {
    "slug": "optics/malus-law",
    "inputs": { "I0": "-100", "th": "60" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__malus_lawExtras();document.getElementById('__tbProbe').textContent='MALUSBAD '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["MALUSBAD OK"],
    "ref": "1000 马吕斯明细同步主区 I₀≥0 校验（PQ-01）：旧版负光强仍写 4 行明细并记历史，修复后清表且不记录。探针只在 clicks 注入后出现，默认态零逃生。"
  },
  {
    "slug": "optics/brewster-angle",
    "inputs": { "n1": "0", "n2": "1.5" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__brewster_angleExtras();document.getElementById('__tbProbe').textContent='BREWBAD '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["BREWBAD OK"],
    "ref": "1000 布儒斯特明细同步主区 n₁>0 校验（PQ-02）：旧版 n₁=0 仍写 3 行明细并用 n1||1 造伪比值，修复后清表且不记录。默认 n₁=1 不含该串。"
  },
  {
    "slug": "optics/brewster-angle",
    "inputs": { "n1": "1.5", "n2": "1.33" },
    "clicks": ["var p=null;globalThis.TBKit={preset:{bar:function(sel,items){p=items;}},util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__brewster_anglePresets();var vals=p?p.map(function(x){return x.values.n1+'/'+x.values.n2;}).join('|'):'NONE';document.getElementById('__tbProbe').textContent='BRWPRE '+vals;"],
    "expect": ["BRWPRE 1.0/1.5|1/1.33|1.5/1.33"],
    "ref": "1000 布儒斯特预设改为不同介质比值（PQ-03）：旧版 2×/0.5× 的 n2/n1 恒 1.5、三个预设输出完全相同；新版空气→水 1.33 与玻璃→水 1.33/1.5 给出不同角度。默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "optics/prism-deviation",
    "inputs": { "n": "-1", "A": "10" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__prism_deviationExtras();document.getElementById('__tbProbe').textContent='PRISMBAD '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["PRISMBAD OK"],
    "ref": "1001 棱镜明细同步主区 n>0 校验：旧版 n=-1、A=10° 仍写 4 行明细并记历史；修复后清表且不记录。默认 n=1.5 不含该串。"
  }

,
{ slug: "optics/focal-length-mirror", inputs: { R: "-20" }, expect: ["-10.00", "-10.0000"], ref: "凸面镜 R=-20cm ⇒ f=-10cm，光焦度=100/(-10)=-10 D；负号必须保留。" },
{ slug: "optics/focal-length-mirror", inputs: { R: "0" }, expect: ["不能为 0"], ref: "R=0 是平面镜，焦距无有限值；不能除零后给伪光焦度。" },
{ slug: "optics/focal-length-mirror", inputs: { R: "" }, expect: ["请填写曲率半径"], ref: "空白不等于 0；旧实现按 0 算会得到 f=0 与巨大光焦度。" },
{ slug: "optics/young-fringe", inputs: { lam: "600", L: "1.2", d: "0.4" }, expect: ["1.800", "0.5556", "条纹密度"], ref: "Δy=550e-9×1/(0.5e-3)=1.1e-3m=1.100mm；密度=1/1.1=0.9091 1/mm。" },
{ slug: "optics/mirror-equation", inputs: { f: "0.3", do: "0.8" }, expect: ["0.4800", "实像"], ref: "凹面镜 f=0.2、d_o=0.5 ⇒ d_i=0.3333m>0，本页约定为镜前实像。" },
{ slug: "optics/mirror-equation", inputs: { f: "-0.2", do: "0.5" }, expect: ["-0.1429", "虚像"], ref: "凸面镜 f=-0.2、d_o=0.5 ⇒ d_i=-0.1429m<0，镜后虚像；不能按与 f 同号判实像。" },
{ slug: "optics/mirror-equation", inputs: { f: "0.2", do: "0.2" }, expect: ["无有限像距"], ref: "物在焦点 ⇒ 1/f-1/d_o=0，出射平行，不能给有限 d_i。" },
{ slug: "optics/brewster-angle", inputs: { n1: "1.0", n2: "1.6" }, expect: ["57.995", "反射角 θ_r", "折射角 θ_t"], ref: "θ_B=arctan(1.5)=56.310°；反射角=θ_B，折射角=90-θ_B=33.690°，互补角不是反射光方向角。" },
{ slug: "optics/doppler-optical", inputs: { f: "5e14", v: "1.2e6", c: "3e8" }, expect: ["5.020e+14", "蓝移（接近）"], ref: "v>0 约定为接近，f′=f(1+v/c)=5.005e14，频率升高为蓝移。" },
{ slug: "optics/doppler-optical", inputs: { f: "5e14", v: "-300000", c: "3e8" }, expect: ["4.995e+14", "红移（远离）"], ref: "v<0 约定为远离，频率降低为红移；与正速度方向相反。" },
{ slug: "optics/doppler-optical", inputs: { f: "5e14", v: "0", c: "3e8" }, expect: ["无频移"], ref: "零速度应输出无频移，不能因 v=0 被判空值。" },
{ slug: "optics/doppler-optical", inputs: { f: "5e14", v: "1e8", c: "3e8" }, expect: ["|v/c|≥0.1"], ref: "v/c=0.333，经典一阶近似误差明显，页面应提示改用相对论公式。" },
{ slug: "optics/magnification-optics", inputs: { do: "0.3", di: "-0.3" }, expect: ["无有限焦距"], ref: "d_o+d_i=0 时等效焦距分母为零，不能替换为 1 后给 -0.09。" },
{ slug: "optics/magnification-optics", inputs: { do: "0.5", di: "0.2" }, expect: ["-0.400", "0.1429"], ref: "M=-0.15/0.3=-0.500；f=0.3×0.15/(0.45)=0.1000m。" },
{ slug: "optics/magnification-optics", inputs: { do: "2", di: "0" }, expect: ["0.000", "取向不适用——像高为零", "退化：f=0"], ref: "第873批：di=0 ⇒ M=0、f=0，像高为零，不能判正立/倒立，更不能称等大；旧实现以 |M|=0 落入 else 分支误显示等大。" },
{ slug: "optics/combined-lens-focal", inputs: { f1: "0.1", f2: "-0.1" }, expect: ["无焦系统", "等效焦距→∞"], ref: "密接双镜光焦度 10+(-10)=0，等效焦距趋于无穷；不能只显示 —。" },
{ slug: "optics/separated-lenses-focal", inputs: { f1: "10", f2: "-10", d: "0" }, expect: ["无焦系统", "等效焦距→∞"], ref: "分离双镜在 d=0 时退化为密接，f1/f2 异号等值 ⇒ 组合光焦度为 0。" },
{ slug: "optics/resolving-power", inputs: { D: "0.2", lam: "600" }, expect: ["3.660e-6", "角分辨本领 1/θ_min"], ref: "θ_min=1.22×550e-9/0.1=6.71e-6 rad；1/θ≈1.49e5 rad⁻¹，不能标成 1/m。" },
{ slug: "optics/resolving-power", inputs: { D: "0", lam: "550" }, expect: ["必须大于 0"], ref: "D=0 时最小分辨角无定义，不能以 1e-12 兜底。" },
{ slug: "optics/angular-magnification", inputs: { N: "250", f: "-20" }, expect: ["均须大于 0"], ref: "负焦距不适用于简单放大镜 M=N/f 模型，旧 Math.max 会给出伪正比值。" },
{ slug: "optics/angular-magnification", inputs: { N: "200", f: "8" }, expect: ["25.00", "0.040000"], ref: "M=250/25=10.00；f/N=0.100000；不得用 max 改写负值。" },
{ slug: "optics/thin-lens-equation", inputs: { f: "-0.1", do: "0.3" }, expect: ["-0.0750", "虚像", "光路图仅支持凸透镜"], ref: "凹透镜 f=-0.1、d_o=0.3 ⇒ d_i=-0.075m 虚像；主计算保留，光路图明确提示不支持。" },
{ slug: "optics/thin-lens-equation", inputs: { f: "0.2", do: "0.5" }, expect: ["0.3333"], ref: "凸透镜 f=0.1、d_o=0.3 ⇒ d_i=0.15m 实像，回归主路径。" }

,
  { slug: "optics/thin-film-max", inputs: { n: "1.2", t: "300", m: "0", n1: "1", n2: "1" }, expect: ["1440.0"], ref: "第967批：反射光下 n=1.2 夹在 n1=n2=1 之间，只有第一界面 π 跃变 δ=0.5；m=0 时 λ=2×1.2×300/0.5=1440.0 nm。旧页固定 λ=2nt/m，m=0 直接拒绝，无法表达该条件。" },
  { slug: "optics/thin-film-min", inputs: { n: "1.2", t: "300", m: "1", n1: "1", n2: "1" }, expect: ["360.0"], ref: "第967批：同一单侧 π 跃变下相消分母=m+0.5+0.5=2，λ=720/2=360.0 nm；旧页固定 m+0.5 ⇒ 480.0。" },
  { slug: "optics/thin-film-max", inputs: { n: "1.2", t: "300", m: "1", n1: "1", n2: "1.5", obs: "transmitted" }, expect: ["720.0", "透射光"], ref: "第967批：透射光无反射相位跃变，相长分母=m=1 ⇒ λ=720.0；旧页无观察光选项，无法区分反射/透射。" },
  { slug: "optics/thin-film-max", inputs: { n: "1.33", t: "500", m: "0", n1: "1", n2: "1.5" }, expect: ["须不小于 1"], ref: "第967批：两界面均 π 跃变 δ=0 时相长条件 2nt=mλ，m=0 无解，必须拒绝而不是除零。" },
  { slug: "optics/thin-film-min", inputs: { n: "1.33", t: "500", m: "1", n1: "0", n2: "1.5" }, expect: ["大于 0"], ref: "第967批：两侧介质折射率必须为有限正数，n1=0 无物理意义。" }
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

  console.log("==== optics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();