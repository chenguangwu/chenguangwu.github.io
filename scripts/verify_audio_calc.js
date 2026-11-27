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
{
  "slug": "audio/analysis-1",
  "inputs": { "fs": "1", "N": "131072", "bin": "1" },
  "expect": ["7.6294e-6"],
  "ref": "第1024批：极低频率不再固定 4/3 位小数被显示为 0；Δf=1/131072=7.6293945e-6，按 4 位有效数字输出 7.6294e-6，目标 bin 同样科学计数。"
},
{
  "slug": "audio/analysis-1",
  "inputs": { "fs": "44100", "N": "1024.5", "bin": "100" },
  "expect": ["正整数 FFT 长度"],
  "ref": "第1024批：FFT 长度必须是正整数；1024.5 不得继续产出分辨率/bin 频率。默认 4096 不含该提示 ⇒ 强判别。"
},
{
  "slug": "audio/analysis-1",
  "clicks": ["document.getElementById('fs').value='';calc();document.getElementById('__tbProbe').textContent='ACOPY '+((document.getElementById('copyBtn').disabled)?'OK':'BAD');"],
  "expect": ["ACOPY OK"],
  "ref": "第1024批：输入无效时复制按钮禁用，避免把“请输入…”错误提示当结果复制；恢复有效输入后 calc 重新启用。"
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
},
{
  "slug": "audio/audio-sample-rate",
  "inputs": { "duration": "90" },
  "expect": ["22,050 Hz", "24,000 Hz", "15.14", "16.48"],
  "ref": "第1025批：频率上限改为精确 Hz（44.1k→22,050、48k→24,000），不再 22.1/24.0 一位小数；PCM 数据量 44.1k/16bit/2ch/90s≈15.14 MiB，48k≈16.48 MiB；默认 60s 为 10.09/10.99，不命中。"
},
{
  "slug": "audio/audio-sample-rate",
  "inputs": { "duration": "0" },
  "expect": ["请输入大于 0 的有效时长（秒）"],
  "ref": "第1025批：时长清空/0 时清空主结果、统计与副结论并显示明确提示；默认 60 秒不含该提示 ⇒ 强判别。"
},
{
  "slug": "audio/audio-sample-rate",
  "clicks": ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-sample-rate.html','utf8');var ok=src.indexOf('function convertFile')>=0&&src.indexOf('OfflineAudioContext')>=0&&src.indexOf('audioBufferToWav')>=0&&src.indexOf('exportResampled')>=0&&src.indexOf('__asrFileSeq')>=0&&src.indexOf('__asrResult')>=0&&src.indexOf('未压缩 PCM')>=0&&src.indexOf('function __asrFmtHz')>=0;document.getElementById('__tbProbe').textContent='ASRATE '+(ok?'OK':'BAD');"],
  "expect": ["ASRATE OK"],
  "ref": "第1025批（6 任务）：本地 OfflineAudioContext 重采样/试听/WAV 导出；输入条件+指标结构化结果供复制与历史；PCM MiB 与理论奈奎斯特口径；无效时长清空全部结论；解码/目标变化可取消。"
},
{
  slug: "audio/audio-echo",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/audio/audio-echo.html','utf8');var ok=src.indexOf('Math.floor(x * total / buckets)')>=0&&src.indexOf('for(var ch=0; ch<channels; ch++)')>=0&&src.indexOf('function applyCompressorRouting')>=0&&src.indexOf('compEnabled')>=0&&src.indexOf('wetOn ? Math.min(60, tailNeeded) : 0')>=0&&src.indexOf('function downmixForExport')>=0&&src.indexOf('srcCh > 2 ? downmixForExport')>=0&&src.indexOf('function flushEffectTail')>=0&&src.indexOf('forcedRate')>=0&&src.indexOf('seed = (seed * 1664525')>=0&&src.indexOf('__audioLoadSeq')>=0&&src.indexOf('（保留）')>=0&&src.indexOf('snap.name.replace')>=0;document.getElementById('__tbProbe').textContent='AUDIOECHO '+(ok?'OK':'BAD');"],
  expect: ["AUDIOECHO OK"],
  ref: "第1023批（10 任务）：波形按比例桶覆盖全声道全部采样；压缩器可显式旁路；纯干声不追加尾长；暂停/停止重建效果链清尾音；多声道下混立体声导出；固定种子脉冲使试听/导出/重复导出一致；解码请求序号与失败保留旧音频；导出快照音频/文件名/参数。"
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
