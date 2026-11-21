# AI 工具 · tools/ai（64 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

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
- 🟢 长期增强（2026-11-21 复核：无缺陷项，转后续批次）

## 2026-11-03 审计补充（静态源码复核）

### 留存优化（低，非确认缺陷）
- `tools/ai/vram-estimate.html:124-129,313-314`：目前判据固定为 24GB，建议增加显存容量输入与 8/16/24/48GB 对比，展示余量；保留近似假设说明。
- 同页 `:125,274-283`：总量只加权重和手填激活，建议区分推理 KV 缓存及训练优化器状态，展示各分项与假设，避免把训练预设误认为完整估算。

### 覆盖范围
- 本次人工读取 1 页 `tools/ai/vram-estimate.html`；未对 `tools/ai/` 其他页面做逐页审计，未运行页面和门禁。

## 2026-11-03 续查（并行批 H）

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
