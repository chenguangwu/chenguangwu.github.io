# ToolBox 开发计划（DEV-PLAN）

> 本文件聚焦「现状基线 + 构建门禁」。历史开发批次——Q1 工具候选池（39 个，一/二/三期各 13）、N3 指南扩容（25 篇，5 批）——均已上线完结，已从本活计划中移除归档。

---

## 一、现状基线（实测，2026-08-28）

| 指标 | 实测值 |
|---|---:|
| 索引收录工具 | 5,023 |
| 行业目录 | 276 |
| 质量分级 | A 5,023（**100%**） / B 0 / C 0 |
| 跳转桩 | 14 |
| 指南 | 149 页（含正文与 cluster 页） |
| 质量门禁 | 五道全绿 |
| CI | 已配置（`.github/workflows/quality-gates.yml`，历史全绿） |
| 搜索能力 | 汉字 / 英文 / 拼音（完整 + 首字母） |
| LICENSE | MIT（已加） |

> **历史遗留任务已清零**：命名规范化（953 编号 URL）/ 跨行业 basename 重复（104 组）因 URL 迁移 SEO 风险跳过；空壳 / 标题重复 / math 过载经实测已自然清零或前提不成立；高频工具质量打磨（30 个 B 级升 A）已完成。后续新工具严格语义化命名、避免同名。
> i18n 状态（行业英文名覆盖、翻译填充）由 i18n agent 跟踪，不在本计划范围。

---

## 二、构建与门禁命令

- 重建索引：`python3 _build.py`
- 质量门禁：`python3 scripts/run_gates.py`（需 5/5 全绿）
- 死链门禁：`python3 _audit_links.py --check`（exit 0）
- 资产门禁：`python3 _audit_assets.py --check`（exit 0）
- 英文同步：每批新增工具后必跑 `scripts/gen_en_override.py` → `_en_override.json`（标题/简介）+ 同步 `slug-en.json`（卡片）；高质量语义化英文，禁止 slug 直译
- 索引提交：不自动跑；`_build.py` 后由用户手动 `python3 _submit_indexnow.py`（定时任务由 crontab 管理）
