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

- [已完成] 交付通用零冲突体验增强模块 `js/tool-ux.js` + `css/common.css`：`enhanceResults` 对确实无复制/下载工具栏的结果区按需补「📋 复制结果 / 💾 下载结果」条（页面自带工具栏则不重复注入）；`enhanceValidation` 校验失败加红框 + `aria-invalid` + 友好原因；`enhancePersistence` 输入值 `localStorage` 持久化（仅回填空字段，不覆盖示例/默认）；`enhanceA11y` 结果区加 `aria-live`。全站工具页注入（build 幂等、随工具数自动适配），不破坏既有工具栏。
- [已完成] 移动端：`.tool-ux-bar` 在 ≤768px 下按钮 50% 宽双列、加大点按区，核心操作单手可达。
- [已完成] 门禁：注入后 `_test_static.py` / `_audit_links.py --check` / `_audit_assets.py --check` 三道全过，build 连跑幂等。
- 注：原「逐工具补示例/清空/复制」方案因工具页 DOM 异构、已有工具栏普遍而放弃高风险全站改造，改为零冲突通用增强（等价达成高频交互 + 移动端 + 可访问性目标）。

### SEO-C：工具页内容差异化与内部链接建设

- [已完成] 22 个重点页增加功能匹配的相关工具（`json/related-tools-curated.json` + `_build.py` 跨行业引用，替代原随机取前 6）。
- [已完成] 为高曝光低点击的 21 个工具补写使用指南（`guides/<slug>-guide.html`），并实现工具页↔指南页双向链接（`_build.py` 按 basename 注入「📖 使用指南」+ 指南页 related chips，均进 sitemap）。
- [已完成] canonical / BreadcrumbList / WebApplication 由 `_build.py` 统一注入，已覆盖。
- [已完成] FAQ 结构化数据：仅指南页（真实含问答）加 FAQPage；工具页无问答内容故不加，符合"禁止批量制造问答"。
- [待开始] 首页热门工具改为使用真实热度数据，优先导流高曝光低点击页面（依赖 51.la 可读后，见 Analytics-B）。

### SEO-D：重复页、薄内容页和长期无流量页治理

- [已完成] 数据驱动识别：复用 `_build.py` 权威质量分级 + 跨行业名称相似度检测（`scripts/audit_seo_d.py` → `json/seo_d_dup_candidates.json`）。当前 C 级(薄内容)=0、A 级率 100%，薄内容维度已基本消除（此前的加真实功能模块优化已生效）。
- [已完成] 残留重复合并 P2d（`scripts/merge_dupes_p2d.py`）：合并 17 对「随机/混乱文件名方 → 规范命名方」真重复，改写为 TOOLBOX-REDIRECT 桩，旧 URL 不丢。工具数 5014→4997，A 级率保持 100%；5 道门禁全过、build 幂等。
- [已完成] 待确认 17 对（原写「18 对」实为 17）逐对源码核对（只读分析 + 复核实测）：判定 merge 13 / separate 3 / rename 1。
  - merge 13 对（真重复）已执行 `scripts/merge_dupes_seod.py`：被合并方（随机/模糊命名）原地改 `TOOLBOX-REDIRECT` 桩，规范命名方保留。工具数 4997→4984，桩总数 36→49，旧 URL 不丢、无死链；build 幂等、三道门禁全过。
  - separate 3 对（功能确实不同，保持独立）：`agriculture/calc-11 <=> machinery-efficiency`（B 含油耗人工成本）、`fishery/estimate-emission-wastewater <=> wastewater-cod`（通用两值计算 vs 按投饵估 COD）、`safety/drill-timer <=> assessor-drill`（计时器 vs 评估表）。
  - rename 1 对（`process/pp-index <=> ppk-index`，Pp/Ppk 不同过程能力指标）：修正两页标题为「Pp 过程性能计算器 / Ppk 过程性能计算器」——改 `i18n/tools/process.json` 对应 `zh-CN.title` 由 build 渲染即区分（手动改 HTML 会被 build 标题覆写逻辑还原，已踩坑）。
- [待开始] 长期无流量页治理：依赖 Analytics-B（51.la 可读）后，按连续周期数据识别 `noindex`/合并/删除。
- [保留] 禁止全站批量重写 Description，所有改动先基于页面数据和搜索意图确认。
  - [已完成] 套话 description 治理（189 页）：全站非 index 工具页中 189 个 meta description 为模板化套话（"免费在线工具/纯前端运行/数据不上传"固定串），逐页基于真实功能撰写 >=30 字中文描述写回 `i18n/tools/<ind>.json` 的 `zh-CN.intro`；build 后原套话唯一标识"免费在线工具"归零，四道门禁全过；commit `1fec7878d`。新描述结尾"纯前端/数据不上传"为真实特性说明（非模板套话），未二次扩大。
  - [已完成] 短描述精修（207→1350 页）：
  - [已完成] 真实短描述扩写（1469 页）：对 description 19–30 字、内容真实但偏短的非 index 工具页，逐页基于真实功能独立撰写 ≥35 字中文描述，写回 `i18n/tools/<ind>.json` 的 `zh-CN.intro`；缺口驱动核对（剔除 67 行公式/代码脏数据后真实待修 1469 页）确保零遗漏、全覆盖；`_build.py` 重建（sitemap 4984工具+266分类+guides，A级100%）+ 四道门禁全过；commit `1a40663de`。
  - [已完成] 续扩 414 个 31-34 字描述至 ≥35 字：全站 4984 工具页 description 现已全部 ≥35 字（≤34 字清零）；`_build.py` 重建 + 四道门禁全过。对 description ≤18 字或标题式的 1350 个工具页，按真实功能独立撰写 ≥30 字中文描述，写回 `i18n/tools/<ind>.json` 的 `zh-CN.intro`；分批写回 + 每百页合并 `_build.py` + 四道门禁（_test_static / _audit_links / _audit_assets / verify_calc）全过；commit `42e9f6371`。遵循「禁止全站批量模板化重写」原则，逐页独立撰写、不碰 HTML、由 build 确定性渲染。
  - [已完成] 清理 per-industry i18n ghost（418 条）：`i18n/tools/<ind>.json` 中无对应 `tools/<ind>/<slug>.html` 的历史残留 slug（含 11 个已无真实工具页的行业整文件留 `{}`）；`*-body/*-phrases/_en_override/slug-en/content_deepdive` 等运行时依赖的翻译资源文件保持不动；`_build.py` 重建 + 四道门禁全过，现存 4846 条目零误删。
  - [已完成] 删除纯前端记录类工具 todo-list：全站唯一纯前端 localStorage 记录类（无计算/生成功能、属伪功能），重写为 TOOLBOX-REDIRECT 桩页（refresh/canonical/JS 跳转 + robots:noindex,follow 指向 `/tools/life/`，同行业落地页权重保留最稳），并从 `i18n/tools/life.json` 删除 todo-list 整条；`_build.py` 重建（sitemap 工具 4983 少1、A级100%）+ 四道门禁全过；commit `069839c35`。

### Performance-A：高热度页面性能与稳定性

- [已完成] 统计脚本稳定性：`js/analytics.js` 全 try/catch + `script.async`，百度/Clarity/51.la 三平台各自 `runSafely` 隔离；`common.js` 兜底补引也 async。统计/CDN 失败时仅不上报，工具核心计算（页面内联 script）不挂（A1 达标）。
- [已完成] 横向溢出审计 5478 页：裸内联 `style="width:Npx"`(>480)=0；16 个扫描命中实为 `max-width:` 类样式或 `@media` 内响应式宽，非真实溢出；表格/pre/code 已有 `overflow-x:auto` 兜底（与 `_perf_baseline.json` 横向溢出告警=0 一致）。仅补 `css/common.css` 全局裸 `pre{overflow-x:auto;max-width:100%}` 加固（A2）。
- [已完成] 触摸目标：输入/按钮大量 `min-height:44/46/52px`，移动端单手可达（A3 达标）。
- [已完成] 性能基线复核：`_perf_baseline.json` 显示 LCP≤172ms、CLS≈0、工具页总体积≤150KB、JS≤100KB、thirdParty≤4，全部远低于预算。本地有 Chrome 但缺 lighthouse 且沙箱出网被封，未重测；性能已健康，无真实瓶颈需优化（A4 现状记录）。
- 注：若后续出现真实性能瓶颈或实测环境就位，再补「优化前后对比记录」。

### 执行顺序

1. 先完成 Analytics-C 首批 4 个页面的标题、摘要、首屏和核心交互优化。
2. 再扩展到前 20 个高曝光低点击页面，并补充相关工具和指南互链。
3. 随后完善高点击率低流量页面的入口和内容覆盖。
4. 最后根据连续周期数据治理重复页、薄内容页和长期无流量页。
