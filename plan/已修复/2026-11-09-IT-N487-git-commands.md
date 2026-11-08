# 第 32 批 · IT-N487 · git-commands 远程分支示例修正（攒满 5 批）

- 日期：2026-11-09
- 页面：`tools/it/git-commands.html`
- 条目：IT-N487（中，示例 fatal）
- 顺带修复：`copyCode` 异步回调缺 `btn` 守卫（任意该页用例失败时会连带让 harness 进程崩溃）
- 同批：`i18n/tools/en/it/git-commands.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、缺陷：示例命令直接 fatal

`COMMANDS` 里 `git switch` 的示例最后一条是

```
# 切换到远程分支
 git switch origin/feature
```

`switch` 只接受本地分支名，不会自动创建跟踪分支。**真实 git 仓库复现**（`git init` + 空提交 + `git update-ref refs/remotes/origin/feature HEAD`）：

| 命令 | 结果 |
|---|---|
| `git switch origin/feature` | `fatal: a branch is expected, got remote branch 'origin/feature'`，**exit 128** |
| `git switch -c feature origin/feature` | `Switched to a new branch 'feature'`，**exit 0** |
| `git switch feature`（本地已有跟踪分支） | `Already on 'feature'`，**exit 0** |
| `git switch --detach origin/feature` | `HEAD is now at …`，**exit 0** |

## 二、修复与同步

示例按清单方案改为三条完整口径：

```
# 从远程分支创建本地跟踪分支并切换
 git switch -c feature origin/feature

# 本地已有跟踪分支时直接切换
 git switch feature

# 只看远程提交（游离 HEAD）
 git switch --detach origin/feature
```

该示例整段中文是 `i18n/tools/en/it/git-commands.json` 的 **map key**，故同批删除旧 key、写入新中文 key 与对应英文译文（`# Create a local tracking branch…` / `# Switch directly when…` / `# Inspect the remote commit only…`）。`_en-i18n/patches/p05.json`、`audit-report3.json` 也含旧串，但 `_build.py` 与 `scripts/*.py` 均不引用 `_en-i18n/`，属历史审计产物，未改动。

### 顺带修：`copyCode` 异步崩溃

第 31 批把复制链路改为 `copyCode(btn, code)` 后，`navigator.clipboard.writeText(code).then(() => { const old = btn.textContent; … })` 在 **harness 兜底循环无参调用** 时 `btn` 为 undefined，Promise 回调里的 TypeError 无人捕获，会让 `verify_it_calc.js` 进程直接崩溃。本批负向对照首次执行时复现（日志尾部 `TypeError: Cannot read properties of undefined (reading 'textContent')` + `Node.js v24.11.1`，统计行没打出来）。

**危险点**：用例**通过**时 harness 在 clicks 阶段就 `return ok`，不会走兜底循环；只有**用例失败**才会触发。也就是说任何一条该页用例变红，都会连带把整个 verify 进程打崩，掩盖真实失败原因。修复：

```js
navigator.clipboard.writeText(code).then(() => {
  if(!btn) return; /* harness 无参兜底调用时 btn 缺省，避免异步回调抛错 */
  const old = btn.textContent;
  …
});
```

真机 `btn` 恒存在，行为零变化。

## 三、测试同步（`scripts/verify_it_calc.js` 新增 3 条，1272 → 1275）

| # | clicks 契约 | expect | 负向变体 |
|---|---|---|---|
| 1 | `COMMANDS.filter(c=>c.cmd==='git switch')[0].example` 含 `-c feature origin/feature` 且**不含**错误串 | `N487 fix=1` | ❌ |
| 2 | 同示例含 `git switch feature` 与 `--detach origin/feature` | `N487 full=1` | ❌ |
| 3 | 护栏：`renderCommands()` 后仍渲染 `git switch main` 且保留 `data-idx=` | `N487 render=1` | 同绿 |

clicks 沿用第 29 批经验：**无花括号**（用箭头函数 `c=>…` 代替 `function(c){…}`）；三条都是纯 clicks，快照态不执行 ⇒ 注入失败必变红。

## 四、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1275/1275 通过**。
- **负向对照采用内存变体**（不用 `git checkout HEAD`）：HEAD 是第 31 批，回退会同时丢掉本批新增的 `btn` 守卫 ⇒ 进程崩溃、统计打不全。改为从修复后页面只把 `git switch` 示例换回旧文本，其余修复（事件委托、守卫、en json）全部保留 → **1273/1275**，恰 2 行 `❌ it/git-commands`，护栏同绿，进程干净退出；恢复后 1275/1275。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 **1274 / 正确变红 1274 / 逃生 0 / 跳过 1**；`audit_verify_input_ids.js` 僵尸 id ① **0**（207 文件 / 9691 用例）；`check_expect_antipattern.py` **0** 处；`_en_i18n_probe.mjs --check` **0 残留**、`--roundtrip` **0 不一致**；页面内联脚本 `node --check` OK；`git switch origin/feature` 在页面与 en json 残留 **0**。
- **真实 git 命令复现**：见第一节表格（4 条命令全部实跑，旧命令 exit 128、新命令 exit 0）。
- jsdom 英文态：示例含新命令、不含错误命令。

## 五、未扩范围的两项（已登记，下一批处理）

1. **COMMANDS 58 条示例里的中文注释**在英文态动态渲染时仍显示中文（`--check`/`--roundtrip` 只扫静态 DOM 与默认态，不覆盖动态区）。这是第 31 批已记录的全站既有数据本地化缺口，需给 58 条加英文示例或运行时映射，本批不扩范围。
2. 覆盖清单里的**低优备注**：`git cherry-pick`（:370/:422）与 `git bisect`（:407/:424）各重复一条，使分类计数与表格总数虚增 2。删除会改变 `COMMANDS.length`（58→56）并牵动 en json 多个 key 与数量契约，留作独立批次。

## 六、清单清理与 5 批闭环

`plan/categories/01-IT开发/it.md`：精确删除 `### IT-N487 …`（标题 + 7 条子弹），覆盖清单行删掉 `IT-N487（中）；无其它高优…`、**保留未处理的低优备注**。行数 **3329 → 3319**，`grep IT-N487` 残留 **0**。

本批是上次 push 后第 **5** 个本地批次，攒满后统一执行 `_build.py` → 全站判别器 → `scripts/run_gates.py` → 提交构建产物 → push。统一 build 后需 grep 核验 5 批改动均未被覆盖：第 28 批 `%` 取模正则 / `__meL`、第 29 批 `__meReuse` / `dataset.expr` / `No Records Yet`、第 30 批 `Math.atan2(mC,dot)` / `__vcpL` / 新 formula-eq、第 31 批 `data-idx` / `copyCodeByIdx` / `__gcL`、第 32 批 `git switch -c feature origin/feature` / `if(!btn) return;`。
