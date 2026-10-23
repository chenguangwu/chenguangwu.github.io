# -*- coding: utf-8 -*-
"""
F-CHAR-2 物理量转换器「实物参照 / 尺度感知」注入。
目标页（tools/life 通用转换器，统一 convert() + inputVal + fromUnit 模板）：
  第一批：length / area / volume / weight / speed
  续批：   time / energy / power / pressure / data-rate / angle / frequency
（temperature 已自带完善的常见温度参考表，排除；data-unit 已自带"常见数据量参考"区块，排除）

注入结构（遵循已通过门禁的 __charDist 范式）：
  <!-- __charRef_start -->
  <section class="char-module" id="__charRef">  ← 静态零中文，仅含输出容器
    <div id="__charRefBox"></div>
  </section>
  <script> ... </script>                        ← 脚本在 section 之外，文本不计入 sec.textContent
  <!-- __charRef_end -->
语言判定直接读 location.search 的 ?lang=en-US（门禁 JSDOM 不加载 TBKit，不能依赖 TBKit.util.isEn）。
模块只渲染"参照标签"，不渲染页内换算裸数值 → 不命中 verify_life_calc.js 的 expect → 不制造逃生项。

用法：python3 scripts/_ux_char_conv.py
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = '<!-- __charRef_start -->'
END = '<!-- __charRef_end -->'

# 每页：基准系数（以页内基准单位计）、基准单位名、实物参照表、小知识。
# refs: v=基准单位值, zh/en=标签, d=友好显示串（避免 JS 浮点格式化误差）
TARGETS = {
    'length-converter.html': {
        'factors': {'mm':0.001,'cm':0.01,'m':1,'km':1000,'in':0.0254,'ft':0.3048,
                    'yd':0.9144,'mi':1609.344,'nmi':1852,'ly':9.46073e15},
        'base_zh':'米','base_en':'m',
        'refs':[
            {'v':0.001,'zh':'1 毫米（银行卡厚度）','en':'1 mm (bank card thick)','d':'0.001'},
            {'v':0.1,'zh':'10 厘米（成人手掌宽）','en':'10 cm (palm width)','d':'0.1'},
            {'v':1,'zh':'1 米（门宽 / 儿童身高）','en':'1 m (door width)','d':'1'},
            {'v':1.7,'zh':'成人身高','en':'adult height','d':'1.7'},
            {'v':5,'zh':'一层楼高','en':'one storey','d':'5'},
            {'v':100,'zh':'足球场长度 / 短跑赛道','en':'football pitch length','d':'100'},
            {'v':400,'zh':'标准跑道一圈','en':'standard track lap','d':'400'},
            {'v':8848,'zh':'珠穆朗玛峰','en':'Mt Everest','d':'8848'},
            {'v':42195,'zh':'马拉松','en':'marathon','d':'42195'},
            {'v':6371000,'zh':'地球半径','en':'Earth radius','d':'6.37×10^6'},
            {'v':384400000,'zh':'地月距离','en':'Earth-Moon dist','d':'3.84×10^8'},
            {'v':149600000000,'zh':'日地距离（1 天文单位）','en':'Earth-Sun dist (1 AU)','d':'1.50×10^11'},
            {'v':9460730000000000,'zh':'1 光年','en':'1 light-year','d':'9.46×10^15'},
        ],
        'facts_zh':'1 英寸 = 2.54 厘米，1 英尺 ≈ 0.3048 米；英里 / 海里常用于里程与航海。',
        'facts_en':'1 inch = 2.54 cm; 1 foot ≈ 0.3048 m; mile / nautical mile are used for distance and navigation.',
    },
    'area-converter.html': {
        'factors': {'mm2':1e-6,'cm2':1e-4,'m2':1,'km2':1e6,'mu':666.6666667,'ha':10000,
                    'acre':4046.8564224,'ft2':0.09290304},
        'base_zh':'平方米','base_en':'m²',
        'refs':[
            {'v':1,'zh':'1 平方米（桌面大小）','en':'1 m² (tabletop)','d':'1'},
            {'v':9,'zh':'标准车位','en':'parking space','d':'9'},
            {'v':100,'zh':'小两居','en':'small flat','d':'100'},
            {'v':667,'zh':'1 亩','en':'1 mu','d':'667'},
            {'v':4047,'zh':'1 英亩','en':'1 acre','d':'4047'},
            {'v':7140,'zh':'标准足球场','en':'football pitch','d':'7140'},
            {'v':10000,'zh':'1 公顷','en':'1 hectare','d':'10000'},
            {'v':720000,'zh':'北京故宫','en':'Forbidden City','d':'7.2×10^5'},
            {'v':1000000,'zh':'1 平方公里','en':'1 km²','d':'1×10^6'},
        ],
        'facts_zh':'1 亩 ≈ 666.7 平方米，1 公顷 = 10000 平方米 = 15 亩；1 英亩 ≈ 4047 平方米。',
        'facts_en':'1 mu ≈ 666.7 m²; 1 hectare = 10,000 m² = 15 mu; 1 acre ≈ 4047 m².',
    },
    'volume-converter.html': {
        'factors': {'ml':1,'L':1000,'gal':3785.411784,'pt':473.176473,'qt':946.352946,
                    'cup':236.5882365,'tbsp':14.7867648,'tsp':4.92892159},
        'base_zh':'毫升','base_en':'mL',
        'refs':[
            {'v':5,'zh':'1 茶匙 ≈ 5 毫升','en':'1 tsp ≈ 5 mL','d':'5'},
            {'v':15,'zh':'1 汤匙 ≈ 15 毫升','en':'1 tbsp ≈ 15 mL','d':'15'},
            {'v':330,'zh':'一罐可乐（330 毫升）','en':'a can of cola (330 mL)','d':'330'},
            {'v':500,'zh':'一瓶矿泉水','en':'a water bottle','d':'500'},
            {'v':1000,'zh':'1 升（等于 1 公斤水）','en':'1 litre (= 1 kg water)','d':'1000'},
            {'v':18900,'zh':'桶装水','en':'water cooler jug','d':'18900'},
            {'v':150000,'zh':'浴缸','en':'bathtub','d':'1.5×10^5'},
            {'v':250000000,'zh':'标准游泳池','en':'swimming pool','d':'2.5×10^8'},
        ],
        'facts_zh':'1 升 = 1000 毫升 = 1 公斤水；1 美加仑 ≈ 3.785 升，1 杯 ≈ 237 毫升。',
        'facts_en':'1 L = 1000 mL = 1 kg water; 1 US gallon ≈ 3.785 L; 1 cup ≈ 237 mL.',
    },
    'weight-converter.html': {
        'factors': {'mg':0.001,'g':1,'kg':1000,'t':1000000,'oz':28.349523125,
                    'lb':453.59237,'ct':0.2,'liang':50,'jin':500},
        'base_zh':'克','base_en':'g',
        'refs':[
            {'v':1,'zh':'1 克（一枚回形针）','en':'1 g (a paperclip)','d':'1'},
            {'v':100,'zh':'一个苹果','en':'an apple','d':'100'},
            {'v':500,'zh':'1 斤','en':'1 jin (500 g)','d':'500'},
            {'v':1000,'zh':'1 千克（1 升水）','en':'1 kg (1 L water)','d':'1000'},
            {'v':5000,'zh':'一只猫','en':'a cat','d':'5000'},
            {'v':25000,'zh':'行李箱','en':'a suitcase','d':'25000'},
            {'v':60000,'zh':'成年人体重','en':'an adult','d':'60000'},
            {'v':250000,'zh':'钢琴','en':'a piano','d':'250000'},
            {'v':1000000,'zh':'1 吨（小型轿车）','en':'1 tonne (car)','d':'1×10^6'},
        ],
        'facts_zh':'1 斤 = 10 两 = 500 克；1 磅 ≈ 453.6 克；1 吨 = 1000 千克。',
        'facts_en':'1 jin = 500 g; 1 lb ≈ 453.6 g; 1 tonne = 1000 kg.',
    },
    'speed-converter.html': {
        'factors': {'mps':1,'kmh':0.277777778,'mph':0.44704,'knot':0.514444444,'mach':340.3},
        'base_zh':'米每秒','base_en':'m/s',
        'refs':[
            {'v':1.4,'zh':'步行（5 公里/时）','en':'walking (5 km/h)','d':'1.4'},
            {'v':5.6,'zh':'骑行（20 公里/时）','en':'cycling (20 km/h)','d':'5.6'},
            {'v':16.7,'zh':'城市快速路（60 公里/时）','en':'urban road (60 km/h)','d':'16.7'},
            {'v':27.8,'zh':'高速公路（100 公里/时）','en':'highway (100 km/h)','d':'27.8'},
            {'v':83.3,'zh':'高铁（300 公里/时）','en':'bullet train (300 km/h)','d':'83.3'},
            {'v':250,'zh':'客机巡航（900 公里/时）','en':'airliner (900 km/h)','d':'250'},
            {'v':340.3,'zh':'音速（1 马赫）','en':'speed of sound (Mach 1)','d':'340.3'},
            {'v':7800,'zh':'地球逃逸速度','en':'Earth escape velocity','d':'7800'},
        ],
        'facts_zh':'1 马赫 = 音速（海平面约 340 米/秒）；1 节 = 1 海里/时 ≈ 0.514 米/秒。',
        'facts_en':'1 Mach = speed of sound (≈340 m/s); 1 knot = 1 nautical mile/hour ≈ 0.514 m/s.',
    },
    'time-converter.html': {
        'factors': {'ms':0.001,'s':1,'min':60,'h':3600,'day':86400,'week':604800,'month':2629800,'year':31557600},
        'base_zh':'秒','base_en':'s',
        'refs':[
            {'v':0.001,'zh':'1 毫秒','en':'1 millisecond','d':'0.001'},
            {'v':0.3,'zh':'一次眨眼','en':'a blink','d':'0.3'},
            {'v':0.8,'zh':'一次心跳','en':'a heartbeat','d':'0.8'},
            {'v':3,'zh':'一次呼吸','en':'a breath','d':'3'},
            {'v':60,'zh':'1 分钟','en':'1 minute','d':'60'},
            {'v':2700,'zh':'一节课（45 分钟）','en':'a class (45 min)','d':'2700'},
            {'v':3600,'zh':'1 小时','en':'1 hour','d':'3600'},
            {'v':86400,'zh':'1 天','en':'1 day','d':'86400'},
            {'v':604800,'zh':'1 周','en':'1 week','d':'604800'},
            {'v':2629800,'zh':'1 个月（平均）','en':'1 month','d':'2.63×10^6'},
            {'v':31557600,'zh':'1 年','en':'1 year','d':'3.16×10^7'},
            {'v':3.16e9,'zh':'1 个世纪','en':'a century','d':'3.16×10^9'},
            {'v':1.58e11,'zh':'人类文明史（约 5000 年）','en':'human civilization (~5000 yr)','d':'1.58×10^11'},
            {'v':1.42e17,'zh':'地球年龄','en':'Earth age','d':'1.42×10^17'},
        ],
        'facts_zh':'1 年按 365.25 天计 ≈ 3.156×10^7 秒；"月"取平均朔望月 29.53 天。',
        'facts_en':'1 year ≈ 3.156×10^7 s (365.25 days); "month" uses the mean synodic month of 29.53 days.',
    },
    'energy-converter.html': {
        'factors': {'J':1,'kJ':1000,'cal':4.184,'kcal':4184,'Wh':3600,'kWh':3600000,'BTU':1055.05585},
        'base_zh':'焦耳','base_en':'J',
        'refs':[
            {'v':4184,'zh':'1 千卡（食物卡路里）','en':'1 kcal (food Calorie)','d':'4184'},
            {'v':10800,'zh':'1 节 5 号电池','en':'an AA battery','d':'1.08×10^4'},
            {'v':3.6e6,'zh':'1 度电（1 千瓦时）','en':'1 kWh (1 unit electricity)','d':'3.6×10^6'},
            {'v':4.184e6,'zh':'1 公斤 TNT','en':'1 kg of TNT','d':'4.18×10^6'},
            {'v':4.2e6,'zh':'一块巧克力（约 1000 千卡）','en':'a chocolate bar (~1000 kcal)','d':'4.2×10^6'},
            {'v':8.4e6,'zh':'成年人一天耗能','en':'adult daily energy','d':'8.4×10^6'},
            {'v':3.2e7,'zh':'1 升汽油','en':'1 litre gasoline','d':'3.2×10^7'},
            {'v':5e9,'zh':'一道闪电','en':'a lightning bolt','d':'5×10^9'},
            {'v':4.184e9,'zh':'1 吨 TNT','en':'1 tonne TNT','d':'4.18×10^9'},
            {'v':6.3e13,'zh':'广岛原子弹','en':'Hiroshima bomb','d':'6.3×10^13'},
            {'v':2e15,'zh':'里氏 7 级地震','en':'M7 earthquake','d':'2×10^15'},
        ],
        'facts_zh':'1 千卡 = 4184 焦耳；1 千瓦时（度）= 3.6×10^6 焦耳；1 英热单位 ≈ 1055 焦耳。',
        'facts_en':'1 kcal = 4184 J; 1 kWh = 3.6×10^6 J; 1 BTU ≈ 1055 J.',
    },
    'power-converter.html': {
        'factors': {'W':1,'kW':1000,'MW':1000000,'hp':735.49875,'hpI':745.699872},
        'base_zh':'瓦特','base_en':'W',
        'refs':[
            {'v':50,'zh':'一台笔记本','en':'a laptop','d':'50'},
            {'v':60,'zh':'老式白炽灯','en':'incandescent bulb','d':'60'},
            {'v':100,'zh':'人体静息代谢','en':'resting human metabolism','d':'100'},
            {'v':735.5,'zh':'1 公制马力','en':'1 metric horsepower','d':'735.5'},
            {'v':1000,'zh':'一台空调','en':'an air conditioner','d':'1000'},
            {'v':1800,'zh':'电热水壶','en':'electric kettle','d':'1800'},
            {'v':1e5,'zh':'汽车发动机','en':'car engine','d':'1×10^5'},
            {'v':8.8e6,'zh':'高铁动车组','en':'bullet-train unit','d':'8.8×10^6'},
            {'v':1e9,'zh':'核电站单堆','en':'one nuclear reactor','d':'1×10^9'},
            {'v':2.25e10,'zh':'三峡电站','en':'Three Gorges dam','d':'2.25×10^10'},
        ],
        'facts_zh':'1 公制马力(PS) ≈ 735.5 瓦，1 英制马力(hp) ≈ 745.7 瓦；1 千瓦 = 1000 瓦。',
        'facts_en':'1 metric hp (PS) ≈ 735.5 W; 1 imperial hp ≈ 745.7 W; 1 kW = 1000 W.',
    },
    'pressure-converter.html': {
        'factors': {'Pa':1,'kPa':1000,'MPa':1000000,'bar':100000,'psi':6894.757293,'atm':101325,'mmHg':133.322368},
        'base_zh':'帕','base_en':'Pa',
        'refs':[
            {'v':15999,'zh':'正常收缩压（120 mmHg）','en':'normal systolic BP (120 mmHg)','d':'1.6×10^4'},
            {'v':1e5,'zh':'10 米水深额外水压','en':'+10 m water depth','d':'1×10^5'},
            {'v':2.4e5,'zh':'汽车轮胎胎压','en':'car tyre pressure','d':'2.4×10^5'},
            {'v':3e5,'zh':'碳酸饮料瓶内压','en':'fizzy-drink bottle','d':'3×10^5'},
            {'v':101325,'zh':'1 个标准大气压','en':'1 atmosphere','d':'1.01×10^5'},
            {'v':1e6,'zh':'深海 100 米水压','en':'100 m ocean depth','d':'1×10^6'},
            {'v':2e7,'zh':'液压系统','en':'hydraulic system','d':'2×10^7'},
            {'v':2.5e8,'zh':'钢铁抗压强度','en':'steel compressive strength','d':'2.5×10^8'},
            {'v':1e11,'zh':'金刚石压砧','en':'diamond anvil','d':'1×10^11'},
            {'v':3.6e11,'zh':'地心压力','en':'Earth core pressure','d':'3.6×10^11'},
        ],
        'facts_zh':'1 标准大气压 ≈ 101325 帕 = 1.013 巴；水银柱每升高 1 毫米 ≈ 133.3 帕；水下每深 10 米约增 1 个大气压。',
        'facts_en':'1 atm ≈ 101325 Pa = 1.013 bar; each 1 mm of mercury ≈ 133.3 Pa; every 10 m of water adds ~1 atm.',
    },
    'data-rate-converter.html': {
        'factors': {'bps':1,'kbps':1000,'Mbps':1000000,'Gbps':1000000000},
        'base_zh':'比特每秒','base_en':'bps',
        'refs':[
            {'v':5.6e4,'zh':'拨号上网（56k）','en':'dial-up (56k)','d':'5.6×10^4'},
            {'v':1e6,'zh':'ADSL 宽带','en':'ADSL','d':'1×10^6'},
            {'v':1e8,'zh':'4G / 百兆宽带','en':'4G / 100 Mbps','d':'1×10^8'},
            {'v':1e9,'zh':'千兆宽带 / 5G 峰值','en':'1 Gbps / 5G peak','d':'1×10^9'},
            {'v':5e9,'zh':'USB 3.0','en':'USB 3.0','d':'5×10^9'},
            {'v':1e10,'zh':'万兆网卡','en':'10 GbE','d':'1×10^10'},
            {'v':1e13,'zh':'海底光缆','en':'submarine cable','d':'1×10^13'},
        ],
        'facts_zh':'单位按十进制：1 kbps = 1000 bps，1 Mbps = 10^6 bps；注意与存储的 KiB(1024) 区分。',
        'facts_en':'Decimal units: 1 kbps = 1000 bps, 1 Mbps = 10^6 bps; do not confuse with binary KiB (1024).',
    },
    'angle-converter.html': {
        'factors': {'deg':1,'rad':57.29577951308232,'grad':0.9,'rev':360},
        'base_zh':'度','base_en':'deg',
        'refs':[
            {'v':6,'zh':'分针走 1 分钟','en':'minute hand, 1 min','d':'6'},
            {'v':23.4,'zh':'地球黄赤交角','en':'Earth axial tilt','d':'23.4'},
            {'v':30,'zh':'时针走 1 小时','en':'hour hand, 1 hour','d':'30'},
            {'v':36,'zh':'五角星尖角','en':'5-point star tip','d':'36'},
            {'v':57.2958,'zh':'1 弧度','en':'1 radian','d':'57.3'},
            {'v':60,'zh':'正三角形内角','en':'equilateral triangle angle','d':'60'},
            {'v':90,'zh':'直角 / 正方形内角','en':'right angle','d':'90'},
            {'v':180,'zh':'平角','en':'straight angle','d':'180'},
            {'v':360,'zh':'周角','en':'full turn','d':'360'},
        ],
        'facts_zh':'360 度 = 2π 弧度 ≈ 6.283 弧度；1 弧度 ≈ 57.3 度；直角 = 90 度，周角 = 360 度。',
        'facts_en':'360° = 2π rad ≈ 6.283 rad; 1 rad ≈ 57.3°; right angle = 90°, full turn = 360°.',
    },
    'frequency-converter.html': {
        'factors': {'Hz':1,'kHz':1000,'MHz':1000000,'GHz':1000000000,'rpm':0.0166666667},
        'base_zh':'赫兹','base_en':'Hz',
        'refs':[
            {'v':1.2,'zh':'静息心跳','en':'resting heartbeat','d':'1.2'},
            {'v':20,'zh':'人耳可闻下限','en':'lowest audible tone','d':'20'},
            {'v':27.5,'zh':'钢琴最低音（A0）','en':'lowest piano note (A0)','d':'27.5'},
            {'v':50,'zh':'市电频率','en':'mains electricity','d':'50'},
            {'v':261.6,'zh':'中央 C','en':'middle C','d':'261.6'},
            {'v':2e4,'zh':'人耳可闻上限','en':'highest audible tone','d':'2×10^4'},
            {'v':1e8,'zh':'FM 广播','en':'FM radio band','d':'1×10^8'},
            {'v':2.4e9,'zh':'Wi-Fi 2.4G','en':'Wi-Fi 2.4G','d':'2.4×10^9'},
            {'v':3e9,'zh':'CPU 主频','en':'CPU clock','d':'3×10^9'},
            {'v':5e14,'zh':'可见光','en':'visible light','d':'5×10^14'},
        ],
        'facts_zh':'1 赫兹 = 每秒 1 次；1 转/分(rpm) = 1/60 赫兹；人耳可听范围约 20 Hz–20 kHz。',
        'facts_en':'1 Hz = one cycle per second; 1 rpm = 1/60 Hz; human hearing spans ~20 Hz–20 kHz.',
    },
}

TMPL = r"""<!-- __charRef_start -->
<section class="char-module" id="__charRef" style="margin-top:16px;">
<div id="__charRefBox"></div>
</section>
<script>
(function(){
  var F = __UXC_FACTORS__;
  var REFS = __UXC_REFS__;
  var BASE = __UXC_BASE__;
  var FACTS = __UXC_FACTS__;
  function isEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function fmt(n){
    var a=Math.abs(n);
    if(a>=1e9 || (a>0 && a<1e-3)){ return n.toExponential(3).replace(/e\+?(-?\d+)/, '×10^$1'); }
    return (Math.round(n*1e6)/1e6).toString();
  }
  function render(){
    var box=document.getElementById('__charRefBox');
    if(!box) return;
    var inp=document.getElementById('inputVal');
    var sel=document.getElementById('fromUnit');
    if(!inp||!sel) return;
    var v=parseFloat(inp.value);
    var from=sel.value;
    if(!isFinite(v)||!F[from]){ box.innerHTML=''; return; }
    var base=v*F[from];
    var best=null, bd=1e18;
    for(var i=0;i<REFS.length;i++){
      var rv=REFS[i].v;
      if(!(rv>0)) continue;
      var d=Math.abs(Math.log10(Math.abs(base)+1e-30)-Math.log10(rv));
      if(d<bd){ bd=d; best=REFS[i]; }
    }
    var en=isEn();
    var bname=en?BASE[1]:BASE[0];
    var html='';
    html+='<div class="card" style="margin-top:0;">';
    html+='<h3>'+(en?'Scale sense: how big is it really?':'📐 尺度感知：这到底有多大')+'</h3>';
    html+='<p>'+(en?'Your input ≈ ':'你的输入 ≈ ')+fmt(base)+' '+bname+'</p>';
    if(best){
      html+='<p style="font-weight:600;color:var(--primary);">💡 ≈ '+best[en?'en':'zh']+' ('+best.d+' '+bname+')</p>';
    }
    html+='<details style="margin-top:6px;"><summary style="cursor:pointer;color:var(--primary);">'+(en?'Typical real-world references':'常见实物参照')+'</summary><ul style="font-size:13px;line-height:1.8;margin:6px 0 0;padding-left:18px;">';
    for(var j=0;j<REFS.length;j++){
      var r=REFS[j];
      html+='<li>'+r[en?'en':'zh']+(en?': ':'：')+r.d+' '+bname+'</li>';
    }
    html+='</ul></details>';
    html+='<p style="font-size:12px;color:var(--text-muted);margin-top:8px;">'+(en?FACTS[1]:FACTS[0])+'</p>';
    html+='</div>';
    box.innerHTML=html;
  }
  var f0=(typeof convert==='function')?convert:null;
  if(f0){ convert=function(){ var r=f0.apply(null,arguments); try{ render(); }catch(e){} return r; }; }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})();
</script>
<!-- __charRef_end -->"""


def build(cfg):
    s = TMPL
    s = s.replace('__UXC_FACTORS__', json.dumps(cfg['factors'], ensure_ascii=False))
    s = s.replace('__UXC_REFS__', json.dumps(cfg['refs'], ensure_ascii=False))
    s = s.replace('__UXC_BASE__', json.dumps([cfg['base_zh'], cfg['base_en']], ensure_ascii=False))
    s = s.replace('__UXC_FACTS__', json.dumps([cfg['facts_zh'], cfg['facts_en']], ensure_ascii=False))
    return s


def strip_old(t):
    # 1) 去掉带起止标记的新块（幂等重注）
    t = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', t, flags=re.S)
    # 2) 去掉遗留的无标记旧块：<section ...id="__charRef"> ... </section>（script 在 section 内）
    t = re.sub(r'<section class="char-module" id="__charRef".*?</section>', '', t, flags=re.S)
    return t


def inject(path, snippet):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        print('MISSING', path); return False
    t = open(p, encoding='utf-8').read()
    t = strip_old(t)
    if '</body>' not in t:
        print('NO_BODY', path); return False
    t = t.replace('</body>', snippet + '\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(t)
    print('INJECTED', path); return True


def main():
    for name, cfg in TARGETS.items():
        inject('tools/life/' + name, build(cfg))


if __name__ == '__main__':
    main()
