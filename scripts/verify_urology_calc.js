#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
// 第八批加固：urology 全部用例去默认化 / 修复破损与退化
// 每条用例输入均 ≠ 页面默认值，且 expect 断言「页面计算出的结果文本」（非输入值、非静态表字面量）。
// 判别力由 scripts/discriminate_check.js 反向验证（模拟注入失败须 FAIL）。
const CASES = [
{
  "slug": "urology/assessor-pressure",
  "inputs": { "pdet": "120", "qmax": "15" },
  "expect": ["BOOI=90（梗阻）", "BCI=195（强收缩力）"],
  "ref": "de-default: pdet120/qmax15→BOOI90 梗阻（标签外纯净串）"
},
{
  "slug": "urology/bladder-capacity",
  "inputs": { "voided": "800", "pvr": "100", "age": "45" },
  "expect": ["900 mL", "膀胱容量偏大"],
  "ref": "de-default: 800/100→900mL 偏大"
},
{
  "slug": "urology/calc-volume",
  "inputs": { "d1": "3.0", "d2": "2.5", "d3": "3.0", "formula": "0.52", "psa": "" },
  "expect": ["11.7", "偏小"],
  "ref": "de-default: 椭球 vol 11.7 偏小（data-grid 数字与 mL 分离）"
},
{
  "slug": "urology/canyuniaoliang-jingfubchao-tuisuan",
  "inputs": { "w": "7", "d": "6", "h": "5", "formula": "0.75" },
  "expect": ["157.5", "残余尿增多"],
  "ref": "de-default: 经腹 vol 157.5 残余尿增多（数字与 mL 分离）"
},
{
  "slug": "urology/hydronephrosis",
  "inputs": { "apd": "30", "cortex": "4", "subject": "adult" },
  "expect": ["重度", "4 mm"],
  "ref": "de-default: apd30/cortex4→重度 + <5mm 皮质萎缩"
},
{
  "slug": "urology/penile-rigidity",
  "inputs": { "ehs": "2", "npt_n": "2", "npt_d": "8", "npt_r": "60" },
  "expect": ["最大硬度60%", "2次/夜"],
  "ref": "de-default: ehs2+NPT(2/8/60均低于正常)→异常器质性ED；expect取动态独有'最大硬度60%'/'2次/夜'，避静态EHS分级表碰撞（ehs:1恰等于校验器误取的首option）"
},
{
  "slug": "urology/prostate-volume",
  "inputs": { "d1": "5", "d2": "4", "d3": "5", "psa": "8", "formula": "0.5236" },
  "expect": ["52.4 mL", "增生程度：重度增大"],
  "ref": "de-default: 椭球 vol 52.4mL 重度增大"
},
{
  "slug": "urology/psa-density",
  "inputs": { "psa": "12", "vol": "25", "age": "50" },
  "expect": ["0.480", "风险分级：高危", "穿刺评估：需结合临床和影像综合判断"],
  "ref": "PSAD 0.480：计算密度并提示综合判断，不能直接决定活检。"
},
{
  "slug": "urology/residual-urine",
  "inputs": { "w": "6", "h": "5", "d": "5", "voided": "350", "formula": "0.7" },
  "expect": ["105 mL", "程度：中度尿潴留"],
  "ref": "de-default: PVR 105mL 中度尿潴留"
},
{
  "slug": "urology/urethral-stricture",
  "inputs": { "qmax": "5", "qave": "4", "vol": "200", "time": "40", "curve": "plateau" },
  "expect": ["高度可疑尿道狭窄"],
  "ref": "de-default: score10→高度可疑（避开静态依据串）"
},
{
  "slug": "urology/urine-flow-rate",
  "inputs": { "age": "60", "qmax": "8", "vol": "200" },
  "expect": ["梗阻可能"],
  "ref": "de-default: 男 qmax8→梗阻可能（标签外纯净串，避静态参考串与子串碰撞）"
},
{
  "slug": "urology/urodynamics",
  "inputs": { "pdet": "120", "qmax": "5", "pdetmax": "130", "fdv": "100", "mcc": "200" },
  "expect": ["145"],
  "ref": "de-default: BCI145（避开默认 BCI110/BOOI110）"
},
{
  "slug": "urology/varicocele-grading",
  "inputs": { "diam": "5.0", "reflux": "4.0" },
  "expect": ["3级（重度）"],
  "ref": "de-default: diam5→3级重度（避开静态显微结扎术串）"
},
{
  "slug": "urology/calc-1",
  "inputs": { "q0": "3", "q1": "3", "q2": "3", "q3": "3", "q4": "3", "q5": "3", "q6": "3" },
  "expect": ["21 分（0-35 分）"],
  "ref": "fix broken template: q0-6=3→总分21（数字在 strong 内，空格感知）"
},
{
  "slug": "urology/catheter-selection",
  "inputs": { "patient": "adult_female" },
  "expect": ["14 Fr"],
  "ref": "de-default: 成人女性→推荐14Fr（computed 串，避静态表/回声）"
},
{
  "slug": "urology/hematuria-differential",
  "inputs": { "morph": "dysmorphic" },
  "expect": ["肾小球性血尿"],
  "ref": "de-default: dysmorphic→肾小球性（strong 内文本，避回声）"
},
{
  "slug": "urology/hydrocele-assessment",
  "inputs": { "age": "infant", "trans": "positive", "depth": "60" },
  "expect": ["大量积液", "60 mm"],
  "ref": "de-default: depth60→大量积液（避开输入值回声）"
},
{
  "slug": "urology/ipss-score",
  "inputs": {},
  "clicks": ["document.getElementById('qol').value='1';__markScaleDirty();"],
  "expect": ["（满意）"],
  "ref": "de-default: qol1→（满意）；改为显式赋值+__markScaleDirty，避免 jsdom 不派发 change 时脏标志未置位。"
},
{
  "slug": "urology/rater-4",
  "inputs": { "e1": "5", "e2": "5", "e3": "5", "e4": "5", "e5": "5" },
  "expect": ["IIEF-5总分25分（22-25分）"],
  "ref": "fix: e1-5=5→总分25/25（标签外纯净串）"
},
{
  "slug": "urology/stone-composition",
  "inputs": { "search": "zzz" },
  "expect": ["未找到匹配的结石成分"],
  "ref": "fix no_inputs: 注入无匹配词→未找到（空搜索默认渲染9石会假通过）"
},
{
  "slug": "urology/stone-size-assessment",
  "inputs": { "size": "15", "loc": "renal" },
  "expect": ["自发排石率低"],
  "ref": "de-default: size15/renal→prob=2(<30)策略'自发排石率低'（避2%⊂42%子串逃逸；回退42%/75%输出均无此串）"
},
{
  "slug": "urology/turp-parameters",
  "inputs": { "vol": "40", "method": "turp" },
  "expect": ["48 分钟"],
  "ref": "de-default: turp+vol40→48min（依赖 vol，避 method 静态串）"
},
{
  "slug": "urology/uti-diagnosis",
  "inputs": { "count": "mid" },
  "expect": ["菌落计数过低，多为标本污染"],
  "ref": "de-default: count mid+无勾选→污染分支（count high 恰为 select 真实默认，须改用 mid）"
},
{
  "slug": "urology/ipss-score",
  "clicks": ["var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/IPSS 总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('result').innerHTML=__ok?'__IPSS_DEF_OK__':'__IPSS_DEF_FAIL__ '+__b;"],
  "expect": ["__IPSS_DEF_OK__"],
  "ref": "批 3 默认态：只出 IPSS 总分与 QOL，结果区不含 分级/建议/诊断/治疗/风险。"
},
{
  "slug": "urology/ipss-score",
  "clicks": ["for(var i=0;i<7;i++){var e=document.getElementById('q'+i);if(e)e.value='5';}var q=document.getElementById('qol');q.value='6';__markScaleDirty();var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/重度/.test(__b)&&/处理建议/.test(__b);document.getElementById('result').innerHTML=__ok?'__IPSS_MOD_OK__':'__IPSS_MOD_FAIL__ '+__b;"],
  "expect": ["__IPSS_MOD_OK__"],
  "ref": "批 3 改动态：7 项各 5 分 + QOL 6 ⇒ 总分 35 落「重度」并给处理建议；确认 dirty 置位后分级文案才出现。"
},
{
  "slug": "urology/ipss-score",
  "clicks": ["__markScaleDirty();resetAll();var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/IPSS 总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('result').innerHTML=__ok?'__IPSS_RST_OK__':'__IPSS_RST_FAIL__ '+__b;"],
  "expect": ["__IPSS_RST_OK__"],
  "ref": "批 3 重置态：先置 dirty 制造决策，再 resetAll() 复位后决策文案消失。"
},
{
  "slug": "urology/ipss-score",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/urology/ipss-score.html','utf8');var noTpl=h.indexOf(\"<li>'+q.t+'</li>\")<0;var noFill=h.indexOf('工作与生活中的相关计算与查询')<0;var noQol=h.indexOf('加 QoL 0-6 共 35')<0;var hasScene=h.indexOf('BPH / 下尿路症状自评')>=0;var hasQol=h.indexOf('QoL 另计 0-6')>=0;document.getElementById('__tbProbe').textContent=(noTpl&&noFill&&noQol&&hasScene&&hasQol)?'__IPSS_CONTENT_OK__':'__IPSS_CONTENT_BAD__ '+[noTpl,noFill,noQol,hasScene,hasQol].join(',');"],
  "expect": ["__IPSS_CONTENT_OK__"],
  "ref": "第1097批 N44/N45/N46：模板残留 '+q.t+' 删除、opt-guide/opt-faq/FAQPage 三处套话「工作与生活中的相关计算与查询」改真实场景、deepdive FAQ 的「加 QoL 0-6 共 35」改为 7 项合计 0-35 且 QoL 另计 0-6 不进总分。五哨兵须同时成立，全为源码形态判别，旧版必红。"
},
{
  "slug": "urology/psa-density",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/urology/psa-density.html','utf8');var ok=h.indexOf('function __psaRefBar(psad)')>=0&&h.indexOf('if(__ppa>0&&__pvol>0) __psaRefBar(__ppa/__pvol);')>=0;document.getElementById('__tbProbe').textContent='PSAREFBAR '+(ok?'OK':'BAD');"],
  "expect": ["PSAREFBAR OK"],
  "ref": "12-N29 同类时序缺陷：PSAD 首屏参考区间标尺须在 TBKit 就绪后重绘；旧版 boot 只挂预设 ⇒ 变红。默认态不产生该串，零逃生。"
},
{
  "slug": "urology/bladder-capacity",
  "inputs": {"voided":"0","pvr":"0","age":"45"},
  "expect": ["排尿量与残余尿至少一项需大于 0"],
  "ref": "12-N108：0+0 空记录旧版按容量0给出偏小/排空障碍；新版前置拦截并停止分级。默认 280+30 不产生该串。"
},
{
  "slug": "urology/bladder-capacity",
  "inputs": {"voided":"120","pvr":"60","age":"45"},
  "expect": ["膀胱容量显著缩小（低于预期50%）"],
  "ref": "12-N109：180/400=45% 旧版只判「偏小」，与 FAQ「<50% 显著下降」冲突；新版三档口径给显著缩小。默认 310/400 不产生该串。"
},
{
  "slug": "urology/bladder-capacity",
  "inputs": {"voided":"300","pvr":"0","age":"45"},
  "clicks": ["var b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ');var ok=b.indexOf('300 + 0 = 300 mL')>=0&&b.indexOf('残余尿：残余尿低于 50 mL，正常')>=0;document.getElementById('__tbProbe').textContent='PVRZERO '+(ok?'OK':'BAD');"],
  "expect": ["PVRZERO OK"],
  "ref": "12-N108 残余尿0：旧版 pvr>0 分支跳过残余尿提示；新版 0 仍显示正常参考。默认 pvr=30 也会显示同类提示，故用注入输入 300+0 与残余尿提示组合成哨兵，只由 clicks 产出，零逃生。"
},
{
  "slug": "urology/stone-size-assessment",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/urology/stone-size-assessment.html','utf8');var ok=h.indexOf('肾结石 8mm（孤立肾）')>=0&&h.indexOf('肾结石 8mm 伴积水')<0&&h.indexOf('hasOwnProperty.call(rec,__cbs[__ci].id)')>=0;document.getElementById('__tbProbe').textContent='STONEPRESET '+(ok?'OK':'BAD');"],
  "expect": ["STONEPRESET OK"],
  "ref": "12-N87/N91：预设标签与 renal=孤立肾/肾功能不全 语义一致，不再谎称伴积水；历史恢复清空未记录勾选的逻辑保留。旧版标签为伴积水 ⇒ 变红。默认态不产生该串，零逃生。"
  },{
    "slug": "urology/stone-size-assessment",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/urology/stone-size-assessment.html','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/urology/stone-size-assessment.json','utf8');var ok=h.indexOf('输尿管中段 0.9')>=0&&h.indexOf('膀胱 1.0')>=0&&h.indexOf('经验修正，非指南直接给出')>=0&&h.indexOf('肾/输尿管上段 0.7、下段 1.25')<0&&en.indexOf('mid ureter 0.9')>=0&&en.indexOf('empirical adjustments')>=0;document.getElementById('__tbProbe').textContent='STONEFACTOR '+(ok?'OK':'BAD');"],
    "expect": ["STONEFACTOR OK"],
    "ref": "12-N90：公式框原只列 3 个部位系数，代码另有 mid 0.9 / bladder 1.0；现补齐 6 个并明示系数为页面经验修正、膀胱套用输尿管模型仅供粗参。旧版缺 mid/bladder 与局限性说明 ⇒ 变红。N89 模型适用性保留专业复核。"
  },{
    "slug": "urology/psa-density",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/urology/psa-density.html','utf8');var ok=h.indexOf('0.15 - &lt;0.25')>=0&&h.indexOf('≥ 0.25')>=0&&h.indexOf('不能决定是否活检')>=0&&h.indexOf('未勾选不代表检查正常')>=0&&h.indexOf('暂不穿刺')<0;document.getElementById('__tbProbe').textContent='PSAGRADE '+(ok?'OK':'BAD');"],
    "expect": ["PSAGRADE OK"],
    "ref": "PSAD 密度边界与不以单一指标直接决定活检的说明。"
  },{
    "slug": "urology/psa-density",
    "inputs": { "psa": "3", "vol": "15", "age": "60" },
    "checkIds": ["mri", "dre"],
    "clicks": ["calc();var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='PSA35 '+((document.getElementById('psa').value==='3'&&r.indexOf('不能决定是否活检')>=0)?'OK':'BAD');"],
    "expect": ["PSA35 OK"],
    "ref": "PSA <4 with suspicious MRI and abnormal DRE must include both findings and avoid a definite no-biopsy recommendation."

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

  console.log("==== urology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
