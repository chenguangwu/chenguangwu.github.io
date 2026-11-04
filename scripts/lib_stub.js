#!/usr/bin/env node
/**
 * 桩保真度共享模块（2026-11-04）
 *
 * 背景：各 verify_* 自带的 DOM 桩长期存在「默认态失真」——
 *   - input 默认值只认 `id` 在 `value` 之前、且只认双引号；
 *   - `<option value="5" selected>` 被取成首个 option（civil/masonry-bearing、
 *     forestry/tree-volume 均因此把错的行为记成事实）；
 *   - `<select multiple>` 只取一个 selected；
 *   - textarea 初始文本只写 `.value`，不写 `.textContent`；
 *   - 带 `checked` 的 checkbox/radio 在全量用例路径恒为 false。
 *
 * 用法：
 *   const { pageDefaults, stubFidelity } = require("./lib_stub.js");
 *   // 默认仍走 legacy（等失配用例迁移完再翻默认）；显式开启：
 *   //   TB_STUB_FIDELITY=1 node scripts/discriminate_check.js
 *   // 一次性逃生（强制回 legacy）：
 *   //   TB_STUB_LEGACY=1 ...
 *
 * 说明：本模块只提供「解析 + 真机语义」的纯函数，不直接改任何桩；
 * 各脚本按需接入，避免一次性全量改。
 */

// 默认 legacy：仅 TB_STUB_FIDELITY=1 时启用保真度；TB_STUB_LEGACY=1 永远优先（逃生开关）。
const FIDELITY = process.env.TB_STUB_FIDELITY === "1" && process.env.TB_STUB_LEGACY !== "1";

function stubFidelity() {
  return FIDELITY;
}

/** 解析 `<input>` 默认值：属性顺序无关、单双引号皆可；无 value 按空串。
 *  opts.skipTypes：跳过这些 type（判别器模拟回退时不把 checkbox/radio 的 value 当输入值）。 */
function parseInputDefaults(html, opts) {
  const skip = (opts && opts.skipTypes) || null;
  const out = {};
  for (const m of String(html).matchAll(/<input\b[^>]*>/gi)) {
    const tag = m[0];
    const id = (tag.match(/\bid\s*=\s*["']([^"']+)["']/i) || [, ""])[1];
    if (!id) continue;
    if (skip) {
      const typ = ((tag.match(/\btype\s*=\s*["']([^"']*)["']/i) || [])[1] || "text").toLowerCase();
      if (skip.test(typ)) continue;
    }
    const val = tag.match(/\bvalue\s*=\s*["']([^"']*)["']/i);
    if (val && out[id] === undefined) out[id] = val[1];
  }
  return out;
}

/** 解析 `<textarea>` 初始文本（真机同时体现在 .value 与 .textContent）。 */
function parseTextareaDefaults(html) {
  const out = {};
  for (const m of String(html).matchAll(/<textarea\b[^>]*id\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/textarea>/gi)) {
    out[m[1]] = m[2].replace(/&#10;/g, "\n").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
  }
  return out;
}

/** 解析全部 `<select>`：返回 id -> options 数组（数组上带 `.multiple` 标记）。 */
function parseSelects(html) {
  const out = {};
  for (const m of String(html).matchAll(/<select\b([^>]*)>([\s\S]*?)<\/select>/gi)) {
    const attrs = m[1] || "";
    const id = (attrs.match(/\bid\s*=\s*["']([^"']+)["']/i) || [, ""])[1];
    if (!id) continue;
    const arr = [...m[2].matchAll(/<option([^>]*)>([\s\S]*?)<\/option>/gi)].map((x) => {
      const a = x[1] || "";
      return {
        value: (a.match(/\bvalue\s*=\s*["']([^"']*)["']/i) || [, ""])[1],
        text: x[2].replace(/<[^>]+>/g, "").trim(),
        attrs: a,
        selected: /\bselected\b/i.test(a),   // 布尔属性与 selected="selected" 都命中
      };
    });
    arr.multiple = /\bmultiple\b/i.test(attrs);
    out[id] = arr;
  }
  return out;
}

/**
 * 单个 select 的默认值：
 * 优先带 `selected` 的 option（不论属性顺序），无则回退首个 option；
 * 无 value 属性时真机 `.value` 取选项文本。
 */
function selectDefault(options) {
  if (!Array.isArray(options) || !options.length) return "";
  const hit = options.find((o) => o.selected) || options[0];
  return hit.value !== "" ? hit.value : (hit.text || "");
}

/** 解析带 HTML `checked` 默认态的 checkbox/radio（按 id）。 */
function parseCheckedIds(html) {
  const ids = new Set();
  for (const m of String(html).matchAll(/<input\b[^>]*>/gi)) {
    const tag = m[0];
    if (!/type\s*=\s*["']?(?:radio|checkbox)/i.test(tag)) continue;
    if (!/\bchecked\b/i.test(tag)) continue;
    const id = (tag.match(/\bid\s*=\s*["']([^"']+)["']/i) || [, ""])[1];
    if (id) ids.add(id);
  }
  return ids;
}

/**
 * 页面默认态（真机首屏口径）：
 * input value + textarea 初始文本 + select 默认选中值。
 * 返回 id -> 字符串；`<select multiple>` 返回首个 selected（与真机 `.value` 一致，
 * 全部 selected 由 `parseSelects(id).multiple` 另行读取）。
 */
function pageDefaults(html) {
  const out = {};
  Object.assign(out, parseInputDefaults(html));
  const ta = parseTextareaDefaults(html);
  for (const [id, v] of Object.entries(ta)) out[id] = v;   // textarea 覆盖同名 input
  const sels = parseSelects(html);
  for (const [id, opts] of Object.entries(sels)) {
    // 真机中 select 的默认 value 优先于同名 input 的 value 属性（罕见 but 保真）
    out[id] = selectDefault(opts);
  }
  return out;
}

/**
 * legacy 默认态（与旧桩一致，仅用于对照）：
 * input 只认 `id` 在 `value` 之前、双引号；select 取「selected 在 value 之前」的写法，
 * 否则回退首个 option；textarea 同 .value 口径。
 */
function legacyPageDefaults(html) {
  const out = {};
  for (const m of String(html).matchAll(/<input\b[^>]*>/gi)) {
    const tag = m[0];
    const id = (tag.match(/\bid\s*=\s*["']([^"']+)["']/i) || [, ""])[1];
    if (!id) continue;
    const typ = ((tag.match(/\btype\s*=\s*["']([^"']*)["']/i) || [])[1] || "text").toLowerCase();
    if (/^(checkbox|radio|button|submit|reset|file|image)$/.test(typ)) continue;
    const val = tag.match(/value\s*=\s*["']([^"']*)["']/i);
    if (out[id] === undefined) out[id] = val ? val[1] : "";
  }
  const ta = parseTextareaDefaults(html);
  for (const [id, v] of Object.entries(ta)) if (out[id] === undefined) out[id] = v;
  for (const m of String(html).matchAll(/<select\b[^>]*\bid\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/select>/gi)) {
    const id = m[1];
    if (out[id] !== undefined) continue;
    const inner = m[2];
    const sel = inner.match(/<option[^>]*\bselected\b[^>]*value=["']([^"']*)["']/i)
             || inner.match(/<option[^>]*\bvalue=["']([^"']*)["']/i)
             || inner.match(/<option[^>]*>([\s\S]*?)<\/option>/i);
    out[id] = sel ? (sel[1] || "").replace(/<[^>]+>/g, "").trim() : "";
  }
  return out;
}

module.exports = {
  stubFidelity,
  parseInputDefaults,
  parseTextareaDefaults,
  parseSelects,
  selectDefault,
  parseCheckedIds,
  pageDefaults,
  legacyPageDefaults,
};
