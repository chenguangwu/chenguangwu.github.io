#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _ux_char_fin.py — UX 工具特异性功能重做 · F-CHAR-11（DEV-PLAN F-CHAR-5 财务衍生）
# 给「财务金融类」工具注入自包含的领域专属解读模块（"这数字在现实里意味着什么"）。
#
# 背景：tools/finance 全族 115 页（计算类约 50 页），grep「解读|意味着|提示|建议|说明什么」
#       命中 **0**；页面只有图表/明细表/通用"注意事项"三条模板，没有任何领域判读知识。
#       但 installment-real-rate 页自身已含 IRR/EAR/名义对比（已是解读），主动不注入避免重复。
#
# 本批 4 页（最高杠杆、误解高发）：
#   compound-interest     复利：72 法则、复利 vs 单利差、频率极限
#   credit-card-interest  信用卡：日息万分之五 → 名义 18.25% / 实际 EAR 19.6%、最低还款雪球、免息期
#   inflation-calculator  通胀：70 法则购买力减半、名义 vs 实际
#   mortgage-prepayment   提前还款：等额本息前期利重、临界点、缩短期限 vs 减少月供
#
# 依据（真实金融常识，非自拟）：
#   72 法则：翻倍年数 ≈ 72 / 年化%   （r 在 6%~10% 最准）
#   70 法则：购买力减半年数 ≈ 70 / 通胀%
#   信用卡 EAR = (1 + 日利率×30)^12 - 1（按月复利近似）
#   等额本息前 1/3 期限利息占比高，提前还款越晚省息越少
#
# 模式沿用 F-CHAR-6..10 已验证：自包含 IIFE / 静态零中文 / JS 按 lang 填文案 /
# 守卫 TBKit / hook calc / 构建安全（插 </body> 前）。
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- 公共 JS 片断
COMMON = r'''
  function __finIsEn(){
    try { if (typeof TBKit !== 'undefined' && TBKit.util && TBKit.util.isEn()) return true; } catch(e){}
    try { return new URLSearchParams(location.search).get('lang') === 'en-US'; } catch(e){}
    return false;
  }
  function __finNum(id){
    var e = document.getElementById(id);
    if (!e) return NaN;
    return parseFloat(e.value);
  }
  // x 已是百分数数值（如 18.25），输出 "18.25%"
  function __finPct(x){ return (isFinite(x) ? x.toFixed(2) : '--') + '%'; }
  function __finRow(k, v){
    return '<tr><td style="padding:5px 6px;border-bottom:1px solid var(--border);width:34%;vertical-align:top;">'
         + k + '</td><td style="padding:5px 6px;border-bottom:1px solid var(--border);">' + v + '</td></tr>';
  }
  function __finBar(ratio, color){
    var w = Math.max(0, Math.min(1, ratio)) * 100;
    return '<div style="background:var(--border);border-radius:6px;height:14px;overflow:hidden;margin:6px 0 2px;">'
         + '<div style="width:' + w.toFixed(1) + '%;height:100%;background:' + color + ';"></div></div>';
  }
'''


def wrap(section_id, update_fn, hook_ids, extra_js, title, desc, note, hook_fn='calc'):
    ids_js = ", ".join("'%s'" % i for i in hook_ids)
    return r'''<section class="char-module" id="%s" style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
  <h2 id="%sTitle" style="font-size:16px;margin:0 0 8px;"></h2>
  <p id="%sDesc" style="font-size:13px;color:var(--text-muted);margin:0 0 10px;"></p>
  <div id="%sBadge" style="display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-size:13px;font-weight:600;margin-bottom:4px;"></div>
  <div id="%sVal" style="font-size:15px;font-weight:600;margin:8px 0 6px;"></div>
  <div id="%sBar"></div>
  <table style="width:100%%;border-collapse:collapse;font-size:13px;">
    <tbody id="%sRows"></tbody>
  </table>
  <p id="%sNote" style="font-size:12px;color:var(--text-muted);margin-top:10px;line-height:1.7;"></p>
</section>
<script>
(function(){
%s
%s
  function __finUpdate(){ %s }
  function __finInit(){
    var en = __finIsEn();
    document.getElementById('%sTitle').textContent = %s;
    document.getElementById('%sDesc').textContent = %s;
    document.getElementById('%sNote').textContent = %s;
    __finUpdate();
    var IDS = [%s];
    IDS.forEach(function(id){
      var el = document.getElementById(id);
      if (!el || !el.addEventListener) return;
      el.addEventListener('input', __finUpdate);
      el.addEventListener('change', __finUpdate);
    });
    try {
      if (typeof %s === 'function' && !%s.__finHooked) {
        var __orig = %s;
        %s = function(){ __orig.apply(this, arguments); try { __finUpdate(); } catch(e){} };
        %s.__finHooked = true;
      }
    } catch(e){}
  }
  if (document.readyState && document.readyState !== 'loading') __finInit();
  else document.addEventListener('DOMContentLoaded', __finInit);
})();
</script>
''' % (section_id, section_id, section_id, section_id, section_id,
       section_id, section_id, section_id,
       COMMON, extra_js, update_fn,
       section_id, title, section_id, desc, section_id, note,
       ids_js, hook_fn, hook_fn, hook_fn, hook_fn, hook_fn)


# ============================================================ 1. 复利
CI_EXTRA = r'''
  function __ciRead(){
    return {
      P: __finNum('principal'),
      r: __finNum('rate'),      // 年化 %
      t: __finNum('years'),
      annual: __finNum('annual') || 0
    };
  }
'''
CI_UPDATE = r'''
    var d = __ciRead();
    var en = __finIsEn();
    var box = document.getElementById('__charCiVal');
    var rows = document.getElementById('__charCiRows');
    var bar = document.getElementById('__charCiBar');
    var badge = document.getElementById('__charCiBadge');
    if (!(d.P > 0) || !(d.r > 0) || !(d.t > 0)) {
      box.textContent = en ? 'Enter principal, annual rate and years.' : '请输入本金、年化利率与年限。';
      rows.innerHTML = ''; bar.innerHTML = ''; badge.textContent = '';
      return;
    }
    var rr = d.r / 100;
    // 72 法则：翻倍年数
    var rule72 = 72 / d.r;
    // 复利终值（仅本金，不计追加）：A = P(1+r)^t
    var A = d.P * Math.pow(1 + rr, d.t);
    // 单利终值
    var Asimple = d.P * (1 + rr * d.t);
    var extra = A - Asimple;                       // 复利比单利多出的部分
    var extraRatio = extra / Asimple;               // 多出的相对比例
    // 频率极限：连续复利因子 e^(rt) 与逐年比较的"额外增益"
    var cont = d.P * Math.exp(rr * d.t);
    var freqGain = cont - A;                        // 从年复利到连续复利的额外量（频率极限效应）
    var badgeTxt = en ? 'Compound interest' : '复利';
    var valTxt = en
      ? 'After ' + d.t + ' years: ¥' + A.toFixed(0) + ' (compound), vs ¥' + Asimple.toFixed(0) + ' (simple)'
      : d.t + ' 年后：¥' + A.toFixed(0) + '（复利），若单利仅 ¥' + Asimple.toFixed(0);
    var html = '';
    html += __finRow(
      en ? 'Doubling time (Rule of 72)' : '翻倍年数（72 法则）',
      en ? '≈ ' + rule72.toFixed(1) + ' years (72 ÷ ' + d.r + '%)'
         : '≈ ' + rule72.toFixed(1) + ' 年（72 ÷ ' + d.r + '%）'
    );
    html += __finRow(
      en ? 'Compound vs simple gain' : '复利比单利多赚',
      en ? '¥' + extra.toFixed(0) + ' (+' + (extraRatio * 100).toFixed(1) + '%)'
         : '¥' + extra.toFixed(0) + '（多 ' + (extraRatio * 100).toFixed(1) + '%）'
    );
    html += __finRow(
      en ? 'Going from annual to continuous compounding' : '从年复利到连续复利的极限',
      en ? 'only +¥' + freqGain.toFixed(0) + ' more — diminishing returns of compounding frequency'
         : '仅再多 ¥' + freqGain.toFixed(0) + ' — 计息频率的边际收益递减'
    );
    rows.innerHTML = html;
    // 进度条：复利终值相对单利的超额占比（封顶 100%）
    bar.innerHTML = __finBar(Math.min(1, extraRatio), '#10b981');
    badge.textContent = badgeTxt;
    badge.style.background = '#10b981';
  '''


# ============================================================ 2. 信用卡利息
CC_EXTRA = r'''
  function __ccRead(){
    return {
      bill: __finNum('billAmount'),
      daily: __finNum('dailyRate'),   // 日利率 %（0.05 = 万分之五）
      minR: __finNum('minRatio')      // 最低还款比例 %（如 10）
    };
  }
'''
CC_UPDATE = r'''
    var d = __ccRead();
    var en = __finIsEn();
    var box = document.getElementById('__charCcVal');
    var rows = document.getElementById('__charCcRows');
    var bar = document.getElementById('__charCcBar');
    var badge = document.getElementById('__charCcBadge');
    if (!(d.daily > 0)) {
      box.textContent = en ? 'Enter the daily rate to see the real annual cost.' : '请输入日利率，查看真实年化成本。';
      rows.innerHTML = ''; bar.innerHTML = ''; badge.textContent = '';
      return;
    }
    var dailyRate = d.daily / 100;                  // 转为小数
    var nominalAnnual = d.daily * 365;              // 名义年化（按天乘）
    var monthlyRate = dailyRate * 30;               // 每月按 30 天近似
    var ear = (Math.pow(1 + monthlyRate, 12) - 1) * 100;  // 实际有效年利率
    var gap = ear - nominalAnnual;
    // 最低还款：以 10% 为例，仅还利息部分滚雪球（粗略演示）
    var minR = (d.minR > 0 ? d.minR : 10) / 100;
    var badgeTxt = en ? 'Credit-card interest' : '信用卡利息';
    var valTxt = en
      ? 'Stated daily ' + d.daily + '% → real APR ' + ear.toFixed(2) + '% (not ' + nominalAnnual.toFixed(2) + '%)'
      : '标称日息 ' + d.daily + '% → 真实年化 ' + ear.toFixed(2) + '%（不是 ' + nominalAnnual.toFixed(2) + '%）';
    var html = '';
    html += __finRow(
      en ? 'Nominal APR (daily × 365)' : '名义年化（日息 × 365）',
      __finPct(nominalAnnual)
    );
    html += __finRow(
      en ? 'Effective APR (compounded monthly)' : '实际有效年利率 EAR（按月复利）',
      __finPct(ear) + (en ? ' (higher!)' : '（更高！）')
    );
    html += __finRow(
      en ? 'Hidden premium of compounding' : '复利带来的隐性溢价',
      en ? '+ ' + __finPct(gap) + ' above the "nominal" number'
         : '比"名义"数字高出 ' + __finPct(gap)
    );
    html += __finRow(
      en ? 'Minimum payment trap' : '最低还款陷阱',
      en ? 'Paying only ~' + (minR * 100).toFixed(0) + '% keeps the balance accruing daily interest — it can take years to clear.'
         : '只还约 ' + (minR * 100).toFixed(0) + '% 时余额按日计息滚雪球，可能要数年才还清。'
    );
    rows.innerHTML = html;
    // 进度条：EAR 相对名义的溢价占比
    bar.innerHTML = __finBar(Math.min(1, gap / Math.max(nominalAnnual, 0.01)), '#ef4444');
    badge.textContent = badgeTxt;
    badge.style.background = '#ef4444';
  '''


# ============================================================ 3. 通胀
INFL_EXTRA = r'''
  function __inflRead(){
    return {
      amt: __finNum('amt'),
      r: __finNum('rate'),
      t: __finNum('years')
    };
  }
'''
INFL_UPDATE = r'''
    var d = __inflRead();
    var en = __finIsEn();
    var box = document.getElementById('__charInflVal');
    var rows = document.getElementById('__charInflRows');
    var bar = document.getElementById('__charInflBar');
    var badge = document.getElementById('__charInflBadge');
    if (!(d.amt > 0) || !(d.r > 0) || !(d.t > 0)) {
      box.textContent = en ? 'Enter amount, inflation rate and years.' : '请输入金额、通胀率与年限。';
      rows.innerHTML = ''; bar.innerHTML = ''; badge.textContent = '';
      return;
    }
    var rr = d.r / 100;
    var halfLife = 70 / d.r;                        // 70 法则：购买力减半
    var need = d.amt * Math.pow(1 + rr, d.t);       // 未来维持同样购买力所需
    var lost = (1 - 1 / Math.pow(1 + rr, d.t)) * 100;  // 购买力流失比例
    var badgeTxt = en ? 'Inflation' : '通货膨胀';
    var valTxt = en
      ? 'In ' + d.t + ' years ¥' + d.amt.toFixed(0) + ' buys what ¥' + (d.amt / Math.pow(1 + rr, d.t)).toFixed(0) + ' buys today'
      : d.t + ' 年后 ¥' + d.amt.toFixed(0) + ' 只相当于今天的 ¥' + (d.amt / Math.pow(1 + rr, d.t)).toFixed(0);
    var html = '';
    html += __finRow(
      en ? 'Purchasing-power half-life (Rule of 70)' : '购买力减半年数（70 法则）',
      en ? '≈ ' + halfLife.toFixed(1) + ' years at ' + d.r + '%'
         : '≈ ' + halfLife.toFixed(1) + ' 年（通胀 ' + d.r + '% 时）'
    );
    html += __finRow(
      en ? 'Amount needed to keep parity' : '为保持同等购买力所需金额',
      en ? '¥' + need.toFixed(0) + ' (was ¥' + d.amt.toFixed(0) + ')'
         : '¥' + need.toFixed(0) + '（原 ¥' + d.amt.toFixed(0) + '）'
    );
    html += __finRow(
      en ? 'Purchasing power lost' : '购买力流失',
      __finPct(lost) + (en ? ' over ' + d.t + ' years' : '（' + d.t + ' 年间）')
    );
    rows.innerHTML = html;
    bar.innerHTML = __finBar(lost / 100, '#f59e0b');
    badge.textContent = badgeTxt;
    badge.style.background = '#f59e0b';
  '''


# ============================================================ 4. 提前还款
MP_EXTRA = r'''
  function __mpRead(){
    return {
      p: __finNum('principal'),
      annual: __finNum('rate'),
      months: __finNum('months'),
      mp: __finNum('monthly'),
      prepay: __finNum('prepay') || 0
    };
  }
'''
MP_UPDATE = r'''
    var d = __mpRead();
    var en = __finIsEn();
    var box = document.getElementById('__charMpVal');
    var rows = document.getElementById('__charMpRows');
    var bar = document.getElementById('__charMpBar');
    var badge = document.getElementById('__charMpBadge');
    if (!(d.p > 0) || !(d.annual > 0) || !(d.months > 0) || !(d.mp > 0)) {
      box.textContent = en ? 'Enter loan principal, rate, term and monthly payment.' : '请输入贷款本金、利率、期限与月供。';
      rows.innerHTML = ''; bar.innerHTML = ''; badge.textContent = '';
      return;
    }
    var m = d.annual / 100 / 12;
    // 首月利息（等额本息前期利息占比高）
    var firstInterest = d.p * m;
    var firstPrincipal = d.mp - firstInterest;
    var firstIntRatio = firstInterest / d.mp;
    // 临界点：已还期数超过 1/3 总期后，提前还款省息效果大幅下降
    var oneThird = d.months / 3;
    // 提前还款占本金比例
    var prepayRatio = d.prepay / d.p;
    var badgeTxt = en ? 'Early repayment' : '提前还款';
    var valTxt = en
      ? 'First-month interest is ' + (firstIntRatio * 100).toFixed(1) + '% of your payment — most of early payments go to interest.'
      : '首月利息占月供的 ' + (firstIntRatio * 100).toFixed(1) + '%，前期还款大多在还利息。';
    var html = '';
    html += __finRow(
      en ? 'First-month interest share' : '首月利息占月供比',
      __finPct(firstIntRatio * 100) + (en ? ' (top-heavy)' : '（前重后轻）')
    );
    html += __finRow(
      en ? 'When prepaying pays off most' : '提前还款最划算的时点',
      en ? 'Best within the first 1/3 of the term (' + oneThird.toFixed(0) + ' of ' + d.months + ' months)'
         : '最好在前 1/3 期限内（共 ' + d.months + ' 期中的前 ' + oneThird.toFixed(0) + ' 期）'
    );
    html += __finRow(
      en ? 'Strategy: shorten term vs lower payment' : '策略：缩短期限 vs 减少月供',
      en ? 'Shortening the term saves more total interest than lowering the monthly payment.'
         : '同样一笔提前还款，「缩短期限」比「减少月供」省下的总利息更多。'
    );
    if (d.prepay > 0) {
      html += __finRow(
        en ? 'This prepayment amount' : '本次提前还款额',
        en ? (prepayRatio * 100).toFixed(1) + '% of principal — the earlier you do it, the more interest you skip.'
           : '占本金 ' + (prepayRatio * 100).toFixed(1) + '%，越早还省的利息越多。'
      );
    }
    rows.innerHTML = html;
    bar.innerHTML = __finBar(firstIntRatio, '#6366f1');
    badge.textContent = badgeTxt;
    badge.style.background = '#6366f1';
  '''


# ---------------------------------------------------------------- 组装
def ci_section():
    return wrap('__charCi', CI_UPDATE, ['principal', 'rate', 'years', 'annual'],
                CI_EXTRA,
                "en ? '📈 What your compound interest really means' : '📈 这笔复利到底意味着什么'",
                "en ? 'The headline number hides three things: how fast it doubles, how much extra compounding adds over simple interest, and why chasing more frequent compounding has vanishing returns.' : '表面数字藏着三件事：多久翻倍、复利比单利多赚多少、以及为什么计息频率越密边际收益越小。'",
                "en ? 'Rule of 72 is most accurate for rates between 6% and 10%. Compounding frequency (annual→monthly→daily→continuous) barely changes the result once you are already compounding — the big jump is from simple to compound.' : '72 法则在 6%~10% 区间最准。计息频率从年→月→日→连续，差别已经很小——真正的大头是从单利到复利那一跳。'")


def cc_section():
    return wrap('__charCc', CC_UPDATE, ['billAmount', 'dailyRate', 'minRatio'],
                CC_EXTRA,
                "en ? '💳 What the credit-card rate really costs' : '💳 这个信用卡利率真实代价有多大'",
                "en ? 'A small daily rate balloons into a double-digit annual rate once compounding is counted, and paying only the minimum keeps the balance growing every day.' : '看似很小的日息，一旦算上复利就会膨胀成两位数的年化；只还最低还款额则余额每天仍在涨。'",
                "en ? 'Paying the full statement balance by the due date triggers the grace period (typically 20-56 days) and charges zero interest. The displayed \"daily rate\" is only the nominal cost — the effective APR is higher.' : '在到期日前全额还款可触发免息期（通常 20~56 天）且不计息。页面写的“日息”只是名义成本，真实年化更高。'")


def infl_section():
    return wrap('__charInfl', INFL_UPDATE, ['amt', 'rate', 'years'],
                INFL_EXTRA,
                "en ? '🔥 What inflation does to your money' : '🔥 通胀对你的钱做了什么'",
                "en ? 'Inflation does not just raise prices — it quietly halves your money\\'s buying power on a predictable schedule, and beats any deposit that pays less than the rate.' : '通胀不只是涨价——它会按可预测的节奏悄悄把购买力减半，而且凡是收益低于通胀的存款都在实际缩水。'",
                "en ? 'Rule of 70: at 3% inflation, purchasing power halves in about 23 years. Your nominal savings grow, but if the return is below the inflation rate, you are losing real value.' : '70 法则：3% 通胀下购买力约 23 年减半。名义上存款在变多，但若收益低于通胀率，真实购买力在缩水。'")


def mp_section():
    return wrap('__charMp', MP_UPDATE, ['principal', 'rate', 'months', 'monthly', 'prepay'],
                MP_EXTRA,
                "en ? '🏠 What early repayment actually saves' : '🏠 提前还款到底能省什么'",
                "en ? 'With equal principal-and-interest loans, early payments are mostly interest. Prepaying early skips the most expensive interest; how you prepay matters too.' : '等额本息贷款前期还款大多是利息。越早提前还，跳过的是最贵的利息；而且怎么还也有讲究。'",
                "en ? 'After about the first third of the term, most interest is already paid, so prepaying saves far less. Choosing to shorten the term (rather than lower the monthly payment) cuts more total interest for the same lump sum.' : '大约过了前 1/3 期限，大部分利息已经还完，再提前还省得很少。同样一笔钱，「缩短期限」比「减少月供」能多省总利息。'")


TARGETS = {
    'tools/finance/compound-interest.html': (ci_section, '__charCi'),
    'tools/finance/credit-card-interest.html': (cc_section, '__charCc'),
    'tools/finance/inflation-calculator.html': (infl_section, '__charInfl'),
    'tools/finance/mortgage-prepayment.html': (mp_section, '__charMp'),
}


def main():
    done = skip = miss = 0
    for rel, (build, mark) in TARGETS.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print('MISS', rel); miss += 1; continue
        html = open(p, encoding='utf-8').read()
        if mark in html:
            print('SKIP', rel, '(already injected)'); skip += 1; continue
        sec = build()
        # 插到 </body> 前
        html = html.replace('</body>', sec + '\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(html)
        print('OK  ', rel, '(+%d bytes)' % len(sec))
        done += 1
    print('done=%d skip=%d miss=%d' % (done, skip, miss))


if __name__ == '__main__':
    main()
