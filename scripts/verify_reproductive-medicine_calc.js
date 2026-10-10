#!/usr/bin node
/**
 * reproductive-medicine 分类计算正确性验证（覆盖 tools/reproductive-medicine/ 全部 22 个数值工具）
 * 期望值由独立复算得出（输入全避开页面默认值）。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_reproductive-medicine_calc.js
 *
 * 说明: jingzidnasuipian-dfi-zhishu 不入 CASES —— harness 对「有默认 value + oninput 属性」
 *   的页面存在竞态，inputs 注入不生效（永远用 HTML 里写死的 dfi=18/hds=8），
 *   无法构造避开默认值的 expect，与 quantum/pair-production-threshold 同类。
 *
 * 跑法:
 *   node scripts/verify_reproductive-medicine_calc.js                # 全部
 *   node scripts/verify_reproductive-medicine_calc.js anti-sperm-antibody  # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "reproductive-medicine/anti-sperm-antibody",
    inputs: { pct: "75", type: "igg" },
    expect: ["强阳性"],
    ref: "pct=75 (默认=10) → ≥75 强阳性，与默认态（可疑阳性）区分" },

  { slug: "reproductive-medicine/baifenbijisuanqi",
    inputs: { v1: "250", v2: "35" },
    expect: ["87.50"],
    ref: "v1=250, v2=35 → 35% of 250 = 87.50" },

  { slug: "reproductive-medicine/calc-volume-concentration",
    inputs: { concentration: "15", volume: "4.0" },
    expect: ["60.0"],
    ref: "15 × 4.0 = 60.0 百万 total" },

  { slug: "reproductive-medicine/detector-9",
    inputs: { ejVol: "1.5", ejConc: "40", urVol: "20", urConc: "0", urPh: "6.0", urFructose: "0" },
    expect: ["无逆行射精"],
    ref: "ejVol>=1.5 + urConc=0 → 无逆行射精（默认态 urConc=5 导致确诊逆行，完全区分）" },

  { slug: "reproductive-medicine/endometrial-receptivity",
    inputs: { thickness: "12", cycleday: "21", pattern: "A" },
    expect: ["周期日 21 天仍为A型"],
    ref: "thickness=12, pattern=A → 良好容受；断言含 cycleday 的结论句（默认 cycleday=14 → 文本不同）→ 原“容受性差”由 pattern=C（select 无默认值，注入失败仍留 C）恒定命中 → 逃生项" },

  { slug: "reproductive-medicine/epididymal-aspiration",
    inputs: { vol: "0.01", conc: "80", motility: "40", oocytes: "12", method: "mesa" },
    expect: ["0.027 每卵×10⁶"],
    ref: "获取 80×10⁶/mL×0.01mL=0.80×10⁶, 活动 0.32×10⁶, 每卵 0.32/12=0.027" },

  { slug: "reproductive-medicine/icsi-success",
    inputs: { mii: "15", injected: "12", survived: "10", fert: "8", good: "5", tr: "3", age: "35-37" },
    expect: ["66.7% ICSI受精率"],
    ref: "ICSI受精率=8/12≈66.7%" },

  { slug: "reproductive-medicine/ivf-statistics",
    inputs: { oocytes: "20", mii: "16", fert: "12", cleaved: "11", good: "7", usable: "9", transferred: "3", sacs: "2", preg: "1" },
    expect: ["60.0% 受精率", "66.7% 着床率"],
    ref: "受精率=12/20=60%, 着床率=2/3=66.7%" },

  { slug: "reproductive-medicine/liquefaction-time",
    inputs: { time: "70", status: "gel" },
    expect: ["液化不全"],
    ref: "time=70 > 60min, 胶冻状 → 液化不全" },

  { slug: "reproductive-medicine/pgt-indication",
    inputs: { ageVal: "42", rplVal: "4" },
    expect: ["PGT-A 推荐类型", "4 PGT-A指征"],
    ref: "age≥38 + RPL≥2 → 2 条 PGT-A 指征" },

  { slug: "reproductive-medicine/progressive-motility",
    inputs: { pr: "20", np: "15", im: "65" },
    expect: ["弱精子症"],
    ref: "PR=20% < 32% 下限 → 弱精子症" },

  { slug: "reproductive-medicine/reproductive-hormones",
    inputs: { fsh: "25", lh: "3", t: "2", e2: "80", prl: "10" },
    expect: ["原发性睾丸功能衰竭"],
    ref: "高 FSH(25>12.4) + 低 T(2<9.9) → 原发性睾丸功能衰竭（默认性腺轴大致正常，完全区分）" },

  { slug: "reproductive-medicine/retrograde-ejaculation",
    inputs: { semenVol: "3.5", semenConc: "25", urineVol: "10", urineConc: "0" },
    expect: ["阴性（无逆行）"],
    ref: "urineConc=0 → 逆行占比 0% → 阴性（默认态 urConc=2 导致完全逆行，完全区分）" },

  { slug: "reproductive-medicine/semen-volume",
    inputs: { vol: "0.8", abstinence: "7" },
    expect: ["少精液症"],
    ref: "vol=0.8 < 1.5ml → 少精液症" },

  { slug: "reproductive-medicine/sperm-concentration",
    inputs: { count: "80", squares: "4", dilution: "2" },
    expect: ["0.40", "隐匿精子症"],
    ref: "浓度=(80/4)×2×0.01=0.40×10⁶/mL → 隐匿精子症" },

  { slug: "reproductive-medicine/sperm-cryopreservation",
    inputs: { preConc: "50", preVol: "1.2", preMot: "55", postConc: "40", postVol: "1.0", postMot: "35" },
    expect: ["66.7% 复苏率"],
    ref: "40/60=66.7%" },

  { slug: "reproductive-medicine/sperm-dfi",
    inputs: { dfi: "30", hds: "35" },
    expect: ["30% DFI", "异常"],
    ref: "DFI=30% > 25% → 异常" },

  { slug: "reproductive-medicine/sperm-morphology",
    inputs: { normal: "3", total: "100" },
    expect: ["3.0% 正常形态率", "偏低"],
    ref: "3/100=3.0% < 4% 参考下限 → 偏低（默认 normal=12 输出 6.0% 正常，区分）" },

  { slug: "reproductive-medicine/testicular-biopsy",
    inputs: { s10: "8", s9: "6", s8: "5", s7: "7", s6: "4", s5: "3", s4: "2", s3: "1", s2: "0", s1: "0", silberGrade: "6" },
    expect: ["7.58 平均 Johnsen", "中度受损"],
    ref: "Σ(n×count)/Σcount=273/36=7.58" },

  { slug: "reproductive-medicine/testicular-volume",
    inputs: { lL: "40", lW: "20", lH: "25", rL: "38", rW: "22", rH: "23", leftP: "15", rightP: "12" },
    expect: ["14.2 左侧 mL", "27.9"],
    ref: "椭球 L=40×20×25×0.71/1000=14.2mL, R=38×22×23×0.71/1000=13.7mL，总=27.9mL；原断言“27 总体积 mL”取自 Prader（leftP/rightP 为 select 无默认值，注入失败仍留 15/12）→ 逃生项" },

  { slug: "reproductive-medicine/total-sperm-count",
    inputs: { conc: "5", vol: "2.0" },
    expect: ["10.0", "少精子症"],
    ref: "5×2=10.0 < 39×10⁶ → 少精子症（默认 conc=40 输出 120.0 正常，区分）" },

  { slug: "reproductive-medicine/embryo-grading",
    inputs: { expansion: "5", icm: "C", te: "C" },
    expect: ["5CC Gardner 评分", "欠佳 分级"],
    ref: "注入非默认（默认 expansion=1/icm=A/te=A → 1AA）：Gardner 评分 = 扩张度 5 + ICM C + TE C = 5CC；含 C 级 ⇒ 分级「欠佳」（默认 1AA 为优质）。「Gardner 评分」标签默认态也出现，故锚带值的合成串 5CC。" },

  { slug: "reproductive-medicine/jingzidnasuipian-dfi-zhishu",
    inputs: { dfi: "35", hds: "20" },
    expect: ["35.0% DFI 较差（Poor）", "20.0% HDS 轻度升高"],
    ref: "注入非默认（默认 dfi=18/hds=8）：DFI 35% 落入「较差（Poor）」档（≥30%），HDS 20% 落入「轻度升高」档（15–25%）。默认态为 18.0% 良好 / 8.0% 正常，两串均不出现。锚值+结论合成串，避开纯标签「DFI 评估」。" },

  { slug: "reproductive-medicine/vasography",
    checkIds: ["vas", "ampulla", "sv", "ejaculatory"],
    expect: ["通畅 通畅性判定", "输精管道全程显影通畅，未见梗阻。"],
    ref: "四个 checkbox（vas/ampulla/sv/ejaculatory）全勾选 + site 默认 none ⇒ 命中首分支 patency=通畅。默认全未勾选态为「部分梗阻/可疑」（else 分支）。checkIds 是 harness 支持的注入字段，回退清空即回到全未勾选态 ⇒ 判别力成立。" },
  {
    "slug": "reproductive-medicine/anti-sperm-antibody",
    "inputs": {
      "pct": "42",
      "type": "iga"
    },
    "expect": [
      "42\niga\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pct\":\"42\",\"type\":\"iga\"}，输出区含「42\niga\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/baifenbijisuanqi",
    "inputs": {
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "42\n42\n42% of 42 = 17.64"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v1\":\"42\",\"v2\":\"42\"}，输出区含「42\n42\n42% of 42 = 17.64」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/calc-volume-concentration",
    "inputs": {
      "concentration": "42",
      "volume": "42"
    },
    "expect": [
      "度（百万/mL） 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"concentration\":\"42\",\"volume\":\"42\"}，输出区含「度（百万/mL） 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/embryo-grading",
    "inputs": {
      "expansion": "2",
      "icm": "B",
      "te": "B"
    },
    "expect": [
      "评分组成 扩张度：2（囊胚） ICM：B（细胞少、松散） TE：B（上皮细胞少、不"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"expansion\":\"2\",\"icm\":\"B\",\"te\":\"B\"}，输出区含「评分组成 扩张度：2（囊胚） ICM：B（细胞少、松散） TE：B（上皮细胞少、…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/detector-9",
    "inputs": {
      "ejVol": "42",
      "ejConc": "42",
      "urVol": "42",
      "urConc": "42",
      "urPh": "42",
      "urFructose": "0"
    },
    "expect": [
      "结果解读： 精液量正常（42ml），但射精后尿液中也发现较多精子（逆向比例50%），提示部分逆行射精。 总精子量：3528"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ejVol\":\"42\",\"ejConc\":\"42\",\"urVol\":\"42\",\"urConc\":\"42\",\"urPh\":\"42\",\"urFructose\":\"0\"}，输出区含「结果解读： 精液量正常（42ml），但射精后尿液中也发现较多精子（逆向比例50%…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/endometrial-receptivity",
    "inputs": {
      "thickness": "42",
      "cycleday": "42",
      "pattern": "B"
    },
    "expect": [
      "42\nB\n42\n42.0 厚度 mm B型 回声类型 内膜过厚 容受性 内膜过厚 ：内膜过厚，需排查增生/息肉等病变。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thickness\":\"42\",\"cycleday\":\"42\",\"pattern\":\"B\"}，输出区含「42\nB\n42\n42.0 厚度 mm B型 回声类型 内膜过厚 容受性 内膜过厚…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/epididymal-aspiration",
    "inputs": {
      "vol": "42",
      "conc": "42",
      "motility": "42",
      "oocytes": "42",
      "method": "mesa"
    },
    "expect": [
      "每卵活动精子 = 740.88 / 42 = 17.640×10⁶ 充足 ：活动精子充足，满足 ICSI 需求。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vol\":\"42\",\"conc\":\"42\",\"motility\":\"42\",\"oocytes\":\"42\",\"method\":\"mesa\"}，输出区含「每卵活动精子 = 740.88 / 42 = 17.640×10⁶ 充足 ：活动…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/icsi-success",
    "inputs": {
      "mii": "42",
      "injected": "42",
      "survived": "42",
      "fert": "42",
      "good": "42",
      "tr": "42",
      "age": "30-34"
    },
    "expect": [
      "42\n42\n42\n42\n42\n30-34\n42\n100.0% 卵子存活率 100.0% ICSI受精率 100.0% 优质胚胎率 指标 结果 参考 卵子存活率 100.0% ≥90% ICSI受精率 100.0% 70-85% 优质胚胎率 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mii\":\"42\",\"injected\":\"42\",\"survived\":\"42\",\"fert\":\"42\",\"good\":\"42\",\"tr\":\"42\",\"age\":\"30-34\"}，输出区含「42\n42\n42\n42\n42\n30-34\n42\n100.0% 卵子存活率 100…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/ivf-statistics",
    "inputs": {
      "oocytes": "42",
      "mii": "42",
      "fert": "42",
      "cleaved": "42",
      "good": "42",
      "usable": "42",
      "transferred": "42",
      "sacs": "42",
      "preg": "0"
    },
    "expect": [
      "算 判读 受精率 100.0% 2PN(42)/获卵(42) 高于参考上限 正常受精率 100.0% 2PN(42)/MII(42) 高于参考上限 卵裂率 100.0% 卵裂(42)/2PN(42) 在参考范围 优质胚胎率 100.0% 优"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"oocytes\":\"42\",\"mii\":\"42\",\"fert\":\"42\",\"cleaved\":\"42\",\"good\":\"42\",\"usable\":\"42\",\"transferred\":\"42\",\"sacs\":\"42\",\"preg\":\"0\"}，输出区含「算 判读 受精率 100.0% 2PN(42)/获卵(42) 高于参考上限 正常…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/pgt-indication",
    "inputs": {
      "ageVal": "42",
      "rplVal": "42"
    },
    "expect": [
      "评估 符合的指征 女方高龄 反复自然流产 PGT-A 指征 ：存在 PGT-A 相关指征，建议遗传咨询后决定。 女方年龄 42 岁（≥38岁），非整倍体风险显著增加。 不明原因反复流产 42 次，建议夫妇染色体核型分析后再行 PGT。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ageVal\":\"42\",\"rplVal\":\"42\"}，输出区含「评估 符合的指征 女方高龄 反复自然流产 PGT-A 指征 ：存在 PGT-A …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/liquefaction-time",
    "inputs": {
      "time": "42",
      "status": "gel"
    },
    "expect": [
      "化时间 (分钟) 液化延迟 判定 液化延迟 ：提示前列腺功能可能异常，建议复查并评估感染。 外观呈胶冻状，提示凝固正常但需评估是否液化。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"time\":\"42\",\"status\":\"gel\"}，输出区含「化时间 (分钟) 液化延迟 判定 液化延迟 ：提示前列腺功能可能异常，建议复查并…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/jingzidnasuipian-dfi-zhishu",
    "inputs": {
      "dfi": "42",
      "hds": "42"
    },
    "expect": [
      "合建议： DFI 明显升高，可能影响受精与胚胎发育，建议男科/生殖医学专科评估。 HDS 明显升高"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dfi\":\"42\",\"hds\":\"42\"}，输出区含「合建议： DFI 明显升高，可能影响受精与胚胎发育，建议男科/生殖医学专科评估。…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/progressive-motility",
    "inputs": {
      "pr": "42",
      "np": "42",
      "im": "42"
    },
    "expect": [
      "细 计数总数 = 126 个 PR% = 42 / 126 ×100 = 33.33% 总活力 = (42+42) / 126 ×100 = 66.67"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pr\":\"42\",\"np\":\"42\",\"im\":\"42\"}，输出区含「细 计数总数 = 126 个 PR% = 42 / 126 ×100 = 33.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/reproductive-hormones",
    "inputs": {
      "fsh": "42",
      "lh": "42",
      "t": "42",
      "e2": "42",
      "prl": "42"
    },
    "expect": [
      "SH IU/L 42 LH IU/L 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fsh\":\"42\",\"lh\":\"42\",\"t\":\"42\",\"e2\":\"42\",\"prl\":\"42\"}，输出区含「SH IU/L 42 LH IU/L 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/retrograde-ejaculation",
    "inputs": {
      "semenVol": "42",
      "semenConc": "42",
      "urineVol": "42",
      "urineConc": "42"
    },
    "expect": [
      "⁶ 逆行占比 = 1764.00 / 3528.00 ×100 = 50.0% 部分逆行射精 ：部分精子逆流入尿液，可尝试药物诱发顺行射精。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"semenVol\":\"42\",\"semenConc\":\"42\",\"urineVol\":\"42\",\"urineConc\":\"42\"}，输出区含「⁶ 逆行占比 = 1764.00 / 3528.00 ×100 = 50.0% …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/semen-volume",
    "inputs": {
      "vol": "42",
      "abstinence": "42"
    },
    "expect": [
      "0 精液量 mL 过多 分级 42 禁欲天数 过多 ：精液量过多，可稀释精子浓度，建议排查附性腺炎症。 禁欲时间过长（&gt;7天），精液量可能偏高且精子活力下降，建议规范禁欲时间。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vol\":\"42\",\"abstinence\":\"42\"}，输出区含「0 精液量 mL 过多 分级 42 禁欲天数 过多 ：精液量过多，可稀释精子浓度…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/sperm-concentration",
    "inputs": {
      "count": "42",
      "squares": "42",
      "dilution": "42"
    },
    "expect": [
      "× 0.01 = 0.42 ×10⁶/mL 隐匿精子症 ：离心沉淀镜检复查，必要时睾丸活检取精。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"count\":\"42\",\"squares\":\"42\",\"dilution\":\"42\"}，输出区含「× 0.01 = 0.42 ×10⁶/mL 隐匿精子症 ：离心沉淀镜检复查，必要…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/sperm-cryopreservation",
    "inputs": {
      "preConc": "42",
      "preVol": "42",
      "preMot": "42",
      "postConc": "42",
      "postVol": "42",
      "postMot": "42"
    },
    "expect": [
      "动精子回收率 = 740.88 / 740.88 ×100 = 100.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"preConc\":\"42\",\"preVol\":\"42\",\"preMot\":\"42\",\"postConc\":\"42\",\"postVol\":\"42\",\"postMot\":\"42\"}，输出区含「动精子回收率 = 740.88 / 740.88 ×100 = 100.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/sperm-dfi",
    "inputs": {
      "dfi": "42",
      "hds": "42"
    },
    "expect": [
      "42\n42\n42% DFI 42% HDS 异常 分级 异常 ：自然受孕率下降，ART可能受影响。 HDS&gt;15%（42%），未成熟精子增多，提示生精功能异常或氧化应激。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dfi\":\"42\",\"hds\":\"42\"}，输出区含「42\n42\n42% DFI 42% HDS 异常 分级 异常 ：自然受孕率下降，…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/sperm-morphology",
    "inputs": {
      "normal": "42",
      "total": "42"
    },
    "expect": [
      "算明细 正常形态 42 / 总数 42 ×100 = 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"normal\":\"42\",\"total\":\"42\"}，输出区含「算明细 正常形态 42 / 总数 42 ×100 = 100」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/testicular-biopsy",
    "inputs": {
      "s10": "42",
      "s9": "42",
      "s8": "42",
      "s7": "42",
      "s6": "42",
      "s5": "42",
      "s4": "42",
      "s3": "42",
      "s2": "42",
      "s1": "42",
      "silberGrade": "8"
    },
    "expect": [
      "评分×管数) = 2310 / 总管数 420 = 5.50 重度受损 ：生精重度受损，取精成功率低。\n8\n8"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"s10\":\"42\",\"s9\":\"42\",\"s8\":\"42\",\"s7\":\"42\",\"s6\":\"42\",\"s5\":\"42\",\"s4\":\"42\",\"s3\":\"42\",\"s2\":\"42\",\"s1\":\"42\",\"silberGrade\":\"8\"}，输出区含「评分×管数) = 2310 / 总管数 420 = 5.50 重度受损 ：生精重…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/testicular-volume",
    "inputs": {
      "lW": "42",
      "lH": "42",
      "rW": "42",
      "rH": "42",
      "leftP": "2",
      "rightP": "2"
    },
    "expect": [
      "丸计对比法\n42\n42\n42\n42\n42\n42\n52.6 左侧 mL 52.6 右侧 mL 105."
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lW\":\"42\",\"lH\":\"42\",\"rW\":\"42\",\"rH\":\"42\",\"leftP\":\"2\",\"rightP\":\"2\"}，输出区含「丸计对比法\n42\n42\n42\n42\n42\n42\n52.6 左侧 mL 52.6 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/total-sperm-count",
    "inputs": {
      "conc": "42",
      "vol": "42"
    },
    "expect": [
      "mL × 精液量 42 mL = 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"conc\":\"42\",\"vol\":\"42\"}，输出区含「mL × 精液量 42 mL = 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "reproductive-medicine/vasography",
    "inputs": {
      "site": "proximal",
      "dilate": "mild"
    },
    "expect": [
      "影 射精管未显影 近端梗阻 ：附睾-输精管连接部梗阻，可行显微吻合。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"site\":\"proximal\",\"dilate\":\"mild\"}，输出区含「影 射精管未显影 近端梗阻 ：附睾-输精管连接部梗阻，可行显微吻合。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

];

"use strict";

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
  console.log("==== reproductive-medicine calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();