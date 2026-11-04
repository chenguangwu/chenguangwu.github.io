# 桩保真度失配清单（第 11 批，2026-11-04）

> 目的：把「HTML 默认态被桩忽略」导致的 verify 失配逐条落地，供各行业修复线按目录认领。
> 取证口径：**真机 Chrome**（headless，`?lang=zh-CN`，按用例 inputs 注入后点击主按钮，采集可见文本 + 表单值）。
> 判定三类：
> - **用例失真**：真机输出 ≠ legacy expect，且差异可由「HTML `checked` 默认态 / `<select selected>` 默认值」解释 ⇒ 改用例期望。
> - **页面缺陷**：真机输出与 legacy、fidelity 都不同，且无法归因于默认态 ⇒ 改页面。
> - **桩仍缺口**：真机输出符合 legacy expect（fidelity 改动反而偏离真机）⇒ 继续修桩。
>
> 复现：`TB_STUB_FIDELITY=1 node scripts/discriminate_check.js`（默认仍走 legacy，避免直接翻默认）。
> 逃生：`TB_STUB_LEGACY=1` 强制回 legacy。

## 1. 共享模块与接入范围

- 新增 `scripts/lib_stub.js`：input 默认值解析（属性顺序/引号无关）、`<select>` 尊重 `selected`（两种写法）+ `<select multiple>`、textarea 初始文本、checkbox/radio `checked` 默认态。
- 本批**只接入** `scripts/discriminate_check.js`（`pageDefaults` 改为调用 `lib_stub`）。
- 各 `verify_*_calc.js` 分行业分批接入；接入前一律保持 legacy 行为。

## 2. 失配分组（按 `tools/<行业>/` 认领）

真机取证：保真模式下全站 verify 失配（**613 条 ❌ 行 / 348 个 slug**）逐 slug 展开为 **871 条用例**，
覆盖 **347 个页面**。每条用例都在真机 Chrome（headless、`?lang=zh-CN`）注入同 inputs / checkIds / radios、
点主按钮、采集可见文本 + 控件值，再与用例 expect 比对。

| 行业目录 | 用例数 | 页数 | 用例失真 | 桩仍缺口 | 需人工 |
|---|---|---|---|---|---|
| tools/it | 344 | 115 | 31 | 137 | 176 |
| tools/biz | 108 | 47 | 40 | 28 | 40 |
| tools/design | 69 | 28 | 6 | 26 | 37 |
| tools/life | 50 | 12 | 4 | 21 | 25 |
| tools/finance | 33 | 12 | 4 | 14 | 15 |
| tools/health | 32 | 15 | 2 | 13 | 17 |
| tools/edu | 21 | 8 | 2 | 2 | 17 |
| tools/image | 18 | 9 | 3 | 5 | 10 |
| tools/science | 17 | 8 | 1 | 6 | 10 |
| tools/language | 13 | 4 | 3 | 1 | 9 |
| tools/marketing | 12 | 4 | 0 | 6 | 6 |
| tools/hydraulic | 10 | 5 | 0 | 5 | 5 |
| tools/bridge | 8 | 4 | 0 | 0 | 8 |
| tools/chinese | 8 | 2 | 0 | 2 | 6 |
| tools/cognition | 8 | 3 | 5 | 2 | 1 |
| tools/agriculture | 8 | 1 | 0 | 1 | 7 |
| tools/fitness | 7 | 4 | 0 | 2 | 5 |
| tools/music | 7 | 1 | 1 | 6 | 0 |
| tools/clinical-lab | 6 | 1 | 0 | 5 | 1 |
| tools/sports | 6 | 3 | 0 | 1 | 5 |
| tools/construction | 5 | 3 | 1 | 0 | 4 |
| tools/energy | 5 | 3 | 0 | 3 | 2 |
| tools/fun | 5 | 5 | 0 | 0 | 5 |
| tools/baking | 4 | 3 | 0 | 3 | 1 |
| tools/fire-rescue | 4 | 2 | 2 | 2 | 0 |
| tools/metalwork | 4 | 2 | 0 | 2 | 2 |
| tools/photo2 | 4 | 1 | 3 | 1 | 0 |
| tools/travel | 4 | 4 | 1 | 1 | 2 |
| tools/clinical-nursing | 3 | 2 | 0 | 0 | 3 |
| tools/data | 3 | 2 | 2 | 1 | 0 |
| tools/home | 3 | 2 | 0 | 0 | 3 |
| 其余 28 个行业（各 1–2 条） | 42 | 33 | 19 | 7 | 16 |
| **合计** | **871** | **347** | **130** | **303** | **438** |

> 「其余 28 个行业」含 audio / cosmetic-derm / electronics / welding / fishery / food / healthcare / text /
> legal / martial / obstetrics / reproductive-medicine / road / tcm-diagnosis / astronomy / automotive /
> cardiology / dermatology / fire / accessibility / beekeeping / property / pulmonology / rubber / safety /
> transport / urology / yi，逐条明细以 `/tmp/mismatch.json`（真机 blob 已截 300 字）为准。

## 3. 三类判定分布与口径

| 判定 | 条数 | 判据（本次实际口径） | 下一步 |
|---|---|---|---|
| 桩仍缺口 | 303 | **真机命中 expect**，验证器未命中 ⇒ 真实默认态没被桩覆盖（checked / select 默认 / textarea / input 属性顺序） | 该行业线把对应 `verify_*` 接入 `lib_stub`，并复核 expect 是否依赖默认态 |
| 用例失真 | 130 | 真机未命中，且页面存在「HTML `checked` 默认态」或「select 默认项≠首项」，而用例又没显式声明该控件 ⇒ 期望是按错默认态写的 | 该行业线改用例期望（用真机取值重算） |
| 需人工 | 438 | 真机未命中且无上述默认态线索 | **不预设为页面缺陷**：含「页面缺陷」与「真机取证噪音」两种可能，必须逐条复核 |

**口径警告（必须读）**：
1. `需人工` 里的真机取证是**启发式**的：统一「注入 inputs → 点第一个 `.btn.primary` → 等 350 ms」，
   对无主按钮 / 异步渲染慢 / 需要多次点击的页面会采集到半成品输出 —— 这部分是噪音，不是页面缺陷。
2. 本次**没有**保存「fidelity 下实际输出」这一列：生成失配清单时 `FIDELITY` 解析写在
   `scripts/verify_it_calc.js` 里，已按要求撤销，无法再批量复现。按行复现命令：
   `TB_STUB_FIDELITY=1 node scripts/verify_<行业>_calc.js <slug>`（fidelity 解析目前只在
   `discriminate_check.js` 接入，verify 侧要等行业线接入 `lib_stub` 后才有「保真实际输出」）。
3. 因此本清单**只给出可被真机证伪的三类**，最终「页面缺陷」裁定必须由行业线带真机取值复核，
   不得拿桩自证。

## 4. 两种模式 discriminate 对照（桩保真度是否在掩护假用例）

全站 207 个 `verify_*_calc.js`，逐文件独立子进程跑（原因见下「注意」），汇总：

| 模式 | 已检 | 正确变红 | 仍 PASS（逃生项） | 跳过 |
|---|---|---|---|---|
| legacy（默认） | 8725 | 8723 | **2** | 54 |
| fidelity（`TB_STUB_FIDELITY=1`） | 8520 | 8434 | **86** | 259 |

结论（与「保真后逃生项应减少」的直觉相反，但含义更强）：
- **逃生项 2 → 86**：不是保真把用例弄坏，而是 legacy 的错误默认值在**掩护**逃生项 ——
  回退到「假默认值」时输出自然不命中 expect，看起来「判别力有效」；回退到**真默认值**后 expect 照样命中，
  说明这些用例的 expect 根本不依赖被测输入（典型如 `it/uuid-generator` 8 例、`it/timestamp-converter` 5 例、
  `life/workday-calculator` 5 例）。
- **跳过 54 → 259**：多出的 205 条是「注入值与页面真实默认值完全相同」的 all_default 弱用例 ——
  legacy 因解析错默认值而让它们**看起来**有注入。
- legacy 自身仍有 2 条逃生项（`it/decimal-encode`、`it/number-base-converter`），与
  `scripts/discriminate_baseline.json` 的 `escape: 0` 不一致；这两条是 IT 线 `6bad8fd7a4` 新增用例引入的，
  **不在本批提交范围**，需 IT 线自查后同步基线。

fidelity 下 86 条逃生项按文件分布（前 10）：`it` 26（uuid 8 / timestamp 5 / 其余 13）、
`life` 9（workday 5 / 其余 4）、`obstetrics` 4、`cosmetic-derm` 5、`legal` 3、
`general` 4、`chinese` 2、`cardiology` 2、`science` 3、`health` 2；其余散见各行业 1–2 条。

> **注意**：`tools/office/pdf-split` 的用例会让单进程全站跑**静默退出**（0 字节输出、exit 0）——
> 该页 `pdfjsReady()` 的轮询 Promise 在 harness 内永不 settle 且定时器不持有事件循环，Node 空事件循环后正常退出。
> 这是既有缺陷，本批不改 `verify_it_calc.js`；因此全站统计采用「逐文件子进程」跑法，该文件无汇总行（贡献 0）。

## 5. 共享模块实现与接入范围

`scripts/lib_stub.js`（新建，纯函数，不改任何桩）：

| 能力 | 实现方式 |
|---|---|
| input 默认值 | 正则扫 `<input …>` 全标签再按 `\bid\s*=\s*["']…["']` / `\bvalue\s*=\s*["']…["']` 各自独立取值 ⇒ 属性顺序、单双引号都无关；`opts.skipTypes` 排除 checkbox/radio/button 等 |
| `<select multiple>` | `parseSelects()` 返回 id → options 数组（数组上挂 `.multiple`），`selected` 布尔属性与 `selected="selected"` 都识别；全选值由调用方按 `.multiple` 自行取全部 selected |
| `<select>` 默认 | `selectDefault()` 优先任意带 `selected` 的 option（不论位置/属性顺序），无则回退首个；option 无 `value` 时取文本，与真机 `.value` 一致 |
| textarea 初始文本 | `parseTextareaDefaults()` 取内联文本并解码 `&#10;`/`&quot;`/`&amp;`，调用方**同时**写 `.value` 与 `.textContent` |
| checkbox/radio 默认态 | `parseCheckedIds()` 返回带 `checked` 的 checkbox/radio 的 id 集合，调用方用 `checkIds` 还原真机默认选中态 |

接入范围（本批）：**仅 `scripts/discriminate_check.js`**（`pageDefaults` 调 `lib_stub`）。
`verify_*_calc.js` 一律未动，等各行业线按第 2 节分组自行接入；接入前行为与 HEAD 逐字节一致。

开关语义：`TB_STUB_FIDELITY=1` 启用保真解析；`TB_STUB_LEGACY=1` 永远优先（一次性逃生）；**默认 legacy**。

残余缺口（接入 verify 时必须补）：**页面脚本在加载末尾设 `select.value`**（如 `forestry/tree-volume`
的 `curFormula`）无法靠静态 HTML 解析 —— `selected` 属性缺失、首项又不是脚本所选值。这项只能在
「跑完页面后读一次真实 `select.value`」时补，属 verify 侧接入工作，`discriminate_check.js`
（只做静态解析）无法覆盖，已在第 2 节的清单里按「需人工」标注。

## 6. 附录：fidelity 模式下的 86 条逃生项（按 `verify_*` 文件）

> 判据：把用例 inputs 逐键换回**页面真实默认值**（模拟注入失败）后仍 PASS ⇒ expect 不依赖被测输入。
> 每条都需该行业线收紧 expect（改成非默认输入下的派生量）。注意部分文件含跨行业 slug（`finance` 文件里有
> `automotive/vin-validator`、`science` 文件里有 `tax/rfc-validator`），按 slug 归属认领。

- `aerospace`：1 — aerospace/flight-time
- `agriculture`：1 — agriculture/dli-calculator
- `astronomy`：1 — astronomy/sunrise-sunset
- `baking`：1 — baking/oven-temp
- `cardiology`：2 — cardiology/ambulatory-bp、cardiology/coronary-calcium
- `chinese`：2 — chinese/chinese-character、chinese/chinese-radical-lookup
- `clinical-lab`：1 — clinical-lab/hba1c-converter
- `cosmetic-derm`：5 — pore-grading、glogau-photoaging、eyebag-assessment、fitzpatrick-wrinkle ×2
- `design`：1 — design/gradient
- `edu`：1 — edu/ebbinghaus-curve
- `endocrinology`：1 — endocrinology/metabolic-syndrome
- `finance`：2 — automotive/vin-validator、finance/currency-symbol
- `fire-rescue`：1 — fire-rescue/calc-1
- `fishery`：1 — fishery/breeding-cycle
- `funeral`：1 — funeral/reminder-3
- `gastroenterology`：1 — gastroenterology/hp-resistance
- `general`：4 — general/calc-14、electrical/temp-26、machinery/torque、hvac/kongtiaolengfuhejisuan
- `health`：2 — health/premature-age-calculator、health/ovulation-calculator
- `image`：1 — image/image-collage
- `it`：26 — uuid-generator ×8、timestamp-converter ×6、confidence-interval、unicode-lookup、
  og-meta-tag-generator、git-commands、regex-cheatsheet、tmux-cheatsheet、url-encode、
  emoji-meaning、captcha-generator、des、rabbit、summary-generator
- `legal`：3 — legal/calendar-qr、legal/calc-17、legal/labor-compensation
- `life`：9 — life/workday-calculator ×5、color-name-finder、date-add-subtract、
  date-difference-calculator、temperature-converter
- `livestock`：1 — livestock/castration-timing
- `marketing`：2 — marketing/marketing-roi、marketing/social-media-image-sizes
- `medical`：1 — medical/reminder-2
- `museum`：1 — museum/historical-calendar
- `obstetrics`：4 — bishop-score、placenta-grading、gestational-age、preeclampsia-prediction
- `pulmonology`：1 — pulmonology/tb-resistance
- `quality`：1 — quality/table-sampling
- `safety`：1 — safety/detector-strength
- `science`：3 — tax/rfc-validator、science/si-unit-converter、science/star-magnitude-compare
- `security`：1 — security/emergency-contacts
- `sports`：1 — sports/calculator-calc-time
- `telecom`：1 — telecom/quick-calc-time-bandwidth
