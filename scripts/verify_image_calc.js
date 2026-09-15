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
    "生成圆角图片预览"
  ],
  "ref": "auto-restore-structural"
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
  "ref": "auto-restore"
},
{
  "slug": "image/nine-grid-cutter",
  "inputs": {},
  "expect": [
    "请先上传图片"
  ],
  "ref": "auto-restore(default)"
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
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== image calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
