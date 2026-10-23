#!/usr/bin/env python3
# _ux_char_bmr.py — UX 工具特异性功能重做 · F-CHAR-2
# 给「基础代谢（BMR）类」工具注入一个自包含的「基础代谢热量去向」特征模块：
#   读页面已填的体重/身高/年龄/性别 → 按 Mifflin-St Jeor 复算 BMR →
#   按生理学典型占比拆解到各器官/组织（肝脏/大脑/骨骼肌/肾脏/心脏/脂肪/其他），
#   并给出「BMR 占 TDEE 约 60%-75%、不建议长期摄入低于 BMR」的领域提示。
# 设计要点（沿用 F-CHAR-1 已验证模式）：
#   1. 自包含：自带 section + script，不耦合页面主 calc；只读页面输入元素的值。
#   2. 构建安全：<section>（非 p，避开 _prerender_tool_body 首 p 覆写）置于 </body> 前；查重防重复。
#   3. 英文态零中文：静态 HTML 不放中文，全部文本由 JS 按 ?lang=en-US 填充；
#      EN 态全英文、ZH 态全中文（JS 内的中文串只在 ZH 分支使用，不进 EN DOM）。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charBmr"'   # 查重标记

# 各器官/组织占 BMR 的典型生理占比（成人静止状态，合计 1.00）
ORGANS = [
    ["肝脏", "Liver", 0.27],
    ["大脑", "Brain", 0.19],
    ["骨骼肌", "Skeletal muscle", 0.18],
    ["肾脏", "Kidneys", 0.10],
    ["心脏", "Heart", 0.07],
    ["脂肪组织", "Adipose tissue", 0.04],
    ["其他（胃肠/肺/皮肤等）", "Other (gut, lungs, skin, etc.)", 0.15],
]

def build_section():
    rows_js = ",\n".join('    [%r, %r, %r]' % (c, e, v) for c, e, v in ORGANS)
    # 静态 HTML 文本全部留空，由 JS 按语言填充
    html = r'''<section class="char-module" id="__charBmr" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charBmrTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charBmrDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="__charBmrVal" style="font-size:15px;font-weight:600;margin-bottom:10px;"></div>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead><tr>
      <th style="text-align:left;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charBmrTh1"></th>
      <th style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charBmrTh2"></th>
      <th style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charBmrTh3"></th>
    </tr></thead>
    <tbody id="__charBmrRows"></tbody>
  </table>
  <p id="__charBmrNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
  var ORGANS = [
''' + rows_js + r'''
  ];
  function __cbIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __cbNum(id){
    var el = document.getElementById(id);
    if(!el) return NaN;
    return parseFloat(el.value);
  }
  // 按 Mifflin-St Jeor 复算 BMR（与页面主公式一致）：男 10W+6.25H-5A+5；女 -161
  function __cbBmr(){
    var w = __cbNum('weight'), h = __cbNum('height'), a = __cbNum('age');
    var sexEl = document.getElementById('sex');
    var s = sexEl ? String(sexEl.value).toLowerCase() : '1';
    var isMale = (s==='1' || s==='m' || s==='male' || s==='男');
    if(!isFinite(w) || !isFinite(h) || !isFinite(a)) return NaN;
    if(w<=0 || h<=0 || a<=0) return NaN;
    return isMale ? (10*w + 6.25*h - 5*a + 5) : (10*w + 6.25*h - 5*a - 161);
  }
  function __cbUpdate(){
    var en = __cbIsEn();
    var bmr = __cbBmr();
    var val = document.getElementById('__charBmrVal');
    var tb = document.getElementById('__charBmrRows');
    if(!isFinite(bmr)){
      if(val) val.textContent = en ? 'Enter valid weight / height / age above.' : '请先在上方填写有效的体重 / 身高 / 年龄。';
      if(tb) tb.innerHTML = '';
      return;
    }
    if(val) val.textContent = (en ? 'Your BMR: ' : '你的 BMR：') + Math.round(bmr) + ' kcal/' + (en ? 'day' : '天');
    if(tb){
      var rows = '';
      for(var i=0;i<ORGANS.length;i++){
        var kcal = bmr * ORGANS[i][2];
        rows += '<tr>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? ORGANS[i][1] : ORGANS[i][0]) + '</td>'
          + '<td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);">' + (ORGANS[i][2]*100).toFixed(0) + '%</td>'
          + '<td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);">' + Math.round(kcal) + ' kcal</td>'
          + '</tr>';
      }
      tb.innerHTML = rows;
    }
  }
  function __cbInit(){
    var en = __cbIsEn();
    document.getElementById('__charBmrTitle').textContent = en
      ? '🔥 Where Your Basal Calories Go'
      : '🔥 基础代谢的热量去向';
    document.getElementById('__charBmrDesc').textContent = en
      ? 'Estimated organ-by-organ breakdown of your basal metabolic rate, based on typical physiological shares.'
      : '你的基础代谢（BMR）按生理学典型占比，主要消耗在各器官/组织的估算拆解。';
    document.getElementById('__charBmrTh1').textContent = en ? 'Organ / Tissue' : '器官/组织';
    document.getElementById('__charBmrTh2').textContent = en ? 'Share' : '占比';
    document.getElementById('__charBmrTh3').textContent = en ? 'kcal/day' : 'kcal/天';
    document.getElementById('__charBmrNote').textContent = en
      ? 'BMR is the energy your body burns at complete rest, typically 60%–75% of total daily expenditure (TDEE). Eating below BMR for long periods may trigger metabolic adaptation (the body down-regulates basal burn), so most guidelines advise against sustained intake under BMR. Figures above are typical population averages, not individual measurements.'
      : 'BMR 是人体完全静息状态下的最低能耗，通常占每日总消耗（TDEE）的 60%–75%。长期摄入低于 BMR 可能引发代谢适应（身体下调基础消耗），因此多数指南不建议长期把摄入压到 BMR 以下。表中占比为人群典型平均值，非个体实测。';
    __cbUpdate();
    // 跟随页面输入联动（不覆盖页面已有的 oninput/onchange）
    ['weight','height','age','sex'].forEach(function(id){
      var el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', __cbUpdate);
      el.addEventListener('change', __cbUpdate);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__cbInit);
  else __cbInit();
})();
</script>
'''
    return html

def inject(path):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return False  # 已注入，跳过
    sec = build_section()
    if '</body>' in s:
        s = s.replace('</body>', sec + '\n</body>', 1)
    else:
        s = s + sec
    open(path, 'w', encoding='utf-8').write(s)
    return True

def main():
    targets = sys.argv[1:] or []
    if not targets:
        print("usage: _ux_char_bmr.py <tool1.html> [tool2.html] ...")
        sys.exit(1)
    done = 0
    skip = 0
    for t in targets:
        p = t if os.path.isabs(t) else os.path.join(ROOT, t)
        if not os.path.exists(p):
            print("MISS", t); continue
        if inject(p): done += 1
        else: skip += 1
    print("injected=%d skipped(already)=%d" % (done, skip))

if __name__ == '__main__':
    main()
