# IT-N370 / IT-N371 — matrix-inverter 奇异判据与默认矩阵

- 修复日期：2026-11-08
- 页面：`tools/it/matrix-inverter.html`
- 用例：`scripts/verify_it_calc.js`（`it/matrix-inverter` 新增 1 条；N371 因 harness 限制未进门禁，见下）

## IT-N370（中）主元用绝对阈值 `1e-12`，合法小量级矩阵被判「奇异」

**失败点**：Gauss-Jordan 选主元后 `if(Math.abs(M[piv][col])<1e-12) return {err:'矩阵不可逆（奇异矩阵）'}`，消元时也用 `Math.abs(f)<1e-12` 跳过。阈值是**绝对值**，与矩阵自身量级无关。另外 `fmt()` 把 `|x|<1e-12` 一律显示成 `0`，小量级结果被抹平。

**修复位点**（`tools/it/matrix-inverter.html`）：

```js
// 奇异性判据改为相对于矩阵自身尺度
let scale=0;
for(let i=0;i<n;i++) for(let j=0;j<n;j++){ const v=Math.abs(A[i][j]); if(v>scale) scale=v; }
const tol = scale>0 ? scale*1e-12 : 1e-12;
```

`fmt()` 改为：仅 `x===0` 写 `0`；`|x|<1e-6` 或 `|x|>=1e12` 走科学计数法（尾零剥掉，`1.000000e+13` → `1e+13`）；其余保持原 `toLocaleString()` 口径。

**证据**：`A = diag(1e-13, 1e-13)`，det = 1e-26 ≠ 0
- 修复前：`Determinant |A| = 1e-26` + `⚠️ 矩阵不可逆（奇异矩阵）`
- 修复后：`Determinant |A| = 1e-26`，`逆矩阵 A⁻¹： 1e+13 0 0 1e+13`，`验证 A × A⁻¹ = I： 1 0 0 1`

负向对照（换回修复前页面）：该用例红；`1097/1098`。

**说明**：`scale*1e-12` 而非 N370 原文建议的 `1e-12*max(1, scale)` —— 后者对 `scale<1` 的小量级矩阵退化成绝对阈值 `1e-12`，`1e-13` 依旧被判奇异，等于没修。已按「纯相对」实现并实测。

## IT-N371（中）4×4 默认矩阵只有两个对角元为 1，选中即必然「奇异」

**失败点**：`build()` 的默认值表达式是 `i===0||i===n+1||(n===3&&i===8) ? 1 : 0`。n=4 时只命中 `a0`、`a5`，后两行全 0 ⇒ det=0，选 4×4 后首屏点「计算逆矩阵」必得「矩阵不可逆（奇异矩阵）」。

**修复位点**：改为 `i%(n+1)===0 ? 1 : 0` —— n=2/3/4 恰好命中主对角线 `0, n+1, 2(n+1), …`，且 n=2/n=3 的既有默认值完全不变（0,3 / 0,4,8）。

**证据（离线 node 直跑 `build()`，比对生成 HTML 里 `id="aN" value="1"` 的格子）**：

| 尺寸 | 修复后对角为 1 的格 | 期望 |
|---|---|---|
| 2×2 | 0,3 | 0,3 |
| 3×3 | 0,4,8 | 0,4,8 |
| 4×4 | 0,5,10,15 | 0,5,10,15 |

**为什么没进门禁**：`build()` 通过 `innerHTML` 渲染 `a0..a15`，而门禁 harness 是自研最小 DOM，`innerHTML` 不解析成可 `getElementById` 的子元素 ⇒ `getM()` 读到的全是空值 0，4×4 恒 det=0，用例对修复前后都无法区分（写进去就是零判别力逃生项）。曾实测：加一条 `size=4 + build()+calculate()` 期望单位阵逆，修复后仍报 `Determinant |A| = 0`，故撤掉该用例，改用离线 node 取证，并把限制写在本档，避免后人误以为漏测。

## 判别力实测

- `env -u NODE_OPTIONS node scripts/verify_it_calc.js` → **1098/1098 通过**
- `env -u NODE_OPTIONS node scripts/discriminate_check.js verify_it_calc.js` → 已检 1097 / 变红 1097 / **逃生 0** / 跳过 1
- 负向对照：`git show HEAD:tools/it/matrix-inverter.html` 覆盖后 → 1097/1098（恰好本批那条红）；恢复后 1098/1098

新增用例判别点：`逆矩阵 A⁻¹： 1e+13 0 0 1e+13`。输入里只有 `1e-13`、量级相反，修复前该串根本不会出现（页面直接报奇异），因此既不可能是回显，也不可能是静态文案。
