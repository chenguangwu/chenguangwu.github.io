# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch1（编号型 ai-4..ai-17，14 工具）。
逐条语义化翻译 ML/数学类计算器文本节点；值纯 ASCII/英文，避开 CJK 与中文标点。
调用共享写入器 apply_tool（ind='ai'）。运行：python3 _en-i18n/gen_ai_b1.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'

# ---------------- ai-4 欧氏距离 ----------------
apply_tool('ai-4', '欧氏距离', 'Euclidean Distance', {
    '📖 查看「欧氏距离使用指南」': '📖 View "Euclidean Distance User Guide"',
    '欧氏距离 = √[Σ(aᵢ − bᵢ)²]；曼哈顿距离 = Σ|aᵢ − bᵢ|；余弦相似度 = (a·b)/(‖a‖·‖b‖)':
        'Euclidean distance = √[Σ(aᵢ − bᵢ)²]; Manhattan distance = Σ|aᵢ − bᵢ|; Cosine similarity = (a·b)/(‖a‖·‖b‖)',
    '三种常用向量度量并列给出：欧氏看绝对位置差，受量纲影响需先标准化；曼哈顿按轴累加，在高维稀疏场景更稳；余弦只看夹角、忽略模长，因此常用于 embedding 与文本相似度比较。':
        'Three common vector metrics are shown side by side: Euclidean captures absolute position difference and is scale-sensitive so features should be standardized first; Manhattan sums axis-wise and is more stable in high-dimensional sparse settings; cosine looks only at the angle and ignores magnitude, so it is commonly used for embeddings and text similarity.',
    '欧氏距离 = √Σ(aᵢ−bᵢ)²': 'Euclidean distance = √Σ(aᵢ−bᵢ)²',
    '余弦相似度 = A·B / (|A||B|)': 'Cosine similarity = A·B / (|A||B|)',
    '余弦相似度范围为 [−1, 1]。': 'Cosine similarity ranges in [−1, 1].',
    '📚 深度解析：欧氏距离': '📚 Deep Dive: Euclidean Distance',
    '欧氏距离 d(x,y)=√(Σ(xᵢ−yᵢ)²)，衡量向量在空间中的绝对距离。':
        'Euclidean distance d(x,y)=√(Σ(xᵢ−yᵢ)²) measures the absolute distance between vectors in space.',
    'cos(x,y)=Σxᵢyᵢ/(‖x‖·‖y‖)，衡量方向一致性而非模长。':
        'cos(x,y)=Σxᵢyᵢ/(‖x‖·‖y‖) measures directional agreement rather than magnitude.',
    '高维空间中欧氏距离因维度灾难趋于收敛，语义比对优先用余弦。':
        'In high-dimensional space Euclidean distance converges due to the curse of dimensionality, so prefer cosine for semantic comparison.',
    '二维向量距离': '2D Vector Distance',
    'x=(3,4), y=(0,0)：d=√(3²+4²)=5。‖x‖=5，若 y 为零向量则余弦分母为 0 无定义，比对前需剔除零向量。':
        'x=(3,4), y=(0,0): d=√(3²+4²)=5. ‖x‖=5; if y is a zero vector the cosine denominator is 0 and undefined, so remove zero vectors before comparison.',
    '欧氏距离与余弦相似度怎么选？': 'How to choose between Euclidean distance and cosine similarity?',
    '关心量级/绝对差用欧氏；关心方向/语义用余弦。文本与图像嵌入几乎都用余弦，因为':
        'Use Euclidean when magnitude or absolute difference matters; use cosine when direction or semantics matter. Text and image embeddings almost always use cosine because ',
    '常受词频或亮度影响、不代表语义强度。':
        'magnitude is often affected by word frequency or brightness and does not represent semantic strength.',
    '维度很高时距离失效怎么办？':
        'What if distance becomes unreliable in very high dimensions?',
    '先对特征做标准化(z-score)消除量纲，或降维(PCA/t-SNE)后再比对；语义场景直接用余弦距离更稳定。':
        'First standardize features (z-score) to remove scale, or reduce dimensionality (PCA/t-SNE) before comparing; in semantic settings cosine distance is more stable directly.',
    '如何使用欧氏距离': 'How to use Euclidean Distance',
    '关心量级/绝对差用欧氏；关心方向/语义用余弦。文本与图像嵌入几乎都用余弦，因为向量模长常受词频或亮度影响、不代表语义强度。':
        'Use Euclidean when magnitude or absolute difference matters; use cosine when direction or semantics matter. Text and image embeddings almost always use cosine because vector magnitude is often affected by word frequency or brightness and does not represent semantic strength.',
}, ind=IND)

# ---------------- ai-5 批量大小迭代次数 ----------------
apply_tool('ai-5', '批量大小迭代次数', 'Batch Size and Iterations', {
    '📖 查看「批量大小迭代次数使用指南」': '📖 View "Batch Size and Iterations User Guide"',
    '每轮步数 = ⌈样本数 / 批量⌉；总步数 = 每轮步数 × 轮数；最后一批大小 = 样本数 mod 批量（余 0 则取批量）':
        'Steps per epoch = ⌈samples / batch⌉; total steps = steps per epoch × epochs; last batch size = samples mod batch (if 0 use batch)',
    '参数更新次数由"样本数/批量"决定而非轮数，直接决定训练时长与学习率调度横坐标。最后一批不满时需要决定是否丢弃（drop_last）：丢弃可让 BatchNorm 统计稳定，保留则能多用一点数据。':
        'The number of parameter updates is determined by "samples / batch" rather than epochs, which directly governs training time and the x-axis of the learning-rate schedule. When the last batch is incomplete you must decide whether to drop it (drop_last): dropping keeps BatchNorm statistics stable, keeping uses a bit more data.',
    '训练 epoch 数': 'Training epochs',
    'steps_per_epoch = ceil(样本数 / batch_size)': 'steps_per_epoch = ceil(samples / batch_size)',
    '总步数 = steps × epochs': 'Total steps = steps × epochs',
    '最后一批可能不满。': 'The last batch may be incomplete.',
    '📚 深度解析：批量大小迭代次数': '📚 Deep Dive: Batch Size and Iterations',
    '每轮迭代步数 steps=⌈N/batch_size⌉，N 为训练样本总数。':
        'Iteration steps per epoch steps=⌈N/batch_size⌉, where N is the total number of training samples.',
    '总优化步数=epochs×steps；batch 越大单轮步数越少但显存与通信开销越高。':
        'Total optimization steps = epochs × steps; a larger batch reduces steps per epoch but raises memory and communication cost.',
    '分布式有效批次=单卡 batch×': 'Distributed effective batch = single-GPU batch',
    '×GPU 数。': ' × GPU count.',
    '一万样本每批 32': 'Ten thousand samples, batch 32',
    'N=10000, batch=32 → steps=⌈10000/32⌉=313 步/轮；训练 10 轮共约 3130 步。若 4 卡数据并行每卡 batch=32，等效 batch=128，steps 降至 79/轮。':
        'N=10000, batch=32 → steps=⌈10000/32⌉=313 steps/epoch; training 10 epochs totals about 3130 steps. With 4-GPU data parallelism at batch=32 each, the effective batch=128 and steps drop to 79/epoch.',
    'batch size 是不是越大越好？': 'Is a larger batch size always better?',
    '不是。大 batch 收敛快但泛化常变差，需配合更大学习率与更强正则；小 batch 梯度噪声大却常泛化更好，需在显存与泛化间权衡。':
        'No. A large batch converges faster but generalization often degrades, requiring a larger learning rate and stronger regularization; a small batch has noisier gradients yet often generalizes better, so you trade off memory against generalization.',
    '最后一个不完整的 batch 怎么处理？': 'How to handle the last incomplete batch?',
    '默认保留尾批(大小不足 batch)；也可 drop_last 丢弃以避免形状不一致，步数用向上取整即包含该尾批。':
        'By default keep the tail batch (smaller than batch); you can also set drop_last to discard it to avoid shape mismatch, and steps use the ceiling which includes that tail batch.',
}, ind=IND)

# ---------------- ai-6 参数数量估算 ----------------
apply_tool('ai-6', '参数数量估算', 'Parameter Count Estimator', {
    '📖 查看「参数数量估算使用指南」': '📖 View "Parameter Count Estimator User Guide"',
    '全连接参数 = in × out + out（偏置）；3×3 卷积参数 = in × out × 9 + out；显存 MB = 参数 × 4 / 1024 / 1024':
        'Fully-connected params = in × out + out (bias); 3x3 conv params = in × out × 9 + out; memory MB = params × 4 / 1024 / 1024',
    '按层的权重矩阵规模累加估算参数量，再按每参数 4 字节（FP32）折算显存。这只是推理权重的下限，训练还要额外放梯度、优化器状态（Adam 再翻 2 倍）与激活值，实际占用通常是权重的 4–6 倍。':
        'Estimate the parameter count by summing the weight-matrix size of each layer, then convert to memory at 4 bytes per parameter (FP32). This is only a lower bound for inference weights; training also needs gradients, optimizer states (Adam adds 2x) and activations, so actual usage is typically 4-6x the weights.',
    '输入维度': 'Input dimension',
    '输出维度': 'Output dimension',
    '是否含偏置 1=是': 'Include bias 1=yes',
    '是否卷积 1=是': 'Is convolutional 1=yes',
    '全连接：params = in × out + out（bias）': 'Fully-connected: params = in × out + out (bias)',
    '卷积 3×3：params = in × out × 9 + out': 'Conv 3x3: params = in × out × 9 + out',
    '用于快速估算模型规模。': 'Used for a quick estimate of model size.',
    '📚 深度解析：参数数量估算': '📚 Deep Dive: Parameter Count Estimator',
    '全连接层参数=(输入维度+1)×输出维度，+1 为偏置。':
        'Fully-connected layer params = (input dimension + 1) × output dimension, where +1 is the bias.',
    '卷积层参数=(k²×C_in+1)×C_out，k 为核边长；深度可分离卷积参数量显著降低。':
        'Conv layer params = (k² × C_in + 1) × C_out, where k is the kernel edge length; depthwise separable convolution greatly reduces the parameter count.',
    '参数量直接决定显存(≈参数量×精度字节)与推理延迟，是轻量化设计的核心约束。':
        'Parameter count directly determines memory (≈ params × precision bytes) and inference latency, and is the core constraint in lightweight design.',
    '卷积层参数量': 'Conv layer parameters',
    '3×3 卷积、输入通道 64、输出通道 128：参数=(3²×64+1)×128=(576+1)×128=73728。若改为深度可分离(3×3×64+1×64×128)=576+8192=8768，仅为原先约 12%。':
        '3x3 conv, input channels 64, output channels 128: params = (3² × 64 + 1) × 128 = (576 + 1) × 128 = 73728. Switching to depthwise separable (3×3×64 + 1×64×128) = 576 + 8192 = 8768, only about 12% of the original.',
    '为什么卷积层参数量远小于全连接？': 'Why is the conv layer parameter count far smaller than fully-connected?',
    '卷积权值共享且局部连接，参数只与核大小、通道数有关，与特征图尺寸无关；全连接则随输入输出维度乘积增长。':
        'Convolution shares weights and connects locally, so parameters depend only on kernel size and channel counts, not feature-map size; fully-connected grows with the product of input and output dimensions.',
    '偏置是否总要加？': 'Should bias always be added?',
    '并非必须。BN 后接的卷积常设 bias=False 以免冗余；最后一层或需学习截距时保留偏置。':
        'Not necessarily. A conv followed by BN often sets bias=False to avoid redundancy; keep bias for the last layer or when an intercept must be learned.',
    '如何使用参数数量估算': 'How to use Parameter Count Estimator',
}, ind=IND)

# ---------------- ai-7 混淆矩阵指标 ----------------
apply_tool('ai-7', '混淆矩阵指标', 'Confusion Matrix Metrics', {
    '📖 查看「混淆矩阵指标使用指南」': '📖 View "Confusion Matrix Metrics User Guide"',
    'MCC 同时用到混淆矩阵四格，取值 [−1,1]，0 表示与随机猜测相当，在不平衡数据上比准确率稳健。FDR 回答"报为正的结果里有多少是误报"，与精确率互补（P = 1 − FDR），常用于多重假设检验的校正判读。':
        'MCC uses all four cells of the confusion matrix, ranges in [-1,1], and 0 means on par with random guessing, making it more robust than accuracy on imbalanced data. FDR answers "of the results called positive, how many are false alarms", complementing precision (P = 1 - FDR), and is often used to interpret corrections in multiple-hypothesis testing.',
    'MCC 范围 [−1,1]，是均衡的评估指标。': 'MCC ranges in [-1,1] and is a balanced evaluation metric.',
    '📚 深度解析：混淆矩阵指标': '📚 Deep Dive: Confusion Matrix Metrics',
    '马修斯': 'Matthews',
    '相关系数': 'correlation coefficient',
    'MCC=(TP·TN−FP·FN)/√((TP+FP)(TP+FN)(TN+FP)(TN+FN))，综合四类计数，类别不平衡时优于准确率。':
        'MCC=(TP·TN−FP·FN)/√((TP+FP)(TP+FN)(TN+FP)(TN+FN)) combines all four counts and beats accuracy under class imbalance.',
    '假正率 FPR=FP/(FP+TN)，衡量负类被误判为正的比例。':
        'False positive rate FPR=FP/(FP+TN) measures the proportion of negatives wrongly called positive.',
    'MCC 取值 [−1,1]，1 为完美、0 为随机、负值为反向相关。':
        'MCC ranges in [-1,1]: 1 is perfect, 0 is random, negative means reverse correlation.',
    '不平衡二分类': 'Imbalanced binary classification',
    'TP=80, FP=20, FN=10, TN=890：准确率=(80+890)/1000=97%，但 MCC=(80×890−20×10)/√(100×90×910×900)=71000/√7371000000≈0.827，FPR=20/(20+890)=2.2%。':
        'TP=80, FP=20, FN=10, TN=890: accuracy=(80+890)/1000=97%, but MCC=(80×890−20×10)/√(100×90×910×900)=71000/√7371000000≈0.827, FPR=20/(20+890)=2.2%.',
    '为什么准确率高分却不可信？': 'Why is a high accuracy score unreliable?',
    '正负样本极不平衡时全猜负类也能得高准确率。MCC 同时用四类计数，能暴露这种假象，是更稳健的单一指标。':
        'When positives and negatives are extremely imbalanced, always guessing negative still yields high accuracy. MCC uses all four counts and exposes this illusion, making it a more robust single metric.',
    'FPR 和 FNR 有何不同？': 'What is the difference between FPR and FNR?',
    'FPR=FP/(FP+TN) 是负类误判率；FNR=FN/(FN+TP) 是漏检率。医学筛查通常压低 FNR(少漏诊)，反垃圾则压低 FPR(少误杀)。':
        'FPR=FP/(FP+TN) is the false-positive rate; FNR=FN/(FN+TP) is the miss rate. Medical screening usually lowers FNR (fewer missed diagnoses), while anti-spam lowers FPR (fewer false kills).',
}, ind=IND)

# ---------------- ai-8 梯度下降一步 ----------------
apply_tool('ai-8', '梯度下降一步', 'Gradient Descent Step', {
    '📖 查看「梯度下降一步使用指南」': '📖 View "Gradient Descent Step User Guide"',
    'w′ = w − lr·(grad + 2λw)，其中 2λw 为 L2 正则梯度；Δw = −lr·(grad + 2λw)':
        "w' = w − lr·(grad + 2λw), where 2λw is the L2 regularization gradient; Δw = −lr·(grad + 2λw)",
    '带 L2（权重衰减）的 SGD 单步更新：每次先按梯度与衰减项的和反向走一小步。注意真正的 weight decay 应独立于梯度缩放施加，而 Adam 中直接把 2λw 加进梯度会被自适应学习率抵消，因此 AdamW 才把衰减挪到更新步。':
        'One SGD step with L2 (weight decay): each time move a small step opposite to the sum of gradient and decay term. Note that true weight decay should be applied independently of gradient scaling; adding 2λw directly into the gradient inside Adam is cancelled by the adaptive learning rate, which is why AdamW moves the decay to the update step.',
    '当前权重': 'Current weight',
    '梯度': 'Gradient',
    '学习率': 'Learning rate',
    'L2 正则化': 'L2 regularization',
    'L2 正则化使权重向零收缩。': 'L2 regularization shrinks weights toward zero.',
    '📚 深度解析：梯度下降一步': '📚 Deep Dive: Gradient Descent Step',
    '参数更新 w←w−η·∇L(w)，η 为学习率，∇L 为损失对参数的梯度。':
        'Parameter update w←w−η·∇L(w), where η is the learning rate and ∇L is the gradient of the loss w.r.t. parameters.',
    '学习率过大易震荡不收敛，过小则收敛缓慢；常配合动量或学习率调度。':
        'Too large a learning rate oscillates and fails to converge; too small converges slowly; usually paired with momentum or a learning-rate schedule.',
    '该工具演示单变量一步更新，用于直观理解收敛轨迹与 η 的影响。':
        'This tool demonstrates a single-variable one-step update to build intuition for the convergence trajectory and the effect of η.',
    '单变量一步更新': 'Single-variable one-step update',
    'w=2.0, 梯度 ∂L/∂w=−3.0, η=0.1 → w←2.0−0.1×(−3.0)=2.3。梯度为负说明增大 w 能降损失，故 w 向正方向移动。':
        'w=2.0, gradient ∂L/∂w=−3.0, η=0.1 → w←2.0−0.1×(−3.0)=2.3. A negative gradient means increasing w lowers the loss, so w moves in the positive direction.',
    '梯度为负为什么参数要增加？': 'Why does a negative gradient increase the parameter?',
    '更新式 w←w−η∇L，梯度为负时减去负数等于加正数，沿损失下降方向(负梯度方向)移动，这是梯度下降的本质。':
        'The update w←w−η∇L: when the gradient is negative, subtracting a negative equals adding a positive, moving along the loss-descent direction (negative gradient direction) - this is the essence of gradient descent.',
    '学习率怎么初选？': 'How to choose an initial learning rate?',
    '常用 1e-3~1e-1 再扫描；配合学习率预热与余弦退火更稳。出现 loss 发散(NaN)立即下调 η 一个数量级。':
        'Commonly start with 1e-3 to 1e-1 then sweep; pair with learning-rate warm-up and cosine annealing for stability. If loss diverges (NaN), immediately lower η by an order of magnitude.',
}, ind=IND)

# ---------------- ai-9 信息增益近似 ----------------
apply_tool('ai-9', '信息增益近似', 'Information Gain Approx.', {
    '📖 查看「信息增益近似使用指南」': '📖 View "Information Gain Approx. User Guide"',
    '基尼 = 2p(1 − p)；加权子基尼 = w_L·2p_L(1 − p_L) + (1 − w_L)·2p_R(1 − p_R)；基尼增益 = 根基尼 − 加权子基尼；熵 = −p·log₂p − (1 − p)·log₂(1 − p)':
        'Gini = 2p(1 − p); weighted child Gini = w_L·2p_L(1 − p_L) + (1 − w_L)·2p_R(1 − p_R); Gini gain = parent Gini − weighted child Gini; entropy = −p·log₂p − (1 − p)·log₂(1 − p)',
    '决策树分裂准则：基尼与熵都衡量节点纯度，取值越小越纯。基尼计算更快（无对数）是 CART 默认；熵对纯度变化略敏感。二者选出的分裂在绝大多数数据集上差异极小。':
        "Decision-tree split criteria: both Gini and entropy measure node purity, with smaller values meaning purer. Gini computes faster (no logarithm) and is CART's default; entropy is slightly more sensitive to purity changes. The splits they pick differ negligibly on most datasets.",
    '根节点正例比例': 'Root positive ratio',
    '左子树正例比例': 'Left child positive ratio',
    '左子树权重': 'Left child weight',
    '右子树正例比例': 'Right child positive ratio',
    '基尼 = 2p(1−p)': 'Gini = 2p(1−p)',
    '熵 = −p·log₂p − (1−p)·log₂(1−p)': 'Entropy = −p·log₂p − (1−p)·log₂(1−p)',
    '增益 = 父不纯度 − 加权子不纯度': 'Gain = parent impurity − weighted child impurity',
    '决策树分裂选择增益最大的特征。': 'A decision tree split picks the feature with the largest gain.',
    '📚 深度解析：信息增益近似': '📚 Deep Dive: Information Gain Approx.',
    '信息熵 H=−Σpᵢlog₂pᵢ；基尼不纯度 G=1−Σpᵢ²，均衡量节点混杂度。':
        'Information entropy H=−Σpᵢlog₂pᵢ; Gini impurity G=1−Σpᵢ², both measuring node mixedness.',
    '信息增益=父节点不纯度−Σ(子节点样本占比×子节点不纯度)，用于决策树分裂特征选择。':
        'Information gain = parent impurity − Σ(child sample proportion × child impurity), used for decision-tree split feature selection.',
    '基尼计算更快且对错误分类敏感，CART 默认用基尼，ID3/C4.5 用熵。':
        'Gini computes faster and is sensitive to misclassification; CART uses Gini by default, ID3/C4.5 use entropy.',
    '二分类节点分裂': 'Binary-class node split',
    '父节点正类 6/负类 6，熵=1.0；按某特征分为左(5正1负)右(1正5负)。左熵≈0.65、右熵≈0.65，加权=0.5×0.65+0.5×0.65=0.65，信息增益=1.0−0.65=0.35。':
        'Parent node 6 positive / 6 negative, entropy=1.0; split by a feature into left (5 pos, 1 neg) and right (1 pos, 5 neg). Left entropy≈0.65, right entropy≈0.65, weighted=0.5×0.65+0.5×0.65=0.65, information gain=1.0−0.65=0.35.',
    '信息增益和基尼该用哪个？': 'Which to use, information gain or Gini?',
    '两者结论常一致。基尼计算免对数更快，对多数类错误更敏感；熵对不纯度变化更敏感、偏向多值特征，需用增益率修正偏置。':
        'Their conclusions often agree. Gini avoids the logarithm and is faster, more sensitive to majority-class errors; entropy is more sensitive to impurity changes and biased toward multi-valued features, so gain ratio is needed to correct the bias.',
    '为什么信息增益偏向取值多的特征？': 'Why does information gain favor features with many values?',
    '取值越多越容易把样本分得更纯，增益天然偏大。C4.5 用增益率(增益/分支熵)惩罚多值特征以纠偏。':
        'More values make it easier to split samples purer, so the gain is naturally larger. C4.5 uses gain ratio (gain / split entropy) to penalize multi-valued features and correct the bias.',
    '如何使用信息增益近似': 'How to use Information Gain Approx.',
}, ind=IND)

# ---------------- ai-10 图像卷积输出尺寸 ----------------
apply_tool('ai-10', '图像卷积输出尺寸', 'Conv Output Size', {
    '📖 查看「图像卷积输出尺寸使用指南」': '📖 View "Conv Output Size User Guide"',
    '输出尺寸 = ⌊(W + 2P − K − (K − 1)(D − 1))/S⌋ + 1；感受野 = K + (K − 1)(D − 1)':
        'Output size = ⌊(W + 2P − K − (K − 1)(D − 1))/S⌋ + 1; receptive field = K + (K − 1)(D − 1)',
    '卷积输出尺寸由输入宽、卷积核、填充、步长与膨胀率共同决定，结果须为整数，非整除时多数框架向下取整（丢弃边缘）。膨胀卷积用 (K−1)(D−1) 扩大感受野而不增加参数，适合密集预测任务。':
        'Conv output size is jointly determined by input width, kernel, padding, stride and dilation; the result must be an integer, and when not divisible most frameworks floor it (dropping edges). Dilated convolution uses (K−1)(D−1) to enlarge the receptive field without adding parameters, suiting dense prediction tasks.',
    '输入尺寸': 'Input size',
    '卷积核大小': 'Kernel size',
    '空洞率': 'Dilation rate',
    '用于设计 CNN 网络结构。': 'Used to design CNN network structures.',
    '📚 深度解析：图像卷积输出尺寸': '📚 Deep Dive: Conv Output Size',
    '输出尺寸 out=⌊(in+2×pad−kernel)/stride⌋+1（向下取整）。':
        'Output size out=⌊(in+2×pad−kernel)/stride⌋+1 (floor).',
    '池化层用相同公式；空洞卷积需把 kernel 替换为 dilation×(k−1)+1。':
        'Pooling uses the same formula; for dilated convolution replace kernel with dilation×(k−1)+1.',
    'Design CNN 时需逐层推算特征图尺寸，确保首尾维度匹配、不出现负数。': 'When designing a CNN you must compute feature-map size layer by layer, ensuring the first and last dimensions match and never go negative.',
    '设计 CNN 时需逐层推算特征图尺寸，确保首尾维度匹配、不出现负数。': 'When designing a CNN you must compute feature-map size layer by layer, ensuring the first and last dimensions match and never go negative.',
    '卷积层尺寸推算': 'Conv layer size computation',
    '输入 224×224，kernel=3, stride=1, padding=1 → out=224。若 stride=2 → out=⌊(224+2−3)/2⌋+1=112，特征图减半，通道数不变。':
        'Input 224×224, kernel=3, stride=1, padding=1 → out=224. If stride=2 → out=⌊(224+2−3)/2⌋+1=112, the feature map halves while the channel count stays the same.',
    'padding 有什么用？': 'What is padding for?',
    'same padding(使 out=in/stride)保护边缘信息、控制尺寸；valid(无填充)逐步缩小特征图。边缘像素被卷积覆盖次数少，填充可缓解边缘信息丢失。':
        'Same padding (making out=in/stride) preserves edge information and controls size; valid (no padding) shrinks the feature map step by step. Edge pixels are covered by convolution fewer times, and padding relieves edge information loss.',
    '输出出现小数或负数说明什么？': 'What do fractional or negative outputs indicate?',
    '说明参数组合非法(如 stride 过大、kernel 超过输入)。需调小 stride、增大 padding 或减小 kernel，直到公式结果≥1。':
        'It means the parameter combination is invalid (e.g. stride too large, kernel exceeding input). Reduce stride, increase padding, or shrink kernel until the formula result is >=1.',
}, ind=IND)

# ---------------- ai-11 过拟合诊断 ----------------
apply_tool('ai-11', '过拟合诊断', 'Overfitting Diagnosis', {
    '📖 查看「过拟合诊断使用指南」': '📖 View "Overfitting Diagnosis User Guide"',
    '损失差距 = 验证损失 − 训练损失；准确率差距 = 训练准确率 − 验证准确率；风险判据：损失差 > 0.3 或准确率差 > 10%':
        'Loss gap = validation loss − training loss; accuracy gap = training accuracy − validation accuracy; risk rule: loss gap > 0.3 or accuracy gap > 10%',
    '训练指标持续优于验证指标就是过拟合信号，差距越大越强。阈值 0.3 / 10% 是常用经验线，但不同任务量纲差异很大，更可靠的是看验证损失是否开始回升（应触发早停）。':
        'When training metrics keep beating validation metrics that is an overfitting signal, and the larger the gap the stronger it is. The 0.3 / 10% thresholds are common rules of thumb, but different tasks differ greatly in scale, so the more reliable sign is whether validation loss starts to rise again (which should trigger early stopping).',
    '训练损失': 'Training loss',
    '验证损失': 'Validation loss',
    '训练准确率 %': 'Training accuracy %',
    '验证准确率 %': 'Validation accuracy %',
    '过拟合：训练表现远好于验证表现': 'Overfitting: training performance far better than validation',
    '准确率差距 >10% 或损失差距 >0.3 通常视为过拟合信号。':
        'An accuracy gap > 10% or loss gap > 0.3 is usually treated as an overfitting signal.',
    '📚 深度解析：过拟合诊断': '📚 Deep Dive: Overfitting Diagnosis',
    '对比训练与验证损失：训练降而验证升→过拟合；两者都高→欠拟合。':
        'Compare training and validation loss: training falls while validation rises means overfitting; both high means underfitting.',
    '过拟合时加大 dropout、权重衰减或数据增强；欠拟合时加深加宽或减小正则。':
        'For overfitting, increase dropout, weight decay or data augmentation; for underfitting, go deeper/wider or reduce regularization.',
    '早停在验证损失连续上升前保存最优权重，是性价比最高的正则手段。':
        'Early stopping saves the best weights before validation loss rises consecutively, the most cost-effective regularization.',
    '损失曲线判读': 'Loss curve interpretation',
    '训练 loss 从 0.9 降到 0.1，验证 loss 从 0.9 降到 0.5 后回升到 0.7 → 第 5 轮附近开始过拟合，应在验证最低点(0.5)早停并回退权重。':
        'Training loss drops from 0.9 to 0.1, validation loss drops from 0.9 to 0.5 then rises back to 0.7 - overfitting begins around epoch 5; stop early at the validation minimum (0.5) and revert weights.',
    '训练和验证都很高怎么办？': 'What if both training and validation are high?',
    '这是欠拟合，模型容量或训练不足。可增大网络、延长训练、降低正则强度，或检查特征与标签质量。':
        'This is underfitting, from insufficient model capacity or training. Enlarge the network, train longer, lower regularization, or check feature and label quality.',
    '验证集必须和训练集同分布吗？': 'Must the validation set share the training set distribution?',
    '应尽量同分布以反映真实泛化；若验证集分布偏移，验证损失只能衡量对该子集的拟合，不能代表线上表现。':
        'It should be as close as possible to reflect true generalization; if the validation set is distribution-shifted, validation loss only measures fit to that subset and cannot represent online performance.',
}, ind=IND)

# ---------------- ai-12 数据增强有效量 ----------------
apply_tool('ai-12', '数据增强有效量', 'Effective Augmentation', {
    '📖 查看「数据增强有效量使用指南」': '📖 View "Effective Augmentation User Guide"',
    '理论扩充量 = 基数 × 增强倍数；有效等效量 = 基数 × [1 + (倍数 − 1) × 多样性系数]':
        'Theoretical expansion = base × augmentation factor; effective equivalent = base × [1 + (factor − 1) × diversity coefficient]',
    '数据增强的收益取决于"新增样本带来多少新信息"：若变换高度相似（旋转 1°），多样性系数趋近 0，扩得再多也只是重复；系数接近 1 才算真正等效的新数据。有效量超过数千后边际收益迅速下降。':
        'The benefit of data augmentation depends on "how much new information the added samples bring": if the transforms are highly similar (rotate 1 degree), the diversity coefficient approaches 0 and more augmentation is just repetition; only a coefficient near 1 counts as truly equivalent new data. Beyond several thousand effective samples the marginal gain drops quickly.',
    '每种样本增强次数': 'Augmentations per sample',
    '增强多样性系数 0-1': 'Augmentation diversity coefficient 0-1',
    '有效量 ≈ 原始样本 × [1 + (aug − 1) × 多样性系数]':
        'Effective ≈ original samples × [1 + (aug − 1) × diversity coefficient]',
    '过度增强可能引入噪声。': 'Excessive augmentation may introduce noise.',
    '📚 深度解析：数据增强有效量': '📚 Deep Dive: Effective Augmentation',
    '等效': 'Equivalent',
    '≈原始样本×增强变换': '≈ original samples × augmentation transforms',
    '组合数': 'Combination count',
    '×重复系数，但重复变换会带来相关性。': ' × repetition coefficient, but repeated transforms bring correlation.',
    '增强主要缓解': 'Augmentation mainly relieves',
    '过拟合': 'overfitting',
    '而非凭空创造独立信息，组合越多样增益越实在。':
        'rather than creating independent information out of thin air; the more diverse the combinations, the more real the gain.',
    '小数据集应优先几何/颜色增强与混合策略(Mixup/CutMix)提升多样性。':
        'Small datasets should prioritize geometric/color augmentation and mixing strategies (Mixup/CutMix) to boost diversity.',
    '增强组合估算': 'Augmentation combination estimate',
    'Original 1000 张，施加翻转/旋转/色彩 3 类各 2 档共 8 种组合 → 等效≈1000×8=8000 张。若同一变换重复 3 次，有效增益远低于 3 倍，因样本高度相关。':
        'Original 1000 images, applying flip/rotate/color across 3 types x 2 levels = 8 combinations → equivalent ≈ 1000x8 = 8000 images. If the same transform repeats 3 times, the effective gain is far below 3x because samples are highly correlated.',
    '原始 1000 张，施加翻转/旋转/色彩 3 类各 2 档共 8 种组合 → 等效≈1000×8=8000 张。若同一变换重复 3 次，有效增益远低于 3 倍，因样本高度相关。':
        'Original 1000 images, applying flip/rotate/color across 3 types x 2 levels = 8 combinations → equivalent ≈ 1000x8 = 8000 images. If the same transform repeats 3 times, the effective gain is far below 3x because samples are highly correlated.',
    '增强越多越好吗？': 'Is more augmentation always better?',
    '否。过度或不当增强(如旋转破坏方向语义)会引入噪声甚至错误标签，反而损害训练。应以验证集表现而非数量为准。':
        'No. Excessive or improper augmentation (e.g. rotation that destroys directional semantics) introduces noise or even wrong labels, harming training. Judge by validation performance, not quantity.',
    '增强样本算独立样本吗？': 'Do augmented samples count as independent samples?',
    '不算。它们与原始高度相关，对泛化的贡献低于等量真实标注数据；扩增主要起正则化作用。':
        'No. They are highly correlated with the originals and contribute less to generalization than an equal amount of real labeled data; augmentation mainly acts as regularization.',
}, ind=IND)

# ---------------- ai-13 早停耐心估算 ----------------
apply_tool('ai-13', '早停耐心估算', 'Early Stopping Patience', {
    '📖 查看「早停耐心估算使用指南」': '📖 View "Early Stopping Patience User Guide"',
    '早停等待时间(分钟) = 耐心轮数 × 单轮时长 / 60；最大建议轮数 = 最小轮数 + 耐心 × 3':
        'Early-stop wait time (minutes) = patience epochs × epoch duration / 60; max suggested epochs = min epochs + patience × 3',
    '早停用"连续多少轮验证指标未改善就停止"防止无效训练与过拟合。耐心值太小会在平台期提前终止（验证损失常先震荡后下降），太大则浪费算力；一般给 5–20 轮，并按单轮时长折算可接受的等待成本。':
        'Early stopping uses "stop after N consecutive epochs without validation improvement" to prevent useless training and overfitting. Too small a patience ends early during plateaus (validation loss often oscillates before dropping), too large wastes compute; usually 5-20 epochs, converted to acceptable wait cost by epoch duration.',
    '每 epoch 秒': 'Seconds per epoch',
    '耐心 epoch 数': 'Patience epochs',
    '最小 epoch': 'Minimum epochs',
    'patience 决定模型在验证指标不改善时继续等待的 epoch 数':
        'Patience decides how many more epochs the model waits when validation does not improve',
    'patience 过大浪费算力，过小可能早停。': 'Too large a patience wastes compute; too small may stop early.',
    '📚 深度解析：早停耐心估算': '📚 Deep Dive: Early Stopping Patience',
    'patience 表示验证指标连续多少轮未改善即停止，用于防止':
        'Patience means stopping after the validation metric fails to improve for consecutive epochs, used to prevent',
    '过拟合': 'overfitting',
    '预计总时长≈(当前轮次+剩余耐心轮次)×单轮耗时，辅助算力排期。':
        'Estimated total time ≈ (current epoch + remaining patience epochs) × epoch cost, aiding compute scheduling.',
    'patience 过小易早停漏掉后期收敛，过大则浪费算力，常用 5~20。':
        'Too small a patience stops early and misses later convergence; too large wastes compute; commonly 5-20.',
    '耐心与训练时长': 'Patience and training time',
    '已训练 30 轮、单轮 4 分钟、patience=10。若验证已 10 轮未改善则立即停止；最坏还需 10×4=40 分钟。据此可提前规划 GPU 释放。':
        'Trained 30 epochs, 4 minutes each, patience=10. If validation has not improved for 10 epochs, stop immediately; worst case needs another 10x4=40 minutes. This lets you plan GPU release ahead of time.',
    'patience 设多大合适？': 'How large should patience be?',
    '取决于训练曲线波动。噪声大(如小 batch)需更大 patience 避免误停；平滑训练可设小些。常取总轮次的 10%~20%。':
        'It depends on training-curve noise. Noisy curves (e.g. small batch) need larger patience to avoid false stops; smooth training can use smaller. Commonly 10%-20% of total epochs.',
    '早停后要不要回退到最优轮？': 'After early stopping, should you revert to the best epoch?',
    '要。监控最佳验证权重并单独保存(model checkpoint)，停止后加载该 checkpoint 而非最后一轮，否则可能用的是已过拟合的权重。':
        'Yes. Monitor and save the best validation weights separately (model checkpoint), then load that checkpoint rather than the last epoch after stopping, otherwise you may be using already-overfit weights.',
}, ind=IND)

# ---------------- ai-14 词嵌入余弦检索 ----------------
apply_tool('ai-14', '词嵌入余弦检索', 'Embedding Cosine Search', {
    '📖 查看「词嵌入余弦检索使用指南」': '📖 View "Embedding Cosine Search User Guide"',
    'cos(q, d) = (q·d)/(‖q‖·‖d‖)，检索取 top-k 最大者':
        'cos(q, d) = (q·d)/(‖q‖·‖d‖), retrieval takes the top-k largest',
    '稠密检索的标准打分：查询向量与文档向量做点积后各自归一化，等价于夹角余弦。实际系统常用内积近似加 ANN 索引（HNSW/IVF）加速，此时必须保证向量已归一化，否则内积会被模长带偏。':
        'The standard scoring for dense retrieval: dot-product the query and document vectors then normalize each, equivalent to the angle cosine. Real systems often approximate with inner product plus an ANN index (HNSW/IVF) for speed; then vectors must be normalized, otherwise the inner product is biased by magnitude.',
    '查询 q1': 'Query q1',
    '查询 q2': 'Query q2',
    '文档 d1': 'Document d1',
    '文档 d2': 'Document d2',
    'RAG 检索中常用余弦相似度。': 'Cosine similarity is commonly used in RAG retrieval.',
    '📚 深度解析：词嵌入余弦检索': '📚 Deep Dive: Embedding Cosine Search',
    '将查询与文档编码为向量，按': 'Encode the query and documents as vectors, then rank by ',
    '排序返回最相近项，是语义检索的核心。': 'similarity and return the closest items, the core of semantic retrieval.',
    'RAG 中先用向量库召回 top-k，再送大模型生成，召回质量直接决定答案上限。':
        'In RAG, first recall top-k from a vector store, then feed the LLM to generate; recall quality directly caps the answer ceiling.',
    '余弦对': 'Cosine is insensitive to ',
    '不敏感，适合比较语义方向；短文本需配合归一化与去停用词。':
        'magnitude, suited to comparing semantic direction; short texts need normalization and stop-word removal.',
    '查询召回排序': 'Query recall ranking',
    "查询'苹果公司股价'，文档向量('苹果,财报')cos=0.82、('水果,营养')cos=0.31、('iPhone,发布会')cos=0.76 → 召回排序为财报>iPhone>水果，正确命中企业语义。":
        "Query 'Apple stock price', document vectors ('Apple, earnings') cos=0.82, ('fruit, nutrition') cos=0.31, ('iPhone, launch') cos=0.76 -> recall ranking earnings > iPhone > fruit, correctly hitting the corporate semantics.",
    '余弦和欧氏在检索里差别大吗？': 'Is the difference between cosine and Euclidean large in retrieval?',
    '归一化后二者单调相关，但余弦更关注方向、对模长不敏感，适合文本嵌入；未归一化时欧氏会被向量长度主导，检索效果通常更差。':
        'After normalization they are monotonically related, but cosine focuses on direction and is insensitive to magnitude, suiting text embeddings; unnormalized Euclidean is dominated by vector length and usually retrieves worse.',
    '召回不准怎么排查？': 'How to troubleshoot inaccurate recall?',
    '先看向量模型是否适配领域(通用模型对专业词弱)，再查切分粒度与停用词；也可换混合检索(向量+关键词)补召回。':
        'First check whether the vector model fits the domain (general models are weak on specialized terms), then inspect chunk granularity and stop words; you can also switch to hybrid retrieval (vector + keyword) to supplement recall.',
}, ind=IND)

# ---------------- ai-15 贝叶斯后验概率 ----------------
apply_tool('ai-15', '贝叶斯后验概率', 'Bayesian Posterior', {
    '📖 查看「贝叶斯后验概率使用指南」': '📖 View "Bayesian Posterior User Guide"',
    'P(B) = 先验 × 敏感度 + (1 − 先验) × (1 − 特异度)；后验 P(A|B) = 先验 × 敏感度 / P(B)；NPV = (1 − 先验) × 特异度 / [(1 − 先验) × 特异度 + 先验 × (1 − 敏感度)]':
        'P(B) = prior × sensitivity + (1 − prior) × (1 − specificity); posterior P(A|B) = prior × sensitivity / P(B); NPV = (1 − prior) × specificity / [(1 − prior) × specificity + prior × (1 − sensitivity)]',
    '贝叶斯定理在检测场景的直接应用：即便试剂敏感度、特异度都很高，若疾病先验极低，阳性预测值仍可能很小（假阳性占多数）——这是"筛查阳性≠患病"的数学根据，也是高危人群筛查才有意义的理由。':
        "A direct application of Bayes' theorem to testing: even with very high sensitivity and specificity, if the disease prior is extremely low the positive predictive value can still be small (false positives dominate) - this is the mathematical basis for \"a positive screen != diseased\", and why screening only makes sense for high-risk groups.",
    '先验 P(A)': 'Prior P(A)',
    '似然 P(B|A)': 'Likelihood P(B|A)',
    '特异度 P(¬B|¬A)': 'Specificity P(¬B|¬A)',
    '即使灵敏度和特异度都很高，低先验也会使后验较低。':
        'Even with high sensitivity and specificity, a low prior keeps the posterior low.',
    '📚 深度解析：贝叶斯后验概率': '📚 Deep Dive: Bayesian Posterior',
    '贝叶斯公式 P(A|B)=P(B|A)P(A)/P(B)，由先验 P(A) 与似然 P(B|A) 更新为后验。':
        "Bayes' formula P(A|B)=P(B|A)P(A)/P(B) updates the prior P(A) and likelihood P(B|A) into the posterior.",
    '医学筛查中 A=患病、B=阳性，后验=P(患病|阳性) 即阳性预测值。':
        'In medical screening A=diseased, B=positive, and posterior = P(diseased|positive), i.e. the positive predictive value.',
    '先验很弱时单次证据即可大幅修正信念；证据越多后验越稳。':
        'When the prior is weak a single piece of evidence can greatly shift belief; more evidence makes the posterior steadier.',
    '疾病筛查阳性解读': 'Disease screening positive interpretation',
    '患病率 P(D)=1%，灵敏度 P(+|D)=90%，': 'Prevalence P(D)=1%, sensitivity P(+|D)=90%, ',
    '特异度': 'specificity',
    'P(−|¬D)=95%。P(+)=0.9×0.01+0.05×0.99=0.0585，后验 P(D|+)=0.009/0.0585≈15.4%。即阳性者真正患病概率仅约 15%。':
        'P(−|¬D)=95%. P(+)=0.9×0.01+0.05×0.99=0.0585, posterior P(D|+)=0.009/0.0585≈15.4%. That is, only about 15% of those who test positive actually have the disease.',
    '为什么阳性了患病概率还这么低？': 'Why is the disease probability still so low despite a positive test?',
    '因为基础患病率极低(1%)，大量健康人被检出的假阳性(5%)远多于真病人。贝叶斯提醒：稀有事件阳性预测值天然偏低，需结合复检。':
        'Because the base prevalence is extremely low (1%), the false positives (5%) among many healthy people far outnumber the true patients. Bayes warns: for rare events the positive predictive value is naturally low and retesting is needed.',
    '先验怎么取？': 'How to choose the prior?',
    '可用人群发病率、历史数据或领域经验；证据充分时后验对先验不敏感，先验主要用于证据不足时的正则化。':
        'Use population incidence, historical data, or domain experience; when evidence is sufficient the posterior is insensitive to the prior, which mainly regularizes when evidence is scarce.',
}, ind=IND)

# ---------------- ai-16 模型融合加权投票 ----------------
apply_tool('ai-16', '模型融合加权投票', 'Weighted Ensemble Voting', {
    '📖 查看「模型融合加权投票使用指南」': '📖 View "Weighted Ensemble Voting User Guide"',
    '加权平均概率 = Σpᵢwᵢ / Σwᵢ；硬投票 = Σ[pᵢ ≥ 0.5] ≥ 2 判正类；集成置信度 = |加权概率 − 0.5| × 2':
        'Weighted average probability = Σpᵢwᵢ / Σwᵢ; hard voting = Σ[pᵢ ≥ 0.5] ≥ 2 predicts positive; ensemble confidence = |weighted probability − 0.5| × 2',
    '软投票用权重平均概率，能利用模型输出的置信度信息，通常优于硬投票的多数决。权重可按各模型验证集表现分配；若子模型同质性太强（同一架构不同种子），集成增益会非常有限。':
        "Soft voting averages probabilities by weight, exploiting the confidence information in model outputs, and usually beats hard voting's majority rule. Weights can be assigned by each model's validation performance; if the sub-models are too homogeneous (same architecture, different seeds) the ensemble gain is very limited.",
    '模型1概率': 'Model 1 probability',
    '模型1权重': 'Model 1 weight',
    '模型2概率': 'Model 2 probability',
    '模型2权重': 'Model 2 weight',
    '模型3概率': 'Model 3 probability',
    '模型3权重': 'Model 3 weight',
    '权重可基于模型验证性能分配。': 'Weights can be assigned based on model validation performance.',
    '📚 深度解析：模型融合加权投票': '📚 Deep Dive: Weighted Ensemble Voting',
    '加权投票：对各类别累加各模型输出概率×权重，取最大者为预测。':
        "Weighted voting: for each class accumulate each model's output probability × weight, and take the largest as the prediction.",
    '加权平均直接对各模型输出概率做加权和，权重常按单模型验证准确率设定。':
        'Weighted averaging directly takes the weighted sum of each model’s output probabilities; weights are usually set by single-model validation accuracy.',
    '融合能降低方差、提升稳健性，前提是基模型具备多样性(误差不相关)。':
        'Ensembling reduces variance and improves robustness, provided the base models are diverse (errors uncorrelated).',
    '两模型加权融合': 'Two-model weighted fusion',
    '模型A对类别1概率0.7(权重0.6)，模型B 0.4(权重0.4) → 融合=0.7×0.6+0.4×0.4=0.58，仍判为类别1。若B权重更高(0.7)则=0.7×0.3+0.4×0.7=0.49 翻转为类别0。':
        'Model A class-1 probability 0.7 (weight 0.6), Model B 0.4 (weight 0.4) -> fusion = 0.7×0.6+0.4×0.4 = 0.58, still class 1. If B’s weight is higher (0.7) then = 0.7×0.3+0.4×0.7 = 0.49, flipping to class 0.',
    '融合一定比单模型好吗？': 'Is ensembling always better than a single model?',
    '不一定。若基模型高度相关(同源训练)，融合增益很小甚至':
        'Not necessarily. If the base models are highly correlated (trained from the same source), the ensemble gain is tiny or even ',
    '过拟合': 'overfitting',
    '；只有误差多样、互补的模型融合才稳定提升。': '; only models with diverse, complementary errors improve stably.',
    '权重怎么定？': 'How to set the weights?',
    '常用各模型在验证集的准确率或 AUC 作权重，也可用网格搜索/线性规划优化组合系数，避免随意设定。':
        'Commonly use each model’s validation accuracy or AUC as weights, or optimize the combination coefficients via grid search / linear programming instead of setting them arbitrarily.',
}, ind=IND)

# ---------------- ai-17 提示词上下文窗口 ----------------
apply_tool('ai-17', '提示词上下文窗口', 'Prompt Context Window', {
    '📖 查看「提示词上下文窗口使用指南」': '📖 View "Prompt Context Window User Guide"',
    '已用 tokens = 系统提示 + 历史 + 当前输入；剩余 = 上下文窗口 − 已用；占用率 = 已用 / 窗口 × 100%':
        'Used tokens = system prompt + history + current input; remaining = context window − used; occupancy = used / window × 100%',
    '上下文窗口是硬性上限，输入加输出总和超限会被截断或报错。占用超过 90% 时应压缩历史、摘要旧对话或改用更长上下文模型；注意输出也要预留额度，不能把窗口填满。':
        'The context window is a hard cap; if input plus output exceeds it the content is truncated or errors out. Above 90% occupancy you should compress history, summarize old turns, or switch to a longer-context model; also reserve budget for output and never fill the window completely.',
    '系统提示 token': 'System prompt tokens',
    '历史消息 token': 'History message tokens',
    '当前输入 token': 'Current input tokens',
    '模型上下文窗口': 'Model context window',
    '上下文占用 = 系统 + 历史 + 当前输入': 'Context occupancy = system + history + current input',
    '接近上限时需截断或总结历史。': 'Near the limit you must truncate or summarize history.',
    '📚 深度解析：提示词上下文窗口': '📚 Deep Dive: Prompt Context Window',
    '上下文占用=累计 token 数 / 模型上下文窗口长度(如 8k/32k/128k)。':
        'Context occupancy = cumulative token count / model context window length (e.g. 8k/32k/128k).',
    '多轮对话需扣除历史 token，超出窗口须裁剪或摘要压缩，否则被截断。':
        'Multi-turn dialogue must deduct history tokens; beyond the window it must be trimmed or summarized, otherwise it is truncated.',
    '占用比越高越易触发截断与成本上升，长对话应定期清理低价值历史。':
        'Higher occupancy more easily triggers truncation and cost rise; long dialogues should periodically clear low-value history.',
    '长对话溢出预警': 'Long-dialogue overflow warning',
    '窗口 32k，当前累计 28k token → 占用 87.5%，剩余 4k 仅够约一句长回复。若再追加 5k 历史将溢出，应裁剪最早 6k 或用摘要替代原文。':
        'Window 32k, currently 28k tokens -> 87.5% occupancy, remaining 4k only enough for about one long reply. Adding another 5k history would overflow; trim the earliest 6k or replace the original with a summary.',
    '为什么超出窗口会被截断？': 'Why does exceeding the window get truncated?',
    '模型注意力只能覆盖固定长度上下文，超出的前缀会被丢弃(或报错)。裁剪应保留最近对话与关键事实，避免丢失约束指令。':
        'A model’s attention can only cover a fixed-length context; the overflowing prefix is discarded (or errors). Trimming should keep recent dialogue and key facts to avoid losing constraint instructions.',
    '压缩历史会丢信息吗？': 'Does compressing history lose information?',
    '会。摘要压缩以语义概括替代原文，可能损失细节；权衡做法是保留最近 N 轮原文、更早的做摘要，关键参数始终置顶。':
        'Yes. Summarization replaces the original with a semantic overview and may lose details; a good trade-off keeps the latest N turns verbatim and summarizes earlier ones, with key parameters always on top.',
}, ind=IND)

print('gen_ai_b1 done: 14 tools written')
