/* ToolBox popular-tool productivity layer.
 * Adds consistent run/copy/export/example/reset workflows to the curated 60
 * without changing each tool's calculation logic. Everything stays local.
 */
(function () {
  'use strict';

  const FILE_TOOLS = new Set([
    'base64-file.html', 'image-compress.html', 'image-format-converter.html',
    'image-cropper.html', 'favicon-generator.html', 'pdf-merge.html',
    'pdf-split.html', 'pdf-rotate.html'
  ]);
  const GENERATOR_TOOLS = new Set([
    'qrcode.html', 'password-generator.html', 'uuid-generator.html', 'wifi-qr.html',
    'lorem.html', 'barcode-generator.html', 'random-string.html'
  ]);
  const CALCULATOR_TOOLS = new Set([
    'unit-converter.html', 'percentage-calculator.html', 'age-calculator.html',
    'date-diff.html', 'timezone-converter.html', 'gpa-calculator.html',
    'roi-calculator.html', 'mortgage-calculator.html', 'compound-interest.html',
    'invoice-generator.html', 'ip-calculator.html'
  ]);
  const ACTION_LABELS = {
    'yaml-to-json.html': ['转换为 JSON', '轉換為 JSON', 'Convert to JSON'],
    'markdown-to-html.html': ['生成 HTML', '產生 HTML', 'Generate HTML'],
    'css-minify.html': ['压缩 CSS', '壓縮 CSS', 'Minify CSS'],
    'js-minify.html': ['压缩 JavaScript', '壓縮 JavaScript', 'Minify JavaScript'],
    'csv-validator.html': ['校验 CSV', '驗證 CSV', 'Validate CSV'],
    'mime-type-lookup.html': ['查询 MIME', '查詢 MIME', 'Look up MIME'],
    'random-string.html': ['生成字符串', '產生字串', 'Generate strings']
  };

  const COPY = {
    'zh-CN': {
      badge: '⚡ 效率工具栏', local: '本地处理', run: '运行', copy: '复制结果',
      export: '导出结果', sample: '恢复示例', clear: '清空输入', shortcut: 'Ctrl/⌘ + Enter 快速运行',
      copied: '结果已复制', downloaded: '结果已导出', empty: '暂无可复制的结果，请先运行工具',
      restored: '已恢复页面示例', cleared: '输入已清空', chars: '字符', lines: '行', fields: '个参数', files: '个文件入口'
    },
    'zh-TW': {
      badge: '⚡ 效率工具列', local: '本機處理', run: '執行', copy: '複製結果',
      export: '匯出結果', sample: '恢復範例', clear: '清空輸入', shortcut: 'Ctrl/⌘ + Enter 快速執行',
      copied: '結果已複製', downloaded: '結果已匯出', empty: '暫無可複製的結果，請先執行工具',
      restored: '已恢復頁面範例', cleared: '輸入已清空', chars: '字元', lines: '行', fields: '個參數', files: '個檔案入口'
    },
    'en-US': {
      badge: '⚡ Productivity bar', local: 'Local only', run: 'Run', copy: 'Copy result',
      export: 'Export result', sample: 'Restore sample', clear: 'Clear inputs', shortcut: 'Ctrl/⌘ + Enter to run',
      copied: 'Result copied', downloaded: 'Result exported', empty: 'No result yet. Run the tool first.',
      restored: 'Sample restored', cleared: 'Inputs cleared', chars: 'characters', lines: 'lines', fields: 'fields', files: 'file inputs'
    }
  };

  let locale = 'zh-CN';
  let text = COPY[locale];
  let primaryAction = null;
  let editableFields = [];
  let initialState = [];
  let metricSource = null;
  let bar = null;
  let toolCard = null;

  const basename = () => location.pathname.split('/').filter(Boolean).pop() || '';

  function currentLocale(explicit) {
    const value = explicit || (window.I18n && window.I18n.get && window.I18n.get()) || document.documentElement.lang || '';
    const normalized = String(value).toLowerCase();
    if (normalized.includes('tw')) return 'zh-TW';
    if (normalized.includes('hk')) return 'zh-TW';
    if (normalized.startsWith('en')) return 'en-US';
    return 'zh-CN';
  }

  function toast(message, type) {
    if (window.ToolBox && typeof window.ToolBox.showToast === 'function') {
      window.ToolBox.showToast(message, type || 'success');
      return;
    }
    const node = document.createElement('div');
    node.className = 'tb-he-toast';
    node.textContent = message;
    document.body.appendChild(node);
    requestAnimationFrame(() => node.classList.add('show'));
    setTimeout(() => node.remove(), 1800);
  }

  function visible(element) {
    if (!element || element.closest('.tb-hot-enhancer')) return false;
    const style = getComputedStyle(element);
    return style.display !== 'none' && style.visibility !== 'hidden' && element.getClientRects().length > 0;
  }

  function fieldValue(field) {
    if (field.type === 'checkbox' || field.type === 'radio') return field.checked;
    if (field.type === 'file') return '';
    return field.value;
  }

  function restoreField(field, value) {
    if (field.type === 'checkbox' || field.type === 'radio') field.checked = Boolean(value);
    else if (field.type === 'file') field.value = '';
    else field.value = value == null ? '' : value;
    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function resultText() {
    const selectors = [
      '[data-result]', '.result-box', '.output', '.output-box', '.preview-result',
      '.password-display', '.big-result', '.code-row', '.result-card', '.data-grid',
      '.json-view', '.tree-view', '#result', '#output', '#preview', '#viewJson',
      '[id^="result"]', '[id^="output"]', '[id$="Result"]', '[id$="Output"]',
      '[id$="Stats"]', '[id$="Display"]', '.result-grid', '.stat-grid',
      'textarea[readonly]', 'pre.code-block'
    ].join(',');
    // Some legacy tools render their output outside the first card after the
    // browser repairs imperfect historical markup. Search the page for the
    // deliberately narrow result selectors so copy/export still works.
    const candidates = Array.from(document.querySelectorAll(selectors)).filter(visible);
    const chunks = [];
    const seen = new Set();
    candidates.forEach((element) => {
      const value = /^(TEXTAREA|INPUT)$/.test(element.tagName) ? element.value : element.innerText;
      const cleaned = String(value || '').replace(/\n{3,}/g, '\n\n').trim();
      if (!cleaned || cleaned === '--' || seen.has(cleaned)) return;
      if (chunks.some((item) => item.includes(cleaned))) return;
      seen.add(cleaned);
      chunks.push(cleaned);
    });
    return chunks.join('\n\n');
  }

  async function copyResult() {
    const value = resultText();
    if (!value) return toast(text.empty, 'warning');
    if (window.ToolBox && typeof window.ToolBox.copyText === 'function') {
      await window.ToolBox.copyText(value, text.copied);
    } else {
      await navigator.clipboard.writeText(value);
      toast(text.copied);
    }
  }

  function exportResult() {
    const value = resultText();
    if (!value) return toast(text.empty, 'warning');
    const title = (document.querySelector('h1') || document.querySelector('h2'))?.textContent.trim() || 'toolbox-result';
    const safeName = title.replace(/[^\w\u3400-\u9fff-]+/g, '-').replace(/^-|-$/g, '') || 'toolbox-result';
    if (window.ToolBox && typeof window.ToolBox.downloadText === 'function') {
      window.ToolBox.downloadText(`${safeName}.txt`, value);
    } else {
      const url = URL.createObjectURL(new Blob([value], { type: 'text/plain;charset=utf-8' }));
      const link = Object.assign(document.createElement('a'), { href: url, download: `${safeName}.txt` });
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 0);
    }
    toast(text.downloaded);
  }

  function restoreSample() {
    initialState.forEach(({ field, value }) => restoreField(field, value));
    toast(text.restored);
    updateMetric();
  }

  function clearInputs() {
    editableFields.forEach((field) => {
      if (field.type === 'checkbox' || field.type === 'radio') restoreField(field, false);
      else if (field.tagName === 'SELECT') restoreField(field, field.options[0]?.value || '');
      else restoreField(field, '');
    });
    toast(text.cleared);
    updateMetric();
  }

  function updateMetric() {
    if (!bar) return;
    const metric = bar.querySelector('.tb-he-metric');
    if (!metric) return;
    const fileCount = editableFields.filter((field) => field.type === 'file').length;
    if (FILE_TOOLS.has(basename()) && fileCount) {
      metric.textContent = `${fileCount} ${text.files}`;
      return;
    }
    if (metricSource) {
      const value = String(metricSource.value || '');
      metric.textContent = `${value.length} ${text.chars} · ${value ? value.split(/\r?\n/).length : 0} ${text.lines}`;
      return;
    }
    metric.textContent = `${editableFields.length} ${text.fields}`;
  }

  function actionLabel() {
    const labels = ACTION_LABELS[basename()];
    if (!labels) return text.run;
    return locale === 'en-US' ? labels[2] : (locale === 'zh-CN' ? labels[0] : labels[1]);
  }

  function applyLocale(nextLocale) {
    locale = currentLocale(nextLocale);
    text = COPY[locale];
    if (!bar) return;
    bar.querySelector('.tb-he-badge').textContent = text.badge;
    bar.querySelector('.tb-he-local').textContent = `✓ ${text.local}`;
    const shortcut = bar.querySelector('.tb-he-shortcut');
    shortcut.textContent = primaryAction ? text.shortcut : '';
    shortcut.hidden = !primaryAction;
    const runButton = bar.querySelector('[data-he-action="run"]');
    if (runButton) runButton.textContent = `▶ ${actionLabel()}`;
    const copyButton = bar.querySelector('[data-he-action="copy"]');
    const exportButton = bar.querySelector('[data-he-action="export"]');
    if (copyButton) copyButton.textContent = `⧉ ${text.copy}`;
    if (exportButton) exportButton.textContent = `↓ ${text.export}`;
    const sampleButton = bar.querySelector('[data-he-action="sample"]');
    if (sampleButton) sampleButton.textContent = `↺ ${text.sample}`;
    bar.querySelector('[data-he-action="clear"]').textContent = `× ${text.clear}`;
    updateMetric();
  }

  function enhancePrimaryLabel() {
    const labels = ACTION_LABELS[basename()];
    if (!labels || !primaryAction) return;
    if (/^(计算|計算|Calculate)$/i.test(primaryAction.textContent.trim())) primaryAction.dataset.heGenericAction = 'true';
    if (primaryAction.dataset.heGenericAction !== 'true') return;
    primaryAction.textContent = actionLabel();
  }

  function buildBar(card) {
    const hasTextActions = !FILE_TOOLS.has(basename());
    const hasSample = initialState.some(({ field, value }) => {
      if (field.type === 'file') return false;
      return typeof value === 'boolean' ? value : String(value || '').trim().length > 0;
    });
    bar = document.createElement('section');
    bar.className = 'tb-hot-enhancer';
    bar.setAttribute('aria-label', 'Tool productivity controls');
    bar.innerHTML = `
      <div class="tb-he-summary">
        <strong class="tb-he-badge"></strong>
        <span class="tb-he-local"></span>
        <span class="tb-he-metric"></span>
        <span class="tb-he-shortcut"></span>
      </div>
      <div class="tb-he-actions">
        ${primaryAction ? '<button type="button" class="tb-he-btn primary" data-he-action="run"></button>' : ''}
        ${hasTextActions ? '<button type="button" class="tb-he-btn" data-he-action="copy"></button>' : ''}
        ${hasTextActions ? '<button type="button" class="tb-he-btn" data-he-action="export"></button>' : ''}
        ${hasSample ? '<button type="button" class="tb-he-btn" data-he-action="sample"></button>' : ''}
        <button type="button" class="tb-he-btn quiet" data-he-action="clear"></button>
      </div>`;
    const intro = card.querySelector('h2');
    const description = intro && intro.nextElementSibling && intro.nextElementSibling.tagName === 'P' ? intro.nextElementSibling : intro;
    if (description) description.insertAdjacentElement('afterend', bar);
    else card.prepend(bar);

    bar.addEventListener('click', (event) => {
      const button = event.target.closest('[data-he-action]');
      if (!button) return;
      const action = button.dataset.heAction;
      if (action === 'run' && primaryAction) primaryAction.click();
      if (action === 'copy') copyResult();
      if (action === 'export') exportResult();
      if (action === 'sample') restoreSample();
      if (action === 'clear') clearInputs();
    });
    applyLocale();
  }

  function injectStyles() {
    if (document.getElementById('tb-hot-enhancer-style')) return;
    const style = document.createElement('style');
    style.id = 'tb-hot-enhancer-style';
    style.textContent = `
      .tb-hot-enhancer{margin:12px 0 16px;padding:10px 12px;border:1px solid var(--border,#e5e7eb);border-radius:12px;background:linear-gradient(135deg,rgba(255,107,53,.055),rgba(124,58,237,.045));}
      .tb-he-summary,.tb-he-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.tb-he-summary{font-size:12px;color:var(--text-muted,#6b7280);margin-bottom:8px}.tb-he-badge{color:var(--text,#1f2937);font-size:12.5px}.tb-he-local{color:var(--success,#10b981)}.tb-he-shortcut{margin-left:auto}.tb-he-metric{padding:2px 7px;border-radius:999px;background:var(--card-bg,#fff);border:1px solid var(--border,#e5e7eb)}
      .tb-he-btn{min-height:34px;padding:6px 11px;border:1px solid var(--border,#e5e7eb);border-radius:9px;background:var(--card-bg,#fff);color:var(--text,#1f2937);font:600 12px/1.2 inherit;cursor:pointer}.tb-he-btn:hover{border-color:var(--primary,#ff6b35);transform:translateY(-1px)}.tb-he-btn.primary{color:#fff;border-color:transparent;background:var(--gradient-primary,linear-gradient(135deg,#ff6b35,#7c3aed))}.tb-he-btn.quiet{margin-left:auto;color:var(--text-muted,#6b7280)}
      .tb-he-toast{position:fixed;left:50%;bottom:28px;z-index:99999;transform:translate(-50%,12px);opacity:0;padding:9px 14px;border-radius:10px;background:#1f2937;color:#fff;font-size:13px;transition:.2s}.tb-he-toast.show{transform:translate(-50%,0);opacity:1}
      @media(max-width:640px){.tb-he-shortcut{display:none}.tb-he-actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.tb-he-btn,.tb-he-btn.quiet{width:100%;margin:0}.tb-he-summary{gap:6px}}
    `;
    document.head.appendChild(style);
  }

  function init() {
    if (document.querySelector('.tb-hot-enhancer')) return;
    const card = document.querySelector('.container > .card, main .card, .card');
    if (!card) return;
    toolCard = card;
    editableFields = Array.from(card.querySelectorAll('input:not([type="hidden"]), textarea, select'))
      .filter((field) => !field.disabled && !field.readOnly);
    initialState = editableFields.map((field) => ({ field, value: fieldValue(field) }));
    metricSource = editableFields.find((field) => field.tagName === 'TEXTAREA') ||
      editableFields.find((field) => ['text', 'search', 'url'].includes(field.type));
    primaryAction = Array.from(card.querySelectorAll('button.btn.primary, .toolbar button.primary, button[type="submit"]'))
      .find((button) => !button.closest('.tb-hot-enhancer') && visible(button)) || null;
    if (FILE_TOOLS.has(basename())) primaryAction = null;

    injectStyles();
    buildBar(card);
    enhancePrimaryLabel();
    editableFields.forEach((field) => field.addEventListener('input', () => {
      if (field.tagName === 'TEXTAREA' || ['text', 'search', 'url'].includes(field.type)) metricSource = field;
      updateMetric();
    }));
    document.addEventListener('keydown', (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && primaryAction) {
        event.preventDefault();
        primaryAction.click();
      }
    });
    document.addEventListener('toolbox:langchange', (event) => {
      applyLocale(event.detail && event.detail.lang);
      enhancePrimaryLabel();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
}());
