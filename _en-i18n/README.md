# _en-i18n（英文态专项工具目录）

本目录不是构建/门禁依赖，`_build.py` 全程跳过。2026-11-23 已清理 1,017 个一次性
`gen_*.py` / `body_*.py` / `head_*.py` 批量生成脚本与 `patches/`，避免 78MB 级历史
工作区长期占仓库体积。

保留的内容：

- `tr_engine.py`：翻译/对齐引擎，供以后新增行业批量补译文时复用。
- `probe_garble.mjs` / `probe_lang_restore.mjs` / `probe_interact.mjs`：专项验证探针。
- `scan_guide_strings.py` / `scan_prefix_garble.py` / `measure_guard.py`：扫描辅助。
- `attr-candidates.json` / `common-candidates.json` / `extra_01.json`：属性与通用短语候选。
- `industries.md`：行业进度账（当前待处理已为 0）。
- `pending/`：待译清单；为空表示无待处理。
- `work/` 与 `work_zh/`：本地缓存，不属于源码。需要时由
  `node scripts/_en_i18n_probe.mjs --extract <industry>/<slug>` 重新生成，禁止提交。

新增行业补英文时，按 `scripts/_en_i18n_probe.mjs` 头部流程执行：scan → extract →
生成字典到 `i18n/tools/en/<industry>/<slug>.json` → check → reindex → promote，
最后必须重跑 `python3 _build.py` 让字典版本戳生效。
