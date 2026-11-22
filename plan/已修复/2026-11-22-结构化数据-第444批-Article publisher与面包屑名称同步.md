# 第 444 批：指南 Article 补 publisher 并同步面包屑名称

- 日期：2026-11-22
- 类别：结构化数据 / SEO
- 状态：已修复并提交

## 一、问题

1. 可索引指南的 `Article` 全部缺 `publisher`，只有 `author` 组织；Google Article 富结果建议同时声明发布方与 logo。
2. 6 个内容集群指南的 `BreadcrumbList` 名称与可见面包屑不一致：
   - 可见「图片与视觉」／LD「图片与视觉内容集群」；
   - 可见「开发者工具」／LD「开发者工具内容集群」；
   - 可见「健康与生活」／LD「健康与生活内容集群」；
   - 其余 3 个同型。

## 二、修复

1. `sync_guide_article_ld()` 扩展：缺失 `publisher` 时写入
   `{"@type":"Organization","name":"ToolBox","logo":{"@type":"ImageObject","url":".../logo-512.png"}}`；
   已有 publisher 不改。
2. 新增 `sync_guide_breadcrumb_names()`：读取可见面包屑的链接与末项文本，逐个 BreadcrumbList 只更新 `name`，保留 `item` 与 `position`；长度不一致时不强行改名。

两者均在繁体站生成前执行，`zh-tw` 副本继承。

## 三、验证

- 可索引指南 Article：`publisher` 覆盖 **3,247 / 3,247**，`image`、`mainEntityOfPage` 同；
- 指南可见面包屑与 BreadcrumbList 名称不一致：**6 → 0**；
- JSON-LD 解析失败：**0**；
- `logo-512.png` 存在且为有效 PNG；
- `_test_static.py`：**4,626 passed / 0 failed / 0 warnings**；
- 构建 exit 0。

## 四、变更范围

- `_build.py`；
- 3,244 个指南 Article（3 页已自带 publisher，未重复写入）；
- 6 个指南 BreadcrumbList；
- `sitemap.xml`、`sitemap_lastmod.json`。

未改动工具页与可见文案（6 处仅结构化名称向可见文本对齐）。
