# 第 459 批：hreflang 注入误删 head 内容修复 + 站点元数据补齐

## 问题一：hreflang 注入会清掉 marker 到 `</head>` 之间的内容（高优先级）

`inject_guide_hreflang()` 与 `inject_core_hreflang()` 先删除页面里已有的 `<link hreflang>` 和 `og:locale`，再调用 `inject_hreflang()`。删除后只剩 `<!-- TOOLBOX-HREFLANG -->` 标记、没有后续 link，`inject_hreflang()` 的整块正则匹配失败，进入兜底分支：

```python
return content[:marker_pos] + block + content[end_pos:]
```

该分支会把 marker 到第一个 `</head>` 之间的全部内容丢弃。实测被误删的有：

- `theme-color`；
- 指南的 `BreadcrumbList` 与 `FAQPage` JSON-LD；
- 同一区段内其他手工 meta。

每次构建都会重新发生，导致指南页在构建后长期缺少面包屑/FAQ 结构化数据，也让本批新增的主题色无法稳定保留。

### 修复

- 有 `I18N_HREFLANG_MARKER` 的页面直接调用 `inject_hreflang()`，由整块正则替换旧 link/locale，不再先删；
- 只有无 marker 的历史页才先清散落 link，再注入。
- 指南与核心页两处同步修复。

### 恢复

- 先 `git checkout HEAD -- guides` 恢复第 458 批提交时的指南内容；
- 重新构建，修复后的 hreflang 注入不再删内容；
- 复核指南结构化数据总量与 HEAD 一致：`BreadcrumbList` 3,247、`FAQPage` 3,241、`Article` 3,247，无丢失；
- `guides hreflang 补齐: 0 页`，重复构建不再改写。

## 问题二：站点基础元数据缺口

只读审计：

- 4,623 个带 `og:image` 的页面缺 `og:site_name`；
- 6,907 个页面缺 `theme-color`，移动端浏览器无法使用品牌色。

### 修复

`_build.py` 新增 `ensure_site_metadata()`：

- 对含 `og:image` 且缺 `og:site_name` 的页面补 `content="ToolBox"`；
- 对缺 `theme-color` 的页面补 `content="#FF6B35"`（与现有 1,172 页品牌橙一致）；
- 已有值一律不动，验证文件/无 `</head>` 的极简文件跳过；
- 分类页生成模板同步加 `theme-color`，避免每轮重建丢失；
- 繁体站随后生成时继承。

## 结果

- 构建输出：`Site metadata: og:site_name +3, theme-color +3461 in 3459 pages`（首次补齐）；
- 修复 hreflang 后再次构建：`theme-color` 仅剩验证文件/极简页 4 处计入，最终全站复核：
  - `og:site_name` 8,065/8,065 覆盖，缺失 0，重复 0；
  - `theme-color` 8,077/8,080 覆盖，缺失 3（`ByteDanceVerify.html`、`google064fa8c25a4f21e0.html`、`games/几猫国产3A大作_V1.html`，均为极简/只读非收录页）；
- 指南结构化数据：`BreadcrumbList` 3,247、`FAQPage` 3,241、`Article` 3,247，与修复前 HEAD 完全一致；
- 静态测试：4,626 passed / 0 failed / 0 warnings（4,606 个工具）；
- 死链门禁：16,743 文件 / 160,344 内链，0 死链；
- 资产完整性：0 资产死链 / 0 `lang` 缺失 / 0 重复 id；
- 内联标记位置审计：4,921 页，0 处加固片段违规；
- 全量质量门禁：268/268 passed（`GATES_EXIT=0`）。

## 变更规模

- `_build.py`：修复 2 个 hreflang 函数、新增 `ensure_site_metadata()`、分类模板加 1 行 meta；
- 全站页面新增 `og:site_name` / `theme-color`；指南与核心页恢复被误删的结构化数据。

## 备注

`core hreflang 补齐: 1 页` 是 `sitemap.html` 每次由模板重建、模板内 hreflang 无 marker 导致，输出内容稳定，不影响最终状态；后续可在模板中补 marker 消除该日志。
