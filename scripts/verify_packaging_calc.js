#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "packaging/calc-66",
  "inputs": {
    "v0": "600",
    "v1": "300",
    "v2": "250",
    "v4": "2.5",
    "v5": "3",
    "v6": "12"
  },
  "expect": [
    "1.800"
  ],
  "ref": "auto-restore"
},
{
  "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
  "inputs": {
    "v0": "400",
    "v1": "240"
  },
  "expect": [
    "40.00%",
    "60.00%",
    "424.00"
  ],
  "ref": "v0=400,v1=240 → 热收缩率=(400-240)/400×100=40.00%、收缩后占比 240/400=60.00%、建议下料膜宽 400×1.06=424.00 mm（默认 300/150 → 50.00%/50.00%/318.00；swap -100.00%/200.00%/159.00，均不重合；收缩量为可正负差值，不作 expect）"
},
{
  "slug": "packaging/strength-11",
  "inputs": {
    "v0": "7",
    "v1": "3"
  },
  "expect": [
    "2251",
    "2.251",
    "321.5"
  ],
  "ref": "v0=7,v1=3 → BCT=5.87×7×√(3×1000)=2251 N（McKee 近似，箱周长 1000 mm）、2.251 kN、系数 5.87×√3000=321.5（默认 6/2.5 → 1761/1.761/293.5；swap 1137/1.137/454.7，均不重合）"
},
{
  "slug": "packaging/strength-12",
  "inputs": {
    "v0": "30",
    "v1": "48",
    "v2": "10",
    "v3": "180",
    "v4": "300",
    "v5": "GB/T 2792",
    "v6": "BOPP/瓦楞纸板"
  },
  "expect": [
    "15.625",
    "625.0",
    "56.25%"
  ],
  "ref": "v0=30,v1=48 → 剥离强度=30×25/48=15.625 N/25mm、30×1000/48=625.0 N/m、相对 10 N/25mm 基准 (15.625-10)/10×100=56.25%（默认 24/45 → 13.333/533.3/33.33%；swap 46.875/1875.0/368.75%，均不重合）"
},
  {
    "slug": "packaging/calc-66",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='0';calc();document.getElementById('__tbProbe').textContent='C66L0 '+((document.getElementById('res').innerHTML.indexOf('「纸箱长 L（mm）」必须大于 0')>=0&&document.getElementById('res').innerHTML.indexOf('方案可行')<0)?'OK':'BAD');"],
    "expect": ["C66L0 OK"],
    "ref": "纸箱长为 0 必须停止计算并点名长度字段，不能输出方案可行。"
  },
  {
    "slug": "packaging/calc-66",
    "inputs": {},
    "clicks": ["document.getElementById('v5').value='0';calc();document.getElementById('__tbProbe').textContent='C66K0 '+((document.getElementById('res').innerHTML.indexOf('「安全系数 K」必须大于 0')>=0)?'OK':'BAD');"],
    "expect": ["C66K0 OK"],
    "ref": "安全系数 K=0 会使最大层数除以零，必须点名 K 并停止。"
  },
  {
    "slug": "packaging/calc-66",
    "inputs": {},
    "clicks": ["document.getElementById('v6').value='0';calc();document.getElementById('__tbProbe').textContent='C66W0 '+((document.getElementById('res').innerHTML.indexOf('「单箱毛重（kg）」必须大于 0')>=0)?'OK':'BAD');"],
    "expect": ["C66W0 OK"],
    "ref": "单箱毛重 0 会使最大堆码层数除以零，必须点名毛重并停止。"
  },
  {
    "slug": "packaging/calc-66",
    "inputs": {},
    "clicks": ["document.getElementById('v4').value='0.1';calc();document.getElementById('__tbProbe').textContent='C66SHORT '+((document.getElementById('res').innerHTML.indexOf('目标高度无法容纳一层')>=0&&document.getElementById('res').innerHTML.indexOf('不能视为目标堆码方案可行')>=0&&document.getElementById('res').innerHTML.indexOf('期望堆码层数')>=0)?'OK':'BAD');"],
    "expect": ["C66SHORT OK"],
    "ref": "期望高度 0.1 m < 单箱高 0.25 m：强制按 1 层并明确目标高度不足，不能显示方案可行。"
  },
  {
    "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='0';calc();document.getElementById('__tbProbe').textContent='SHR0 '+((document.getElementById('res').innerHTML.indexOf('「产品原始尺寸」必须大于 0')>=0)?'OK':'BAD');"],
    "expect": ["SHR0 OK"],
    "ref": "原始尺寸=0 时收缩率除零，必须拒绝并说明原因。"
  },
  {
    "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='400';document.getElementById('v1').value='440';calc();document.getElementById('__tbProbe').textContent='SHREXP '+((document.getElementById('res').innerHTML.indexOf('膨胀率')>=0&&document.getElementById('res').innerHTML.indexOf('-10.00%')>=0&&document.getElementById('res').innerHTML.indexOf('尺寸增大（膨胀）')>=0)?'OK':'BAD');"],
    "expect": ["SHREXP OK"],
    "ref": "400→440 尺寸增大：收缩率 -10.00%，同时给出膨胀率 10.00%，明确按膨胀理解。"
  },
  {
    "slug": "packaging/shousuomo-shousuolv-refeng-canshu",
    "inputs": { "v0": "400", "v1": "240", "v3": "10", "v4": "20", "v5": "150", "v6": "1" },
    "clicks": ["calc();document.getElementById('__tbProbe').textContent='SHRW '+document.getElementById('res').innerHTML;"],
    "expect": ["460.00", "284.00", "温度 150 °C", "时间 1 s"],
    "ref": "可调余量 10%、封口搭接 20：下料=400×1.1+20=460.00；包覆=240×1.1+20=284.00；热封 150°C/1s 仅记录。"
  },
  {
    "slug": "packaging/strength-12",
    "inputs": {},
    "clicks": ["document.getElementById('v1').value='0';calc();document.getElementById('__tbProbe').textContent='STW0 '+((document.getElementById('res').innerHTML.indexOf('「胶带宽度」必须大于 0')>=0)?'OK':'BAD');"],
    "expect": ["STW0 OK"],
    "ref": "胶带宽度=0 会除零，必须拒绝并点名宽度。"
  },
  {
    "slug": "packaging/strength-12",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='-1';calc();document.getElementById('__tbProbe').textContent='STFN '+((document.getElementById('res').innerHTML.indexOf('「实测剥离力」必须为非负数')>=0)?'OK':'BAD');"],
    "expect": ["STFN OK"],
    "ref": "剥离力 -1 必须拒绝；0 是合法值不应被当未填。"
  },
  {
    "slug": "packaging/strength-12",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='24';document.getElementById('v1').value='25';calc();document.getElementById('__tbProbe').textContent='ST25 '+((document.getElementById('res').innerHTML.indexOf('24.000')>=0&&document.getElementById('res').innerHTML.indexOf('960.0')>=0&&document.getElementById('res').innerHTML.indexOf('9.60')>=0)?'OK':'BAD');"],
    "expect": ["ST25 OK"],
    "ref": "24 N / 25 mm：N/25mm=24.000、N/m=960.0、N/cm=9.60。"
  },
  {
    "slug": "packaging/strength-12",
    "inputs": {},
    "clicks": ["document.getElementById('v0').value='30';document.getElementById('v1').value='48';document.getElementById('v2').value='10';document.getElementById('v5').value='GB/T 2792';document.getElementById('v6').value='BOPP/瓦楞纸板';calc();document.getElementById('__tbProbe').textContent='STB '+((document.getElementById('res').innerHTML.indexOf('56.25%')>=0&&document.getElementById('res').innerHTML.indexOf('GB/T 2792')>=0&&document.getElementById('res').innerHTML.indexOf('仅记录')<0&&document.getElementById('res').innerHTML.indexOf('不判定合格与否')>=0)?'OK':'BAD');"],
    "expect": ["STB OK"],
    "ref": "用户基准 10、同条件记录：15.625 相对基准偏差 56.25%，显示标准/基材，不判合格。"
  },
  {
    "slug": "packaging/calc-1",
    "inputs": {
      "inL": "42",
      "inW": "42",
      "inH": "42",
      "pad": "42",
      "board": "42"
    },
    "expect": [
      "（长×宽×高）： 210 × 210 × 21"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inL\":\"42\",\"inW\":\"42\",\"inH\":\"42\",\"pad\":\"42\",\"board\":\"42\"}，输出区含「（长×宽×高）： 210 × 210 × 21」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "packaging/calc-2",
    "inputs": {
      "dropH": "42",
      "gValue": "42",
      "cValue": "42",
      "weight": "42",
      "area": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n建议缓冲厚度： 420.0 mm（ 42.00 cm） 缓冲面动应力： 4,118.79 kPa"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dropH\":\"42\",\"gValue\":\"42\",\"cValue\":\"42\",\"weight\":\"42\",\"area\":\"42\"}，输出区含「42\n42\n42\n42\n42\n建议缓冲厚度： 420.0 mm（ 42.00 c…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "packaging/calc-1",
    "inputs": { "inL": "", "inW": "200", "inH": "150", "pad": "10", "board": "5" },
    "clicks": ["document.getElementById('inL').value='310';"],
    "expect": ["340 × 230 × 180"],
    "ref": "空尺寸拦截状态链（2026-11-16）：空内长先拒绝（旧实现 parseFloat('')||0 回退 0 得 30mm 并写 localStorage），再注入 310 ⇒ 外箱 310+2×(10+5)=340、230、180 mm。原拒绝提示在纯默认快照也出现（逃生），改为锁恢复后的实算尺寸。"
  },
  {
    "slug": "packaging/calc-1",
    "inputs": { "inL": "310", "inW": "210", "inH": "160", "pad": "12", "board": "6" },
    "expect": ["346 × 246 × 196", "0.0167"],
    "ref": "外箱尺寸复算去默认化：注入 310/210/160、pad=12、board=6（页面默认 300/200/150/10/5）⇒ add=2×(12+6)=36 ⇒ 346×246×196 mm；外体积 /1e9 = 0.01668 ⇒ 0.0167。默认态 330×230×180/0.0137 不含本串。"
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

  console.log("==== packaging calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
