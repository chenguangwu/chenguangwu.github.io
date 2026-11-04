# 交互有效性扫描（第二轮：点了到底有没有用）

- 扫描时间：2026/11/4 21:31:05
- 覆盖工具页：**40**
- 有输入控件的页：**37**
- 无输入控件（纯展示/参考卡，跳过）：**3**
- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**18**
- 命中至少一类问题：**2**

> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll('input')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。

## 总览（按类型）

| 类型 | 页数 | 严重度 |
|---|---|---|
| 改了输入再点主按钮，输出完全不变（已二次复验） | **1** | 中 |
| 输入即出结果，点击按钮也不产生新结果（可能只是冗余按钮） | **1** | 低 |

## Top 50 高影响页面（按严重度加权）

| # | 页面 | 得分 | 类型 | 证据 |
|---|---|---|---|---|
| 1 | `tools/health/blood-type-calculator.html` | 2 | no_effect | 按钮「血型推算」｜构造值 fatherType [select] "A" → "B"｜改前 父亲A型 + 母亲A型 A 93.8% O 6.3% ❌ 不可能出现：B型、AB型 ⏐ 📋 复制结果⬇️ … |
| 2 | `tools/health/ibw-calculator.html` | 0.8 | button_dead_live_calc | 按钮「计算公式」｜构造值 height [number] "12" → "31"｜改前 -59.9 kg ⏐ Devine 理想体重 (IBW) → 点击后 -59.9 kg ⏐ Devine 理想体… |

## 一、按钮有效性（点了没反应 / 点了报错）

### 改了输入再点主按钮，输出完全不变（已二次复验）（1 页）

- `tools/health/blood-type-calculator.html` — 按钮「血型推算」｜构造值 fatherType [select] "A" → "B"｜改前 父亲A型 + 母亲A型 A 93.8% O 6.3% ❌ 不可能出现：B型、AB型 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 父亲A型 + 母亲A型 A 93.8% O 6.3% ❌ 不可能出现：B型、AB型 ⏐ 📋 复制结果⬇️ 导出 TXT

### 输入即出结果，点击按钮也不产生新结果（可能只是冗余按钮）（1 页）

- `tools/health/ibw-calculator.html` — 按钮「计算公式」｜构造值 height [number] "12" → "31"｜改前 -59.9 kg ⏐ Devine 理想体重 (IBW) → 点击后 -59.9 kg ⏐ Devine 理想体重 (IBW)

### 低置信度线索：导出/下载未观察到触发（5 页）

> 这些页的导出按钮 onclick 函数存在、点击也不报错，但没观察到带 download 的 `a.click()`；多为结果为空时静默 return，需人工复核，不计入缺陷数。

- `tools/health/blood-type-calculator.html` —「导出明细 CSV」（__blood_type_calculatorExport）
- `tools/health/calorie-needs.html` —「导出明细 CSV」（__calorie_needsExport）
- `tools/health/milk-tea-calories.html` —「导出明细 CSV」（__milk_tea_caloriesExport）
- `tools/health/rehab-timer.html` —「导出明细 CSV」（__rehab_timerExport）
- `tools/health/symptom-checker.html` —「导出明细 CSV」（__symptom_checkerExport）

