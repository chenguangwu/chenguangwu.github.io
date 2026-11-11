# 第159批 · IT 清单 1 条 · regex-escape verbose 模式过度转义非元字符

- 来源：`plan/categories/01-IT开发/it.md` → IT-N59（已整条删除）
- 修复日期：2026-11-11
- 类型：低风险确定性源码缺陷（纯前端转义逻辑），无口径裁断

## 失败点
`tools/it/regex-escape.html` 的 `VERBOSE_META = '\\^$*+?.()|{}[]/,;:<>@#&~='` 把 `,;:<>@#&~=` 当作正则元字符加反斜杠。这些字符在 ECMAScript 正则中不是元字符：非 u/v 模式下是无害 identity escape，但带 `u`/`v` 标志时 `new RegExp('a\\=b\\,c','u')` 直接抛 `SyntaxError: Invalid escape`，导致 verbose 风味的输出无法用于严格正则。

## 根因
verbose 风味的元字符集用「尽量多转义」的粗放策略，把标点一并纳入；与真实 ECMAScript 元字符集（`. * + ? ( ) [ ] { } ^ $ | \`，另 `/` 按风味/开关处理）不一致。

## 修复位点
`tools/it/regex-escape.html:246`：删除 `,;:<>@#&~=` 七个非元字符，保留真正则元字符 + `/`；补注释说明 u/v 标志动因。未改 UI、未引入新文案（i18n 0 残留）。字符类内的 `-` 属进阶上下文处理，原实现为扁平逐字符转义，本批不做以控制风险（清单方案择其前者）。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增 1 条 it/regex-escape 用例（注入 `input="a=b,c.d", flavor="verbose"`, clicks `esc()`，expect `a=b,c\.d`）——expect 含被转义的 `.`，非纯输入回显。it 全量 1484/1484。
2. **旧源码差分**：换回 `HEAD` 旧源码 → 该用例红（4/5 通过，`❌ it/regex-escape 未匹配期望值`）；恢复修好版 → 5/5 绿。判别力成立。
3. **JSDOM 真机**（`scripts/_verify_it_batch159.mjs`）：10/10 PASS，覆盖 verbose 非元字符原样、核心元字符仍转义、混合串、u/v 标志下 `new RegExp` 合法、裸 `/` 仍转义、通用风味不变、`\`转义 `/` 回归、unesc `\x41` 回归、空输入安全。
4. **判别力**：单文件判别 1483 已检 / 1482 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：`audit_verify_input_ids.js` 10278 用例僵尸 id=0；`_en_i18n_probe --check it/regex-escape` 残留 0 页。

## 备注
- 本批只改源码 + verify + 清单条目 + 本移交档，纯 verify 侧改动不涉及构建产物字节变化；按节奏攒批后再统一跑全站门禁。
