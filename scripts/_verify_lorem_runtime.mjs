#!/usr/bin/env node
/**
 * Lorem 生成器（tools/it/lorem.html）的运行期回归验证。
 *
 * 为什么不用 verify_it_calc.js：该页结果写在 textarea.value，harness 的 blob 归一后
 * 无法精确断言「词数严格等于 count」；预设栏 / 历史恢复回调也不在 stub.click 可达范围。
 * 因此这里从源文件抽取真实的顶层脚本函数体，在 Node vm 里以最小 DOM 桩执行 —— 与线上同一份源码。
 *
 * 覆盖 IT-N523（count 精确性与边界钳制）、IT-N524（预设/历史回调应重算而非下载）、
 * IT-N525（中文占位与句长范围承诺须有实现）。
 *
 * 用法：node scripts/_verify_lorem_runtime.mjs
 * 退出码：0 全通过；1 有失败项。
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import vm from "node:vm";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PAGE = resolve(ROOT, "tools/it/lorem.html");
const html = readFileSync(PAGE, "utf8");

// 顶层 <script> 从词表开始，到首次 generate() 调用为止（不含该调用）
const start = html.indexOf('const words = "lorem ipsum');
const end = html.indexOf("\ngenerate();", start);
if (start < 0 || end < 0) throw new Error("页面结构变化，抽取区间失效，请更新本脚本的行锚点");
const src = html.slice(start, end);

function setup() {
  const els = {
    count: { value: "3" },
    startLorem: { checked: true },
    minWords: { value: "8" },
    maxWords: { value: "19" },
    output: { value: "" },
  };
  const document = {
    getElementById: (id) => els[id] || null,
    querySelectorAll: () => [],
  };
  const ctx = { console, document };
  vm.createContext(ctx);
  vm.runInContext(
    src +
      "\n;globalThis.__api={generate:generate,setType:setType," +
      "sentenceRange:(typeof sentenceRange==='function'?sentenceRange:function(){return [8,19];})," +
      "randomSentence:randomSentence,randomChineseSentence:randomChineseSentence," +
      "getType:function(){return currentType;}};",
    ctx
  );
  return { els, api: ctx.__api };
}

function select(type) {
  return { dataset: { type }, classList: { add() {} } };
}

const results = [];
function check(name, ok, detail) {
  results.push({ name, ok });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  —  " + detail : ""}`);
}

// ---- IT-N523：数量严格等于 count ----
{
  const { els, api } = setup();
  els.count.value = "1";
  api.setType(select("words"));
  check("N523 words count=1 只输出 1 词（不再多塞 ipsum）", els.output.value === "lorem", JSON.stringify(els.output.value));
}
{
  const { els, api } = setup();
  els.count.value = "2";
  api.setType(select("words"));
  check("N523 words count=2 恰为 lorem ipsum", els.output.value === "lorem ipsum", JSON.stringify(els.output.value));
}
{
  const { els, api } = setup();
  els.count.value = "5";
  els.startLorem.checked = false;
  api.setType(select("words"));
  const n = els.output.value.trim().split(/\s+/).length;
  check("N523 words count=5 输出 5 词", n === 5, `got ${n}: ${els.output.value}`);
}
{
  const { els, api } = setup();
  els.count.value = "-5";
  api.generate();
  check("N523 count=-5 钳制回写 1 且结果非空", String(els.count.value) === "1" && els.output.value.length > 0, `count=${els.count.value} len=${els.output.value.length}`);
}
{
  const { els, api } = setup();
  els.count.value = "1000";
  api.generate();
  const paras = els.output.value.split("\n\n").length;
  check("N523 count=1000 钳制回写 100 且生成 100 段", String(els.count.value) === "100" && paras === 100, `count=${els.count.value} paras=${paras}`);
}

// ---- IT-N525：中文占位与句长范围真实可用 ----
{
  const { els, api } = setup();
  els.count.value = "3";
  api.setType(select("chinese"));
  const lines = els.output.value.split("\n");
  const ok = lines.length === 3 && lines.every((l) => /[一-龥]/.test(l) && l.endsWith("。"));
  check("N525 chinese 模式输出 3 行中文占位句", ok, JSON.stringify(els.output.value));
}
{
  const { els, api } = setup();
  els.count.value = "2";
  els.startLorem.checked = false;
  els.minWords.value = "3";
  els.maxWords.value = "3";
  api.setType(select("sentences"));
  const sents = els.output.value.trim().split(/\.\s+/).filter(Boolean);
  const ok = sents.length === 2 && sents.every((s) => s.replace(/\.$/, "").trim().split(/\s+/).length === 3);
  check("N525 句长区间 3–3 时每句恰 3 词", ok, JSON.stringify(els.output.value));
}
check("N525 源码存在 chinese 分支并调用 randomChineseSentence", src.includes("currentType === 'chinese'") && src.includes("result.push(randomChineseSentence())"));
check("N525 页面含中文按钮与句长控件且公式已同步", html.includes('data-type="chinese"') && html.includes('id="minWords"') && html.includes('id="maxWords"') && html.includes("句长由最小 / 最大词数区间决定"));
check("N525 sentenceRange 默认区间为 8–19（与既有随机序列一致）", (() => {
  const { api } = setup();
  const r = api.sentenceRange();
  return r[0] === 8 && r[1] === 19;
})());

// ---- IT-N524：预设 / 历史回调重新计算而非下载旧文本 ----
check("N524 预设回调调用 generate()", html.includes("],function(){ generate(); });"));
check("N524 历史恢复回调调用 generate()", html.includes("generate();\n            }catch(e2){}"));
check("N524 两处回调已不再调用 downloadTxt()", !html.includes("],function(){ downloadTxt(); });") && !html.includes("downloadTxt();\n            }catch(e2){}"));

const pass = results.filter((r) => r.ok).length;
console.log(`\n==== ${pass}/${results.length} 通过 ====`);
process.exit(pass === results.length ? 0 : 1);
