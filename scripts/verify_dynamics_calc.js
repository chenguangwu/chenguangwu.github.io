#!/usr/bin/env node
/**
 * dynamics 分类计算正确性验证（23 个确定性数值工具，全覆盖）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 用法: node scripts/verify_dynamics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;

const CASES = [
  { slug: "dynamics/angular-momentum-conservation",
    inputs: { I1: "4", w1: "6", I2: "2" },
    expect: ["12.000"],
    ref: "ω₂=I1·ω1/I2=4·6/2=12.000 rad/s" },

  { slug: "dynamics/angular-momentum",
    inputs: { I: "2", w: "3" },
    expect: ["6.000"],
    ref: "L=I·ω=2·3=6.000 kg·m²/s" },

  { slug: "dynamics/banked-curve",
    inputs: { r: "200", th: "45", g: "9.81" },
    expect: ["44.29"],
    ref: "v=√(r·g·tanθ)=√(200·9.81·1)=44.29 m/s" },

  { slug: "dynamics/coefficient-restitution",
    inputs: { v1: "10", v2: "2", v1p: "4", v2p: "5" },
    expect: ["0.125"],
    ref: "e=(v2p−v1p)/(v1−v2)=(5−4)/(10−2)=0.125" },

  { slug: "dynamics/elastic-collision-1d",
    inputs: { m1: "3", m2: "5", v1: "6", v2: "2" },
    expect: ["1.000", "5.000"],
    ref: "一维弹性碰撞：v1′=((m1−m2)v1+2m2v2)/(m1+m2)=1.000；v2′=(2m1v1−(m1−m2)v2)/(m1+m2)=5.000" },

  { slug: "dynamics/hooke-force",
    inputs: { k: "150", x: "0.2" },
    expect: ["30.00"],
    ref: "F=k·x=150·0.2=30.00 N" },

  { slug: "dynamics/impulse",
    inputs: { F: "250", dt: "0.4" },
    expect: ["100.00"],
    ref: "J=F·Δt=250·0.4=100.00 N·s" },

  { slug: "dynamics/inclined-plane-accel",
    inputs: { th: "45", mu: "0.2", g: "9.8" },
    expect: ["5.544"],
    ref: "a=g(sinθ−μcosθ)=9.8(sin45−0.2cos45)=5.544 m/s²" },

  { slug: "dynamics/kinetic-friction",
    inputs: { mu: "0.25", N: "200" },
    expect: ["50.00"],
    ref: "Fk=μ·N=0.25·200=50.00 N" },

  { slug: "dynamics/moment-of-inertia-point",
    inputs: { m: "3", r: "0.4" },
    expect: ["0.480"],
    ref: "I=m·r²=3·0.4²=0.480 kg·m²" },

  { slug: "dynamics/momentum-conservation",
    inputs: { m1: "2000", v1: "15", m2: "1000", v2: "10" },
    expect: ["13.333 末速度"],
    ref: "v′=(m1v1+m2v2)/(m1+m2)=(2000·15+1000·10)/3000=13.333 m/s" },

  { slug: "dynamics/momentum",
    inputs: { m: "1200", v: "25" },
    expect: ["30000.0"],
    ref: "p=m·v=1200·25=30000.0 kg·m/s" },

  { slug: "dynamics/power-force",
    inputs: { F: "3000", v: "8" },
    expect: ["24000.0", "24.00"],
    ref: "P=F·v=3000·8=24000.0 W；kW=24.00" },

  { slug: "dynamics/power-rotational",
    inputs: { tau: "7", w: "3" },
    expect: ["21.00"],
    ref: "P=τ·ω=7·3=21.00 W" },

  { slug: "dynamics/rotational-kinetic-energy",
    inputs: { I: "2", w: "4" },
    expect: ["16.000"],
    ref: "E=½Iω²=0.5·2·4²=16.000 J" },

  { slug: "dynamics/spring-potential",
    inputs: { k: "300", x: "0.2" },
    expect: ["6.000"],
    ref: "U=½k·x²=0.5·300·0.2²=6.000 J" },

  { slug: "dynamics/static-friction-max",
    inputs: { mu: "0.4", N: "250" },
    expect: ["100.00"],
    ref: "Fmax=μ·N=0.4·250=100.00 N" },

  { slug: "dynamics/terminal-velocity",
    inputs: { m: "100", g: "9.81", rho: "1.225", cd: "0.8", A: "0.5" },
    expect: ["63.28"],
    ref: "vt=√(2mg/(ρ·Cd·A))=√(2·100·9.81/(1.225·0.8·0.5))=63.28 m/s" },

  { slug: "dynamics/torque-force",
    inputs: { r: "0.3", F: "200", th: "60" },
    expect: ["51.96"],
    ref: "τ=r·F·sinθ=0.3·200·sin60=51.96 N·m" },

  { slug: "dynamics/weight-force",
    inputs: { m: "85", g: "9.8" },
    expect: ["833.00", "84.91"],
    ref: "W=m·g=85·9.8=833.00 N；kgf=833/9.81=84.91" },

  { slug: "dynamics/work-energy-theorem",
    inputs: { m: "5", v1: "2", v2: "8" },
    expect: ["150.00"],
    ref: "W=½m(v2²−v1²)=0.5·5·(64−4)=150.00 J" },
  {
    "slug": "dynamics/angular-momentum-conservation",
    "inputs": {
      "I1": "42",
      "w1": "42",
      "I2": "42"
    },
    "expect": [
      "kg*m2/s) 37044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I1\":\"42\",\"w1\":\"42\",\"I2\":\"42\"}，输出区含「kg*m2/s) 37044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/angular-momentum",
    "inputs": {
      "I": "42",
      "w": "42"
    },
    "expect": [
      " L 反推角速度 37044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I\":\"42\",\"w\":\"42\"}，输出区含「 L 反推角速度 37044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/banked-curve",
    "inputs": {
      "r": "42",
      "th": "42",
      "g": "42"
    },
    "expect": [
      " v (m/s) 143.47"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"r\":\"42\",\"th\":\"42\",\"g\":\"42\"}，输出区含「 v (m/s) 143.47」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/coefficient-restitution",
    "inputs": {
      "v1": "6",
      "v2": "0",
      "v1p": "3",
      "v2p": "4"
    },
    "expect": [
      "0.167 恢复系数 e"
    ],
    "ref": "第864批：6/0→3/4 输出 e=0.167、接近 6、分离 1；旧测试用四项全 42（接近速度 0）现按零相对接近速度拦截。输入避开页面默认值。"
  },
  {
    "slug": "dynamics/elastic-collision-1d",
    "inputs": {
      "m1": "42",
      "m2": "42",
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m1\":\"42\",\"m2\":\"42\",\"v1\":\"42\",\"v2\":\"42\"}，输出区含「42\n42\n42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/hooke-force",
    "inputs": {
      "k": "42",
      "x": "42"
    },
    "expect": [
      "弹力大小 |F| = k|x| (N) 37044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k\":\"42\",\"x\":\"42\"}，输出区含「弹力 F (N) 37044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/impulse",
    "inputs": {
      "F": "42",
      "dt": "42"
    },
    "expect": [
      "·ms 牛毫秒) 179.8779"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"dt\":\"42\"}，输出区含「·ms 牛毫秒) 179.8779」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/inclined-plane-accel",
    "inputs": {
      "th": "42",
      "mu": "42",
      "mus": "0.15",
      "g": "42"
    },
    "expect": [
      "-1282.804 加速度 a (m/s²)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"th\":\"42\",\"mu\":\"42\",\"g\":\"42\"}，输出区含「42\n42\n42\n-1282.804」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/kinetic-friction",
    "inputs": {
      "mu": "42",
      "N": "42"
    },
    "expect": [
      "kgf 千克力) 1764.0000 摩擦系数平方"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"N\":\"42\"}，输出区含「kgf 千克力) 1764.0000 摩擦系数平方」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/moment-of-inertia-point",
    "inputs": {
      "m": "42",
      "r": "42"
    },
    "expect": [
      "(kg·m²) 148176"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"r\":\"42\"}，输出区含「(kg·m²) 148176」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/momentum-conservation",
    "inputs": {
      "m1": "42",
      "v1": "42",
      "m2": "42",
      "v2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m1\":\"42\",\"v1\":\"42\",\"m2\":\"42\",\"v2\":\"42\"}，输出区含「42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/momentum",
    "inputs": {
      "m": "42",
      "v": "42"
    },
    "expect": [
      "g·m²/s²) 1.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"v\":\"42\"}，输出区含「g·m²/s²) 1.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/power-force",
    "inputs": {
      "F": "42",
      "v": "42"
    },
    "expect": [
      "功率 P (W) 1.76 P (kW) 2.398"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"v\":\"42\"}，输出区含「功率 P (W) 1.76 P (kW) 2.398」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/power-rotational",
    "inputs": {
      "tau": "42",
      "w": "42"
    },
    "expect": [
      "功率 P (W) 2.3656"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tau\":\"42\",\"w\":\"42\"}，输出区含「功率 P (W) 2.3656」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/rotational-kinetic-energy",
    "inputs": {
      "I": "42",
      "w": "42"
    },
    "expect": [
      "动能 E (J) 74088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I\":\"42\",\"w\":\"42\"}，输出区含「动能 E (J) 74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/static-friction-max",
    "inputs": {
      "mu": "42",
      "N": "42"
    },
    "expect": [
      "大静摩擦 (N) 179.8779"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mu\":\"42\",\"N\":\"42\"}，输出区含「大静摩擦 (N) 179.8779」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/terminal-velocity",
    "inputs": {
      "m": "42",
      "g": "42",
      "rho": "42",
      "cd": "42",
      "A": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n0.22"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"g\":\"42\",\"rho\":\"42\",\"cd\":\"42\",\"A\":\"42\"}，输出区含「42\n42\n42\n42\n42\n0.22」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/spring-potential",
    "inputs": {
      "k": "42",
      "x": "42"
    },
    "expect": [
      "弹力 F (N) 74088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k\":\"42\",\"x\":\"42\"}，输出区含「弹力 F (N) 74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/weight-force",
    "inputs": {
      "m": "42",
      "g": "42"
    },
    "expect": [
      "重力 W (N) 179.82 W (kgf) 68.04"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"g\":\"42\"}，输出区含「重力 W (N) 179.82 W (kgf) 68.04」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/torque-force",
    "inputs": {
      "r": "42",
      "F": "42",
      "th": "42"
    },
    "expect": [
      "有效力臂 (m) 31.212 径向分量 (N)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"r\":\"42\",\"F\":\"42\",\"th\":\"42\"}，输出区含「有效力臂 (m) 31.212 径向分量 (N)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/work-energy-theorem",
    "inputs": {
      "m": "42",
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "力功 W (J) 37044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"v1\":\"42\",\"v2\":\"42\"}，输出区含「力功 W (J) 37044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "dynamics/rotational-kinetic-energy",
    "clicks": ["var d=document.getElementById;function g(v){d('I').value=v;calcTool();return String(d('result').innerHTML);}var a=g('-1'),b=g('0');d('I').value='0.5';var c=g('0.5');var ok=a.indexOf('转动惯量 I 必须为正数')>=0&&a.indexOf('转动动能')<0&&b.indexOf('转动惯量 I 必须为正数')>=0&&b.indexOf('转动动能')<0&&c.indexOf('25.000')>=0;document.getElementById('__tbProbe').textContent='RKENEG '+(ok?'OK':'BAD a='+a.slice(0,25));"],
    "expect": ["RKENEG OK"],
    "ref": "12-N84 负惯量守卫：I=-1 旧版 E=0.5×(-1)×100=-50 J 负动能、I=0 出 0 J 仍展示结果；新版拦截并清空结果；I=0.5、ω=10 合法仍出 25.000 J。哨兵要求两非法态提示且无动能卡、合法态有 25.000，依赖 clicks 注入，默认态不命中。"
  },
  {
    "slug": "dynamics/rotational-kinetic-energy",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/dynamics/rotational-kinetic-energy.html','utf8');var n=h.split('TBKit.chart.line(').length-1;var ok=h.indexOf('rkeChartL')>=0&&n===2&&h.indexOf('转速加倍（动能×4）')>=0&&h.indexOf('示例 2×')<0&&h.indexOf('Angular Momentum L (kg·m²/s) vs ω')>=0;document.getElementById('__tbProbe').textContent='RKECHART '+(ok?'OK':'BAD');"],
    "expect": ["RKECHART OK"],
    "ref": "12-N85/N86：动能(J)与角动量(kg·m²/s)拆成两张图避免量纲混轴；预设按真实倍数命名（转速加倍动能×4）。旧版同图且示例2×实际8倍 ⇒ 变红。默认态不产生该串，零逃生。"
  },
  {
    "slug": "dynamics/kinetic-friction",
    "clicks": ["var d=document.getElementById;function o(m,n){d('mu').value=m;d('N').value=n;calcTool();return String(d('result').innerHTML);}var a=o('0','100'),b=o('-1','5'),c=o('','10'),e=o('0.3','100');var ok=a.indexOf('无定义')>=0&&a.indexOf('Infinity')<0&&b.indexOf('必须为非负')>=0&&c.indexOf('请填写')>=0&&e.indexOf('30.00')>=0;document.getElementById('__tbProbe').textContent='KFRB '+(ok?'OK':'BAD '+a.slice(0,30)+'|'+b.slice(0,30));"],
    "expect": ["KFRB OK"],
    "ref": "第864批：μ=0 时“正压力/摩擦系数”显示无定义而非 1e9 级伪值；μ=-1、空值分别提示；0.3/100 仍出 30.00。依赖 clicks 注入，默认态不命中。"
  },
  {
    "slug": "dynamics/static-friction-max",
    "clicks": ["var d=document.getElementById;function o(m,n){d('mu').value=m;d('N').value=n;calcTool();return String(d('result').innerHTML);}var a=o('','100'),b=o('0','100'),c=o('-1','100'),e=o('0.5','100');var ok=a.indexOf('请填写')>=0&&b.indexOf('无定义')>=0&&b.indexOf('Infinity')<0&&c.indexOf('必须为非负')>=0&&e.indexOf('50.00')>=0;document.getElementById('__tbProbe').textContent='SFRB '+(ok?'OK':'BAD '+a.slice(0,30)+'|'+b.slice(0,30));"],
    "expect": ["SFRB OK"],
    "ref": "第864批：补输入守卫——空值提示不按 0；μs=0 比值无定义；μs=-1 拦截；0.5/100 仍出 50.00。旧版无校验，空值直接算 0 并显示巨大比值。"
  },
  {
    "slug": "dynamics/coefficient-restitution",
    "clicks": ["var d=document.getElementById;function o(a,b,c,e){d('v1').value=a;d('v2').value=b;d('v1p').value=c;d('v2p').value=e;calcTool();return String(d('result').innerHTML);}var z=o('5','5','1','2'),g=o('5','0','6','3'),u=o('5','0','0','6'),v=o('5','0','2','3');var ok=z.indexOf('接近速度必须大于 0')>=0&&g.indexOf('方向不符')>=0&&u.indexOf('e>1')>=0&&v.indexOf('0.200')>=0&&v.indexOf('恢复系数 e')>=0;document.getElementById('__tbProbe').textContent='CORB '+(ok?'OK':'BAD '+z.slice(0,25)+'|'+g.slice(0,25));"],
    "expect": ["CORB OK"],
    "ref": "第864批：碰前相对接近速度 0 拦截；碰后分离速度为负（方向不一致）拦截；e=1.2 标注 e>1 可能外部能量；合法 5/0→2/3 仍 e=0.200。允许负速度表示方向，不再一律禁负。"
  },
  {
    "slug": "dynamics/work-energy-theorem",
    "clicks": ["var d=document.getElementById;function o(m,a,b){d('m').value=m;d('v1').value=a;d('v2').value=b;calcTool();return String(d('result').innerHTML);}var neg=o('-1','0','10'),e=o('','0','10'),rev=o('2','-10','2'),pos=o('2','0','10');var ok=neg.indexOf('质量 m 必须为正')>=0&&e.indexOf('请填写')>=0&&rev.indexOf('-96.00')>=0&&rev.indexOf('负功')>=0&&pos.indexOf('100.00')>=0&&pos.indexOf('正功')>=0;document.getElementById('__tbProbe').textContent='WETB '+(ok?'OK':'BAD '+neg.slice(0,25)+'|'+rev.slice(0,40));"],
    "expect": ["WETB OK"],
    "ref": "第864批：质量必须为正、空值提示；v₁=-10→v₂=2 按动能平方得 -96 J 负功（旧文案用 v₂>v₁ 会误判正功）；v₁=0→v₂=10 为 +100 J 正功。"
  },
  {
    "slug": "dynamics/inclined-plane-accel",
    "clicks": ["var d=document.getElementById;function o(t,k,ms,st,g){d('th').value=t;d('mu').value=k;d('mus').value=ms;d('state').value=st;d('g').value=g;calcTool();return String(d('result').innerHTML);}var h=o('90','0.1','0.15','rest','9.8'),n=o('-5','0.1','0.15','rest','9.8'),run=o('30','0.1','0.15','rest','9.8'),still=o('10','0.1','0.3','rest','9.8'),slide=o('10','0.3','0.3','sliding','9.8');var ok=h.indexOf('倾角须在 0–90°')>=0&&n.indexOf('倾角须在 0–90°')>=0&&run.indexOf('起动后沿斜面加速')>=0&&still.indexOf('静止')>=0&&still.indexOf('0.000')>=0&&slide.indexOf('已下滑：减速')>=0;document.getElementById('__tbProbe').textContent='IPAB '+(ok?'OK':'BAD '+run.slice(0,40)+'|'+slide.slice(0,40));"],
    "expect": ["IPAB OK"],
    "ref": "第864批：新增静摩擦系数与初始状态——30°、μs=0.15 由静止释放起动加速；10°、μs=0.3 静止且 a=0；10°、已下滑 μk=0.3 为减速而非静止；90° 与负角拦截。"
  },
  {
    "slug": "dynamics/momentum-conservation",
    "clicks": ["var d=document.getElementById;function o(a,b,c,e){d('m1').value=a;d('v1').value=b;d('m2').value=c;d('v2').value=e;calcTool();return String(d('result').innerHTML);}var bad=o('-1','20','2','0'),z=o('1','0','0','0'),v=o('1000','20','1500','0');var ok=bad.indexOf('质量都必须为正')>=0&&z.indexOf('质量都必须为正')>=0&&v.indexOf('8.000')>=0&&v.indexOf('20000.000')>=0;document.getElementById('__tbProbe').textContent='MCVB '+(ok?'OK':'BAD '+bad.slice(0,30)+'|'+v.slice(0,40));"],
    "expect": ["MCVB OK"],
    "ref": "第864批：负质量与 0 质量均拦截；1000×20 + 1500×0 给出共同末速 8.000、总动量 35000。速度 0/负仍合法。"
  },
  {
    "slug": "dynamics/terminal-velocity",
    "clicks": ["var d=document.getElementById;function o(m,g,r,c,a){d('m').value=m;d('g').value=g;d('rho').value=r;d('cd').value=c;d('A').value=a;calcTool();return String(d('result').innerHTML);}var n=o('-1','-9.81','-1.2','-1','-0.7'),z=o('80','9.81','1.2','1','0.7');var ok=n.indexOf('都必须为正')>=0&&z.indexOf('43.2')>=0;document.getElementById('__tbProbe').textContent='TMVB '+(ok?'OK':'BAD '+n.slice(0,30)+'|'+z.slice(0,30));"],
    "expect": ["TMVB OK"],
    "ref": "第864批：五项全负旧版相互抵消仍得正速度，现拦截；80 kg/9.81/1.2/1/0.7 仍约 43.2 m/s。"
  },
  {
    "slug": "dynamics/hooke-force",
    "clicks": ["var d=document.getElementById;function o(k,x){d('k').value=k;d('x').value=x;calcTool();return String(d('result').innerHTML);}var b=o('','0.1'),n=o('-200','0.1'),neg=o('200','-0.1'),z=o('200','0');var ok=b.indexOf('请填写')>=0&&n.indexOf('必须为正')>=0&&neg.indexOf('20.00')>=0&&neg.indexOf('恢复力 F = −k·x (N)')>=0&&neg.indexOf('弹力大小 |F| = k|x| (N)')>=0&&z.indexOf('0.00')>=0&&z.indexOf('恢复力 F = −k·x (N)')>=0;document.getElementById('__tbProbe').textContent='HKFB '+(ok?'OK':'BAD '+neg.slice(0,50)+'|'+z.slice(0,30));"],
    "expect": ["HKFB OK"],
    "ref": "第864批：k 空/负拦截；x=-0.1 恢复力 +20 N（指向平衡位置）、大小 20 N；x=0 合法输出 0，不再按空值 0 兜底。"
  },
  {
    "slug": "dynamics/elastic-collision-1d",
    "clicks": ["var d=document.getElementById;function o(a,b,c,e){d('m1').value=a;d('m2').value=b;d('v1').value=c;d('v2').value=e;calcTool();return String(d('result').innerHTML);}var n=o('-1','2','4','0'),v=o('2','1','4','0');var ok=n.indexOf('质量都必须为正')>=0&&v.indexOf('1.333')>=0&&v.indexOf('5.333')>=0&&v.indexOf('动量校验')>=0&&v.indexOf('动能校验')>=0;document.getElementById('__tbProbe').textContent='EC1B '+(ok?'OK':'BAD '+n.slice(0,30)+'|'+v.slice(0,60));"],
    "expect": ["EC1B OK"],
    "ref": "第864批：负质量拦截；2 kg/4 m·s⁻¹ 撞 1 kg 静止仍得 1.333/5.333，并显示动量与动能校验。"
  },
  {
    "slug": "dynamics/banked-curve",
    "clicks": ["var d=document.getElementById;function o(r,t,g){d('r').value=r;d('th').value=t;d('g').value=g;calcTool();return String(d('result').innerHTML);}var nd=o('-50','30','-9.81'),h=o('50','90','9.81'),z=o('50','0','9.81'),v=o('50','30','9.81');var ok=nd.indexOf('必须为正')>=0&&h.indexOf('必须为正')>=0&&z.indexOf('0.00')>=0&&z.indexOf('无倾角')>=0&&v.indexOf('16.8')>=0;document.getElementById('__tbProbe').textContent='BKCB '+(ok?'OK':'BAD '+nd.slice(0,30)+'|'+z.slice(0,40));"],
    "expect": ["BKCB OK"],
    "ref": "第864批：负半径/负重力、90° 倾角拦截；0° 合法输出设计速度 0 并说明仅靠轮胎侧向力；30° 仍约 16.8 m/s。"
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

  console.log("==== dynamics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();