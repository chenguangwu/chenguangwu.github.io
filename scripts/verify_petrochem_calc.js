#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "53",
    "sgVal": "0.85"
  },
  "expect": [
    "766.1707"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "-130",
    "sgVal": "0.85"
  },
  "expect": [
    "超出原油常见范围"
  ],
  "ref": "修复前 API=-130 输出密度 94.24 g/cm³ 且标「超重质」无警示；现保留计算但给出范围提示"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "7500",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "700",
    "flow2": "5000",
    "residence": "30",
    "density2": "850",
    "bulkDensity2": "700"
  },
  "expect": [
    "088.24"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": { "feed": "1500", "prodCount": "2" },
  "clicks": ["buildList();document.getElementById('prod1').value='塔顶油';document.getElementById('prod2').value='塔底油';document.getElementById('amt1').value='1000';document.getElementById('amt2').value='400';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='DIST '+((h.indexOf('未闭合差额')>=0&&h.indexOf('1,400')>=0&&h.indexOf('100</strong>')>=0)?'OK':'BAD '+h);"],
  "expect": [ "DIST OK" ],
  "ref": "第1117批：产量留空不再按 0；进料 1500、产品 1000+400 ⇒ 总产品 1400、未闭合差额 100（6.67%），旧版显示「损失/残液 100」并称真实损失。"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": { "feed": "1000", "prodCount": "1" },
  "clicks": ["buildList();document.getElementById('amt1').value='1050';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='DISTX '+((h.indexOf('物料平衡超额')>=0&&h.indexOf('50 吨')>=0&&h.indexOf('-50')<0)?'OK':'BAD '+h);"],
  "expect": [ "DISTX OK" ],
  "ref": "第1117批：产品超进料显示「物料平衡超额 50」，不再输出负损失/负残液。"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": { "feed": "1000", "prodCount": "2" },
  "clicks": ["buildList();document.getElementById('amt1').value='600';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='DISTM '+((h.indexOf('未填写产量')>=0&&h.indexOf('总收率')<0)?'OK':'BAD '+h);"],
  "expect": [ "DISTM OK" ],
  "ref": "第1117批：一项产量留空即停止平衡计算并列明缺项，不把未知当 0。"
},
{
  "slug": "petrochem/distillation-yield",
  "inputs": { "feed": "1000", "prodCount": "1" },
  "clicks": ["buildList();document.getElementById('prod1').value='<img src=x onerror=alert(1)>';document.getElementById('amt1').value='900';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='DISTE '+(h.indexOf('&lt;img')>=0&&h.indexOf('<img')<0?'OK':'BAD '+h);"],
  "expect": [ "DISTE OK" ],
  "ref": "第1117批：产品名按纯文本转义，不把尖括号/事件属性拼进 innerHTML。"
},
{
  "slug": "petrochem/pipe-pressure",
  "inputs": {
    "flow": "100",
    "diameter": "200",
    "length": "500",
    "density": "900",
    "viscosity": "50",
    "roughness": "0.1"
  },
  "expect": [
    "过渡区压降范围",
    "17.6839 – 38.8389"
  ],
  "ref": "第1117批：Re 3183 过渡区给出层流端—湍流端范围，单点 f=0.0442 仅作湍流端参考。"
},
{
  "slug": "petrochem/pipe-pressure",
  "inputs": {
    "flow": "75",
    "diameter": "100",
    "length": "500",
    "density": "850",
    "viscosity": "5",
    "roughness": "-0.1"
  },
  "expect": [
    "粗糙度须填写 ≥0 的有限数值"
  ],
  "ref": "第1117批：粗糙度负数不再按 -0.0001 m 参与计算，直接提示。"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "7500",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "700",
    "voidage": "0.4",
    "actualFlow": "7.5"
  },
  "clicks": ["calcLsv();document.getElementById('__tbProbe').textContent='CATRES '+document.getElementById('actualResNote').innerText;"],
  "expect": ["空隙停留时间"],
  "ref": "第1117批：补充空隙率与工况流量后估算真实空隙停留时间；不提供时只显示名义空间时间。"
},
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "35",
    "sgVal": "0.85"
  },
  "clicks": ["document.getElementById('waterTemp').value='0';calcApi();"],
  "expect": ["水密度须为有限正值"],
  "ref": "第1117批：水密度为 0 时清除结果并提示，不再用 0 乘出 0 密度。"
},
{
  "slug": "petrochem/api-gravity",
  "inputs": {
    "apiVal": "35",
    "sgVal": "0.85"
  },
  "clicks": ["document.getElementById('waterTemp').value='0.998';calcApi();"],
  "expect": ["0.8482", "0.998 g/cm³"],
  "ref": "第1117批：API 35、SG 0.8498 在 20℃ 水密度 0.998 下密度 0.8482 g/cm³，并标明基准与未做温度修正。"
},
{
  "slug": "petrochem/pipe-pressure",
  "inputs": {
    "flow": "75",
    "diameter": "100",
    "length": "500",
    "density": "850",
    "viscosity": "5",
    "roughness": "0.045"
  },
  "expect": [
    "093.9005"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/tank-capacity",
  "inputs": {
    "diameter": "15",
    "length": "12",
    "density": "850",
    "level": "8",
    "safety": "90"
  },
  "expect": [
    "120.58"
  ],
  "ref": "auto-restore"
},
{
  "slug": "petrochem/catalyst-calc",
  "inputs": {
    "flow": "5000",
    "lsv": "2",
    "density": "850",
    "bulkDensity": "0"
  },
  "expect": [
    "请输入正的流量、空速、进料密度与催化剂堆积密度"
  ],
  "ref": "修复前堆积密度清空/0 直接按 0 得装量 0 kg（负堆密度还得负质量）；现与流量/空速/进料密度一并校验并提示补全。默认 700 不出现该文案。"
},
{
  "slug": "petrochem/catalyst-calc",
  "clicks": [
    "switchMode('time');document.getElementById('__tbProbe').textContent='CATSW='+(String(document.getElementById('resultTime').innerHTML).indexOf('催化剂体积')>=0?'Y':'N');"
  ],
  "expect": [
    "CATSW=Y"
  ],
  "ref": "修复前切到停留时间模式只切面板、未改输入前 resultTime 为空；现 switchMode 立即调用 calcTime()，默认 5000 kg/h、30 s、850 kg/m³、700 kg/m³ ⇒ 体积流量 5.88 m³/h、装量 0.049 m³ / 34.31 kg。默认态无该探针串。"
},
{
  "slug": "petrochem/tank-capacity",
  "clicks": ["document.getElementById('safety').value='0';calc();var h=String(document.getElementById('result').innerHTML);var ok=h.indexOf('请检查输入')>=0&&h.indexOf('安全装料系数')>=0&&h.indexOf('安全容量')<0;document.getElementById('__tbProbe').textContent='TANKSAFE '+(ok?'OK':'BAD '+h);"],
  "expect": ["TANKSAFE OK"],
  "ref": "第1094批 I8：safety=0 旧版 parseFloat||0 得 safeVol=0、装料率>0 即报「超出安全液位」并显示安全容量 0；修复后 1–100 范围校验拦截，字段级提示且不出容量结论。哨兵锚错误与「安全容量」消失，旧版必红。"
},
{
  "slug": "petrochem/tank-capacity",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/petrochem/tank-capacity.html','utf8');var ok=h.indexOf('safety<1||safety>100')>=0&&h.indexOf('density<=0')>=0&&h.indexOf('level>maxLevel')>=0&&h.indexOf('var maxLevel=')>=0;document.getElementById('__tbProbe').textContent='TANKFIX '+(ok?'OK':'BAD');"],
  "expect": ["TANKFIX OK"],
  "ref": "第1094批 I8 源码形态：安全系数 1–100、密度>0、液位 0..D（立式 0..L）三项前置守卫必须存在；旧版仅 Math.max/min 截断且结果文本打印原始越界液位。"
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

  console.log("==== petrochem calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
