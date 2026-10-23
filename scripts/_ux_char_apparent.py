#!/usr/bin/env python3
# _ux_char_apparent.py — UX 工具特异性功能重做 · F-CHAR-3
# 给「体感温度（Steadman AT）类」工具注入自包含的「体感分级 + 健康提示 + 穿衣建议」模块。
# 背景：该页 meta description 自述「用于高温高湿或风寒环境下的健康提示与穿衣建议」，
#       但页面正文只有裸 AT 数值 + 水汽压 + 温差，完全没有分级/提示/建议 ⇒ 承诺未实现，属真缺口。
# 模块内容（领域专属，非通用图表/导出套壳）：
#   1. 复算 AT（与页面主公式一致：e=(RH/100)*6.105*exp(17.27T/(237.7+T))，AT=T+0.33e-0.70ws-4.0）
#   2. 按 AT 落档到 10 级体感分级（极热/炎热/热/偏热/舒适/凉爽/较冷/冷/寒冷/极寒），给出健康提示
#   3. 按档位给出穿衣建议
#   4. 成因解读：Δ=AT−T 判湿热（+）或风寒（−），说明为什么感觉和气温不同
# 沿用 F-CHAR-1/2 已验证模式：自包含 / 构建安全 / 静态无中文、JS 按 ?lang=en-US 填充。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charApparent"'   # 查重标记

# (下限℃, 中文档名, 英文档名, 颜色, 中文健康提示, 英文健康提示, 中文穿衣, 英文穿衣)
# 顺序由高到低，命中第一个 AT>=下限 的档位。
LEVELS = [
    [40, "极热", "Extreme heat", "#b91c1c",
     "热射病高风险：体温调节可能失控，避免户外活动，警惕头晕、恶心、停止出汗等信号。",
     "High risk of heat stroke: thermoregulation may fail. Avoid outdoor activity; watch for dizziness, nausea, or cessation of sweating.",
     "尽量避免外出；如需外出选清晨/傍晚，戴宽檐帽、透气浅色衣物，持续补水与电解质。",
     "Stay indoors if possible; if you must go out, choose early morning or evening, wear a wide-brim hat and light breathable clothing, and keep hydrating with electrolytes."],
    [35, "炎热", "Hot", "#dc2626",
     "易中暑：长时间户外有热衰竭风险，需主动降温与补水。",
     "Heat exhaustion is likely with prolonged exposure. Take active cooling breaks and drink water regularly.",
     "短袖透气衣物 + 防晒；每 20-30 分钟补水，尽量在遮阴处活动。",
     "Light breathable clothing plus sun protection; drink water every 20-30 minutes and stay in shade where possible."],
    [30, "热", "Warm", "#ea580c",
     "偏热：长时间活动会明显出汗，注意补水防脱水。",
     "Warm: noticeable sweating during activity. Keep hydrated to avoid dehydration.",
     "短袖即可，注意透气；户外工作者应安排轮休与饮水。",
     "Short sleeves are fine; prioritise breathability. Outdoor workers should schedule rest and water breaks."],
    [25, "偏热", "Mildly warm", "#f59e0b",
     "多数人感觉偏热，但仍在可耐受范围，敏感人群注意通风。",
     "Most people feel mildly warm but still within tolerance; sensitive groups should ensure ventilation.",
     "轻薄单层衣物；室内可开窗或低速风扇。",
     "Single light layer; open windows or use a low-speed fan indoors."],
    [20, "舒适", "Comfortable", "#16a34a",
     "最适宜区间：人体热平衡最佳，适合户外活动。",
     "Optimal range: the body is in its best thermal balance, ideal for outdoor activity.",
     "单层长袖或短袖均可，无需特别保暖或降温。",
     "A single layer (short or long sleeve) is fine; no special warming or cooling needed."],
    [15, "凉爽", "Cool", "#0d9488",
     "凉爽舒适，久坐或体弱者可能偏凉，注意添衣。",
     "Cool and pleasant, but may feel chilly when seated still or for frail individuals; add a layer.",
     "长袖 + 薄外套，早晚温差大时随身备一件。",
     "Long sleeves plus a light jacket; carry an extra layer when day-night温差 is large."],
    [5, "较冷", "Chilly", "#0284c7",
     "明显偏冷，血管收缩、关节不适人群需注意保暖。",
     "Distinctly chilly; people with poor circulation or joint issues should keep warm.",
     "外套 + 长裤；风大时加防风层。",
     "Jacket and long trousers; add a windproof layer when it is windy."],
    [-5, "冷", "Cold", "#2563eb",
     "寒冷：长时间暴露有感冒与呼吸道刺激风险。",
     "Cold: prolonged exposure raises the risk of colds and airway irritation.",
     "冬装外套 + 毛衣，头部与手部保暖。",
     "Winter coat plus sweater; keep head and hands covered."],
    [-15, "寒冷", "Very cold", "#1d4ed8",
     "低温风险：外周血管强烈收缩，手指/耳廓冻伤风险上升。",
     "Low-temperature risk: strong peripheral vasoconstriction raises frostbite risk for fingers and ears.",
     "厚羽绒/棉服 + 手套、帽子、围巾，减少皮肤裸露。",
     "Heavy down or padded coat with gloves, hat and scarf; minimise exposed skin."],
    [-999, "极寒", "Extreme cold", "#3730a3",
     "冻伤与失温高风险：裸露皮肤可在数十分钟内冻伤，必须全面防护并缩短暴露时间。",
     "High risk of frostbite and hypothermia: exposed skin can freeze within tens of minutes. Full protection and shortened exposure are essential.",
     "全面防寒：保暖内衣 + 厚外套 + 防风外层，手套帽子面罩齐全，避免长时间户外。",
     "Full cold protection: thermal base layer, heavy coat and windproof shell, with gloves, hat and face covering. Avoid prolonged time outdoors."],
]


def build_section():
    lv_js = ",\n".join(
        '    [%r, %r, %r, %r, %r, %r, %r, %r]' % (a, b, c, d, e, f, g, h)
        for a, b, c, d, e, f, g, h in LEVELS
    )
    html = r'''<section class="char-module" id="__charApparent" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charAppTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charAppDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="__charAppBadge" style="display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-size:13px;font-weight:600;margin-bottom:4px;"></div>
  <div id="__charAppVal" style="font-size:15px;font-weight:600;margin:8px 0 10px;"></div>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tbody id="__charAppRows"></tbody>
  </table>
  <p id="__charAppNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
  var LEVELS = [
''' + lv_js + r'''
  ];
  function __caIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __caNum(id){
    var el = document.getElementById(id);
    if(!el) return NaN;
    return parseFloat(el.value);
  }
  // 与页面主公式一致：e=(RH/100)*6.105*exp(17.27T/(237.7+T)); AT=T+0.33e-0.70ws-4.0
  function __caAT(){
    var T = __caNum('T'), RH = __caNum('RH'), ws = __caNum('ws');
    if(!isFinite(T) || !isFinite(RH) || !isFinite(ws)) return null;
    if(RH < 0 || RH > 100) return null;
    var e = (RH/100)*6.105*Math.exp(17.27*T/(237.7+T));
    var AT = T + 0.33*e - 0.70*ws - 4.0;
    if(!isFinite(AT)) return null;
    return {T:T, RH:RH, ws:ws, e:e, AT:AT};
  }
  function __caLevel(at){
    for(var i=0;i<LEVELS.length;i++){ if(at >= LEVELS[i][0]) return LEVELS[i]; }
    return LEVELS[LEVELS.length-1];
  }
  function __caUpdate(){
    var en = __caIsEn();
    var badge = document.getElementById('__charAppBadge');
    var val = document.getElementById('__charAppVal');
    var tb = document.getElementById('__charAppRows');
    var r = __caAT();
    if(!r){
      if(badge){ badge.style.display='none'; }
      if(val) val.textContent = en ? 'Enter a valid temperature / humidity / wind speed above.' : '请先在上方填写有效的气温 / 相对湿度 / 风速。';
      if(tb) tb.innerHTML = '';
      return;
    }
    var lv = __caLevel(r.AT);
    if(badge){
      badge.style.display='inline-block';
      badge.style.background = lv[3];
      badge.textContent = (en ? lv[2] : lv[1]);
    }
    if(val) val.textContent = (en ? 'Apparent temperature: ' : '体感温度：') + r.AT.toFixed(1) + ' \u00b0C';
    if(tb){
      var d = r.AT - r.T;
      var cause, causeVal;
      if(d >= 2){ cause = en ? 'Humid / muggy' : '湿热闷热'; causeVal = en ? ('Feels ' + d.toFixed(1) + ' \u00b0C hotter than the air: high humidity slows sweat evaporation, so the body cannot shed heat.')
                                                          : ('比气温高 ' + d.toFixed(1) + ' \u00b0C：湿度大，汗液难以蒸发，人体散热受阻，所以更闷热。'); }
      else if(d <= -2){ cause = en ? 'Wind chill' : '风寒显著'; causeVal = en ? ('Feels ' + Math.abs(d).toFixed(1) + ' \u00b0C colder than the air: wind strips away the warm boundary layer around skin and clothing.')
                                                             : ('比气温低 ' + Math.abs(d).toFixed(1) + ' \u00b0C：风带走体表与衣物间的暖空气层，所以感觉更冷。'); }
      else { cause = en ? 'Close to air temperature' : '接近气温'; causeVal = en ? 'Humidity and wind roughly offset each other, so it feels about the same as the thermometer reads.'
                                                                  : '湿度与风速影响大致抵消，体感与实测气温接近。'; }
      var rows = '';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);width:32%;">' + (en ? 'Health note' : '健康提示') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? lv[5] : lv[4]) + '</td></tr>';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'What to wear' : '穿衣建议') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? lv[7] : lv[6]) + '</td></tr>';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Why it differs' : '成因解读') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + cause + (en ? ': ' : '：') + causeVal + '</td></tr>';
      tb.innerHTML = rows;
    }
  }
  function __caInit(){
    var en = __caIsEn();
    document.getElementById('__charAppTitle').textContent = en
      ? '🌡️ What This Feels Like & What To Do'
      : '🌡️ 体感分级与健康提示';
    document.getElementById('__charAppDesc').textContent = en
      ? 'Translates the apparent temperature into a comfort/safety level, with the health note, clothing advice and the reason it differs from the thermometer reading.'
      : '把体感温度换算成舒适/安全档位，给出对应的健康提示、穿衣建议，以及它为什么和气温读数不一样。';
    document.getElementById('__charAppNote').textContent = en
      ? 'Levels follow common heat/cold comfort scales; thresholds are indicative, not medical advice. Individual tolerance varies with age, acclimatisation, activity level and clothing. If you or someone else shows signs of heat stroke or hypothermia, seek medical help immediately.'
      : '档位参考常见的冷热舒适度分级，为提示性阈值而非医疗建议。个体耐受随年龄、热适应、活动强度与衣物而差异很大。若出现热射病或失温征兆，请立即就医。';
    __caUpdate();
    ['T','RH','ws'].forEach(function(id){
      var el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', __caUpdate);
      el.addEventListener('change', __caUpdate);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__caInit);
  else __caInit();
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
    targets = sys.argv[1:] or []
    if not targets:
        print("usage: _ux_char_apparent.py <tool1.html> [tool2.html] ...")
        sys.exit(1)
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
