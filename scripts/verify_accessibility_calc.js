#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "accessibility/braille-translator",
  "inputs": {"srcInput": ""},
  "clicks": ["doTranslate()"],
  "expect": ["请输入文本后再转译。"],
  "ref": "空输入守卫：清空 srcInput 后点转译，必须给输入提示，不得输出「原文：（空）字母 0 个 · 数字 0 个 · 盲文符号 0 格」的伪统计；默认 hello 2026 不含该提示。"
},
{
  "slug": "accessibility/braille-translator",
  "inputs": {
    "srcInput": "ab",
    "caseSel": "upper"
  },
  "expect": [
    "⠠⠁⠠⠃",
    "原文： AB 字母 2 个 · 数字 0 个 · 盲文符号 4 格"
  ],
  "ref": "盲文翻译：注入 ab + caseSel=upper ⇒ 全部大写模式对每个字母加大写符 ⠠（点6），输出 ⠠⠁⠠⠃，统计 4 格。旧用例期望 ⠁⠃/2 格，正是「全部大写遗漏大写符」的回归锚点，已按修复后语义更新。默认态 hello 2026 不含该串。"
},
{
  "slug": "accessibility/braille-translator",
  "inputs": {"srcInput": "1a"},
  "expect": ["⠼⠁⠰⠁", "4 格"],
  "ref": "数字后接字母边界：1a ⇒ 数字符 ⠼ + 数字 1 的 ⠁ + 字母符 ⠰（点5,6）+ 字母 a 的 ⠁ = ⠼⠁⠰⠁，共 4 格。若不加字母符，第二个 ⠁ 会被误读为数字 1；默认 hello 2026 不含字母符。"
},
{
  "slug": "accessibility/braille-translator",
  "inputs": {"srcInput": "中文"},
  "expect": ["未支持字符", "「中」"],
  "ref": "未支持字符显式提示：输入中文「中文」⇒ 只做拉丁字母/数字/空格映射，结果区列出未支持字符「中」「文」，不把汉字原样混进盲文串。默认 hello 2026 不含该提示。"
},
{
  "slug": "accessibility/braille-translator",
  "inputs": {"srcInput": "A", "caseSel": "keep"},
  "expect": ["⠠⠁"],
  "ref": "保留原样模式：大写 A ⇒ 大写符 ⠠ + a 的 ⠁；小写 a 不应带大写符。与 upper 模式用例共同覆盖三种大小写模式。"
},
{
  "slug": "accessibility/braille-translator",
  "inputs": {
    "srcInput": "12"
  },
  "expect": [
    "⠼⠁⠃",
    "原文： 12 字母 0 个 · 数字 2 个 · 盲文符号 3 格"
  ],
  "ref": "数字点位回归：1→a=⠁、2→b=⠃（不是 c 的 ⠉），数字前加数字符 ⠼ ⇒ ⠼⠁⠃、3 格。深度解析原写「2→⠉」与代码/FAQ 矛盾，已改「2→⠃」。"
},
{
  "slug": "accessibility/sign-language",
  "inputs": {
    "searchInput": "zzzqx"
  },
  "expect": [
    "未找到匹配词汇"
  ],
  "ref": "关键词过滤型：inputs 写 searchInput=zzzqx ⇒ oninput=render() 过滤 43 条词汇得空集 ⇒ 「未找到匹配词汇」。默认态渲染全量 43 条、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "accessibility/voice-synthesis",
  "inputs": {
    "rate": "1",
    "pitch": "1",
    "vol": "1",
    "text": "abcde",
    "langFilter": "zh"
  },
  "expect": [
    "5 字"
  ],
  "ref": "语音合成：harness 无 speechSynthesis ⇒ supported=false ⇒ loadVoices() 首行即 return，音色列表永远为空、无从锚定；唯一不依赖该分支的派生量是 updateCharCount() 写入的 #charCount（注入 abcde ⇒ 5 字，默认 23 字）。旧锚 expect [\"zh\"] 是 langFilter 输入值回显、零判别力，已替换。"
},
{
  clicks: ["calc()"],
  "slug": "accessibility/ramp-slope",
  "inputs": { "height": "90", "ratio": "10", "sceneSel": "resident" },
  "expect": ["10.80 水平长度(m)", "该坡度下单段最大高差为 75cm"],
  "ref": "注入 height=90（默认 40）+ sceneSel=resident（默认 general）。⚠ ratio 的注入被页面的场景联动覆盖回 1:12（选场景会写回标准坡度比），这是真机 onchange 行为 ⇒ 水平长度按 1:12 算：L = 90×12 = 1080 cm = 10.80 m；斜长 = √(1080²+90²) = 10.84 m；坡度 8.33%（4.76°）。居住区场景单段限高 75 cm ⇒ 90 cm 超限，输出「需设休息平台分段」提示。默认态（40 cm / general）为 4.80 m 且达标无提示，两串均不出现。⚠ 该页原「初始化失败」：页面用 document.createElementNS 建 SVG 示意图，harness 未建模该 API ⇒ 整页不可验证；已补 createElementNS 桩（返回与 createElement 同构节点）。"
},
{
  "slug": "accessibility/ramp-slope",
  "clicks": ["document.getElementById('sceneSel').value='general';document.getElementById('height').value='200';document.getElementById('ratio').value='50';calc();var h=String(document.getElementById('tipBox').innerHTML);var ok=h.indexOf('建议设 1 处休息平台')>=0&&h.indexOf('单段最大高差为 120cm')>=0;document.getElementById('__tbProbe').textContent='RAMP50 '+(ok?'OK':'BAD '+h);"],
  "expect": ["RAMP50 OK"],
  "ref": "第1092批 J2：H=200cm、1:50 → 单段最大高差 120cm 超限，水平 100m；每段水平上限=120×50÷100=60m，平台数=ceil(100/60)−1=1。旧版平台数仅在 X∈[10,20) 计算，X=50 恒为 0 ⇒ 无平台建议，哨兵变红。clicks 里先定场景再覆写 ratio，避免 onScene 联动覆盖。"
},
{
  "slug": "accessibility/ramp-slope",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/accessibility/ramp-slope.html','utf8');var ok=h.indexOf('var allowedRun = specMaxH > 0 ? (specMaxH * X / 100) : 0;')>=0&&h.indexOf('msg = needPlatform')>=0&&h.indexOf('每段坡道水平长度超过 9m 或高差超过 0.75m')<0&&h.indexOf('1:20 为 24m')>=0;document.getElementById('__tbProbe').textContent='RAMPFIX '+(ok?'OK':'BAD');"],
  "expect": ["RAMPFIX OK"],
  "ref": "第1092批 J2 源码形态：needPlatform 必须进入提示分支（旧版算后从未使用）；平台上限按坡度×单段高差统一（1:20=24m），旧「超过9m一律设平台」与按 X 分段的两套口径均须消失。"
},
{
  "slug": "accessibility/sign-language",
  "inputs": {"searchInput":"mom"},
  "expect": ["Mother","Little finger out","Terms of address"],
  "ref": "第830批：英文检索需匹配英文词/别名并渲染英文卡片。mom 命中「妈妈」的 enAlias；卡片输出 Mother、英文动作说明与 Terms of address。中文态默认 43 条不含该组串，零逃生。"
},
{
  "slug": "accessibility/sign-language",
  "clicks": ["applySignPreset('greet');var a=document.getElementById('searchInput').value;applySignPreset('family');var b=document.getElementById('searchInput').value;applySignPreset('help');var c=document.getElementById('searchInput').value;document.getElementById('searchInput').value='SIGNPRESET '+((a==='你好'&&b==='妈妈'&&c==='医院')?'OK':'BAD '+a+'/'+b+'/'+c);"],
  "expect": ["SIGNPRESET OK"],
  "ref": "三个预设必须与按钮标签一致：问候→你好、家庭称谓→妈妈、医疗求助→医院。旧实现 help 分支写死“谢谢”，探针会红；医院是词表已存在词条，不在本页新造未核验词。"
},
{
  "slug": "accessibility/ramp-slope",
  "clicks": ["document.getElementById('height').value='90';document.getElementById('ratio').value='10';document.getElementById('sceneSel').value='resident';calc();var __tip=document.getElementById('tipBox').textContent;document.getElementById('height').value='';calc();var __r=document.getElementById('result').innerHTML;var __g=document.getElementById('grid').innerHTML;var __s=document.getElementById('rampSvg').innerHTML;var __t=document.getElementById('tipBox').innerHTML;document.getElementById('tipBox').innerHTML='RAMPCLR '+((__g===''&&__s===''&&__t===''&&__r.indexOf('请输入有效')>=0&&__r.indexOf('符合无障碍坡道规范')<0)?'OK':'BAD '+__g+'/'+__s+'/'+__t);"],
  "expect": ["RAMPCLR OK"],
  "ref": "输入失效清空：先用 90/1:10/居住区算出旧提示与图形，再把高差清空并 calc ⇒ 结果区只显示“请输入有效的高差与坡度比”，tipBox、grid、rampSvg 全部清空，旧“符合无障碍坡道规范要求”不得残留。旧实现只替换 #result 后 return，探针必红。"
},
{
  clicks: ["calc()"],
  "slug": "accessibility/ramp-slope",
  "inputs": {"height":"40","ratio":"12","sceneSel":"general"},
  "expect": ["只校核坡度与单段高差", "未校核项：净宽、扶手"],
  "ref": "结论限定：默认 40cm/1:12 的提示只声明坡度与单段高差通过，并列出未校核的净宽、扶手、防滑、平台尺寸、入口衔接等；不得再输出“符合无障碍坡道规范要求”这种整体合规措辞。"
},
{
  "slug": "accessibility/accessible-restroom",
  "clicks": ["document.getElementById('scopeRegion').value='us';updateScope();"],
  "expect": ["32 in", "33–36 in", "60 in"],
  "ref": "地区切换必须作用于卡片与清单：美国 ⇒ 门净宽 ≥32 in（0.815 m）、扶手 33–36 in（0.84–0.91 m）、回转 60 in（1.525 m）。默认中国大陆为 0.80m/0.70m/1.50m，三个串均不出现，强判别。"
},
{
  "slug": "accessibility/accessible-restroom",
  "clicks": ["document.getElementById('scopeRegion').value='other';updateScope();"],
  "expect": ["按当地规范", "本页不提供可直接验收数值"],
  "ref": "其他地区不得继续呈现中国数值：卡片统一显示“按当地规范 / 本页不提供可直接验收数值”，提示“本页数值不适用”。默认中国大陆不出现该串。"
},
{
  "slug": "accessibility/accessible-restroom",
  "clicks": ["document.getElementById('scopeRegion').value='cn';document.getElementById('scopeType').value='home';updateScope();"],
  "expect": ["住宅改造：确认门洞", "住宅改造：紧急呼叫按钮"],
  "ref": "项目类型必须作用于清单：住宅适老化改造追加门洞改造、紧急呼叫响应、照护者试用三条；公共建筑默认不含这些条目。"
},
{
  "slug": "accessibility/accessible-restroom",
  "clicks": ["document.getElementById('scopeRegion').value='cn';document.getElementById('scopeType').value='home';updateScope();exportChecklist();"],
  "expect": ["项目所在地：中国大陆", "项目类型：住宅适老化改造", "页面核验日期：2026-11-27", "核验：待核验"],
  "ref": "导出必须包含选择、限制和核验日期：buildExportText 生成文本后写入 #exportPreview，并由 exportChecklist 复制；文本含地区、项目类型、GB 55019-2021、页面核验日期 2026-11-27、逐项“核验：待核验”。旧实现固定文本且无预览，探针会红。"
},
{
  "slug": "accessibility/voice-synthesis",
  "clicks": ["supported=true;globalThis.speechSynthesis={getVoices:function(){return [{name:'Only English',lang:'en-US'}];},speaking:false,paused:false,speak:function(){},cancel:function(){},pause:function(){},resume:function(){}};document.getElementById('langFilter').value='zh';loadVoices();var __n=document.getElementById('voiceNotice').textContent;var __d=document.getElementById('voiceSel').disabled;var __o=document.getElementById('voiceSel').textContent;document.getElementById('langFilter').value='';loadVoices();var __all=document.getElementById('voiceSel').value;document.getElementById('status').textContent='VOICEFILTER '+((__n.indexOf('没有匹配')>=0&&__n.indexOf('不再静默回退')>=0&&__d&&__o.indexOf('Only English')<0&&__all==='Only English')?'OK':'BAD '+__n+'/'+__o+'/'+__all);"],
  "expect": ["VOICEFILTER OK"],
  "ref": "无匹配不回退：桩只有 en-US 语音，筛选 zh ⇒ 列表显示“没有匹配的中文（zh）语音”并禁用，提示明确不回退为全部；切回“全部”后才出现 Only English 并可主动选择。旧实现静默 filtered=voices，探针会红。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== accessibility calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
