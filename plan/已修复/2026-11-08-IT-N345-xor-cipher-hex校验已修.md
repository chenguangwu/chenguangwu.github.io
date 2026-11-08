# IT-N345 xor-cipher hex 输入校验（已修复 · 申请复核）

- **分类**：it / 编码转换
- **原缺陷**：`parseInput('hex')` 不校验字符集与长度，`new Uint8Array(s.length/2)` 对奇数长度静默截断，`parseInt(_,16)` 遇非法字符得 `NaN` 写入类型数组变 `0`。表现：hex 输入 `zz` → 按 `0x00` 参与异或（密文=密钥字节本身）；`1`（奇数）→ 长度 0、输出空；含非法字符的串被静默转成错误字节。
- **证据（修复前）**：`tools/it/xor-cipher.html` `parseInput` hex 分支（原 :270-274），`process()` catch 仅 `alert` 不回显。
- **根因**：缺少输入预校验 + 错误不进入结果区，用户拿到看似正常却错误的密文无法察觉。
- **修复位点**：
  1. `tools/it/xor-cipher.html` `parseInput` hex 分支：去空白后先校验 `s.length % 2 === 0` 与 `/^[0-9a-fA-F]+$/`，不满足则 `throw`；
  2. `process()` catch：把错误写入 `output` 文本框（`document.getElementById('output').value = '处理失败：' + e.message`），便于结果区采集与用户可见。
- **判别力实测**：
  - 修复前：`输入 '1g' inFmt=hex` → 静默输出 `59`（1^X=0x59）；`输入 '1a2'` → 截断输出 `42`。
  - 修复后：`'1g'` → `处理失败：包含非十六进制字符`；`'1a2'` → `处理失败：十六进制长度必须为偶数（每字节两位十六进制）`；合法 `1a2b`+key `XY` → `4272`（正确）。
  - 门禁：新增 2 条 N345 回归用例（非法字符 / 奇数长度）+ 同步修正既有 xor 用例 click 为 `process()`；`verify_it_calc.js` 1072/1072 通过；`discriminate_check.js` 单文件版 1071 正确变红、0 逃生项。
- **结论**：工具逻辑修复，回归用例锁定行为；非逃生、强判别。
