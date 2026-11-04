# 主工作区待集成入库清单（构建产物快照）

> 快照：2026-11-05 05:30:55（Asia/Shanghai）｜HEAD `ca856a739e`｜已跟踪变更 **125** 条（未跟踪 1 条，均为本文件自身，不计入清单）

>
> **本文件是集成线的 add 目标。** 工作区是移动靶：任何更晚的提交/编辑都会使本清单过期，
> 入库前以本文件 §0 为准，并重新跑一次 `git status --short` 核对条数。

## 0. 可直接 add 的构建产物（`git add --pathspec-from-file` 用这一段）

```text
json/industry-biz.json
json/industry-data.json
json/industry-edu.json
json/industry-electrical.json
json/industry-finance.json
json/industry-fitness.json
json/industry-food-testing.json
json/industry-groups.json
json/industry-healthcare.json
json/industry-hematology.json
json/industry-it.json
json/industry-realestate.json
json/industry-urban.json
json/tools.json
tools/biz/index.html
tools/data/index.html
tools/edu/index.html
tools/electrical/index.html
tools/finance/index.html
tools/fishery/index.html
tools/fitness/index.html
tools/food-testing/index.html
tools/healthcare/index.html
tools/hematology/index.html
tools/hr/index.html
tools/it/index.html
tools/nephrology/index.html
tools/realestate/index.html
tools/rehabilitation/index.html
index.html
sitemap.html
sitemap.xml
sw.js
```

合计 **33** 条 = json **14** + 分类索引 **15** + 根文件 **4**。
这些文件只由 `_build.py` 生成，不含任何他线源码内容。（`zh-tw/` 为 gitignore，不进 status，随构建重建。）

---

## 1. `json/*.json`（14 个，逐个列全）

```text
json/industry-biz.json
json/industry-data.json
json/industry-edu.json
json/industry-electrical.json
json/industry-finance.json
json/industry-fitness.json
json/industry-food-testing.json
json/industry-groups.json
json/industry-healthcare.json
json/industry-hematology.json
json/industry-it.json
json/industry-realestate.json
json/industry-urban.json
json/tools.json
```

## 2. 分类索引 `tools/<cat>/index.html`（15 个，逐个列全）

```text
tools/biz/index.html
tools/data/index.html
tools/edu/index.html
tools/electrical/index.html
tools/finance/index.html
tools/fishery/index.html
tools/fitness/index.html
tools/food-testing/index.html
tools/healthcare/index.html
tools/hematology/index.html
tools/hr/index.html
tools/it/index.html
tools/nephrology/index.html
tools/realestate/index.html
tools/rehabilitation/index.html
```

## 3. 工具页（80 个，逐个列全）

**为什么此前出现「101」与「79」——口径不同 + 工作区是移动靶：**
- 「101」是旧口径 `git status --short | grep -c 'tools/.*\.html'`，**把 15 个分类索引页也算进去了**，
  当时对应工具页 86 个；「79」是旧口径下「不含索引的工具页」数。
- 本快照同口径 `tools/**/*.html` = **95** = 工具页 80 + 分类索引 15；
  工具页较旧快照由 86 → 现在的 80，净变化来自并发提交与本快照前的新页诞生，
  **逐秒重建 05:1x 的历史清单已不可能**，故本文件只对当前快照负责（这也是要把清单落盘的原因）。
- 可核对的提交：`033b62b912` 收走 5 个 B 类导出页；`939f5f1adb` 的 5 个条码页 05:25 诞生、05:26 即提交，
  未进入旧快照。`47be176ff5` 提交过 `it/json-formatter.html`，但该页此刻又有未提交的 `lang=en-US` 守卫改动，
  故仍出现在 §3b —— 属 IT 线在途，不是构建派生。

**派生字段 vs 他线在途内容（判据：`git diff -U0` 每行增删是否全部命中派生字段）：**
本快照工具页 **80** 个中，「仅构建派生」**1** 个、「含他线源码改动」**79** 个。
派生字段 = `<title>` / `og:title` / `meta[name=toolbox]`（含 `icon=`）/ JSON-LD `"name"` / `bc-current` / `TOOLBOX-DEEP-DIVE` 标记；
空白行增删不计入内容。

> **§3b 与 §4b 的路径严禁按构建产物 `git add`**：它们是他线在途源码（内容、FAQ、示例、meta description、
> i18n/JS 等），必须由各自线完成并单独提交；混入构建提交会把半成品带上线。

### 3a. 仅构建派生（1 个）

```text
tools/it/xml-validator.html
```

### 3b. 含他线在途源码改动（79 个，**不得进构建提交**）

```text
tools/acupuncture/acupoint-location.html
tools/agriculture/calculator-calc-concentration.html
tools/agriculture/irrigation-uniformity.html
tools/audio/audio-recorder.html
tools/biz/text-merge.html
tools/biz/text-to-banner.html
tools/cardiology/ckd-epi.html
tools/cardiology/coronary-calcium.html
tools/cardiology/hypertension-jnc.html
tools/chess/xiangqi-endgame.html
tools/civil/slope-stability-fos.html
tools/clinical-lab/convert-39.html
tools/clinical-lab/vaginal-discharge-grading.html
tools/clinical-nursing/assessor-rater-risk.html
tools/construction/ac-size-guide.html
tools/construction/calc-1.html
tools/data/generator-35.html
tools/dermatology/vasi-vitiligo.html
tools/design/mesh-gradient.html
tools/design/pixel-art-generator.html
tools/ecommerce/analysis-cost-8.html
tools/ecommerce/report.html
tools/edu/calc-4.html
tools/edu/exam-gpa-calculator.html
tools/electrical/generator-23.html
tools/energy/conductive-heat-rate.html
tools/finance/generator-report-1.html
tools/fire-rescue/smoke-management.html
tools/fire-rescue/sprinkler-design.html
tools/fishery/calc-power.html
tools/fishery/density-1.html
tools/fishery/drug-withdrawal-fish.html
tools/fishery/estimate-23.html
tools/fishery/feed-protein-fat.html
tools/fishery/pond-desilting.html
tools/fishery/stocking-density.html
tools/fitness/generator.html
tools/food-testing/generator-27.html
tools/food/convert-concentration.html
tools/fun/coin-toss-streak.html
tools/fun/color-guess.html
tools/fun/daily-riddle.html
tools/gardening/balcony-sunlight.html
tools/healthcare/antipyretic-dose.html
tools/healthcare/egfr.html
tools/healthcare/ibw.html
tools/hematology/generator-analysis.html
tools/hr/analysis-29.html
tools/hr/annual-leave-prorate.html
tools/hr/assessor-training-hr.html
tools/hr/attendance-stats.html
tools/hr/calc-81.html
tools/it/calc-2.html
tools/it/calc-8.html
tools/it/json-formatter.html
tools/it/whitespace.html
tools/leather/xueyunhoudukongzhi.html
tools/life/generator-price.html
tools/marketing/email-subject-line-tester.html
tools/marketing/marketing-discount-rate.html
tools/nephrology/proteinuria-24h.html
tools/nutrition/generator-nutrition-label.html
tools/obstetrics/bishop-score.html
tools/obstetrics/fetal-weight-hadlock.html
tools/obstetrics/gdm-ogtt.html
tools/obstetrics/kupperman-score.html
tools/pediatrics/pediatric-anemia.html
tools/pediatrics/pediatric-asthma.html
tools/psychiatry/cdrisc-resilience.html
tools/pulmonology/anti-tb-dosing.html
tools/realestate/generator-assessor.html
tools/rehabilitation/berg-balance-scale.html
tools/rheumatology/assessor-10.html
tools/rheumatology/essdai.html
tools/tcm-pharmacy/tcm-adr-assessment.html
tools/tcm-pharmacy/tcm-dosage.html
tools/telecom/ap-coverage.html
tools/urban/building-height.html
tools/urology/iief5-score.html
```

## 4. 根文件与其他源文件（16 条）

### 4a. 根构建产物（4 个，已含在 §0）

```text
index.html
sitemap.html
sitemap.xml
sw.js
```

### 4b. 其他源文件（12 个，他线源码，**不得进构建提交**）

```text
AGENTS.md
i18n/tools/en/it/base64-converter.json
i18n/tools/en/it/json-formatter.json
i18n/tools/en/it/json-to-csv.json
i18n/tools/en/it/timestamp-converter.json
i18n/tools/en/it/token-generator.json
js/industry-info.js
js/tool-i18n-en.js
js/tool-i18n.js
plan/runtime-errors.md
scripts/audit_page_numbers.js
scripts/verify_acupuncture_calc.js
```

## 5. 记账口径（供复核）

- 本快照已跟踪变更 **125** = json 14 + 分类索引 15 + 工具页 80 + 根文件 4 + 其他源文件 12。
- 「18 个构建产物」= json 14 + 根文件 4（此前把两者合并表述，才与「14 个 json」看似矛盾）；**实际可 add 的构建产物共 33 条**（另 15 个分类索引也是构建产物）。
- 「210 个 json / 211 个工具页」是**构建写盘数**（mtime 命中），不等于 git 差异数：只有内容真变的才进 status。
