# IT-N367 text-similarity「比较模式」是死输入 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/text-similarity.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

`calculate()` 读出了 `compareMode` 却从未使用：差异高亮无条件走 LCS，两个选项的结果区、高亮、评分完全一致。预设里还专门为它写了值（`逐字符差异` 预设置 `compareMode:'char'`），用户以为切了比较口径，实际什么都没变。

## 修复

1. 新增 `computeDiffByPos(a, b)`：等长逐位对比，相同位置标 `same`，不同位置 A 侧 `del`、B 侧 `ins`，长度不等时多出的尾巴整段标新增/删除。
2. 差异高亮按模式选择口径：

```js
var diff = (compareMode === 'char') ? computeDiffByPos(aUnits, bUnits) : computeDiff(aUnits, bUnits);
```

`full` 保持原 LCS 对齐（能识别插入/删除造成的位移），`char` 用逐位对比（错位即整段标红）。

3. 差异区增加一行口径与计数摘要（高亮样式在纯文本里看不见，且用户也需要知道当前口径）：

```
比较口径：逐字符 · 差异合计 7 字符（A 侧 3 / B 侧 4）
比较口径：完整文本 · 差异合计 1 字符（A 侧 0 / B 侧 1）
```

4. 顺带把静态标签「差异对比（逐字符）」改为「差异对比」（口径已可变），并同步 `i18n/tools/en/it/text-similarity.json` 的映射键与英文（`Difference comparison`）。

## 判别力实测

同一对文本 `abc` vs `xabc`：

| 模式 | 差异合计 | 说明 |
|---|---|---|
| full | 1 | LCS 把 `abc` 对齐掉，只剩插入的 `x` |
| char | 7 | 3 位全部错位（A 侧 3）+ B 侧多出的首/尾（B 侧 4） |

新增两条门禁用例（同一输入、只切 `compareMode`，互为对照）：

```
expect: ["完整文本 · 差异合计 1 字符"]
expect: ["逐字符 · 差异合计 7 字符"]
```

修复前两模式输出逐字节相同、且这行摘要根本不存在 ⇒ 两条都不命中；默认 `compareMode=full` 且示例文本不同 ⇒ char 用例默认态不命中，非逃生项。

`node scripts/verify_it_calc.js` → **1085/1085 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1084 / 正确变红 1084 / 逃生 0**。
