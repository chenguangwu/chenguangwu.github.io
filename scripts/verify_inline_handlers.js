/**
 * 内联事件 → 全局函数回归：内联事件属性在全局作用域求值，实现被 IIFE / module 包住即抛 "X is not defined"。
 *
 * 背景：`__charDistUpdate` 曾定义在 IIFE 内、`__*Export` 曾定义在 module 内或名字缺下划线前缀，
 * 内联 `onclick="__xExport()"` 点击即抛 ReferenceError。本用例覆盖：
 * ① 六个已修页真触发内联事件（输入 / 点击）不抛 "is not defined"；
 * ② 全站 `__` 前缀内联处理函数必须在页面内可见（`window.X =` / 顶层 `function X(`）或走共享脚本。
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

const ROOT = path.resolve(__dirname, "..");
const CASES = [];

/** 修复页清单：页面 / 触发方式 / 期望的全局函数名 */
const FIXED = [
  ["tools/astronomy/hubble-redshift-distance.html", "input", "__charDistUpdate"],
  ["tools/legal/calc-16.html", "click", "__c16Export"],
  ["tools/legal/calc-17.html", "click", "__c17Export"],
  ["tools/legal/calc-96.html", "click", "__c96Export"],
  ["tools/legal/calculator-calc-6.html", "click", "__cc6Export"],
  ["tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html", "click", "__jyExport"],
];

/** 这些共享脚本提供的全局函数，允许页面内不出现定义文本 */
const SHARED = {
  __charDistUpdate: /js\/tools\/char-distance-ref\.js/,
};

CASES.push({
  name: "已修页触发内联事件不抛 is not defined",
  run() {
    const failed = [];
    for (const [rel, action, name] of FIXED) {
      const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
      const vc = new VirtualConsole();
      const errs = [];
      vc.on("jsdomError", e => errs.push(e.message + (e.detail ? " :: " + e.detail.message : "")));
      // 共享脚本与 common.js 里由外链提供、jsdom 不加载的依赖：按需内联或打桩
      let doc = html;
      if (SHARED[name]) {
        const sharedSrc = fs.readFileSync(path.join(ROOT, "js/tools/char-distance-ref.js"), "utf8");
        doc = doc.replace("</body>", `<script>${sharedSrc}</script></body>`);
      }
      const dom = new JSDOM(doc, {
        url: "http://localhost/" + rel,
        runScripts: "dangerously",
        virtualConsole: vc,
        pretendToBeVisual: true,
        beforeParse(win) {
          win.ToolBox = { setResult() {}, toggleToolTheme() {}, copy() {}, toast() {} };
        },
      });
      const win = dom.window;
      win.addEventListener("error", e => errs.push(String(e.message || "")));
      const g = typeof win[name];

      if (action === "input") {
        const el = win.document.getElementById("__charDistVal");
        if (el) {
          el.value = "2500";
          el.dispatchEvent(new win.Event("input", { bubbles: true }));
        }
      } else {
        win.document.querySelectorAll("[onclick]").forEach(b => {
          if (/__\w*Export\s*\(/.test(b.getAttribute("onclick") || "")) {
            try { b.click(); } catch (e) { errs.push(e.message); }
          }
        });
      }

      const ref = errs.filter(m => /is not defined/.test(m));
      if (g !== "function" || ref.length) {
        failed.push(`${rel} global=${g} ${ref.join(" ;; ") || ""}`.trim());
      }
    }
    return { ok: failed.length === 0, got: failed.length ? failed.join(" | ") : "6/6 页面触发无 ReferenceError" };
  },
});

CASES.push({
  name: "全站 __ 前缀内联处理函数均可全局解析",
  run() {
    const files = [];
    (function walk(dir) {
      for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, e.name);
        if (e.isDirectory()) walk(p);
        else if (e.name.endsWith(".html")) files.push(p);
      }
    })(path.join(ROOT, "tools"));

    const missing = [];
    for (const f of files) {
      const html = fs.readFileSync(f, "utf8");
      const cleaned = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ");
      for (const m of cleaned.matchAll(/\b(on\w+)\s*=\s*("[^"]*"|'[^']*')/gi)) {
        for (const nm of m[2].slice(1, -1).matchAll(/(__[A-Za-z0-9_]+)\s*\(/g)) {
          const n = nm[1];
          if (SHARED[n] && SHARED[n].test(html)) continue;
          const visible = new RegExp(`window\\.${n}\\s*=|function\\s+${n}\\s*\\(`).test(html);
          if (!visible) missing.push(`${path.relative(ROOT, f)} | ${n}`);
        }
      }
    }
    return {
      ok: missing.length === 0,
      got: missing.length ? `缺定义 ${missing.length} 处: ${missing.slice(0, 5).join(" | ")}` : `${files.length} 页全部命中`,
    };
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
console.log(`\n==== inline handler global ${pass}/${CASES.length} ====`);
process.exit(pass === CASES.length ? 0 : 1);
