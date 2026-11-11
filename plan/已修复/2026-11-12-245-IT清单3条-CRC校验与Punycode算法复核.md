# 第245批 · IT 清单 3 条移交复核

- 日期：2026-11-12
- 条目：IT-N55、IT-N56、IT-N57
- 涉及页：`tools/it/crc-calculator.html`、`tools/it/punycode.html`
- 状态：已修复（进批时源码已修好），本批补真机证据 + 销账，未改页面源码

## IT-N55 CRC hex 模式校验（中）· 复核已修
- 复核结论：进批时 `getInputBytes()` 已修好——去分隔符后先校验 `/^[0-9a-fA-F]+$/` 且长度为偶数，否则在结果区提示"十六进制输入须为偶数位、且仅含 0-9 / A-F"并返回 null。与备份 `/tmp/bk245` 一致，属"已修未销账"。
- 证据：JSDOM `ABC`（奇数位）与 `zz`（非法字符）均返回 null 并给明确提示；`48656C6C6F` 与带分隔符 `48 65:6C,6C;6F` 均正常解析为 5 字节 `48 65 6C 6C 6F`。

## IT-N56 Punycode RFC 3492 核心算法（高）· 复核已修
- 复核结论：进批时编解码已按 RFC 3492 修好——编码器终止位用 `digitToChar(q)`、解码器 `i += d * w` 且 `w *= BASE - t` 参与权重。与备份一致，属"已修未销账"。
- 证据：JSDOM 对 4 组样例 `中文`→`fiq228c`、`中国`→`fiqs8s`、`bücher`→`bcher-kva`、`中文abc`→`abc-u68do18h` 的编码结果与 **Node 内置 `punycode` 模块独立参考值逐组一致**，解码均还原原文。verify 相关用例全过。

## IT-N57 纯 ASCII 尾随连字符与示例（低）· 复核已修
- 复核结论：进批时已修——`encode()` 仅在存在基本码点且实际有扩展码点时处理（纯 ASCII 由 `enc()` 对无点号输入原样返回），页面示例已是 `中文.com`→`xn--fiq228c.com`、编码示例 `中文`→`xn--fiq228c`，无 `fiqs8s` 误标中文。与备份一致，属"已修未销账"。
- 证据：JSDOM ACE 勾选下 `hello`→`hello`（无尾随 `-`）、`中文.com`→`xn--fiq228c.com`、反向解码回 `中文.com`。

## 验证汇总
- 新旧源码差分：`_verify_it_batch245.mjs` 新 16/16、旧（`/tmp/bk245`）16/16——三条在备份时已全部修好，差分无差异属预期（真值由 Node punycode 独立锚定，非页面自证）。
- verify 全量：1620/1620（无功能代码变更，用例数不变）；punycode/crc 相关既有用例全过。
- 门禁：本批为门禁后第 2 批，攒 5 批后再跑完整 build + 258 gates。

## 待复核重点
- 真机（Chrome/Firefox）下 `xn--` ACE 前缀与中文域名编码是否与 Node punycode 一致。
- CRC hex 模式带各类分隔符（空格/逗号/冒号/分号/下划线/连字符）混合输入时的边界行为。
