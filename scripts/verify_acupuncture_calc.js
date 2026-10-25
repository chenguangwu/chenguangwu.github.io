#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "acupuncture/acupoint-injection",
  "inputs": {
    "points": "5"
  },
  "expect": [
    "5.00ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/acupoint-location",
  "inputs": { "realCm": "27", "targetCun": "6" },
  "clicks": ["selectRegion('chest');calc()"],
  "expect": [
    "3.00 每寸厘米",
    "18.00 cm",
    "天突(胸骨上窝)→歧骨(胸剑联合)"
  ],
  "ref": "selectRegion('chest') 自动选中首段「天突(胸骨上窝)→歧骨(胸剑联合)」（标准折量 9 寸）；实测 27 cm ⇒ 每寸 27/9 = 3.00 cm；目标 6 寸 ⇒ 定位 6×3.00 = 18.00 cm。默认态 currentPart 未选、realCm 为空 ⇒ result 只出提示文案，三串均不命中。"
},
  // 注：acupuncture/analysis-10 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "acupuncture/bloodletting-therapy",
  "inputs": {
    "points": "6"
  },
  "expect": [
    "1.32ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/cupping-mark-analysis",
  "clicks": [
    "selectMark('red');analyze();"
  ],
  "expect": [
    "鲜红 辨证分析"
  ],
  "ref": "弱用例去默认化（BATCH118）：原锚默认态「5-7」（消退天数常量，判别力0）。clicks 经 selectMark('red')+analyze() 切到鲜红罐印，expect 锚「鲜红 辨证分析」标题 —— 页面默认 currentMark 为 purple（默认态渲染「紫红 辨证分析」），故红色分析只在非默认态出现；清 clicks 兜底遍历不产出该串 ⇒ 零逃生项（锚「紫红」会撞默认态，不可用）。"
},
{
  "slug": "acupuncture/cupping-pressure",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "255"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/deqi-sensation",
  "inputs": {
    "patientScore": "5",
    "doctorScore": "5",
    "propagation": "1"
  },
  "expect": [
    "2.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/ear-acupressure",
  "clicks": ["selectArea('三角窝');"],
  "expect": [
    "共找到 3 个耳穴"
  ],
  "ref": "独立复算：EAR_POINTS 中 area 含「三角窝」的共 3 条（神门等），selectArea 写 currentArea 后 renderList 按 area 子串过滤，命中分支渲染「共找到 <strong>3</strong> 个耳穴」；默认 currentArea='all' 渲染总数 42 ⇒ 串不同。注意空态串「未找到匹配耳穴」不可用：零参兜底 selectArea() 会把 searchPart 置 undefined、同样落空态，属逃生项。"
},
{
  "slug": "acupuncture/electroacupuncture",
  "inputs": {
    "duration": "20",
    "purpose": "spasm"
  },
  "expect": [
    "spasm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/flash-cupping",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "10分钟)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/guasha-direction",
  "inputs": {
    "purpose": "pain"
  },
  "expect": [
    "舒筋止痛可重点在阿是穴及痛点周围加重"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/intradermal-needle",
  "inputs": {
    "part": "face"
  },
  "expect": [
    "0.35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/meridian-pathway",
  "inputs": {
    "sensType": "partial"
  },
  "expect": [
    "部分感传(短程)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/moxibustion-count",
  "inputs": {
    "moxaType": "aiJiong"
  },
  "expect": ["无明显反应 皮肤色白无温热感 局部温热 有温热感，皮肤略红 潮红红晕 皮肤潮红，温热舒适 灼热明显 灼热明显，红晕扩大 灼痛难忍 灼痛欲起泡，应止灸\n皮肤反应 基础壮数 判定 ● 无明显反应 3壮 皮肤色白无温热感 ● 局部温热 5壮 有温热感，皮肤略红 ● 潮红红晕 7壮 皮肤潮红，温热舒适 ● 灼热明显 9壮 灼热明显，红晕扩大 ● 灼痛难忍 止灸 灼痛欲起泡，应止灸 艾灸剂量原则： ①\"壮\"为艾炷灸的计量单位，每燃一个艾炷为一壮；②一般每穴 3-7 壮，急性病可至 7-10 壮；③以\"灸至皮肤潮红、患者温热舒适\"为适度；④化脓灸(瘢痕灸)每穴 5-9 壮，使局部组织烫伤化脓；⑤间接灸壮数可适当增加。\naiJiong\nmedium\nxu\nnormal\n灸法： 间接灸 ｜ 皮肤反应：潮红红晕 ｜ 证候：虚寒证 10 壮/穴（推荐） 范围 7 ~ 13 壮 7 反应基础壮 1.43 综合系数 ● 皮肤反应 施灸要点： · 间接灸，皮肤反应为「潮红红晕」时，推荐 10 壮。 间接灸(隔姜/隔蒜)每灸一壮更换衬垫，以局部温热红晕为度。"],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needle-retention",
  "inputs": {
    "age": "adult"
  },
  "expect": [
    "1.10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needling-depth",
  "inputs": {
    "bodyType": "medium"
  },
  "expect": ["百会 (DU20) 四神聪 (EX-HN1) 印堂 (EX-HN3) 太阳 (EX-HN5) 睛明 (BL1) 攒竹 (BL2) 迎香 (LI20) 下关 (ST7) 颊车 (ST6) 地仓 (ST4) 风池 (GB20) 风府 (DU16) 天柱 (BL10) 大椎 (DU14) 肺俞 (BL13) 心俞 (BL15) 肝俞 (BL18) 脾俞 (BL20) 肾俞 (BL23) 命门 (DU6) 膻中 (RN17) 中脘 (RN12) 神阙 (RN8) 气海 (RN6) 关元 (RN4) 中极 (RN3) 肩髃 (LI15) 曲池 (LI11) 手三里 (LI10) 外关 (SJ5) 内关 (PC6) 合谷 (LI4) 环跳 (GB30) 风市 (GB31) 阳陵泉 (GB34) 足三里 (ST36) 上巨虚 (ST37) 丰隆 (ST40) 三阴交 (SP6) 阴陵泉 (SP9) 委中 (BL40) 承山 (BL57) 昆仑 (BL60) 太冲 (LR3) 太溪 (KI3) 太白 (SP3) 涌泉 (KI1)\n进针角度 适用部位 角度范围 说明 直刺 大部分穴位 90° 肌肉丰厚处最常用 斜刺 骨骼边缘/内有脏器 45° 避开血管或防伤脏器 平刺(横刺) 头面/胸背皮薄处 15° 沿皮刺，多用于头部 深度安全原则： ①胸背穴位向脊柱方向斜刺，控制深度防伤肺；②项部风池风府不可深刺防伤延髓；③眼周穴位缓慢进针禁提插；④孕妇腹部腰骶及合谷三阴交禁针。\nmedium\nyoung\nnormal\n穴位： 百会 (DU20) ｜ 部位：头部 ｜ 标准深度： 0.5寸 0.50 寸 建议进针深度（约 1.1 cm） 平刺 0.30 深度下限(寸) 0.50 推荐深度(寸) 0.65 深度上限(寸) 操作要点： 平刺0.5-0.8寸，沿皮刺 个体化调整明细： · 体型系数：适中 × 1 · 年龄系数：青中年 × 1 · 体质系数：一般 × 1 · 综合系数：1.00（标准 0.5寸 × 1.00 = 0.50寸）"],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/pediatric-tuina",
  "inputs": {
    "constitution": "weak"
  },
  "expect": [
    "144"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-acupoint",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-time",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore(default-hit)（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "acupuncture/tuina-frequency",
  "inputs": {
    "duration": "8"
  },
  "expect": ["滚法 揉法 推法 拿法 按法 摩法 擦法 捏法 拨法 抖法 摇法 拨伸法 拍法 点法\n手法 频率(次/分) 力度 适用/要点 滚法 140~160 中 腕关节主动屈伸，压力持续，用于颈肩腰背 揉法 120~160 中 带动皮下组织，用于脾胃、躯干 推法 60~120 中 直线推动，平推/直推/分推 拿法 60~80 较强 捏而提起，用于颈项、肩部、四肢 按法 30~60 较强 垂直按压，逐渐用力，用于穴位 摩法 80~120 轻 环形抚摩，用于胸腹，宜轻缓 擦法 100~140 中 直线往返摩擦，以透热为度 捏法 60~90 中 捏脊常用，用于小儿及背部 拨法 40~60 较强 垂直肌纤维方向弹拨，解痉止痛 抖法 120~160 轻 抖动肢体，放松肌肉 摇法 20~40 中 摇动关节，柔和缓慢，用于关节 拨伸法 5~15 较强 拔伸牵引，持续缓慢，用于关节 拍法 60~100 中 虚掌拍打，用于腰背下肢 点法 30~50 强 点压穴位，由轻到重 手法基本要求： 持久（保持一定时间）、有力（力度适当）、均匀（节律一致）、柔和（轻而不浮重而不滞）、深透（力达病所）。频率与力度需配合，频率快则力度宜轻，频率慢则力度可稍重。\nrelax\nnormal\n8\n手法： 滚法 ｜ 标准频率 140~160 次/分 ｜ 力度：中 150 次/分钟（推荐） 范围 128 ~ 173 次/分 30 105 180 8 操作时长(分) 1200 总次数 0.40 单次秒数 操作要点： 腕关节主动屈伸，压力持续，用于颈肩腰背；中频偏柔和。 · 8分钟约操作 1200 次，单次约 0.40 秒。"],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/tuina-medium",
  "inputs": {
    "technique": "ca"
  },
  "expect": [
    "适配擦/推法"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/warm-needle-moxibustion",
  "inputs": {
    "ambTemp": "38"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
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

  console.log("==== acupuncture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
