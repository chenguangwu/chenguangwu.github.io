# 第302批 · text-truncate chars 模式 fromEnd 忽略 wordBoundary

- 来源：`plan/categories/01-IT开发/it.md` 并行批 G 留存优化第86行。
- 缺陷：`tools/it/text-truncate.html::truncOne()` 的 chars 模式正向分支按 `wordBoundary` 在空白边界回退（保留完整词），但 `fromEnd` 分支直接 `cps.slice(cps.length - budget)`，起点常落在单词中间，把词切开，与正向不对称。
- 复现：输入 `aa bb cc dd`(11 字素)、limit=7、省略符 `...`(3) ⇒ budget=4，末 4 字素起点落在 `cc` 中间 ⇒ 旧输出 `...c dd`。

## 改动
- `tools/it/text-truncate.html`：fromEnd 分支对称应用 wordBoundary——起点若在词中间则前进到下一词首丢弃不完整词（与正向「回退丢弃不完整词」对称），保证结果不超 budget；无后续词首时保留原起点避免清空结果。
- `scripts/verify_it_calc.js`：新增强锁用例 `TRUNCEB`，精确断言输出 `...dd`（精确相等探针）。

## 验证
- verify 单 slug：旧源码 8/9（新用例红 `...c dd`）、修复后 9/9 全绿。
- 全量 verify：1706/1706 通过（EXIT=0）。
- JSDOM 真机四态：词中间+fromEnd → `...dd`（对齐词首）；已是词首 → `...d`；无空白 → `...ghij`（回退不误清空）；关闭 wordBoundary → `...c dd`（旧行为未误伤）。
- 旧源码差分：换回旧 fromEnd 后词中间场景 BAD（`...c dd`），判别成立；已恢复修好版。

## 销账
- `plan/categories/01-IT开发/it.md` 第86行改为「第302批修复销账」。
- 门禁与构建待批处理；只本地 commit，不 push。
