#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "security/anti-fraud-cards",
  "inputs": {
    "catFilter": "telecom"
  },
  "expect": [
    "telecom"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/data-erase-simulator",
  "inputs": {
    "blockSize": "24"
  },
  "expect": [
    "24"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/detector-45",
  "inputs": {
    "resistTime": "23",
    "steelThick": "1.2",
    "lockTime": "5",
    "envScore": "8"
  },
  "expect": [
    "23分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/earthquake-escape",
  "inputs": {
    "floorSelect": "mid"
  },
  "expect": [
    "mid"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/emergency-contacts",
  "inputs": {
    "customName": "测试王医生",
    "customPhone": "13800000000"
  },
  "clicks": [
    "addCustom()"
  ],
  "expect": [
    "测试王医生"
  ],
  "ref": "去默认化（原 expect「400-161-9995」＝核心应急联系人卡片恒显号码，注入失败仍命中 → 逃生项）：inputs 填自定义联系人姓名/电话后 clicks 调 addCustom()（window 全局，读输入框并写 localStorage+渲染 customList），customList 新增「测试王医生 / 13800000000」；默认 customList 为「暂无自定义联系人」，不含「测试王医生」，注入失败即不命中。"
},
{
  "slug": "security/first-aid-kit",
  "inputs": {},
  "clicks": [
    "selectScene('outdoor');generateList();"
  ],
  "expect": [
    "蛇药片"
  ],
  "ref": "clicks 注入：本页逻辑包在 IIFE 里，但把入口显式挂到了 window（selectScene / generateList / toggleItem / checkAll / uncheckAll）⇒ pageEval 与 harness 的 globalThis 导出都能调到。注意 selectScene() 只重渲场景卡，物品清单必须再显式 generateList() 才会渲染（少这一步则注入无输出，是本页最易踩的点）。注入后 selectedScene='outdoor'，清单渲染户外专属条目（蛇药片、防中暑药（藿香正气水）、净水片、急救指南卡片等），默认 selectedScene='home' 不产出这些名 ⇒ 零逃生项。旧锚「20片」是家庭包首项数量字面量 ⇒ 判别力 0。"
},
{
  "slug": "security/flood-level",
  "inputs": {
    "depthSlider": "7"
  },
  "expect": [
    "7cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/smoke-alarm-test",
  "inputs": {
    "alarmLocation": "卧室"
  },
  "expect": [
    "卧室"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/typhoon-scale",
  "inputs": {
    "windInput": "45"
  },
  "expect": [
    "162.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/virtual-safe",
  "inputs": {
    "itemContent": ""
  },
  "expect": [
    "请设置一个主密码来创建新的保险箱"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：需 WebCrypto（crypto.subtle）派生密钥 + 主密码解锁，"
     + "harness 无 WebCrypto ⇒ 保险箱列表恒空，注入 itemTitle / itemContent 不改变输出（2026-09-25 实测）。"
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
  console.log("==== security calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
