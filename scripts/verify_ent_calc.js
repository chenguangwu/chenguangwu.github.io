#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  // 原为 no_inputs 弱用例：expect「26-50%」来自 grade=2 的默认档，与勾选无关。
  "slug": "ent/adenoid-grading",
  "checkIds": [
    "s1",
    "s6"
  ],
  "expect": [
    "存在手术指征（腺样体面容）",
    "伴随症状： 张口呼吸、腺样体面容"
  ],
  "ref": "grade 默认 2（II度）；勾选 s1(张口呼吸)+s6(腺样体面容) → 症状列表拼接，且 s6 直接触发手术指征（surgReason=[腺样体面容]）。回退默认（未勾选、grade=2 且 s5 未勾选）→ 输出「目前暂无明确手术指征」，两串均不命中。"
},
{
  "slug": "ent/ahi-severity",
  "inputs": {
    "apneas": "45",
    "hypopneas": "50",
    "sleepHours": "6",
    "lowSpO2": "82",
    "odCount": "60",
    "arousals": "40"
  },
  "expect": [
    "15.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/allergy-skin-test",
  "inputs": {
    "histWheal": "12",
    "histFlare": "20",
    "allerWheal": "5",
    "allerFlare": "15"
  },
  "expect": [
    "但小于阳性对照的1/2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/calc-1",
  "inputs": {
    "rhinorrhea": "3",
    "sneeze": "3",
    "itch": "2",
    "congestion": "3"
  },
  "expect": [
    "TNSS 总分： 11 分（0-12 分） 症状程度： 极重度"
  ],
  "ref": "TNSS 四症状各 0-3 分（rhinorrhea/sneeze/itch/congestion select）；注入 3/3/2/3 ⇒ 总分 11 > 9 ⇒ classify() 返回「极重度」并输出「建议耳鼻喉科就诊，评估药物治疗方案。」。默认 0/0/0/0 ⇒ 总分 0「轻度」。原 expect「0-12」是结果区固定文案「（0-12 分）」，与输入无关（常量型逃生项）。"
},
{
  "slug": "ent/caloric-test",
  "inputs": {
    "rw": "38",
    "lw": "22",
    "rc": "20",
    "lc": "18"
  },
  "expect": [
    "18.4%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/eustachian-tube",
  "clicks": [
    "selections.valsalva_tm=0;selections.valsalva_subj=0;selections.tympanogram=0;selections.reflex_ipsi=1;selections.toynbee=0;symptomSelected={'耳闷胀感':1};symptomNone=false;calc()"
  ],
  "expect": [
    "需手术干预，明确病因（肿瘤、腺样体肥大等）"
  ],
  "ref": "5 项客观检查（valsalva_tm/valsalva_subj/tympanogram/reflex_ipsi/toynbee）默认合计 16/18 ⇒「0级·正常」；clicks 置 0/0/0/1/0 并把症状「耳闷胀感」计 1 分（symptomNone=false）⇒ 综合评分 0-1=-1→0 ⇒「IV级·极重度障碍」+「需手术干预」。默认态为「0级·正常」。原 expect「(89%)」是默认态进度条 16/18=88.9% 的文案（常量型逃生项）。"
},
{
  "slug": "ent/facial-nerve-hb",
  "clicks": [
    "grade=5;calc()"
  ],
  "expect": [
    "重度面神经功能障碍。需行面神经电图评估，若变性>90%需考虑面神经减压术。需眼部保护。预后较差。"
  ],
  "ref": "页面顶层 var grade 默认 1 ⇒ House-Brackmann I级·正常；clicks 置 grade=5 后 calc() ⇒ V级·重度功能障碍及其治疗建议「需行面神经电图评估，若变性>90%需考虑面神经减压术」。默认态只有 I级 文案。原 expect「面神经功能障碍程度」是结果区固定小标题（常量型逃生项）。"
},
{
  "slug": "ent/fistula-test",
  "inputs": {
    "positivePressure": "450",
    "negativePressure": "200"
  },
  "expect": [
    "正压450mmH"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/gag-reflex",
  "clicks": [
    "grade=4;calc()"
  ],
  "expect": [
    "咽反射极度敏感，严重影响口腔检查和治疗操作。可能与心理因素、焦虑或神经官能症有关。"
  ],
  "ref": "var grade 默认 2 ⇒「2级·反射正常」；clicks 置 grade=4 ⇒ 4级·极度敏感及临床建议「进行口腔操作前可考虑表面麻醉或行为干预」。原 expect「2级」恰是默认档名（常量型逃生项）。"
},
{
  "slug": "ent/grbas-scale",
  "clicks": [
    "scores.G=3;scores.R=3;scores.B=2;scores.A=1;scores.S=0;calc()"
  ],
  "expect": [
    "嗓音重度异常，G评分多为3分，严重影响交流，需综合治疗",
    "粗糙声明显（声带振动不规则，可见于声带息肉、肿瘤等）"
  ],
  "ref": "var scores={G,R,B,A,S} 默认全 0 ⇒ 总分 0/15「正常」；clicks 置 3/3/2/1/0 ⇒ 总分 9 ⇒「重度异常」+ 特征分析两条（R>=2 粗糙声明显、B>=2 气息声明显）。原 expect「总评(0-3)」是 stat-card 的 lbl（常量型逃生项）。"
},
{
  "slug": "ent/hearing-loss-classification",
  "inputs": {
    "ac500": "38",
    "ac1000": "30",
    "ac2000": "35",
    "ac4000": "40",
    "bc500": "10",
    "bc1000": "15",
    "bc2000": "15",
    "bc4000": "20"
  },
  "expect": [ "34 PTA气导" ],
  "ref": "auto-restore"
},
{
  "slug": "ent/laryngeal-nerve",
  "inputs": {
    "f0": "180",
    "jitter": "2.5",
    "shimmer": "5.0",
    "nhr": "0.20",
    "hnr": "15",
    "mpt": "8"
  },
  "expect": [ "基频 180" ],
  "ref": "auto-restore"
},
{
  "slug": "ent/lund-kennedy-score",
  "clicks": [
    "scores.L={polyp:2,edema:2,discharge:2,scar:2,crust:2};scores.R={polyp:2,edema:2,discharge:2,scar:2,crust:2};calc()"
  ],
  "expect": [
    "黏膜炎症严重，建议行鼻内镜手术"
  ],
  "ref": "var scores={L:{polyp,edema,discharge,scar,crust}, R:{…}} 默认全 0 ⇒ 总分 0/20「轻度」；clicks 置双侧各 2 ⇒ 总分 20 > 13 ⇒「重度」+「黏膜炎症严重，建议行鼻内镜手术」。原 expect「左侧(0-10)」是 stat-card 的 lbl（常量型逃生项）。"
},
{
  "slug": "ent/lund-mackay-score",
  "clicks": [
    "scores.right={maxillary:2,anterior_ethmoid:2,posterior_ethmoid:2,sphenoid:2,frontal:2,omc:2};scores.left={maxillary:2,anterior_ethmoid:2,posterior_ethmoid:2,sphenoid:1,frontal:1,omc:2};calc()"
  ],
  "expect": [
    "全组鼻窦严重受累",
    "强烈建议尽早手术，术后定期随访"
  ],
  "ref": "var scores={right:{6 组鼻窦}, left:{…}} 默认全 0 ⇒ 0/24「轻度」；clicks 置右 12（maxillary 2 等全 2）、左 10 ⇒ 总分 22 > 20 ⇒「极重度」+「全组鼻窦严重受累」+「强烈建议尽早手术」。原 expect「24」是分母「/ 24 分」（常量型逃生项）。"
},
{
  "slug": "ent/nasal-resistance",
  "inputs": {
    "lp": "225",
    "lv": "350",
    "rp": "150",
    "rv": "400"
  },
  "expect": [
    "0.237"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/pure-tone-audiometry",
  "inputs": {
    "ptDur": "1050",
    "ptVol": "100"
  },
  "expect": [
    "1050"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "ent/tdi-score",
  "inputs": {
    "scoreT": "9",
    "scoreD": "10",
    "scoreI": "11"
  },
  "expect": [
    "62.5%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/tdi-score",
  "inputs": {"scoreT":"","scoreD":"","scoreI":""},
  "clicks": ["calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='TDIGUARD '+(h.indexOf('0–16')>=0&&h.indexOf('功能性失嗅')<0?'OK':'BAD '+h.slice(0,70));"],
  "expect": ["TDIGUARD OK"],
  "ref": "N115 清空守卫：三项留空经 `+||0` 旧版得 tdi=0「功能性失嗅」；修复后 __tdiInputs 判空+范围（0–16）⇒ 提示「0–16」不出分级。旧版 BAD。默认 9/10/11 合法不含该提示，零逃生。"
},
{
  "slug": "ent/tdi-score",
  "inputs": {"scoreT":"20","scoreD":"16","scoreI":"16"},
  "clicks": ["var __cap='';var old=ToolBox.copyText;ToolBox.copyText=function(s){__cap=String(s);};copyResult();ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='TDICOPY '+(__cap.indexOf('总分=52')<0?'OK':'BAD '+__cap.slice(0,80));"],
  "expect": ["TDICOPY OK"],
  "ref": "N116 复制一致性：T=20 越界（>16），旧版 copyResult 不 clamp ⇒ 复制「总分=52.0/48」（超满分），修复后 __tdiInputs ok=false ⇒ 不复制、只刷新结果提示 ⇒ 无「总分=52」。默认 9/10/11 合法，但本哨兵只在 clicks 注入 copyResult 探针后出现，零逃生。"
},
{
  "slug": "ent/temporal-resolution-hearing",
  "inputs": {
    "trGapSlider": "20",
    "trModFreq": "4",
    "trModDepth": "30",
    "trGapMode": "manual"
  },
  "expect": [
    "manual"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "ent/tinnitus-matching",
  "inputs": {
    "loudness": "8",
    "masking": "50"
  },
  "expect": [
    "42"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「26-50%」来自 grade=2 的默认档，与勾选无关。
  "slug": "ent/tonsil-grading",
  "checkIds": [
    "s1",
    "s4"
  ],
  "expect": [
    "需要进一步评估（反复发作≥3次/年、扁桃体周围脓肿史）"
  ],
  "ref": "grade 默认 2（II度）；勾选 s1(反复扁桃体炎)+s4(周围脓肿史) → surgReason 依序拼接为「反复发作≥3次/年、扁桃体周围脓肿史」。回退默认（未勾选、grade=2）→ 「目前暂无明确手术指征」，该串不命中。"
},
{
  "slug": "ent/tympanic-perforation",
  "inputs": {
    "perfD": "6",
    "perfW": "2",
    "tmD": "10",
    "tmW": "9"
  },
  "expect": [
    "13.3%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/tympanometry",
  "inputs": {
    "tpp": "0",
    "sc": "3.7",
    "ecv": "1.0",
    "grad": "40"
  },
  "expect": [ "3.70 声顺" ],
  "ref": "auto-restore"
},
{
  "slug": "ent/vocal-cord-assessment",
  "clicks": [
    "sel.mobility='固定';sel.position='中间位';sel.side='双侧';sel.closure='无法闭合';calc()"
  ],
  "expect": [
    "声带完全麻痹（III度）",
    "双侧声带麻痹可致喉梗阻及呼吸困难，需评估气道安全性，必要时行气管切开"
  ],
  "ref": "var sel={mobility:正常,side:左侧,position:正中位,closure:完全闭合,arytenoid:活动正常} 默认 ⇒「声带运动正常」；clicks 置 mobility=固定/position=中间位/side=双侧/closure=无法闭合 ⇒「声带完全麻痹（III度）」+「双侧声带麻痹可致喉梗阻…行气管切开」+「声门闭合不全…声带内移术」。原 expect「声带运动功能正常」是默认档 advice 片段（常量型逃生项）。"
},
  { slug: "ent/caloric-test",
    inputs: { rw: "", lw: "", rc: "", lc: "" },
    expect: ["请填写四组冷热试验反应值（°/s）后再判读。"],
    ref: "空态守卫：四项全清空时不再把空值按 0 参与计算（旧实现 +''||0 → 总和 0 → UW=0/DP=0 →「前庭功能正常」），改为只输出填写提示，不给正常/异常结论。默认态四项 25/22/20/18 有值 ⇒ 提示串不出现。" },
  { slug: "ent/lund-mackay-score",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ent/lund-mackay-score.html','utf8');var ok=h.indexOf('各 5 个鼻窦')>=0&&h.indexOf('OMC（仅 0 或 2')>=0&&h.indexOf('各 6 个鼻窦 / 窦口复合体（每项 0 至 2')<0;document.getElementById('__tbProbe').textContent='LMFIX '+(ok?'OK':'BAD');"],
    expect: ["LMFIX OK"],
    ref: "第1096批 N30：公式框旧文案把 6 个部位都写成 0 至 2 三档，但 OMC 只有 0 未阻塞/2 完全阻塞两档，用户会以为漏了 1 分按钮；改为 5 个鼻窦 0–2 + OMC 仅 0 或 2，源码形态判别旧串消失且新串出现。" },
{
  "slug": "ent/lund-mackay-score",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ent/lund-mackay-score.html','utf8');var ok=h.indexOf('function __lmRefBar(total)')>=0&&h.indexOf('try{__lmRefBar(__lmTotal());}catch(e){} try{__lmChart();}catch(e){}')>=0;document.getElementById('__tbProbe').textContent='LMREFBAR '+(ok?'OK':'BAD');"],
  "expect": ["LMREFBAR OK"],
  "ref": "12-N29 首屏参考区间标尺：DOMContentLoaded 后必须重绘 refBar；旧版回调只调 __lmChart、refBar 被吞掉 ⇒ 变红。默认态不产生该串，零逃生。"
},
{
  "slug": "ent/tonsil-grading",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ent/tonsil-grading.html','utf8');var ok=h.indexOf('out.grade=String(grade)')>=0&&h.indexOf('TBKit.preset.bar(')>=0&&h.indexOf('tonsil_gradingPresets')>=0&&h.indexOf('Grade III with OSAHS')>=0&&h.indexOf('ToolBox.copyText(full')>=0&&h.indexOf('hasOwnProperty.call(rec')>=0;document.getElementById('__tbProbe').textContent='TONSILHIST '+(ok?'OK':'BAD');"],
  "expect": ["TONSILHIST OK"],
  "ref": "12-N101/N102/N103 复制部分：历史快照显式包含分度且恢复时同步按钮；预设栏补三组场景；复制结果改为完整结果文本。旧版快照无 grade、预设空壳、复制仅分度 ⇒ 变红。IV 度单独是否手术仍待专业复核，不在本用例。"
},
{
  "slug": "ent/tdi-score",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ent/tdi-score.html','utf8');var ok=h.indexOf('id=\"scoreT\" value=\"6\" min=\"0\" max=\"16\"')>=0&&h.indexOf('范围 0-16')>=0&&h.indexOf('阈值T (0-16)')>=0&&h.indexOf('总分 >30.5 正常')>=0&&h.indexOf('min=\"1\" max=\"16\"')<0&&h.indexOf('范围 1-16')<0&&h.indexOf('总分 >30 正常')<0;document.getElementById('__tbProbe').textContent='TDIRANGE '+(ok?'OK':'BAD');"],
  "expect": ["TDIRANGE OK"],
  "ref": "12-N117：T 子项统一 0–16，引据阈值统一 >30.5；旧版 min=1、提示 1-16、引据 >30 ⇒ 变红。默认态不产生该串，零逃生。"
  },{
    "slug": "ent/tonsil-grading",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/ent/tonsil-grading.html','utf8');var dd=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/ent/tonsil-grading.json','utf8');var a=JSON.parse(dd)['ent/tonsil-grading'].faqs.filter(function(f){return f.q==='分度与手术关系？';})[0].a;var ok=h.indexOf('吞咽困难（仅记录，不参与指征判断）')>=0&&a.indexOf('吞咽障碍')<0&&a.indexOf('不能单凭分度或打鼾决定手术')>=0&&en.indexOf('record only, not a surgical indication')>=0;document.getElementById('__tbProbe').textContent='TONSILS3 '+(ok?'OK':'BAD');"],
    "expect": ["TONSILS3 OK"],
    "ref": "12-N100：吞咽困难原被采集却称「伴吞咽障碍多建议手术」，与判定逻辑（s3 不参与指征）冲突。现复选框明示仅记录，深解 FAQ 对齐页面既有手术指征列表并声明吞咽困难不单独构成指征。旧版 FAQ 仍含「吞咽障碍」且无仅记录标注 ⇒ 变红。N103 的 IV 度单独手术阈值保留专业复核。"
  },
  {"slug":"ent/tonsil-grading", "clicks":["setGrade(4);calc()"], "expect":["未选择上述症状或病史；仅凭分度不能判定是否需要手术"], "ref":"IV 度无症状不单独判定手术"},
  {"slug":"ent/tonsil-grading", "checkIds":["s2"], "clicks":["setGrade(4);calc()"], "expect":["需要进一步评估（睡眠打鼾/呼吸暂停）"], "ref":"打鼾是评估线索，不能直接确诊 OSAHS 或决定手术"}
,
{
  "slug": 'ent/ahi-severity',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/ent/ahi-severity.html\',\'utf8\');var i=h.indexOf(\'function copyResult(){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+900):\'\';var ok=seg.indexOf(\'var hours = +document.getElementById(\\\'sleepHours\\\').value || 1;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'AHICP0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['AHICP0 OK'],
  "ref": "第1341批·复制与页面结果不同源修复源码形态强锚：旧版 copyResult 另算一遍且无守卫，页面显示错误/—时复制仍输出 Infinity/0dB 假值；修复后 copyResult 补与 calc 同源守卫，无效时提示并 return。旧版无 ⇒ BAD。"
},
{
  "slug": 'ent/tympanic-perforation',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/ent/tympanic-perforation.html\',\'utf8\');var i=h.indexOf(\'function copyResult(){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+900):\'\';var ok=seg.indexOf(\'if(!isFinite(tmArea)||tmArea<=0)\')>=0&&seg.indexOf(\'请先填写有效的鼓膜尺寸再复制\')>=0;document.getElementById(\'__tbProbe\').textContent=\'TympCP0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['TympCP0 OK'],
  "ref": "第1341批·复制与页面结果不同源修复源码形态强锚：旧版 copyResult 另算一遍且无守卫，页面显示错误/—时复制仍输出 Infinity/0dB 假值；修复后 copyResult 补与 calc 同源守卫，无效时提示并 return。旧版无 ⇒ BAD。"
},
{
  "slug": 'ent/hearing-loss-classification',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/ent/hearing-loss-classification.html\',\'utf8\');var i=h.indexOf(\'function copyResult(){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+900):\'\';var ok=seg.indexOf(\'__ids.every(function(id)\')>=0&&seg.indexOf(\'请先填写听阈再复制\')>=0;document.getElementById(\'__tbProbe\').textContent=\'HLCCP0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['HLCCP0 OK'],
  "ref": "第1341批·复制与页面结果不同源修复源码形态强锚：旧版 copyResult 另算一遍且无守卫，页面显示错误/—时复制仍输出 Infinity/0dB 假值；修复后 copyResult 补与 calc 同源守卫，无效时提示并 return。旧版无 ⇒ BAD。"
},
{ slug:"ent/allergy-skin-test", inputs:{"histWheal":"","histFlare":"","allerWheal":"","allerFlare":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"ent/laryngeal-nerve", inputs:{"f0":"","jitter":"","shimmer":"","nhr":"","hnr":"","mpt":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"ent/nasal-resistance", inputs:{"lp":"","lv":"","rp":"","rv":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"ent/tinnitus-matching", inputs:{"loudness":"","masking":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"ent/tympanic-perforation", inputs:{"perfD":"","perfW":"","tmD":"","tmW":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" }
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

  console.log("==== ent calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
