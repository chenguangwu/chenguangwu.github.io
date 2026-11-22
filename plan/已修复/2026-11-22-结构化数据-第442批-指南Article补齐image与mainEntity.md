# 第 442 批：指南 Article 补齐 image 与 mainEntityOfPage

- 日期：2026-11-22
- 类别：结构化数据 / SEO
- 状态：已修复并提交

## 一、问题

全站 3,247 个可索引指南的 `Article` JSON-LD：

- **image 缺失 3,247/3,247（100%）**；
- `mainEntityOfPage` 缺失 592 个。

`image` 是 Google Article 富结果的推荐字段；`mainEntityOfPage` 用于明确文章主体页面。缺失不影响页面展示，但会降低结构化数据的完整度，且属于全站一致性缺口。

## 二、修复

`_build.py` 新增幂等函数 `sync_guide_article_ld()`：

- 逐个 `<script type="application/ld+json">` 解析，只处理 `@type == "Article"`；
- 缺失 `image` 时写入该页 `og:image`（回退站点 `og-image.png`）；
- 缺失 `mainEntityOfPage` 时写入 `{"@type":"WebPage","@id":<指南规范 URL>}`；
- 已有值一律不改；无变化不重写文件；
- 在 `generate_opencc_static_locales()` 之前调用，繁体副本继承后由既有生成器把 URL 改写为 `zh-tw/` 规范地址。

未对缺失的 `datePublished` / `dateModified` 做猜测填充：指南页没有可见发布日期，构建期也没有可靠的发布时间源，强行补日期会制造不实数据。

## 三、验证

- 可索引指南 Article `image` 覆盖：**3,247 / 3,247**；
- `mainEntityOfPage` 覆盖：**3,247 / 3,247**；
- JSON-LD 解析失败：**0**；
- 繁体指南 Article 字段缺失：**0**；`mainEntityOfPage @id` 已正确指向 `zh-tw/guides/...` 自身；
- `_test_static.py`：**4,626 passed / 0 failed / 0 warnings**；
- 构建 exit 0。

## 四、变更范围

- `_build.py`；
- 3,247 个 `guides/*.html` 的 Article JSON-LD；
- `sitemap.xml`、`sitemap_lastmod.json`（指南 lastmod 随内容变更更新）。

未改动工具页，未改任何可见文案。
