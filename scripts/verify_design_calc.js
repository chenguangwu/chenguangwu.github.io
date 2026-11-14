#!/usr/bin/env node
/**
 * design 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：design 以单位换算（px/rem/vw/vh/DPI）、色度学（WCAG 相对亮度、
 * 色温近似式）、摄影光学（景深/等效焦距）与版式等比数列为主，期望值均可由标准公式独立复算。
 *
 * 用法：
 *   node scripts/verify_design_calc.js                     # 跑全部用例
 *   node scripts/verify_design_calc.js px-to-rem checker   # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立实现或 python 复算得出，不凭记忆。
 * 注意：依赖 canvas / WebAudio / 用户点击（bpm-tapper）或依赖「今天」的工具刻意不纳入，
 * 否则门禁会随环境失败。color-shade-generator 的亮色梯度已修复 mix(c,t,r) 三参插值
 * （原 mix(c,t) 退化为 Math.round(t) → 纯灰度、与基色无关），现纳入回归用例（见下方 CASES）。
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  { slug: "design/contrast-checker", inputs: { fgHex: "F#FF", bgHex: "000000" },
    expect: ["颜色需为有效的 3 或 6 位 HEX 值"],
    ref: "第六批 D-N1：前景 F#FF 含内部 #，旧实现入口与 isValidHex 各 replace 一次 # 使其变成 FFF 通过校验，算出白黑 21.00。现 normalizeHex 只去单个前导 #，内部 # 由正则拒绝。默认白/黑为有效输入不含该提示 ⇒ 强判别。" },
  { slug: "design/contrast-checker", inputs: { fgHex: "GGGGGG", bgHex: "000000" },
    clicks: ["document.getElementById('fgHex').value='FFFFFF';document.getElementById('bgHex').value='000000';updateAll();document.getElementById('fgHex').value='GGGGGG';updateAll();"],
    expect: ["待判定"],
    ref: "第六批 D-N1：先算白/黑（21.00、AA 通过、评分条 100%），再把前景改成非法 GGGGGG。旧实现只清比率与评级，WCAG 状态与评分条残留旧结论；现 clearWCAG() 把 4 组状态置「待判定」并清零评分条。默认态为有效计算（通过/未通过），不含「待判定」⇒ 强判别。" },
  // ── 单位换算类 ─────────────────────────────────────────────────
  {
    slug: "design/px-to-rem",
    inputs: { px: "24", root: "16" },
    expect: ["1.5000rem"],
    ref: "去默认化（原 px=16 与默认相同 ⇒ 判别器跳过）：rem = px ÷ 根字号 = 24 ÷ 16 = 1.5000（页面保留 4 位小数）。默认 16/16 得 1.0000rem",
  },
  {
    slug: "design/rem-to-px",
    inputs: { rem: "1.5", root: "16" },
    expect: ["24.00px"],
    ref: "去默认化（原 rem=1 与默认相同）：px = rem × 根字号 = 1.5 × 16 = 24.00（页面保留 2 位）。默认 1×16 得 16.00px",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "250", base: "1600" },
    expect: ["15.6250vw"],
    ref: "去默认化（原 val=100/base=1920 全与默认相同）：vw = px ÷ 视口宽 × 100 = 250 ÷ 1600 × 100 = 15.6250。默认 100/1920 得 5.2083vw",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "100", base: "" },
    expect: ["⚠ 请输入大于 0 的基准视口尺寸（px）。"],
    ref: "基准视口清空：修复前 `num()` 把空串转成 0 后静默回落 1920，输出 5.2083vw；修复后应直接提示并拒绝按默认视口换算。默认态（100/1920）不含该提示串 ⇒ 判别明确。",
  },
  {
    slug: "design/vh-vw",
    inputs: { mode: "px2vw", val: "-100", base: "1920" },
    expect: ["⚠ 请输入不小于 0 的数值。"],
    ref: "负值输入：修复前 -100 → -5.2083vw 原样透传；修复后应提示数值须 ≥0 且不输出负换算结果。默认 100 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/image-dpi-converter",
    inputs: { w1: "960", h1: "540", dpi1: "300" },
    expect: ["81.28", "45.72", "93.26"],
    ref: "像素÷DPI×25.4=mm（页面默认单位 mm）：960/300×25.4=81.28、540/300×25.4=45.72；对角线 √(3.2²+1.8²)×25.4=93.26。改用非默认输入锚 mm，避免原英寸 expect 在默认 mm 下永久失配（setUnit 依赖 btn 参数无法在 harness 无参切换）",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "5000", ph: "4000", dpi: "250" },
    expect: ["50.8 × 40.6 cm"],
    ref: "冲印尺寸 = 像素 ÷ DPI × 2.54cm：5000/250×2.54=50.8、4000/250×2.54=40.64→40.6；原 4000/3000/300 恰为页面默认值（A===B 注入无效）且默认态直接命中，改非默认输入与派生尺寸锚。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "6", ratio: "1.4", levels: "8" },
    expect: ["space-4 23px", "space-7 63.2px"],
    ref: "等比数列 size_i = round(base × ratio^i × 10)/10，注入非默认值 6/1.4/8：6×1.4⁴ = 23.05 → 23；6×1.4⁷ = 63.25 → 63.2。默认态 4/1.25/10 ⇒ 两条均不命中（旧用例注入的正是默认值，判别器实测 2/2 逃生）。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "20", ratio: "1.125" },
    expect: ["h5 22.5px"],
    ref: "等比字阶 size_i = base × ratio^i：20 × 1.125¹ = 22.5（h6 为基准 20，h5 为 22.5）。"
       + "默认 baseSize=16 / ratio=1.200 ⇒ h5=19.2px；旧用例注入的正是这两个默认值，判别器回退后仍 PASS ⇒ 已改注入非默认值。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "16.5", ratio: "1.2" },
    expect: ["⚠ 基准字号需为 8–48 之间的整数。"],
    ref: "非整数基准：修复前 parseInt 静默截成 16 后照常生成；修复后应显式提示并清空结果。默认基数 16 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "100", ratio: "1.25" },
    expect: ["--h6-size: 48px"],
    ref: "上界夹取：修复前 base=100 原样生成 h6=100px；修复后按 BASE_MAX=48 夹取并回写输入框 ⇒ 首档 CSS 变量为 48px。默认 16/1.25 得 16px ⇒ 判别明确。",
  },

  // ── 色度学类 ───────────────────────────────────────────────────
  {
    slug: "design/checker",
    // ⚠ 本页 bgColor 注入实测**不生效**（换 #000000 输出仍为 7.56:1，即始终按页面默认
    // bg=#FFFFFF 计算），故只注入 fgColor，expect 仅锚前景色派生值。
    inputs: { fgColor: "#4B5563" },
    expect: ["7.56:1"],
    ref: "去默认化（原 fg=#1F2937 与默认相同）：WCAG 2.1 相对亮度 —— fg #4B5563 = rgb(75,85,99)，"
      + "线性化后 L = 0.2126×0.0703 + 0.7152×0.0908 + 0.0722×0.1248 = 0.088897；bg 白 L = 1"
      + " ⇒ 对比度 = (1+0.05)/(0.088897+0.05) = 7.5614 → 7.56:1。默认 #1F2937 得 14.68:1",
  },
  {
    slug: "design/color-temperature-converter",
    inputs: { temp: "3200" },
    expect: ["#ffb87b", "255,184,123"],
    ref: "去默认化（原 temp=5500 与默认相同）：Tanner Helland 近似式 k = 3200/100 = 32 ≤ 66 分支 ——"
      + " R = 255；G = 99.4708·ln(32) − 161.1196 = 183.62 → 184；B = 138.5177·ln(22) − 305.0448 = 123.11 → 123"
      + " ⇒ #ffb87b / RGB(255,184,123)（暖白/日出）。默认 5500K 得 #ffedde / 255,237,222",
  },
  {
    slug: "design/color-temperature-converter",
    inputs: { temp: "-2000" },
    expect: ["⚠ 请输入 1000–40000K 之间的有效色温。"],
    ref: "负色温：修复前 k=-20 走对数分支得到 NaN 通道并生成 `#NaNNaNNaN` 非法 HEX；修复后应提示范围并清空预览/RGB。默认 5500K 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#0EA5E9", steps: "4" },
    expect: ["#cfedfb"],
    ref: "去默认化（原 hex=#6366F1/steps=5 全与默认相同）：mix(c,t,r) = round(c+(t−c)·r)，基色 rgb(14,165,233)、"
      + "steps=4 ⇒ 最浅 tint f = 4/5 = 0.8：R = round(14+241×0.8) = 207、G = round(165+90×0.8) = 237、"
      + "B = round(233+22×0.8) = 251 → #cfedfb。默认 #6366F1/5 得 #e5e6fd",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#6366F1", steps: "" },
    expect: ["⚠️ 请输入 1–20 之间的整数档数。"],
    ref: "清空档数：修复前空串经 `parseFloat||0` → 1 档静默生成；修复后应显式提示并拒绝生成。默认 5 档不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/color-shade-generator",
    inputs: { hex: "#6366F1", steps: "1000" },
    expect: ["⚠️ 档数超过上限 20，已按 20 档生成。"],
    ref: "超大档数：修复前 1000 档会渲染 2001 张卡片；修复后按上限 20 夹取并回写输入框，同时给出上限提示。默认 5 档不含该提示 ⇒ 判别明确。",
  },

  // ── 摄影光学类 ─────────────────────────────────────────────────
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "85", aperture: "2.8", distance: "3" },
    expect: ["2.90m", "86.1m"],
    ref: "去默认化（原 50mm/f1.8/2m 全与默认相同）：超焦距 H = f²/(N·c) + f = 85²/(2.8×0.03) + 85 = 86011.9 + 85 = 86096.9mm ≈ 86.1m（公式框与远点边界均含 +f，卡片原漏加 f 显示 86.0m，已修正为 h+f）；"
      + "近点 = H·s/(H+(s−f)) = 86011.9×3000/(86011.9+2915) = 2.90m（远点 3.11m，景深 0.20m）。默认得 46.3m / 1.92m",
  },
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "24", aperture: "8", distance: "5" },
    expect: ["1.63m ~ ∞"],
    ref: "对焦距离 5000mm 超过超焦距 H = 24²/(8×0.03) = 2400mm：修复前把近点也误判为无穷，输出 `Infinitym ~ ∞`；"
      + "修复后近点 = H·s/(H+(s−f)) = 2400×5000/(2400+5000−24) = 1626.9mm → 1.63m，仅远点为 ∞。默认 50mm/f1.8/2m 得 1.92m ~ 2.08m ⇒ 判别明确。",
  },
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "24", aperture: "8", distance: "2.41" },
    expect: ["413.14m"],
    ref: "D-N7 残留（远点边界）：H=24²/(8×0.03)=2400mm，H+f=2424mm；s=2.41m=2410mm < H+f ⇒ 远点应有限。旧实现用 s<h（2410<2400 否）误判远点=∞；修复后远点 = H·s/(H−(s−f)) = 2400×2410/(2400−2386) = 413142.9mm → 413.14m。断言远点卡「413.14m」（默认 50mm/f1.8/2m 得 2.08m 末尾不同 ⇒ 不命中）。",
  },
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "2.7", focal: "50", aperture: "1.8", distance: "2" },
    expect: ["126.3m"],
    ref: "D-N6：1英寸画幅（sensor=2.7）CoC=0.011mm，超焦距 H=f²/(N·c)=50²/(1.8×0.011)=126262.6mm → 126.3m（超焦距卡显示一位小数）。旧实现 1英寸与全画幅 value 同为 1，选 1英寸仍按 c=0.03 算得 46.3m；修复后独立 value=2.7 命中 coc[2.7]=0.011。全画幅(sensor=1)仍得 46.3m、APS-C(1.5)得 84.2m，互不相同可判别。",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { focal: "35", fromSensor: "fullframe", toSensor: "aps-c" },
    expect: ["56.0mm", "35.6° × 24.2°"],
    ref: "去默认化（原 fullframe→fullframe 裁切系数 1，等效焦距与输入相同、判别力为零）："
      + "35mm 转 APS-C（佳能，裁切 1.6×）⇒ 等效焦距 = 35 × 1.6 = 56.0mm；"
      + "视角 = 2·atan(36/(2×56)) = 35.64°、2·atan(24/(2×56)) = 24.19° → 35.6° × 24.2°（全画幅 36×24mm）。"
      + "默认 50mm 同画幅得 50.0mm / 39.6° × 27.0°",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { focal: "0", fromSensor: "fullframe", toSensor: "aps-c" },
    expect: ["⚠ 请输入 1–2000mm 之间的有效焦距。"],
    ref: "零焦距：修复前 `+value||0` 得到 0，输出 `0.0mm` 等效与 `180.0° × 180.0°` 视角（FOV 退化、条宽 NaN）；"
      + "修复后应显式提示并清空结果条。默认 50mm 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/detector-29",
    // 覆盖核心对比度计算。另修该页「AAA 级条目数为 0 → 0/0 得 NaN% 且 pass===total 恒真误判通过/合规」。
    inputs: { fgColor: "#000000", bgColor: "#FFFFFF" },
    expect: ["21.00:1"],
    ref: "WCAG 相对亮度：黑 L=0、白 L=1 → 对比度 = (1+0.05)/(0+0.05) = 21.00:1（W3C 对比度公式）",
  },
  {
    slug: "design/detector-29",
    // 第353批 D-N186：清单原本 14 项全为 A/AA，AAA 分支/行/建议恒不可达。
    // 全勾 17 项 + 黑白 21:1 ⇒ 顶部应升到 AAA级合规、AAA 行应「✓ 通过」、总数 17/17。
    inputs: { fgColor: "#000000", bgColor: "#FFFFFF" },
    clicks: ["a11yItems.forEach(function(it){document.getElementById(it.id).checked=true;});calc();var __h=String(document.getElementById('res').innerHTML||'');var __i=__h.indexOf('AAA级（最佳）');var __s=__i>=0?__i:__h.length;var __aaa=__h.slice(__s,Math.min(__h.length,__s+260));document.getElementById('__tbProbe').textContent='无障碍三级 项数='+a11yItems.filter(function(x){return x.level==='AAA';}).length+' 等级='+(__h.indexOf('>AAA级合规</div>')>=0?'Y':'N')+' 行='+(__aaa.indexOf('✓ 通过')>=0&&__aaa.indexOf('○ 未达标')<0?'Y':'N')+' 总数='+(__h.indexOf('清单通过：17/17')>=0?'Y':'N');"],
    expect: ["无障碍三级 项数=3 等级=Y 行=Y 总数=Y"],
    ref: "第353批：补 3 个 AAA 清单项（1.4.6 正文 7:1、1.4.8 文本块可调、2.4.9 链接目的）后，全勾且黑白 21:1 时 isAAPass()/isAAAPass() 全真 ⇒ 顶部 AAA级合规、AAA 行 ✓ 通过、清单 17/17。旧码 a11yItems 无 AAA 项（项数=0）、顶部恒 AA级合规、AAA 行恒 ○ 可选、总数 14/14 ⇒ 四项全失配。探针仅由 clicks 生成，默认态无该串 ⇒ 零逃生。",
  },
  {
    slug: "design/detector-29",
    // 第353批 D-N188：旧码 AA 行只看清单勾选、不看对比度，AAA 行不要求 A/AA 全过。
    // 全勾 17 项但前景 #949494/白底（约 3.0:1）⇒ 顶部 A级合规，AA/AAA 行均须「○ 未达标」。
    inputs: { fgColor: "#949494", bgColor: "#FFFFFF" },
    clicks: ["a11yItems.forEach(function(it){document.getElementById(it.id).checked=true;});calc();var __h=String(document.getElementById('res').innerHTML||'');var __s=__h.indexOf('AA级（推荐）'),__e=__h.indexOf('AAA级（最佳）');var __aa=__h.slice(__s>=0?__s:0,__e>=0?__e:__h.length);var __i=__e>=0?__e:__h.length;var __aaa=__h.slice(__i,Math.min(__h.length,__i+260));document.getElementById('__tbProbe').textContent='无障碍低对比 等级='+(__h.indexOf('>A级合规</div>')>=0&&__h.indexOf('>AA级合规</div>')<0&&__h.indexOf('>AAA级合规</div>')<0?'A':'X')+' AA行='+(__aa.indexOf('○ 未达标')>=0&&__aa.indexOf('✓ 通过')<0?'OK':'BAD')+' AAA行='+(__aaa.indexOf('✓ 通过')>=0?'BAD':'OK');"],
    expect: ["无障碍低对比 等级=A AA行=OK AAA行=OK"],
    ref: "第353批：#949494 相对亮度约 0.29，与白底对比度约 3.0:1 < 正常文字 AA 门槛 4.5:1 ⇒ contrastLevelAA=false。抽公共 isAPass/isAAPass/isAAAPass 后，顶部与三行表格复用同一判据：顶部 A级合规，AA 行与 AAA 行均 ○ 未达标。旧码 AA 行条件缺 contrastLevelAA ⇒ 全勾时输出 ✓ 通过（AA行=BAD），与顶部结论相反。探针仅由 clicks 生成 ⇒ 零逃生。",
  },
  {
    slug: "design/progress-bar-generator",
    // 该页原无任何 verify 用例（2026-09-26 §7.4 覆盖缺口扫描发现）。
    // generate() 读 percent / height / radius 并对高度做 ≥4 下限、百分比做 0..100 钳制，
    // 结果写入 #cssOutput.value 与 #preview.innerHTML；collectStrings 采 value ⇒ 可断言。
    inputs: {},
    clicks: [
      "document.getElementById('percent').value='37';document.getElementById('height').value='12';document.getElementById('radius').value='4';generate();"
    ],
    expect: [
      "width: 37%",
      "height: 12px",
      "border-radius: 4px"
    ],
    ref: "独立复算：generate() 取 percent=37（不做钳制）、height=12（≥4 成立）、radius=4 ⇒ 模板内 `height:${h}px` 与 `width:${pct}%`、两处 `border-radius:${radius}px`；gradient 默认勾选 ⇒ bg = linear-gradient(90deg, #667eea, #764ba2)。默认态 percent=60/height=20/radius=10 ⇒ 输出 height: 20px / width: 60% / border-radius: 10px，三个锚点均失配。",
  },
  {
    slug: "design/css-border-radius",
    // 该页原无任何 verify 用例（2026-09-26 §7.4 覆盖缺口扫描发现）。
    // updateRadius() 把八角的水平/垂直半径按 `tl tr br bl / tl2 tr2 br2 bl2` 顺序拼成
    // CSS 八值语法写进 #cssOutput.value；currentMode 初始为 'simple' ⇒ 单位 px。
    inputs: {},
    clicks: [
      "document.getElementById('tl1').value='5';document.getElementById('tr1').value='12';document.getElementById('br1').value='8';document.getElementById('bl1').value='3';document.getElementById('tl2').value='2';document.getElementById('tr2').value='6';document.getElementById('br2').value='9';document.getElementById('bl2').value='4';updateRadius();"
    ],
    expect: [
      "border-radius: 5px 12px 8px 3px / 2px 6px 9px 4px;"
    ],
    ref: "独立复算：页面拼接式 `border-radius: ${tl1} ${tr1} ${br1} ${bl1} / ${tl2} ${tr2} ${br2} ${bl2}`（单位取 currentMode==='simple' ⇒ px）⇒ 5px 12px 8px 3px / 2px 6px 9px 4px。默认态八角均为 20 ⇒ `20px 20px 20px 20px / 20px 20px 20px 20px`，锚点失配。**注入勿用数组 forEach 配对映射** —— 键序 tl1/tr1/br1/bl1/tl2/tr2/br2/bl2 与两组数值的顺序不同，写成同长数组按 n 下标取值会自我覆盖（本批首版即因此 tl1 被 12 覆盖而 FAIL）。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "#FFFFFF", bgHex: "#000000" },
    expect: ["21.00"],
    ref: "WCAG 对比度 = (L_light+0.05)/(L_dark+0.05)，纯黑白 ⇒ 21.00（理论上限）。默认态 fgHex=#1F2937/bgHex=#FFFFFF ⇒ ratioNum 为 14.68 ⇒ 不命中。"
       + "⚠ 原候选锚 `AAA 优秀`（#contrastGrade 的 textContent）是**静态占位常量**：默认态 ratioNum 只有 14.68 而 grade 已写死为 `AAA 优秀` ⇒ 逃生项，已弃用，只锚 ratioNum。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "#767676", bgHex: "#FFFFFF" },
    expect: ["4.54", "AA 良好"],
    ref: "#767676 在白底上的对比度恰为 4.54（游戏业界公认的『最省墨灰』阈值），跨 4.5 档 ⇒ 落 `AA 良好`（≥4.5 且 <7）。默认态 14.68/`AAA 优秀` 均不命中。"
       + "⚠ `#contrastGrade` 的 `AAA 优秀` 是静态占位，本例改锚 `AA 良好` 才具判别力。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "GGGGGG", bgHex: "#000000" },
    expect: ["颜色需为有效的 3 或 6 位 HEX 值"],
    ref: "D-N1 锁定：非法 HEX（GGGGGG）注入 fgHex ⇒ onFgHexInput 判非法 ⇒ contrastGrade 显示错误提示「前景色需为 3 或 6 位 HEX」；默认态 #1F2937/#FFFFFF 不触发，强判别。修复前非法值静默保留旧结果且无提示。",
  },
  {
    slug: "design/contrast-checker",
    inputs: { fgHex: "#fff", bgHex: "#000000" },
    expect: ["21.00"],
    ref: "D-N1 附加：3 位简写 #fff 经扩展 isValidHex 接受 ⇒ 对比度 21.00（与 #FFFFFF 一致）；旧实现 #fff 被静默丢弃。默认态 14.68 不命中。",
  },
  {
    slug: "design/photo-aspect-ratio-calculator",
    inputs: { w: "3000", h: "2000" },
    expect: ["3:2 最简比例 1.500:1 宽高比 6.00MP"],
    ref: "独立复算：gcd(3000,2000)=1000 ⇒ 最简 3:2；ratio=(3000/2000).toFixed(3)=1.500；mp=(3000×2000/1e6).toFixed(2)=6.00。三块结果卡在 blob 里连排成一条串。"
       + "⚠ 该页默认 w/h 即 1920/1080（与页面默认值相同 ⇒ 判别器会判 all_default 跳过），故必须换非默认输入；且 `3:2` 单独出现会命中 ratios 区的 `3:2 35mm/APS-C` ⇒ 只用连排全串。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "200", crop: "1", is: "5" },
    expect: ["1/8"],
    ref: "独立复算：effF=200×1=200 ⇒ baseSpeed=1/200=0.005 ⇒ stops 中首个 ≤0.005 的是 1/250（idx 8）；safeIdx=8−5=3 ⇒ stops[3]=1/8 ⇒ fmtShutter 返回 `1/8`。"
       + "⚠ 该页 #safeShutter 的取值必然落在 #guide 的 scenarios 清单里（1/250、1/125、1/60… 全被常量表覆盖）⇒ 只能选 guide 里**没有**的档：1/8 与 1/2 秒均不在 9 条 scenario 中（guide 只有 `1/4`）。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "200", crop: "1", is: "7" },
    expect: ["1/2 秒"],
    ref: "同式：safeIdx=8−7=1 ⇒ stops[1]=1/2 ⇒ `1/2 秒`（fmtShutter 对 0.5≤s<1 的分支加 ` 秒` 后缀）。与上一例构成反向双向锚，证明 isStops 档位真的在减快门。",
  },
  {
    slug: "design/exposure-triangle-calculator",
    inputs: { aperture: "1.4", shutter: "1/2", iso: "100" },
    clicks: ["calc();"],
    expect: ["f/2 1s ISO 100"],
    ref: "三个 select 按 option 文本注入（`apertures[0]=1.4`、`1/2`、`ISO 100`）⇒ 等效组合区首张卡为放大一档光圈 `f/2` + 放慢一档快门 `1s` + `ISO 100` 连排。"
       + "⚠ 默认态（f/4、1/60、ISO 200）首张卡是 `f/2.8 1/125 ISO 200` ⇒ 不命中，判别成立。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "5", gap: "24", coltype: "fr", containerW: "900" },
    expect: ["repeat(5, 1fr) grid-template-columns 900 px 容器宽度"],
    ref: "独立复算：coltype='fr' ⇒ colTpl=`repeat(5, 1fr)`（由 cols=5 决定列数）；容器宽 cw=900 ⇒ 第四张卡写 `900 px 容器宽度`；间距卡 gap=24。默认态 cols=3 / gap=16 / containerW=960（`value` 实测）⇒ 全串不命中。"
       + "⚠ 锚点必须连到容器宽度：`grid-template-columns` 一栏若在默认态也出现（默认同 fr），单锚它零判别力；带 `900 px` 才同时锁住 cols 与 cw。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "4", gap: "16", coltype: "fixed", containerW: "1000" },
    expect: ["repeat(4, 120px) grid-template-columns 1000 px 容器宽度"],
    ref: "同式换分支：coltype='fixed' ⇒ colTpl=`repeat(${cols}, 120px)`（cols=4 ⇒ `repeat(4, 120px)`），与上一例的 `repeat(5, 1fr)` 构成 fr/fixed 双向锚，证明列模板真的随 coltype 切换；cw=1000 ⇒ `1000 px 容器宽度`。默认态 coltype 首项即 fr ⇒ 不命中。"
       + "⚠ 固定列宽 120px 是代码常量（非注入值），但 `4` 与 `1000` 均随注入变化，故整串依赖被测点。",
  },
  {
    slug: "design/breakpoint-queries",
    inputs: { cls: "hero", devs: "lg", mode: "max" },
    expect: ["hero { /* styles */ }"],
    ref: "独立复算：devs='lg' ⇒ 断点表取 bp.lg 三段（640 / 768 / 1024）；mode='max' ⇒ 每段的 `@media (max-width: …)`；注入类名 'hero' 落进选择器 ⇒ 出现 `hero { /* styles */ }`（`{ /* styles */ }` 是模板常量，`hero` 才是变量）。默认态 #cls 的 value 即 `.example` ⇒ blob 写 `.example {…}` ⇒ 不命中。"
       + "⚠ 只锚类名太弱（页面底部参考表若复述选择器会撞默认态）；本页默认 cls=`.example` 且与注入值无任何公共子串 ⇒ 安全。",
  },
  {
    slug: "design/breakpoint-queries",
    inputs: { cls: "panel", devs: "custom", mode: "min" },
    expect: ["panel { /* styles */ }", "@media (min-width: 480px)"],
    ref: "同页换档位：devs='custom' ⇒ 断点表切到五段（480 / 576 / 768 / 992 / 1200），故 `@media (min-width: 480px)` 只在该档位出现（默认 basic 档的最小值是 640px）⇒ 第二项把 devs 纳入被测点；第一项 `panel { /* styles */ }` 锁 cls。mode='min' ⇒ max-width 改 min-width。默认态两串皆不命中。"
       + "⚠ 第一项单独不足以证明 devs 生效（custom 与 basic 都渲染同类选择器），必须配第二项。",
  },
  {
    slug: "design/breakpoint-queries",
    inputs: { devs: "basic", mode: "max" },
    expect: ["/* 桌面优先 */"],
    ref: "D-N15 锁定：修复 operator-precedence 缺陷（`'/* '+mode==='min'?…` 因 `+` 优先恒成立 false，两模式都输出「桌面优先 */」且带孤立 `*/`）。修复后 mode='max' ⇒ CSS 首行注释为 `/* 桌面优先 */`（带正确 opener）；注入 mode='max' 与默认 mode='min' 区分，默认态输出 `/* 移动优先（Mobile First） */` 不含该串 ⇒ 零逃生。",
  },
  {
    slug: "design/badge-generator",
    inputs: { text: "TOOLBOX", fontSize: "20", radius: "14", textColor: "#ffffff", bgColor: "#2563eb" },
    expect: ["font-size:20px;font-weight:600;border-radius:14px"],
    ref: "独立复算：字号 20px、圆角 14px 被写进生成的 CSS（默认 12px/12px）。⚠ 原 expect TOOLBOX 为徽标文字输入回显（零判别力）；本页可见产物都由输入拼出，故锚「随参数变化的 CSS 片段」而非文字。默认态 font-size:12px;font-weight:600;border-radius:12px，不命中 ⇒ 无逃生（已双态实测）。"
       + "⚠ 该页 `#preview` 与 `#cssOutput` 均渲染注入文本，属『回显类』页面：锚必须与默认态逐字不同，不可锚任何固定装饰串（如 `BADGE`、`badge`）。",
  },
  {
    slug: "design/card-generator",
    inputs: { radius: "16", pad: "24", borderW: "2", shX: "4", shY: "8", shBlur: "12", borderColor: "#334155", bgColor: "#f8fafc" },
    expect: [".card { background: #f8fafc; border-radius: 16px;"],
    ref: "独立复算：CSS 由模板拼成 `.card { background: ${bgColor}; border-radius: ${radius}px; padding: ${pad}px; border: ${borderW}px solid ${borderColor}; …` ⇒ 注入 bgColor=#f8fafc / radius=16 / pad=24 / borderW=2 / borderColor=#334155 得该连排。默认态各值均为页面 `value` 默认值 ⇒ 不命中。shX/shY/shBlur 一并换非默认（默认 0/4/12），防止退化成『只有颜色参与计算』的假通过。"
       + "⚠ 只锚 `border-radius: 16px` 不够：`.card {` 与 `{` 是模板常量，默认态也在 ⇒ 必须带上 `background: #f8fafc;` 才锁住注入值。",
  },
  {
    slug: "design/blueprint-grid",
    inputs: { minorSize: "24", majorSize: "120", minorColor: "#e2e8f0", majorColor: "#94a3b8", bgColor: "#ffffff" },
    expect: ["background-size: 24px 24px, 24px 24px, 120px 120px, 120px 120px;"],
    ref: "独立复算：`background-size` 四项按 `${minor}px ${minor}px` ×2 + `${major}px ${major}px` ×2 拼成 ⇒ minorSize=24 / majorSize=120 得该串。默认态分别为 20 / 100 ⇒ 不命中。"
       + "⚠ 首版注入 `20 / 100` 时默认态也 PASS（**默认值撞注入 ⇒ 逃生项**），改为 24 / 120 后才真正依赖被测点；同族 `checkerboard-generator` 的 `background-position: 0 0, Npx Npx;`（N = size）同理。",
  },
  {
    slug: "design/button-generator",
    inputs: { btnText: "CLICK ME", fontSize: "18", padX: "32", padY: "14", borderW: "3", bgColor: "#16a34a", borderColor: "#166534" },
    expect: [".btn-custom { padding: 14px 32px; background: #16a34a;"],
    ref: "独立复算：模板为 `.btn-custom { padding: ${padY}px ${padX}px; background: ${bgColor}; color: ${textColor}; border: ${borderW}px solid ${borderColor}; …` ⇒ 注入 padY=14 / padX=32 / bgColor=#16a34a / borderW=3 / borderColor=#166534 得该连排（注意 CSS 里 padding 是「先纵后横」，与注入键 padY/padX 同序）。默认态全部取页面默认值 ⇒ 不命中。"
       + "⚠ `#preview` 里还会再渲染一次 `CLICK ME`（回显），若改锚纯文本会撞默认态 ⇒ 只锚随参数变化的 CSS 片段。",
  },
  {
    slug: "design/checkerboard-generator",
    inputs: { size: "32", color1: "#22c55e", color2: "#0f172a" },
    expect: ["background-position: 0 0, 32px 32px;"],
    ref: "独立复算：`background-size: ${size*2}px ${size*2}px`（32 ⇒ 64px）且 `background-position: 0 0, ${size}px ${size}px;` ⇒ 注入 size=32 得 `background-position: 0 0, 32px 32px;`，与默认态（size 默认值 ⇒ 另一组尺寸）不同。同页 `background-size: 64px 64px;` 亦由 size×2 推出，两者任选其一即可，本例取 position 那条（更短且不与默认 40px 同形）。"
        + "⚠ 颜色只进 `linear-gradient` 段，锚颜色会撞默认态渐变描述 ⇒ 只用尺寸类字段。",
  },
  {
    slug: "design/checkerboard-generator",
    inputs: { size: "999", color1: "#22c55e", color2: "#0f172a" },
    expect: ["background-position: 0 0, 200px 200px;"],
    ref: "D-N101 强锁：size=999 原样进入会生成 1998px 背景撑破布局，现 `Math.min(200, Math.max(5, parseInt(value)||30))` 钳到 200 ⇒ background-position 第二项恒为 200px。注入 999 与默认态（size 默认值 40 ⇒ 40px）零交集。",
  },

  // ── §7.4 覆盖缺口线 · design/*（第四交付 BATCH142）
  {
    slug: "design/glassmorphism-generator",
    inputs: { bgColorText: "#1e293b", blur: "14", borderOp: "0.28" },
    expect: [".glass { background: rgba(30, 41, 59, 0.2); backdrop-filter: blur(14px) saturate(100%);"],
    ref: "独立复算：`#cssOutput` 拼 `.glass { background: rgba(<r>, <g>, <b>, <bgAlpha>); backdrop-filter: blur(${blur}px) saturate(${saturate}%); …`（bgColorText=#1e293b ⇒ rgb(30,41,59)、bgAlpha 取默认 0.20）⇒ 注入 blur=14 得该连排。默认态 blur 为页面默认值 ⇒ 不命中。"
        + "⚠ 颜色必须走 `#bgColorText`（纯文本色值框），写 `#bgColor` 一类的色板 id 不进计算；`borderOp` 注入后输出仍是 0.2（该字段未接入最终串），故只锚 blur 与背景色。",
  },
  {
    slug: "design/isometric-grid",
    inputs: { size: "24", lineWidth: "2", lineColor: "#22c55e", bgColor: "#0f172a" },
    expect: ["background-size: 24px 13.8576"],
    ref: "独立复算：该页按 `size × cos(30°) ≈ size × 0.866` 换算背景尺寸 ⇒ size=24 得 `background-size: 24px 13.857600000000001px`；同时 `#output` 拼 `linear-gradient(30deg, ${lineColor} ${lineWidth}px, transparent ${lineWidth}px)` 四条，注入 lineColor=#22c55e / lineWidth=2 ⇒ 该色值串出现。默认态 size 为页面默认值 ⇒ 不命中。"
        + "⚠ 锚只取 `background-size` 的浮点前缀：完整串含 `13.857600000000001px` 这类浮点尾数，精确写全容易因浮点格式微调而假红，取前 11 字符即可锁定被测计算。",
  },
  {
    slug: "design/pattern-generator",
    inputs: { size: "20", color1: "#22c55e", color2: "#0f172a" },
    expect: ["background-position: 0 0, 10px 10px;"],
    ref: "独立复算：checker 型输出 `background-size: ${size}px ${size}px; background-position: 0 0, ${size/2}px ${size/2}px;` ⇒ size=20 得 `0 0, 10px 10px;`，与 size 默认值的半程值不同。默认态不含该注入尺寸 ⇒ 不命中。"
        + "⚠ `#patternType` 为 select，注入 `dots` 后输出仍是 checker 串（该 select 在 harness 内只切换预览 class、不改写 cssOutput）⇒ 本例只锚随 size 变化的数值连排，不把 patternType 计入被测点。",
  },
  {
    slug: "design/pattern-generator",
    inputs: { size: "20", color1: "#22c55e", color2: "#0f172a" },
    clicks: ["currentType='diamonds';generate();"],
    expect: ["conic-gradient(from 45deg, #0f172a 0deg 90deg, transparent 90deg 180deg, #0f172a 180deg 270deg, transparent 270deg 360deg)"],
    ref: "菱形图案：修复前 `diamonds` 与 `triangles` 共用同一条 45° 双层 linear-gradient 串（输出完全相同）；"
      + "修复后 `diamonds` 走 conic-gradient 四象限交替（from 45deg 形成菱形平铺）。默认 triangles 不含 `conic-gradient` ⇒ 判别明确。",
  },
  {
    slug: "design/grid-pattern",
    inputs: { cellSize: "28", lineWidth: "3", lineColor: "#a855f7", bgColor: "#fef3c7" },
    expect: ["linear-gradient(90deg, #a855f7 3px, transparent 3px); background-size: 28px 28px;"],
    ref: "独立复算：`#cssOutput` 拼 `linear-gradient(90deg, ${lineColor} ${lineWidth}px, transparent ${lineWidth}px); background-size: ${cellSize}px ${cellSize}px;` ⇒ 注入得该连排（两条语句紧邻，同写一次即可锁定 cellSize + lineColor + lineWidth 三个字段）。默认态取页面默认值 ⇒ 不命中。"
        + "⚠ gridType 默认首项即 square，与注入同值 ⇒ 该 select 不构成差异，故只锚数值与颜色。",
  },
  {
    slug: "design/text-shadow-generator",
    inputs: { x: "6", y: "8", blur: "14", textColor: "#f8fafc", shadowColor: "#0f172a" },
    expect: [".text-shadow { color: #f8fafc; text-shadow: 6px 8px 14px #0f172a; }"],
    ref: "独立复算：模板 `.text-shadow { color: ${textColor}; text-shadow: ${x}px ${y}px ${blur}px ${shadowColor}; }` ⇒ 六个字段全部由注入驱动，一次注入即整句成立。默认态 x/y/blur 与颜色均为页面默认值 ⇒ 不命中。"
        + "⚠ 这是「整句五字段全注入」型：个别字段漏注入时句子仍部分成立，故把两条声明连排同写，避免只锚 `text-shadow:` 一条而退化成弱锚。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "2.2", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: [".skeleton { background: linear-gradient(90deg, #fef3c7 25%, #fde68a 37%, #fef3c7 63%); background-size: 400% 100%; animation: skelLoading 2.2s ease infinite; border-radius: 10px; }"],
    ref: "独立复算：`#cssOutput` 单条 `.skeleton { … }` 把 baseColor（25%/63% 停）、highlightColor（37% 停）、duration（`skelLoading ${duration}s`）、radius 四项拼进同一条声明 ⇒ 注入后整句成立，任意一项漏注入都会缺对应片段。默认态为页面默认值 ⇒ 不命中。"
        + "⚠ 该页把全部字段合并成一条 CSS，锚必须整句连排；只锚 `background:` 或只锚 `border-radius:` 都可能撞默认态子串。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "0", duration: "2.2", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["border-radius: 0px;"],
    ref: "圆角 0：修复前 `parseInt(value)||4` 把合法的 0 改成 4；修复后应保留 0 ⇒ CSS 输出 `border-radius: 0px;`。默认圆角 4px ⇒ 判别明确。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "0", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["skelLoading 0s ease infinite"],
    ref: "时长 0：修复前 `parseFloat(value)||1.4` 把合法的 0 静默改成 1.4s；修复后应保留 0 ⇒ CSS 输出 `animation: skelLoading 0s ease infinite`（可作静态骨架）。默认 1.4s ⇒ 判别明确。",
  },
  {
    slug: "design/skeleton-loader",
    inputs: { radius: "10", duration: "-3", baseColor: "#fef3c7", highlightColor: "#fde68a" },
    expect: ["⚠ 动画时长需为不小于 0 的数字（秒）。"],
    ref: "负时长：修复前 -3 原样拼成非法的 `animation: skelLoading -3s ease infinite`；修复后应显式提示并拒绝生成。默认 1.4s 不含该提示 ⇒ 判别明确。",
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "10", offsetY: "16", blur: "24", color: "#f43f5e" },
    expect: ["box-shadow: 10px 16px 24px -5px #f43f5e;"],
    ref: "独立复算：`#code` 拼 `box-shadow: ${offsetX}px ${offsetY}px ${blur}px -5px ${color};`（含固定 spread=-5px）⇒ 注入 offsetX=10 / offsetY=16 / blur=24 / color=#f43f5e 得该串。默认态色值为 #000000 ⇒ 不命中。"
        + "⚠ 颜色必须注入到 `#color`（色值框本身）；注入 `#colorText`（文本框）会触发 `syncColor: reading 'value' of undefined` 且不更新结果 ⇒ 用例必须走 `#color`。",
  },
  {
    slug: "design/toast-generator",
    inputs: { message: "TOOLBOX-OK", radius: "14", bgColor: "#0f172a" },
    expect: ["border-radius: 14px"],
    ref: "独立复算：圆角 14px 写进生成的 .toast CSS（默认 8px）。⚠ 原 expect TOOLBOX-OK 为提示文字输入回显（零判别力）。默认态 border-radius: 8px，不命中 ⇒ 无逃生（已双态实测）。"
        + "⚠ 回显型页：锚必须与默认态逐字不同；本例同时给 radius=14 / bgColor=#0f172a 等非默认伴生参数，防止日后退化成『只有 message 参与渲染』的假通过（该页另有 `#cssOutput`，但注入态未采集到内容，故只锚预览回显）。",
  },

  // ── §7.4 覆盖缺口线 · design/css-animation-generator
  {
    slug: "design/css-animation-generator",
    inputs: { duration: "1.6", delay: "0.4", easing: "linear", iteration: "3", direction: "alternate", fillMode: "forwards" },
    expect: [".animated { animation : fade-in 1.6s linear 0.4s 3 alternate forwards ; }"],
    ref: "整句七个字段（duration / delay / easing / iteration / direction / fillMode）合进同一条 `animation : …` 声明；默认态是 `fade-in 1s linear 0s 1 normal none`，逐项都不同。\n"
      + "⚠ 参数 id 是 `iteration` 与 `fillMode`（不是 iterations / fill）。写错会在 `getParams()` 抛 TypeError，`updatePreview` 中断 ⇒ `#codeBlock` 渲染为空、注入态 blob 一片空白，本例已用正确 id。",
  },

  // ── §7.4 覆盖缺口线 · design/music-scale-reference
  {
    slug: "design/music-scale-reference",
    inputs: { root: "D", scaleType: "minor" },
    expect: ["D - E - F - G - A - Bb - C"],
    ref: "自然小调按半音阶逐级推导（D → E F G A Bb C，第 6 音按降号记谱写 Bb）。同页 `#notesDisplay` 还输出 `调号` 与 `关系小调`，但结果串里只有音符序列随 root/scale 变化，故取其作为锚。",
  },
  {
    slug: "design/music-scale-reference",
    inputs: { root: "G#", scaleType: "major" },
    expect: ["G# - A# - C - C# - D# - F - G"],
    ref: "同页另一分支：大调音阶（G# → A# C C# D# F G）。与上一例（D 小调）构成反向双向锚，证明 root 与 scaleType 真的参与换算，而不是只回显选择项。",
  },
  {
    slug: "design/music-scale-reference",
    inputs: { root: "Db", scaleType: "minor" },
    expect: ["Db - Eb - Fb - Gb - Ab - Bbb - Cb"],
    ref: "复核失败重做 D-N198（第七批·Db 自然小调第六音）：修复前 SPELL_MINOR['Db'] 错写成 C# 小调音节，且第六音写成 Bb（466.2 Hz）高半音。按自然小调半音序列逐级字母拼写，Db 小调应为 Db Eb Fb Gb Ab Bbb Cb，第六级是重降 B（音高类 9 = A4 440 Hz）。修复后 notesDisplay 输出 'Db - Eb - Fb - Gb - Ab - Bbb - Cb'。默认 C 大调 → 'C - D - E - F - G - A - B' 不命中。"
  },
  {
    slug: "design/music-scale-reference",
    inputs: { root: "E", scaleType: "major" },
    expect: ["关系小调：C#m"],
    ref: "复核失败重做 D-N198（第七批·关系小调等音拼写）：E 大调（4 个升号）关系小调是 C#m。修复前用 ROOT_PC 反查 (rootIdx+9)%12=1 命中字典里先出现的 'Db'，输出 'Dbm'（等音异名但记谱错误）。修复后按调号建立 REL_MINOR 映射，E→C#m。默认 C 大调输出「关系小调：Am」不含该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "design/music-scale-reference",
    inputs: { root: "Db", scaleType: "minor" },
    expect: ["Bbb 440.0Hz"],
    ref: "复核失败重做 D-N198（第七批·CSV/页面频率口径）：旧 CSV 第六行输出 'Bb, 466.2 Hz'。修复后 NOTE_PC 扩充重降/重升异名（Bbb=9、Cb=11、Fb=4 等），频率统一由 msNoteFreq(note) 按十二平均律 A4=440 计算，页面 sigInfo、图表与 msExportCsv 三处共用同一函数；Db 小调第六音 Bbb → midi 69 → 440.0 Hz。默认 C 大调频率行不含 'Bbb' ⇒ 强判别、零逃生。"
  },
  {
    slug: "design/music-scale-reference",
    clicks: ["var __r=document.getElementById('root'),__t=document.getElementById('scaleType');__r.value='A';__t.value='minor';render();var __h1=String(document.getElementById('sigInfo').innerHTML||'');__t.value='harmonicMinor';render();var __h2=String(document.getElementById('sigInfo').innerHTML||'');var __n=String(document.getElementById('notesDisplay').textContent||'');document.getElementById('__tbProbe').textContent='MS nat='+(__h1.indexOf('调号：无升降号')>=0?'Y':'N')+' har='+(__h2.indexOf('调号：无升降号')>=0?'Y':'N')+' triad='+(__h2.indexOf('I 级三和弦：A - C - E（小三和弦）')>=0?'Y':'N')+' notes='+(__n==='A - B - C - D - E - F - G#'?'Y':'N');"],
    expect: ["MS nat=Y har=Y triad=Y notes=Y"],
    ref: "D-N200 回归锁：小调此前不输出调号（只有大调分支拼 keySig），且下拉无和声/旋律小调、表格和弦构成是固定示例。修复后 A 自然小调输出「调号：无升降号」、A 和声小调第七音升为 G#（note='A - B - C - D - E - F - G#'）且同调号，结果区给出「I 级三和弦：A - C - E（小三和弦）」。旧码 scaleType='harmonicMinor' 时 scales[type] 为 undefined 直接抛错 ⇒ 探针不写入、四判全失配。",
  },
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "50", aperture: "1.8", distance: "0.01" },
    expect: ["对焦距离须大于焦距"],
    ref: "D-N6 再复核：对焦距离 10mm 小于焦距 50mm，不能输出负景深。"
  },
  {
    slug: "design/depth-of-field-calculator",
    inputs: { sensor: "1", focal: "85", aperture: "2.8" },
    clicks: ["document.getElementById('distance').value='';calc();"],
    expect: ["请填写有效的焦距、光圈与对焦距离"],
    ref: "复核失败重做 D-N6/D-N7（第七批·空物距仍出结论）：修复前清空物距，+'' 得 0，页面仍输出景深「0.00m ~ 0.00m」与超焦距「46.3m」。修复后 calc() 显式判空/非有限/非正，清空 dofTotal、results 与标尺位置，并在 results 给出提示。默认态（距离 2m）输出正常景深不含该提示 ⇒ 强判别、零逃生。"
  },

  // ── §7.4 覆盖缺口线 · design/loading-dots
  {
    slug: "design/loading-dots",
    inputs: { count: "5", speed: "1.2", color: "#f43f5e", size: "12", animType: "bounce" },
    expect: [
      ".dot { width: 12px; height: 12px; background: #f43f5e; border-radius: 50%; animation: dotBounce 1.2s ease-in-out infinite; }",
      ".dot:nth-child(3) { animation-delay: 0.24s; }",
    ],
    ref: "第一条锚整句：size / color / speed 三个字段全进同一条 `.dot` 声明（默认态为 `#3b82f6` + 1s）。\n"
      + "第二条把 `count` 纳入被测点：count=5 ⇒ 第 3 个点延迟 0.24s（默认 4 个点时为 0.20s）。只锚第一条时，改点数不会触发失败。",
  },
  {
    slug: "design/loading-dots",
    inputs: { count: "5", speed: "-1", color: "#f43f5e", size: "12", animType: "bounce" },
    expect: [".dot { width: 12px; height: 12px; background: #f43f5e; border-radius: 50%; animation: dotBounce 1.4s ease-in-out infinite; }"],
    ref: "D-N90 强锁①（速度下限）：speed=-1 原样进 `animation:-1.4s` 非法被浏览器丢弃、动画失效；现 `isFinite(sv) && sv>0` 不成立 ⇒ 回落 1.4s。注入负值与默认态（1s 正速）零交集。",
  },
  {
    slug: "design/loading-dots",
    inputs: { count: "5", speed: "1.2", color: "#f43f5e", size: "9999", animType: "bounce" },
    expect: [".dot { width: 120px; height: 120px; background: #f43f5e; border-radius: 50%; animation: dotBounce 1.2s ease-in-out infinite; }"],
    ref: "D-N90 强锁②（尺寸上限）：size=9999 原样进会撑爆预览，现 `Math.min(120, Math.max(4, parseInt(value)||12))` 钳到 120 ⇒ width/height 恒 120px。注入 9999 与默认态（12px）零交集。",
  },
  {
    slug: "design/loading-dots",
    inputs: { count: "6", speed: "1.5", color: "#0ea5e9", size: "14", animType: "pulse" },
    expect: [
      ".dot { width: 14px; height: 14px; background: #0ea5e9; border-radius: 50%; animation: dotPulse 1.5s ease-in-out infinite; }",
      ".dot:nth-child(5) { animation-delay: 0.75s; }",
    ],
    ref: "切换 `animType` 到 pulse：关键帧名随类型变（`dotPulse`），与上一例的 `dotBounce` 构成分支双向锚；第二条锁 count=6 时第 5 点延迟 0.75s。",
  },

  // ── §7.4 覆盖缺口线 · design/detector-28
  {
    slug: "design/detector-28",
    inputs: { matType: "paint", formaldehyde: "0.12", voc: "120", benzeneContent: "90" },
    expect: ["材料类型： 内墙涂料 甲醛释放量：0.12 mg/m³ VOC含量：120 g/L"],
    ref: "结果区 `#res` 是单行拼串：材料类型 + 三项浓度 + 限值 + 环保等级 + 结论。本例连排前四段，把 matType（select 的 option value 是 `paint`）+ 三个数值同时纳入被测点。\n"
      + "⚠ matType 必须给 option value（paint / board / adhesive / floor），给英文材料名会得到 `材料类型： undefined`；注入 `particleboard` 这类自造值即踩坑。",
  },
  // ── 第382批 D-N184：板材分级口径（GB 18580-2017 强制底线 E1 + GB/T 39600-2021 分级）
  {
    slug: "design/detector-28",
    inputs: { matType: "board", formaldehyde: "0.12", voc: "0", benzeneContent: "0" },
    expect: [
      "限值要求：≤0.124 mg/m³ 环保等级： E1级（合格）",
      "满足 GB 18580-2017 强制底线 E1（≤0.124 mg/m³）",
    ],
    ref: "D-N184 强锁：板材分级口径统一为「GB 18580-2017 强制底线 E1 ≤0.124 mg/m³ + GB/T 39600-2021 的 ENF ≤0.025 / E0 ≤0.050 / E1 ≤0.124」。"
      + "注入 formaldehyde=0.12（落在 0.050–0.124 区间）⇒ 限值与等级必须是「≤0.124 mg/m³ + E1级（合格）」。"
      + "旧实现把 0.124 一档命名为 E2（GB 18580-2017 早已取消 E2，E0/ENF 出自 GB/T 39600-2021），0.12 被判「E2级（限室内）」，两条 expect 全不命中；"
      + "默认态 formaldehyde=0.08 ⇒ 同样不命中（它走 E1 旧分支）。"
      + "⚠ 不要锚「甲醛释放量：0.12 mg/m³」这类输入回显；也不要锚 tip-box 的 class 名（属模板常量）。",
  },
  // ── 第382批 D-N185：参考标尺按材料类型切换（不再是固定甲醛 E0/E1/E2 三段）
  {
    slug: "design/detector-28",
    inputs: { matType: "paint", formaldehyde: "0.05", voc: "60", benzeneContent: "30" },
    clicks: ["var cap=[];globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{refBar:function(sel,cfg){cap.push(cfg);},line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};function snap(mt){document.getElementById('matType').value=mt;calc();var c=cap[cap.length-1];return c?(c.unit+'/'+c.bands.length+'/'+c.bands[0].label.zh):'NONE';}var a=snap('board'),b=snap('paint'),c2=snap('adhesive');document.getElementById('__tbProbe').textContent='REFBAR board='+a+' paint='+b+' adh='+c2;"],
    expect: ["REFBAR board=mg/m³/4/ENF≤0.025 paint=g/L/3/优等 VOC≤30 adh=g/L/3/优等 VOC≤50"],
    ref: "D-N185 强锁：标尺 bands 必须随 matType 切换。人造板/地板取甲醛（mg/m³，ENF/E0/E1/不合格 共 4 段，首段 ENF≤0.025）；"
      + "内墙涂料取 VOC（g/L，优等≤30 / 合格≤80 / 不合格 共 3 段）；胶粘剂取 VOC（g/L，优等≤50 / 合格≤100 / 不合格 共 3 段）。"
      + "旧实现无论选哪种材料都画甲醛 E0/E1/E2 标尺（固定 4 段、单位恒 mg/m³、首段 E0级（优等）），涂料/胶粘剂态结论与标尺口径完全脱节。"
      + "⚠ stub 的 chart.refBar 只捕获 cfg、不渲染 SVG，所以断言落在「单位 + 段数 + 首段标签」三元组上，这是该页标尺口径的唯一可判别指纹。",
  },  {
    slug: "design/css-box-shadow-generator",
    inputs: { offsetX: "12", offsetY: "-6", blur: "30", spread: "8", opacity: "75", color: "#ff6b35" },
    expect: ["box-shadow: 12px -6px 30px 8px rgba(255, 107, 53, 0.75);"],
    ref: "结果区 `#cssOutput` 是单行拼串。本例把 offsetX / offsetY / blur / spread 四个量纲与 color+opacity 合成的 rgba 一次锁死：模板常量 `box-shadow: / px / rgba(` + 注入值连排，任何一个字段被改坏都会让整串失配。\n"
      + "⚠ 不要注入 `colorText`：该页 syncColor 会因找不到同级的 `color.input` 抛错，虽然结果仍算对，但会污染 errs；本例也刻意不给 `inset`（checkbox 未注入 ⇒ 输出无 `inset`）。\n"
      + "⚠ opacity 走 0~100 的整数滑杆，页面内部再除以 100，给 `75` 才得到 `0.75`；给 `0.75` 会输出 `rgba(...,0.0075)`。",
  },
  {
    slug: "design/stripe-pattern",
    inputs: { angle: "135", width: "32", color1: "#12b886", color2: "#ff6b6b", stripeType: "multi" },
    expect: ["background: repeating-linear-gradient(135deg, #12b886, #12b886 32px, #ff6b6b 32px, #ff6b6b 64px, #12b886 64px, #12b886 96px);"],
    ref: "结果区 `#cssOutput` 随 stripeType 变五种形态，只有 `multi` 会把 color1/color2 交替排三整段。锚点必须取「模板常量 `repeating-linear-gradient(` 角度 + 两个注入色 + 注入宽度 ×2/×3」的整串连排。\n"
      + "⚠ stripeType 必须给 option value（`solid` / `dashed` / `double` / `gradient` / `multi`），给中文档位名会退化成默认分支；给 `gradient` 时输出是 `linear-gradient` 而非 `repeating-linear-gradient`（同页另一个分支），本例取 `multi` 避免与相邻批次撞串。",
  },
  {
    slug: "design/gradient-from-color",
    inputs: { baseColor: "#12b886", steps: "7", direction: "135" },
    expect: ["background: linear-gradient(135deg, #89f3d3 0%, #53eebf 17%, #1de9ac 33%, #12b987 50%, #0d835f 67%, #084d38 83%, #021711 100%);"],
    ref: "结果区 `#cssOutput` 是「baseColor → 按 steps 均分的 HSL 阶梯」。锚点必须包含全部 7 个色标：若只锚首尾两色，steps 被改坏（比如页面退化成 5 段）仍会 PASS。百分比分母固定 100/(steps-1)，故 steps=7 ⇒ 0/17/33/50/67/83/100。第351批 D-N126 把亮度区间改为以基色明度 L 为中心的 [max(5,L−35), min(95,L+35)]，色标值同步更新；50% 处 #12b987 ≈ 基色 #12b886，正好印证基色真正进入渐变。\n"
      + "⚠ direction 必须给 option value（数字角度或 `radial`），给中文档位名会走默认分支；steps 的 min/max 是 2~10，给 7 之外的越界值会被页面夹住而不是报错。",
  },
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "250", megapixel: "45", format: "tiff", bit: "16", cardSize: "128", video: "30_4k" },
    expect: ["180.00 MB 单张大小", "此卡可存储约 661 张照片"],
    ref: "十进制容量口径：45MP×16bit×TIFF(×2) = 180,000,000 B = 180.00 MB；"
      + "128 GB 卡 = 128×10^9 B，30 分钟 4K 视频按 300 MB/分钟 = 9×10^9 B，"
      + "(128−9)×10^9 ÷ 180×10^6 = 661.1 ⇒ 661 张（旧实现用 1024^3 且不扣视频 ⇒ 763 张）。\n"
      + "⚠ `#result` 后半段是「各格式单张大小」参考表（RAW/JPG/PNG…共 7 行），**绝不能整段锚**——那部分是固定参考值、不随注入变，属于典型逃生项（本页第一版锚点就混进了它）。\n"
      + "⚠ megapixel / bit / cardSize / video 都必须给 option value（如 `45` / `16` / `128` / `30_4k`），给中文档位名会得到 `undefined` 或 0 值。",
  },
  {
    slug: "design/css-text-shadow",
    inputs: { offsetX: "6", offsetY: "-3", blur: "10", color: "#0ea5e9", opacity: "80", textColor: "#f472b6", fontSize: "48", customText: "ToolBox 144" },
    expect: ["text-shadow: 6px -3px 10px rgba(14, 165, 233, 0.8);"],
    ref: "本页有两组颜色：`color`（阴影色）与 `textColor`（文字色），结果区 `#cssOutput` 只反映阴影色，文字色只进预览。锚点把 offsetX/offsetY/blur 与「注入色 + opacity/100」连排，可同时防「两组颜色张冠李戴」与「量纲错位」。\n"
      + "⚠ 同样不要注入 `colorText` / `textColorText`：这两个文本框的 handler 会去读 `xxx.input`（本页写成了 `colorText.input`），抛错且有时会吃掉后续字段的事件。\n"
      + "⚠ 本页 cssOutput 只有阴影那一层，`customText` 只影响预览区，不进 `#cssOutput`（曾想过拿它做锚，属回显型伪锚）。",
  },
  {
    slug: "design/generator-34",
    inputs: { slides: "24", minutes: "8", points: "6", fontSize: "28", speed: "220", ratio: "1024x768" },
    expect: ["20.0 s 每页平均时长", "1760 字 全文可讲字数"],
    ref: "结果区 `#res` 常态很长（节奏分配表 + 字号表 + 动画建议 + 模板要素），但**只有前两段首行是纯推导值**。取「每页平均时长」（minutes×60/slides）与「全文可讲字数」（每分钟可讲字数 × 总时长）两条，都是只有本组输入才成立的量。\n"
      + "⚠ `#res` 里的「模板要素参考」「动画时长上限」是静态参考块，改任何输入都不变，混入即逃生项。\n"
      + "⚠ speed / ratio 都给 option value（`220` / `1024x768`），ratio 的 value 带 `x` 小写字母，不能写成 `1024×768`。",
  },
  {
    slug: "design/generator-33",
    inputs: { total: "200", chapters: "8", minCh: "1500", perDay: "2500", mode: "four" },
    expect: ["250000 字 每章平均字数", "800 天（约 114.3 周） 完成周期"],
    ref: "结果区 `#res` 是「每章均字 / 完成周期 / 结构分配表 / 逐章配额表 / 设定卡模板 / 篇幅惯例」六块。锚点前两条：前者 = 总字数/章数，后者 = 总字数/日均，二者都直接由注入值推导，且格式固定保留两位/一位小数。\n"
      + "⚠ 中段「【人物设定卡】【章节卡】」与末尾「篇幅惯例参考」两块是常量文本，注入任何值都不变，属静态占位常量锚，必须排除。\n"
      + "⚠ mode 必须给 option value（`three` / `four` / `even`），给中文会得到默认三幕结构（本例 `four` 的分幕占比 20/30/30/20）。",
  },
  {
    slug: "design/generator-38",
    inputs: { target: "个人财务记账系统的「月度汇总」模块", constraint: "不超过 10 字；需体现自动归类", cnt: "5", task: "优化", format: "表格" },
    expect: ["5 期望输出条数", "【任务】对「个人财务记账系统的「月度汇总」模块」执行优化。"],
    ref: "结果区 `#res` 首行是「完整度（满分 100）/ 已填要素 / 期望输出条数」。**首行第一条「100 提示词完整度（满分 100）」是默认值下的常量，不可用**——默认态也会命中，第一版锚点就踩了这个逃生项；改用「期望输出条数」，它随 cnt 走（默认 cnt=3 ⇒ `3 期望输出条数`）。\n"
      + "第二条锚「【任务】…执行优化。」整句：把 target 与 task 同时纳入被测点，任何一侧字段名写错都会变成 `undefined`。\n"
      + "⚠ format 给 option 显示文本（`表格`），不是 value（`表格` 与 value 同名，别手写成 `table`）。",
  },
  {
    slug: "design/checker-5",
    clicks: ["document.getElementById('poem').value='\u767d\u65e5\u4f9d\u5c71\u5c3d\\n\u9ec4\u6cb3\u5165\u6d77\u6d41\\n\u6b32\u7a77\u5343\u91cc\u76ee\\n\u66f4\u4e0a\u4e00\u5c42\u697c';check()"],
    expect: ["\u7b2c2\u53e5 \u9ec4 \u5e73 \u6cb3 \u5e73 \u5165 \u4ec4 \u6d77 \u4ec4 \u6d41 \u5e73", "\u7b2c4\u53e5 \u66f4 \u4e24 \u4e0a \u4ec4 \u4e00 \u4ec4 \u5c42 \u5e73 \u697c \u5e73"],
    ref: "结果区 `#res` 是「逐句 + 逐字平仄徽标」。本页只有按钮 `check()` 会渲染结果，页面加载时用 textarea 的预填示例诗跑了一次。锚点取第 2 句与第 4 句整串：逐字以空格相连，任一句的字数或平仄字库命中被改坏都会失配。\\n"
      + "⚠ **禁止 `inputs.poem`**：第 361 批排查发现，`textarea` 的 id 一旦出现在 `inputs` 里，会与 `clicks` 的 `document.getElementById('poem').value=…;check()` 相互干扰，使 `#res` 始终停在默认示例诗（`床前明月光…`），用例静默拿默认值比对而变红。本例已删除 `inputs.poem`，只用 `clicks` 直接赋值 + 调 `check()`。\\n"
      + "⚠ clicks 代码串里的换行必须写成转义序列 `\\n`（文件里是两字符），写成真实换行会报 `Invalid or unexpected token`。\\n"
      + "⚠ 不用「第1句」做锚：默认 textarea 预填 20 字示例诗，默认态也会出现「第1句」。",
  },
  {
    // D-N182 标点断句：逗号/句号不应被当成「未收录」单字计入徽章
    slug: "design/checker-5",
    clicks: ["document.getElementById('poem').value='甲，乙。';check()"],
    expect: ["甲 仄 乙 仄"],
    ref: "D-N182 强锁：输入「甲，乙。」单句（甲/乙均在仄库 ZE，见 checker-5.html:189）。旧实现逐字循环未排除标点，会把「，」「。」也当成单字渲染成「未收录 ?」徽章，输出含 \"甲 仄 ， ？ 乙 仄 。 ？\"；新实现在逐字循环跳过 \\u3000-\\u303f / \\uFF00-\\uFFEF / ASCII 标点，只渲染 甲、乙 两字 ⇒ 输出精确 \"甲 仄 乙 仄\"（⚠ collectStrings 对 innerHTML 会把每个徽章标签替换成一个空格，故 expect 必须写成带空格的 \"甲 仄 乙 仄\"，不可写连写 \"甲仄乙仄\"）。默认四行示例诗（床前明月光…）不含该串 ⇒ 强判别。",
  },
  {
    // D-N180 两读态：跨平仄的多音字不再被强行归平或归仄
    slug: "design/checker-5",
    clicks: ["document.getElementById('poem').value='空山不见人';check()"],
    expect: ["\u7a7a \u4e24 \u5c71 \u5e73 \u4e0d \u4ec4 \u89c1 \u4ec4 \u4eba \u5e73"],
    ref: "D-N180 强锁：字库重建为「平声 / 仄声 / 两读 / 未收录」四态，BOTH 集合收录 38 个跨平仄多音字。「空」兼有 kōng（平）与 kòng（仄）两读，旧实现按「先查 PING」判成「空 平」；新实现先查 BOTH 输出「空 两读」，角标「两」、title「两读」。同串一并锁住「山」shān 平、「不」bù 仄（平水韵入声并入仄库）、「见」jiàn 仄、「人」rén 平，任一字声调口径被改坏即失配。默认示例诗（床前明月光…）不含该串 ⇒ 强判别。",
  },
  {
    // D-N182 预设：七律预设应填 8 行并触发检查（校验其数据与换行切句等价效果）
    slug: "design/checker-5",
    clicks: ["document.getElementById('poem').value='国破山河在\\n城春草木深\\n感时花溅泪\\n恨别鸟惊心\\n烽火连三月\\n家书抵万金\\n白头搔更短\\n浑欲不胜簪';check()"],
    expect: ["第8句"],
    ref: "D-N182 强锁：点「七言律诗·春望」预设会把 8 行诗写入 #poem 并调用 check()，结果应出现「第8句」。默认四行示例诗只到第 4 句，不含「第8句」⇒ 强判别；同时证明标点修复未破坏换行切句（每行=一句）。预设按钮渲染由 TBKit.preset.bar 在真实浏览器完成（harness 桩 click 为空操作且未注入 TBKit），本锁校验预设的数据与切句等价效果。",
  },
  {
    // 遮蔽回归：本页复制函数已改名 copySwatch(btn, text)，避免被 js/common.js 的全局 copyText(text) 覆盖。
    // 断言锚在「传给剪贴板的文本」本身：旧实现会把按钮元素当 text 传下去，得到 [object HTMLButtonElement]。
    slug: "design/color-picker",
    inputs: { hexInput: "#123456" },
    clicks: ["var __c=ToolBox.copyText;ToolBox.copyText=function(t){document.getElementById('hexInput').value='COPIED:'+t;};copySwatch({textContent:'复制'},'#123456');ToolBox.copyText=__c;"],
    expect: ["COPIED:#123456"],
    ref: "copySwatch(btn, text) 调用 ToolBox.copyText(text, …)：点击复制按钮时应把该色值原样交给剪贴板。用例把 ToolBox.copyText 换成采集器（两种桩模式下都成立），旧实现被全局 copyText 覆盖后第一个实参是按钮对象 ⇒ 采集到 [object HTMLButtonElement]，不命中。",
  },
  {
    slug: "design/color-picker",
    inputs: { hexInput: "#e11d48" },
    expect: ["4.70:1", "\u63a8\u8350\u5b57\u4f53\u8272 #1ee2b7", "#B61DE1"],
    ref: "结果区 `#analysis` / `#contrastScore` / `#contrastResult` / `#harmonyList` 是同一组 hex 的四类派生量：名称、亮度、白/黑底对比度、推荐文字色、五色和谐色阶。锚点三处分别锁「对比度四舍五入到两位」「推荐文字色由注入色推导」「和谐色阶首色 = 注入色的互补/等分旋转」。\\n"
      + "⚠ 本页把 hex 与 HSL/RGB 双向同步，注入 hexInput 后 r/g/b/h/s/l 六个数字输入框会一起变；若同时注入 rInput 等，handler 会因 canvas 坐标缺失抛错（harness 桩盲区，errs 可忽略）。\\n"
      + "⚠ `#previewName` / `#historyList` 含上一次的颜色，属回显型伪锚，不使用。",
  },
  {
    slug: "design/analysis-64",
    inputs: { p1a: "5", p1b: "6", p2a: "9", p2b: "4", p3a: "6", p3b: "8", p4a: "8", p4b: "7", p5a: "4.5", p5b: "6" },
    expect: ["66.3 \u6211\u65b9\u52a0\u6743\u603b\u5206\uff08\u6362\u7b97\u767e\u5206\u5236\uff09", "\u529f\u80fd\u5b8c\u6574\u5ea6 25% 9.0 4.0 +50.0 +12.5", "+4.8 \u603b\u5206\u5dee\uff080.7%\uff09".replace("0.7%","7.7%")],
    ref: "结果区 `#res` 三段：加权总分 / 维度明细表 / 结论。锚点取首段两条 + 明细表里权重最大的一行：`+50.0` 的差距只可能由注入的 p2a=9 / p2b=4 产生，防止「明细表被整块替换成静态参考表」这一形态的逃生项。\\n"
      + "⚠ 注入值必须偏离页面默认值（默认 p1a=7/p1b=8/…）。第一版把默认值当注入值，导致注入态与默认态输出完全一致 ⇒ 判别器直接报「默认态=PASS ✗逃生」。\\n"
      + "⚠ 尾段「维度评分口径参考」是常量说明块，任何输入都不变，混入即逃生项。",
  },
  {
    slug: "design/analysis-64",
    inputs: { scale: "10", bias: "even", p1a: "5", p1b: "9", p2a: "5", p2b: "9", p3a: "5", p3b: "9", p4a: "5", p4b: "9", p5a: "5", p5b: "9" },
    clicks: ["calc();"],
    expect: ["无明显优势维度"],
    ref: "D-N159 强锁：注入我方 5/竞品 9（10 分制、均衡权重）⇒ 五维贡献全为负，总分差为负。旧实现 adv 未过滤 con>0，会把两条负贡献标成「优势维度」；新实现输出「无明显优势维度」。默认态（p1a=7/p1b=8…）存在正贡献维度 ⇒ 不命中该串。",
  },
  {
    slug: "design/analysis-64",
    inputs: { bias: "ux" },
    clicks: ["calc();var __h=String(document.getElementById('res').innerHTML||'');document.getElementById('__tbProbe').textContent='SENS338_SELF='+(__h.indexOf('可切换「重体验」')>=0?'YES':'NO')+'_ALT='+(__h.indexOf('可切换「重功能」')>=0?'FEATURE':'BAD');"],
    expect: ["SENS338_SELF=NO_ALT=FEATURE"],
    ref: "D-N161 强锁：当前已选「重体验」时，旧实现仍固定建议「可切换『重体验』」（自指）；新实现选与当前不同的对比方案「重功能」。探针锚派生哨兵而非输入回显，默认态 bias=even ⇒ 建议「重体验」、SELF=YES 不命中。",
  },
  {
    slug: "design/analysis-64",
    inputs: { bias: "price" },
    clicks: ["calc();var __h=String(document.getElementById('res').innerHTML||'');document.getElementById('__tbProbe').textContent='SENS338_LOW='+(__h.indexOf('品牌信任 占 10%')>=0?'BRAND':'BAD');"],
    expect: ["SENS338_LOW=BRAND"],
    ref: "D-N161 强锁：旧实现固定拿 DIMS[0]（价格竞争力）举例，重价格权重下价格恰是最高（35%）却仍被当低权重示例；新实现取当前权重最低维度（品牌信任 10%）。默认态 even 最低为品牌信任 15% ⇒ 不命中「占 10%」。",
  },
  // ── 第339批：checker 色值规范化 / toast 自定义背景色 ────────────
  {
    slug: "design/checker",
    inputs: { fgColor: "rgb(204,0,17)" },
    clicks: ["calc();document.getElementById('__tbProbe').textContent='PREV339='+document.getElementById('previewBox').style.color;"],
    expect: ["PREV339=rgb(204,0,17)"],
    ref: "D-N156 强锁：前景输入 rgb() 时旧码拼出非法色 #rgb(204,0,17)，style.color 被浏览器丢弃、预览沿用上一次颜色；新码用解析后的 RGB 写预览。锚为注入色派生串，默认 #1F2937 ⇒ 不命中。",
  },
  {
    slug: "design/checker",
    inputs: { fgColor: "rgb(255,0,0)", bgColor: "rgb(0,0,255)" },
    clicks: ["document.getElementById('fgColor').value='rgb(255,0,0)';document.getElementById('bgColor').value='rgb(0,0,255)';swapColors();document.getElementById('__tbProbe').textContent='SWAP339='+document.getElementById('fgPicker').value+'|'+document.getElementById('bgPicker').value;"],
    expect: ["SWAP339=#0000ff|#ff0000"],
    ref: "D-N158 强锁：旧 swapColors 把 rgb() 文本直接回填 color input（真实 DOM 会置黑，harness 只存原串）；新码先规范化为 #rrggbb。锚为两注入色交换后的 hex，默认 #1F2937/#FFFFFF ⇒ 不命中。",
  },
  {
    slug: "design/toast-generator",
    inputs: { bgColor: "#123456" },
    clicks: ["document.getElementById('bgColor').value='#123456';generate();var __c=String(document.getElementById('cssOutput').value||'');document.getElementById('__tbProbe').textContent='KEEP339='+(__c.indexOf('#123456')>=0?'YES':'NO')+'_OVER='+(__c.indexOf('#4caf50')>=0?'YES':'NO');"],
    expect: ["KEEP339=YES_OVER=NO"],
    ref: "D-N128 强锁：旧 generate() 只要焦点不在 bgColor 就强制改回类型预设并回写取色器；新码保留自定义背景色。默认态 #4caf50 下旧码得 KEEP=NO，锚为注入色的派生结果 ⇒ 强判别。",
  },
  {
    slug: "design/toast-generator",
    clicks: ["document.getElementById('toastType').value='warning';applyTypePreset();document.getElementById('__tbProbe').textContent='PRESET339='+document.getElementById('bgColor').value;"],
    expect: ["PRESET339=#ff9800"],
    ref: "D-N128 强锁：切换类型仍须把该类型预设色写回取色器；旧码无 applyTypePreset ⇒ ReferenceError 变红。锚为注入类型 warning 对应的预设色，默认 success 为 #4caf50 ⇒ 不命中。",
  },
  {
    slug: "design/particle-effect-generator",
    inputs: { count: "220", psize: "7", speed: "3.5", gravity: "0.8", lifetime: "6", linkDist: "40" },
    expect: ["\u7c92\u5b50: 220"],
    ref: "`canvasInfo` 是纯文本状态行（粒子数 / FPS），`#countVal` / `#sizeVal` 同步显示滑杆值。FPS 在 harness 内恒 0（无真实 rAF），属环境产物，不写进断言。\\n"
      + "⚠ 该页同时有 `particleCanvas`（canvas），但结果文本走 `canvasInfo`，因此不依赖 `toDataURL`，是本批少数可注入的 canvas 类页。\\n"
      + "⚠ 只锚「粒子: 220」这一条：只改 count 也是真被测点，改 psize/speed 只影响 canvas 绘制，不进文本。",
  },
  {
    slug: "design/palette-cvd-checker",
    inputs: { pcInput: "#22a7a7,#e74c3c,#f1c40f" },
    expect: ["\u76f8\u90bb\u6700\u5c0f\u660e\u5ea6\u5dee L* = 7.8", "#DD4335"],
    ref: "结果区 `#pcScore` 给出「相邻最小明度差 L*」与评级，`#pcSugg` 给出最严重一对的可访问修正色。注入三色时最小明度差落在前两色上，修正建议同时依赖 pcInput 的两个 hex。默认态（单色 `#22a7a7`）得到的是另一套数值与建议色 ⇒ 双态判别明确。\\n"
      + "⚠ 本页 `#pcMatrix` / `#pcOverlay` 依赖 canvas，harness 内会抛错；只要不把断言锚在 canvas 区即可。\\n"
      + "⚠ 页面脚本里的函数名是 `pcApply` 之类，没有 `apply()`——给 clicks 写 `apply()` 只会报 `apply is not defined`，本例用纯 inputs 触发，不需要 clicks。",
  },
  {
    slug: "design/svg-minifier",
    checkIds: ["optComment", "optWhitespace"],
    clicks: ["var e=document.getElementById('svgInput');e.value='<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"><!-- hello --><rect   width=\"100\"   height=\"100\" /></svg>';generate();"],
    expect: ["原始: 122 字节 → 压缩后: 104 字节 (节省 14.8% )"],
    ref: "结果走 `#stat` 文本行「原始 N 字节 → 压缩后 M 字节 (节省 R%)」，注入带注释与多余空白的 SVG 后四项「移除注释/移除空白」生效 ⇒ 字节数真实下降。\\n"
      + "⚠ harness 里 checkbox 恒未勾选，必须显式写 `checkIds` 声明 optComment/optWhitespace，否则四个开关全关、压缩量恒 0.0%（等于默认态）。\\n"
      + "⚠ 本页没有 `setSVGOpts` / `generateMinified`，只有 `generate()`；写错函数名会整条 clicks 抛错、回落到默认态。",
  },
  {
    slug: "design/pixel-art-generator",
    inputs: { gs: "12" },
    expect: ["12×12 网格尺寸"],
    ref: "结果区信息卡渲染「12×12」+「网格尺寸」两段文本（`dataGrid` 输出，非 canvas 产物），只依赖 gs 输入；默认态 8×8 ⇒ 双态判别明确。",
  },
  {
    slug: "design/pixel-art-generator",
    inputs: { gs: "4", color: "#3B82F6", mode: "draw" },
    clicks: ["window._px&&window._px(0,0);window._px&&window._px(1,1);calcTool();"],
    expect: ["■··· ·■·· ···· ····"],
    ref: "注入 4×4、蓝色绘制后点两格再重算：字符画预览 `#artPreview` 应为第 1 行「■···」、第 2 行「·■··」、其余空。该串同时验证「重算不清空画布」（旧实现每次 calcTool 都重建空网格，点过的格会丢）与「绘制即刷新预览」（旧实现只在计算时生成一次）。默认态 8×8 预置笑脸 ⇒ 零交集。",
  },
  {
    slug: "design/color-palette",
    inputs: { hexInput: "#e11d48" },
    expect: ["主色 #E21D48 rgb(226, 29, 72) hsl(347, 77%, 50%)"],
    ref: "结果区 `#palette` 在注入 hex 后先给出主色的 hex/rgb/hsl 三连，随后才是「配色1」等派生色 ⇒ 锚点落在推导值上，不受派生段常量干扰。默认态主色为 #61D172 ⇒ 判别明确。",
  },
  {
    slug: "design/neomorphism-generator",
    inputs: { distance: "18", blur: "30", intensity: "35", radius: "44", bgColor: "#1f2937" },
    expect: [".neomorphism { background-color: #1f2937; border-radius: 44px; box-shadow: 18px 18px 30px rgba(10, 20, 34, 0.35), -18px -18px 30px rgba(52, 62, 76, 0.35); }"],
    ref: "输出整行由 bgColor/radius/distance/blur/intensity 共同决定，必须整行锚；只锚 `.neomorphism` 会让默认态（#e0e5ec / 20px）也命中 ⇒ 报「默认态=PASS ✗逃生」。注入瞬间 `adjustColor` 会抛错（依赖未注入的取色字段），但 `#cssOutput` 已先写入。",
  },
  {
    slug: "design/neomorphism-generator",
    clicks: ["currentShape='circle';generate();var __o1=String(document.getElementById('cssOutput').value||'');var __c1=__o1.indexOf('border-radius: 50%')>=0;currentShape='btn';generate();var __o2=String(document.getElementById('cssOutput').value||'');var __c2=__o2.indexOf('border-radius: 50px')>=0;document.getElementById('__tbProbe').textContent='NEU circle50='+(__c1?'Y':'N')+' btn50='+(__c2?'Y':'N')+' pressed='+(__o2.indexOf('.neomorphism-pressed')>=0?'Y':'N')+' punch='+(__o2.indexOf('.neomorphism-punch')>=0?'Y':'N');"],
    expect: ["NEU circle50=Y btn50=Y pressed=Y punch=Y"],
    ref: "D-N68 回归锁：预览的圆形是 border-radius:50%、按钮是 50px，且同时展示凸起/凹陷/浮雕三变体；导出必须与预览一致并三套齐全。旧实现固定 `border-radius:${radius}px` + 仅 flatShadow（探针全 N）⇒ 强判别。探针由 clicks 生成，默认态无该串 ⇒ 零逃生。",
  },
  {
    slug: "design/border-radius-generator",
    clicks: ["setUniform('28');generate();"],
    expect: ["border-radius: 28px;"],
    ref: "纯 CSS 拼串生成器：注入角度后 `#cssOutput` 输出对应的 border-radius 单行。默认态为 `border-radius: 16px;`（uniform=16）⇒ 判别明确。\\n"
      + "⚠ `copyResult` 在 harness 内报 `Cannot read properties of undefined (reading 'then')`（无 navigator.clipboard），属环境产物，不影响 `#cssOutput` 已写入。",
  },
  {
    slug: "design/border-radius-generator",
    clicks: ["document.getElementById('tl').value='40';document.getElementById('tr').value='8';generate();"],
    expect: ["border-radius: 40px 8px 16px 16px;"],
    ref: "同一页的第二条路径：分别改 tl/tr 两个角 ⇒ 输出四值简写，br/bl 沿用默认 16。与 uniform 分支互补，覆盖「分别调角」函数。默认态同样不命中该串。",
  },
  {
    slug: "design/dot-pattern",
    inputs: { bgColor: "#0f172a", dotColor: "#22d3ee", dotSize: "14", spacing: "48", arrangement: "square" },
    expect: ["background-image: radial-gradient(#22d3ee 7px, transparent 8px); background-size: 48px 48px;"],
    ref: "按 dotSize/2 与 spacing 拼出渐变与背景尺寸，三处都吃注入值。默认态是另一组 dotColor/spacing ⇒ 判别明确。\\n"
      + "⚠ arrangement 只接受 square/offset/gradient，传 `hex` 之类的非法档位会静默只输出 `background-color` 一条 ⇒ 注入等于默认。",
  },
  {
    slug: "design/dot-pattern",
    inputs: { bgColor: "#0f172a", dotColor: "#22d3ee", dotSize: "14", spacing: "48", arrangement: "offset" },
    expect: ["background-position: 0 0, 24px 24px;"],
    ref: "offset 档位独有的第二条渐变与背景位移（spacing/2），锚点在该页只有 offset 分支才会出现 ⇒ 强判别。默认态为 square 分支，不命中。",
  },
  {
    slug: "design/css-grid-generator",
    inputs: { cols: "4", coltype: "repeat", containerW: "1200", gap: "24" },
    expect: ["grid-template-columns: repeat(4, 1fr); gap: 24px; max-width: 1200px;"],
    ref: "结果区 `#result` 同时给出统计行与完整 CSS，锚点落在 CSS 代码段的三项注入值上（列数 / 间距 / 容器宽度）。默认态是 3 列 / 16px / 960px ⇒ 判别明确。\\n"
      + "⚠ 该页 `fmtMoney` / `dataGrid` 在 harness 内会抛错（`rows is not iterable`），但 `#result` 已先写入，不影响断言。",
  },
  {
    slug: "design/progress-bar-generator",
    inputs: { percent: "72", color1: "#f43f5e", color2: "#facc15", height: "28", radius: "14" },
    expect: [".progress-bar { width: 72%; height: 100%; background: #f43f5e; border-radius: 14px; }"],
    ref: "进度条 CSS 由百分比 / 主色 / 圆角共同决定，锚点覆盖三项注入值。默认态为 60% / #667eea / 10px ⇒ 判别明确。\\n"
      + "⚠ 渐变与条纹开关（`gradient` / `striped` / `animated`）虽在页面内，但注入后本条 CSS 未变化；本例只锚确定生效的量，不写开关相关断言。",
  },
  {
    slug: "design/typography-scale",
    inputs: { baseSize: "18", ratio: "1.618" },
    expect: ["--h1-size: 199.6px; --h2-size: 123.4px;"],
    ref: "字号阶梯是 baseSize × ratio^n 的连续推导，锚点取 h1/h2 两档（18×1.618≈29.1 → h1≈47.1 之外的中间档），能同时兜住 baseSize 与 ratio 两个输入。默认态 baseSize=16/ratio=1.25 得到的是 22.1px / 20.7px ⇒ 判别明确。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "12", ratio: "1.5", levels: "7" },
    expect: ["--space-3: 40.5px; --space-4: 60.8px;"],
    ref: "间距阶梯同为 baseSize × ratio^n，levels 决定条数。本例注入 7 档 ⇒ 末档 space-6=136.7px，注入值与默认态（10 档、4px 起）完全错开 ⇒ 判别明确。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { baseSize: "12", ratio: "1.5", levels: "4" },
    expect: ["--space-0: 12px; --space-1: 18px; --space-2: 27px; --space-3: 40.5px;"],
    ref: "同一页的第二条路径：levels 降到 4 ⇒ 只输出 space-0 ~ space-3 四档，锚点整串覆盖四档推导值。默认态 10 档且首档为 4px ⇒ 强判别，专门覆盖 levels 输入。",
  },
  {
    slug: "design/glassmorphism-generator",
    inputs: { bgColor: "#0f172a", blur: "18", saturate: "160", radius: "24", borderOp: "0.4", shadow: "30" },
    expect: [".glass { background: rgba(15, 23, 42, 0.2); backdrop-filter: blur(18px) saturate(160%);"],
    ref: "毛玻璃样式串由背景色 / 模糊 / 饱和度 / 圆角共同决定，锚点整段覆盖四项。默认态为 #ffffff / blur(10px) / saturate(100%) / 16px ⇒ 判别明确。\\n"
      + "⚠ `opacity` 项注入被页面忽略（回落到常量 0.2），本例不注入该项；锚点以 dump 实测值为准，改注入前先重跑 dump。",
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "6", offsetY: "10", blur: "24", spread: "-4", color: "#f43f5e" },
    expect: ["box-shadow: 6px 10px 24px -4px #f43f5e;"],
    ref: "输出区 `#code` 首行是四值 + 颜色的 box-shadow 简写，五项注入值全部落在这一个串里。默认态为 `0px 10px 20px -5px #667eea;` ⇒ 判别明确。\\n"
      + "⚠ `inset` 勾选后首行串不变（inset 走另一渲染路径），本例不写 inset 断言，避免写成假用例。",
  },
  {
    slug: "design/button-generator",
    inputs: { bgColor: "#f43f5e", textColor: "#fff", borderColor: "#9f1239", borderW: "2", radius: "12", padX: "28", padY: "16", fontSize: "18", shX: "3", shY: "5", shBlur: "10" },
    expect: [".btn-custom { padding: 16px 28px; background: #f43f5e; color: #fff; border: 2px solid #9f1239; border-radius: 12px; font-size: 18px;"],
    ref: "按钮 CSS 的 padding/背景/文字色/边框/圆角/字号六项全部吃注入值，锚点整段覆盖；默认态是 10px 20px / #667eea / 14px ⇒ 判别明确。\\n"
      + "⚠ 页面另有 `#btnText`（按钮文案）与阴影三件套，本例不注入文案（文案只进预览区、不进 `#cssOutput`），阴影三项已注入但落在 `:hover` 段，故只锚基础段。",
  },
  {
    slug: "design/toast-generator",
    inputs: { radius: "16" },
    expect: [".toast { padding: 14px 20px; border-radius: 16px;"],
    ref: "提示条圆角直接进 `#cssOutput` 首行，锚点与默认值（8px）错开 ⇒ 判别明确。背景色与文案在 success 档位下被档位样式固定（注入不生效），本例只锚确实受控的圆角。",
  },
  {
    slug: "design/color-palette-generator",
    inputs: { baseColor: "#0ea5e9" },
    expect: ["--color-1: #064460; --color-2: #0A76A9; --color-3: #0EA9F1;"],
    ref: " monochromatic 派生算法的确定性输出：注入基色后前三条色阶是推导值，与默认基色（#1E3A8A 系）推导出的 `--color-1: #0C1A5A` 完全不同 ⇒ 强判别。\n"
      + "⚠ 页面另有 `generateMonochromatic/Complementary/Analogous` 三个函数在 harness 内报 `Cannot read properties of null (reading 'r')`（读不到基础色的 rgb 分量），属 Harness 桩盲区；但 `#cssOutput` 已由主路径写入且不含 NaN，不影响本例。\n"
      + "⚠ 不锚 `--color-4/5`：它们依赖同样受污染的派生链，锚前三档已足够锁定被测点。",
  },
  {
    slug: "design/color-palette-generator",
    inputs: { baseColor: "#808080" },
    expect: ["字色对比 4.78:1 AA", "白字 3.95", "黑字 4.78"],
    ref: "色块文字对比度（D-N2 修正）：WCAG 相对亮度 —— #808080 线性化后 L≈0.2159；"
      + "白字 #fff 对比度 = 1.05/(0.2159+0.05)=3.95:1、黑字 #111（实际选用色，相对亮度≈0.0056）对比度 = (0.2159+0.05)/(0.0056+0.05)=4.78:1 ⇒ 选黑字并标注 4.78:1 AA。"
      + "修复前错把黑字当成 #000 算成 5.32:1（虚标 AA，实际 #111 仅 4.78 勉强 AA），并误用「白底/黑底」语义（实为白字/黑字）。"
      + "默认基色 #667eea 派生色对比度不含该串 ⇒ 判别明确。",
  },
  {
    slug: "design/generator-6",
    inputs: { cnt: "6" },
    expect: [".shadow-6 { box-shadow:"],
    ref: "随机阴影生成器。`#res` 每条的 `box-shadow` 数值是随机的，本例只锚第 6 条的**结构前缀** `.shadow-6 { box-shadow:`，该串只在 cnt≥6 时出现 ⇒ 条数型判别。\n"
      + "默认态 cnt=5 ⇒ 只有 `.shadow-1`~`.shadow-5`，必然不命中。\n"
      + "⚠ 严禁把随机数值写进 expect，否则每次跑都不同（flaky）。",
  },
  {
    slug: "design/generator-7",
    inputs: { cnt: "7" },
    expect: [".border-7 { border:"],
    ref: "随机边框生成器，锚第 7 条的结构前缀 `.border-7 { border:`。边框样式枚举（solid/dashed/dotted/...）与颜色是随机的，只取结构前缀规避 flaky。默认态 5 条 ⇒ 不命中。",
  },
  {
    // D-N208 默认态：真实 QR 编码（29 字节 → 版本 3 / 29×29 / 纠错 M）
    slug: "design/generator-8",
    expect: ["版本 3 · 29×29 模块 · 纠错 M · 29 字节"],
    ref: "D-N208 强锁：页面改为调用项目内置 js/qrcode.js 真实编码（ISO/IEC 18004）。默认文本 `https://chenguangwu.github.io`（29 字节 UTF-8）在 M 级下由库自动选中版本 3 ⇒ 模块数 4×3+17 = 29。\n"
      + "期望值由 node 独立跑库复算：`qrcode(0,'M') + addData(text,'Byte') + make()` → getModuleCount() = 29、版本 (29-17)/4 = 3，与页面信息行逐字一致。\n"
      + "旧实现只拼「配置参数 #1:」随机文本、不生成任何矩阵，不含该串 ⇒ 强判别。\n"
      + "⚠ harness 原本不加载外部 <script src>；本轮在 verify_it_calc.js 里按「页面 HTML 引用 js/qrcode.js」为条件把构造函数作为 new Function 形参注入，未引用该库的用例行为不变。",
  },
  {
    // D-N208 纠错等级参与版本选择：同一文本 H 级比 M 级高一版
    slug: "design/generator-8",
    inputs: { qrtext: "https://example.com", qrecl: "H" },
    expect: ["版本 3 · 29×29 模块 · 纠错 H · 19 字节"],
    ref: "D-N208 强锁：同一文本在 H 级下需要更多纠错码字，版本被抬高。node 复算 `https://example.com`（19 字节）：L/M/Q 均版本 2（25×25），H 为版本 3（29×29）。\n"
      + "默认态是 M 级版本 2，本用例改 qrecl=H 后取得「版本 3 … 纠错 H」，证明纠错等级真正参与编码而不是只改标签。\n"
      + "⚠ 只注入 qrtext 与 qrecl 两个键，不动 qrsize/qrmargin/qrfg/qrbg，避免颜色变化干扰文本锚点。",
  },
  {
    // D-N208 批量：多行文本各生成一个二维码
    slug: "design/generator-8",
    inputs: { qrtext: "A\nB\nC" },
    expect: ["生成结果：共 3 个二维码（纠错 M，静区 4 模块）"],
    ref: "D-N208：输入框按行切分，每行一个二维码（上限 20 行）。三行 ⇒ 首行汇总写「共 3 个二维码」。默认态 1 行 ⇒ 不含「共 3 个」⇒ 强判别；同时验证空行/去空格逻辑未把换行吞掉。",
  },
  {
    // D-N208 UTF-8 字节计数：中文按 3 字节/字，而非按字符数
    slug: "design/generator-8",
    inputs: { qrtext: "中文测试" },
    expect: ["版本 1 · 21×21 模块 · 纠错 M · 12 字节"],
    ref: "D-N208 强锁：编码按 UTF-8 计字节，`中文测试` 4 个汉字 = 12 字节（每字 3 字节），M 级下落在版本 1 ⇒ 21×21。\n"
      + "若把字节数误写成字符数会显示「4 字节」，与 12 字节的期望不符 ⇒ 本条同时锁住 qrUtf8Len 的多字节处理；旧实现无任何版本/字节信息 ⇒ 强判别。\n"
      + "⚠ 不锚 SVG 属性（如 fill=\"#xxxxxx\"）：collectStrings 剥标签时会把属性整块吞掉，颜色类断言在门禁里恒红，改锁文本信息行。",
  },
  {
    slug: "design/generator-9",
    inputs: { cnt: "6" },
    expect: ["6. EAN-13 条形码"],
    ref: "EAN-13 生成器。12 位随机码 + 确定校验位 ⇒ 数值部分不可锚，只锚第 6 条的序号与标题 `6. EAN-13 条形码`（默认态 5 条 ⇒ 不命中）。校验位算法本身的正确性由页面其它验证路径覆盖，本例只锁「条数随 cnt 增长」。\n"
      + "本页是本批唯一 `errs` 为空的 generator 页（gen 不依赖 `randItem`）。",
  },
  {
    slug: "design/generator-11",
    inputs: { cnt: "6" },
    expect: ["6. 波浪纹理"],
    ref: "纹理生成器。纹理类型序列固定（圆点/条纹/网格/棋盘/斜线/波浪），注入 cnt=6 时第 6 条为波浪纹理；随机色值不进 expect。默认态 5 条 ⇒ 不命中。",
  },
  {
    slug: "design/generator-12",
    inputs: { cnt: "6" },
    expect: ["6. square 粒子方案"],
    ref: "粒子特效生成器。形状枚举按序取（circle/square/...），第 6 条落到 square；粒子数量/速度/色值随机，不进 expect。默认态 5 条 ⇒ 不命中。",
  },
  // ── 第386批 D-N210：输出改为「可运行 HTML + CSS」，animation 真正绑定到粒子节点
  {
    slug: "design/generator-12",
    inputs: { cnt: "50" },
    expect: [
      "animation: float-50 var(--speed) linear infinite",
    ],
    ref: "D-N210 强锁：第 50 条方案必须真正把 animation 绑到粒子选择器上，且 keyframes 名 float-50 与选择器同源。"
      + "旧实现只声明 `--count/--shape` 等变量与 `@keyframes float-N`，全文没有任何选择器写 animation，`--count`/`--shape`/`--speed` 也没被引用 ⇒ 复制的 CSS 跑不出粒子。"
      + "⚠ 只能保留这一条：`50. square 粒子方案` 这类「序号 + 形状」标题新旧实现都有，属零判别力串（首版两条 expect 时旧码也 2/2 通过，已实测）。"
      + "默认态（5 条）只有 float-1..float-5 ⇒ 该串默认不命中，零逃生。",
  },
  // ── 第386批 D-N210 配套：参数控件（每套粒子数 / 周期 / 颜色）必须真正进入输出
  {
    slug: "design/generator-12",
    inputs: { cnt: "1", pcount: "88" },
    expect: ["88 个粒子 ·"],
    ref: "D-N210 配套强锁：`每套粒子数` 输入必须驱动输出，方案说明里出现「88 个粒子 ·」（其后尺寸/周期/扩散仍随机，故只锚到「·」为止）。"
      + "旧实现只有「生成数量」一个输入，粒子数固定随机 20–200，该串永不出现。默认态 pcount 为空 ⇒ 随机值 ⇒ 不命中。",
  },
  {
    slug: "design/generator-12",
    inputs: { cnt: "1", pcolor: "#123456", pspeed: "1.2" },
    expect: ["--color: #123456;"],
    ref: "D-N210 配套强锁：`粒子颜色` 与 `动画周期` 必须写进生成的 CSS 变量。"
      + "注入 #123456 / 1.2 ⇒ 输出含 `--color: #123456;`（颜色取自固定 10 色随机池，不可能撞上 #123456）。"
      + "⚠ 只锚颜色、不锚 `--speed: 1.2s;`：周期在一位小数区间内随机，实测旧码在同一注入下随机到 1.2 而误判通过（已踩坑），属逃生项。",
  },
  {
    slug: "design/favicon-generator",
    inputs: { textInput: "AB", fgColor: "#f43f5e", bgColor: "#0f172a", fontSize: "22", fontWeight: "700" },
    expect: [ "#0f172a" ],
    ref: "浏览器地址栏 favicon 预览 `#browserFavicon` 直接渲染 `textInput` 的首字母组合：默认文本是 `F`（默认文字 'Favicon'），注入 `AB` 后变 `AB` ⇒ 默认态必然不命中。\n ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。"
      + "⚠ 这是「输入 → 结果区文本渲染」型锚，不是纯输入框回显：被测点是**渲染管线**而非回显本身，页面默认值与注入值明确错开。\n"
      + "⚠ `errs` 里的 `canvas.toBlob is not a function` / `draw: ... 'getC...` 是 harness 无 canvas 2d 上下文的产物，不阻断 `#browserFavicon` 写入；`#sizesPreview` 是常量（16×16px…256×256px），不锚。",
  },
  {
    slug: "design/favicon-generator",
    inputs: { textInput: "72" },
    expect: ["72"],
    ref: "覆盖「注入值为纯数字」的分支（首例测字母）。默认态文本 `F` 不命中，注入 `72` 后 `#browserFavicon` 渲染为 `72`。\n"
      + "⚠ 本页只有一个文本结果通道（`#browserFavicon`），因此只拆两例（字母 / 数字），刻意不重复同一形态。",
  },

  // ── BATCH157：CSS 生成类（走 clicks 改层参数）＋ 色板搜索类（空态反用）────
  {
    slug: "design/shadow-generator-advanced",
    clicks: ["layers[0].x=20;layers[0].blur=40;layers[0].alpha=0.5;generate();"],
    expect: ["20px 4px 40px -4px rgba(0,0,0,0.5)"],
    ref: "顶层 var `layers` 每项有 x/y/blur/spread/color/alpha，层内输入框无 id ⇒ 只能走 clicks 直接改字段再 generate()。注入后首层为 x=20/blur=40/alpha=0.5（默认 0/20/0.25），锚首层完整串而非单个数字，避免只改一个字段的弱断言。",
  },
  {
    slug: "design/material-color",
    inputs: { searchInput: "zzzz" },
    expect: ["未找到匹配颜色"],
    ref: "顺序保持型筛选 ⇒ 注入命中词（如 `red`）只会渲染默认态的子集、任何锚都成默认态子串（逃生项），故改走反用：注入无匹配词 `zzzz` ⇒ 落空态。⚠ 该空态安全的前提是零参 `render()` 的 filter 默认为空串、渲染全量、不复现空态；若页面兜底改成带 filter 调用需重评。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  {
    slug: "design/tailwind-colors",
    inputs: { searchInput: "zzzz" },
    expect: ["未找到匹配颜色"],
    ref: "与 material-color 同模板同渲染函数，空态成因与安全性一致；两例同锚但落在不同页，可互相兜住模板改动。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },

  // ── §7.4 零用例加固：design 确定性页（注入非默认 + harness 实测锚）──
  {
    slug: "design/tester-assessor",
    inputs: {
      totalTasks: "6", successTasks: "5", avgTime: "150", expectedTime: "100",
      helpCount: "1", satisfaction: "4",
      sus0: "4", sus1: "4", sus2: "4", sus3: "4", sus4: "4",
      sus5: "4", sus6: "4", sus7: "4", sus8: "4", sus9: "4"
    },
    expect: ["83% (5/6)", "1.50x (150s/100s)", "4/7"],
    ref: "注入非默认(默认 5/4/120/90/2/5)：任务完成率 5/6 = 83%、完成时间比 150/100 = 1.50x、用户满意度 4/7；SUS 十题全选 4 ⇒ 偶数索引(正表述) val−1=3×5=15、奇数索引(反表述) 5−val=1×5=5 ⇒ susSum=20 ⇒ SUS=50.0。⚠ 两条排雷：① harness 判定是『expect 任一子串命中即通过』，而判别器是**一次性把 inputs 全部换回页面默认**；sus0..sus9 由 JS 动态渲染、不在静态 HTML ⇒ 无法回退 ⇒ 失败态 = 默认绩效 + 注入 SUS，实测其任务绩效综合也恰为 73、综合评分也恰为 59 ⇒ **SUS 类锚与综合评分锚在两态相同，一律不可用**，只能锚依赖绩效输入的明细串；② errors 键改 2/1 时错误率评分四舍五入后综合不变 ⇒ 对输出无判别力，不予注入。",
  },
  {
    slug: "design/ripple-effect",
    inputs: { duration: "1.5", size: "320" },
    clicks: ["generate();var t=String(document.getElementById('cssOutput').value);document.getElementById('__tbProbe').textContent='RIP css='+(t.indexOf('animation: rippleAnim 1.5s ease-out')>=0?'Y':'N')+' js='+(t.indexOf('box.addEventListener(')>=0?'Y':'N');"],
    expect: ["RIP css=Y js=Y"],
    ref: "注入非默认(默认 duration=0.8)：生成 CSS 的关键帧时长取注入值（animation: rippleAnim 1.5s ease-out）。D-N95：页面 meta/公式框承诺「导出 CSS/JS」，旧码只输出 CSS ⇒ 修复后 click 型追加可直接粘贴的 JS 片段（事件委托 + 生成 .ripple span，超时时间取 duration）。且断言 css 与 js 两段同时命中，旧码 js=N ⇒ 红；默认态不含该探针串。",
  },
  {
    slug: "design/spinner-generator",
    inputs: { size: "64", speed: "2" },
    expect: ["width: 64px", "animation: spinGen 2s linear infinite"],
    ref: "注入非默认(默认 size=40/speed=1)： spinner 边长取注入的 64px、旋转周期取注入的 2s ⇒ 生成 CSS 含 'width: 64px' 与 'animation: spinGen 2s linear infinite'。默认态为 40px/1s，两条均不命中。",
  },
  {
    slug: "design/flexbox-generator",
    inputs: { gap: "20" },
    expect: ["gap: 20px;"],
    ref: "注入 gap=20（默认 12）⇒ 生成的 CSS 与预览内联 style 里都出现 `gap: 20px;`。expect 带 `gap: ` 前缀与 px 单位，而输入框 value 只是裸值 `20` ⇒ 不与输入回显冲突。默认态输出 `gap: 12px`。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20'><text x='0' y='15'>probeTB2026</text></svg>" },
    clicks: ["generate()"],
    expect: ["probeTB2026"],
    ref: "注入带唯一文本标记 probeTB2026 的 SVG。generate() 对输入做安全清洗后写入 preview.innerHTML，文本节点 probeTB2026 进入输出。注意：采集器会去标签，故标记必须置于 <text> 内容而非 id 属性（属性会被整块吞掉）。默认态 svgInput 为空 ⇒ 输出『请输入 SVG 代码』，不出现 probeTB2026。纯前端无随机。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg xmlns='http://www.w3.org/2000/svg' onload='alert(1)'><script>alert(2)</script><text x='0' y='15'>SVGXSS2026</text></svg>" },
    clicks: ["generate()"],
    expect: ["已移除 SVG 中的不安全脚本或事件属性", "SVGXSS2026"],
    ref: "安全修复判别：注入含 onload 与 <script> 的 SVG。清洗后仍预览 SVGXSS2026，并额外输出『已移除 SVG 中的不安全脚本或事件属性』提示；旧实现直接 innerHTML 原文、无该提示 ⇒ 不命中。默认态无该提示。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg><image href='data:image/svg+xml;base64,PHN2Zz48L3N2Zz4='/><text>SVGB2026</text></svg>" },
    clicks: ["var __r=sanitizeSvg(document.getElementById('svgInput').value);var __h=String(__r.html).toLowerCase();var __bad=(__h.indexOf('<script')>=0||__h.indexOf('<foreignobject')>=0||__h.indexOf('data:image/svg')>=0||__h.indexOf('javascript:')>=0);document.getElementById('__tbProbe').textContent='SVGB2026_CLEAN='+(__bad?'BAD':'OK')+'_RM='+__r.removed+'_DANGER='+__svgStillDangerous(__r.html);"],
    expect: ["SVGB2026_CLEAN=OK_RM=true_DANGER=false"],
    ref: "B 类绕过（data:image/svg+xml 可内嵌脚本）：旧清洗白名单 /^data:image\\// 放行 ⇒ 残留危险串、removed=false；新清洗仅放行位图 data URI ⇒ 该 href 被移除、removed=true，终检不触发。expect 锚清洗后的派生哨兵（非输入回显），默认态 svgInput 为示例 SVG ⇒ RM=false 不命中。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg><scr<script>ipt>alert(3)</scr<script>ipt><text>SVGC2026</text></svg>" },
    clicks: ["var __r=sanitizeSvg(document.getElementById('svgInput').value);var __h=String(__r.html).toLowerCase();var __bad=(__h.indexOf('<script')>=0||__h.indexOf('<foreignobject')>=0||__h.indexOf('data:image/svg')>=0||__h.indexOf('javascript:')>=0);document.getElementById('__tbProbe').textContent='SVGC2026_CLEAN='+(__bad?'BAD':'OK')+'_RM='+__r.removed+'_DANGER='+__svgStillDangerous(__r.html);"],
    expect: ["SVGC2026_CLEAN=OK_RM=true_DANGER=false"],
    ref: "C 类绕过（<scr<script>ipt> 嵌套重组）：旧清洗单次 replace 移除内层后重组出新的 <script>；新清洗循环到不动点 ⇒ 彻底清除。expect 锚清洗后派生哨兵，默认态 RM=false 不命中。",
  },
  {
    slug: "design/svg-viewer",
    inputs: { svgInput: "<svg><foreignObj<foreignObject>ect><div>X</div></foreignObj<foreignObject>ect><text>SVGD2026</text></svg>" },
    clicks: ["var __r=sanitizeSvg(document.getElementById('svgInput').value);var __h=String(__r.html).toLowerCase();var __bad=(__h.indexOf('<script')>=0||__h.indexOf('<foreignobject')>=0||__h.indexOf('data:image/svg')>=0||__h.indexOf('javascript:')>=0);document.getElementById('__tbProbe').textContent='SVGD2026_CLEAN='+(__bad?'BAD':'OK')+'_RM='+__r.removed+'_DANGER='+__svgStillDangerous(__r.html);"],
    expect: ["SVGD2026_CLEAN=OK_RM=true_DANGER=false"],
    ref: "D 类绕过（foreignObject 嵌套重组）：payload 中 <foreignObj<foreignObject>ect> 经旧清洗单次 replace 移除内层后重组出完整 <foreignObject>…</foreignObject>（实测旧码输出该标签对）；新清洗循环到不动点 ⇒ 彻底清除。expect 锚清洗后派生哨兵，默认态 RM=false 不命中。",
  },
  {
    slug: "design/font-preview",
    inputs: { fpText: "ZZPREVZZ" },
    expect: ["ZZPREVZZ"],
    ref: "注入唯一预览文字 ZZPREVZZ。fpText 的 input 监听器更新 state.text 后 render()，将 ZZPREVZZ 渲染进每个可见字体的预览区（escHtml 转义后仍为文本，去标签后保留）。默认态 fpText=『永和九年岁在癸丑』，不出现 ZZPREVZZ。render 纯本地 fonts 对象、不触网，确定性强。 ⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  },
  // ── 零用例收敛（2026-10-09）：design 29 页中仅本页可收敛 ──
  {
    slug: "design/iso-noise-reference",
    inputs: { sensor: "medium", light: "low", camera: "canon_r5", isoRange: "51200" },
    expect: ["中画幅", "佳能 R5 全画幅 · 45MP", "8K视频", "几乎不可见，画质纯净"],
    ref: "注入 sensor=medium（默认 phone）/ light=low（默认 bright）/ camera=canon_r5（默认 sony_a7iv）。三条均经页面 change 监听器 → onISOChange → renderISO 生效，独立复算依据页面内置噪声基准表：medium 画幅 cleanMax=6400 / usableMax=25600、mult=1.5 ⇒ 折算到机身 ISO 的纯净/可用上限为 9600 / 38400；弱光档等效 ISO = 6400×1.3 = 8320。判别锚（均与默认态零撞车）：①『中画幅』（默认渲染『手机 (1/1.3 吋)』）②『佳能 R5 全画幅 · 45MP』（默认 sony_a7iv ⇒『索尼 A7 IV 全画幅 · 33MP』）③『8K视频』（佳能 R5 独有优点，默认 A7 IV 为『对焦优秀、视频强、实时眼部对焦』）④『几乎不可见，画质纯净』（ISO 6400 在 medium+low 下评『优秀』，默认 phone+bright 评『较重』并输出『噪点明显，需要后期降噪』）。⚠️ 不用『原生ISO 100-51200』——默认 A7 IV 同为 100-51200，属逃生串（判别器已实测报出）。纯本地查表，无随机、无时间依赖。",
  },
  // ── 第384批 D-N206：噪点分级阈值统一到「机身 ISO」侧（上限展示 = cleanMax×mult / usableMax×mult）
  {
    slug: "design/iso-noise-reference",
    inputs: { sensor: "medium", isoRange: "20" },
    expect: ["9,600", "38,400"],
    ref: "D-N206 强锁：判定在等效 ISO（机身 ISO ÷ mult）上做，所以统计卡展示的上限必须是 cleanMax×mult / usableMax×mult。"
      + "中画幅 mult=1.5、cleanMax=6400、usableMax=25600 ⇒ 展示 9,600 / 38,400（toLocaleString 带千分位）。"
      + "旧实现直接展示 6400 / 25600，与「ISO 6400 在 medium 下仍判优秀、到 9600 才掉档」自相矛盾 —— 两条 expect 全不命中。"
      + "默认 sensor=aps（mult=0.7）展示 1,120 / 4,480 ⇒ 默认态同样不命中，无逃生。",
  },
  {
    slug: "design/cvd-safe-palette",
    inputs: { csMode: "sequential", csStrategy: "lightness" },
    expect: ["sequential"],
    ref: "⚠ 下拉值回显（结构性不可修）：csMode=sequential / csStrategy=lightness 注入后，模式与策略标签确实变化，但对照组（同一色板）数值锚会在默认态命中 —— 该页主逻辑在 IIFE 内、`change` 监听器读 `this.value` 而 harness 的 fire 不绑定 this、`click()` 又是空操作，故策略无法在同步 stub 内驱动。D-N107（maxmin 空实现）改以独立复算取证（见交接档 2026-11-14-378），此处只保留下拉回显。",
  },
  {
    "slug": "design/avatar-generator",
    "inputs": {
      "seed": "abc123测试",
      "size": "42",
      "radius": "42",
      "c1": "abc123测试",
      "c2": "abc123测试",
      "avatarStyle": "block"
    },
    "expect": [
      "abc123测试\n42\n42\nabc123测试\nabc123测试\nblock\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"seed\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\",\"c1\":\"abc123测试\",\"c2\":\"abc123测试\",\"avatarStyle\":\"block\"}，输出区含「abc123测试\n42\n42\nabc123测试\nabc123测试\nblock\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/analysis-64",
    "inputs": {
      "p1a": "42",
      "p1b": "42",
      "p2a": "42",
      "p2b": "42",
      "p3a": "42",
      "p3b": "42",
      "p4a": "42",
      "p4b": "42",
      "p5a": "42",
      "p5b": "42",
      "scale": "5",
      "bias": "price"
    },
    "expect": [
      "0 功能完整度 20% 5.0 5.0 +0.0 +0.0 使用体验 20% 5.0 5.0 +0.0 +0.0 品牌信任 10% 5.0 5.0 +0.0 +0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p1a\":\"42\",\"p1b\":\"42\",\"p2a\":\"42\",\"p2b\":\"42\",\"p3a\":\"42\",\"p3b\":\"42\",\"p4a\":\"42\",\"p4b\":\"42\",\"p5a\":\"42\",\"p5b\":\"42\",\"scale\":\"5\",\"bias\":\"price\"}，输出区含「0 功能完整度 20% 5.0 5.0 +0.0 +0.0 使用体验 20% 5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/aztec-code",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "#112233",
      "bgColor": "#ffffff",
      "size": "42",
      "ecc": "50"
    },
    "expect": [
      "层数 2 · 紧凑型 · 19×19 模块 · 数据码字 21 · 纠错 50% · 12 字节"
    ],
    "ref": "第390批：真编码接管后重写本用例（原为自动补强的输入回显弱用例）。注入中文混排文本 + 纠错 50% ⇒ 符号必须由内容与纠错率共同决定：12 字节（abc123 六字节 + 两个汉字各 3 字节 UTF-8）在 50% 纠错下升到紧凑型 2 层、19×19、15 个数据码字。旧假实现只有 hash+LCG，输出里没有任何层数/码字信息，默认态（33% + TB-2026-009）得到的是 1 层 15×15 11 码字 ⇒ 双向强判别。"
  },
  {
    "slug": "design/badge-generator",
    "inputs": {
      "text": "abc123测试",
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "radius": "42",
      "fontSize": "42",
      "cssOutput": "1\n2\n3",
      "badgeStyle": "outline"
    },
    "expect": [
      "ckground:transparent;color:abc123测试;border:1px solid abc123测试; }"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"radius\":\"42\",\"fontSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"badgeStyle\":\"outline\"}，输出区含「ckground:transparent;color:abc123测试;bord…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/base64-to-image",
    "inputs": {
      "b64Input": "1\n2\n3"
    },
    "expect": [
      "1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"b64Input\":\"1\\n2\\n3\"}，输出区含「1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/blueprint-grid",
    "inputs": {
      "bgColor": "abc123测试",
      "majorColor": "abc123测试",
      "minorColor": "abc123测试",
      "majorSize": "42",
      "minorSize": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "nd-size: 42px 42px, 42px 42px, 42px 42px, 42px 42px;"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"majorColor\":\"abc123测试\",\"minorColor\":\"abc123测试\",\"majorSize\":\"42\",\"minorSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「nd-size: 42px 42px, 42px 42px, 42px 42px…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/border-radius-generator",
    "inputs": {
      "uniform": "42",
      "tl": "42",
      "tr": "42",
      "br": "42",
      "bl": "42",
      "cssOutput": "1\n2\n3",
      "unit": "%"
    },
    "expect": [
      "-radius: 42%;\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"uniform\":\"42\",\"tl\":\"42\",\"tr\":\"42\",\"br\":\"42\",\"bl\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"unit\":\"%\"}，输出区含「-radius: 42%;\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/button-generator",
    "inputs": {
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "radius": "42",
      "padX": "42",
      "padY": "42",
      "borderColor": "abc123测试",
      "borderW": "42",
      "btnText": "abc123测试",
      "fontSize": "42",
      "shX": "42",
      "shY": "42",
      "shBlur": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\n42\nabc123测试\n5\nabc123测试\n42\n42\n42\n42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"radius\":\"42\",\"padX\":\"42\",\"padY\":\"42\",\"borderColor\":\"abc123测试\",\"borderW\":\"42\",\"btnText\":\"abc123测试\",\"fontSize\":\"42\",\"shX\":\"42\",\"shY\":\"42\",\"shBlur\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\nabc123测试\n42\n42\n42\nabc123测试\n42\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/breakpoint-queries",
    "inputs": {
      "cls": "abc123测试"
    },
    "expect": [
      "40px） */ abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cls\":\"abc123测试\"}，输出区含「40px） */ abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/card-generator",
    "inputs": {
      "bgColor": "abc123测试",
      "radius": "42",
      "shX": "42",
      "shY": "42",
      "shBlur": "42",
      "pad": "42",
      "borderColor": "abc123测试",
      "borderW": "42",
      "shadowColor": "abc123测试",
      "shadowOp": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\n42\n42\n42\n42\n42\nabc123测试\n5\nabc123测试\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"radius\":\"42\",\"shX\":\"42\",\"shY\":\"42\",\"shBlur\":\"42\",\"pad\":\"42\",\"borderColor\":\"abc123测试\",\"borderW\":\"42\",\"shadowColor\":\"abc123测试\",\"shadowOp\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\n42\n42\n42\n42\n42\nabc123测试\n42\nabc1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/checker",
    "inputs": {
      "fgColor": "abc123测试",
      "fgPicker": "abc123测试",
      "bgColor": "abc123测试",
      "bgPicker": "abc123测试"
    },
    "expect": [
      "ABC123测试\nABC123测试\n色值格式无效，请输入 #RRGGBB 或 rgb(r,g,b) 格式\nabc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）· 第339批漂移同步：注入非默认输入{\"fgColor\":\"abc123测试\",\"fgPicker\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgPicker\":\"abc123测试\"}。D-N158 修复后 swapColors 对非法色值不再把原串写回 color input（真实 DOM 会置黑并覆盖文本），末两行由大写回显变为注入原串小写；旧源码差分已证明该漂移来自修复本身。默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/checkerboard-generator",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "size": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "ent 75%, abc123测试 75%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「ent 75%, abc123测试 75%, abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/color-shade-generator",
    "inputs": {
      "hex": "abc123测试",
      "steps": "42"
    },
    "expect": [
      "abc123测试\n明暗梯度 ⚠️ 请输入有效的 HEX 颜色（如 #6366F1）。\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"hex\":\"abc123测试\",\"steps\":\"42\"}，输出区含「abc123测试\n明暗梯度 ⚠️ 请输入有效的 HEX 颜色（如 #6366F1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/colorblind-simulator",
    "inputs": {
      "c1Color": "abc123测试",
      "c1Hex": "abc123测试",
      "c1R": "42",
      "c1G": "42",
      "c1B": "42",
      "c1Sev": "42",
      "c4Fg": "abc123测试",
      "c4FgHex": "abc123测试",
      "c4Bg": "abc123测试",
      "c4BgHex": "abc123测试",
      "c5Base": "abc123测试",
      "c5BaseHex": "abc123测试",
      "c5Count": "42",
      "c2Input": "1\n2\n3",
      "c4Size": "large",
      "c5Mode": "lightness"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\n42\n1 2 3\nlarge\nlightness"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c1Color\":\"abc123测试\",\"c1Hex\":\"abc123测试\",\"c1R\":\"42\",\"c1G\":\"42\",\"c1B\":\"42\",\"c1Sev\":\"42\",\"c4Fg\":\"abc123测试\",\"c4FgHex\":\"abc123测试\",\"c4Bg\":\"abc123测试\",\"c4BgHex\":\"abc123测试\",\"c5Base\":\"abc123测试\",\"c5BaseHex\":\"abc123测试\",\"c5Count\":\"42\",\"c2Input\":\"1\\n2\\n3\",\"c4Size\":\"large\",\"c5Mode\":\"lightness\"}，输出区含「abc123测试\nabc123测试\n42\n42\n42\n42\nabc123测试\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/contrast-checker",
    "inputs": {
      "fgColor": "abc123测试",
      "fgHex": "abc123测试",
      "bgColor": "abc123测试",
      "bgHex": "abc123测试"
    },
      "expect": [
        "灰背景 暖色背景\nabc123测试\nabc123测试\n—\n颜色需为有效的 3 或 6 位 HEX 值"
      ],
      "ref": "自动补强（B类零用例）：注入非默认输入{\"fgColor\":\"abc123测试\",\"fgHex\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgHex\":\"abc123测试\"}；D-N1 修复后 updateAll() 对任一非法 HEX 统一拦截，输出区含「灰背景 暖色背景\nabc123测试\nabc123测试\n—\n颜色需为有效的 3 或 6 位 HEX 值」（修复前 hexToRgb 回退黑色算成 1.00/不达标）；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-animation-generator",
    "inputs": {
      "duration": "42",
      "delay": "42",
      "bx1": "42",
      "by1": "42",
      "bx2": "42",
      "by2": "42",
      "easing": "ease",
      "iteration": "2",
      "direction": "reverse",
      "fillMode": "forwards"
    },
    "expect": [
      " fade-in 42s ease 42s 2 reverse forwards ; }\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"duration\":\"42\",\"delay\":\"42\",\"bx1\":\"42\",\"by1\":\"42\",\"bx2\":\"42\",\"by2\":\"42\",\"easing\":\"ease\",\"iteration\":\"2\",\"direction\":\"reverse\",\"fillMode\":\"forwards\"}，输出区含「 fade-in 42s ease 42s 2 reverse forwards…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-border-radius",
    "inputs": {
      "allRadius": "42",
      "tl1": "42",
      "tl2": "42",
      "tr1": "42",
      "tr2": "42",
      "bl1": "42",
      "bl2": "42",
      "br1": "42",
      "br2": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      " 斜角 ☆ 波浪\n42\n42px\n42\n42\n42\n42\n42\n42\n42\n42\n42%\n42%\n42%\n42%\n42%\n42%\n42%\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"allRadius\":\"42\",\"tl1\":\"42\",\"tl2\":\"42\",\"tr1\":\"42\",\"tr2\":\"42\",\"bl1\":\"42\",\"bl2\":\"42\",\"br1\":\"42\",\"br2\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「 斜角 ☆ 波浪\n42\n42px\n42\n42\n42\n42\n42\n42\n42\n42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-grid-generator",
    "inputs": {
      "cols": "42",
      "gap": "42",
      "containerW": "42"
    },
    "expect": [
      "42\n42\nfr\n42\n列数需在 1-12 之间。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cols\":\"42\",\"gap\":\"42\",\"containerW\":\"42\"}，输出区含「42\n42\n42\n列数需在 1-12 之间。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-box-shadow-generator",
    "inputs": {
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "spread": "42",
      "opacity": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "-shadow: 42px 42px 42px 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"spread\":\"42\",\"opacity\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「-shadow: 42px 42px 42px 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/data-matrix",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/css-text-shadow",
    "inputs": {
      "customText": "abc123测试",
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "opacity": "42",
      "textColor": "abc123测试",
      "textColorText": "abc123测试",
      "fontSize": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "\n#000000\n42\n42px\nabc123测试\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customText\":\"abc123测试\",\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"opacity\":\"42\",\"textColor\":\"abc123测试\",\"textColorText\":\"abc123测试\",\"fontSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「\n#000000\n42\n42px\nabc123测试\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/depth-of-field-calculator",
    "inputs": {
      "focal": "42",
      "aperture": "42",
      "distance": "42",
      "sensor": "1.5"
    },
    "expect": [
      "2.00m ~ ∞\n2.00m 近点清晰 ∞ 远点清晰 2.1m 超焦距"
    ],
    "ref": "自动补强（B类零用例，2026-10-25 去双重裁剪后 h=f²/(N·c)=42²/(42×0.02)=2100mm=2.1m（f/42 光圈、APS-C c=0.02）；s=42m>h ⇒ 仅远点=∞，近点 = h·s/(h+s−f) = 2100×42000/(2100+42000−42) = 2001.9mm → 2.00m。原 expect `—m ~ ∞` 记录的是修复前「近点也误判为 ∞」的缺陷输出（经通用替换成 —），现按正确公式更新。默认态（50mm/1.8/2m/全幅 → 46.4m）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/detector-28",
    "inputs": {
      "formaldehyde": "42",
      "voc": "42",
      "benzeneContent": "42",
      "matType": "paint"
    },
    "expect": [
      "/kg 限值要求：VOC≤80g/L 且苯系物≤50mg/kg 环保等级： 合格品 符合GB 18582标准，可用于室内墙面"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"formaldehyde\":\"42\",\"voc\":\"42\",\"benzeneContent\":\"42\",\"matType\":\"paint\"}，输出区含「/kg 限值要求：VOC≤120g/L 环保等级： 合格品 符合GB 18582…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/detector-28",
    "inputs": {
      "matType": "paint",
      "formaldehyde": "0.05",
      "voc": "20",
      "benzeneContent": "5"
    },
    "expect": [
      "/kg 限值要求：VOC≤30g/L 且苯系物≤10mg/kg 环保等级： 优等品 低VOC环保涂料，适合儿童房和敏感人群使用"
    ],
    "ref": "D-N183 强锁：内墙涂料优等边界 voc=20/bz=5（≤30 且 ≤10）应判优等品，limit 文案须为「VOC≤30g/L 且苯系物≤10mg/kg」。旧实现 limit 写「VOC≤80g/L」（与合格阈值混淆）、公式块/引据也写 80/120，四套口径矛盾；新实现统一为判定值 30/10。默认态（voc 回退默认 80）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/detector-29",
    "inputs": {
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "textSize": "large",
      "targetLevel": "aaa"
    },
    "expect": [
      "Over） AA\nabc123测试\nabc123测试\nlarge\naaa\n颜色格式错误，请输入正确的HEX颜色（如#1F2937）\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textSize\":\"large\",\"targetLevel\":\"aaa\"}，输出区含「Over） AA\nabc123测试\nabc123测试\nlarge\naaa\n颜色格…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/dot-pattern",
    "inputs": {
      "bgColor": "abc123测试",
      "dotColor": "abc123测试",
      "dotSize": "42",
      "spacing": "42",
      "cssOutput": "1\n2\n3",
      "arrangement": "offset"
    },
    "expect": [
      "ckground-position: 0 0, 21px 21px;"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"dotColor\":\"abc123测试\",\"dotSize\":\"42\",\"spacing\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"arrangement\":\"offset\"}，输出区含「ckground-position: 0 0, 21px 21px;」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-from-emoji",
    "inputs": {
      "emoji": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42",
      "radius": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42\nabc123测试 abc123测试 abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"emoji\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\"}，输出区含「abc123测试\nabc123测试\n42\n42\nabc123测试 abc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/farnsworth-d15-test",
    "inputs": {
      "fdSize": "42",
      "fdShuffle": "medium",
      "fdMode": "swap",
      "fdLabel": "none"
    },
    "expect": [
      "基准 ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fdSize\":\"42\",\"fdShuffle\":\"medium\",\"fdMode\":\"swap\",\"fdLabel\":\"none\"}，输出区含「基准 ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀ ▶ ◀…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-from-text",
    "inputs": {
      "text": "abc123测试",
      "bgColor": "abc123测试",
      "textColor": "abc123测试",
      "size": "42",
      "radius": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\n42\nabc123测试 abc123测试 abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\n42\nabc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/flexbox-generator",
    "inputs": {
      "gap": "42",
      "dir": "row-reverse",
      "just": "center",
      "ali": "flex-start",
      "wrap": "wrap"
    },
    "expect": [
      "row-reverse\ncenter"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gap\":\"42\",\"dir\":\"row-reverse\",\"just\":\"center\",\"ali\":\"flex-start\",\"wrap\":\"wrap\"}，输出区含「row-reverse\ncenter」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/favicon-generator",
    "inputs": {
      "textInput": "abc123测试",
      "bgColor": "abc123测试",
      "bgHex": "abc123测试",
      "fgColor": "abc123测试",
      "fgHex": "abc123测试",
      "fontSize": "42",
      "fontWeight": "bold"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\nbold\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"textInput\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"bgHex\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"fgHex\":\"abc123测试\",\"fontSize\":\"42\",\"fontWeight\":\"bold\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\nbold\nabc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/font-preview",
    "inputs": {
      "fpSize": "42",
      "fpSearch": "abc123测试",
      "fpText": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n42\nNaNpx\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fpSize\":\"42\",\"fpSearch\":\"abc123测试\",\"fpText\":\"1\\n2\\n3\"}，输出区含「1 2 3\n42\nNaNpx\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/focal-length-equivalent",
    "inputs": {
      "focal": "42",
      "compareFocal": "42",
      "fromSensor": "aps-c",
      "toSensor": "aps-c"
    },
    "expect": [
      "段类型 视角: 30.0° × 20.2° → 30.0° × 20.2°\n67mm 全画幅等效\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"compareFocal\":\"42\",\"fromSensor\":\"aps-c\",\"toSensor\":\"aps-c\"}，输出区含「段类型 视角: 30.0° × 20.2° → 30.0° × 20.2°\n67…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-10",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "42. .slideUp-"
    ],
    "ref": "注入非默认输入{\"cnt\":\"42\"}，输出区含第 42 条的标题前缀「42. .slideUp-」（八种动画按 i % 8 轮换，41 % 8 = 1 ⇒ 第 42 条必为 slideUp）。原 expect 锚「mation: flip-873 2.7s cubic-bezier(…」依赖随机时长/延迟/缓动与随机后缀，页面源码一改随机序列即位移而假红，改锚确定性结构串；默认态 5 条 ⇒ 不含该串。"
  },
  {
    "slug": "design/generator-11",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "42. 波浪纹理"
    ],
    "ref": "注入非默认输入{\"cnt\":\"42\"}，输出区含第 42 条的标题「42. 波浪纹理」（六种纹理按 i % 6 轮换，41 % 6 = 5 ⇒ 第 42 条必为波浪）。原 expect 锚「(45deg, #00C9A7, #00C9A7 10.75px…」依赖随机双色与随机尺寸，页面源码一改随机序列即位移而假红，改锚确定性结构串；默认态 5 条 ⇒ 不含该串。"
  },
  
  {
    "slug": "design/generator-33",
    "inputs": {
      "total": "42",
      "chapters": "42",
      "minCh": "42",
      "perDay": "42",
      "mode": "four"
    },
    "expect": [
      "00 万 字 / 21 章 转 30% 13 章 12.60 万 字 33.60 万 字 / 34 章 合 20% 8 章 8.40 万 字 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"chapters\":\"42\",\"minCh\":\"42\",\"perDay\":\"42\",\"mode\":\"four\"}，输出区含「00 万 字 / 21 章 转 30% 13 章 12.60 万 字 33.60…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-38",
    "inputs": {
      "target": "abc123测试",
      "constraint": "abc123测试",
      "cnt": "42",
      "task": "优化",
      "format": "表格"
    },
    "expect": [
      "家。 【任务】对「abc123测试」执行优化。 【输出格式】按表格输出 20"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"target\":\"abc123测试\",\"constraint\":\"abc123测试\",\"cnt\":\"42\",\"task\":\"优化\",\"format\":\"表格\"}，输出区含「家。 【任务】对「abc123测试」执行优化。 【输出格式】按表格输出 20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-34",
    "inputs": {
      "slides": "42",
      "minutes": "42",
      "points": "42",
      "fontSize": "42",
      "speed": "180",
      "ratio": "1920x1200"
    },
    "expect": [
      "第 4 页 正文 61.2 s 1.5 s 110 字 第 22 页 正文 61.2 s 1.5 s 110 字 第 39 页 正文 61.2 s 1.5 s 110 字 第 40 页 正文 61.2 s 1.5 s 110 字 第 41 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"slides\":\"42\",\"minutes\":\"42\",\"points\":\"42\",\"fontSize\":\"42\",\"speed\":\"180\",\"ratio\":\"1920x1200\"}，输出区含「第 4 页 正文 61.2 s 1.5 s 110 字 第 22 页 正文 61…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-9",
    "inputs": {
      "bcode": "690123456789",
      "cnt": "42"
    },
    "expect": [
      "完整数字: 6901234567892 | 校验位: 2"
    ],
    "ref": "D-N211 强锁（同时替换原「锚 harness 固定随机序列」的 flaky 用例）：注入 12 位 bcode ⇒ 校验位自动补为 2，且填写固定条码时只输出 1 条（cnt=42 被忽略）。"
      + "原用例锚的是随机生成串（`1 661910 592918 …校验位: 8`），只要任何改动改变了 Math.random 消费次数（本批新增 bcode 输入与编码函数即触发）就会漂，属典型 flaky；"
      + "现改为完全确定性：数字与校验位都由注入值唯一决定。随机不可能撞出 6901234567892 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/generator-9",
    "inputs": {
      "bcode": "6901234567899"
    },
    "expect": [
      "请输入 12 位数字（校验位自动补）或校验位正确的 13 位数字。"
    ],
    "ref": "D-N211 强锁：13 位输入的校验位必须与按前 12 位算出的校验位一致，否则显式报错而不是静默改数。"
      + "690123456789 的正确校验位是 2，注入尾位 9 ⇒ 判错并提示；旧实现没有任何输入框，更不会校验，该串永不出现。"
      + "默认态 bcode 为空（随机生成）⇒ 不命中。"
  },
  {
    "slug": "design/generator-7",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "border-41 {",
      "42. outset 边框"
    ],
    "ref": "注入非默认输入{\"cnt\":\"42\"}，输出区含第 41 条的结构前缀「border-41 {」与第 42 条标题「42. outset 边框」（八种样式轮换，42 % 8 = 2 ⇒ 第 42 条必为 outset）。原 expect 锚「-radius: 26px; } 16. outset」依赖随机圆角，改控件后随机序列位移即失效（且本属 flaky），改锚确定性结构串；默认态 5 条 ⇒ 不含该串。"
  },
  {
    "slug": "design/generator-6",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "-shadow: 7px -13px 9px 1px rgba(59, 130, 246, 0.40), -9px 7px 19px 9px rgba(245, 158, 11, 0.47), -6px 18px 26"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「-shadow: 7px -13px 9px 1px rgba(59, 130,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient",
    "inputs": {
      "angle": "42",
      "cssOutput": "1\n2\n3",
      "gradientType": "radial"
    },
    "expect": [
      "× 100% ×\nradial"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"angle\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"gradientType\":\"radial\"}，输出区含「× 100% ×\nradial」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient",
    "inputs": {
      "cssCheck": "linear-gradient(90deg, #000000 0%, #ffffff 100%)"
    },
    "clicks": [
      "checkContrast()"
    ],
    "expect": [
      "#000000 ↔ #ffffff：21.00:1"
    ],
    "ref": "WCAG 相邻色标对比度：粘贴纯黑(#000000)→纯白(#ffffff)渐变，相对亮度 0 与 1，对比度=(1+0.05)/(0+0.05)=21.00:1。默认 667eea/764ba2 约 1.35:1，输入为空或注入失败即不命中。"
  },
  {
    "slug": "design/grid-pattern",
    "inputs": {
      "bgColor": "abc123测试",
      "lineColor": "abc123测试",
      "cellSize": "42",
      "lineWidth": "8",
      "cssOutput": "1\n2\n3",
      "gridType": "dotted"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n8\ndotted"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"lineColor\":\"abc123测试\",\"cellSize\":\"42\",\"lineWidth\":\"8\",\"cssOutput\":\"1\\n2\\n3\",\"gridType\":\"dotted\"}，输出区含「abc123测试\nabc123测试\n42\n8\ndotted」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。第318批：lineWidth 由 42 改为合法值 8（HTML max=10），因修复后 generate() 会按 1..10 钳制并回写，越界 42 会被回写成 10 而破坏回显锚。"
  },
  {
    "slug": "design/glassmorphism-generator",
    "inputs": {
      "opacity": "42",
      "blur": "42",
      "radius": "42",
      "borderOp": "42",
      "shadow": "42",
      "saturate": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "玻璃 方形玻璃\n\nabc123测试\n42\n42\n42\n42\n42\n42\n0.42\n42px\n42px\n0.42\n0.42\n42%\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"opacity\":\"42\",\"blur\":\"42\",\"radius\":\"42\",\"borderOp\":\"42\",\"shadow\":\"42\",\"saturate\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「玻璃 方形玻璃\n\nabc123测试\n42\n42\n42\n42\n42\n42\n0.42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/gradient-from-color",
    "inputs": {
      "baseColor": "abc123测试",
      "steps": "42",
      "cssOutput": "1\n2\n3",
      "direction": "90"
    },
    "expect": [
      "gradient(90deg, #fd8075 0%, #fc5d4f 11%, #fc3b29 22%, #fb1804 33%, #d51403 44%, #b01103 56%, #8a0d02 67%, #640a02 78%, #"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseColor\":\"abc123测试\",\"steps\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"direction\":\"90\"}，输出区含「gradient(90deg, #fd8075 0%, #fc5d4f 11%,…」（第351批随 D-N126 亮度口径同步更新）；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/identicon-generator",
    "inputs": {
      "seed": "abc123测试",
      "size": "42",
      "bgColor": "abc123测试",
      "blocks": "42"
    },
    "expect": [
      "abc123测试\n42\nabc123测试\n42\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"seed\":\"abc123测试\",\"size\":\"42\",\"bgColor\":\"abc123测试\",\"blocks\":\"42\"}，输出区含「abc123测试\n42\nabc123测试\n42\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-dpi-converter",
    "inputs": {
      "w1": "42",
      "h1": "42",
      "dpi1": "42",
      "w2": "42",
      "h2": "42",
      "dpi2": "42",
      "w3": "42",
      "h3": "42",
      "diag3": "6.1"
    },
    "expect": [
      "线 (mm) 1.0000 宽高比 42 × 42 像素 @ 42 DPI = 25.40 × 25.40 mm\n42\n42\n42\n694 宽度 (像素) 694 高度 (像素) 0.48 MP 总像素 1.0000 宽高比 42 × 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w1\":\"42\",\"h1\":\"42\",\"dpi1\":\"42\",\"w2\":\"42\",\"h2\":\"42\",\"dpi2\":\"42\",\"w3\":\"42\",\"h3\":\"42\",\"diag3\":\"6.1\"}，输出区含「线 (mm) 1.0000 宽高比 42 × 42 像素 @ 42 DPI = …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-cropper",
    "inputs": {
      "cx": "42",
      "cy": "42",
      "cw": "42",
      "ch": "42"
    },
    "expect": [
      "42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cx\":\"42\",\"cy\":\"42\",\"cw\":\"42\",\"ch\":\"42\"}，输出区含「42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-cropper",
    "inputs": { "cx": "12", "cy": "34", "cw": "56", "ch": "78" },
    "clicks": [
      "origImg={width:200,height:160};generate();window.__n1=document.getElementById('dlName').textContent;window.__h1=document.getElementById('downloadLink').href;origImg={width:240,height:180};document.getElementById('cx').value='5';document.getElementById('cy').value='6';document.getElementById('cw').value='70';document.getElementById('ch').value='80';generate();var __n2=document.getElementById('dlName').textContent;var __h2=document.getElementById('downloadLink').href;document.getElementById('dlName').textContent=__n2+'|nameChanged='+(window.__n1!==__n2)+'|hrefSet='+!!__h2+'|hrefFirstSet='+!!window.__h1;"
    ],
    "expect": [
      "cropped_240x180_5-6_70x80.png|nameChanged=true|hrefSet=true|hrefFirstSet=true"
    ],
    "ref": "换图/改参回归：先以 200×160 原图 + 裁剪(12,34,56×78) 生成下载名 cropped_200x160_12-34_56x78.png，再换 240×180 原图并把参数改为(5,6,70×80) 重跑 generate()。断言新文件名为 cropped_240x180_5-6_70x80.png、nameChanged=true（与上一张不同）、下载链接 href 已置为当前 canvas 数据（hrefSet/hrefFirstSet=true）。旧实现下载入口恒指上一张裁剪结果且 href 不随裁剪刷新，本用例不命中。"
  },
  {
    "slug": "design/image-resizer",
    "inputs": {
      "width": "42",
      "height": "42"
    },
    "expect": [
      "42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"height\":\"42\"}，输出区含「42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-rounded-corners",
    "inputs": {
      "radiusSlider": "42",
      "tlSlider": "42",
      "trSlider": "42",
      "blSlider": "42",
      "brSlider": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "gradColor1": "abc123测试",
      "gradColor1Text": "abc123测试",
      "gradColor2": "abc123测试",
      "gradColor2Text": "abc123测试",
      "gradDirection": "to bottom"
    },
    "expect": [
      "42\nundefinedpx\n42\n42\n42\n42\n42\n42\n42\n42\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nabc123测试\nto bottom"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"radiusSlider\":\"42\",\"tlSlider\":\"42\",\"trSlider\":\"42\",\"blSlider\":\"42\",\"brSlider\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"gradColor1\":\"abc123测试\",\"gradColor1Text\":\"abc123测试\",\"gradColor2\":\"abc123测试\",\"gradColor2Text\":\"abc123测试\",\"gradDirection\":\"to bottom\"}，输出区含「42\nundefinedpx\n42\n42\n42\n42\n42\n42\n42\n42\na…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-format-converter",
    "inputs": {
      "qualitySlider": "42",
      "customWidth": "42",
      "customHeight": "42",
      "percentScale": "42"
    },
    "expect": [
      "42\n42%\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"qualitySlider\":\"42\",\"customWidth\":\"42\",\"customHeight\":\"42\",\"percentScale\":\"42\"}，输出区含「42\n42%\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/image-to-ascii",
    "inputs": {
      "width": "42",
      "contrast": "42",
      "brightness": "42"
    },
    "expect": [
      "42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"contrast\":\"42\",\"brightness\":\"42\"}，输出区含「42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/initials-avatar",
    "inputs": {
      "name": "abc123测试",
      "size": "42",
      "radius": "42",
      "fontSize": "42",
      "textColor": "abc123测试",
      "bg1": "abc123测试",
      "bg2": "abc123测试",
      "bgStyle": "custom",
      "letterCount": "2"
    },
    "expect": [
      "abc123测试\n42\n42\n42\nabc123测试\ncustom\nabc123测试\nabc123测试\n2\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"name\":\"abc123测试\",\"size\":\"42\",\"radius\":\"42\",\"fontSize\":\"42\",\"textColor\":\"abc123测试\",\"bg1\":\"abc123测试\",\"bg2\":\"abc123测试\",\"bgStyle\":\"custom\",\"letterCount\":\"2\"}，输出区含「abc123测试\n42\n42\n42\nabc123测试\ncustom\nabc123…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/iso-noise-reference",
    "inputs": {
      "isoRange": "42",
      "sensor": "m43",
      "light": "normal",
      "camera": "sony_a7rv"
    },
    "expect": [
      "焦 ⚠️ 不足： 高感不如低像素机型、文件大 💡 总结： 高像素机型，高感表现尚可，缩图后接近低像素机型"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"isoRange\":\"42\",\"sensor\":\"m43\",\"light\":\"normal\",\"camera\":\"sony_a7rv\"}，输出区含「焦 ⚠️ 不足： 高感不如低像素机型、文件大 💡 总结： 高像素机型，高感表现…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/isometric-grid",
    "inputs": {
      "bgColor": "abc123测试",
      "lineColor": "abc123测试",
      "size": "42",
      "lineWidth": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"lineColor\":\"abc123测试\",\"size\":\"42\",\"lineWidth\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「abc123测试\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/loading-dots",
    "inputs": {
      "color": "abc123测试",
      "count": "42",
      "size": "42",
      "speed": "42",
      "cssOutput": "1\n2\n3",
      "animType": "pulse"
    },
    "expect": [
      "pulse\nabc123测试\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color\":\"abc123测试\",\"count\":\"42\",\"size\":\"42\",\"speed\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"animType\":\"pulse\"}，输出区含「pulse\nabc123测试\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/neomorphism-generator",
    "inputs": {
      "distance": "42",
      "blur": "42",
      "intensity": "42",
      "radius": "42",
      "bgColor": "abc123测试",
      "bgColorText": "abc123测试",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "-shadow: 42px 42px 42px rgba(199, 204, 211, 0.42), -42px -42px 4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"distance\":\"42\",\"blur\":\"42\",\"intensity\":\"42\",\"radius\":\"42\",\"bgColor\":\"abc123测试\",\"bgColorText\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「-shadow: 42px 42px 42px rgba(199, 204, 2…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/material-color",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「abc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/palette-cvd-checker",
    "inputs": {
      "pcPick": "abc123测试",
      "pcInput": "1\n2\n3",
      "pcMetric": "e76"
    },
    "expect": [
      "正常 红色盲 红色弱 绿色盲 绿色弱 蓝色盲 蓝色弱 全色盲\n尚未解析到有效颜色\ne76\n1 2 3\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pcPick\":\"abc123测试\",\"pcInput\":\"1\\n2\\n3\",\"pcMetric\":\"e76\"}，输出区含「正常 红色盲 红色弱 绿色盲 绿色弱 蓝色盲 蓝色弱 全色盲\n尚未解析到有效颜色\ne76\n1 2 3\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/pattern-generator",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "size": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "ent 75%, abc123测试 75%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「ent 75%, abc123测试 75%, abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-aspect-ratio-calculator",
    "inputs": {
      "w": "42",
      "h": "42"
    },
    "expect": [
      "幅 3:1 全景\n42 × 42\n1:1 最简比例 1.000:1 宽高比 0.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"w\":\"42\",\"h\":\"42\"}，输出区含「幅 3:1 全景\n42 × 42\n1:1 最简比例 1.000:1 宽高比 0.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/particle-effect-generator",
    "inputs": {
      "count": "42",
      "psize": "42",
      "speed": "42",
      "gravity": "42",
      "lifetime": "42",
      "linkDist": "42",
      "pColor": "abc123测试",
      "bgColor": "abc123测试"
    },
    "expect": [
      "42\n42\n42\nabc123测试\nabc123测试\n42\n42\n42\n42\n42\n42\n42.00\n42\n∞\n粒子: 42 | FPS: 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"psize\":\"42\",\"speed\":\"42\",\"gravity\":\"42\",\"lifetime\":\"42\",\"linkDist\":\"42\",\"pColor\":\"abc123测试\",\"bgColor\":\"abc123测试\"}，输出区含「42\n42\n42\nabc123测试\nabc123测试\n42\n42\n42\n42\n4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-print-size",
    "inputs": {
      "pw": "42",
      "ph": "42",
      "dpi": "200"
    },
    "expect": [
      "| 需要像素: 1599×2000 (3.2MP) A4 ⚠️ 像素不"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pw\":\"42\",\"ph\":\"42\",\"dpi\":\"200\"}，输出区含「| 需要像素: 1599×2000 (3.2MP) A4 ⚠️ 像素不」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/pixel-art-generator",
    "inputs": {
      "gs": "42"
    },
    "expect": [
      "网格尺寸需在 4-24 之间。"
    ],
    "ref": "注入越界输入{\"gs\":\"42\"}，页面走尺寸校验分支输出「网格尺寸需在 4-24 之间。」；默认态（gs=8 合法）走正常绘制分支、不产生该提示 ⇒ 双态判别明确、零逃生。"
  },
  {
    "slug": "design/pixel-art",
    "inputs": {
      "colorPicker": "abc123测试",
      "colorText": "abc123测试"
    },
    "expect": [
      "\nabc123测试"
    ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
    "ref": "自动补强（B类零用例）：注入非默认输入{\"colorPicker\":\"abc123测试\",\"colorText\":\"abc123测试\"}，输出区含「\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/progress-bar-generator",
    "inputs": {
      "percent": "42",
      "height": "42",
      "color1": "abc123测试",
      "color2": "abc123测试",
      "radius": "42",
      "cssOutput": "1\n2\n3"
    },
    "expect": [
      "42\n42\nabc123测试\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"percent\":\"42\",\"height\":\"42\",\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"radius\":\"42\",\"cssOutput\":\"1\\n2\\n3\"}，输出区含「42\n42\nabc123测试\nabc123测试\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/px-to-rem",
    "inputs": {
      "px": "42",
      "root": "42"
    },
    "expect": [
      "x（1rem = 42px）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"px\":\"42\",\"root\":\"42\"}，输出区含「x（1rem = 42px）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/photo-storage-calculator",
    "inputs": {
      "count": "42",
      "megapixel": "20",
      "format": "raw_uncompressed",
      "bit": "12",
      "cardSize": "64",
      "video": "10"
    },
    "expect": [
      "30.00 MB 单张大小",
      "可存储约 2,113 张照片"
    ],
    "ref": "自动补强（B类零用例）+ 本批修正：20MP×12bit 未压缩 = 30,000,000 B = 30.00 MB；"
      + "64 GB 卡 = 64×10^9 B，10 分钟 1080p 视频按 60 MB/分钟 = 600×10^6 B，"
      + "(64−0.6)×10^9 ÷ 30×10^6 = 2,113.3 ⇒ 2,113 张（旧实现按 1024^3 且不扣视频 ⇒ 2,290 张）。"
      + "默认态（24MP/14bit/RAW/1000 张/64GB/无视频）不含这两个锚 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/png-to-svg",
    "inputs": {
      "blockSize": "42",
      "alphaTh": "42",
      "svgCode": "1\n2\n3"
    },
    "expect": [
      "42\n42\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"blockSize\":\"42\",\"alphaTh\":\"42\",\"svgCode\":\"1\\n2\\n3\"}，输出区含「42\n42\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/qr-code-styled",
    "inputs": {
      "text": "abc123测试",
      "fgColor": "abc123测试",
      "bgColor": "abc123测试",
      "size": "42",
      "ecLevel": "M"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\nM"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"text\":\"abc123测试\",\"fgColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"size\":\"42\",\"ecLevel\":\"M\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\nM」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/rem-to-px",
    "inputs": {
      "rem": "42",
      "root": "42"
    },
    "expect": [
      "42\n42\n转换结果 42rem = 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rem\":\"42\",\"root\":\"42\"}，输出区含「42\n42\n转换结果 42rem = 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/ripple-effect",
    "inputs": {
      "bgColor": "abc123测试",
      "rippleColor": "abc123测试",
      "duration": "42",
      "size": "42",
      "cssOutput": "1\n2\n3",
      "rippleType": "pulse"
    },
    "expect": [
      "pulse\nabc123测试\nabc123测试\n42\n42\n\n.pulse-dot"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bgColor\":\"abc123测试\",\"rippleColor\":\"abc123测试\",\"duration\":\"42\",\"size\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"rippleType\":\"pulse\"}，输出区含「pulse\nabc123测试\nabc123测试\n42\n42\n\n.pulse-do…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/signature-pad",
    "inputs": {
      "strokeWidth": "42",
      "colorPicker": "abc123测试"
    },
    "expect": [
      "42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"strokeWidth\":\"42\",\"colorPicker\":\"abc123测试\"}，输出区含「42\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/shadow-generator",
    "inputs": {
      "offsetX": "42",
      "offsetY": "42",
      "blur": "42",
      "spread": "42",
      "color": "abc123测试",
      "colorText": "abc123测试",
      "inset": "inset"
    },
    "expect": [
      "-shadow: inset 42px 42px 42px 42px abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"offsetX\":\"42\",\"offsetY\":\"42\",\"blur\":\"42\",\"spread\":\"42\",\"color\":\"abc123测试\",\"colorText\":\"abc123测试\",\"inset\":\"inset\"}，输出区含「-shadow: inset 42px 42px 42px 42px abc12…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/shutter-speed-calculator",
    "inputs": {
      "focal": "42",
      "crop": "1.5",
      "is": "2"
    },
    "expect": [
      "42\n1.5\n2\n1/3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"1.5\",\"is\":\"2\"}，输出区含「42\n1.5\n2\n1/3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/skeleton-loader",
    "inputs": {
      "baseColor": "abc123测试",
      "highlightColor": "abc123测试",
      "duration": "42",
      "radius": "42",
      "cssOutput": "1\n2\n3",
      "skelType": "list"
    },
    "expect": [
      "t(90deg, abc123测试 25%, abc123测试 37%, abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseColor\":\"abc123测试\",\"highlightColor\":\"abc123测试\",\"duration\":\"42\",\"radius\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"skelType\":\"list\"}，输出区含「t(90deg, abc123测试 25%, abc123测试 37%, abc…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spacing-scale",
    "inputs": {
      "baseSize": "42",
      "levels": "42",
      "cssOutput": "1\n2\n3",
      "ratio": "1.25"
    },
    "expect": [
      "--space-14: 955px; }"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseSize\":\"42\",\"levels\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"ratio\":\"1.25\"}，输出区含「--space-14: 955px; }」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spinner-generator",
    "inputs": {
      "color": "abc123测试",
      "size": "42",
      "speed": "42",
      "cssOutput": "1\n2\n3",
      "spinType": "dual"
    },
    "expect": [
      "px solid abc123测试; border-bottom"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color\":\"abc123测试\",\"size\":\"42\",\"speed\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"spinType\":\"dual\"}，输出区含「px solid abc123测试; border-bottom」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/stripe-pattern",
    "inputs": {
      "color1": "abc123测试",
      "color2": "abc123测试",
      "angle": "42",
      "width": "42",
      "cssOutput": "1\n2\n3",
      "stripeType": "dashed"
    },
    "expect": [
      "radient(42deg, abc123测试, abc123测试 42px, abc123测试 42px, abc123测试 47px);"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"angle\":\"42\",\"width\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"stripeType\":\"dashed\"}，输出区含「radient(42deg, abc123测试, abc123测试 42px, …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/spectrum-visualizer",
    "inputs": {
      "bars": "42",
      "color1": "abc123测试",
      "color2": "abc123测试",
      "barStyle": "mirror"
    },
    "expect": [
      "42\nmirror\nabc123测试\nabc123测试\n⏸ 暂停"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bars\":\"42\",\"color1\":\"abc123测试\",\"color2\":\"abc123测试\",\"barStyle\":\"mirror\"}，输出区含「42\nmirror\nabc123测试\nabc123测试\n⏸ 暂停」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/svg-minifier",
    "inputs": {
      "svgInput": "1\n2\n3",
      "output": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n1 2 3\n原始: 5 字节 → 压缩后: 5 字节 (节省 0.0% )"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"svgInput\":\"1\\n2\\n3\",\"output\":\"1\\n2\\n3\"}，输出区含「1 2 3\n1 2 3\n原始: 5 字节 → 压缩后: 5 字节 (节省 0.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/svg-to-png",
    "inputs": {
      "width": "42",
      "height": "42",
      "svgInput": "<svg xmlns='http://www.w3.org/2000/svg'><rect width='10' height='10'/></svg>"
    },
    "clicks": ["generate()"],
    "expect": [
      "42 × 42 · 1x · transparent · contain"
    ],
    "ref": "42×42、1x 透明背景生成前输出像素元信息；不依赖输入回显或测试环境中的 Image 实现。"
  },
  {
    "slug": "design/svg-to-png",
    "inputs": {
      "width": "200",
      "height": "100",
      "svgInput": "<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'><rect width='64' height='64'/></svg>"
    },
    "clicks": ["document.getElementById('fitMode').value='stretch';generate()"],
    "expect": ["200 × 100 · 1x · transparent · stretch"],
    "ref": "D-N25 强锁：拉伸铺满模式下 exportMetaVal 同步串含 'stretch'（与默认 contain 区分）。64×64 SVG 在 200×100 画布下若用 contain 会是 100×100 居中，stretch 才是 200×100 铺满 ⇒ 模式串可判别。"
  },
  {
    "slug": "design/tester-assessor",
    "inputs": {
      "totalTasks": "10",
      "successTasks": "7",
      "avgTime": "160",
      "expectedTime": "100",
      "errors": "3",
      "helpCount": "2",
      "userCount": "6",
      "satisfaction": "4",
      "sus0": "5", "sus1": "1", "sus2": "5", "sus3": "1", "sus4": "5",
      "sus5": "1", "sus6": "5", "sus7": "1", "sus8": "5", "sus9": "1"
    },
    "expect": [
      "70% (7/10)",
      "1.60x (160s/100s)",
      "0.3次/任务 (3次)",
      "4/7",
      "86 综合可用性评分"
    ],
    "ref": "重写：原注入裸键 sus（页面只生成 sus0..sus9、calc 循环读 getElementById('sus'+i)，裸 sus 从不被读取 ⇒ 注入落空）。改为真实动态键 sus0..sus9：奇数题(索引偶数)取 5 → (5−1)=4 共 5 题，偶数题(索引奇数)取 1 → (5−1)=4 共 5 题，susSum=40 ⇒ SUS=100 分（默认全 3 ⇒ susSum=20 ⇒ 50 分；且**均匀取值恒为 50 分**——5*(v−1)+5*(5−v)=20，故只有混合取值才能证明这些键真被读取）。绩效锚：成功率 7/10=70%、时间比 160/100=1.60x、错误率 3/10=0.3次/任务、满意度 4 → 4/7；默认 5/4/120/90/3/2/5/5 ⇒ 80% (4/5)、1.33x、0.6次/任务、5/7。末锚「86 综合可用性评分」= taskScore 65.5×(40%) + susScore 100×(60%) = 86.2 → 86，同时依赖绩效注入与 SUS 注入（performance 不变而 sus 落空时得 56、sus 生效而绩效回退时得 89），是证明 sus0..sus9 真被读取的唯一可靠锚。不直接锚「SUS得分（等级A）」——sus* 由 JS 动态生成，discriminate_check 的 pageDefaults 解析不到、无法回退，该锚会恒真成为逃生项。"
  },
  {
    "slug": "design/tailwind-colors",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「abc123测试\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/text-shadow-generator",
    "inputs": {
      "shadowColor": "abc123测试",
      "textColor": "abc123测试",
      "bgColor": "abc123测试",
      "x": "42",
      "y": "42",
      "blur": "42",
      "cssOutput": "1\n2\n3",
      "preset": "hard"
    },
    "expect": [
      "abc123测试\nabc123测试\nabc123测试\n42\n42\n42\nhard"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"shadowColor\":\"abc123测试\",\"textColor\":\"abc123测试\",\"bgColor\":\"abc123测试\",\"x\":\"42\",\"y\":\"42\",\"blur\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"preset\":\"hard\"}，输出区含「abc123测试\nabc123测试\nabc123测试\n42\n42\n42\nhard」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/toast-generator",
    "inputs": {
      "message": "abc123测试",
      "radius": "42",
      "bgColor": "abc123测试",
      "cssOutput": "1\n2\n3",
      "toastType": "error"
    },
    "expect": [
      "error\nabc123测试\n42\n#f44336\n✕ abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"message\":\"abc123测试\",\"radius\":\"42\",\"bgColor\":\"abc123测试\",\"cssOutput\":\"1\\n2\\n3\",\"toastType\":\"error\"}，输出区含「error\nabc123测试\n42\n#f44336\n✕ abc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/vh-vw",
    "inputs": {
      "val": "42",
      "base": "42",
      "mode": "px2vh"
    },
    "expect": [
      "px2vh\n42\n42\n转换结果 42 → 100.0000vh 按视口高度 42px 计算"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"base\":\"42\",\"mode\":\"px2vh\"}，输出区含「px2vh\n42\n42\n转换结果 42 → 100.0000vh 按视口高度 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/typography-scale",
    "inputs": {
      "baseSize": "42",
      "cssOutput": "1\n2\n3",
      "ratio": "1.125",
      "fontFamily": "Georgia, serif"
    },
    "expect": [
      "42\n1.125\nGeorgia, "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"baseSize\":\"42\",\"cssOutput\":\"1\\n2\\n3\",\"ratio\":\"1.125\",\"fontFamily\":\"Georgia, serif\"}，输出区含「42\n1.125\nGeorgia, 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/waveform-visualizer",
    "inputs": {
      "freq": "8",
      "amp": "0.6",
      "phase": "42",
      "color": "abc123测试",
      "waveType": "square"
    },
    "expect": [
      "square\n8\n0.6\n42\nabc123测试\n⏸ 暂停"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"freq\":\"8\",\"amp\":\"0.6\",\"phase\":\"42\",\"color\":\"abc123测试\",\"waveType\":\"square\"}，输出区含「square\n8\n0.6\n42\nabc123测试\n⏸ 暂停」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。第318批：freq/amp 由越界 42 改为合法 8/0.6（HTML 1–20 / 0.1–1），因修复后 drawWave() 会钳制并回写，越界 42 会被回写成 20/1 而破坏回显锚。"
  },
  {
    "slug": "design/web-audio-metronome",
    "inputs": {
      "bpmSlider": "42",
      "vol": "42",
      "beatsPer": "3",
      "sound": "beep"
    },
    "expect": [
      "3\n1 2 3\nNaN\nNaN\n42\nbeep"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bpmSlider\":\"42\",\"vol\":\"42\",\"beatsPer\":\"3\",\"sound\":\"beep\"}，输出区含「3\n1 2 3\nNaN\nNaN\n42\nbeep」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "design/cvd-safe-palette",
    "inputs": {
      "csCount": "42",
      "csMode": "sequential",
      "csStrategy": "lightness"
    },
    "expect": [
      " #0EA5E9\nsequential\n42\nlightness"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"csCount\":\"42\",\"csMode\":\"sequential\",\"csStrategy\":\"lightness\"}，输出区含「 #0EA5E9\nsequential\n42\nlightness」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "design/shadow-generator",
    // S2 设计系统风格预设组（04 批次）：clicks 直调 applyPreset(i)，i 依赖 PRESETS 追加序
    // （原 12 个 index 0-11；追加 Material1=12 / Material4=13 / Neu亮=14 / Neu暗=15 / Glass+=16 / Brutal=17 / TW sm=18 / TW md=19 / TW lg=20 / TW xl=21）。
    // applyPreset → parseShadow（色提尾、数值四元、缺省补 0）→ buildShadowStr 拼 `x y blur spread color`（层间 ', '）→ #code = `box-shadow: ...;`
    inputs: {},
    clicks: ["applyPreset(14);"],
    expect: ["box-shadow: 9px 9px 18px 0px #d1d9e6, -9px -9px 18px 0px #ffffff;"],
    ref: "Neu 亮预设（index 14）：parseShadow('9px 9px 18px #d1d9e6') → x9 y9 blur18 spread0 → '9px 9px 18px 0px #d1d9e6'；第二层 '-9px -9px 18px 0px #ffffff'。默认态 #code='box-shadow: 0px 10px 20px -5px #667eea;' ⇒ 零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: {},
    clicks: ["applyPreset(17);"],
    expect: ["box-shadow: 8px 8px 0px 0px #000000;"],
    ref: "Brutal 预设（index 17）：'8px 8px 0 #000000' → blur=0/spread=0 补 0px。默认态零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: {},
    clicks: ["applyPreset(21);"],
    expect: ["box-shadow: 0px 20px 25px -5px rgba(0,0,0,0.1), 0px 8px 10px -6px rgba(0,0,0,0.1);"],
    ref: "TW xl 预设（index 21，Tailwind shadow-2xl）：两层 rgba 保留原串。默认态零交集。"
  },
  {
    slug: "design/shadow-generator",
    inputs: { offsetX: "6", offsetY: "8", blur: "14", spread: "7", color: "#f43f5e", colorText: "#f43f5e" },
    // setMode('text') 后把预览的内联 textShadow 追加进 code 元素，一次校验导出与预览同步
    clicks: ["setMode('text'); document.getElementById('code').textContent += ' | ' + document.getElementById('preview').style.textShadow;"],
    expect: ["text-shadow: 6px 8px 14px #f43f5e; | 6px 8px 14px #f43f5e"],
    ref: "N4-C text-shadow 只有 offset-x offset-y blur color：即使扩散=7px 也必须省略第 4 个长度值，"
       + "导出声明与预览内联值一致为「6px 8px 14px #f43f5e」。旧实现拼成「6px 8px 14px 7px #f43f5e」，"
       + "整条声明非法；默认 box 模式输出含 spread，本用例只锚文字阴影模式。"
  },
  {
    slug: "design/spinner-generator",
    inputs: { size: "64", speed: "2", spinType: "border" },
    // generate() 后读取预览专用 <style>，用前缀锚定，避免误命中 textarea 里本就存在的一份 keyframes
    clicks: ["document.getElementById('output').textContent = 'PREVIEWSTYLE:' + document.getElementById('spinnerPreviewStyle').textContent;"],
    expect: ["PREVIEWSTYLE:@keyframes spinGen { to { transform: rotate(360deg); } }"],
    ref: "N4-D 预览动画：keyframes 必须真正进入预览样式节点（旧页面从未注入，预览只读到内联 animation 而无"
       + "对应 @keyframes ⇒ 全静止）。前缀 PREVIEWSTYLE 确保区分于 cssOutput 导出文本；默认 generate() 同样"
       + "执行但旧实现该前缀后为空，故可强判别修复前后。"
  },
  {
    slug: "design/mesh-gradient",
    inputs: { overlay: "#000000" },
    expect: ["最低对比度 3.30:1（与 #764ba2）· AA 大文本"],
    ref: "WCAG 改造：默认三色 #667eea/#764ba2/#f093fb，叠加文字注入 #000000 ⇒ 与最暗色 #764ba2 对比度 = (0.1187+0.05)/(0.0353+0.05)=3.30"
       + "（独立复算 sRGB 线性化），等级按 <4.5 判「AA 大文本」。默认态 overlay=#ffffff 输出「最低对比度 2.04:1（与 #f093fb）」，不含该串。"
  },
  {
    slug: "design/mesh-gradient",
    clicks: ["var __seq=[];var _ce=document.createElement.bind(document);document.createElement=function(t){var el=_ce(t);if(t==='canvas'){el.getContext=function(){return{fillRect:function(){},createRadialGradient:function(){return{addColorStop:function(o,c){if(o===0)__seq.push(c);}};},fillStyle:null};};el.toDataURL=function(){return 'data:image/png;base64,';};}return el;};colors=['#ff0000','#0000ff'];pos=[[50,50],[50,50]];var css=meshCSS();var cssFirst=(css.indexOf('#ff0000')>=0&&css.indexOf('#ff0000')<css.indexOf('#0000ff'))?1:0;downloadPNG();document.getElementById('__tbProbe').textContent='MESHLAYER css='+cssFirst+' order='+__seq.join(',')+' ok='+((__seq[__seq.length-1]==='#ff0000')?1:0);"],
    expect: ["MESHLAYER css=1 order=#0000ff,#ff0000 ok=1"],
    ref: "复核失败重做·D-N60 1/2（重合色点层叠顺序）：CSS 多个 background-image 是「第一层在最上」，canvas 却是「后画的覆盖先画的」。把红/蓝两色点都放在 50% 50%，捕获 addColorStop(0,c) 的绘制序列 ⇒ 修复前 order=#ff0000,#0000ff（最后画的蓝覆盖中心，与预览相反，ok=0）；修复后倒序 order=#0000ff,#ff0000，最后画的是 CSS 首层红 ⇒ 预览与 PNG 中心一致。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "design/mesh-gradient",
    clicks: ["var __seq=[];var _ce=document.createElement.bind(document);document.createElement=function(t){var el=_ce(t);if(t==='canvas'){el.getContext=function(){return{fillRect:function(){},createRadialGradient:function(){return{addColorStop:function(o,c){if(o===0)__seq.push(c);}};},fillStyle:null};};el.toDataURL=function(){return 'data:image/png;base64,';};}return el;};colors=['#111111','#222222','#333333'];pos=[[50,50],[50,50],[50,50]];downloadPNG();document.getElementById('__tbProbe').textContent='MESH3 order='+__seq.join(',')+' ok='+((__seq[__seq.length-1]==='#111111'&&__seq[0]==='#333333')?1:0);"],
    expect: ["MESH3 order=#333333,#222222,#111111 ok=1"],
    ref: "复核失败重做·D-N60 2/2（三色重合护栏）：三个色点重合时绘制序列必须严格倒序 #333333,#222222,#111111，证明逆序修复不止对两色成立。修复前为正序 ⇒ ok=0。"
  },
  // ── 照片存储：超容量明示（不再静默夹 100%）────────────────────
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "3000", megapixel: "45", format: "tiff", bit: "16", cardSize: "64", video: "0" },
    expect: ["超出容量：", "476.00 GB"],
    ref: "45MP×16bit×TIFF(×2) = 180,000,000 B/张；3000 张 = 540×10^9 B，64 GB 卡 = 64×10^9 B；"
       + "超出 476×10^9 B ⇒ 必须提示「超出容量：476.00 GB」。旧实现把百分比夹到 100% 且不提示，默认 1000 张也不会超出。",
  },
  {
    slug: "design/photo-storage-calculator",
    inputs: { count: "-1", megapixel: "0", format: "tiff", bit: "16", cardSize: "0", video: "0" },
    expect: ["请填写大于 0 的像素（MP）与存储卡容量"],
    ref: "非法容量/像素必须明确报错，不能靠 Infinity/0 静默出结果；默认 24MP/64GB 不命中该提示。",
  },
  // ── 冲印尺寸：DPI/像素非正数明确报错 ──────────────────────────
  {
    slug: "design/photo-print-size",
    inputs: { pw: "0", ph: "3000", dpi: "300" },
    expect: ["像素尺寸必须为大于 0 的整数"],
    ref: "宽 0 时旧实现 `+value||1` 回退成 1px，静默给出错误的冲印尺寸；现直接提示。默认 3000×2000/300DPI 不命中。",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "3000", ph: "2000", dpi: "0" },
    expect: ["DPI 必须大于 0"],
    ref: "DPI 为 0 时旧实现除零得 Infinity，随后把整个尺寸列表替换成「—」；现给出明确提示。",
  },
  // ── SVG 转 PNG：宽高为 0/负数校验 ─────────────────────────────
  {
    slug: "design/svg-to-png",
    inputs: { width: "0", height: "400" },
    clicks: ["generate()"],
    expect: ["⚠ 宽度和高度必须为正整数"],
    ref: "宽 0 时旧实现 parseInt||400 回退成 400，静默导出与输入不符的图；现直接提示。默认 400×400 不命中。",
  },
  // ── SVG 转 PNG：外部资源净化（防 canvas 被污染）─────────────────
  {
    slug: "design/svg-to-png",
    inputs: {},
    clicks: ["var r=__svgSanitize('<svg xmlns=\"http://www.w3.org/2000/svg\"><foreignObject width=\"10\" height=\"10\"><div xmlns=\"http://www.w3.org/1999/xhtml\">x</div></foreignObject><image href=\"https://evil.example/x.png\" xlink:href=\"https://evil.example/x.png\"/><style>@import url(\"https://evil.example/a.css\");</style></svg>');document.getElementById('exportMetaVal').textContent='FO:'+r.report.foreignObject+' EXT:'+r.report.externalRefs+' CSS:'+r.report.cssRefs+' GONE:'+(r.svg.indexOf('evil.example')>=0?'NO':'YES');"],
    expect: ["FO:1 EXT:2 CSS:1 GONE:YES"],
    ref: "净化口径：foreignObject 整块删除计 1；href 与 xlink:href 两个外链属性各计 1；<style> 内 @import 计 1；净化产物不含 evil.example ⇒ 外链确被剥离。"
      + "门禁无 DOMParser/XMLSerializer ⇒ 走字符串兜底路径，与浏览器 DOM 路径计数口径一致（<style> 文本另计）。"
      + "默认态（空输入）exportMetaVal 为「输出像素：」且不含 FO:/EXT: 串 ⇒ 判别明确。",
  },

  // ── 导出失败必须可见（canvas.toDataURL 抛异常时不得静默）───────
  ...["design/avatar-generator", "design/aztec-code", "design/data-matrix", "design/favicon-from-emoji"].map(function (slug) {
    return {
      slug: slug,
      inputs: {},
      clicks: ["var _ce=document.createElement.bind(document);document.createElement=function(t){var el=_ce(t);if(t==='canvas'){el.toDataURL=function(){throw new Error('boom')};}return el;};generate();"],
      expect: ["⚠ 导出 PNG 失败：Error"],
      ref: "失败注入：把桩内 createElement('canvas') 产物的 toDataURL 改成必抛 Error，再跑 generate() ⇒ 必须在结果区出现可见的「⚠ 导出 PNG 失败：Error」。"
        + "修复前裸调 toDataURL，异常直接冒成 pageerror、页面无任何提示；默认态（不注入）无该文案 ⇒ 判别明确。",
    };
  }),
  // ── px→rem：全角数字/单位后缀解析 + 根字号夹取提示 ────────────
  {
    slug: "design/px-to-rem",
    inputs: { px: "２４px", root: "１６px" },
    expect: ["1.5000rem"],
    ref: "全角数字 ２４＋单位后缀 px 归一为 24，根字号 １６px 归一为 16 ⇒ 24/16 = 1.5000rem；"
       + "旧实现 parseFloat('２４px') = NaN ⇒ 0 ⇒ 输出 0.0000rem。默认 16px/16px ⇒ 1.0000rem，注入失败即不命中。",
  },
  {
    slug: "design/px-to-rem",
    inputs: { px: "100", root: "0" },
    expect: ["根字号必须大于 0，请重新输入"],
    ref: "D-N14：根字号为 0 时旧实现静默改成 16 后继续输出伪结果；现显式提示并清空结果，不再代算。默认 16 不命中。",
  },
  {
    slug: "design/shutter-speed-calculator",
    inputs: { focal: "" },
    expect: ["Enter a valid focal length, crop factor and stabilization stops."],
    ref: "焦距清空后旧实现 +''||50 静默按 50mm 计算安全快门；现显式拦截空值。默认 50 ⇒ 不命中。",
  },
  {
    slug: "design/image-dpi-converter",
    inputs: { w1: "" },
    expect: ["⚠ 计算结果含无效值，请检查输入是否为有效正数。"],
    ref: "像素宽清空后旧实现 ||0 继续算出 0 英寸等伪结果；现由既有 NaN/Infinity 守卫报错。"
       + "默认 3000px ⇒ 不命中。",
  },
  {
    slug: "design/photo-aspect-ratio-calculator",
    inputs: { w: "" },
    expect: ["Enter valid width and height (both positive)."],
    ref: "宽度清空后旧实现 +''||1 静默按 1px 计算比例；现显式要求正数。默认 1920×1080 ⇒ 不命中。",
  },
  {
    slug: "design/detector-28",
    inputs: { formaldehyde: "" },
    expect: ["Enter valid formaldehyde, VOC and benzene values (enter 0 if not detected)."],
    ref: "甲醛清空后旧实现 +''||0 静默按 0 计 ⇒ 直接判「E0 级（优等）」；现显式要求填写（未检出请填 0）。"
       + "默认 0.08 ⇒ 不命中。",
  },
  {
    slug: "design/analysis-64",
    inputs: { p3a: "" },
    expect: ["Fill in both scores for all 5 dimensions (enter 0 explicitly)."],
    ref: "某一维我方得分清空后旧实现 +''||0 静默记 0 分 ⇒ 总分差被放大、结论可能翻转；"
       + "现要求 5 维双方得分齐全（0 分显式填 0）。默认 p3a=9 ⇒ 不命中。",
  },
  {
    slug: "design/focal-length-equivalent",
    inputs: { compareFocal: "" },
    expect: ["Enter a valid focal length (mm)."],
    ref: "对比焦距清空后旧实现 +''||50 静默按 50mm 参与对比 ⇒ 对比表结论变化；现显式要求正数。"
       + "默认 50 ⇒ 不命中。",
  },
  {
    slug: "design/typography-scale",
    inputs: { ratio: "" },
    expect: ["⚠ 比例需为大于 0 且不等于 1 的数值。"],
    ref: "比例清空后旧实现 parseFloat('')||1.2 静默按 1.2 生成整组字阶；现显式提示并清空输出。"
       + "默认 1.25 ⇒ 不命中。",
  },
  {
    slug: "design/spacing-scale",
    inputs: { ratio: "" },
    expect: ["⚠ 请输入有效的基准间距（>0）、比例（>0 且 ≠1）与档位数（正整数）。"],
    ref: "比例清空后旧实现 parseFloat('')||1.25 静默按 1.25 生成整组间距；现三处（基准/比例/档位数）"
       + "统一显式校验。默认 4/1.25/10 ⇒ 不命中。",
  },
  {
    slug: "design/tester-assessor",
    inputs: { totalTasks: "" },
    clicks: ["calc()"],
    expect: ["测试任务总数需为不小于 1 的整数。"],
    ref: "任务总数清空后旧实现 parseFloat('')||1 静默按 1 个任务继续出分（成功率 0% 也会给出总分）；"
       + "现要求全部绩效字段有效且数值合法。默认 5 ⇒ 不命中。",
  },
  {
    slug: "design/photo-print-size",
    inputs: { pw: "", ph: "", dpi: "" },
    clicks: ["ppExportCsv()"],
    expect: ["导出前请先填写有效的像素尺寸与 DPI。"],
    ref: "旧导出路径 +value||1 / ||300 会把空值静默当 1px×1px@300dpi 导出错误清单；"
       + "现导出前显式拒绝并同步清空最大可印尺寸。默认 4032×3024@300 ⇒ 不命中。",
  },
  {
    slug: "design/color-palette",
    inputs: { hexInput: "#F5F5F5" },
    expect: ["黑字 19.26:1 ✔ · 白字 1.09:1 ✘"],
    ref: "黑白字改按 WCAG 对比度取较大者：L(#F5F5F5)=0.913099，黑字 (0.963099)/0.05=19.26:1 ✔、"
       + "白字 1.05/0.963099=1.09:1 ✘。旧阈值 lum>0.5 在 L=0.2369 的 #667eea 上选白字（3.66:1，未过 AA），"
       + "新口径选黑字（5.74:1）。默认 #667eea ⇒ 不含 19.26:1 串。",
  },
  {
    slug: "design/color-picker",
    inputs: { hexInput: "#788EED" },
    expect: ["#000000（6.89:1）"],
    ref: "L(#788EED)=0.294535：黑字 (0.344535)/0.05=6.89:1、白字 1.05/0.344535=3.05:1 ⇒ 应选黑字。"
       + "旧阈值 lum>0.5 会选白字（3.05:1，未过 AA）。默认 #4151e1（L=0.1319）选白字 ⇒ 不含该串。",
  },
  {
    slug: "design/material-color",
    clicks: ["showDetail('Blue',4,'#42a5f5')"],
    expect: ["#000000（7.93:1）"],
    ref: "Material Blue 400 #42a5f5：L=0.346611，黑字 (0.396611)/0.05=7.93:1、白字 2.65:1 ⇒ 应选黑字；"
       + "旧阈值 lum>0.5 选白字（2.65:1）。默认未打开详情（自动调用无参数）⇒ 不含该串。",
  },
  {
    slug: "design/tailwind-colors",
    clicks: ["showDetail('blue',4,'#60a5fa')"],
    expect: ["#000000（8.26:1）"],
    ref: "Tailwind blue-400 #60a5fa：L=0.362992，黑字 (0.412992)/0.05=8.26:1、白字 2.54:1 ⇒ 应选黑字；"
       + "旧阈值 lum>0.5 选白字（2.54:1）。默认未打开详情 ⇒ 不含该串。",
  },
  {
    slug: "design/initials-avatar",
    inputs: { name: "AB" },
    expect: ["文字对比度 10.69:1"],
    ref: "姓名 AB 哈希取调色板 #1dd1a1（WCAG 相对亮度 L=0.4844）：与黑 (0.5344)/0.05=10.69:1、与白 1.05/0.5344=1.96:1 ⇒ 应自动选黑字。"
       + "默认 Tool Box 哈希为 #5f27cd（白字 7.90:1），不含 10.69:1；旧页无对比度输出 ⇒ 注入后必红。",
  },
  {
    slug: "design/initials-avatar",
    inputs: { bgStyle: "custom", bg1: "#777777", textColor: "#ffffff" },
    expect: ["文字对比度 4.48:1", "建议改用 #000000（4.69:1）"],
    ref: "#777777 相对亮度 L=0.1845：白字 1.05/0.2345=4.48:1（<4.5），黑字 0.2345/0.05=4.69:1 ⇒ "
       + "自定义模式应给出具体建议色与比值。默认 hash 模式为 7.90:1 且无「建议改用」，注入后旧实现不命中。",
  },
  {
    slug: "design/bpm-tapper",
    clicks: ["document.getElementById('bpm').innerHTML='SNAP='+computeBpm([0,900,1800]);"],
    expect: ["SNAP=65"],
    ref: "声明「round(实测 BPM ÷ 5) × 5」：三次点击间隔 900ms ⇒ 原始 BPM=60000/900=66.67，"
       + "按 5 取整 = round(13.33)×5=65；旧实现直接 round(66.67)=67。默认 BPM 区不含 SNAP 串。",
  }

,
{
  "slug": "design/color-palette-generator",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-cropper",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-flipper",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-flipper",
  "clicks": ["var _ce=document.createElement.bind(document);document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.toDataURL=function(){return 'data:image/png;base64,AAA';};}return e;};origImg={width:20,height:20};flip('h');flip('h');document.getElementById('__svg_probe').textContent='FLIP2:'+(currentImg?'OK':'NULL');"],
  "expect": ["FLIP2:OK"],
  "ref": "D-N23 回归锁：原 currentImg 仅在 newImg.onload 异步回调里更新，快速连点两次 flip('h') 时第二次仍读旧图、无法还原（FLIP2:NULL）；修复后 currentImg 在每次 flip 内同步设为本次 canvas（canvas 可作 drawImage 源），两次水平翻转即还原（FLIP2:OK）。toDataURL 覆盖为返回测试串以保证翻转流程走完，不依赖真实像素。"
},
{
  "slug": "design/image-format-converter",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-resizer",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-rotator",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-rounded-corners",
  "clicks": ["var g=(typeof window!=='undefined'?window.__svgFileBlocked:null)||(typeof __svgFileBlocked==='function'?__svgFileBlocked:null);document.getElementById('__svg_probe').textContent='SVG:'+(g&&g({name:'evil.svg',type:'image/svg+xml'})?'BLOCK':'PASS')+'|PNG:'+(g&&g({name:'ok.png',type:'image/png'})?'BLOCK':'PASS');"],
  "expect": ["SVG:BLOCK|PNG:PASS"],
  "ref": "C1 上传口径（canvas 污染源根除）：SVG（可含 foreignObject/外链）必须被拒收，位图必须放行。由真机负向自证（21/21）配套覆盖。"
},
{
  "slug": "design/image-color-picker",
  "clicks": ["canvas={width:10,height:10};ctx={getImageData:function(){return {data:[255,0,0,128]};}};var __el={getBoundingClientRect:function(){return {left:0,top:0,width:10,height:10};}};pickColor({clientX:1,clientY:1},__el);document.getElementById('__tbProbe').textContent='ALPHA hex='+document.getElementById('hex').textContent+' rgb='+document.getElementById('rgb').textContent;"],
  "expect": ["ALPHA hex=#FF7F7F rgb=rgb(255, 127, 127)"],
  "ref": "D-N46 回归锁：预览区为白底（.preview-area background:#fff），50% 透明纯红像素在画面上呈现 rgb(255,127,127)，取色必须与之一致。注入 data=[255,0,0,128] 后按白底合成得 #FF7F7F；旧实现直取 RGB 三通道得 #FF0000（且全透明像素得 #000000）⇒ 强判别。探针仅由 clicks 生成，默认态无该串 ⇒ 零逃生。"
},
// ── B 类：导出失败必须可见（toDataURL/toBlob 抛异常或返回 null 时不得静默）──
...[
  {
    slug: "design/color-palette-generator",
    entry: "exportImage()",
    ref: "exportImage() 内 toDataURL 裸调；注入后必须 toast「导出失败：<e.name||e.message>」。",
  },
  {
    slug: "design/image-resizer",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-resizer generate() 内 toDataURL 裸调；注入后必须 toast。默认态（无注入）无该文案 ⇒ 判别明确。",
  },
  {
    slug: "design/image-rotator",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-rotator generate() 内 toDataURL 裸调；注入后必须 toast。",
  },
  {
    slug: "design/image-cropper",
    entry: "origImg={width:20,height:20};generate()",
    ref: "image-cropper generate() 内 toDataURL 裸调（toBlob 链路另有 null 分支）；注入后必须 toast。",
  },
  {
    slug: "design/image-flipper",
    entry: "origImg={width:20,height:20};flip('h')",
    ref: "image-flipper flip() 内 toDataURL 裸调（toBlob 回调原为 if(blob) 静默）；注入后必须 toast。",
  },
].map(function (c) {
  return {
    slug: c.slug,
    inputs: {},
    clicks: [
      // 页面失败提示有两条路径：优先裸 `showToast`（common.js 全局），回落 `ToolBox.showToast`。
      // 保真模式下 common.js 提供了裸全局 ⇒ 只替换 ToolBox.showToast 会被绕过、录音器收不到；
      // 两条都替换，覆盖默认桩与线上真实执行。
      "window.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
      + "ToolBox.showToast=window.showToast;"
      + "window.canvasExportError=window.canvasExportError||function(){return null;};"
      + "var _ce=document.createElement.bind(document);"
      + "document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')};}return e;};"
      + c.entry,
    ],
    expect: ["TOAST:导出失败：Error"],
    ref: "失败注入：把桩内 canvas.toDataURL 改成必抛 Error 并把 ToolBox.showToast 换成录音器，再走真实导出入口 ⇒ 结果区必须出现「TOAST:导出失败：Error」。"
      + "修复前异常裸冒成 pageerror、页面无提示；默认态无 TOAST: 串 ⇒ 判别明确。" + c.ref,
  };
}),
// design/colorblind-simulator 的导出逻辑在外部模块 js/tools/colorblind-simulator.js（IIFE）里，
// 门禁 harness 不加载 /js/tools/*.js ⇒ 模块内 toast() 与 renderImagePane 均不可达，
// 无法做桩级失败注入；改为真机注入（toDataURL 抛 Error / toBlob 回调 null）验证，结果记录在本批回报。
// ── D1 批：B 类余页导出失败可见（新建 canvas 的页面）──
...[
  { slug: "design/favicon-from-text", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },
  { slug: "design/identicon-generator", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },
  { slug: "design/initials-avatar", entry: "generate()", ref: "generate() 的 lastURL 赋值裸调 toDataURL。" },

  { slug: "design/pixel-art", entry: "exportPNG()", ref: "exportPNG() 的 tmp.toDataURL 裸调。" },
  { slug: "design/signature-pad", entry: "strokes.push({});exportPNG();", ref: "exportPNG() 的 tmp.toDataURL 裸调；先塞一条空笔画绕过「请先签名」前置判断。" },
].map(function (c) {
  return {
    slug: c.slug,
    inputs: {},
    clicks: [
      "ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};"
      + "var _ce=document.createElement.bind(document);"
      + "document.createElement=function(t){var e=_ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')};}return e;};"
      + c.entry,
    ],
    expect: ["TOAST:导出失败：Error"],
    ref: "失败注入：canvas.toDataURL 必抛 Error + 录制 ToolBox.showToast ⇒ 必须出现「TOAST:导出失败：Error」。默认态无 TOAST: 串 ⇒ 判别明确。" + c.ref,
  };
}),
{
  "slug": "design/spectrum-visualizer",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var cv=document.getElementById('canvas');cv.toDataURL=function(){throw new Error('boom')};copyResult();"],
  "expect": ["TOAST:导出失败：Error"],
  "ref": "copyResult() 直接对页面 canvas 调 toDataURL（不经 createElement）⇒ 注入该元素 toDataURL 抛 Error + 录制 ToolBox.showToast，必须出现「TOAST:导出失败：Error」；且不得再走 clipboard。",
},
{
  "slug": "design/waveform-visualizer",
  "clicks": ["ToolBox.showToast=function(m){document.getElementById('__svg_probe').textContent='TOAST:'+m;};var cv=document.getElementById('canvas');cv.toDataURL=function(){throw new Error('boom')};copyResult();"],
  "expect": ["TOAST:导出失败：Error"],
  "ref": "copyResult() 直接对页面 canvas 调 toDataURL ⇒ 注入后必须「TOAST:导出失败：Error」，且不得再走 clipboard。",
},
{
  "slug": "design/favicon-generator",
  "clicks": ["var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toBlob=function(){throw new Error('boom')}};return e;};downloadSingle(16);"],
  "expect": ["导出失败：Error"],
  "ref": "失败注入：新建画布的 toBlob 必抛 Error ⇒ downloadSingle 必须 toast「导出失败：Error」。"
     + "修复前异常裸冒成 pageerror、且紧随其后仍弹「已下载 favicon-16x16.png」（失败被成功消息盖掉）；默认态无该串 ⇒ 判别明确。",
},
{
  "slug": "design/favicon-generator",
  "clicks": ["var __ce=document.createElement.bind(document);document.createElement=function(t){var e=__ce(t);if(t==='canvas'){e.toDataURL=function(){throw new Error('boom')}};return e;};copyDataURL();"],
  "expect": ["复制失败：Error"],
  "ref": "失败注入：新建画布的 toDataURL 必抛 Error ⇒ copyDataURL 必须 toast「复制失败：Error」并终止。"
     + "修复前异常裸冒成 pageerror、剪贴板复制提示不执行；默认态无该串 ⇒ 判别明确。",
},
// ── 零覆盖攻坚：font-pairing（成品 CSS 由 FONT_PAIRS 数据驱动，确定性可复算）──
{
  "slug": "design/font-pairing",
  "inputs": {},
  "clicks": ["selectPair(2);"],
  "expect": ["font-family: 'Manrope', sans-serif;", "family=Manrope:wght@700&family=Inter:wght@400"],
  "ref": "selectPair(i) 取 FONT_PAIRS[currentCategory='modern'][2] = {title:'Manrope', body:'Inter', titleWeight:700, bodyWeight:400}，"
     + "把 @import 与 h1..h6/body 两组规则整体写进 #cssOutput.value。故可锚 `family=Manrope:wght@700&family=Inter:wght@400` 与 "
     + "`font-family: 'Manrope', sans-serif;`（标题字体取自数据 title 字段）。默认态未调用 selectPair ⇒ cssOutput 为空，两条均失配。"
},
{
  "slug": "design/font-pairing",
  "inputs": {},
  "clicks": ["setCategory('classic');selectPair(3);"],
  "expect": ["font-family: 'Cormorant Garamond', sans-serif;", "font-weight: 500;"],
  "ref": "setCategory('classic') 切分类后 selectPair(3) 取 FONT_PAIRS.classic[3] = {title:'Cormorant Garamond', body:'Inter', titleWeight:500}，"
     + "标题规则字体名与字重（500，非默认 400/600/700）同时落进 cssOutput。默认态（modern、未选）cssOutput 为空 ⇒ 零交集。"
},
{
  "slug": "design/color-palette",
  "clicks": ["document.getElementById('__tbProbe').textContent=(hexToRgb('#gggggg')===null&&JSON.stringify(hexToRgb('#667eea'))==='[102,126,234]'?'HEXVAL OK':'BAD '+JSON.stringify(hexToRgb('#gggggg')));"],
  "expect": ["HEXVAL OK"],
  "ref": "D-N33：hexToRgb 旧实现只校验长度，parseInt 得 NaN 数组（真值）使调用处 if(rgb) 校验失效 ⇒ 产出 #NaNNaNNaN。修复后加 /^[0-9a-fA-F]{6}$/ 字符校验、非法返回 null。探针断言非法 hex 返回 null 且合法 #667eea 仍正确 ⇒ HEXVAL OK。默认态不生成该哨兵。"
},
// ── 第314批：边界校验与输入同步强锁 ─────────────────────────────
{
  slug: "design/spacing-scale",
  inputs: { baseSize: "6", ratio: "1.4", levels: "20" },
  expect: ["实际生成 15 档"],
  ref: "D-N13：档位数越界旧实现静默夹到 15 且输入框仍显示 20，也没有任何档数标注；修复后在 CSS 首行标注实际档数并把夹取值回写输入框。默认 10 档不含「实际生成 15 档」⇒ 强判别。",
},
{
  slug: "design/px-to-rem",
  inputs: { px: "", root: "16" },
  expect: ["请输入有效的 px 数值与大于 0 的根字号"],
  ref: "D-N14：px 清空旧实现按 0 算出 0.0000rem；修复后显式拦截空值。默认 16 不含该提示 ⇒ 强判别。",
},
{
  slug: "design/rem-to-px",
  inputs: { rem: "", root: "16" },
  expect: ["请输入有效的 rem 数值与大于 0 的根字号"],
  ref: "D-N14：rem 清空旧实现按 0 算出 0.00px；修复后显式拦截空值。默认 1 不含该提示 ⇒ 强判别。",
},
{
  slug: "design/css-grid-generator",
  inputs: { cols: "4", coltype: "fixed", gap: "16", containerW: "960" },
  expect: ["grid-template-columns: repeat(4, 120px)"],
  ref: "D-N27：旧实现 select 无任何 option，注入 fixed 无效、永远走 fr 分支得 repeat(4, 1fr)；修复后补 fr/fixed/auto 三选项，fixed 分支生成 repeat(4, 120px)。默认 fr 不含该串 ⇒ 强判别。",
},
{
  slug: "design/css-grid-generator",
  inputs: { cols: "5", coltype: "fr", gap: "16", containerW: "960" },
  expect: ["&lt;div&gt;3&lt;/div&gt;"],
  ref: "D-N28：旧实现 HTML 结构硬编码 1、2、cols 三个子项，cols=5 时不含第 3 格；修复后按列数循环生成 1..5。默认 3 列不含第 3 格转义串 ⇒ 强判别。",
},
{
  slug: "design/css-grid-generator",
  inputs: { cols: "3", gap: "-10", containerW: "960" },
  expect: ["gap: 0px;"],
  ref: "D-N29：旧实现负 gap 原样拼出 gap: -10px 与负 padding；修复后 clamp 到 0..80 并回写 ⇒ gap: 0px。默认 gap=16 不含该串 ⇒ 强判别。",
},
{
  slug: "design/color-picker",
  inputs: { hInput: "400", sInput: "50", lInput: "50" },
  clicks: ["onHslInput();document.getElementById('formatList').textContent+='|H='+document.getElementById('hInput').value;"],
  expect: ["H=360"],
  ref: "D-N31：旧实现 clampInput 把 400 夹成 360 但不回写正在聚焦的输入框，框内仍显示 400；修复后强制回写 ⇒ H=360。默认 234 不含 ⇒ 强判别。",
},
{
  slug: "design/color-picker",
  inputs: { hexInput: "#11223344" },
  clicks: ["onHexInput();"],
  expect: ["rgb(17, 34, 51)"],
  ref: "D-N32：旧实现 hexToRgb 只接受 3/6 位，8 位 #RRGGBBAA 被判非法、颜色停留默认 #4151e1；修复后支持 8 位并解析 alpha ⇒ rgb(17, 34, 51)。默认态不含 ⇒ 强判别。",
},
{
  slug: "design/shadow-generator-advanced",
  clicks: ["layers[0].x=NaN;generate();if(document.getElementById('cssOutput').value==='')document.getElementById('cssOutput').value='NANGUARD OK';"],
  expect: ["NANGUARD OK"],
  ref: "D-N45：旧实现把 NaN 直接拼进 box-shadow 得 NaNpx，整条声明被浏览器丢弃且无任何提示；修复后有限性守卫清空输出。探针在输出为空时写哨兵 ⇒ NANGUARD OK，旧实现输出非空不写。默认态不含 ⇒ 强判别。",
},
{
  slug: "design/text-shadow-generator",
  inputs: { blur: "-4" },
  clicks: ["generate();if(document.getElementById('cssOutput').value==='')document.getElementById('cssOutput').value='BLURGUARD OK';"],
  expect: ["BLURGUARD OK"],
  ref: "D-N53：旧实现负 blur 原样拼进 text-shadow 使整条声明失效；修复后 blur 必须为 0..50 有限数，非法清空输出。探针在输出为空时写哨兵 ⇒ BLURGUARD OK，旧实现非空不写。默认 blur=4 不含 ⇒ 强判别。",
},
{
  slug: "design/flexbox-generator",
  inputs: { gap: "-10" },
  expect: ["gap: 0px;"],
  ref: "D-N29 同族：旧实现把负 gap 原样拼进 gap: -10px；修复后 clamp 到 0..80 并回写输入框 ⇒ gap: 0px。默认 gap=12 不含该串 ⇒ 强判别。",
},
// ── 第315批：边界钳制与 XSS 转义强锁 ─────────────────────────────
{
  slug: "design/color-temperature-converter",
  inputs: { rgb: "0, 0, 255" },
  expect: ["该颜色不在黑体轨迹附近"],
  ref: "D-N18：纯蓝远离黑体轨迹，旧实现仍返回边界色温 11800K 冒充精确值；修复后残差超阈值时提示无法给出可靠色温。默认输入为合法色温 RGB，不含该提示 ⇒ 强判别。",
},
{
  slug: "design/badge-generator",
  inputs: { text: "<img src=x onerror=alert(1)>" },
  expect: ["&lt;img src=x onerror=alert(1)&gt;"],
  ref: "D-N47：徽章文字旧实现原样拼进 preview.innerHTML，注入的 img 会注册 onerror；修复后先做 HTML 转义再拼接，输出 &lt;img。默认文案 Badge 不含该串 ⇒ 强判别。",
},
{
  slug: "design/card-generator",
  inputs: { borderW: "-1" },
  expect: ["border: 0px"],
  ref: "D-N50：负边框宽旧实现原样输出 border: -1px；修复后 clamp 到 0..5 并回写输入框 ⇒ border: 0px。默认 borderW=1 不含 ⇒ 强判别。",
},
{
  slug: "design/button-generator",
  inputs: { radius: "-5" },
  expect: ["border-radius: 0px"],
  ref: "D-N52：负圆角旧实现输出 border-radius: -5px；修复后 clamp 到 0..50 并回写 ⇒ border-radius: 0px。默认 radius=8 不含 ⇒ 强判别。",
},
{
  slug: "design/css-animation-generator",
  inputs: { easing: "custom", bx1: "-0.5" },
  expect: ["cubic-bezier( 0 ,"],
  ref: "D-N54：x1 越界旧实现输出 cubic-bezier(-0.5, …)；修复后 x1/x2 clamp 到 0..1 并回写 ⇒ cubic-bezier(0, …。默认 easing 非 custom，不含该串 ⇒ 强判别。",
},
{
  slug: "design/pattern-generator",
  inputs: { size: "999" },
  expect: ["background-size: 200px 200px"],
  ref: "D-N62：size=999 旧实现原样输出 background-size: 999px 999px；修复后 clamp 到 5..200 并回写 ⇒ background-size: 200px 200px。默认 size=40 不含 ⇒ 强判别。",
},

// ── 第318批：数值钳制 + 结果区读取 + 复制兜底强锁 ─────────────────
{
  slug: "design/grid-pattern",
  inputs: { cellSize: "999", lineWidth: "999" },
  expect: ["background-size: 200px 200px;"],
  ref: "D-N73：旧实现只夹下限，cellSize=999 直接进 background-size: 999px 999px；修复后 clamp 到 5..200 并回写 ⇒ background-size: 200px 200px;。默认 cellSize=30 不含该串 ⇒ 强判别。",
},
{
  slug: "design/progress-bar-generator",
  inputs: { height: "9999", radius: "-10" },
  expect: ["height: 60px;", "border-radius: 0px;"],
  ref: "D-N74：旧实现 height 无上限、radius 接受负值 ⇒ height: 9999px / border-radius: -10px；修复后 clamp 高度 4..60、圆角 0..50 并回写 ⇒ height: 60px; 与 border-radius: 0px;。默认 20/10 两串皆不含 ⇒ 强判别。",
},
{
  slug: "design/shutter-speed-calculator",
  inputs: { focal: "100000", crop: "2.7", is: "5" },
  clicks: ["calc();"],
  expect: ["焦距超过 2000 mm"],
  ref: "D-N120：旧实现焦距无上限，100000mm×2.7 仍按档位表封顶给出 1/30 的荒谬结论；修复后 f>2000 直接给出越界提示并停止计算。默认焦距 50 不触发 ⇒ 强判别。",
},
{
  slug: "design/waveform-visualizer",
  inputs: { freq: "999", amp: "999" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='CLAMP:'+document.getElementById('freq').value+'|'+document.getElementById('amp').value;"],
  expect: ["CLAMP:20|1"],
  ref: "D-N133：旧实现 amp/freq 越界不拦截，amp=999 使 py 远在画布外；修复后 clamp 到 freq 1..20、amp 0.1..1 并回写 ⇒ 输入框为 20|1。默认 3|0.8 不含该串 ⇒ 强判别。",
},
{
  slug: "design/spectrum-visualizer",
  inputs: { bars: "-8" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='CLAMP:'+document.getElementById('bars').value;"],
  expect: ["CLAMP:8"],
  ref: "D-N136：旧实现 bars=-8 参与 barW=w/-8 计算导致画布空白；修复后 clamp 到 8..120 并回写 ⇒ 输入框为 8。默认 48 不含该串 ⇒ 强判别。",
},
{
  slug: "design/stripe-pattern",
  inputs: { angle: "137", width: "47", color1: "#12b886", stripeType: "multi" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='RES:'+__stripe_patternResText();"],
  expect: ["RES:background: repeating-linear-gradient(137deg, #12b886, #12b886 47px"],
  ref: "D-N163：旧 ResText 读空 #output.textContent 恒返回 ''，历史/CSV 全空；修复后改读 #cssOutput.value ⇒ 探针得到含注入角度/宽度/颜色的 CSS 摘要。旧实现探针只有 RES: ⇒ 强判别。",
},
{
  slug: "design/stripe-pattern",
  inputs: { color1: "#ff0000", color2: "#00ff00", angle: "45", width: "3", stripeType: "double" },
  clicks: ["generate();var __el=document.getElementById('__svg_probe')||document.getElementById('__tbProbe');var __c=document.getElementById('cssOutput').value;var __hasMid=/#00ff00 4px, #ff0000 4px/.test(__c);var __bad=/9px/.test(__c);__el.textContent='STRIPE340_DBL='+(__hasMid?'OK':'BAD')+'_BADPERIOD='+__bad;"],
  expect: ["STRIPE340_DBL=OK_BADPERIOD=false"],
  ref: "D-N164：双线型旧实现内部停点用固定 w+3/w+6，宽度<6 时 w+6>2w 致周期坍缩为 w+6（输出含 9px 且缺 4px 段）；修复后内部细线宽随 w 等比缩放、周期恒 2w（width=3 时末段 6px、含 #00ff00 4px,#ff0000 4px 中段）。注入 width=3 双线：旧码 STRIPE340_DBL=BAD_BADPERIOD=true，新码 OK。锚派生 CSS 而非输入回显 ⇒ 强判别。",
},
{
  slug: "design/dot-pattern",
  inputs: { dotSize: "18", spacing: "54", dotColor: "#22d3ee", arrangement: "square" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='RES:'+__dot_patternResText();"],
  expect: ["RES:background-color: #f5f7fa; background-image: radial-gradient(#22d3ee 9px"],
  ref: "D-N166：旧 ResText 读空 #output 恒返回 ''；修复后改读 #cssOutput.value ⇒ 探针得到含注入点径 9px（dotSize 18 的一半）与点色的 CSS 摘要。旧实现只有 RES: ⇒ 强判别。锚长控制在 ResText 的 slice(0,80) 内。第351批随 D-N126 亮度口径同步更新首色标。",
},
{
  slug: "design/gradient-from-color",
  inputs: { baseColor: "#12b886", steps: "7", direction: "135" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='RES:'+__gradient_from_colorResText();"],
  expect: ["RES:background: linear-gradient(135deg, #89f3d3 0%"],
  ref: "D-N124：旧 ResText 读空 #output 恒返回 ''，历史/趋势/CSV 全空；修复后改读 #cssOutput.value ⇒ 探针得到含注入方向 135deg 与基色首色标的 CSS 摘要。旧实现只有 RES: ⇒ 强判别。",
},
{
  slug: "design/isometric-grid",
  inputs: { size: "64", lineWidth: "3" },
  clicks: ["try{generate();}catch(e){};document.getElementById('__svg_probe').textContent='RES:'+__isometric_gridResText();"],
  expect: ["RES:background-color: #1a1a2e; background-image: linear-gradient(30deg, #667eea 3px"],
  ref: "D-N193：旧 ResText 读只有预览 div 的 #output 恒返回 ''；修复后改读 #cssOutput.value ⇒ 探针得到含注入线宽 3px 的 CSS 摘要。旧实现只有 RES: ⇒ 强判别。锚长控制在 slice(0,80) 内。",
},
{
  slug: "design/gradient-from-color",
  clicks: ["alert=function(m){document.getElementById('__svg_probe').textContent='ALERT:'+m;};document.getElementById('cssOutput').value='SENTINEL_CSS';copyResult();"],
  expect: ["ALERT:复制失败，请手动复制"],
  ref: "D-N127：harness 内 navigator.clipboard 缺失，旧实现 copyResult 直接 writeText 抛 TypeError 静默失败；修复后走 __gfcFallback（execCommand 亦不可用）⇒ catch 给出「复制失败，请手动复制」反馈。默认态不调 copyResult ⇒ 强判别。",
},

// ── 第319批：画布/图片类页面结果区恒空同族强锁 ─────────────────
{
  slug: "design/initials-avatar",
  inputs: { name: "张伟", size: "128", radius: "12", fontSize: "56", textColor: "#123456", bgStyle: "solid", bg1: "#abcdef" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__initials_avatarResText();"],
  expect: ["RES:头像:张伟|128px|圆角12|字号56|solid|#123456"],
  ref: "D-N86：旧 ResText 读只有 img 的 #output.textContent 恒返回空串，历史/数据表/CSV 永不记录；修复后返回姓名、尺寸、圆角、字号、背景模式与色值的参数摘要。探针锚含全部注入值，默认态 name='Tool Box' 不命中 ⇒ 强判别。",
},
{
  slug: "design/identicon-generator",
  inputs: { seed: "workbuddy", size: "256", blocks: "7", bgColor: "#101010" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__identicon_generatorResText();"],
  expect: ["RES:Identicon:workbuddy|256|7|#101010"],
  ref: "D-N89：同族结果区恒空；修复后按清单方案返回 seed|size|blocks|bg 摘要。锚含注入的种子与尺寸，默认 seed='github'/200 不命中 ⇒ 强判别。",
},
{
  slug: "design/waveform-visualizer",
  inputs: { waveType: "square", freq: "7", amp: "0.5", phase: "90", color: "#ff0000" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__waveform_visualizerResText();"],
  expect: ["RES:波形:square|7|0.5|90|#ff0000"],
  ref: "D-N155-1：旧 ResText 读只有 canvas 的 #output 恒空；修复后返回 type|freq|amp|phase|color 参数摘要。锚含注入的方波类型与频率相位，默认 sine|3|0.8 不命中 ⇒ 强判别。",
},
{
  slug: "design/spectrum-visualizer",
  inputs: { bars: "64", barStyle: "mirror", color1: "#112233", color2: "#445566" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__spectrum_visualizerResText();"],
  expect: ["RES:频谱:64|mirror|#112233|#445566"],
  ref: "D-N155-2：旧 ResText 读只有 canvas 的 #output 恒空；修复后返回 bars|style|color1|color2 摘要。锚含注入条数与镜像样式，默认 48|bars 不命中 ⇒ 强判别。",
},
{
  slug: "design/data-matrix",
  inputs: { text: "ORDER-77", size: "18", fgColor: "#111111", bgColor: "#fafafa" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__data_matrixResText();"],
  expect: ["RES:DataMatrix:ORDER-77|18|#111111|#fafafa"],
  ref: "D-N155-3：结果区只有 canvas，旧 ResText 恒空；修复后返回 text|size|fg|bg 摘要。锚含注入文本与尺寸，默认 'Data Matrix'|14 不命中 ⇒ 强判别。",
},
{
  slug: "design/base64-to-image",
  inputs: { b64Input: "data:image/webp;base64,QUJDREVG" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__base64_to_imageResText();"],
  expect: ["RES:Base64:image/webp|"],
  ref: "D-N155-4：结果区只有 img，旧 ResText 恒空；修复后返回 mime|数据长度的摘要。注入 webp 头，默认输入为 image/svg+xml ⇒ 不命中，强判别。",
},
{
  slug: "design/aztec-code",
  inputs: { text: "TICKET-9527", size: "21", fgColor: "#123456", bgColor: "#abcdef" },
  clicks: ["document.getElementById('__svg_probe').textContent='RES:'+__aztec_codeResText();"],
  expect: ["RES:Aztec:TICKET-9527|21|#123456|#abcdef"],
  ref: "D-N179-1：结果区只有 canvas，旧 ResText 恒空且历史钩子错挂在 downloadImg 上；修复后返回文本|尺寸|前景|背景摘要并改挂 generate。锚含注入文本，默认 'Hello Aztec' 不命中 ⇒ 强判别。",
},
{
  slug: "design/aztec-code",
  inputs: { text: "NEW-TEXT" },
  clicks: ["alert=function(m){document.getElementById('__svg_probe').textContent='ALERT:'+m+'|'+document.getElementById('text').value;};lastURL='SENTINEL_PNG';__aztecParams='OLD|#000000|#ffffff|15';downloadImg();"],
  expect: ["ALERT:参数已变更，请先点击生成再下载|NEW-TEXT"],
  ref: "D-N179-2：旧实现 lastURL/预览只在 generate 时刷新，改文本不点生成直接下载会拿到旧 PNG；修复后生成时记录参数快照，下载前比对当前输入，不一致即拦截并提示。探针同时回显注入文本，expect 依赖输入；旧码直接走 a.click() 不产生 alert ⇒ 强判别。",
},

// ── 第390批：Aztec 真实编码（层数/码字/字节随内容与纠错率变化） ──────
{
  slug: "design/aztec-code",
  inputs: { text: "TB-2026-009", ecc: "23", size: "12" },
  expect: ["层数 1 · 紧凑型 · 15×15 模块 · 数据码字 11 · 纠错 23% · 11 字节"],
  ref: "D-N177：旧实现 hash+LCG 随机填格，输出里没有层数/码字概念，任何文本都是同一尺寸；真编码后 11 字节在 23% 纠错下恰好落入紧凑型 1 层、15×15、11 个数据码字。默认态为 33% 纠错（同尺寸但码字/占比不同）⇒ 串含纠错比例，双向可判别。",
},
{
  slug: "design/aztec-code",
  clicks: ["document.getElementById('text').value=Array(201).join('A');document.getElementById('ecc').value='33';generate();"],
  expect: ["层数 7 · 全尺寸 · 45×45 模块 · 数据码字 125 · 纠错 33% · 200 字节"],
  ref: "D-N178：旧实现矩阵尺寸只由滑杆决定、与文本长度无关，10 字符与 200 字符同尺寸。真编码后 200 字节必须升级为全尺寸 7 层、45×45、125 个数据码字 ⇒ 尺寸由 payload 决定。默认文本 TB-2026-009 只有 1 层 15×15 ⇒ 判别明确。",
},
{
  slug: "design/aztec-code",
  inputs: { text: "中文二维码" },
  expect: ["层数 2 · 紧凑型 · 19×19 模块 · 数据码字 26 · 纠错 33% · 15 字节"],
  ref: "非 ASCII 路径：5 个汉字按 UTF-8 编码为 15 字节并写入 ECI 26，符号随之为紧凑型 2 层 / 26 个数据码字。旧实现按 UTF-16 code unit 算 hash，字节数无意义；默认 ASCII 文本得 11 字节 ⇒ 字节数与层数同时变化，判别明确。",
},
{
  slug: "design/aztec-code",
  inputs: { text: "TB-2026-009", size: "1" },
  clicks: ["generate();var _vb=(String(lastSVG).split('viewBox=\"0 0 ')[1]||'').split(' ')[0];document.getElementById('__svg_probe').textContent='SZ='+document.getElementById('size').value+' DIM='+_vb;"],
  expect: ["SZ=4 DIM=92"],
  ref: "D-N178 第二处：旧实现预设 8/10 低于 min=11，输入框显示 8 但矩阵被夹成 11，UI 与实际不符。修复后每模块像素夹到 4–40 并回写输入框，画布与 SVG 用同一夹取后取值（15+4+4 模块 × 4px = 92）。旧实现无 SVG、无回写 ⇒ 三个量全部对不上。",
},
{
  slug: "design/aztec-code",
  inputs: { text: "AZTEC-VERIFY" },
  clicks: ["generate();document.getElementById('__svg_probe').textContent='TAG='+(lastSVG.indexOf('<svg')===0?'OK':'BAD')+' VB='+(/viewBox=\"0 0 276 276\"/.test(lastSVG)?'OK':'BAD')+' BADCOLOR='+(lastSVG.indexOf('#112233')>=0?'Y':'N');"],
  expect: ["TAG=OK VB=OK BADCOLOR=N"],
  ref: "矢量导出：SVG 必须以 <svg 开头、viewBox 覆盖符号加 4 模块留白（(15+8)×12=276），且不得混入未使用的颜色值。旧实现只有 canvas、lastSVG 恒空 ⇒ TAG=BAD VB=BAD，判别明确。",
},

// ── 第320批：网格渐变结果区/预设占位/非法数量强锁 ──────────────
{
  slug: "design/mesh-gradient",
  clicks: ["colors=['#123456','#abcdef','#ff0000'];pos=defaultPos(3);generate();document.getElementById('__svg_probe').textContent='RES:'+__mesh_gradientResText();"],
  expect: ["RES:background-color: #123456; background-image: radial-gradient("],
  ref: "D-N59：旧 ResText 读只有预览 div 的 #output.textContent 恒返回空串，历史/预设/CSV 全空；修复后改读 #cssOutput.value ⇒ 探针得到含注入首色 #123456 的 CSS 摘要。默认首色 #667eea 不命中，旧码只有 RES: ⇒ 强判别。",
},
// 说明：D-N173 的「预设占位 div 是否存在」不写进本门禁——harness 的 getEl 对找不到的 id
// 会造游离桩，getElementById 恒真，构成假绿逃生。该项由 JSDOM 真机（真实 DOM 解析）单独验证。
{
  slug: "design/generator-6",
  inputs: { cnt: "0" },
  clicks: ["try{gen();}catch(e){};var h=document.getElementById('cntHint');document.getElementById('__svg_probe').textContent='HINT:'+(h?h.textContent:'无提示位')+'|CNT:'+document.getElementById('cnt').value;"],
  expect: ["HINT:请输入 1–50 之间的整数|CNT:0"],
  ref: "D-N170：旧实现 parseInt(value)||5 把 0 静默当成 5 且 oninput 键入即重掷整批；修复后 Number.isInteger+范围校验，非法时给出提示且不重掷，并把触发改为 onchange。探针回显注入的 0，旧码无提示位 ⇒ 强判别。",
},

// ── 第321批：阴影层刷新 / 进度条动画共存 / 恢复改重绘 ──────────
{
  slug: "design/css-box-shadow-generator",
  inputs: { offsetX: "37" },
  clicks: ["var o=document.getElementById('cssOutput');try{update();}catch(e){};try{addLayer();}catch(e){};var v=o.value;document.getElementById('__svg_probe').textContent='SHADOW:'+v.split('), ').length+'|X37:'+(v.indexOf('37px')>=0?1:0);"],
  expect: ["SHADOW:2|X37:1"],
  ref: "D-N63：旧 addLayer 只经 setActive→renderLayerList，不调 render，新增层不进 #cssOutput；修复后三处层管理入口补 render。探针先 update() 让注入的 37px 进当前层，再 addLayer() 数 CSS 里的层分隔 ⇒ 修好版 2 层、旧码仍 1 层。expect 含注入值派生的 X37 ⇒ 强判别。",
},
{
  slug: "design/css-text-shadow",
  inputs: { offsetX: "37" },
  clicks: ["var o=document.getElementById('cssOutput');try{update();}catch(e){};try{addLayer();}catch(e){};var v=o.value;document.getElementById('__svg_probe').textContent='SHADOW:'+v.split('), ').length+'|X37:'+(v.indexOf('37px')>=0?1:0);"],
  expect: ["SHADOW:2|X37:1"],
  ref: "D-N64：与 D-N63 同模板缺陷（text-shadow 版）；修复后 addLayer/deleteLayer/resetLayers 均补 render。探针同样依赖注入的 37px 与层数 ⇒ 强判别。",
},
{
  slug: "design/progress-bar-generator",
  inputs: { percent: "37", height: "24", radius: "6" },
  clicks: ["document.getElementById('striped').checked=true;document.getElementById('animated').checked=true;try{generate();}catch(e){};var v=document.getElementById('cssOutput').value;var s='ANIM:'+(v.indexOf('width: 30%;')>=0?1:0)+'|BOTH:'+(v.indexOf('stripes 1s linear infinite, progressAnim')>=0?1:0)+'|PCT:'+document.getElementById('percent').value;document.getElementById('preview').textContent=s;"],
  expect: ["ANIM:1|BOTH:1|PCT:37"],
  ref: "D-N71：旧实现 animated 的 animation 覆盖 striped 的 stripes ⇒ 条纹停滚；@keyframes progressAnim 固定 0/80/100 与输入百分比无关，预览也不显示 pct。修复后两动画合并为一条 animation 声明，关键帧 50% 用 round(pct*0.8)=30%、100% 用 pct，预览回显百分比。探针写 #preview（该页无 __svg_probe 结果位）；旧码 ANIM:0|BOTH:0 ⇒ 强判别，expect 含注入的 37。",
},

// ── 第322批：玻璃拟态背景图案 / Identicon 画廊 ─────────────────
{
  slug: "design/glassmorphism-generator",
  clicks: ["try{setPattern(8);}catch(e){};var e=document.getElementById('bgPattern');var t=String(e.style.cssText||'');var s='BG:'+(t.indexOf('background:')>=0?1:0)+'|SIZE:'+(t.indexOf('background-size')>=0?1:0)+'|IDX:'+currentPattern;document.getElementById('bgPattern').innerHTML=s;document.getElementById('preview').textContent=s;document.getElementById('cssOutput').value=s;document.getElementById('__svg_probe').textContent=s;"],
  expect: ["BG:1|SIZE:1|IDX:8"],
  ref: "D-N67：PATTERNS 存的是纯渐变值（无属性名），旧 setPattern 直接 style.cssText=PATTERNS[i].css、缩略图 style=\"${p.css}\"，CSSOM 会丢弃无属性名的声明 ⇒ 12 种背景图案全不生效。修复后两处均补 'background:' 前缀。选第 8 项「圆点」（含 background-size 多声明），探针回显注入的索引 8；旧码 BG:0 ⇒ 强判别。",
},
{
  slug: "design/identicon-generator",
  inputs: { blocks: "9", bgColor: "#123456" },
  clicks: ["try{generateGallery();}catch(e){};var g=document.getElementById('gallery');document.getElementById('__svg_probe').textContent='G:'+g.getAttribute('data-blocks')+'|'+g.getAttribute('data-bg');"],
  expect: ["G:9|#123456"],
  ref: "D-N88：旧画廊硬编码 blocks=5、底色 #f0f0f0、列数 3，与当前输入脱节；修复后读 #blocks/#bgColor、列数改 ceil(blocks/2)，由 generate() 末尾重绘，并把当前参数写进 #gallery 的 data-blocks/data-bg 便于核对。探针锚含两个注入值；旧码无这两个属性 ⇒ G:null|null，强判别。",
},
{
  slug: "design/favicon-from-text",
  inputs: { size: "9999", radius: "9999" },
  clicks: ["var s0=document.getElementById('size').value;generate();document.getElementById('__svg_probe').textContent='IN:'+s0+'|CLAMP:'+document.getElementById('size').value+'|'+document.getElementById('radius').value;"],
  expect: ["IN:9999|CLAMP:256|128"],
  ref: "D-N76：旧码 size 只夹下限、radius 只夹下限，注入 9999 直接建 9999px 画布且半径远超半边长导致贝塞尔路径自交；修复后 size 夹到 16–256、radius 夹到 ≤size/2 并回写输入框。探针回显注入原值 9999；旧码 CLAMP:9999|9999 ⇒ 强判别。",
},
{
  slug: "design/favicon-from-text",
  inputs: { text: "ZX", size: "128", radius: "24" },
  clicks: ["generate();var h=String(document.getElementById('preview').innerHTML);var rad=(h.match(/border-radius:[0-9.]+px/g)||[]).map(function(x){return x.replace(/[^0-9.]/g,'');}).join('|');var fs=(h.match(/font-size:[0-9.]+px/g)||[]).map(function(x){return x.replace(/[^0-9.]/g,'');}).join('|');document.getElementById('__svg_probe').textContent='RAD:'+rad+' FS:'+fs+' IN:'+document.getElementById('size').value+'/'+document.getElementById('radius').value;"],
  expect: ["RAD:3|12|24 FS:8.8|35.2|70.4 IN:128/24"],
  ref: "D-N75：旧码三档预览按固定 64/128 参照缩放（radius/64*8、radius、radius*2），且只有中档给字号；修复后统一按 radius÷size×档位边长（16/64/128 px），三档字号均按 ×0.55 比例给 8.8/35.2/70.4px。旧码 RAD:3|24|48 FS:35.2 ⇒ 强判别，expect 含注入的 128/24。",
},
{
  slug: "design/favicon-from-text",
  inputs: { text: "Q7" },
  clicks: ["var cap=null;globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(sel,items,c){cap=items;}}};__favicon_from_textPresets();var bad=cap?cap.filter(function(x){return String(x.values.text).length>2;}).map(function(x){return x.values.text;}):['NONE'];document.getElementById('__svg_probe').textContent='IN:'+document.getElementById('text').value+'|PRESET:'+(bad.length?bad.join(','):'OK')+'|N:'+(cap?cap.length:0);"],
  expect: ["IN:Q7|PRESET:OK|N:4"],
  ref: "D-N79：输入框标注 1–2 字符且 maxlength=2，旧预设却写入 3 字符 API（程序赋值绕过 maxlength）；修复后预设改双字 AB。探针用桩捕获 __favicon_from_textPresets() 传给 TBKit.preset.bar 的全部条目并校验 text 长度；旧码 PRESET:API ⇒ 强判别，expect 含注入的 Q7。",
},
{
  slug: "design/favicon-from-emoji",
  inputs: { size: "9999", radius: "9999" },
  clicks: ["var s0=document.getElementById('size').value;generate();document.getElementById('__svg_probe').textContent='IN:'+s0+'|CLAMP:'+document.getElementById('size').value+'|'+document.getElementById('radius').value;"],
  expect: ["IN:9999|CLAMP:256|128"],
  ref: "D-N82：旧码 size 只夹下限、radius 只夹下限，HTML max=256/100 不参与脚本校验，默认 128 下 radius=100 即生成自交路径；修复后 size 夹到 16–256、radius 夹到 ≤size/2 并回写输入框。探针回显注入原值 9999；旧码 CLAMP:9999|9999 ⇒ 强判别。",
},
{
  slug: "design/favicon-from-emoji",
  inputs: { emoji: "FOX", size: "64", radius: "24" },
  clicks: ["generate();var h=String(document.getElementById('preview').innerHTML);var rad=(h.match(/border-radius:[0-9.]+px/g)||[]).map(function(x){return x.replace(/[^0-9.]/g,'');}).join('|');document.getElementById('__svg_probe').textContent='RAD:'+rad+' IN:'+document.getElementById('size').value+'/'+document.getElementById('radius').value;"],
  expect: ["RAD:6|24|48 IN:64/24"],
  ref: "D-N80：旧码三档预览固定按 128 参照缩放（radius/128*16、radius/2、radius），改 size 后比例失真；修复后按 radius÷size×档位边长（16/64/128 px）。注入 size=64/radius=24 期望 6|24|48；旧码 3|12|24 ⇒ 强判别。",
},
{
  slug: "design/initials-avatar",
  inputs: { name: "😀 Smith" },
  clicks: ["var a=computeInitials(document.getElementById('name').value,2);var b=computeInitials(document.getElementById('name').value,1);document.getElementById('__svg_probe').textContent='INI:'+a+'|'+b+'|LEN:'+Array.from(a).length;"],
  expect: ["INI:😀S|😀|LEN:2"],
  ref: "D-N84：旧码 parts[0][0] / substring / initials[0] 按 UTF-16 码位切分，emoji 名称会切出孤立高位代理字符；修复后抽 computeInitials() 用 Array.from 按码点取首字符。注入 😀 Smith 期望双字 😀S、单字 😀、码点数 2；旧码无该函数且切出代理字符 ⇒ 强判别。",
},
{
  slug: "design/ripple-effect",
  inputs: { rippleType: "pulse", rippleColor: "#ff0000", duration: "1.2" },
  clicks: ["generate();var h=String(document.getElementById('preview').innerHTML);var c=String(document.getElementById('cssOutput').value);var s='COL:'+document.getElementById('rippleColor').value+'|HTML:'+(h.indexOf('#ff0000')>=0?1:0)+'|CSS:'+(c.indexOf('#ff0000')>=0?1:0);document.getElementById('__svg_probe').textContent=s;document.getElementById('cssOutput').value=s;document.getElementById('preview').textContent=s;"],
  expect: ["COL:#ff0000|HTML:1|CSS:1"],
  ref: "D-N94（脉冲）：旧码 r/g/b 只用于点击模式，脉冲模式的圆环与导出 CSS 全用背景色，涟漪色输入被静默吞掉；修复后圆环 border 与 .pulse-ring 都用 rippleColor。探针多载体写入（该页 __svg_probe 不进采集区）；旧码 HTML:0|CSS:0 ⇒ 强判别，expect 含注入的 #ff0000。",
},
{
  slug: "design/ripple-effect",
  inputs: { rippleType: "multi", rippleColor: "#ff0000", duration: "1.2" },
  clicks: ["generate();var h=String(document.getElementById('preview').innerHTML);var c=String(document.getElementById('cssOutput').value);var s='COL:'+document.getElementById('rippleColor').value+'|HTML:'+(h.indexOf('#ff0000')>=0?1:0)+'|CSS:'+(c.indexOf('#ff0000')>=0?1:0);document.getElementById('__svg_probe').textContent=s;document.getElementById('cssOutput').value=s;document.getElementById('preview').textContent=s;"],
  expect: ["COL:#ff0000|HTML:1|CSS:1"],
  ref: "D-N94（多重）：旧码三个圆点与 .multi-pulse div 全用背景色；修复后预览与导出都取 rippleColor。注入 #ff0000 后两处均应出现；旧码 HTML:0|CSS:0 ⇒ 强判别。",
},
{
  slug: "design/qr-code-styled",
  inputs: { text: "HELLO-324", size: "300" },
  clicks: ["qrcode=function(){throw new Error('boom');};lastURL='OLDPNG-324';generate();document.getElementById('__svg_probe').textContent='IN:'+document.getElementById('text').value+'|URL:'+String(lastURL)+'|END';"],
  expect: ["IN:HELLO-324|URL:|END"],
  ref: "D-N12（失败分支）：旧码 lastURL 只在生成成功回调里写，生成抛错等失败分支只改预览文案，上一次的码仍可下载；修复后 generate() 开头先清空 lastURL。第390批修正：第389批让 harness 注入真实 qrcode 后，本页不再必然走「库未定义」分支（原断言随之常红），改为显式注入必抛异常的编码器，仍锁定同一失败分支；旧码 URL:OLDPNG-324 ⇒ 强判别，expect 含注入文本。",
},
{
  slug: "design/qr-code-styled",
  inputs: { text: "HELLO-324" },
  clicks: ["var orig=document.getElementById('text').value;lastURL='OLDPNG-324';lastQRSig=__qrSig();document.getElementById('text').value='CHANGED-324';document.getElementById('__svg_probe').textContent='IN:'+orig+'|STALE:'+(__qrStale()?1:0);"],
  expect: ["IN:HELLO-324|STALE:1"],
  ref: "D-N12（参数快照）：修复后生成时记录 text/fg/bg/size/ecLevel 签名，下载或复制前比对当前输入；改文本后 __qrStale() 为真。旧码无该组函数，探针抛错 ⇒ 强判别，expect 含注入的 HELLO-324。",
},
{
  slug: "design/qr-code-styled",
  inputs: { text: "HELLO-324" },
  clicks: ["var orig=document.getElementById('text').value;lastURL='OLDPNG-324';lastQRSig='OLD-SIG';var clicked=0;var oc=document.createElement;document.createElement=function(t){var e=oc(t);if(t==='a'){e.click=function(){clicked++;};}return e;};downloadImg();document.createElement=oc;document.getElementById('__svg_probe').textContent='IN:'+orig+'|CLICK:'+clicked+'|URL:'+String(lastURL)+'|END';"],
  expect: ["IN:HELLO-324|CLICK:0|URL:|END"],
  ref: "D-N12（下载拦截）：签名过期时 downloadImg() 必须清空 lastURL 并提示，绝不触发 a.click()。桩捕获 a 元素的 click 次数；旧码直接下载旧图 ⇒ CLICK:1|URL:OLDPNG-324，强判别。",
},
{
  slug: "design/image-rotator",
  inputs: { angle: "45" },
  clicks: ["var orig=document.getElementById('angle').value;origImg={width:20,height:20};lastURL='OLDPNG-324';lastIrotSig=__irotSig();document.getElementById('angle').value='135';document.getElementById('__svg_probe').textContent='IN:'+orig+'|STALE:'+(__irotStale()?1:0);"],
  expect: ["IN:45|STALE:1"],
  ref: "D-N11：旧码上传换图与改角度都不使 lastURL 失效，下载直取旧图；修复后生成时记录「角度 + 原图 src 尾段」签名，下载/复制前比对，上传回调另立即清空。注入 angle=45 后改 135 判过期；旧码无该组函数 ⇒ 强判别。",
},
{
  slug: "design/image-cropper",
  inputs: { cw: "37" },
  clicks: ["var orig=document.getElementById('cw').value;origImg={width:200,height:200};lastURL='OLDPNG-324';lastCropSig=__icropSig();document.getElementById('cw').value='88';document.getElementById('__svg_probe').textContent='IN:'+orig+'|STALE:'+(__icropStale()?1:0);"],
  expect: ["IN:37|STALE:1"],
  ref: "D-N26：旧码换图已失效但改 cx/cy/cw/ch 仍可下载上一张旧裁剪；修复后生成时记录「四个裁剪参数 + 原图 src 尾段」签名，下载/复制前比对并撤销旧 blob URL。注入 cw=37 后改 88 判过期；旧码无该组函数 ⇒ 强判别。",
},
// ── 第341批：design 多缺陷批量强锁 ───────────────────────────────
{
  slug: "design/generator-7",
  clicks: ["var bad=0;for(var i=0;i<200;i++){gen();var h=document.getElementById('res').innerHTML;var re=/border:\\s*(\\d+)px\\s+double/g;var m;while((m=re.exec(h))){if(parseInt(m[1],10)<3)bad++;}}document.getElementById('__tbProbe').textContent='G7DBL='+bad;"],
  expect: ["G7DBL=0"],
  ref: "D-N202 回归：double 在 1–2px 时浏览器按 solid 渲染，预览与 solid 无差异。修复后 gen() 在 style==='double' 且 width<3 时把 width 提升到 3。跑 200 次生成、每次扫描 #res 内所有 `border: Npx double`，任一 N<3 计 bad。修复前约出现数十个 width=1/2 的 double 卡 ⇒ G7DBL>0；修复后恒 0。默认态（页面加载时也 gen() 一次）不产生该探针串。"
},
{
  slug: "design/exposure-triangle-calculator",
  inputs: { aperture: "2" },
  clicks: ["calc();var h=document.getElementById('equiv').innerHTML;var c=(h.match(/f\\/1\\.4</g)||[]).length;document.getElementById('__tbProbe').textContent='EXP_DUP='+c;"],
  expect: ["EXP_DUP=1"],
  ref: "D-N118 回归（重复卡片）：光圈选 f/2（index 1）时，da=-2 与 da=-1 均被 clamp 到 na=0（f/1.4）且 neededSi 相同，旧实现生成两张完全一样的 f/1.4 卡片。修复后按 na 去重，#equiv 中 `f/1.4<` 仅 1 次。注入 aperture='2'（非默认 f/4），旧实现下 EXP_DUP=2。"
},
{
  slug: "design/exposure-triangle-calculator",
  clicks: ["toggleLock();var s0=document.getElementById('shutter').selectedIndex;changeExp(-1);var s1=document.getElementById('shutter').selectedIndex;var lb=String(document.getElementById('lockBtn').textContent);changeExp(1);var s2=document.getElementById('shutter').selectedIndex;document.getElementById('aperture').value='8';calc();document.getElementById('__tbProbe').textContent='LOCK_SH='+document.getElementById('shutter').value+' d1='+(s1-s0)+' d2='+(s2-s1)+' L='+(lb.indexOf('解锁曝光 (EV ')>=0?'SYNC':'NOSYNC');"],
  expect: ["LOCK_SH=1/15 d1=-1 d2=1 L=SYNC"],
  ref: "D-N118 回归（锁定曝光）：默认 f/4·1/60·ISO200 锁定 EV≈8.9 后，把光圈改为 f/8，锁定逻辑应自动调快门维持 EV。t=64/2^(8.907+log2(200/100))=64/2^9.907≈0.0667s ⇒ 最近档 1/15。旧实现「🔒 锁定曝光」按钮只调 calc() 无任何锁定，改光圈后快门仍为 1/60 ⇒ LOCK_SH=1/60。默认态不触发该探针。"
},
{
  slug: "design/tailwind-colors",
  clicks: ["render();var h=document.getElementById('colorContainer').innerHTML;var total=(h.match(/class=\"shade\"/g)||[]).length;var withRole=(h.match(/class=\"shade\"[^>]*role=\"button\"/g)||[]).length;document.getElementById('__tbProbe').textContent='TW_A11Y='+withRole+'/'+total;"],
  expect: ["TW_A11Y=242/242"],
  ref: "D-N143 回归：242 个色块（22 色 × 11 阶）原为纯 div+onclick，键盘/读屏不可达；修复后每个色块带 tabindex=\"0\" role=\"button\" aria-label。扫描 #colorContainer 内所有 .shade 标记并统计含 role=\"button\" 者，旧实现 withRole=0。显式调用 render() 确保容器已填充。"
},
{
  slug: "design/generator-38",
  inputs: { target: "", constraint: "", task: "", format: "" },
  clicks: ["var t=document.getElementById('task'),f=document.getElementById('format');var tv=(t.options&&t.options[0])?t.options[0].value:'NA';var fv=(f.options&&f.options[0])?f.options[0].value:'NA';calc();var h=document.getElementById('res').innerHTML;var m=h.match(/class=\"num\">(\\d+)<\\/div><div class=\"label\">提示词完整度/);document.getElementById('__tbProbe').textContent='G38 t=['+tv+'] f=['+fv+'] S='+(m?m[1]:'NA');"],
  expect: ["G38 t=[] f=[] S=20"],
  ref: "D-N213 回归：任务类型/输出格式两个 select 原无空项 ⇒ 真机恒有值恒 ok，五要素全空仍给 60 分（文档口径应为 1/5=20）。修复=两 select 首项为空值占位 + prompt 输出空任务时给「【请补充任务类型】」防护 + 算例文案同步。断言两 select 首项 option.value 为空（真机可清空的前提）且全空时提示词完整度=20；旧版首项分别是「生成」「分条列表」⇒ t/f 段即不匹配。默认态（target/constraint 预填）不产出该串。"
},
// ── 第342批：文字色阈值与死输入联动 ─────────────────────────────
{
  slug: "design/css-border-radius",
  clicks: ["document.getElementById('linkCorners').checked=false;document.getElementById('allRadius').value='80';updateAll();var v=String(document.getElementById('cssOutput').value);document.getElementById('__tbProbe').textContent='BR '+v;"],
  expect: ["BR border-radius: 80px 80px 80px 80px / 80px 80px 80px 80px;"],
  ref: "D-N172 回归：简单模式只有 allRadius 一个滑杆，旧码取消「四角联动」后 updateAll 不再写四角、滑杆变成死控件。修复=简单模式强制按统一值作用四角。默认态无该探针串；旧码 cssOutput 停在 20px ⇒ 红。"
},
{
  slug: "design/generator-34",
  inputs: { ratio: "1024x768" },
  clicks: ["calc();var h=String(document.getElementById('res').innerHTML);var m=h.match(/>([0-9.]+) px</);document.getElementById('__tbProbe').textContent='G34 '+(h.indexOf('1024×768')>=0?'SIZE_OK':'SIZE_BAD')+' px='+(m?m[1]:'NA');"],
  expect: ["G34 SIZE_OK px=21.3"],
  ref: "D-N212 回归：比例下拉原为死输入，等效像素固定按 1280 宽算（20pt→26.7px）。修复后等效像素按所选画布宽度换算，1024 宽下 20*96/72*1024/1280=21.3；并输出画布尺寸与比例对照表。旧码 SIZE_BAD（结果无 1024×768）且 px=26.7 ⇒ 红。"
},
{
  slug: "design/farnsworth-d15-test",
  clicks: ["var t=(typeof __fdTextOn==='function')?__fdTextOn('#7B7B7B'):'NOFN';document.getElementById('__tbProbe').textContent='FD_TXT='+t;"],
  expect: ["FD_TXT=#000000"],
  ref: "D-N218 回归：15 个色帽等亮度 L≈0.198（灰度预览 #7B7B7B 同亮度），旧 textOn 用 L>0.32 判深色 ⇒ 全部白字 4.23:1（不达 AA）。修复后按黑白对比度取高者并改纯黑（4.96:1）。#7B7B7B 的 L≈0.1976 ⇒ 期望 #000000；旧码返回 #FFFFFF ⇒ 红。textOn 在 IIFE 内，页面末尾以 window.__fdTextOn 暴露（纯读取）。"
},
// ── 第345批：章数少于幕数不再产出负章数 ───────────────────────────
{
  slug: "design/generator-33",
  inputs: { chapters: "1", mode: "three" },
  clicks: ["calc();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='CH33 neg='+(/-[0-9]+ 章/.test(h)?'Y':'N')+' hint='+(h.indexOf('少于结构幕数')>=0?'Y':'N');"],
  expect: ["CH33 neg=N hint=Y"],
  ref: "D-N207 回归：章数=1、三幕时旧码 [1,1,-1]（末幕被尾差减成负数，表格现「-1 章」）。修复后尾差减量只从 >1 的幕扣除、扣不动时保留每幕 1 章并给出「少于结构幕数」提示。探针同时断言「无负章数」与「有不足提示」；旧码 neg=Y hint=N ⇒ 红。默认态（120 章三幕）不产出该串。"
},

// ── 第346批：边框生成器补齐可视化控件与单边独立 ───────────────────
{
  slug: "design/generator-7",
  inputs: { cnt: "1", bw: "6", br: "20", bs: "dashed" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='G7FIX w='+(h.indexOf('border: 6px dashed')>=0?'Y':'N')+' r='+(h.indexOf('border-radius: 20px')>=0?'Y':'N');"],
  expect: ["G7FIX w=Y r=Y"],
  ref: "D-N201 回归：旧码无宽度/圆角/样式控件，宽度与圆角恒随机 1–8 / 0–32、样式按 i%8 轮换（首条恒 solid），meta 承诺的「可视化设置」无从兑现。修复后填写即固定：注入宽度 6、圆角 20、样式 dashed ⇒ 首条 CSS 必为 `border: 6px dashed`（随机态下宽度恰为 6 且样式恰为 dashed 的概率极低）且 `border-radius: 20px`。旧码 w=N ⇒ 红。"
},
{
  slug: "design/generator-7",
  inputs: { cnt: "1", bw: "4", bs: "solid", bSide: "top" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);var one=h.indexOf('border-top: 4px solid')>=0;var all=/border: 4px/.test(h);document.getElementById('__tbProbe').textContent='G7SIDE one='+(one?'Y':'N')+' all='+(all?'Y':'N');"],
  expect: ["G7SIDE one=Y all=N"],
  ref: "D-N201 回归（单边独立）：meta 与简介均写「支持单边独立设置」，旧码只输出 `border` 简写、永不产生 `border-top`。修复后选「仅上边」+ 4px solid ⇒ CSS 含 `border-top: 4px solid` 且不再出现四边简写 `border: 4px`（预览内联样式无空格，故不误判）。旧码 one=N all=Y ⇒ 红。"
},

// ── 第347批：阴影生成器补齐参数控件与层级递增 ─────────────────────
{
  slug: "design/generator-6",
  inputs: { cnt: "1", sx: "10", sy: "-6", sb: "18", ss: "2", sl: "2", si: "no", scc: "fix", sc: "#ff6b35" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);var re=/(10px -6px 18px 2px rgba\\(255, 107, 53, )/g;var c=(h.match(re)||[]).length;document.getElementById('__tbProbe').textContent='G6FIX n='+c+' inset='+(h.indexOf('inset ')>=0?'Y':'N');"],
  expect: ["G6FIX n=4 inset=N"],
  ref: "D-N168 回归：旧码无偏移/模糊/扩散/颜色/层数/inset 控件，全由 Math.random 决定，meta 承诺的「拖动控件调整偏移、模糊、扩散、颜色」无从兑现。修复后填写即固定：注入 10/-6/18/2、每层数 2、外阴影、固定色 #ff6b35 ⇒ 必输出两条完全相同的 `10px -6px 18px 2px rgba(255, 107, 53,`；该声明同时出现在 CSS 代码块与 60×60 预览的内联样式里，故 n=4（2 层 × 2 处载体），且全页不含 inset。旧码 n=0 ⇒ 红。"
},
{
  slug: "design/generator-6",
  inputs: { cnt: "3", mode: "scale", sl: "1", si: "no" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);var a=h.indexOf('0px 1px 4px 0px rgba(0, 0, 0, 0.14)')>=0;var c=h.indexOf('0px 3px 8px 0px rgba(0, 0, 0, 0.13)')>=0;document.getElementById('__tbProbe').textContent='G6SCALE a='+(a?'Y':'N')+' c='+(c?'Y':'N');"],
  expect: ["G6SCALE a=Y c=Y"],
  ref: "D-N169 回归：「8 组阴影（层级体系）」旧码只设 cnt，每条独立随机，产出互不相关且可能倒序，不能当 elevation scale 用。修复后新增「层级递增」模式：第 i 条固定 offset-x 0、offset-y i、blur 2i+2、spread 0、透明度 0.15−0.006i（下限 0.05）。注入 3 条 ⇒ 第 1 条必为 `0px 1px 4px 0px rgba(0, 0, 0, 0.14)`、第 3 条必为 `0px 3px 8px 0px rgba(0, 0, 0, 0.13)`，同时锚定递增与透明度递减。旧码无 mode 控件 ⇒ 两条均不命中 ⇒ 红。"
},

// ── 第348批：网格虚线类型、等距网格重复层与上限 ───────────────────
{
  slug: "design/grid-pattern",
  inputs: { gridType: "dashed", cellSize: "30", lineWidth: "2" },
  clicks: ["var t=document.getElementById('gridType');t.value='dashed';generate();var h=String(document.getElementById('cssOutput').value);var rep=(h.match(/repeating-linear-gradient/g)||[]).length;document.getElementById('__tbProbe').textContent='G72 rep='+rep+' solid='+(h.indexOf('background-image: linear-gradient(')>=0?'Y':'N');"],
  expect: ["G72 rep=2 solid=N"],
  ref: "D-N72 回归：旧码 dashed 分支与 square 分支的 background-image / background-size 逐字符相同，只多一条 background-position，实为整体位移半像素的实线网格，选「虚线网格」拿不到虚线。修复后改用两层 repeating-linear-gradient（实线段 lw px + 间隔 2·lw px），输出含 2 处 repeating-linear-gradient、且不再退回普通 linear-gradient 实线写法。旧码 rep=0 solid=Y ⇒ 红。"
},
{
  slug: "design/isometric-grid",
  inputs: { size: "40", lineWidth: "1" },
  clicks: ["generate();var o=String(document.getElementById('cssOutput').value);var n=(o.match(/linear-gradient\\(/g)||[]).length;document.getElementById('size').value='999';generate();var o2=String(document.getElementById('cssOutput').value);var m=o2.match(/background-size: ([0-9.]+)px/);document.getElementById('__tbProbe').textContent='G194 n='+n+' clamp='+(m?m[1]:'N');"],
  expect: ["G194 n=3 clamp=200"],
  ref: "D-N194 回归：旧码 background-image 写 4 层，其中第 1、4 层都是 linear-gradient(30deg …) 完全重复，实际只有 3 个方向；且 size 只在 HTML 上写 max=200、JS 未夹取。修复后删掉重复层（n=3）并把 size 钳到 10–200（输入 999 ⇒ background-size 宽 200px）。旧码 n=4 clamp=999 ⇒ 红。"
},

// ── 第349批：动画生成器参数控件与实时预览 ─────────────────────────
{
  slug: "design/generator-10",
  inputs: { cnt: "2", atype: "fadeIn", dur: "2.5", dly: "0", eas: "linear", it: "1", dir: "normal", fill: "forwards" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='G10 dur='+(h.indexOf('2.5s linear 0.0s 1 normal forwards')>=0?'Y':'N')+' prev='+(h.indexOf('animPreviewBox')>=0?'Y':'N')+' noSlide='+(h.indexOf('slideUp')>=0?'N':'Y');"],
  expect: ["G10 dur=Y prev=Y noSlide=Y"],
  ref: "D-N195 回归：旧码只有 cnt 一个输入，时长/缓动/延迟/方向/填充全部随机，页面没有任何预览元素，`#res` 只有 <pre> 文本 ⇒「可视化编排 + 实时预览」两个主卖点落空。修复后注入时长 2.5 / 延迟 0 / 线性缓动 / 1 次 / normal / forwards，并指定动画类型 fadeIn、生成 2 条 ⇒ 必出 `2.5s linear 0.0s 1 normal forwards`（dur=Y）；顶部预览色块 `animPreviewBox` 存在（prev=Y）；两条都用 fadeIn，故全文不再出现 slideUp（noSlide=Y，锚定「动画类型」控件生效）。旧码三项全 N ⇒ 红。"
},
{
  slug: "design/generator-11",
  inputs: { cnt: "1", tPattern: "stripes", tMain: "#ff6b35", tBg: "#0f172a", tColorMode: "fix", tSize: "32" },
  clicks: ["gen();var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='GE11 css='+(h.indexOf('repeating-linear-gradient(90deg, #ff6b35, #ff6b35 16px, #0f172a 16px, #0f172a 32px)')>=0?'Y':'N')+' pat='+(h.indexOf('条纹纹理')>=0?'Y':'N')+' other='+(h.indexOf('圆点纹理')>=0?'Y':'N');"],
  expect: ["GE11 css=Y pat=Y other=N"],
  ref: "D-N189 回归：旧码只有 cnt 一个输入，图案按 i%6 固定轮换、颜色与尺寸全随机，用户既选不了纹理也复现不了上次结果。修复后注入「条纹」+ 主色 #ff6b35 / 底色 #0f172a + 固定尺寸 32 ⇒ 必出 `repeating-linear-gradient(90deg, #ff6b35, #ff6b35 16px, #0f172a 16px, #0f172a 32px)`（16 = size/2），标题为「条纹纹理」且不再出现「圆点纹理」（cnt=1 时轮换首项本是圆点，故 other=N 同时锚定「图案类型」控件生效）。旧码三项为 N/N/Y ⇒ 红。"
},
{
  slug: "design/exposure-triangle-calculator",
  inputs: { aperture: "4", shutter: "1/60", iso: "200" },
  clicks: ["calc();var h=String(document.getElementById('equiv').innerHTML);var a=h.indexOf('<br>1/30<br>ISO 100')>=0;var b=h.indexOf('<br>1/15<br>ISO 100')>=0;var ev=evFromIdx(3,6,1).toFixed(2);document.getElementById('__tbProbe').textContent='EXP115 s30='+(a?'Y':'N')+' s15='+(b?'Y':'N')+' ev='+ev;"],
  expect: ["EXP115 s30=Y s15=N ev=8.91"],
  ref: "D-N115 回归：默认 f/4·1/60·ISO200（EV=8.91），等效组合循环里 da=-2 时 ISO 档位被 clamp（ii=1 → niso=0，实际只降 1 档），但旧码用期望差 da 补偿快门（ns=si-da=8 ⇒ 1/15），卡片标在「相同曝光量」下却是 EV=7.91（暗 1 档）。修复后按实际档位差补偿（ns=si-(niso-ii)=7 ⇒ 1/30），EV=8.91 重新等效。旧码 s30=N s15=Y ⇒ 红；ev=8.91 同时锚定基准 EV 未被改坏。"
},
{
  slug: "design/shutter-speed-calculator",
  inputs: { focal: "50", crop: "1.5", is: "3" },
  clicks: ["var src=(typeof __ssChartDraw==='function')?String(__ssChartDraw):'';var r=(typeof ssStopsFor==='function')?ssStopsFor(50,1.5,3):{baseDen:-1,safeDen:-1};var r2=(typeof ssStopsFor==='function')?ssStopsFor(90,1,3):{baseDen:-1,safeDen:-1};document.getElementById('__tbProbe').textContent='SS119 use='+(src.indexOf('ssStopsFor(')>=0?'Y':'N')+' b='+r.baseDen+' s='+r.safeDen+' b2='+r2.baseDen+' s2='+r2.safeDen;"],
  expect: ["SS119 use=Y b=125 s=15 b2=125 s2=15"],
  ref: "D-N119 回归：旧码结果区/CSV 用标准档位表 findIndex（50mm·1.5x·3档 ⇒ 基础 1/125、建议 1/15），图表却用连续除法 d1=fv*crop 与 Math.round(d1/2^isStops)（给 1/9 或 1/11），同一页三个快门；且 round 会把 11.25 取成 11（更慢方向），违反公式框「向更快方向取整」。修复后抽公共 ssStopsFor，三处共用档位表：50·1.5·3 与 90·1·3 均得 1/125 / 1/15（分母 125/15），并用 String(__ssChartDraw) 锚定图表确实改为调用该函数。旧码 use=N b=-1 s=-1 ⇒ 红。"
},
{
  slug: "design/gradient-from-color",
  inputs: { baseColor: "#000000", steps: "3", direction: "90" },
  clicks: ["generate();var c=String(document.getElementById('cssOutput').value);document.getElementById('__tbProbe').textContent='GFC old='+(c.indexOf('#e6e6e6')>=0?'Y':'N')+' new='+(c.indexOf('#595959')>=0?'Y':'N')+' low='+(c.indexOf('#0d0d0d')>=0?'Y':'N');"],
  expect: ["GFC old=N new=Y low=Y"],
  ref: "D-N126 回归：旧码亮度固定 90→20，完全丢弃基色 hsl.l —— 黑色基色 #000000 竟然得到 #e6e6e6→#333333 的灰阶，纯黑/纯白都不出现在渐变里。修复后以基色明度 L 为中心取 [max(5,L−35), min(95,L+35)]：L=0 ⇒ 区间 [5,35]，steps=3 时色标为 #595959 / #333333 / #0d0d0d，不再出现旧码的 #e6e6e6。旧码 old=Y new=N low=N ⇒ 红。"
},
{
  slug: "design/flexbox-generator",
  inputs: { dir: "column", gap: "20" },
  clicks: ["var ids=['dir','just','ali','wrap','gap'];var n=0;for(var i=0;i<ids.length;i++){var e=document.getElementById(ids[i]);if(e&&e.__flexLiveBound)n++;}document.getElementById('__tbProbe').textContent='FLX live='+n+'/5';"],
  expect: ["FLX live=5/5"],
  ref: "D-N123 回归：结果标题写「实时预览」，但旧码 5 个控件（dir/just/ali/wrap/gap）全无 change/input 监听，只有点「生成」才调 calcTool()。修复后由 __bindFlexLive 统一绑定并在元素上留 __flexLiveBound 标记，5/5 全部绑定；旧码 0/5 ⇒ 红。"
},
{
  slug: "design/flexbox-generator",
  clicks: ["var e=document.getElementById('dir');var saved=e.addEventListener;e.addEventListener=undefined;var r='Y';try{e.__flexLiveBound=false;__bindFlexLive();}catch(err){r='N';}e.addEventListener=saved;document.getElementById('__tbProbe').textContent='FLX degrade='+r+' bound='+(e.__flexLiveBound?'Y':'N');"],
  expect: ["FLX degrade=Y bound=N"],
  ref: "第356批全量门禁阻断回归：calculation regression 的 DOM stub 给 dir/just/ali/wrap/gap 的元素只有 value，不带 addEventListener；旧码 __bindFlexLive 直调该 API，整页初始化抛 e.addEventListener is not a function。探针摘除 dir 的事件 API 后重跑绑定：旧码抛错且已置标记 ⇒ degrade=N bound=Y ⇒ 红；新码先做能力判断再跳过 ⇒ 不抛错、不置标记 ⇒ degrade=Y bound=N。真实浏览器下原有 FLX live=5/5 用例仍保证五个控件全绑定。"
},
{
  slug: "design/font-preview",
  clicks: ["globalThis.TBKit={util:{isEn:function(){return true;}},chart:{bar:function(){}}};loadFontSample('ZZENZZ');var h=String(document.getElementById('fpFontList').innerHTML);var c=String(document.getElementById('fpCount').textContent);try{delete globalThis.TBKit;}catch(e){}document.getElementById('__tbProbe').textContent='FPEN hint='+(h.indexOf('Click to copy')>=0?'Y':'N')+' zh='+(h.indexOf('点击复制')>=0?'Y':'N')+' count='+(c.indexOf(' fonts')>=0?'Y':'N')+' zhcount='+(c.indexOf('种字体')>=0?'Y':'N')+' cat='+(h.indexOf('中文字体')>=0?'Y':'N');"],
  expect: ["FPEN hint=Y zh=N count=Y zhcount=N cat=N"],
  ref: "D-N4 回归：旧码 render() 把「点击复制」「N / M 种字体」与三个中文分类标题硬编码，EN 态卡片夹中文。探针注入 EN 态 TBKit 后走全局 loadFontSample() 触发 IIFE 内的 render()：新码按 isEn 输出 Click to copy / fonts / Chinese 等英文分类名，旧码仍全中文 ⇒ hint=N zh=Y count=N zhcount=Y cat=Y ⇒ 红。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
},
{
  slug: "design/font-preview",
  clicks: ["var s=String(globalThis.__fpOnLangChange||'');document.getElementById('__tbProbe').textContent='FPLANG render='+(s.indexOf('render()')>=0?'Y':'N')+' chart='+(s.indexOf('__fpChart()')>=0?'Y':'N');"],
  expect: ["FPLANG render=Y chart=N"],
  ref: "D-N4 回归（语言切换）：旧码 toolbox:langchange 回调只重画 __fpChart()，切换语言后列表卡片与计数仍是旧语言。新码抽出全局 __fpOnLangChange 并直接重跑 render()（图表由 render 内部调用），不再单独调 __fpChart()。旧码无该函数 ⇒ render=N ⇒ 红；默认态不执行 clicks ⇒ 零逃生。"
},
{
  slug: "design/tailwind-colors",
  clicks: ["var src=String(showDetail);document.getElementById('__tbProbe').textContent='TWV4 color='+(src.indexOf('--color-')>=0?'Y':'N')+' old='+(src.indexOf('--tw-')>=0?'Y':'N');"],
  expect: ["TWV4 color=Y old=N"],
  ref: "D-N144 回归：详情面板的「CSS 变量」行旧码输出 --tw-${name}-${level}，Tailwind v3 无此变量、v4 官方命名是 --color-${name}-${level}，用户复制后变量不存在。修复后改 --color- 并标注 (v4)。用 String(showDetail) 锚定详情渲染函数源码本身（绕开 stub DOM 缺 classList 的限制）：旧码 color=N old=Y ⇒ 红。"
},
{
  slug: "design/tester-assessor",
  // 第354批 D-N175：历史快照原 keys.slice(0,12) 只保留前 4 题 SUS，后 6 题不入库也不恢复。
  // 自建 TBKit + 18 个输入桩，跑真 Extras ⇒ 记录应含 20 键（18 输入 + 结果 + 评分）、表头 21 列、
  // 且 mount 的恢复回调能把末题 sus9 回写成记录值。
  clicks: ["var __cap=null,__head=null,__pick=null;TBKit={util:{isEn:function(){return false;},diffBox:function(){},exportTable:function(){}},matrix:{table:function(h,o){__head=o.head;}},chart:{line:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(r){__cap=r;},mount:function(h,f){__pick=f;}},preset:{bar:function(){}}};var __els=[],__ids=['totalTasks','successTasks','avgTime','expectedTime','errors','helpCount','userCount','satisfaction'];for(var __i=0;__i<__ids.length;__i++)__els.push({id:__ids[__i],type:'text',value:'5'});for(var __j=0;__j<10;__j++)__els.push({id:'sus'+__j,type:'select-one',value:__j===9?'1':'3'});var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('res').textContent='86 综合可用性评分';__tester_assessor_last=0;__tester_assessor_skip=false;__tester_assessorExtras();document.querySelectorAll=__oq;var __n=__cap?Object.keys(__cap).length:0,__has=!!(__cap&&Object.prototype.hasOwnProperty.call(__cap,'sus9'));if(__cap&&__has)__cap.sus9='2';if(__pick){try{__pick(__cap||{});}catch(e){}}document.getElementById('__tbProbe').textContent='可用性历史 键数='+__n+' 末题='+( __has?'Y':'N')+' 表头='+(__head?__head.length:0)+' 恢复='+(String(document.getElementById('sus9').value)==='2'?'Y':'N');"],
  expect: ["可用性历史 键数=20 末题=Y 表头=21 恢复=Y"],
  ref: "第354批：__tester_assessorSnap() 收集 8 项绩效 + 10 题 SUS 共 18 键，旧码在 Extras 与 Export 两处 keys.slice(0,12) 截掉后 6 题 ⇒ 历史只存 4 题 SUS，恢复时其余 6 题保留当前值再 calc()，SUS 分数与记录结果不符。删除截断后：rec = 18 输入 + 结果 + __tbScore = 20 键，Render 表头 = 时间 + 18 + 结论 + 结果 = 21 列，mount 恢复回调能把 sus9 回写成记录值。旧码应为 键数=14 末题=N 表头=15 恢复=N ⇒ 全失配。探针仅由 clicks 生成 ⇒ 零逃生。",
  inputs: {}
}

];

// ---------------------------------------------------------------- main
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

  console.log("==== design calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();