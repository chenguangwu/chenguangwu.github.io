#!/usr/bin/env python3
# _ux_char_noise.py — UX 工具特异性功能重做 · F-CHAR-4
# 给「声学声级（dB）类」工具注入自包含的「噪声暴露安全时限 + 声源对照 + 听力防护」模块。
# 背景：整个 acoustics 分类 27 页，grep「OSHA|暴露时限|3 dB|减半」命中 **0**
#       ⇒ 噪声职业暴露安全标准这一声学独有的官方知识，全族零覆盖，是真缺口。
# 依据（真实标准，非自拟）：
#   NIOSH 推荐暴露限值 85 dBA / 8 h，对等交换率 3 dB ⇒ 声级每 +3 dB，允许时间减半：
#   T = 8 · 2^((85 − L)/3) 小时（85→8h, 88→4h, 91→2h, 94→1h, 97→30min, 100→15min,
#   103→7.5min, 106→3.75min, 109→1.9min, 112→1min, 115→约 0.5min）
# 按页定制 dB 取值（各页公式/输入不同，不做统一硬套）：
#   声强级 10log10(I/1e-12) / 声压级 20log10(p/20e-6) / 声功率级 10log10(W/1e-12)
#   / 双声源叠加 10log10(10^(L1/10)+10^(L2/10)) / 平方反比衰减后声强级
# 沿用 F-CHAR-1/2/3 已验证模式：自包含 / 构建安全 / 静态无中文、JS 按 ?lang=en-US 填充。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'id="__charNoise"'

# 相对路径 -> (dB 取值 JS 表达式, 需要监听的输入 id 列表)
# 表达式内可直接用 num(id)；常量与页面主脚本保持一致：I0=1e-12, p0=20e-6, W0=1e-12
TARGETS = {
    'tools/acoustics/intensity-level.html': (
        "10*Math.log10(num('I')/1e-12)", ['I']),
    'tools/acoustics/sound-intensity-level.html': (
        "10*Math.log10(num('I')/1e-12)", ['I']),
    'tools/acoustics/sound-pressure-level.html': (
        "20*Math.log10(num('p')/20e-6)", ['p']),
    'tools/acoustics/sound-power-level.html': (
        "10*Math.log10(num('W')/1e-12)", ['W']),
    'tools/acoustics/spl-add.html': (
        "10*Math.log10(Math.pow(10,num('L1')/10)+Math.pow(10,num('L2')/10))", ['L1', 'L2']),
    'tools/acoustics/combine-two-spl.html': (
        "10*Math.log10(Math.pow(10,num('l1')/10)+Math.pow(10,num('l2')/10))", ['l1', 'l2']),
    'tools/acoustics/intensity-inverse-square.html': (
        "10*Math.log10(num('I1')*Math.pow(num('r1')/num('r2'),2)/1e-12)", ['I1', 'r1', 'r2']),
}

# 常见声源声级对照 [dB, 中文, 英文]
SOURCES = [
    [0, "听觉阈值", "Threshold of hearing"],
    [20, "耳语、安静卧室", "Whisper, quiet bedroom"],
    [40, "图书馆、冰箱嗡鸣", "Library, refrigerator hum"],
    [60, "正常交谈、空调", "Normal conversation, air conditioner"],
    [70, "吸尘器、繁忙街道", "Vacuum cleaner, busy street"],
    [85, "繁忙车流、地铁进站", "Heavy traffic, subway arriving"],
    [90, "摩托车、草坪机", "Motorcycle, lawn mower"],
    [100, "电锯、地铁车厢内", "Chainsaw, inside a subway car"],
    [110, "夜总会、摇滚演出", "Night club, rock concert"],
    [120, "痛阈、喷气发动机近场", "Threshold of pain, jet engine nearby"],
    [130, "军用喷气起飞", "Military jet take-off"],
    [140, "枪声、爆竹近距", "Gunshot, firecracker up close"],
]


def build_section(expr, ids):
    src_js = ",\n".join('    [%r, %r, %r]' % (a, b, c) for a, b, c in SOURCES)
    ids_js = ", ".join("'%s'" % i for i in ids)
    html = r'''<section class="char-module" id="__charNoise" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="__charNoiseTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="__charNoiseDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="__charNoiseBadge" style="display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-size:13px;font-weight:600;margin-bottom:4px;"></div>
  <div id="__charNoiseVal" style="font-size:15px;font-weight:600;margin:8px 0 10px;"></div>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tbody id="__charNoiseRows"></tbody>
  </table>
  <p id="__charNoiseNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
  var SOURCES = [
''' + src_js + r'''
  ];
  var IDS = [''' + ids_js + r'''];
  function __cnIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function num(id){
    var el = document.getElementById(id);
    if(!el) return NaN;
    return parseFloat(el.value);
  }
  function __cnDb(){
    var v = (''' + expr + r''');
    if(!isFinite(v)) return null;
    return v;
  }
  // NIOSH 推荐限值 85 dB / 8 h，3 dB 交换率：T = 8 * 2^((85-L)/3) 小时
  function __cnLimit(L){
    if(L < 80) return null;             // 基本无限制
    var h = 8 * Math.pow(2, (85 - L) / 3);
    if(!isFinite(h)) return null;
    return h;
  }
  function __cnFmtHours(h){
    if(h >= 24) return null;            // 超过 24h 视为无实际限制
    if(h >= 1) return { v: h, u: 'h' };
    var m = h * 60;
    if(m >= 1) return { v: m, u: 'min' };
    return { v: m * 60, u: 's' };
  }
  function __cnNearest(L){
    var best = SOURCES[0], bd = Math.abs(SOURCES[0][0] - L);
    for(var i=1;i<SOURCES.length;i++){
      var d = Math.abs(SOURCES[i][0] - L);
      if(d < bd){ bd = d; best = SOURCES[i]; }
    }
    return best;
  }
  function __cnUpdate(){
    var en = __cnIsEn();
    var badge = document.getElementById('__charNoiseBadge');
    var val = document.getElementById('__charNoiseVal');
    var tb = document.getElementById('__charNoiseRows');
    var L = __cnDb();
    if(L === null){
      if(badge){ badge.style.display='none'; }
      if(val) val.textContent = en ? 'Enter valid input above to get a sound level first.' : '请先在上方填写有效输入，算出声级后再看暴露时限。';
      if(tb) tb.innerHTML = '';
      return;
    }
    var color, label, risk, protect;
    if(L < 60){ color = '#16a34a'; label = en ? 'Safe' : '安全';
      risk = en ? 'Well below any occupational limit; no hearing damage expected from ordinary exposure.' : '远低于任何职业限值，日常暴露不会造成听力损伤。';
      protect = en ? 'No hearing protection needed.' : '无需听力防护。'; }
    else if(L < 85){ color = '#0d9488'; label = en ? 'Generally safe' : '基本安全';
      risk = en ? 'Below the 85 dB occupational action level; prolonged close-range exposure may still cause fatigue.' : '低于 85 dB 职业行动水平；长时间近距离暴露仍可能引起疲劳与不适。';
      protect = en ? 'No protection normally needed; consider earplugs for long sessions.' : '通常无需防护；长时间处于该环境可考虑耳塞。'; }
    else if(L < 100){ color = '#ea580c'; label = en ? 'Protection advised' : '建议防护';
      risk = en ? 'At or above the 85 dB action level: cumulative exposure can cause permanent hearing loss.' : '达到或超过 85 dB 行动水平：累积暴露可导致永久性听力损伤。';
      protect = en ? 'Wear hearing protection and limit continuous exposure to the time below.' : '应佩戴听力防护，并把连续暴露控制在下方时限内。'; }
    else if(L < 115){ color = '#dc2626'; label = en ? 'Hazardous' : '危险';
      risk = en ? 'Only minutes of exposure are permitted; unprotected exposure risks immediate and permanent damage.' : '只允许数分钟暴露；无防护暴露可造成即时且永久的损伤。';
      protect = en ? 'Hearing protection is mandatory; double protection (plugs + muffs) is recommended.' : '必须佩戴听力防护；建议双重防护（耳塞 + 耳罩）。'; }
    else { color = '#7f1d1d'; label = en ? 'Extreme danger' : '极度危险';
      risk = en ? 'At or above the threshold of pain: any unprotected exposure can cause immediate injury.' : '达到或超过痛阈：任何无防护暴露都可能造成即时伤害。';
      protect = en ? 'Do not approach unprotected; only trained personnel with full protection should be present.' : '不得无防护接近；仅限佩戴全套防护的受训人员在场。'; }

    if(badge){ badge.style.display='inline-block'; badge.style.background = color; badge.textContent = label; }
    if(val) val.textContent = (en ? 'Sound level: ' : '声级：') + L.toFixed(1) + ' dB';

    var h = __cnLimit(L);
    var lim;
    if(h === null){ lim = en ? 'No practical limit below 80 dB.' : '低于 80 dB，实际无限制。'; }
    else {
      var f = __cnFmtHours(h);
      if(f === null) lim = en ? 'More than 24 h (no practical limit).' : '超过 24 小时（实际无限制）。';
      else {
        var uv = f.u === 'h' ? (en ? ' h' : ' 小时') : (f.u === 'min' ? (en ? ' min' : ' 分钟') : (en ? ' s' : ' 秒'));
        lim = (en ? 'Permitted continuous exposure: about ' : '允许连续暴露约 ') + (f.v < 10 ? f.v.toFixed(1) : Math.round(f.v)) + uv + (en ? ' (NIOSH 85 dB / 8 h, 3 dB exchange rate).' : '（NIOSH 85 dB / 8 小时，3 dB 交换率）。');
      }
    }
    var near = __cnNearest(L);
    var rows = '';
    rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);width:32%;">' + (en ? 'Risk' : '风险说明') + '</td>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + risk + '</td></tr>';
    rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Exposure limit' : '暴露时限') + '</td>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + lim + '</td></tr>';
    rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Protection' : '防护建议') + '</td>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + protect + '</td></tr>';
    rows += '<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? 'Sounds like' : '相当于') + '</td>'
          + '<td style="padding:4px 6px;border-bottom:1px solid var(--border);">' + (en ? near[2] : near[1]) + (en ? ' (' : ' （') + near[0] + ' dB' + (en ? ')' : '）') + '</td></tr>';
    if(tb) tb.innerHTML = rows;
  }
  function __cnInit(){
    var en = __cnIsEn();
    document.getElementById('__charNoiseTitle').textContent = en
      ? '🔊 Noise Exposure Limit & Hearing Protection'
      : '🔊 噪声暴露时限与听力防护';
    document.getElementById('__charNoiseDesc').textContent = en
      ? 'Turns the calculated sound level into an occupational exposure limit, with the risk, the protection required and a familiar sound for comparison.'
      : '把算出的声级换算成职业噪声暴露时限，并给出风险、所需防护以及一个日常熟悉的声音作对照。';
    document.getElementById('__charNoiseNote').textContent = en
      ? 'Limits follow the NIOSH recommended exposure limit (85 dB for 8 h) with a 3 dB exchange rate: each 3 dB increase halves the permitted time. Values assume continuous exposure and no hearing protection; actual regulations vary by country and by whether A-weighted or peak measurements are used. Indicative only, not a substitute for a workplace noise assessment.'
      : '时限依据 NIOSH 推荐暴露限值（85 dB / 8 小时）与 3 dB 交换率：声级每提高 3 dB，允许时间减半。数值按连续暴露且无防护估算；各国法规、以及是否采用 A 计权或峰值测量，都会改变实际限值。以上仅供提示，不能替代工作场所噪声检测评估。';
    __cnUpdate();
    IDS.forEach(function(id){
      var el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', __cnUpdate);
      el.addEventListener('change', __cnUpdate);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__cnInit);
  else __cnInit();
})();
</script>
'''
    return html


def inject(path, expr, ids):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return False
    sec = build_section(expr, ids)
    if '</body>' in s:
        s = s.replace('</body>', sec + '\n</body>', 1)
    else:
        s = s + sec
    open(path, 'w', encoding='utf-8').write(s)
    return True


def main():
    done = skip = miss = 0
    for rel, (expr, ids) in TARGETS.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("MISS", rel); miss += 1; continue
        if inject(p, expr, ids): done += 1
        else: skip += 1
    print("injected=%d skipped(already)=%d missing=%d" % (done, skip, miss))


if __name__ == '__main__':
    main()
