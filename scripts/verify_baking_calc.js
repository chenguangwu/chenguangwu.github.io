#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // FT-N10：百分比输入不再整表重绘。flour=600、目标 900，水从 65 改为连续键入 12：
  // 断言派生汇总（总百分比 115.5%、面团总重 693g）与「tbody 未被重建」标记。
  "slug": "baking/baker-percentage",
  "inputs": {
    "flourWeight": "600",
    "targetTotal": "900"
  },
  "clicks": [
    "var body=document.getElementById('ingBody');var before=body.innerHTML;document.getElementById('pct-1').value='1';updatePct(1,'1');document.getElementById('pct-1').value='12';updatePct(1,'12');document.getElementById('localUpdateCheck').textContent=(body.innerHTML===before?'LOCAL_UPDATE_OK':'REBUILT');"
  ],
  "expect": [
    "LOCAL_UPDATE_OK",
    "115.5%",
    "693 g"
  ],
  "ref": "独立复算：flour=600、水 12%、盐 2%、酵母 1.5% ⇒ 重量 600/72/12/9g、总百分比 115.5%、面团总重 693g（默认 500/65 为 168.5% / 842.5g，不命中）。连续输入用同一 input 两次调用 updatePct，若仍整表重建则 tbody innerHTML 改变 ⇒ 标记为 REBUILT 而失配。"
},
{
  // 改非默认面粉/目标重量，断言由两者派生的缩放比例与新面粉重量（独立 Python 复算）。
  "slug": "baking/baker-percentage",
  "inputs": {
    "flourWeight": "600",
    "targetTotal": "1000"
  },
  "expect": [
    "缩放比例： ×0.989",
    "新面粉重量： 593.5 g"
  ],
  "ref": "配料表百分比和 totalPct=100+65+2+1.5=168.5；newFlour = 1000/168.5×100 = 593.4718 → fmtNum 取 1 位小数 = 593.5；ratio = 593.4718/600 = 0.98912 → fmtNum 取 3 位小数 = 0.989。回退默认（500/800）→ ×0.95 / 474.8 g，两串均不命中。"
},
{
  "slug": "baking/convert-28",
  "inputs": {
    "flour": "750",
    "pct": "72"
  },
  "expect": [
    "540.0 g",
    "1 : 1.389",
    "1290.00 g"
  ],
  "ref": "非默认输入（默认 500/60）：配料重 = 750 × 72 ÷ 100 = 540 ⇒ 主行「540.0 g」；主料与配料合计 = 750 + 540 = 1290 ⇒ 换算链「1290.00 g」；粉水比例 = 100 ÷ 72 = 1.389 ⇒「1 : 1.389」。默认态为 300.0 g / 800.00 g / 1 : 1.667。"
},
{
  "slug": "baking/convert-temp",
  "inputs": {
    "val": "200",
    "from": "1",
    "to": "2",
    "comp": "17"
  },
  "expect": [
    "392.0 ℉",
    "风炉等效 375.0 ℃"
  ],
  "ref": "200℃→℉: 200×9/5+32=392.0；风炉等效=392−17=375.0℃（风炉比平炉低17℃经验值）。默认 val=180 from=1 to=2 comp=17 → 356.0℉/339.0℃ 不命中"
},
{
  "slug": "baking/dough-hydration",
  "inputs": {
    "flour": "800",
    "water": "400"
  },
  "expect": [
    "极低含水量",
    "紧实干硬，难以揉制 · 适合贝果、椒盐脆饼"
  ],
  "ref": "非默认输入（默认 500/350 ⇒ 70%）：含水量 = 400 ÷ 800 × 100 = 50%（hydVal 显示 50%，但页面静态参考表已含「50%」故不锚）；50 < 56 落 getHydInfo 首分支 ⇒ grade「极低含水量」、desc「紧实干硬，难以揉制 · 适合贝果、椒盐脆饼」（默认 70% 落 <73 的「较高含水量」分支）。"
},
{
  "slug": "baking/fermentation-time",
  "inputs": {
    "baseTime": "40",
    "actualTemp": "17",
    "actualHumidity": "75",
    "fermType": "cold"
  },
  "expect": [
    "100 分钟",
    "修正系数 ×0.4",
    "约 1.7 小时（基准 40 分钟）"
  ],
  "ref": "非默认输入（默认 60/24/70/yeast）：fermType=cold ⇒ q10 = 2.5；tempFactor = 2.5^((17−27)/10) = 2.5^(−1) = 0.4；humFactor = 1 + (75−75)×0.008 = 1；totalFactor = 0.4 ⇒ 实际时长 = 40 ÷ 0.4 = 100 分钟；小时 = 100/60 = 1.667 ⇒ 显示「约 1.7 小时（基准 40 分钟）」；系数徽标「修正系数 ×0.4」。默认态为 76.9 分钟 / ×0.8。"
},
{
  "slug": "baking/fermentation-time",
  "inputs": {
    "yeastAmount": "30",
    "yeastType": "active"
  },
  "expect": [
    "鲜酵母 90.00 g",
    "即发酵母 22.50 g"
  ],
  "ref": "2026-10-27 新增「🍞 酵母鲜干换算」模块：注入 yeastAmount=30、yeastType=active（活性干酵母）→ fresh = 30×3 = 90.00 g、instant = 30×0.75 = 22.50 g。默认态 yeastAmount=15、yeastType=fresh ⇒ 鲜酵母 15.00 g、即发酵母 3.75 g，两条锚均不命中 ⇒ 强判别、零逃生。换算比 鲜:活性干:即发 ≈ 3:1:0.75 为经验值，页面已注明品牌活性差异以包装标注为准。"
},
{
  "slug": "baking/mold-volume",
  "clicks": [
    "document.getElementById('fromD').value='15';document.getElementById('fromH').value='4';document.getElementById('toD').value='20';document.getElementById('toH').value='10';calc()"
  ],
  "expect": [
    "× 4.44",
    "707 原模具容积 (ml)",
    "3142 目标模具容积 (ml)",
    "2042 建议填充量 (ml)"
  ],
  "ref": "**坏用例重写**（原 inputs 键是生成器模板串残留 `\"'+side+'D\"`、expect 只有静态标签词「高度」，页面无此 id ⇒ 判别器与 selfcheck 双双漏判）。该页静态无任何 input，控件由 `renderInputs(side)` 运行期拼 innerHTML 生成、`calcVolume(side)` 再按 id 读取 ⇒ 只能用 clicks 在同一次求值内赋值。两模具均为默认 round 形状：from D=15、H=4 ⇒ 容积 = π×(15/2)²×4 = 706.86 ml ⇒ fmtNum 取整「707」；to D=20、H=10 ⇒ π×10²×10 = 3141.59 ml ⇒「3142」；缩放比 = 3141.59 ÷ 706.86 = 4.4445 ⇒ 显示「× 4.44」；建议填充量 = 3141.59 × 0.65 = 2042.03 ⇒「2042」（ratio > 1.1 落「目标模具更大」分支）。未注入时 harness 读不到运行期生成的 D ⇒ 体积 0 ⇒ 渲染「请输入有效的模具尺寸」，四串均不含。"
},
{
  // FT-N12 放大分支：ratio 1.494 ⇒ 文案必须是「调整至 149%（即增加 49%）」，
  // 而非旧实现误写的「需增加 149%」。
  "slug": "baking/mold-volume",
  "clicks": [
    "applyMoldPreset('toast')"
  ],
  "expect": [
    "调整至原配方的 149%",
    "增加 49%"
  ],
  "ref": "独立复算：吐司盒 22×12×7=1848 ml，6寸圆模 π×7.5²×7=1236.98 ml ⇒ ratio=1848/1236.98=1.49399 ⇒ fmtNum「1.49」，ratio×100=149.4→「149」，增加=(ratio−1)×100=49.4→「49」。默认态 6寸→8寸 ratio=1.78 输出 178%/78%，两串均不命中。"
},
{
  // FT-N12 缩小分支口径：ratio 0.884 ⇒「调整至 88%」，与放大分支统一为「调整至」。
  "slug": "baking/mold-volume",
  "clicks": [
    "applyMoldPreset('round2square')"
  ],
  "expect": [
    "调整至原配方的 88%"
  ],
  "ref": "独立复算：圆模 D18×H6 ⇒ π×9²×6=1526.81 ml；方模 15×15×6=1350 ml ⇒ ratio=1350/1526.81=0.88420 ⇒ ratio×100=88.42→「88」（ratio<0.9 落「目标模具更小」分支）。默认态 ratio=1.78 输出 178%，不命中。"
},
{
  // 原 expect「请输入有效温度」由零参兜底调用 convertTemp() 触发（两个温度框皆空）→ 与注入无关的逃生项。
  // 改断言双向换算结果 + 按摄氏值分档的标签；回退默认（tempC=180、tempF 空）会落到错误分支，故必失配。
  "slug": "baking/oven-temp",
  "inputs": {
    "tempC": "160",
    "tempF": "320"
  },
  "expect": [
    "160°C = 320°F",
    "中低温 - 蛋糕、饼干"
  ],
  "ref": "160°C → f = 160×9/5+32 = 320°F；getTempLabel(160)：140 ≤ c < 170 → 「中低温 - 蛋糕、饼干」。回退默认 tempC=180 → 「180°C = 356°F」+「中温 - 面包、披萨（常用）」，且 tempF 变空后落到「请输入有效温度」分支，两串均不命中。"
},
{
  "slug": "baking/recipe-scaler",
  "inputs": {
    "factor": "4.5",
    "rows": "面粉=200g\\n糖=100g\\n鸡蛋=2个\\n牛奶=150ml\\n黄油=50g"
  },
  "expect": [
    "900g"
  ],
  "ref": "auto-restore"
},
{
  // 5 行配料真实换行 + 非默认倍数：任一行解析失败即缺后续锚点。
  "slug": "baking/recipe-scaler",
  "inputs": {
    "factor": "2.5",
    "rows": "面粉=240g\n糖=90g\n鸡蛋=3个\n牛奶=180ml\n黄油=60g"
  },
  "expect": [
    "225g",
    "7.5个",
    "450ml"
  ],
  "ref": "5 行配料 ×2.5：面粉 240→600g、糖 90→225g、鸡蛋 3→7.5个、牛奶 180→450ml、黄油 60→150g。锚点取后 3 行（默认/单行解析均不产生），避免首行 600g 在「只解析 1 行」缺陷态下仍命中；**不再锚「150g」** —— 默认样例 ×1.5 的糖 100g 同样得 150g，注入失败时仍 PASS（逃生）。"
},
{
  // 兼容用户粘贴的字面量 \\n：解析前应归一为真实换行。
  "slug": "baking/recipe-scaler",
  "inputs": {
    "factor": "2",
    "rows": "面粉=240g\\n糖=90g\\n鸡蛋=3个\\n牛奶=180ml\\n黄油=60g"
  },
  "expect": [
    "180g",
    "6个",
    "360ml",
    "120g"
  ],
  "ref": "字面量 \\n 分隔的 5 行 ×2：面粉 240→480g、糖 90→180g、鸡蛋 3→6个、牛奶 180→360ml、黄油 60→120g。后 4 行锚点区分「字面 \\n 未归一 ⇒ 整段只解析首行」的缺陷态。"
}
,
{
  "slug": "baking/recipe-scaler",
  "inputs": {"factor": ""},
  "clicks": ["calcTool()"],
  "expect": ["请填写缩放倍数后再计算。"],
  "ref": "空倍数：先判存在性（trim 后为空），不再走 +''||0，直接提示、不渲染「×0」配方；默认 1.5 ⇒ 正常配方，不命中。"
},
{
  "slug": "baking/recipe-scaler",
  "inputs": {"factor": "2", "rows": ""},
  "clicks": ["calcTool()"],
  "expect": ["请填写原料清单"],
  "ref": "空原料清单：倍数有效但 rows 为空 ⇒ 提示先填清单，不输出空配方；默认 rows 含 4 行 ⇒ 正常配方，不命中。"
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

  console.log("==== baking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
