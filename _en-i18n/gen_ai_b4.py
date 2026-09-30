# -*- coding: utf-8 -*-
"""ai 行业正文英文化 batch4（剩余工具第 2 批 11 个）。逐条语义化翻译；值纯英文避开 CJK/中文标点。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool

IND = 'ai'

# ---------------- image-classification 图像分类识别 ----------------
apply_tool('image-classification', '图像分类识别', 'Image Classification', {
    '🖼️ 图像分类识别': '🖼️ Image Classification',
    '基于 Transformers.js 在浏览器本地运行 ViT 模型，识别图像中的物体 / 场景，数据不上传。': 'Runs a ViT model locally in the browser via Transformers.js to recognize objects / scenes in images, with no data upload.',
    '📖 查看「图像分类识别使用指南」': '📖 View "Image Classification User Guide"',
    '本工具在浏览器本地加载图像分类模型，对上传图片推理并返回置信度最高的前 5 个类别，全程不上传。': 'This tool loads an image-classification model locally in the browser, runs inference on the uploaded image and returns the top 5 classes by confidence, all without upload.',
    '📚 深度解析：图像分类识别': '📚 Deep Dive: Image Classification',
    '在浏览器本地用预训练模型(如 MobileNet)对上传图片推理，输出 Top5 类别与概率。': 'Run a pretrained model (e.g. MobileNet) locally in the browser on the uploaded image and output the Top-5 classes with probabilities.',
    '纯前端运行，图片不上传，保护隐私且离线可用，适合轻量识别与演示。': 'Runs fully client-side with no upload, protecting privacy and working offline, suited to lightweight recognition and demos.',
    '模型精度有限且对对抗样本敏感，结果仅供辅助，关键场景需人工确认。': 'Model accuracy is limited and sensitive to adversarial examples; results are for assistance only, and critical cases need human confirmation.',
    '本地识别': 'Local recognition',
    "上传一张猫的照片，模型返回 Top5：['Egyptian cat' 0.82,'tabby' 0.10,...]。概率高但非绝对，混淆类别(如不同猫种)需结合上下文判断。":
        "Upload a photo of a cat; the model returns Top-5: ['Egyptian cat' 0.82,'tabby' 0.10,...]. High probability is not absolute; confusable classes (e.g. cat breeds) need contextual judgment.",
    '为什么有时认错？': 'Why does it sometimes misclassify?',
    '预训练模型覆盖有限、对角度/光照/背景敏感，且可能受对抗扰动影响；纯前端轻量模型精度低于云端大模型，重要判断需复核。': 'Pretrained models have limited coverage and are sensitive to angle/lighting/background, and may be affected by adversarial perturbations; lightweight client-side models are less accurate than cloud LLMs, so important judgments need review.',
    '上传的图片会泄露吗？': 'Will the uploaded image leak?',
    '不会。本工具在浏览器内完成推理，图片不离开设备；但仅本地也意味着无法调用更强的云端模型。': 'No. Inference runs entirely inside the browser and the image never leaves the device; but being local-only also means no stronger cloud model can be used.',
}, ind=IND)

# ---------------- inference-throughput 推理吞吐估算 ----------------
apply_tool('inference-throughput', '推理吞吐估算', 'Inference Throughput Estimator', {
    '🔮 推理吞吐估算': '🔮 Inference Throughput Estimator',
    '由生成 token 与时延估算推理吞吐。': 'Estimate inference throughput from generated tokens and latency.',
    '📖 查看「推理吞吐估算使用指南」': '📖 View "Inference Throughput Estimator User Guide"',
    '吞吐 = tokens / 秒；单请求吞吐 = tokens / (秒 × 并发批量)': 'Throughput = tokens / sec; per-request throughput = tokens / (sec x concurrency batch)',
    '推理服务的核心指标：总吞吐衡量集群利用率，单请求吞吐才是用户感知的快慢。batching 能显著提升总吞吐但会拉长单请求延迟，在线服务通常需要在两者间按 SLO 折中。':
        'A core metric for inference serving: total throughput measures cluster utilization, while per-request throughput is what users feel as speed. Batching greatly raises total throughput but lengthens per-request latency, so online services usually trade off between them by SLO.',
    '生成 tokens': 'Generated tokens',
    '耗时 秒': 'Elapsed seconds',
    '并发数': 'Concurrency',
    '吞吐 = tokens / 耗时；人均 = 吞吐 / 并发': 'Throughput = tokens / elapsed; per-request = throughput / concurrency',
    '实际受批大小与排队影响。': 'Affected in practice by batch size and queuing.',
    '📚 深度解析：推理吞吐估算': '📚 Deep Dive: Inference Throughput Estimator',
    '吞吐≈生成 token 数 / 端到端时延(tokens/s)，衡量服务处理速度。': 'Throughput ~ generated tokens / end-to-end latency (tokens/s), measuring serving speed.',
    '受模型大小、批大小、KV 缓存与硬件带宽共同影响，非仅由 FLOPs 决定。': 'Driven jointly by model size, batch size, KV cache and hardware bandwidth, not solely by FLOPs.',
    '容量规划用 吞吐×并发上限 估算峰值 QPS，需预留余量防雪崩。': 'For capacity planning, peak QPS ~ throughput x max concurrency, with headroom reserved against overload.',
    '单请求吞吐': 'Per-request throughput',
    '生成 200 token 耗时 4s → 吞吐=50 tokens/s。若单卡支持 4 并发且各 50 tok/s，总吞吐≈200 tok/s；但实际共享 KV 缓存与带宽，并发增益低于线性。':
        'Generating 200 tokens in 4s -> throughput = 50 tokens/s. If one card supports 4-way concurrency at 50 tok/s each, total ~ 200 tok/s; but with shared KV cache and bandwidth, the concurrency gain is below linear.',
    '为什么吞吐不随并发线性增长？': 'Why does throughput not grow linearly with concurrency?',
    '显存带宽与算力是共享瓶颈，多请求竞争 KV 缓存与计算单元，边际吞吐递减；需实测找到拐点再定并发上限。': 'Memory bandwidth and compute are shared bottlenecks; many requests compete for KV cache and units, so marginal throughput declines. Measure to find the knee before setting the concurrency cap.',
    '首 token 延迟和吞吐冲突吗？': 'Do first-token latency and throughput conflict?',
    '常冲突。大模型首 token 受预填充耗时影响，吞吐受解码并行影响；优化方向相反时按业务(对话要低延迟、批处理要高吞吐)取舍。': 'Often yes. First-token latency is driven by prefill cost, while throughput is driven by decode parallelism; when the optimization directions oppose, choose by business (low latency for chat, high throughput for batch).',
}, ind=IND)

# ---------------- k-means 聚类 K-Means 代价 ----------------
apply_tool('k-means', '聚类 K-Means 代价', 'K-Means Cost', {
    '📊 聚类 K-Means 代价': '📊 K-Means Cost',
    '估算 K-Means 聚类的惯性 inertia。': 'Estimate the K-Means clustering inertia.',
    '📖 查看「聚类 K-Means 代价使用指南」': '📖 View "K-Means Cost User Guide"',
    'Inertia 估算 ≈ n·dim·spread²/k；每簇样本 ≈ ⌈n/k⌉': 'Inertia estimate ~ n·dim·spread²/k; samples per cluster ~ ceil(n/k)',
    '在样本近似均匀分布的假设下，簇内平方和随 K 增大按 1/k 衰减，可用于快速预判需要多少簇。实际数据有簇密度差异时，应结合业务含义定 K，而不是只看指标拐点。':
        'Assuming roughly uniform samples, the within-cluster sum of squares decays with K by 1/k, useful for a quick guess of how many clusters are needed. With real clusters of varying density, set K by business meaning rather than only the metric knee.',
    '聚类数': 'Cluster count',
    '簇内散布': 'Intra-cluster spread',
    'Inertia 越小簇内越紧密。': 'Smaller inertia means tighter clusters.',
    '📚 深度解析：K-Means 代价': '📚 Deep Dive: K-Means Cost',
    '惯性 inertia=Σ‖x−μ_k‖²(簇内平方和 WCSS)，越小聚类越紧致。': 'Inertia = Σ‖x-μ_k‖² (within-cluster sum of squares WCSS); smaller means more compact clusters.',
    'inertia 随 k 增大单调下降，需用拐点(手肘)或轮廓系数选 k。': 'Inertia drops monotonically with k; choose k by the elbow knee or silhouette score.',
    'K-Means 对初始中心与异常值敏感，常多次初始化取最优。': 'K-Means is sensitive to initial centers and outliers, so it is often run with multiple initializations and the best retained.',
    '代价比较': 'Cost comparison',
    'k=2 时 inertia=500, k=3 时=300, k=4 时=220。inertia 持续下降，k=3→4 降幅(80)明显小于 2→3(200)，结合业务选 k=3 或 4。':
        'k=2 inertia=500, k=3=300, k=4=220. Inertia keeps falling; the k=3->4 drop (80) is much smaller than 2->3 (200), so pick k=3 or 4 by business.',
    'inertia 越小越好吗？': 'Is smaller inertia always better?',
    '不是。k 越大 inertia 越小，k=样本数时为 0 但失去聚类意义；应兼顾紧致性与簇数简洁，用手肘/轮廓系数平衡。': 'No. Larger k gives smaller inertia; at k=sample count it is 0 but clustering loses meaning. Balance compactness and cluster simplicity via elbow/silhouette.',
    '异常值怎么处理？': 'How to handle outliers?',
    '异常值会大幅拉高 inertia 并偏移质心，可先做离群检测或用 K-Medoids(基于距离': 'Outliers greatly inflate inertia and shift the centroid; first do outlier detection or use K-Medoids (distance-based',
    ')更稳健。': ') which is more robust.',
}, ind=IND)

# ---------------- l1-l2 L1 L2 正则化惩罚 ----------------
apply_tool('l1-l2', 'L1 L2 正则化惩罚', 'L1 L2 Regularization Penalty', {
    '🔍 L1 L2 正则化惩罚': '🔍 L1 L2 Regularization Penalty',
    '计算 L1 和 L2 正则化对损失的惩罚项。': 'Compute the L1 and L2 regularization penalties on the loss.',
    '📖 查看「L1 L2 正则化惩罚使用指南」': '📖 View "L1 L2 Regularization Penalty User Guide"',
    'L1 = λ₁·Σ|wᵢ|；L2 = λ₂·Σwᵢ²；总惩罚 = L1 + L2': 'L1 = λ₁·Σ|wᵢ|; L2 = λ₂·Σwᵢ²; total penalty = L1 + L2',
    'L1 在 0 处不可导且梯度恒为 ±λ，会把不重要权重精确压到 0，产生稀疏解可用于特征选择；L2 惩罚与权重成正比，越接近 0 推力越弱，只做均匀收缩、保留小权重，泛化通常更稳。二者混用即 Elastic Net。':
        'L1 is non-differentiable at 0 with gradient ±λ, pushing unimportant weights exactly to 0 and producing a sparse solution useful for feature selection; L2 penalizes in proportion to weight, weakening near 0, only shrinking uniformly and keeping small weights, usually more stable for generalization. Mixing both is Elastic Net.',
    'L1 系数': 'L1 coefficient',
    'L2 系数': 'L2 coefficient',
    'L1 产生稀疏权重，L2 使权重平滑。': 'L1 yields sparse weights, L2 smooths weights.',
    '📚 深度解析：L1 L2 正则化惩罚': '📚 Deep Dive: L1 L2 Regularization Penalty',
    '惩罚项加入损失：L_total=Loss+λ₁‖w‖₁+λ₂‖w‖₂²，统称弹性网络(Elastic Net)。': 'Add the penalty to the loss: L_total = Loss + λ₁‖w‖₁ + λ₂‖w‖₂², collectively Elastic Net.',
    'L1 促稀疏(特征选择)，L2 促平滑(权重衰减)，二者互补。': 'L1 promotes sparsity (feature selection), L2 promotes smoothness (weight decay); they complement each other.',
    '权重衰减(weight decay)本质是 L2，深度学习常用之稳定训练。': 'Weight decay is essentially L2, commonly used in deep learning to stabilize training.',
    '组合惩罚': 'Combined penalty',
    'Loss=0.2, w=[3,−4], λ₁=0.01, λ₂=0.01：L1 惩罚=0.01×7=0.07，L2 惩罚=0.01×25=0.25，总损失=0.2+0.07+0.25=0.52。':
        'Loss=0.2, w=[3,-4], λ₁=0.01, λ₂=0.01: L1 penalty=0.01x7=0.07, L2 penalty=0.01x25=0.25, total loss=0.2+0.07+0.25=0.52.',
    'Elastic Net 比单独 L1/L2 好在哪？': 'Where does Elastic Net beat L1 or L2 alone?',
    '同时获得稀疏性与分组稳定性，尤其特征高度相关时比纯 L1 更稳健；代价是多一个超参，需用交叉验证调。': 'It gains both sparsity and group stability, especially more robust than pure L1 when features are highly correlated; the cost is one more hyperparameter tuned by cross-validation.',
    '权重衰减和 L2 完全等价吗？': 'Is weight decay exactly equivalent to L2?',
    '在标准 SGD 下等价；但用 AdamW 时权重衰减与梯度解耦，实现不同、效果更优，不能简单当作 L2 代入。': 'Equivalent under standard SGD; but with AdamW weight decay is decoupled from the gradient, implemented differently and working better, so it cannot be simply substituted as L2.',
}, ind=IND)

# ---------------- l1-l2-regularization L1/L2 正则项 ----------------
apply_tool('l1-l2-regularization', 'L1/L2 正则项', 'L1/L2 Norm', {
    '🔍 L1/L2 正则项': '🔍 L1/L2 Norm',
    '计算权重向量的 L1 与 L2 范数。': 'Compute the L1 and L2 norms of a weight vector.',
    '📖 查看「L1/L2 正则项使用指南」': '📖 View "L1/L2 Norm User Guide"',
    'L1 范数 = Σ|wᵢ|；L2 范数 = √(Σwᵢ²)': 'L1 norm = Σ|wᵢ|; L2 norm = √(Σwᵢ²)',
    '两个范数量化权重矩阵的整体规模：L1 反映绝对值总量，对少量大权重敏感；L2（Frobenius 范数）反映能量，常被直接写进损失作为惩罚项。监控范数随训练的变化能快速判断是否出现权重爆炸。':
        'The two norms quantify the overall scale of the weight matrix: L1 reflects total absolute value, sensitive to a few large weights; L2 (Frobenius norm) reflects energy and is often written directly into the loss as a penalty. Monitoring the norm over training quickly reveals weight explosion.',
    '权重4': 'Weight 4',
    'L1 倾向稀疏，L2 倾向小权重。': 'L1 tends to sparsity, L2 tends to small weights.',
    '📚 深度解析：L1/L2 正则项': '📚 Deep Dive: L1/L2 Norm',
    'L1 范数 ‖w‖₁=Σ|wᵢ|，L2 范数 ‖w‖₂=√(Σwᵢ²)，分别衡量权重大小。': 'L1 norm ‖w‖₁ = Σ|wᵢ|, L2 norm ‖w‖₂ = √(Σwᵢ²), each measuring weight magnitude.',
    '对应惩罚项 λ‖w‖₁(Lasso,促稀疏)与 (λ/2)‖w‖₂²(Ridge,促平滑)。': 'The corresponding penalties are λ‖w‖₁ (Lasso, sparse) and (λ/2)‖w‖₂² (Ridge, smooth).',
    '正则项加入损失函数，限制权重幅度以抑制': 'The regularization term is added to the loss to limit weight magnitude and suppress',
    '过拟合': 'overfitting',
    '范数计算': 'Norm computation',
    'w=[3,−4]：‖w‖₁=|3|+|−4|=7；‖w‖₂=√(9+16)=5，L2 惩罚=(λ/2)·25。L1 对大权重同等惩罚，L2 更压大权重。':
        'w=[3,-4]: ‖w‖₁ = |3|+|-4| = 7; ‖w‖₂ = √(9+16) = 5, L2 penalty = (λ/2)·25. L1 penalizes large weights equally, L2 presses large weights harder.',
    'L1 为什么能稀疏？': 'Why can L1 produce sparsity?',
    'L1 在零点不可导、等高线为菱形，最优解易落在坐标轴上使部分权重恰为 0，实现特征选择；L2 只缩小不置零。': 'L1 is non-differentiable at zero with diamond contours, so the optimum tends to land on axes, zeroing some weights and achieving feature selection; L2 only shrinks, never zeroes.',
    '正则系数 λ 怎么选？': 'How to choose the regularization coefficient λ?',
    '用验证集网格/贝叶斯搜索；λ 过小过拟合、过大欠拟合。通常对权重先标准化，再在 10⁻⁴~10 量级扫描。': 'Use grid or Bayesian search on the validation set; too small λ overfits, too large underfits. Usually standardize weights first, then scan λ in the 10⁻⁴ to 10 range.',
}, ind=IND)

# ---------------- lr-decay 学习率衰减 ----------------
apply_tool('lr-decay', '学习率衰减', 'Learning Rate Decay', {
    '📖 学习率衰减': '📖 Learning Rate Decay',
    '按指数衰减计算当前学习率。': 'Compute the current learning rate by exponential decay.',
    '📖 查看「学习率衰减使用指南」': '📖 View "Learning Rate Decay User Guide"',
    'lr(epoch) = lr₀ × γ^epoch（指数衰减，γ<1）': 'lr(epoch) = lr₀ × γ^epoch (exponential decay, γ<1)',
    '指数衰减让学习率随轮数几何级下降，早期大步探索、后期小步精修，有利于跳出尖锐极小值。γ 常取 0.9–0.99 或按验证指标下降时再降（ReduceOnPlateau）；搭配 warmup 可避免训练初期大学习率导致发散。':
        'Exponential decay drops the learning rate geometrically with epochs: large steps early for exploration, small steps late for refinement, helping escape sharp minima. γ is often 0.9-0.99, or reduce on validation plateau (ReduceOnPlateau); paired with warmup it avoids divergence from a large initial rate.',
    '初始 LR': 'Initial LR',
    '衰减率': 'Decay rate',
    '指数衰减常用于后期精调。': 'Exponential decay is often used for late-stage fine-tuning.',
    '📚 深度解析：学习率衰减': '📚 Deep Dive: Learning Rate Decay',
    '指数衰减 lr=lr₀·γ^t；阶梯衰减每 N 步乘一次因子；余弦退火平滑降至近 0。': 'Exponential decay lr=lr₀·γ^t; step decay multiplies by a factor every N steps; cosine annealing smoothly falls near 0.',
    '衰减让训练初期大步探索、后期细调，提升收敛质量与稳定性。': 'Decay lets training explore in big steps early and refine later, improving convergence quality and stability.',
    '衰减策略需与总步数匹配，过早或过猛会陷入局部或过慢。': 'The decay schedule must match the total steps; too early or too aggressive gets stuck locally or too slow.',
    '指数衰减': 'Exponential decay',
    'lr₀=0.1, γ=0.95, 第 20 步 → lr=0.1×0.95²⁰≈0.0359。每步小幅下降，20 步后约为初始的 36%。': 'lr₀=0.1, γ=0.95, step 20 -> lr=0.1×0.95²⁰≈0.0359. Small drops each step; after 20 steps about 36% of the initial.',
    '余弦退火为什么流行？': 'Why is cosine annealing popular?',
    '它在训练中后段平滑降到很低，利于精细收敛且对超参不敏感，常配合预热使用；相比阶梯衰减更平滑、易复现好结果。': 'It smoothly falls very low in the mid-late training, aiding fine convergence and being insensitive to hyperparameters, often with warmup; smoother and more reproducible than step decay.',
    '学习率衰减和预热能同时用吗？': 'Can decay and warmup be used together?',
    '能且常见：先线性预热到峰值再余弦衰减(warmup+cosine)，兼顾初期稳定与后期收敛，是大模型训练标配。': 'Yes and it is common: linear warmup to peak then cosine decay (warmup+cosine) balances early stability and late convergence, a staple of large-model training.',
}, ind=IND)

# ---------------- lr-warmup 学习率预热步数 ----------------
apply_tool('lr-warmup', '学习率预热步数', 'Learning Rate Warmup Steps', {
    '📖 学习率预热步数': '📖 Learning Rate Warmup Steps',
    '根据总步数与比例计算预热步数。': 'Compute warmup steps from total steps and ratio.',
    '📖 查看「学习率预热步数使用指南」': '📖 View "Learning Rate Warmup Steps User Guide"',
    '预热步数 = 总步数 × 比例；预热末 LR = 峰值 LR': 'Warmup steps = total steps x ratio; warmup-end LR = peak LR',
    '训练最初若干步把学习率从 0 线性升到峰值，给 Adam 的二阶动量估计留出稳定时间，避免大 batch 训练初期因梯度方差大而发散。典型配置是总步数的 1%–5%，之后接 cosine 或线性衰减。':
        'For the first steps, linearly raise the learning rate from 0 to the peak, giving Adam\'s second-moment estimate time to stabilize and avoiding divergence from high gradient variance early in large-batch training. A typical setting is 1%-5% of total steps, followed by cosine or linear decay.',
    '总步数': 'Total steps',
    '预热比例': 'Warmup ratio',
    '峰值 LR': 'Peak LR',
    'warmup = 总步数 × 比例': 'warmup = total steps x ratio',
    '预热可稳定训练初期梯度。': 'Warmup stabilizes early-training gradients.',
    '📚 深度解析：学习率预热步数': '📚 Deep Dive: Learning Rate Warmup Steps',
    '预热步数=总步数×预热比例；期间 lr 从 0(或很小)线性升到峰值。': 'Warmup steps = total steps x warmup ratio; during it lr rises linearly from 0 (or very small) to the peak.',
    '避免训练初期大 lr 破坏随机初始化、造成梯度震荡或不稳定。': 'Avoid a large early lr destroying random initialization and causing gradient oscillation or instability.',
    '常用预热比例 0~10%，与余弦衰减衔接形成 warmup+decay 调度。': 'Common warmup ratio 0-10%, chained with cosine decay into a warmup+decay schedule.',
    '预热区间': 'Warmup range',
    '总步数 10000、预热比例 5% → 预热步数=500，前 500 步 lr 从 0 线性增至峰值(如 1e-3)，之后进入衰减。无预热时首步即 1e-3 易震荡。':
        'Total steps 10000, warmup ratio 5% -> warmup steps = 500; the first 500 steps raise lr linearly from 0 to the peak (e.g. 1e-3), then decay begins. Without warmup the first step already at 1e-3 easily oscillates.',
    '预热一定要吗？': 'Is warmup necessary?',
    '大模型/大 batch 通常必要，能稳定初期训练；小模型小学习率可省略。跳过预热常出现首轮 loss 尖峰甚至 NaN。': 'Usually necessary for large models / large batches to stabilize early training; small models with small lr can skip it. Skipping warmup often causes first-epoch loss spikes or even NaN.',
    '预热比例多大合适？': 'What warmup ratio is appropriate?',
    '常见 0~10%，Transformer 训练多用 1%~6%；过大则有效训练步数被浪费，过小保护不足，以验证曲线平滑为准。': 'Common 0-10%, Transformers often use 1%-6%; too large wastes effective training steps, too small under-protects; aim for a smooth validation curve.',
}, ind=IND)

# ---------------- min-max 特征缩放 Min-Max ----------------
apply_tool('min-max', '特征缩放 Min-Max', 'Min-Max Feature Scaling', {
    '🖼️ 特征缩放 Min-Max': '🖼️ Min-Max Feature Scaling',
    '将特征值缩放到 [0,1] 或 [−1,1]。': 'Scale feature values to [0,1] or [-1,1].',
    '📖 查看「特征缩放 Min-Max使用指南」': '📖 View "Min-Max Feature Scaling User Guide"',
    'x′ = (x − min)/(max − min)；[-1,1] 映射 x″ = 2x′ − 1；Z-score 近似 (x − x̄)/((max − min)/2)': "x' = (x - min)/(max - min); [-1,1] map x'' = 2x' - 1; Z-score approx (x - x_bar)/((max - min)/2)",
    'Min-Max 把特征线性压到固定区间，保留原始分布形状但不改变相对关系；缺点是受离群点支配（一个极大值会把其余样本挤到窄区间）。树模型不需要缩放，而梯度下降类与距离类模型通常必须做。':
        'Min-Max linearly compresses features into a fixed range, preserving shape but not relative relations; the downside is domination by outliers (one huge value squeezes the rest into a narrow band). Tree models need no scaling, while gradient-descent and distance-based models usually must do it.',
    '目标范围 1=[0,1] 2=[-1,1]': 'Target range 1=[0,1] 2=[-1,1]',
    '映射到 [−1,1]：2x\' − 1': 'Map to [-1,1]: 2x\' - 1',
    '注意 max 不能等于 min。': 'Note max must not equal min.',
    '📚 深度解析：特征缩放 Min-Max': '📚 Deep Dive: Min-Max Feature Scaling',
    '[0,1] 缩放 x\'=(x−min)/(max−min)；[−1,1] 缩放 x\'=2(x−min)/(max−min)−1。': "[0,1] scale x'=(x-min)/(max-min); [-1,1] scale x'=2(x-min)/(max-min)-1.",
    '要求 max≠min，否则分母为零；异常值会压缩正常样本区间。': 'Requires max!=min, else division by zero; outliers compress the normal-sample range.',
    '缩放到固定区间利于梯度下降与距离类算法(如 KNN、K-Means)收敛。': 'Scaling to a fixed range helps gradient descent and distance-based algorithms (e.g. KNN, K-Means) converge.',
    '归一化计算': 'Normalization computation',
    '特征取值 10~40，x=25 → [0,1]:(25−10)/30=0.5；[−1,1]:2×0.5−1=0.0，恰为区间中点。若含异常值 1000 则正常样本全挤在 0 附近。':
        'Feature range 10-40, x=25 -> [0,1]: (25-10)/30=0.5; [-1,1]: 2x0.5-1=0.0, exactly the midpoint. With an outlier 1000, normal samples all squeeze near 0.',
    'Min-Max 和 StandardScaler 怎么选？': 'How to choose between Min-Max and StandardScaler?',
    'Min-Max 固定边界、对异常值敏感，适合已知范围(如图像 0~255)；StandardScaler(均值0方差1)对异常更稳健，适合多数建模。': 'Min-Max has fixed bounds and is outlier-sensitive, suited to known ranges (e.g. images 0-255); StandardScaler (mean 0, variance 1) is more robust to outliers, suited to most modeling.',
    '测试集怎么缩放？': 'How to scale the test set?',
    '必须用训练集的 min/max 缩放测试集，不能用测试集自身统计量，否则引入数据泄露、夸大泛化效果。': 'Scale the test set with the training set\'s min/max, never the test set\'s own statistics, or you introduce data leakage and overstate generalization.',
}, ind=IND)

# ---------------- model-accuracy 模型准确率 ----------------
apply_tool('model-accuracy', '模型准确率', 'Model Accuracy', {
    '🧮 模型准确率': '🧮 Model Accuracy',
    '根据混淆矩阵计算分类准确率。': 'Compute classification accuracy from the confusion matrix.',
    '📖 查看「模型准确率使用指南」': '📖 View "Model Accuracy User Guide"',
    '准确率 = (TP+TN)/(TP+TN+FP+FN)×100%': 'Accuracy = (TP+TN)/(TP+TN+FP+FN) x 100%',
    '分类模型最直观的整体判对比例。它隐含"各类代价相同"的假设，当负样本占绝大多数时（如 99:1 的欺诈检测），恒判负类即可拿到 99% 准确率却毫无价值，此时必须配合精确率、召回率或 MCC 一起判读。':
        'The most intuitive overall correct-rate of a classifier. It implicitly assumes equal cost per class; when negatives dominate (e.g. 99:1 fraud detection), always predicting negative gives 99% accuracy yet no value, so it must be read together with precision, recall or MCC.',
    '类别不均衡时准确率易误导，应结合其他指标。': 'Accuracy misleads under class imbalance; combine with other metrics.',
    '📚 深度解析：模型准确率': '📚 Deep Dive: Model Accuracy',
    '整体准确率=(正确预测数)/(总样本数)，按混淆矩阵 TP+TN 之和计算。': 'Overall accuracy = (correct predictions)/(total samples), from the sum TP+TN in the confusion matrix.',
    '各类别正确率=该类别预测正确数/该类别样本数，揭示对少数类的表现。': 'Per-class accuracy = correct predictions for that class / samples of that class, revealing performance on minority classes.',
    '类别不平衡时整体准确率易虚高，需结合宏/微平均与混淆矩阵解读。': 'Under class imbalance overall accuracy easily inflates; interpret with macro/micro average and the confusion matrix.',
    '整体与各类别': 'Overall and per-class',
    '三类各 100 样本，A 类对 90、B 类对 80、C 类对 60 → 整体准确率=(90+80+60)/300=76.7%；各类别 90%/80%/60%，可见模型在 C 类最弱。':
        'Three classes of 100 samples each, A correct 90, B 80, C 60 -> overall accuracy = (90+80+60)/300 = 76.7%; per-class 90%/80%/60%, showing the model is weakest on C.',
    '整体准确率高但某类很差是正常的吗？': 'Is high overall accuracy with one weak class normal?',
    '在不平衡或多类场景中常见，说明模型偏向多数/易分样本。应报告各类别准确率与混淆矩阵，而非只看整体数字。': 'Common in imbalanced or multi-class settings, meaning the model favors majority/easy samples. Report per-class accuracy and the confusion matrix, not just the overall number.',
    '准确率和 F1 冲突听谁的？': 'When accuracy and F1 conflict, which wins?',
    '看业务代价。若漏检/误判代价高(医疗、风控)，优先看精确率/召回/F1 与具体类别指标，而非整体准确率。': 'It depends on business cost. If missed/false judgments are costly (medical, risk control), prioritize precision/recall/F1 and per-class metrics over overall accuracy.',
}, ind=IND)

# ---------------- multi-agent-overhead 多智能体通信开销 ----------------
apply_tool('multi-agent-overhead', '多智能体通信开销', 'Multi-Agent Communication Overhead', {
    '🤖 多智能体通信开销': '🤖 Multi-Agent Communication Overhead',
    '估算全连接多智能体的通信开销。': 'Estimate the communication overhead of fully-connected multi-agent systems.',
    '📖 查看「多智能体通信开销使用指南」': '📖 View "Multi-Agent Communication Overhead User Guide"',
    '消息总数 = n(n − 1) × 轮数；总流量 = 消息总数 × 单条大小': 'Total messages = n(n - 1) x rounds; total traffic = total messages x message size',
    '全连接广播模式下每个智能体每轮要向其余 n−1 个发消息，通信量随智能体数量呈平方增长，这是多智能体系统规模化的主要瓶颈。改为分层或共享黑板（blackboard）可把复杂度降到线性。':
        'In full-mesh broadcast each agent sends to the other n-1 agents every round, so traffic grows quadratically with agent count - the main scaling bottleneck of multi-agent systems. Switching to hierarchical or shared blackboard reduces complexity to linear.',
    '智能体数': 'Agent count',
    '通信轮次': 'Communication rounds',
    '单消息 KB': 'KB per message',
    '消息 = n·(n−1)·轮次（全连接）': 'Messages = n·(n-1)·rounds (full mesh)',
    '随智能体数平方增长，需谨慎设计拓扑。': 'Grows with the square of agent count; design the topology carefully.',
    '📚 深度解析：多智能体通信开销': '📚 Deep Dive: Multi-Agent Communication Overhead',
    '全连接拓扑下每轮消息数=C(n,2)=n(n−1)/2，随智能体数平方增长。': 'Under full mesh, messages per round = C(n,2) = n(n-1)/2, growing quadratically with agent count.',
    '开销=消息数×单消息体量(上下文/token)，是通信瓶颈与成本主因。': 'Overhead = message count x message size (context/token), the main cause of communication bottleneck and cost.',
    '可用分层/星型/广播拓扑削减边数，或用摘要压缩降低单消息体量。': 'Use hierarchical/star/broadcast topologies to cut edges, or compress messages with summaries to reduce per-message size.',
    '全连接开销': 'Full-mesh overhead',
    'n=10 个智能体全连接：每轮消息=10×9/2=45 条。若单条含 2k token，每轮通信≈90k token；n=20 时消息=190，开销约 4 倍，增长极快。':
        'n=10 agents full mesh: messages per round = 10x9/2 = 45. With 2k tokens each, ~90k tokens per round; at n=20 messages=190, ~4x overhead, growing extremely fast.',
    '怎么降低多智能体通信成本？': 'How to lower multi-agent communication cost?',
    '改全连接为星型/分层(中心协调)，减少边数；消息用摘要而非全文；并设定通信轮次上限，避免无限对话空转。': 'Change full mesh to star/hierarchical (central coordination) to cut edges; send summaries instead of full text; and cap communication rounds to avoid idle infinite dialog.',
    '全连接有必要吗？': 'Is full mesh necessary?',
    '多数任务不需要。全连接让任意两体直连、信息同步快但成本高；若任务可分解，子团队+汇总更高效，性价比更好。': 'Most tasks do not need it. Full mesh links any pair directly with fast sync but high cost; if the task is decomposable, sub-teams plus aggregation is more efficient and cost-effective.',
}, ind=IND)

# ---------------- ocr OCR 文字识别 ----------------
apply_tool('ocr', 'OCR 文字识别', 'OCR Text Recognition', {
    '🔍 OCR 文字识别': '🔍 OCR Text Recognition',
    '基于 Transformers.js 在浏览器本地运行 TrOCR 模型，从图片中提取印刷体文字，数据不上传。': 'Runs a TrOCR model locally in the browser via Transformers.js to extract printed text from images, with no data upload.',
    '📖 查看「OCR 文字识别使用指南」': '📖 View "OCR Text Recognition User Guide"',
    '本工具在浏览器本地加载 OCR 模型，对上传图片执行文字检测与识别，全程不依赖服务器、图片不上传。': 'This tool loads an OCR model locally in the browser and performs text detection and recognition on the uploaded image, with no server dependency and no upload.',
    '📚 深度解析：OCR 文字识别': '📚 Deep Dive: OCR Text Recognition',
    '在浏览器本地用预训练 OCR 从图片提取文字，支持中英文与多行，结果可复制编辑。': 'Extract text from images locally in the browser with a pretrained OCR, supporting Chinese/English and multi-line, with copyable editable results.',
    '纯前端运行，图片不上传，保护隐私；适合票据、文档、截图快速转文字。': 'Runs fully client-side with no upload, protecting privacy; suited to quickly turning invoices, documents and screenshots into text.',
    '识别质量受清晰度、排版与字体影响，复杂版面需后处理校对。': 'Recognition quality depends on clarity, layout and font; complex layouts need post-processing proofreading.',
    '本地提取': 'Local extraction',
    '上传一张含中文说明书的图片，工具逐行返回识别文字，可直接复制进文档。若图片模糊或倾斜，个别字会误识，需人工校对关键数字。': 'Upload an image with a Chinese manual; the tool returns recognized text line by line, ready to copy into a document. If blurry or skewed, some characters misread, so manually proofread key numbers.',
    '识别不准怎么办？': 'What if recognition is inaccurate?',
    '先提升图像质量(去噪、拉直、提高分辨率)，再对关键字段(金额、日期)人工复核；复杂表格建议用专用结构化 OCR。': 'First improve image quality (denoise, deskew, raise resolution), then manually verify key fields (amount, date); for complex tables use a dedicated structured OCR.',
    '图片会泄露吗？': 'Will the image leak?',
    '不会。本工具在浏览器内完成识别，图片不离开设备；但仅本地模型精度有限，强需求可换云端 OCR 并评估隐私风险。': 'No. Recognition runs entirely inside the browser and the image never leaves the device; but the local-only model has limited accuracy, and strong needs can switch to cloud OCR after assessing privacy risk.',
}, ind=IND)

print('gen_ai_b4 done')
