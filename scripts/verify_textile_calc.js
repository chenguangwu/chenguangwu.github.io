#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "textile/calc-gsm",
  "inputs": {
    "wWeight": "8.2",
    "wWidth": "20",
    "wLength": "20",
    "wFabricWidth": "150",
    "cValue": "200",
    "cWidth": "150",
    "yWarpCount": "40",
    "yWeftCount": "40",
    "yEPC": "25",
    "yPPC": "22",
    "yWarpCrimp": "5",
    "yWeftCrimp": "4",
    "yFabricWidth": "150"
  },
  "expect": [
    "30750.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/color-fastness",
  "inputs": {
    "fastType": "rub"
  },
  "expect": [
    "4(干)/3(湿)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/colorfastness",
  "inputs": {
    "origColor": "#1e88e5_X",
    "testColor": "#90caf9"
  },
  "expect": [
    "1e88e5_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/colorfastness",
  "clicks": ["var w=rgbToLab(hexToRgb('#ffffff')),k=rgbToLab(hexToRgb('#000000')),d=deltaE(w,k);document.getElementById('__tbProbe').textContent='CF715 '+((Math.abs(w.a)<0.05&&Math.abs(w.b)<0.05&&Math.abs(w.L-100)<0.05&&Math.abs(d-100)<0.1)?'OK':'BAD');"],
  "expect": ["CF715 OK"],
  "ref": "白点归一化：旧实现把 sRGB 矩阵结果乘参考白后再除同一白，纯白得 a≈-8.4、b≈-5.8，白-黑 ΔE=100.59；现逐行除以矩阵自身白点 (0.9505/1.0000/1.0890)，纯白 a=b=0、ΔE(白,黑)=100.00。"
},
{
  "slug": "textile/shrinkage",
  "clicks": ["document.getElementById('shrinkPct').value='150';calcPredict();var t=String(document.getElementById('resultPredict').innerHTML);document.getElementById('__tbProbe').textContent='SK715 '+((t.indexOf('0~100%')>=0&&t.indexOf('-50')<0)?'OK':'BAD');"],
  "expect": ["SK715 OK"],
  "ref": "预测缩水率 150%：旧实现算出成品 -50cm；现要求 0≤缩水率<100%，越界提示且不输出负成品。默认 100cm/5% 不命中。"
},
{
  "slug": "textile/shrinkage",
  "clicks": ["document.getElementById('shrinkPct').value='';calcPredict();var t=String(document.getElementById('resultPredict').innerHTML);document.getElementById('__tbProbe').textContent='SK715B '+((t.indexOf('留空不按 0 计算')>=0)?'OK':'BAD');"],
  "expect": ["SK715B OK"],
  "ref": "缩水率清空：旧 parseFloat(...)||0 把空值当 0 并输出「不变」；现提示留空不按 0 计算，不再给出确定结果。"
},
{
  "slug": "textile/shrinkage",
  "clicks": ["document.getElementById('shrinkPct2').value='';calcReverse();var t=String(document.getElementById('resultReverse').innerHTML);document.getElementById('__tbProbe').textContent='SK715C '+((t.indexOf('留空不按 0 计算')>=0)?'OK':'BAD');"],
  "expect": ["SK715C OK"],
  "ref": "反算缩水率清空：旧实现同样按 0 处理并给出应裁剪尺寸；现拦截。"
},
{
  "slug": "textile/shrinkage",
  "clicks": ["var t=String(document.getElementById('resultReverse').innerHTML);document.getElementById('__tbProbe').textContent='SK715D '+((t.indexOf('需裁剪')>=0)?'OK':'BAD');"],
  "expect": ["SK715D OK"],
  "ref": "反算初始态：页面加载时仅运行预测，反算结果区为空直到改动输入；现初始化同时运行 calcReverse，默认 100cm/5% 即显示应裁剪 105.26cm。"
},
{
  "slug": "textile/convert-48",
  "inputs": {
    "val": "30"
  },
  "expect": [ "旦尼尔 270.00" ],
  "ref": "auto-restore"
},
{
  "slug": "textile/convert-yarn",
  "inputs": { "val": "30", "from": "ne" },
  "expect": ["英支 Ne = 30.00", "公支 Nm = 50.80", "旦尼尔 D = 177.15", "特克斯 tex = 19.68"],
  "ref": "英支 Ne=30 → tex=590.5/30=19.68，Nm=1000/19.68=50.80，D=9×19.68=177.15（默认 Ne=1 得 tex 590.50，注入态不重合）"
},
{
  "slug": "textile/convert-yarn",
  "inputs": { "val": "180", "from": "d" },
  "expect": ["旦尼尔 D = 180.00", "特克斯 tex = 20.00", "公支 Nm = 50.00"],
  "ref": "旦尼尔 D=180 → tex=20.00，Nm=50.00，Ne=29.52"
},
{
  "slug": "textile/cost-calculator",
  "inputs": {
    "fabricPrice": "53",
    "fabricUsage": "1.5",
    "fabricWidth": "150",
    "gsm": "200",
    "accessoryCost": "8",
    "laborCost": "15",
    "orderQty": "500",
    "profitMargin": "30",
    "wastage": "5",
    "otherCost": "3"
  },
  "expect": [
    "156.39"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/cutting-1",
  "inputs": {
    "width": "225",
    "length": "10",
    "pieces": "12"
  },
  "expect": [
    "53.33%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/density-8",
  "inputs": {
    "area": "150",
    "stitch": "2",
    "density": "80"
  },
  "expect": [
    "12000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/dye-mixer",
  "inputs": {
    "fabricWeight": "150",
    "concentration": "2",
    "liquorRatio": "20"
  },
  "expect": [
    "150"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "textile/dye-temp",
  "inputs": {
    "dyeType": "vat"
  },
  "expect": [
    "升温至50-60°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/dyeing-time",
  "inputs": {
    "startTemp": "30",
    "targetTemp": "195",
    "rate": "1.5",
    "holdTime": "60",
    "startTemp2": "30",
    "targetTemp2": "130",
    "reqTime": "60",
    "holdTime2": "45"
  },
  "expect": [
    "195"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "textile/estimate-dosage-fabric-qty",
  "inputs": {
    "perLen": "4.5",
    "width": "150",
    "qty": "500",
    "waste": "3",
    "price": "25"
  },
  "expect": [
    "57937.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fabric-converter",
  "inputs": {
    "gsm": "300",
    "width": "150",
    "price": "30",
    "rmb": "30",
    "value": "60"
  },
  "expect": [
    "450.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fukuanpailiaoliyonglv",
  "inputs": {
    "width": "225",
    "effWidth": "140",
    "perLen": "1.2",
    "qty": "100"
  },
  "expect": [
    "270.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/fuliao-lalian-niukou-guige",
  "inputs": {
    "v0": "100",
    "v1": "12",
    "v2": "5"
  },
  "expect": [
    "110.0 cm",
    "10 颗",
    "26 mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/hardness-5",
  "inputs": {
    "weight": "45",
    "temp": "140",
    "pressure": "30",
    "durtime": "15"
  },
  "expect": [ "手感硬度 45" ],
  "ref": "auto-restore"
},
{
  "slug": "textile/kangjingdianbanshuaiqi",
  "inputs": {
    "v0": "1500",
    "vt": "500",
    "t": "2"
  },
  "expect": [
    "1.262"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/length-gsm",
  "inputs": {
    "loopLen": "6",
    "tex": "15",
    "wpc": "15",
    "cpc": "20"
  },
  "expect": [
    "270.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/liquor-ratio",
  "inputs": {
    "fabricWt": "300",
    "ratio": "10",
    "chemAmount": "5000",
    "density": "1.2",
    "fabricWt2": "100",
    "ratio2": "10",
    "owf": "3",
    "concGl": "0"
  },
  "expect": [
    "300"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "textile/pattern-calculator",
  "inputs": {
    "fabricWidth": "225",
    "fabricLength": "200",
    "seamAllowance": "8"
  },
  "expect": [
    "20.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/ratio-20",
  "inputs": {
    "partName": "胸围",
    "baseSize": "150",
    "grade": "4"
  },
  "expect": [
    "142.0cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/shrinkage",
  "inputs": {
    "cutSize": "150",
    "shrinkPct": "5",
    "targetSize": "100",
    "shrinkPct2": "5"
  },
  "expect": [
    "142.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/thread-count",
  "inputs": {
    "value": "48",
    "d": "75",
    "warp": "200",
    "weft": "180",
    "width": "150",
    "wTex": "20",
    "fTex": "20"
  },
  "expect": [
    "12.30"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/yarn-count",
  "inputs": {
    "value": "60"
  },
  "expect": ["Ne\n60\n输入：60 Ne 9.8423 特克斯 tex 98.4233 分特 dtex 88.581 旦尼尔 D 60 英支 Ne 101.6019 公支 Nm 粗细判断： 特细支纱"],
  "ref": "auto-restore"
},
{
  "slug": "textile/zuranyangzhishu-loi",
  "inputs": {
    "loi": "42"
  },
  "expect": [
    "42.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "textile/convert-yarn",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/textile/convert-yarn.html','utf8');var i=h.indexOf('function calc(){');var s=i>=0?h.slice(i,i+320):'';var ok=s.indexOf('!isFinite(v)||v<=0')>=0&&s.indexOf('请输入大于 0 的纱线细度值')>=0;document.getElementById('__tbProbe').textContent='YARNDIV '+(ok?'OK':'BAD');"],
  "expect": ["YARNDIV OK"],
  "ref": "第1343批 除零守卫：纱线细度值为 0/空/非数字时原 calc 走 590.5/0=Infinity，改为有限正数守卫并显示提示后 return。"
},
{
  "slug": "textile/fabric-converter",
  "inputs": {
    "gsm": "0"
  },
  "expect": [
    "请填写克重与幅宽"
  ],
  "ref": "gsm<=0 时清空米重/码价结果（FABRICCLEAR）；旧实现仅 toast，结果仍为上一次 148.5 g/m"
},
{
  "slug": "textile/thread-count",
  "inputs": {
    "value": "0"
  },
  "expect": [
    "请填写大于 0 的支数"
  ],
  "ref": "支数<=0 时清空 Tex/Nm/Ne/D 结果（THREADCLEAR）；旧实现仅 toast，旧换算值残留"
},
{ slug:"textile/pattern-calculator", clicks:["calc();var had=!!window._lastCalc;['fabricWidth','fabricLength','seamAllowance'].forEach(function(id){document.getElementById(id).value='';});calc();document.getElementById('__tbProbe').textContent='B616PAT '+((had&&window._lastCalc===null)?'OK':'BAD last='+JSON.stringify(window._lastCalc));"], expect:["B616PAT OK"], ref:"第1368批空态缓存：默认排料后清空门幅/长度/缝份，calc 提前返回必须把 _lastCalc 置 null，复制与保存历史不得使用上一轮排料。旧实现保留对象 ⇒ BAD。" },
{ slug:"textile/pattern-calculator", inputs:{fabricWidth:"150",fabricLength:"200",seamAllowance:"0"}, expect:["34.7%","含0%缝份","裁片总面积 1.04m²"], ref:"缝份/损耗 0% 合法：默认 5 片裁片总面积 1.04m²、利用率 34.7%；不得回落 8%。" },
{ slug:"textile/thread-count", clicks:["cur='density';renderParams();document.getElementById('warp').value='200';document.getElementById('weft').value='180';document.getElementById('width').value='150';document.getElementById('length').value='10';calc();document.getElementById('__tbProbe').textContent='T861D '+document.querySelector('#result').innerText;"], expect:["T861D","经纱总根数","3,000","纬纱总根数（按 10 m 布长）","18,000","经纬纱总根数","21,000"], ref:"#861 织物密度：纬纱须按布长计数，不能复用幅宽；200/180 根/10cm、幅宽150cm、布长10m → 经3000、纬18000、总21000。旧实现纬纱也按幅宽得2700、总5700。" },
{ slug:"textile/dye-mixer", clicks:["toggleDye('red');document.getElementById('fabricWeight').value='';document.getElementById('concentration').value='2';document.getElementById('liquorRatio').value='20';calc();document.getElementById('__tbProbe').textContent='D861 '+document.getElementById('result').innerText;"], expect:["D861","请填写大于 0 的织物重量","已清除旧配方"], ref:"#861 染料配色：清空织物重量不得回落默认 100g；无效时清配方并重置色块。" },
{ slug:"textile/dye-mixer", clicks:["toggleDye('red');document.getElementById('fabricWeight').value='100';document.getElementById('concentration').value='0';calc();document.getElementById('__tbProbe').textContent='D861B '+document.getElementById('result').innerText;"], expect:["D861B","请填写大于 0 的织物重量、染色浓度与浴比"], ref:"#861 染料配色：浓度 0 不再被 ||2 静默替换，提示且不生成配方。" },
{ slug:"textile/convert-yarn", inputs:{val:"100",from:"nm"}, expect:["公英制关系：英支 Ne = 0.5905 × 公支 Nm","Nm ≈ 1.693 × Ne","英支 Ne = 59.05"], ref:"#861 纱线细度：Nm=100 → Ne=59.05；说明旧写 Ne=1.693×Nm 方向倒置，现改为 Ne=0.5905×Nm。" },
{ slug:"textile/cost-calculator", clicks:["['fabricPrice','fabricUsage','fabricWidth','gsm','accessoryCost','laborCost','orderQty','profitMargin','wastage','otherCost'].forEach(function(id){document.getElementById(id).value='0';});document.getElementById('fabricPrice').value='35';document.getElementById('fabricUsage').value='1.5';document.getElementById('orderQty').value='500';document.getElementById('profitMargin').value='100';calc();document.getElementById('__tbProbe').textContent='C861 '+document.getElementById('result').innerText;"], expect:["C861","利润率须在 0–99.9% 之间","无意义"], ref:"#861 服装成本：利润率 100% 时售价公式除零，旧实现输出 Infinity/极大值；现拦截并提示。" },
{ slug:"textile/cost-calculator", clicks:["['fabricPrice','fabricUsage','fabricWidth','gsm','accessoryCost','laborCost','orderQty','profitMargin','wastage','otherCost'].forEach(function(id){document.getElementById('id');});document.getElementById('fabricPrice').value='35';document.getElementById('fabricUsage').value='1.5';document.getElementById('accessoryCost').value='0';document.getElementById('laborCost').value='0';document.getElementById('otherCost').value='0';document.getElementById('wastage').value='0';document.getElementById('orderQty').value='0';document.getElementById('profitMargin').value='30';document.getElementById('fabricWidth').value='150';document.getElementById('gsm').value='200';calc();document.getElementById('__tbProbe').textContent='C861B '+document.getElementById('result').innerText;"], expect:["C861B","订单数量须为不小于 1 的整数"], ref:"#861 服装成本：订单数量 0 不再静默替换为 1，提示且不输出 1 件汇总。" },
{ slug:"textile/cost-calculator", clicks:["['fabricPrice','fabricUsage','fabricWidth','gsm','accessoryCost','laborCost','orderQty','profitMargin','wastage','otherCost'].forEach(function(id){document.getElementById('id');});['fabricPrice','fabricUsage','gsm','accessoryCost','laborCost','otherCost','wastage'].forEach(function(id){document.getElementById(id).value='0';});document.getElementById('fabricWidth').value='150';document.getElementById('orderQty').value='500';document.getElementById('profitMargin').value='30';calc();document.getElementById('__tbProbe').textContent='C861C '+document.getElementById('result').innerText;"], expect:["C861C","单件总成本为 0","无意义"], ref:"#861 服装成本：零成本时旧实现成本占比 0/0 显示 NaN；现提示总成本为 0 且不输出占比。" },
{ slug:"textile/calc-gsm", clicks:["currentTab='yarn';document.getElementById('yWarpCount').value='40';document.getElementById('yWeftCount').value='40';document.getElementById('yEPC').value='25';document.getElementById('yPPC').value='22';document.getElementById('yWarpCrimp').value='';document.getElementById('yWeftCrimp').value='4';document.getElementById('yFabricWidth').value='150';calcYarn();document.getElementById('__tbProbe').textContent='G861 '+document.getElementById('yRes').innerText;"], expect:["G861","经向缩率须填写 0–100%","已清除旧结果"], ref:"#861 织物克重：纱支推算的空缩率旧实现按 0 计算；现区分缺失与合法 0，提示且清结果。" },
{ slug:"textile/calc-gsm", clicks:["currentTab='yarn';document.getElementById('yWarpCount').value='40';document.getElementById('yWeftCount').value='40';document.getElementById('yEPC').value='25';document.getElementById('yPPC').value='22';document.getElementById('yWarpCrimp').value='5';document.getElementById('yWeftCrimp').value='-200';document.getElementById('yFabricWidth').value='150';calcYarn();document.getElementById('__tbProbe').textContent='G861B '+document.getElementById('yRes').innerText;"], expect:["G861B","纬向缩率须填写 0–100%"], ref:"#861 织物克重：纬向缩率 -200% 旧实现代入负值可产负克重；现范围校验拦截。" }
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

  console.log("==== textile calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
