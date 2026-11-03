#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "image/generator-15",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "共 8 张"
  ],
  "ref": "auto-restore-structural（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "image/id-photo-crop",
  "inputs": {
    "bgColor": "#ffffff",
    "filename": "id-photo.png",
    "preset": "413,531,二寸（413×531）"
  },
  "expect": [
    "413×531"
  ],
  "ref": "auto-restore"
},
{
  "slug": "image/image-collage",
  "inputs": {
    "rows": "2",
    "cols": "3",
    "fixedVal": "1200",
    "bgColor": "#ffffff",
    "gap": "8",
    "margin": "10",
    "layout": "h"
  },
  "expect": [
    "固定高度"
  ],
  "ref": "auto-restore"
},
{
  "slug": "image/image-compress",
  "inputs": {
    "quality": "120"
  },
  "expect": [
    "120%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "image/image-crop",
  "inputs": {
    "quality": "138"
  },
  "expect": [
    "138"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "image/image-filter",
  "inputs": {
    "brightness": "150",
    "contrast": "100",
    "saturate": "100",
    "hue": "0",
    "blur": "0",
    "grayscale": "0",
    "sepia": "0",
    "invert": "0"
  },
  "expect": [
    "150%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "image/image-mosaic",
  "inputs": {
    "block-size": "15"
  },
  "expect": [
    "15"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "image/image-resize",
  "inputs": {
    "percentSlider": "50",
    "qualitySlider": "85",
    "algorithm": "fast"
  },
  "expect": [
    "fast"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "image/image-rotate",
  "inputs": {
    "angleSlider": "0",
    "customColor": "#3b82f6",
    "formatSelect": "jpeg"
  },
  "expect": [
    "jpeg"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "image/image-watermark",
  "inputs": {
    "wmText": "ToolBox 水印",
    "wmFontSize": "48",
    "wmColor": "#FF6B35",
    "wmColorHex": "#FF6B35",
    "wmOpacity": "50",
    "wmStroke": "0",
    "wmImgScale": "30",
    "wmImgOpacity": "80",
    "wmMargin": "20",
    "wmX": "20",
    "wmY": "20",
    "tileGapX": "120",
    "tileGapY": "120",
    "tileAngle": "-30",
    "tileStagger": "50"
  },
  "expect": [
    "48"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "image/nine-grid-cutter",
  "inputs": {},
  "expect": [
    "请先上传图片"
  ],
  "ref": "结构性不可注入（2026-10-10 复核，原 ref 为 auto-restore(default) 未评估项）：splitAndRender() 依赖 FileReader 读取 #file 图片后 canvas 切片；harness 无文件输入/FileReader/canvas 度量 ⇒ 注入态与默认态均落到「请先上传图片」空文件提示（memory 已知缺口：File API/canvas 图片类不可收敛）。无任何随输入变化的输出。维持 no_inputs。"
},
{
  "slug": "image/nine-grid-cutter",
  "clicks": [
    "document.getElementById('ngcRows').value='9';__ngcSetGrid();"
  ],
  "expect": [
    "已恢复上次合法值 3"
  ],
  "ref": "IM-N7 回归：行数 9 越界（合法 1–6）时必须提示并回退上次合法值 3、输入框同步回显 3。默认态该提示框为空 ⇒ 注入失败/默认态不命中。"
},
{
  "slug": "image/nine-grid-cutter",
  "clicks": [
    "blobs=[Promise.resolve(new Blob([new Uint8Array([1,2,3])],{type:'image/png'}))];downloadAll();"
  ],
  "expect": [
    "多文件下载"
  ],
  "ref": "IM-N5 回归：downloadAll() 入口须同步写入「请允许多文件下载」提示（串行逐张触发）；默认态提示框为空、不调用 downloadAll ⇒ 不命中。"
},
{
  "slug": "image/gif-split",
  "clicks": [
    "var __probe=__gsMakeZip([{name:'probe.txt',bytes:new Uint8Array([65,66,67])}]);document.getElementById('zipStatus').textContent='ZIP:'+__probe.type+':'+__probe.size;"
  ],
  "expect": [
    "ZIP:application/zip"
  ],
  "ref": "IM-N6 回归：本地最小 ZIP（STORE）写入实现 __gsMakeZip 必须返回 application/zip Blob（不再依赖外部 JSZip CDN）；默认态 zipStatus 为空 ⇒ 不命中。"
},
{
  "slug": "image/wechat-cover-maker",
  "inputs": {
    "title": "工具名示例_X",
    "subtitle": "今日学习一款实用在线工具",
    "c1": "#ff6b35",
    "c2": "#7c3aed",
    "textColor": "#ffffff"
  },
  "expect": [
    "工具名示例_X"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
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

  console.log("==== image calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
