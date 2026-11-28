# BVAS 英文预渲染标题误写为白塞病评分

## 问题

`bvas.html` 的标题区域简体原文是血管炎 BVAS 评分，预渲染英文却是“Behcet Disease Activity Score”；行业 body 字典也为该工具保存了相同英文标题。独立英文工具字典提供了正确译文，运行时可能覆盖，仍需实测不同语言及无脚本抓取结果。错误的初始正文或元信息会让英文读者及搜索引擎误认工具用途。

## 解决方案

核对该工具的 body 数据源、预渲染标题及相关 SEO 元信息，统一为 Birmingham Vasculitis Activity Score 的准确名称；核验构建后 HTML 和英文运行态，避免与白塞病活动度工具混淆。

## 受影响的工具路径

- `tools/rheumatology/bvas.html`
