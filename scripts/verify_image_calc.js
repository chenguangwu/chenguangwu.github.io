#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "image/generator-15",
  "clicks": ["document.getElementById('__tbProbe').textContent='RC '+rcRadiusFor(400,300,50,'pct')+'|'+rcRadiusFor(400,300,20,'px')+'|'+rcRadiusFor(100,100,80,'pct');"],
  "expect": [
    "RC 150|20|50"
  ],
  "ref": "第206批·真实圆角半径：400×300 短边 300 的 50%=150px；固定 20px=20；百分比上限 50% ⇒ 100×100 的 80% 被夹到 50px。旧随机半径实现无此函数 ⇒ 失败。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
  "slug": "image/image-mosaic",
  "inputs": { "block-size": "7" },
  "clicks": ["var g=window.__mosaicGeom;var n=+document.getElementById('block-size').value;document.getElementById('block-val').textContent='S:'+g.mapBlockToCanvas(n,0.253333)+'|B:'+g.mapBlockToCanvas(50,0.253333)+'|Z:'+(g.planPreview('area',null,n,0.5).mosaic?1:0);"],
  "expect": ["S:2|B:13|Z:0"],
  "ref": "深度解析算例复算：3000×2000 大图 dispScale=0.253333，块 7px 预览 round(1.773)=2、上限 50px round(12.666)=13；区域模式无选区时 mosaic=0（不画马赛克）。默认块 10 会得到 S:3 ⇒ 注入 7 才命中。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
// 已移除 image/nine-grid-cutter 的空文件态用例（inputs:{}，expect ["请先上传图片"]）。
// 原因：splitAndRender() 依赖 FileReader 读 #file 后 canvas 切片，harness 无文件输入/FileReader/canvas 度量，
// 注入态与默认态都落到同一条「请先上传图片」提示 ⇒ 判别力 0。该 slug 已有「行数越界回退」「多文件下载」
// 「SVG 拒收」「toBlob 失败提示」四条可判别用例覆盖，故按纪律删除该条而非保留 skip。
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
  "slug": "image/gif-split",
  "clicks": ["document.getElementById('zipStatus').textContent='D:'+formatDelay(8)+'|'+formatDelay(5)+'|'+formatDelay(0);"],
  "expect": ["D:80ms|50ms|0ms"],
  "ref": "深度解析算例复算：GIF 帧延时单位 1/100 秒，8→80ms、5→50ms、0→0ms（formatDelay 原样返回 0ms，不兜底 100ms）。默认态 zipStatus 为空 ⇒ 不命中。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "image/wechat-cover-maker",
  "clicks": ["var cv=document.getElementById('cover');cv.width=900;cv.height=383;var ops=[];var ctx={createLinearGradient:function(){return {addColorStop:function(){}}},fillRect:function(x,y,w,h){ops.push([this.fillStyle,x,y,w,h].join(','))},fillText:function(){},measureText:function(s){return {width:s.length*10}}};cv.getContext=function(){return ctx};render();document.getElementById('wcSizeTbl').textContent=ops.join('|');"],
  "expect": ["rgba(0,0,0,0.35),0,222,900,161"],
  "ref": "绘图指令验证：900×383 画布按 58% 高度起遮罩：y=round(383×0.58)=222，高 383−222=161，宽 900，透明度 0.35；记录实际 fillRect 指令，不声称测试了像素。"
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
  "clicks": ["var f=document.getElementById('rcRadius');f.value='';var ff=document.getElementById('rcFiles');Object.defineProperty(ff,'files',{value:[],configurable:true});rcRender();"],
  "expect": ["请先上传 1–12 张图片"],
  "ref": "第206批·无文件空态：不生成任何随机色块，明确提示先上传；旧实现会直接画随机圆角色块 ⇒ 强判别。"
},
{
  "slug": "image/image-filter",
  "clicks": ["applyPreset(13);document.getElementById('__tbProbe').textContent='FLT '+document.getElementById('brightness').value+'|'+document.getElementById('blur').value+'|'+document.getElementById('saturate').value;"],
  "expect": ["FLT 110|1|130"],
  "ref": "第207批·预设回写滑杆：梦幻 preset 必须把亮度 110、模糊 1px、饱和 130 写回输入；旧 applyPreset 只改 CSS ⇒ 滑杆仍是默认 100|0|100，零交集。"
},
{
  "slug": "image/id-photo-crop",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/id-photo-crop",
  "clicks": ["var calls=[],ctx={fillStyle:'',fillRect:function(){},drawImage:function(){calls.push(Array.prototype.slice.call(arguments,1).join(','));}};var img={width:200,height:100};drawCropped(ctx,img,100,100,'#fff','contain');var a=calls.slice();calls=[];drawCropped(ctx,img,100,100,'#fff','cover');document.getElementById('__tbProbe').textContent='IDFIT '+a.join(';')+' | '+calls.join(';');"],
  "expect": ["IDFIT 0,25,100,50 | 50,0,100,100,0,0,100,100"],
  "ref": "2026-11-16（694 批）适配方式：contain 把 200×100 等比缩到 100×50 并垂直居中（dx0,dy25），cover 先横向居中裁出 100×100（sx50,sw100）再铺满整框。旧实现只有 cover 分支、底色永远被照片盖住 ⇒ 无法命中前半段。"
},
{
  "slug": "image/image-collage",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-compress",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-converter",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-crop",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-filter",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-mosaic",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-resize",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-rotate",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/image-watermark",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/nine-grid-cutter",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "image/nine-grid-cutter",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};downloadOne(document.createElement('canvas'),1);"],
  "expect": ["TOAST:导出失败："],
  "ref": "B 类失败注入：桩内 canvas.toBlob 恒回调 null（等价画布被污染时浏览器返回 null）。原本 downloadOne 里 `if (!blob) return;` 静默跳过，"
    + "现必须走 __ngcExportFail → toast「导出失败：浏览器未能生成 PNG（画布可能被污染）」。默认态无 TOAST: 串 ⇒ 判别明确。"
},
{
  "slug": "image/wechat-cover-maker",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var cv=document.getElementById('cover');cv.toBlob=function(cb){cb(null)};download();"],
  "expect": ["TOAST:导出失败：浏览器未能生成 PNG"],
  "ref": "B 类失败注入：download() 原为 `if (!blob) return;` 静默跳过。注入 #cover.toBlob 恒回调 null + 录制 ToolBox.showToast ⇒ 必须出现「TOAST:导出失败：浏览器未能生成 PNG」。"
    + "默认态无 TOAST: 串 ⇒ 判别明确。"
},
{
  "slug": "image/gif-split",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')}};return e;};makeThumb(document.createElement('canvas'),200);"],
  "expect": ["TOAST:缩略图生成失败：Error"],
  "ref": "失败注入：新建画布的 toDataURL 必抛 Error ⇒ makeThumb 必须 toast「缩略图生成失败：Error」并返回空串，不得让异常打断 renderFrameGrid 整帧渲染。"
    + "修复前异常裸冒成 pageerror、整帧网格渲染中断；默认态无 TOAST: 串 ⇒ 判别明确。"
},
{
  "slug": "image/image-compress",
  "clicks": ["var cap='';ToolBox.showToast=function(m){cap=String(m);};TBKit={util:{isEn:function(){return true;}}};__svgFileBlocked({type:'image/svg+xml',name:'x.svg'});var en=cap;TBKit={util:{isEn:function(){return false;}}};__svgFileBlocked({type:'image/svg+xml',name:'x.svg'});var zh=cap;document.getElementById('__svg_probe').textContent='IMN3 '+(en.indexOf('Only bitmap')>=0&&en.indexOf('SVG')>=0&&zh.indexOf('仅支持位图')>=0?'OK':'BAD '+en+'|'+zh);"],
  "expect": ["IMN3 OK"],
  "ref": "IM-N3 英文态动态 toast：旧版 __svgFileBlocked 的 toast 硬编码中文「仅支持位图（PNG/JPG/WebP），不支持 SVG」，EN 探针按 textContent 替换不会改写 JS 动态 toast，英文态用户看到中文。现所有动态 toast 走 __imgEn() 中英切换。注入 isEn=true/false 双断言；默认态不执行 clicks 故无 IMN3 串 ⇒ 强判别。"
},
{
  "slug": "image/image-resize",
  "clicks": ["var cap='';ToolBox.showToast=function(m){cap=String(m);};TBKit={util:{isEn:function(){return true;}}};__svgFileBlocked({type:'image/svg+xml',name:'x.svg'});var en=cap;TBKit={util:{isEn:function(){return false;}}};__svgFileBlocked({type:'image/svg+xml',name:'x.svg'});var zh=cap;document.getElementById('__svg_probe').textContent='IMN3R '+(en.indexOf('SVG images are not supported')>=0&&zh.indexOf('不支持 SVG 图片')>=0?'OK':'BAD '+en+'|'+zh);"],
  "expect": ["IMN3R OK"],
  "ref": "IM-N3 resize 页同类：旧版 __svgFileBlocked 及下载/导出/复制 toast 全硬编码中文。现统一 __imgEn() 中英切换（含「尺寸过大」「导出失败」「已下载」「复制失败」）。isEn 双断言，默认态不命中。"
},
{
  "slug": "image/image-resize",
  "clicks": ["var r0=window.__resizeValidate(100.4,200);var r1=window.__resizeValidate(100,200.75);var r2=window.__resizeValidate(100,200);document.getElementById('sizeError').textContent='I731A:'+(r0.valid?'1':'0')+'|'+(r1.valid?'1':'0')+'|'+r2.w+'x'+r2.h+'|'+r0.error;"],
  "expect": ["I731A:0|0|100x200|宽高必须是整数像素（当前 100.4×200），小数会改变宽高比，请改成 100×200 或调整锁定比例。"],
  "ref": "第731A批·小数尺寸不再静默取整：旧 validateTargetSize 对 100.4 四舍五入成 100（用户填 100.4 却导出 100），现小数直接判无效并给出实际取整建议；合法 100×200 仍通过。默认态 sizeError 无文本 ⇒ 不命中。"
},
{
  "slug": "image/image-converter",
  "clicks": ["var a=window.__convResolveMaxSide('800');var b=window.__convResolveMaxSide('800.5');var c=window.__convResolveMaxSide('0');var d=window.__convResolveMaxSide('12000');var e=window.__convResolveMaxSide('-5');document.getElementById('convMaxSideError').textContent='M731A:'+a.value+'|'+(b.valid?'1':'0')+'|'+c.value+'|'+(d.valid?'1':'0')+'|'+(e.valid?'1':'0')+'|'+b.error;"],
  "expect": ["M731A:800|0|0|0|0|最长边必须是整数像素（当前“800.5”），请取整后再转换。"],
  "ref": "第731A批·最长边不再 parseInt 截断：旧实现 800.5→800、12000→静默夹到 10000、负数→不限制。现合法整数 800 通过，留空/0 仍表示原尺寸，小数与超限明确报错。默认态 convMaxSideError 无文本 ⇒ 不命中。"
},
{
  "slug": "image/image-converter",
  "clicks": ["var n0=window.__convDownloadName('照片 a.png','webp',800,600,85);var n1=window.__convDownloadName('a/b:c*?.jpg','png',100,100,null);var n2=window.__convDownloadName('','jpg',10,10,null);document.getElementById('convMaxSideError').textContent='F731A:'+n0+'|'+n1+'|'+n2;"],
  "expect": ["F731A:照片_a-800x600-q85.webp|bc-100x100.png|image-10x10.jpg"],
  "ref": "第731A批·下载文件名带来源：旧名恒为 converted-时间戳.扩展名，多图混在一起无法对应。现保留清洗后的来源名（去路径/非法字符）+ 实际输出尺寸 + 有损质量；中文名、非法字符、空名三种输入都落到可辨识且安全的名字。"
},
{
  "slug": "image/image-collage",
  "clicks": ["var a=CollageTool.gridSize('2.5','3');var b=CollageTool.gridSize('','3');var c=CollageTool.gridSize('4','5');var d=CollageTool.gridSize('21','3');document.getElementById('infoBox').textContent='G731A:'+(a.valid?'1':'0')+'|'+(b.valid?'1':'0')+'|'+c.rows+'x'+c.cols+'|'+(d.valid?'1':'0')+'|'+a.error;"],
  "expect": ["G731A:0|0|4x5|0|行数必须是整数（当前“2.5”），小数无法排出完整网格。"],
  "ref": "第731A批·自定义网格行列严格整数：旧实现 clamp(+value||1,1,20) 让 2.5 列照常参与 Math.floor(idx/cols)，空值静默变 1、21 静默变 20。现小数/空值/越界均判无效并给出对应提示，1–20 整数正常通过（4×5）。"
},
{
  "slug": "image/image-compress",
  "clicks": ["document.getElementById('bgColor').value='#112233';document.getElementById('fmt').value='jpeg';var s=getSettings();document.getElementById('results-card').textContent='BG986:'+s.bg.toUpperCase()+'|F:'+s.format;"],
  "expect": ["BG986:#112233|F:jpeg"],
  "ref": "第987批：JPEG 背景色必须进入压缩参数；注入 #112233 后 getSettings().bg 原样返回（非法值回落 #ffffff），避免 UI 选色与实际 canvas 填充脱节。"
}
];
function batch204StaticChecks(){
  var src = fs.readFileSync("tools/image/image-resize.html","utf8");
  var out=[];
  out.push({name:"B204 platform presets",ok:src.indexOf('setPlatformSize(1242,1660')>=0&&src.indexOf('setPlatformSize(900,383')>=0&&src.indexOf('function setPlatformSize(w,h,label)')>=0});
  var cmp = fs.readFileSync("tools/image/image-compress.html","utf8");
  var rc = fs.readFileSync("tools/image/generator-15.html","utf8");
  var rot2 = fs.readFileSync("tools/image/image-rotate.html","utf8");
  out.push({name:"B212 rotate batch and memory",ok:rot2.indexOf("multiple style=")>=0&&rot2.indexOf("downloadBatchZip")>=0&&rot2.indexOf("localStorage.setItem(PREF_KEY")>=0&&rot2.indexOf("id=\"batchBar\"")>=0});
  var idc = fs.readFileSync("tools/image/id-photo-crop.html","utf8");
  out.push({name:"B211 id-photo crop view/dpi/zip",ok:idc.indexOf('id="cropZoom"')>=0&&idc.indexOf("function pngWithDpi")>=0&&idc.indexOf("function downloadAllPresets")>=0&&idc.indexOf("cropView.dx = clampNum")>=0});
  var col = fs.readFileSync("tools/image/image-collage.html","utf8");
  out.push({name:"B210 collage sort/reverse/undo",ok:col.indexOf("sortNames: function")>=0&&col.indexOf("images.reverse()")>=0&&col.indexOf("history.pop()")>=0&&col.indexOf('id="listToolbar"')>=0});
  var mos = fs.readFileSync("tools/image/image-mosaic.html","utf8");
  out.push({name:"B210 mosaic multiple regions",ok:mos.indexOf('id="mosaicMulti"')>=0&&mos.indexOf('regions.push(nr)')>=0&&mos.indexOf('regionsNat.forEach')>=0});
  var ngc = fs.readFileSync("tools/image/nine-grid-cutter.html","utf8");
  out.push({name:"B209 nine-grid output size",ok:ngc.indexOf('id="ngcOutSide"')>=0&&ngc.indexOf("function __ngcComputeDims")>=0&&ngc.indexOf("输出每片")>=0&&ngc.indexOf("像素保真")>=0});
  var cvr = fs.readFileSync("tools/image/image-converter.html","utf8");
  out.push({name:"B209 converter controls",ok:cvr.indexOf('id="convQuality"')>=0&&cvr.indexOf('id="convMaxSide"')>=0&&cvr.indexOf('class="convFmt"')>=0&&cvr.indexOf('f.lossy ? quality : undefined')>=0});
  var idp = fs.readFileSync("tools/image/id-photo-crop.html","utf8");
  out.push({name:"B207 id-photo onerror clears",ok:idp.indexOf('srcImg = null;')>=0&&idp.indexOf('无法解码该图片')>=0});
  var rot = fs.readFileSync("tools/image/image-rotate.html","utf8");
  out.push({name:"B208 rotate preview cap",ok:rot.indexOf("PREVIEW_MAX_PIXELS = 16000000")>=0&&rot.indexOf("PREVIEW_MAX_SIDE = 4096")>=0&&rot.indexOf("function rotatedDimensions(w, h, a)")>=0&&rot.indexOf("function drawRotatedImage(canvas, img, scale, state)")>=0&&rot.indexOf("lastPreviewScale")>=0});
  out.push({name:"B207 rotate filename after decode",ok:(function(){var i=rot.indexOf('img.onload = function()');var j=rot.indexOf('resolve({ img: img, name:',i);var k=rot.indexOf('img.onerror',i);return i>=0&&j>i&&k>j&&rot.indexOf('fileName = batchImages[i].name')>=0;})()});
  var wc = fs.readFileSync("tools/image/wechat-cover-maker.html","utf8");
  out.push({name:"B207 cover sizes",ok:wc.indexOf('id="coverSize"')>=0&&wc.indexOf('function wcTargetSize')>=0&&wc.indexOf('wcFitBlock')>=0&&wc.indexOf('hasCJK')>=0&&wc.indexOf('Math.max(tw / c.width, th / c.height)')<0});
  var flt = fs.readFileSync("tools/image/image-filter.html","utf8");
  out.push({name:"B207 filter preset sync",ok:flt.indexOf("document.getElementById('brightness').value = m[1]")>=0&&flt.indexOf('exportFilter')>=0});
  out.push({name:"B206 real rounded image",ok:rc.indexOf('id="rcFiles"')>=0&&rc.indexOf('function rcRender()')>=0&&rc.indexOf('function rcRadiusFor(')>=0&&rc.indexOf('function randColor()')<0});
  out.push({name:"B205 target volume",ok:cmp.indexOf("function compressToTarget(img,s,targetBytes)")>=0&&cmp.indexOf("targetSize")>=0&&cmp.indexOf("tries++>=7")>=0});
  out.push({name:"B731A resize BMP accept",ok:src.indexOf('accept="image/png,image/jpeg,image/webp,image/gif,image/bmp,.bmp"')>=0&&src.indexOf('支持 PNG / JPEG / WebP / GIF / BMP')>=0});
  out.push({name:"B731A converter maxside/outsize/filename",ok:cvr.indexOf("function resolveMaxSide(")>=0&&cvr.indexOf("function makeDownloadName(")>=0&&cvr.indexOf('id="convOutSize"')>=0&&cvr.indexOf('id="convMaxSideError"')>=0&&cvr.indexOf('converted-${Date.now()')<0});
  out.push({name:"B731A collage grid integer",ok:col.indexOf("function resolveGridSize(")>=0&&col.indexOf("gridSize: resolveGridSize")>=0&&col.indexOf("layout').value === 'custom'")>=0});
  out.push({name:"B986 converter JPEG background",ok:cvr.indexOf('id="convBg"')>=0&&cvr.indexOf('ctx.fillStyle = jpegBg')>=0&&cvr.indexOf('JPEG 背景 ')>=0});
  out.push({name:"B986 compress JPEG background",ok:cmp.indexOf('id="bg-row"')>=0&&cmp.indexOf('id="bgColor"')>=0&&cmp.indexOf('bg:s.bg')>=0&&cmp.indexOf('ctx.fillStyle=(s.bg||')>=0&&cmp.indexOf("(__imgEn()?'JPEG background: '")>=0});
  out.push({name:"B986 resize JPEG background",ok:src.indexOf('id="bgRow"')>=0&&src.indexOf('id="bgColor"')>=0&&src.indexOf('ctx.fillStyle = jpegBg')>=0&&src.indexOf("(__imgEn()?'JPEG background: '")>=0});
  return out;
}

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

  const __stat = batch204StaticChecks();
  const __sf = __stat.filter(function(x){return !x.ok;});
  for (const x of __sf) console.log("❌ [static] " + x.name);
  console.log("==== image calc " + pass + "/" + cases.length + " ====");
  if (fails.length || __sf.length) process.exit(1);
}
if (require.main === module) main();
