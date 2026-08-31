# DEV-PLAN

## 当前未完成任务

### Analytics-B：补齐可用的站点流量数据

- [阻塞] 51.la 低安全性鉴权已打通，但最近访问明细接口返回 `5005` 鉴权失败；需要在 51.la 控制台为 API 应用开通访问明细/页面分析权限后，才能提取 URL 并参与合并。
- [已完成] Microsoft Clarity 聚合导出已生成，结果文件为 `clarity_traffic_export.csv`。
- [已完成] Bing Webmaster 查询与页面统计已生成，结果文件为 `bing_traffic_export.csv`，共 156 条查询、57 条页面记录。
- [已完成] Bing 与 Clarity 已合并为 `analytics_traffic_merged.csv`，每行带有 `source` 和统一分析字段。
- [已完成] 合并数据过滤规则已加入：移除 `evernode/`、`localhost`、`127.0.0.1` 页面及当前项目中已不存在的页面。
- [已完成] 最终结果按 URL 去重聚合，汇总展示/点击并按热度排序，每个 URL 只保留一行。
- [已完成] 站点级 51.la 概览已从 URL 合并结果中移除，不再用于页面热度分析；待取得访问 URL 明细后再接入。
- [已完成] 51.la Open API 拉取脚本已加入 `scripts/fetch_51la_overview.py`，支持低安全性 `LA_ACCESS_KEY` 和高安全性 `LA_SECRET_KEY`，密钥不写入仓库。
- 百度统计暂不纳入本轮数据源。

## 数据使用边界

- Clarity 只使用聚合统计，不导出会话明细、消息、时间线或可识别个人的数据。
- 51.la 仅保留聚合指标；认证失败或站点未授权时不生成候选数据。
- 站点内容优化需等 51.la 数据可读后，再结合 Clarity 结果确定优先级。

## 下一阶段：基于流量数据的功能、体验与 SEO 优化

### Analytics-C：高曝光低点击工具页优化

- [已完成] 从分来源数据（`analytics_traffic_by_source.csv`）筛选 Bing 展示高、点击 0 的页面（Bing 与 Clarity 口径不同，已分开统计，见 `scripts/analytics_by_source.py`）。
- [已完成] 首批 4 页（id-card-generator / video-speed / sample-size-calculator / lottery-odds-calculator）重写 Title/Description/H1/首段，消除模板化。
- [已完成] 扩展至 21 个高曝光低点击页补写真实中文描述；并修复 `_build.py` 提取 description 被 JS 校验串污染的系统性 bug（33 页）+ 273 页 meta 多余尖括号导致 `<head>` 提前闭合。
- [已完成] 相关工具与指南互链见 SEO-C。
- 注：Bing 数据仍稀疏（站点爬取爬升期），后续周期数据到位后再滚动扩面。

### UX-A：高热度工具功能与移动端体验升级

- [待开始] 统一补充示例输入、一键填入示例、清空、复制、下载和恢复默认值。
- [待开始] 优化输入校验，展示具体错误原因和错误位置，避免只提示“格式错误”。
- [待开始] 为计算器、生成器、校验器、转换器和文本工具分别补齐对应的高频交互能力。
- [待开始] 使用 `localStorage` 保存最近一次非敏感输入，提升重复使用效率。
- [待开始] 优化移动端首屏、按钮尺寸、结果反馈和底部主要操作区，确保核心功能单手可用。
- [待开始] 补齐可见 label、键盘操作、焦点状态和屏幕阅读器可理解的提示。

### SEO-C：工具页内容差异化与内部链接建设

- [已完成] 22 个重点页增加功能匹配的相关工具（`json/related-tools-curated.json` + `_build.py` 跨行业引用，替代原随机取前 6）。
- [已完成] 为高曝光低点击的 21 个工具补写使用指南（`guides/<slug>-guide.html`），并实现工具页↔指南页双向链接（`_build.py` 按 basename 注入「📖 使用指南」+ 指南页 related chips，均进 sitemap）。
- [已完成] canonical / BreadcrumbList / WebApplication 由 `_build.py` 统一注入，已覆盖。
- [已完成] FAQ 结构化数据：仅指南页（真实含问答）加 FAQPage；工具页无问答内容故不加，符合"禁止批量制造问答"。
- [待开始] 首页热门工具改为使用真实热度数据，优先导流高曝光低点击页面（依赖 51.la 可读后，见 Analytics-B）。

### SEO-D：重复页、薄内容页和长期无流量页治理

- [已完成] 数据驱动识别：复用 `_build.py` 权威质量分级 + 跨行业名称相似度检测（`scripts/audit_seo_d.py` → `json/seo_d_dup_candidates.json`）。当前 C 级(薄内容)=0、A 级率 100%，薄内容维度已基本消除（此前的加真实功能模块优化已生效）。
- [已完成] 残留重复合并 P2d（`scripts/merge_dupes_p2d.py`）：合并 17 对「随机/混乱文件名方 → 规范命名方」真重复，改写为 TOOLBOX-REDIRECT 桩，旧 URL 不丢。工具数 5014→4997，A 级率保持 100%；5 道门禁全过、build 幂等。
- [待确认] 另有 18 对（35 高置信中减 17）需人工逐对确认是否真重复，不擅自合并：
  - 功能可能不同（不合并）：`agriculture/calc-11 <=> machinery-efficiency`（对比 vs 成本）、`encode/utf-8 <=> utf8-bytes`（编码 vs 字节）、`construction/estimate-area-dosage-1 <=> soundproof-material`（面积剂量 vs 隔音）。
  - 实为命名 Bug 非重复：`process/pp-index <=> ppk-index`（Pp 与 Ppk 不同指标，应改标题而非合并）。
  - 双方均规范命名、仅差后缀（待确认）：`food-testing/rater-risk <=> allergen-cross-risk`、`fishery/estimate-emission-wastewater <=> wastewater-cod`、`safety/drill-timer <=> assessor-drill`、`it/git-cheatsheet <=> git-commands`、`pet/pet-food <=> pet-feeding-calc`、`design/color-scheme-generator <=> color-palette`、`energy/calculator-calc-power <=> standby-power-calculator`、`it/sn-generator <=> serial-key-generator`、`energy/calc-area-air <=> air-purifier-area`、`meteorology/beaufort-scale <=> wind-beaufort`、`hydraulic/estimate-18 <=> calc-54`、`construction/estimate-volume-load <=> radiator-calculator`、`legal/estimate-accident <=> traffic-accident-compensation`。
- [待开始] 长期无流量页治理：依赖 Analytics-B（51.la 可读）后，按连续周期数据识别 `noindex`/合并/删除。
- [保留] 禁止全站批量重写 Description，所有改动先基于页面数据和搜索意图确认。

### Performance-A：高热度页面性能与稳定性

- [待开始] 检查重点页面首屏脚本、重复 CSS、图片尺寸和第三方统计加载情况。
- [待开始] 保证统计脚本失败、网络异常或 CDN 不可用时，工具核心功能仍可正常使用。
- [待开始] 修复移动端横向溢出、结果区域跳动和输入控件尺寸不足问题。
- [待开始] 建立优化前后的页面加载、交互完成率和点击率对比记录。

### 执行顺序

1. 先完成 Analytics-C 首批 4 个页面的标题、摘要、首屏和核心交互优化。
2. 再扩展到前 20 个高曝光低点击页面，并补充相关工具和指南互链。
3. 随后完善高点击率低流量页面的入口和内容覆盖。
4. 最后根据连续周期数据治理重复页、薄内容页和长期无流量页。
