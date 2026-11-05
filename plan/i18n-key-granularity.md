# 第三层英文字典「键粒度」台账

> **一句话结论**：英文态「半译」大多不是漏翻，而是**键的粒度错了**——要么键不是真实原文，要么一句里的重复中文串只被前缀层替换了一次。

适用对象：`i18n/tools/en/<ind>/<slug>.json` 的 `map`（第三层，优先级最高，运行时按 `el.textContent.trim()` 精确匹配）。

## 硬约束

### ① 键必须照抄真实原文

`map` 的键必须是**页面运行时真实 `textContent.trim()` 的逐字原文**，不能写成「我以为它长什么样」。

- 运行时是 `pickEn` 精确匹配，错一个字（大小写、空格、全半角、顺序）= 永久缺口，而且**探针看不出缺键**，只表现为「半英半中」。
- **典型反例**（2026-11-05 `it/timestamp-converter`）：页面真实渲染 `本地时间 (本地时间)`，键却写成 `Local Time (本地时间)`——后者是「前缀层替换后」的形态，永远打不中。随后前缀层把第一个 `本地时间` 换成 `Local Time`，尾巴 `(本地时间)` 留下 → `Local Time (本地时间)` 半译。
- 写键前的正确取法：真机跑一次，`JSON.stringify(el.textContent)` 原样拷；**不要**从译文侧反推原文。

### ② 同一句里重复的中文串，必须整句成键

前缀层（`BODY_PHRASE_MAP` / `<ind>-phrases.json`，`longestPrefixKey`）**对每个文本节点只替换第一个命中**。若一句里出现两次同一中文串（`本地时间 (本地时间)`），短语层只能替换一半。

- **判据**：探针报「半译」时，先看这句里是否有**重复中文串**。有 → 整句写进第三层 `map`，不要补短语层。
- 整句成键后 `pickEn` 先命中，前缀层不再介入，尾部不会残留。

## 已落案例

| 日期 | 页面 | 现象 | 根因 | 修法 |
|---|---|---|---|---|
| 2026-11-05 | `tools/it/timestamp-converter.html` | `.tz-name` 恒为 `Local Time (本地时间)` | 键写成替换后形态 `Local Time (本地时间)`；前缀层只替换首个 `本地时间` | 键改为真实原文 `本地时间 (本地时间)` → `Local Time` |

复验：10 页交互探针由 `A=1 页` 降为 `A=0 页`（该页归 C-正常）。

## 附：`TBKit` 外部全局盘点（已盘点，**不做门禁**）

- `tools/it/` 共 339 页，335 页引用 `TBKit`；**完全没有任何 `typeof TBKit` 守卫的页面：0**。
- `TBKit.` 调用点约 2.8k，绝大多数在 `try{…}catch(e){}` 或 `if (typeof TBKit === 'undefined') return;` 之后。
- 行级启发式扫出的 286 处「疑似裸调用」经复核**真阳性 0**；4 页误报全部位于守卫表达式内部。
- **结论：已盘点、不需要门禁。** 行级启发式误报率 100%，做成门禁只会制造假红；半年后不必重做。

## 待构建提交（构建窗口开放后随批入库）

> 红线 3：`i18n/tools/en/**` 已纳入 SW 版本戳，改后必须重跑 `_build.py`；窗口未开前**留在工作区、不要清理**。

| 文件 | 改动 | 为什么等 |
|---|---|---|
| `i18n/tools/en/it/timestamp-converter.json` | 键 `Local Time (本地时间)` → `本地时间 (本地时间)`；补 `Unix 秒/毫秒`、星期名等 | 第三层字典，须 `_build.py` 刷新版本戳 |
| `i18n/tools/en/it/{json-repair,regex,yaml-validator,html-nesting-checker}.json` | 各补 1–3 条静态结果串键（`✅ JSON 合法…`、超时中止整句、`YAML 语法验证通过`、`✅ HTML 嵌套结构合法…`） | 同上 |
| `tools/it/json-formatter.html` | `__en` / `✅ Valid JSON` 两处补 `/lang=en-US/i.test(location.search)` 兜底 | 页面改动须与字典同批构建 |
| `tools/it/{calc-8,regex-visualizer,password-generator,text-diff,csv-to-json,text-statistics}.html` | 首屏/动态结果串按 `location.search` 或 `TBKit.util.isEn()` 输出英文；`text-statistics` 预设 `labelEn` 改英文描述 | 同上 |
| ~~`js/tool-i18n.js`~~ | ~~`convertPunct()` 新增「数据分隔符保护」…（`isNumericSep`）~~ **✅ 已整文件提交 `b1effabac1`**：两组改动（数据上下文标点保护 + 动态补译积压重放）一并入库 | 仍待 `_build.py` 刷 SW 版本戳 |

状态：✅ 已提交 `3ce0948e47` + `b1effabac1`（共享层 `js/tool-i18n.js` 已整文件入库），⏳ **仍待构建**——`_build.py` 未跑，SW 版本戳未更新；构建窗口开放后重跑 `_build.py` 再随批入库。
