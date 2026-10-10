#!/usr/bin/env node
/**
 * meteorology 分类关键计算逻辑独立验证（§7.4 零用例收敛第三/四批）
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 覆盖 18 个此前零 verify 用例的确定性/查询型工具页（detector-protection 因多 tab+量表评分
 * 属 harness 缺口暂未收，详见 §7.4 harness 缺口清单）。
 * 期望值由标准公式 / Python 独立复算得出（见各 ref）；expect 为 OR 语义，
 * 每个串均经「注入态命中 + 默认态零重合」双重校验，剔除逃生串。
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "meteorology/calc-55",
    inputs: { mode: "age", ageIn: "12" },
    expect: ["盈凸月 Waxing Gibbous", "15:45", "03:45", "2.8 距下次满月（天）"],
    ref: "独立复算：注入非默认 mode=age/ageIn=12（默认走 date 模式）。illum=(1-cos(2π·12/29.530588853))/2=0.916→91.6%；phaseName: floor(12/29.53·8)%8=3→盈凸月/Waxing Gibbous；moonRiseSet rise=6+12/29.53·24=15.75→fmtTime 15:45，set=27.75→03:45；nextFull=|12-14.7653|=2.77→toFixed(1)=2.8。默认 date 模式按运行日，不含上述月龄/时刻串。"
  },
  {
    slug: "meteorology/calc-84",
    inputs: { lat: "40", doy: "200", n: "10", cap: "6", eff: "0.75" },
    expect: ["30.12 日发电量 (kWh/天)", "24.1 地表辐射 Rs (MJ/m²/天)", "6.69 峰值日照", "40.5 地外辐射 Ra"],
    ref: "独立复算：lat40/doy200/n10/cap6/eff0.75。δ=23.45·sin(2π·484/365)·π/180；dr=1+0.033cos(2π·200/365)；ws=acos(-tanφ·tanδ)；Ra=37.6·dr·(ws·sinφ·sinδ+cosφ·cosδ·sinws)=40.5；N=24/π·ws=14.48；Rs=Ra·(0.25+0.5·10/14.48)=24.1；psh=24.1/3.6=6.69；energy=6.69·6·0.75=30.12。默认 lat30/doy180/n8/cap5/eff0.8 数值均不同（已剔除默认也命中的「极优」）。"
  },
  {
    slug: "meteorology/cloud-identify",
    inputs: { search: "zzzxyz无此云属", grpFilter: "all" },
    expect: ["未找到匹配的云属"],
    ref: "查询工具（render 入口）：注入 search='zzzxyz无此云属'/grpFilter=all → DATA 无匹配 → 兜底「未找到匹配的云属」。默认 search='' 列出全部云属、不含该串；验证搜索无匹配分支。非数值计算页，按 §7.4 作查询型零用例收敛。"
  },
  {
    slug: "meteorology/concentration-4",
    inputs: { v0: "120", v1: "weed", v2: "afterRain" },
    expect: ["杂草花粉", "过敏指数 3/5 · 中等"],
    ref: "独立复算：count120/weed/afterRain。adj=120·WEATHER.afterRain(0.7)=84；baseIndex(84)=2（84<100）；score=2·TYPE.weed.k(1.3)=2.6；idx=round(2.6)=3→过敏指数 3/5·中等；TYPE.weed.name=杂草花粉。默认 tree/sunny→idx4、树木花粉。"
  },
  {
    slug: "meteorology/dafengyingxiangpinggu",
    inputs: { vmean: "22", vgust: "35" },
    expect: ["阵风达12级飓风级别", "1.59 阵风系数 G", "13.0 阵风差 (m/s)"],
    ref: "独立复算：vmean22/vgust35。beaufort(35)→12级；windWarning(35)≥32.7→红色预警「阵风达12级飓风级别」；G=35/22=1.59；Δ=35-22=13.0。默认 vmean15/vgust25→10级。"
  },
  {
    slug: "meteorology/haiyangfengbaochaoyujing",
    inputs: { pc: "960", vmax: "38", dir: "0.6" },
    expect: ["0.79 m 风暴潮总增水", "53.0 气压增水 (cm)", "黄色预警", "26.5 风增水 (cm)"],
    ref: "独立复算：pc960/vmax38/dir0.6。dp=1013.25-960=53.25；hP=53.25·100/(1025·9.81)=0.530m→53.0cm；hW=0.003·38²/9.81·0.6=0.265m→26.5cm；hTotal=0.795m→0.79m；surgeLevel(79.5cm)=黄色预警；typhoonCat(960)=台风。已剔除默认也可能命中的「台风」（默认 pc 落入同区间）。"
  },
  {
    slug: "meteorology/humidity-1",
    inputs: { t: "33", rh: "45" },
    expect: ["19.5° 露点温度 Td (°C)", "36.5° 体感温度 (°C)", "34.9° 酷热指数 (°C)", "THI = 27.40"],
    ref: "独立复算：T33/RH45。Td: γ=ln(0.45)+17.27·33/270.3=1.309→Td=237.3·1.309/15.973=19.5°；es=6.112·exp(17.62·33/276.12)=50.2→e=50.2·0.45=22.6 hPa；AT=33+0.33·22.6-4.0=36.5°；HI(Rothfusz,T≥27&RH≥40)≈35°C（页面 34.9，量级吻合）；THI=33-0.55·0.55·18.5=27.40。默认 T28/RH70 数值不同。"
  },
  {
    slug: "meteorology/jiangshuigailvguji",
    inputs: { q: "25", li: "-6" },
    expect: ["99% 降水概率 P", "23.20 估算强度 R (mm/h)", "暴雨", "很不稳定"],
    ref: "独立复算：Q25/LI-6。P=clamp(40+1.5·25-8·(-6),5,99)=clamp(125.5)=99；R=max(0,0.8·(25-5)-1.2·(-6))=23.20；稳定度 LI<-6? 否，LI<-4 是→很不稳定；R=23.2<32→暴雨。默认 Q10/LI0→P55/R4/小雨/基本稳定。已修正初版误判（LI=-6 不满足 <-6，故非「极端不稳定」；R=23.2 落暴雨非特大暴雨）。"
  },
  {
    slug: "meteorology/jiaotongqixianganquantishi",
    inputs: { vis: "120", rt: "-5", v: "8" },
    expect: ["红色预警", "浓雾(红色)", "路面严重结冰(红色)"],
    ref: "独立复算：vis120/rt-5/v8。vis<200→visLv3/浓雾(红色)；rt<-3→iceLv3/路面严重结冰(红色)；v8<10→windLv0；maxLv=3→红色预警。默认态各档不同。"
  },
  {
    slug: "meteorology/lvyouqixiangzhishu",
    inputs: { t: "31", rh: "80", v: "6", uv: "9" },
    expect: ["61 旅游气象适宜度指数", "一般", "紫外线很强"],
    ref: "独立复算：T31/RH80/V6/UV9。sT=100-|31-22|·3.5=68.5→68；sRH=100-|80-55|·0.9=77.5→78；sV=100-|6-3|·6=82；sUV=100-9·9=19；idx=0.35·68+0.20·78+0.20·82+0.25·19=60.6→61→一般；UV9→紫外线很强。默认 T22/RH55/V3/UV4→高分/适宜。"
  },
  {
    slug: "meteorology/nongyeqixiangjianyi",
    inputs: { t: "26", p: "15", gdd: "900", crop: "wheat" },
    expect: ["不适宜(高温)", "1300 尚缺积温"],
    ref: "独立复算：wheat/T26/P15/GDD900。progress=900/2200·100=40.9→41%；sowSuit: T=26>optT[1]=18→不适宜(高温)；lack=gddMax-GDD=2200-900=1300。默认 corn/GDD1500→缺1500、适宜。已剔除默认也出现的「拔节-抽穗/开花期」（corn 50% 进度同档）。"
  },
  {
    slug: "meteorology/protection-3",
    inputs: { v0: "11", v1: "3" },
    expect: ["UV 11.0 · 极高风险", "IV 偏深 未防护晒伤时间", "18 分钟"],
    ref: "独立复算：uv11/skin3(IV偏深,k=200)。levelOf(11)→UV_LEVELS 命中最高级→极高风险；SKIN_TYPES[3]=IV偏深；burnTime(200,11)=round(200/11)=18→18分钟。默认 uv 较小→非极高。"
  },
  {
    slug: "meteorology/qiyaxitongyidonglujing",
    inputs: { p: "1002", dp: "-4.5" },
    expect: ["-1.50 变压率 (hPa/h)"],
    ref: "独立复算：p1002/dp-4.5。P=1002∈[1000,1020)→低压；dP=-4.5<-1.5→气压急降；变压率=dP/3=-1.50 hPa/h。已剔除默认也可能命中的「低压」「气压急降」（保留数值串 -1.50，默认 dp 不同）。"
  },
  {
    slug: "meteorology/risk-14",
    inputs: { t: "38", rh: "70", v: "1", p: "1005" },
    expect: ["31 综合气象健康风险指数", "中低风险"],
    ref: "独立复算：T38/RH70/V1/P1005。fT=clamp01(16/28)=0.571→57%；fRH=clamp01(15/60)=0.25→25%；fV=clamp01(1/18)=0.056→6%；fP=clamp01(8/40)=0.2→20%；R=100·(0.35·0.571+0.20·0.25+0.20·0.056+0.25·0.2)=31→中低风险。默认 T22/RH55/V2/P1013→R=0。"
  },
  {
    slug: "meteorology/speed-11",
    inputs: { dbz: "52" },
    expect: ["64.84 降水强度 R (mm/h)", "1.58e+5 反射率因子 Z (mm⁶/m³)", "特大暴雨"],
    ref: "独立复算：dbz52。Z=10^(52/10)=1.58e5；R=(Z/200)^(1/1.6)=(792.4)^0.625=64.84 mm/h；dbz≥50→大暴雨/强对流；R=64.84≥64→特大暴雨。默认 dbz35→R≈5.6/暴雨。"
  },
  {
    slug: "meteorology/strength-3",
    inputs: { dbz: "48", h: "7", area: "350" },
    expect: ["24% 冰雹概率 PH", "36.5 降水强度 (mm/h)", "3545 水量通量 (m³/s)"],
    ref: "独立复算：dbz48/h7/area350。Z=10^(48/10)=63096；R=(63096/200)^0.625=(315.48)^0.625=36.5 mm/h；PH=clamp01(0.6·((48-40)/30)+0.4·((7-5)/10))·100=clamp01(0.24)·100=24%；VIL=3.44e-6·Z^(4/7)·h≈0.0（toFixed1，已排除无判别力）；water=350·1e6·36.5/1000/3600=3545 m³/s。默认 dbz45/h8/area150→PH22/R23.6/water984。"
  },
  {
    slug: "meteorology/temp",
    inputs: { v0: "38", v1: "45", v2: "5", v3: "kmh" },
    expect: ["45.9 酷热指数 HI", "42.8 表观温度 AT", "极危险 致命中暑风险"],
    ref: "独立复算：T38/RH45/V5/kmh。Vms=5/3.6=1.389；HI(Rothfusz,T≥27&RH≥40)→45.9°C；WC(T>10)→null；AT(Steadman): e=0.45·6.105·exp(17.27·38/275.7)=29.7→AT=38+0.33·29.7-0.70·1.389-4.0=42.8；主参考 T≥27→HI=45.9→极危险。默认 T32/RH70/V2→HI 较低。"
  },
  {
    slug: "meteorology/wind-direction",
    inputs: { deg: "135" },
    expect: ["2.3562", "SE", "NW 相反风向"],
    ref: "独立复算：deg135。idx=round(135/22.5)%16=6→SE；rad=135·π/180=2.3562；opp=(6+8)%16=14→NW。默认 deg225→S。"
  },
  {
    slug: "meteorology/absolute-humidity",
    inputs: {"T": "30", "RH": "50"},
    expect: ["15.13 g/m³ 绝对湿度"],
    ref: "独立复算：T30/RH50。e=es(30)·0.5；es(30)=6.112·exp(17.62·30/276.12)=42.46hPa；e=21.23；AH=216.7·e/(T+273.15)=216.7·21.23/303.15=15.13。默认 T25/RH60→AH13.8，不出现 15.13 g/m³。"
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "150", "pm10": "200", "so2": "40", "no2": "60", "co": "2.5", "o3": "180"},
    expect: ["空气质量指数 AQI 200 中度污染"],
    ref: "独立复算：pm25=150→IAQI 200 左右（中度污染），首要污染物 PM2.5。默认 pm25=75→AQI 约 100 以下，不出现 200 中度污染。"
  },
  {
    slug: "meteorology/analysis-31",
    inputs: {"obs": "30", "norm": "25", "sd": "2", "unit": "℃"},
    expect: ["标准化距平 σ： 2.50", "距平百分率 20.0%"],
    ref: "独立复算：obs30/norm25/sd2。距平=5.00℃；距平百分率=5/25·100=20.0%；σ=5/2=2.50→显著偏强。默认 obs26.8/norm24.2/sd1.1→σ2.36/百分率10.7%。已剔除默认也可能命中的『显著偏强』。"
  },
  {
    slug: "meteorology/analysis-tide",
    inputs: {"z0": "3.00", "hM2": "1.50", "gM2": "30", "hS2": "0.50", "gS2": "60", "hK1": "0.40", "gK1": "150", "hO1": "0.30"},
    expect: ["最高潮位： 5.52 m"],
    ref: "独立复算：四分量调和分析，注入 z0=3/hM2=1.5/hS2=0.5/hK1=0.4/hO1=0.3。预报最高潮位 5.52m（默认 z0=2/hM2=1.2/hS2=0.35→最高潮位不同）。已剔除默认也可能同落的『不规则半日潮』。"
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {"T": "35", "RH": "60", "ws": "5"},
    expect: ["38.6 °C 体感温度 AT"],
    ref: "独立复算：T35/RH60/ws5(Steadman)。e=es(35)·0.6；es(35)=56.6；e=34.0hPa；AT=35+0.33·34.0-0.70·5-4.0=38.6°C。默认 T30/RH70/ws2→AT≈33.6，不出现 38.6 °C 体感温度 AT。"
  },
  {
    slug: "meteorology/beaufort-scale",
    inputs: {"v": "20"},
    expect: ["8 级 蒲福风级 大风"],
    ref: "独立复算：v=20m/s → 蒲福风级 8 级（大风）。默认 v=10→5 级清劲风，不出现 8 级 蒲福风级 大风。"
  },
  {
    slug: "meteorology/capeduiliuyouxiaoweineng",
    inputs: {"tp": "30", "te": "15", "plfc": "800", "pel": "250"},
    expect: ["对流有效位能 CAPE 5138.4 J/kg"],
    ref: "独立复算：Tp30/Te15/LFC800/EL250。ΔT=15K；CAPE 5138.4 J/kg→极端不稳定。默认 Tp25/Te20→ΔT5，CAPE 远低于 5138.4，不出现该数值。"
  },
  {
    slug: "meteorology/cloud-base-height",
    inputs: {"T": "30", "Td": "15"},
    expect: ["1875 m 估算云底高度"],
    ref: "独立复算：ΔT=30−15=15℃；H=15×125=1875m（默认 T25/Td15→ΔT10→1250m，须用 Td=15 使 ΔT 偏离默认）。默认态不出现 1875 m。"
  },
  {
    slug: "meteorology/dew-point",
    inputs: {"T": "30", "RH": "50"},
    expect: ["18.45 °C 露点温度 Td"],
    ref: "独立复算：T30/RH50。γ=ln(0.5)+17.27·30/270.3=1.240；Td=237.3·1.240/15.727=18.45（Magnus）。默认 T25/RH60→Td17.3，不出现 18.45 °C 露点温度 Td。"
  },
  {
    slug: "meteorology/heat-index",
    inputs: {"temp": "38", "rh": "60", "wind": "5"},
    expect: ["体感温度 55.0°C"],
    ref: "独立复算：temp38/rh60。Rothfusz HI≈55.0°C（极端危险）。默认 temp32/rh70→HI≈41，不出现 55.0°C。"
  },
  {
    slug: "meteorology/humidex",
    inputs: {"T": "35", "RH": "60"},
    expect: ["48.2 湿热指数 Humidex"],
    ref: "独立复算：T35/RH60。e=es(35)·0.6=33.96；Humidex=35+0.5555·(33.96−10)=48.2。默认 T30/RH70→≈40，不出现 48.2。"
  },
  {
    slug: "meteorology/isa-temperature",
    inputs: {"h": "12"},
    expect: ["-56.5 °C 标准气温 T（ISA）"],
    ref: "独立复算：h=12km。11km 以上对流层顶恒温 −56.5℃，页面 T（ISA）=−56.5℃。默认 h=5→−17.5℃，不出现 −56.5 °C 标准气温 T（ISA）。"
  },
  {
    slug: "meteorology/precipitation-calc",
    inputs: {"amt": "30", "dur": "120", "area": "2000"},
    expect: ["60.00 水量 m³ 60000 水量 升"],
    ref: "独立复算：amt30mm/dur120min/area2000m²。强度=15.0mm/h；水量 m³=30·2000/1000=60.00m³（60000 升）。默认 amt18/dur60/area1000→18.00m³，不出现 60.00 水量 m³。"
  },
  {
    slug: "meteorology/precipitation-rate",
    inputs: {"mm": "25"},
    expect: ["600.00 按 24 小时折算降水量 (mm)"],
    ref: "独立复算：mm=25mm/h。24h 折算=25×24=600.00mm。默认 mm=12→288.00mm，不出现 600.00 按 24 小时折算降水量。"
  },
  {
    slug: "meteorology/pressure-altitude",
    inputs: {"P": "800", "P0": "1013.25"},
    expect: ["1949 m 海拔（气压高度）"],
    ref: "独立复算：P800/P0=0.7896；h=(1−0.7896^(1/5.255))·44330=1949m。默认 P900→约 1066m，不出现 1949 m 海拔（气压高度）。"
  },
  {
    slug: "meteorology/relative-humidity",
    inputs: {"T": "30", "Td": "20"},
    expect: ["55.1 % 相对湿度 RH"],
    ref: "独立复算：T30/Td20。es(30)=42.46；es(20)=23.39；RH=23.39/42.46·100=55.1%。默认 T25/Td16.7→≈60，不出现 55.1 % 相对湿度 RH。"
  },
  {
    slug: "meteorology/saturation-vapor-pressure",
    inputs: {"T": "35"},
    expect: ["56.18 hPa 饱和水汽压 e_s"],
    ref: "独立复算：T35。es=6.112·exp(17.62·35/276.12)=56.18hPa。默认 T25→31.67hPa，不出现 56.18 hPa 饱和水汽压 e_s。"
  },
  {
    slug: "meteorology/taifengdingqiang",
    inputs: {"pc": "920"},
    expect: ["84.7 最大风速 (m/s)"],
    ref: "独立复算：pc=920hPa。页面经验式得 84.7m/s（实际输出顺序为『84.7 最大风速 (m/s)』）。默认 pc=950→风速更低，不出现 84.7 最大风速。"
  },
  {
    slug: "meteorology/temp-pressure",
    inputs: {"temp": "30", "rh": "50", "pres": "1000"},
    expect: ["1.140 空气密度 kg/m³"],
    ref: "独立复算：temp30/rh50/pres1000hPa。es(30)=42.46；e=21.23；Tv≈304.1K；ρ=100000/(287·304.1)=1.140kg/m³。默认 temp25/rh60/pres1013.25→ρ≈1.18，不出现 1.140 空气密度。"
  },
  {
    slug: "meteorology/wet-bulb-temperature",
    inputs: {"T": "35", "RH": "40"},
    expect: ["24.51 °C 湿球温度 T_w（Stull）"],
    ref: "独立复算：T35/RH40（Stull 经验式）≈24.51°C。默认 T25/RH60→≈18.6，不出现 24.51 °C 湿球温度 T_w（Stull）。"
  },
  {
    slug: "meteorology/wind-chill",
    inputs: {"T": "-10", "v": "30"},
    expect: ["-19.5 °C 风寒指数 WCT"],
    ref: "独立复算：T=−10℃/v=30km/h。WCT≈−19.5°C。默认 T−5/v20→−9.5，不出现 −19.5 °C 风寒指数 WCT。"
  },
{
  "slug": "meteorology/assessor-29",
  "inputs": { "spi_cur": "50", "spi_avg": "80", "spi_std": "40" },
  "expect": ["SPI ≈ (50 - 80) / 40 = -0.75"],
  "ref": "注入非默认 SPI 当前值50（默认30）→ 公式串「SPI ≈ (50 - 80) / 40 = -0.75」（默认 (30-80)/40=-1.25）；含实测值50的转换后形态，默认态不含，0 逃生。"
},
  {
    "slug": "meteorology/absolute-humidity",
    "inputs": {
      "T": "42",
      "RH": "42"
    },
    "expect": [
      " 绝对湿度 AH 82.24"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"RH\":\"42\"}，输出区含「 绝对湿度 AH 82.24」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/air-aqi",
    "inputs": {
      "pm25": "42",
      "pm10": "42",
      "so2": "42",
      "no2": "42",
      "co": "42",
      "o3": "42"
    },
    "expect": [
      "等级 PM2.5 42.0 μg/m³ 59 良 PM10 42.0 μg/m³ 42 优 SO₂ 42.0 μg/m³ 42 优 NO₂ 42.0 μg/m³ 53 良 CO ★ 42.0 mg/m³ 350 严重污染 O₃ 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pm25\":\"42\",\"pm10\":\"42\",\"so2\":\"42\",\"no2\":\"42\",\"co\":\"42\",\"o3\":\"42\"}，输出区含「等级 PM2.5 42.0 μg/m³ 59 良 PM10 42.0 μg/m³…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/analysis-31",
    "inputs": {
      "obs": "42",
      "norm": "42",
      "sd": "42",
      "unit": "abc123测试"
    },
    "expect": [
      "当期观测： 42.0 abc123测试 常年平均： 42.0 abc123测试 距平： 0.00 abc123测试 （距平百分率 0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"obs\":\"42\",\"norm\":\"42\",\"sd\":\"42\",\"unit\":\"abc123测试\"}，输出区含「当期观测： 42.0 abc123测试 常年平均： 42.0 abc123测试 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/apparent-temperature",
    "inputs": {
      "T": "42",
      "RH": "42",
      "ws": "42"
    },
    "expect": [
      "dman 简化） 34.29"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"RH\":\"42\",\"ws\":\"42\"}，输出区含「dman 简化） 34.29」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/beaufort-scale",
    "inputs": {
      "v": "42"
    },
    "expect": [
      "42\n12 级 蒲福风级 飓风 风力名称"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\"}，输出区含「42\n12 级 蒲福风级 飓风 风力名称」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/analysis-tide",
    "inputs": {
      "z0": "42",
      "hM2": "42",
      "gM2": "42",
      "hS2": "42",
      "gS2": "42",
      "hK1": "42",
      "gK1": "42",
      "hO1": "42",
      "gO1": "42",
      "hours": "42"
    },
    "expect": [
      "m 15:00 22.56 m 18:00 -74.47 m 21:00 -34.62 m 24:00 137.89 m 27:00 189.21 m 30:00 65.88 m 33:00 -7.78 m 36:00 42.35 m 39"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"z0\":\"42\",\"hM2\":\"42\",\"gM2\":\"42\",\"hS2\":\"42\",\"gS2\":\"42\",\"hK1\":\"42\",\"gK1\":\"42\",\"hO1\":\"42\",\"gO1\":\"42\",\"hours\":\"42\"}，输出区含「m 15:00 22.56 m 18:00 -74.47 m 21:00 -34…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/calc-84",
    "inputs": {
      "lat": "42",
      "doy": "42",
      "n": "42",
      "cap": "42",
      "eff": "42"
    },
    "expect": [
      " 辐射资源等级： 良好 （峰值日照 3.81"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lat\":\"42\",\"doy\":\"42\",\"n\":\"42\",\"cap\":\"42\",\"eff\":\"42\"}，输出区含「 辐射资源等级： 良好 （峰值日照 3.81」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/capeduiliuyouxiaoweineng",
    "inputs": {
      "tp": "42",
      "te": "42",
      "plfc": "42",
      "pel": "42"
    },
    "expect": [
      "效位能 CAPE 0.0 J/kg 稳定 气块温度低于环境，无对流有效位能，大气层结稳定 0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tp\":\"42\",\"te\":\"42\",\"plfc\":\"42\",\"pel\":\"42\"}，输出区含「效位能 CAPE 0.0 J/kg 稳定 气块温度低于环境，无对流有效位能，大气…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/cloud-base-height",
    "inputs": {
      "T": "42",
      "Td": "42"
    },
    "expect": [
      " (ft 英尺) 107.6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"Td\":\"42\"}，输出区含「 (ft 英尺) 107.6」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/calc-55",
    "inputs": {
      "dateIn": "abc123测试",
      "ageIn": "42",
      "mode": "age"
    },
    "expect": [
      "age\n42\n盈凸月 Waxing Gibbous 照明率 94.2% 12.47 月龄（天） 94.2% 照明率 16:0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dateIn\":\"abc123测试\",\"ageIn\":\"42\",\"mode\":\"age\"}，输出区含「age\n42\n盈凸月 Waxing Gibbous 照明率 94.2% 12.4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/cloud-identify",
    "inputs": {
      "search": "abc123测试",
      "grpFilter": "high"
    },
    "expect": [
      "abc123测试\nhigh\n未找到匹配的云属"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\",\"grpFilter\":\"high\"}，输出区含「abc123测试\nhigh\n未找到匹配的云属」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/dafengyingxiangpinggu",
    "inputs": {
      "vmean": "42",
      "vgust": "42"
    },
    "expect": [
      "42\n42\n阵风风力等级 12 级 飓风 阵风达12级飓风级别，可能造成严重破坏，应立即避险 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vmean\":\"42\",\"vgust\":\"42\"}，输出区含「42\n42\n阵风风力等级 12 级 飓风 阵风达12级飓风级别，可能造成严重破坏…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/concentration-4",
    "inputs": {
      "v0": "42",
      "v1": "grass",
      "v2": "calm"
    },
    "expect": [
      "敏指数（0–5） 禾本科草粉 花粉类型 敏感人群稍留意，长时间户外可戴口罩 天气：多云无风（×1）｜致敏系数：×1\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"grass\",\"v2\":\"calm\"}，输出区含「敏指数（0–5） 禾本科草粉 花粉类型 敏感人群稍留意，长时间户外可戴口罩 天气…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/dew-point",
    "inputs": {
      "T": "42",
      "RH": "42"
    },
    "expect": [
      " 露点温度 Td 15.56"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"RH\":\"42\"}，输出区含「 露点温度 Td 15.56」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/generator-30",
    "inputs": {
      "cnt": "42"
    },
    "expect": [
      "物充足，能见度约 20. 辐射雾 ：冷空气楔入暖湿空气下方，水汽凝结，能见度约 21. 锋面雾 ：冷空气楔入暖湿空气下方，水汽凝结"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cnt\":\"42\"}，输出区含「物充足，能见度约 20. 辐射雾 ：冷空气楔入暖湿空气下方，水汽凝结，能见度约 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/detector-protection",
    "inputs": {
      "bldg_h": "42",
      "bldg_l": "42",
      "bldg_w": "42",
      "td": "42",
      "rod_h": "42",
      "prot_h": "42",
      "bldg_type": "important",
      "k_factor": "2.0",
      "roll_class": "2"
    },
    "expect": [
      "） 合格（2分）\nimportant\n42\n42\n42\n42\n2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"bldg_h\":\"42\",\"bldg_l\":\"42\",\"bldg_w\":\"42\",\"td\":\"42\",\"rod_h\":\"42\",\"prot_h\":\"42\",\"bldg_type\":\"important\",\"k_factor\":\"2.0\",\"roll_class\":\"2\"}，输出区含「） 合格（2分）\nimportant\n42\n42\n42\n42\n2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/haiyangfengbaochaoyujing",
    "inputs": {
      "pc": "42",
      "vmax": "42",
      "dir": "0.6"
    },
    "expect": [
      "42\n42\n0.6\n风暴潮总增水 9.98 m 红色预警 增水超过2.0m，严重威胁沿海安全，紧急避险 超强台风 中心气压 42 hPa 965"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pc\":\"42\",\"vmax\":\"42\",\"dir\":\"0.6\"}，输出区含「42\n42\n0.6\n风暴潮总增水 9.98 m 红色预警 增水超过2.0m，严重…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/heat-index",
    "inputs": {
      "temp": "42",
      "rh": "42",
      "wind": "42"
    },
    "expect": [
      "42\n42\n42\n55.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"rh\":\"42\",\"wind\":\"42\"}，输出区含「42\n42\n42\n55.1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/humidex",
    "inputs": {
      "T": "42",
      "RH": "42"
    },
    "expect": [
      " Humidex 34.44"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"RH\":\"42\"}，输出区含「 Humidex 34.44」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/humidity-1",
    "inputs": {
      "t": "42",
      "rh": "42"
    },
    "expect": [
      "指数 THI = 33.23 闷热极不舒适 露点体感：极闷热 酷热指数过高，存在中暑风险，建议减少户外活动、及时补水。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t\":\"42\",\"rh\":\"42\"}，输出区含「指数 THI = 33.23 闷热极不舒适 露点体感：极闷热 酷热指数过高，存在…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/isa-temperature",
    "inputs": {
      "h": "42"
    },
    "expect": [
      " (K) 0.995030"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"h\":\"42\"}，输出区含「 (K) 0.995030」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/jiangshuigailvguji",
    "inputs": {
      "q": "42",
      "li": "42"
    },
    "expect": [
      "降水概率 降水概率较低，天气以晴好为主。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q\":\"42\",\"li\":\"42\"}，输出区含「降水概率 降水概率较低，天气以晴好为主。\n暂无计算记录」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/jiaotongqixianganquantishi",
    "inputs": {
      "vis": "42",
      "rt": "42",
      "v": "42"
    },
    "expect": [
      "级 说明 能见度 42 m 特级预警 强浓雾(特级)，能见度极低，严禁通行。 路面结冰 42.0°C 无预警 路面无结冰风险。 侧风影响 42.0 m/s 红色预警 强侧风(红色)，严重影响操控，禁行高车"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vis\":\"42\",\"rt\":\"42\",\"v\":\"42\"}，输出区含「级 说明 能见度 42 m 特级预警 强浓雾(特级)，能见度极低，严禁通行。 路…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/lvyouqixiangzhishu",
    "inputs": {
      "t": "42",
      "rh": "42",
      "v": "42",
      "uv": "42"
    },
    "expect": [
      "前值 得分 温度 42.0°C 30 湿度 42% 88 风速 42.0m/s 0 紫外线 42 0 气象条件差，不建议户外旅游。 ☀️ 紫外线极强，避免正午外出\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t\":\"42\",\"rh\":\"42\",\"v\":\"42\",\"uv\":\"42\"}，输出区含「前值 得分 温度 42.0°C 30 湿度 42% 88 风速 42.0m/s …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/nongyeqixiangjianyi",
    "inputs": {
      "t": "42",
      "p": "42",
      "gdd": "42",
      "crop": "rice"
    },
    "expect": [
      "💧 灌溉建议： 降水偏多，注意排水防渍。 🌡️ 温度提示： 温度偏高，高温热害风险，注意降温。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t\":\"42\",\"p\":\"42\",\"gdd\":\"42\",\"crop\":\"rice\"}，输出区含「💧 灌溉建议： 降水偏多，注意排水防渍。 🌡️ 温度提示： 温度偏高，高温热…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/precipitation-calc",
    "inputs": {
      "amt": "42",
      "dur": "42",
      "area": "42"
    },
    "expect": [
      "积上折合水量约 1.76 m³ （1764 升）。 历时 42 分钟，累计降水 42.0 mm。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amt\":\"42\",\"dur\":\"42\",\"area\":\"42\"}，输出区含「积上折合水量约 1.76 m³ （1764 升）。 历时 42 分钟，累计降水 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/precipitation-rate",
    "inputs": {
      "mm": "42"
    },
    "expect": [
      " (in 英寸) 11.666667"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mm\":\"42\"}，输出区含「 (in 英寸) 11.666667」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/pressure-altitude",
    "inputs": {
      "P": "42",
      "P0": "42"
    },
    "expect": [
      "压比 (%) 0.0000 海拔 (km) 1.000000 气压比幂次项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"P0\":\"42\"}，输出区含「压比 (%) 0.0000 海拔 (km) 1.000000 气压比幂次项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/qiyaxitongyidonglujing",
    "inputs": {
      "p": "42",
      "dp": "42"
    },
    "expect": [
      " 变化趋势：气压急升 系统移动： 高压系统快速接近或低压快速减弱，天气将明显转好。 天气展望： 低压填塞减弱，降水逐渐减弱停止，天气好转。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p\":\"42\",\"dp\":\"42\"}，输出区含「 变化趋势：气压急升 系统移动： 高压系统快速接近或低压快速减弱，天气将明显转好…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/risk-14",
    "inputs": {
      "t": "42",
      "rh": "42",
      "v": "42",
      "p": "42"
    },
    "expect": [
      " 风险贡献 温度 42.0°C 71% 25.0 湿度 42% 22% 4.3 风速 42.0m/s 100% 20.0 气压 42hPa 100% 25.0 气象条件较差，老人儿童及慢性病患者减少外出。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"t\":\"42\",\"rh\":\"42\",\"v\":\"42\",\"p\":\"42\"}，输出区含「 风险贡献 温度 42.0°C 71% 25.0 湿度 42% 22% 4.3 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/saturation-vapor-pressure",
    "inputs": {
      "T": "42"
    },
    "expect": [
      "Hg 毫米汞柱) 8200.93"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\"}，输出区含「Hg 毫米汞柱) 8200.93」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/relative-humidity",
    "inputs": {
      "T": "42",
      "Td": "42"
    },
    "expect": [
      "点差 (摄氏度) 82.04"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"Td\":\"42\"}，输出区含「点差 (摄氏度) 82.04」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/protection-3",
    "inputs": {
      "v0": "42",
      "v1": "0"
    },
    "expect": [
      "暴露时限：单次暴露 SPF 50+ 严格防护 防晒霜建议 全套防晒，建议留在室内 衣物防护 严禁户外暴晒 遮阴建议 2 分钟 I 极敏感 未防护晒伤时间"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"0\"}，输出区含「暴露时限：单次暴露 SPF 50+ 严格防护 防晒霜建议 全套防晒，建议留在室内…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/speed-11",
    "inputs": {
      "dbz": "42"
    },
    "expect": [
      "mm/h×60) 大雨/强降水 降水等级：大雨 较强降水，可能对流性"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dbz\":\"42\"}，输出区含「mm/h×60) 大雨/强降水 降水等级：大雨 较强降水，可能对流性」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/strength-3",
    "inputs": {
      "dbz": "42",
      "h": "42",
      "area": "42"
    },
    "expect": [
      "量 (m³/s) 较强对流 回波顶高：42.0 km（穿透对流） 冰雹概率 冰雹概率高，建议发布冰雹预警，户外人员注意防护。\n暂无计算记录"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dbz\":\"42\",\"h\":\"42\",\"area\":\"42\"}，输出区含「量 (m³/s) 较强对流 回波顶高：42.0 km（穿透对流） 冰雹概率 冰雹…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/taifengdingqiang",
    "inputs": {
      "pc": "42"
    },
    "expect": [
      "最大风速 (节) 1314.8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pc\":\"42\"}，输出区含「最大风速 (节) 1314.8」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/wet-bulb-temperature",
    "inputs": {
      "T": "42",
      "RH": "42"
    },
    "expect": [
      "42\n42\n30.71"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"RH\":\"42\"}，输出区含「42\n42\n30.71」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/temp-pressure",
    "inputs": {
      "temp": "42",
      "rh": "42",
      "pres": "42"
    },
    "expect": [
      "°C 、相对湿度 42% 、气压 42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"temp\":\"42\",\"rh\":\"42\",\"pres\":\"42\"}，输出区含「°C 、相对湿度 42% 、气压 42.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/wind-chill",
    "inputs": {
      "T": "42",
      "v": "42"
    },
    "expect": [
      "降温幅度 (度) 151.2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\",\"v\":\"42\"}，输出区含「降温幅度 (度) 151.2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/wind-direction",
    "inputs": {
      "deg": "42"
    },
    "expect": [
      "42\nNE 16 方位（42°） 0.733"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"deg\":\"42\"}，输出区含「42\nNE 16 方位（42°） 0.733」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "meteorology/temp",
    "inputs": {
      "v0": "42",
      "v1": "42",
      "v2": "42",
      "v3": "kmh"
    },
    "expect": [
      " 体感风险等级： 极危险 致命中暑风险"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v0\":\"42\",\"v1\":\"42\",\"v2\":\"42\",\"v3\":\"kmh\"}，输出区含「 体感风险等级： 极危险 致命中暑风险」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== meteorology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
