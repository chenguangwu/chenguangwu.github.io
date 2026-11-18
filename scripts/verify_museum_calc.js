#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B,C';syncNodes();edges=[['A','B',-12],['B','C',7]];compute();"],
  "expect": [
    "19 m 总距离"
  ],
  "ref": "负距离回归（N5-C）：通道 A–B 注入 -10 m、B–C 5 m，负权先取绝对值 ⇒ 最短流线 A→B→C 总距离 12+7=19 m；旧实现直接把负权喂给 Dijkstra，输出总距离 -5 m（且前驱回溯无访问集合，负权环会无限回溯）。19 m 不与默认展线（15 m）冲突，避开默认态。"
},
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B';syncNodes();edges=[['A','B',-10],['B','A',10]];compute();"],
  "expect": [
    "10 m 总距离"
  ],
  "ref": "负权环终止性（N5-C）：双向边 -10/10 构成负权环，旧实现 relax 后 prev[A]=B、prev[B]=A 且回溯无访问集合 ⇒ 死循环挂死页面。修复后负距离取绝对值（均为 10）、回溯带 seen 集合与步数上限 ⇒ 正常输出 A→B 总距离 10 m。"
},
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B,C,D';syncNodes();edges=[['A','B',10],['B','C',10],['C','D',10],['A','D',100]];document.getElementById('waypoints').value='C';compute();"],
  "expect": [
    "30 m",
    "（必看）"
  ],
  "ref": "必看节点串联：A→B→C→D 各段 10 m，途经必看节点 C 后总距离 30 m，而直达 A→D 为 100 m；「（必看）」标记只对必看节点输出。旧实现无 waypoints 输入、无条件直接求 start→end ⇒ 总距离 100 m 且无必看标记，两条均不命中。默认展线为 115 m，30 m 亦不与默认冲突。"
},
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B,C';syncNodes();edges=[['A','B',30],['A','B',100],['B','C',10]];compute();"],
  "expect": [
    "A (30m) → 2. B"
  ],
  "ref": "平行边分段（RL-K46）：A–B 同时存在 30 m 与 100 m 两条通道，Dijkstra 选 30 m。旧版分段渲染遍历全部 edges 并覆盖权值为最后一条 100 m，显示「A (100m) → 2. B」；修复后取 prevW 实际选中边显示「A (30m) → 2. B」。锚含节点 A/B，避开默认态（入口→青铜馆 30m）与「40 m 总距离」两版同值造成的假绿。"
},
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='3';document.getElementById('era2').value='9';compare()"],
  "expect": [
    "时间跨度相差: 839 年",
    "秦朝 15 年 vs 唐朝 289 年 (差 274 年)",
    "比值 0.25（相当于 25.0%；唐朝为秦朝的 4.00 倍）"
  ],
  "ref": "两个朝代 <select> 的 option 由 JS 按 ERAS 下标填充（静态无 option ⇒ clicks 赋值后调 compare()）：era1=3 秦朝(s=-221,dur=15,人口约2000万)、era2=9 唐朝(s=618,dur=289,人口约8000万) ⇒ 起始年差 |−221−618|=839、时长差 |15−289|=274；人口按万=1e4 统一换算后 2e7/8e7=0.25（相当于 25.0%，唐朝为秦朝的 4 倍）。旧实现按未换算数字 2000/8000 求 max/min=4.0 倍，断言语义已切换为前/后比值。"
},
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='9';document.getElementById('era2').value='10';compare()"],
  "expect": [
    "唐朝 约 8000 万（8000 万） vs",
    "宋朝 约 1 亿（1 亿）",
    "比值 0.80（相当于 80.0%；宋朝为唐朝的 1.25 倍）"
  ],
  "ref": "量纲回归（万/亿混用）：era1=9 唐朝（约 8000 万 = 8e7）、era2=10 宋朝（约 1 亿 = 1e8）⇒ 统一换算后 8e7/1e8=0.80（相当于 80.0%；按任务给的 0.08/8% 口径复算，8000 万实为 0.8 亿，正确比值为 0.8），旧实现把 8000 与 1 直接相比输出 8000 倍。断言同时校验两侧统一量纲展示（8000 万 / 1 亿）。"
},
{
  "slug": "museum/exhibit-spacing",
  "inputs": {
    "artWidth": "120",
    "artHeight": "100",
    "centerH": "150",
    "hAngle": "30",
    "vAngle": "15",
    "eyeH": "155",
    "viewers": "2",
    "shoulder": "60"
  },
  "expect": [
    "216.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/exhibit-spacing",
  "inputs": {
    "artWidth": "120",
    "artHeight": "100",
    "centerH": "150",
    "hAngle": "30",
    "vAngle": "15",
    "eyeH": "155",
    "viewers": "2",
    "shoulder": "60"
  },
  "expect": [
    "0.46 幅/m"
  ],
  "ref": "每米布展数（RL-K32）：推荐间距 = max(120+60×2×0.8, 120×1.5) = 216 cm ⇒ 100÷216 = 0.46296 ⇒ 显示 0.46 幅/m。旧版 Math.floor 截成 0 幅/m，默认态为 0.57，两值均不命中 0.46。"
},
{
  "slug": "museum/exhibit-spacing",
  "inputs": {
    "artWidth": "80",
    "artHeight": "100",
    "centerH": "150",
    "hAngle": "60",
    "vAngle": "45",
    "eyeH": "155",
    "viewers": "1",
    "shoulder": "60"
  },
  "expect": [
    "视角与清晰距离冲突：已按最小观看距离给建议。"
  ],
  "ref": "距离冲突（RL-K33）：水平 40÷tan60°≈23.1 cm、垂直 (5+50)÷tan45°=55 cm，视角最佳 55 cm < 对角线 0.6 倍 76.8 cm。修复后最佳距离抬到 76.8 cm 并提示冲突；旧版两条建议打架且无该提示，默认态也不命中。"
},
{
  "slug": "museum/historical-calendar",
  "inputs": {
    "date-input": "2008-08-08"
  },
  "clicks": ["update()"],
  "expect": [
    "2008 年 8 月 8 日",
    "星期五",
    "戊子年",
    "属鼠"
  ],
  "ref": "注入 2008-08-08 ⇒ 公历 2008 年 8 月 8 日、星期五（datetime 独立复算一致）、干支 戊子年"
     + "（(2008−4)%10=4→戊、(2008−4)%12=0→子）、生肖 属鼠。"
     + "不锚「距今 N 天」—— harness 用固定时钟 FrozenDate，该值随基准日漂移（实测 5790）。"
     + "原 expect「undefined-NaN-undefined」是兜底阶段无参 selectDate() 的产物（y/m/d 全 undefined ⇒ 拼出该串），"
     + "它既非页面缺陷也零判别力（默认态即命中）。",
},
{
  "slug": "museum/historical-calendar",
  "clicks": ["document.getElementById('date-input').value='1899-12-31';update();"],
  "expect": [
    "仅支持 1900–2100 年日期，请重新选择。"
  ],
  "ref": "年份越界（RL-K36）：solarToLunar 对 1899 年返回 null，旧版未判空直接读 lunar.y ⇒ TypeError 中断，详情与历史事件停留在上一次结果。修复后给出范围提示并清空事件列表；默认态为当前本地日期，不含该提示。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "7",
    "lumens": "500",
    "distance": "0.8",
    "beamAngle": "36",
    "utilCoef": "0.7",
    "area": "2",
    "trans": "92"
  },
  "expect": [
    "11452"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "5",
    "area": "4"
  },
  "clicks": ["document.getElementById('lumens').value='0';calc();"],
  "expect": [
    "单盏光通量需大于 0 lm。"
  ],
  "ref": "零光通守卫（RL-K13）：单盏 0 lm 是无效光源，旧版 parseFloat('0')||0 后照度 0 lx 却判「照度达标 ✓」，把全暗包装成合规。修复后拦截「单盏光通量需大于 0 lm。」，旧版不输出该串。用 clicks 注入是因为 harness 会无参试探 onLampChange() 把 lumens 重置为预设 500。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "5",
    "area": "4",
    "trans": "0"
  },
  "expect": [
    "玻璃透过率需大于 0 且不超过 100%。"
  ],
  "ref": "零透过率守卫（RL-K13）：透过率 0% 表示玻璃完全不透光，旧版 ||100 当成 100% 算出 875 lx 并报超标（中等敏感 150 lx），既掩盖输入错误又给出无意义结论。修复后直接拦截，旧版不含该提示。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "5",
    "area": "4"
  },
  "clicks": ["document.getElementById('utilCoef').value='0';calc();"],
  "expect": [
    "利用系数需大于 0 且不超过 1。"
  ],
  "ref": "零利用系数守卫（RL-K13）：旧版 util=0 被 ||0.7 静默替换，5 盏 500 lm、面积 4 ㎡ 算出无效照度。修复后拦截，旧版不含该提示。clicks 注入避开 onLampChange() 预设重置。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "5",
    "area": ""
  },
  "expect": [
    "展柜面积需大于 0 ㎡。"
  ],
  "ref": "空面积守卫（RL-K13）：面积清空旧版 ||1 当作 1 ㎡ 继续算并给出超标结论，修复后明确要求大于 0。空字符串随 input/change 事件触发 calc()，断言只落在结果区提示。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "1",
    "distance": "0.8",
    "area": "20",
    "trans": "92",
    "sensClass": "high"
  },
  "expect": [
    "中心照度过曝 ✕",
    "尽管平均照度达标"
  ],
  "ref": "峰值合规双条件（RL-K14）：1 盏 500 lm、36°、利用系数 0.7、透过率 92%、距离 0.8 m、面积 20 ㎡、高敏感 50 lx ⇒ 平均 16 lx 达标但中心约 1636 lx 远超限值。旧版只看 avgLux 输出「照度达标 ✓」，两条断言均不命中；修复后输出「照度中心照度过曝 ✕」与峰值警告。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "sensClass": "low",
    "lampCount": "2",
    "area": "7"
  },
  "expect": [
    "展品限值（低敏感） 150 lx，年曝光量≤150万 lx·h/年"
  ],
  "ref": "年曝光口径（RL-K15）：低敏感照度限值 150 lx 对应年曝光量应与其他档同量级为 150 万 lx·h/年，旧版写「≤150 lx·h」少四个数量级。锚含「展品限值（低敏感）」上下文，默认中等敏感不命中；旧版低敏感串不含「万」也不命中。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "3",
    "area": "4",
    "distance": "1.2"
  },
  "expect": [
    "375 lm/㎡ 光通量密度（标称）"
  ],
  "ref": "术语与量纲（RL-K15）：灯数×单灯光通÷面积 的单位是 lm/㎡，属于光通量密度而非功率密度（W/㎡）。旧版结果卡片写「展柜功率密度」，修复后改「光通量密度（标称）」并同步公式框。锚带非默认数值 3×500÷4=375 lm/㎡（默认 4×500÷2=1000），避免默认态静态标签造成假绿。"
},
{
  "slug": "museum/showcase-monitor",
  "inputs": {
    "temp": "30",
    "rh": "55",
    "tempSwing": "2",
    "rhSwing": "5"
  },
  "expect": [
    "建议降温至"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/showcase-monitor",
  "clicks": [
    "currentMat='ceramic';document.getElementById('temp').value='40';document.getElementById('rh').value='50';evalEnv();"
  ],
  "expect": [
    "温度偏高，建议降至 35℃ 以下"
  ],
  "ref": "范围型材质建议（RL-K38）：陶瓷/玻璃用 tempR=[5,35]、rhR=[20,60]，旧版建议分支只覆盖数组 temp 与 rhMax，40℃ 超标时 advice 为空，输出「调整建议：。」。修复后按 tempR 上下界给出降温建议；默认材质为书画（数组 temp），不命中该串。"
},
{
  "slug": "museum/timeline-viewer",
  "clicks": [
    "currentTheme='世界历史';renderTimeline();"
  ],
  "expect": [
    "前 3100 年 上下埃及统一"
  ],
  "ref": "去默认化（原 expect「2070」＝默认「中国历史」主题下夏朝建立 -2070 的渲染串，注入失败仍命中 → 逃生项）：clicks 置顶层全局 currentTheme='世界历史' 后调 renderTimeline()，timeline 渲染世界史首条「前 3100 年 上下埃及统一 政治 古埃及第一王朝建立」；默认中国历史显示「夏朝建立 ... -2070」，注入失败即不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "20",
    "perExhibit": "60",
    "moveTime": "20",
    "introTime": "30",
    "available": "50"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "26分50秒 讲解总时长",
    "+23分10秒",
    "150 秒"
  ],
  "ref": "总时长 = 20×60 + (20−1)×20 + 30 = 1200+380+30 = 1610 秒 ⇒ fmtTime 26分50秒；可用 = 50×60 = 3000 秒 ⇒ 50分0秒；时间差 = +1390 秒 ⇒ +23分10秒（充裕）；每件可用 = floor(3000/20) = 150 秒。默认态（30 件/90 秒/移动 30/开场 60/可用 90 分钟）为 1时0分30秒 / +29分30秒 / 180 秒，三条全不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "10",
    "perExhibit": "90",
    "moveTime": "10",
    "introTime": "20",
    "available": "15"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "略超时",
    "缩短单件讲解至 79 秒",
    "减少讲解展品数至 8 件"
  ],
  "ref": "总时长 = 10×90 + 9×10 + 20 = 1010 秒 ⇒ 16分50秒；可用 = 15×60 = 900 秒 ⇒ 15分0秒；时间差 = −110 秒（≥−300 ⇒ 「略超时」档）；压缩建议：单件讲解 cutPer = floor((900 − 9×10 − 20)/10) = 79 秒（旧实现误乘 90×900 得 8089 秒）、展品数 = floor((900−20)/(90+10)) = 8 件。默认态为「时间充裕」，三条全不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "40",
    "perExhibit": "120",
    "moveTime": "30",
    "introTime": "60",
    "available": "40"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "1时40分30秒 讲解总时长",
    "严重超时",
    "缩短单件讲解至 29 秒",
    "减少讲解展品数至 15 件"
  ],
  "ref": "总时长 = 40×120 + 39×30 + 60 = 4800+1170+60 = 6030 秒 ⇒ 1时40分30秒；可用 = 2400 秒 ⇒ 40分0秒；时间差 = −3630 秒（< −300 ⇒ 「严重超时」）；每件可用 = floor(2400/40) = 60 秒；cutPer = floor((2400 − 39×30 − 60)/40) = 29 秒（旧实现误乘 120×2400 得 7169 秒）；展品数 = floor((2400−60)/(120+30)) = 15 件。默认态全不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "10",
    "perExhibit": "90",
    "moveTime": "30",
    "introTime": "40",
    "available": "9"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "缩短单件讲解至 23 秒"
  ],
  "ref": "量纲回归（W6-D）：总时长 = 10×90 + 9×30 + 40 = 1210 秒；可用 = 9×60 = 540 秒；时间差 = −670 秒（严重超时）；cutPer = floor((540 − 9×30 − 40)/10) = 23 秒（旧实现给 floor((90×540 − 270 − 40)/10) = 4829 秒）；展品数 = floor((540−40)/(90+30)) = 4 件。已删「严重超时」「减少讲解展品数至 4 件」两条弱锚：旧量纲版这两条仍成立，会让 expect 的「或」语义假绿，只保留随修复切换的 23 秒强锚。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "1",
    "perExhibit": "50",
    "moveTime": "30",
    "introTime": "10",
    "available": "10"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "× 0 段 = 0 秒",
    "600 秒",
    "1分0秒 讲解总时长"
  ],
  "ref": "总时长 = 1×50 + 0（count>1 为假 ⇒ 移动 0 段）+ 10 = 60 秒 ⇒ 1分0秒；可用 = 600 秒 ⇒ 10分0秒；时间差 = +540 秒；每件可用 = floor(600/1) = 600 秒。表格里「移动时间 × 0 段 = 0 秒」是本例独有形态，默认态（29 段移动）不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "5",
    "perExhibit": "60",
    "moveTime": "10",
    "introTime": "20",
    "available": "0"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "可用时间需大于 0，无法排程。"
  ],
  "ref": "可用时间边界（RL-K31）：可用 0 分钟旧版仍算出「每件可用 0 秒 / 缩短至 0 秒 / 减少至 -1 件」，给出物理上无法执行的建议。修复后在计算前拦截并提示，断言只在结果区出现；默认态 available=90 不命中。"
},
{
    dynDom: true,
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "5",
    "perExhibit": "60",
    "moveTime": "10",
    "introTime": "400",
    "available": "5"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "②开场结束已占满可用时间，无法再安排讲解；"
  ],
  "ref": "开场超时保护（RL-K31）：可用 300 秒 < 开场结束 400 秒，旧版 floor((300−400)/(60+10)) = −2 件仍输出「减少讲解展品数至 -2 件」。修复后容量封顶为 0 并改提示「无法再安排讲解」，断言依赖 intro>avail 的输入组合，默认态不命中。"
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

  console.log("==== museum calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
