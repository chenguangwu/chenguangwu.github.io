# 378 设计 · cvd-safe 配色：maxmin 策略落地 + 预计算 Lab 复用（D-N107 / D-N111）

- **分类**：04-设计创意
- **工具页**：`tools/design/cvd-safe-palette.html`
- **日期**：2026-11-14
- **缺陷编号**：D-N107（中）、D-N111（低）

## 缺陷与根因

### D-N107：maxmin 策略是空实现

`generate()` 中两个分支语句完全相同：

```js
if (strat === 'lightness' || strat === 'auto') { seq = greedyQualitative(n, seeds); }
else { seq = greedyQualitative(n, seeds); }
```

`greedyQualitative` 内部恒用 `targetL` 明度邻域过滤 + 明暗交替，`maxmin` 没有任何实现分支，但界面提供该选项（下拉 + 预设"最大色差定性 6 色"），用户以为换了算法。

### D-N111：预计算的 `c.labs` 完全没用上

`CAND` 构建时已为每个候选算好 8 型模拟 + Lab（`c.labs`），但贪心评分仍调 `minDeltaAcross8(c.rgb, chosen[j].rgb)` —— 每次配对都对两边重跑 8 次 `simulate + rgbToLab`，预计算数据白占内存。除首色外，每次迭代约 1800 候选 × 已选数 × 8 类型次重复转换。

## 修复

1. **新增 `minDeltaAcrossLabs(la, lb)`**：直接吃两边的 8 型 Labs 数组算最小 ΔE2000，供贪心复用。
2. **`greedyQualitative(n, seeds, strat)`**：
   - 锁定色统一包装为 `{rgb, labs}`，评分全程走 `minDeltaAcrossLabs`；
   - `maxmin` 分支**不做明度邻域过滤**，在全体候选中取「与已选色最小 ΔE 最大」者；`lightness/auto` 保持原邻域搜索行为。
3. **`generate()`** 合并两个相同分支为 `seq = greedyQualitative(n, seeds, strat)`。

## 验证（独立复算 + 零回归对照）

该页主逻辑在 IIFE 内（`change` 监听器读 `this.value` 而 harness 的 `fire` 不绑定 this、`click()` 为空操作），策略无法在同步 stub 内驱动。按项目既有核查方式（design.md 多处以 node 内存复算判定），抽取页面纯数学函数（`M_*` / `VTYPES` / `simulate` / `rgbToLab` / `deltaE2000` / `oklchToRgb` / `buildCandidates` / `candLabs` / 贪心）做独立复算：

| 版本 | lightness 5 色 | maxmin 5 色 | 结论 |
|---|---|---|---|
| 旧实现 | `#DBBAC3,#5D0064,#EA4770,#006E1E,#BD9E00` | `#DBBAC3,#5D0064,#EA4770,#006E1E,#BD9E00` | **完全相同（空实现）** |
| 新实现 | `#DBBAC3,#5D0064,#EA4770,#006E1E,#BD9E00` | `#DBBAC3,#5D0064,#B65963,#7E4739,#EE6E91` | **产生差异（maxmin 生效）** |

关键交叉验证：**新版 lightness 输出与页面真机默认渲染逐字节一致**（verify 采集到的 `#DBBAC3 → #5D0064 → #EA4770 → #006E1E → #BD9E00`），说明 D-N111 的 Lab 预计算复用**未改变 lightness 原有行为**，属零回归重构。

- `verify_design_calc.js design/cvd-safe-palette` → **2/2 通过**（既有下拉回显用例 + 自动补强用例）。
  - 原用例 ref 中"该页色板不受模式/策略影响"的表述已随本次修复更新为"策略无法在同步 stub 内驱动"，避免文档与实现再次矛盾。
- `check_inline_js_syntax.js` → **12141** 个内联脚本语法正确。

## 影响面

仅 `tools/design/cvd-safe-palette.html` + `scripts/verify_design_calc.js` 一条 ref 文案。无 i18n / EN 字典 / 构建源变更，`_build.py` 无需重跑。
