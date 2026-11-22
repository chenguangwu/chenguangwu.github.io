# 第 450 批：WebApplication 补 isAccessibleForFree

- 日期：2026-11-22
- 类别：结构化数据 / SEO
- 状态：已修复并提交

## 一、问题

第 448 批移除重复 `SoftwareApplication` 后，现行 `WebApplication` 块缺少 `isAccessibleForFree`：

- 4,606 个工具页全部没有该字段；
- 而旧 `SoftwareApplication` 中 916 页曾声明 `isAccessibleForFree: true`；
- 与 `offers.price = "0"` 自相印证的信息缺失，Google 对“免费应用”的识别少一条明确信号。

## 二、修复

在 `_build.py` 的 `app_json_block` 模板中，于 `image` 之后、`offers` 之前加入：

`"isAccessibleForFree":true`

构建时按 script 块稳态重写，不新增重复块。

## 三、验证

- `WebApplication` 块：**4,606**；
- 含 `isAccessibleForFree: true`：**4,606 / 4,606**；
- `offers.price == "0"`：**4,606 / 4,606**；
- JSON-LD 解析失败：**0**；
- 连续两次构建 diff 统计一致（幂等）；
- `_test_static.py`：**4,626 passed / 0 failed / 0 warnings**；
- 构建 exit 0。

## 四、变更范围

- `_build.py`：`app_json_block` 增加字段；
- 4,606 个 `tools/**/*.html` 的 `WebApplication` JSON-LD 更新；
- 构建产物：`json/tools.json`、`sitemap.xml`、`sw.js` 等随构建更新。

未改可见文案与工具行为。
