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

## 0. 纪律：新增 / 修改 verify 用例必须过 fidelity（任何线都适用）

> **新增或修改 verify 用例后，必须用 `TB_STUB_FIDELITY=1` 跑该文件，且逃生项 = 0、all_default 不高于基线；否则视为用例不合格。**

判定口径（两条都要满足）：

1. 输出行 `仍 PASS(逃生项): 0` —— 逐键回退到**真实默认值**后，用例必须变红；
2. `TB_DISCRIM_REPORT=1` 导出的 `kind:"all-default"` 条数 **不得高于该文件的历史基线**（新增用例不得再拿默认输入当注入值）。

只跑 legacy 变绿**不算通过**：legacy 的假默认值会把「注入值与默认值算出同一结果」的用例掩护成绿（§4 已实测：fidelity 比 legacy 多暴露 19 条）。`TB_STUB_LEGACY=1` 仅用于定位历史差异，不能作为验收口径。

可直接复制的命令模板：

```bash
# ① 单文件（改完某个 verify_*_calc.js 后必跑）
TB_STUB_FIDELITY=1 node scripts/discriminate_check.js verify_<行业>_calc.js

# ② 单行业多文件（一条命令并列多个裸文件名）
TB_STUB_FIDELITY=1 node scripts/discriminate_check.js verify_<行业>_calc.js verify_<行业2>_calc.js

# ③ 全站（提交前/收口时跑；逐文件子进程，约数分钟）
TB_STUB_FIDELITY=1 node scripts/discriminate_check.js

# 辅助：导出逐条明细（含 kind/why/expect/reverted），用来核对 all-default 与逃生项
TB_STUB_FIDELITY=1 TB_DISCRIM_REPORT=1 node scripts/discriminate_check.js verify_<行业>_calc.js
```

> 计数说明：`已检` 不含隔离项；有文件「无统计行就退出」时会单独打印
> `⚠️ 逐文件隔离：N 个 verify 文件无统计行（贡献计 0；已单独列出，未当作通过）`，
> 该类文件**不得计入通过率**。`已检` 还受 `TB_DISCRIM_MIN`（默认 8000）下限约束，低于即 FAIL。

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
| legacy（默认） | 8725 | 8722 | **3** | 54 |
| fidelity（`TB_STUB_FIDELITY=1`） | 8694 | 8672 | **22** | 85 |

结论（与「保真后逃生项应减少」的直觉相反，但含义更强）：**legacy 的假默认值在掩护逃生项** ——
回退到「假默认值」时输出自然不命中 expect，看起来「判别力有效」；回退到**真默认值**后 expect 照样命中，
说明这些用例的 expect 根本不依赖被测输入。fidelity 比 legacy 多暴露 19 条；逃生的具体位置见 §7 工单。

跳过 54 → 85（+31）的构成（`TB_DISCRIM_REPORT=1` 逐条导出）：
**all_default 弱用例 36**（注入值 = 真实默认值）、**无法静态解析 40**（控件 id 由页面脚本运行时生成，
如矩阵打分 `m0_0`、尿检 `ua_leu`）、**无注入 10**（本来就不适用）。详见 §8。

legacy 自身 3 条逃生项（`construction/calc-204`、`it/decimal-encode`、`it/number-base-converter`），
与 `scripts/discriminate_baseline.json` 的 `escape: 0` 不一致 —— 不是本批引入，需各线收紧后同步基线。
其中 `construction/calc-204` 已由本线在 §6.3 收紧（2026-11-05），当前只剩两条 it 用例待 IT 线处理。

> **口径修正（2026-11-05）**：上一版（`b96ec6d21d`）报的「fidelity 86 逃生 / 跳过 259」是
> `lib_stub.parseInputDefaults` 的缺陷造成的假象 —— 无 `value` 属性的 `<input>`（如 `type="date"`）
> 被整键丢弃，导致 214 条用例被判「控件解析不到」而跳过、部分错位成逃生。已修（无 value ⇒ 空串，
> 与真机 `.value`/legacy 一致），修正后为 **22 逃生 / 跳过 85**。以本节数字为准。

> **复测（2026-11-05，本线收紧 5 条后；当前工作区含其他线并行改动）**：
> legacy `已检 8728 / 正确变红 8726 / 逃生 2 / 跳过 54`（2 条均为 it：`decimal-encode`、`number-base-converter`）；
> fidelity `已检 8698 / 正确变红 8690 / 逃生 8 / 跳过 84`。两模式均隔离 1（`verify_office_calc.js` 无统计行）。
> 剩余 8 条 fidelity 全部属其他线：agriculture/dli-calculator、gastroenterology/hp-resistance、image/image-collage、
> it/confidence-interval、it/captcha-generator、it/des、it/summary-generator、sports/calculator-calc-time。
> `construction/calc-204`、`machinery/torque`、`electrical/temp-26`、`hvac/kongtiaolengfuhejisuan`、
> `fire-rescue/calc-1` 已不再出现在任一模式的逃生列表（收紧方式见 §6.3）。

> **注意（静默退出）**：`tools/office/pdf-split` 的用例会让**单进程**全站跑静默退出（0 字节输出、exit 0）——
> 该页 `pdfjsReady()` 的轮询 Promise 在 harness 内永不 settle、定时器又不持有事件循环，Node 事件循环空后静默 exit 0。
> 现在判别器改为「逐文件子进程 + 父进程汇总」，该文件被单独列为**隔离跑**（不计入总量、不当作通过），
> 并加了「未打印统计行 ⇒ exit 1」「已检 < 下限 ⇒ exit 1」两道闸；`--selftest` 可自证这两道闸会变红。
> 根因仍在页面（`pdfjsReady` 的轮询未绑定可清理的定时器），需 office 线修。

## 5. 共享模块实现与接入范围

`scripts/lib_stub.js`（新建，纯函数，不改任何桩）：

| 能力 | 实现方式 |
|---|---|
| input 默认值 | 正则扫 `<input …>` 全标签再按 `\bid\s*=\s*["']…["']` / `\bvalue\s*=\s*["']…["']` 各自独立取值 ⇒ 属性顺序、单双引号都无关；**无 `value` 属性 ⇒ 空串**（真机 `.value` 语义）；`opts.skipTypes` 排除 checkbox/radio/button 等 |
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

## 6. 逃生项修复工单（fidelity 22 条，按行业认领）

> 判据：把用例 inputs 逐键换回**页面真实默认值**（模拟注入失败）后仍 PASS ⇒ 该 expect 不依赖被测输入。
> 「为什么逃生」列的真机证据来自 headless Chrome（默认态 / 注入态各跑一次，采集可见文本 + 控件值）；
> 「建议新锚点」是从注入态输出里自动挑出、**默认态与页面静态文案都不出现**的数字/单位片段，
> **仅供参考**（评级按钮、色值等低置信候选已尽量剔除），行业线须按页面语义确认。
> 本工单**不代表改动用例** —— 每条由所属行业线自行收紧，严禁跨线改。

### 6.1 明细（22 条）

| 行业 | slug | 文件 | 用例 ref | 当前 expect | 为什么逃生（具体位置） | 建议新锚点 |
|---|---|---|---|---|---|---|
| cosmetic-derm | `cosmetic-derm/eyebag-assessment` | verify_cosmetic-derm_calc.js | raw=3×3+2×2+2×2+2×2.5+4×0.5=24 → 评 | 48 / 中度眼袋 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`中度眼袋` 默认态就已输出 | `3/4` / `2/3` |
| cosmetic-derm | `cosmetic-derm/glogau-photoaging` | verify_cosmetic-derm_calc.js | 评=(2×3+4×2+3×1.5+2×2+4×1.5)/10=28. | 2.9 / Ⅲ型 | expect 含页面静态文案（源码可见，不随输入变化）：`Ⅲ型` 是页面静态文案 | `2.85` / `2.9` |
| cosmetic-derm | `cosmetic-derm/fitzpatrick-wrinkle` | verify_cosmetic-derm_calc.js | 注入四项全非默认（默认 wrinkleGrade=1 / elast | 100 重度光老化 / 皱纹等级 Ⅳ级 / 弹力变性 重度 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `9/10` / `200` |
| fire-rescue | `fire-rescue/calc-1` | verify_fire-rescue_calc.js | 同一 0.30 MPa 换 16 mm 水枪（默认口径 19 mm） | 19.68 / 13.92 / 24.26 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`24.26` 默认态就已输出 | `19.68 m` / `13.92 m` |
| cosmetic-derm | `cosmetic-derm/fitzpatrick-wrinkle` | verify_cosmetic-derm_calc.js | 自动补强（B类零用例） | 素沉着）。 建议：综合治疗方案——激光焕肤+填充+肉毒素+线雕提拉。 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `10/10` |
| gastroenterology | `gastroenterology/hp-resistance` | verify_gastroenterology_calc.js | 三药全部未检测（默认 clar 敏感 / metro 耐药 / le | 未检测药物：克拉霉素、甲硝唑、左氧氟沙星 / 中（存在未检测药物） | expect 含页面默认态就生成的输出（回退默认后仍命中）：`中（存在未检测药物）` 默认态就已输出 | （无可靠候选，需人工） |
| machinery | `machinery/torque` | verify_general_calc.js | M10 公称应力截面积 As=58.0mm²（标准值） | 58.0 / 22.27 / 0.220 / 384 / 49.0 | expect 含页面静态文案（源码可见，不随输入变化）：`58.0` 是页面静态文案；`0.220` 是页面静态文案 | `22.27` / `49.0` |
| electrical | `electrical/temp-26` | verify_general_calc.js | 标志按 Ex+型式+气体类别+温度组别 拼接 = 「Ex i IIB | Ex i IIB T4 / 135 / 0区、1区、2区 | expect 含页面静态文案（源码可见，不随输入变化）：`135` 是页面静态文案 | `Ex i IIB T4` / `0区、1区、2区` |
| construction | `construction/calc-204` | verify_general_calc.js | 自动补强（B类零用例） | 0.82 理论支撑间距 s (m) / 2704 支撑总根数 / 5 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `52×52` / `0.81` |
| image | `image/image-collage` | verify_image_calc.js | auto-restore | 固定高度 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`固定高度` 默认态就已输出 | （无可靠候选，需人工） |
| hvac | `hvac/kongtiaolengfuhejisuan` | verify_general_calc.js | 自动补强（B类零用例） | � 推荐空调配置：3-5匹柜机/天井机 暂无计算记录 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `13.14` / `13144` |
| it | `it/confidence-interval` | verify_it_calc.js | 独立复算：SE=s/√n=15/√30=2.7386；95% 双侧  | [ 94.632 , 105.368 ] / 临界值 z = 1.9 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`临界值 z = 1.960` 默认态就已输出 | `94.632 ,` / `15/√30 =` |
| it | `it/des` | verify_it_calc.js | openssl 交叉验证 | 3des | expect 含页面默认态就生成的输出（回退默认后仍命中）：`3des` 默认态就已输出 | `0.8` / `0.5` |
| it | `it/captcha-generator` | verify_it_calc.js | 自动补强（B类零用例） | nQ6zE复制导出gre2B复制导出yq1uF复制导出0glzX复制 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | （无可靠候选，需人工） |
| it | `it/summary-generator` | verify_it_calc.js | 自动补强（B类零用例） | 社会的方方面面。 5 14 5 469 68 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `1 2 3` / `0.00` |
| obstetrics | `obstetrics/placenta-grading` | verify_obstetrics_calc.js | 注入孕周 32 周 + Grannum 2 级（默认 36 周 +  | II级(成熟) / 32–36周 / 绒毛板切迹深入实质未达基底 / | expect 含页面静态文案（源码可见，不随输入变化）：`II级(成熟)` 默认态就已输出；`32–36周` 是页面静态文案；`绒毛板切迹深入实质未达基底` 默认态就已输出；`胎盘成熟度与孕周基本相符` 默认态就已输出 | `II级(成熟)Grannum分级32周当前孕周32–` |
| obstetrics | `obstetrics/bishop-score` | verify_obstetrics_calc.js | 注入五项 Bishop 项（默认全 0）。独立复算（页面权重表） | 11/13 / Bishop总分 11 / 可直接用缩宫素引产 /  | expect 含页面静态文案（源码可见，不随输入变化）：`11/13` 是页面静态文案；`可直接用缩宫素引产` 默认态就已输出 | `宫口扩张：3分` / `宫颈消退：3分` |
| obstetrics | `obstetrics/preeclampsia-prediction` | verify_obstetrics_calc.js | 自动补强（B类零用例） | %） 确诊界值：≥110（晚 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `1,500 →` / `1.0` |
| sports | `sports/calculator-calc-time` | verify_sports_calc.js | 总用时 12600 s ÷ 42.195 km = 298.61 s | 4:59 / 半程马拉松 21.098 / 3:30:00 | expect 含页面静态文案（源码可见，不随输入变化）：`半程马拉松 21.098` 默认态就已输出；`3:30:00` 是页面静态文案 | `1 km 4:59 4:59/km` / `12.06` |
| pulmonology | `pulmonology/tb-resistance` | verify_pulmonology_calc.js | auto-restore | 有传染性，需呼吸道隔离 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`有传染性，需呼吸道隔离` 默认态就已输出 | （无可靠候选，需人工） |
| cosmetic-derm | `cosmetic-derm/pore-grading` | verify_cosmetic-derm_calc.js | 评=(2×3+2×3+3×2+2×2)/10×25=22/10×25 | 55 / 中度毛孔粗大 | expect 含页面默认态就生成的输出（回退默认后仍命中）：`中度毛孔粗大` 默认态就已输出 | `颊部 3级 扩大伴黑头` / `前额 2级 明显可见` |
| agriculture | `agriculture/dli-calculator` | verify_agriculture_calc.js | 自动补强（B类零用例） | /m²/d（代表：黄瓜、番茄幼苗、草本植物） DLI达标，当前光照满 | 真机两态都未复现（随机种子/交互路径/异步），需人工复核 | `400 →` / `12.7` |

### 6.2 原因分布与按行业

**原因分布**：默认态输出 8 / 静态文案 6 / 其它 8。
- **默认态输出（8）**：expect 里有一项是页面默认输入就能生成的数值/结论（回退默认后必然命中）。
- **静态文案（6）**：expect 里有一项是页面可见静态文字（如 `Ⅲ型`、`58.0`、`3:30:00`），与输入完全无关。
- **其它（8）**：真机默认态与注入态都未复现该串 —— 多为随机种子（`captcha-generator` 的验证码串
  是 harness 固定 PRNG 的输出）、或需要多步交互/异步渲染，**必须人工复核**后才能定性质。

**按行业**：cosmetic-derm 5、it 4、obstetrics 3、fire-rescue 1、gastroenterology 1、machinery 1、electrical 1、construction 1、image 1、hvac 1、sports 1、pulmonology 1、agriculture 1。

### 6.3 本批收口记录（2026-11-05，construction 线）

已收紧并复验（`verify_general_calc.js` / `verify_fire-rescue_calc.js`，仅改用例、未改桩、未改页面）：

| slug | 逃生根因 | 收紧方式 | 结果 |
|---|---|---|---|
| `construction/calc-204` | 注入 42/42/42/42 时 s=√(42/63)=0.82，与真实默认 6/3/30/30 的 √(30/45)=0.82 **同值** | 改注入 5/2/40/20（q_d=60），锚 `0.58` / `36` / `9×4` / `16.7` / `600`，全部带输出标签 | 注入态命中，回退默认全不命中 |
| `machinery/torque` | vSize 取了默认 M10，expect 首位 `58.0` 回退默认仍命中 | 改 M12（As=84.3），锚 `84.3` / `32.37` / `0.220` / `85.5` / `384` | 同上 |
| `electrical/temp-26` | v1 取了默认 T4，expect 含 `135`（T4 上限） | 改 T5，锚 `Ex i IIB T5` / `100 最高表面温度 (℃)` / `0区、1区、2区` | 同上 |
| `hvac/kongtiaolengfuhejisuan` | 只锚档位文案「3-5匹柜机/天井机」，默认 area=50 也落同一档 | 改 area=100，锚实算 `17.16` / `172` / `6.9`（档位文案在静态说明里也出现，弃用） | 同上 |
| `fire-rescue/calc-1` | 第三锚 `24.26`（出口流速）只由压力决定、与口径无关 | 剔除 `24.26`，保留 `19.68` / `13.92`（均依赖 16 mm 口径） | 同上 |

判别力验证：把 `construction/calc-204` 的五项 expect 全部改成错值后，`node scripts/verify_general_calc.js calc-204` 输出 `❌ 未匹配期望值`、exit 1；恢复后 2/2 通过。两文件 discriminate（legacy 与 `TB_STUB_FIDELITY=1`）均为 `仍 PASS(逃生项): 0`。

