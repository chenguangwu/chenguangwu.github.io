#!/usr/bin/env node
/**
 * 动态表单默认值解析（判别器专用，只读）。
 *
 * 背景：不少工具页的表单控件不是静态 HTML，而是页面 JS 在加载时拼 innerHTML 生成的
 * （`id="pt'+i+'"`、`id="q${i}"`、`id="m'+mi+'_'+ii+'"`、`id="'+d.key+'"` …）。
 * `discriminate_check.js` 的 pageDefaults 只解析静态标签，于是这些页的注入键一律
 * 判「unresolved ⇒ 跳过」，既无法模拟「注入失败」，也把真正该判别的用例漏掉了。
 *
 * 做法（不写第二套 JS 解释器）：定位生成语句所在的渲染函数，在受控沙箱里**执行页面
 * 自己的渲染函数**（只提供 document/全局变量桩，不加载外部脚本、不触碰网络），
 * 采集它写出的 innerHTML，再从生成结果里读出真实 `id → value` 默认值。
 * 这样循环上界、数据数组、条件表达式都由页面自己算，天然与真机一致。
 *
 * 安全边界：
 *   - 只执行「含动态 id 模板」的函数，最多 25 个，逐个 try/catch；
 *   - document 为纯内存桩，无网络/存储/定时器；
 *   - 静态 HTML 里不存在的「动态前缀 id」返回 null（与真机一致，防止页面读 prev 值时
 *     把空串当成已录入值、覆盖掉数据数组默认值）；
 *   - 任一环节抛错即返回空映射，调用方维持原有的 unresolved 跳过口径。
 *
 * 与 audit_verify_input_ids.js 的关系：该脚本的 classify() 复用本模块的
 * `isDynamicId()` 判定「运行期生成」，避免两处各自维护一套正则。
 */
"use strict";

const SCRIPT_RE = /<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
const SCRIPT_BLOCK_RE = /<script\b[\s\S]*?<\/script>|<style\b[\s\S]*?<\/style>/gi;

/** 所有内联脚本拼接 */
function scriptsText(html) {
  let s = "";
  for (const m of String(html).matchAll(SCRIPT_RE)) s += "\n" + m[1] + "\n";
  return s;
}

/** 静态标记里的 id 集合（排除 script/style 块，避免把动态模板当成静态 id） */
function staticIds(html) {
  const out = new Set();
  const markup = String(html).replace(SCRIPT_BLOCK_RE, " ");
  for (const m of markup.matchAll(/\bid\s*=\s*["']([^"']+)["']/g)) out.add(m[1]);
  return out;
}

/** 按字符扫描脚本：跳过字符串与注释，回调 depth（花括号层数）与位置 */
function walkTopLevel(scripts, onToken) {
  let depth = 0, q = null;
  for (let i = 0; i < scripts.length; i++) {
    const ch = scripts[i];
    if (q) {
      if (ch === "\\") { i++; continue; }
      if (ch === q) q = null;
      continue;
    }
    if (ch === "/" && scripts[i + 1] === "/") { while (i < scripts.length && scripts[i] !== "\n") i++; continue; }
    if (ch === "/" && scripts[i + 1] === "*") { i += 2; while (i < scripts.length && !(scripts[i] === "*" && scripts[i + 1] === "/")) i++; i++; continue; }
    if (ch === "'" || ch === '"' || ch === "`") { q = ch; continue; }
    if (ch === "{") depth++;
    else if (ch === "}") depth--;
    else if (depth === 0) onToken(i, ch);
  }
}

/** 从 start 起截取「顶层」声明初始化式（到 depth=0 的 ; 或换行；数组/对象跨行不算结束） */
function takeInitializer(scripts, start) {
  let i = start, depth = 0, q = null;
  for (; i < scripts.length; i++) {
    const ch = scripts[i];
    if (q) {
      if (ch === "\\") { i++; continue; }
      if (ch === q) q = null;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === "`") { q = ch; continue; }
    if (ch === "(" || ch === "[" || ch === "{") depth++;
    else if (ch === ")" || ch === "]" || ch === "}") {
      depth--;
      if (depth < 0) return { text: scripts.slice(start, i), end: i };
    } else if (ch === ";" && depth === 0) return { text: scripts.slice(start, i), end: i };
    else if (ch === "\n" && depth === 0) return { text: scripts.slice(start, i), end: i };
  }
  return { text: scripts.slice(start, i), end: i };
}

function safeEval(expr, env) {
  try {
    const names = Object.keys(env).filter((n) => /^[A-Za-z_$][\w$]*$/.test(n));
    return new Function(...names, '"use strict";return (' + expr + ")")(...names.map((n) => env[n]));
  } catch (e) {
    return undefined;
  }
}

/** <select id=…> 的默认选中值（带 selected 的选项，否则首个选项） */
function selectDefaults(html) {
  const out = {};
  const re = /<select\b[^>]*\bid="([^"]+)"[^>]*>([\s\S]*?)<\/select>/gi;
  for (const m of String(html).matchAll(re)) {
    const opts = [...m[2].matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/gi)];
    if (!opts.length) continue;
    const pick = opts.find((o) => /\bselected\b/.test(o[1])) || opts[0];
    const vm = pick[1].match(/\bvalue="([^"]*)"/i);
    out[m[1]] = vm ? vm[1] : pick[2].trim();
  }
  return out;
}

/**
 * 顶层 var/let/const 的初始化式（多行数组/对象一并捕获；函数内声明忽略）。
 * `document.getElementById('size').value` 用 select 默认值代入。
 */
function globalEnv(scripts, selects) {
  const env = {};
  const found = [];
  walkTopLevel(scripts, (i) => {
    const m = /^(?:var|let|const)\b/.exec(scripts.slice(i, i + 8));
    if (!m) return;
    const nm = /^([A-Za-z_$][\w$]*)\s*=\s*/.exec(scripts.slice(i + m[0].length, i + m[0].length + 80).replace(/^\s+/, ""));
    if (!nm) return;
    const eqAt = scripts.indexOf("=", i);
    if (eqAt < 0) return;
    const init = takeInitializer(scripts, eqAt + 1);
    found.push({ name: nm[1], expr: init.text.trim() });
  });
  for (const f of found) {
    let expr = f.expr;
    expr = expr.replace(/document\.getElementById\(['"]([^'"]+)['"]\)\.value/g, (_, id) =>
      JSON.stringify(selects[id] !== undefined ? selects[id] : "")
    );
    const v = safeEval(expr, env);
    if (v !== undefined) env[f.name] = v;
  }
  return env;
}

/** 所有「顶层 function name(...) {…}」的源码（供渲染函数调用同页 helper） */
function topLevelFunctions(scripts) {
  const out = [];
  const re = /^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/;
  walkTopLevel(scripts, (i) => {
    const m = re.exec(scripts.slice(i, i + 60));
    if (!m) return;
    const braceAt = scripts.indexOf("{", i);
    if (braceAt < 0) return;
    let depth = 0, q = null, end = -1;
    for (let j = braceAt; j < scripts.length; j++) {
      const ch = scripts[j];
      if (q) {
        if (ch === "\\") { j++; continue; }
        if (ch === q) q = null;
        continue;
      }
      if (ch === "'" || ch === '"' || ch === "`") { q = ch; continue; }
      if (ch === "{") depth++;
      else if (ch === "}") {
        depth--;
        if (depth === 0) { end = j + 1; break; }
      }
    }
    if (end > 0) out.push({ name: m[1], src: scripts.slice(i, end) });
  });
  return out;
}

/**
 * 找出所有「动态 id 模板」出现位置：脚本里 `id="…"` 且内容含 `' +` / `+ '` / `${`。
 * 返回 [{ pos, inner, prefix }]；prefix 为模板里第一个动态拼接之前的字面量前缀。
 */
function findDynamicTemplates(html) {
  const scripts = scriptsText(html);
  const out = [];
  for (const m of scripts.matchAll(/\bid\s*=\s*(["'`])([\s\S]*?)\1/g)) {
    const inner = m[2];
    if (!/\$\{/.test(inner) && !/\s*\+\s*/.test(inner)) continue;
    const prefix = (inner.match(/^([A-Za-z_][A-Za-z0-9_-]*)/) || ["", ""])[1];
    out.push({ pos: m.index, inner, prefix });
  }
  return out;
}

/** 动态 id 前缀集合（供 audit_verify_input_ids 共用，不再维护第二套正则） */
function dynamicPrefixes(html) {
  const res = { prefixes: [], open: false };
  for (const t of findDynamicTemplates(html)) {
    if (t.prefix) res.prefixes.push(t.prefix);
    else res.open = true;   // 模板整体由变量拼成（id="'+d.key+'"）⇒ 任意 id 都可能
  }
  return res;
}

/** 该 id 是否由脚本运行期生成（audit_verify_input_ids 的二档判据） */
function isDynamicId(html, id) {
  const p = dynamicPrefixes(html);
  if (p.open) return true;
  return p.prefixes.some((pre) => id.startsWith(pre) && id.length > pre.length);
}

/** 从 pos 向前找最近的 `function name(`，返回函数源码（花括号配平） */
function functionAround(scripts, pos) {
  const head = scripts.slice(0, pos);
  const m = /function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{/g;
  let last = null;
  for (const hit of head.matchAll(m)) last = hit;
  if (!last) return null;
  const start = last.index;
  const braceStart = start + last[0].length - 1;
  let depth = 0, q = null;
  for (let i = braceStart; i < scripts.length; i++) {
    const ch = scripts[i];
    if (q) {
      if (ch === "\\") { i++; continue; }
      if (ch === q) q = null;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === "`") { q = ch; continue; }
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        const name = last[1];
        // 包一层：模板若位于 setAttribute / 事件回调里也能拿到外层函数
        return { name, src: scripts.slice(start, i + 1) };
      }
    }
  }
  return null;
}

/** 受控 document 桩：静态不存在的动态前缀 id 返回 null（与真机一致） */
function makeDoc(selects, captured, known, dynamicPrefixSet) {
  const els = {};
  const created = {};
  function isDynamicIdLocal(id) {
    for (const p of dynamicPrefixSet) if (id.startsWith(p) && id.length > p.length) return true;
    return false;
  }
  function makeEl(id) {
    if (els[id]) return els[id];
    let html = "";
    const el = {
      id,
      value: selects[id] !== undefined ? String(selects[id]) : "",
      textContent: "",
      style: {},
      dataset: {},
      children: [],
      options: [],
      parentElement: null,
      selectedIndex: 0,
      classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
      addEventListener() {}, removeEventListener() {},
      insertAdjacentHTML() {}, insertBefore() {}, appendChild() {}, removeChild() {},
      setAttribute() {}, getAttribute() { return null; }, removeAttribute() {},
      querySelector() { return null; }, querySelectorAll() { return []; },
      add() {}, cloneNode() { return makeEl(""); }, focus() {}, select() {},
      getElementsByTagName() { return []; },
    };
    Object.defineProperty(el, "textContent", {
      configurable: true,
      get() { return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim(); },
      set(v) { html = String(v); },
    });
    Object.defineProperty(el, "innerHTML", {
      configurable: true,
      get() { return html; },
      set(v) {
        html = String(v == null ? "" : v);
        captured.push(html);
        // 登记生成出来的控件，供同一函数后续 getElementById 读回（真机语义）
        for (const m of html.matchAll(/<(?:input|textarea)\b([^>]*)>/gi)) {
          const idm = m[1].match(/\bid="([^"]+)"/i);
          if (!idm) continue;
          const vm = m[1].match(/\bvalue="([^"]*)"/i);
          created[idm[1]] = vm ? vm[1] : "";
        }
      },
    });
    els[id] = el;
    return el;
  }
  return {
    getElementById: (id) => {
      id = String(id);
      if (created[id] !== undefined) {
        const e = makeEl(id);
        e.value = created[id];
        return e;
      }
      if (known.has(id) || !isDynamicIdLocal(id)) return makeEl(id);
      return null;   // 真机上尚不存在的动态控件
    },
    querySelector: () => null,
    querySelectorAll: () => [],
    getElementsByClassName: () => [],
    getElementsByTagName: () => [],
    addEventListener() {},
  };
}

/** 执行一个渲染函数，返回它写出的全部 innerHTML 文本 */
function runGenerator(fnSrc, fnName, env, selects, helpers, known, prefixes) {
  // prefixes：动态 id 的静态前缀集合；未知但带这些前缀的 id 视为「真机上尚不存在」⇒ 返回 null
  const captured = [];
  const doc = makeDoc(selects, captured, known, prefixes);
  const names = Object.keys(env).filter((n) => /^[A-Za-z_$][\w$]*$/.test(n) && !helpers.some((h) => h.name === n));
  try {
    // 末尾显式返回函数名，否则 new Function 里只有声明、拿不到引用
    const body = helpers.map((h) => h.src).join("\n") + "\n" + fnSrc + "\nreturn " + fnName + ";\n//# sourceURL=tb-dyn-defaults.js";
    const fn = new Function("document", ...names, body)(doc, ...names.map((n) => env[n]));
    if (typeof fn === "function") fn();
  } catch (e) {
    return null;
  }
  return captured.join("\n");
}

/** 从生成的 HTML 里抽 <input>/<textarea>/<select> 的 id → value */
function parseControls(html) {
  const out = {};
  for (const m of String(html).matchAll(/<(?:input|textarea)\b([^>]*)>/gi)) {
    const a = m[1];
    const id = a.match(/\bid="([^"]+)"/i);
    if (!id) continue;
    const val = a.match(/\bvalue="([^"]*)"/i);
    out[id[1]] = val ? val[1] : "";
  }
  for (const m of String(html).matchAll(/<select\b([^>]*)>([\s\S]*?)<\/select>/gi)) {
    const a = m[1];
    const id = a.match(/\bid="([^"]+)"/i);
    if (!id) continue;
    const opts = [...m[2].matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/gi)];
    const pick = opts.find((o) => /\bselected\b/.test(o[1])) || opts[0];
    if (!pick) { out[id[1]] = ""; continue; }
    const vm = pick[1].match(/\bvalue="([^"]*)"/i);
    out[id[1]] = vm ? vm[1] : pick[2].trim();
  }
  return out;
}

/**
 * 解析页面动态生成控件的默认值。
 * @param {string} html 页面源码
 * @param {string[]} [wanted] 只关心这些 id（缺省则返回全部解析结果）
 * @returns {Record<string,string>}
 */
function dynamicDefaults(html, wanted) {
  const scripts = scriptsText(html);
  const selects = selectDefaults(html);
  const templates = findDynamicTemplates(html);
  if (!templates.length) return {};
  const fns = [];
  for (const t of templates) {
    const fn = functionAround(scripts, t.pos);
    if (fn && !fns.some((f) => f.name === fn.name)) fns.push(fn);
    if (fns.length >= 25) break;
  }
  if (!fns.length) return {};
  const helpers = topLevelFunctions(scripts);
  const known = staticIds(html);
  const prefixes = new Set(templates.map((t) => t.prefix).filter(Boolean));
  const env = globalEnv(scripts, selects);
  const out = {};
  for (const fn of fns) {
    const gen = runGenerator(fn.src, fn.name, env, selects, helpers, known, prefixes);
    if (!gen) continue;
    Object.assign(out, parseControls(gen));
  }
  if (!Array.isArray(wanted) || !wanted.length) return out;
  const picked = {};
  for (const k of wanted) if (out[k] !== undefined) picked[k] = out[k];
  return picked;
}

module.exports = {
  dynamicDefaults,
  findDynamicTemplates,
  dynamicPrefixes,
  isDynamicId,
  staticIds,
  selectDefaults,
  scriptsText,
  functionAround,
  globalEnv,
  topLevelFunctions,
  runGenerator,
};
