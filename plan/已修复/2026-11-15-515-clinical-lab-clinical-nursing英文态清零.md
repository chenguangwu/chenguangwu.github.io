# 515 批：clinical-lab / clinical-nursing 英文态清零

- 日期：2026-11-15
- 范围：`clinical-lab` 22 页中 14 页、`clinical-nursing` 26 页中 16 页，合计 74 条键。
- 手段：只改 `i18n/tools/en/<industry>/*.json` 的 `map`；
  检验判读口径/护理评分量表/筛选与渲染规则整句英译，`请选择…` → `Select…`，
  `如 22（14–40）` → `e.g. 22 (14-40)`。
- 备注：`urine-sediment-atlas` / `parasite-egg-id` 的「含真实镜检图片」免责句按页分别改写（两页措辞不同）。
- 验收：两行业 `--check` 均残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
