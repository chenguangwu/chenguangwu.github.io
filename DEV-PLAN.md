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

### PLAN-V2 认知脑力 26 工具：已落盘，文档状态待同步
- 2026-09-05 路径核查：`tools/cognition|psychology|ophthalmology|ent|colorvision|fun` 下 T01–T26 共 **26 个路径全部 EXISTS**（实际已开发落盘）。
- 但 `PLAN-V2-BRAIN-SENSES.md` 仍标「状态：待开工」、T01–T26 全 `⬜ 待做`，文档状态滞后。
- 待办：① 补标记 26 工具完成态；② 跑 `scripts/run_gates.py` 确认全 A 级；③ 逐工具核对 i18n 八件套（en_override / slug-en / industry 三件套）是否补齐；④ 确认 T22 是否已按 PLAN 从旧 4 型 `design/color-blindness-simulator.html` 升级为 `colorvision/colorblind-simulator.html` 新版（8 型 + 图片 + WCAG + 安全色）。
- 完成收尾后该计划文档可归档删除（不长期留滞后状态文档）。

### 本次清理（2026-09-05，按老板要求）
- 删 `RESULT-INTERPRET-TODO.md`：阶段六 122 工具结果解读，全 `[x]` 完成。
- 删 `gap-report.md`：竞品(it-tools)覆盖率 100%，无缺失项。
- 删 `backlink-plan.md`：外链作战清单，无勾选待办，纯运营方案（可复跑 `scripts/gen_backlink_plan.py`）。
- 删 `PLAN-V2-BRAIN-SENSES.md`：26 工具已落盘、文档滞后，收尾项已归并上方。
- 删 `HTML-SIZE-TODO.md`：本会话大文件优化清单，已落地、执行记归档于 `.workbuddy/memory/2026-09-05.md`。
- 保留 `DEV-PLAN.md`：本文件，项目权威分批计划载体。
