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
  "clicks": [
    "var p=CollageTool.fitPlan(200,100,10,10,100,100,'cover');var o=CollageTool.orderLoaded([{index:2,item:'c'},{index:0,item:'a'},{index:3,item:null},{index:1,item:'b'}]);document.getElementById('infoBox').textContent='DRAW:'+[p.dx,p.dy,p.dw,p.dh].join(',')+'|CLIP:'+[p.clip.x,p.clip.y,p.clip.w,p.clip.h].join(',')+'|ORD:'+o.join('');"
  ],
  "expect": [
    "DRAW:-40,10,200,100|CLIP:10,10,100,100|ORD:abc"
  ],
  "ref": "IM-D2 回归：cover 下 200×100 图填入 (10,10) 起点的 100×100 格会画到 −40..160、覆盖邻格与间距 ⇒ fitPlan 必须给出严格裁剪矩形 clip=格子本身；加载完成须按 FileList 索引归并（乱序回调 2,0,3(失败),1 → abc，失败项剔除）。旧实现无 fitPlan/orderLoaded ⇒ 点击即抛错、infoBox 为空。"
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
  "slug": "image/image-compress",
  "clicks": [
    "var s=getSettings();document.getElementById('quality').value='0';var q0=getSettings().quality;document.getElementById('results-card').textContent='EXT:'+extForMime('image/webp')+'|Q:'+s.quality+'|Q0:'+q0;"
  ],
  "expect": [
    "EXT:webp|Q:0.8|Q0:0.01"
  ],
  "ref": "质量参数边界/格式扩展名回归：默认质量 80 ⇒ 0.8；注入 0 后必须夹到 0.01（旧实现直接 0/100=0，传给 toBlob 越界）；下载扩展名按实际 blob 类型映射（image/webp→webp），改格式后不会出现旧内容配新扩展名。默认态 results-card 为空 ⇒ 不命中。"
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
  "slug": "image/image-mosaic",
  "inputs": {
    "block-size": "15"
  },
  "clicks": [
    "var g=window.__mosaicGeom;var n=+document.getElementById('block-size').value;var p=g.planPreview('full',null,n,0.25);var q=g.planPreview('area',{x:0,y:0,w:40,h:40},n,0.5);document.getElementById('block-val').textContent='PLAN:'+p.block+':'+(p.mosaic?'1':'0')+':'+(p.region===null?'F':'R')+'|AREA:'+q.block+':'+(q.region===null?'F':'R')+'|RAW:'+g.mapBlockToCanvas(n,1);"
  ],
  "expect": [
    "PLAN:4:1:F|AREA:8:R|RAW:15"
  ],
  "ref": "IM-D1 回归：块大小统一以原图坐标定义并按画布缩放换算（15px @0.25 → 4、@0.5 → 8、1:1 → 15）；全图模式预览必须实际打码（mosaic=1 且 region 为空）。旧实现全图预览直接画原图（mosaic=0），且把显示坐标下的数值直接当块大小（预览高估强度）。默认块大小 10 会得到 PLAN:3:1:F|AREA:5:R|RAW:10 ⇒ 注入失败必失配。"
},
{
  "slug": "image/image-crop",
  "clicks": [
    "var g=window.__cropGeom;var b=g.fitCropBox(98,98,12,12,100,100,12,1);var o=g.clampCropOutput({x:88.4,y:88.4,w:12.6,h:12.6},100,100);document.getElementById('ci-w').textContent='BOX:'+[b.x,b.y,b.w,b.h].join(',')+'|OUT:'+[o.x,o.y,o.w,o.h].join(',');"
  ],
  "expect": [
    "BOX:88,88,12,12|OUT:88,88,12,12"
  ],
  "ref": "IM-D3 回归：100×100 图在右下角 (98,98) 建 1:1 框，最小 12px 在边界内放不下 ⇒ 必须移动起点到 (88,88) 且保持 12×12（旧实现先限边界再强推最小尺寸，内存留在 12×12 但导出只剩 2×2）；clampCropOutput 同时保证取整夹边后「信息栏显示尺寸 = 实际导出尺寸」（12.6 取整 13 后夹到 12）。旧实现无这两个纯函数 ⇒ 点击即抛错、ci-w 为空。"
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
  "slug": "image/image-resize",
  "clicks": [
    "var r0=window.__resizeValidate(0,500);var r1=window.__resizeValidate(12000,800);var r2=window.__resizeValidate(800,600);document.getElementById('sizeError').textContent='V0:'+(r0.valid?'1':'0')+'|V1:'+(r1.valid?'1':'0')+'|V2:'+(r2.valid?'1':'0')+':'+r1.error;showSourceNotice('image/gif');"
  ],
  "expect": [
    "V0:0|V1:0|V2:1:请输入 1–10000 之间的整数宽高。"
  ],
  "ref": "IM-N1 回归：目标宽高为 0 / 超过 10000 时必须判为无效（旧实现 parseInt||1 会静默输出 1×1、超上限仍建超大画布），合法 800×600 必须通过。默认态无 sizeError 文本 ⇒ 不命中。"
},
{
  "slug": "image/image-resize",
  "clicks": [
    "showSourceNotice('image/gif');"
  ],
  "expect": [
    "本工具只读取第一帧"
  ],
  "ref": "IM-N2 回归：GIF 输入必须出现「只读取第一帧」提示（旧实现静默把动图当静态位图）。默认态 sourceNotice 为空 ⇒ 不命中。"
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
  "slug": "image/image-watermark",
  "clicks": [
    "var p=exportPlan('webp');var j=exportPlan('jpeg');document.getElementById('resultBox').textContent='WEBP:'+(p.flatten?'1':'0')+':'+(p.background===null?'F':'B')+'|JPEG:'+(j.flatten?'1':'0')+':'+j.background;"
  ],
  "expect": [
    "WEBP:0:F|JPEG:1:#FFFFFF"
  ],
  "ref": "水印透明回归：透明 PNG/WebP 导出不得铺白底（旧实现 format!=='png' 一律铺白，WebP 丢 alpha）；仅 JPEG 铺 #FFFFFF。默认态 resultBox 为空 ⇒ 不命中。"
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
},
{
  "slug": "design/image-flipper",
  "clicks": [
    "var _oc=document.createElement;window.Image=function(){this.width=40;this.height=30;var s='';var self=this;Object.defineProperty(this,'src',{get:function(){return s;},set:function(v){s=v;if(self.onload)self.onload();}});};window.FileReader=function(){this.readAsDataURL=function(f){if(this.onload)this.onload({target:{result:f.dataURL}});};};document.createElement=function(t){if(t==='canvas'){return{width:0,height:0,getContext:function(){return{translate:function(){},scale:function(){},drawImage:function(){}};},toDataURL:function(){return 'data:image/png;base64,'+window.__flipToken;},toBlob:null};}return _oc(t);};var fi=document.getElementById('fileInput');window.__flipToken='TOKEN_A';fi.files=[{dataURL:'data:image/png;base64,TOKEN_A'}];fi.fire('change');flip('h');var s1=window.__flipperState();window.__flipToken='TOKEN_B';fi.files=[{dataURL:'data:image/png;base64,TOKEN_B'}];fi.fire('change');var s2=window.__flipperState();flip('v');var s3=window.__flipperState();document.getElementById('image_flipperPresets').textContent='SW1:'+(s1.hasResult?1:0)+'|SW2:'+(s2.hasResult?1:0)+'|NEW:'+(s3.dataURL.indexOf('TOKEN_B')>=0?1:0)+'|SRC:'+(s3.source.indexOf('TOKEN_B')>=0?1:0)+'|HREF:'+(s3.href===s3.dataURL?1:0);"
  ],
  "expect": [
    "SW1:1|SW2:0|NEW:1|SRC:1|HREF:1"
  ],
  "ref": "EL-J1 回归：上传 A → 水平翻转 → 换图 B（must 立即作废旧结果）→ 垂直翻转。旧实现换图不清 lastURL，s2.hasResult 仍为 1 且下载 href 指向 A；新实现换图即 clearResult()，s2=0，翻转后 dataURL/currentImg 均为 B、下载 href 与 dataURL 一致。"
},
{
  "slug": "image/generator-15",
  "inputs": { "cnt": "" },
  "expect": ["请输入生成数量（1–50）后再生成。"],
  "ref": "空态回归：生成数量清空时旧实现 `parseInt||5` 仍生成 5 张预览；现要求提示且不出图。默认态含「共 5 张」不含该提示 ⇒ 强判别。"
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
