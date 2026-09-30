# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch5（剩余工具第 3 批 11 个）。逐条语义化翻译；值纯英文避开 CJK/中文标点。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'

# ---------------- precision-recall 精确率与召回率 ----------------
apply_tool('precision-recall', '精确率与召回率', 'Precision and Recall', {
    '🧮 精确率与召回率': '🧮 Precision and Recall',
    '计算二分类的精确率、召回率与 F1。': 'Compute precision, recall and F1 for binary classification.',
    '📖 查看「精确率与召回率使用指南」': '📖 View "Precision and Recall User Guide"',
    '精确率 P = TP/(TP+FP)；召回率 R = TP/(TP+FN)；F1 = 2PR/(P+R)': 'Precision P = TP/(TP+FP); Recall R = TP/(TP+FN); F1 = 2PR/(P+R)',
    'P 与 R 天然此消彼长：放宽阈值召回升高但误报增多。F1 用调和平均综合两者，对较小的一方更敏感（接近 0 时 F1 也接近 0），适合作为单一权衡指标；若业务更看重漏检（如疾病筛查）应改用 F2 加权召回。':
        'P and R naturally trade off: lowering the threshold raises recall but increases false alarms. F1 uses the harmonic mean to combine them, more sensitive to the smaller one (near 0 when F1 is near 0), suiting a single trade-off metric; if the business cares more about missed detections (e.g. disease screening), switch to F2 which weights recall.',
    '精确率关注预测正确性，召回率关注覆盖度。': 'Precision focuses on prediction correctness, recall on coverage.',
    '📚 深度解析：精确率与召回率': '📚 Deep Dive: Precision and Recall',
    '精确率 P=TP/(TP+FP) 衡量预测为正的纯度；召回 R=TP/(TP+FN) 衡量正类覆盖。': 'Precision P=TP/(TP+FP) measures the purity of positive predictions; recall R=TP/(TP+FN) measures positive-class coverage.',
    'F1=2PR/(P+R) 调和平均，二者冲突时综合评估。': 'F1=2PR/(P+R) harmonic mean, a combined assessment when the two conflict.',
    '阈值升高→精确率升、召回降；按业务代价选平衡点(如反欺诈重召回)。': 'Higher threshold -> precision up, recall down; choose the balance by business cost (e.g. anti-fraud favors recall).',
    '阈值权衡': 'Threshold trade-off',
    '某模型 TP=80,FP=20,FN=10。阈值低时 FP 多 P=80/100=80%、R=80/90=89%；抬高阈值 FP 降为 5 但 FN 升为 30 → P=80/85=94%、R=80/110=73%。':
        'A model with TP=80,FP=20,FN=10. At a low threshold FP is large: P=80/100=80%, R=80/90=89%; raising the threshold drops FP to 5 but FN rises to 30 -> P=80/85=94%, R=80/110=73%.',
    '什么时候更看重召回？': 'When should recall matter more?',
    '漏检代价高时(癌症筛查、欺诈拦截)，宁肯多报假阳性也要少漏，优先高召回；再用人工或二次模型过滤假阳性。':
        'When missed-detection cost is high (cancer screening, fraud interception), prefer false positives over misses and prioritize high recall; then filter false positives with humans or a second model.',
    'PR 曲线和 ROC 曲线怎么选？': 'How to choose between the PR curve and the ROC curve?',
    '类别不平衡时 PR 曲线更敏感、更贴切；ROC 在平衡数据下更稳。AUC-PR 对正类稀少场景更能反映性能。':
        'Under class imbalance the PR curve is more sensitive and fitting; ROC is more stable on balanced data. AUC-PR better reflects performance when positives are rare.',
}, ind=IND)

# ---------------- quantization-ratio 量化压缩比 ----------------
apply_tool('quantization-ratio', '量化压缩比', 'Quantization Compression Ratio', {
    '🗜️ 量化压缩比': '🗜️ Quantization Compression Ratio',
    '估算模型量化（如 FP32→INT8）的压缩比。': 'Estimate the compression ratio of model quantization (e.g. FP32->INT8).',
    '📖 查看「量化压缩比使用指南」': '📖 View "Quantization Compression Ratio User Guide"',
    '压缩比 = 原位数 / 目标位数；模型大小(MB) ≈ 参数量 × 位数 / 8 / 1024²': 'Compression ratio = original bits / target bits; model size (MB) ~ parameter count x bits / 8 / 1024²',
    '量化通过降低权重数值精度（FP32→INT8 即 4:1）直接缩小体积与带宽需求，算力受限场景收益明显。但精度损失会体现在指标上，对异常值敏感的模型需做量化感知训练或逐通道校准。':
        'Quantization lowers weight numeric precision (FP32->INT8 is 4:1), directly shrinking size and bandwidth needs, with clear gains on compute-limited devices. But accuracy loss shows up in metrics; models sensitive to outliers need quantization-aware training or per-channel calibration.',
    '参数量(百万)': 'Parameters (millions)',
    '原字节/参': 'Original bytes/param',
    '量化字节/参': 'Quantized bytes/param',
    '压缩比 = 原字节/量化字节': 'Compression ratio = original bytes / quantized bytes',
    'FP32→INT8 约 4× 压缩，需校准保精度。': 'FP32->INT8 is about 4x compression and needs calibration to preserve accuracy.',
    '📚 深度解析：量化压缩比': '📚 Deep Dive: Quantization Compression Ratio',
    '压缩比=量化前位数/量化后位数，如 FP32(32bit)→INT8(8bit) 理论压缩 4×。': 'Compression ratio = pre-quantization bits / post-quantization bits, e.g. FP32 (32bit) -> INT8 (8bit) is theoretically 4x.',
    '实际显存节省还需扣减反量化层与激活的精度开销，常略低于理论值。': 'Actual memory savings must also subtract the dequantization layer and activation precision overhead, often slightly below the theoretical value.',
    '量化分训练后(PTQ)与量化感知训练(QAT)，后者精度损失更小。': 'Quantization is split into post-training (PTQ) and quantization-aware training (QAT); the latter loses less accuracy.',
    '7B 模型 FP16 权重≈14GB，量化 INT8≈3.5GB(约 4× 压缩)，可在消费级显卡部署；若进一步 INT4≈1.75GB 但精度损失更明显，需实测可接受度。':
        'A 7B model FP16 weights ~14GB, INT8 ~3.5GB (~4x), deployable on consumer GPUs; further INT4 ~1.75GB but with more visible accuracy loss, so verify acceptability empirically.',
    '量化一定会掉精度吗？': 'Does quantization always lose accuracy?',
    '会损失一定精度，但 PTQ+校准或 QAT 可把损失压到很小；小模型/低比特(INT4)损失更大，需以下游任务指标验证。':
        'It loses some accuracy, but PTQ+calibration or QAT can shrink the loss greatly; small models / low bits (INT4) lose more and need validation by downstream metrics.',
    '压缩比和推理速度是一回事？': 'Are compression ratio and inference speed the same thing?',
    '相关但不等价。低比特省显存、提升访存带宽利用率，常提速；但是否真正加速还取决于硬件对低比特算子与反量化的支持。':
        'Related but not equivalent. Low bits save memory and improve memory-bandwidth utilization, often speeding up; but real acceleration also depends on hardware support for low-bit operators and dequantization.',
}, ind=IND)

# ---------------- rag RAG 召回率 ----------------
apply_tool('rag', 'RAG 召回率', 'RAG Recall', {
    '🤖 RAG 召回率': '🤖 RAG Recall',
    '评估 RAG 检索召回相关文档的比例。': 'Evaluate the proportion of relevant documents recalled by RAG retrieval.',
    '📖 查看「RAG 召回率使用指南」': '📖 View "RAG Recall User Guide"',
    '召回率 = 检索到的相关文档数 / 相关文档总数 × 100%；精确率 = 检索到的相关文档数 / 检索总数 × 100%；F1 = 2·P·R/(P + R)；命中率 = 检索到 ≥1 篇相关 ? 100% : 0':
        'Recall = retrieved relevant docs / total relevant docs x 100%; Precision = retrieved relevant docs / total retrieved x 100%; F1 = 2·P·R/(P + R); Hit rate = retrieved >=1 relevant ? 100% : 0',
    'RAG 的检索质量直接决定生成上限：召回率不足会漏掉关键证据导致幻觉，精确率不足则把噪声塞进上下文稀释注意力。命中率（Recall@k 的特例）常用于快速判断 top-k 是否够用。':
        'RAG retrieval quality directly sets the generation ceiling: insufficient recall misses key evidence and causes hallucinations, while insufficient precision stuffs noise into context and dilutes attention. Hit rate (a special case of Recall@k) is often used to quickly judge whether top-k is enough.',
    '相关文档总数': 'Total relevant docs',
    '检索返回数': 'Retrieved count',
    '检索中相关文档数': 'Relevant in retrieved',
    'Recall = 检索到的相关 / 所有相关': 'Recall = retrieved relevant / all relevant',
    'Precision = 检索到的相关 / 检索总数': 'Precision = retrieved relevant / total retrieved',
    'RAG 系统需权衡召回率与精确率。': 'RAG systems must trade off recall and precision.',
    '📚 深度解析：RAG 召回率': '📚 Deep Dive: RAG Recall',
    '召回率=检索命中的相关文档数/相关文档总数，衡量检索覆盖质量。': 'Recall = retrieved relevant docs / total relevant docs, measuring retrieval coverage quality.',
    'RAG 先召回再生成，召回不足会直接限制答案上限(garbage in, garbage out)。': 'RAG retrieves before generating; insufficient recall directly caps the answer ceiling (garbage in, garbage out).',
    '常用向量检索+关键词混合召回提升覆盖率，再重排 top-k。': 'Commonly use vector search + keyword hybrid recall to raise coverage, then rerank top-k.',
    '召回评估': 'Recall evaluation',
    '知识库某问题共有 10 篇相关文档，检索返回 top-20 中命中 8 篇 → 召回率=80%。若只命中 3 篇，则生成极易遗漏要点，需扩大召回或改进切分。':
        'A question has 10 relevant docs in the knowledge base; the top-20 retrieval hits 8 -> recall = 80%. If only 3 are hit, generation easily misses key points; expand recall or improve chunking.',
    '召回率高就够了吗？': 'Is high recall enough?',
    "不够。召回高只保证'找得全'，还需重排把最相关置顶、控制噪声，否则无关文档挤占上下文反而干扰生成。":
        "Not enough. High recall only guarantees 'completeness'; you still need reranking to put the most relevant on top and control noise, otherwise irrelevant docs crowd the context and disturb generation.",
    '怎么提升 RAG 召回？': 'How to improve RAG recall?',
    '优化文档切分粒度、用混合检索(向量+BM25)、加元数据过滤与重排；并定期用标准问答集测召回率指导迭代。':
        'Optimize chunking granularity, use hybrid retrieval (vector + BM25), add metadata filtering and reranking; and periodically measure recall on a standard QA set to guide iteration.',
}, ind=IND)

# ---------------- relu-leakyrelu ReLU 与 LeakyReLU ----------------
apply_tool('relu-leakyrelu', 'ReLU 与 LeakyReLU', 'ReLU and LeakyReLU', {
    '📖 查看「ReLU 与 LeakyReLU使用指南」': '📖 View "ReLU and LeakyReLU User Guide"',
    'ReLU = max(0, x)；LeakyReLU = x (x≥0) 否则 αx；ELU = x (x≥0) 否则 α(eˣ − 1)': 'ReLU = max(0, x); LeakyReLU = x (x>=0) else αx; ELU = x (x>=0) else α(eˣ - 1)',
    'ReLU 计算极快且正区间梯度恒为 1，但负区间硬置 0 会造成"死神经元"；LeakyReLU 用很小的 α（常 0.01）保留一丝负梯度；ELU 负区间平滑趋近 −α，输出均值更接近 0，收敛更快但含指数运算成本略高。':
        'ReLU is extremely fast and its positive-interval gradient is always 1, but hard-zeroing the negative interval causes "dead neurons"; LeakyReLU uses a tiny α (often 0.01) to keep a sliver of negative gradient; ELU\'s negative interval smoothly approaches -α, its output mean closer to 0, converging faster but with slightly higher exponential cost.',
    '输入 x': 'Input x',
    'LeakyReLU 斜率 α': 'LeakyReLU slope α',
    '激活函数是神经网络非线性的来源。': 'Activation functions are the source of neural-network nonlinearity.',
    '📚 深度解析：ReLU and LeakyReLU': '📚 Deep Dive: ReLU and LeakyReLU',
    "ReLU(x)=max(0,x)，负值输出 0，带来稀疏性与非负性；负值区梯度为 0 易致'神经元死亡'。":
        "ReLU(x)=max(0,x), negative output 0, bringing sparsity and non-negativity; the zero-gradient negative region easily causes 'dead neurons'.",
    'LeakyReLU(x)=max(αx,x)，负值给小斜率 α(如 0.01)保留微弱梯度，缓解死亡。': 'LeakyReLU(x)=max(αx,x), the negative region gets a small slope α (e.g. 0.01) keeping a weak gradient, easing death.',
    '二者均为非线性激活，使网络能拟合复杂函数。': 'Both are nonlinear activations that let the network fit complex functions.',
    '激活对比': 'Activation comparison',
    'x=−2, α=0.01：ReLU=0(梯度断流)，LeakyReLU=0.01×(−2)=−0.02(保留微弱信号)。x=3 时二者均输出 3。': 'x=-2, α=0.01: ReLU=0 (gradient cut), LeakyReLU=0.01x(-2)=-0.02 (keeps weak signal). At x=3 both output 3.',
    '为什么用 LeakyReLU 而不是 ReLU？': 'Why use LeakyReLU instead of ReLU?',
    'ReLU 在负区梯度恒为 0，若神经元输出长期为负则永久不更新(死亡)。LeakyReLU 给负区小斜率保留学习信号，训练更稳。':
        'ReLU\'s negative-region gradient is always 0; if a neuron\'s output stays negative it never updates (dies). LeakyReLU gives the negative region a small slope to keep a learning signal, stabilizing training.',
    '负值区斜率 α 取多大？': 'How large is the negative-region slope α?',
    '常用 0.01~0.1 固定，或参数化(PReLU)让模型学 α；α 过大负区信号过强、过小则接近 ReLU，0.01 是常见默认。':
        'Commonly fixed at 0.01-0.1, or parametric (PReLU) letting the model learn α; too large α over-weights the negative signal, too small approaches ReLU, 0.01 is the common default.',
}, ind=IND)

# ---------------- rmse 均方误差 RMSE ----------------
apply_tool('rmse', '均方误差 RMSE', 'Root Mean Squared Error', {
    '🏋️ 均方误差 RMSE': '🏋️ Root Mean Squared Error',
    '计算回归预测的 MSE、RMSE、MAE、R²。': 'Compute MSE, RMSE, MAE and R² for regression predictions.',
    '📖 查看「均方误差 RMSE使用指南」': '📖 View "Root Mean Squared Error User Guide"',
    '平方和展开式可在只有汇总量时算 MSE，避免逐样本遍历。RMSE 与 y 同量纲但对离群点敏感，MAE 更稳健；R² 表示相对"直接预测均值"提升的比例，可为负，说明模型还不如基准线。':
        'The sum-of-squares expansion lets you compute MSE from aggregates alone, avoiding per-sample iteration. RMSE shares the unit of y but is sensitive to outliers; MAE is more robust; R² is the proportion of improvement over "predicting the mean directly", can be negative, meaning the model is worse than the baseline.',
    '真实值之和': 'Sum of true values',
    '预测值之和': 'Sum of predicted values',
    '真实值平方和': 'Sum of squared true values',
    '预测值平方和': 'Sum of squared predicted values',
    '真实×预测之和': 'Sum of true x predicted',
    '输入聚合统计量即可计算。': 'Compute directly from aggregate statistics.',
    '📚 深度解析：均方误差 RMSE': '📚 Deep Dive: Root Mean Squared Error',
    'MSE=mean((y−ŷ)²)；RMSE=√MSE 与原始量纲一致，便于解释。': 'MSE=mean((y-y_hat)²); RMSE=√MSE matches the original unit, easy to interpret.',
    'MAE=mean|y−ŷ| 对离群更稳健；R²=1−SS_res/SS_tot 衡量解释方差比例。': 'MAE=mean|y-y_hat| is more robust to outliers; R²=1-SS_res/SS_tot measures the explained-variance ratio.',
    '回归评估应同时看 RMSE/MAE(误差量级)与 R²(拟合优度)。': 'Regression evaluation should look at both RMSE/MAE (error magnitude) and R² (goodness of fit).',
    '回归误差计算': 'Regression error computation',
    '真实 [3,5,2], 预测 [2.5,5,3]：残差 [0.5,0,−1]，MSE=(0.25+0+1)/3=0.417，RMSE=0.646，MAE=(0.5+0+1)/3=0.5，R² 需结合均值算解释度。':
        'True [3,5,2], predicted [2.5,5,3]: residuals [0.5,0,-1], MSE=(0.25+0+1)/3=0.417, RMSE=0.646, MAE=(0.5+0+1)/3=0.5, R² needs the mean for explained variance.',
    'RMSE 和 MAE 哪个好？': 'Which is better, RMSE or MAE?',
    'RMSE 对大误差惩罚更重(平方)，对离群敏感；MAE 更稳健、直观。关注极端偏差(如股价)看 RMSE，关注平均偏差看 MAE。':
        'RMSE penalizes large errors more (squared) and is outlier-sensitive; MAE is more robust and intuitive. Watch RMSE for extreme deviations (e.g. stock prices), MAE for average deviation.',
    'R² 为负说明什么？': 'What does a negative R² mean?',
    "说明模型比'直接取均值'还差，拟合失败；可能特征无用、": "It means the model is worse than 'simply taking the mean', fitting failed; the features may be useless,",
    '过拟合': 'overfitting',
    '或数据本身无结构，需重做特征与模型。': 'or the data itself has no structure, requiring redone features and model.',
}, ind=IND)

# ---------------- roc-auc ROC AUC 近似 ----------------
apply_tool('roc-auc', 'ROC AUC 近似', 'ROC AUC Approximation', {
    '🤖 ROC AUC 近似': '🤖 ROC AUC Approximation',
    '用正例与负例得分估算 AUC。': 'Estimate AUC from positive and negative scores.',
    '📖 查看「ROC AUC 近似使用指南」': '📖 View "ROC AUC Approximation User Guide"',
    'AUC ≈ 0.5 + 0.5·erf[(μ₊ − μ₋)/√(2(σ₊² + σ₋²))]；分离度 d\' = (μ₊ − μ₋)/√[(σ₊² + σ₋²)/2]': 'AUC ~ 0.5 + 0.5·erf[(μ₊ - μ₋)/√(2(σ₊² + σ₋²))]; separability d\' = (μ₊ - μ₋)/√[(σ₊² + σ₋²)/2]',
    '在正负样本得分各自近似正态的假设下，AUC 可由两分布的均值差与方差直接算出，无需逐对比较，适合只有汇总统计量的快速估算。若真实分布长尾或严重偏态，该近似会偏离实测 AUC，此时应改用秩次法。':
        'Assuming positive and negative scores are each roughly normal, AUC can be computed directly from the two distributions\' mean difference and variance, without pairwise comparison, suiting quick estimation from aggregates. If the real distribution is heavy-tailed or severely skewed, this approximation deviates from the measured AUC, and the rank-sum method should be used instead.',
    '正例平均得分': 'Positive mean score',
    '负例平均得分': 'Negative mean score',
    '正例标准差': 'Positive std dev',
    '负例标准差': 'Negative std dev',
    '基于正态分布假设的近似。': 'Approximation under the normal-distribution assumption.',
    '📚 深度解析：ROC AUC 近似': '📚 Deep Dive: ROC AUC Approximation',
    'AUC 为 ROC 曲线下面积，等价于随机正样本得分高于随机负样本的概率。': 'AUC is the area under the ROC curve, equivalent to the probability that a random positive scores higher than a random negative.',
    'AUC=0.5 为随机分类，1 为完美；对类别不平衡与阈值选择不敏感。': 'AUC=0.5 is random classification, 1 is perfect; insensitive to class imbalance and threshold choice.',
    '近似可用梯形法逐点算 ROC 下面积，或 Mann-Whitney 由秩和估算。': 'The approximation can use the trapezoidal method to integrate the ROC area point by point, or Mann-Whitney from the rank sum.',
    'AUC 解读': 'AUC interpretation',
    '某模型 AUC=0.85：随机抽取一正一负样本，正样本得分更高概率 85%。相比准确率需固定阈值，AUC 给出整体排序质量。':
        'A model with AUC=0.85: drawing one positive and one negative at random, the positive scores higher with 85% probability. Unlike accuracy which needs a fixed threshold, AUC gives overall ranking quality.',
    'AUC 高但线上效果差？': 'High AUC but poor online results?',
    'AUC 只反映排序能力，不保证某业务阈值下的准确率/召回；且训练/验证分布若与线上偏移，AUC 高也可能落地差。':
        'AUC only reflects ranking ability, not guaranteeing accuracy/recall at a business threshold; and if train/validation distribution drifts from online, high AUC can still land poorly.',
    '样本极不平衡 AUC 还准吗？': 'Is AUC still accurate under extreme imbalance?',
    'AUC 本身对不平衡稳健(基于排序)，但正类极少时估计方差大、且业务更关心正类召回，应辅以 PR-AUC。':
        'AUC itself is robust to imbalance (rank-based), but with very few positives the estimate variance is large and the business cares more about positive recall, so add PR-AUC.',
    '如何使用ROC AUC 近似': 'How to use the ROC AUC Approximation',
}, ind=IND)

# ---------------- sentiment-analysis 情感分析 ----------------
apply_tool('sentiment-analysis', '情感分析', 'Sentiment Analysis', {
    '📊 情感分析': '📊 Sentiment Analysis',
    '基于 Transformers.js 在浏览器本地判断文本情感倾向。英文走 DistilBERT 模型，中文走本地情感词库，数据不上传。': 'Runs locally in the browser via Transformers.js to judge text sentiment. English uses the DistilBERT model, Chinese uses a local sentiment lexicon, with no data upload.',
    '📖 查看「情感分析使用指南」': '📖 View "Sentiment Analysis User Guide"',
    '分析情感': 'Analyze sentiment',
    '本工具在浏览器本地对文本做情感分析（中文内置情感词库 / 英文 DistilBERT 模型），输出情感极性，全程不上传。': 'This tool runs sentiment analysis locally in the browser (Chinese built-in lexicon / English DistilBERT model) and outputs sentiment polarity, all without upload.',
    '📚 深度解析：情感分析': '📚 Deep Dive: Sentiment Analysis',
    '在浏览器本地对文本做正/负/中性倾向识别，输出情感标签与置信度。': 'Locally identify positive/negative/neutral tendencies in text and output sentiment labels with confidence.',
    '纯前端运行，文本不上传，适合评论、舆情与客服消息快速判断。': 'Runs fully client-side with no upload, suited to quickly judging reviews, public opinion and customer-service messages.',
    '基于轻量模型，对讽刺、反语与上下文依赖句识别有限，结果供辅助。': 'Based on a lightweight model, recognition of sarcasm, irony and context-dependent sentences is limited; results are for assistance.',
    '本地情感判断': 'Local sentiment judgment',
    "输入'这家店服务太差，再也不来了' → 标签'负面', 置信度 0.92。'还行吧，一般般' → '中性'。模型对含蓄表达(如反讽)可能误判。":
        "Input 'This store's service was terrible, never coming back' -> label 'Negative', confidence 0.92. 'It was okay, so-so' -> 'Neutral'. The model may misjudge implicit expressions (e.g. irony).",
    '为什么有时判错？': 'Why does it sometimes misjudge?',
    '轻量本地模型难捕讽刺、双重否定与领域黑话；强需求可用云端大模型配合上下文，但涉及文本外发需评估隐私。': 'Lightweight local models struggle with sarcasm, double negatives and domain slang; strong needs can use a cloud LLM with context, but text egress requires privacy assessment.',
    '文本会泄露吗？': 'Will the text leak?',
    '不会。本工具在浏览器内完成推理，文本不离开设备；代价是模型能力受本地资源限制。': 'No. Inference runs entirely inside the browser and the text never leaves the device; the trade-off is that model capability is limited by local resources.',
    '输入要分析的句子，例如：这部电影太精彩了，强烈推荐！': 'Enter a sentence to analyze, e.g.: This movie was amazing, highly recommended!',
}, ind=IND)

# ---------------- sigmoid Sigmoid 输出 ----------------
apply_tool('sigmoid', 'Sigmoid 输出', 'Sigmoid Output', {
    'S Sigmoid 输出': 'S Sigmoid Output',
    '计算 Sigmoid 函数值与分类阈值。': 'Compute the Sigmoid function value and the classification threshold.',
    '📖 查看「Sigmoid 输出使用指南」': '📖 View "Sigmoid Output User Guide"',
    'σ(z) = 1/(1 + e^(−z))；对数几率 logit = ln[p/(1 − p)] = z': 'sigma(z) = 1/(1 + e^(-z)); log-odds logit = ln[p/(1 - p)] = z',
    'Sigmoid 把任意实数压到 (0,1)，输出可直接当概率用；其导数 σ′=σ(1−σ)，在 |z| 较大时趋于 0，是深层网络梯度消失的根源之一，所以隐藏层现多改用 ReLU 系。阈值不必固定 0.5，应按业务代价调整。':
        'Sigmoid squeezes any real number into (0,1), usable directly as a probability; its derivative sigma\' = sigma(1-sigma) tends to 0 when |z| is large, one root cause of vanishing gradients in deep networks, so hidden layers now mostly switch to the ReLU family. The threshold need not be fixed at 0.5; adjust it by business cost.',
    '输入 z': 'Input z',
    '分类阈值': 'Classification threshold',
    '将任意实数映射到 (0,1)。': 'Maps any real number to (0,1).',
    '📚 深度解析：Sigmoid 输出': '📚 Deep Dive: Sigmoid Output',
    'σ(x)=1/(1+e⁻ˣ)，将任意实数映射到 (0,1)，用于二分类概率化。': 'sigma(x)=1/(1+e^-x), mapping any real number to (0,1), used to probabilize binary classification.',
    'x=0 时 σ=0.5；x 很大趋近 1、很小趋近 0，具饱和性。': 'At x=0 sigma=0.5; for very large x it approaches 1, very small approaches 0, being saturating.',
    '与 BCE 损失配合；其导数 σ\'(x)=σ(x)(1−σ(x))，便于反向传播。': 'Paired with BCE loss; its derivative sigma\'(x)=sigma(x)(1-sigma(x)) eases backprop.',
    '概率映射': 'Probability mapping',
    'logit=2 → σ=1/(1+e⁻²)=0.881；logit=−2 → σ=0.119；logit=0 → 0.5。可见 logit 每增加 1，概率向 1 推进一步但减速(饱和)。':
        'logit=2 -> sigma=1/(1+e^-2)=0.881; logit=-2 -> sigma=0.119; logit=0 -> 0.5. Each +1 in logit pushes probability toward 1 but decelerates (saturation).',
    'Sigmoid 和 Softmax 区别？': 'What is the difference between Sigmoid and Softmax?',
    'Sigmoid 独立处理每个 logit、输出各维独立概率(可不和为1)，适合多标签；Softmax 归一化使各类概率和为1，适合单标签多分类。':
        'Sigmoid handles each logit independently, outputting independent per-dimension probabilities (need not sum to 1), suiting multi-label; Softmax normalizes so class probabilities sum to 1, suiting single-label multi-class.',
    '为什么 Sigmoid 易饱和导致梯度消失？': 'Why does Sigmoid easily saturate and cause vanishing gradients?',
    '当 |x| 很大时 σ 接近 0 或 1，导数≈0，反向传播梯度趋零；深层网络常用 BatchNorm 与 ReLU 缓解，或用 Swish 等替代。':
        'When |x| is large, sigma approaches 0 or 1 and the derivative ~ 0, so backprop gradients vanish; deep networks often use BatchNorm and ReLU to ease this, or switch to Swish.',
}, ind=IND)

# ---------------- softmax Softmax 概率 ----------------
apply_tool('softmax', 'Softmax 概率', 'Softmax Probabilities', {
    '🎲 Softmax 概率': '🎲 Softmax Probabilities',
    '将一组 logits 转换为概率分布。': 'Convert a set of logits into a probability distribution.',
    '📖 查看「Softmax 概率使用指南」': '📖 View "Softmax Probabilities User Guide"',
    'Softmax 把 logits 变成和为 1 的概率分布，指数放大差距使最大值更突出。实现上通常先减去 max(z) 再取指数以避免上溢；输出概率并不等于模型置信度，未经校准的模型常过度自信。':
        'Softmax turns logits into a probability distribution summing to 1, with the exponential amplifying gaps to highlight the max. In implementation, subtract max(z) before exponentiating to avoid overflow; the output probability is not the model\'s confidence - uncalibrated models are often overconfident.',
    'Softmax 输出概率之和为 1。': 'Softmax output probabilities sum to 1.',
    '📚 深度解析：Softmax 概率': '📚 Deep Dive: Softmax Probabilities',
    'softmax(z)_i=exp(z_i)/Σⱼexp(z_j)，将 logits 归一化为和为 1 的概率分布。': 'softmax(z)_i = exp(z_i)/Σⱼexp(z_j), normalizing logits into a probability distribution summing to 1.',
    '输出具平移不变性(全体加常数不变)，但对尺度敏感(乘系数放大差异)。': 'The output is translation-invariant (unchanged by adding a constant) but scale-sensitive (multiplying amplifies differences).',
    '多分类输出层标配，配合交叉熵作损失；数值上先减最大值防溢出。': 'The standard output layer for multi-class, paired with cross-entropy as loss; numerically subtract the max first to prevent overflow.',
    '概率归一化': 'Probability normalization',
    'logits=[2,1,0.1]，减最大值 2 得 [0,−1,−1.9]，exp=[1,0.368,0.149]，Σ=1.517 → 概率=[0.659,0.243,0.098]，和为 1。':
        'logits=[2,1,0.1], subtract max 2 to get [0,-1,-1.9], exp=[1,0.368,0.149], Σ=1.517 -> probabilities=[0.659,0.243,0.098], summing to 1.',
    '为什么要减去最大值？': 'Why subtract the maximum?',
    'exp 大数会溢出。softmax 具平移不变性，先减最大值不改变结果却把所有指数压到 ≤0，避免 exp 上溢、数值稳定。':
        'Large exp overflows. Softmax is translation-invariant, so subtracting the max changes nothing yet pushes all exponents to <=0, avoiding exp overflow and staying numerically stable.',
    'softmax 和 sigmoid 在二分类下等价吗？': 'Are softmax and sigmoid equivalent for binary classification?',
    '等价。二分类 softmax 两维概率互为补数，与对单 logit 用 sigmoid 一致；多分类才必须用 softmax 归一化。':
        'Yes. Binary softmax gives complementary two-class probabilities, identical to sigmoid on a single logit; multi-class must use softmax normalization.',
}, ind=IND)

# ---------------- softmax-2 温度缩放 Softmax ----------------
apply_tool('softmax-2', '温度缩放 Softmax', 'Temperature-Scaled Softmax', {
    '🖼️ 温度缩放 Softmax': '🖼️ Temperature-Scaled Softmax',
    '观察温度参数对 Softmax 分布尖锐程度的影响。': 'Observe how the temperature parameter affects the sharpness of the Softmax distribution.',
    '📖 查看「温度缩放 Softmax使用指南」': '📖 View "Temperature-Scaled Softmax User Guide"',
    'Pᵢ(T) = e^{zᵢ/T} / Σⱼ e^{zⱼ/T}；分布熵 H = −Σ Pᵢ ln Pᵢ': 'P_i(T) = e^{z_i/T} / Σⱼ e^{zⱼ/T}; distribution entropy H = -Σ P_i ln P_i',
    '温度 T 控制分布锐度：T→0 趋近 one-hot（更确定），T→∞ 趋近均匀分布。训练时用高温做知识蒸馏可暴露类别间关系；但温度缩放只改变锐度不改变排序，不能修复模型本身的排序错误。':
        'Temperature T controls distribution sharpness: T->0 approaches one-hot (more certain), T->infinity approaches uniform. In training, high temperature for knowledge distillation exposes inter-class relations; but temperature scaling only changes sharpness, not ranking, and cannot fix the model\'s own ranking errors.',
    '温度 T': 'Temperature T',
    'T→0 更尖锐，T→∞ 更均匀': 'T->0 sharper, T->infinity more uniform',
    '知识蒸馏中常用温度缩放。': 'Temperature scaling is common in knowledge distillation.',
    '📚 深度解析：温度缩放 Softmax': '📚 Deep Dive: Temperature-Scaled Softmax',
    '温度缩放 y_i=exp(z_i/T)/Σexp(z_j/T)，T>1 使分布更平滑(更不确定)，T<1 更尖锐。': 'Temperature scaling y_i=exp(z_i/T)/Σexp(z_j/T), T>1 makes the distribution smoother (more uncertain), T<1 sharper.',
    'T→∞ 趋近': 'T->infinity approaches',
    '均匀分布': 'uniform distribution',
    '，T→0 趋近 one-hot(argmax)。': ', T->0 approaches one-hot (argmax).',
    '温度常用于调节生成多样性与模型校准，不改变 argmax 类别。': 'Temperature is often used to tune generation diversity and model calibration, without changing the argmax class.',
    '温度影响分布': 'Temperature affects the distribution',
    'logits=[2,1,0.5]：T=1 → 概率≈[0.6285,0.2312,0.1402]；T×2=2 → [0.4810,0.2918,0.2272] 更平滑；T/2=0.5 → [0.8438,0.1142,0.0420] 更尖锐。三个温度下的 argmax 始终为第 1 类，说明温度只改变置信度分布、不改变预测类别。':
        'logits=[2,1,0.5]: T=1 -> probabilities ~[0.6285,0.2312,0.1402]; T×2=2 -> [0.4810,0.2918,0.2272] smoother; T/2=0.5 -> [0.8438,0.1142,0.0420] sharper. The argmax stays class 1 across all three temperatures, showing temperature only changes the confidence distribution, not the predicted class.',
    '温度能校准模型吗？': 'Can temperature calibrate a model?',
    '温度缩放是最简单的后校准方法，调 T 使输出置信度匹配实际准确率；但它只缩放分布、不能修正错误预测的方向。':
        'Temperature scaling is the simplest post-calibration method, tuning T so output confidence matches actual accuracy; but it only rescales the distribution and cannot correct the direction of wrong predictions.',
    '生成时温度设多高？': 'How high should the generation temperature be?',
    '创意写作用较高 T(0.7~1.0)增多样性，事实问答用低 T(0~0.3)增确定性；过高会胡言乱语，过低则重复僵化。':
        'Creative writing uses higher T (0.7-1.0) for diversity, factual QA uses lower T (0-0.3) for determinism; too high rambles, too low repeats rigidly.',
    '页面上为什么要同时给出 T=1、T/2、T×2 三行？': 'Why does the page show T=1, T/2 and T×2 rows together?',
    '单看一个温度看不出趋势。三行分别代表基准、低温(更尖锐、更自信)与高温(更平缓、更不确定)，可直接读出「T 减半最大概率从 62.85% 升到 84.38%、T 翻倍降到 48.10%」这种量级变化，便于判断该往哪个方向调。温度必须大于 0，T=0 时 logits÷T 无定义。':
        'A single temperature hides the trend. The three rows represent baseline, low temperature (sharper, more confident) and high temperature (smoother, more uncertain), letting you read magnitude changes like "halving T raises max probability from 62.85% to 84.38%, doubling T drops it to 48.10%", helping decide which way to tune. T must be greater than 0; at T=0 logits/T is undefined.',
}, ind=IND)

# ---------------- specificity 特异度计算 ----------------
apply_tool('specificity', '特异度计算', 'Specificity Calculation', {
    '🧮 特异度计算': '🧮 Specificity Calculation',
    '评估模型识别负类（特异度）的能力。': 'Evaluate the model\'s ability to identify the negative class (specificity).',
    '📖 查看「特异度计算使用指南」': '📖 View "Specificity Calculation User Guide"',
    '特异度 TNR = TN/(TN+FP)×100%；假阳性率 FPR = FP/(TN+FP)×100% = 1 − 特异度': 'Specificity TNR = TN/(TN+FP) x 100%; False Positive Rate FPR = FP/(TN+FP) x 100% = 1 - Specificity',
    '特异度衡量负类被正确排除的能力，与召回率（灵敏度）构成 ROC 曲线的两个轴。筛查场景宁可牺牲特异度换取高召回，而 spam 误杀正常邮件的代价很高，应反过来优先保特异度。':
        'Specificity measures how well the negative class is correctly excluded, forming one axis of the ROC curve with recall (sensitivity). Screening scenarios may sacrifice specificity for high recall, but spam wrongly blocking legitimate mail is costly, so specificity should be prioritized instead.',
    '特异度 = TN/(TN+FP)': 'Specificity = TN/(TN+FP)',
    '特异度衡量模型识别负类的能力。': 'Specificity measures the model\'s ability to identify the negative class.',
    '📚 深度解析：特异度计算': '📚 Deep Dive: Specificity Calculation',
    '特异度 Specificity=TN/(TN+FP)，衡量模型正确识别负类的能力。': 'Specificity = TN/(TN+FP), measuring the model\'s ability to correctly identify the negative class.',
    '与灵敏度(召回)互补：灵敏度看重病不漏，特异度看重健康不误判。': 'Complementary to sensitivity (recall): sensitivity insists on not missing disease, specificity insists on not misjudging health.',
    '医学筛查常要求高特异度以降低假阳性带来的过度检查。': 'Medical screening often requires high specificity to reduce over-testing from false positives.',
    '筛查特异度': 'Screening specificity',
    'TN=900, FP=30 → 特异度=900/930=96.8%，即健康人被 correctly 判为健康的比例；若 FP 升到 100 则特异度降到 90%，假阳性增多。':
        'TN=900, FP=30 -> specificity = 900/930 = 96.8%, i.e. the share of healthy people correctly judged healthy; if FP rises to 100, specificity drops to 90% with more false positives.',
    '特异度和精确率有什么区别？': 'What is the difference between specificity and precision?',
    '特异度=TN/(TN+FP) 站在负类视角；精确率=TP/(TP+FP) 站在预测为正视角。二者分母不同，关注点不同。':
        'Specificity = TN/(TN+FP) views from the negative class; precision = TP/(TP+FP) views from predicted-positive. Their denominators differ, so do their focuses.',
    '为什么筛查要重视特异度？': 'Why should screening care about specificity?',
    '假阳性会引不必要的复查与焦虑、浪费资源；高特异度减少误报，但常与灵敏度权衡(卡阈值时此消彼长)。':
        'False positives trigger unnecessary rechecking and anxiety and waste resources; high specificity reduces false alarms, but often trades off with sensitivity (the two move opposite when setting the threshold).',
}, ind=IND)

print('gen_ai_b5 done')
