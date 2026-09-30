# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch6（剩余工具第 4 批 10 个）。逐条语义化翻译；值纯英文避开 CJK/中文标点。
内置校验：每个 work json 的 zh（含 name）必须有译文；译文键必须对应 work json 的 zh，否则报错/告警。"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'ai')

def verify(slug, name_zh, mp):
    path = os.path.join(WORK, slug + '.json')
    with open(path, encoding='utf-8') as f:
        wj = json.load(f)
    required = set(it['zh'] for it in wj.get('items', []))
    required.add(name_zh)
    for zh in required:
        if zh not in mp:
            print('MISSING translation for', repr(zh), 'in', slug)
            sys.exit(1)
    extra = set(mp.keys()) - required
    if extra:
        print('WARN unused keys in', slug, ':', sorted(extra))
    return

# ---------------- speech-to-text 语音转文字 ----------------
ST = {
    '🤖 语音转文字': '🤖 Speech to Text',
    '基于 Transformers.js 在浏览器本地运行 Whisper 模型，将音频转换为文字，数据不上传。': 'Runs the Whisper model locally in the browser via Transformers.js to convert audio into text, with no data upload.',
    '📖 查看「语音转文字使用指南」': '📖 View "Speech to Text User Guide"',
    '选择音频': 'Select audio',
    '开始转换': 'Start conversion',
    '本工具在浏览器本地解码音频并加载 Whisper 模型转写文字，支持 mp3 / wav / m4a 等格式，全程不上传。': 'This tool decodes audio locally in the browser and loads the Whisper model to transcribe text, supporting mp3 / wav / m4a and more, with no upload at any stage.',
    '📚 深度解析：语音转文字': '📚 Deep Dive: Speech to Text',
    '在浏览器本地用 Web Speech API 将麦克风录音实时识别为中文文本。': 'Uses the Web Speech API in the browser to recognize microphone audio into Chinese text in real time.',
    '纯前端、不上传音频，保护隐私；适合会议纪要、字幕与速记。': 'Pure front-end, no audio upload, privacy-preserving; suited to meeting notes, subtitles and transcription.',
    '识别受口音、噪声与网络语音引擎可用性影响，长段需分段校对。': 'Recognition is affected by accent, noise and the availability of the network speech engine; long passages need segment-by-segment proofreading.',
    '本地转写': 'Local transcription',
    '点击录音后口述\'明天上午十点开会\'，工具实时返回\'明天上午十点开会\'。环境嘈杂或含专有名词时可能误识，需人工核对关键点。': "After clicking record and saying 'Meeting at 10am tomorrow', the tool returns 'Meeting at 10am tomorrow' in real time. In noisy environments or with proper nouns it may misrecognize, so verify key points manually.",
    '为什么有时识别不了？': 'Why does it sometimes fail to recognize?',
    'Web Speech API 在部分浏览器/环境需联网调用系统语音引擎，离线或无权限时会失败；口音重、噪声大也会降准。': 'The Web Speech API needs to call the system speech engine online in some browsers/environments and fails offline or without permission; heavy accents and loud noise also lower accuracy.',
    '录音会泄露吗？': 'Will the recording leak?',
    '本工具在浏览器内处理、不上传；但是否真正本地取决于浏览器实现，部分引擎仍会调用云端识别服务，敏感内容需确认。': 'This tool processes inside the browser with no upload; but whether it is truly local depends on the browser implementation, and some engines still call cloud recognition services, so confirm before handling sensitive content.',
    '语音转文字': 'Speech to Text',
}
verify('speech-to-text', '语音转文字', ST)
apply_tool('speech-to-text', '语音转文字', 'Speech to Text', ST, ind=IND)

# ---------------- steps-per-epoch 每轮训练步数 ----------------
SP = {
    '🧮 每轮训练步数': '🧮 Steps per Epoch',
    '由数据集与批次计算每轮训练步数。': 'Compute the number of training steps per epoch from the dataset and batch size.',
    '📖 查看「每轮训练步数使用指南」': '📖 View "Steps per Epoch User Guide"',
    '每卡步数 = ⌈样本数 / 批量⌉；每步覆盖样本 = 批量 × 卡数': 'Steps per GPU = ceil(samples / batch); samples covered per step = batch x GPUs',
    '多卡数据并行时，全局批量 = 单卡批量 × 卡数，每卡步数不变但每步实际看到的样本翻倍数等于卡数。因此扩卡后要保持等效训练强度，需按比例调大学习率或增加轮数。': 'With multi-GPU data parallelism, global batch = per-GPU batch x GPU count; per-GPU steps stay the same but each step sees samples multiplied by the GPU count. To keep equivalent training intensity after scaling up, raise the learning rate or add epochs proportionally.',
    '数据集大小': 'Dataset size',
    '批次大小': 'Batch size',
    '步数 = ⌈数据/批次⌉': 'Steps = ceil(data / batch)',
    '分布式下每卡步数不变，总样本覆盖相同。': 'Under distribution, per-GPU steps are unchanged and total sample coverage is the same.',
    '📚 深度解析：每轮训练步数': '📚 Deep Dive: Steps per Epoch',
    '每轮步数 steps=⌈数据集样本数/batch_size⌉，决定单轮迭代次数。': 'Steps per epoch = ceil(dataset size / batch_size), determining the number of iterations per epoch.',
    '分布式下每卡步数=⌈N/(batch×world_size)⌉，注意尾批与丢弃策略。': 'Under distribution per-GPU steps = ceil(N / (batch x world_size)); mind the tail batch and drop strategy.',
    '步数×单步耗时≈单轮时长，是训练排期与进度估算的基础。': 'Steps x per-step time ~ epoch duration, the basis for training scheduling and progress estimation.',
    '步数计算': 'Step calculation',
    'N=50000, batch=64 → steps=⌈50000/64⌉=782 步/轮。4 卡数据并行每卡 batch=64 则每卡 782 步(总样本不变)，等效 batch=256 使收敛更快。': 'N=50000, batch=64 -> steps=ceil(50000/64)=782 steps/epoch. With 4 GPUs data-parallel and per-GPU batch=64, each GPU does 782 steps (total samples unchanged); the effective batch=256 converges faster.',
    '分布式每卡步数变少吗？': 'Do per-GPU steps decrease under distribution?',
    '若每卡 batch 不变，每卡处理的样本数减少，步数按每卡样本算会减少；总计算量不变，只是并行加速，等效 batch 变大了。': 'If per-GPU batch stays the same, each GPU processes fewer samples, so steps counted per GPU decrease; total compute is unchanged, only parallel-accelerated, and the effective batch grows.',
    '尾批怎么影响步数？': 'How does the tail batch affect steps?',
    '向上取整已含尾批(不足 batch 的余量)。若启用 drop_last 则步数=⌊N/batch⌋，少算一个不完整批，需在指标上对应处理。': 'Ceiling already includes the tail batch (the remainder below one batch). If drop_last is enabled, steps = floor(N / batch), dropping one incomplete batch, which must be handled in the metrics.',
    '每轮训练步数': 'Steps per Epoch',
}
verify('steps-per-epoch', '每轮训练步数', SP)
apply_tool('steps-per-epoch', '每轮训练步数', 'Steps per Epoch', SP, ind=IND)

# ---------------- temperature-scaling 温度缩放 Logits ----------------
TS = {
    '🖼️ 温度缩放 Logits': '🖼️ Temperature-Scaled Logits',
    '演示 softmax 前对 logits 做温度缩放。': 'Demonstrates temperature scaling of logits before softmax.',
    '📖 查看「温度缩放 Logits使用指南」': '📖 View "Temperature-Scaled Logits User Guide"',
    'z′ = z/T（T>1 平滑分布，T<1 锐化分布）': "z' = z/T (T>1 smooths the distribution, T<1 sharpens it)",
    '对 logits 统一除以温度是最简单的概率校准手段，T 在验证集上用 NLL 搜索得到，不改变 argmax 因此不影响准确率，只改善置信度的可靠性（ECE）。它只能校正整体过度/不足自信，无法修正逐类别偏差。': 'Dividing logits uniformly by a temperature is the simplest probability calibration; T is found on the validation set by minimizing NLL. It does not change the argmax, so accuracy is unaffected, only the reliability of confidence (ECE) improves. It can only correct overall over/under-confidence, not per-class bias.',
    'logit 值': 'Logit value',
    '对比 logit': 'Comparison logit',
    'scaled = logit / T；T>1 更平滑，T<1 更尖锐': 'scaled = logit / T; T>1 smoother, T<1 sharper',
    '仅用于演示 softmax 前缩放，不改变 argmax。': 'Only for demonstrating pre-softmax scaling; does not change the argmax.',
    '📚 深度解析：温度缩放 Logits': '📚 Deep Dive: Temperature-Scaled Logits',
    '在 softmax 前对 logits 做 z/T，演示温度对概率形态的影响，不改变 argmax。': 'Applying z/T to logits before softmax shows how temperature shapes the probability distribution, without changing the argmax.',
    'T>1 平滑分布(置信度降低)，T<1 锐化(更自信)，是模型校准常用手段。': 'T>1 smooths the distribution (lower confidence), T<1 sharpens it (more confident); a common model-calibration technique.',
    '与生成温度同源：同一机制既可用于校准也可调生成多样性。': 'Shares the same mechanism as generation temperature: one mechanism serves both calibration and tuning generation diversity.',
    '校准演示': 'Calibration demo',
    'logits=[3,1,0]，T=1 → 概率≈[0.8438,0.1142,0.0420]；T=2 → [0.6285,0.2312,0.1402]，最高概率由 84.38% 降到 62.85%，更接近真实准确率即达到校准目的；T=0.5 → [0.9796,0.0179,0.0024] 过度自信。注意缩放只改数值大小，argmax 仍是第 1 类。': 'logits=[3,1,0], T=1 -> prob ~[0.8438,0.1142,0.0420]; T=2 -> [0.6285,0.2312,0.1402], the max probability drops from 84.38% to 62.85%, closer to true accuracy and thus calibrated; T=0.5 -> [0.9796,0.0179,0.0024] overconfident. Note scaling only changes magnitudes, argmax stays class 1.',
    '温度缩放能提升准确率吗？': 'Can temperature scaling improve accuracy?',
    '不直接提升': 'Not directly',
    '分类准确率': 'Classification accuracy',
    '(argmax 不变)，只让输出置信度更\'诚实\'地反映正确率，对需要可靠概率的应用(如风险决策)很有价值。': "(argmax unchanged), it only makes the output confidence more 'honest' about the true accuracy, valuable for applications needing reliable probabilities (e.g. risk decisions).",
    'T 用什么值校准？': 'What T value is used for calibration?',
    '在验证集上用负对数似然最小化搜索最优 T(通常略大于 1)，使预测置信度与经验准确率对齐；是后处理、不改模型权重。': 'On the validation set, search for the optimal T by minimizing negative log-likelihood (usually slightly above 1) so predicted confidence aligns with empirical accuracy; it is post-processing and does not change model weights.',
    '温度缩放 Logits': 'Temperature-Scaled Logits',
}
verify('temperature-scaling', '温度缩放 Logits', TS)
apply_tool('temperature-scaling', '温度缩放 Logits', 'Temperature-Scaled Logits', TS, ind=IND)

# ---------------- text-summarization 文本摘要 ----------------
TX = {
    '#️⃣ 文本摘要': '#️⃣ Text Summarizer',
    '基于 Transformers.js 在浏览器本地运行 BART 模型，将长文压缩为简洁摘要，数据不上传。': 'Runs the BART model locally in the browser via Transformers.js to compress long text into a concise summary, with no data upload.',
    '📖 查看「文本摘要使用指南」': '📖 View "Text Summarizer User Guide"',
    '短（~60 字）': 'Short (~60 chars)',
    '中（~120 字）': 'Medium (~120 chars)',
    '长（~200 字）': 'Long (~200 chars)',
    '本工具在浏览器本地加载摘要模型，对输入文本生成摘要（英文较长段落效果最佳），全程不上传。': 'This tool loads a summarization model locally in the browser and generates a summary for the input text (best on longer English passages), with no upload at any stage.',
    '📚 深度解析：文本摘要': '📚 Deep Dive: Text Summarizer',
    '在浏览器本地用 NLP 抽取关键句生成摘要，支持调节压缩比，文本不上传。': 'Uses NLP locally in the browser to extract key sentences into a summary, supports adjusting the compression ratio, and does not upload text.',
    '抽取式摘要忠于原文、零上传零成本，适合长文速读；改写式需云端大模型。': 'Extractive summarization stays faithful to the source, zero upload and zero cost, suited to quick reading of long texts; abstractive needs a cloud LLM.',
    '摘要质量依赖句子重要性打分，建议人工复核关键结论。': 'Summary quality depends on sentence-importance scoring; manual review of key conclusions is recommended.',
    '压缩比调节': 'Compression ratio tuning',
    '一篇 2000 字报告，设压缩比 20% → 抽取约 400 字关键句。若关键事件集中在开头，摘要可能偏向前段，需检查是否覆盖尾段要点。': 'A 2000-character report at 20% compression -> about 400 characters of key sentences extracted. If key events cluster at the start, the summary may skew to the front, so check whether the tail points are covered.',
    '抽取式和生成式摘要差在哪？': 'What is the difference between extractive and abstractive summarization?',
    '抽取式只挑原文句子、不动写、本地零成本；生成式可重写更连贯但需联网/算力且文本外发。按隐私与流畅度需求取舍。': 'Extractive only picks original sentences, does not rewrite, zero local cost; abstractive can rewrite more coherently but needs network/compute and sends text out. Choose by privacy and fluency needs.',
    '摘要遗漏重点怎么办？': 'What if the summary misses key points?',
    '调高抽取比例或换句子打分策略；关键句被埋没时常因权重算法偏向位置，可结合关键词加权或人工指定重点。': 'Raise the extraction ratio or switch the sentence-scoring strategy; key sentences are often buried because the weighting algorithm favors position, so add keyword weighting or manually specify priorities.',
    '粘贴一段较长的中文或英文文章…': 'Paste a longer Chinese or English article...',
    '文本摘要': 'Text Summarizer',
}
verify('text-summarization', '文本摘要', TX)
apply_tool('text-summarization', '文本摘要', 'Text Summarizer', TX, ind=IND)

# ---------------- token Token 数量估算 ----------------
TK = {
    '🔑 Token 数量估算': '🔑 Token Count Estimator',
    '根据文本长度估算大模型 Token 数量。': 'Estimate the token count of a large model from text length.',
    '📖 查看「Token 数量估算使用指南」': '📖 View "Token Count Estimator User Guide"',
    '估算 token 数 = ⌈字符数 × 语言系数 / 重叠系数⌉；英文参考 = ⌈字符数 × 0.3 / 1.5⌉；成本 ≈ token 数 / 10⁶ × 单价': 'Estimated tokens = ceil(characters x language factor / overlap factor); English reference = ceil(characters x 0.3 / 1.5); cost ~ tokens / 10^6 x unit price',
    '不同语言与分词器的压缩率差异很大：中文常约 1–1.5 字符/token，英文约 4 字符/token。此式为量级估算，精确计费必须调用对应模型的官方 tokenizer；代码与数字因切分更碎，实际 token 数常高于纯文本估计。': 'Compression ratios vary widely by language and tokenizer: Chinese is often about 1-1.5 chars/token, English about 4 chars/token. This formula is an order-of-magnitude estimate; exact billing must call the model official tokenizer; code and numbers split finer, so actual tokens often exceed the plain-text estimate.',
    '语言系数 1=中文 0.3=英文': 'Language factor: 1=Chinese, 0.3=English',
    '中文 ≈ 0.6-1 token/字': 'Chinese ~ 0.6-1 token/char',
    '英文 ≈ 0.2-0.25 token/字': 'English ~ 0.2-0.25 token/char',
    '不同分词器结果差异较大。': 'Results differ greatly across tokenizers.',
    '📚 深度解析：Token 数量估算': '📚 Deep Dive: Token Count Estimator',
    '根据文本长度与语言比例估算大模型 token 数，帮助用户把控上下文窗口。': 'Estimate large-model token counts from text length and language ratio, helping users manage the context window.',
    '中文约每 1~2 字 1 token，英文约每 4 字符 1 token，具体随分词器变化。': 'Chinese is about 1 token per 1-2 chars, English about 1 token per 4 chars; details vary by tokenizer.',
    '估算用于预判 API 调用成本与是否触发上下文截断。': 'The estimate is used to predict API call cost and whether context truncation is triggered.',
    '长度估算': 'Length estimate',
    '一段 800 中文字的文本，按 1.5 字/token 估算≈533 token；若叠加 200 英文词≈260 token，合计≈793 token，接近 1k 上下文占用的 80%。': 'An 800-Chinese-character text at 1.5 chars/token ~ 533 tokens; adding 200 English words ~ 260 tokens, total ~ 793 tokens, about 80% of a 1k context.',
    '估算和真实计费差多少？': 'How far is the estimate from real billing?',
    '量级基本一致，精确值取决于具体模型分词器；中文差异可能被放大数倍，正式计费以厂商返回 token 数为准。': 'The order of magnitude is basically consistent; the exact value depends on the specific model tokenizer; Chinese differences can be amplified several times, and official billing uses the token count returned by the vendor.',
    '怎么避免超出上下文？': 'How to avoid exceeding the context?',
    '先在本地估算文本 token，长文本做摘要或分块，预留生成空间(通常留 20%~30%)，避免触发截断导致信息丢失。': 'First estimate text tokens locally; summarize or chunk long texts, and reserve generation space (usually 20%-30%) to avoid truncation and information loss.',
    'Token 数量估算': 'Token Count Estimator',
}
verify('token', 'Token 数量估算', TK)
apply_tool('token', 'Token 数量估算', 'Token Count Estimator', TK, ind=IND)

# ---------------- token-2 提示词 Token 成本 ----------------
TK2 = {
    '🔑 提示词 Token 成本': '🔑 LLM Token Cost Estimator',
    '估算 LLM API 输入输出 Token 费用。': 'Estimate LLM API input and output token costs.',
    '📖 查看「提示词 Token 成本使用指南」': '📖 View "LLM Token Cost Estimator User Guide"',
    '输入费用 = 输入 tokens / 10⁶ × 输入单价；输出费用 = 输出 tokens / 10⁶ × 输出单价；人民币 ≈ 美元 × 汇率': 'Input cost = input tokens / 10^6 x input unit price; output cost = output tokens / 10^6 x output unit price; CNY ~ USD x exchange rate',
    '大模型 API 普遍按输入与输出分别计价，且输出单价通常高于输入，因此压缩提示词与控制生成长度都能直接省钱。换算人民币时汇率按当期取值，另需考虑批量/缓存折扣与最低计费粒度。': 'LLM APIs generally price input and output separately, and output unit price is usually higher than input, so compressing prompts and controlling generation length both save money directly. When converting to CNY, use the current exchange rate, and also consider batch/cache discounts and minimum billing granularity.',
    '输入 Token 数': 'Input tokens',
    '输出 Token 数': 'Output tokens',
    '输入单价 $/1M': 'Input price $/1M',
    '输出单价 $/1M': 'Output price $/1M',
    '费用 = Token 数 × 单价 / 1,000,000': 'Cost = tokens x unit price / 1,000,000',
    '汇率按 1 USD ≈ 7.2 CNY 估算。': 'Exchange rate estimated at 1 USD ~ 7.2 CNY.',
    '📚 深度解析：提示词 Token 成本': '📚 Deep Dive: LLM Token Cost Estimator',
    '费用=输入 token×输入单价+输出 token×输出单价，按模型计费口径估算。': 'Cost = input tokens x input price + output tokens x output price, estimated by the model billing basis.',
    '支持按 1 USD≈7.2 CNY 折算人民币，辅助调用预算与成本对比。': 'Supports converting to CNY at 1 USD ~ 7.2 CNY to aid call budgeting and cost comparison.',
    '不同模型分词器差异大，token 数需以对应模型为准，本估算为量级参考。': 'Tokenizers differ greatly across models; token counts must follow the corresponding model, and this estimate is an order-of-magnitude reference.',
    '成本估算': 'Cost estimate',
    '输入 10k token($0.01/1k)、输出 2k token($0.03/1k) → 费用=10×0.01+2×0.03=0.16 USD≈1.15 元。批量调用前用此预判账单。': 'Input 10k tokens ($0.01/1k), output 2k tokens ($0.03/1k) -> cost = 10 x 0.01 + 2 x 0.03 = 0.16 USD ~ 1.15 CNY. Use this to predict the bill before batch calls.',
    '为什么不同模型费用差很多？': 'Why do different models differ so much in cost?',
    '单价随模型能力与上下文长度差异大，且输入输出单价常不同；大上下文/强模型更贵，选型需权衡效果与成本。': 'Unit price varies greatly with model capability and context length, and input/output prices often differ; larger context / stronger models cost more, so weigh effect vs cost when choosing.',
    '估算的 token 数准吗？': 'Is the estimated token count accurate?',
    '不准到精确位。中文在 GPT/Claude/国产模型下 token 数差异明显，本工具给量级参考，精确计费以厂商账单为准。': 'Not accurate to the exact figure. Chinese token counts differ noticeably across GPT/Claude/domestic models; this tool gives an order-of-magnitude reference, and exact billing follows the vendor invoice.',
    '提示词 Token 成本': 'LLM Token Cost Estimator',
}
verify('token-2', '提示词 Token 成本', TK2)
apply_tool('token-2', '提示词 Token 成本', 'LLM Token Cost Estimator', TK2, ind=IND)

# ---------------- token-usage Token 用量估算 ----------------
TKU = {
    '🔑 Token 用量估算': '🔑 Token Usage Estimator',
    '按中英文与代码估算 token 用量。': 'Estimate token usage by the mix of Chinese, English and code.',
    '📖 查看「Token 用量估算使用指南」': '📖 View "Token Usage Estimator User Guide"',
    'tokens ≈ 中文字数 / 1.5 + 英文词数 / 0.75 + 代码字符数': 'tokens ~ Chinese chars / 1.5 + English words / 0.75 + code characters',
    '混合内容按三类分别折算：中文按字符、英文按词、代码按字符（切分最碎）。这是粗略预算工具，实际值随分词器与符号密度浮动 ±20%，用于判断是否接近上下文上限时应留出安全余量。': 'Mixed content is converted by three classes: Chinese by character, English by word, code by character (split finest). This is a rough budgeting tool; actual values fluctuate +/-20% with tokenizer and symbol density, so leave a safety margin when judging whether you are near the context limit.',
    '中文字数': 'Chinese characters',
    '英文词数': 'English words',
    '代码片段 tokens': 'Code snippet tokens',
    '中文≈字数/1.5，英文≈词数/0.75': 'Chinese ~ chars/1.5, English ~ words/0.75',
    '不同分词器差异较大，仅供参考。': 'Tokenizers differ greatly; for reference only.',
    '📚 深度解析：Token 用量估算': '📚 Deep Dive: Token Usage Estimator',
    '按中英文与代码比例估算文本 token 数，提示不同分词器差异。': 'Estimate text token counts by the ratio of Chinese, English and code, and note the differences across tokenizers.',
    '中文约 1~2 字/token(因模型而异)，英文约 4 字符/token，代码密度更高。': 'Chinese is about 1-2 chars/token (model-dependent), English about 4 chars/token, and code is denser.',
    '估算用于把控上下文窗口与 API 成本，精确值需对应模型分词器计数。': 'The estimate helps manage the context window and API cost; the exact value needs the corresponding model tokenizer count.',
    '中英混排估算': 'Chinese-English mixed estimate',
    '一段 500 中文字+200 英文词：中文≈500×1.5=750 token，英文≈200×1.3=260 token，合计≈1010 token。实际因模型分词不同会有偏差。': 'A passage of 500 Chinese chars + 200 English words: Chinese ~ 500 x 1.5 = 750 tokens, English ~ 200 x 1.3 = 260 tokens, total ~ 1010 tokens. Actual results deviate by model tokenizer.',
    '为什么中文 token 数不固定？': 'Why is the Chinese token count not fixed?',
    '不同模型对中文的子词切分不同(按字/按词/混合)，同一段中文 token 数可差数倍；本估算仅给量级，精确需对应分词器。': 'Different models subword-split Chinese differently (by char / by word / mixed), so the same Chinese passage can differ several times in token count; this estimate only gives magnitude, and exact counts need the corresponding tokenizer.',
    '代码为什么更费 token？': 'Why does code consume more tokens?',
    '代码含大量符号、缩进与标识符，信息密度高、子词切分更碎，同等字符数常比自然语言消耗更多 token。': 'Code contains many symbols, indentation and identifiers, with high information density and finer subword splits, so the same character count often consumes more tokens than natural language.',
    'Token 用量估算': 'Token Usage Estimator',
}
verify('token-usage', 'Token 用量估算', TKU)
apply_tool('token-usage', 'Token 用量估算', 'Token Usage Estimator', TKU, ind=IND)

# ---------------- training-flops 训练算力需求 ----------------
TF = {
    '🧮 训练算力需求': '🧮 Training Compute Estimator',
    '用 Kaplan 缩放律估算训练总算力。': 'Estimate total training compute with Kaplan scaling laws.',
    '📖 查看「训练算力需求使用指南」': '📖 View "Training Compute Estimator User Guide"',
    '训练 FLOPs ≈ 6·N·D（N 为参数量，D 为训练 token 数）；训练月数 ≈ 6ND / (卡数 × 单卡算力 × 3600 × 24 × 30)': 'Training FLOPs ~ 6 x N x D (N = parameters, D = training tokens); training months ~ 6ND / (GPU count x per-GPU compute x 3600 x 24 x 30)',
    'Transformer 训练的经验法则：前向 2N、反向约 4N，合计每 token 约 6N FLOPs，即 Chinchilla 系列缩放律推导的基础。再除以集群有效算力（须乘 MFU，实际常 30%–50%）得到训练周期。': 'The empirical rule for Transformer training: forward 2N, backward about 4N, total about 6N FLOPs per token, the basis of the Chinchilla-family scaling laws. Divide by the cluster effective compute (must multiply MFU, usually 30%-50% in practice) to get the training period.',
    '参数量(亿)': 'Parameters (100M)',
    '训练 tokens(亿)': 'Training tokens (100M)',
    'C ≈ 6·N·D（Kaplan 估算）': 'C ~ 6 x N x D (Kaplan estimate)',
    'N、D 单位需一致，结果数量级参考。': 'N and D must use consistent units; the result is an order-of-magnitude reference.',
    '📚 深度解析：训练算力需求': '📚 Deep Dive: Training Compute Estimator',
    'Kaplan 缩放律：训练 FLOPs≈6·N·D，N 为参数量、D 为训练 token 数。': 'Kaplan scaling law: training FLOPs ~ 6 x N x D, where N is parameters and D is training tokens.',
    '前向约 2ND、反向约 4ND，合计 6ND；用于大模型算力与时间表规划。': 'Forward about 2ND, backward about 4ND, total 6ND; used for large-model compute and timeline planning.',
    '实际受并行效率、通信与显存限制，理论值需乘开销系数。': 'In practice limited by parallel efficiency, communication and memory; multiply the theoretical value by an overhead factor.',
    '7B 模型算力': '7B model compute',
    'N=7×10⁹, D=1×10¹² → FLOPs≈6×7e9×1e12=4.2×10²²。按 1e15 FLOPs/s(约 1 PFLOPS 有效)需≈4.2e7 秒≈487 天单卡；实际靠千卡集群并行缩短。': 'N=7x10^9, D=1x10^12 -> FLOPs ~ 6 x 7e9 x 1e12 = 4.2x10^22. At 1e15 FLOPs/s (about 1 effective PFLOPS) it needs ~ 4.2e7 seconds ~ 487 days on a single GPU; in practice a thousand-GPU cluster parallelizes to shorten this.',
    '6ND 是上限还是典型值？': 'Is 6ND an upper bound or a typical value?',
    '6ND 是前向+反向的理论下界(理想乘加计数)，实际含激活重算、通信与低效会更高；规划时乘以 1.5~3 倍余量更稳妥。': '6ND is the theoretical lower bound of forward+backward (ideal multiply-add count); in practice activation recompute, communication and inefficiency raise it; for planning, multiply by a 1.5-3x margin to be safe.',
    '参数量和训练数据哪个更耗算力？': 'Which consumes more compute, parameters or training data?',
    '二者线性相乘，等比例增。但现代训练常\'数据受限\'，即数据量不足以让参数充分训练，此时加数据比加参数更划算(直到 Chinchilla 最优点)。': "They multiply linearly and scale proportionally. But modern training is often 'data-limited', meaning data is insufficient to train parameters fully, so adding data is more cost-effective than adding parameters (until the Chinchilla optimum).",
    '训练算力需求': 'Training Compute Estimator',
}
verify('training-flops', '训练算力需求', TF)
apply_tool('training-flops', '训练算力需求', 'Training Compute Estimator', TF, ind=IND)

# ---------------- transformer-params Transformer 参数量 ----------------
TP = {
    '🏋️ Transformer 参数量': '🏋️ Transformer Parameter Estimator',
    '估算 Transformer 主体与嵌入参数量。': 'Estimate the body and embedding parameter count of a Transformer.',
    '📖 查看「Transformer 参数量使用指南」': '📖 View "Transformer Parameter Estimator User Guide"',
    '主体参数 ≈ 12·L·d²；嵌入参数 ≈ vocab × d': 'Body params ~ 12 x L x d^2; embedding params ~ vocab x d',
    '每层含 Q/K/V/O 四个 d×d 矩阵（4d²）与两层 FFN（通常 4d 宽，共 8d²），合计 12d²，乘层数 L 即得主体规模；词表嵌入另计 vocab×d（若解绑则输出层再加一份）。实际模型还有 LayerNorm 等小量参数，估算值略偏小。': 'Each layer has four d x d matrices Q/K/V/O (4d^2) and two FFN layers (usually 4d wide, total 8d^2), summing to 12d^2, times layer count L gives the body size; the vocabulary embedding is counted separately as vocab x d (plus one more copy at the output if untied). Real models also have small parameters like LayerNorm, so the estimate is slightly low.',
    '隐藏维度': 'Hidden dimension',
    '词表大小': 'Vocabulary size',
    '近似 12·L·d²（含注意力与 FFN）': '~ 12 x L x d^2 (attention + FFN)',
    '实际随具体架构大幅浮动。': 'Actual values vary widely with the specific architecture.',
    '📚 深度解析：Transformer 参数量': '📚 Deep Dive: Transformer Parameter Estimator',
    '标准 Transformer 每层参数量≈12·L·d²(L 层数、d 模型维度)，含自注意力与 FFN。': 'A standard Transformer has about 12 x L x d^2 parameters per layer (L layers, d model dimension), including self-attention and FFN.',
    'token 嵌入≈V·d(V 词表大小)，位置编码若可学习再加 d 或 V·d。': 'Token embedding ~ V x d (V vocabulary size); if positional encoding is learnable, add d or V x d.',
    '总参数量用于显存与算力预算，是模型规模评估的核心指标。': 'Total parameter count is used for memory and compute budgeting and is the core metric for model-scale assessment.',
    '参数量估算': 'Parameter estimation',
    'L=12, d=768, V=50000：每层≈12×768²≈7.08M，12 层≈85M；嵌入 50000×768≈38.4M；合计≈123M(典型 BERT-base 量级)。': 'L=12, d=768, V=50000: per layer ~ 12 x 768^2 ~ 7.08M, 12 layers ~ 85M; embedding 50000 x 768 ~ 38.4M; total ~ 123M (typical BERT-base scale).',
    '为什么 FFN 占参数最多？': 'Why does FFN hold the most parameters?',
    '标准 FFN 内部维度常 4d，其两层权重约 8d²，而注意力 Q/K/V/O 共 4d²，故 FFN 占每层约 2/3 参数；这也是大模型压缩的重点。': 'A standard FFN inner dimension is often 4d, its two weight layers about 8d^2, while attention Q/K/V/O totals 4d^2, so FFN holds about 2/3 of each layer parameters; it is also the focus of large-model compression.',
    '词表越大参数越多吗？': 'Does a larger vocabulary mean more parameters?',
    '是。嵌入层≈V·d 随词表线性增长；为控参数量常用子词分词限制 V，或用因子分解嵌入降低维度开销。': 'Yes. The embedding layer ~ V x d grows linearly with the vocabulary; to control parameters, subword tokenization is commonly used to limit V, or factorized embeddings reduce the dimension cost.',
    'Transformer 参数量': 'Transformer Parameter Estimator',
}
verify('transformer-params', 'Transformer 参数量', TP)
apply_tool('transformer-params', 'Transformer 参数量', 'Transformer Parameter Estimator', TP, ind=IND)

# ---------------- vram-estimate 模型显存估算 ----------------
VR = {
    '🔮 模型显存估算': '🔮 Model VRAM Estimator',
    '按参数量与字节数估算权重显存。': 'Estimate weight VRAM from parameter count and bytes.',
    '📖 查看「模型显存估算使用指南」': '📖 View "Model VRAM Estimator User Guide"',
    '权重显存 ≈ 参数量 × 每参数字节数；总显存 ≈ 权重 + 激活/1000': 'Weight VRAM ~ parameters x bytes per param; total VRAM ~ weights + activation/1000',
    '推理显存主要由权重决定：FP16 为 2 字节、INT8 为 1 字节、FP32 为 4 字节。训练还要加梯度与 Adam 状态（各再占 1 份与 2 份权重），加上随批量与序列长度增长的激活值，常是权重本身的数倍。': 'Inference VRAM is mainly determined by weights: FP16 is 2 bytes, INT8 is 1 byte, FP32 is 4 bytes. Training also adds gradients and Adam states (one and two extra copies of weights respectively), plus activation values that grow with batch and sequence length, often several times the weights themselves.',
    '参数量(十亿)': 'Parameters (billions)',
    '每参数字节': 'Bytes per param',
    '激活 MB': 'Activation MB',
    '显存 ≈ 参数(十亿)×字节 + 激活开销': 'VRAM ~ params (billions) x bytes + activation overhead',
    '训练还需优化器状态（通常 2–4 倍权重）。': 'Training also needs optimizer states (usually 2-4x the weights).',
    '📚 深度解析：模型显存估算': '📚 Deep Dive: Model VRAM Estimator',
    '权重显存≈参数量×每参数字节数(FP16=2, INT8=1, FP32=4)。': 'Weight VRAM ~ parameters x bytes per param (FP16=2, INT8=1, FP32=4).',
    '推理显存还需加激活/KV 缓存，训练另需梯度与优化器状态(常数倍于权重)。': 'Inference VRAM also needs activation/KV cache; training additionally needs gradients and optimizer states (constant multiples of weights).',
    '估算用于硬件选型、batch 设定与显存溢出预警。': 'The estimate is used for hardware selection, batch setting and VRAM-overflow warning.',
    '7B 模型显存': '7B model VRAM',
    '7B 参数 FP16：权重≈7e9×2=14GB；加 KV 缓存与激活后推理约 16~18GB，可在 24GB 显卡跑；若训则需额外梯度+优化器(约 3~4 倍权重)。': '7B params FP16: weights ~ 7e9 x 2 = 14GB; with KV cache and activation, inference is about 16-18GB, runnable on a 24GB GPU; if training, add gradients + optimizer (~ 3-4x weights).',
    '为什么训练显存远大于推理？': 'Why is training VRAM much larger than inference?',
    '训练需保留前向激活供反向、存梯度(同尺寸)与优化器状态(Adam 约 2 倍权重)，常使总显存达权重 3~4 倍；推理只需权重+少量激活。': 'Training must keep forward activations for backprop, store gradients (same size) and optimizer states (Adam about 2x weights), often bringing total VRAM to 3-4x the weights; inference only needs weights + a little activation.',
    '显存不够怎么办？': 'What if VRAM is insufficient?',
    '量化降权重字节数、用梯度检查点换计算省激活、降 batch、或模型并行/张量并行分片；必要时上更大显存或分布式。': 'Quantize to reduce weight bytes, use gradient checkpointing to trade compute for activation savings, reduce batch, or use model/tensor parallel sharding; if necessary, use larger VRAM or distribution.',
    '模型显存估算': 'Model VRAM Estimator',
}
verify('vram-estimate', '模型显存估算', VR)
apply_tool('vram-estimate', '模型显存估算', 'Model VRAM Estimator', VR, ind=IND)

print('gen_ai_b6 done')
