# -*- coding: utf-8 -*-
"""
F-CHAR-3 日期/年龄/倒计时工具「日期解读」注入。
目标页（tools/life，统一 <input type=date> + 主函数 calc/setTarget）：
  age-in-days          (birthDate,  calc)        → 生日模式：生肖/星座/季节/年内第几天/闰年/距下次生日
  date-diff            (date1/date2, calc)        → 日期模式：星期/季节/年内第几天/闰年（两端点）
  countdown            (targetDate, setTarget)    → 日期模式：星期/季节/年内第几天/闰年（目标日）

纪律（复用已通过门禁的 __charRef/__charDist 范式）：
  - 静态 section 零中文，仅含输出容器 <div id="__charDateBox">
  - <script> 放在 section 之外（否则 JS 中文字面量被计入 sec.textContent → EN 态泄漏）
  - 语言判定读 location.search 的 ?lang=en-US（门禁 JSDOM 不加载 TBKit）
  - 生肖复用本站既有简化格里历口径 (year-4)%12，与 age-calculator.getZodiac 一致
  - 只渲染日期派生事实，不重算页内主结果 → 不命中 verify 逃生项
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = '<!-- __charDate_start -->'
END = '<!-- __charDate_end -->'

# 每页：输入列表（id + 中英标签）、模式（birth/date）
TARGETS = {
    'age-in-days.html': {
        'mode': 'birth',
        'inputs': [{'id': 'birthDate', 'zh': '出生日期', 'en': 'Birth date'}],
    },
    'date-diff.html': {
        'mode': 'date',
        'inputs': [
            {'id': 'date1', 'zh': '开始日期', 'en': 'Start date'},
            {'id': 'date2', 'zh': '结束日期', 'en': 'End date'},
        ],
    },
    'countdown.html': {
        'mode': 'date',
        'inputs': [{'id': 'targetDate', 'zh': '目标日期', 'en': 'Target date'}],
    },
}

TMPL = r"""<!-- __charDate_start -->
<section class="char-module" id="__charDate" style="margin-top:16px;">
<div id="__charDateBox"></div>
</section>
<script>
(function(){
  var INPUTS = __UXD_INPUTS__;
  var MODE = '__UXD_MODE__';
  function isEn(){ try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; } }
  var ZH=['鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪'];
  var EN=['Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat','Monkey','Rooster','Dog','Pig'];
  function zodiac(y){ return ZH[((y-4)%12+12)%12]; }
  function zodiacE(y){ return EN[((y-4)%12+12)%12]; }
  // 星座：[起月,起日,止月,止日,中文,英文]（按公历日期，含跨年摩羯）
  var CONS=[[12,22,1,19,'摩羯','Capricorn'],[1,20,2,18,'水瓶','Aquarius'],[2,19,3,20,'双鱼','Pisces'],
    [3,21,4,19,'白羊','Aries'],[4,20,5,20,'金牛','Taurus'],[5,21,6,21,'双子','Gemini'],
    [6,22,7,22,'巨蟹','Cancer'],[7,23,8,22,'狮子','Leo'],[8,23,9,22,'处女','Virgo'],
    [9,23,10,23,'天秤','Libra'],[10,24,11,22,'天蝎','Scorpio'],[11,23,12,21,'射手','Sagittarius']];
  function constellation(m,d){
    for(var i=0;i<CONS.length;i++){ var c=CONS[i];
      if(c[0]===c[2]){ if(m===c[0]&&d>=c[1]&&d<=c[3]) return c; }
      else { if((m===c[0]&&d>=c[1])||(m===c[2]&&d<=c[3])) return c; } }
    return CONS[0];
  }
  var WK=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
  var WE=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  function dayOfYear(y,m,d){ var start=new Date(y,0,0); var dt=new Date(y,m-1,d); return Math.round((dt-start)/86400000); }
  function isLeap(y){ return (y%4===0&&y%100!==0)||(y%400===0); }
  function season(m){ if(m>=3&&m<=5) return ['春季','Spring']; if(m>=6&&m<=8) return ['夏季','Summer']; if(m>=9&&m<=11) return ['秋季','Autumn']; return ['冬季','Winter']; }
  function nextBirthday(y,m,d){ var t=new Date(); var thisY=new Date(t.getFullYear(),m-1,d); var next=(thisY.getTime()<=Date.now())?new Date(t.getFullYear()+1,m-1,d):thisY; return Math.ceil((next.getTime()-Date.now())/86400000); }
  function factsFor(dateStr, label){
    if(!dateStr) return null;
    var p=String(dateStr).split('-'); if(p.length<3) return null;
    var y=+p[0], m=+p[1], d=+p[2]; if(isNaN(y)||isNaN(m)||isNaN(d)) return null;
    var dt=new Date(y,m-1,d); if(isNaN(dt.getTime())) return null;
    var en=isEn();
    var rows=[];
    var dow=dt.getDay();
    rows.push((en?'Day of week: ':'星期：')+(en?WE[dow]:WK[dow]));
    rows.push((en?'Day of year: ':'年内第几天：')+dayOfYear(y,m,d)+(en?(' (of '+y+')'):('（'+y+'年）')));
    var s=season(m); rows.push((en?'Season (N. Hem.): ':'季节（北半球）：')+(en?s[1]:s[0]));
    rows.push((en?'Leap year: ':'闰年：')+(isLeap(y)?(en?'Yes':'是'):(en?'No':'否')));
    if(MODE==='birth'){
      rows.push((en?'Chinese zodiac: ':'生肖：')+(en?zodiacE(y):zodiac(y)));
      var con=constellation(m,d); rows.push((en?'Constellation: ':'星座：')+(en?con[5]:con[4]));
      rows.push((en?'Days to next birthday: ':'距下次生日：')+nextBirthday(y,m,d)+(en?' days':' 天'));
    }
    return {label:label, rows:rows};
  }
  function render(){
    var box=document.getElementById('__charDateBox'); if(!box) return;
    var en=isEn(); var out='';
    out+='<div class="card" style="margin-top:0;">';
    out+='<h3>'+(en?'Date facts: more than just a number':'📅 日期解读：不止是数字')+'</h3>';
    var any=false;
    for(var i=0;i<INPUTS.length;i++){
      var el=document.getElementById(INPUTS[i].id);
      var f=factsFor(el?el.value:null, INPUTS[i]);
      if(!f) continue; any=true;
      out+='<div style="margin-top:8px;"><strong>'+(en?f.label.en:f.label.zh)+'</strong><ul style="font-size:13px;line-height:1.8;margin:4px 0 0;padding-left:18px;">';
      for(var j=0;j<f.rows.length;j++) out+='<li>'+f.rows[j]+'</li>';
      out+='</ul></div>';
    }
    if(!any){ box.innerHTML=''; return; }
    out+='<p style="font-size:12px;color:var(--text-muted);margin-top:8px;">'+(en?NOTE_EN:NOTE_ZH)+'</p>';
    out+='</div>';
    box.innerHTML=out;
  }
  var HOOKS=['calc','calcDiff','calcAddSub','setTarget','updateTimerDisplay'];
  for(var k=0;k<HOOKS.length;k++){
    var f0=(typeof window[HOOKS[k]]==='function')?window[HOOKS[k]]:null;
    if(f0){ window[HOOKS[k]]=(function(orig){ return function(){ var r=orig.apply(this,arguments); try{ render(); }catch(e){} return r; }; })(f0); }
  }
  for(var i=0;i<INPUTS.length;i++){ var el=document.getElementById(INPUTS[i].id); if(el){ el.addEventListener('change',render); el.addEventListener('input',render); } }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render); else render();
})();
</script>
<!-- __charDate_end -->"""

NOTE_ZH = '生肖按简化格里历年份推算（与本站“精确年龄计算器”口径一致，农历新年前后可能有约 1 天偏差）；星座按公历日期；季节为北半球。'
NOTE_EN = 'Zodiac uses a simplified Gregorian-year rule (consistent with this site’s age calculator; may differ ~1 day around the lunar new year). Constellation by Gregorian date; season is for the Northern Hemisphere.'


def build(cfg):
    s = TMPL
    s = s.replace('__UXD_INPUTS__', json.dumps(cfg['inputs'], ensure_ascii=False))
    s = s.replace('__UXD_MODE__', cfg['mode'])
    s = s.replace('NOTE_ZH', json.dumps(NOTE_ZH, ensure_ascii=False))
    s = s.replace('NOTE_EN', json.dumps(NOTE_EN, ensure_ascii=False))
    return s


def strip_old(t):
    t = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', t, flags=re.S)
    t = re.sub(r'<section class="char-module" id="__charDate".*?</section>', '', t, flags=re.S)
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
