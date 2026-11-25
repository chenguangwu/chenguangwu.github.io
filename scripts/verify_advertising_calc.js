#!/usr/bin node
"use strict";
// 第十八批（advertising）弱用例去默认化：
//   原 16 例中 12 例为 all_default（注入值 = 页面默认值，注入失败也 PASS），
//   另有 analysis-27/55 两例断言 textarea 回显 "80_X"、generator-time/storyboard-timeline 两例靠兜底函数命中。
//   本批全部改为「非默认输入 + Python 独立复算 expect」，expect 逐例避开页面可见静态文案/算例字面量。
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "advertising/ad-size",
  "inputs": { "width": "600", "height": "1600", "fromUnit": "mm", "dpi": "96" },
  "expect": ["1709mm / 6458px", "60.0×160.0 厘米 cm"],
  "ref": "默认 1920×1080 px/300dpi；独立复算：mm 原样→wPX=round(600/25.4×96)=2268、hPX=round(1600/25.4×96)=6047，cm=60.0/160.0，对角线 mm=√2920000=1709、px=√(2268²+6047²)=6458。默认态输出 187mm / 2203px，零交集。"
},
{
  "slug": "advertising/assessor-52",
  "inputs": { "budget": "200000", "venueCost": "60000", "promoCost": "30000", "otherCost": "10000", "reach": "120000", "attendRate": "2", "convRate": "8", "arpu": "150" },
  "expect": ["-71.2% 活动 ROI", "¥-71,200 净收益/亏损"],
  "ref": "默认 ROI +248.8%（优秀）；独立复算：总成本=60000+30000+10000=100000，到场=120000×2%=2400，转化=2400×8%=192，收入=192×150=28800，ROI=(28800-100000)/100000=-71.2%，净收益=-71200。"
},
{
  "slug": "advertising/assessor-53",
  "inputs": { "ch0": "信息流", "cost0": "12000", "ch1": "短视频", "cost1": "9000", "totalConv": "300", "convValue": "200" },
  "expect": ["¥23,500 总触点成本", "155% 整体 ROI"],
  "ref": "默认触点成本 ¥10,500 / ROI 471%；独立复算：成本=12000+9000+2000+500=23500，收入=300×200=60000，ROI=(60000-23500)/23500=155.3%→155%。注意不能选「¥60,000 总转化价值」（默认 120×500 也是 60000）。"
},
{
  "slug": "advertising/assessor-54",
  "inputs": { "traffic": "20000", "boards": "3", "days": "14", "noticeRate": "20", "targetPop": "800000", "totalCost": "50000" },
  "expect": ["CPM 千次曝光成本 ¥59.52", "单次注意成本 ¥0.2976"],
  "ref": "默认 CPM ¥10.00 / 单次 ¥0.0286；独立复算：OTS=20000×3×14=840000，注意到=840000×20%=168000，CPM=50000/840000×1000=59.5238→59.52，单次=50000/168000=0.297619→0.2976。"
},
{
  "slug": "advertising/assessor-55",
  "inputs": { "targetPop": "300", "spots": "40", "rating": "1.5", "totalCost": "120", "reachCap": "60", "effFreq": "4" },
  "expect": ["预估到达率 48.00%", "有效到达率（≥4次） 15.00%"],
  "ref": "默认到达率 68.18%（默认 effFreq=3 无「≥4次」字样）；独立复算：GRP=1.5×40=60，Reach=(60/75)×60=48（≤上限60），频次=60/48=1.25，有效到达=48×(1.25/4)=15.00%。"
},
{
  "slug": "advertising/color-convert",
  "inputs": { "r": "0", "g": "114", "b": "187" },
  "expect": ["互补色： #FF8D44", "C:100 M:39 Y:0 K:27", "203° 色相 H"],
  "ref": "默认 #FF6B35 → 互补 #0094CA / CMYK C:0 M:58 Y:79 K:0 / 色相 16°；独立复算：k=1-187/255=0.2667，C=(1-0-0.2667)/0.7333=100、M=(1-114/255-0.2667)/0.7333=39、Y=0、K=27，HSL h=203°，互补=(255,141,68)=#FF8D44。注意不可用等级词「冷色」——兜底 randomColor() 在 harness 确定性 PRNG 下恒得 rgb(91,27,172)（h=266°，同为冷色），会成逃生项。"
},
{
  "slug": "advertising/color-convert",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/advertising/color-convert.html','utf8');var i=h.indexOf('function fromRGB(){');var seg=i>=0?h.slice(i,i+520):'';var ok=seg.indexOf('rv===')>=0&&seg.indexOf('gv===')>=0&&seg.indexOf('bv===')>=0&&seg.indexOf('__clearColorOutputs')>=0;document.getElementById('__tbProbe').textContent='CCRGB0 '+(ok?'OK':'BAD');"],
  "expect": ["CCRGB0 OK"],
  "ref": "第1369批·RGB 空项按 0 计算修复：fromRGB 逐项校验 r/g/b，任一项空/非法即清空 hex/CMYK/HSL/LAB 与预览；旧版整表空才守卫、单空按 0 ⇒ BAD。"
},
{
  "slug": "advertising/reach-frequency",
  "clicks": ["document.getElementById('rounds').value='0';document.getElementById('singleReach').value='20';calcMulti()"],
  "expect": ["投放轮次须为 ≥1 的整数。"],
  "ref": "第1344批·0 轮被替换为 1 修复：注入 0 轮必须拒绝（旧版 +v||1 替换成 1 仍出一轮结果，命中「1轮」而非该提示）。"
},
{
  "slug": "advertising/reach-frequency",
  "clicks": ["document.getElementById('rounds').value='2';document.getElementById('singleReach').value='0';calcMulti()"],
  "expect": ["0.0%"],
  "ref": "第1344批·合法 0% 不得被当成空值：单次到达率 0%、2 轮 ⇒ 累计到达 0.0%，仍应正常出表；默认 25%/4 轮为 68.4%，不命中。"
},
{
  "slug": "advertising/convert-26",
  "inputs": { "px": "192", "dpi": "96" },
  "expect": ["物理尺寸 = 50.80 mm"],
  "ref": "去默认化：物理尺寸 = px×25.4/DPI = 192×25.4/96 = 50.80 mm。默认态 px=96/dpi=96 ⇒ 25.40 mm，不命中。"
},
{
  "slug": "advertising/convert-26",
  "inputs": { "px": "100", "dpi": "72" },
  "expect": ["物理尺寸 = 35.28 mm"],
  "ref": "去默认化：100×25.4/72 = 35.28 mm。默认态不命中。"
},
{
  "slug": "advertising/convert-26",
  "inputs": { "px": "150", "dpi": "300" },
  "expect": ["物理尺寸 = 12.70 mm"],
  "ref": "去默认化：150×25.4/300 = 12.70 mm。默认态不命中。"
},
{
  "slug": "advertising/convert-27",
  "inputs": { "c": "100", "m": "100", "y": "100", "k": "0" },
  "expect": ["R = 0", "G = 0", "B = 0"],
  "ref": "去默认化：CMYK(100,100,100,0) ⇒ 纯黑 R=G=B=0。默认态 C=M=Y=K=0 ⇒ 白(255/255/255)，不命中。"
},
{
  "slug": "advertising/convert-27",
  "inputs": { "c": "0", "m": "100", "y": "100", "k": "0" },
  "expect": ["G = 0", "B = 0"],
  "ref": "去默认化：CMYK(0,100,100,0) ⇒ 红 R=255/G=0/B=0。默认态白屏 G=B=255，故锚 G=0、B=0（避 R=255 撞默认）不命中。"
},
{
  "slug": "advertising/convert-27",
  "inputs": { "c": "50", "m": "0", "y": "0", "k": "0" },
  "expect": ["R = 128"],
  "ref": "去默认化：CMYK(50,0,0,0) ⇒ R=255×0.5=128、G=B=255。默认态 R=255，故仅锚 R=128（避 G=B=255 撞默认）不命中。"
},
{
  "slug": "advertising/convert-27",
  "inputs": { "c": "0", "m": "50", "y": "0", "k": "25" },
  "expect": ["R = 191", "G = 96", "B = 191"],
  "ref": "去默认化：CMYK(0,50,0,25) ⇒ R=255×0.75=191、G=255×0.5×0.75=96、B=191。默认态不命中。"
},
{
  "slug": "advertising/copy-duration",
  "inputs": { "content": "" },
  "clicks": ["calc()"],
  "expect": ["请输入文案内容后再计算朗读时长。"],
  "ref": "空文案必须给输入提示，不得输出「0秒朗读时长 / 0中文字数」的伪结果；默认文案非空、不含该提示。"
},
{
  "slug": "advertising/copy-duration",
  "inputs": { "content": "品牌增长方法论与实战案例拆解", "speedType": "custom", "customSpeed": "300", "lang": "zh", "pauseTime": "1" },
  "expect": ["300字/分钟 （自定义）", "纯朗读： 2.8秒"],
  "ref": "默认（空文案 + 正常 240字/分）输出 0 字 / 0.0秒 /「240字/分钟 （正常）」；独立复算：中文 14 字→等效 14，baseSec=14/300×60=2.8，单段落→停顿 0.0，语速名=自定义。"
},
{
  "slug": "advertising/estimate-cycle",
  "inputs": { "arpu": "120", "churn": "4", "margin": "60", "cac": "300" },
  "expect": ["¥1,800.00 LTV 用户生命周期价值", "6.00:1 LTV:CAC 比率"],
  "ref": "默认 LTV ¥700.00 / 3.50:1 / 25.0→20.0 月；独立复算：生命周期=1/4%=25 月，月毛利=120×60%=72，LTV=72/0.04=1800，比率=1800/300=6.00，回本=300/72=4.17→4.2 月。"
},
{
  "slug": "advertising/reach-frequency",
  "inputs": { "population": "500000", "reach": "120000", "impressions": "480000", "cost": "24000", "mPopulation": "2000000", "rounds": "6", "singleReach": "15" },
  "expect": ["62.3% 累计到达率", "1,245,701 累计触达人数", "¥250.00 CP/GRP"],
  "ref": "默认累计 68.4% / 683,594 / CP-GRP ¥571.43；独立复算：单轮 15% → 6 轮后未触达=0.85⁶=0.377150，累计=62.285%→62.3%，人数=round(0.62285×2000000)=1245701；基础 GRP=24×4=96，CP/GRP=24000/96=250.00。避开静态文案「边际递减效应」。"
},
{
  "slug": "advertising/tester-15",
  "inputs": { "impA": "4000", "clickA": "80", "impB": "4000", "clickB": "200", "alpha": "0.01" },
  "expect": ["样本量偏少，建议每组至少 5000 次曝光以保证统计效力。", "Z 统计量 7.3003"],
  "ref": "默认每组 12000→「样本量充足，检验结果可信。」；独立复算：CTR_A=2%、CTR_B=5%、合并=3.5%，SE=√(0.035×0.965×(1/4000+1/4000))=0.0041093，Z=0.03/0.0041093=7.3003>2.576 显著。P 值因 '< 0.001' 被标签剥离吞掉，不作 expect。"
},
{
  "slug": "advertising/analysis-27",
  "inputs": { "data": "小米,30\n华为,25\n苹果,20\nOPPO,15\nvivo,10" },
  "expect": ["最大份额竞品： 小米", "HHI 指数： 2250"],
  "ref": "重做为「竞品份额定位分析」：输入 竞品,份额 多行。独立复算：份额降序 小米30/华为25/苹果20/OPPO15/vivo10，top=小米（30.00%），HHI=30²+25²+20²+15²+10²=2250（>1800 高度集中）。默认 data（自家,18/竞品A,35…）top=竞品A、HHI=2526，与本例零交集，判別力成立。"
},
{
  "slug": "advertising/analysis-55",
  "inputs": { "data": "A,1000,50,5,3\nB,2000,80,10,5\nC,1500,60,8,4" },
  "expect": ["转化率最高： C", "13.33%"],
  "ref": "重做为「竞品广告/投放/创意分析」：输入 竞品,曝光,点击,转化,创意数。独立复算：A cvr=5/50=10.00%、B=10/80=12.50%、C=8/60=13.33%，按 cvr 降序 best=C（13.33%）。默认 data（4 项）cvr 均≤5%，与 13.33% 零交集。"
},
{
  "slug": "advertising/generator-time",
  "inputs": { "cnt": "12" },
  "expect": ["12 00:"],
  "ref": "默认 cnt=5 只生成 5 行（序号最大 5），注入 12 才有第 12 行；SHOTS 共 12 条，cnt≥12 时恒为 12 行。前 11 条时长各 2–5 秒 → 第 12 行时间码恒 <60s（00:22–00:55），故「12 00:」与 PRNG 取值无关、稳定成立。原断言「8 00:」虽非默认，但只能靠条数判别，保留同机制并放大到 12。"
},
{
  "slug": "advertising/storyboard-timeline",
  "inputs": { "targetDuration": "45" },
  "expect": ["还剩45秒空间", "-45 差异(秒)"],
  "ref": "默认 target=30 → 差异 -30 /「还剩30秒空间」；本例 harness 下 scenes 为空数组（总时长 0），diff=0-45=-45。原断言「还剩15秒空间」依赖兜底函数加载模板后才成立，属危险信号，改为只依赖注入键的真值。"
},
{
  "slug": 'advertising/ad-size',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/advertising/ad-size.html\',\'utf8\');var i=h.indexOf(\'function copyResult(){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+900):\'\';var ok=seg.indexOf(\'请先填写宽度与高度再复制\')>=0&&seg.indexOf(\'fromUnit\')>=0&&seg.indexOf(\'wPX\')>=0;document.getElementById(\'__tbProbe\').textContent=\'ADSCP0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['ADSCP0 OK'],
  "ref": "第1341批·复制与页面结果不同源修复源码形态强锚：旧版 copyResult 另算一遍且无守卫，页面显示错误/—时复制仍输出 Infinity/0dB 假值；修复后 copyResult 补与 calc 同源守卫，无效时提示并 return。旧版无 ⇒ BAD。"
},
{
  "slug": "advertising/reach-frequency",
  "clicks": ["var c=[],t=[];var oc=ToolBox.copyText,ot=ToolBox.showToast;ToolBox.copyText=function(x){c.push(String(x))};ToolBox.showToast=function(m){t.push(String(m))};document.getElementById('population').value='100000';document.getElementById('reach').value='35000';document.getElementById('impressions').value='87500';document.getElementById('cost').value='50000';calcBasic();copyBasic();document.getElementById('population').value='';calcBasic();copyBasic();ToolBox.copyText=oc;ToolBox.showToast=ot;document.getElementById('__tbProbe').textContent='BASICCP '+((c.length===1&&c[0].indexOf('到达率:35.0%')>=0&&t.length===1&&t[0].indexOf('请先完成有效')>=0)?'OK':'BAD');"],
  "expect": ["BASICCP OK"],
  "ref": "第1347批·空输入复制假结果修复：先有效计算并复制（35.0%/2.50），再清空人口计算后复制应拒绝并提示；旧版 copyBasic 用默认值直接算 ⇒ 第二次仍复制且无提示，BAD。"
},

{
  "slug": 'advertising/convert-26',
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+\"tools/advertising/convert-26.html\",'utf8');var i=h.indexOf('const px=+document.getElementById(\\\"px\\\")');var seg=i>=0?h.slice(i,i+240):'';var ok=seg.indexOf('!isFinite(dpi)||dpi<=0')>=0&&seg.indexOf('DPI 须为正数')>=0;document.getElementById('__tbProbe').textContent='PXDPIDIV '+(ok?'OK':'BAD');})();"],
  "expect": ['PXDPIDIV OK'],
  "ref": "第1346批·分母为零守卫源码形态强锚：旧版 dpi=0 时 mm=px*25.4/0=Infinity，主输出显示「物理尺寸 = Infinity mm」；修复后 dpi 非正提示并 return。旧版无 ⇒ BAD。"
},
{
  "slug": "advertising/reach-frequency",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/advertising/reach-frequency.html','utf8');var i=h.indexOf('function copyBasic(){');var seg=i>=0?h.slice(i,i+500):'';var ok=h.indexOf('var lastBasicResult')>=0&&h.indexOf('到达率:')>=0&&seg.indexOf('if(!lastBasicResult)')>=0&&seg.indexOf('ToolBox.showToast')>=0&&seg.indexOf('ToolBox.copyText(lastBasicResult')>=0;document.getElementById('__tbProbe').textContent='BASICCP '+(ok?'OK':'BAD');"],
  "expect": ["BASICCP OK"],
  "ref": "第1347批·空输入复制假结果修复：calcBasic 末尾缓存有效结果到 lastBasicResult（缺参/无效值时保持空），copyBasic 只复制该缓存并在空时提示拒绝；旧版用默认值直接算 ⇒ BAD。真机有效复制 35.0%/2.50、清空人口后拒绝提示。"
},

{
  "slug": "advertising/estimate-cycle",
  "inputs": { "arpu": "50", "churn": "5", "margin": "", "cac": "200" },
  "expect": ["请填写毛利率后再计算。"],
  "ref": "毛利率留空：旧代码 parseFloat||0 使 LTV、LTV:CAC 与回本周期全部变成 0 或无穷，却照常渲染结论；新增守卫后须提示。"
},

  // 第883批
  {
  slug: "advertising/color-convert",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/advertising/color-convert.html','utf8');document.getElementById('__tbProbe').textContent='RGBLAB '+((src.indexOf('RGB 反相色（非色轮互补）')>=0&&src.indexOf('HSL 色相 +180°')>=0)?'OK':'BAD');"],
  expect: ["RGBLAB OK"],
  ref: "第883批：原把 255−RGB 叫「互补色」，与 HSL 色轮互补不一致；现明确标为 RGB 反相色并提示色轮互补按 HSL 色相 +180° 计算。"
},
  {
  slug: "advertising/assessor-55",
  clicks: ["calc()"],
  inputs: {"targetPop": "500", "spots": "60", "rating": "2.5", "totalCost": "80", "reachCap": "75", "effFreq": "3"},
  expect: ["68.2", "106.67"],
  ref: "第883批：深挖示例原用「到达人数」当 CPM 分母，与页面 GRP/100×目标观众的总曝光公式不一致；现示例改为 750 万 OTS、CPM 106.7，并用同一组默认参数测试 68.2%/106.67。"
},
  {
  slug: "advertising/reach-frequency",
  clicks: ["var src=__tbFs.readFileSync(process.cwd()+'/tools/advertising/reach-frequency.html','utf8');document.getElementById('__tbProbe').textContent='REACHCPM '+((src.indexOf('200万÷1000')>=0)?'OK':'BAD');"],
  expect: ["REACHCPM OK"],
  ref: "第883批：深挖算例用触达 40 万当 CPM 分母，算出 500 元/千人，与 CPM=费用/总曝光×1000 不符；现按 200 万曝光得 100 元/千人，并补 CPR 0.5 元/人。"
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

  console.log("==== advertising calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
