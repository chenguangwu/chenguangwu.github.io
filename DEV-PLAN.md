# DEV-PLAN.md — 待处理任务清单

> **本文件只放「待处理任务」与「现状基线」。**
> 所有长期开发约束 / 坑 / 反模式 / harness 工作口径已收敛至 `AGENTS.md`（动工前必读）：
> - 🚫 **硬性约束**：纯前端、构建系统、URL 稳定性、单 Agent 串行、删除/迁移死链…
> - 📋 **项目特有坑与速查**：构建缓存 / 页面与 `_build.py` 交互 / i18n / 内容质量 / 无头浏览器 / verify 脚本口径 / 热度排序…
> - 📌 **开发约束补充（从本文件收敛）**：分类收口纪律、内容质量红线、verify 与判别力、批量与构建纪律、i18n 键与函数可见性、指南与复用、仓库体积维护。
>
> 已完成项、批次流水一律不写入本文件（归档走 `.workbuddy/memory/YYYY-MM-DD.md`）。
> **体积红线**：本文件 `wc -c` > 20 KB 即说明有约束/流水混入，先清理再干活。

---

## 一、待处理任务（按优先级）

### P0 · 定时到期（不可忘，到期主动执行）

- **重定向存根到期物理删除**：`_redirect_stubs_todo.md` 登记 6 个 `tools/pets/` URL（pet-age-convert / feeding-amount / vaccine-reminder / grooming-guide / kennel-space / index），建存根日期 2026-10-10，**到期日 2026-11-10**。到期动作：① 物理删除存根（简体 + 核对 zh-tw 由 CI 自动消失）→ ② commit/push → Actions success → ③ `python3 _submit_indexnow_deadlinks.py --file <死链列表.txt>`（默认校验，此时旧 URL 已真 404）→ ④ 登记表状态改「已删（commit xxx）」。

### P2 · 数据驱动 SEO（需新数据，择机执行）

- **GSC 收录数据刷新**：`_gsc_inspect_progress.json` / `_gsc_unindexed.csv` 停留 2026-08-07（6155 URL）。可择机重跑 `scripts/_gsc_inspect_urls.py`（注意 GSC API 限额，单次查询不循环），对新出现「未收录」URL 归因：低价值 / 重复 / 抓取异常 / 新 URL 未提交。
- **51.la 站点级数据定期复盘**：看 PV / 来源 / CTR 趋势，指导 title/description 精修与 `hot` 热度模型校准（URL 级接口限流 5005，逐工具真实 PV 暂不可得；如确需，另立方案如自建计数，**当前维持确定性评分模型不动**）。
- **sitemap lastmod**：随每次构建自动更新（`sitemap_lastmod.json` 为 CI 唯一真实来源），无手工事项。

### P2 · 仓库卫生（低风险）

- **`.git` 730MB（pack 619MB）压缩**：跑 `git gc --aggressive --prune=now`（不动历史、不改 commit、无 SEO 风险），预期压缩 10–20%。执行前 `git status` 确认干净，执行后 `git fsck` 校验。

### P3 · 待老板定夺（方向性，不擅自开工）

- **新工具扩充**：受纯前端红线约束（禁实时数据/位置/社交/AI 服务/第三方 API/数据库依赖类）。如有方向，走 `scripts/gen_*` 批量生成 + 中英文/指南三件套齐全（AGENTS.md「新增工具强制约束」）。
- **英文 i18n 残余全量审计**：`scripts/audit_all.mjs` 真机跑一轮，确认 `?lang=en-US` 内容区零中文残留（前三层字典机制见 AGENTS.md i18n 节）。
- **UI-OPT-PLAN.md**：209/209 分类 + 375/768/1280 三断点已收口，文件可归档；后续 UI 问题走「发现即修」模式，不再单独立项。

---

## 二、现状基线（实测，2026-10-12）

- 门禁 `scripts/run_gates.py` **217/217 全过**（含 expect anti-pattern 静态门禁）；逃生项 0；CI 最近 5 个 run 全部 success。
- 工具 **4719** 个：**A 4719 / B 0 / C 0**，A 级率 **100%**（209 分类；全站首次全部 A 级。收尾项：P1 convert 薄页 18 页提升 + `ai` 5 页 `<script type="module">` 计入 own_len 的口径修正与真实派生功能补强）。
- 分类错配迁移收官（2026-10-12）：16 个错配工具页迁入正确行业（含 fun 下火锅/烧烤/婚礼备餐等）+ 6 个跨分类重复副本转 `TOOLBOX-REDIRECT` 存根，同步修正 canonical/og:url/breadcrumb、en 字典、deepdive、lastmod、verify 用例与 tools.json industry；en 字典补 16 个历史缺键，`life` 目录 1 个错放副本清理。16+6 页探针 0 残留，门禁 217/217。
- `guides/` 3410 页，社交标签仅 1 页缺（`vaccine-reminder-guide.html` 系 pets 重定向存根，到期随存根删除，**不用修**）。
- 统计三件套已集成：百度统计 + 51.la（SDK + footer 实时挂件）+ Microsoft Clarity，统一收口 `js/analytics.js`；广告点击埋点 `js/ad_metrics.js` 六位全覆盖。
- CRITICAL_TOOL_CSS 冗余已治理（2026-09-05：引 common.css 页面零内联副本，工具页均 20KB）。
- 清理专项已收官：pet/pets 合并、design WCAG 对（color-contrast-check→contrast-checker）、it/analysis 对、5 项跨分类重复；`retire_crosscat_dupes.py` 为权威清单，非审定对不得擅并。
- `legal/calc-8`（年终奖计税）实证非缺陷，公式文案「年薪×12」→「月薪×12」已修正上线。
- 热度排序模型上线：80 个编辑精选（HOT_TOOL_URLS 原序不动）+ `compute_hot()` 确定性评分，hot 持久化 tools.json，全入口降序。
- 索引三通道（IndexNow / Bing URL API / GSC Sitemap）crontab 调度运行中（IndexNow 14:00 / Bing 15:00 / GSC 15:30 / 收录监控 16:00）。
