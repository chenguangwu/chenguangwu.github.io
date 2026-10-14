#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX-Q4 薄弱页「本地记录 / 趋势 / 导出」改造器（A 档：不碰计算内核）。

背景：全站 16 个 score<=2 的薄弱页都是「游戏 / 答题 / 展示」页，没有输入控件，
通用 calcTool 接线器（scripts/_ux_wire.py）套不上，只能逐页精做。

本脚本做的事（每页）：
  ① 在结果区之后插入一张「成绩趋势与历史记录」卡片（趋势图 + 记录表 + 提示条）
  ② 页面尾部注入共享脚本：记录 → 趋势 → 表格 → 导出 CSV / 清空（数据仅存本机）
  ③ 包装页面原有的「出结果」函数（finishQuiz / renderResult / showScore / calc …），
     出结果后自动落一条历史（首次用户交互后才记账，避免页面加载时的自动 calc 污染）

守卫：全部调用点 `typeof TBKit==='undefined'` 保护；i18n 走 TBKit.util.isEn()；
幂等：已含 tbHistCard 的页直接跳过。
用法：python3 scripts/_ux_hist.py [--apply] [--only cat/slug]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHARED_JS = r"""
/* ═════ 本地记录 · 趋势 · 导出（数据只存本机浏览器，不上传服务器） ═════ */
var __tbDict = {
  '时间':['Time','时间'], '得分':['Score','得分'], '正确率':['Accuracy','正确率'],
  '错题数':['Wrong','错题数'], '结果':['Result','结果'], '用时':['Duration','用时'],
  '步数':['Moves','步数'], '难度':['Level','难度'], '模式':['Mode','模式'],
  '评级':['Grade','评级'], '等级':['Grade','等级'], '备注':['Note','备注'],
  '名称':['Name','名称'], '数值':['Value','数值'], '详情':['Detail','详情'],
  '局数':['Rounds','局数'], '正确':['Correct','正确'], '错误':['Wrong','错误'],
  '总分':['Total','总分'], '题数':['Questions','题数'], '答对':['Correct','答对'],
  '分级':['Level','分级'], '高危项':['Top risks','高危项'], '设备':['Device','设备'],
  '系统':['OS','系统'], '分辨率':['Resolution','分辨率'], '语言':['Language','语言'],
  '剩余':['Remaining','剩余'], '日期':['Date','日期'], '类型':['Type','类型'],
  '节日':['Festival','节日'], '星期':['Weekday','星期'], '剩余天数':['Days left','剩余天数'],
  '最近节日':['Next event','最近节日'], '核心':['CPU cores','核心'], '浏览器':['Browser','浏览器'],
  '时长':['Length','时长'], '曲目':['Track','曲目'], '按键':['Keys','按键'],
  '命中':['Hits','命中'], '准确率':['Accuracy','准确率'], '速度':['Speed','速度'],
  '关卡':['Stage','关卡'], '连击':['Combo','连击'], '字符':['Character','字符'],
  '笔顺':['Stroke order','笔顺'], '成语':['Idiom','成语'], '回合':['Rounds','回合']
};
function __tbL(en, zh){ return (typeof TBKit !== 'undefined' && TBKit.util.isEn()) ? en : zh; }
function __tbTr(k){ var d = __tbDict[k]; return d ? __tbL(d[0], d[1]) : k; }
function __tbTime(){
  var d = new Date();
  function p(x){ return (x < 10 ? '0' : '') + x; }
  return p(d.getMonth()+1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
}
/* 首次真实交互后才记账：避免页面加载时的自动 calc / 自动开局写进历史 */
function __tbArm(){
  if (window.__tbArmed) return;
  window.__tbArmed = true;
  try {
    document.removeEventListener('pointerdown', __tbArm);
    document.removeEventListener('keydown', __tbArm);
    document.removeEventListener('change', __tbArm);
  } catch (e) {}
}
try {
  document.addEventListener('pointerdown', __tbArm);
  document.addEventListener('keydown', __tbArm);
  document.addEventListener('change', __tbArm);
} catch (e) {}
function __tbHistSave(rec){
  if (typeof TBKit === 'undefined' || !rec || !window.__tbArmed) return;
  try { TBKit.history.record(rec, window.__tbCoalesce || 0); } catch (e) {}
  __tbHistRender();
}
function __tbHistRender(){
  if (typeof TBKit === 'undefined') return;
  var box = document.getElementById('tbHistTable');
  if (!box) return;
  var cbox = document.getElementById('tbHistChart');
  var tip = document.getElementById('tbHistTip');
  var arr = TBKit.history.list();
  if (!arr.length) {
    box.innerHTML = '<p style="font-size:12px;color:var(--text-muted);">' +
      __tbL('No records yet — finish one round and it will be saved on this device.',
            '暂无记录，完成一次后自动保存在本机。') + '</p>';
    if (cbox) cbox.innerHTML = '';
    if (tip) tip.innerHTML = '';
    return;
  }
  var head = [];
  for (var k0 in arr[0].d) {
    if (k0 === '__v') continue;
    if (Object.prototype.hasOwnProperty.call(arr[0].d, k0)) head.push(k0);
  }
  var rows = [], pts = [], labels = [];
  for (var i = 0; i < arr.length; i++) {
    var d = arr[i].d || {};
    var row = [];
    for (var j = 0; j < head.length; j++) row.push(d[head[j]] == null ? '' : String(d[head[j]]));
    rows.push(row);
    pts.push(typeof d.__v === 'number' ? d.__v : 0);
    labels.push('#' + (arr.length - i));
  }
  rows.reverse(); pts.reverse(); labels.reverse();
  if (!window.__tbNoChart && cbox && TBKit.chart && TBKit.chart.line) {
    try { TBKit.chart.line(cbox, { labels: labels, series: [{ name: __tbL('Trend', '趋势'), data: pts }] }); } catch (e) {}
  }
  try { TBKit.matrix.table(box, { head: head.map(__tbTr), rows: rows }); } catch (e) {}
  if (tip) {
    var df = null;
    try { df = TBKit.history.diffLast(['__v']); } catch (e) {}
    if (df && df.__v) {
      var dv = df.__v.delta;
      tip.innerHTML = '<div class="tip-box ' + (dv > 0 ? 'tip-success' : (dv < 0 ? 'tip-error' : 'tip-warn')) +
        '">' + __tbL('Change vs last round: ', '较上次：') + (dv > 0 ? '+' : '') + dv + '</div>';
    } else { tip.innerHTML = ''; }
  }
}
function __tbHistExport(){
  if (typeof TBKit === 'undefined') return;
  var ok = false;
  try { ok = TBKit.util.exportTable('#tbHistTable', window.__tbCsvName || 'history.csv'); } catch (e) {}
  if (!ok && typeof ToolBox !== 'undefined' && ToolBox.toast) {
    try { ToolBox.toast(__tbL('No records to export yet', '暂无可导出的记录')); } catch (e) {}
  }
}
function __tbHistClear(){
  if (typeof TBKit === 'undefined') return;
  try { TBKit.history.clear(); } catch (e) {}
  __tbHistRender();
}
function __tbHistInit(){
  try {
    var h = document.getElementById('tbHistTitle');
    if (h) h.textContent = __tbL(window.__tbEnTitle || 'Trend & History', window.__tbZhTitle || '成绩趋势与历史记录');
    var p = document.getElementById('tbHistSub');
    if (p) p.textContent = __tbL('Every round is saved locally on this device only. Export CSV for backup or clear anytime.',
                                 '每次完成后自动保存在本机浏览器，可导出 CSV 备份或随时清空。');
    var b1 = document.getElementById('tbExpBtn');
    if (b1) b1.textContent = __tbL('Export CSV', '导出 CSV');
    var b2 = document.getElementById('tbClrBtn');
    if (b2) b2.textContent = __tbL('Clear records', '清空记录');
    var xl = window.__tbExtraLabels || {};
    for (var xid in xl) {
      if (!Object.prototype.hasOwnProperty.call(xl, xid)) continue;
      var xb = document.getElementById(xid);
      if (xb) xb.textContent = __tbL(xl[xid][0], xl[xid][1]);
    }
  } catch (e) {}
  __tbHistRender();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', __tbHistInit);
else setTimeout(__tbHistInit, 0);
"""

CARD_HTML = """
  <div class="card" id="tbHistCard">
    <h3 id="tbHistTitle">📈 成绩趋势与历史记录</h3>
    <p id="tbHistSub" style="font-size:12px;color:var(--text-muted);">每次完成后自动保存在本机浏览器，可导出 CSV 备份或随时清空。</p>
    __EXTRA_DIV__
    <div id="tbHistChart"></div>
    <div id="tbHistTip"></div>
    <div id="tbHistTable"></div>
    <div class="toolbar" style="margin-top:12px;">
      __EXTRA_BTNS__
      <button type="button" class="btn" id="tbExpBtn" onclick="window.__tbHistExport()">导出 CSV</button>
      <button type="button" class="btn" id="tbClrBtn" onclick="window.__tbHistClear()">清空记录</button>
    </div>
  </div>
"""


def wrap_js(fn, rec):
    return (
        "\n/* 出结果后自动落一条本机记录（包装原 %s，不改其计算逻辑） */\n"
        "var __tbF_%s = (typeof %s === 'function') ? %s : null;\n"
        "if (__tbF_%s) {\n"
        "  %s = function () {\n"
        "    var __r = __tbF_%s.apply(null, arguments);\n"
        "    try { __tbHistSave(%s); } catch (e) {}\n"
        "    return __r;\n"
        "  };\n"
        "}\n" % (fn, fn, fn, fn, fn, fn, fn, rec)
    )


def preset_js(host, presets, after):
    """presets: [{label, labelEn, values:{id:val}}]"""
    items = []
    for p in presets:
        vals = ", ".join("'%s':'%s'" % (k, v) for k, v in p["values"].items())
        items.append("    { label: '%s', labelEn: '%s', values: {%s} }" % (p["label"], p["labelEn"], vals))
    return (
        "\n/* 常见场景一键填充 */\n"
        "function __tbPresets(){\n"
        "  if (typeof TBKit === 'undefined' || !TBKit.preset) return;\n"
        "  try {\n"
        "    TBKit.preset.bar('#%s', [\n%s\n    ], function () { try { %s(); } catch (e) {} });\n"
        "  } catch (e) {}\n"
        "}\n"
        "if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', __tbPresets);\n"
        "else setTimeout(__tbPresets, 0);\n" % (host, ",\n".join(items), after)
    )


# ─────────────────────────── 页面配置 ───────────────────────────
PAGES = [
    {
        "path": "tools/safety/safety-quiz.html",
        "csv": "safety-quiz-history.csv",
        "title_zh": "📈 自测成绩趋势与历史记录",
        "title_en": "📈 Quiz Score Trend & History",
        "wrap": ("finishQuiz",
                 "(function(){var n=qOrder.length||1;var p=Math.round(score/n*100);"
                 "return {时间:__tbTime(),得分:score+'/'+n,正确率:p+'%',错题数:wrongList.length,__v:p};})()"),
    },
    {
        "path": "tools/safety/self-test.html",
        "csv": "self-test-history.csv",
        "title_zh": "📈 自测成绩趋势与历史记录",
        "title_en": "📈 Self-Test Score Trend & History",
        "wrap": ("renderResult",
                 "(function(){var c=0;for(var i=0;i<currentQuiz.length;i++){if(userAnswers[i]===currentQuiz[i].a)c++;}"
                 "var s=c*10;return {时间:__tbTime(),得分:s,答对:c+'/'+currentQuiz.length,"
                 "评级:__tbL(s>=80?'Excellent':(s>=60?'Pass':'Fail'),s>=80?'优秀':(s>=60?'合格':'不合格')),__v:s};})()"),
    },
    {
        "path": "tools/tcm-diagnosis/misdiagnosis-training.html",
        "csv": "misdiagnosis-training-history.csv",
        "title_zh": "📈 训练成绩趋势与历史记录",
        "title_en": "📈 Training Score Trend & History",
        "wrap": ("showScore",
                 "(function(){var c=0;for(var i=0;i<CASES.length;i++){if(userAnswers[i]===CASES[i].correct)c++;}"
                 "var p=Math.round(c/CASES.length*100);"
                 "return {时间:__tbTime(),答对:c+'/'+CASES.length,正确率:p+'%',__v:p};})()"),
    },
    {
        "path": "tools/dentistry/rater-risk-2.html",
        "csv": "cariogram-history.csv",
        "title_zh": "📈 评估记录与风险趋势",
        "title_en": "📈 Assessment Records & Risk Trend",
        "wrap": ("calc",
                 "(function(){var t=0,h=[];for(var i=0;i<DIMS.length;i++){"
                 "var el=document.getElementById('d_'+DIMS[i].key);if(!el)continue;var v=+el.value;t+=v;"
                 "if(v===2)h.push(DIMS[i].name.split('（')[0]);}"
                 "return {时间:__tbTime(),总分:t+'/14',"
                 "分级:__tbL(t<=3?'Low':(t<=8?'Medium':'High'),t<=3?'低风险':(t<=8?'中风险':'高风险')),"
                 "高危项:h.join('、')||__tbL('none','无'),__v:t};})()"),
        "preset_host": "tbPre",
        "preset_after": "calc",
        "preset_before": '    <div id="items"></div>',
        "presets": [
            {"label": "低风险示例（全部最优）", "labelEn": "Low risk (all optimal)",
             "values": {"d_exp": "0", "d_ms": "0", "d_diet": "0", "d_plaque": "0",
                        "d_fluoride": "0", "d_flow": "0", "d_buffer": "0"}},
            {"label": "中风险示例（口腔卫生一般）", "labelEn": "Medium risk (average hygiene)",
             "values": {"d_exp": "1", "d_ms": "1", "d_diet": "1", "d_plaque": "1",
                        "d_fluoride": "1", "d_flow": "0", "d_buffer": "1"}},
            {"label": "高风险示例（多因素叠加）", "labelEn": "High risk (multi-factor)",
             "values": {"d_exp": "2", "d_ms": "2", "d_diet": "2", "d_plaque": "2",
                        "d_fluoride": "2", "d_flow": "1", "d_buffer": "2"}},
        ],
    },
    {
        "path": "tools/fun/gomoku-ai.html",
        "csv": "gomoku-history.csv",
        "title_zh": "📈 对战战绩与历史记录",
        "title_en": "📈 Match Records & History",
        "inject": "block",
        "wrap": ("place",
                 "(function(){var win=(typeof checkWin==='function')&&checkWin(r,c,color);"
                 "var full=history.length===SIZE*SIZE;if(!win&&!full)return null;"
                 "return {时间:__tbTime(),结果:__tbL(win?(color===BLACK?'Win':'Lose'):'Draw',"
                 "win?(color===BLACK?'胜':'负'):'和棋'),步数:history.length,__v:history.length};})()"),
    },
    {
        "path": "tools/fun/minesweeper.html",
        "csv": "minesweeper-history.csv",
        "title_zh": "📈 扫雷战绩与历史记录",
        "title_en": "📈 Minesweeper Records & History",
        "hook_anchor": "})();",
        "hook": (
            "  /* 一局结束（胜/负）自动落一条本机记录 */\n"
            "  var __tbF_showOverlay = (typeof showOverlay === 'function') ? showOverlay : null;\n"
            "  if (__tbF_showOverlay) {\n"
            "    showOverlay = function (result) {\n"
            "      var __r = __tbF_showOverlay.apply(null, arguments);\n"
            "      try { window.__tbHistSave({ 时间: window.__tbTime(), 难度: getDiffLabel(),\n"
            "        结果: window.__tbL(result === 'won' ? 'Win' : 'Lose', result === 'won' ? '胜利' : '失败'),\n"
            "        用时: formatTime(elapsedTime), __v: elapsedTime }); } catch (e) {}\n"
            "      return __r;\n"
            "    };\n"
            "  }\n"),
    },
    {
        "path": "tools/it/device-info.html",
        "csv": "device-info-snapshots.csv",
        "title_zh": "📈 设备快照记录与对比",
        "title_en": "📈 Device Snapshots & Comparison",
        "extra_div": False,
        "extra_btns": [("tbSaveBtn", "__tbDevSave", "保存本次快照"),
                       ("tbCopyBtn", "__tbDevCopy", "复制全部信息")],
        "extra_js": r"""
function __tbDevRec(){
  var na = navigator || {}, sc = screen || {};
  return {时间:__tbTime(), 系统:(na.platform||''), 分辨率:(sc.width||0)+'x'+(sc.height||0),
          语言:na.language||'', 核心:na.hardwareConcurrency||'', __v:(+na.hardwareConcurrency)||0};
}
function __tbDevSave(){ window.__tbArmed = true; __tbHistSave(__tbDevRec()); }
function __tbDevCopy(){
  var ids = ['screenInfo','browserInfo','localeInfo','deviceStatus','uaBox'], out = [];
  for (var i = 0; i < ids.length; i++) {
    var el = document.getElementById(ids[i]);
    if (el && el.textContent) out.push(el.textContent.replace(/\s+/g, ' ').trim());
  }
  var t = out.join('\n');
  if (!t) return;
  if (typeof TBKit !== 'undefined' && TBKit['export'] && TBKit['export'].copy) { TBKit['export'].copy(t); return; }
  try { navigator.clipboard.writeText(t); } catch (e) {}
}
window.__tbExtraLabels = {tbSaveBtn:['Save snapshot','保存本次快照'], tbCopyBtn:['Copy all info','复制全部信息']};
""",
    },
    {
        "path": "tools/life/event-countdown.html",
        "csv": "event-countdown.csv",
        "title_zh": "📈 倒计时记录与节日总表",
        "title_en": "📈 Countdown Records & Festival Table",
        "inject": "block",
        "extra_div": True,
        "extra_btns": [("tbSaveBtn", "__tbCdSave", "记录当前倒计时")],
        "extra_js": r"""
var WEEK = ['周日','周一','周二','周三','周四','周五','周六'];
function __tbCdList(){
  var now = new Date(); now.setHours(0,0,0,0); var rows = [];
  for (var i = 0; i < events.length; i++) {
    var d = getNextEvent(events[i].getNext);
    if (!d) continue;
    rows.push([events[i].name, fmtDate(d), WEEK[d.getDay()], String(Math.round((d - now) / 86400000))]);
  }
  rows.sort(function(a,b){ return (+a[3]) - (+b[3]); });
  return rows;
}
function __tbCdTable(){
  if (typeof TBKit === 'undefined') return;
  try { TBKit.matrix.table('#tbExtra', { head: [__tbL('Festival','节日'), __tbL('Date','日期'),
        __tbL('Weekday','星期'), __tbL('Days left','剩余天数')], rows: __tbCdList() }); } catch (e) {}
}
function __tbCdSave(){
  window.__tbArmed = true;
  var l = __tbCdList();
  if (!l.length) return;
  __tbHistSave({时间:__tbTime(), 最近节日:l[0][0], 日期:l[0][1], 剩余天数:l[0][3], __v:(+l[0][3])||0});
}
window.__tbHistExport = function(){
  if (typeof TBKit === 'undefined') return;
  var ok = false;
  try { ok = TBKit.util.exportTable('#tbExtra', window.__tbCsvName || 'event-countdown.csv'); } catch (e) {}
  if (!ok) { try { ok = TBKit.util.exportTable('#tbHistTable', window.__tbCsvName); } catch (e) {} }
};
window.__tbExtraLabels = {tbSaveBtn:['Save countdown','记录当前倒计时']};
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', __tbCdTable);
else setTimeout(__tbCdTable, 0);
""",
    },
]


def container_end(s, start):
    """从 s[start] 处（应为 <div ...> 起点）找到配对的 </div> 结束偏移。"""
    depth = 0
    i = start
    while i < len(s):
        lt = s.find("<", i)
        if lt < 0:
            break
        if s.startswith("</div", lt):
            gt = s.find(">", lt)
            depth -= 1
            i = gt + 1
            if depth == 0:
                return lt
            continue
        if s.startswith("<div", lt):
            gt = s.find(">", lt)
            depth += 1
            i = gt + 1
            continue
        i = lt + 1
    return -1


def apply_page(cfg, apply):
    path = os.path.join(ROOT, cfg["path"])
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if "tbHistCard" in s:
        print("SKIP(already) %s" % cfg["path"])
        return False
    body_i = s.find("<body")
    if body_i < 0:
        print("SKIP(no body) %s" % cfg["path"])
        return False
    body = s[body_i:]

    # ① 插入历史卡片
    pos = -1
    for anchor in ("<!-- 注意事项区块 -->", "<!-- TOOLBOX-DEEP-DIVE -->"):
        a = body.find(anchor)
        if a > 0:
            pos = a
            break
    if pos < 0:
        c = body.find('<div class="container">')
        if c >= 0:
            pos = container_end(body, c)
    if pos < 0:
        print("SKIP(no anchor) %s" % cfg["path"])
        return False
    card = CARD_HTML.replace("成绩趋势与历史记录", cfg.get("title_zh", "成绩趋势与历史记录"), 1)
    extra_div = '    <div id="tbExtra"></div>\n' if cfg.get("extra_div") else ""
    extra_btns = ""
    for b in cfg.get("extra_btns", []):
        extra_btns += ('      <button type="button" class="btn" id="%s" onclick="window.%s()">%s</button>\n'
                       % (b[0], b[1], b[2]))
    card = card.replace("__EXTRA_DIV__", extra_div).replace("__EXTRA_BTNS__", extra_btns)
    body = body[:pos] + card + "\n" + body[pos:]

    # ② 预设容器（可选）
    if cfg.get("preset_before"):
        pb = body.find(cfg["preset_before"])
        if pb < 0:
            print("SKIP(preset anchor missing) %s" % cfg["path"])
            return False
        body = body[:pb] + '    <div id="%s"></div>\n' % cfg["preset_host"] + body[pb:]

    # ③ 注入脚本
    js = SHARED_JS
    js += "\nwindow.__tbCsvName = '%s';\n" % cfg.get("csv", "history.csv")
    js += "\nwindow.__tbZhTitle = \"%s\";\nwindow.__tbEnTitle = \"%s\";\n" % (
        cfg.get("title_zh", "成绩趋势与历史记录"), cfg.get("title_en", "Trend & History"))
    if cfg.get("no_chart"):
        js += "\nwindow.__tbNoChart = 1;\n"
    if cfg.get("coalesce"):
        js += "\nwindow.__tbCoalesce = %d;\n" % cfg["coalesce"]
    if cfg.get("wrap"):
        js += wrap_js(cfg["wrap"][0], cfg["wrap"][1])
    if cfg.get("presets"):
        js += preset_js(cfg["preset_host"], cfg["presets"], cfg.get("preset_after", "calc"))
    if cfg.get("extra_js"):
        js += "\n" + cfg["extra_js"] + "\n"

    hook = cfg.get("hook")

    if cfg.get("inject") == "block":
        # 追加到 body 内最长的 script 块末尾（页面用 let/const 声明内部变量时，
        # 跨 script 块的词法共享在 verify 沙箱里不成立，必须同块注入）
        best = None
        best_len = 0
        for m in re.finditer(r"(<script\b[^>]*>)(.*?)(</script>)", body, flags=re.S | re.I):
            if len(m.group(2)) > best_len:
                best, best_len = m, len(m.group(2))
        if not best or best_len < 200:
            print("SKIP(no main script block) %s" % cfg["path"])
            return False
        anchor = cfg.get("hook_anchor")
        if hook and anchor:
            seg = best.group(2)
            k = seg.rfind(anchor)
            if k < 0:
                print("SKIP(hook anchor missing) %s" % cfg["path"])
                return False
            newseg = seg[:k] + "\n" + js + "\n" + hook + "\n" + seg[k:]
        else:
            newseg = best.group(2) + "\n" + js + "\n" + (hook or "")
        body = body[:best.start(2)] + newseg + body[best.end(2):]
    else:
        bi = body.rfind("</body>")
        if bi < 0:
            print("SKIP(no </body>) %s" % cfg["path"])
            return False
        # 先定位主 script 块（必须在注入共享块之前，否则会选中刚注入的共享块）
        best = None
        best_len = 0
        for m in re.finditer(r"(<script\b[^>]*>)(.*?)(</script>)", body, flags=re.S | re.I):
            if len(m.group(2)) > best_len:
                best, best_len = m, len(m.group(2))
        body = body[:bi] + "<script>\n" + js + "\n</script>\n" + body[bi:]
        if hook:
            anchor = cfg.get("hook_anchor")
            if anchor:
                seg = best.group(2)
                k = seg.rfind(anchor)
                if k < 0:
                    print("SKIP(hook anchor missing) %s" % cfg["path"])
                    return False
                body = body[:best.start(2)] + seg[:k] + "\n" + hook + "\n" + seg[k:] + body[best.end(2):]
            else:
                body = body[:best.end(2)] + "\n" + hook + "\n" + body[best.end(2):]

    out = s[:body_i] + body
    if apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        print("APPLIED %s" % cfg["path"])
    else:
        print("WOULD-APPLY %s" % cfg["path"])
    return True


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    only = None
    if "--only" in args:
        only = args[args.index("--only") + 1]
    n = 0
    for cfg in PAGES:
        if only and not cfg["path"].endswith(only + ".html") and only not in cfg["path"]:
            continue
        if apply_page(cfg, apply):
            n += 1
    print("done: %d page(s) %s" % (n, "applied" if apply else "dry-run"))


if __name__ == "__main__":
    main()
