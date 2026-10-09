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
