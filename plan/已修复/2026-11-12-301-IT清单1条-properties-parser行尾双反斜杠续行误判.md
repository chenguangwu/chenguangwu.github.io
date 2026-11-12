# 第301批 · properties-parser 行尾双字面反斜杠被误当续行符

- 来源：`plan/categories/01-IT开发/it.md` 并行批 G 留存优化第83行（第299批同页遗留的独立子问题）。
- 缺陷：`tools/it/properties-parser.html::parseProps()` 原用 `while(t.endsWith('\\'))` 判定续行，只要行尾有反斜杠就吞掉下一行。但 `.properties` 规范中行尾连续反斜杠只有「奇数个」才表示续行（最后一个是续行符，前面成对的是字面量）；偶数个（如 `C:\\`）全是字面反斜杠，不应续行。
- 复现：`path=C:\\`(两字面反斜杠) + 换行 + `next=1` → 旧输出 `{"path":"C:\next=1"}`，`next=1` 被吞进 path 值并被当 `\n` 转义解码，丢失独立 `next` 键。

## 改动
- `tools/it/properties-parser.html`：续行判定改为统计行尾连续反斜杠个数 `bs`，`bs===0 || bs%2===0` 时 break（不续行），仅奇数个才 `slice(0,-1)` 去续行符并拼接下一行。
- `scripts/verify_it_calc.js`：新增强锁用例 `PPBS`，探针在 clicks 内构造两字面反斜杠+换行输入，断言输出含独立 `"next": "1"` 键。

## 验证
- verify 单 slug：旧源码 5/6（新用例红）、修复后 6/6 全绿。
- 全量 verify：1705/1705 通过（EXIT=0）。
- JSDOM 真机双态：偶数 `C:\\` → `{"path":"C:\\","next":"1"}`（不吞行）；奇数 `a=b\` + 换行 → `{"a":"bc=d"}`（仍正常续行，未误伤）。
- 旧源码差分：换回旧 `endsWith` 逻辑后 EVEN 场景 BAD（`C:\next=1`），判别证据成立；已恢复修好版。

## 销账
- `plan/categories/01-IT开发/it.md` 第83行改为「第301批修复销账」。
- 门禁与构建待批处理；只本地 commit，不 push。
