#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B,C';syncNodes();edges=[['A','B',-12],['B','C',7]];document.getElementById('startNode').value='A';document.getElementById('endNode').value='C';compute();"],
  "expect": [
    "以下通道距离为空、非数值或负数，未纳入计算",
    "距离为负数"
  ],
  "ref": "负距离拒绝（第1147批）：旧版把 -12 m 取绝对值后参与计算，未知/错误通道可能变成最短路径。现版直接排除负距离并在结果上方列出原因；A–C 无有效路径时错误提示与无效通道提示同时出现。断言不再要求 19 m 总距离。"
},
{
  "slug": "museum/visitor-route",
  "inputs": {},
  "clicks": ["document.getElementById('nodeInput').value='A,B';syncNodes();edges=[['A','B',-10],['B','A',10]];document.getElementById('startNode').value='A';document.getElementById('endNode').value='B';compute();"],
  "expect": [
    "以下通道距离为空、非数值或负数，未纳入计算",
    "10 m 总距离"
  ],
  "ref": "负权环不再进入图（第1147批）：双向边 -10/10 以前会把负权取绝对值形成两条 10 m 通道；现版排除负数，仅保留显式填写的 10 m 边，A→B 总距离 10 m。负权不再进入 Dijkstra，不会因前驱成环回溯冻死页面。"
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
  "slug": "museum/visitor-route",
  "clicks": ["document.getElementById('nodeInput').value='入口,青铜馆,陶瓷馆,书画馆,玉器馆,东门';edges=[['玉器馆','出口',30]];syncNodes();document.getElementById('__tbProbe').textContent='MIG '+(edges[0][1]==='东门'?'OK':'BAD '+edges[0][1])"],
  "expect": ["MIG OK"],
  "ref": "RL-K47 展厅改名端点迁移：页面初始 nodes 含末项「出口」，edges 有「玉器馆—出口」边；把 nodeInput 末项改为「东门」后 syncNodes()，旧版不迁移、边端点仍是「出口」（下拉无匹配项、compute 静默丢弃），修复版按索引 1:1 迁移为「东门」。哨兵检查 edges[0][1]。"
},
{
  "slug": "museum/visitor-route",
  "clicks": ["document.getElementById('nodeInput').value='入口,青铜馆,陶瓷馆,书画馆,玉器馆,出口,东门';edges=[['入口','青铜馆',10],['青铜馆','出口',10],['玉器馆','玉石馆',30]];document.getElementById('startNode').value='入口';document.getElementById('endNode').value='出口';compute();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent=(h.indexOf('端点已失效')>=0)?'DEAD OK':'DEAD BAD'"],
  "expect": ["DEAD OK"],
  "ref": "RL-K47 失效边提示：新增「东门」使「玉石馆」边不满足改名迁移（玉石馆从未在 nodes），compute() 时旧版对不在 nodes 的端点静默跳过、无任何提示，修复版在结果区输出「通道端点已失效、未纳入计算」。保留入口→青铜馆→出口有效路径避免无路径提前 return。"
},
{
  "slug": "museum/visitor-route",
  "clicks": ["edges=[['A','B',137],['B','C',8]];var s=__visitor_routeSnap();var e=[];try{e=JSON.parse(s.__vrEdges||'[]');}catch(err){}document.getElementById('__tbProbe').textContent=(e.length===2&&e[0][0]==='A'&&e[0][2]==137&&e[1][1]==='C')?'SNAP OK':'SNAP BAD'"],
  "expect": ["SNAP OK"],
  "ref": "RL-K53 快照含通道数据：历史快照原先只采集带 id 的控件，通道行只有 data-i/data-k 无 id ⇒ 快照不含边。修复后 __visitor_routeSnap() 增加内部键 __vrEdges 序列化 edges。注入非默认边 A–B 137m/B–C 8m 后断言快照 __vrEdges 解析含两条边及 137/8 数值；旧版无该键解析为空 ⇒ SNAP BAD。"
},
{
  "slug": "museum/visitor-route",
  "clicks": ["document.getElementById('nodeInput').value='A,B,C';syncNodes();document.getElementById('startNode').value='A';document.getElementById('endNode').value='C';edges=[['A','B',5],['B','C',5]];__visitor_routeApplySnap({nodeInput:'A,B,C',startNode:'A',endNode:'C',__vrEdges:JSON.stringify([['A','B',90],['B','C',4]])},'结果');var h=String(document.getElementById('result').innerHTML);var ok=(edges.length===2&&edges[0][2]==90&&edges[1][2]==4&&h.indexOf('94 m')>=0);document.getElementById('__tbProbe').textContent=ok?'REPLAY OK':'REPLAY BAD'"],
  "expect": ["REPLAY OK"],
  "ref": "RL-K53 回放重建通道：把当前 edges 设为 5+5（总 10m），回放一条快照 edges=90+4（总 94m），修复后 __visitor_routeApplySnap() 先恢复 edges 再 compute ⇒ result 显示 94 m、edges 为 90/4；旧版无该函数（或回放只回填带 id 控件不动 edges）⇒ 仍是 10m ⇒ REPLAY BAD。94 m 非默认态。"
},
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='3';document.getElementById('era2').value='9';compare()"],
  "expect": [
    "建立时间相差: 838 年",
    "秦朝 15 年 vs 唐朝 289 年 (差 274 年)",
    "比值 0.25（相当于 25.0%；唐朝为秦朝的 4.00 倍）"
  ],
  "ref": "两个朝代 <select> 的 option 由 JS 按 ERAS 下标填充（静态无 option ⇒ clicks 赋值后调 compare()）：era1=3 秦朝(s=-221,dur=15,人口约2000万)、era2=9 唐朝(s=618,dur=289,人口约8000万) ⇒ 起始年差按无公元 0 年规则 = 618 + 221 − 1 = 838、时长差 |15−289|=274；人口按万=1e4 统一换算后 2e7/8e7=0.25（相当于 25.0%，唐朝为秦朝的 4 倍）。旧实现按未换算数字 2000/8000 求 max/min=4.0 倍，断言语义已切换为前/后比值。RL-K19：源码文案早已从「时间跨度相差」改为「建立时间相差」（e98f3a7d60），旧 expect 仍是「时间跨度相差」死锚、靠另外两条假绿，本批同步为现行文案。"
},
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='14';document.getElementById('era2').value='15';compare();var h=String(document.getElementById('result').innerHTML);var y=new Date().getFullYear();document.getElementById('__tbProbe').textContent=(h.indexOf('- '+y+' 年')>=0)?'NOWYEAR OK':'NOWYEAR STALE '+y"],
  "expect": [
    "NOWYEAR OK"
  ],
  "ref": "RL-K19 现代中国止年不能写死 2025：修复后 ERAS 末项 e=MODERN_END_YEAR=new Date().getFullYear()、dur=e-1949 ⇒ 哨兵「NOWYEAR OK」；批前版写死 e=2025/dur=76 ⇒ 哨兵「NOWYEAR STALE 2025/76」不命中。锚不锁具体年份、不依赖当前时间，只校验动态一致性。"
},
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='9';document.getElementById('era2').value='10';compare()"],
  "expect": [
    "唐朝 约 8000 万（8000 万，约 公元 750 年） vs",
    "宋朝 约 1 亿（1 亿，约 公元 1100 年）",
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
    "仅支持 1900-01-31 至 2099-12-31 的公历日期，请重新选择。"
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
  "clicks": ["evalEnv();"],
  "expect": [
    "温度偏高，建议降温至"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/showcase-monitor",
  "clicks": [
    "currentMat='ceramic';document.getElementById('temp').value='40';document.getElementById('rh').value='50';evalEnv();"
  ],
  "expect": [
    "温度偏高，建议降温至 35℃ 以下"
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
  "slug": "museum/timeline-viewer",
  "clicks": ["document.getElementById('tlCentury').value='b3';renderTimeline();var h=String(document.getElementById('timeline').innerHTML);document.getElementById('__tbProbe').textContent=(h.indexOf('前 221')>=0&&h.indexOf('前 202')>=0&&h.indexOf('前 2070')<0)?'CEN OK':'CEN BAD'"],
  "expect": ["CEN OK"],
  "ref": "RL-K48 世纪筛选：新增 tlCentury 下拉与 renderTimeline 世纪过滤；选「公元前 3 世纪」(-300..-201) 应含前 221 秦统一、前 202 汉建立，不含前 2070 夏（前 21 世纪）。批前版无该控件（钩子缺失即缺陷）、无过滤、渲染全表 ⇒ 哨兵不成立。"
},
{
  "slug": "museum/timeline-viewer",
  "clicks": ["document.getElementById('tlKeyword').value='甲午';renderTimeline();var h=String(document.getElementById('timeline').innerHTML);document.getElementById('__tbProbe').textContent=(h.indexOf('1894')>=0&&h.indexOf('甲午战争')>=0&&h.indexOf('夏朝建立')<0)?'KW OK':'KW BAD'"],
  "expect": ["KW OK"],
  "ref": "RL-K48 关键词筛选 + 算例数据补齐：新增 tlKeyword 输入框按标题/分类/简述过滤，且中国历史补 1405 郑和、1861 洋务、1894 甲午三条算例事件（深度解析算例原有但数据缺失）。输入「甲午」应只显示 1894 甲午战争、不含夏朝建立；批前版无控件无该事件 ⇒ 哨兵不成立。"
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
    "129 秒"
  ],
  "ref": "总时长 = 20×60 + (20−1)×20 + 30 = 1200+380+30 = 1610 秒 ⇒ fmtTime 26分50秒；可用 = 50×60 = 3000 秒 ⇒ 50分0秒；时间差 = +1390 秒 ⇒ +23分10秒（充裕）；每件可用 = floor((3000−19×20−30)/20) = 129 秒。默认态（30 件/90 秒/移动 30/开场 60/可用 90 分钟）为 1时0分30秒 / +29分30秒 / 180 秒，三条全不命中。"
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
  "ref": "总时长 = 40×120 + 39×30 + 60 = 4800+1170+60 = 6030 秒 ⇒ 1时40分30秒；可用 = 2400 秒 ⇒ 40分0秒；时间差 = −3630 秒（< −300 ⇒ 「严重超时」）；每件可用 = floor((2400−39×30−60)/40) = 29 秒；cutPer = floor((2400 − 39×30 − 60)/40) = 29 秒（旧实现误乘 120×2400 得 7169 秒）；展品数 = floor((2400−60)/(120+30)) = 15 件。默认态全不命中。"
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
    "590 秒",
    "1分0秒 讲解总时长"
  ],
  "ref": "总时长 = 1×50 + 0（count>1 为假 ⇒ 移动 0 段）+ 10 = 60 秒 ⇒ 1分0秒；可用 = 600 秒 ⇒ 10分0秒；时间差 = +540 秒；每件可用 = floor((600−0−10)/1) = 590 秒。表格里「移动时间 × 0 段 = 0 秒」是本例独有形态，默认态（29 段移动）不命中。"
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
    "可用时间需大于 0 分钟，无法排程。"
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
} ,
{dynDom:true, slug:"museum/audio-guide-timer", inputs:{exhibitCount:"3",perExhibit:"40",moveTime:"20",introTime:"0",available:"1.6666666666666667"},clicks:["calcQuick();"],expect:["减少讲解展品数至 2 件"],ref:"100 秒恰好容纳两件 40 秒讲解及一次 20 秒移动。"},
{dynDom:true, slug:"museum/audio-guide-timer", inputs:{exhibitCount:"3",perExhibit:"50",moveTime:"20",introTime:"30",available:"1"},clicks:["calcQuick();"],expect:["剩余时间不足以安排一件展品的讲解"],ref:"开场 30 秒后剩余 30 秒，少于单件 50 秒。"},
{ slug:"museum/exhibit-spacing", inputs:{"artWidth":"","artHeight":"","centerH":"","hAngle":"","vAngle":"","eyeH":"","viewers":"","shoulder":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ "slug":"museum/historical-calendar", "clicks":["document.getElementById('res').textContent='T1='+getSolarTerm(2024,12,21)+'/T2='+getSolarTerm(2024,12,22)+'/T3='+getSolarTerm(2024,8,22)"], "expect":["T1=冬至/T2=/T3=处暑"], "ref":"RL-K35：2024 年冬至为 12-21，12-22 不应再标冬至；处暑为 08-22。按太阳黄经逐年计算后不再用固定月日表。" },
{
  "slug": "museum/historical-calendar",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/museum/historical-calendar.html','utf8');var a=solarToLunar(1900,1,1),b=solarToLunar(1900,1,30),c=solarToLunar(1900,1,31),d=solarToLunar(2099,12,31),e=solarToLunar(2100,1,1);var ok=a===null&&b===null&&c&&c.y===1900&&c.m===1&&c.d===1&&d&&d.y===2099&&e===null&&h.indexOf('1900-01-31')>=0;document.getElementById('__tbProbe').textContent='HISTBOUND '+(ok?'OK':'BAD');"],
  "expect": ["HISTBOUND OK"],
  "ref": "第280批：LUNAR_INFO 基准为 1900-01-31，早于基准会得到负偏移/1899 年。solarToLunar 必须对 1900-01-01、1900-01-30 返回 null，1900-01-31 正常；2099-12-31 合法、2100-01-01 拒绝；日期控件 min 必须为 1900-01-31。旧版仅判 y<1900、min=1900-01-01 ⇒ BAD。"
},
{
  "slug": "museum/historical-calendar",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/museum/historical-calendar.html','utf8');var deep=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/museum/historical-calendar.json','utf8');var dj=JSON.parse(deep)['museum/historical-calendar'];var djx=JSON.stringify(dj);var ok=h.indexOf('1900–2100')<0&&h.indexOf('1900-2100')<0&&h.indexOf('1900–2099')>=0&&djx.indexOf('1900–2100')<0&&djx.indexOf('1900–2099')>=0&&en.indexOf('1900–2100')<0&&en.indexOf('1900–2099')>=0;document.getElementById('__tbProbe').textContent='HISTRANGE '+(ok?'OK':'BAD');"],
  "expect": ["HISTRANGE OK"],
  "ref": "第280批：历史日历实际仅支持到 2099，正文、深解源与英文词典不得再称 1900–2100。旧版三处均写 2100 ⇒ BAD。"
}
,{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='4';document.getElementById('era2').value='9';compare()"],
  "expect": ["存续 421 年", "建立时间相差: 819 年"],
  "ref": "跨公元前后（RL-K36）：汉朝 −202→220 无公元 0 年 ⇒ 421 年（旧版 422）；汉唐建立差 618+202−1=819。锚选非默认汉/唐组合，默认秦/唐不命中。"
},
{
  "slug": "museum/showcase-monitor",
  "inputs": {"temp":"19","rh":"","tempSwing":"2","rhSwing":"5"},
  "clicks": ["evalEnv();"],
  "expect": ["请填写实测温度、实测相对湿度及两项日波动允差后再判定"],
  "ref": "缺测守卫（RL-K37）：湿度留空不得给出瞬时达标结论；旧版把空字符串当 0 或跳过判定。锚为缺测提示整句，正常输入不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {"exhibitCount":"2.5","perExhibit":"120","moveTime":"30","introTime":"60","available":"20"},
  "clicks": ["calcQuick();"],
  "expect": ["展品数量需为不小于 1 的整数。"],
  "ref": "小数展品（RL-K38）：2.5 件不得被 parseInt 截断为 2 件继续排程；旧版不输出该提示。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {"lampCount":"1.9","lumens":"500","distance":"0.8","beamAngle":"36","utilCoef":"0.7","area":"2","trans":"92"},
  "clicks": ["calc();"],
  "expect": ["光源数量需为大于 0 的整数（小数不会截断为整数）。"],
  "ref": "小数灯数（RL-K38）：1.9 盏不得截断为 1 盏；旧版 parseInt 后输出 1 盏结果，不含该提示。"
},
{
  "slug": "museum/lighting-lux",
  "inputs": {"lampCount":"4","lumens":"500","distance":"0.8","beamAngle":"180","utilCoef":"0.7","area":"2","trans":"92"},
  "clicks": ["calc();"],
  "expect": ["光束角需大于 0 且小于 180 度"],
  "ref": "180° 边界（RL-K38）：tan(90°) 无有限值，必须拒绝并提示，不得输出 Infinity/NaN 光斑。"
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
