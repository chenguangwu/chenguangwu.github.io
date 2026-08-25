/* B5-10 隐私优先的本地使用指标（纯前端，默认关闭，绝不向任何第三方发送数据）
 *
 * 设计原则：
 *  - 默认关闭（opt-in）。只有用户在「本地数据管理」中显式开启后才会记录。
 *  - 所有数据仅存于浏览器 localStorage，不上传任何服务器，不含任何后端请求。
 *  - 只记录匿名、聚合所需的字段：事件类型、工具文件名、行业、AI 模型名、成功/失败布尔。
 *  - 绝不记录用户输入内容、URL 查询参数内容、文件内容或个人标识。
 *  - 采样上限 + 保留天数限制，避免无界增长。
 *
 * 暴露 window.ToolBox.Metrics：
 *   EVENTS        事件字典（中文名）
 *   enabled()     是否已开启
 *   setEnabled(b) 开启/关闭（写入 localStorage toolbox_metrics_optin）
 *   track(name, payload) 记录一次事件（未开启则静默跳过）
 *   summary()     本地汇总（各事件计数 + 时间范围）
 *   exportData()  导出当前数据（供维护者本地聚合分析）
 *   clear()       清空本地指标事件
 */
(function (global) {
  'use strict';

  var KEY = 'toolbox_metrics_optin';        // '1' = 已开启
  var LOG_KEY = 'toolbox_metrics_events';   // 事件环形缓冲
  var MAX_EVENTS = 500;                     // 单端采样上限
  var RETENTION_DAYS = 30;                  // 保留天数

  // 事件字典：type -> 中文说明
  var EVENTS = {
    tool_launch: '工具打开',
    tool_complete: '工具完成计算/产出',
    copy: '复制结果',
    download: '下载文件',
    guide_click: '点击使用指南',
    chain_complete: '完成一条工具链',
    ai_model_success: 'AI 模型推理成功',
    ai_model_failure: 'AI 模型推理失败'
  };

  function enabled() { return localStorage.getItem(KEY) === '1'; }
  function setEnabled(on) { localStorage.setItem(KEY, on ? '1' : '0'); }

  function load() {
    try { return JSON.parse(localStorage.getItem(LOG_KEY) || '[]'); }
    catch (e) { return []; }
  }
  function save(arr) {
    var cutoff = Date.now() - RETENTION_DAYS * 86400000;
    arr = arr.filter(function (e) { return e.t >= cutoff; });
    if (arr.length > MAX_EVENTS) arr = arr.slice(arr.length - MAX_EVENTS);
    try { localStorage.setItem(LOG_KEY, JSON.stringify(arr)); } catch (e) {}
  }

  // 仅保留匿名聚合字段，禁止记录用户输入/查询内容/个人标识
  function track(name, payload) {
    if (!enabled()) return;
    if (!EVENTS[name]) return;
    var ev = { e: name, t: Date.now() };
    if (payload && typeof payload === 'object') {
      if (payload.tool) ev.tool = String(payload.tool);                 // 文件名，非用户内容
      if (payload.industry) ev.ind = String(payload.industry);
      if (payload.model) ev.model = String(payload.model);             // 模型名，非用户输入
      if (typeof payload.ok === 'boolean') ev.ok = payload.ok;
    }
    var arr = load();
    arr.push(ev);
    save(arr);
  }

  function summary() {
    var arr = load();
    var by = {};
    Object.keys(EVENTS).forEach(function (k) { by[k] = 0; });
    arr.forEach(function (e) { if (by[e.e] !== undefined) by[e.e]++; });
    return {
      total: arr.length,
      by: by,
      since: arr.length ? arr[0].t : null,
      latest: arr.length ? arr[arr.length - 1].t : null
    };
  }

  function exportData() { return { optin: enabled(), events: load() }; }
  function clear() { localStorage.removeItem(LOG_KEY); }

  global.ToolBox = global.ToolBox || {};
  global.ToolBox.Metrics = {
    EVENTS: EVENTS,
    enabled: enabled,
    setEnabled: setEnabled,
    track: track,
    summary: summary,
    exportData: exportData,
    clear: clear,
    MAX_EVENTS: MAX_EVENTS,
    RETENTION_DAYS: RETENTION_DAYS
  };
})(window);
