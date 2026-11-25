#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "shipping/calc-76",
  "inputs": {
    "v0": "270",
    "v1": "28",
    "v2": "9.5",
    "v3": "9.7",
    "v4": "9.9",
    "v5": "0.72",
    "v6": "1.025",
    "v7": "",
    "v8": "12000"
  },
  "expect": [
    "153.36"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": {
    "val": "1",
    "from": "0.539956803456",
    "to": "1"
  },
  "expect": [ "= 0.539956803456 节 (kn)" ],
  "ref": "2026-11-04 换算系数修正（1 km/h = 0.5399568 kn）：1 千米/时 → 0.539956803456 节。默认 1 节 → 1.852 km/h，不含该串。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "v": "15",
    "t": "8"
  },
  "expect": [
    "航程 = 120.00 海里 (≈ 222.24 km)"
  ],
  "ref": "去默认化：航程 = v×t = 15×8 = 120.00 海里，km = 120×1.852 = 222.24。默认态 v=10/t=5 ⇒ 50.00 海里/92.60 km 不命中。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "v": "20",
    "t": "3"
  },
  "expect": [
    "航程 = 60.00 海里 (≈ 111.12 km)"
  ],
  "ref": "去默认化：航程 = 20×3 = 60.00 海里，km = 60×1.852 = 111.12。默认态不命中。"
},
{
  "slug": "shipping/estimate-length",
  "inputs": {
    "v0": "23",
    "v1": "18",
    "v2": "1.5",
    "v3": "5000",
    "v5": "4"
  },
  "expect": [
    "121.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "shipping/tide",
  "clicks": ["for(var i=0;i<4;i++){var d=[['03:20','1.2','high'],['09:40','0.4','low'],['15:50','1.5','high'],['22:10','0.3','low']][i];document.getElementById('rt'+i).value=d[0];document.getElementById('rh'+i).value=d[1];document.getElementById('rtype'+i).value=d[2];}document.getElementById('hTimeOff').value='45';document.getElementById('lTimeOff').value='20';document.getElementById('hRatio').value='1.1';document.getElementById('lRatio').value='0.9';calc();"],
  "expect": ["1.38"],
  "ref": "默认参考站 4 次潮汐：高潮 1.2/1.5 倍 1.1 → 1.32/1.65，低潮 0.4/0.3 倍 0.9 → 0.36/0.27，潮差 1.65−0.27=1.38；旧用例用未存在的 rt0 等 id 只回显 45。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": {
    "v": "",
    "t": ""
  },
  "expect": [
    "请填写所选模式需要的两项数据后再计算"
  ],
  "ref": "空态守卫：航速与时间留空 ⇒ 提示，不再按 0 兜底输出航程 0.00 海里。默认态 v=10/t=5 输出 50.00 海里，不含该提示 ⇒ 可判别。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": { "mode": "time", "d": "120", "v": "15" },
  "expect": ["航行时间 = 8.00 小时"],
  "ref": "已知航程 120 海里、航速 15 节 → 8.00 h；旧实现只能求航程。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": { "mode": "speed", "d": "120", "t": "8" },
  "expect": ["平均航速 = 15.00 节"],
  "ref": "已知航程 120 海里、时间 8 h → 15.00 节；覆盖第三种求解模式。"
},
{
  "slug": "shipping/convert-time-speed",
  "inputs": { "v": "-2", "t": "5" },
  "expect": ["航速须大于 0"],
  "ref": "负航速应拒绝；旧实现 10 节/负 2 小时会显示负航程。"
},
{
  "slug": "shipping/calc-76",
  "inputs": { "v5": "1.2" },
  "expect": ["方形系数 Cb 必须在 0（不含）到 1（含）之间"],
  "ref": "Cb=1.2 越界不得静默截成 1；旧实现 Math.min 后继续算。"
},
{
  "slug": "shipping/calc-76",
  "inputs": { "v7": "1.3" },
  "expect": ["水线面系数 Cw 必须在 0（不含）到 1（含）之间"],
  "ref": "Cw=1.3 越界不得原样参与排水量/TPC 计算。"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": { "stw": "12", "cur": "3", "curDir": "0" },
  "expect": ["15.00", "对地航速 SOG"],
  "ref": "顺流：12+3=15.00 节，偏移角 0°；旧页面没有流速矢量输入。"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": { "stw": "10", "cur": "2", "curDir": "180" },
  "expect": ["8.00", "对地航速 SOG"],
  "ref": "顶流：10−2=8.00 节。"
},
{
  "slug": "shipping/convert-speed-1",
  "inputs": { "stw": "10", "cur": "2", "curDir": "90" },
  "expect": ["10.20", "11.3"],
  "ref": "横流：SOG=√(10²+2²)=10.198→10.20，偏移角 atan(2/10)=11.3°。"
},
{
  "slug": "shipping/tide",
  "clicks": ["for(var i=0;i<4;i++){var d=[['03:20','1.2','high'],['09:40','0.4','low'],['15:50','1.5','high'],['22:10','0.3','low']][i];document.getElementById('rt'+i).value=d[0];document.getElementById('rh'+i).value=d[1];document.getElementById('rtype'+i).value=d[2];}document.getElementById('hRatio').value='';calc();"],
  "expect": ["高潮/低潮潮高比必须填写大于 0"],
  "ref": "潮高比留空应停止输出；旧实现空值按 0 继续，潮差无效。"
},
{
  "slug": "shipping/tide",
  "clicks": ["for(var i=0;i<4;i++){var d=[['03:20','1.2','high'],['09:40','0.4','low'],['15:50','1.5','high'],['22:10','0.3','low']][i];document.getElementById('rt'+i).value=d[0];document.getElementById('rh'+i).value=d[1];document.getElementById('rtype'+i).value=d[2];}for(var i=0;i<4;i++){document.getElementById('rtype'+i).value='high';}calc();"],
  "expect": ["必须同时包含高潮与低潮"],
  "ref": "四次事件全为高潮时缺低潮组，旧实现潮差出现无穷值。"
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

  console.log("==== shipping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
