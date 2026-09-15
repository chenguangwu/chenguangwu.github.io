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
  "expect": [
    "2026-07-01"
  ],
  "ref": "auto-restore(default)"
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
    "price": "23",
    "tax": "8.85",
    "extra": "0.8",
    "dp": "30",
    "years": "3",
    "rate": "4.8",
    "fee": "0"
  },
  "expect": [
    "12191"
  ],
  "ref": "auto-restore"
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
    "w": "12",
    "l": "50",
    "wd": "40",
    "h": "30",
    "ins": "0",
    "insr": "0.5",
    "cw": "0",
    "cn": "0"
  },
  "expect": [
    "36.5"
  ],
  "ref": "auto-restore"
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
    "km": "450",
    "fc": "20",
    "price": "7.5",
    "speed": "60",
    "load": "5",
    "rate": "60",
    "v0": "60",
    "rt": "1",
    "vol": "10",
    "wt": "6",
    "tire": "205/55R16",
    "mu": "6.5"
  },
  "expect": [
    "675"
  ],
  "ref": "auto-restore"
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
    "volt": "18",
    "vreg": "14.4",
    "cutin": "700",
    "rpm": "2500",
    "vbat": "12.4",
    "rloop": "0.08",
    "load": "10",
    "len": "5",
    "area": "2.5"
  },
  "expect": [
    "17.3"
  ],
  "ref": "auto-restore"
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
    "lf": "8.2",
    "rf": "5.0",
    "lr": "6.8",
    "rr": "6.6",
    "newD": "8",
    "km": "20000",
    "minD": "1.6",
    "interval": "10000"
  },
  "expect": [
    "-0.2"
  ],
  "ref": "auto-restore"
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
