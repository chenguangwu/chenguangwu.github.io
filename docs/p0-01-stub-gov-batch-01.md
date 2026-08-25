# P0-01 跳转桩治理批次 01

## 执行时间
- 2026-08-19

## 执行命令
- `python3 scripts/audit_stubs.py --dedupe-duplicates --apply`

## 审计结果
- 处理前：287 个跳转桩，`missing_target=0`，`duplicate_target_count=4`
- 处理后：287 个跳转桩，`missing_target=0`，`duplicate_target_count=0`
- 并重复类型：`to-duplicate-keeper`

## 并桶明细
- `tools/pipe/tool-020-109.html -> tools/pipe/tool-004-110.html`
- `tools/realestate/tool-014-72.html -> tools/realestate/tool-013-33.html`
- `tools/valve/tool-020-110.html -> tools/valve/tool-004-111.html`
- `tools/text/tool-012-3.html -> tools/text/tool-006-3.html`

## 产物
- 修改脚本：`scripts/audit_stubs.py`
- 变更文件：以上 4 个重复跳转桩，保留首个为入口，其他指向首个，减轻重复目标。
