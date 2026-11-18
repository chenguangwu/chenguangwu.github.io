#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical/assessor-risk-3",
  "inputs": {
    "ph": "9",
    "water": "1500",
    "protein": "1.2",
    "sodium": "3000",
    "oxalate": "150"
  },
  "expect": [
    "4/20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calc-34",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30"
  },
  "expect": [
    "1898"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "weight": "30",
    "age": ""
  },
  "expect": ["375.0 mg 单次剂量", "60 mg/kg × 30 kg = 1.80 g/日；成人按成人绝对上限"],
  "ref": "成人分轨：年龄空值按成人口径，有效上限只取成人绝对上限 4.00 g/日，不再与儿童按体重上限（1.80 g）取较小值。30 kg 对乙酰氨基酚中位单次 375.0 mg，未超限。默认态 20 kg ⇒ 单次 250.0 mg / 体重上限串为 1.20 g，均不命中。"
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "5",
    "freq": "12",
    "tier": "high",
    "weight": "60",
    "age": ""
  },
  "expect": ["已超过最大日剂量 1.00 g"],
  "ref": "成人分轨（年龄空值）：头孢呋辛酯（idx 5）30 mg/kg q12h、60 kg ⇒ 单次 1800 mg、日 3600 mg；成人绝对上限 1000 mg/日 ⇒ 超限并给出封顶 500.0 mg。旧实现取 min(1000,3600)=1000 结果相同，但口径已改为成人只取成人上限；默认态 500/20/中位 日 250 mg 远低于上限，不命中。",
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "0",
    "freq": "4",
    "tier": "high",
    "weight": "30",
    "age": "13"
  },
  "expect": ["年龄 13 岁：按儿童口径处理（未满 14 岁）", "已超过最大日剂量 1.80 g"],
  "ref": "D-N5 13 岁：对乙酰氨基酚上限档 15 mg/kg q4h、30 kg ⇒ 单次 450 mg、日 2700 mg；儿童按体重上限 60×30 = 1800 mg，成人绝对上限 4000 mg，有效上限 min = 1800 mg ⇒ 超限。旧实现 13 岁走儿童口径本也 1800 mg，但新增「年龄 13 岁」明确标注；默认态年龄空值只会显示「年龄未填写」，不命中。",
},
{
  "slug": "medical/calculator-calc-2",
  "inputs": {
    "drug": "0",
    "freq": "4",
    "tier": "high",
    "weight": "30",
    "age": "14"
  },
  "expect": ["年龄 14 岁：按成人口径处理（≥14 岁）", "60 mg/kg × 30 kg = 1.80 g/日；成人按成人绝对上限"],
  "ref": "成人分轨：14 岁按成人口径，有效上限 = 成人绝对上限 4000 mg（不再取 min(4000,1800)=1800），日剂量 2700 mg 不再超限；与 13 岁用例（超限 1.80 g）方向相反，构成边界判别。默认态年龄空值只显示「年龄未填写」，且体重 20 kg ⇒ 体重上限串为 1.20 g，均不命中。",
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "750",
    "dur": "4",
    "conc": "0.4",
    "w": "60"
  },
  "expect": [
    "187.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "240",
    "dur": "4",
    "drop": "20",
    "drug": "nacl3"
  },
  "expect": ["当前 3%氯化钠 速率 = 0.510 mEq/kg/h"],
  "ref": "D-N8 首次切换实况：240 mL/4 h/60 kg，滴系数 20 ⇒ 60.0 mL/h；切换 3%NaCl 后默认浓度 0.51 mEq/mL ⇒ 30.6 mEq/h ÷ 60 kg = 0.510 mEq/kg/h，超过 0.5 限值应判超限。旧实现 onchange 先 calc（用旧浓度 0.4）再 toggle 改浓度 ⇒ 首次算得 0.400 并误判安全；默认态 drug=none 无该速率串 ⇒ 判别力成立（注入 conc 会掩盖该缺陷，故不注入）。",
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "100",
    "dur": "24",
    "drug": "kcl",
    "conc": "2.0",
    "w": "60"
  },
  "expect": ["浓度超过外周静脉上限"],
  "ref": "D-N9 浓度硬上限：100 mL/24 h ⇒ 4.17 mL/h × 2.0 mEq/mL = 8.33 mEq/h（≤20 旧实现判安全），但浓度 2.0 是外周上限 0.4 的 5 倍 ⇒ 须判超限并提示中心静脉/心电监护。drug 先于 conc 注入，避免 toggleDrugRow 把浓度改回默认 0.4。",
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "100",
    "dur": "1",
    "drug": "kcl",
    "conc": "0.4",
    "w": "20"
  },
  "expect": ["取较小值 ≤10.0 mEq/h"],
  "ref": "D-N9 体重上限：100 mL/1 h ⇒ 100 mL/h × 0.4 = 40 mEq/h；20 kg 按 0.5 mEq/kg/h = 10 mEq/h，与成人 20 取较小值 ⇒ 10.0，应判超限。旧实现只比 20 ⇒ 40 > 20 也超，但 20 kg 的 10 mEq/h 门槛完全未体现；56 kg 以上时 0.5×w ≥ 20，成人口径不变。",
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "100",
    "dur": "1",
    "drug": "kcl",
    "conc": "0.2",
    "w": "60"
  },
  "expect": ["✓ 当前 KCl 输注速率 = 20.00 mEq/h"],
  "ref": "D-N9 边界放行：100 mL/h × 0.2 mEq/mL = 20.00 mEq/h，等于成人上限、浓度 0.2 ≤0.4 ⇒ 应判安全（✓），防止把 ≤ 误写成 <。默认态 drug=none 不含该串。",
},
{
  "slug": "medical/calculator-calc-infusion",
  "inputs": {
    "vol": "100",
    "dur": "1",
    "drug": "kcl",
    "conc": "0",
    "w": "60"
  },
  "expect": ["请输入有效的 KCl 浓度"],
  "ref": "D-N9 浓度空/零守卫：conc=0 时速率恒 0 会被误判安全，须拒绝并提示输入有效浓度。",
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "2.0",
    "meld_cr": "1.0",
    "meld_inr": "1.2",
    "meld_na": "140",
    "gcs_e": "3"
  },
  "expect": [
    "E3+V5+M6"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "3.0",
    "meld_cr": "2.0",
    "meld_inr": "1.5",
    "meld_na": "130"
  },
  "expect": [
    "MELD-Na = 26.0（已纳入血钠校正）"
  ],
  "ref": "W1-A 回归：标准 MELD = 3.78×ln(3.0) + 11.2×ln(1.5) + 9.57×ln(2.0) + 6.43 = 21.8；血钠 130（钳制区间内）⇒ MELD-Na = 21.8 + 1.32×7 − 0.033×21.8×7 = 26.0。四项输入均非默认（2.0/1.0/1.2/140）；旧实现输出 MELD-Na 恒 6，本串不命中。"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "meld_bili": "1.0",
    "meld_cr": "10.0",
    "meld_inr": "1.0",
    "meld_na": "120"
  },
  "expect": [
    "MELD-Na = 27.7（已纳入血钠校正）"
  ],
  "ref": "D-N40 封顶与钳制：肌酐 10 须按 UNOS 上限 4.0 计（未勾透析），胆红素/INR 下限按 1 ⇒ MELD = 9.57×ln4 + 6.43 = 19.7；血钠 120 钳制到 125 ⇒ MELD-Na = 19.7 + 1.32×12 − 0.033×19.7×12 = 27.7。旧实现不封顶肌酐且按 (MELD−6) 查表校正，本串不命中。"
},
{
  "slug": "medical/clinical-tools",
  "checkIds": ["cha_chf", "cha_htn", "cha_age75", "cha_age65"],
  "clicks": [
    "calcCHA();var b=document.getElementById('result-cha').innerHTML;var m=/class=\"val\">(\\d+)</.exec(b);document.getElementById('result-cha').innerHTML=(m&&m[1]==='4')?'__CHA_AGE_OK__':'__CHA_AGE_FAIL__'+b"
  ],
  "expect": [
    "__CHA_AGE_OK__"
  ],
  "ref": "D-N41 年龄互斥：心衰 1 + 高血压 1 + ≥75 岁 2 = 4 分；65–74 岁与 ≥75 岁同时勾选时按较高档计并取消低档（旧实现相加成 5 分并抬到「高风险」）。clicks 把结果区分数读回比对，4 分输出标记串；5 分（旧实现）或分数解析失败均输出 FAIL 串。"
},
{
  "slug": "medical/clinical-tools",
  "inputs": {
    "gcs_e": "1",
    "gcs_v": "2",
    "gcs_m": "3"
  },
  "expect": [
    "（E1+V2+M3=6）",
    "重度昏迷"
  ],
  "ref": "D-N41 去默认化：注入 E1+V2+M3=6（页面默认 4/5/6）⇒ 重度昏迷。旧实现把 6 分归入轻/中度或只回显默认总分，两锚均失配；默认态 15 分不含本串。"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "1",
    "from": "1",
    "to": "18.0182"
  },
  "expect": [
    "0.0554994394557"
  ],
  "ref": "统一系数 18.0182 后：1 mg/dL→mmol/L = 1×1÷18.0182 = 0.0554994394557（toPrecision(12)）。默认「5.6 mmol/L → mg/dL」为 100.90192，不命中。"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "5"
  },
  "expect": [
    "90.091",
    "正常（空腹）"
  ],
  "ref": "D-N32 默认方向去默认化：注入 val=5（页面默认 5.6）、from=mmol、to=mg/dL ⇒ 5×18.0182 = 90.091 mg/dL；按 5 mmol/L 落「正常（空腹）」。修复前默认 to 也是 mmol/L ⇒ 同单位换算，系数取整 18 时输出 90；默认态 100.90192 不含本串。"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "7.2",
    "from": "18.0182",
    "to": "18.0182"
  },
  "expect": [
    "7.2",
    "源单位与目标单位相同"
  ],
  "ref": "D-N32 同单位守卫去默认化：注入 val=7.2（页面默认 5.6）且 from=to ⇒ 提示无需换算并回显注入值；旧实现输出「7.2 mmol/L = 7.2 mmol/L」并附分级，不命中本串。"
},
{
  "slug": "medical/convert-glucose",
  "inputs": {
    "val": "",
    "from": "18.0182",
    "to": "1"
  },
  "expect": [
    "请输入有效的血糖数值"
  ],
  "ref": "D-N32 空值守卫：清空数值时旧实现 +''||0 ⇒ 0，输出 0 mg/dL 并判低血糖；修复后拒绝并提示须 >0。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "20",
    "time": "",
    "dripIn": "30"
  },
  "expect": [
    "按已知滴速反算输注时长 = 333.3 分钟（约 5 小时 33 分钟）"
  ],
  "ref": "D-N10 反向换算：总滴数 = 500×20 = 10000；时长 = 10000÷30 = 333.33 → 333.3 分钟 = 5 小时 33 分；并输出预计完成时间。修复前无 dripIn 输入、只能按时间正向算，无法完成页面宣称的时间换算。默认 dripIn 空 ⇒ 不命中。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "20",
    "time": "120",
    "dripIn": "30"
  },
  "expect": [
    "相差 213.3 分钟，请确认以哪个为准"
  ],
  "ref": "D-N10 双向核对：计划 120 分钟 vs 按 30 滴/分反算 333.3 分钟，差 213.3 分钟 ⇒ 并列提示以哪个为准，不静默覆盖。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "20",
    "time": "",
    "dripIn": ""
  },
  "expect": [
    "输注时间须大于 0（或填写已知滴速以反算时长）"
  ],
  "ref": "D-N10 输入完整性：时间与已知滴速同时为空 ⇒ 无法换算，须提示至少填写一项（原实现只校验 time>0，文案已扩展）。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "1000",
    "df": "15",
    "time": "60"
  },
  "expect": [
    "滴速 = 250.00 滴/分"
  ],
  "ref": "去默认化：滴速 = vol×df/time = 1000×15/60 = 250.00 滴/分。默认态 vol=500/df=20/time=120 ⇒ 83.33 滴/分，不命中。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "250",
    "df": "20",
    "time": "100"
  },
  "expect": [
    "滴速 = 50.00 滴/分"
  ],
  "ref": "去默认化：滴速 = 250×20/100 = 50.00 滴/分。默认态不命中。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "20",
    "time": "0"
  },
  "expect": ["输注时间须大于 0"],
  "ref": "D-N10 时长 0 实况：旧实现 time=0 ⇒ 500×20÷0 = Infinity 滴/分；修复后逐项守卫判 time>0 失败，清空主结果并提示「输注时间须大于 0」，不输出 Infinity/NaN。默认 time=120 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "500",
    "df": "0",
    "time": "120"
  },
  "expect": ["滴系数须大于 0"],
  "ref": "D-N10 逐项校验：滴系数 0 时旧实现滴速 0、总滴数 0 且无提示；修复后判 df>0 失败并提示。默认 df=20 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/convert-time-infusion",
  "inputs": {
    "vol": "0",
    "df": "20",
    "time": "120"
  },
  "expect": ["液体量须大于 0"],
  "ref": "D-N10 逐项校验：液体量 0 时旧实现滴速 0、总滴数 0 且无提示；修复后判 vol>0 失败并提示整句「液体量须大于 0」。默认 vol=500 有效，不含该提示 ⇒ 判别力成立。"
},
{
  "slug": "medical/drug-info",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "未找到匹配药物"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=render() 过滤 34 种药物得空集 ⇒ 结果区渲染「未找到匹配药物」。默认态（search 空）渲染全部 34 种、blob 内无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "medical/drug-info",
  "inputs": {
    "search": "肝毒性"
  },
  "expect": [
    "共 1 种药物"
  ],
  "ref": "D-N12 搜索字段扩展：blob 纳入 dose/adverse/contraind/note 后，仅在「不良反应：肝毒性」出现的对乙酰氨基酚应命中 1 种；修复前 blob 只含 name/en/goods/use/cat ⇒ 0 种（「未找到匹配药物」）。默认空搜索为「共 34 种药物」，与本锚零交集。"
},
{
  "slug": "medical/drug-info",
  "clicks": [
    "currentCat='解热镇痛';initCats();render();applyDrugPreset('bp');document.getElementById('__tbProbe').textContent='D12 '+document.getElementById('countBar').textContent;"
  ],
  "expect": [
    "D12 共 4 种药物"
  ],
  "ref": "D-N12 预设重置分类：先切到「解热镇痛」分类（此时点降压预设会被分类过滤成 0 条），再 applyDrugPreset('bp')；修复后先把 currentCat 重置为 all ⇒ 「高血压」命中 4 种（氨氯地平/美托洛尔/依那普利/缬沙坦）。修复前分类不变 ⇒ 「共 0 种药物」。默认态为「共 34 种药物」，探针串不命中。"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "weight": "98",
    "height": "170",
    "age": "30",
    "bf": ""
  },
  "expect": [
    "+7.9%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "weight": "70",
    "height": "170",
    "age": "30",
    "bf": "80"
  },
  "expect": [
    "1618 kcal/天"
  ],
  "ref": "D-N73/D-N74：注入 70kg/170cm/30 岁/男、体脂 80% 越界，旧实现仍按 Katch 算成「三式平均」；修复后越界体脂按缺失处理，Mifflin-St Jeor = 10×70+6.25×170−5×30+5 = 1617.5 ⇒ 1618 kcal/天。原「两式平均」在默认空体脂也出现（逃生），已剔除，只保留注入值决定的 BMR 锚。"
},
{
  "slug": "medical/estimate-metabolism",
  "inputs": {
    "sex": "m",
    "weight": "120",
    "height": "190",
    "age": "25",
    "activity": "1.9",
    "bf": ""
  },
  "expect": [
    "超过建议的 300–500 kcal 上限"
  ],
  "ref": "D-N75 缺口上限：120kg/190cm/25 岁/1.9 ⇒ TDEE≈4308、-20% 缺口≈862 kcal > 500，应提示下调；旧实现只比较减脂热量是否低于 RMR，本例 3447>2268 会静默通过。默认 65/170/30/1.2 缺口约 376 kcal，不触发。"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "90",
    "dose_per_kg": "10",
    "dose_freq": "3",
    "iv_volume": "500",
    "iv_time": "120",
    "glucose_mmol": "5.6",
    "glucose_mg": "100.9",
    "temp_value": "36.5",
    "bp_sbp": "120",
    "bp_dbp": "80",
    "timer_custom_min": ""
  },
  "expect": [
    "900.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "medical/medical-calculator",
  "inputs": {
    "dose_weight": "60",
    "dose_per_kg": "10",
    "dose_freq": "1.5"
  },
  "expect": [
    "每次剂量 = 600.0mg / 1.5次 = 400.0mg"
  ],
  "ref": "D-N23 小数频次：旧实现 parseInt 把 1.5 截断为 1，每日 600.0mg 被算成每次 600.0mg；修复后 parseFloat 保留 1.5 ⇒ 600.0 ÷ 1.5 = 400.0mg。默认 freq=3 时该串为「600.0mg / 3次 = 200.0mg」，不命中 ⇒ 强判别。"
},
{
  "slug": "medical/medical-calculator",
  "inputs": { "dose_weight": "60", "dose_per_kg": "10", "dose_freq": "0.5" },
  "expect": ["服药频率须为 1–24 次/天"],
  "ref": "D-N23（2026-11-16）：频率输入标注 1–24 次/天，但旧实现只拦 ≤0，0.5 次/天输出日 600.0 mg、每次 1200.0 mg。现 freq<1 直接拦截。默认 3 ⇒ 不命中。"
},
{
  "slug": "medical/medical-calculator",
  "clicks": [
    "document.getElementById('glucose_mmol').value='';convertGlucose('mmol');"
  ],
  "expect": ["请输入有效的血糖值（mmol/L ≥ 0）"],
  "ref": "D-N24（2026-11-16）：清空 mmol/L 后旧实现直接 return，mg/dL 与「正常空腹血糖」结论原样保留。现清空另一侧并替换为提示；默认 5.6/100.9 ⇒ 不命中。"
},
{
  "slug": "medical/medical-calculator",
  "clicks": [
    "document.getElementById('glucose_mg').value='abc';convertGlucose('mg');"
  ],
  "expect": ["请输入有效的血糖值（mg/dL ≥ 0）"],
  "ref": "D-N24 反向：mg/dL 非法输入同样清空 mmol/L 并提示，不再保留旧分级。"
},
{
  "slug": "medical/reminder-2",
  "inputs": {
    "medName": "阿莫西林胶囊",
    "medBatch": "B20260118",
    "medExpiry": "2027-03-15",
    "medSpec": "0.25g×24粒",
    "medLocation": "客厅药箱"
  },
  "clicks": ["addMed()"],
  "expect": [
    "阿莫西林胶囊 0.25g×24粒",
    "1 药品总数",
    "批号：B20260118"
  ],
  "ref": "addMed() 要求 medName 与 medExpiry 均非空（否则 showToast 后直接 return），两项都要注入；"
     + "入表后 renderAll() 刷新 medList 与 statGrid。不锚「剩 N 天」与安全/注意/紧急计数 —— 均随运行日漂移。"
     + "默认态 meds 为空 ⇒ 列表恒「暂无药品记录」、总数恒 0。",
},
{
  "slug": "medical/stats-4",
  "inputs": {
    "cases": "阑尾切除,55\n阑尾切除,72\n阑尾切除,64\n阑尾切除,88\n阑尾切除,61"
  },
  "expect": [
    "68.0",
    "89.0",
    "12.75"
  ],
  "ref": "手术时长：5 例 55/72/64/88/61 → 均值 340/5=68.0 分钟，样本标准差 12.75，排台上限 P95=68.0+1.645×12.75=89.0（独立复算，非页面默认记录）"
}
,{
  "slug": "medical/dosage-calculator",
  "inputs": {"tyAge": "12"},
  "clicks": ["function setv(id,v){document.getElementById(id).value=v} function tick(id,v){document.getElementById(id).checked=v} setv('tyAge','12');setv('tyTaken','8');setv('tyHours','4');setv('tyReason','fever');tick('tyProduct',true);tick('tyRisk',true);tick('tyLimits',true);tyCheck();var ok=document.getElementById('tyResult').textContent.indexOf('650 mg')>=0; setv('tyAge','11.99');tyCheck();ok=ok&&document.getElementById('tyResult').textContent.indexOf('650 mg')<0;setv('tyAge','12');setv('tyTaken','9');tyCheck();ok=ok&&document.getElementById('tyResult').textContent.indexOf('650 mg')<0;setv('tyTaken','8');setv('tyHours','3.99');tyCheck();ok=ok&&document.getElementById('tyResult').textContent.indexOf('650 mg')<0;setv('tyHours','4');setv('tyReason','other');tyCheck();ok=ok&&document.getElementById('tyResult').textContent.indexOf('650 mg')<0;setv('tyReason','pain');tick('tyRisk',false);tyCheck();ok=ok&&document.getElementById('tyResult').textContent.indexOf('650 mg')<0;document.getElementById('__tbProbe').textContent='TYLABEL '+(ok?'OK':'BAD');"],
  "expect": ["TYLABEL OK"],
  "ref": "指定美版 325 mg 片剂标签：12 岁、过去 24 小时 8 片、间隔 4 小时及安全确认时展示；低龄、9 片、间隔不足、非适应证和未确认均拦截。"
}


,{
  "slug": "medical/dosage-calculator",
  "inputs": {"tyAge": "12"},
  "clicks": ["var noLegacy=typeof DRUGS==='undefined'&&typeof copyResult==='undefined'&&typeof __dosage_calculatorExport==='undefined'&&typeof __dosage_calculatorRender==='undefined';document.getElementById('__tbProbe').textContent='LEGACYREMOVED '+(noLegacy?'OK':'BAD');"],
  "expect": ["LEGACYREMOVED OK"],
  "ref": "原通用药品库、计算表单、历史、预设、复制及导出入口均应移除，避免使用未经核验的数据。"
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

  console.log("==== medical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
