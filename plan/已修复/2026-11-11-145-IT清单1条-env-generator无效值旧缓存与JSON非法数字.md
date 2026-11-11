# 第 145 批 · IT 分类清单 1 条移交（修复方 → 复核方）

- 来源分类：`plan/categories/01-IT开发/it.md` →「2026-11-06 IT 工具静态续审」段「环境变量预览错误保留旧复制值（中，代码确认）」
- 修复页面：`tools/it/env-generator.html`
- 性质：**确认缺陷真修**（2 个子问题同条整体修复），已完成旧源码差分自证。

## 失败点 / 缺陷

**子问题1（旧缓存）**：`generatePreview()` 在 `highlightOutput()` 结果含 `Infinity`/独立 `NaN` 时提前 return，只改 `preview.innerHTML` 显示警告，未清除 `preview.dataset.raw`。此前有效预览写入的旧配置仍留在 `dataset.raw`，`copyResult()`/`downloadResult()` 读它 → 用户看到"无效值"警告，但复制/下载的却是上一次的有效配置。

**子问题2（伪造数据）**：`generateOutput()` 的 JSON 分支对 `type==='number'` 变量执行 `Number(val)||0`，空值或非法数字（如 `abc`）被静默改成 `0`，导出 JSON 与用户输入不符。

## 根因

- 子问题1：无效值守卫的提前 return 路径遗漏了缓存字段（正常路径 L853 才写 `dataset.raw`，异常路径没有清空）。
- 子问题2：`Number(x)||0` 把 `NaN`（含解析失败的非法值）和空串都折叠成 `0`，属于「给非法值兜底成别的值」，违反"不改变用户数据"。

## 修复位点

`tools/it/env-generator.html`：
1. `generatePreview()` 两处无效值守卫（L847/L849）提前 return 前加 `preview.dataset.raw='';` → 缓存同步清空，`copyResult()` 的空串守卫接管、给出"无内容"提示，不再吐旧配置。
2. JSON 分支 number 转换（L745 附近）：改为 `_nv=Number(val)`，仅当 `String(val).trim()!=='' && isFinite(_nv)` 时转数字，否则**保留原字符串**，让非法值在导出 JSON 中可见待核对。合法数字（如 `42`）行为不变。

## 证据

- **真机脚本** `scripts/_verify_it_batch145.mjs`（JSDOM `runScripts:'dangerously'` + 自建 i18nText/ToolBox 桩 + 走真实 `addVariable()`/`deleteVar()`/`generatePreview()`/`copyResult()` 入口）：
  - 新源码 **8/8 PASS**：有效态写入 raw；无效态显示警告且 raw 清空、复制不含旧配置；JSON 非法 number `abc`→保留字符串、空值→保留空串、合法 `42`→仍转数字（防回归）。
  - **旧源码差分**：写回原始源码 → **5/8 FAIL**（`dataset.raw="…GOOD=hello"` 残留、复制吐旧配置、`BADNUM:0`/`EMPTYNUM:0` 伪造），恢复修复 → **8/8 PASS**。差分用 `/tmp` 备份恢复，未用 `git checkout --`。
- **单分类门禁**：`verify_it_calc.js` **1466/1466 通过**；`audit_verify_input_ids.js` 无报错。
- **语法自检**：`node --check scripts/_verify_it_batch145.mjs` OK。

### 为何未新增 verify 用例

缺陷发生在 `generatePreview` 的 `dataset.raw` 缓存与 JSON 导出文本，输出落在 `#previewCode`（非 verify harness 采集的结果容器），且依赖 `ToolBox`/`Blob` 桩；harness 难以稳定断言缓存清除。按纪律不硬塞弱锁，以 JSDOM 真机全链路脚本（旧红新绿已证）作为判别证据——复核判据以真机为准、不认 verify expect。

## 判别力实测

真机脚本对 5 个核心断言做 A/B：旧源码全红、新源码全绿。断言绑定具体输入值（`GOOD=hello`/`BADNUM:abc`/`EMPTYNUM`/`OKNUM:42`），非输入回显、非默认态逃生；含合法数字防回归断言，确保修复未破坏正常路径。

## 状态

本批为可独立收口的确认缺陷真修，移交复核方按真机视角复核。仅本地提交，未 push。
