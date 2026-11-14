# 493 · mining / psychiatry 英文态清零（17 页 60 条）

## 问题
- mining：吨矿成本、爆破装药、需风量、安全检查达标率、储量、运输优化、密度、品位等 10 页公式与 placeholder。
- psychiatry：C-SSRS 分层（自评/评分两页）、PHQ-9 算例、CD-RISC、ISI、LSAS、Y-BOCS 共 7 页。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 60 条。
`psychiatry/calc-1` 的算例文本被 `<a>` 链接拆开，英文片段以 "requires immediate" 收尾并与后续节点衔接。

## 验证
- mining / psychiatry 两行业 `--check` 全部 **残留 0**（36 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
