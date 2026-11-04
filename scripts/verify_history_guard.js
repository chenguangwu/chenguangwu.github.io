/**
 * 历史区字段守卫回归：确保 null/undefined/NaN 不会以文本形式渲染进 TBKit.history 区域。
 *
 * 背景：`__sxExtras()` 曾把 `conf: null` 写入历史，`tool-kit.js` 原样拼接后显示 `conf null`。
 * 用例：① 公共组件跳过缺失/非有限值；② 合法的 0 仍保留；③ sentiment-analysis 缺省时省略 conf 键。
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const CASES = [];

CASES.push({
  name: "工具库历史区跳过 null/undefined/NaN",
  run() {
    const dom = new JSDOM('<!doctype html><body><div id="hist"></div></body>', {
      url: "http://localhost/",
      runScripts: "outside-only",
    });
    const win = dom.window;
    win.localStorage.clear();
    win.eval(fs.readFileSync(path.join(ROOT, "js/tool-kit.js"), "utf8"));
    win.TBKit.history.record({ conf: null, score: undefined, prob: NaN, mean: Infinity, ok: 1 });
    const host = win.document.getElementById("hist");
    win.TBKit.history.mount("#hist");
    const text = host.textContent;
    const dirty = /\b(null|undefined|NaN|Infinity)\b/.test(text);
    return { ok: !dirty && text.includes("ok 1"), got: text.trim() };
  },
});

CASES.push({
  name: "工具库历史区保留合法 0",
  run() {
    const dom = new JSDOM('<!doctype html><body><div id="hist"></div></body>', {
      url: "http://localhost/",
      runScripts: "outside-only",
    });
    const win = dom.window;
    win.localStorage.clear();
    win.eval(fs.readFileSync(path.join(ROOT, "js/tool-kit.js"), "utf8"));
    win.TBKit.history.record({ conf: 0, score: 0 });
    const host = win.document.getElementById("hist");
    win.TBKit.history.mount("#hist");
    return { ok: host.textContent.includes("conf 0"), got: host.textContent.trim() };
  },
});

CASES.push({
  name: "sentiment-analysis 缺省时省略 conf 键",
  run() {
    const src = fs.readFileSync(path.join(ROOT, "tools/ai/sentiment-analysis.html"), "utf8");
    const ok = src.includes("if(conf!=null) rec.conf=conf;") && !/history\.record\s*\(\s*\{[^}]*conf\s*:\s*conf/.test(src);
    return { ok, got: ok ? "rec.conf 仅在有值时写入" : "仍可能写入 conf:null" };
  },
});

let pass = 0;
for (const c of CASES) {
  let r;
  try {
    r = c.run();
  } catch (e) {
    r = { ok: false, got: "抛出异常: " + e.message };
  }
  if (r.ok) pass++;
  else console.log(`❌ ${c.name} — ${r.got}`);
}
console.log(`\n==== history field guard ${pass}/${CASES.length} ====`);
process.exit(pass === CASES.length ? 0 : 1);
