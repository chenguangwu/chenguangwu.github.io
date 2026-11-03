#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 12-J3：等量曝光表固定 ISO，光圈按 2^(s/2)、快门按 2^s，N²/t 不变 ⇒ 各档偏差≈0。
  // 基准 f/4、1/125s（非默认 f/5.6、1/60）驱动，期望串均与默认表不同。
  "slug": "photo2/exposure-triangle",
  "clicks": [
    "document.getElementById('aperture').value='4';document.getElementById('shutter').value='0.008';calcEquivalent();"
  ],
  "expect": [
    "1/500s",
    "-0.09"
  ],
  "ref": "独立复算：基准 f/4、1/125(0.008s)、ISO100 ⇒ EV=log2(4²/0.008)=10.97。s=-2：N=2、t=0.002→1/500s ⇒ EV11.0、偏差 +0.00；s=-1：N=2.828→f/2.8、t=0.004→1/250s ⇒ -0.03；s=0 ⇒ +0.00；s=+1：N=5.657→f/5.6、t=0.016→1/60s ⇒ -0.09；s=+2：N=8、t=0.032→1/30s ⇒ -0.04。全部 |偏差|<0.1。默认表（f/5.6、1/60）的偏差为 +0.06/+0.09/0/+0.04/-0.05，无 1/500s 与 -0.09。"
},
{
  // 12-J4：预设「极端值」必须写入控件真实存在的 ISO 档位（旧值 300 不在选项内 → 控件读空 → EV Infinity）。
  "slug": "photo2/exposure-triangle",
  "clicks": [
    "document.getElementById('presetCheck').textContent=(__exposure_trianglePresets.toString().indexOf('\"iso\":\"300\"')>=0?'BAD_PRESET':'PRESET_OK');"
  ],
  "expect": [
    "PRESET_OK"
  ],
  "ref": "读取页面导出的 __exposure_trianglePresets 源码串，必须不含 iso=300 这一无效档位（该值不在 #iso 的 option 列表，浏览器会把 select.value 读成空串）；改为 400 后位于选项内。clicks 被判别器清空时 marker 为空 ⇒ 失配。"
},
{
  // 12-J4 守卫：ISO 为空时提示而非输出 Infinity。
  "slug": "photo2/exposure-triangle",
  "clicks": [
    "document.getElementById('iso').value='';calcEV();"
  ],
  "expect": [
    "ISO 不能为空"
  ],
  "ref": "iso 空串经 +'' 得 0 ⇒ calcEV 守卫输出「请选择有效的光圈、快门与 ISO（ISO 不能为空）」。默认 iso=100 无此提示串，clicks 被清空即失配。"
},
{
  // 12-J4 对照：ISO 400 属真实档位，EV 正常有限（8.9）。
  "slug": "photo2/exposure-triangle",
  "clicks": [
    "document.getElementById('iso').value='400';calcEV();"
  ],
  "expect": [
    "EV 8.9"
  ],
  "ref": "f/5.6、1/60s、ISO400 ⇒ EV=10.88−log2(4)=8.88 →「EV 8.9」。默认 iso=100 ⇒「EV 10.9」，clicks 被清空即失配。"
},
{
  // 12-J5：APS-C 参考对角线统一为 28.2mm（与机身表一致），当前画幅=参考画幅 ⇒ 等效 24mm、系数 1.00。
  "slug": "photo2/focal-length",
  "inputs": {
    "focal": "24"
  },
  "clicks": [
    "document.getElementById('refSensor').value='28.2';selectSensor(1);"
  ],
  "expect": [
    "52.4°",
    "36.0°"
  ],
  "ref": "独立复算：APS-C 23.6×15.6@24mm ⇒ 水平 FOV=2×atan(23.6/48)=52.41°→「52.4°」；垂直 =2×atan(15.6/48)=36.01°→「36.0°」；等效焦距=24×(28.2/28.2)=24mm。默认态 focal=50、全画幅 ⇒ 39.6°/27.0°、50mm，两串均不命中。注意不能锚「24mm」——默认输出「（36×24mm）」会命中，属逃生项。"
},
{
  // 12-J5 守卫：焦距 ≤0 拒绝计算并提示，不再输出负视角。
  "slug": "photo2/focal-length",
  "inputs": {
    "focal": "-50"
  },
  "expect": [
    "请输入大于 0 的有效焦距"
  ],
  "ref": "焦距 -50 经 parseFloat 后 f<=0 ⇒ calc 直接返回错误提示，不产生 atan 负角。默认 focal=50 正常算出 39.6°，无该提示串。"
},
{
  "slug": "photo2/focal-length",
  "inputs": {
    "focal": "53"
  },
  "expect": [
    "37.5°"
  ],
  "ref": "全画幅 36×24@53mm：水平 FOV = 2×atan(36/106)=37.52°→「37.5°」。"
},
{
  "slug": "photo2/video-storage",
  "inputs": {
    "bitrate": "20",
    "hours": "4",
    "minutes": "0",
    "audioBitrate": "128"
  },
  "expect": ["1920,1080\n30\n51.8\n128\n4\n0\n1\n91.28 GB 文件大小 51.93 总码率 Mbps 4时0分 录制时长 分辨率： 1920×1080 （2.1MP/帧） 总帧数： 432,000 帧 @30fps 每分钟存储： 389.5 MB 每小时存储： 22.82 GB 存储卡容量参考： 存储卡 可录时长 32 GB 1时24分 64 GB 2时48分 128 GB 5时36分 256 GB 11时13分 512 GB 22时26分"],
  "ref": "auto-restore"
},
{
  "slug": "photo2/white-balance",
  "inputs": {
    "kelvin": "5503"
  },
  "expect": [
    "5503K"
  ],
  "ref": "auto-restore"
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

  console.log("==== photo2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
