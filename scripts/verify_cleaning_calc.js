#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cleaning/area-hours",
  "inputs": {
    "area": "250",
    "staff": "3",
    "dirt": "1.6"
  },
  "expect": [
    "66.7 小时",
    "4000 分钟",
    "22.2 h"
  ],
  "ref": "去默认化：日常保洁 10 分钟/㎡ × 250㎡ × 1.6（重度脏污系数）= 4000 分钟 = 66.67 小时；3 人 → 22.2 h/人；工期 4000/60/8 = 8.33 天。默认 100㎡/2人/1.0 → 1000 分钟、16.7 小时、8.3 h/人、2.1 天，不含上述任一条（注意默认的「8.3 h」与注入的「8.3 天」仅单位不同，故刻意避开工期串）"
},
{
  "slug": "cleaning/dilution-ratio",
  "inputs": {
    "totalVolP": "5",
    "conc": "50"
  },
  "expect": [
    "98 ml",
    "4902 ml",
    "1.96%"
  ],
  "ref": "去默认化：预设模式（1:100 日常地面清洁）下 原液 = 总量/(1 + N·conc/100) = 5/(1 + 100×0.5) = 0.098039 L = 98 ml；加水 5000−98 = 4902 ml；原液占比 1.96%。默认 10 L / conc 100 → 99 ml、9901 ml、0.99%。**ratioN 在预设模式下是无效键**（ratioN 取自 PRESETS；切自定义需 setMode，而 setMode 已被 harness 的 DESTRUCTIVE ^set[A-Z] 排除），故不再注入它"
},
{
  "slug": "cleaning/supply-usage",
  "inputs": {
    "area": "500",
    "period": "60",
    "safety": "14",
    "freq": "2"
  },
  "expect": [
    "150000 ml",
    "185000 ml",
    "370 瓶（500ml/瓶）"
  ],
  "ref": "去默认化：全能清洁剂 2.5 ml/㎡ × 500㎡ × 2 次/天 × 60 天 = 150000 ml；安全库存 14 天 → 150000×(1+14/60) = 185000 ml；÷500ml = 370 瓶。默认 200㎡/1 次/30 天/7 天 → 15000 ml、18500 ml、37 瓶，均不含上述串"
},
{
  "slug": "cleaning/appliance-cycle",
  "clicks": [
    "localStorage.getItem=function(k){return k===STORAGE_KEY?JSON.stringify({fridge:'2099-01-01',washer:'2099-01-01'}):null;};loadStorage();render();"
  ],
  "expect": [
    "✅ 2 项 状态正常，无需清洁"
  ],
  "ref": "覆写 localStorage 使 fridge/washer 记录为未来日期（2099-01-01）→ loadStorage() 重读 records、render() 渲染：「✅ 2 项 状态正常，无需清洁」（默认 14 项全部已到周期、无此串）。回退默认（records 空）→ 仍 14 项已到周期，不命中。"
},
{
  "slug": "cleaning/checker-10",
  "inputs": {
    "a0_0": "5", "a0_1": "5", "a0_2": "5", "a0_3": "5",
    "a1_0": "4", "a1_1": "4", "a1_2": "4", "a1_3": "4", "a1_4": "4",
    "a2_0": "3", "a2_1": "3", "a2_2": "3",
    "a3_0": "2", "a3_1": "2", "a3_2": "2", "a3_3": "2"
  },
  "expect": [
    "70 / 100 分",
    "20/20",
    "9/15",
    "8/20"
  ],
  "ref": "去默认化（16 项打分全部非默认）：地面 4 项全 5 → 20/20（均分 5.0）、卫生间 5 项全 4 → 20/25（4.0）、玻璃 3 项全 3 → 9/15（3.0）、公共设施 4 项全 2 → 8/20（2.0）⇒ 总均分 (5+4+3+2)/4 = 3.5 → 综合考核分 round(3.5×20) = 70（合格）。默认全 0 → 0 分、0/20、0/25、0/15、0/20。注：select id 由 JS 模板拼接（a{区号}_{项号}），HTML 源码里无字面 id ⇒ 注入有效但 discriminate 无法解析默认值、该例被判跳过，判别力已用同口径双态 dump 人工确认（默认态不含 20/20、9/15、8/20）"
},
{
  "slug": "cleaning/checker-9",
  "inputs": {
    "m0_0": "2", "m0_1": "2", "m0_2": "2", "m0_3": "2", "m0_4": "2",
    "m1_0": "1", "m1_1": "1", "m1_2": "1", "m1_3": "1", "m1_4": "1",
    "m2_0": "0", "m2_1": "0", "m2_2": "0", "m2_3": "0", "m2_4": "0"
  },
  "expect": [
    "10/10",
    "5/10",
    "待完善项（10）"
  ],
  "ref": "去默认化（15 项评级全部非默认）：一、SOP 5 项全「已制定并执行」→ 10/10（100%）；二、操作规范 5 项全「已制定待完善」→ 5/10（50%）；三、检查标准 5 项全「未制定」→ 0/10（0%）⇒ 总得分 15/30 = 50%（需重建），待完善项 = 5 待完善 + 5 未制定 = 10 项。默认全 0 → 0/10 ×3、待完善项（15），不含上述串。注：id 由 JS 模板拼接（m{模块}_{项}），判别器无法解析 ⇒ 判别力已用同口径双态 dump 人工确认"
},
{
  "slug": "cleaning/cycle-20",
  "inputs": {
    "carpetType": "synthetic"
  },
  "expect": [
    "synthetic"
  ],
  "ref": "auto-restore：**已知弱断言，暂无法加固** —— 页面需先点「添加地毯」才有可计算内容（默认输出「暂无地毯，请先添加」「暂无维护记录」），harness 无 clicks 字段 ⇒ 换 carpetType 只改变 select 的 value 回显，页面计算结果不变。本例 expect 锚的正是该回显，属 §10.5 记录的「输入值回显型」断言，仅能守住页面初始化渲染不报错"
},
{
  "slug": "cleaning/staff-schedule",
  "inputs": {
    "newName": "李四",
    "newArea": "800"
  },
  "expect": [
    "800㎡ 总负责面积",
    "1 保洁人数"
  ],
  "ref": "去默认化：注入姓名/面积后由 harness 兜底调用 addStaff()（页面无 calc 入口、harness 无 clicks 字段）→ 1 人、负责 800㎡、人均 800㎡、默认排班 6 个工作日 × 8h = 48h。默认态为「暂无人员，请添加或载入示例」+「0 保洁人数」「0㎡ 总负责面积」，不含上述串。注：本例依赖兜底副作用（addStaff/toggleShift 均被尝试调用），属 §7.1 记录的兜底依赖型用例，排班格子顺序不宜作为 expect"
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
  console.log("==== cleaning calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
