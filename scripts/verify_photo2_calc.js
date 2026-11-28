#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 12-J3：等量曝光表固定 ISO，光圈按 2^(s/2)、快门按 2^s，N²/t 不变 ⇒ 各档偏差≈0。
  // 基准 f/4、1/125s（非默认 f/5.6、1/60）驱动，期望串均与默认表不同。
  "slug": "photo2/exposure-triangle",
  "clicks": [
    "var ap=document.getElementById('aperture');ap.selectedIndex=4;var sh=document.getElementById('shutter');sh.selectedIndex=3;calcEquivalent();"
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
    "document.getElementById('__tbProbe').textContent=(__exposure_trianglePresets.toString().indexOf('\"iso\":\"300\"')>=0?'BAD_PRESET':'PRESET_OK');"
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
  "expect": ["20.13 Mbps","折算后总码率","十进制 GB"],
  "ref": "auto-restore"
},
{
  "slug": "photo2/video-storage",
  "inputs": {
    "bitrate": "20",
    "hours": "0",
    "minutes": "0",
    "audioBitrate": "128"
  },
  "expect": ["录制总时长须大于 0"],
  "ref": "978 零时长守卫：hours=minutes=0 时 sizeGB=0，存储卡可录时长全为 0 分；修复前照常渲染 0KB，默认 hours=1 不含该提示。"
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
},
{
  "slug": "photo2/video-storage",
  "inputs": {"bitrate":"20","hours":"1","minutes":"0","audioBitrate":"128","codec":"0.5"},
  "expect": ["26.03 Mbps","11.71 GB"],
  "ref": "第830批：编码因子只作用于视频码率 20×0.5=10，加音频 0.128 ⇒ 10.13 Mbps；1 小时按十进制 GB=(51.8×0.5+0.128=26.03Mbps ⇒ 11.71GB。页面按分辨率建议把视频码率置 51.8Mbps；旧版把系数同时乘音频并按 1024 换算，得约 22.82GB，两串均不命中。"
},
{
  "slug": "photo2/focal-length",
  "inputs": {"focal":"20"},
  "clicks": ["selectSensor(4);"],
  "expect": ["按参考画幅等效约 55mm","标准/中焦"],
  "ref": "第830批：1 英寸画幅（13.2×8.8）装 20mm，按全幅参考对角线等效约 20×43.27/15.86≈55mm；建议须按等效焦距判为标准/中焦，旧版按实际 20mm 判超广角。默认全幅 50mm 输出约 50mm，不含 55mm 前缀。"
},
{
  "slug": "photo2/exposure-triangle",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/photo2/exposure-triangle.html','utf8');var ok=h.indexOf('EV 加 1 表示这组光圈/快门少收一档光')>=0&&h.indexOf('ISO 只改变亮度增益，不改变光学进光量')>=0&&h.indexOf('数值每加 1 表示进光量翻倍')<0;document.getElementById('__tbProbe').textContent='EV830 '+(ok?'OK':'BAD');"],
  "expect": ["EV830 OK"],
  "ref": "第830批：EV=log2(N²/t) 只由光圈快门定义，加 1 档是少收一档光（光学曝光量减半）；ISO 仅亮度增益。旧 FAQ 称「每加 1 进光量翻倍、三者综合」方向相反，探针同时要求新表述存在且旧句消失。"
},
{
    "slug": "photo2/white-balance",
    "inputs": {"kelvin":"30000"},
    "expect": ["30000K","Mired 绝对值：33"],
    "ref": "第865批：输入上限 40000 K，calc 旧实现只到 20000 K；30000 K 应正常出结果，Mired 绝对值 33。"
  },
  {
    "slug": "photo2/white-balance",
    "inputs": {"kelvin":"30000"},
    "clicks": ["var c=0;var old=ToolBox.copyText;ToolBox.copyText=function(){c++;};copyResult();ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='TB865W '+((c===1)?'OK':'BAD');"],
    "expect": ["TB865W OK"],
    "ref": "第865批：复制入口复用 1000–40000 K 校验，不再被空的 Mired 必填拦截；30000 K 应成功复制一次。"
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
