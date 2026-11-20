#!/usr/bin/env node
/**
 * 全站运行时冒烟扫描：随机抽工具页，逐页加载并记录
 *  - 未捕获异常 / console.error（含资源 404）
 *  - 页面是否存在「空白 body」「无任何 input/select」等结构性死壳
 *  - 结果区首屏是否为空
 *
 * 用途：把 verify 用例覆盖不到的运行时错误捞出来（verify 只跑有断言的计算路径）。
 *
 * 用法：
 *   python3 -m http.server 8137 --directory . &
 *   node scripts/smoke_scan.mjs --sample 80 --out /tmp/smoke.json
 *   node scripts/smoke_scan.mjs --urls /tmp/urls.txt
 */
import fs from "node:fs";
import puppeteer from "puppeteer-core";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const argv = process.argv.slice(2);
const getArg = (k, d) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const SAMPLE = Number(getArg("--sample", "60"));
const BASE = getArg("--base", "http://127.0.0.1:8137");
const OUT = getArg("--out", "");
const URLS = getArg("--urls", "");
const CLICK = argv.includes("--click");
const SEED = Number(getArg("--seed", "20261120"));

function pick(n) {
  if (URLS) return fs.readFileSync(URLS, "utf8").split("\n").filter(Boolean);
  const tools = JSON.parse(fs.readFileSync("json/tools.json", "utf8"));
  const all = tools.map((t) => "/" + String(t.url).replace(/^\/+/, "")).filter((u) => u.endsWith(".html"));
  let s = SEED;
  const rnd = () => ((s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
  const c = all.slice(); const out = [];
  for (let i = 0; i < n && c.length; i++) out.push(c.splice(Math.floor(rnd() * c.length), 1)[0]);
  return out;
}

(async () => {
  const pages = pick(SAMPLE);
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
  });
  const rows = [];
  // 复用同一个标签页（每页建独立 context 在长时间扫描中会触发 CDP session 失效）；
  // 冒烟只关心本页加载期错误，复用页不影响判断，切页时清空监听数组即可。
  const page = await browser.newPage();
  await page.setCacheEnabled(false);
  for (const u of pages) {
    const errs = [];
    const onErr = (e) => errs.push("pageerror: " + String(e).slice(0, 160));
    const onCon = (m) => {
      if (m.type() !== "error") return;
      const t = m.text();
      // 浏览器/第三方统计的已知策略噪音：非页面缺陷，过滤掉以免淹没真实错误
      if (/Permissions policy violation: unload/i.test(t)) return;
      if (/clarity\.ms|clarity-js/i.test(t)) return;
      errs.push("console: " + t.slice(0, 160));
    };
    const onFail = (r) => errs.push("reqfail: " + r.url().split("/").pop() + " " + (r.failure() || {}).errorText);
    page.on("pageerror", onErr); page.on("console", onCon); page.on("requestfailed", onFail);
    let info = {};
    try {
      await page.goto(BASE + u, { waitUntil: "load", timeout: 20000 });
      await new Promise((r) => setTimeout(r, 350));
      info = await page.evaluate(() => {
        const r = document.querySelector(".result-box") || document.querySelector("#result");
        return {
          bodyLen: (document.body ? document.body.innerText : "").trim().length,
          controls: document.querySelectorAll("input,select,textarea").length,
          resultLen: r ? (r.innerText || "").replace(/\s+/g, " ").trim().length : 0
        };
      });
      if (CLICK) {
        info.before = info.resultLen;
        await page.evaluate(() => {
          const b = document.querySelector("button.btn.primary, button.primary, .btn.primary") ||
                    document.querySelector("button[onclick*='calc'], button[onclick*='generate'], button[onclick*='Generate']");
          if (b) b.click();
        });
        await new Promise((r) => setTimeout(r, 250));
        info.after = await page.evaluate(() => {
          const r = document.querySelector(".result-box") || document.querySelector("#result");
          return r ? (r.innerText || "").replace(/\s+/g, " ").trim().length : 0;
        });
      }
    } catch (e) {
      errs.push("goto: " + String(e).slice(0, 120));
    }
    rows.push({ url: u, ...info, errors: errs });
    page.off("pageerror", onErr); page.off("console", onCon); page.off("requestfailed", onFail);
  }
  await browser.close();

  const bad = rows.filter((r) => r.errors.length || r.bodyLen < 50 || (r.controls === 0 && r.resultLen === 0));
  console.log(`扫描 ${rows.length} 页，问题 ${bad.length} 页`);
  for (const b of bad) {
    console.log(`- ${b.url} | body=${b.bodyLen} controls=${b.controls} result=${b.resultLen} | ${b.errors.join(" ;; ") || "结构性空页"}`);
  }
  if (OUT) fs.writeFileSync(OUT, JSON.stringify(rows, null, 2));
})();
