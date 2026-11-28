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
  "slug": "telecom/ap-coverage",
  "inputs": { "ptx": "20", "gt": "3", "freq": "5200", "prmin": "-82", "gr": "2", "extraLoss": "10", "fadeMargin": "8", "env": "2" },
  "expect": [ "室内密集(隔墙多) / 5GHz 及以上", "保守布点半径" ],
  "ref": "5GHz+室内密集：良好阈值 12×0.6=7.2m、一般 5×0.6=3m；结果必须显示环境/频段分档与 70% 保守半径，旧版固定 50/15/3m 且无频段折算。"
},
{
  "slug": "telecom/bandwidth-calculator",
  "inputs": {
    "bandwidth": "100",
    "fileSize": "7.7",
    "efficiency": "85"
  },
  "expect": [ "7884.8 文件大小" ],
  "ref": "auto-restore（7.7 GiB = 7884.8 MiB；输出卡标签改为 MiB）"
},
{
  "slug": "telecom/bandwidth-calculator",
  "clicks": [
    "document.getElementById('sizeUnit').value='1024'; document.getElementById('fileSize').value='2048'; document.getElementById('bandwidth').value='4'; document.getElementById('efficiency').value='100'; calc();"
  ],
  "expect": [
    "2048 KiB = 2097152 B = 2.10 MB（十进制 10⁶） = 2.00 MiB（二进制 2²⁰）"
  ],
  "ref": "单位双口径：sizeUnit 的 value 统一为每单位字节数（KiB=1024），2048 KiB=2,097,152 B=2.10 MB=2.00 MiB；同时校验十进制与二进制两条换算，旧实现把 KiB 当 MB、把 MB/GB 当 1024 倍。"
},
{
  "slug": "telecom/bandwidth-calculator",
  "clicks": [
    "document.getElementById('result').textContent='T '+fmtTime(119.6);"
  ],
  "expect": [ "T 2 分 0 秒" ],
  "ref": "时间进位回归：119.6 秒旧实现 Math.floor(119.6/60)=1 + Math.round(59.6)=60 ⇒「1 分 60 秒」；新实现先四舍五入总秒再拆分 ⇒ 120 秒=2 分 0 秒。与默认 4.7 GiB/100Mbps 大耗时零交集。"
},
{
  "slug": "telecom/bandwidth-calculator",
  "clicks": [
    "document.getElementById('sizeUnit').value='1000000000'; document.getElementById('fileSize').value='1'; document.getElementById('bandwidth').value='100'; document.getElementById('efficiency').value='100'; calc();"
  ],
  "expect": [ "1 GB = 1000000000 B = 1000.00 MB（十进制 10⁶） = 953.67 MiB（二进制 2²⁰）" ],
  "ref": "十进制 GB 与二进制 GiB 区分：1 GB=10⁹ B=1000 MB=953.67 MiB，旧实现 sizeUnit=1024 把 GB 当 1024 MB。"
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
  "slug": "telecom/ber-snr",
  "inputs": { "ber": "1e-5", "mod": "qam64" },
  "expect": [ "高 SNR 近似式", "Gray 映射" ],
  "ref": "QAM 页面必须标注高 SNR 近似、Gray 映射与矩形星座假设；默认 qam64 BER=1e-5 反解 17.79 dB 同时带口径说明。"
},
{
  clicks: ["calc()"],
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
  clicks: ["calc()"],
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
  clicks: ["calc()"],
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
  "inputs": { "ber": "1e-5abc", "mod": "qam64" },
  "expect": [ "BER 格式无效" ],
  "ref": "严格解析回归：parseFloat('1e-5abc') 旧实现静默取 1e-5 并算出 17.79 dB；新实现用完整数字/科学计数正则拒绝尾随字符。合法 1e-5 不出现提示。"
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
  clicks: ["calc()"],
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
  "slug": "telecom/ap-coverage",
  "inputs": { "ptx": "20", "gt": "3", "freq": "2412", "prmin": "-82", "gr": "2", "extraLoss": "-10", "fadeMargin": "8" },
  "expect": [ "环境附加损耗与衰落余量必须 ≥ 0 dB" ],
  "ref": "负损耗回归：旧实现直接把 -10 dB 计入 totalLoss，MAPL 被抬高、覆盖半径虚高；新实现拒绝负附加损耗与负衰落余量。默认 10/8 不出现该提示。"
},
{
  "slug": "telecom/bandwidth-calculator",
  "inputs": { "bandwidth": "100", "fileSize": "4.7", "efficiency": "120" },
  "expect": [ "传输效率需在 1–100% 之间" ],
  "ref": "传输效率 >100% 物理上不存在，旧实现按 120% 照算（高估下载速度）；新实现拒绝。默认 85% 不出现该提示。"
}
,
{
  "slug": "telecom/webrtc-leak-test",
  "clicks": ["(function(){var F=globalThis.__ntAnalyze;function cls(t,e){var h=F('x',t,e);if(h.indexOf('>不一致<')>=0||h.indexOf('>Mismatch<')>=0)return 'NEG';if(h.indexOf('>一致<')>=0||h.indexOf('>Match<')>=0)return 'POS';if(h.indexOf('>无法判断<')>=0||h.indexOf('>Unknown<')>=0)return 'UNK';return '?';}var N=String.fromCharCode(10);var r1=cls('一致性: 不一致'+N+'内网地址: —',false);var r2=cls('Consistency: Mismatch'+N+'Private addresses: —',true);var r3=cls('一致性: 一致'+N+'内网地址: —',false);var r4=cls('Consistency: Match'+N+'Private addresses: —',true);var ok=(r1==='NEG'&&r2==='NEG'&&r3==='POS'&&r4==='POS');document.getElementById('__tbProbe').textContent='WEBRTC '+(ok?'OK':'BAD '+[r1,r2,r3,r4].join(','));})()"],
  "expect": ["WEBRTC OK"],
  "ref": "第288批：__ntAnalyze 一致性须按完整状态精确判断。中文「不一致」含「一致」、英文「Mismatch」含 match，旧版 /一致|Match/ 会把不一致误判为一致（或落到 Check）。用真实结果格式「一致性: 不一致 / Consistency: Mismatch」反例，四态须 NEG/NEG/POS/POS；修复前 r1=POS、r2=? ⇒ BAD。"
},
{
  "slug": "telecom/public-ip-lookup",
  "clicks": ["(function(){var F=globalThis.__ntAnalyze;function cls(ip){var N=String.fromCharCode(10);var h=F('x','IP: '+ip+N+'来源: test'+N+'时区: —',false);if(h.indexOf('>私有/保留地址<')>=0)return 'RES';if(h.indexOf('>公网地址<')>=0)return 'PUB';if(h.indexOf('>地址性质待确认<')>=0)return 'UNK';return '?';}var ips=['100.64.0.1','fc00::1','8.8.8.8','2001:4860:4860::8888','192.168.1.1'];var want=['RES','RES','PUB','PUB','RES'];var got=ips.map(cls);var ok=(got.join(',')===want.join(','));document.getElementById('__tbProbe').textContent='IPCLS '+(ok?'OK':'BAD '+got.join(','));})()"],
  "expect": ["IPCLS OK"],
  "ref": "第288批：T1 地址分类旧版只排除少量 IPv4 私网段，100.64.0.1（100.64.0.0/10 CGNAT 共享地址）与 IPv6 fc00::1（fc00::/7 ULA）被误判为「全球可路由地址」。修复后按完整保留段判定、对无法确认的地址不断言公网；注入 5 地址须 RES/RES/PUB/PUB/RES，修复前为 PUB/PUB/PUB/PUB/RES ⇒ 强判别。"
},
{
  clicks: ["calc()"],
  "slug": "telecom/distance-power-frequency",
  "inputs": {"v0":"20","v1":"5800","v2":"3","v3":"3","v4":"-90"},
  "expect": ["最大距离处接收功率（=灵敏度，dBm）", "-90.0"],
  "ref": "最大距离处 Pr=Pt+Gt+Gr−FSPL，且 FSPL 由 Pr=灵敏度 反解，故应显示 −90.0 而不是 Pt+Gt+Gr=−67.0。"
},
{
  "slug": "telecom/distance-power-frequency",
  "inputs": {"v0":"abc","v1":"5800","v2":"3","v3":"3","v4":"-90"},
  "expect": ["输入含非数字值"],
  "ref": "非数字输入不得被 getV 的 isNaN→0 吞掉；0 dBm/0 dBi 仍是合法值，空值另提示。"
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {"baseIp":"0.0.0.0","oldMask":"0","divideMode":"count","subCount":"1"},
  "expect": ["1 个子网（/0）", "0.0.0.0"],
  "ref": "数量=1 时新前缀仍为 /0，掩码必须是 0.0.0.0；旧实现 0xFFFFFFFF<<32 变成 <<0 得 255.255.255.255。"
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {"baseIp":"10.0.0.0","oldMask":"30","divideMode":"prefix","newMask":"31"},
  "expect": ["10.0.0.1", "—（/31 点对点无广播）"],
  "ref": "/31 的两个地址都是主机，不能把第二个标成广播；旧实现首可用=10.0.0.0、广播=10.0.0.1。"
},
{
  "slug": "telecom/subnet-planner",
  "inputs": {"baseIp":"10.0.0.0","oldMask":"30","divideMode":"prefix","newMask":"32"},
  "expect": ["—（/32 单主机无广播）", "10.0.0.0（单主机）"],
  "ref": "/32 只有一个地址，不能显示广播；首末可用均应为该地址。"
},
{
  clicks: ["calc()"],
  "slug": "telecom/convert-24",
  "inputs": {"mode":"ebn0","snr":"10"},
  "expect": ["归一化信道容量：不可用"],
  "ref": "Eb/N0 口径缺少 R/B，不能把 Eb/N0 直接代入 log2(1+x) 当带宽内 SNR 容量。"
},
{
  clicks: ["calc()"],
  "slug": "telecom/convert-24",
  "inputs": {"mode":"snr","snr":"10","bitrate":"2","bandwidth":"1"},
  "expect": ["Eb/N0 = SNR − 10log10(R/B) = 6.99 dB", "归一化信道容量 = log2(1 + SNR线性) = 3.4594"],
  "ref": "SNR=10、R/B=2 ⇒ Eb/N0=10−3.0103=6.99 dB；容量用 SNR 线性 10 ⇒ log2(11)=3.4594，不得用 Eb/N0。"
},
{
  "slug": "telecom/ber-snr",
  "inputs": {"ber":"1e-320","mod":"bpsk"},
  "expect": ["低于本工具在 28 dB 处可分辨的下限"],
  "ref": "1e-320 低于 BPSK 在 28 dB 附近可表示的下限，旧二分 hi=60 返回 60 dB 假答案；应明确拒绝。"
},
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
