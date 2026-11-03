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
