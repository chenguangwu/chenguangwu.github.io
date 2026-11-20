#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "security/anti-fraud-cards",
  "inputs": {
    "catFilter": "telecom"
  },
  "expect": [
    "telecom"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "security/data-erase-simulator",
  "clicks": [
    "document.getElementById('blockSize').value='24'; startSim();"
  ],
  "expect": [
    "第2遍：一填充",
    "第3遍：随机填充"
  ],
  "ref": "startSim 同步 renderSteps(0) → stepList 渲染 DoD 三步列表（「第2遍：一填充」等）；判别态 clicks 清空 ⇒ stepList 为空，零交集。原 auto-restore 锚「24」是 byteGrid 随机字节值的概率性回显（撞值即逃生，2026-10-26 收紧为确定性步骤锚）。"
},
{
  "slug": "security/data-erase-simulator",
  "clicks": [
    "selectAlgo('gutmann');"
  ],
  "expect": [
    "标准依据 Gutmann 1996"
  ],
  "ref": "E3 引据徽标（2026-10-26）：#standardBadge 渲染选中算法的标准依据（strong 前缀+文本同元素连续）；clicks 切到 Gutmann → 徽标「标准依据　Gutmann 1996 论文…」。判别态 clicks 清空 → badge 回 DoD 引据；compareTable 虽全算法渲染 standard 列但无「标准依据　」前缀（跨元素被 \\n 分隔）⇒ 锚零交集。"
},
{
  "slug": "security/detector-45",
  "inputs": {
    "resistTime": "23",
    "steelThick": "1.2",
    "lockTime": "5",
    "envScore": "8"
  },
  "expect": [
    "23分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/earthquake-escape",
  "inputs": {
    "floorSelect": "mid"
  },
  "expect": [
    "mid"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "security/emergency-contacts",
  "inputs": {
    "customName": "测试王医生",
    "customPhone": "13800000000"
  },
  "clicks": [
    "addCustom()"
  ],
  "expect": [
    "测试王医生"
  ],
  "ref": "去默认化（原 expect「400-161-9995」＝核心应急联系人卡片恒显号码，注入失败仍命中 → 逃生项）：inputs 填自定义联系人姓名/电话后 clicks 调 addCustom()（window 全局，读输入框并写 localStorage+渲染 customList），customList 新增「测试王医生 / 13800000000」；默认 customList 为「暂无自定义联系人」，不含「测试王医生」，注入失败即不命中。 [被覆盖的前条说明：⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。]"
},
{
  "slug": "security/emergency-contacts",
  "inputs": {
    "customName": "A",
    "customPhone": "');globalThis.__ecPwn=1;//",
    "customNote": "<img src=x onerror=alert(1)>"
  },
  "clicks": [
    "addCustom();var h=String(document.getElementById('customList').innerHTML);document.getElementById('__tbProbe').textContent='ECINJ '+((h.indexOf('A')>=0&&h.indexOf('onclick')<0&&h.indexOf('callCustom')<0)?'OK':'BAD');"
  ],
  "expect": [
    "ECINJ OK"
  ],
  "ref": "2026-11-16（694 批）紧急联系人用户内容不得进入内联事件：电话带单引号+JS 时，旧实现把 escHtml 结果拼进 onclick=\"callCustom('…')\"（HTML 转义不转义 JS 字符串）⇒ 生成的列表 HTML 含 onclick 与 callCustom。现 renderCustom 用 createElement + textContent + addEventListener ⇒ 列表 HTML 无内联事件，且姓名 A 确实渲染证明 addCustom 分支执行。默认无自定义联系人 ⇒ 探针串不出现。"
},
{
  "slug": "security/virtual-safe",
  "clicks": [
    "document.getElementById('masterPwd').value='TestPass123456';unlockVault();document.getElementById('itemTitle').value='T';document.getElementById('itemContent').value='%41 中文 😀';addItem();var k=null;for(var i=0;i<localStorage.length;i++){var kk=localStorage.key(i);if(String(localStorage.getItem(kk)||'').indexOf('\"salt\"')>=0){k=kk;break;}}var arr=k?JSON.parse(localStorage.getItem(k)):[],bid=arr.length?'body_'+arr[0].id:'';if(bid)revealItem(arr[0].id);var txt=bid?String(document.getElementById(bid).textContent):'';document.getElementById('__tbProbe').textContent='ECRT '+((txt==='%41 中文 😀')?'OK':'BAD')+' N='+arr.length;"
  ],
  "expect": [
    "ECRT OK N=1"
  ],
  "ref": "2026-11-16（694 批）保险箱文本往返：新建保险箱后存入「%41 中文 😀」，revealItem 解出的明文必须逐字符一致。旧实现对 >255 的字符先 encodeURIComponent 再统一 decodeURIComponent ⇒ 明文里的 %41 被还原成 A；emoji 因 charAt 拆成孤立代理项直接抛 URIError。现按标准 UTF-8 字节加解密（密文带 v2: 前缀），旧记录仍按原口径解析，保证历史数据可读。"
},
{
  "slug": "security/first-aid-kit",
  "inputs": {},
  "clicks": [
    "selectScene('outdoor');generateList();"
  ],
  "expect": [
    "蛇药片"
  ],
  "ref": "clicks 注入：本页逻辑包在 IIFE 里，但把入口显式挂到了 window（selectScene / generateList / toggleItem / checkAll / uncheckAll）⇒ pageEval 与 harness 的 globalThis 导出都能调到。注意 selectScene() 只重渲场景卡，物品清单必须再显式 generateList() 才会渲染（少这一步则注入无输出，是本页最易踩的点）。注入后 selectedScene='outdoor'，清单渲染户外专属条目（蛇药片、防中暑药（藿香正气水）、净水片、急救指南卡片等），默认 selectedScene='home' 不产出这些名 ⇒ 零逃生项。旧锚「20片」是家庭包首项数量字面量 ⇒ 判别力 0。"
},
{
  "slug": "security/flood-level",
  "inputs": {
    "depthSlider": "7"
  },
  "expect": [
    "7cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/flood-level",
  "inputs": { "depthSlider": "7" },
  "clicks": ["applyFloodPreset('red')"],
  "expect": ["红色预警（≥200cm）"],
  "ref": "12-K9：红色预设旧值 250 落入紫色 ≥250cm 档，按钮文案却写「红色250cm」；现将红色预设改为 200，与 LEVELS/标尺一致。先注入 7cm 非默认值再点预设，默认态不出现该文案。"
},
{
  "slug": "security/smoke-alarm-test",
  "inputs": {
    "alarmLocation": "卧室"
  },
  "expect": [ "50016 要求住宅每间卧室内部或门外走" ],
  "ref": "auto-restore"
},
{
  "slug": "security/smoke-alarm-test",
  "inputs": {
    "alarmLocation": "厨房附近"
  },
  "expect": [
    "距烹饪区至少 3 米"
  ],
  "ref": "E3 引据徽标：选择「厨房附近」⇒ #alarmStdBadge 渲染该位置专属标准文案（距烹饪区至少 3 米、光电式优先）。默认态（客厅）badge 不含该串 ⇒ 强判别。badge 通用引据（GB 20517-2009 等）渲染不依赖输入，不可作 expect（A===B 盲区）。",
},
{
  "slug": "security/smoke-alarm-test",
  "inputs": {
    "alarmLocation": "地下室"
  },
  "expect": [
    "烟气易积聚"
  ],
  "ref": "E3 引据徽标第二位置锚：选择「地下室」⇒ badge 渲染地下室专属文案（逃生路径长、烟气易积聚、GB 50016 地下场所增设探测）。默认态（客厅）不含该串。",
},
{
  "slug": "security/typhoon-scale",
  "inputs": {
    "windInput": "45"
  },
  "expect": [
    "162.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "security/typhoon-scale",
  "inputs": {
    "windInput": "60"
  },
  "expect": [
    "（对应：超强台风）"
  ],
  "ref": "修复前 ≥51.0 m/s 的「超强台风」以 ≥ 开头，parseFloat 得 NaN，两个分支都不命中；现提取首个数值作下限，60 m/s 归入超强台风。默认 45 m/s 输出 162.0 km/h，且静态卡片无「（对应：…）」串。"
},
{
  "slug": "security/typhoon-scale",
  "inputs": {
    "windInput": ""
  },
  "expect": [
    "请输入 ≥0 的风速"
  ],
  "ref": "修复前风速清空或负数直接 return，结果区保留上一次换算与风级，易误读；现清空并提示，默认 45 m/s 正常出结果、不出现该文案。"
},
{
  "slug": "security/typhoon-scale",
  "clicks": [
    "document.getElementById('__tbProbe').textContent='BFUNIT='+(String(document.getElementById('beaufortList').innerHTML).indexOf('≥64 节')>=0?'OK':'BAD');"
  ],
  "expect": [
    "BFUNIT=OK"
  ],
  "ref": "修复前蒲福表 speed（节数范围）被标成 m/s 与「级」；现标注为「节」并附中值 m/s，12 级行为「≥64 节」。探针串仅 clicks 注入后出现。"
},
{
  "slug": "security/virtual-safe",
  "inputs": {},
  "clicks": [
    "document.getElementById('masterPwd').value='Abc12345!';unlockVault();"
  ],
  "expect": [
    "保险箱为空，添加你的第一条加密内容吧"
  ],
  "ref": "（2026-09-25 曾判「需 WebCrypto 派生密钥 ⇒ 结构性不可改造」，本批次推翻）unlockVault 是 window 导出的全局函数，未创建保险箱时走「首次创建」分支（setItem 是 harness 空桩，不影响分支选择），随后 showVault()→renderList() 渲染列表区 ⇒ 命中「保险箱为空，添加你的第一条加密内容吧」。默认态停在锁屏文案「请设置一个主密码来创建新的保险箱。」，两态区分。**注意**：强度计 updateStrength() 未导出到 window，不可直接调用。旧锚「请设置一个主密码来创建新的保险箱」正是默认态文案、判别力 0，已弃；itemContent 空 inputs 也一并移除（属无影响键，见 §10.5）。"
},
{
  "slug": "security/virtual-safe",
  "inputs": {
    "masterPwd": "Abc12345!"
  },
  "expect": [
    "NIST 800-63B：长度 ≥8 位即可"
  ],
  "ref": "E3 引据联动：主密码输入触发 updateStrength（masterPwd addEventListener input）⇒ #strengthLabel 追加 NIST SP 800-63B 长度建议行（动态串过 TBKit 双语 helper）。默认态密码为空 ⇒ strengthBox display:none、无该串，强判别。"
},
// ── 零覆盖攻坚：passphrase-generator（随机口令无锚，改锚确定性熵值行）──
{
  "slug": "security/passphrase-generator",
  "inputs": {
    "wc": "8"
  },
  "clicks": ["generate();"],
  "expect": ["约 59.2 位熵（基于 169 词库 / 8 词）"],
  "ref": "口令短语本身由 crypto.getRandomValues 逐词随机（无种子、无锚，不可断言）；但同一次渲染里的熵值行 "
     + "`熵 = log₂(WORDS.length) × wc` 是确定性派生量：WORDS 实测 169 词（页面 FORMULA 写的 170 为陈旧说明，以数组长度为准），"
     + "log₂(169) = 7.40088 ⇒ 8 × 7.40088 = 59.207 → toFixed(1) = 59.2，文本为「约 59.2 位熵（基于 169 词库 / 8 词）」。"
     + "默认 wc=5 且页面加载不自动生成 ⇒ 输出区为空；判别态清空 clicks ⇒ generate() 不执行，同样为空 ⇒ 零逃生。"
},
{ slug:"security/detector-45", inputs:{"resistTime":"","steelThick":"","lockTime":"","envScore":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" }
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

  console.log("==== security calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
