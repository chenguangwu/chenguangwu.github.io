# 重定向存根待删登记（TOOLBOX-REDIRECT Stubs → 保留 1 个月后删除）

> 本文件是 `AGENTS.md` §4.6 规定的**统一登记处**。所有 `TOOLBOX-REDIRECT` 迁移存根（临时过渡，最长保留 **1 个月**）必须登记于此，到期由维护者**主动删除**，**不依赖定时任务**。
>
> 维护约定：
> - 新建重定向存根的同一批次 → 在此追加一行 + 同步 `--no-verify` 提死链（见 §4.6）。
> - 到「到期日」后 → 按底部「删除 SOP」主动处理，并把状态改为「已删（commit xxx）」。
> - 每条记录删完后**保留历史行**（标「已删」），便于审计，不要整行删除。

## 字段
| 字段 | 含义 |
|------|------|
| 源 URL | 旧地址（重定向存根，到期真正 404） |
| 目标 URL | 新地址（跳转目的地） |
| 建存根日期 | 写入 `TOOLBOX-REDIRECT` 的日期 |
| 到期日 | 建存根日期 + 1 个月，须物理删除 |
| 状态 | 待删 / 已删（注明删除 commit） |
| 备注 | 繁体 zh-tw 由 CI 自动消失等 |

## 待删清单

| 源 URL | 目标 URL | 建存根日期 | 到期日 | 状态 | 备注 |
|--------|----------|-----------|--------|------|------|
| https://chenguangwu.github.io/tools/pets/pet-age-convert.html | https://chenguangwu.github.io/tools/pet/pet-age-converter.html | 2026-10-10 | 2026-11-10 | 待删 | 繁体 `zh-tw/tools/pets/pet-age-convert.html` 同规则，CI 自动消失 |
| https://chenguangwu.github.io/tools/pets/feeding-amount.html | https://chenguangwu.github.io/tools/pet/pet-feeding-calc.html | 2026-10-10 | 2026-11-10 | 待删 | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/vaccine-reminder.html | https://chenguangwu.github.io/tools/pet/reminder-vaccine-deworming.html | 2026-10-10 | 2026-11-10 | 待删 | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/grooming-guide.html | https://chenguangwu.github.io/tools/pet/grooming-guide.html | 2026-10-10 | 2026-11-10 | 待删 | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/kennel-space.html | https://chenguangwu.github.io/tools/pet/kennel-space.html | 2026-10-10 | 2026-11-10 | 待删 | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/index.html | https://chenguangwu.github.io/tools/pet/index.html | 2026-10-10 | 2026-11-10 | 待删 | 分类落地页存根；繁体同理 |

## 删除 SOP（到期执行）
1. `cd /Users/cgw/project/cgw/chenguangwu.github.io`
2. 先 grep 全站（排除 `zh-tw/`、排除 `tools/pets/` 存根自身）所有指向待删源 URL 的内部链接（`href`/`src`），改写为目标 URL 或删除，避免删除后产生内部死链（`_audit_links.py` 门禁不过）。
3. `git rm tools/pets/<file>.html …`（删空目录由 git 处理）。
4. `zh-tw/` 是 CI 构建产物，删源后自动消失，无需手动删。
5. `python3 scripts/run_gates.py` → 确认 216 项全过（存根本就被 `_test_static` 跳过，删除不应破坏门禁）。
6. 旧 URL 已是真 404，用默认校验提死链：`python3 _submit_indexnow_deadlinks.py --file _deadlinks_2026-10-10_pets.txt`（脚本自动 HTTP 校验，只交已 404 的；**不要再 `--no-verify`**）。
7. `git add -A` → `commit`（说明「删除 pets 重定向存根，旧 URL 真正 404」）→ `push origin master`。
8. 单次查询 GitHub Actions 确认部署成功（不轮询）。
9. 回本文件把对应行状态改为「已删（commit xxx）」。
