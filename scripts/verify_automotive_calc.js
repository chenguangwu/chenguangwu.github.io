#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "automotive/analysis-diagnosis",
  "inputs": {
    "code1": "P0301",
    "code2": "P0171",
    "code3": "",
    "code4": "",
    "coolant": "138",
    "stft": "18",
    "rpm": "750",
    "tps": "12"
  },
  "expect": [
    "138"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/analysis-strength",
  "inputs": {
    "b": "90",
    "h": "120",
    "L": "1000",
    "F": "5000",
    "sf": "1.5",
    "T": "2000"
  },
  "expect": [
    "1/25630"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/brake-pad-life",
  "inputs": {
    "newThickness": "18",
    "currentThickness": "6",
    "mileage": "30000",
    "yearlyKm": "15000"
  },
  "expect": [
    "14.0mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/bus-arrival-estimator",
  "inputs": {
    "interval": "15",
    "last": "09:05",
    "now": "09:12",
    "ride": "0",
    "err": "2",
    "iv2": "15",
    "last2": "09:02"
  },
  "expect": [
    "113"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-1",
  "inputs": {
    "m": "2250",
    "P": "130",
    "T": "250",
    "i": "12",
    "r": "0.32",
    "eff": "88",
    "cda": "0.65",
    "mu": "0.9",
    "sh": "2",
    "st": "0.35"
  },
  "expect": [
    "10.86"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-2",
  "inputs": {
    "tq": "375",
    "rpm": "4000",
    "kw": "",
    "rpm2": ""
  },
  "expect": [
    "157.08"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-3",
  "inputs": {
    "pv": "5.3"
  },
  "expect": [
    "76.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-4",
  "inputs": {
    "gw": "2250",
    "cap": "250",
    "lo": "10",
    "hi": "15",
    "real": "260"
  },
  "expect": [
    "1688"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-5",
  "inputs": {
    "v": "150",
    "s": "40",
    "g": "9.81"
  },
  "expect": [
    "41.67"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/calc-72",
  "inputs": {
    "bore": "129",
    "stroke": "86",
    "cyl": "4",
    "vc": "56"
  },
  "expect": [
    "21.07"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/catalyst",
  "inputs": {
    "hc1": "180",
    "hc2": "18",
    "co1": "0.8",
    "co2": "0.06",
    "nx1": "800",
    "nx2": "120"
  },
  "expect": [
    "92.5%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/cheshenkongqizulixishu",
  "inputs": {
    "area": "5.2",
    "cd": "0.30",
    "v": "100",
    "rho": "1.225",
    "cd2": "0.38",
    "eff": "90"
  },
  "expect": [
    "1062"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/container-loading",
  "inputs": {
    "pl": "4",
    "pw": "0.8",
    "ph": "0.6",
    "qty": "500",
    "wt": "80",
    "loss": "0"
  },
  "expect": [
    "14.18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/countdown-engine-oil",
  "inputs": {
    "car": "我的爱车",
    "last": "75000",
    "cur": "54000",
    "kmY": "15000"
  },
  "expect": [
    "-21000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/current-3",
  "inputs": {
    "volt": "17.5",
    "cur": "180",
    "pout": "1500",
    "rpm": "200",
    "tq": "",
    "ref": "50"
  },
  "expect": [
    "0.0972"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/cycle-13",
  "inputs": {
    "wPos": "rear"
  },
  "expect": [
    "后雨刷状态正常"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/cycle-belt",
  "inputs": {
    "curKm": "127500",
    "lastKm": "0",
    "yearKm": "15000"
  },
  "expect": [
    "127500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/depreciation",
  "inputs": {
    "price": "30",
    "res": "5",
    "years": "5",
    "used": "3",
    "kmY": "1.5"
  },
  "expect": [
    "12.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/detector-recorder-fuel",
  "inputs": {
    "win": "7",
    "car": "我的车",
    "data": "8.0\n7.8\n8.2\n7.9\n8.1\n8.3\n7.7\n8.0\n8.1\n7.8\n8.2\n10.5"
  },
  "expect": [
    "8.37"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/drive",
  "inputs": {
    "gear": "6.5",
    "final": "4.1",
    "circ": "2.0",
    "rpm": "6000",
    "tq": "200",
    "eff": "90"
  },
  "expect": [
    "15070220"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/engine-oil",
  "inputs": {
    "tmin": "-10",
    "tmax": "35",
    "age": "5",
    "eng": "turbo"
  },
  "expect": [
    "turbo"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/estimate-distance-1",
  "inputs": {
    "v": "150",
    "rt": "1",
    "mu": "1.0",
    "grade": "0",
    "mu2": "0.6",
    "gap": "2",
    "bt": "0"
  },
  "expect": [
    "130.2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/estimate-wear-tire",
  "inputs": {
    "nw": "12",
    "cw": "4",
    "km": "40000",
    "lim": "1.6",
    "warn": "3",
    "kmY": "15000",
    "other": "4.6"
  },
  "expect": [
    "208000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/fuel-anomaly",
  "inputs": {},
  "clicks": [
    "addRecord();addRecord();"
  ],
  "expect": [
    "49,000 1500km 40L 2.7 ¥312"
  ],
  "ref": "clicks 注入：addRecord() 在末条记录（47,500 km）基础上追加 1500 km、40 L、7.8 元/L 的新记录并重算平均油耗/异常条数/明细表。只点一次时该串也会被兜底遍历里的零参 addRecord() 复现（via=addRecord），故连点两次使之在 clicks 阶段即存在（实测第二次点击后 49,000 走 via=click）。旧锚「2026-07-01」是静态种子记录日期 ⇒ 判别力 0；新锚不含日期字段（addRecord 的日期取 new Date()，会随真实日期漂移），跨天仍稳定。清 clicks 后重跑不产出该行 ⇒ 零逃生项。"
},
{
  "slug": "automotive/fuel-cost-calculator",
  "inputs": {
    "km": "450",
    "fc": "7",
    "price": "8",
    "ppl": "4",
    "fc2": "9",
    "budget": "300"
  },
  "expect": [
    "450km"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/fuel-economy",
  "inputs": {
    "fuelL": "60",
    "dist": "560",
    "price": "8",
    "tank": "50",
    "remain": "10",
    "monthKm": "1500"
  },
  "expect": [
    "10.71"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/insurance-premium-estimator",
  "inputs": {
    "price": "23",
    "seatAmt": "1",
    "seats": "5"
  },
  "expect": [
    "0.88%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/lifespan-brake",
  "inputs": {
    "newT": "18",
    "curT": "6",
    "rateM": "0.5",
    "minT": "2",
    "kmM": "1200"
  },
  "expect": [
    "75%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/loan-calculator",
  "inputs": {
    "price": "18.8",
    "tax": "10",
    "extra": "1.5",
    "dp": "30",
    "years": "3",
    "rate": "4.35",
    "fee": "0",
    "mode": "equal"
  },
  "expect": [
    "月供 3906 元",
    "落地 22.18 万 · 含息总计 23.08 万",
    "9012 贷款总利息"
  ],
  "ref": "去默认化：priceY = 18.8×10000 = 188000；购置税 = 188000×10% = 18800；首付 = 188000×30% = 56400 ⇒ 本金 loanY = 131600（13.16 万）。月利率 r = 4.35/100/12 = 0.003625、n = 36 ⇒ 1.003625³⁶ = 1.1391458；月供 = 131600×0.003625×1.1391458/(1.1391458−1) = 3905.888 ⇒ 3906 元；总利息 = 3905.888×36 − 131600 = 9012 元。落地价 = (188000+18800+1.5×10000)/10000 = 22.18 万；含息总计 = (221800+9012)/10000 = 23.08 万。默认态 price=15 / tax=8.85 / extra=0.8 / rate=4.8 ⇒ 月供 3138 元、落地 17.13 万、含息 17.92 万，三条锚全部失配。（extra 单位是「万元」不是元 —— 误把 3000 灌进去会让落地价放大百倍；mode 的合法取值只有 equal / principal。）"
},
{
  "slug": "automotive/lux-1",
  "inputs": {
    "lm": "2250",
    "pw": "55",
    "d": "10",
    "ang": "15",
    "eff": "85",
    "lm2": "1000"
  },
  "expect": [
    "357.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/maintenance-schedule",
  "inputs": {
    "km": "67500",
    "kmM": "1200",
    "mon": "8",
    "ahead": "1000"
  },
  "expect": [
    "120000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/oil-change-countdown",
  "inputs": {
    "ldate": "2026-01-15",
    "last": "120000",
    "cur": "87000",
    "iv": "10000",
    "ivm": "12",
    "warn": "500"
  },
  "expect": [
    "120000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/oil-change",
  "inputs": {
    "yearKm": "22500",
    "curKm": "30000",
    "doneKm": "3000"
  },
  "expect": [
    "22500"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/parking-fee-calculator",
  "inputs": {
    "firstMin": "90",
    "firstFee": "10",
    "unitMin": "30",
    "unitFee": "5",
    "parkMin": "180",
    "cap": "60",
    "freeMin": "0",
    "days": "1"
  },
  "expect": [
    "8.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/pressure-fuel-oil",
  "inputs": {
    "flow": "525",
    "ratedP": "3",
    "railP": "3",
    "pw": "3.5",
    "cyl": "4",
    "rpm": "2500",
    "disp": "2.0",
    "ve": "35"
  },
  "expect": [
    "0.0306"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/qichekongtiaoxuanxing",
  "inputs": {
    "vol": "8",
    "ppl": "2",
    "amb": "35",
    "dt": "15",
    "cop": "2.8"
  },
  "expect": [
    "5.42"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/recommender-6",
  "inputs": {
    "amb": "38",
    "p1": "2.3",
    "p2": "2.3",
    "ref": "20",
    "alm": "25"
  },
  "expect": [
    "-0.03"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/resistance-1",
  "inputs": {
    "rp": "3.8",
    "rs": "8",
    "t": "25"
  },
  "expect": [
    "3.73"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/scheduler-cycle-maintenance",
  "inputs": {
    "km": "78000",
    "last": "45000",
    "kmM": "1500",
    "ahead": "1000"
  },
  "expect": [
    "105000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/shipping-cost-compare",
  "inputs": {
    "w": "18",
    "l": "60",
    "wd": "40",
    "h": "35",
    "ratio": "8000",
    "zone": "1",
    "ins": "5000",
    "insr": "0.5",
    "cw": "0",
    "cn": "0"
  },
  "expect": [
    "体积重 10.5 kg",
    "最低总价 经济快递 84 元",
    "保价费 25 元"
  ],
  "ref": "去默认化：体积重 = 60×40×35/8000 = 10.5 kg；实重 18 > 体积重 ⇒ 计费重量取 18 kg（按实重计费，byVol 为假）。保价费 = max(1, 5000×0.5%) = 25 元。邻省档（zone=1）首重价：经济 8 / 标准 11 / 时效 18；大件首重 3 kg 价 20。续重件数 = ceil(18−1) = 17 ⇒ 经济 8+17×3 = 59、标准 11+17×4 = 79、时效 18+17×6 = 120；大件 = ceil(18−3) = 15 ⇒ 20+15×3 = 65。加保价费后总价：经济 84、大件 90、标准 104、时效 145 ⇒ 最低「经济快递 84 元」，最贵「时效快递」，差 61 元。默认态 w=8 / l=50 / wd=40 / h=30 / ratio=6000 / zone=0(同城) / ins=0 ⇒ 体积重 10 kg 且按体积重计费、最低总价 24 元、未保价，三条锚全部失配。（ratio 是 select，合法取值仅 6000/8000/12000，注入 5000 会静默不生效。）"
},
{
  "slug": "automotive/temp-pressure-1",
  "inputs": {
    "lp": "3.18",
    "hp": "1.35",
    "amb": "30",
    "vent": "8",
    "stat": "0"
  },
  "expect": [
    "3.18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/tester-10",
  "inputs": {
    "c1": "75.5",
    "c2": "49.8",
    "c3": "50.2",
    "c4": "46.5",
    "std": "50",
    "tol": "5",
    "rep": "1",
    "dur": "60"
  },
  "expect": [
    "13.436"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/tester-11",
  "inputs": {
    "cca0": "900",
    "cca": "510",
    "res": "7.2",
    "temp": "25",
    "age": "42",
    "disp": "2.0"
  },
  "expect": [
    "+85.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/time-maintenance",
  "inputs": {
    "km": "64500",
    "age": "4",
    "last": "11",
    "perY": "9000",
    "ahead": "800"
  },
  "expect": [
    "120000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/tire-pressure",
  "inputs": {
    "f0": "5.3",
    "r0": "2.1",
    "fc": "2.0",
    "rc": "1.9"
  },
  "expect": [
    "76.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/tire-wear",
  "inputs": {
    "newDepth": "12",
    "mileage": "35000"
  },
  "expect": [
    "11.6mm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/traffic-fine-calculator",
  "inputs": {
    "had": "9",
    "cut": "0"
  },
  "expect": [
    "117"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/transport-calculator",
  "inputs": {
    "km": "620",
    "fc": "7.8",
    "price": "8.35",
    "speed": "70",
    "load": "2.1",
    "rate": "85",
    "v0": "90",
    "rt": "1.2",
    "vol": "1000",
    "wt": "790",
    "tire": "205/55 R16",
    "mu": "4.5"
  },
  "expect": [
    "油费 404 元 · 吨公里 0.36 元",
    "实载 1.78 吨",
    "99.4 米"
  ],
  "ref": "去默认化：注入 km=620 / fc=7.8 / price=8.35 ⇒ 油费 = 620/100×7.8×8.35 = 403.806 ⇒ fmtNum(,0) 为 404；装载率 85% ⇒ 实载 = 2.1×85/100 = 1.785 ⇒ toFixed(2) 去尾零为 1.78；吨公里 = 403.806/(1.785×620) = 0.36481 ⇒ 0.36。制动段：v0=90 ⇒ vms = 25；反应距离 = 25×1.2 = 30；制动距离 = 25²/(2×4.5) = 69.4444；停车总距离 = 99.4444 ⇒ 99.4 米。默认态 km=300 / fc=20 / price=7.5 / load=5 / rate=60 / v0=60 / rt=1 / mu=6.5 ⇒ 油费 450、实载 3.00、吨公里 0.50、停车总距离 38.1 米，三条锚全部失配。（mu 取标注内的「湿滑 4.5」值；该字段 label 写作「荷载系数」却在制动公式中当摩擦系数用，属既有口径缺陷，本例不把制动距离写成断言以外的判定。）"
},
{
  "slug": "automotive/voltage-1",
  "inputs": {
    "altCurrent": "135",
    "voltage": "14.4",
    "chargeCurrent": "10",
    "newLoadName": "",
    "newLoadCurrent": "0"
  },
  "expect": [
    "28.1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/voltage-2",
  "inputs": {
    "volt": "14",
    "vreg": "14.4",
    "cutin": "1200",
    "rpm": "2000",
    "vbat": "12.4",
    "rloop": "0.35",
    "load": "25",
    "len": "4",
    "area": "2.5",
    "mat": "0.0282"
  },
  "expect": [
    "充电电流 5.7 A",
    "末端电压 11.74 V",
    "2.26 V（16.1%）"
  ],
  "ref": "去默认化：注入 rpm=2000 / cutin=1200 ⇒ ratio = 1.6667 ≥ 1 ⇒ genV = 14.4×min(1,1.6667) = 14.4；充电电流 = (14.4−12.4)/max(0.35,0.001) = 5.7143 ⇒ 5.7 A；vbat=12.4 落在 [12.24,12.45) ⇒ SOC 文案「约 50%」。线路：Rs = 0.0282×4/2.5 = 0.04512，Rd = 2Rs = 0.09024 ⇒ 压降 = 25×0.09024 = 2.256 ⇒ 2.26 V；压降率 = 2.256/14×100 = 16.1138 ⇒ 16.1%；末端电压 = 14−2.256 = 11.744 ⇒ 11.74 V，>8% ⇒ 判定「过高（>8%）」。默认态 volt=12 / mat=0.0175 / len=5 / load=10 / rloop=0.08 / cutin=700 / rpm=2500 ⇒ 末端电压 11.30 V、压降 0.70 V（5.8%）、充电电流 25.0 A，三条锚全部失配。（「发电机输出电压 14.4 V」不可作锚 —— 默认态 ratio≥1 时 genV 同为 14.4。）"
},
{
  "slug": "automotive/wear-brake",
  "inputs": {
    "nw": "38",
    "cu": "23.5",
    "min": "22",
    "run": "0.03",
    "km": "6",
    "pad": "8"
  },
  "expect": [
    "14.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "automotive/wear-tire",
  "inputs": {
    "lf": "4.0",
    "rf": "3.9",
    "lr": "5.4",
    "rr": "5.2",
    "newD": "8",
    "km": "26000",
    "minD": "1.6",
    "interval": "10000",
    "drive": "awd",
    "single": "yes"
  },
  "expect": [
    "后→前磨损差异 1.35 mm",
    "四轮最大差异 1.5 mm",
    "右前（14585 km）"
  ],
  "ref": "去默认化：newD=8 ⇒ 四轮磨损 = [8−4.0, 8−3.9, 8−5.4, 8−5.2] = [4.0, 4.1, 2.6, 2.8]。前轴均 = (4.0+4.1)/2 = 4.05、后轴均 = (2.6+2.8)/2 = 2.7 ⇒ 后→前差 = 1.35 mm；四轮极差 = 4.1−2.6 = 1.5 mm；同轴左右差 前 0.10 / 后 0.20。轴差 1.35 < 1.5 但极差 1.5 ≥ 1.5 ⇒ 换位条件 needRot 为真。已行驶 26000 km ⇒ kmW = 2.6 万；各轮剩余里程 = (当前深度−1.6) ÷ (磨损量/2.6) × 10000 ⇒ 左前 15600、右前 14585.37、左后 38000、右后 33428.57 ⇒ 最小为右前 ⇒ 14585 km。默认态 lf=5.2 / rf=5.0 / lr=6.8 / rr=6.6 / km=20000 ⇒ 后→前差 1.60 mm、极差 1.80 mm、最先到限 22667 km，三条锚全部失配。（single=yes 使换位方案文案变为「单向花纹：…」；drive / single 均为 select，合法取值 awd|ff|fr 与 yes|no。）"
},
{
  "slug": "automotive/xuanguatanhuangzunitexing",
  "inputs": {
    "k": "42",
    "c": "2000",
    "m": "400",
    "mu": "45",
    "kt": "220",
    "load": "380",
    "stroke": "200"
  },
  "expect": [
    "1.631"
  ],
  "ref": "auto-restore"
},

  // ---- BATCH265：automotive 分类「油耗 / 油费 / 胎压psi / 轮胎磨损率 / 电池SOH」第二组参数族（5 例） ----
  {
    "slug": "automotive/fuel-economy",
    "inputs": { "fuelL": "45", "dist": "700", "price": "7.5", "tank": "55", "remain": "5", "monthKm": "2000" },
    "expect": [ "6.43 L/100km", "337.5 元" ],
    "ref": "第二组参数（第一组为 60L/560km/8元）。百公里油耗 = 45 L ÷ 700 km × 100 = **6.43**，本次油费 = 6.4286 × 700 × 7.5 ÷ 100 = **337.5 元** —— 两条同源不同式（一个是每百公里油耗、一个是整段油价总价），可独立复核。默认组（40 L / 560 km / 8 元）算得 7.14 L/100km 与 320 元，均不命中。",
  },
  {
    "slug": "automotive/fuel-cost-calculator",
    "inputs": { "km": "500", "fc": "8.5", "price": "7.8", "ppl": "5", "fc2": "10", "budget": "400" },
    "expect": [ "331.5 元", "人均 66.3 元" ],
    "ref": "第二组参数（第一组为 450km/7L/8元）。油费 = 500 ÷ 100 × 8.5 L × 7.8 元 = **331.5 元**；人均 = 331.5 ÷ 5 = **66.3 元**。默认组的 168 元与 42 元都不命中。刻意让 fc（本组油耗）与 ppl（乘车人数）取不同值，使人均值不与总油价同值。",
  },
  {
    "slug": "automotive/tire-pressure",
    "inputs": { "f0": "2.5", "r0": "2.2", "fc": "2.2", "rc": "2.0" },
    "expect": [ "折合 前 36.3", "后 31.9 psi" ],
    "ref": "第二组参数（第一组 f0=5.3）。bar → psi 换算系数 14.5038：前轮 2.5 × 14.5038 = **36.3** psi，后轮 2.2 × 14.5038 = **31.9** psi，同系数不同被换算量 ⇒ 互为交叉校验。默认组 2.3/2.1 bar ⇒ 33.4 / 30.5 psi，不命中。锚不碰「前 2.5 / 后 2.2 bar」（那是输入回显）。",
  },
  {
    "slug": "automotive/estimate-wear-tire",
    "inputs": { "nw": "9", "cw": "5", "km": "60000" },
    "expect": [ "0.067 mm/千km" ],
    "ref": "第二组参数（第一组 nw=12/cw=4/km=40000）。磨损率 = (新胎花纹 9 − 当前 5) ÷ 60 千km = **0.067 mm/千km**，一步除法可手算；默认组的 0.1 mm/千km 不命中。同页的「剩余可用深度 / 剩余里程」由 other 与 kmY 复合得出、来源无法独立复算 ⇒ 不锚。",
  },
  {
    "slug": "automotive/tester-11",
    "inputs": { "cca0": "650", "cca": "520", "res": "8.5", "temp": "20", "age": "48" },
    "expect": [ "SOH 80 %" ],
    "ref": "第二组参数（第一组 cca0=900/cca=510）。SOH = 实测 CCA 520 ÷ 新电池 CCA 650 = **80%**，一次除法即可复核。第一组用例锚的是差值行 +85.1，本条锚的是比值本身，两者互不削弱。",
  },

{
    "slug": "automotive/parking-fee-calculator",
    "inputs": {
      "firstMin": "15",
      "firstFee": "10",
      "unitMin": "15",
      "unitFee": "5",
      "parkMin": "120",
      "cap": "50",
      "freeMin": "0",
      "days": "1"
    },
    "expect": [
      "应付 45 元"
    ],
    "ref": "计费时长 120 − 免费 0 = 120 分钟；首段 15 分钟收 10 元，剩余 105 分钟 ÷ 15 = 7 单位 × 5 元 = 35 元；合计 45 元（未触封顶 50）。页面输出 '应付 45 元'。默认态参数组合不产生 45 元。"
  },
  {
    "slug": "automotive/fuel-cost-calculator",
    "inputs": {
      "km": "100",
      "fc": "8",
      "price": "7.5",
      "ppl": "0",
      "fc2": "0",
      "budget": "0"
    },
    "expect": [
      "60 单程油费 (元)"
    ],
    "ref": "油费 = 100 ÷ 100 × 8 × 7.5 = ¥60.00。页面输出 '60 单程油费 (元)'。默认态其他输入不产生 60。"
  }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== automotive calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
