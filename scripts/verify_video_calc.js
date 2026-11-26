#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
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
  "expect": ["1920×1080 横屏 16:9 输出", "8000k 视频码率", "0.90GB 按目标码率预估", "-b:v 8000k", "force_original_aspect_ratio=increase,crop=1920:1080", "output.webm"],
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
},
{
  slug: "video/video-compressor",
  clicks: ["var calls=0;globalThis.TBKit={util:{isEn:function(){return false},exportTable:function(){calls++}},history:{record:function(){calls++}}};var d=document.getElementById('duration');d.value='';calc();__video_compressorExport();__video_compressorExtras();var a=calls;d.value='10';__video_compressorExport();document.getElementById('__tbProbe').textContent='VIDEXPORTC_'+(a===0&&calls===1?'OK':'BAD');"],
  expect: ["VIDEXPORTC_OK"],
  ref: "943再次复核：空时长禁止导出和保存，恢复有效时长后导出可用。"
},
{
  slug: "video/video-converter",
  clicks: ["var calls=0;globalThis.TBKit={util:{isEn:function(){return false},exportTable:function(){calls++}},history:{record:function(){calls++}}};var d=document.getElementById('duration');d.value='0';generate();__video_converterExport();__video_converterExtras();var a=calls;d.value='10';__video_converterExport();document.getElementById('__tbProbe').textContent='VIDEXPORTV_'+(a===0&&calls===1?'OK':'BAD');"],
  expect: ["VIDEXPORTV_OK"],
  ref: "943再次复核：零时长禁止导出和保存，恢复有效时长后导出可用。"
},
{
  slug: "video/video-speed",
  clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+'tools/video/video-speed.html','utf8');var i=h.indexOf('const totalSec=totalMs/1000;');var s=i>=0?h.slice(i,i+380):'';var ok=s.indexOf('sp<=0')>=0&&s.indexOf('totalSec<=0')>=0&&s.indexOf('播放速度须为正数')>=0;document.getElementById('__tbProbe').textContent='VIDSPDIV '+(ok?'OK':'BAD');"],
  expect: ["VIDSPDIV OK"],
  ref: "第1346批·分母为零守卫：旧版 sp=0 时 newMs=totalMs/0=Infinity、totalSec=0 时 savePct=0/0=NaN%；修复后 sp 与 totalSec 非正均提示并 return。"
},
{
  slug: "video/video-speed",
  clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+'tools/video/video-speed.html','utf8');var i=h.indexOf('var __fpsRaw=');var s=i>=0?h.slice(i,i+560):'';var ok=s.indexOf('__fpsRaw===')>=0&&s.indexOf('parseFloat(__fpsRaw)')>=0&&s.indexOf('!isFinite(fps)||fps<=0')>=0&&s.indexOf('帧率须为正数')>=0;document.getElementById('__tbProbe').textContent='VIDFPSNEG '+(ok?'OK':'BAD');"],
  expect: ["VIDFPSNEG OK"],
  ref: "第1348批·帧率为负守卫：旧版 fps=-1 时输出「总帧数 -300 @ -1fps / 帧时长 -1000ms」荒谬值（帧率须为正）；输入守卫只拦空与非数字不拦负数。修复后 fps 非正数提示并 return。"
},
{
  "slug": "video/video-speed",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/video/video-speed.html','utf8');var i=h.indexOf('var __spRaw=');var s=i>=0?h.slice(i,i+260):'';var ok=s.indexOf('var __spRaw=')>=0&&s.indexOf('__spRaw===')>=0&&s.indexOf('parseFloat(__spRaw)')>=0;document.getElementById('__tbProbe').textContent='VSPDRAW '+(ok?'OK':'BAD');"],
  "expect": ["VSPDRAW OK"],
  "ref": "第1346批·速度 0 被 ||1 静默替换修复：速度改为原始串解析并去除 ||1；真机 speed=0 提示「播放速度须为正数」并拒绝。旧版 +value||1 ⇒ BAD。"
},
{
  "slug": "video/video-speed",
  "clicks": ["document.getElementById('h').value='0';document.getElementById('m').value='0';document.getElementById('s').value='0';document.getElementById('ms').value='999';document.getElementById('fps').value='30';document.getElementById('speed').value='1';calc();"],
  "expect": ["00:00:01:00"],
  "ref": "时间码进位：0.999s@30fps 旧版直接四舍五入毫秒部分得 FF=30（00:00:00:30 越界）；现先算总帧数 round(0.999×30)=30，再按 fps 进位得 00:00:01:00。默认 30 分钟无此值。"
},
{
  "slug": "video/video-fps",
  "clicks": ["document.getElementById('srcFps').value='';calc();"],
  "expect": ["请填写有效的正数：源帧率"],
  "ref": "空帧率守卫：旧版 srcFps 为空时 srcFrames=NaN、ratio=NaN 仍落入「帧率相同」；现要求源/目标帧率均有限正数，否则清空帧数/网格并提示。默认 24/30 不命中。"
},
{
  "slug": "video/analysis-69",
  "clicks": ["document.getElementById('selfViews').value='1000';document.getElementById('rivalViews').value='0,0';calc();"],
  "expect": ["相对差距不可定义"],
  "ref": "零均值除零：竞品样本 0,0 时均值 0，旧版 gap=Infinity、定位落长尾；现停止并明确不可定义。默认竞品样本非零不命中。"
},
{
  "slug": "video/video-converter",
  "clicks": ["document.getElementById('rateMode').value='crf';generate();"],
  "expect": ["-crf 23 -preset medium", "CRF 恒定质量模式", "不能当作精确预估"],
  "ref": "CRF 与目标码率分离：恒定质量模式命令不再同时含 -b:v，并说明大小不可精确预估；默认 bitrate 模式含 -b:v，不命中。"
},
{
  "slug": "video/subtitle-tool",
  "clicks": ["var nl=String.fromCharCode(10);document.getElementById('srt-input').value=['1','00:00:01,000 --> 00:00:04,000','Hello','','2','00:00:05,000 --> 00:00:06,000','World'].join(nl);parseSRT();document.getElementById('offset-ms').value='-5000';document.getElementById('shift-only-positive').checked=true;applyOffset();"],
  "expect": ["1 条字幕已移除", "00:00:00,000 → 00:00:01,000"],
  "ref": "只保留正时间：偏移 -5s 后第 1 条（1–4s）终点 -1s 完全早于 0 被删除，第 2 条 5–6s 变 0–1s；旧版把两条都截成 0 起点且保留零时长。"
},
{
  "slug": "video/subtitle-tool",
  "clicks": ["var nl=String.fromCharCode(10);document.getElementById('srt-input').value=['1','00:00:01,000 --> 00:00:04,000','Hello'].join(nl);parseSRT();document.getElementById('offset-ms').value='-3000';document.getElementById('shift-only-positive').checked=false;applyOffset();"],
  "expect": ["-00:00:02,000", "预览保留负时间"],
  "ref": "未勾选时保留负时间预览：1–4s 偏移 -3s 得 -2–1s，不再强制截 0；导出时才裁剪/跳过。默认 offset=0 不命中。"
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
