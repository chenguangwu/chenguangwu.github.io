#!/usr/bin/env python3
# _ux_char_windchill.py — UX 工具特异性功能重做 · F-CHAR-3b
# 给「风寒指数（WCT）类」工具注入自包含的「风寒冻伤风险分级 + 暴露时限 + 防护建议」模块。
# 背景：页面 FAQ 自述「按风寒分级做户外时长限制」，但 calcTool 只输出 WCT / 降温幅度 / 风速
#       三个裸数值，页面内无任何分级实现 ⇒ 承诺未实现，属真缺口。
# 分级依据：加拿大官方 Wind Chill Index 风险分级（真实领域标准，非自拟）：
#   0 ~ -9 低风险 / -10 ~ -27 中等 / -28 ~ -39 高（裸露皮肤 10-30 min 可冻伤）
#   / -40 ~ -47 很高（5-10 min）/ -48 ~ -54 严重（2-5 min）/ ≤ -55 极端（<2 min）
# 与 apparent-temperature 模块内容不同（本模块是冻伤风险与暴露时限，非冷热舒适度/穿衣），
# 且 humidex / heat-index 已各自有官方分级 → 均不注入，避免重复。
# 沿用 F-CHAR-1/2 已验证模式：自包含 / 构建安全 / 静态无中文、JS 按 ?lang=en-US 填充。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charWindchill"'

# (下限℃, 中文档名, 英文档名, 颜色, 中文风险说明, 英文风险说明, 中文防护, 英文防护)
# 由高到低，命中第一个 WCT >= 下限 的档位。
LEVELS = [
    [0, "基本无冻伤风险", "Little to no frostbite risk", "#16a34a",
     "风寒值在 0°C 以上，冻伤风险很低，但湿冷仍可能让人不适。",
     "Wind chill is above 0 °C; frostbite risk is low, though damp cold can still feel unpleasant.",
     "常规秋冬衣物即可；注意防潮，湿衣服会显著加快散热。",
     "Regular autumn/winter clothing is fine; stay dry, since wet clothing greatly accelerates heat loss."],
    [-9, "低风险", "Low risk", "#0d9488",
     "轻微不适，长时间静止或潮湿时体感会更冷。",
     "Slight discomfort; it feels colder when standing still for long periods or when damp.",
     "外套 + 长裤；久坐或等车时加一件，手部注意保暖。",
     "Jacket and long trousers; add a layer when standing or waiting, and keep hands warm."],
    [-27, "中等风险", "Moderate risk", "#0284c7",
     "明显不适，长时间暴露存在冻伤可能，需遮盖暴露皮肤。",
     "Distinctly uncomfortable; frostbite becomes possible with prolonged exposure. Cover exposed skin.",
     "厚外套 + 帽子手套；尽量遮盖面部与耳朵，缩短连续暴露时间。",
     "Heavy coat with hat and gloves; cover face and ears, and shorten continuous exposure."],
    [-39, "高风险", "High risk", "#2563eb",
     "裸露皮肤约 10-30 分钟即可冻伤，需限制户外时长。",
     "Exposed skin can freeze in roughly 10-30 minutes. Limit time outdoors.",
     "全面保暖并遮住所有裸露皮肤；户外每 20-30 分钟进室内回暖。",
     "Full cold-weather coverage with no exposed skin; return indoors to warm up every 20-30 minutes."],
    [-47, "很高风险", "Very high risk", "#1d4ed8",
     "裸露皮肤约 5-10 分钟即可冻伤，应避免非必要户外停留。",
     "Exposed skin can freeze in roughly 5-10 minutes. Avoid unnecessary time outdoors.",
     "防风外层 + 面罩/护目；非必要不外出，外出需结伴并定时检查皮肤。",
     "Windproof shell with face protection; avoid going out unless necessary, go with others and check skin regularly."],
    [-54, "严重风险", "Severe risk", "#3730a3",
     "裸露皮肤约 2-5 分钟即可冻伤，非紧急事务不应外出。",
     "Exposed skin can freeze in roughly 2-5 minutes. Do not go out except for emergencies.",
     "极地式防护：多层保暖 + 全面罩；取消户外作业与体育课等活动。",
     "Expedition-grade protection: multiple insulating layers and full face covering. Cancel outdoor work and activities such as outdoor classes."],
    [-999, "极端风险", "Extreme risk", "#581c87",
     "裸露皮肤 2 分钟内即可冻伤，同时伴随失温风险，禁止户外暴露。",
     "Exposed skin can freeze in under 2 minutes, with concurrent hypothermia risk. Outdoor exposure should be prohibited.",
     "禁止户外暴露；必须外出时按极寒作业规程，全程有人陪同并限定分钟级时长。",
     "Outdoor exposure is prohibited. If travel is unavoidable, follow extreme-cold operating procedures with a companion and a strict minute-level time limit."],
]


def build_section():
    lv_js = ",\n".join(
        '    [%r, %r, %r, %r, %r, %r, %r, %r]' % (a, b, c, d, e, f, g, h)
        for a, b, c, d, e, f, g, h in LEVELS
    )
    html = r'''<section class="char-module" id="__charWindchill" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charWcTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charWcDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="__charWcBadge" style="display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-size:13px;font-weight:600;margin-bottom:4px;"></div>
  <div id="__charWcVal" style="font-size:15px;font-weight:600;margin:8px 0 10px;"></div>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tbody id="__charWcRows"></tbody>
  </table>
  <p id="__charWcNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
  var LEVELS = [
''' + lv_js + r'''
  ];
  function __cwIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __cwNum(id){
    var el = document.getElementById(id);
    if(!el) return NaN;
    return parseFloat(el.value);
  }
  // 与页面主公式一致：WCT = 13.12 + 0.6215T - 11.37*v^0.16 + 0.3965*T*v^0.16  (v: km/h)
  function __cwWct(){
    var T = __cwNum('T'), v = __cwNum('v');
    if(!isFinite(T) || !isFinite(v) || v < 0) return null;
    var p = Math.pow(v, 0.16);
    var WCT = 13.12 + 0.6215*T - 11.37*p + 0.3965*T*p;
    if(!isFinite(WCT)) return null;
    return {T:T, v:v, WCT:WCT};
  }
  function __cwLevel(w){
    for(var i=0;i<LEVELS.length;i++){ if(w >= LEVELS[i][0]) return LEVELS[i]; }
    return LEVELS[LEVELS.length-1];
  }
  function __cwUpdate(){
    var en = __cwIsEn();
    var badge = document.getElementById('__charWcBadge');
    var val = document.getElementById('__charWcVal');
    var tb = document.getElementById('__charWcRows');
    var r = __cwWct();
    if(!r){
      if(badge){ badge.style.display='none'; }
      if(val) val.textContent = en ? 'Enter a valid temperature and wind speed above.' : '请先在上方填写有效的气温与风速。';
      if(tb) tb.innerHTML = '';
      return;
    }
    var lv = __cwLevel(r.WCT);
    if(badge){
      badge.style.display='inline-block';
      badge.style.background = lv[3];
      badge.textContent = (en ? lv[2] : lv[1]);
    }
    if(val) val.textContent = (en ? 'Wind chill index: ' : '风寒指数：') + r.WCT.toFixed(1) + ' \u00b0C';
    if(tb){
      var drop = r.T - r.WCT;
      var causeVal;
      if(drop >= 10) causeVal = en ? ('Wind strips heat ' + drop.toFixed(1) + ' \u00b0C faster than still air: at this wind speed the warm layer around skin is removed continuously, so cooling is dramatic.')
                                    : ('风让散热比无风时多降 ' + drop.toFixed(1) + ' \u00b0C：该风速下体表暖空气层被持续吹散，所以降温非常剧烈。');
      else if(drop >= 3) causeVal = en ? ('Wind removes heat ' + drop.toFixed(1) + ' \u00b0C faster than still air.')
                                       : ('风让散热比无风时多降 ' + drop.toFixed(1) + ' \u00b0C。');
      else causeVal = en ? 'Wind has little effect at this speed, so apparent temperature stays close to the air temperature.'
                         : '该风速影响很小，体感与气温接近。';
      var rows = '';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);width:32%;">' + (en ? 'Risk' : '风险说明') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? lv[5] : lv[4]) + '</td></tr>';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Protection' : '防护建议') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? lv[7] : lv[6]) + '</td></tr>';
      rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Why it differs' : '成因解读') + '</td>'
            + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + causeVal + '</td></tr>';
      tb.innerHTML = rows;
    }
  }
  function __cwInit(){
    var en = __cwIsEn();
    document.getElementById('__charWcTitle').textContent = en
      ? '🧊 Frostbite Risk & Exposure Limit'
      : '🧊 冻伤风险分级与暴露时限';
    document.getElementById('__charWcDesc').textContent = en
      ? 'Turns the wind chill index into an official risk level, showing how fast exposed skin can freeze and how to protect yourself.'
      : '把风寒指数换算成官方风险档位，说明裸露皮肤多久可能冻伤，以及该怎么防护。';
    document.getElementById('__charWcNote').textContent = en
      ? 'Levels follow the Canadian Wind Chill Index risk scale; freeze times assume exposed skin with no wind protection. Clothing, wind exposure, sunlight and individual circulation all change actual risk. These are indicative thresholds, not medical advice: seek medical help immediately for suspected frostbite or hypothermia.'
      : '档位依据加拿大风寒指数（Wind Chill Index）风险分级；冻伤时间按裸露皮肤、无防风保护估算。衣物、迎风情况、日照与个体循环都会改变实际风险。以上为提示性阈值而非医疗建议，疑似冻伤或失温请立即就医。';
    __cwUpdate();
    ['T','v'].forEach(function(id){
      var el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', __cwUpdate);
      el.addEventListener('change', __cwUpdate);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__cwInit);
  else __cwInit();
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
        print("usage: _ux_char_windchill.py <tool1.html> [tool2.html] ...")
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
