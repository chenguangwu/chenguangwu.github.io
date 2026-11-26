# 第721批：JSON 转 CSV 与 CSV 转 JSON 结果清理

日期：2026-11-24

## 任务来源
- `plan/it/JSON转CSV-编辑输入后仍可导出旧数据.md`
- `plan/it/JSON转CSV-非对象元素丢失.md`
- `plan/it/JSON转CSV-导出公式保护改变负数类型.md`
- `plan/it/JSON转CSV-英文介绍错误声称支持对象.md`
- `plan/it/JSON转CSV-导出明细不是转换后的表格.md`
- `plan/it/JSON转CSV-转换失败仍可复制下载旧结果.md`（受影响页实为 `tools/it/csv-to-json.html`）

## 修复内容

### 1. 输入或选项变更后结果失效（`tools/it/json-to-csv.html`）
- 新增 `__jsonToCsvInvalidate()`，监听 `#input` 的 `input` / `change`。
- 输入变更即清空 `#output` 与 `__jsonToCsvExportSafe`，结果区提示“输入已更改，请重新点击‘转换’生成 CSV”。
- 复制 / 下载不再可能取到上一次的旧 CSV。

### 2. 非对象元素不再静默丢失（`tools/it/json-to-csv.html`）
- 转换前逐项校验：`null`、数组、数字、字符串等非对象元素直接阻止输出。
- 错误提示精确到 1 基序号与类型，例如“第 2 个元素不是 JSON 对象（数组）……”。
- 全部元素为空对象时也明确报错，不再输出 0 列表头 + 空行却提示成功。
- 空输入与解析空数组提示统一为“请输入非空 JSON 对象数组”。

### 3. 负数不再被公式保护改写成文本（`tools/it/json-to-csv.html`）
- `cellExport()` 先判断原始值为有限数字，数字（含负数）跳过单引号前缀，保持电子表格数值类型。
- 字符串仍按 `= + - @ \t \r` 前缀加单引号，公式注入防护不回退。
- 页面说明改为双语，明确“只给文本单元格加引号，JSON 数值保持数值类型”。

### 4. 简介不再声称支持单个对象（`tools/it/json-to-csv.html`、`i18n/tools/it.json`、`i18n/tools/it-body.json`）
- 中英文简介统一改为“JSON 对象数组”，不再写 “arrays or objects”。
- 修正 `i18n/tools/it-body.json` 原先的占位 intro（仅 “JSON to CSV”），与 `i18n/tools/it.json` 的 `zh-CN.intro` 同步。

### 5. 导出按钮名实相符（`tools/it/json-to-csv.html`、`js/tool-i18n-en.js`）
- “导出明细 CSV”改名为“导出历史统计 CSV”，并加提示：导出的是下方历史统计表，不是本次转换数据。
- 补英文映射 `导出历史统计 CSV → Export History Stats CSV`。

### 6. JSON→CSV 失败后清理旧结果（`tools/it/csv-to-json.html`）
- 新增 `clearJsonCsvResult()`：清空 `#csvOutput`、`csvExportSafe`、`currentData`，并把预览计数与表体重置为本地化空态。
- `jsonToCsv()` 的空输入与解析失败分支都调用清理，复制 / 下载不再残留旧 CSV。
- `#jsonInput` 输入及 `outDelimiter/outQuote/outHeader/quoteAll` 变更即触发清理。
- `clearJson()` 复用同一清理函数；预览空态按中英文分别输出。

## 验证
- `node scripts/verify_it_calc.js`：1847/1847 通过。
- 更新 3 条 JSON 转 CSV 空态断言为“请输入非空 JSON 对象数组”。
- 将一条自动补强零用例改写为真实清理回归：先成功生成 CSV，再输入非法 JSON，断言旧结果被清空。
- Puppeteer 真机：输入变更清空、非对象元素报错、空对象报错、负数导出保持数值、字符串公式仍加引号、按钮文案中英文、失败后 `csvOutput/csvExportSafe` 为空、预览空态中英文正确。
- 全量 `python3 scripts/run_gates.py`：277/277 通过。
