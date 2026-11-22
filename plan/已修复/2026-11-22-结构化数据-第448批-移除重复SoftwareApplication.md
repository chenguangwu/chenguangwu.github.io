# 第 448 批：移除同页重复 SoftwareApplication

- 日期：2026-11-22
- 类别：结构化数据 / SEO
- 状态：已修复并提交

## 一、问题

全站 5,525 个应用实体块中，919 页同时输出两个应用实体：

- `SoftwareApplication`：旧模板，`operatingSystem: "Web"`、无 `image`、`softwareVersion: "1.0"`；
- `WebApplication`：现行块，`operatingSystem: "Any"`、含 `image`、三语 `inLanguage`。

两块 `name` / `url` / `applicationCategory` 相同，Google 会视为同一页面的重复应用实体，弱化实体唯一性。

类型组合实测：`SoftwareApplication only` 0、`WebApplication only` 3,687、**两者都有 919**。

## 二、修复

在 `_build.py` 新增 `_strip_redundant_app_ld(src)`：

- 逐个 `<script type="application/ld+json">` 解析，不跨 script 匹配；
- 页面存在 `WebApplication` 时，删除所有 `SoftwareApplication` 块（含前导换行）；
- 只有 `SoftwareApplication` 的页面保持不动（当前为 0，保留该安全分支）；
- 连续空行归一，保证幂等。

调用点放在 `_replace_webapp_ld()` 与兜底注入之后，确保页面先有现行 `WebApplication`，再清理旧块。

## 三、验证

- `SoftwareApplication`：**919 → 0**；
- 每个工具页恰好 1 个 `WebApplication`，重复 **0**；
- JSON-LD 解析失败 **0**；
- 繁体工具页同样 0 个 `SoftwareApplication`、每页 1 个 `WebApplication`；
- 连续两次构建 diff 统计完全一致（幂等）；
- `_test_static.py`：**4,626 passed / 0 failed / 0 warnings**；
- 构建 exit 0。

## 四、变更范围

- `_build.py`：新增 `_strip_redundant_app_ld()` 及调用；
- 919 个 `tools/**/*.html` 删除旧 `SoftwareApplication` JSON-LD 块；
- 构建产物：`json/tools.json`、`sitemap.xml`、`sw.js` 等随构建更新。

未改任何可见文案、页面交互或工具逻辑。
