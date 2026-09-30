# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch2（具名工具前 8 个）。逐条语义化翻译；值纯英文避开 CJK/中文标点。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'

# ---------------- ai 分类准确率评估 ----------------
apply_tool('ai', '分类准确率评估', 'Classification Accuracy Evaluator', {
    '📖 查看「分类准确率评估使用指南」': '📖 View "Classification Accuracy Evaluator User Guide"',
    '准确率 = (TP+TN)/(TP+FP+FN+TN)×100%；精确率 = TP/(TP+FP)×100%；召回率 = TP/(TP+FN)×100%；F1 = 2TP/(2TP+FP+FN)×100%':
        'Accuracy = (TP+TN)/(TP+FP+FN+TN) x 100%; Precision = TP/(TP+FP) x 100%; Recall = TP/(TP+FN) x 100%; F1 = 2TP/(2TP+FP+FN) x 100%',
    '由混淆矩阵四类计数推导：准确率衡量整体判对比例，精确率关注"报为正的有多少真"，召回率关注"真正例被找出多少"，F1 是二者调和平均。样本极度不平衡时准确率会失真，应改看 F1 或 PR 曲线下的面积。':
        'Derived from the four confusion-matrix counts: accuracy measures the overall correct proportion, precision focuses on "of those called positive, how many are truly positive", recall focuses on "how many true positives are found", and F1 is their harmonic mean. Accuracy becomes misleading under extreme imbalance, so switch to F1 or the area under the PR curve.',
    '真正例 TP': 'True Positive TP',
    '假正例 FP': 'False Positive FP',
    '假反例 FN': 'False Negative FN',
    '真反例 TN': 'True Negative TN',
    '用于二分类模型评估。': 'Used for binary classification model evaluation.',
    '📚 深度解析：分类准确率评估': '📚 Deep Dive: Classification Accuracy Evaluator',
    '准确率 Accuracy=(TP+TN)/(TP+TN+FP+FN)，衡量整体正确比例。':
        'Accuracy = (TP+TN)/(TP+TN+FP+FN), measuring the overall correct proportion.',
    '精确率 P=TP/(TP+FP) 关注预测为正的纯度；召回 R=TP/(TP+FN) 关注正类覆盖。':
        'Precision P=TP/(TP+FP) focuses on the purity of positive predictions; recall R=TP/(TP+FN) focuses on positive-class coverage.',
    'F1=2PR/(P+R) 在类别不平衡时比准确率更可靠。':
        'F1 = 2PR/(P+R) is more reliable than accuracy under class imbalance.',
    '二分类四指标': 'Four metrics for binary classification',
    'TP=70, FP=10, FN=20, TN=100：准确率=(70+100)/200=85%，P=70/80=87.5%，R=70/90=77.8%，F1=2×0.875×0.778/(0.875+0.778)≈82.4%。':
        'TP=70, FP=10, FN=20, TN=100: accuracy=(70+100)/200=85%, P=70/80=87.5%, R=70/90=77.8%, F1=2x0.875x0.778/(0.875+0.778)≈82.4%.',
    '准确率 85% 算好吗？': 'Is 85% accuracy good?',
    '取决于基线。若正类仅占 10%，全猜负类就有 90% 准确率却毫无正类识别力；此时应看精确率/召回/F1 与 PR 曲线。':
        'It depends on the baseline. If positives are only 10%, always guessing negative already gives 90% accuracy yet detects no positives; in that case look at precision/recall/F1 and the PR curve.',
    '多分类怎么算精确率？': 'How to compute precision for multi-class?',
    '常用宏平均(各类指标等权平均，看重小类)或微平均(汇总所有 TP/FP/FN，等价于整体准确率)，按业务对小类敏感度选择。':
        'Commonly macro-average (equal-weight average of per-class metrics, favoring minority classes) or micro-average (sum all TP/FP/FN, equivalent to overall accuracy); choose by how sensitive the business is to minority classes.',
}, ind=IND)

# ---------------- ai-code-review AI 代码审查 ----------------
apply_tool('ai-code-review', 'AI 代码审查', 'AI Code Review', {
    '📖 查看「AI 代码审查使用指南」': '📖 View "AI Code Review User Guide"',
    '本工具在浏览器本地用规则与启发式对 JavaScript/TypeScript 做静态分析，识别未声明变量、冗余分支、可疑空值解引用等模式并给出提示；纯前端运行，代码不上传服务器。':
        'This tool runs locally in the browser using rules and heuristics to statically analyze JavaScript/TypeScript, flagging patterns like undeclared variables, redundant branches, and suspicious null dereferences; it runs fully client-side and never uploads your code to a server.',
    '选择语言': 'Select language',
    '粘贴代码': 'Paste code',
    '粘贴需要审查的代码...': 'Paste the code to review...',
    '开始审查': 'Start review',
    '示例代码': 'Example code',
    '📚 深度解析：AI 代码审查': '📚 Deep Dive: AI Code Review',
    '在浏览器本地用规则与启发式静态分析 JS/TS 代码，识别未定义变量、冗余分支、潜在空值等问题。':
        'Locally analyze JS/TS code with rules and heuristics to detect undefined variables, redundant branches, potential null dereferences and similar issues.',
    '纯前端运行，代码不上传，适合隐私敏感与离线场景的轻量自查。':
        'Running entirely client-side with no upload suits privacy-sensitive and offline lightweight self-checks.',
    '审查结果应作为人工复核的辅助，不能替代团队 Code Review 与安全测试。':
        'Review results should assist manual review, not replace team Code Review or security testing.',
    '常见问题识别': 'Common issue detection',
    "输入含 let x; if(x>0){} 的代码，工具提示 'x 未初始化即参与比较'；对 if(a){}else if(a){} 提示 '互斥分支不可能同时成立'。定位后由开发者确认修正。":
        "For code like 'let x; if(x>0){}', the tool warns 'x is compared before initialization'; for 'if(a){}else if(a){}' it warns 'mutually exclusive branches cannot both hold'. The developer then confirms and fixes.",
    '它能发现所有 bug 吗？': 'Can it find all bugs?',
    '不能。静态分析只能捕获模式化、确定性问题，无法理解业务语义与运行时行为；深度缺陷仍需单测、集成测试与人工评审。':
        'No. Static analysis only catches patterned, deterministic issues and cannot understand business semantics or runtime behavior; deep defects still require unit tests, integration tests and manual review.',
    '为什么强调纯前端不上传？': 'Why stress local, no-upload?',
    '代码常含商业逻辑与密钥风险，本地处理避免源码外泄；但仅本地也意味着无法调用云端大模型做更深入的语义理解。':
        'Code often contains business logic and secret risks; local processing avoids source leakage, but being local-only also means no cloud LLM for deeper semantic understanding.',
    '关于「AI 代码审查」': 'About "AI Code Review"',
    'AI 代码审查。AI 辅助工具，帮助理解算法原理与数据处理流程。': 'AI Code Review. An AI-assisted tool that helps you understand algorithm principles and data-processing flows.',
}, ind=IND)

# ---------------- ai-prompt-generator AI 提示词生成器 ----------------
apply_tool('ai-prompt-generator', 'AI 提示词生成器', 'AI Prompt Generator', {
    '📖 查看「AI 提示词生成器使用指南」': '📖 View "AI Prompt Generator User Guide"',
    '高质量提示词(Prompt)通常包含五要素,本工具按模板拼接并填空:': 'A high-quality prompt usually has five elements; this tool concatenates and fills a template:',
    '角色(Role)': 'Role',
    '任务(Task)': 'Task',
    '上下文(Context)': 'Context',
    '格式(Format)': 'Format',
    '约束(Constraints)': 'Constraints',
    '可附加 few-shot 示例、chain-of-thought(逐步推理)引导。': 'You can attach few-shot examples and chain-of-thought (step-by-step reasoning) prompts.',
    'token 估算:中文约 1 字 ≈ 1.5 token、英文约 1 词 ≈ 1.3 token(仅作量级参考)。有效提示应': 'Token estimate: Chinese is about 1 char ~ 1.5 tokens, English about 1 word ~ 1.3 tokens (magnitude only). An effective prompt should ',
    '明确、单一、给示例与边界': 'be clear, single-purpose, and give examples with boundaries.',
    '本工具按所选场景与角色、任务、约束等字段套用结构化模板拼接生成 Prompt；纯前端拼接，内容不上传服务器。':
        'This tool applies a structured template using the selected scenario, role, task and constraints to assemble the prompt; it runs purely client-side and does not upload content to a server.',
    '角色/身份': 'Role / identity',
    '任务描述': 'Task description',
    '背景信息（可选）': 'Background info (optional)',
    '输出要求': 'Output requirements',
    '例如：资深产品经理、Python 专家、营销文案': 'e.g. senior product manager, Python expert, marketing copywriter',
    '例如：帮我写一份产品介绍、解释这段代码、生成营销文案': 'e.g. write a product intro, explain this code, generate marketing copy',
    '相关背景、数据、约束条件等': 'Relevant background, data, constraints, etc.',
    '例如：表格形式、100字以内、分步骤': 'e.g. table format, within 100 words, step by step',
    '语气风格': 'Tone / style',
    '专业严谨': 'Professional and rigorous',
    '友好亲切': 'Friendly and warm',
    '幽默风趣': 'Humorous and witty',
    '简洁直接': 'Concise and direct',
    '学术正式': 'Academic and formal',
    '口语化': 'Conversational',
    '生成提示词': 'Generate prompt',
    '随机示例': 'Random example',
    '📚 深度解析：AI 提示词生成器': '📚 Deep Dive: AI Prompt Generator',
    '按应用场景(写作/编程/分析)与角色、任务、约束等字段，套用结构化模板拼接出专业 Prompt。':
        'Given the scenario (writing/coding/analysis) and fields like role, task and constraints, it assembles a professional prompt from a structured template.',
    '结构化提示(角色+任务+上下文+格式+约束)比一句话诉求更易被模型稳定遵循。':
        'A structured prompt (role + task + context + format + constraints) is followed more reliably by models than a one-line request.',
    '生成结果可复制微调，适配不同大模型；纯前端拼接，内容不上传。':
        'The result can be copied and fine-tuned for different LLMs; it runs client-side with no upload.',
    '角色+任务模板': 'Role + task template',
    "选'编程助手'，填角色=资深": "Choose 'Coding Assistant', set role = senior ",
    "工程师、任务=写爬虫、约束=用 requests+异常处理 → 生成 '你是一位资深Python工程师，请用 requests 编写带异常处理的爬虫，输出可直接运行的代码与说明'。":
        "engineer, task = write a crawler, constraint = use requests + exception handling -> generates 'You are a senior Python engineer; please write a crawler with exception handling using requests, and output runnable code with explanations'.",
    '为什么需要结构化提示？': 'Why do we need structured prompts?',
    '模型对明确角色、边界与输出格式响应更稳，能减少跑题与幻觉；结构化模板把模糊需求显式化，可复现性好。':
        'Models respond more reliably to clear roles, boundaries and output formats, reducing drift and hallucination; a structured template makes vague requirements explicit and reproducible.',
    '生成后还要改吗？': 'Do you still need to edit after generation?',
    '建议据模型实际表现迭代：补充示例(少样本)、收紧约束、给出输出样例，比一次生成更管用。':
        "Iterate based on the model's actual behavior: add examples (few-shot), tighten constraints, and give output samples; this works better than one-shot generation.",
    '关于「AI 提示词生成器」': 'About "AI Prompt Generator"',
    'AI 提示词生成器。AI 辅助工具，帮助理解算法原理与数据处理流程。': 'AI Prompt Generator. An AI-assisted tool that helps you understand algorithm principles and data-processing flows.',
}, ind=IND)

# ---------------- ai-text-summarizer AI 文本摘要 ----------------
apply_tool('ai-text-summarizer', 'AI 文本摘要', 'AI Text Summarizer', {
    '📖 查看「AI 文本摘要使用指南」': '📖 View "AI Text Summarizer User Guide"',
    '本工具基于 TextRank 算法在浏览器本地对句子构图（句间相似度为边、按重要度排序）抽取关键句生成摘要；纯前端运行，文本不上传服务器。':
        'This tool uses the TextRank algorithm to build a sentence graph locally in the browser (inter-sentence similarity as edges, ranked by importance) and extracts key sentences as a summary; it runs client-side and never uploads text to a server.',
    '输入文本（建议 200-5000 字）': 'Input text (recommended 200-5000 characters)',
    '粘贴需要摘要的文章、报告、新闻等...': 'Paste the article, report, news, etc. to summarize...',
    '摘要句子数：': 'Number of summary sentences:',
    '📚 深度解析：AI 文本摘要': '📚 Deep Dive: AI Text Summarizer',
    '基于 TextRank 算法在浏览器本地对句子构图(相似度连边)，按重要性排序抽取关键句生成摘要。':
        'Locally build a sentence graph with TextRank (similarity as edges) and extract key sentences by importance as the summary.',
    '纯前端运行，文本不上传，适合长文速览与隐私场景。': 'Runs client-side with no upload, suited to quick long-doc skimming and privacy scenarios.',
    '抽取式摘要保留原文句子，忠于原意但可能缺乏连贯；如需改写式需云端大模型。':
        'Extractive summarization keeps original sentences, faithful but possibly less coherent; abstractive rewriting needs a cloud LLM.',
    '关键句抽取': 'Key-sentence extraction',
    "输入一篇 10 段新闻，工具按句间相似度构图，选出得分最高的 3 句作为摘要。若原文有'公司营收增长 30%'等核心句，会被高权重保留。":
        "Input a 10-paragraph news article; the tool builds the sentence graph by inter-sentence similarity and picks the top-3 scoring sentences as the summary. A core sentence like 'company revenue grew 30%' gets high weight and is retained.",
    'TextRank 和云端大模型摘要有何区别？': 'How does TextRank differ from a cloud LLM summary?',
    'TextRank 是本地抽取式，只挑原文句子、不动写、零上传、零成本；大模型可生成式改写更流畅，但需联网与算力且涉及数据外发。':
        'TextRank is local and extractive: it only picks original sentences, zero upload, zero cost; an LLM can rewrite more fluently but needs network and compute and sends data out.',
    '摘要太短或太长怎么调？': 'How to adjust if the summary is too short or too long?',
    '调整抽取句数或压缩比；句数过少会漏要点，过多则失去摘要意义，以覆盖主干事件为准。':
        'Adjust the sentence count or compression ratio; too few misses key points, too many defeats the purpose; aim to cover the main events.',
    '关于「AI 文本摘要」': 'About "AI Text Summarizer"',
    'AI 文本摘要。AI 辅助工具，帮助理解算法原理与数据处理流程。': 'AI Text Summarizer. An AI-assisted tool that helps you understand algorithm principles and data-processing flows.',
}, ind=IND)

# ---------------- attention-flops 注意力计算量 ----------------
apply_tool('attention-flops', '注意力计算量', 'Attention FLOPs', {
    '📖 查看「注意力计算量使用指南」': '📖 View "Attention FLOPs User Guide"',
    '单层 FLOPs ≈ 2S²d (QKᵀ) + 2S²d (AV) = 4S²d；全模型 GFLOPs = 单层 × 层数 / 10⁹':
        'Single-layer FLOPs ~ 2S²d (QKᵀ) + 2S²d (AV) = 4S²d; total model GFLOPs = single-layer x layers / 10⁹',
    '自注意力的两次矩阵乘各为 S×S×d 规模，乘加各算一次故乘 2，合计 4S²d，随序列长度呈平方增长——这正是长上下文成本暴涨的原因。线性注意力与稀疏注意力正是为打破这一 S² 项。':
        'The two self-attention matrix multiplies are each SxSxd in size; multiply-add counts once each so x2, totaling 4S²d, growing quadratically with sequence length - exactly why long-context cost explodes. Linear and sparse attention exist to break this S² term.',
    '序列长度': 'Sequence length',
    '单层注意力 ≈ 2·S²·d(QKᵀ) + 2·S²·d(·V)': 'Single-layer attention ~ 2·S²·d (QKᵀ) + 2·S²·d (·V)',
    '注意力和序列长度平方相关，长序列代价高。': 'Attention scales with sequence length squared, so long sequences are costly.',
    '📚 深度解析：注意力计算量': '📚 Deep Dive: Attention FLOPs',
    '单头注意力 FLOPs≈2·S²·d（QKᵀ 与 AV 两次矩阵乘），S 为序列长、d 为维度。':
        'Single-head attention FLOPs ~ 2·S²·d (the QKᵀ and AV matrix multiplies), where S is sequence length and d is dimension.',
    '多头总计算≈2·S²·h·d_head + 4·S·d²（含 Q/K/V/O 投影），S² 项使长序列算力平方增长。':
        'Multi-head total ~ 2·S²·h·d_head + 4·S·d² (including Q/K/V/O projections); the S² term makes compute grow quadratically with long sequences.',
    '与 FFN 相比，注意力在长序列时 dominated by S²，是推理成本优化的重点。':
        'Compared with the FFN, attention is dominated by S² for long sequences and is the key target for inference-cost optimization.',
    '单层注意力算力': 'Single-layer attention compute',
    'S=1024, h=16, d_head=64(总 d=1024)：S² 项≈2×1024²×1024≈2.15×10⁹ FLOPs；投影 4·S·d²=4×1024×1024²≈4.29×10⁹。单层约 6.4×10⁹ FLOPs，12 层约 7.7×10¹⁰。':
        'S=1024, h=16, d_head=64 (total d=1024): the S² term ~ 2x1024²x1024 ~ 2.15x10⁹ FLOPs; projections 4·S·d² = 4x1024x1024² ~ 4.29x10⁹. One layer ~ 6.4x10⁹ FLOPs, 12 layers ~ 7.7x10¹⁰.',
    '为什么长文本推理特别慢？': 'Why is long-text inference especially slow?',
    '注意力核心项是 S²·d，序列翻倍算力翻约 4 倍；KV 缓存虽降重算，但注意力矩阵仍随上下文长度平方增长，故长上下文成本陡增。':
        'The core term is S²·d; doubling the sequence quadruples compute. KV cache cuts recompute but the attention matrix still grows with context length squared, so long-context cost rises sharply.',
    'FLOPs 和显存是一回事吗？': 'Are FLOPs and memory the same thing?',
    '不是。FLOPs 衡量算力(时间)，显存衡量参数与激活的存储(空间)。量化降显存但不降 FLOPs，稀疏/蒸馏可同时降两者。':
        'No. FLOPs measure compute (time); memory measures storage of parameters and activations (space). Quantization lowers memory but not FLOPs; sparsity/distillation can lower both.',
}, ind=IND)

# ---------------- attention-head-dim 注意力头维度 ----------------
apply_tool('attention-head-dim', '注意力头维度', 'Attention Head Dimension', {
    '📖 查看「注意力头维度使用指南」': '📖 View "Attention Head Dimension User Guide"',
    '每头维度 = d / heads；单层权重参数 ≈ 4d² + 2d·ffn':
        'Dimension per head = d / heads; single-layer weight parameters ~ 4d² + 2d·ffn',
    '多头注意力把 d 维切成 heads 份并行计算，每头维度须整除，头数过多会让单头维度过小、表达能力下降。单层参数由注意力四矩阵 4d² 与 FFN 两层 2d·ffn 构成，是显存与算力的主要来源。':
        'Multi-head attention splits the d dimension into heads for parallel computation; the per-head dimension must divide evenly, and too many heads make each head too small and weaken expressiveness. The single-layer parameters come from the four attention matrices (4d²) and the two FFN layers (2d·ffn), which dominate memory and compute.',
    '模型维度': 'Model dimension',
    '头数': 'Number of heads',
    'FFN 维度': 'FFN dimension',
    '常见 head_dim 64，过大或过小均影响表达。': 'A common head_dim is 64; too large or too small hurts expressiveness.',
    '📚 深度解析：注意力头维度': '📚 Deep Dive: Attention Head Dimension',
    '每头维度 d_head=d_model/h，需整除；常见 d_model=512,h=8→d_head=64。':
        'Per-head dimension d_head = d_model / h, must divide evenly; common d_model=512, h=8 -> d_head=64.',
    '单层注意力参数量≈4·d_model²（Q/K/V/O 四个投影），与头数无关只与总维度相关。':
        'Single-layer attention parameters ~ 4·d_model² (the Q/K/V/O projections), independent of head count and only tied to total dimension.',
    '头数过多而 d_head 过小会限制每头表达能力，需权衡并行度与单头容量。':
        'Too many heads with too small d_head limits each head’s capacity; balance parallelism against per-head capacity.',
    '头维度与参数量': 'Head dimension and parameters',
    'd_model=768, h=12 → d_head=64。Q/K/V/O 各 768×768≈590k 参数，单层注意力≈4×590k=2.36M 参数；与 h 取值无关，只取决于 d_model。':
        'd_model=768, h=12 -> d_head=64. Each of Q/K/V/O is 768x768 ~ 590k params, single-layer attention ~ 4x590k = 2.36M params; independent of h, only depends on d_model.',
    '头数越多越好吗？': 'Are more heads always better?',
    '不一定。头数增加提升并行关注不同子空间的能力，但 d_head 随之变小、每头容量受限；过大头数收益递减且增算力。':
        'Not necessarily. More heads improve the ability to attend to different subspaces in parallel, but d_head shrinks and per-head capacity is limited; excessive heads yield diminishing returns and more compute.',
    'd_head 不整除怎么办？': 'What if d_head does not divide evenly?',
    '需调整 d_model 或头数使其整除，否则框架会报错或 padding 引入冗余；常见组合保证 d_model%h==0。':
        'Adjust d_model or head count so it divides evenly, otherwise the framework errors or padding adds redundancy; common configs ensure d_model % h == 0.',
    '如何使用注意力头维度': 'How to use Attention Head Dimension',
}, ind=IND)

# ---------------- auc-rank AUC 秩次估算 ----------------
apply_tool('auc-rank', 'AUC 秩次估算', 'AUC Rank Estimate', {
    '📖 查看「AUC 秩次估算使用指南」': '📖 View "AUC Rank Estimate User Guide"',
    'U = ΣRank(正例) − nPos(nPos+1)/2；AUC = U/(nPos × nNeg)':
        'U = ΣRank(positives) − nPos(nPos+1)/2; AUC = U / (nPos × nNeg)',
    'Mann-Whitney U 统计视角：AUC 等于"随机抽一个正例与一个负例，正例得分更高的概率"。把所有样本按得分升序排名，用正例秩和减去最小可能秩和即得 U，再除以正负配对总数 nPos×nNeg，结果 0.5 表示无区分能力。':
        'From the Mann-Whitney U view: AUC equals "the probability that a randomly drawn positive outranks a randomly drawn negative". Rank all samples by score ascending, subtract the minimum possible rank sum from the positive rank sum to get U, then divide by the total positive-negative pairs nPos×nNeg; 0.5 means no discrimination.',
    '正样本数': 'Number of positives',
    '负样本数': 'Number of negatives',
    '正样本秩和': 'Positive rank sum',
    'AUC=0.5 为随机，1 为完美排序。': 'AUC=0.5 is random, 1 is a perfect ranking.',
    '📚 深度解析：AUC 秩次估算': '📚 Deep Dive: AUC Rank Estimate',
    'AUC 等价于随机抽一正一负样本、正样本得分更高的概率，可用 Mann-Whitney U 由秩和估算。':
        'AUC equals the probability that a random positive outranks a random negative, estimable from the rank sum via Mann-Whitney U.',
    '公式 AUC=1−U₁/(n₁·n₂)，U₁=R₁−n₁(n₁+1)/2，R₁ 为正类秩和。':
        'Formula AUC = 1 − U₁/(n₁·n₂), U₁ = R₁ − n₁(n₁+1)/2, where R₁ is the positive-class rank sum.',
    'AUC=0.5 为随机，1 为完美排序；对类别不平衡与阈值无关，适合排序质量评估。':
        'AUC=0.5 is random, 1 is perfect; it is threshold-independent and robust to class imbalance, suited to ranking-quality evaluation.',
    '秩和算 AUC': 'Rank-sum AUC',
    '正类 3 个得分排序后的秩和 R₁=2+4+5=11，n₁=3,n₂=3。U₁=11−3×4/2=5，AUC=1−5/(3×3)=1−0.556=0.444。说明正负排序接近随机偏弱。':
        'Three positives with sorted ranks R₁=2+4+5=11, n₁=3, n₂=3. U₁=11−3×4/2=5, AUC=1−5/(3×3)=1−0.556=0.444, indicating near-random, weak discrimination.',
    'AUC 和准确率有什么关系？': 'How is AUC related to accuracy?',
    '无直接等价。准确率是固定阈值下的分类正确率，AUC 是遍历所有阈值的整体排序质量，AUC 高不代表某阈值下准确率也高。':
        'No direct equivalence. Accuracy is the correct rate at a fixed threshold; AUC is the overall ranking quality across all thresholds. A high AUC does not mean high accuracy at a given threshold.',
    '大时秩和法还准吗？': 'Is the rank-sum method still accurate at scale?',
    '准。Mann-Whitney 是 AUC 的无偏估计，样本越多越稳；只是实现上可用更高效的计数法避免显式排序开销。':
        'Yes. Mann-Whitney is an unbiased estimate of AUC and stabilizes with more samples; in practice a more efficient counting method avoids explicit sorting cost.',
}, ind=IND)

# ---------------- augmentation-multiplier 数据增强倍数 ----------------
apply_tool('augmentation-multiplier', '数据增强倍数', 'Augmentation Multiplier', {
    '📖 查看「数据增强倍数使用指南」': '📖 View "Augmentation Multiplier User Guide"',
    '增强后总量 = 原始样本数 × (1 + 系数 × 变换种类数)':
        'Augmented total = original samples × (1 + coefficient × number of transform types)',
    '按每种变换贡献的增量线性外推总量，系数反映单次变换的等效增益（通常 <1）。这是上界估计：变换间高度相关时实际有效量远小于此，且增强样本不能完全替代真实数据的分布覆盖。':
        'Linearly extrapolate the total from each transform’s incremental contribution; the coefficient reflects the effective gain per transform (usually < 1). This is an upper bound: when transforms are highly correlated the real effective amount is far smaller, and augmented samples cannot fully replace the distribution coverage of real data.',
    '变换种类': 'Transform types',
    '每种倍数': 'Multiplier per type',
    '总量 = 原始 ×(1 + 倍数 × 变换数)': 'Total = original × (1 + multiplier × transform count)',
    '实际去重后可能低于估算。': 'After deduplication the real amount may be lower than the estimate.',
    '📚 深度解析：数据增强倍数': '📚 Deep Dive: Augmentation Multiplier',
    '增强后样本总量≈原始量×变换': 'Augmented total ~ original × transforms',
    '组合数': 'Combination count',
    '×重复系数，用于训练集扩容规划。': '× repetition coefficient, for training-set expansion planning.',
    '倍数高不等于信息量等比例增长，重复/相似变换带来相关性。': 'A higher multiplier does not mean information grows proportionally; repeated/similar transforms bring correlation.',
    '应结合验证集表现设定增强强度，避免过度失真。': 'Set augmentation strength against validation performance to avoid excessive distortion.',
    '增强倍数估算': 'Augmentation multiplier estimate',
    'Original 5000 张，旋转/翻转/色彩 3 类各 3 档共 9 组合 → 总量≈5000×9=45000 张。若叠加 2 次重复则≈90000，但有效增益低于 18 倍。':
        'Original 5000 images, rotate/flip/color across 3 types x 3 levels = 9 combinations -> total ~ 5000x9 = 45000 images. With 2x repetition ~ 90000, but the effective gain is below 18x.',
    '原始 5000 张，旋转/翻转/色彩 3 类各 3 档共 9 组合 → 总量≈5000×9=45000 张。若叠加 2 次重复则≈90000，但有效增益低于 18 倍。':
        'Original 5000 images, rotate/flip/color across 3 types x 3 levels = 9 combinations -> total ~ 5000x9 = 45000 images. With 2x repetition ~ 90000, but the effective gain is below 18x.',
    "倍数和'有效量'有什么区别？": "What is the difference between 'multiplier' and 'effective amount'?",
    '倍数只算变换乘积，有效量还扣减相关性带来的信息折损；本工具给倍数，是否等效需结合增强多样性判断。':
        'The multiplier only computes the transform product; the effective amount also subtracts the information loss from correlation. This tool gives the multiplier; whether it is equivalent depends on augmentation diversity.',
    '增强强度设多大？': 'How strong should augmentation be?',
    '以验证集指标为准：增强不足仍': 'Judge by validation metrics: if augmentation is insufficient and still ',
    '过拟合': 'overfitting',
    '则加强，过强导致训练误差难降则回撤；图像常用轻几何+色彩抖动。': 'then strengthen it; if too strong makes training error hard to drop, pull back. Images commonly use light geometry + color jitter.',
}, ind=IND)

print('gen_ai_b2 done: 8 tools written')
