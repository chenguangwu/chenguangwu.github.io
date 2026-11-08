# 第 26 批 · IT-N426 · random-port-generator 文案与实现口径统一

- 日期：2026-11-08
- 页面：`tools/it/random-port-generator.html`
- 条目：IT-N426（中，承诺未实现）
- 顺带修复：英文态动态结果串 / 复制 toast 硬中文残留
- 同批：`i18n/tools/content_deepdive.json`、`scripts/apply_it.py`、`i18n/tools/en/it/random-port-generator.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、缺陷：说明承诺「49152–65535 / 未被占用」，实现是 1024–65535

`gen()` 为 `1024 + rnd[0] % (65535-1024+1)`，覆盖整个注册段 + 动态段；页面部分文案（meta / h2 / formula-eq / 结果串）在此前批次已改成 1024–65535，但仍有四处残留相反说法：

| 位置 | 修复前 | 性质 |
|---|---|---|
| `formula-desc` | 「生成未被占用的随机端口号。」 | 承诺浏览器做不到的占用检测 |
| FAQ 第 2 条 | 「本工具只是按 IANA 规定从动态/私有端口范围（49152–65535）中随机取值」 | **事实陈述错误**（实现不是这个范围） |
| deep-dive 场景 1 | 「选未占用的临时端口（建议 49152–65535）」 | 暗示工具只出动态段 |
| deep-dive 示例 | 「随机 `52341`（动态/私有端口段）」 | 同上 |

**方案选择**：清单给了两条路（统一文案 / 改实现范围）。选**统一文案为「1024–65535，不保证未被占用」**，不动实现，理由：

1. 页面 meta / h2 / formula-eq / 结果串 / 参考表均已写 1024–65535，改实现会一次性推翻多处已上线文案；
2. 「避开常用保留端口」功能依赖注册段——`RESERVED` 里的 3000 / 3306 / 5432 / 6379 / 8080 / 8443 / 9000 全在 1024–49151，若只取 49152+ 该功能形同虚设；
3. 浏览器无法探测本机端口占用是客观限制，只能如实声明，不能靠改范围伪装。

## 二、四处权威源同步（防 `_build.py` 覆盖）

`grep` 逐条定位确认：FAQ / 深度解析由 `i18n/tools/content_deepdive.json` 与 `scripts/apply_it.py`（KB）注入，`formula-desc` / `formula-eq` / 结果串只在页面 HTML。故**四个文件全部同步**，避免统一 build 后文案回退：

| 文件 | 改动 |
|---|---|
| `tools/it/random-port-generator.html` | formula-desc、FAQ、场景、示例、formula-eq 末尾补「本工具不检测端口是否被实际占用」；`__h1` 结果串补「，不保证端口未被占用」；新增 `__rpgL(zh,en)` helper；`copyOne` toast 双语 |
| `i18n/tools/content_deepdive.json` | FAQ `a`、scenarios[0]、examples[0].body 同文案替换（保持原 JSON 格式，只做字符串精确替换） |
| `scripts/apply_it.py` | `KB['it/random-port-generator']` 的 scenarios / examples 同步（该 KB 无第二条 FAQ，故只改两处） |
| `i18n/tools/en/it/random-port-generator.json` | **5 个中文原文 key 全量替换**（旧 key 删除）：formula-desc、场景、示例、FAQ、formula-eq；英文值同步改写 |

`formula-eq` 的中文原文是 i18n map 的 key，末尾加字后若不替换 key，英文态会回落中文 —— 已按第 21–25 批纪律处理。

**动态结果串双语化**（`_en_i18n_probe.mjs --check` 看不到运行时串）：中文态 `已生成 7 个随机端口（1024-65535，不保证端口未被占用）`，英文态 `Generated 7 random ports (1024-65535, no guarantee the ports are free)`；复制 toast 由「已复制端口 N」改 `Copied port N`。中文态除新增免责声明外逐字不变。

## 三、测试同步（`scripts/verify_it_calc.js` 新增 4 条，1246 → 1250）

| # | 类别 | 驱动 | expect | 修复前 |
|---|---|---|---|---|
| 1 | N426 | `skip=false, count=7, gen()` | `已生成 7 个随机端口（1024-65535，不保证端口未被占用）` | ❌ 无免责声明 |
| 2 | 护栏 | `count=20, gen()` + 范围复算 | `N426 range=oktrue n=20` | 同绿 |
| 3 | 护栏 | `count=20, gen()` + 去重统计 | `N426 uniq=20/20` | 同绿 |
| 4 | N426 | `skip=true, count=10, gen()` | `已生成 10 个随机端口（1024-65535，已避开常用保留端口，不保证端口未被占用）` | ❌ 无免责声明 |

**两个 harness 坑（本批踩过）**：

1. **stub 元素的 `innerHTML` 与 `textContent` 不联动**。初版探针先 `gen()`（写 `innerHTML`）再读 `textContent` 拼串，得到空串 ⇒ 3 条 FAIL。但 blob 本身**已直接采集 `#result` 的 innerHTML 文本**，故功能用例直接断言结果串即可，无需探针拼接；纯统计类护栏仍写独立 `textContent` 探针串。
2. **英文态 `window.TBKit` mock 在本页不生效**（`gen()` 内 helper 仍读中文态），初版 EN 用例得 `generated=0`。不在 harness 里硬凑，改由 jsdom 真机探针加载真实 `js/tool-kit.js` + `?lang=en-US` 验证；`_en_i18n_probe.mjs --check/--roundtrip` 负责静态文案。

判别力：判别器快照态不执行 `clicks`，默认 `count=5` 的结果串不含「7 个…不保证」，`1249/1249` 正确变红、逃生 0。所有 `clicks` 只用单引号，无 `\"` 转义引号 / 正则 / 注释字面量。

## 四、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1250/1250 通过**。
- **负向对照**：备份 → `git checkout HEAD -- tools/it/random-port-generator.html` → **1248/1250 通过**，恰 2 行 `❌ it/random-port-generator`（2 条功能用例变红），2 条范围/去重护栏按设计前后同绿 → 恢复后 1250/1250。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 1249 / 正确变红 1249 / **逃生 0** / 跳过 1；`audit_verify_input_ids.js` 僵尸 id ①0；`check_expect_antipattern.py` 0 处；`node --check` 页面内联脚本 OK；`content_deepdive.json` / en json 均可 `json.load`，`apply_it.py` 可 `py_compile`；`_en_i18n_probe.mjs --check` → 0 残留、`--roundtrip` → 0 不一致。
- **jsdom 真机（本批主证据）**：修复后中文态 5 项静态文案全部合规（formula-desc 不再承诺未占用、formula-eq 补声明、场景/示例/FAQ 事实改为 1024–65535）、结果串带免责声明、0 JS 异常；英文态动态串 `Generated 7 random ports (1024-65535, no guarantee the ports are free)`、0 中文残留；修复前 `git show HEAD` 页面同探针复跑，确认「生成未被占用的随机端口号」「按 IANA 规定…49152–65535」「结果串无免责声明」三项对照成立。
- 按 2026-11-07 门禁节奏，本批只跑秒级轻量项；**本批改动含构建源（`content_deepdive.json` / `apply_it.py`）与 `i18n/tools/en/**`，统一攒到 ≥5 批后跑 `_build.py`，届时需再 grep 核验 FAQ / formula-eq 未被构建覆盖回退**。

## 五、清单清理

`plan/categories/01-IT开发/it.md`：精确边界断言整条删除 `### IT-N426 …`（标题 + 6 条子弹）与覆盖清单行 ``- `random-port-generator`：IT-N426（中）；无高优缺陷…``。行数 **3389 → 3380**，`grep 'IT-N426|random-port-generator'` 残留 **0**。IT-N423 `country-code-lookup` 因缺权威 ISO 3166-1 全表仍留在清单，未标已修。
