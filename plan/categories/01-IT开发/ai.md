# AI 工具 · tools/ai（64 页）

## 已知问题
### A1. 「参数估算器」类页与实际框架口径脱节
- 描述：training-flops/vram-estimate/transformer-params 等按教科书式估算，与 transformers/deepspeed 实测差异大（激活重计算/序列并行未建模）。
- 受影响：tools/ai/training-flops.html、vram-estimate.html、transformer-params.html 等
- 方案：增加「口径开关」（是否重计算/ZeRO 档位），并注明与 N 卡实测的对表来源。

### A2. 概念演示页交互浅
- 描述：softmax/k-means/attention 等页多为静态算例，滑杆联动少。
- 受影响：tools/ai/softmax*.html、k-means、attention-flops 等（已补图表，交互待深）
- 方案：统一加「拖拽数据点看输出即时变化」的最小交互（canvas 已具备）。

## 功能缺陷
- token 计数页与主流 tokenizer 口径未对齐（中文按字/词差异提示不足）。

## 优化点
- 「模型对照表」内容模块：主流开源模型参数/显存/长度速查（静态数据+筛选），是 AI 类搜索流量入口，市面单页工具稀缺。
- S2 场景预设：VRAM 页预设「7B-FSRLora / 13B-QLoRA / 70B-Int4」等真实部署场景。

## 受影响范围
- tools/ai/（64 页）

## 进度
- 🟢 批次 04-b1（2026-10-26 · S2 真实部署场景预设）：`vram-estimate` +3 预设（7B LoRA 微调 bf16 act=14GB → 28GB 总、13B QLoRA 4-bit act=8GB → 14.5GB、70B INT4 推理 act=1GB → 36GB）；calc() 动态串（权重显存/总显存估算）EN 治理；**__veL 修复**：原 `typeof TBKit!=='undefined'&&TBKit.util.isEn()` 在 jsdom/检测器环境（不加载外链）恒 false → 补 location.search/lang fallback。verify ai 118→121、判别器 0、门禁 218/218。
- 🔴 待开发

## 2026-11-03 审计补充（静态源码复核）

### 确认缺陷：显存估算的图表、明细和历史容器被计算过程移除（高）
- 问题：每次计算会覆盖结果容器的全部子节点，导致图表、明细、历史及 CSV 导出的目标容器丢失。
- 证据：`tools/ai/vram-estimate.html:136-140` 将 `veChart`、`veTable`、`veDiff`、`veHist` 放在 `result` 内；`:284` 用 `result.innerHTML` 整体替换；`:301` 导出目标为 `#veTable`，`:311-318` 渲染图表、表格及历史。这是源码路径确认，尚未进行浏览器运行时验证。
- 影响：单页的图表、明细、对比、历史及 CSV 导出；主数字计算仍可显示。
- 方案：为计算结果单独保留容器，避免替换其它宿主；修复后分别验证首屏、修改输入、预设点击、CSV、历史回填。

### 疑似待验证：历史回填的数据字段不匹配（中）
- 证据：`tools/ai/vram-estimate.html:316-318` 写入历史仅包含 `total`，回填却读取 `params`、`bytes`、`act`；目前宿主被移除使该路径不可验证。
- 影响：单页；图表宿主修复后可能使历史恢复无效。
- 方案：记录并回填同一组输入字段，再验证两次计算与历史切换。

### 留存优化（低，非确认缺陷）
- `tools/ai/vram-estimate.html:124-129,313-314`：目前判据固定为 24GB，建议增加显存容量输入与 8/16/24/48GB 对比，展示余量；保留近似假设说明。
- 同页 `:125,274-283`：总量只加权重和手填激活，建议区分推理 KV 缓存及训练优化器状态，展示各分项与假设，避免把训练预设误认为完整估算。

### 覆盖范围
- 本次人工读取 1 页 `tools/ai/vram-estimate.html`；未对 `tools/ai/` 其他页面做逐页审计，未运行页面和门禁。

## 2026-11-03 续查：浏览器本地推理

### AI-N1 成功计算破坏明细和历史宿主（高，确认源码缺陷）
- 证据：`tools/ai/image-classification.html:145-151,324,343-385`、`tools/ai/sentiment-analysis.html:131-135,307,322,349-364`、`tools/ai/text-summarization.html:141-145,311,338-353`、`tools/ai/speech-to-text.html:137-141,310,328-343` 均将表格、历史宿主放入 `result`，成功时用 `innerHTML` 替换全部子节点；随后增强逻辑继续访问已被移除的目标。图像和语音数据表切换还隐藏其父容器（`image-classification.html:470-488`）。
- 影响：以上 4 页的明细、历史、对比或 CSV 目标不可用，图像页图表也受影响；同类已有显存页问题，按页面归并，不混计全站共性条目。
- 方案：主结果、数据表、图表、历史改为独立稳定的同级容器；覆盖成功、失败、预设、标签切换及导出，真实浏览器核验。

### AI-N2 情感与摘要 CSV 调用模块私有函数（中，确认源码缺陷）
- 证据：`tools/ai/sentiment-analysis.html:126,283,349` 和 `tools/ai/text-summarization.html:135,286,338` 的内联按钮调用名称只声明在 `type=module` 中，未暴露到 window，因模块作用域不会作为内联事件的全局函数。
- 影响：`tools/ai/sentiment-analysis.html`、`tools/ai/text-summarization.html`；即使恢复表格宿主，导出按钮仍无法按现状调用目标函数。
- 方案：用事件监听器绑定并提示空表导出失败；覆盖两页点击导出并核对文件内容。

### AI-N3 中文词库命中比例误称置信度，否定句误判（高，确认函数缺陷）
- 证据：`tools/ai/sentiment-analysis.html:235-250,302-307` 以子串命中计数，正负相等选正面，将最大命中占比作为置信度；执行函数时「不好」因命中「好」得到正面 100%，「好差」得到正面 50%。
- 影响：`tools/ai/sentiment-analysis.html`；将启发式比例误作模型概率，否定和平局可产生误导性结论。
- 方案：标识词库规则与局限，将比例改称命中占比；处理否定和平局并展示命中依据，不能暗示概率经校准。

### AI-N4 双声道语音只读取左声道（高，确认源码缺陷）
- 证据：`js/ai-core.js:74-90` 的 `decodeAudioTo16k` 只调用 `getChannelData(0)`；`tools/ai/speech-to-text.html:295-308` 使用其结果转写。左声道全零、右声道有声的模拟输入会输出全零；真实音频识别效果尚未测试。
- 影响：`tools/ai/speech-to-text.html`；右声道独有内容被遗漏。
- 方案：提供声道选择或明确的混音处理，并提示相位抵消风险；用左右独立语音样本验证与展示源音频信息。

### AI-N5 敏感输入历史本地留存且清除入口被移除（高，确认源码路径，浏览器待核验）
- 证据：`tools/ai/sentiment-analysis.html:353-364`、`tools/ai/text-summarization.html:342-353` 将输入前 300 个 UTF-16 码元写入历史；`js/tool-kit.js:1066-1080,1088-1099,1146-1158` 使用 localStorage 并由历史面板提供清除。成功结果覆盖宿主后面板不可见（AI-N1）。这不是已证实的数据上传。
- 影响：`tools/ai/sentiment-analysis.html`、`tools/ai/text-summarization.html`；共享设备上文本可能残留而用户找不到清除入口。
- 方案：敏感文本默认不存历史或明确取得同意，提供独立可见的清除入口并说明本地保留范围；实际检查 localStorage 与清除行为。

### AI-N6 摘要与语音页面说明不符（中，确认源码缺陷）
- 证据：`tools/ai/text-summarization.html:117,124-129,309` 说明可调压缩率/抽取关键句且标「约 60/120/200 字」，实际是生成模型的 `max_new_tokens`；`tools/ai/speech-to-text.html:20,123-127,295-308,391-398` 宣称麦克风 Web Speech API 实时转写，实际提供音频文件输入和 Whisper。
- 影响：`tools/ai/text-summarization.html`、`tools/ai/speech-to-text.html`；功能和输出预期不符。
- 方案：按真实能力改写中英文介绍、FAQ 和示例，解释 token 与字数不等；需要实时录音或压缩比时另行实现。补充首次下载模型、缓存条件及长音频内存需求，具体离线效果待实测。

### 续查覆盖
- 新抽查 `tools/ai/image-classification.html`、`tools/ai/sentiment-analysis.html`、`tools/ai/text-summarization.html`、`tools/ai/speech-to-text.html` 4 页，新增 6 条（其中 4 条高优）；为源码/内存函数证据，未做真实浏览器、网络及线上验证。

## 2026-11-03 续查（并行批 H）

### AI-N7 首个 `calc()` 即覆盖结果容器，图表/数据表/历史宿主从未渲染（高，确认源码缺陷）
- 描述：6 个估算页都把图表、数据表、差值、历史容器放进 `#result`，而主计算函数用 `innerHTML` 整体替换 `#result`；扩展逻辑随后按 id 取宿主，只能拿到 `null`。
- 证据：`tools/ai/token.html:136-141,288`（`#tkChart/#tkTable/#tkDiff/#tkHist` 均在 `#result` 内，`:288` 整体替换）、`tools/ai/token-2.html:137-141,289`、`tools/ai/token-usage.html:136-141,281`、`tools/ai/context-window.html:137-141,292`、`tools/ai/inference-throughput.html:136-141,286`、`tools/ai/quantization-ratio.html:136-141,288`；扩展段目标分别为 `tkChart`(`token.html:313`)、`t2Chart`(`token-2.html:312`)、`tuChart`(`token-usage.html:306`)、`cwChart`(`context-window.html:316`)、`itChart`(`inference-throughput.html:311`)、`qrChart`(`quantization-ratio.html:312`)。`token.html:298` 的裸 `calc()` 先于 `__tkBoot` 执行，故首屏即丢失宿主。
- 影响：以上 6 页的图表、数据表、差值、历史长期为空（"数据表/历史"页签点了也无内容）；`导出 CSV` 也依赖同名表格宿主（`token.html:305` 等），实际无内容可导。主数字结果与预设仍正常。同类问题亦见于 `tools/ai/ai-text-summarizer.html:185-189,397`：`#tzTable/#tzDiff/#tzHist` 位于 `#result` 内，执行摘要后表格与历史被清空（图表在结果区外，仍可用）。
- 方案：把主结果与图表/表格/差值/历史拆成稳定同级容器，计算只写主结果节点；修复后逐页验证首屏、改输入、预设、页签切换、导出与历史回填。

### AI-N8 历史只记录输出值，回填却读取输入字段（高，确认源码缺陷）
- 描述：`history.record` 写入的字段与 `history.mount` 回填读取的字段不是同一组，回填时把输入框写成字符串 `undefined`。
- 证据：`tools/ai/token.html:318,320` 记录 `{tokens}`、回填读 `chars/lang/overlap`；`tools/ai/token-2.html:320,322` 记录 `{total}`、回填读 `input_tokens/output_tokens/input_price/output_price`；`tools/ai/token-usage.html:315,317`、`tools/ai/context-window.html:321,323`、`tools/ai/inference-throughput.html:316,318`、`tools/ai/quantization-ratio.html:320,322` 同样错位。全目录 64 处 `history.mount` 中仅 `min-max`、`dropout`、`cross-entropy`、`sigmoid`、`lr-decay`、`lr-warmup`、`relu-leakyrelu`、`precision-recall`、`ai-prompt-generator` 等少数页面同时记录输入字段。
- 证据（node 内存复算）：按 `token.html:318,320` 的 record/mount 口径复现「记录 `{tokens:334}` → 回填 `chars=v.chars`（`v.tokens!=null` 恒真，未拦住 undefined）」，三个输入在 DOM 侧落为字符串 `undefined`，随后 `+value || 0` 兜底使估算 token 输出 `0`（不是原 334）。
- 影响：本批 6 页及 ai 目录多数同类页的历史点击回填无效或归零，历史面板形同装饰。
- 方案：record 与 mount 使用同一组字段（输入 + 输出），回填前做 `!= null` 判别与数值化，空值不覆盖现有输入；逐页验证「计算两次 → 点历史第一条 → 输入与结果还原」。

### AI-N9 历史写入未合并且首屏即写，20 条槽位被噪音占满（中，确认源码缺陷）
- 描述：`history.record` 支持 `coalesceMs` 合并连续输入，但本批页面全部不传该参数；同时 `__*Boot` 在无用户输入时也调用扩展段，首屏即写入一条默认/空记录。
- 证据：`js/tool-kit.js:1088-1099`（`coalesceMs` 缺省时不合并，仅 `unshift` 后截断 20 条）；`tools/ai/token.html:334-342`、`tools/ai/context-window.html:337-345`、`tools/ai/ai-text-summarizer.html:480-486`、`tools/ai/ai-code-review.html:452-458` 均在 boot 调 `__*Extras`，而扩展段内直接 `record`（`context-window.html:321`、`ai-text-summarizer.html:466`、`ai-code-review.html:438`）。
- 证据（node 内存复算）：`context-window` 默认值 `500/1500/1000/128000` 在无交互时写入 `pct=2.3`；`ai-text-summarizer` 空输入写入 `{text:'',ratio:0}`；`ai-code-review` 空代码写入 `{code:'',issues:0}`。
- 影响：每敲一个字符就新增一条历史，几次输入即把 20 条槽位刷满为同值噪音，真实对比记录被挤掉；首屏空记录还会被用户误认为"上次结果"。
- 方案：`record(obj, 800)` 合并连续输入；boot 阶段只渲染空态、不写历史；历史列表按输入指纹去重，并显示时间与关键输入。

### AI-N10 `token-2` 导出按钮被反向守卫永久拦截（高，确认源码缺陷）
- 描述：`__t2Export` 的守卫写成 `typeof TBKit!='undefined'` 时 return，恰好把唯一可用场景挡掉；该写法在整个 `tools/ai/` 仅此一处。
- 证据：`tools/ai/token-2.html:306`。按同一守卫逻辑在 node 中复现：传入 `TBKit` 桩时分支立即 `return`、`exportTable` 零调用；不传 `TBKit` 时反而进入 `try` 并因 `TBKit` 未定义抛错，被空 `catch` 吞掉。
- 影响：`token-2` 的 CSV 导出始终无效；与 AI-N7 叠加后即使修好宿主也仍无导出。
- 方案：守卫改为 `if(typeof TBKit==='undefined')return;`，并对空表给出提示；修复后点击导出核对文件名与表头。

### AI-N11 `token-2` 单价与币种口径自相矛盾（中，确认源码缺陷）
- 描述：输入与主结果按美元计价，数据表却把同一批数字标成 `¥/百万` 与 `¥`，并额外给出 `×30` 的"月度估算"。
- 证据：`tools/ai/token-2.html:129-130`（标签 `$/1M`）、`:281-288`（输出 `USD`、`CNY` 固定 7.2）、`:317-318`（`input price (¥/M)`、`input cost (¥)`、`monthly est. (×30, ¥)`）、`:146-147`（固定 7.2 汇率说明）。
- 证据（node 内存复算）：默认 `1000/500` token、单价 `2/6` → 主结果总费用 `0.005 USD`；同组数字在表格被标成 `¥0.005`，`×30` 后为 `¥0.1500`，与 `0.005×7.2≈0.036 元` 不符。
- 影响：`token-2`；用户按表头理解会把美元金额当人民币，月度预算低估约 7.2 倍，且"单次×30"并非月度调用量。
- 方案：表头统一 `$/1M` 与 `USD`，人民币列单列并按可编辑汇率换算；删除或改写 `×30` 为"按每日 N 次"的可输入估算；同步修正 `:177` 用 `$0.01/1k` 的示例单位。

### AI-N12 `token` 的英文参考双口径不一致，输入名与公式不符（中，确认源码缺陷）
- 描述：主结果把英文参考固定按 `/1.5` 计算，数据表却用用户输入的 `平均词长`（实为"每 token 字符数/重叠系数"）作分母；同一页同一指标给出两个值。
- 证据：`tools/ai/token.html:282`（`Math.ceil(chars*0.3/1.5)`）、`:315-316`（`Math.ceil(chars*0.3/overlap)`）、`:124`（公式文字写死 `/1.5`）、`:129`（输入标签"平均词长"，公式称"重叠系数"）。
- 证据（node 内存复算）：`chars=500, lang=1, overlap=3` → 主结果"英文参考" `100`，数据表"英文参考 (×0.3)" `50`；另 `0.3` 系数对应 5 字符/token，与 `:125` 文案"英文约 4 字符/token"不一致。
- 影响：`token`；用户改"平均词长"后看到两组不同英文参考，无法判断哪个用于容量规划。
- 方案：英文参考统一口径（建议 `chars/4` 或明确复用同一分母），把输入改名为"每 token 字符数"并给出中英文预设；公式、文案、表格三处同步。

### AI-N13 `token-usage` 深度解析示例与公式方向相反，代码输入单位不符（中，确认源码缺陷）
- 描述：公式按"中文字数÷1.5"，示例却按"500×1.5=750 token"，相差 2.25 倍；输入标签是"代码片段 tokens"，数据表却写作"代码行数"。
- 证据：`tools/ai/token-usage.html:124`（`tokens=中文字数÷1.5+英文词数÷0.75+代码 tokens`）、`:176`（示例 `500×1.5=750`、`200×1.3=260`、合计 `≈1010`）、`:129`（`代码片段 tokens`）、`:313`（`['代码行数', code.toFixed(0)]`）。
- 证据（node 内存复算）：按页面 `calc` 口径 `500/200/0` → `500/1.5+200/0.75=600` token（`toFixed(0)` 显示 `600`）；示例却给 `1010`，且中文项由 333 变成 750。
- 影响：`token-usage`；示例与工具结果对不上，用户会误判中文 token 密度（1.5 token/字 vs 0.67 token/字）；代码项按行数填写则结果偏小数量级。
- 方案：按 `:279` 的表达式重写示例（`500 中文字 + 200 英文词 ≈ 600 token`），中文密度与 `:145` 的口径说明统一；输入与表格统一为"代码 tokens"，并提示需先用分词器计数。

### AI-N14 `inference-throughput` 批处理时延方向与全文相反，指标互不自洽（中，确认源码缺陷）
- 描述：页面正文与 FAQ 反复说"batching 会拉长单请求时延"，图表与表格却用 `耗时÷批大小`（批越大时延越小）；`每 token 毫秒` 用总 token 数，`单请求吞吐` 又按批大小折算，二者无法同时成立。
- 证据：`tools/ai/inference-throughput.html:124`（公式框写"总吞吐…仅由 token 数与耗时决定"，等于声称 `batch` 无关）、`:145`（"并发批量越大人均吞吐越低，batching 以拉长单请求时延换取总吞吐"）、`:125`、`:180`（正文与 FAQ 的"延迟/吞吐取舍"表述）、`:311`（图表 `latency per request` 用 `sec/b`，即"批越大时延越低"）、`:313-314`（`lat` 与 `ms per token` 两行）、`:282-283`（主结果总吞吐与人均吞吐）。
- 证据（node 内存复算）：预设 `tokens=2000, sec=2, batch=4` → 总吞吐 `1000 tok/s`、单请求 `250 tok/s`、单请求时延 `0.5 s`、每 token `1.0 ms`；但按单请求 `250 tok/s` 反推应为 `4.0 ms/token`，且 `0.5 s × 250 tok/s = 125 token/请求` 与输入的 `2000 token` 矛盾。
- 影响：`inference-throughput`；容量规划会把"批越大越快"当结论，与同页 SLO 建议冲突，`ms/token` 与人均吞吐差 4 倍。
- 方案：明确输入语义（总 token/单请求 token、端到端时延/单请求时延），图表改为按实测"批越大单请求时延上升、总吞吐上升"的双轴；`ms/token` 改用单请求 token 数。

### AI-N15 `quantization-ratio` 反向量化时"节省"被取绝对值显示为正（中，确认源码缺陷）
- 描述：当 `量化字节/参 > 原字节/参`（如误填放大）时 `saved` 为负数，饼图库对数值取 `Math.abs`，于是"节省"扇区反被画成正面积，与表格的负节省率互相矛盾。
- 证据：`tools/ai/quantization-ratio.html:311-318`（`saved=before-after` 直接进饼图与表格）、`js/tool-kit.js:468`（`total` 用 `Math.abs`）、`js/tool-kit.js:476`（扇区 `v=Math.abs(...)`）。
- 证据（node 内存复算）：`params=7000, fromB=1, toB=4` → 原 `7000 MB`、新 `28000 MB`、`saved=-21000`、`空间节省率=-300.0%`、压缩比 `0.25×`；饼图入参绝对值 `21000`，与"节省"语义相反。
- 影响：`quantization-ratio`；用户填反字节数时图表显示"保留了 28GB、节省了 21GB"，与实际体积增长矛盾；压缩比仍显示 `0.25×`，三处结论互相打架。
- 方案：`toB>fromB` 时显示"体积增加"并使用正向增长扇区（不经 `Math.abs`）；压缩比继续按 `fromB/toB`，但补充"<1 表示体积变大"提示。

### AI-N16 `ai-text-summarizer` 短句文本落进 NaN 错误分支，关键词为滑窗碎片（中，确认函数缺陷）
- 描述：句子切分只保留 `trim().length > 5` 的句子；当整段文本由 ≤5 字短句组成时句数为 0，压缩比 `0/0=NaN`，被守卫判为"输入无效"；关键词则把同一短语的 2-gram/3-gram 当作多个独立词输出。
- 证据：`tools/ai/ai-text-summarizer.html:300`（`filter(s => s.trim().length > 5)`）、`:368-371`（长度≥50 才进入）、`:378`（`result.length/origSentences.length` 后 NaN 守卫）、`:287-292`（2-gram/3-gram 全量入数组）、`:354-363`（按出现次数排序、无去重/合并）。
- 证据（node 内存复算）：`"天很蓝。"×13`（52 字，满足长度门槛）→ `splitSentences` 得 `0` 句 → 压缩比 `0/0=NaN` → 输出通用错误"⚠ 计算结果含无效值，请检查输入是否为有效正数。"；对示例长文 `keywords(...,5)` 得 `["智能",18] ["人工",10] ["工智",10] ["人工智",10] ["工智能",10]`；英文 `"Machine learning models…"` 得 `["ac",4] ["in",4] ["mo",3]` 等无意义二字母片段。
- 影响：`ai-text-summarizer`；合法的短句清单/口语文本被判"输入无效"，关键词面板中文全是重叠子串、英文全是字母碎片，用户无法得到可用词表。
- 方案：句子切分保留非空短句（或整段兜底为 1 句），压缩比分母为 0 时显示"—"而非报错；关键词改用 `Intl.Segmenter` 分词并合并同源 n-gram（最长匹配去重），英文按单词而非字符 n-gram 计数。

### AI-N17 `ai-code-review` 语言选择器未接线，两种语言审查结果完全相同（中，确认源码缺陷）
- 描述：页面提供 JavaScript/TypeScript 下拉框，但 `review()` 与图表统计均未读取该值；规则集是纯 JS 正则，TypeScript 特有语法没有任何检查。
- 证据：`tools/ai/ai-code-review.html:170`（`select id="lang"`；全文仅此一处定义该 id，无任何脚本按 id 读取它）、`:303-327`（`review()` 只读 `code` 与 `RULES`）、`:549-561`（图表同样只遍历 `RULES`）、`:280-301`（规则集无语言字段）。
- 影响：`ai-code-review`；用户切换语言获得逐字相同的评分与问题清单，形成"已按 TS 审查"的错误预期。
- 方案：要么移除该下拉框，要么给规则加 `lang` 维度并补充 TS 规则（如 `any`、`as` 断言、接口命名）；修复后对比同一段代码在两种语言下的差异输出。

### AI-N18 `ai-code-review` 示例代码被注入守卫片段污染，并制造额外误报（中，确认源码缺陷）
- 描述：`loadSample()` 的模板字符串里混入一段自动生成的 `NaN` 守卫代码（含 `__h4`、`document.getElementById('result').innerHTML=__h4`），示例本身不可运行，并额外触发 `innerHTML` 与 `longLine` 两条告警（`==` 命中的是原示例第 3 行 `if (data == null)`，与注入无关）。
- 证据：`tools/ai/ai-code-review.html:386-400`，其中 `:393` 为注入片段；`:283`（`innerHTML` 规则）、`:296`（`==` 规则）、`:298`（`longLine` 规则）。
- 证据（node 内存复算）：`loadSample()` 生成的示例共 13 行 604 字符，`includes("__h4")===true`、`includes("innerHTML=__h4")===true`；按页面 `RULES` 命中 `eval:[9]`、`innerHTML:[7]`、`debugger:[11]`、`console:[6]`、`var:[2,8,9]`、`==:[3]`、`longLine:[7]`（第 7 行 324 字符）。
- 影响：`ai-code-review`；点"示例代码"后用户看到的是一段带构建残留的乱码式示例；审查该示例时评分 61，且注入行额外制造 `innerHTML`/`longLine` 两条命中。
- 方案：把示例还原为干净的 `const el = '<p>' + data.name + '</p>';` 或改用 `textContent`，删除注入守卫；示例填入后自动触发一次审查，便于对照预期命中。

### AI-N19 "示例代码"只填文本框不重算，结果区保留上一份代码的评分（低，确认源码缺陷）
- 描述：`loadSample()` 仅给 `#code` 赋值，既不调用 `review()` 也不清空 `#scoreBox`/`#result`；换入示例后，屏幕上仍是上一段代码的评分与问题清单。
- 证据：`tools/ai/ai-code-review.html:386-400`（`loadSample` 全程只有一次 `document.getElementById('code').value=...`，`:400` 直接结束）、`:352`（`#scoreBox` 只在 `review()` 内写入）、`:377`（`#result` 只在 `review()` 内写入）。
- 证据（node 内存复算）：用状态桩执行 `review()` 后读取 `scoreBox.innerHTML`，再调用 `loadSample()` 二次读取，字符串完全一致（代码已替换、评分未变）。
- 影响：`ai-code-review`；用户以为看到的是示例的审查结果，实际是旧代码分数，易得出错误结论。
- 方案：`loadSample()` 末尾调用 `review()`（或清空 `scoreBox`/`result` 并提示"点击开始审查"）；按钮文案可改为"载入并审查"。

### AI-N20 计算器页重复渲染两组"相关工具"卡片（低，确认源码缺陷）
- 描述：同一页连续出现两个 `data-related-tools` 区块，前 4 张卡片完全重复，用户会看到重复推荐。
- 证据：`tools/ai/token.html:214-242` 与 `:244-272`（两组各 6 张，`dropout/l1-l2/rag/roc-auc` 重复）；统计 `class="related-tools"` 出现次数：`token.html`、`token-2.html`、`token-usage.html`、`context-window.html`、`inference-throughput.html`、`quantization-ratio.html`、`transformer-params.html` 均为 `2`，`ai-text-summarizer.html`、`ai-code-review.html` 为 `1`。
- 影响：本批 6 个估算页；页尾重复推荐、页面变长，且两组卡片描述截断不一致（如 `relu-leakyrelu` 显示"R ReLU 与 LeakyReLU"）。
- 方案：每页仅保留一组相关工具（保留较新的一组），或合并去重后由构建统一注入；修复后核对卡片数量与去重。

### 留存优化
- `token` / `token-usage` / `token-2` 三页都做 token 估算与成本换算，口径（1.5 字/token vs 1.5 token/字、$/1M vs ¥/M）互相冲突；建议统一到"按分词器实测 + 语言系数可调"的单一口径，页间互相引用，避免用户在三页得到三个答案。
- `context-window.html:127-130` 的窗口上限建议内置 4k/8k/32k/128k 预设，并在超限时对"剩余"着红色；当前只显示负数，缺少显式"已超限 N token"文案（表格内虽有 `已超`，主结果无）。
- `quantization-ratio.html` 可补"量化后仍以 FP16 保存的嵌入/激活"开关，说明 4× 只是权重理论上限，避免把估算当实测体积。
- `inference-throughput.html` 建议把"首 token 延迟"与"每 token 间隔"拆成两个输入，当前只有一个端到端时延，无法覆盖 FAQ 里强调的 TTFT 场景。
- `ai-text-summarizer.html:446-450` 的 3 个预设文本均为 4-5 句，默认抽取 3 句时压缩比高达 60%-75%（`ai-text-summarizer.html:172` 默认值 3），建议补一段 15 句以上的长文预设，才能体现 TextRank 的排序价值。

### 续查覆盖
- 本批新读源码 8 页：`token.html`、`token-2.html`、`token-usage.html`、`context-window.html`、`inference-throughput.html`、`quantization-ratio.html`、`ai-text-summarizer.html`、`ai-code-review.html`（均未在既有条目中覆盖）。
- 新增 14 条（AI-N7 至 AI-N20），其中高优 3 条（AI-N7/AI-N8/AI-N10）。
- 取证方式：逐页读取源码 + node 内存复算（直接 eval 页面函数或按源码表达式重算），证据均为"文件:行号 + 复现输入 → 实际输出"；**未做**浏览器运行时、英文态、移动端、CSV 实际落盘与 `run_gates.py`/`_build.py` 门禁验证。
