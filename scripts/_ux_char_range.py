#!/usr/bin/env python3
# _ux_char_range.py — UX 工具特异性功能重做 · F-CHAR-5
# 给「Breguet 航程」工具注入自包含的「这航程能飞到哪里」模块（航空专属，非通用距离参照）。
# 背景：页面输出航程 (km) / (n mile) 两个裸数值；grep「相当于|量级|参照」仅命中
#       「常见使用场景」「FAQ」两个标题 ⇒ 没有把航程换算成可感知的航线，是真缺口。
# 与 F-CHAR-1 通用距离量级表的区别（避免同质化）：
#   通用表给「跑道/珠峰/赤道/地月」等自然尺度；本表给**真实航线大圆距离**并逐条判定
#   「是否可达」，直接回答航空语境下的问题「这航程能飞到哪」，另补航空专属知识：
#   Breguet 为理论航程，实际运行还需航路余油 / 备降场 / 等待油量 / 风的折算。
# 沿用已验证模式：自包含 / 构建安全 / 静态无中文、JS 按 ?lang=en-US 填充。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charRange"'

# 典型航线大圆距离（km），由近到远
ROUTES = [
    ["北京—上海", "Beijing–Shanghai", 1067],
    ["上海—东京", "Shanghai–Tokyo", 1766],
    ["北京—广州", "Beijing–Guangzhou", 1898],
    ["北京—乌鲁木齐", "Beijing–Urumqi", 2423],
    ["上海—新加坡", "Shanghai–Singapore", 3800],
    ["北京—迪拜", "Beijing–Dubai", 5840],
    ["上海—悉尼", "Shanghai–Sydney", 7900],
    ["北京—伦敦", "Beijing–London", 8140],
    ["上海—法兰克福", "Shanghai–Frankfurt", 9200],
    ["上海—洛杉矶", "Shanghai–Los Angeles", 10400],
    ["北京—纽约", "Beijing–New York", 10990],
]


def build_section():
    rt_js = ",\n".join('    [%r, %r, %r]' % (a, b, c) for a, b, c in ROUTES)
    html = r'''<section class="char-module" id="__charRange" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charRangeTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charRangeDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="__charRangeVal" style="font-size:15px;font-weight:600;margin-bottom:10px;"></div>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead><tr>
      <th style="text-align:left;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charRangeTh1"></th>
      <th style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charRangeTh2"></th>
      <th style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);" id="__charRangeTh3"></th>
    </tr></thead>
    <tbody id="__charRangeRows"></tbody>
  </table>
  <p id="__charRangeNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
  var ROUTES = [
''' + rt_js + r'''
  ];
  function __crIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __crNum(id){
    var el = document.getElementById(id);
    if(!el) return NaN;
    return parseFloat(el.value);
  }
  // 与页面主公式一致：R = v * (L/D) / 9.81 * ln(Wi/Wf)  [m] → km
  function __crKm(){
    var v = __crNum('v'), ld = __crNum('ld'), wi = __crNum('wi'), wf = __crNum('wf');
    var isp = 6000;  // 与页面一致：Isp 取喷气发动机典型值 6000 s
    if(!isFinite(v) || !isFinite(ld) || !isFinite(wi) || !isFinite(wf)) return null;
    if(v <= 0 || ld <= 0 || wi <= 0 || wf <= 0 || wi <= wf) return null;
    var R = v * isp * ld * Math.log(wi / wf);
    if(!isFinite(R) || R <= 0) return null;
    return R / 1000;
  }
  function __crUpdate(){
    var en = __crIsEn();
    var val = document.getElementById('__charRangeVal');
    var tb = document.getElementById('__charRangeRows');
    var km = __crKm();
    if(km === null){
      if(val) val.textContent = en ? 'Enter valid speed, L/D and weights above (takeoff weight must exceed landing weight).' : '请先在上方填写有效的速度 / 升阻比 / 起飞与着陆重量（起飞重量须大于着陆重量）。';
      if(tb) tb.innerHTML = '';
      return;
    }
    var far = null;
    for(var i=0;i<ROUTES.length;i++){ if(ROUTES[i][2] <= km) far = ROUTES[i]; }
    if(val){
      val.textContent = (en ? 'Theoretical range: ' : '理论航程：') + km.toFixed(0) + ' km'
        + (far ? (en ? ' — up to ' : ' — 最远可直达 ') + (en ? far[1] : far[0]) : (en ? ' — shorter than any listed route' : ' — 短于表中任一航线'));
    }
    if(tb){
      var rows = '';
      for(var j=0;j<ROUTES.length;j++){
        var ok = ROUTES[j][2] <= km;
        rows += '<tr>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? ROUTES[j][1] : ROUTES[j][0]) + '</td>'
          + '<td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);">' + ROUTES[j][2] + ' km</td>'
          + '<td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);color:' + (ok ? '#16a34a' : '#dc2626') + ';">' + (ok ? (en ? 'Reachable' : '可达') : (en ? 'Not reachable' : '不可达')) + '</td>'
          + '</tr>';
      }
      tb.innerHTML = rows;
    }
  }
  function __crInit(){
    var en = __crIsEn();
    document.getElementById('__charRangeTitle').textContent = en
      ? '✈️ How Far Can This Range Actually Fly?'
      : '✈️ 这航程能飞到哪里';
    document.getElementById('__charRangeDesc').textContent = en
      ? 'Compares the computed range against real great-circle route distances, so the number turns into concrete destinations.'
      : '把算出的航程与真实航线大圆距离对照，让数字变成具体的目的地。';
    document.getElementById('__charRangeTh1').textContent = en ? 'Route' : '航线';
    document.getElementById('__charRangeTh2').textContent = en ? 'Great-circle distance' : '大圆距离';
    document.getElementById('__charRangeTh3').textContent = en ? 'Status' : '是否可达';
    document.getElementById('__charRangeNote').textContent = en
      ? 'The Breguet result is a still-air theoretical range: it excludes route reserve fuel, diversion to an alternate, holding fuel, taxi fuel, wind (headwind can cut effective range substantially) and airway detours. Real dispatch planning adds these margins on top, so treat this as an upper bound rather than an operable range.'
      : 'Breguet 结果为无风理论航程，不含航路余油、备降场油量、等待油量、滑行油量，也未计风的影响（逆风会显著缩短实际可达距离）与航路绕飞。航班实际放行计算需在此之上叠加这些余度，因此本结果应视为上限，而非可运行航程。';
    __crUpdate();
    ['v','ld','wi','wf'].forEach(function(id){
      var el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', __crUpdate);
      el.addEventListener('change', __crUpdate);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__crInit);
  else __crInit();
})();
</script>
'''
    return html


def inject(path):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return False
    sec = build_section()
    if '</body>' in s:
        s = s.replace('</body>', sec + '\n</body>', 1)
    else:
        s = s + sec
    open(path, 'w', encoding='utf-8').write(s)
    return True


def main():
    targets = sys.argv[1:] or ['tools/aerospace/breguet-range.html']
    done = skip = 0
    for t in targets:
        p = t if os.path.isabs(t) else os.path.join(ROOT, t)
        if not os.path.exists(p):
            print("MISS", t); continue
        if inject(p): done += 1
        else: skip += 1
    print("injected=%d skipped(already)=%d" % (done, skip))


if __name__ == '__main__':
    main()
