/**
 * 历史区字段守卫回归：确保 null/undefined/NaN 不会以文本形式渲染进 TBKit.history 区域。
 *
 * 背景：`__sxExtras()` 曾把 `conf: null` 写入历史，`tool-kit.js` 原样拼接后显示 `conf null`。
 * 用例：① 公共组件跳过缺失/非有限值；② 合法的 0 仍保留。
 */
"use strict";
const fs = require("fs");
const path = require("path");

// jsdom 只在动态用例里用；CI 未装依赖时不能让整条门禁在 require 阶段直接崩（假红）。
// 缺依赖 → 动态用例显式 SKIP(no-browser)，静态用例照常判红/绿。
let JSDOM = null;
let JSDOM_ERR = "";
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  JSDOM_ERR = e.message;
}

const ROOT = path.resolve(__dirname, "..");
const CASES = [];

CASES.push({
  name: "工具库历史区跳过 null/undefined/NaN",
  run() {
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
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
    if (!JSDOM) return { skip: true, got: "jsdom 不可用: " + JSDOM_ERR };
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

let pass = 0;
let fail = 0;
let skipped = 0;
for (const c of CASES) {
  let r;
  try {
    r = c.run();
  } catch (e) {
    r = { ok: false, got: "抛出异常: " + e.message };
  }
  if (r.skip) {
    if (process.env.TB_REQUIRE_DYNAMIC === "1") {
      fail++;
      console.log(`❌ ${c.name} — TB_REQUIRE_DYNAMIC=1 但动态段被跳过：${r.got}`);
    } else {
      skipped++;
      console.log(`⚠️ SKIP(no-browser): ${c.name} — ${r.got}`);
    }
  } else if (r.ok) {
    pass++;
  } else {
    fail++;
    console.log(`❌ ${c.name} — ${r.got}`);
  }
}
console.log(`\n==== history field guard ${pass} passed / ${fail} failed / ${skipped} skipped ====`);
if (fail > 0) process.exit(1);
// 防空跑假绿：没有任何用例真正执行（全部跳过且无失败）时不能判绿
if (pass === 0) {
  console.log("❌ 0 个用例实际执行（全部跳过），拒绝判绿");
  process.exit(1);
}
process.exit(0);
