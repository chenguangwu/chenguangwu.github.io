# DEV-PLAN

## 当前未完成任务

### SEO-D：长期无流量页治理（进行中）
- [进行中] 无流量页候选清单已生成（`json/seo_d_lowtraffic.json`：4320/4983 工具页无流量，按行业 it279/general154/finance94/design88…）；noindex/合并/删除动作按原要求需连续周期数据到位后执行，单期数据不立即治理。
- [保留] 禁止全站批量重写 Description，所有改动先基于页面数据和搜索意图确认。

## 数据使用边界
- Clarity 只使用聚合统计，不导出会话明细、消息、时间线或可识别个人的数据。
- 51.la 仅保留聚合指标；认证失败或站点未授权时不生成候选数据。
- 百度统计暂不纳入本轮数据源。
- 站点内容优化基于 Bing + Clarity 真实流量数据确定优先级。

## 待续 / 滚动扩面
- Analytics-C 高曝光低点击优化：首批 21 页已重写 Title/Description/H1/首段并补使用指南，Bing 数据仍稀疏（站点爬取爬升期），后续周期数据到位后再滚动扩面。

## 待核查 / 收尾（2026-09-05 清理任务文件时归并）

### PLAN-V2 认知脑力 26 工具：已落盘 + 质量验收通过（2026-09-05 21:30 核查）
- 路径核查：T01–T26 共 26 路径全部 EXISTS；`classify_quality` 实测 **26/26 全 A 级**。
- i18n 八件套数据层补齐：`i18n/tools/_en_override.json` 26/26、`i18n/tools/slug-en.json` 26/26、行业 i18n(`i18n/tools/<ind>.json`) 26/26 全覆盖（key 格式：英文数据源为 `ind/slug`，行业 i18n 为裸 `slug`）；抽查 scl90 英文 en/ed 已生成。
- 文档状态滞后已在清理时解决（`PLAN-V2-BRAIN-SENSES.md` 已删，结论归并本文件）。**PLAN-V2 收尾 ①②③ 已验证通过、无遗留。**

### T22 色盲模拟器升级收尾（已完成，方案 A，2026-09-05 执行）
- 已执行方案 A：`git rm tools/design/color-blindness-simulator.html`（旧 4 型）+ `guides/color-blindness-sim-guide.html` 硬链接改指向 `tools/colorvision/colorblind-simulator.html` + 清 5 个 i18n 旧 slug key（`design.json`/`_en_override.json`/`slug-en.json`/`design-body.json`/`content_deepdive.json`，新版对应数据已补齐不丢功能）。
- `_build.py` 重建自动清 `industry-design.json`/`tools.json`/`sitemap.xml`/`sitemap.html`/`design/index.html` 旧引用（扫描 tools/ 不再含旧文件）；A 级 **5008**（删 1 页后总数正确）。
- 五道门禁全过（含死链 `_audit_links --check`）；无头 Chrome 实机验证：design 分类页无旧链接(103 卡)、guide 页 DOM 含新版链接、colorvision 新版 h1 正常、本地资源零错误（第三方 403 已排除）。
- 注：旧 URL `tools/design/color-blindness-simulator.html` 现已 404（方案 A 不保留旧 URL 权重）；如需保已收录权重，后续可加 301 重定向桩（即方案 B）。

### SEO-D / Analytics-C（仍卡数据依赖，本次未推进）
- SEO-D：无流量页治理需连续周期 Bing+Clarity 数据到位，单期不治理（原要求保留）。
- Analytics-C：Bing 数据仍稀疏（站点爬取爬升期），等周期数据到位后再滚动扩面。

### 心理分类全量重做（2026-09-06 启动，进行中）
- 目标：把 `tools/psychology/` 全部工具统一到 `tester-2.html`(MBTI) 的「逐题作答」生产级标准：真实题库 + 逐题引擎（进度条/单题卡片/5档/题号速览回跳/键盘/本机存进度）+ 真实计分 + 深度解读；清掉所有"生理常数/常见场景：XXX"套话、链着生成器的相关工具。
- 分诊结论：仅 MBTI 已是逐题引擎；其余 19 个均为老式整页罗列。其中 PSS/PHQ-9/PSQI/SAS 核心计分正确但外壳烂；holland(72题)/bubble-tea(48题)/enneagram/bigfive/attachment(ECR)/scl90/tester-3(VARK) 有真实题库但老布局；calc-12(幸福感)/calc-self-assess(乐观)/assessor(拖延)/rater(PSQI简化)/self-assess(EQ)/analysis-2(性格色彩)/generator-20/random-12 偏薄或偏生成器。
- 顺序（一道题一道题）：①self-test-pressure(PSS) ②sas(已修计分,升逐题) ③phq9 ④psqi ⑤calc-12(幸福感) ⑥calc-self-assess(乐观) ⑦assessor(拖延) ⑧self-assess(EQ) ⑨analysis-2(性格色彩) ⑩rater(PSQI简化) ⑪tester-3(VARK) ⑫holland ⑬bigfive ⑭enneagram ⑮attachment ⑯scl90 ⑰bubble-tea ⑱generator-20 ⑲random-12。每完成一个跑 `_build.py` + `_test_static.py`，按"批量多文件合并提交"原则分批 commit。
- 改动方式：python 正则精准替换正文区块（保留 head 脚手架），避免整文件重写误伤 toolbox 桩。

### 本次清理（2026-09-05，按老板要求）
- 删 `RESULT-INTERPRET-TODO.md`：阶段六 122 工具结果解读，全 `[x]` 完成。
- 删 `gap-report.md`：竞品(it-tools)覆盖率 100%，无缺失项。
- 删 `backlink-plan.md`：外链作战清单，无勾选待办，纯运营方案（可复跑 `scripts/gen_backlink_plan.py`）。
- 删 `PLAN-V2-BRAIN-SENSES.md`：26 工具已落盘、文档滞后，收尾项已归并上方。
- 删 `HTML-SIZE-TODO.md`：本会话大文件优化清单，已落地、执行记归档于 `.workbuddy/memory/2026-09-05.md`。
- 保留 `DEV-PLAN.md`：本文件，项目权威分批计划载体。
