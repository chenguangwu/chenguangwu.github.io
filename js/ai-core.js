// js/ai-core.js — ToolBox 纯前端 AI 推理共享加载器 (Transformers.js)
//
// 设计原则（纯前端 / 隐私优先）：
//  - 模型从 Hugging Face CDN 懒加载（仅首次使用时下载，浏览器缓存 + 库内置 IndexedDB 缓存）
//  - 所有推理在用户浏览器本地完成，图片 / 音频 / 文本不会上传到任何服务器
//  - 不依赖任何后端 API
//
// 用法（工具页内）：
//   <script type="module">
//     import { getPipeline, progressText, decodeAudioTo16k } from '../../js/ai-core.js';
//   </script>

const TF_VERSION = '3.8.1';
const CDN = `https://cdn.jsdelivr.net/npm/@huggingface/transformers@${TF_VERSION}`;

// 模型 revision 锁定：固定到 commit sha，避免上游更新 resolve/main 时静默换权重。
// 这些 sha 取自 https://huggingface.co/api/models/<repo> 的 sha 字段；
// 升级模型或 Transformers.js 时需复验 pipeline({ revision }) 仍被透传。
const MODEL_REVISIONS = {
  'Xenova/whisper-base': '64da57285918e20ea79ea5c88eed7197933abaa8',
  'Xenova/distilbert-base-uncased-finetuned-sst-2-english': '0b6928efcb76139cae2c6881d49cda67fe119f42',
  'Xenova/trocr-base-printed': 'cf024f7df347684b6ee92859452962b67c6873fb',
  'Xenova/vit-base-patch16-224': '66fef688e8dbe77dd9d5aa256353f9ad8b0ef799',
  'Xenova/distilbart-cnn-6-6': '6b476295a3cf27d5b20e8c8b847a54ab8e5d0df9',
};

let _tf = null;
let _tfPromise = null;

// 懒加载 Transformers.js（动态 import，避免拖慢首屏）
export async function getTransformers() {
  if (_tf) return _tf;
  if (!_tfPromise) {
    _tfPromise = import(/* @vite-ignore */ CDN);
  }
  _tf = await _tfPromise;
  // 版本断言：CDN 若下发非 3.8.1 内容则拒绝继续（动态 import 无法挂 SRI）
  if (_tf.env && _tf.env.version && _tf.env.version !== TF_VERSION) {
    const actual = _tf.env.version;
    _tf = null;
    _tfPromise = null;
    throw new Error(`Transformers.js 版本校验失败：期望 ${TF_VERSION}，实际 ${actual}`);
  }
  // 纯前端：禁用本地模型目录，全部走 CDN 缓存
  _tf.env.allowLocalModels = false;
  return _tf;
}

// 带缓存的 pipeline 加载（同一模型只初始化一次）
const _cache = new Map();
export async function getPipeline(task, model, onProgress) {
  const revision = MODEL_REVISIONS[model];
  if (!revision) {
    console.warn(`[ai-core] 模型 ${model} 未登记 revision，回退 main；上游更新不会被感知。`);
  }
  const key = `${task}|${model}|${revision || 'main'}`;
  if (_cache.has(key)) {
    // 命中缓存视为模型可用（成功路径）
    if (typeof window !== 'undefined' && window.ToolBox && window.ToolBox.Metrics) {
      window.ToolBox.Metrics.track('ai_model_success', { model: model });
    }
    return _cache.get(key);
  }
  const tf = await getTransformers();
  const options = { progress_callback: (e) => { if (onProgress) onProgress(e); } };
  if (revision) options.revision = revision;
  try {
    const p = await tf.pipeline(task, model, options);
    _cache.set(key, p);
    if (typeof window !== 'undefined' && window.ToolBox && window.ToolBox.Metrics) {
      window.ToolBox.Metrics.track('ai_model_success', { model: model });
    }
    return p;
  } catch (err) {
    if (typeof window !== 'undefined' && window.ToolBox && window.ToolBox.Metrics) {
      window.ToolBox.Metrics.track('ai_model_failure', { model: model });
    }
    throw err;
  }
}

// 把进度事件转成可读中文文案
export function progressText(e) {
  if (!e) return '';
  if (e.status === 'progress' && e.total) {
    const pct = Math.round((e.loaded / e.total) * 100);
    return `下载 ${e.file || ''} ${pct}%`;
  }
  if (e.status === 'ready') return '模型已就绪，开始推理…';
  if (e.status === 'initiate') return `开始加载 ${e.file || ''}`;
  if (e.status === 'download') return `下载 ${e.file || ''}…`;
  if (e.status === 'done') return '模型加载完成';
  return e.status || '';
}

// 解码音频文件为 16000Hz 单声道 Float32Array（Whisper 需要）
export async function decodeAudioTo16k(file) {
  const arrBuf = await file.arrayBuffer();
  const AC = window.AudioContext || window.webkitAudioContext;
  const ac = new AC();
  const audioBuf = await ac.decodeAudioData(arrBuf);
  const targetRate = 16000;
  const ratio = audioBuf.sampleRate / targetRate;
  const src = audioBuf.getChannelData(0);
  const newLen = Math.max(1, Math.round(src.length / ratio));
  const out = new Float32Array(newLen);
  for (let i = 0; i < newLen; i++) {
    const pos = i * ratio;
    const i0 = Math.floor(pos);
    const i1 = Math.min(i0 + 1, src.length - 1);
    const frac = pos - i0;
    out[i] = src[i0] * (1 - frac) + src[i1] * frac;
  }
  if (ac.close) ac.close();
  return out;
}

// 简单 HTML 转义，防止结果文本破坏页面
export function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
