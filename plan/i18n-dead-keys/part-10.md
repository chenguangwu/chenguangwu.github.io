## 第三批：`data` + `electrical`（2026-11-05）

> 白名单：仅 `i18n/tools/en/data/**`、`i18n/tools/en/electrical/**`；未跑 `_build.py`、未 push。

### 口径与核实

- **弃用纯静态判死**：源码缺失 ≠ 运行时不用（动态文本可由 JS 拼出）。本批对每个静态候选做**运行时标记法复核**——临时把候选键值改为 `@@MKn@@` 加载 `?lang=en-US`，读 `document.body.textContent` + `input/textarea` 的 `placeholder/value` + `title/aria-label/alt` + `data-zh/data-i18n` 属性；**标记未出现才判死**。
- 候选 37 条（data 19 / electrical 18），其中 **3 条被运行时读取，保留**：`data/xml-html-css-geshihua-yiyou-kebuchong` 的 `如 2（1–8）`、`data/yaml-json` 的 `| 保留换行，> 折叠换行`、`electrical/generator-23` 的 1 条。
- 本批未触碰 `i18n/tools/data-body.json` / `electrical-body.json`（无必要改动）。

### 结果

| 目录 | 词典页 | 键总数（改前） | 删死键 | 补/修半译键 | 键总数（改后） | 探针残留 | 真机剩余（动态） |
|---|---|---|---|---|---|---|---|
| `data` | 22 | 501 | 17 | 17 | 501 | **0 页** | 4 页 / 7 条 |
| `electrical` | 36 | 1172 | 17 | 237 | 1392 | **0 页** | 32 页 / 50 条 |
| 合计 | 58 | 1673 | **34** | **254** | 1893 | **0** | 36 页 / 57 条 |

### 删死键明细（34 条）

| 页面 | 条数 | 内容 |
|---|---|---|
| `data/csv-json` | 3 | 3 条旧 FAQ（页面已删正文，仅余 `<h3>❓ 常见问题（FAQ）</h3>`） |
| `data/csv-to-markdown` | 3 | 同上 |
| `data/generator-35` | 3 | 旧「组距/边界」说明段（已改写为新口径） |
| `data/index` | 5 | 1 条旧介绍 + 4 条旧 FAQ（已改写为「分类下的工具需要下载或注册吗？」等新文案） |
| `data/yaml-json` | 3 | 3 条旧 FAQ |
| `electrical/calc-2` | 1 | `🧮 三相功率计算`（卡片名已改） |
| `electrical/detector-resistance-1` `-aging` `detector-resistance` | 3 | `⚡ 检测…服务`（3 页各 1 条） |
| `electrical/dianhuaxuedunhuakongzhi` | 2 | 旧标题 + 旧公式说明 |
| `electrical/generator-23` | 4 | 旧 intro / deep-dive / 运算符说明 / 占位串 |
| `electrical/index` | 4 | 4 条旧 FAQ（已改写） |
| `electrical/power-factor-compensation` | 1 | `🔌 功率因数补偿` |
| `electrical/voltage-divider` | 1 | `🔌 分压电路计算` |
| `electrical/voltage` | 1 | `🛠️ 电子束焊接参数`（错配卡片名） |

### 半译修复（254 条，键一律照抄运行时 `textContent.trim()`）

- `electrical` 以**公式说明行**（`formula-eq`）+ `placeholder` + 结果区标签（如 `总电压 (V)`、`视在功率 S（kVA）`）为主；`data` 以直方图/统计标签与 `placeholder` 为主。
- **动态数字型不硬拗**：含随输入变化的数值串（如 `总能量 10240 Wh`、`步骤1…`、`0时…` 除外——后者是 24 个固定轴标签，已程序化补键 `0时→0h`）一律不建键，计入「真机剩余」。
- 特例 `electrical/transformer-sizing`：标准容量枚举 `30、50、63…` 是**固定串**，整串成键（译为半角逗号列表），兼顾 IT 线新加的「数字间全角分隔符保留」规则。

### 改前 → 改后（实际渲染）

| 页面 | 改前 | 改后 |
|---|---|---|
| `tools/data/generator-35.html` | `📊 统计摘要` / `如 12,15,16,18,20` | `📊 Summary Statistics` / `e.g. 12,15,16,18,20` |
| `tools/electrical/voltage-divider.html` | `输入电压 Vin (V)` / `R1 (Ω, 上)` | `Input voltage Vin (V)` / `R1 (Ω, top)` |
| `tools/electrical/wire-resistance.html` | `导体电阻 R = 电阻率 ρ × 长度 L ÷ 截面积 A。校验：…` | `Conductor resistance R = resistivity ρ × length L ÷ cross-section A. Validation: …` |

### 剩余（真机 `?lang=en-US`，均为随输入变化的动态值，需页面/运行时改动，不在本批白名单）

| 目录 | 页 | 条 | 样例 |
|---|---|---|---|
| `data` | 4 | 7 | `颜色越深值越大 · 7行 × 24列`、`标签数：10 个`、`Max nesting depth：3 层` |
| `electrical` | 32 | 50 | `总能量 10240 Wh，续航 14.75 小时`、`＝ 51.20 V`、`步骤1` 序列 |

> 另有 5 条键（`electrical/detector-175` 的 `Estimated shaft power:约`、`temp-26` 的 `🛡️ Flameproof type:` / `📦 Recommended device:`、`dianhuaxuedunhuakongzhi` 的 `Potential below passivation threshold，金属持续溶解` 等）在**直接 `?lang=en-US` 首屏**仍显示中文——根因是页面脚本在翻译之后重写同一节点（本批只补了键，切换语言路径已可用；首屏需页面侧或 `tool-i18n.js` 处理，另行立项）。

### 待构建

| 目录 | 文件数 | 说明 |
|---|---|---|
| `i18n/tools/en/data/` | 7 | `csv-json`、`csv-to-markdown`、`data-visualizer`、`generator-35`、`index`、`xml-html-css-geshihua-yiyou-kebuchong`、`yaml-json` |
| `i18n/tools/en/electrical/` | 34 | 见本节「删死键明细」，含 `calc-1`、`calc-2`、`calc-power-voltage`、`current-divider`、`detector-173/175/aging/protection-2/resistance*`、`dianhuaxuedunhuakongzhi`、`generator-23`、`home-load-estimate`、`index`、`led-resistor`、`lizishujianshejisuan`、`load-curve`、`power-7`、`power-factor-compensation`、`power-voltage-1`、`rc-filter`、`rlc-resonance`、`speed-9`、`temp-26`、`transformer-sizing`、`voltage-8/9`、`voltage-divider`、`voltage-drop`、`voltage`、`wire-gauge-selector`、`wire-resistance` |
| `js/tool-i18n.js` | 1 | 共享层（数据上下文标点保护 + 动态补译积压重放），已单独提交 `b1effabac1`；2026-11-05 追加 `isNumericSep` token 化（见下节），随本批提交、同样待构建 |
| **合计** | **42** | 均须 `_build.py` 刷新 SW 版本戳后生效 |

## 今日新增经验（2026-11-05）

### 一、半译键必须先 `--keysrc` 还原源文键

`--check` 输出的是**运行时改写后的残留串**，其中「标签：」片段可能已被全局层（`BODY_PHRASE_MAP` / `replaceColonLabelsAll`）先替换成英文；直接照抄该串建键，键在 `applyEnDict` 执行时已不存在，永远打不中。

- 实例：`usedcar/rater-37` 的 `Rating:≥85 优秀…` 源文实为 `评级：≥85 优秀…`；`usedcar/tester-12` 的 `Charge voltage：…` 源文为 `充电电压：…`；`usedcar/wear` 的 `Deviation <0 时…` 源文为 `偏差 <0 时…`；`finance/points-redemption-value` 的 `（Reference:现金抵扣…` 源文为 `（参考：现金抵扣…`。
- 做法：先跑 `node scripts/_en_i18n_probe.mjs --keysrc <ind>/<slug>`，把输出里 `≠ EN … / ZH: …` 的 ZH 串作为 `map` 键。
- 同类历史坑：`🟢 状态良好：剩余里程充足`、`generic` 占位。

### 二、复查期新出现的正文要按当前 DOM 补译，被他人持有的页标记「待重译」

批量收口期间页面可能被其他线改写（新增深度解析段、FAQ 等），复查时会冒出 `--check` 首轮从未出现的条目。此时按**当前 DOM**补译即可；若该页仍在被别的线改造（如 `tools/finance/salary-after-tax.html` 正被假工具重写线处理），**不要硬译**，登记「待重译」，等对方提交后再补键，避免白译与键漂移。

## 第四批：`js/tool-i18n.js` 的 `isNumericSep` 改为 token 级（2026-11-05）

> 承接 `b1effabac1` 引入的「数据分隔符保护」；该判据原按**相邻字符**判断（`[0-9+\-.]`），判据过宽，把 `0.06、300rpm`、`20→10、2s`、`1.96（95% 置信）；…` 这类文案分隔符也当成数据保留全角，造成多页英文态残留回归。

### 判据

- token = 以空白或全角分隔符（`，；、`）为界的连续片段；`，；、` **左右跳过空白后的完整 token 都必须是纯数字**（`^[+-]?(\d+(\.\d+)?|\.\d+)$`）才判数据、保留全角。
- 任一侧 token 含字母 / 单位 / 运算符 / 中文 ⇒ 判文案、转半角。
- 该判据是旧判据的**真子集**（token 纯数字 ⇒ 其首/尾字符必属 `[0-9+\-.]`），故只会多转、不会新留。

### 结果

| 口径 | 旧判据 | 新判据 |
|---|---|---|
| 全站静态文本节点「含全角标点且无汉字」残留（4912 个 HTML，Python 模拟同一算法） | 17 | **3** |
| 上述修复节点 / 涉及页 | — | 14 节点 / 12 页 |
| 反向新增（新留旧转） | — | **0** |
| 14 页回归清单 `--check`（同进程、复跑 2/2 稳定） | 31 条 / 9 页 | **21 条 / 8 页** |
| 同上，对照 `57c062bc91`（`isNumericSep` 引入前） | — | 19 条 / 8 页 |

- 新判据结果与「引入前」逐条一致，差额仅 2 条 = `accessibility/braille-translator` 的 `1、2、3` / `4、5、6`（盲文点序，判数据保留）。
- 新判据仍保留的 3 个节点：`electrical/transformer-sizing` 标准容量枚举 `30、50、63…`（固定数据串）+ 上述盲文 2 条。
- 密码学 4 页（`it/atbash-cipher`、`caesar-cipher`、`vigenere-visualizer`、`text-similarity`）注入 `1，2，3` 仍 4/4 保留全角；反向保护 3 页（`statistics/z`、`paper/basis-weight`、`statistics/stddev-list`）仍 0 条。
- `scripts/verify_it_calc.js` 999/999；`scripts/discriminate_check.js verify_it_calc.js` 999 / 999 / 逃生 0 / 弱用例 0。

### 批处理探针噪声（重要，后续复验勿踩）

全站一次性 `--check`（4705 页同进程）存在**字典加载竞态**：同一页批量跑报 7 条残留、隔离单页跑为 0（实测 `marketing/assessor-51`）；且两次全站批跑（旧判据 2834 页 / 新判据 2987 页）出现**违反单调性**的反向变化（新判据只会多转、不可能多留），同样证明是竞态而非真实差异。**结论口径：`--check` 复验按「单页或 ≤14 页小批」执行，禁止用一次全站批跑的差值下结论。**

