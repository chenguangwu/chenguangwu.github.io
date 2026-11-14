# 469 · aquaculture / audit 两行业英文态残留清零

## 问题
`--check aquaculture` 5/5 页、`--check audit` 5/5 页均有残留：
- `aquaculture`：孵化水流/溶氧、增氧机功率/面积、投喂频率/粒径、运输密度/存活率 4 个计算页的公式说明与结果模板，以及 `index` 首页全部标题/简介/FAQ（共 19 + 92 条）。
- `audit`：`ratio-analysis` 10 项比率公式、`depreciation-compare` 三法对比公式、`irr-table` 折现率扫描说明、`index` 首页（共 59 条）。

## 处理
只改源 `i18n/tools/en/aquaculture/*.json` 与 `i18n/tools/en/audit/*.json`，共 111 条：
- 公式/判定说明按变量原义英译，保留 `× ÷ − ≥` 与单位（mu、m、mg/L、kW·h）。
- 占位符「如 1.5 / 如 6 / 20」统一转 `e.g. 1.5`（正则放宽为 `^如 ([\d.]+)$`，兼容小数）。
- `index` 行业首页按既有模板英译（行业名、工具标题/描述、About、FAQ）。
- `irr-table`、`depreciation-compare` 的公式块是运行时 `_prefix` 半译形态（`判定：`→`Determination:`、`年折旧`→`yr Depreciation`），
  故以 zh 态源文（含 `判定：` / `年折旧 = …`）作键写入，覆盖半译后的残留。
- `decimal encode` 类含汉字译文（「中」等）统一改为拼音或英文描述，避免残留判定误伤。

## 验证
- `--check aquaculture`：5 页 **残留 0**。
- `--check audit`：5 页 **残留 0**。
- `python3 _build.py` 通过；`python3 _test_static.py` 4685/4685 通过。
