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
  "expect": [ "11.1 pW" ],
  "ref": "接收功率按自动单位显示：Pr=20+2+2−(20log10 3600+32.44)=−79.57 dBm ⇒ 1.10e−11 W = 11.1 pW（旧实现 mW 定点 4 位只剩 0.0000）。默认态（2400 MHz）为 24.9 pW，不命中。"
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
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {
    "baseIp": "0.0.0.0",
    "oldMask": "0",
    "newMask": "1"
  },
  "expect": [ "0.0.0.0/1" ],
  "ref": "0.0.0.0 是合法地址且掩码 0 必然产生 baseInt=0：旧实现 `if(!baseInt)` 误判为非法直接报错；改为 `baseInt===null` 后 /0→/1 正常输出首子网 0.0.0.0/1。默认 192.168.1.0/24 不出现该串。"
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {
    "baseIp": "1.2.3.4.5",
    "oldMask": "24",
    "newMask": "27"
  },
  "expect": [ "请输入有效的网络地址" ],
  "ref": "旧实现 ip.split('.').map(Number) 对 `1.2.3.4.5`（5 段）与 `1..2.3`（空段 Number('')=0）都误判合法；新实现用 ^(\\d{1,3}\\.){3}\\d{1,3}$ 严格匹配。默认态不出现该提示。"
},
{
  "slug": "telecom/ber-snr",
  "inputs": {
    "ber": "0.1",
    "mod": "bpsk"
  },
  "expect": [ "-0.86" ],
  "ref": "BPSK/QPSK：0.5·erfc(√γb)=0.1 ⇒ √γb=0.9063 ⇒ γb=0.8214 ⇒ 10log10 = −0.86 dB（旧实现 lo=0 只能解出 0 dB 以上的 BER，低信噪比无解）。默认态 BER=1e-5 ⇒ 9.6 dB，不命中。"
},
{
  "slug": "telecom/ber-snr",
  "inputs": {
    "ber": "0.45",
    "mod": "bpsk"
  },
  "expect": [ "超出本工具可解范围" ],
  "ref": "BPSK 在 −20 dB 时 BER=0.5·erfc(0.1)=0.4438 已是可达上限，目标 0.45 无解；旧实现会静默返回 0 dB 假答案。默认态不出现该提示。"
},
{
  "slug": "telecom/convert-24",
  "inputs": {
    "snr": "30"
  },
  "expect": [ "低于双精度下限" ],
  "ref": "Eb/N0=1000 ⇒ 0.5·erfc(√1000) 双精度下溢为 0，旧实现输出「1e-Infinity」；新实现显式提示。默认 snr=10 不出现该串。"
},
{
  "slug": "telecom/estimate-9",
  "inputs": { "freq": "3600", "dist": "1", "ptx": "20", "gt": "2", "gr": "2" },
  "expect": [ "11.051 pW" ],
  "ref": "Pr=20+2+2−(20log10 3600+32.44)=−79.57 dBm ⇒ 1.105e−8 mW=11.051 pW（旧实现只降到 µW，显示 0.000 µW）。默认 2400 MHz 得 24.900 pW，不命中。"
},
{
  "slug": "telecom/estimate-9",
  "inputs": { "freq": "2400", "dist": "1", "ptx": "" },
  "expect": [ "未填写发射功率" ],
  "ref": "页面文案声明 Pt/Gt/Gr 可空，但旧守卫把 ptx 列入必填清单、空值直接拦截，与「跳过链路预算」分支矛盾；改为只强制 freq/dist 后空 Pt 走该提示。默认 Pt=20 不出现。"
},
{
  "slug": "telecom/bandwidth-calculator",
  "inputs": { "bandwidth": "100", "fileSize": "4.7", "efficiency": "120" },
  "expect": [ "传输效率需在 1–100% 之间" ],
  "ref": "传输效率 >100% 物理上不存在，旧实现按 120% 照算（高估下载速度）；新实现拒绝。默认 85% 不出现该提示。"
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
