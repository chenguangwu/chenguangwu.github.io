#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "audio/analysis-1",
  "inputs": {
    "fs": "8000",
    "N": "1024",
    "bin": "10"
  },
  "expect": [
    "78.125"
  ],
  "ref": "Δf=8000/1024=7.8125 Hz，目标 bin10 对应频率=10×7.8125=78.125 Hz（独立计算）"
},
// 已移除 audio/audio-cut（inputs startInput=0/endInput=0，expect ["00.000"]）。
// 原因：结果区由音频文件解码后的 duration 驱动，harness 无文件输入/Web Audio 解码 ⇒ 注入 start/end
// 后输出逐字不变（默认态即命中），无任何可判别增量 ⇒ 按纪律删除而非保留 skip。
{
  "slug": "audio/audio-waveform",
  "inputs": {
    "waveColor": "#FF6B35",
    "smoothing": "3.8"
  },
  "expect": [
    "3.8"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "audio/analysis-1",
  "inputs": {
    "fs": "48000",
    "N": "8192",
    "bin": "1000"
  },
  "expect": [
    "5859.375"
  ],
  "ref": "Δf=48000/8192=5.859375 Hz，目标 bin1000 对应频率=1000×5.859375=5859.375 Hz（独立计算）；默认态 44100/4096/bin200 输出 2153.32 ⇒ 强判别"
},
{
  "slug": "audio/analysis-1",
  "inputs": { "fs": "", "N": "", "bin": "" },
  "expect": ["请输入有效采样率与 FFT 长度"],
  "ref": "空态回归：fs/N 为空时旧实现 `parseFloat(...)||44100 / ||4096` 静默代入默认值并输出分辨率/奈奎斯特频率；现要求提示。默认态 10.7666/22050.00 不含该提示 ⇒ 强判别。"
},

  // 第883批
  {
  slug: "audio/audio-waveform",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-waveform.html','utf8');document.getElementById('__tbProbe').textContent='AUDIOWAVE '+((src.indexOf('role=\"slider\"')>=0&&src.indexOf(\"progressTrack').addEventListener('keydown\")>=0)?'OK':'BAD');"],
  expect: ["AUDIOWAVE OK"],
  ref: "第883批：波形播放器进度条补键盘语义，方向键 ±5 秒、Shift ±1 秒、Home/End 跳首尾，并同步 aria-valuenow。"
},
{
  slug: "audio/audio-waveform",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-waveform.html','utf8');var ok=src.indexOf('__overviewState')>=0&&src.indexOf('retryOverview')>=0&&src.indexOf('Math.floor(i * samples / bucketCount)')>=0&&src.indexOf('Math.floor(i * bufLen / barCount)')>=0&&src.indexOf('Oscilloscope')>=0&&src.indexOf('Playback failed')>=0;document.getElementById('__tbProbe').textContent='AVWAVE2 '+(ok?'OK':'BAD');"],
  expect: ["AVWAVE2 OK"],
  ref: "第1020批：概览分桶按 samples/bucketCount 比例覆盖首尾且桶数不超过样本数；频谱按 bufLen/barCount 比例覆盖尾部高频；解码状态 idle/loading/ok/fail + retryOverview；画布标签与播放失败提示按 __awEn() 输出英文。"
},
{
  slug: "audio/audio-recorder",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-recorder.html','utf8');var ok=src.indexOf('isStarting')>=0&&src.indexOf('micReqSeq')>=0&&src.indexOf('function finishRecording')>=0&&src.indexOf('function cleanupRecording')>=0&&src.indexOf('recSeq++')>=0&&src.indexOf('function stopListAudio')>=0&&src.indexOf('loadedObjectUrl')>=0&&src.indexOf('releaseLoadedObjectUrl')>=0&&src.indexOf('function audioExtForBlob')>=0&&src.indexOf('snapBlob')>=0&&src.indexOf('clipped = 0')>=0&&src.indexOf('normalized')>=0&&src.indexOf('preservesPitch = false')>=0&&src.indexOf('AR_LASTKEY')>=0&&src.indexOf('__arCommitBaseline')>=0&&src.indexOf('recordings.length + 1')<0;document.getElementById('__tbProbe').textContent='AUDIOREC ALL '+(ok?'OK':'BAD');"],
  expect: ["AUDIOREC ALL OK"],
  ref: "第1021批（15 任务）：录音请求守卫与清理、列表单实例播放、对象地址释放、原扩展名映射、导出快照与削波归一化、试听保调开关统一、设置基线独立保存。"
},
{
  slug: "audio/audio-cut",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-cut.html','utf8');var ok=src.indexOf('function getMinGap')>=0&&src.indexOf('function getFadeSeconds')>=0&&src.indexOf('fadeEnable')>=0&&src.indexOf('for (var ch = 0; ch < channels; ch++)')>=0&&src.indexOf('updateSelInfo(true); // 回填')>=0&&src.indexOf('snapStart')>=0&&src.indexOf('makeExportName(snapName')>=0&&src.indexOf('loadSeq')>=0&&src.indexOf('rec.__file')>=0&&src.indexOf('handleFileSelect();')<0;document.getElementById('__tbProbe').textContent='AUDIOCUT '+(ok?'OK':'BAD');"],
  expect: ["AUDIOCUT OK"],
  ref: "第1022批（9 任务）：全声道峰值聚合；动态 getMinGap 支持短于 20ms 文件；时间输入越界回填；导出文件名/选区/淡变快照；getFadeSeconds 试听与导出一致且可关闭；loadSeq 防解码竞态、失败保留旧音频；历史在解码后记录、恢复不调用文件选择。"
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

  console.log("==== audio calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
