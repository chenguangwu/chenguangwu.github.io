#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "telecom/ap-coverage",
  "inputs": {
    "ptx": "30",
    "gt": "3",
    "freq": "2412",
    "prmin": "-82",
    "gr": "2",
    "extraLoss": "10",
    "fadeMargin": "8"
  },
  "expect": [
    "0.88231"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/bandwidth-calculator",
  "inputs": {
    "bandwidth": "100",
    "fileSize": "7.7",
    "efficiency": "85"
  },
  "expect": [ "7884.8 文件大小" ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/bandwidth-calculator",
  "clicks": [
    "document.getElementById('sizeUnit').value='0.0009765625'; document.getElementById('fileSize').value='2048'; document.getElementById('bandwidth').value='4'; document.getElementById('efficiency').value='100'; calc();"
  ],
  "expect": [
    "2048 KB = 2.00 MB"
  ],
  "ref": "E2 口径统一（byte 系 1024）：KB 选项 value=1/1024，2048 KB = 2048×0.0009765625 = 2.00 MB（step3 回显含 sizeLabel）。判别态 clicks 清空回默认 GB/4.7 → 「4.7 GB = 4812.80 MB」零交集。"
},
{
  "slug": "telecom/ber-snr",
  "inputs": {
    "ber": "1e-5",
    "mod": "qam64"
  },
  "expect": [
    "17.79"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/convert-24",
  "inputs": {
    "snr": "5"
  },
  "expect": [
    "误码率 BER ≈ 5.954e-3"
  ],
  "ref": "去默认化：SNR=5dB ⇒ Eb/N0=10^0.5=3.162，BER=0.5·erfc(√3.162)=5.954e-3。默认态 snr=10 ⇒ 3.876e-6，不命中。"
},
{
  "slug": "telecom/convert-24",
  "inputs": {
    "snr": "15"
  },
  "expect": [
    "误码率 BER ≈ 9.216e-16"
  ],
  "ref": "去默认化：SNR=15dB ⇒ Eb/N0=10^1.5=31.62，BER=0.5·erfc(√31.62)=9.216e-16。默认态不命中。"
},
{
  "slug": "telecom/convert-24",
  "inputs": {
    "snr": "20"
  },
  "expect": [
    "误码率 BER ≈ 1.090e-45"
  ],
  "ref": "去默认化：SNR=20dB ⇒ Eb/N0=100，BER=0.5·erfc(10)=1.090e-45。默认态不命中。"
},
{
  "slug": "telecom/estimate-9",
  "inputs": {
    "freq": "3600",
    "dist": "1",
    "ptx": "20",
    "gt": "2",
    "gr": "2"
  },
  "expect": [ "103.57 路径损耗" ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/path-loss",
  "inputs": {
    "freq": "3600",
    "dist": "1",
    "ptx": "20",
    "gt": "2",
    "gr": "2"
  },
  "expect": [
    "(3600.00)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "telecom/quick-calc-time-bandwidth",
  "inputs": {
    "kw": "zzzz"
  },
  "clicks": ["search()"],
  "expect": [
    "未找到匹配项"
  ],
  "ref": "与 quality/table-sampling 同模板：kw 为空时输出 DATA 全量，具体编号在默认态必命中 ⇒ 反向锚"
     + "「未找到匹配项」。原 expect「A01」是默认全量表首行编号，零判别力。",
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {
    "baseIp": "172.16.5.0",
    "oldMask": "22",
    "newMask": "27"
  },
  "expect": [
    "172.16.4.31",
    "255.255.255.224"
  ],
  "ref": "去默认化（原注入值恰为页面默认 192.168.1.0/24/26）：注入 172.16.5.0、原前缀 22、新前缀 27。独立复算：network=172.16.5.0 & /22 = 172.16.4.0；subnetSize=2^5=32；subCount=2^(27-22)=32；hostsPerSubnet=30；新掩码=255.255.255.224；首子网 172.16.4.0/27（可用 172.16.4.1–30，广播 172.16.4.31）。默认态输出 192.168.1.0/26，两条均不命中。"
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

  console.log("==== telecom calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
