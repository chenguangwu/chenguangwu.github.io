# -*- coding: utf-8 -*-
"""修复 fishery 5 个通用壳工具：将其错位/空的通用计算器替换为领域专用真实算法。

修复对象（共用同一套"综合评分/面积/周长"模板，且 calc() 依赖 h1 标题——这些页只有 h2，
导致结果恒空）：
  calc-power     → 用电功率 P = V×I
  density-1     → 放养密度 = 尾数/面积
  estimate-23   → 增长估算 = 基准×(1+增长率/100)
  ratio-hormone → 配比与比例（最简整数比/占比/倍数）
  temp-density  → 水温—饱和溶氧与饱和度

每个文件替换：h2 标题、副标题、formula-eq/desc、两个输入(标签+默认值)、info-box、resetAll 默认值，
以及整段 calc() 函数（brace-matched 从 "function calc(){" 到匹配的右括号）。
用法：python3 scripts/fix_fishery_shells.py --apply
"""
import os, re, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(ROOT, 'tools', 'fishery')

# 各工具的新内容
CFG = {
    "calc-power": {
        "h2": '🐟 用电功率计算',
        "sub": '输入电压与电流，计算电功率（P = V × I）。',
        "eq": '功率 P = V × I',
        "desc": '电功率等于电压与电流的乘积；1 kW = 1000 W。',
        "labelA": '电压 (V)', "labelB": '电流 (A)',
        "defA": '220', "defB": '10',
        "info": '💡 公式提示：功率 P = V × I（W），除以 1000 得 kW。',
        "calc": '''function calc(){
  var iv=readInputs();
  var v=iv.a, i=iv.b;
  var p=v*i;
  var pKw=p/1000;
  var html='<div class="data-grid">'+
    '<div class="data-card"><div class="num">'+p.toFixed(2)+' W</div><div class="label">功率 P = V×I</div></div>'+
    '<div class="data-card"><div class="num">'+pKw.toFixed(4)+' kW</div><div class="label">功率(kW)</div></div>'+
    '<div class="data-card"><div class="num">'+v.toFixed(2)+' V</div><div class="label">电压</div></div>'+
    '<div class="data-card"><div class="num">'+i.toFixed(2)+' A</div><div class="label">电流</div></div>'+
    '</div>';
  document.getElementById('res').innerHTML=html;
  if(iv.valid) saveHistory(v,i);
}''',
    },
    "density-1": {
        "h2": '🐟 放养密度计算',
        "sub": '输入总尾数与养殖面积，计算放养密度（尾/亩、尾/m²）。',
        "eq": '密度 = 尾数 / 面积',
        "desc": '放养密度 = 总尾数 ÷ 面积；1 亩 ≈ 666.67 m²。',
        "labelA": '总尾数 (尾)', "labelB": '面积 (亩)',
        "defA": '1000', "defB": '1',
        "info": '💡 公式提示：密度 = 尾数 ÷ 面积（尾/亩），可折合尾/m²。',
        "calc": '''function calc(){
  var iv=readInputs();
  var n=iv.a, area=iv.b;
  var perMu = area>0 ? n/area : 0;
  var perM2 = area>0 ? n/(area*666.67) : 0;
  var html='<div class="data-grid">'+
    '<div class="data-card"><div class="num">'+perMu.toFixed(1)+' 尾/亩</div><div class="label">放养密度</div></div>'+
    '<div class="data-card"><div class="num">'+perM2.toFixed(2)+' 尾/m²</div><div class="label">折合 m²</div></div>'+
    '<div class="data-card"><div class="num">'+n.toFixed(0)+' 尾</div><div class="label">总尾数</div></div>'+
    '<div class="data-card"><div class="num">'+area.toFixed(2)+' 亩</div><div class="label">面积</div></div>'+
    '</div>';
  document.getElementById('res').innerHTML=html;
  if(iv.valid) saveHistory(n,area);
}''',
    },
    "estimate-23": {
        "h2": '🐟 增长估算计算',
        "sub": '输入基准值与增长率，估算增长后的结果。',
        "eq": '结果 = 基准值 × (1 + 增长率/100)',
        "desc": '按百分比增长率对基准值进行线性增长估算。',
        "labelA": '基准值', "labelB": '增长率 (%)',
        "defA": '100', "defB": '20',
        "info": '💡 公式提示：结果 = 基准值 × (1 + 增长率/100)。',
        "calc": '''function calc(){
  var iv=readInputs();
  var base=iv.a, rate=iv.b;
  var result=base*(1+rate/100);
  var growth=base*rate/100;
  var html='<div class="data-grid">'+
    '<div class="data-card"><div class="num">'+result.toFixed(2)+'</div><div class="label">估算结果</div></div>'+
    '<div class="data-card"><div class="num">'+growth.toFixed(2)+'</div><div class="label">增长量</div></div>'+
    '<div class="data-card"><div class="num">'+base.toFixed(2)+'</div><div class="label">基准值</div></div>'+
    '<div class="data-card"><div class="num">'+rate.toFixed(2)+'%</div><div class="label">增长率</div></div>'+
    '</div>';
  document.getElementById('res').innerHTML=html;
  if(iv.valid) saveHistory(base,rate);
}''',
    },
    "ratio-hormone": {
        "h2": '🐟 配比与比例计算',
        "sub": '输入两个数值，求最简整数比、占比与倍数关系。',
        "eq": '最简比 = a/g : b/g（g 为最大公约数）',
        "desc": '用于药剂配比、浓度比例等场景的快速换算。',
        "labelA": '数值 A', "labelB": '数值 B',
        "defA": '100', "defB": '50',
        "info": '💡 公式提示：最简整数比 = A/g : B/g，占比 = A/B×100%。',
        "calc": '''function calc(){
  var iv=readInputs();
  var a=iv.a, b=iv.b;
  var g=b?gcd(a,b):0;
  var sr=g?(a/g)+':'+(b/g):'-';
  var pct=b?(a/b*100).toFixed(2)+'%':'-';
  var mult=b?(a/b).toFixed(4):'-';
  var html='<div class="data-grid">'+
    '<div class="data-card"><div class="num">'+sr+'</div><div class="label">最简整数比</div></div>'+
    '<div class="data-card"><div class="num">'+pct+'</div><div class="label">A 占比</div></div>'+
    '<div class="data-card"><div class="num">'+mult+'</div><div class="label">A / B 倍数</div></div>'+
    '<div class="data-card"><div class="num">'+a.toFixed(2)+'</div><div class="label">数值 A</div></div>'+
    '</div>';
  document.getElementById('res').innerHTML=html;
  if(iv.valid) saveHistory(a,b);
}''',
    },
    "temp-density": {
        "h2": '🐟 水温—饱和溶氧与饱和度',
        "sub": '输入水温与实测溶氧，估算饱和溶氧与饱和度，判断溶氧是否充足。',
        "eq": '饱和溶氧 ≈ 14.652 − 0.41022T + 0.007991T² − 0.000077774T³',
        "desc": '饱和溶氧随温度升高而下降；饱和度 = 实测 ÷ 饱和。',
        "labelA": '水温 (℃)', "labelB": '实测溶氧 (mg/L)',
        "defA": '25', "defB": '6.5',
        "info": '💡 公式提示：饱和度 = 实测溶氧 ÷ 该温度饱和溶氧 ×100%。',
        "calc": '''function calc(){
  var iv=readInputs();
  var T=iv.a, doMeas=iv.b;
  var sat = 14.652 - 0.41022*T + 0.007991*T*T - 0.000077774*T*T*T;
  var pct = sat>0 ? (doMeas/sat*100) : 0;
  var level = pct>=100?'充足':pct>=80?'可接受':'偏低';
  var html='<div class="data-grid">'+
    '<div class="data-card"><div class="num">'+sat.toFixed(2)+' mg/L</div><div class="label">饱和溶氧</div></div>'+
    '<div class="data-card"><div class="num">'+pct.toFixed(1)+'%</div><div class="label">饱和度</div></div>'+
    '<div class="data-card"><div class="num">'+doMeas.toFixed(2)+' mg/L</div><div class="label">实测溶氧</div></div>'+
    '<div class="data-card"><div class="num">'+level+'</div><div class="label">评价</div></div>'+
    '</div>';
  document.getElementById('res').innerHTML=html;
  if(iv.valid) saveHistory(T,doMeas);
}''',
    },
}


def replace_calc(src, new_calc):
    """brace-matched 替换 function calc(){ ... } 整段。"""
    idx = src.find('function calc(){')
    if idx < 0:
        return None
    i = idx + len('function calc(){') - 1  # 指向首个 {
    depth = 0
    j = i
    while j < len(src):
        if src[j] == '{':
            depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    end = j + 1  # 包含闭合 }
    return src[:idx] + new_calc + '\n' + src[end:]


def fix_one(slug, cfg):
    fp = os.path.join(TDIR, slug + '.html')
    s = open(fp, encoding='utf-8').read()

    # 1) h2 标题
    s = re.sub(r'<h2 [^>]*>.*?</h2>', '<h2 data-zh="%s">%s</h2>' % (cfg['h2'], cfg['h2']), s, count=1)
    # 2) 副标题
    s = re.sub(r'<p [^>]*>.*?calculate online, free and accurate\..*?</p>',
               '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="%s">%s</p>' % (cfg['sub'], cfg['sub']),
               s, count=1, flags=re.S)
    # 3) formula-eq / formula-desc
    s = re.sub(r'<div class="formula-eq">.*?</div>', '<div class="formula-eq">%s</div>' % cfg['eq'], s, count=1, flags=re.S)
    s = re.sub(r'<p class="formula-desc">.*?</p>', '<p class="formula-desc">%s</p>' % cfg['desc'], s, count=1, flags=re.S)
    # 4) 两个输入行
    s = re.sub(r'<label>[^<]*</label><input type="number" id="v0" value="[^"]*"',
               '<label>%s</label><input type="number" id="v0" value="%s"' % (cfg['labelA'], cfg['defA']), s, count=1)
    s = re.sub(r'<label>[^<]*</label><input type="number" id="v1" value="[^"]*"',
               '<label>%s</label><input type="number" id="v1" value="%s"' % (cfg['labelB'], cfg['defB']), s, count=1)
    # 5) info-box
    s = re.sub(r'<div class="info-box">.*?</div>', '<div class="info-box">%s</div>' % cfg['info'], s, count=1, flags=re.S)
    # 6) resetAll 默认值
    s = re.sub(r"document.getElementById\('v0'\).value=100;", "document.getElementById('v0').value=%s;" % cfg['defA'], s, count=1)
    s = re.sub(r"document.getElementById\('v1'\).value=50;", "document.getElementById('v1').value=%s;" % cfg['defB'], s, count=1)
    # 7) 整段 calc()
    new = replace_calc(s, cfg['calc'])
    if new is None:
        raise RuntimeError('未找到 calc() : ' + slug)
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    for slug, cfg in CFG.items():
        new = fix_one(slug, cfg)
        if args.apply:
            open(os.path.join(TDIR, slug + '.html'), 'w', encoding='utf-8').write(new)
            print('FIXED: %s.html' % slug)
        else:
            print('PREVIEW: %s.html (len %d)' % (slug, len(new)))
    if not args.apply:
        print('预览模式（加 --apply 落盘）')


if __name__ == '__main__':
    raise SystemExit(main())
