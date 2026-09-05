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

### T22 色盲模拟器升级收尾（真实待办，待老板确认方案）
- 现状：旧 4 型 `tools/design/color-blindness-simulator.html`（30KB）仍残留磁盘，且被 `tools/design/index.html`、`json/industry-design.json`、`json/tools.json` 引用，**非重定向桩**；新版 8 型 `tools/colorvision/colorblind-simulator.html`（29KB，含 wcag/CVD/安全色等 23 处特征）已就位。
- 升级未彻底：旧版未移除、引用未切换至新版。
- 收尾方案待选（均属 SEO 风险动作，需老板拍板后执行）：
  - **A**：删旧版 + 改 `design/index.html` 与 `industry-design.json` 引用指向 `colorvision` 新版 → 重跑 `run_gates.py` + 实机验证无死链。
  - **B**：旧版 301 重定向到新版（保留旧 URL 权重）。

### SEO-D / Analytics-C（仍卡数据依赖，本次未推进）
- SEO-D：无流量页治理需连续周期 Bing+Clarity 数据到位，单期不治理（原要求保留）。
- Analytics-C：Bing 数据仍稀疏（站点爬取爬升期），等周期数据到位后再滚动扩面。

### 本次清理（2026-09-05，按老板要求）
- 删 `RESULT-INTERPRET-TODO.md`：阶段六 122 工具结果解读，全 `[x]` 完成。
- 删 `gap-report.md`：竞品(it-tools)覆盖率 100%，无缺失项。
- 删 `backlink-plan.md`：外链作战清单，无勾选待办，纯运营方案（可复跑 `scripts/gen_backlink_plan.py`）。
- 删 `PLAN-V2-BRAIN-SENSES.md`：26 工具已落盘、文档滞后，收尾项已归并上方。
- 删 `HTML-SIZE-TODO.md`：本会话大文件优化清单，已落地、执行记归档于 `.workbuddy/memory/2026-09-05.md`。
- 保留 `DEV-PLAN.md`：本文件，项目权威分批计划载体。
