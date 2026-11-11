# 第167批 · IT 清单 1 条 · properties-parser CRLF 的 \r 残留在值尾

- 来源：`plan/categories/01-IT开发/it.md` → IT-D33（问题表格行 + 逐页结论摘要已同步更新）
- 修复日期：2026-11-11
- 类型：高风险解析正确性缺陷（CRLF 文件值被污染），纯前端逻辑，无文案/口径变更

## 失败点
`tools/it/properties-parser.html` 的 `parseProps()` 用 `text.split('\n')` 切行，Windows CRLF 文本的 `\r` 残留在每行值尾：`a=b\r\nc=d\r\n` → `{"a":"b\r","c":"d\r"}`，期望 `{"a":"b","c":"d"}`。

## 根因
只按 LF 切行，未按 properties 常见跨平台换行口径处理 CRLF / 裸 CR。

## 修复位点
`parseProps()`：`text.split('\n')` → `text.split(/\r\n|\r|\n/)`，统一三种换行。续行拼接、注释跳过逻辑沿用切分后的 lines，自动受益。复用既有输出，i18n 0 残留。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增用例（CRLF 输入 `a=b\r\nc=d\r\n`，expect 锚 `"a": "b"` / `"c": "d"`）。properties-parser 4/4、it 全量 **1495/1495**。
2. **旧源码差分**：换回 `HEAD` 旧源码 → properties-parser 3/4 红（新锁失败）；恢复修好版 → 4/4 绿。判别力成立。
3. **JSDOM 真机**（`scripts/_verify_it_batch167.mjs`）：**6/6 PASS**，覆盖 CRLF、裸 CR、LF、混合换行、CRLF 续行拼接、CRLF 注释跳过。
4. **判别力**：单文件 1494 已检 / 1493 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：`audit_verify_input_ids.js` 10289 用例僵尸 id=0；`_en_i18n_probe --check it/properties-parser` 残留 0 页。

## 备注
- 本批只改源码 + verify + 清单条目（表格行+摘要）+ 真机脚本 + 本移交档；攒批后统一跑全站门禁。
