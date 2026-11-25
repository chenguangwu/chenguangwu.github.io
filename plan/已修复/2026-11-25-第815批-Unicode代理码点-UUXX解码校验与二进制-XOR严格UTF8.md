# 第815批：Unicode 代理码点 / UU、XX 解码校验与二进制 / XOR 严格 UTF-8

日期：2026-11-25

## 修复内容

### Unicode 查询（`tools/it/unicode-lookup.html`）

- 新增 `isSurrogate()`，区分 Unicode 码点与可独立编码的标量值：U+D800–U+DFFF 为代理码点。
- 详情页对代理码点不再调用 `encodeURIComponent`（避免 URIError）：UTF-8 与 URL 编码显示“不适用”，UTF-16 标注“孤立代理项，不能单独编码为标量值”，分类显示“代理项（Surrogate）”。
- `lookupName()` 对代理码点直接返回“代理码点（Surrogate）”，不再伪装成普通名称。
- 搜索卡片对代理码点显示 `\uD800` 形式，避免孤立代理项渲染成替换字符。
- `showDetail()` 增加非数字/超范围入参守卫；U+E000、U+1F600 等普通标量仍正常显示 UTF-8/URL 编码。
- 工作原理说明补充代理码点用途与编码限制。

### UU 解码（`tools/it/uuencode.html`）

- `decodeUu()` 改为逐行严格校验：长度头范围 32–95、编码字符范围、按长度头计算所需编码字符数、数据不足即报“第 N 行数据被截断”。
- 含 `begin` 头时要求出现零长度行、反引号行或 `end`，否则报“缺少结束标记”；无头数据段仍兼容，合法多行继续解析。
- 新增 `decodeInfo` 状态区：成功显示字节数/UTF-8/十六进制预览。
- 文本输出改用 `TextDecoder('utf-8',{fatal:true})`：非 UTF-8 字节不再被替换为 U+FFFD，改为十六进制预览并明确提示。
- 新增“下载原始字节”按钮，保存最近一次成功解码的 `Uint8Array` 为 `.bin`，保证二进制可逆。

### XX 解码（`tools/it/xxencode.html`）

- `decodeXx()` 同样严格校验长度字符、字符集、编码长度与终止标志；非法字符/截断数据报行号并停止，不返回部分结果。
- 文本输出严格 UTF-8；非法序列显示十六进制预览与提示。
- 新增 `decodeInfo` 状态区与“下载原始字节”按钮，二进制内容可无损保存。

### XOR 加密解密（`tools/it/xor-cipher.html`）

- 文本输出改为严格 UTF-8 解码；遇到非法字节不再静默输出 U+FFFD。
- 非法 UTF-8 时输出十六进制预览，并在 `xorInfo` 明确提示“需要完整字节请把输出格式切换为十六进制或 Base64”。
- 十六进制/Base64 输出仍逐字节保留，新增字节数与十六进制预览状态。
- 工作原理文案补充严格校验与无损输出说明。

## 验证

- 定向：`node scripts/verify_it_calc.js it/unicode-lookup it/uuencode it/xxencode it/xor-cipher` ⇒ 27/27 通过。
- 全量 IT：`node scripts/verify_it_calc.js` ⇒ 2447/2447 通过。
- 真机（Puppeteer，Chrome headless）：
  - Unicode：U+D800 详情不抛错并显示不适用；U+E000、U+1F600 正常显示 UTF-8/URL；
  - UU：`$3$` 报截断；`00 80 FF` 显示十六进制且提示非 UTF-8；
  - XX：`00 80 FF` 同样提示并保留预览；
  - XOR：`0080ff`+密钥 `a` 文本模式输出 `61 E1 9E` 并提示，十六进制模式输出 `61e19e`。
- 门禁：static 4654 通过 / 0 失败 / 0 告警；links 0 死链；assets 0 死链 / 0 lang 缺失 / 0 重复 id；marker 全部通过。
