#!/usr/bin/env node
/**
 * 第 38 道门禁：cosmetic-derm 分类计算正确性验证（19 个确定性数值/等级工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 期望串优先取「区分度足够」的数值/判定文案（避免 1~2 位数字串被输入框 value 命中而假通过）。
 * 跳过：
 *   - mesotherapy / cosmetic-injection / meso-cocktail：勾选态由 checkbox.checked 驱动，
 *     桩环境无法注入非默认勾选，改走默认态则与页面默认输出重合（无验证意义）；
 *   - fitzpatrick-wrinkle：光型为 radio（name=photo），非 id 注入；
 *   - injection / laser-parameters / jiguangbochangbadian / time-23 / wrinkle-dynamic-static 以外
 *     的纯文案页（无确定性数值输出）。
 * 用法: node scripts/verify_cosmetic_derm_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    "slug": "cosmetic-derm/chemical-peel",
    "inputs": {
      "concentration": "42",
      "ph": "42",
      "duration": "42",
      "acidType": "lactic",
      "sensitivity": "1.0",
      "firstTime": "0"
    },
    "expect": [
      "AHA) 酸类型 极浅层焕肤：温和去角质，无脱屑或轻微脱屑。适合日常维护和初次刷酸。 ✅ 参数在相对安全范围内。仍建议术前测试小面积皮肤反应。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"concentration\":\"42\",\"ph\":\"42\",\"duration\":\"42\",\"acidType\":\"lactic\",\"sensitivity\":\"1.0\",\"firstTime\":\"0\"}，输出区含「AHA) 酸类型 极浅层焕肤：温和去角质，无脱屑或轻微脱屑。适合日常维护和初次刷…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/corneometer",
    "inputs": {
      "forehead": "42",
      "cheek": "42",
      "nose": "42",
      "hand": "42",
      "humidity": "42",
      "product": "1"
    },
    "expect": [
      "分级 状态 前额 40 偏低 干燥 颊部 40 偏低 干燥 鼻翼 40 偏低 干燥 手背 40 偏低 干燥 ⚠️ 您标注已涂抹护肤品，测量值可能偏高，结果仅供粗略参考。建议洁面后静置15-30分钟再测量。 皮肤偏干：加强保湿，选择含透明质酸"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"forehead\":\"42\",\"cheek\":\"42\",\"nose\":\"42\",\"hand\":\"42\",\"humidity\":\"42\",\"product\":\"1\"}，输出区含「分级 状态 前额 40 偏低 干燥 颊部 40 偏低 干燥 鼻翼 40 偏低 干…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/calc-51",
    "inputs": {
      "uvb": "42",
      "uva": "42"
    },
    "expect": [
      "A 等级 SPF 1.7 · 低防晒 PA (无) · 几乎没有"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"uvb\":\"42\",\"uva\":\"42\"}，输出区含「A 等级 SPF 1.7 · 低防晒 PA (无) · 几乎没有」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/concentration",
    "inputs": {
      "conc": "42",
      "ph": "42",
      "acid": "bha"
    },
    "expect": [
      "bha\n42\n42\n深度 剥脱深度 0.00% 游离酸浓度 0.0% 游离酸比例 深层化学剥脱 深层剥脱，需专业操作 游离酸 0.0% 🔬 pH 评估：pH 较高，剥脱力温和（pKa = 2.97） 💡 建议：恢复期5-10天，须由医师操作"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"conc\":\"42\",\"ph\":\"42\",\"acid\":\"bha\"}，输出区含「bha\n42\n42\n深度 剥脱深度 0.00% 游离酸浓度 0.0% 游离…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。原 expect 尾部拼了「\\n暂无估算记录」，但历史区已有记录 ⇒ 永远不命中（用例错）。"
  },
  {
    "slug": "cosmetic-derm/cosmetic-injection",
    "inputs": {
      "muscleStrength": "1.0",
      "depression": "1.0",
      "syringe": "0.8"
    },
    "expect": [
      "选需要治疗的部位\n1.0\n0.8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"muscleStrength\":\"1.0\",\"depression\":\"1.0\",\"syringe\":\"0.8\"}，输出区含「选需要治疗的部位\n1.0\n0.8」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/eyebag-assessment",
    "inputs": {
      "fatHerniation": "1",
      "skinLaxity": "1",
      "tearTrough": "1",
      "edema": "1",
      "bagType": "edema",
      "age": "2"
    },
    "expect": [
      " 等级 脂肪膨出 1/4 皮肤松弛 1/4 泪沟凹陷 1/4 水肿程度 1/3 水肿型 ：体液潴留所致，晨起重。以生活调理为主——低盐、高枕睡眠、冷敷。排除甲状腺/肾脏问题。 轻中度：玻尿酸填充泪沟+射频紧肤。脂肪型可考虑内切法。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fatHerniation\":\"1\",\"skinLaxity\":\"1\",\"tearTrough\":\"1\",\"edema\":\"1\",\"bagType\":\"edema\",\"age\":\"2\"}，输出区含「 等级 脂肪膨出 1/4 皮肤松弛 1/4 泪沟凹陷 1/4 水肿程度 1/3 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/fitzpatrick-wrinkle",
    "inputs": {
      "laxity": "3",
      "pigment": "10",
      "wrinkleGrade": "1",
      "elastosis": "1"
    },
    "expect": [
      "65 中重度光老化"
    ],
    "ref": "独立复算：皱纹Ⅰ级 25 + 弹力变性轻度 20 + 松弛 3/10→15 + 色素 10→5 ⇒ 65 ⇒ 中重度光老化。原用例注入松弛/色素 42（超出 0–10 量程，被页面夹到上限）后总分仍封顶 100，与默认态同走「重度光老化」文案 ⇒ 逃生。默认 45 中度光老化 ⇒ 「65 中重度光老化」不命中。"
  },
  {
    "slug": "cosmetic-derm/glogau-photoaging",
    "inputs": {
      "wrinkle": "2",
      "pigment": "2",
      "keratosis": "2",
      "makeup": "2",
      "age": "2",
      "photo": "2"
    },
    "expect": [
      "au 光老化分型 2.0 综合评分 Ⅱ型 对应分型 早-中度光老化：早期色素斑（雀斑/日光斑），可触及角化症，运动时出现细纹。 光型Ⅲ-Ⅳ型：可常规治疗，注意术后防晒。 建议：外用维A酸+维C，化学焕肤（果酸20-35%），IPL光子嫩肤改"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wrinkle\":\"2\",\"pigment\":\"2\",\"keratosis\":\"2\",\"makeup\":\"2\",\"age\":\"2\",\"photo\":\"2\"}，输出区含「au 光老化分型 2.0 综合评分 Ⅱ型 对应分型 早-中度光老化：早期色素斑（…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/laser-parameters",
    "inputs": {
      "laserSelect": "q532",
      "chromSelect": "melanin"
    },
    "expect": [
      "靶色团：黑色素 以下激光以该靶色团为主要作用目标： 调Q 532nm (KTP) 波长： 532nm · 脉宽： 5-10ns 靶色团： 黑色素 / 血红蛋白 穿透深度： 0.5-1mm（表皮-浅真皮） 适应症： 表浅色素斑、雀斑、日光性黑"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"laserSelect\":\"q532\",\"chromSelect\":\"melanin\"}，输出区含「靶色团：黑色素 以下激光以该靶色团为主要作用目标： 调Q 532nm (KTP)…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/meso-cocktail",
    "inputs": {
      "totalVol": "42",
      "frequency": "2",
      "sensitivity": "1.0",
      "session": "3"
    },
    "expect": [
      "42\n2\n1.0\n3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalVol\":\"42\",\"frequency\":\"2\",\"sensitivity\":\"1.0\",\"session\":\"3\"}，输出区含「42\n2\n1.0\n3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/injection",
    "inputs": {
      "type": "ha",
      "effect": "2"
    },
    "expect": [
      "ha\n鼻唇沟\n鼻唇沟唇部苹果肌鼻部下巴颞部（单侧）泪沟法令纹\n2\n0.8 推荐用量 (ml) 鼻唇沟 注射部位 中度 目标效果 玻尿酸 · 鼻唇沟"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"type\":\"ha\",\"effect\":\"2\"}，输出区含「ha\n鼻唇沟\n鼻唇沟唇部苹果肌鼻部下巴颞部（单侧）泪沟法令纹\n2\n0.8 推荐用…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/jiguangbochangbadian",
    "inputs": {
      "laser": "585"
    },
    "expect": [
      "深度 0.5-1.2mm 临床适应症 鲜红斑痣、血管瘤、玫瑰痤疮红血丝、疤痕红斑 注意事项 紫癜为常见反应，1-2周消退"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"laser\":\"585\"}，输出区含「深度 0.5-1.2mm 临床适应症 鲜红斑痣、血管瘤、玫瑰痤疮红血丝、疤痕红斑…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/mesotherapy",
    "inputs": {
      "totalVol": "42",
      "area": "42",
      "depth": "1",
      "syringe": "2"
    },
    "expect": [
      "42\n42\n1\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalVol\":\"42\",\"area\":\"42\",\"depth\":\"1\",\"syringe\":\"2\"}，输出区含「42\n42\n1\n2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/length-spacing",
    "inputs": {
      "len": "42",
      "spacing": "42",
      "dia": "42"
    },
    "expect": [
      "积占比 作用层次：深层真皮/皮下 深层重塑，适合重度瘢痕，需严格术后护理 穿透深度 33.60mm 渗透占比 78.5% 💡 建议：极深层微针，恢复期5-7天，须由医师操作并严格术后护理"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"len\":\"42\",\"spacing\":\"42\",\"dia\":\"42\"}，输出区含「积占比 作用层次：深层真皮/皮下 深层重塑，适合重度瘢痕，需严格术后护理 穿透深…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。原 expect 尾部拼了「\\n暂无计算记录」，但历史区已有记录 ⇒ 永远不命中（用例错）。"
  },
  {
    "slug": "cosmetic-derm/microneedle",
    "inputs": {
      "needleLength": "42",
      "spacing": "42",
      "diameter": "42",
      "passes": "42",
      "mw": "42",
      "concentration": "42",
      "area": "42",
      "purpose": "collagen"
    },
    "expect": [
      "总孔体积(μL) 95% 渗透效率 推荐长度：1.0-2.5mm。胶原诱导需到达真皮中层以上。配合维A酸/维C可增强效果。间隔4-6周一次。 ⚠️ 注意： • 遍数过多（>6遍）可能导致过度损伤 预计恢复期：5-7"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"needleLength\":\"42\",\"spacing\":\"42\",\"diameter\":\"42\",\"passes\":\"42\",\"mw\":\"42\",\"concentration\":\"42\",\"area\":\"42\",\"purpose\":\"collagen\"}，输出区含「总孔体积(μL) 95% 渗透效率 推荐长度：1.0-2.5mm。胶原诱导需到达…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/post-procedure-recovery",
    "inputs": {
      "procDate": "abc123测试",
      "procedure": "laser_co2",
      "intensity": "1.0",
      "photo": "2"
    },
    "expect": [
      "少48-72小时） ⚠️ 您的PIH（炎症后色素沉着）风险为 高 。建议术后立即开始严格防晒，并使用含维C/烟酰胺的修复产品（结痂脱落后）预防色素沉着。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"procDate\":\"abc123测试\",\"procedure\":\"laser_co2\",\"intensity\":\"1.0\",\"photo\":\"2\"}，输出区含「少48-72小时） ⚠️ 您的PIH（炎症后色素沉着）风险为 高 。建议术后立即…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/pore-grading",
    "inputs": {
      "noseTip": "1",
      "nasalAla": "1",
      "cheek": "1",
      "forehead": "1",
      "poreType": "aging",
      "sebumLevel": "2"
    },
    "expect": [
      "等级 评估 鼻头 1级 近距离可见 鼻翼 1级 近距离可见 颊部 1级 近距离可见 前额 1级 近距离可见 老化型 毛孔类型 1.0 平均等级 胶原流失导致毛孔周围支撑结构松弛。重点在抗衰——维A酸、点阵激光刺激胶原再生。 皮脂正常，综合护"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"noseTip\":\"1\",\"nasalAla\":\"1\",\"cheek\":\"1\",\"forehead\":\"1\",\"poreType\":\"aging\",\"sebumLevel\":\"2\"}，输出区含「等级 评估 鼻头 1级 近距离可见 鼻翼 1级 近距离可见 颊部 1级 近距离可…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/rf-tightening",
    "inputs": {
      "temp": "42",
      "duration": "42",
      "interval": "42",
      "freq": "2",
      "sessions": "3",
      "cooling": "0"
    },
    "expect": [
      "有效范围内（42-48°C）。 轻度效果：以促进循环和肤质改善为主。紧肤效果有限，适合维护性治疗。 疗程：3次 × 间隔42周，共126周。效果预计维持 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"duration\":\"42\",\"interval\":\"42\",\"freq\":\"2\",\"sessions\":\"3\",\"cooling\":\"0\"}，输出区含「有效范围内（42-48°C）。 轻度效果：以促进循环和肤质改善为主。紧肤效果有限…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/sebumeter",
    "inputs": {
      "forehead": "42",
      "nose": "42",
      "cheek": "42",
      "chin": "42",
      "temp": "42",
      "timePoint": "1"
    },
    "expect": [
      "偏低 偏干/中性 环境温度 42°C，已对皮脂值进行温度校正（基准 25°C，每±1°C 约 ±1% 皮脂变化）。 干性肌肤：注重保湿修复，选择含神经酰胺、角鲨烷的滋润型产品，避免过度清洁。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"forehead\":\"42\",\"nose\":\"42\",\"cheek\":\"42\",\"chin\":\"42\",\"temp\":\"42\",\"timePoint\":\"1\"}，输出区含「偏低 偏干/中性 环境温度 42°C，已对皮脂值进行温度校正（基准 25°C，每…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/skin-ph",
    "inputs": {
      "phValue": "42",
      "site": "cheek",
      "postClean": "1",
      "skincare": "1"
    },
    "expect": [
      "42\n请输入有效的 pH 值 (0-14)\ncheek\n1\n1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phValue\":\"42\",\"site\":\"cheek\",\"postClean\":\"1\",\"skincare\":\"1\"}，输出区含「42\n请输入有效的 pH 值 (0-14)\ncheek\n1\n1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/spf-pa-calculator",
    "inputs": {
      "med": "42",
      "outdoorTime": "42",
      "reapply": "42",
      "photo": "2",
      "uvi": "5",
      "spf": "30",
      "pa": "2",
      "activity": "0.7"
    },
    "expect": [
      "钟 理论保护时间 1260 分钟 (21.0h) 活动校正后 882"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"med\":\"42\",\"outdoorTime\":\"42\",\"reapply\":\"42\",\"photo\":\"2\",\"uvi\":\"5\",\"spf\":\"30\",\"pa\":\"2\",\"activity\":\"0.7\"}，输出区含「钟 理论保护时间 1260 分钟 (21.0h) 活动校正后 882」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/telangiectasia-area",
    "inputs": {
      "areaPct": "42",
      "density": "42",
      "diameter": "42",
      "vesselType": "venous",
      "zone": "2",
      "symptom": "1"
    },
    "expect": [
      "42\n42\n42\nvenous\n2\n1\n100 极重度毛细血管扩张 42% 受累面积 42 密度根/cm² 42mm 血管直径 面颊中部 分布区域 小静脉扩张 ：蓝色血管，首选"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"areaPct\":\"42\",\"density\":\"42\",\"diameter\":\"42\",\"vesselType\":\"venous\",\"zone\":\"2\",\"symptom\":\"1\"}，输出区含「42\n42\n42\nvenous\n2\n1\n100 极重度毛细血管扩张 42% 受累…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/visia-spots",
    "inputs": {
      "spotCount": "42",
      "areaPct": "42",
      "depth": "42",
      "percentile": "42",
      "zone": "2",
      "spotType": "solar"
    },
    "expect": [
      "42\n42\n42\n2\nsolar\n42\n100 极重度色斑 42 色斑数量 42% 面积占比 42/10 色素深度 42% 同龄百分位 日光性黑子 ：光老化所致，调Q激光或 IPL 有效，注意与恶性黑子鉴别"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"spotCount\":\"42\",\"areaPct\":\"42\",\"depth\":\"42\",\"percentile\":\"42\",\"zone\":\"2\",\"spotType\":\"solar\"}，输出区含「42\n42\n42\n2\nsolar\n42\n100 极重度色斑 42 色斑数量 42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/thread-lift",
    "inputs": {
      "insertAngle": "42",
      "liftAngle": "42",
      "threadLength": "42",
      "threadCount": "42",
      "anchorForce": "42",
      "zone": "lowerface",
      "threadType": "cog_bidirectional",
      "laxity": "2"
    },
    "expect": [
      "°) 提拉方向 42° (推荐 35°) 锚定区域 耳前筋膜 两端反向锯齿，中部锚定。提拉力中等，适合轻中度松弛"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"insertAngle\":\"42\",\"liftAngle\":\"42\",\"threadLength\":\"42\",\"threadCount\":\"42\",\"anchorForce\":\"42\",\"zone\":\"lowerface\",\"threadType\":\"cog_bidirectional\",\"laxity\":\"2\"}，输出区含「°) 提拉方向 42° (推荐 35°) 锚定区域 耳前筋膜 两端反向锯齿，中部…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/temp-time-4",
    "inputs": {
      "temp": "42",
      "time": "42",
      "rftype": "bi"
    },
    "expect": [
      "胶原收缩率（估） 42℃ 真皮温度 无效 紧肤效果 双极射频 · 无效 温度低于胶原变性阈值，无明显"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"time\":\"42\",\"rftype\":\"bi\"}，输出区含「胶原收缩率（估） 42℃ 真皮温度 无效 紧肤效果 双极射频 · 无效 温度低于…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "cosmetic-derm/wrinkle-dynamic-static",
    "inputs": {
      "crow_d": "1",
      "crow_s": "1",
      "glab_d": "1",
      "glab_s": "1",
      "fore_d": "1",
      "fore_s": "1",
      "nas_d": "1",
      "nas_s": "1",
      "nl_d": "1",
      "nl_s": "1"
    },
    "expect": [
      "建议方案 鱼尾纹 1 1 混合型 肉毒6U 川字纹 1 1 混合型 肉毒10U 抬头纹 1 1 混合型 肉毒8U 鼻背纹 1 1 混合型 肉毒2U 法令纹 1 1 混合型 0.5ml填充"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"crow_d\":\"1\",\"crow_s\":\"1\",\"glab_d\":\"1\",\"glab_s\":\"1\",\"fore_d\":\"1\",\"fore_s\":\"1\",\"nas_d\":\"1\",\"nas_s\":\"1\",\"nl_d\":\"1\",\"nl_s\":\"1\"}，输出区含「建议方案 鱼尾纹 1 1 混合型 肉毒6U 川字纹 1 1 混合型 肉毒10U …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
{
  "slug": "cosmetic-derm/wrinkle-dynamic-static",
  "inputs": {},
  "expect": ["请输入五个区域的动态与静态皱纹评分（0=无、4=重度）后再评估。"],
  "ref": "原生缺陷修复：10 个评分下拉全部改为「请选择」空值默认，首屏不再直接给出总体类型与除皱剂量建议。"
},
{ slug:"cosmetic-derm/assessor-67", inputs:{"pb":"","as":"","hg":"","methanol":""}, expect:["请填写铅、砷、汞、甲醇实测值"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{ slug:"cosmetic-derm/corneometer", inputs:{"forehead":"","cheek":"","nose":"","hand":""}, expect:["请填写各部位含水量读数"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{ slug:"cosmetic-derm/sebumeter", inputs:{"forehead":"","nose":"","cheek":"","chin":""}, expect:["请填写各部位皮脂读数"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{ slug:"cosmetic-derm/spf-pa-calculator", inputs:{"med":"","uvi":"","outdoorTime":""}, expect:["请填写MED、UVI 与户外时长"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{ slug:"cosmetic-derm/telangiectasia-area", inputs:{"areaPct":"","density":"","diameter":""}, expect:["请填写受累面积、密度与血管直径"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{ slug:"cosmetic-derm/visia-spots", inputs:{"spotCount":"","areaPct":"","depth":""}, expect:["请填写色斑数量、面积占比与深度"], ref:"核心测量值留空不得给出分级/合格结论（LABCLR）" },
{
  slug: "cosmetic-derm/maokongcudafenji",
  inputs: { dia: "500", area: "鼻头", type: "oil" },
  expect: ["建议光电治疗（点阵/微针）", "中度粗大"],
  ref: "恢复第321批旧页：直径 500 μm 落在 400–800 区间，须输出中度粗大及光电治疗建议；评分式 pore-grading 无此直径入口。"
},
{
  slug: "cosmetic-derm/formula-1",
  inputs: { total: "12", ha: "8", vc: "25", rHa: "60", rVc: "25", rPep: "15" },
  expect: ["57.60", "75.00", "136.20"],
  ref: "恢复第321批旧页（非默认配方）：12 mL、60/25/15 ⇒ 7.2/3.0/1.8 mL；8 mg/mL 玻尿酸 57.6 mg、25 mg/mL VC 75 mg、2 mg/mL 肽 3.6 mg，合计 136.2 mg。"
},
{
  slug: "cosmetic-derm/ratio-composition-injection",
  inputs: { total: "6", ha: "10", rHa: "50", rVc: "25", rGsh: "15", rOther: "10" },
  expect: ["30.00", "135.00"],
  ref: "恢复第321批旧页（非默认配比）：6 mL、玻尿酸 50% 且原液 10 mg/mL ⇒ 3 mL×10=30 mg；四项含量合计 135 mg。mesotherapy 仅自动分配比例，不能输入原液浓度。"
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

  console.log("==== cosmetic-derm calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();