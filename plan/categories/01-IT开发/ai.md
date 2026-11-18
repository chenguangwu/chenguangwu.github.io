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

### AI-N5 已下架页面的敏感历史可能仍保留（高，待核验）
- 旧情感分析和摘要页曾通过 `TBKit.history.record` 将输入前 300 个 UTF-16 码元写入 localStorage；`js/tool-kit.js` 以 `tbk_hist_` 加页面路径作为键。页面下架并不自动清除用户浏览器中的旧记录。
- 影响：共享设备上的旧文本可能残留；这不是已证实的数据上传。
- 方案：核实旧路径对应的记录及现有清除入口，验证旧用户能否清除残留。

## 2026-11-03 续查（并行批 H）

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

### AI-N14 `inference-throughput` 批处理时延方向与全文相反，指标互不自洽（中，确认源码缺陷）
- 描述：页面正文与 FAQ 反复说"batching 会拉长单请求时延"，图表与表格却用 `耗时÷批大小`（批越大时延越小）；`每 token 毫秒` 用总 token 数，`单请求吞吐` 又按批大小折算，二者无法同时成立。
- 证据：`tools/ai/inference-throughput.html:124`（公式框写"总吞吐…仅由 token 数与耗时决定"，等于声称 `batch` 无关）、`:145`（"并发批量越大人均吞吐越低，batching 以拉长单请求时延换取总吞吐"）、`:125`、`:180`（正文与 FAQ 的"延迟/吞吐取舍"表述）、`:311`（图表 `latency per request` 用 `sec/b`，即"批越大时延越低"）、`:313-314`（`lat` 与 `ms per token` 两行）、`:282-283`（主结果总吞吐与人均吞吐）。
- 证据（node 内存复算）：预设 `tokens=2000, sec=2, batch=4` → 总吞吐 `1000 tok/s`、单请求 `250 tok/s`、单请求时延 `0.5 s`、每 token `1.0 ms`；但按单请求 `250 tok/s` 反推应为 `4.0 ms/token`，且 `0.5 s × 250 tok/s = 125 token/请求` 与输入的 `2000 token` 矛盾。
- 影响：`inference-throughput`；容量规划会把"批越大越快"当结论，与同页 SLO 建议冲突，`ms/token` 与人均吞吐差 4 倍。
- 方案：明确输入语义（总 token/单请求 token、端到端时延/单请求时延），图表改为按实测"批越大单请求时延上升、总吞吐上升"的双轴；`ms/token` 改用单请求 token 数。

### AI-N16 `ai-text-summarizer` 关键词为滑窗碎片（中，确认函数缺陷）
- 已修（971 批）：短句文本 0/0=NaN 假合规——`splitSentences` 由 `trim().length>5` 改为 `>0` 保留非空短句、压缩比分母为 0 显示"—"，真机回放 5/5 通过（"天很蓝。"×13 → 原句数 13、压缩比 23%）。
- 残留描述：关键词把同一短语的 2-gram/3-gram 当作多个独立词输出。证据 `tools/ai/ai-text-summarizer.html:287-292`（2-gram/3-gram 全量入数组）、`:354-363`（按出现次数排序、无去重/合并）。node 内存复算：示例长文 `keywords(...,5)` 得 `["智能",18] ["人工",10] ["工智",10] ["人工智",10] ["工智能",10]`；英文 `"Machine learning models…"` 得 `["ac",4] ["in",4] ["mo",3]` 等无意义二字母片段。
- 影响：`ai-text-summarizer` 关键词面板中文全是重叠子串、英文全是字母碎片，用户无法得到可用词表。
- 方案（需算法重做/专业裁断）：关键词改用 `Intl.Segmenter` 分词并合并同源 n-gram（最长匹配去重），英文按单词而非字符 n-gram 计数。

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
