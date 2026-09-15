#!/usr/bin/env node
/**
 * 第 42 道门禁：encode 分类计算正确性验证（26 个确定性数值估算工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（非数值估算，stub 无验证意义）：
 *   - binary-to-ascii：文本进制解码（走 calcTool/dataGrid 渲染，输出为非固定数值）
 *   - calc-1 / calc-2：Base64 / URL 文本编解码（字符串变换，非数值）
 *   - image-to-base64：文件读取与本地转换（依赖 FileReader）
 * 用法: node scripts/verify_encode_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "encode/ascii-readability",
    inputs: { total: "200", nonAscii: "50", control: "10" },
    expect: ["75.0", "70.0"],
    ref: "ASCII 占比=(200−50)/200×100=75.0%；安全可打印=(200−50−10)/200×100=70.0%（默认 100/8/2→92.0/90.0，避开）" },

  { slug: "encode/base32",
    inputs: { bytes: "100", pad: "1", line: "64" },
    expect: ["163"],
    ref: "ceil(100/5)×8=160，每 64 字符换行→+ceil(160/64)=3→163（默认 line=0→160，避开）" },

  { slug: "encode/base58",
    inputs: { payload: "32", checksum: "4", version: "1" },
    expect: ["37", "51"],
    ref: "总字节=32+4+1=37；Base58 长度=ceil(37×8/5.86)=ceil(50.51)=51（默认 25/4/1→30/41，避开）" },

  { slug: "encode/base64-length",
    inputs: { bytes: "50", padding: "1", wrap: "76" },
    expect: ["68"],
    ref: "ceil(50/3)×4=17×4=68 字符（默认 bytes=100→136，避开）" },

  { slug: "encode/base64-size",
    inputs: { kb: "200", header: "0", linebreak: "0" },
    expect: ["266.67"],
    ref: "ceil(200×1024/3)×4/1024=266.66797→266.67 KB（默认 kb=100→133.34，避开）" },

  { slug: "encode/checksum-collision",
    inputs: { k: "8", attempts: "1000", bits: "1024" },
    expect: ["0.390625"],
    ref: "单次漏检率=2^−8×100=0.390625%（默认 k=16→0.001526，避开；k=32 会舍入为 0.000000 故取 k=8）" },

  { slug: "encode/compression-ratio",
    inputs: { original: "2000", compressed: "500", files: "2" },
    expect: ["75.00", "3000"],
    ref: "压缩率=(1−500/2000)×100=75.00%；总节省=(2000−500)×2=3000 字节（默认 1000/400/1→60.00/600，避开）" },

  { slug: "encode/crc-error-rate",
    inputs: { r: "24", frames: "10000", dataBits: "64" },
    expect: ["27.27"],
    ref: "编码开销=24/(64+24)×100=27.27%（默认 r=16→20.00，避开）" },

  { slug: "encode/crc",
    inputs: { poly_degree: "12", input_bytes: "8" },
    expect: ["4096"],
    ref: "余数空间=2^12=4096（默认 poly_degree=16→65536，避开）" },

  { slug: "encode/encode-2",
    inputs: { len: "512", diff_rate: "25", samples: "2000" },
    expect: ["128", "500"],
    ref: "差异比特=round(512×25/100)=128；采样差异=round(2000×25/100)=500（默认 256/10/1000→26/100，避开）" },

  { slug: "encode/encode-3",
    inputs: { algo: "1", hex: "16" },
    expect: ["24"],
    ref: "algo=1→16 字节→Base64 长度=ceil(16/3)×4=24（默认 algo=3→32 字节→44，避开）" },

  { slug: "encode/encode-4",
    inputs: { letters: "10", dots: "6", unit: "120" },
    expect: ["10800", "0.93"],
    ref: "总时长=10×6×120×1.5=10800 ms；字符速率=10/(10800/1000)=0.93 字/秒（默认 5/4/100→3000/1.67，避开）" },

  { slug: "encode/encode-5",
    inputs: { chars: "50", mode: "1", ec: "2" },
    expect: ["3.33"],
    ref: "mode=1（数字）→3.33 bit/字符（默认 mode=3（字节）→8.00，避开）" },

  { slug: "encode/encode-6",
    inputs: { value: "1000000", base: "10" },
    expect: ["20"],
    ref: "二进制位数=ceil(log(1000001)/log(2))=ceil(19.93)=20（默认 value=255→8；改用以 10 为底避免与 base 默认值 16 撞车）" },

  { slug: "encode/encode-7",
    inputs: { bits: "24", n: "2000" },
    expect: ["5793"],
    ref: "安全阈值 n=√(2×2^24)=√33554432=5792.6→5793（默认 bits=128→2^64.5 巨值，避开）" },

  { slug: "encode/encode",
    inputs: { pos: "10", shift: "7", mod: "26" },
    expect: ["17"],
    ref: "新位置=(10+7)%26=17（默认 0/3/26→3，避开）" },

  { slug: "encode/encoding-redundancy",
    inputs: { avgLen: "3", entropy: "2", symbols: "500" },
    expect: ["33.33", "66.67"],
    ref: "冗余度=(3−2)/3×100=33.33%；编码效率=(2/3)×100=66.67%（默认 2.2/1.8/1000→18.18/81.82，避开；不断言'节省位数'因其恒等于输入 symbols 会撞快照）" },

  { slug: "encode/hamming-bits",
    inputs: { m: "16", msgBits: "10000", dataRate: "2000" },
    expect: ["76.2", "6.563"],
    ref: "m=16→r=5（2^5≥16+5+1）；编码效率=16/21×100=76.2%；传输时间=10000×21/(16×2000)=6.5625→6.563 s（默认 m=8→66.7/12.000，避开）" },

  { slug: "encode/html",
    inputs: { chars: "200", special: "20", unicode: "5" },
    expect: ["335", "48.89"],
    ref: "转义后长度=200+20×5+5×7=335；增长=(20×5+5×7−20−5)/225×100=48.89%（默认 100/10/2→164/46.43，避开）" },

  { slug: "encode/huffman-avg-length",
    inputs: { f1: "10", l1: "1", f2: "5", l2: "3", f3: "5", l3: "4" },
    expect: ["2.2500"],
    ref: "平均码长=(10×1+5×3+5×4)/20=45/20=2.2500 bit/符号（默认 5/3/2→1.7000，避开）" },

  { slug: "encode/jwt-size",
    inputs: { header: "100", payload: "300", sig: "64" },
    expect: ["624", "626"],
    ref: "Base64 部分=ceil(100/3)×4+ceil(300/3)×4+ceil(64/3)×4=136+400+88=624；含分隔符=626（默认 50/200/32→380/382，避开）" },

  { slug: "encode/radix-digits",
    inputs: { N: "1000", base: "10", bytes: "1" },
    expect: ["125"],
    ref: "所需位数=ceil(log1000/log10)=3；可表字节=floor(10^3/8)=125（默认 N=256/base=16→32，避开）" },

  { slug: "encode/shannon-entropy",
    inputs: { p1: "0.25", p2: "0.25", p3: "0.25", p4: "0.25" },
    expect: ["2.0000"],
    ref: "H=4×(−0.25×log2 0.25)=4×0.5=2.0000 bit/符号（默认 0.5/0.25/0.15/0.1→1.7427，避开）" },

  { slug: "encode/url-encoded-length",
    inputs: { textLen: "40", special: "10", alreadyEnc: "5" },
    expect: ["70", "175.0"],
    ref: "编码后长度=(40−10−5)+(10+5)×3=25+45=70；膨胀率=70/40×100=175.0%（默认 20/5/0→30/150.0，避开）" },

  { slug: "encode/url",
    inputs: { ascii: "100", nonascii: "20", space: "10" },
    expect: ["190", "46.15"],
    ref: "编码后长度=100+20×3+10×3=190；增长=(20×2+10×2)/130×100=46.15%（默认 80/10/5→125/31.58，避开）" },

  { slug: "encode/utf-8",
    inputs: { ascii: "200", cjk: "50", emoji: "10" },
    expect: ["390", "50.00"],
    ref: "总字节=200+50×3+10×4=390；较 ASCII 膨胀=(390/260−1)×100=50.00%（默认 100/20/5→180/44.00，避开）" },
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
  console.log("==== encode calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();