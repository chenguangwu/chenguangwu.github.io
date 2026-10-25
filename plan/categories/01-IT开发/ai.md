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
