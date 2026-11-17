#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "video/analysis-69",
  "inputs": {
    "selfViews": "12000",
    "selfLike": "8",
    "selfFinish": "55",
    "rivalViews": "3000,4000,3500,5000,2500"
  },
  "expect": [
    "竞品平均播放： 3600",
    "竞品中位播放： 3500",
    "相对均值差距： 233.3%",
    "市场定位： 头部账号"
  ],
  "ref": "非默认：竞品(3000,4000,3500,5000,2500)均值3600、中位3500；自身12000→差距(12000-3600)/3600=233.3%；12000>3600*1.5=5400→头部。默认(8000/5000,7000,6000,9000,4500)均值6300腰部，注入失败即不命中"
},
{
  "slug": "video/subtitle-tool",
  "inputs": {
    "offset-ms": "7",
    "speed-factor": "1",
    "srt-input": " 00:00:04,000\nHello World\">"
  },
  "expect": [
    "007"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-compressor",
  "inputs": {
    "duration": "15",
    "targetSize": "100"
  },
  "expect": [
    "910kbps"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-converter",
  "inputs": {
    "duration": "15"
  },
  "expect": ["youtube\n1080\n15\nh264\n1080p 分辨率 8000k 视频码率 0.90GB 预估大小 H264 编码 💻 FFmpeg 命令： ffmpeg -i input.mp4 -c:v libx264 -b:v 8000k -c:a aac -b:a 384k -s 1920:1080 -preset medium -crf 23 output.webm 视频大小 878.9MB 音频大小 42.2MB 时长 15分钟 目标平台 YouTube\n暂无记录"],
  "ref": "auto-restore"
},
{
  "slug": "video/video-speed",
  "inputs": {
    "h": "7",
    "m": "30",
    "s": "0",
    "ms": "0",
    "fps": "30",
    "speed": "1.5"
  },
  "expect": [
    "810"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-trimmer",
  "inputs": {
    "start-h": "0",
    "start-m": "1",
    "start-s": "30",
    "end-h": "0",
    "end-m": "3",
    "end-s": "0"
  },
  "expect": [
    "00:01:30 → 00:03:00",
    "总时长: 00:01:30"
  ],
  "ref": "start=0×3600+1×60+30=90s ⇒ 00:01:30；end=3×60=180s ⇒ 00:03:00；片段时长=180−90=90s ⇒ 00:01:30。"
     + "原 expect「添加一个开始吧」是空列表提示（默认全 0 ⇒ 起止相同、无法成段，回退默认仍命中 ⇒ 逃生项）。"
},
{
  "slug": "video/video-compressor",
  "clicks": ["document.getElementById('duration').value='0';calc();"],
  "expect": ["请输入有效的视频时长"],
  "ref": "943零值守卫：时长显式填 0 须提示并停止，不得静默按 10 分钟计算。默认 duration=10 ⇒ 出压缩参数不含该提示。"
},
{
  "slug": "video/video-compressor",
  "clicks": ["var d=document.getElementById('duration');d.value='';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='VCDUR '+(h.indexOf('请输入有效的视频时长')>=0&&h.indexOf('kbps')<0?'OK':'BAD');"],
  "expect": ["VCDUR OK"],
  "ref": "943清空守卫：时长清空须同样拦截且不残留旧 kbps 参数；旧版 +''||10 会静默按 10 分钟出结果 ⇒ 哨兵 BAD。"
},
{
  "slug": "video/video-converter",
  "clicks": ["document.getElementById('duration').value='0';generate();"],
  "expect": ["请输入有效的视频时长"],
  "ref": "943零值守卫：转换器时长 0 须提示，不得用 0 估算大小/生成命令。默认 duration=10 不命中。"
},
{
  "slug": "video/video-speed",
  "inputs": { "h": "0", "m": "0", "s": "1", "ms": "0", "fps": "30", "speed": "0.75" },
  "expect": ["增加00:00.333"],
  "ref": "减速对照：1 秒素材按 0.75× 播放需 1.333 秒，差值为负 0.333 秒。旧版把负数直接送 fmtTimeShort 得「节省-1:-1」；现按绝对值显示并改标签为「增加00:00.333」。默认 30 分钟 1.5× 命中「节省」不命中本串。"
},
{
  "slug": "video/video-fps",
  "inputs": { "duration": "10" },
  "clicks": ["var s=document.getElementById('srcFps'),d=document.getElementById('dstFps');s.value='24';d.value='60';calc();var t=String(document.getElementById('frameDesc').innerHTML||'');var r=String(document.getElementById('frameResult').textContent||'');var ok=t.indexOf('时长仍为 10s 不变')>=0&&t.indexOf('放慢')<0&&t.indexOf('慢放')>=0&&r.indexOf('240 → 600 帧')>=0;document.getElementById('__tbProbe').textContent='VFPSUP '+(ok?'OK':'BAD '+t.slice(0,120));"],
  "expect": ["VFPSUP OK"],
  "ref": "P-N9 升帧误述：源24→目标60、10s，旧版 frameDesc 写「放慢2.50倍播放」暗示时长变 25s，但 frameResult 仍 240→600 帧/时长10s，自相矛盾。现改为「时长仍为 10s 不变」并提示如需慢放须另用变速重定时。注入非默认目标60（默认30）避开默认态。"
},
{
  "slug": "video/video-fps",
  "inputs": { "duration": "10" },
  "clicks": ["var s=document.getElementById('srcFps'),d=document.getElementById('dstFps');s.value='60';d.value='24';calc();var t=String(document.getElementById('frameDesc').innerHTML||'');var r=String(document.getElementById('frameResult').textContent||'');var ok=t.indexOf('时长仍为 10s 不变')>=0&&t.indexOf('加速')<0&&t.indexOf('快放')>=0&&r.indexOf('600 → 240 帧')>=0;document.getElementById('__tbProbe').textContent='VFPSDN '+(ok?'OK':'BAD '+t.slice(0,120));"],
  "expect": ["VFPSDN OK"],
  "ref": "P-N9 降帧误述：源60→目标24、10s，旧版写「加速2.50倍播放」暗示时长变 4s，但帧数 600→240/时长10s。现改为「时长仍为 10s 不变」+「如需快放须另用变速重定时」。注入非默认源60（默认24）避开默认态。P-N10 同批修正公式框与权威源算例口径（时长比=源÷目标、速度比=目标÷源）。"
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

  console.log("==== video calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
