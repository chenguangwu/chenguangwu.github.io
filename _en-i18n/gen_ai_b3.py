# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch3（剩余工具前 10 个）。逐条语义化翻译；值纯英文避开 CJK/中文标点。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'

# ---------------- best-epoch 最佳轮次选择 ----------------
apply_tool('best-epoch', '最佳轮次选择', 'Best Epoch Selection', {
    '🚀 最佳轮次选择': '🚀 Best Epoch Selection',
    '从若干轮损失中选出最优轮次。': 'Select the best epoch from several rounds of loss.',
    '📖 查看「最佳轮次选择使用指南」': '📖 View "Best Epoch Selection User Guide"',
    '最佳轮次 = argmin(验证损失)；最小验证损失 = min(l₁…l₅)': 'Best epoch = argmin(validation loss); minimum validation loss = min(l₁…l₅)',
    '取验证损失最低的轮次而非最后一轮，是早停的标准做法。若多个轮次损失接近，优先选更靠后的（通常更稳）或按次要指标（F1）再筛；注意"用验证集选轮次"本身会轻微乐观，严格评估应留出独立测试集。':
        'Choosing the epoch with the lowest validation loss rather than the last epoch is the standard early-stopping practice. If several epochs have close losses, prefer a later one (usually more stable) or re-filter by a secondary metric (F1); note that "selecting the epoch on the validation set" is itself slightly optimistic, so a strict evaluation should reserve an independent test set.',
    'loss 轮1': 'loss epoch 1',
    'loss 轮2': 'loss epoch 2',
    'loss 轮3': 'loss epoch 3',
    'loss 轮4': 'loss epoch 4',
    'loss 轮5': 'loss epoch 5',
    '最佳轮次 = loss 最小者': 'Best epoch = the one with minimum loss',
    '应结合验证集，避免过拟合轮次。': 'Combine with the validation set to avoid overfit epochs.',
    '📚 深度解析：最佳轮次选择': '📚 Deep Dive: Best Epoch Selection',
    '在记录中各轮验证指标(如验证 loss/F1)取最优轮次，作为部署权重。': 'Among the records, pick the epoch with the best validation metric (e.g. validation loss/F1) as the deployed weights.',
    '监控指标上升即早停，并回退到最佳轮 checkpoint，避免用': 'Stop early once the metric rises and roll back to the best-epoch checkpoint, avoiding using',
    '过拟合': 'overfitting',
    '权重。': 'weights.',
    '若多指标冲突(如 loss 最低但 F1 非最高)，按业务优先级选定主指标。': 'If multiple metrics conflict (e.g. lowest loss but not highest F1), choose the primary metric by business priority.',
    '选最优轮': 'Select best epoch',
    '10 轮验证 F1 为 [0.80,0.83,0.85,0.86,0.87,0.87,0.86,0.85,0.84,0.83]，最佳为第 6 轮(0.87)，应加载第 6 轮权重而非最后一轮。':
        '10 epochs of validation F1: [0.80,0.83,0.85,0.86,0.87,0.87,0.86,0.85,0.84,0.83], best is epoch 6 (0.87); you should load epoch-6 weights rather than the last epoch.',
    '用 loss 还是 F1 选最佳轮？': 'Use loss or F1 to pick the best epoch?',
    '看目标。回归用验证 loss/RMSE；分类常看 F1/Accuracy；若关注误杀率则看精确率。主指标应直接对应业务收益。':
        'It depends on the goal. Regression uses validation loss/RMSE; classification often looks at F1/Accuracy; if the false-negative rate matters, look at precision. The primary metric should directly map to business value.',
    '验证指标波动怎么选？': 'How to choose when validation metrics fluctuate?',
    '取平滑后的最优且要求持续优势(patience)，避免单点噪声误导；也可在最佳轮附近做少量额外验证确认稳定。':
        'Take the smoothed optimum and require a sustained lead (patience) to avoid single-point noise; you can also run a few extra validations near the best epoch to confirm stability.',
}, ind=IND)

# ---------------- cohens-kappa Cohen Kappa 系数 ----------------
apply_tool('cohens-kappa', 'Cohen Kappa 系数', "Cohen's Kappa Coefficient", {
    '🤖 Cohen Kappa 系数': '🤖 Cohen\'s Kappa Coefficient',
    '计算评价者一致性的 Cohen Kappa。': "Compute Cohen's Kappa for rater agreement.",
    '📖 查看「Cohen Kappa 系数使用指南」': '📖 View "Cohen\'s Kappa Coefficient User Guide"',
    'Cohen\'s Kappa 剔除"偶然一致"后衡量两个标注者（或模型与金标）的真实一致性：Pe 是按各自边缘分布随机撞上的概率。κ>0.8 视为几乎完全一致，0.4–0.6 中等，低于 0 说明一致性还不如随机，标注口径需要重新对齐。':
        "Cohen's Kappa measures the true agreement between two annotators (or a model and the gold standard) after removing \"chance agreement\": Pe is the probability they agree by random chance from their marginal distributions. kappa>0.8 is near-perfect, 0.4-0.6 moderate, below 0 means worse than random, so the annotation protocol needs re-alignment.",
    'κ>0.8 几乎完全一致，<0.2 微弱。': 'kappa>0.8 nearly perfect, <0.2 slight.',
    '📚 深度解析：Cohen Kappa 系数': '📚 Deep Dive: Cohen\'s Kappa Coefficient',
    'κ=(p_o−p_e)/(1−p_e)，p_o 为观测一致率，p_e 为随机一致率(按边际概率算)。': 'kappa=(p_o-p_e)/(1-p_e), where p_o is the observed agreement rate and p_e is the chance agreement rate (from marginal probabilities).',
    'κ=1 完全一致，0 为仅随机一致，负值表示一致性差于随机。': 'kappa=1 perfect agreement, 0 is chance-only, negative means worse than chance.',
    '用于标注一致性、诊断一致性等可靠性评估，比单纯准确率排除随机巧合。': 'Used for reliability assessment of annotation or diagnostic agreement; it excludes random coincidence better than raw accuracy.',
    '两人标注一致性': 'Two-annotator agreement',
    '两类各 100 例，观测一致 85 例 p_o=0.85；边际概率算得随机一致 p_e=0.50 → κ=(0.85−0.50)/(1−0.50)=0.70，属高度一致。':
        'Two classes of 100 cases each, observed agreement 85 cases p_o=0.85; marginal probabilities give chance agreement p_e=0.50 -> kappa=(0.85-0.50)/(1-0.50)=0.70, indicating substantial agreement.',
    'kappa 和准确率差在哪？': 'How does kappa differ from accuracy?',
    "准确率不剔除'瞎猜也能碰对'的巧合；kappa 用 p_e 扣除随机一致，更能反映真实一致性，类别越不平衡 p_e 越高、越需 kappa。":
        "Accuracy does not remove the coincidence of 'guessing right by luck'; kappa uses p_e to subtract chance agreement, better reflecting true agreement. The more imbalanced the classes, the higher p_e, the more kappa is needed.",
    'kappa 多高算可靠？': 'How high is kappa considered reliable?',
    '经验尺：0.01~0.20 轻微、0.21~0.40 一般、0.41~0.60 中等、0.61~0.80 高度、0.81~1.00 几乎完全；但阈值随领域而变。':
        'Empirical scale: 0.01-0.20 slight, 0.21-0.40 fair, 0.41-0.60 moderate, 0.61-0.80 substantial, 0.81-1.00 almost perfect; thresholds vary by domain.',
}, ind=IND)

# ---------------- context-window 上下文窗口占用 ----------------
apply_tool('context-window', '上下文窗口占用', 'Context Window Usage', {
    '📚 上下文窗口占用': '📚 Context Window Usage',
    '计算提示与回复对上下文窗口的占用。': 'Compute how much the prompt and reply occupy the context window.',
    '📖 查看「上下文窗口占用使用指南」': '📖 View "Context Window Usage User Guide"',
    '占用率 = (系统提示 + 用户输入 + 预期回复) / 上下文窗口 × 100%；剩余 = 窗口 − 已用': 'Usage = (system prompt + user input + expected reply) / context window x 100%; remaining = window - used',
    '规划对话时把预期回复长度一并计入，避免生成到一半撞上窗口上限被截断。长窗口模型虽标称很大，但注意力成本随长度平方增长，且中段内容容易被忽略（lost-in-the-middle），并非越长越好。':
        'When planning a conversation, include the expected reply length, so generation is not truncated by hitting the window limit mid-way. Although long-window models advertise large sizes, attention cost grows with the square of length, and middle content is easily ignored (lost-in-the-middle), so longer is not always better.',
    '系统提示 tokens': 'System prompt tokens',
    '对话 tokens': 'Conversation tokens',
    '回复 tokens': 'Reply tokens',
    '上下文上限': 'Context limit',
    '占用 = 系统+对话+回复；占用率 = 已用/上限': 'Usage = system + conversation + reply; usage rate = used / limit',
    '超出上限需截断或摘要历史。': 'Exceeding the limit requires truncating or summarizing history.',
    '📚 深度解析：上下文窗口占用': '📚 Deep Dive: Context Window Usage',
    '占用比=提示词 token + 生成 token / 窗口上限(如 4k/32k/128k)。': 'Usage ratio = prompt tokens + generation tokens / window limit (e.g. 4k/32k/128k).',
    '中英混排时中文按字或 subword 计，需以具体分词器为准估算。': 'For mixed Chinese-English text, Chinese is counted per character or subword; estimates must follow the specific tokenizer.',
    '占用超 100% 将截断，长任务应预留生成空间并定期压缩历史。': 'Usage over 100% will be truncated; long tasks should reserve generation space and periodically compress history.',
    '占用预警': 'Usage warning',
    '窗口 8k，提示 6k + 预计生成 2k = 8k 恰好满；若实际生成超 2k 即溢出。建议提示控制在 5k 以内留 3k 给生成。':
        'Window 8k, prompt 6k + expected generation 2k = 8k exactly full; if actual generation exceeds 2k it overflows. Keep the prompt under 5k and leave 3k for generation.',
    '为什么显示占用满了却还能聊？': 'Why can it still chat when usage shows full?',
    "部分实现会滚动丢弃最早历史以维持窗口，表现为'能继续但忘了开头'；严格实现则直接报错。占用比应预留生成余量。":
        "Some implementations scroll-drop the earliest history to maintain the window, appearing as 'can continue but forgot the beginning'; strict ones error out. Always reserve generation headroom in the usage ratio.",
    '不同模型 token 数一样吗？': 'Do different models count the same number of tokens?',
    '不同。同一段中文在 GPT/Claude/国产模型下 token 数差异明显，估算仅供参考，精确值需对应分词器计数。':
        'No. The same Chinese passage yields noticeably different token counts under GPT/Claude/domestic models; estimates are for reference only, exact values need the corresponding tokenizer.',
}, ind=IND)

# ---------------- cosine-similarity 余弦相似度 ----------------
apply_tool('cosine-similarity', '余弦相似度', 'Cosine Similarity', {
    '🤖 余弦相似度': '🤖 Cosine Similarity',
    '计算两个向量的余弦相似度。': 'Compute the cosine similarity between two vectors.',
    '📖 查看「余弦相似度使用指南」': '📖 View "Cosine Similarity User Guide"',
    '余弦相似度取值范围 [−1,1]，1 为同向、0 为正交、−1 为反向。因为做了模长归一化，它对向量整体缩放不敏感，适合比较长度差异很大的文本或特征向量；若需要同时反映模长差异应改回欧氏距离。':
        'Cosine similarity ranges [-1,1]: 1 same direction, 0 orthogonal, -1 opposite. Because it normalizes vector length, it is insensitive to overall scaling, suiting texts or feature vectors of very different lengths; to also reflect length differences switch back to Euclidean distance.',
    '取值 −1 到 1，越接近 1 越相似。': 'Ranges -1 to 1; closer to 1 means more similar.',
    '📚 深度解析：余弦相似度': '📚 Deep Dive: Cosine Similarity',
    'cos(x,y)=Σxᵢyᵢ/(‖x‖·‖y‖)，取值 [−1,1]，1 为同方向、0 正交、−1 反向。': 'cos(x,y)=Σxᵢyᵢ/(‖x‖·‖y‖), ranges [-1,1]: 1 same direction, 0 orthogonal, -1 opposite.',
    '对向量归一化后，余弦等价于内积，计算更快且利于检索索引。': 'After normalizing vectors, cosine equals the inner product, faster to compute and friendly to retrieval indexes.',
    '文本/图像嵌入比对几乎都用余弦，因模长常受频率或亮度干扰不代表语义。': 'Text/image embedding comparisons almost all use cosine, since length is often distorted by frequency or brightness and does not represent semantics.',
    '两': 'Two',
    '向量夹角': 'Vector angle',
    'x=(1,2,2), y=(2,4,4)：‖x‖=3,‖y‖=6,内积=2+8+8=18 → cos=18/(3×6)=1，两向量同向(实际 y=2x)，完全相似。':
        'x=(1,2,2), y=(2,4,4): ‖x‖=3,‖y‖=6, dot=2+8+8=18 -> cos=18/(3x6)=1, the vectors are parallel (in fact y=2x), perfectly similar.',
    '余弦为负说明什么？': 'What does a negative cosine indicate?',
    '说明两向量夹角大于 90°，语义倾向相反(如反义句、对立情感)。多数相似度场景只取非负区间，需按业务决定是否保留负值。':
        'It means the angle between the two vectors exceeds 90 deg, so their semantics tend to oppose (e.g. antonyms, conflicting sentiment). Most similarity use cases take only the non-negative range; decide per business whether to keep negatives.',
    '为什么先归一化？': 'Why normalize first?',
    '归一化后模长均为 1，余弦=内积，便于用内积加速检索(如 FAISS)；且消除向量长度对相似度的影响，聚焦方向。':
        'After normalization all lengths are 1, cosine = inner product, enabling inner-product-accelerated retrieval (e.g. FAISS); it also removes the effect of vector length on similarity, focusing on direction.',
}, ind=IND)

# ---------------- cross-entropy 交叉熵损失 ----------------
apply_tool('cross-entropy', '交叉熵损失', 'Cross-Entropy Loss', {
    '🌡️ 交叉熵损失': '🌡️ Cross-Entropy Loss',
    '计算二分类交叉熵损失。': 'Compute binary cross-entropy loss.',
    '📖 查看「交叉熵损失使用指南」': '📖 View "Cross-Entropy Loss User Guide"',
    '单样本 L = −[y·ln p + (1 − y)·ln(1 − p)]；批量 L = 单样本 × n': 'Single-sample L = -[y·ln p + (1 - y)·ln(1 - p)]; batch L = single-sample x n',
    '二分类交叉熵对 confident 且错误的预测给出极大惩罚（p→0 而 y=1 时趋于无穷），梯度形式简洁 (p − y)，配合 sigmoid 反向传播非常干净。实现时要注意对 p 做 eps 截断防止 log(0)。':
        'Binary cross-entropy heavily penalizes confident yet wrong predictions (tends to infinity when p->0 but y=1); its gradient is simple (p - y) and backprop through sigmoid is very clean. In implementation, watch the eps clipping on p to prevent log(0).',
    '真实标签 0/1': 'True label 0/1',
    '预测概率': 'Predicted probability',
    'p 应裁剪至 (ε,1−ε) 避免 log(0)。': 'Clip p to (ε,1-ε) to avoid log(0).',
    '📚 深度解析：交叉熵损失': '📚 Deep Dive: Cross-Entropy Loss',
    '二分类交叉熵 CE=−[y·log(p)+(1−y)·log(1−p)]，y∈{0,1}, p 为预测正类概率。': 'Binary CE = -[y·log(p)+(1-y)·log(1-p)], y in {0,1}, p is the predicted positive-class probability.',
    '多分类用 −Σyᵢlog(pᵢ)，要求 p 经 softmax 且和为 1。': 'Multi-class uses -Σyᵢlog(pᵢ), requiring p from softmax and summing to 1.',
    'CE 对错误预测惩罚重(对数放大)，是分类模型训练的标准损失。': 'CE heavily penalizes wrong predictions (logarithmic amplification) and is the standard loss for classification training.',
    '单样本损失': 'Single-sample loss',
    '真实 y=1，预测 p=0.9 → CE=−log(0.9)=0.105；若 p=0.1 → CE=−log(0.1)=2.303。预测越错损失越大，驱动模型修正。':
        'True y=1, predicted p=0.9 -> CE=-log(0.9)=0.105; if p=0.1 -> CE=-log(0.1)=2.303. The more wrong the prediction, the larger the loss, driving the model to correct.',
    '为什么用交叉熵而不是均方误差？': 'Why use cross-entropy instead of mean squared error?',
    'CE 对概率错误更敏感且在 sigmoid/softmax 下梯度更优，MSE 用于概率会产生饱和、收敛慢；CE 是分类自然对应的对数似然损失。':
        'CE is more sensitive to probability errors and has better gradients under sigmoid/softmax; MSE on probabilities saturates and converges slowly; CE is the log-likelihood loss naturally matched to classification.',
    'p 为 0 或 1 会怎样？': 'What happens when p is 0 or 1?',
    'log(0) 得 −∞ 导致数值爆炸。实践中对 p 做裁剪(clip 到 ε~1−ε)或用带 logits 的稳定实现(直接吃 raw score 算 softmax)避免。':
        'log(0) yields -infinity and causes numerical explosion. In practice clip p (to ε~1-ε) or use a numerically stable logits-based implementation (compute softmax directly from raw scores) to avoid it.',
}, ind=IND)

# ---------------- dropout Dropout 保留期望 ----------------
apply_tool('dropout', 'Dropout 保留期望', 'Dropout Expected Output', {
    '🤖 Dropout 保留期望': '🤖 Dropout Expected Output',
    '计算 Dropout 后的期望输出与缩放因子。': 'Compute the expected output and scaling factor after Dropout.',
    '📖 查看「Dropout 保留期望使用指南」': '📖 View "Dropout Expected Output User Guide"',
    '保留概率 p = 1 − rate；训练期望 E[x] = p·x；缩放因子 = 1/p（inverted dropout）': 'Keep probability p = 1 - rate; training expectation E[x] = p·x; scaling factor = 1/p (inverted dropout)',
    '训练时按 rate 随机置零并在保留分支乘 1/p，使期望与推理一致，推理阶段不做任何丢弃也不缩放。这相当于对大量稀疏子网络做隐式集成，抑制神经元共适应；rate 常取 0.1–0.5，过大反而欠拟合。':
        'During training, randomly zero out units at the rate and multiply the kept branch by 1/p so the expectation matches inference; at inference no dropping and no scaling occurs. This implicitly ensembles many sparse sub-networks, suppressing neuron co-adaptation; rate is often 0.1-0.5, and too large causes underfitting.',
    'Dropout 率': 'Dropout rate',
    '神经元数': 'Number of neurons',
    '期望输出 = x · (1 − p)': 'Expected output = x · (1 - p)',
    '推理时缩放 1/(1−p)': 'At inference scale by 1/(1-p)',
    'Dropout 率通常取 0.2-0.5。': 'Dropout rate usually ranges 0.2-0.5.',
    '📚 深度解析：Dropout 保留期望': '📚 Deep Dive: Dropout Expected Output',
    '训练期以概率 p 随机丢弃神经元，期望输出 E[out]=p·x，破坏 co-adaptation 起正则作用。': 'During training, neurons are randomly dropped with probability p; expected output E[out]=p·x, breaking co-adaptation and acting as regularization.',
    '推理期若不做缩放，需将权重乘 p(或训练期除以 p)使期望一致，即 inverted dropout。': 'At inference, without scaling you must multiply weights by p (or divide by p during training) to match expectations - that is inverted dropout.',
    '常用 p=0.5 于隐藏层、0.0~0.2 于输入层；过大 p 会欠拟合。': 'Commonly p=0.5 for hidden layers, 0.0-0.2 for input layers; too large p causes underfitting.',
    '期望与缩放': 'Expectation and scaling',
    '输入 x=2.0, p=0.5：训练期期望输出=0.5×2=1.0。推理期若保留全部神经元，须把权重×0.5 使输出期望仍为 1.0( inverted dropout 在训练时先除 p)。':
        'Input x=2.0, p=0.5: training expected output = 0.5x2 = 1.0. At inference, keeping all neurons requires multiplying weights by 0.5 so the expected output stays 1.0 (inverted dropout divides by p upfront in training).',
    '为什么推理时要缩放？': 'Why scale at inference?',
    '训练丢弃使激活期望变为 p·x，若不缩放推理输出会比训练期望大 1/p 倍，分布错位导致性能下降；缩放恢复一致期望。':
        'Training dropout makes the activation expectation p·x; without scaling, inference output is 1/p times larger than the training expectation, causing distribution mismatch and performance drop; scaling restores consistent expectation.',
    'dropout 现在还常用吗？': 'Is dropout still commonly used?',
    '在 Transformer 等大模型中常被 LayerNorm/BatchNorm 与权重衰减部分替代，但仍是有效正则；现代多用 dropout 配合注意力 dropout 与随机深度。':
        'In large models like Transformers it is partly replaced by LayerNorm/BatchNorm and weight decay, but remains an effective regularizer; modern usage often pairs dropout with attention dropout and stochastic depth.',
}, ind=IND)

# ---------------- elbow-wcss 手肘法 WCSS 降幅 ----------------
apply_tool('elbow-wcss', '手肘法 WCSS 降幅', 'Elbow Method WCSS Drop', {
    '🤖 手肘法 WCSS 降幅': '🤖 Elbow Method WCSS Drop',
    '通过 WCSS 降幅辅助选择聚类 k。': 'Use the WCSS drop to help choose the cluster count k.',
    '📖 查看「手肘法 WCSS 降幅使用指南」': '📖 View "Elbow Method WCSS Drop User Guide"',
    '降幅 = (WCSS_k − WCSS_{k+1}) / WCSS_k × 100%；比率 = WCSS_{k+1} / WCSS_k': 'Drop = (WCSS_k - WCSS_{k+1}) / WCSS_k x 100%; ratio = WCSS_{k+1} / WCSS_k',
    '手肘法看簇内平方和随 K 增大而下降的边际收益：降幅突然变小的拐点即"手肘"。它依赖人眼判读，簇形状不均时拐点不明显，可辅以轮廓系数或 Calinski-Harabasz 指数交叉验证。':
        'The elbow method looks at the marginal gain as within-cluster sum of squares falls with growing K: the inflection where the drop suddenly shrinks is the "elbow". It relies on eye judgment, the inflection is unclear when clusters are uneven, and can be cross-checked with silhouette or the Calinski-Harabasz index.',
    'k 时 WCSS': 'WCSS at k',
    'k+1 时 WCSS': 'WCSS at k+1',
    '降幅 = (WCSS_k − WCSS_{k+1})/WCSS_k': 'Drop = (WCSS_k - WCSS_{k+1})/WCSS_k',
    '降幅明显减缓处常选为最佳 k。': 'The point where the drop clearly slows is often chosen as the optimal k.',
    '📚 深度解析：手肘法 WCSS 降幅': '📚 Deep Dive: Elbow Method WCSS Drop',
    'WCSS(簇内平方和)=Σ‖x−μ_k‖²，k 越大 WCSS 越小，降幅随 k 增大而递减。': 'WCSS (within-cluster sum of squares) = Σ‖x-μ_k‖²; larger k gives smaller WCSS, and the drop decreases as k grows.',
    '手肘点是降幅明显变缓处，对应较优聚类数 k，是 K-Means 选 k 的经验法。': 'The elbow point is where the drop clearly eases, corresponding to a good cluster count k; it is a heuristic for choosing k in K-Means.',
    '应结合业务可解释性与轮廓系数综合判断，避免只看单一拐点。': 'Combine with business interpretability and the silhouette score for a comprehensive judgment; avoid relying on a single inflection.',
    '选 k': 'Choose k',
    'k=2→WCSS=500, k=3→300(降200), k=4→220(降80), k=5→190(降30)。降幅在 k=3→4 明显放缓，手肘点约 k=3~4，选 k=4 既紧致又不冗余。':
        'k=2->WCSS=500, k=3->300 (drop 200), k=4->220 (drop 80), k=5->190 (drop 30). The drop clearly slows at k=3->4, elbow around k=3-4; choosing k=4 is both compact and non-redundant.',
    '手肘法一定准吗？': 'Is the elbow method always accurate?',
    '不一定。数据无清晰簇结构时拐点模糊，需配合轮廓系数、Gap Statistic 或业务含义；手肘法只是启发式起点。':
        'Not necessarily. When data has no clear cluster structure the inflection is fuzzy; pair it with silhouette, Gap Statistic, or business meaning; the elbow method is only a heuristic starting point.',
    'WCSS 一直降要不要一直加 k？': 'Should you keep adding k since WCSS keeps dropping?',
    "不必。k 接近样本数时 WCSS→0 但失去聚类意义；目标是'信息增益'与'简洁性'平衡，拐点之后边际收益迅速变小。":
        "No. When k approaches the sample count, WCSS->0 but clustering loses meaning; the goal is balancing 'information gain' and 'simplicity', and marginal gains shrink fast after the inflection.",
}, ind=IND)

# ---------------- epoch-time 单轮训练时长 ----------------
apply_tool('epoch-time', '单轮训练时长', 'Single-Epoch Training Time', {
    '⏱️ 单轮训练时长': '⏱️ Single-Epoch Training Time',
    '估算完成若干轮训练所需时长。': 'Estimate the time needed to finish several training epochs.',
    '📖 查看「单轮训练时长使用指南」': '📖 View "Single-Epoch Training Time User Guide"',
    '总步数 = ⌈轮数 × 样本数 / 批量⌉；训练时长(小时) = 轮数 × 样本数 / 批量 / 速度 / 3600': 'Total steps = ceil(epochs x samples / batch); training time (hours) = epochs x samples / batch / throughput / 3600',
    '把步数除以单卡吞吐（样本/秒）再换算成小时，用于排期与算力预算评估。速度为经验值，实际受数据加载、混合精度、通信开销影响，多卡时还要乘上并行效率（通常 0.7–0.9）。':
        'Divide steps by single-card throughput (samples/sec) and convert to hours, for scheduling and compute budgeting. Throughput is empirical; actual values are affected by data loading, mixed precision, and communication overhead; with multiple cards multiply by parallel efficiency (usually 0.7-0.9).',
    '数据集规模': 'Dataset size',
    '批次': 'Batch',
    '吞吐 样本/s': 'Throughput samples/s',
    '步数 = ⌈epochs×数据/批次⌉；时长 = 步数/吞吐': 'Steps = ceil(epochs x data / batch); time = steps / throughput',
    '未计通信与 I/O 开销。': 'Communication and I/O overhead not counted.',
    '📚 深度解析：单轮训练时长': '📚 Deep Dive: Single-Epoch Training Time',
    '单轮时长≈每步平均耗时×步数；总时长=单轮×轮数(+验证/通信开销)。': 'Single-epoch time ~ average per-step time x steps; total time = single-epoch x epochs (+ validation/communication overhead).',
    '步数=⌈样本数/batch⌉，故增大 batch 可减少步数、缩短单轮(受显存上限)。': 'Steps = ceil(samples/batch), so a larger batch reduces steps and shortens a single epoch (bounded by memory).',
    '分布式加速比受通信与负载均衡限制，并非线性随 GPU 数提升。': 'Distributed speedup is limited by communication and load balancing, not linear in the number of GPUs.',
    '训练排期': 'Training schedule',
    '每步 50ms、步数 313、轮数 10 → 单轮≈15.65s，总训练≈156s 不含验证。若数据并行 4 卡步数减半则单轮≈7.8s。':
        'Per step 50ms, 313 steps, 10 epochs -> single epoch ~15.65s, total training ~156s excluding validation. With 4-card data parallelism halving steps, single epoch ~7.8s.',
    '显存不够 batch 又想快怎么办？': 'Not enough memory but want a fast batch?',
    '用梯度累积模拟大 batch(不增显存)，或降低精度(混合精度)提速；也可优化数据管道减少 IO 等待，避免 GPU 空转。':
        'Use gradient accumulation to simulate a large batch (no extra memory), or lower precision (mixed precision) to speed up; also optimize the data pipeline to reduce IO waits and avoid GPU idling.',
    '实测比估算慢很多？': 'Measured much slower than estimated?',
    '多半是数据加载瓶颈或通信开销。检查 DataLoader 预取、SSD/缓存、NCCL 拓扑；纯计算外的等待会显著拉长单轮。':
        'Mostly a data-loading bottleneck or communication overhead. Check DataLoader prefetch, SSD/cache, NCCL topology; waits outside pure compute significantly lengthen a single epoch.',
}, ind=IND)

# ---------------- flops 模型 flops 估算 ----------------
apply_tool('flops', '模型 flops 估算', 'Model FLOPs Estimator', {
    '🔮 模型 flops 估算': '🔮 Model FLOPs Estimator',
    '估算全连接层和卷积层的前向 FLOPs。': 'Estimate forward FLOPs of fully-connected and convolutional layers.',
    '📖 查看「模型 flops 估算使用指南」': '📖 View "Model FLOPs Estimator User Guide"',
    '卷积 FLOPs ≈ 2·H·W·C_in·C_out·K²；全连接 FLOPs ≈ 2·in·out；MACs ≈ FLOPs / 2': 'Conv FLOPs ~ 2·H·W·C_in·C_out·K²; FC FLOPs ~ 2·in·out; MACs ~ FLOPs / 2',
    '按输出特征图每个元素所需的乘加次数累计：卷积为 K²·C_in 次乘加、输出 HWC_out 个元素，乘 2 得 FLOPs。1 MAC = 1 次乘加 = 2 FLOPs，硬件标称算力多用 MACs，对比时要注意单位换算。':
        'Accumulate the multiply-adds needed per output feature-map element: convolution is K²·C_in MACs times HWC_out output elements, times 2 for FLOPs. 1 MAC = 1 multiply-add = 2 FLOPs; hardware ratings often use MACs, so mind the unit conversion when comparing.',
    '输入高': 'Input height',
    '输入宽': 'Input width',
    '输入通道': 'Input channels',
    '输出通道': 'Output channels',
    '卷积核': 'Kernel',
    '全连接输入': 'FC input',
    '全连接输出': 'FC output',
    '卷积 FLOPs ≈ 2 × H × W × C_in × C_out × K²': 'Conv FLOPs ~ 2 x H x W x C_in x C_out x K²',
    '全连接 FLOPs ≈ 2 × in × out': 'FC FLOPs ~ 2 x in x out',
    'FLOPs 衡量模型计算量。': 'FLOPs measure a model\'s compute.',
    '📚 深度解析：模型 flops 估算': '📚 Deep Dive: Model FLOPs Estimator',
    '全连接层 FLOPs≈2·in·out·batch·seq(乘加各算一次)。': 'FC layer FLOPs ~ 2·in·out·batch·seq (multiply and add each counted once).',
    '卷积层 FLOPs≈2·k²·C_in·C_out·H_out·W_out。': 'Conv layer FLOPs ~ 2·k²·C_in·C_out·H_out·W_out.',
    'FLOPs 衡量算力需求(时间)，结合参数量评估推理成本与硬件选型。': 'FLOPs measure compute demand (time); combined with parameter count they assess inference cost and hardware selection.',
    '卷积层算力': 'Conv layer compute',
    '3×3 卷积, C_in=64,C_out=128, 特征图 56×56：FLOPs≈2×9×64×128×56×56≈4.66×10⁹ 次/样本。可见大特征图与多通道下卷积算力增长极快。':
        '3x3 conv, C_in=64, C_out=128, feature map 56x56: FLOPs ~ 2x9x64x128x56x56 ~ 4.66x10⁹ per sample. This shows conv compute grows extremely fast with large feature maps and many channels.',
    'FLOPs 越大模型越慢？': 'Does higher FLOPs mean a slower model?',
    '通常如此，但还受显存带宽与并行度影响；某些高 FLOPs 算子若访存密集会被带宽卡住，实际延迟需结合硬件实测。':
        'Usually yes, but it also depends on memory bandwidth and parallelism; some high-FLOPs operators are memory-bound and stall on bandwidth, so real latency needs hardware measurement.',
    '训练 FLOPs 怎么算？': 'How to estimate training FLOPs?',
    '约为前向的 2~3 倍(反向含梯度计算)，再乘训练 token 数；大模型的训练算力常用 Kaplan 缩放律直接由参数量与数据量估算。':
        'Roughly 2-3x the forward (backward includes gradient computation), then multiplied by training token count; large-model training compute is often estimated directly from parameters and data via Kaplan scaling laws.',
    '如何使用模型 flops 估算': 'How to use the Model FLOPs Estimator',
}, ind=IND)

# ---------------- grad-accumulation 梯度累积步数 ----------------
apply_tool('grad-accumulation', '梯度累积步数', 'Gradient Accumulation Steps', {
    '🧮 梯度累积步数': '🧮 Gradient Accumulation Steps',
    '计算达到目标批次所需的累积步数。': 'Compute the accumulation steps needed to reach a target batch.',
    '📖 查看「梯度累积步数使用指南」': '📖 View "Gradient Accumulation Steps User Guide"',
    '累积步数 = ⌈目标批量 / (单卡批量 × 卡数)⌉': 'Accumulation steps = ceil(target batch / (per-card batch x cards))',
    '显存不够放大 batch 时，用小批量连续跑若干步再把梯度相加、只做一次参数更新，等效于大批量训练。注意归一化层统计与 BatchNorm 仍按小批量计算，与真正的大 batch 不完全等价；学习率要按等效批量同步放大。':
        'When memory cannot fit a larger batch, run several small batches consecutively, sum their gradients, and update parameters only once, equivalent to large-batch training. Note that normalization-layer statistics and BatchNorm still compute per small batch, not fully equivalent to a true large batch; scale the learning rate by the effective batch.',
    '目标批次': 'Target batch',
    '单卡批次': 'Per-card batch',
    '累积 = ⌈目标批次 /(单卡批次×GPU数)⌉': 'Accumulation = ceil(target batch /(per-card batch x GPUs))',
    '累积步数越多显存占用越低。': 'More accumulation steps means lower memory usage.',
    '📚 深度解析：梯度累积步数': '📚 Deep Dive: Gradient Accumulation Steps',
    '等效 batch=单卡 batch×累积步数×GPU 数；累积步数=目标 batch/单卡 batch。': 'Effective batch = per-card batch x accumulation steps x GPU count; accumulation steps = target batch / per-card batch.',
    '显存不足时用小 batch 累积多次再更新，模拟大 batch 的统计效果。': 'When memory is insufficient, accumulate several small batches before updating, simulating the statistical effect of a large batch.',
    '累积期间不更新参数、只累加梯度，故优化步数变少、训练更慢但等效 batch 更大。': 'During accumulation parameters are not updated, only gradients summed, so optimization steps are fewer, training slower, but the effective batch is larger.',
    '累积步数计算': 'Accumulation step calculation',
    '目标 batch=128、单卡 batch=32、2 卡 → 累积步数=128/(32×2)=2。每 2 个小步累加梯度后更新一次，等效 batch=128。':
        'Target batch=128, per-card batch=32, 2 cards -> accumulation steps = 128/(32x2)=2. Every 2 small steps sum gradients then update once; effective batch=128.',
    '累积会影响收敛吗？': 'Does accumulation affect convergence?',
    '等效 batch 相同则统计近似一致，但累积使更新频率降低、训练更慢；学习率应按等效 batch 调整，而非单卡 batch。':
        'With the same effective batch the statistics are approximately consistent, but accumulation lowers update frequency and slows training; tune the learning rate by effective batch, not per-card batch.',
    '累积步数设太大怎样？': 'What if accumulation steps are set too large?',
    '等效 batch 过大易泛化变差、显存虽省但训练极慢；且 BN 统计仍按小 batch，与真实大 batch 有偏差，需同步调大 BN 动量或使用同步 BN。':
        'An overly large effective batch easily hurts generalization; memory is saved but training is extremely slow; and BN statistics still follow the small batch, deviating from a true large batch, so increase BN momentum or use synchronized BN.',
}, ind=IND)

print('gen_ai_b3 done')
