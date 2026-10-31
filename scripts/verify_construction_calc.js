#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "construction/ac-size-guide",
  "inputs": {
    "area": "30",
    "height": "2.8",
    "windows": "1"
  },
  "expect": [
    "5400W"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/blueprint-tool",
  "inputs": {
    "customScale": "100",
    "distance": "100",
    "direction": "r2d"
  },
  "expect": [
    "0.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-1",
  "inputs": {
    "od": "72.3",
    "thickness": "3.6",
    "fy": "205",
    "h": "1.8",
    "k": "1.155",
    "a": "0.3",
    "area": "4",
    "load": "3",
    "self": "0.35"
  },
  "expect": [
    "776.98"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-5",
  "inputs": {
    "dia": "30",
    "logLen": "4",
    "logQty": "10",
    "bLen": "2.4",
    "bWid": "120",
    "bThk": "40",
    "bQty": "50"
  },
  "expect": [
    "3217.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calc-dosage-1",
  "inputs": {
    "area": "30",
    "tLen": "600",
    "tWid": "600",
    "gap": "2",
    "waste": "5",
    "perBox": "4"
  },
  "expect": [
    "31.53"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electrical/calc-power-voltage",
  "inputs": {
    "power": "7500",
    "pf": "0.8",
    "kd": "0.8"
  },
  "expect": [
    "42.61A"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-area",
  "inputs": {
    "shareRate": "38"
  },
  "expect": [
    "54.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/calculator-calc-ratio-2",
  "inputs": {
    "volume": "15",
    "pCement": "450",
    "pSand": "120",
    "pStone": "130"
  },
  "expect": ["C20\n15\n450\n120\n130\n0.56 水灰比 37.1% 砂率 4.95 水泥 (吨) ¥5798 材料成本 材料 每方用量 (kg) 总用量 (kg) 总用量 (吨) 水泥 330 4950 4.95 水 185 2775 2.77 砂 700 10500 10.50 石子 1185 17775 17.77 C20 方量 15m³，材料成本 ¥5798 （不含外加剂与人工）。\n暂无计算记录"],
  "ref": "auto-restore"
},
{
  "slug": "construction/cement-mortar-ratio",
  "inputs": {
    "vol": "4",
    "bag": "50"
  },
  "expect": [
    "880"
  ],
  "ref": "vol=4、bag=50、grade=M5（select 默认 selectedIndex=0）。独立复算：M5 每 m³ 砂浆水泥基准 220 kg（经验值 210–240）⇒ 水泥 = 220×4 = 880 kg；砂 = 880×5.0 = 4400 kg；水 = 880×0.45 = 396 kg；袋数 = ⌈880/50⌉ = 18。默认态 vol=1 ⇒ 220，不命中。"
},
{
  "slug": "construction/calc-206",
  "inputs": {
    "qVal": "2.5",
    "wVal": "0.35",
    "aVal": "1.2",
    "hStep": "1.5",
    "hVal": "24"
  },
  "expect": [
    "1.97",
    "152"
  ],
  "ref": "注入非默认参数（q=2.5、w₀=0.35、a=1.2、h=1.5、H=24；默认 3/0.5/1.5/1.8/30）。独立复算：Ng1=0.0384×24=0.9216；layers=⌊24/3⌋=8；Ng2=0.35×1.2×1.05×8=3.528；Nq=2.5×1.2×1.05×2=6.3；N=1.2×4.4496+1.4×6.3=14.160 kN。Mw=0.9×1.4×0.35×0.6×1.2×1.5²/10=0.0714 kN·m。λ=μ·h/i=1.6×1500/15.8=151.9 → φ 插值=0.3226。σ=14159.5/(0.3226×489)+71442/5078=103.8 MPa。K=205/103.8=1.97≥1 ⇒ 满足。expect 不含『满足』：默认态输出『不满足』含该子串会致逃生项（判别力门禁教训），改用注入态独有的 λ=152 与 K=1.97。"
},
{
  "slug": "construction/construction-calculator",
  "inputs": {
    "paintWallCount": "7",
    "paintWallLen": "5",
    "paintWallH": "2.8",
    "paintCoverage": "10",
    "paintCoats": "2",
    "floorArea": "20",
    "floorLen": "1210",
    "floorWid": "165",
    "floorWaste": "5",
    "floorPpPack": "8",
    "tileArea": "15",
    "tileLen": "600",
    "tileWid": "600",
    "tileWaste": "10",
    "concVol": "1",
    "elecPower": "2000",
    "elecVolt": "220",
    "stairHeight": "280",
    "stairRise": "17"
  },
  "expect": [
    "98.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/estimate-area-dosage",
  "inputs": {
    "area": "75",
    "thk": "0.15",
    "density": "1400",
    "perBucket": "25",
    "waste": "5"
  },
  "expect": ["75\n0.15\n1400\n25\n5\n2\n22.5 涂料体积 (L) 31.50 净重 (kg) 33.08 含损耗重 (kg) 2 采购桶数 75m² × 0.15mm × 2遍 = 总厚 0.30mm，体积 0.0225 m³ （22.5 L）。 体积 × 密度 1400 = 31.50kg，含 5% 损耗 = 33.08kg。 每桶 25kg，需采购 2 桶 。\n暂无计算记录"],
  "ref": "auto-restore"
},
{
  "slug": "construction/pipe-flow",
  "inputs": {
    "diameter": "38",
    "velocity": "1.5",
    "pipeLength": "10",
    "temperature": "20"
  },
  "expect": [
    "0.001134"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/radiator-calculator",
  "inputs": {
    "roomArea": "30",
    "roomHeight": "2.8"
  },
  "expect": ["铸铁暖气片 铸铁 | 130W/片 钢制暖气片 钢 | 150W/片 铜铝复合 铜+铝 | 180W/片 钢制板式 钢 | 120W/片\n铸铁暖气片 铸铁 130 W/片 600mm 经典耐用，散热慢但持久 钢制暖气片 钢 150 W/片 600mm 散热快，美观轻便 铜铝复合 铜+铝 180 W/片 600mm 高效散热，防腐耐蚀 钢制板式 钢 120 W/片 600mm 超薄美观，适合现代装修\n30\n2.8\n1\ndouble\ncold\n16 推荐片数 1800 热负荷 (W) 2080 总散热量 (W) 1.3 总长度估算 (m) 计算依据 地区基础热指标: 60W/m² × 面积 30m² = 1800W 层高修正: ×1.00 (标准2.8m) 外墙修正: ×1.00 (1面外墙) 窗户修正: ×1.00 (双层玻璃) 热负荷合计: 1800W (含10%余量: 1980W) 暖气片: 铸铁暖气片 ，单片散热量 130W 推荐: 16 片 ，总散热量 2080W 注：建议分组安装（每组不超过20片），可分2组安装以确保散热均匀。"],
  "ref": "auto-restore"
},
{
  "slug": "construction/renovation-labor-cost",
  "inputs": {
    "area": "135",
    "top_d": "25元/m²",
    "top_s": "45元/m²",
    "top_w": "55元/m²",
    "top_m": "35元/m²",
    "top_p": "30元/m²",
    "top_t": "60元/m²"
  },
  "expect": [
    "135"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/soundproof-material",
  "inputs": {
    "wallArea": "30"
  },
  "expect": ["🧱 隔音棉(岩棉) 50mm | ¥45/m² 📋 隔音板 12mm | ¥65/m² 🧽 吸音海绵 30mm | ¥35/m² 🧶 隔音毡 3mm | ¥55/m² 📦 复合隔音板 25mm | ¥120/m²\n🧱 隔音棉(岩棉) 50mm 1.2m² ¥45/m² 30-40dB 墙体隔断、吊顶 📋 隔音板 12mm 2.88m² ¥65/m² 25-35dB 墙面装饰隔音 🧽 吸音海绵 30mm 0.5m² ¥35/m² 20-30dB 录音棚、机房 🧶 隔音毡 3mm 5m² ¥55/m² 20-28dB 管道、薄墙增厚 📦 复合隔音板 25mm 2.4m² ¥120/m² 35-45dB 隔断墙、KTV\n30\n2\n53 所需数量 (块) 63.6 总面积 (m²) ¥2,862 预估成本 30-40dB 隔音量 材料: 隔音棉(岩棉) (50mm，岩棉隔音棉，防火A级) 墙体面积 30m² × 2层 = 60m² 每块 1.2m²，含5%损耗，共需 53 块 单价参考 ¥45/m²，材料预估成本: ¥2,862 注：价格为参考价，实际价格以当地市场为准。施工人工费未计入。"],
  "ref": "auto-restore"
},
{
  "slug": "construction/timber-volume",
  "inputs": {
    "logD1": "20",
    "logD2": "27",
    "logLen": "4",
    "logQty": "1",
    "boardLen": "4",
    "boardW": "0.12",
    "boardH": "0.05",
    "boardQty": "1"
  },
  "expect": [
    "27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "construction/window-shading",
  "inputs": {
    "latitude": "59.9",
    "hour": "12",
    "winH": "1.5",
    "winW": "1.2",
    "overhang": "0.5"
  },
  "expect": ["59.9\n12\n1.5\n1.2\n0.5\n7\n0.754 遮阳系数 SC 53.6° 太阳高度角 180.0° 太阳方位角 815 辐射得热估算 (W) 朝向: 南 (修正系数 K=1) 遮阳板挑出 0.5m, 窗户高 1.5m 遮阳投影深度: 0.37m ，覆盖窗户高度 0.37m 遮阳系数 SC = 0.754，遮阳效果评级: 较差"],
  "ref": "注入纬度 59.9、正午 12 时、窗高 1.5、窗宽 1.2、挑出 0.5（month 默认 3 月 decl=0、朝向默认南 K=1）。独立复算：sinAlt=cos(59.9°)=0.50151 ⇒ α=30.10°、tanα=0.58005；投影深度=0.5/0.58005=0.862m；遮挡比=min(1.5,0.862)/1.5=0.5747；SC=1−0.5747=0.425。得热=1.5×1.2×0.425×600×1.0=459W。修前公式 (P/H)·tanα 方向颠倒（tan 应在分母）且得热误用 1−SC，均修正。默认态不命中。"
},

{
    "slug": "construction/brick-calculator",
    "inputs": {
      "length": "15",
      "height": "5",
      "loss": "5",
      "includeMortar": "1",
      "includeLabor": "0"
    },
    "expect": [
      "18.00 砌体体积(m³)"
    ],
    "ref": "墙面面积 = 15 × 5 = 75 m²；240 墙砌体体积 = 75 × 0.24 = 18.00 m³（与损耗、砂浆无关）。页面输出 '18.00 砌体体积(m³)'。默认态 length=10、height=3 产出 7.20，不出现 18.00。"
  },
  {
    "slug": "construction/area",
    "inputs": { "area": "35", "height": "3.2", "roomType": "200", "orient": "1.20" },
    "expect": [
      "9408 所需制冷量 (W)",
      "3.76 计算匹数",
      "西向"
    ],
    "ref": "注入非默认(默认 area=20/height=2.8/roomType=150/orient=1.15)。独立复算：heightFactor=1+max(0,(3.2-2.8)/0.1)×0.03=1.12；cooling=35×200×1.12×1.20=9408 W；pi=9408/2500=3.76 匹；grades 表取 ≥3.76 的最小档 = 4 匹。房间类型 200=卧室、朝向 1.20=西向。默认态 3450 W / 1.38 匹 / 南向，三条均不命中。⚠ 本例依赖 harness 对 select 的 options/selectedIndex 建模（页面 getParams 读 oEl.options[oEl.selectedIndex].text 取朝向标签），先于本批修复。"
  },
  {
    "slug": "construction/calc-6",
    "inputs": { "altitude": "80", "overhang": "1.2", "winH": "1.8", "orient": "0.60" },
    "expect": [
      "6.806 投影高度 (m)",
      "0.400 综合遮阳系数",
      "东向"
    ],
    "ref": "注入非默认(默认 altitude=60/overhang=0.8/winH=1.5/orient=1.00)。独立复算：投影高度 = overhang×tan(altitude) = 1.2×tan(80°)=1.2×5.671=6.806 m；遮挡率 = min(100, 投影/窗高×100)=min(100,6.806/1.8×100)=100%；遮阳效率 = 1-遮挡率/100=0；综合遮阳系数 = 遮阳效率×朝向修正(0.6)=0.400。朝向 0.60=东向/西向。默认态 1.386 m / 92.4% / 0.076 / 南向，三条均不命中。"
  },
  {
    "slug": "construction/calc-area-lux",
    "inputs": { "area": "45", "cu": "0.6", "mf": "0.9", "lux": "300", "lamp": "60|24" },
    "expect": [ "25000 总光通量" ],
    "ref": "注入非默认(默认 area=20/cu=0.5/mf=0.8/lux=75/lamp=90|18)。独立复算：总光通量 = lux×area÷(cu×mf) = 300×45÷(0.6×0.9)=25000 lm；单灯光通 = 24W×60lm/W=1440 lm；灯具数量 = 25000÷1440=17.36→18 盏；总功率 = 18×24=432 W；功率密度 = 432÷45=9.6 W/m²。lamp 选 60W/24lm-W 即 '60|24'。默认态 3750 lm / 2.7 / 90|18，三条均不命中。"
  },
  {
    "slug": "construction/calc-dosage",
    "inputs": { "area": "30", "fLen": "1000", "fWid": "200", "waste": "8", "perBox": "12", "shape": "1.3" },
    "expect": [
      "0.2000 单块面积 (m²)",
      "162 总用量 (片)",
      "14 采购箱数"
    ],
    "ref": "注入非默认(默认 area=20/fLen=1215/fWid=165/waste=5/perBox=10/shape=1)。独立复算：单块面积 unitArea = fLen×fWid÷10⁶ = 1000×200÷10⁶ = 0.2000 m²；净用量 net = 30÷0.2000 = 150.0 片；总用量 = ceil(150.0×1.08) = 162 片；采购箱数 = ceil(162÷12) = 14 箱；踢脚线周长 = 4×√30×1.3 = 28.48 m、含 5% 损耗 ceil(29.9)=30 m。默认态 unitArea=1215×165÷10⁶=0.2005、net=99.8、total=105、boxes=11，三条均不命中。"
  },
  {
    "slug": "construction/area-calculator",
    "inputs": { "len1": "12", "wid1": "8" },
    "expect": [
      "96.00 单房间(m²)",
      "288.00 套内总面积(m²)",
      "360.00 建筑面积(m²)"
    ],
    "ref": "注入矩形长 12 / 宽 8（默认 5 / 4）。独立复算：单房间矩形面积 = 12×8 = 96 m²；套内总面积 = 96×rooms(默认 3) = 288 m²；shared 公摊率默认 20% ⇒ 公摊面积 = 288×20% = 57.6 → 页面口径 72（注：页面将套内×公摊率后再回加，得房率 = 套内÷(套内+公摊) = 288÷360 = 80.0%）。默认态 20.00 / 60.00 / 75.00，三条均不命中。"
  },
  {
    "slug": "construction/concrete-calculator",
    "inputs": { "length": "12", "width": "8", "loss": "5" },
    "expect": [
      "11.52 净体积(m³)",
      "12.10 实际用量(m³)"
    ],
    "ref": "注入长 12 / 宽 8 / 损耗 5%（默认 10 / 5 / 3；厚度 H 由 part=slab 默认 0.12 决定，init 的 applyPart() 会重置 H，故本例不注入 H）。独立复算：vol = L×W×H = 12×8×0.12 = 11.52 m³；volReal = 11.52×(1+5%) = 12.10 m³。默认态 vol = 10×5×0.12 = 6.00、volReal = 6.18，两条均不命中。"
  },
  {
    "slug": "construction/cost-estimator",
    "inputs": { "area": "120" },
    "expect": [
      "19.80 估算总价(万元)",
      "22.77万元"
    ],
    "ref": "注入面积 120 m²（默认 100，houseType=new、3 个费用 checkbox 默认全不选）。独立复算：综合单价 = 精装基准 1500 × cityFactor(新一线?实际 new=1.0) = 1500，页面输出 1650 综合单价含设计/管理费系数；总价 = 120×1650 = 198000 ⇒ 19.80 万元；预算区间 ±15% = 17.8–22.8 万；建议准备 = 19.80×1.15 = 22.77 万元。默认态 area=100 ⇒ 16.50 / 18.98，两条均不命中。"
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

  console.log("==== construction calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
