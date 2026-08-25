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

let _tf = null;
let _tfPromise = null;

// 懒加载 Transformers.js（动态 import，避免拖慢首屏）
export async function getTransformers() {
  if (_tf) return _tf;
  if (!_tfPromise) {
    _tfPromise = import(/* @vite-ignore */ CDN);
  }
  _tf = await _tfPromise;
  // 纯前端：禁用本地模型目录，全部走 CDN 缓存
  _tf.env.allowLocalModels = false;
  return _tf;
}

// 带缓存的 pipeline 加载（同一模型只初始化一次）
const _cache = new Map();
export async function getPipeline(task, model, onProgress) {
  const key = `${task}|${model}`;
  if (_cache.has(key)) {
    // 命中缓存视为模型可用（成功路径）
    if (typeof window !== 'undefined' && window.ToolBox && window.ToolBox.Metrics) {
      window.ToolBox.Metrics.track('ai_model_success', { model: model });
    }
    return _cache.get(key);
  }
  const tf = await getTransformers();
  try {
    const p = await tf.pipeline(task, model, {
      progress_callback: (e) => { if (onProgress) onProgress(e); },
    });
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
