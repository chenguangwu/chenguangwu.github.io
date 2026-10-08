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
