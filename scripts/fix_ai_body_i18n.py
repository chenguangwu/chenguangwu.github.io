#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai (64) 分类英文态数据源根治：同步三端 + 清孤儿键。

三处数据源（与 science/sports/fun 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/ai-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
  ② i18n/tools/ai.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_ai_body_i18n.py --dry-run
  python3 scripts/fix_ai_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'ai')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'ai-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'ai.json')

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 依据 ai 工具中文名与描述撰写；重点修掉 ai-8/ai-9/ai-12 的 "Ai 8" 类 slug 代号残留。
NAME = {
    'ai': 'Classification Accuracy Evaluator',
    'ai-10': 'CNN Feature Map Size Calculator',
    'ai-11': 'Overfitting Diagnosis',
    'ai-12': 'Data Augmentation Effective Sample Size',
    'ai-13': 'Early Stopping Patience Estimator',
    'ai-14': 'Embedding Cosine Retrieval',
    'ai-15': 'Bayesian Posterior Probability',
    'ai-16': 'Ensemble Weighted Voting',
    'ai-17': 'Prompt Context Window Usage',
    'ai-4': 'Euclidean Distance Calculator',
    'ai-5': 'Batch Size and Iterations Calculator',
    'ai-6': 'Neural Network Parameter Count Estimator',
    'ai-7': 'Confusion Matrix Metrics (MCC / FPR)',
    'ai-8': 'Gradient Descent Step Simulator',
    'ai-9': 'Information Gain (Gini / Entropy) Calculator',
    'ai-code-review': 'AI Code Review',
    'ai-prompt-generator': 'AI Prompt Generator',
    'ai-text-summarizer': 'AI Text Summarizer',
    'attention-flops': 'Attention FLOPs Estimator',
    'attention-head-dim': 'Attention Head Dimension Calculator',
    'auc-rank': 'AUC Rank Estimator',
    'augmentation-multiplier': 'Data Augmentation Multiplier',
    'best-epoch': 'Best Epoch Selector',
    'cohens-kappa': "Cohen's Kappa Coefficient",
    'context-window': 'Context Window Usage Calculator',
    'cosine-similarity': 'Cosine Similarity Calculator',
    'cross-entropy': 'Binary Cross-Entropy Loss Calculator',
    'dropout': 'Dropout Expected Output Calculator',
    'elbow-wcss': 'Elbow Method WCSS Drop Analyzer',
    'epoch-time': 'Epoch Training Time Estimator',
    'flops': 'Model FLOPs Estimator',
    'grad-accumulation': 'Gradient Accumulation Steps Calculator',
    'image-classification': 'Local Image Classification',
    'inference-throughput': 'Inference Throughput Estimator',
    'k-means': 'K-Means Cost (Inertia) Estimator',
    'l1-l2': 'L1 / L2 Regularization Penalty Calculator',
    'l1-l2-regularization': 'L1 / L2 Norm and Penalty Calculator',
    'lr-decay': 'Learning Rate Decay Calculator',
    'lr-warmup': 'Learning Rate Warmup Steps Calculator',
    'min-max': 'Min-Max Feature Scaler',
    'model-accuracy': 'Model Accuracy Calculator',
    'multi-agent-overhead': 'Multi-Agent Communication Overhead Estimator',
    'ocr': 'OCR Text Recognition',
    'precision-recall': 'Precision, Recall and F1 Calculator',
    'quantization-ratio': 'Quantization Compression Ratio Estimator',
    'rag': 'RAG Retrieval Recall Calculator',
    'relu-leakyrelu': 'ReLU and LeakyReLU Activation Visualizer',
    'rmse': 'MSE / RMSE / MAE / R-squared Calculator',
    'roc-auc': 'ROC AUC Estimator',
    'sentiment-analysis': 'Local Sentiment Analysis',
    'sigmoid': 'Sigmoid Output Calculator',
    'softmax': 'Softmax Probability Converter',
    'softmax-2': 'Temperature-Scaled Softmax Visualizer',
    'specificity': 'Specificity Calculator',
    'speech-to-text': 'Speech to Text',
    'steps-per-epoch': 'Steps per Epoch Calculator',
    'temperature-scaling': 'Temperature-Scaled Logits Demo',
    'text-summarization': 'Text Summarizer',
    'token': 'Token Count Estimator',
    'token-2': 'LLM Token Cost Estimator',
    'token-usage': 'Token Usage Estimator',
    'training-flops': 'Training Compute Estimator',
    'transformer-params': 'Transformer Parameter Estimator',
    'vram-estimate': 'Model VRAM Estimator',
}

INTRO = {
    'ai': 'Enter TP / FP / FN / TN from a confusion matrix to get accuracy, precision, recall and F1 for a binary classifier. Everything runs locally in the browser.',
    'ai-10': 'Enter input size, kernel size, stride and padding to compute the feature-map size after convolution or pooling. Built for CNN architecture design and receptive-field checks.',
    'ai-11': 'Compare training and validation loss curves to tell overfitting from underfitting, and get targeted regularization and early-stopping advice.',
    'ai-12': 'Estimate how many effective training samples a set of augmentation transforms actually adds, from the number of transforms and repeat factor. Use it to judge whether your dataset is large enough.',
    'ai-13': 'Estimate a sensible early-stopping patience and the expected total training time from your observed training speed, before you launch a long run.',
    'ai-14': 'Compute cosine similarity between a query vector and document vectors and rank the hits. Handy for RAG pipelines, semantic search and embedding debugging.',
    'ai-15': 'Update a posterior probability from a prior and a likelihood using Bayes theorem. Applies to medical screening, spam filtering and any belief-updating task.',
    'ai-16': 'Combine several models by weighted voting or weighted averaging to get an ensemble probability, and see how each model weight shifts the result.',
    'ai-17': 'Count the tokens used by a multi-turn conversation and see what share of the model context window they occupy, so you know when to trim or compress history.',
    'ai-4': 'Compute the Euclidean distance and cosine similarity between two vectors. Used for feature similarity, nearest-neighbour checks and clustering analysis.',
    'ai-5': 'Enter dataset size and batch size to get the number of iterations per epoch, and sanity-check your training loop configuration.',
    'ai-6': 'Estimate the parameter count of fully-connected and convolutional layers from layer widths, kernel sizes and channel counts. Useful for model sizing and memory budgeting.',
    'ai-7': 'Enter TP / FP / FN / TN to get the Matthews correlation coefficient and false positive rate, two metrics that stay informative on imbalanced data.',
    'ai-8': 'Simulate a single gradient descent update from the current parameter, gradient and learning rate, and watch how the loss moves toward the minimum.',
    'ai-9': 'Measure the impurity drop before and after a binary split using the Gini index or entropy, to compare candidate features when building a decision tree.',
    'ai-code-review': 'Statically analyze JavaScript and TypeScript in the browser to surface common issues such as unused variables, unsafe equality and missing error handling.',
    'ai-prompt-generator': 'Pick a scenario, fill in the key fields, and assemble a well-structured professional prompt from proven templates.',
    'ai-text-summarizer': 'Extract the key sentences from Chinese text with TextRank, entirely in the browser. Nothing is uploaded.',
    'attention-flops': 'Estimate the floating-point operations of a single attention layer and of the whole model from sequence length, head count and hidden size.',
    'attention-head-dim': 'Compute the per-head dimension and the single-layer parameter count of multi-head attention from hidden size and head count.',
    'auc-rank': 'Estimate the area under the ROC curve from sample rank sums using the Mann-Whitney U approach, without drawing the curve.',
    'augmentation-multiplier': 'Compute how much your training set grows after augmentation, from the number of transforms and the repeat factor.',
    'best-epoch': 'Paste per-epoch validation metrics and let the tool pick the best epoch, with an early-stopping recommendation for your next run.',
    'cohens-kappa': "Compute Cohen's kappa from two annotators' labels to measure agreement beyond chance. Standard for annotation QA and diagnostic consistency.",
    'context-window': 'Count the tokens in your prompt and expected completion and see how much of the model context window they consume.',
    'cosine-similarity': 'Compute the cosine similarity of two vectors to measure how closely their directions agree. Common in text matching, recall and embedding comparison.',
    'cross-entropy': 'Compute binary cross-entropy loss from true labels and predicted probabilities to monitor training and spot badly calibrated outputs.',
    'dropout': 'Compute the expected output after dropout from the keep probability, plus the inference-time scaling factor that keeps train and test expectations aligned.',
    'elbow-wcss': 'Enter within-cluster sum of squares for several values of k and find the elbow where adding clusters stops paying off.',
    'epoch-time': 'Estimate the time for one epoch and for the whole run from per-step cost and step count. Useful for scheduling and compute budgeting.',
    'flops': 'Estimate forward-pass FLOPs from fully-connected and convolutional layer dimensions, to compare model architectures before training.',
    'grad-accumulation': 'Compute how many gradient accumulation steps you need to reach a target effective batch size when a single device batch is limited by memory.',
    'image-classification': 'Classify an image with a pre-trained model running locally in the browser and see the Top-5 categories with probabilities. The image never leaves your device.',
    'inference-throughput': 'Estimate inference throughput in tokens per second from the generated token count and end-to-end latency, for capacity planning.',
    'k-means': 'Estimate K-Means inertia, the within-cluster sum of squares, from sample points and centroids, to compare clustering configurations.',
    'l1-l2': 'Compute the L1 or L2 penalty added to the loss from your weights and regularization strength, and compare Lasso sparsity with Ridge shrinkage.',
    'l1-l2-regularization': 'Compute the L1 and L2 norms of a weight vector together with the matching penalty terms, to build intuition about sparsity and shrinkage.',
    'lr-decay': 'Compute the current learning rate under exponential or step decay schedules, for scheduler tuning and training-curve diagnosis.',
    'lr-warmup': 'Compute how many steps a linear learning-rate warmup should cover, from total training steps and the warmup ratio, to keep early training stable.',
    'min-max': 'Linearly rescale feature values into the [0, 1] or [-1, 1] range, the standard preprocessing step before distance-based models.',
    'model-accuracy': 'Compute overall accuracy and per-class accuracy from a confusion matrix, for model evaluation and error analysis reports.',
    'multi-agent-overhead': 'Estimate the communication overhead of a fully-connected multi-agent system from agent count and message frequency, before you commit to an architecture.',
    'ocr': 'Extract text from images locally in the browser, with Chinese and English support and multi-line layout. Results can be copied and edited.',
    'precision-recall': 'Compute precision, recall and F1 from true positives, false positives and false negatives. Useful for threshold selection on imbalanced data.',
    'quantization-ratio': 'Estimate the parameter and memory compression ratio when quantizing a model, for example from FP32 down to INT8, to plan deployment.',
    'rag': 'Compute retrieval recall from the number of relevant documents and the number actually retrieved, to measure the coverage of your RAG retriever.',
    'relu-leakyrelu': 'Compute and compare ReLU and LeakyReLU activations for a given input, with a visual plot that shows the dead-neuron problem.',
    'rmse': 'Evaluate regression quality from predictions and ground truth, reporting MSE, RMSE, MAE and R-squared in one pass.',
    'roc-auc': 'Estimate the area under the ROC curve from positive and negative prediction scores, to compare the ranking ability of classifiers.',
    'sentiment-analysis': 'Detect positive or negative sentiment in text locally, with an emotion label and confidence score. Suited to quick review and opinion triage.',
    'sigmoid': 'Map any real number through the sigmoid function and see where it falls relative to the classification threshold.',
    'softmax': 'Convert a set of logits into a probability distribution that sums to 1, the standard last step of a multi-class model.',
    'softmax-2': 'See how a temperature parameter sharpens or flattens a softmax distribution, which is the basis of model calibration.',
    'specificity': 'Compute specificity from true negatives and false positives to measure how well a model recognises the negative class. Complements sensitivity.',
    'speech-to-text': 'Transcribe recorded speech into Chinese text in real time using the Web Speech API, entirely in the browser.',
    'steps-per-epoch': 'Compute the number of training steps per epoch from dataset size and batch size, for training-loop and sharding checks.',
    'temperature-scaling': 'Scale logits by a temperature before softmax and watch the calibrated distribution change, a practical demo of confidence calibration.',
    'text-summarization': 'Extract the key sentences of an article locally with an adjustable compression ratio, for fast reading of long documents.',
    'token': 'Estimate how many tokens a piece of text will consume, so you can keep prompts inside the context window and control cost.',
    'token-2': 'Estimate API cost from input and output token counts and unit price, to budget a LLM feature before launch.',
    'token-usage': 'Estimate token usage by the mix of Chinese, English and code in your text, and see how much tokenizers disagree.',
    'training-flops': 'Estimate total training FLOPs from parameter count and training tokens using Kaplan-style scaling laws, for compute planning.',
    'transformer-params': 'Estimate the parameter count of a Transformer from layer count, hidden size and vocabulary, separating body and embedding parameters.',
    'vram-estimate': 'Estimate the VRAM needed for model weights and inference from parameter count, precision bytes and activation overhead, to choose deployment hardware.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# 候选写盘格式（ai-body.json 现为紧凑型 indent=0+无空格分隔符，
# 盲目 indent=2 重写会造成整文件 diff，故按原格式探测后回写）
_CANDIDATES = (
    dict(indent=0, separators=(',', ':')),
    dict(indent=1, separators=(',', ':')),
    dict(indent=1),
    dict(indent=2, separators=(',', ':')),
    dict(indent=2),
    dict(indent=None, separators=(',', ':')),
    dict(indent=None),
)


def dump_like(path, data, orig_raw):
    """按文件原有 JSON 格式回写：逐一尝试候选格式，取能无损还原原串的那个。"""
    body_raw = orig_raw.rstrip('\n')
    trailing = '\n' if orig_raw.endswith('\n') else ''
    try:
        orig = json.loads(orig_raw)
    except Exception:
        orig = None
    if orig is not None:
        for c in _CANDIDATES:
            try:
                if json.dumps(orig, ensure_ascii=False, **c) == body_raw:
                    return json.dumps(data, ensure_ascii=False, **c) + trailing
            except Exception:
                continue
    return json.dumps(data, ensure_ascii=False, indent=2) + trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = added_body = added_gis = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'ai/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'ai'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'ai')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + ai-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + ai.json 新增条目:', slug)
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # ---- 孤儿键清理（三端统一）----
    # 判定口径：键名在全站无对应页面，或对应页面不在本行业目录（跨行业残留），一律删除。
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    ai_basenames = set(slugs)

    orphans = [k for k in list(body.keys())
               if k not in all_basenames or k not in ai_basenames]
    for k in orphans:
        del body[k]

    ov_orphans = [k for k in list(ov.keys())
                  if k.startswith('ai/') and k.split('/', 1)[1] not in ai_basenames]
    for k in ov_orphans:
        del ov[k]

    gis_orphans = [k for k in list(gis.keys()) if k not in ai_basenames]
    for k in gis_orphans:
        del gis[k]

    print('\n--- 汇总 ---')
    print('ai 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('ai-body 更新:', chg_body, ' 新增:', added_body)
    print('ai.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis)
    print('ai-body 孤儿键删除:', len(orphans), orphans)
    print('_en_override 孤儿键删除:', len(ov_orphans))
    print('ai.json 孤儿键删除:', len(gis_orphans), gis_orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    with open(OV, encoding='utf-8') as f:
        ov_raw = f.read()
    with open(BODY, encoding='utf-8') as f:
        body_raw = f.read()
    with open(GIS, encoding='utf-8') as f:
        gis_raw = f.read()

    for path, data, raw in ((OV, ov, ov_raw), (BODY, body, body_raw), (GIS, gis, gis_raw)):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dump_like(path, data, raw))
        print('written:', path)


if __name__ == '__main__':
    raise SystemExit(main())
