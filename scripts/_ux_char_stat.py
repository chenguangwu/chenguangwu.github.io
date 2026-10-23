#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _ux_char_stat.py — UX 工具特异性功能重做 · F-CHAR-6（DEV-PLAN 立项项）
# 给「统计推断类」工具注入自包含的「这意味着什么」领域解读模块。
#
# 背景：tools/statistics 全族 51 页，grep「解读|意味着|提示|建议」命中 **0**
#       ⇒ 统计量算出来了，但"这个数到底说明什么"这一统计学科独有的判读知识全族零覆盖。
#       已侦察确认：这些页只有 chart / table / CI / 散点等"再算一遍"型组件，
#       没有一条是回答"结果在现实里意味着什么"的，属真缺口而非同质化重复。
#
# 依据（真实标准，非自拟）：
#   1) Cohen J. (1988) Statistical Power Analysis for the Behavioral Sciences, 2nd ed.
#      |r|: 0.10 小 / 0.30 中 / 0.50 大；d: 0.2 小 / 0.5 中 / 0.8 大
#      Cramer's V 按 df* = min(r-1, c-1) 取 0.10/0.30/0.50 (df*=1)、0.07/0.21/0.35 (df*=2)、
#      0.06/0.17/0.29 (df*=3)
#   2) Cohen's U3 = Phi(d)；分布重叠 Overlap = 2*Phi(-|d|/2)；
#      概率优势 CLES/AUC = Phi(d/sqrt(2))；NNT = 1/(CLES - 0.5)
#   3) 双尾 alpha=0.05 检验效能 80% 所需每组样本量 n = 2*(1.96+0.8416)^2 / d^2 ≈ 15.7/d^2
#   4) 相关系数临界值 |r|_crit = t_crit(df=n-2) / sqrt(t_crit^2 + df)  （t 与 r 的换算）
#   5) 比值比 ≠ 相对风险：由对照组基线风险 P0 反推 RR = OR / ((1-P0) + P0*OR)
#      （即 P1 = OR*P0 / ((1-P0) + P0*OR)）；仅当结局率 <10% 时 OR ≈ RR
#      NNT = 1/|P1 - P0|（绝对风险差的倒数）
#
# 沿用 F-CHAR-1..5 已验证模式：
#   自包含 IIFE / 静态 HTML 零中文（只有空容器）/ 文本由 JS 按 ?lang=en-US 填充 /
#   守卫 typeof TBKit==='undefined' / 不依赖页面 extras，只读输入自行重算 /
#   hook calcTool 使"计算"按钮也刷新 / 构建安全（插在 </body> 前，_build.py 不动该区）
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 公共 JS 片断
COMMON = r'''
  function __stIsEn(){
    try { if (typeof TBKit !== 'undefined' && TBKit.util && TBKit.util.isEn()) return true; } catch(e){}
    try { return new URLSearchParams(location.search).get('lang') === 'en-US'; } catch(e){}
    return false;
  }
  // Abramowitz & Stegun 7.1.26 正态 CDF 近似（|err| < 7.5e-8），零依赖
  function __stNcdf(z){
    var s = z < 0 ? -1 : 1, u = Math.abs(z) / Math.SQRT2;
    var t = 1 / (1 + 0.3275911 * u);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t
          - 0.284496736) * t + 0.254829592) * t) * Math.exp(-u * u);
    return 0.5 * (1 + s * y);
  }
  function __stNum(id){
    var e = document.getElementById(id);
    if (!e) return NaN;
    return parseFloat(e.value);
  }
  function __stPct(x){ return (x * 100).toFixed(1) + '%'; }
  function __stRow(k, v){
    return '<tr><td style="padding:5px 6px;border-bottom:1px solid var(--border);width:30%;vertical-align:top;">'
         + k + '</td><td style="padding:5px 6px;border-bottom:1px solid var(--border);">' + v + '</td></tr>';
  }
  function __stBar(ratio, color){
    var w = Math.max(0, Math.min(1, ratio)) * 100;
    return '<div style="background:var(--border);border-radius:6px;height:14px;overflow:hidden;margin:6px 0 2px;">'
         + '<div style="width:' + w.toFixed(1) + '%;height:100%;background:' + color + ';"></div></div>';
  }
  // 双尾 alpha=0.05 的 t 临界值（df 1..30 精确，之后按常用分档）
  function __stTcrit(df){
    var T = [12.706,4.303,3.182,2.776,2.571,2.447,2.365,2.306,2.262,2.228,
             2.201,2.179,2.160,2.145,2.131,2.120,2.110,2.101,2.093,2.086,
             2.080,2.074,2.069,2.064,2.060,2.056,2.052,2.048,2.045,2.042];
    if (!(df >= 1)) return NaN;
    if (df <= 30) return T[df - 1];
    if (df <= 40) return 2.021;
    if (df <= 60) return 2.000;
    if (df <= 120) return 1.980;
    return 1.960;
  }
'''


def wrap(section_id, update_fn, hook_ids, extra_js, title, desc, note, hook_fn='calcTool'):
    """生成自包含 IIFE：init 填文案 + update 渲染 + hook 页面计算函数 + 监听输入。

    hook_fn：页面主计算函数名，多数页是 calcTool，少数页（如 it/hypothesis-test）是 calculate。
    注意：整个模板只做**一次** % 格式化。若留 %s 占位做二次格式化，
    COMMON 里的 `'%'`（__stPct 的百分号）会在第二轮被当成格式符而 ValueError。
    """
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
  function __stUpdate(){ %s }
  function __stInit(){
    var en = __stIsEn();
    document.getElementById('%sTitle').textContent = %s;
    document.getElementById('%sDesc').textContent = %s;
    document.getElementById('%sNote').textContent = %s;
    __stUpdate();
    var IDS = [%s];
    IDS.forEach(function(id){
      var el = document.getElementById(id);
      if (!el || !el.addEventListener) return;
      el.addEventListener('input', __stUpdate);
      el.addEventListener('change', __stUpdate);
    });
    // 点「计算」按钮时也要刷新：包装页面已有的计算函数（幂等，防重复包装）
    try {
      if (typeof %s === 'function' && !%s.__stHooked) {
        var __orig = %s;
        %s = function(){ __orig.apply(this, arguments); try { __stUpdate(); } catch(e){} };
        %s.__stHooked = true;
      }
    } catch(e){}
  }
  if (document.readyState && document.readyState !== 'loading') __stInit();
  else document.addEventListener('DOMContentLoaded', __stInit);
})();
</script>
''' % (section_id, section_id, section_id, section_id, section_id,
       section_id, section_id, section_id,
       COMMON, extra_js, update_fn,
       section_id, title, section_id, desc, section_id, note,
       ids_js, hook_fn, hook_fn, hook_fn, hook_fn, hook_fn)


# ============================================================ 1. 相关系数
CORR_EXTRA = r'''
  // 与页面 calcTool 完全一致的皮尔逊 r 重算（自读输入，不依赖页面内部变量）
  function __stCorr(){
    function arr(id){
      var e = document.getElementById(id);
      if (!e) return [];
      return String(e.value || '').split(',').map(function(s){ return parseFloat(s.trim()); })
               .filter(function(v){ return isFinite(v); });
    }
    var xa = arr('x'), ya = arr('y');
    var n = Math.min(xa.length, ya.length);
    if (n < 2 || xa.length !== ya.length) return null;
    var mx = 0, my = 0, i;
    for (i = 0; i < n; i++){ mx += xa[i]; my += ya[i]; }
    mx /= n; my /= n;
    var num_ = 0, dx = 0, dy = 0;
    for (i = 0; i < n; i++){ num_ += (xa[i]-mx)*(ya[i]-my); dx += Math.pow(xa[i]-mx,2); dy += Math.pow(ya[i]-my,2); }
    if (!(dx > 0) || !(dy > 0)) return null;
    var r = num_ / Math.sqrt(dx*dy);
    if (!isFinite(r)) return null;
    return { r: Math.max(-1, Math.min(1, r)), n: n };
  }
'''

CORR_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charCorrBadge');
    var val = document.getElementById('__charCorrVal');
    var bar = document.getElementById('__charCorrBar');
    var tb = document.getElementById('__charCorrRows');
    var m = __stCorr();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter at least 2 valid pairs of X and Y (equal counts) to see what r means here.'
                                    : '请先填入至少 2 组有效且等量的 X / Y，再看相关系数的现实含义。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var ar = Math.abs(m.r), r2 = m.r * m.r, df = m.n - 2;
    var lvl, color;
    if (ar >= 0.50){ lvl = en ? 'Large (Cohen)' : '大效应（Cohen）'; color = '#dc2626'; }
    else if (ar >= 0.30){ lvl = en ? 'Medium (Cohen)' : '中等效应（Cohen）'; color = '#ea580c'; }
    else if (ar >= 0.10){ lvl = en ? 'Small (Cohen)' : '小效应（Cohen）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen)' : '可忽略（Cohen）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'r = ' + m.r.toFixed(3) + ' · ' + lvl; }

    var dir = m.r > 0 ? (en ? 'positive' : '正相关') : (m.r < 0 ? (en ? 'negative' : '负相关') : (en ? 'none' : '无'));
    if (val) val.textContent = (en ? 'r = ' : 'r = ') + m.r.toFixed(4) + (en ? '  (' : '（') + dir + (en ? ')' : '）');

    // r^2：变异解释率，这是 r 最容易被误读的地方
    if (bar) bar.innerHTML = __stBar(r2, color)
      + '<div style="font-size:12px;color:var(--text-muted);">' +
      (en ? 'Share of variance explained (r²) = ' : '变异解释率（r²）= ') + __stPct(r2) + '</div>';

    var rows = '';
    // 头号误解：r=0.5 不等于"一半相关"
    var mis = (ar >= 0.4 && ar <= 0.6)
      ? (en ? 'r is about 0.5, but that does NOT mean "half related": r² = ' + __stPct(r2)
              + ', so only about ' + __stPct(r2) + ' of the variation in Y goes with X.'
        : 'r 约等于 0.5，但这不等于"有一半相关"：r² = ' + __stPct(r2)
          + '，也就是 Y 的变异中只有约 ' + __stPct(r2) + ' 与 X 的线性变化同步。')
      : (en ? 'r² = ' + __stPct(r2) + ' of the variation in Y goes with the linear change in X; the rest comes from other factors.'
        : 'r² = ' + __stPct(r2) + '，即 Y 的变异中有 ' + __stPct(r2) + ' 与 X 的线性变化同步，其余来自其他因素。');
    rows += __stRow(en ? 'What r² means' : 'r² 的实际含义', mis);

    // 显著性：当前 n 下这个 r 是否显著（t <-> r 换算）
    var tc = __stTcrit(df), sig = '';
    if (isFinite(tc) && ar < 1){
      var rcrit = tc / Math.sqrt(tc * tc + df);
      var t = m.r * Math.sqrt(df) / Math.sqrt(1 - m.r * m.r);
      sig = (ar > rcrit)
        ? (en ? 'Significant at alpha = 0.05 (two-tailed): |r| = ' + ar.toFixed(3) + ' exceeds the critical ' + rcrit.toFixed(3)
                + ' for n = ' + m.n + ' (t = ' + (isFinite(t) ? t.toFixed(3) : '-') + ').'
          : '在 alpha = 0.05 双尾下显著：n = ' + m.n + ' 时临界 |r| = ' + rcrit.toFixed(3)
            + '，实际 |r| = ' + ar.toFixed(3) + '（t = ' + (isFinite(t) ? t.toFixed(3) : '-') + '）。')
        : (en ? 'Not significant at alpha = 0.05: n = ' + m.n + ' needs |r| above ' + rcrit.toFixed(3)
                + '; yours is ' + ar.toFixed(3) + '. Collect more data before drawing conclusions.'
          : '在 alpha = 0.05 下不显著：n = ' + m.n + ' 时至少需 |r| > ' + rcrit.toFixed(3)
            + '，当前为 ' + ar.toFixed(3) + '，先补样本再下结论。');
    } else {
      sig = en ? 'Not enough data for a significance check (need at least 3 pairs with |r| < 1).'
               : '样本不足以做显著性判断（至少 3 组且 |r| < 1）。';
    }
    rows += __stRow(en ? 'Significance' : '是否显著', sig);

    // 显著 vs 有意义：三种典型情形分别说清
    var warn;
    if (isFinite(rcrit) && ar >= 0.30 && ar <= rcrit){
      // 效应看着不小、但样本不够 => 最常见的误判来源
      warn = (en ? 'The effect looks substantial, yet with n = ' + m.n + ' it is not significant: enlarge the sample before claiming anything, '
                   + 'and remember a large r on tiny data is often just noise.'
             : '效应看起来不小，但 n = ' + m.n + ' 时尚未显著：先扩大样本再下结论 —— 小样本上的大 r 常常只是噪声。');
    } else if (ar > 0 && ar < 0.30){
      warn = (en ? 'Even if significant, an effect this small is usually of little practical use - report r² and the confidence interval, not just "p < 0.05".'
             : '即便统计显著，这么小的效应通常没有实际价值 —— 报告时应给出 r² 与置信区间，而不是只写"p < 0.05"。');
    } else {
      warn = (en ? 'Statistical significance and practical importance are different things: always pair r with its confidence interval.'
             : '统计显著与实际重要性是两件事：报告 r 时应同时给出置信区间。');
    }
    rows += __stRow(en ? 'Practical vs statistical' : '显著 ≠ 有意义', warn);

    // 相关不等于因果：四条替代解释
    rows += __stRow(en ? 'Correlation is not causation' : '相关不等于因果',
      en ? 'Four other explanations fit the same r: (1) Y causes X (reverse direction); '
          + '(2) a third variable drives both; (3) coincidence, especially with small n; '
          + '(4) selection or range restriction. Only a controlled design can separate them.'
      : '同样的 r 至少有四种替代解释：（1）反向因果，是 Y 导致 X；（2）存在同时影响两者的第三变量；'
        + '（3）巧合，样本小时尤其常见；（4）样本选择偏差或取值范围受限。只有受控设计才能区分。');

    // 三个会毁掉 r 的陷阱
    rows += __stRow(en ? 'What can break it' : '会毁掉 r 的陷阱',
      en ? 'A single outlier can swing r a lot; r only measures LINEAR association, so a clear curve can still give r near 0; '
          + 'and pooling subgroups can reverse the sign (Simpson paradox). Always look at the scatter plot above.'
      : '一个离群点就能大幅改变 r；r 只度量线性关系，明显的曲线关系也可能 r 接近 0；'
        + '合并子组还可能让符号反转（辛普森悖论）。务必结合上方散点图一起看。');
    if (tb) tb.innerHTML = rows;
  }'''

CORR_NOTE = (r"""en
      ? 'Bands follow Cohen (1988): |r| = 0.10 small, 0.30 medium, 0.50 large. The critical value uses the exact t-to-r relation r_crit = t/sqrt(t^2 + df) with df = n - 2 at alpha = 0.05 two-tailed. r assumes a linear relationship and is not robust to outliers; for monotonic but curved patterns use Spearman rho instead. Indicative reading aid, not a substitute for study design review.'
      : '分级依据 Cohen (1988)：|r| = 0.10 为小效应、0.30 中、0.50 大。临界值用 t 与 r 的精确换算 r_crit = t/√(t²+df)，df = n−2，alpha = 0.05 双尾。r 只刻画线性关系且对离群点不稳健；单调但明显弯曲的关系应改用斯皮尔曼 rho。以上为判读提示，不能替代研究设计审查。'""")

# ============================================================ 2. Cohen's d
CD_EXTRA = r'''
  function __stD(){
    var m1 = __stNum('m1'), m2 = __stNum('m2'), s1 = __stNum('s1'),
        s2 = __stNum('s2'), n1 = __stNum('n1'), n2 = __stNum('n2');
    if (!isFinite(m1) || !isFinite(m2) || !isFinite(s1) || !isFinite(s2) || !isFinite(n1) || !isFinite(n2)) return null;
    if (n1 < 2 || n2 < 2) return null;
    var sp = Math.sqrt(((n1-1)*s1*s1 + (n2-1)*s2*s2) / (n1 + n2 - 2));
    if (!(sp > 0)) return null;
    var d = (m1 - m2) / sp;
    if (!isFinite(d)) return null;
    return { d: d, n1: n1, n2: n2 };
  }
'''

CD_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charCohenBadge');
    var val = document.getElementById('__charCohenVal');
    var bar = document.getElementById('__charCohenBar');
    var tb = document.getElementById('__charCohenRows');
    var m = __stD();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Fill in both group means, SDs and sizes (each n >= 2) to see what d means here.'
                                    : '请完整填写两组均值、标准差与样本量（每组 n ≥ 2），再看效应量的现实含义。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var ad = Math.abs(m.d), sg = m.d >= 0 ? 1 : -1;
    var lvl, color;
    if (ad >= 0.80){ lvl = en ? 'Large (Cohen)' : '大效应（Cohen）'; color = '#dc2626'; }
    else if (ad >= 0.50){ lvl = en ? 'Medium (Cohen)' : '中等效应（Cohen）'; color = '#ea580c'; }
    else if (ad >= 0.20){ lvl = en ? 'Small (Cohen)' : '小效应（Cohen）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen)' : '可忽略（Cohen）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'd = ' + m.d.toFixed(3) + ' · ' + lvl; }

    var who = en ? (sg > 0 ? 'Group 1 is higher.' : 'Group 2 is higher.')
                 : (sg > 0 ? '组 1 更高。' : '组 2 更高。');
    if (val) val.textContent = (en ? 'd = ' : 'd = ') + m.d.toFixed(4)
      + (en ? '  (group means differ by ' : '（两组均值相差 ') + ad.toFixed(2)
      + (en ? ' pooled SD)' : ' 个合并标准差）') + ' ' + who;

    // 概率优势 CLES / AUC：随机各抽一人，实验组更高的概率
    var cles = __stNcdf(m.d / Math.SQRT2);
    if (bar) bar.innerHTML = __stBar(cles, color)
      + '<div style="font-size:12px;color:var(--text-muted);">' +
      (en ? 'Chance a random group-1 case beats a random group-2 case = ' : '随机抽组 1 一个体高于组 2 一个体的概率 = ')
      + __stPct(cles) + '</div>';

    var overlap = 2 * __stNcdf(-ad / 2);          // 两分布重叠面积
    var u3 = __stNcdf(m.d);                        // Cohen's U3
    var nnt = cles > 0.5 ? 1 / (cles - 0.5) : null;
    var need = ad > 0 ? Math.ceil(2 * Math.pow(1.96 + 0.8416, 2) / (ad * ad)) : null;

    var rows = '';
    rows += __stRow(en ? 'Overlap of the two distributions' : '两分布重叠比例',
      (en ? 'About ' : '约 ') + __stPct(overlap) + (en ? ' of the two groups overlap, so ' : ' 的个体落在共同区间，也就是说 ')
      + __stPct(1 - overlap) + (en ? ' of the cases are separated. Even d = 0.5 still leaves most of the two distributions on top of each other.'
                                  : ' 的个体能被区分开。即便 d = 0.5，两组分布仍有大部分相互重叠。'));
    rows += __stRow(en ? "Cohen's U3" : 'Cohen U3 指标',
      (en ? 'About ' : '约 ') + __stPct(u3) + (en ? ' of group 1 sit above the mean of group 2'
                                              : ' 的组 1 个体高于组 2 的均值')
      + (en ? ' (50% would mean no effect at all).' : '（无效应时该值为 50%）。'));
    rows += __stRow(en ? 'AUC / common-language effect size' : 'AUC 概率优势',
      (en ? 'A randomly picked case from group 1 beats one from group 2 with probability ' : '随机抽取组 1 与组 2 各一个体，前者更高的概率为 ')
      + __stPct(cles) + (en ? '; 50% means a coin flip.' : '；50% 相当于抛硬币。'));
    if (nnt !== null && nnt < 10000){
      rows += __stRow(en ? 'Number needed to treat' : '需治人数 NNT',
        (en ? 'About ' : '约 ') + Math.ceil(nnt) + (en ? ' cases would need the treatment instead of the control for one extra favourable outcome (1/(AUC - 0.5)).'
                                                   : ' 例需要接受处理而非对照，才能多换来一个有利结局（1/(AUC−0.5)）。'));
    }
    if (need !== null){
      rows += __stRow(en ? 'Sample size for 80% power' : '达到 80% 检验效能所需样本',
        (en ? 'Detecting this effect at alpha = 0.05 two-tailed with 80% power needs about ' : '在 alpha = 0.05 双尾、效能 80% 下检出该效应，每组约需 ')
        + need + (en ? ' per group (' : ' 例（') + (2 * need) + (en ? ' in total). Your current n1 = ' : ' 例合计）。当前 n1 = ')
        + m.n1 + (en ? ', n2 = ' : '，n2 = ') + m.n2
        + (en ? (Math.min(m.n1, m.n2) >= need ? ', which is enough.' : ', which is likely under-powered - a non-significant result here would not prove "no effect".')
              : (Math.min(m.n1, m.n2) >= need ? '，样本已足够。' : '，很可能效能不足 —— 此时不显著并不能证明"没有效应"。')));
    }
    rows += __stRow(en ? 'Significant vs meaningful' : '显著 ≠ 有意义',
      en ? 'd is a standardised difference, so a large sample can make a tiny d "significant". Judge it against a cost or a clinical threshold, and always report the confidence interval for d.'
        : 'd 是标准化差值，样本足够大时极小的 d 也会"显著"。判读时应对照成本或临床阈值，并始终报告 d 的置信区间。');
    if (tb) tb.innerHTML = rows;
  }'''

CD_NOTE = (r"""en
      ? 'Bands follow Cohen (1988): d = 0.2 small, 0.5 medium, 0.8 large. Overlap = 2*Phi(-|d|/2), U3 = Phi(d), AUC = Phi(d/sqrt(2)), NNT = 1/(AUC - 0.5); the power figure uses n = 2*(z(0.975)+z(0.80))^2/d^2 per group. All assume two independent groups, roughly normal distributions and similar variances - with strong skew or very unequal SDs, read d with care. Indicative reading aid, not a substitute for a power analysis by a statistician.'
      : '分级依据 Cohen (1988)：d = 0.2 小、0.5 中、0.8 大。重叠比例 = 2Φ(−|d|/2)，U3 = Φ(d)，AUC = Φ(d/√2)，NNT = 1/(AUC−0.5)；效能样本量取每组 n = 2(z0.975+z0.80)²/d²。以上均假设两组独立、分布近似正态且方差相近 —— 严重偏态或两组标准差相差很大时，d 需谨慎解读。以上为判读提示，不能替代统计师做的效能分析。'""")

# ============================================================ 3. Cramer's V
CR_EXTRA = r'''
  function __stV(){
    var a = __stNum('a'), b = __stNum('b'), c = __stNum('c'), d = __stNum('d');
    if (!isFinite(a) || !isFinite(b) || !isFinite(c) || !isFinite(d)) return null;
    var n = a + b + c + d;
    if (!(n > 0)) return null;
    var e11 = (a+b)*(a+c)/n, e12 = (a+b)*(b+d)/n, e21 = (c+d)*(a+c)/n, e22 = (c+d)*(b+d)/n;
    if (!(e11 > 0) || !(e12 > 0) || !(e21 > 0) || !(e22 > 0)) return null;
    var chi = (a-e11)*(a-e11)/e11 + (b-e12)*(b-e12)/e12 + (c-e21)*(c-e21)/e21 + (d-e22)*(d-e22)/e22;
    var V = Math.sqrt(chi / n);
    if (!isFinite(V)) return null;
    return { V: Math.min(1, V), chi: chi, n: n };
  }
'''

CR_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charCramBadge');
    var val = document.getElementById('__charCramVal');
    var bar = document.getElementById('__charCramBar');
    var tb = document.getElementById('__charCramRows');
    var m = __stV();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Fill in all four cells (a, b, c, d) to see how strong this association is.'
                                    : '请完整填写四格 a、b、c、d，再看关联强度判读。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    // 2x2 表：df* = min(r-1, c-1) = 1，此时 Cramer's V 就等于 phi 系数
    var lo = 0.10, mid = 0.30, hi = 0.50;   // Cohen 对 df* = 1 的基准
    var lvl, color;
    if (m.V >= hi){ lvl = en ? 'Large (Cohen)' : '大关联（Cohen）'; color = '#dc2626'; }
    else if (m.V >= mid){ lvl = en ? 'Medium (Cohen)' : '中等关联（Cohen）'; color = '#ea580c'; }
    else if (m.V >= lo){ lvl = en ? 'Small (Cohen)' : '小关联（Cohen）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen)' : '可忽略（Cohen）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'V = ' + m.V.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'Cramer\'s V = ' : 'Cramer\'s V = ') + m.V.toFixed(4)
      + (en ? '  from chi-square = ' : '（由卡方 χ² = ') + m.chi.toFixed(3)
      + (en ? ' with n = ' : '，n = ') + m.n + (en ? '' : '）');
    if (bar) bar.innerHTML = __stBar(m.V, color)
      + '<div style="font-size:12px;color:var(--text-muted);">' +
      (en ? 'V runs from 0 (no association) to 1 (perfect association)' : 'V 取值 0（无关联）到 1（完全关联）') + '</div>';

    var rows = '';
    rows += __stRow(en ? 'For this table' : '本表的换算',
      en ? 'For a 2x2 table df* = min(rows-1, cols-1) = 1, so Cramer\'s V equals the phi coefficient: V = sqrt(chi-square / n). '
          + 'Larger tables need df* in the denominator and use lower thresholds (0.07 / 0.21 / 0.35 at df* = 2).'
      : '2×2 表的 df* = min(行数−1, 列数−1) = 1，因此 Cramer\'s V 就等于 phi 系数：V = √(χ²/n)。'
        + '更大的表分母要除以 df*，阈值也更低（df* = 2 时为 0.07 / 0.21 / 0.35）。');
    rows += __stRow(en ? 'Significant vs strong' : '显著 ≠ 强',
      en ? 'Chi-square grows with sample size: with n in the thousands, even V = 0.05 can be "significant". '
          + 'A significant test says the association is unlikely to be zero; V says how strong it is. Report both.'
      : '卡方随样本量增大：n 到几千时，即便 V = 0.05 也会"显著"。显著性只说明关联不太可能为 0，V 才说明关联有多强，两者都要报告。');
    rows += __stRow(en ? 'No direction, no causation' : '无方向、非因果',
      en ? 'V is always between 0 and 1 and carries no sign, so it cannot tell you which way the association runs. '
          + 'Use the odds ratio for direction. A high V still says nothing about cause and effect.'
      : 'V 恒在 0 到 1 之间且不带符号，因此无法说明关联的方向；要看方向请改用比值比。V 高同样不说明因果关系。');
    rows += __stRow(en ? 'What to check' : '使用前先检查',
      en ? 'The chi-square behind V needs expected counts that are not too small (a common rule is at least 5); '
          + 'with thin cells use Fisher exact test instead. Very unbalanced margins also pull V down even when the pattern is clear.'
      : '卡方要求期望频数不能太小（常用规则是不低于 5）；格子太稀疏时应改用 Fisher 精确检验。'
        + '行列合计极不均衡时，即便模式很明显，V 也会被压低。');
    if (tb) tb.innerHTML = rows;
  }'''

CR_NOTE = (r"""en
      ? 'Bands follow Cohen (1988) for df* = 1: V = 0.10 small, 0.30 medium, 0.50 large. V = sqrt(chi-square / (n * df*)) with df* = min(rows-1, cols-1); this page uses a 2x2 table, so df* = 1 and V = phi. V has no sign and no causal meaning. Indicative reading aid, not a substitute for a modelling approach matched to the study design.'
      : '分级依据 Cohen (1988) 对 df* = 1 的基准：V = 0.10 小、0.30 中、0.50 大。V = √(χ²/(n·df*))，df* = min(行数−1, 列数−1)；本页为 2×2 表，故 df* = 1、V 等于 phi。V 不带符号，也不表示因果。以上为判读提示，不能替代与研究设计匹配的建模分析。'""")

# ============================================================ 4. Odds ratio
OR_EXTRA = r'''
  function __stOR(){
    var a = __stNum('a'), b = __stNum('b'), c = __stNum('c'), d = __stNum('d');
    if (!isFinite(a) || !isFinite(b) || !isFinite(c) || !isFinite(d)) return null;
    if (a <= 0 || b <= 0 || c <= 0 || d <= 0) return null;
    var OR = (a * d) / (b * c);
    if (!isFinite(OR) || OR <= 0) return null;
    var p1 = a / (a + b), p0 = c / (c + d);
    var se = Math.sqrt(1/a + 1/b + 1/c + 1/d);
    var lo = Math.exp(Math.log(OR) - 1.96 * se), hi = Math.exp(Math.log(OR) + 1.96 * se);
    return { OR: OR, p1: p1, p0: p0, lo: lo, hi: hi };
  }
'''

OR_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charOrBadge');
    var val = document.getElementById('__charOrVal');
    var bar = document.getElementById('__charOrBar');
    var tb = document.getElementById('__charOrRows');
    var m = __stOR();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'All four cells (a, b, c, d) must be positive to read the odds ratio.'
                                    : '四格 a、b、c、d 都需为正数，才能判读比值比。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var sig = !(m.lo <= 1 && m.hi >= 1);
    var lvl, color;
    if (!sig){ lvl = en ? 'Not significant (CI includes 1)' : '不显著（CI 含 1）'; color = '#16a34a'; }
    else if (m.OR >= 2 || m.OR <= 0.5){ lvl = en ? 'Significant, sizeable' : '显著且幅度不小'; color = '#dc2626'; }
    else { lvl = en ? 'Significant, modest' : '显著但幅度不大'; color = '#ea580c'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'OR = ' + m.OR.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'OR = ' : 'OR = ') + m.OR.toFixed(4)
      + (en ? '  95% CI ' : '  95% 置信区间 ') + m.lo.toFixed(3) + ' - ' + m.hi.toFixed(3);

    var rows = '';
    // 头号误解：OR 不是相对风险
    var rr = m.p0 > 0 ? (m.p1 / m.p0) : null;
    var rrFromOR = m.OR / ((1 - m.p0) + m.p0 * m.OR);
    var gap = (rr !== null && rr > 0) ? Math.abs(m.OR - rr) / rr : null;
    var rare = m.p1 < 0.10 && m.p0 < 0.10;
    var mis = en
      ? ('OR is NOT the relative risk. OR = ' + m.OR.toFixed(3) + ' does not mean "the risk is '
         + m.OR.toFixed(2) + ' times as high": the actual risk ratio here is RR = ' + (rr === null ? '-' : rr.toFixed(3))
         + '. ' + (rare ? 'Both outcome rates are below 10%, so OR and RR happen to be close and treating OR as RR is acceptable.'
                       : 'Outcome rates here are not rare, so OR and RR differ - quoting OR as if it were RR overstates the effect.'))
      : ('比值比不是相对风险。OR = ' + m.OR.toFixed(3) + ' 并不表示"风险是 ' + m.OR.toFixed(2) + ' 倍"：'
         + '本表的真实风险比 RR = ' + (rr === null ? '-' : rr.toFixed(3)) + '。'
         + (rare ? '两组结局率都低于 10%，此时 OR 与 RR 接近，按 RR 近似使用可以接受。'
                 : '本表结局率并不罕见，OR 与 RR 差异明显 —— 把 OR 当 RR 报会夸大效应。'));
    rows += __stRow(en ? 'OR is not "risk doubled"' : 'OR 不等于风险翻倍', mis);

    // 用基线风险反推：给出可落地的绝对数字
    rows += __stRow(en ? 'Turning OR into a risk' : '把 OR 换算成风险',
      en ? ('With the control-group risk in this table (P0 = ' + __stPct(m.p0) + '), OR = ' + m.OR.toFixed(3)
            + ' implies an exposed risk of P1 = OR*P0/((1-P0)+OR*P0) = ' + __stPct(m.p0 * rrFromOR > 0 ? m.p0 * rrFromOR : m.p1)
            + ' and a risk ratio of ' + rrFromOR.toFixed(3) + '. The same OR produces very different absolute risks at a different baseline.')
        : ('按本表对照组基线风险（P0 = ' + __stPct(m.p0) + '），OR = ' + m.OR.toFixed(3)
           + ' 对应暴露组风险 P1 = OR·P0/((1−P0)+OR·P0) = ' + __stPct(m.p0 * rrFromOR > 0 ? m.p0 * rrFromOR : m.p1)
           + '，风险比 ' + rrFromOR.toFixed(3) + '。同一个 OR 在别的基线风险下会换算出完全不同的绝对风险。'));

    // 绝对风险差与 NNT
    var ard = m.p1 - m.p0;
    rows += __stRow(en ? 'Absolute risk difference' : '绝对风险差',
      (en ? 'Risk goes from ' : '风险由 ') + __stPct(m.p0) + (en ? ' in the unexposed to ' : '（非暴露）变为 ')
      + __stPct(m.p1) + (en ? ' in the exposed, an absolute difference of ' : '（暴露），绝对差值 ')
      + __stPct(Math.abs(ard)) + (en ? (ard >= 0 ? ' (increase).' : ' (decrease).') : (ard >= 0 ? '（上升）。' : '（下降）。'))
      + (Math.abs(ard) > 1e-9
          ? (ard >= 0
              ? (en ? ' That is 1 extra outcome for every ' : ' 相当于每 ') + Math.ceil(1 / Math.abs(ard))
                + (en ? ' people exposed (NNT).' : ' 人暴露就多出现 1 例结局（NNT）。')
              : (en ? ' That is 1 outcome avoided for every ' : ' 相当于每 ') + Math.ceil(1 / Math.abs(ard))
                + (en ? ' people exposed (NNT).' : ' 人暴露就少出现 1 例结局（NNT）。'))
          : (en ? ' No absolute difference.' : ' 绝对风险无差异。')));

    // 研究设计决定能算什么
    rows += __stRow(en ? 'Which design gives what' : '不同设计能算什么',
      en ? 'A case-control study cannot compute incidence, so it can only give an OR - and the OR is still valid there. '
          + 'Cohort and trial data can give risk ratios and absolute risks directly, which are easier to act on.'
        : '病例对照研究无法计算发病率，因此只能给出 OR —— 但 OR 在这种设计下依然成立。'
          + '队列研究与试验数据可以直接给出风险比与绝对风险，更便于决策。');
    rows += __stRow(en ? 'Reading the interval' : '怎么看置信区间',
      (en ? 'The 95% CI ' : '95% 置信区间 ') + m.lo.toFixed(3) + ' - ' + m.hi.toFixed(3)
      + (sig ? (en ? ' excludes 1, so the association is significant at the 5% level.'
                   : ' 不含 1，关联在 5% 水平显著。')
             : (en ? ' includes 1, so this table does not rule out no association. Check the width: a very wide interval means the estimate is fragile.'
                   : ' 含 1，本表不能排除无关联。注意区间宽度：非常宽说明估计很不稳定。'))
      + (en ? ' The CI is computed on the log scale (Woolf formula) and is asymmetric on purpose.'
            : ' 置信区间在对数尺度上计算（Woolf 公式），因此左右不对称，这是正常的。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      var p = Math.max(m.p0, m.p1);
      bar.innerHTML = __stBar(m.p1, '#dc2626')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Exposed event rate ' : '暴露组事件率 ') + __stPct(m.p1)
        + (en ? '  vs  unexposed ' : '  对照 ') + __stPct(m.p0)
        + (en ? '  (only the absolute gap matters for decisions)' : '（决策只关心绝对差值）')
        + '</div>';
    }
  }'''

OR_NOTE = (r"""en
      ? 'Conversion uses P1 = OR*P0/((1-P0)+OR*P0), so RR = OR/((1-P0)+OR*P0); OR approximates RR only when the outcome is rare (roughly below 10%). NNT = 1/|P1 - P0|. The CI uses the Woolf log-scale formula SE = sqrt(1/a+1/b+1/c+1/d). The OR is symmetric under transposing the table, which is why case-control studies can estimate it; it is not a risk ratio and should not be reported as one. Indicative reading aid, not clinical advice.'
      : '换算采用 P1 = OR·P0/((1−P0)+OR·P0)，故 RR = OR/((1−P0)+OR·P0)；只有当结局罕见（约低于 10%）时 OR 才可近似 RR。NNT = 1/|P1−P0|。置信区间用 Woolf 对数尺度公式 SE = √(1/a+1/b+1/c+1/d)。比值比在转置表格时保持不变，这正是病例对照研究能估计它的原因；它不是风险比，不应按风险比来报告。以上为判读提示，不构成临床建议。'""")


# ============================================================ 5. 相对风险 RR
RR_EXTRA = r'''
  function __stRR(){
    var a = __stNum('a'), b = __stNum('b'), c = __stNum('c'), d = __stNum('d');
    if (!isFinite(a) || !isFinite(b) || !isFinite(c) || !isFinite(d)) return null;
    if (a <= 0 || b <= 0 || c <= 0 || d <= 0) return null;
    var e1 = a / (a + b), e0 = c / (c + d);
    if (!(e0 > 0)) return null;
    var RR = e1 / e0;
    if (!isFinite(RR) || RR <= 0) return null;
    // ln(RR) 的标准误（Katz 对数法）
    var se = Math.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d));
    var lo = Math.exp(Math.log(RR) - 1.96 * se), hi = Math.exp(Math.log(RR) + 1.96 * se);
    var OR = (a * d) / (b * c);
    return { RR: RR, e1: e1, e0: e0, lo: lo, hi: hi, OR: OR };
  }
'''

RR_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charRrBadge');
    var val = document.getElementById('__charRrVal');
    var bar = document.getElementById('__charRrBar');
    var tb = document.getElementById('__charRrRows');
    var m = __stRR();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'All four cells (a, b, c, d) must be positive to read the relative risk.'
                                    : '四格 a、b、c、d 都需为正数，才能判读相对风险。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var sig = !(m.lo <= 1 && m.hi >= 1);
    var lvl, color;
    if (!sig){ lvl = en ? 'Not significant (CI includes 1)' : '不显著（CI 含 1）'; color = '#16a34a'; }
    else if (m.RR >= 2 || m.RR <= 0.5){ lvl = en ? 'Significant, sizeable' : '显著且幅度不小'; color = '#dc2626'; }
    else { lvl = en ? 'Significant, modest' : '显著但幅度不大'; color = '#ea580c'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'RR = ' + m.RR.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'RR = ' : 'RR = ') + m.RR.toFixed(4)
      + (en ? '  95% CI ' : '  95% 置信区间 ') + m.lo.toFixed(3) + ' - ' + m.hi.toFixed(3);

    var ard = m.e1 - m.e0;
    var nnt = Math.abs(ard) > 1e-9 ? Math.ceil(1 / Math.abs(ard)) : null;
    var rows = '';

    // 绝对风险差与 NNT：决策真正需要的数字
    rows += __stRow(en ? 'Absolute risk difference' : '绝对风险差',
      (en ? 'Risk moves from ' : '风险由 ') + __stPct(m.e0) + (en ? ' to ' : ' 变为 ') + __stPct(m.e1)
      + (en ? ', an absolute change of ' : '，绝对变化 ') + __stPct(Math.abs(ard))
      + (en ? (ard >= 0 ? ' (increase).' : ' (decrease).') : (ard >= 0 ? '（上升）。' : '（下降）。'))
      + (nnt !== null
          ? (ard >= 0
              ? (en ? ' One extra outcome for every ' : ' 相当于每 ') + nnt + (en ? ' people exposed (NNT).' : ' 人暴露多出现 1 例结局（NNT）。')
              : (en ? ' One outcome avoided for every ' : ' 相当于每 ') + nnt + (en ? ' people exposed (NNT).' : ' 人暴露少出现 1 例结局（NNT）。'))
          : (en ? ' No absolute difference.' : ' 绝对风险无差异。')));

    // 头号误读：同样的 RR 在不同基线风险下完全不是一回事
    var nntHi = m.RR !== 1 ? Math.ceil(1 / Math.abs(0.10 * (m.RR - 1))) : null;   // 基线 10%
    var nntLo = m.RR !== 1 ? Math.ceil(1 / Math.abs(0.01 * (m.RR - 1))) : null;   // 基线 1%
    var baseWarn;
    if (nntHi !== null && nntLo !== null){
      baseWarn = en
        ? ('The same RR = ' + m.RR.toFixed(2) + ' means very different things at different baselines: '
           + 'with a 10% baseline risk, about 1 in ' + nntHi + ' exposed people is affected; '
           + 'with a 1% baseline risk, only about 1 in ' + nntLo + '. Never quote RR without the baseline risk.')
        : ('同样的 RR = ' + m.RR.toFixed(2) + ' 在不同基线风险下含义完全不同：'
           + '若基线风险为 10%，约每 ' + nntHi + ' 个暴露者才影响 1 人；'
           + '若基线风险只有 1%，则约每 ' + nntLo + ' 人才影响 1 人。'
           + '报告 RR 时必须同时给出基线风险。');
    } else {
      baseWarn = en ? 'RR = 1 means the two risks are equal, so no baseline adjustment is needed.'
                    : 'RR = 1 表示两组风险相同，无需再看基线。';
    }
    rows += __stRow(en ? 'The same RR, different baselines' : '同 RR 不同基线', baseWarn);

    // RR 与 OR 的关系
    rows += __stRow(en ? 'RR vs odds ratio' : 'RR 与比值比',
      en ? ('On this table the odds ratio is OR = ' + m.OR.toFixed(3) + ' while the risk ratio is RR = ' + m.RR.toFixed(3)
            + '. The OR is always further from 1 than the RR when an effect exists, so quoting an OR as if it were a risk ratio exaggerates it. '
            + 'RR needs incidence, so it comes from cohorts and trials; a case-control study can only give an OR.')
        : ('本表的比值比 OR = ' + m.OR.toFixed(3) + '，风险比 RR = ' + m.RR.toFixed(3)
           + '。存在效应时，OR 总是比 RR 更远离 1，因此把 OR 当 RR 报会夸大效应。'
           + 'RR 需要发病率数据，只能来自队列研究或试验；病例对照研究只能给出 OR。'));

    rows += __stRow(en ? 'Reading the interval' : '怎么看置信区间',
      (en ? 'The 95% CI ' : '95% 置信区间 ') + m.lo.toFixed(3) + ' - ' + m.hi.toFixed(3)
      + (sig ? (en ? ' excludes 1, so the difference is significant at the 5% level.'
                   : ' 不含 1，差异在 5% 水平显著。')
             : (en ? ' includes 1, so this table does not establish a difference. Remember "not significant" is not the same as "no difference".'
                   : ' 含 1，本表不足以说明有差异。注意"不显著"不等于"没有差异"。'))
      + (en ? ' Computed on the log scale (Katz method), which is why the interval is not symmetric around RR.'
            : ' 该区间在对数尺度上计算（Katz 法），因此相对 RR 左右不对称。'));

    rows += __stRow(en ? 'What to report' : '报告时该写什么',
      en ? 'Report the risk in each group, the absolute difference and the NNT alongside the RR. A relative risk alone cannot tell a reader whether the change is worth acting on.'
        : '报告 RR 的同时应给出两组各自的风险、绝对风险差与 NNT。只有相对风险，读者无法判断这个变化值不值得行动。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.e1, '#dc2626')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Exposed ' : '暴露组 ') + __stPct(m.e1)
        + (en ? '  vs  unexposed ' : '  对照 ') + __stPct(m.e0)
        + (en ? '  (the gap, not the ratio, drives decisions)' : '（决策看的是差值，不是比值）')
        + '</div>';
    }
  }'''

RR_NOTE = (r"""en
      ? 'The CI uses the Katz log method, SE(ln RR) = sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d)); NNT = 1/|P1 - P0|. RR requires incidence, so it applies to cohort and trial data; case-control studies yield only an odds ratio, which is always further from 1 than the RR when an effect exists. The same RR implies very different absolute effects at different baseline risks, so always report the absolute risks too. Indicative reading aid, not clinical advice.'
      : '置信区间用 Katz 对数法，SE(ln RR) = √(1/a − 1/(a+b) + 1/c − 1/(c+d))；NNT = 1/|P1 − P0|。RR 需要发病率，适用于队列研究与试验；病例对照研究只能给出比值比，且存在效应时 OR 总比 RR 更远离 1。同一个 RR 在不同基线风险下对应的绝对效应差别很大，因此必须同时报告绝对风险。以上为判读提示，不构成临床建议。'""")

# ============================================================ 6. 比例的置信区间
CI_EXTRA = r'''
  // Wald 区间（与页面一致）+ Wilson 区间对照
  function __stCI(){
    var x = __stNum('x'), n = __stNum('n'), z = __stNum('z');
    if (!isFinite(x) || !isFinite(n) || !isFinite(z)) return null;
    if (!(n > 0) || x < 0 || x > n) return null;
    var p = x / n;
    var se = Math.sqrt(p * (1 - p) / n);
    var lo = p - z * se, hi = p + z * se;
    var denom = 1 + z * z / n;
    var centre = (p + z * z / (2 * n)) / denom;
    var half = (z / denom) * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n));
    return { p: p, n: n, z: z, se: se, lo: lo, hi: hi,
             wlo: Math.max(0, centre - half), whi: Math.min(1, centre + half) };
  }
'''

CI_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charCiBadge');
    var val = document.getElementById('__charCiVal');
    var bar = document.getElementById('__charCiBar');
    var tb = document.getElementById('__charCiRows');
    var m = __stCI();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter successes x, sample size n and the z value (1.96 for 95%).'
                                    : '请填写成功数 x、样本量 n 与 z 值（95% 用 1.96）。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var half = m.z * m.se;
    var width = 2 * half;
    // 判定 Wald 区间是否可靠：成功/失败数是否够大
    var succ = m.p * m.n, fail = (1 - m.p) * m.n;
    var thin = Math.min(succ, fail) < 5;
    var lvl = en ? (thin ? 'Wald interval unreliable here' : 'Wald interval reasonable')
                 : (thin ? 'Wald 区间在此不可靠' : 'Wald 区间可用');
    var color = thin ? '#dc2626' : '#0d9488';
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color; badge.textContent = lvl; }
    if (val) val.textContent = (en ? 'p = ' : 'p = ') + m.p.toFixed(4)
      + (en ? '  95%-style interval ' : '  区间 ') + m.lo.toFixed(4) + ' - ' + m.hi.toFixed(4)
      + (en ? '  (half width ' : '（半宽 ') + half.toFixed(4) + (en ? ')' : '）');

    var rows = '';
    // 头号误解：CI 不是"真值有 95% 概率落在里面"
    rows += __stRow(en ? 'What "95%" really means' : '95% 到底指什么',
      en ? 'It does NOT mean there is a 95% probability that the true value lies inside THIS interval. '
          + 'For the interval you just computed, the true value is either in it or not. '
          + 'The 95% describes the procedure: if the same study were repeated many times and the interval rebuilt each time, '
          + 'about 95% of those intervals would cover the true value.'
        : '它并不表示"真值有 95% 的概率落在当前这个区间里"。对已经算出来的这一个区间，真值要么在里面，要么不在。'
          + '95% 描述的是方法：如果重复抽样很多次、每次都用同样方法重算区间，约 95% 的区间会覆盖真值。');

    // Wilson 对照
    var gap = Math.abs(m.wlo - m.lo) + Math.abs(m.whi - m.hi);
    rows += __stRow(en ? 'Check against the Wilson interval' : '与 Wilson 区间对照',
      (en ? 'The Wilson interval for the same data is ' : '同一数据的 Wilson 区间为 ') + m.wlo.toFixed(4) + ' - ' + m.whi.toFixed(4)
      + (thin
          ? (en ? '. Successes or failures here are fewer than 5, so the simple Wald interval above can miss badly '
                  + '(it may even run below 0 or above 1). Use the Wilson interval, or the exact Clopper-Pearson interval.'
            : '。本表成功数或失败数少于 5，上方简单的 Wald 区间可能严重失准'
              + '（甚至会算出小于 0 或大于 1 的边界）。请改用 Wilson 区间或精确的 Clopper-Pearson 区间。')
          : (en ? '. The two agree closely, so the simple interval above is fine here.'
                : '。两者接近，上方简单区间在此可用。')));

    // 样本量与精度的 sqrt(n) 关系
    var needHalf = half > 0 ? Math.ceil(m.z * m.z * m.p * (1 - m.p) / Math.pow(half / 2, 2)) : null;
    rows += __stRow(en ? 'Precision scales with sqrt(n)' : '精度与 √n 成正比',
      (en ? 'The half width is ' : '当前半宽 ') + half.toFixed(4) + (en ? '. Cutting it in half requires about 4x the sample: '
                                                                    : '。要把半宽压缩一半，样本量需约 4 倍：')
      + (needHalf !== null ? (en ? 'roughly n = ' : '约 n = ') + needHalf + (en ? ' instead of ' : '（当前 ') + m.n + (en ? '.' : '）。')
                           : (en ? 'not applicable at p = 0 or 1.' : 'p 为 0 或 1 时不适用。'))
      + (en ? ' Precision costs sample size, not clever maths.' : ' 提高精度只能靠加大样本，没有捷径。'));

    rows += __stRow(en ? 'What this interval is not' : '这个区间不是什么',
      en ? 'This is an interval for the population proportion, not a range that contains 95% of individual observations. '
          + 'It also says nothing about causality, and it assumes the sample is random and independent.'
        : '这是总体比例的区间，不是"包含 95% 个体观测值"的范围。它也不说明因果，并假设样本随机且相互独立。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      var scale = 1;
      bar.innerHTML = __stBar(m.hi, '#0d9488')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Interval width ' : '区间宽度 ') + __stPct(width)
        + (en ? '  (upper end ' : '（上限 ') + __stPct(Math.min(1, m.hi)) + (en ? ')' : '）')
        + '</div>';
    }
  }'''

CI_NOTE = (r"""en
      ? 'The page interval is the Wald form p +/- z*sqrt(p(1-p)/n); the Wilson check uses centre = (p + z^2/(2n))/(1 + z^2/n) with half width (z/(1+z^2/n))*sqrt(p(1-p)/n + z^2/(4n^2)). A common rule of thumb is that the Wald interval is unreliable when either np or n(1-p) is below about 5. Half width scales as 1/sqrt(n), so halving it needs about four times the sample. The 95% is a property of the procedure over repeated samples, not a probability statement about this one interval. Indicative reading aid.'
      : '页面区间为 Wald 形式 p ± z·√(p(1−p)/n)；Wilson 对照取 centre = (p + z²/(2n))/(1 + z²/n)，半宽 (z/(1+z²/n))·√(p(1−p)/n + z²/(4n²))。常用经验规则：当 np 或 n(1−p) 低于约 5 时，Wald 区间不可靠。半宽按 1/√n 收缩，故减半需要约 4 倍样本。95% 描述的是重复抽样下方法的覆盖比例，不是对当前这一个区间的概率陈述。以上为判读提示。'""")

# ============================================================ 7. 独立样本 t 检验前提
TT_EXTRA = r'''
  function __stT(){
    var m1 = __stNum('m1'), m2 = __stNum('m2'), s1 = __stNum('s1'),
        s2 = __stNum('s2'), n1 = __stNum('n1'), n2 = __stNum('n2');
    if (!isFinite(m1) || !isFinite(m2) || !isFinite(s1) || !isFinite(s2) || !isFinite(n1) || !isFinite(n2)) return null;
    if (n1 < 2 || n2 < 2 || s1 <= 0 || s2 <= 0) return null;
    var sp = Math.sqrt(((n1-1)*s1*s1 + (n2-1)*s2*s2) / (n1 + n2 - 2));
    var d = (m1 - m2) / sp;
    var se = sp * Math.sqrt(1/n1 + 1/n2);
    var t = (m1 - m2) / se;
    // Welch 自由度与 Welch t
    var v1 = s1*s1/n1, v2 = s2*s2/n2;
    var dfw = Math.pow(v1 + v2, 2) / (Math.pow(v1,2)/(n1-1) + Math.pow(v2,2)/(n2-1));
    var tw = (m1 - m2) / Math.sqrt(v1 + v2);
    return { d: d, t: t, df: n1 + n2 - 2, dfw: dfw, tw: tw,
             s1: s1, s2: s2, n1: n1, n2: n2, ratio: Math.max(s1, s2) / Math.min(s1, s2) };
  }
'''

TT_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charTtBadge');
    var val = document.getElementById('__charTtVal');
    var bar = document.getElementById('__charTtBar');
    var tb = document.getElementById('__charTtRows');
    var m = __stT();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter both means, SDs (positive) and sample sizes (at least 2 each) to check the assumptions behind this test.'
                                    : '请填写两组均值、标准差（大于 0）与样本量（每组至少 2），再检查该检验的前提。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    // 三项前提：方差齐性 / 正态性可依赖程度 / 样本量
    var hetero = m.ratio > 2;
    var small = Math.min(m.n1, m.n2) < 15;
    var lvl, color;
    if (hetero){ lvl = en ? 'Unequal variances - use Welch' : '方差不齐，建议 Welch'; color = '#dc2626'; }
    else if (small){ lvl = en ? 'Small sample - normality matters' : '样本偏小，正态性重要'; color = '#ea580c'; }
    else { lvl = en ? 'Assumptions look reasonable' : '前提看起来满足'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color; badge.textContent = lvl; }
    if (val) val.textContent = (en ? 't = ' : 't = ') + m.t.toFixed(4)
      + (en ? '  (df = ' : '（df = ') + m.df + (en ? ')' : '）')
      + (en ? '   Cohen\'s d = ' : '   Cohen\'s d = ') + m.d.toFixed(3);

    var rows = '';
    // 方差齐性：最常见的翻车点
    rows += __stRow(en ? 'Equal variances' : '方差齐性',
      (en ? 'The two SDs are ' : '两组标准差为 ') + m.s1.toFixed(3) + (en ? ' and ' : ' 与 ') + m.s2.toFixed(3)
      + (en ? ', a ratio of ' : '，比值 ') + m.ratio.toFixed(2) + (en ? 'x. ' : ' 倍。')
      + (hetero
          ? (en ? 'A ratio above about 2 breaks the pooled-variance t test. The Welch version is the safer default here: '
                  + 'Welch t = ' + m.tw.toFixed(4) + ' with about ' + Math.round(m.dfw) + ' degrees of freedom, instead of '
                  + m.t.toFixed(4) + ' with ' + m.df + '.'
            : '比值超过约 2 会破坏合并方差 t 检验的前提。此处 Welch 检验更稳妥：'
              + 'Welch t = ' + m.tw.toFixed(4) + '，自由度约 ' + Math.round(m.dfw)
              + '；而合并方差结果为 t = ' + m.t.toFixed(4) + '，自由度 ' + m.df + '。')
          : (en ? 'Within the usual tolerance, so the pooled t test above is appropriate.'
                : '在通常可接受的范围内，上方合并方差 t 检验适用。')));

    // 正态性：小样本才是硬前提
    rows += __stRow(en ? 'Normality' : '正态性',
      (small
        ? (en ? 'With only ' + Math.min(m.n1, m.n2) + ' in the smaller group, the t test leans on the data being roughly normal. '
                + 'Check a histogram or a Q-Q plot; with skew or heavy tails switch to the Mann-Whitney U test or a bootstrap.'
          : '较小一组只有 ' + Math.min(m.n1, m.n2) + ' 例，t 检验依赖数据近似正态。'
            + '请查看直方图或 Q-Q 图；若明显偏态或重尾，改用 Mann-Whitney U 检验或自助法。')
        : (en ? 'Both groups have at least 15 observations, so the central limit theorem carries most of the load and mild non-normality is usually tolerable. '
                + 'Extreme outliers still matter.'
          : '两组都至少 15 例，中心极限定律足以支撑，轻度偏离正态通常可以容忍；但极端离群点仍需处理。')));

    // 独立性：唯一不能靠统计补救的前提
    rows += __stRow(en ? 'Independence' : '独立性',
      en ? 'The one assumption no correction can fix: observations must be independent within and between groups. '
          + 'Repeated measures on the same subject, clustered sampling or paired designs need a paired test or a mixed model instead.'
        : '这是无法用统计方法补救的前提：组内与组间观测必须相互独立。'
          + '同一受试者的重复测量、整群抽样或配对设计，应改用配对检验或混合模型。');

    // 单尾/双尾 与 多重比较
    rows += __stRow(en ? 'One-tailed, and multiple looks' : '单尾检验与多次比较',
      en ? 'A two-sided test is the default and the safer choice; a one-sided test needs a reason recorded before seeing the data. '
          + 'Testing several outcomes and reporting only the significant one inflates the false-positive rate: '
          + '20 independent tests at the 5% level give about a 64% chance of at least one false positive.'
        : '默认且更稳妥的是双尾检验；单尾检验需要在看数据之前就记录理由。'
          + '检验多个结局却只报告显著的那个，会抬高假阳性率：'
          + '在 5% 水平做 20 次独立检验，出现至少一次假阳性的概率约 64%。');

    rows += __stRow(en ? 'Report more than p' : '别只报 p',
      (en ? 'Pair the test with an effect size: Cohen\'s d here is ' : '检验应配上效应量：本例 Cohen\'s d = ') + m.d.toFixed(3)
      + (en ? ' (' + (Math.abs(m.d) >= 0.8 ? 'large' : (Math.abs(m.d) >= 0.5 ? 'medium' : (Math.abs(m.d) >= 0.2 ? 'small' : 'negligible')))
              + ' by Cohen), plus the confidence interval for the difference. A p value alone says nothing about how big the difference is.'
        : '（按 Cohen 标准属' + (Math.abs(m.d) >= 0.8 ? '大' : (Math.abs(m.d) >= 0.5 ? '中' : (Math.abs(m.d) >= 0.2 ? '小' : '可忽略')))
          + '效应），并给出差值的置信区间。只报 p 值无法说明差异有多大。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, Math.abs(m.d) / 2), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Effect size |d| = ' : '效应量 |d| = ') + Math.abs(m.d).toFixed(3)
        + (en ? '  (0.2 small / 0.5 medium / 0.8 large)' : '（0.2 小 / 0.5 中 / 0.8 大）')
        + '</div>';
    }
  }'''

TT_NOTE = (r"""en
      ? 'The pooled t test assumes independent samples, roughly normal group data and equal variances; the variance ratio here is compared against the common rule of thumb of 2. Welch degrees of freedom use the Welch-Satterthwaite formula. With at least about 15 per group the central limit theorem makes mild non-normality tolerable, but outliers and dependence are not fixed by sample size. Effect size bands follow Cohen (1988). Indicative reading aid, not a substitute for checking the assumptions on the real data.'
      : '合并方差 t 检验假设样本独立、组内数据近似正态且方差相等；此处方差比值与常用的 2 倍经验阈值比较。Welch 自由度采用 Welch-Satterthwaite 公式。每组约 15 例以上时，中心极限定律使轻度非正态可以容忍，但离群点与不独立无法靠增大样本解决。效应量分级依据 Cohen (1988)。以上为判读提示，不能替代对真实数据前提的检验。'""")

# ============================================================ 8. 单因素方差分析
AV_EXTRA = r'''
  function __stAnova(){
    var ms = [], ss = [], ns = [], i;
    for (i = 1; i <= 3; i++){
      var m = __stNum('m' + i), s = __stNum('s' + i), n = __stNum('n' + i);
      if (!isFinite(m) || !isFinite(s) || !isFinite(n)) return null;
      if (n < 2 || s <= 0) return null;
      ms.push(m); ss.push(s); ns.push(n);
    }
    var N = 0, sum = 0;
    for (i = 0; i < 3; i++){ N += ns[i]; sum += ns[i] * ms[i]; }
    var grand = sum / N;
    var ssb = 0, ssw = 0;
    for (i = 0; i < 3; i++){ ssb += ns[i] * Math.pow(ms[i] - grand, 2); ssw += (ns[i] - 1) * ss[i] * ss[i]; }
    var sst = ssb + ssw;
    if (!(sst > 0)) return null;
    var dfb = 2, dfw = N - 3;
    if (!(dfw > 0)) return null;
    var msb = ssb / dfb, msw = ssw / dfw;
    var F = msw > 0 ? msb / msw : NaN;
    var eta2 = ssb / sst;
    var omega2 = (ssb - dfb * msw) / (sst + msw);
    return { F: F, eta2: Math.max(0, eta2), omega2: omega2, dfb: dfb, dfw: dfw, N: N, ssb: ssb, ssw: ssw };
  }
'''

AV_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charAvBadge');
    var val = document.getElementById('__charAvVal');
    var bar = document.getElementById('__charAvBar');
    var tb = document.getElementById('__charAvRows');
    var m = __stAnova();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter all three group means, SDs and sizes (each n >= 2) to see how much the groups really differ.'
                                    : '请填写三组均值、标准差与样本量（每组 n ≥ 2），再看组间差异到底有多大。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var lvl, color;
    if (m.eta2 >= 0.14){ lvl = en ? 'Large (Cohen)' : '大效应（Cohen）'; color = '#dc2626'; }
    else if (m.eta2 >= 0.06){ lvl = en ? 'Medium (Cohen)' : '中等效应（Cohen）'; color = '#ea580c'; }
    else if (m.eta2 >= 0.01){ lvl = en ? 'Small (Cohen)' : '小效应（Cohen）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen)' : '可忽略（Cohen）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'eta-squared = ' + m.eta2.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'F(' : 'F(') + m.dfb + ', ' + m.dfw + (en ? ') = ' : ') = ')
      + (isFinite(m.F) ? m.F.toFixed(4) : '-')
      + (en ? '   eta-squared = ' : '   η² = ') + m.eta2.toFixed(4);

    var rows = '';
    // eta-squared：方差解释比例，ANOVA 里最该报却被漏掉的数
    rows += __stRow(en ? 'How much the groups explain' : '组间解释了什么',
      (en ? 'Eta-squared = SS_between / SS_total = ' : 'η² = 组间平方和 / 总平方和 = ') + m.eta2.toFixed(4)
      + (en ? ', so group membership accounts for about ' : '，也就是说分组因素约解释了 ') + __stPct(m.eta2)
      + (en ? ' of the total variation; the remaining ' : ' 的总变异，剩下 ') + __stPct(1 - m.eta2)
      + (en ? ' is noise and individual differences. Cohen bands: 0.01 small, 0.06 medium, 0.14 large.'
        : ' 来自噪声与个体差异。Cohen 分级：0.01 小、0.06 中、0.14 大。'));

    // omega-squared：更少偏的估计
    rows += __stRow(en ? 'Less biased: omega-squared' : '更少偏的 ω²',
      (en ? 'Omega-squared = ' : 'ω² = ') + (isFinite(m.omega2) ? m.omega2.toFixed(4) : '-')
      + (en ? '. Eta-squared is biased upward, especially with small samples, so omega-squared is the better number to report.'
        : '。η² 存在高估偏倚，样本小时尤其明显，因此报告时更推荐 ω²。'));

    // ANOVA 显著只说明"不完全相等"
    rows += __stRow(en ? 'It does not tell you which' : '它没告诉你是哪两组',
      en ? 'A significant F only says the three means are not all equal - it does not say which pair differs. '
          + 'You need a post-hoc comparison with a corrected threshold (Tukey HSD is the usual choice). '
          + 'Running three separate t tests instead leaves the family-wise error rate near 14% rather than 5%.'
        : 'F 显著只说明三组均值不全相等，并不说明哪两组不同。'
          + '需要做事后多重比较并校正阈值（通常用 Tukey HSD）。'
          + '若直接做三次两两 t 检验，整体假阳性率会接近 14% 而不是 5%。');

    rows += __stRow(en ? 'Assumptions to check' : '要检查的前提',
      en ? 'Independent observations, roughly normal residuals, and similar variances across groups. '
          + 'With unequal variances use Welch ANOVA; with clear skew or ordinal data use the Kruskal-Wallis test. '
          + 'Unbalanced group sizes make the violation of equal variances much more damaging.'
        : '观测独立、残差近似正态、各组方差相近。方差不齐时用 Welch 方差分析；'
          + '明显偏态或有序数据用 Kruskal-Wallis 检验。各组样本量不均衡时，方差不齐的危害会明显放大。');

    rows += __stRow(en ? 'Significant vs meaningful' : '显著 ≠ 有意义',
      en ? 'F grows with sample size, so with a large N even a trivial spread of means becomes significant. '
          + 'Decide using eta-squared against a threshold that matters in your field, and report the group means and SDs.'
        : 'F 随样本量增大，N 很大时即便均值差异微不足道也会显著。'
          + '判读应把 η² 与本领域有意义的阈值对照，并报告各组均值与标准差。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.eta2, color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Share of total variation explained by group: ' : '分组解释的总变异比例：') + __stPct(m.eta2)
        + '</div>';
    }
  }'''

AV_NOTE = (r"""en
      ? 'Eta-squared = SS_between/SS_total; omega-squared = (SS_between - df_between*MS_within)/(SS_total + MS_within) and is less biased. Cohen bands for eta-squared are 0.01 small, 0.06 medium, 0.14 large. Between-group and within-group sums of squares are reconstructed from the group means, SDs and sizes, so results match the standard one-way ANOVA only when those summaries are the whole story. A significant F does not localise the difference; use Tukey HSD or another corrected post-hoc procedure. Indicative reading aid.'
      : 'η² = 组间平方和/总平方和；ω² = (组间平方和 − 组间自由度×组内均方)/(总平方和 + 组内均方)，偏倚更小。η² 的 Cohen 分级为 0.01 小、0.06 中、0.14 大。组间与组内平方和由各组均值、标准差与样本量还原，因此只有在这些汇总量反映全部信息时才与标准单因素方差分析一致。F 显著并不定位差异所在，需用 Tukey HSD 或其他校正后的事后比较。以上为判读提示。'""")

# ---------------------------------------------------------------- 组装
CORR_TITLE = "en ? '\\uD83D\\uDCC8 What this correlation actually means' : '\\uD83D\\uDCC8 这个相关系数到底说明什么'"
CORR_DESC = ("en ? 'Turns r into plain language: how much variation it really explains, "
             "whether it is significant at this sample size, and what else could produce the same number.' "
             ": '把 r 翻译成人话：它到底解释了多少变异、在当前样本量下是否显著、以及还有哪些情况能产生同样的数值。'")


def corr_section():
    return wrap('__charCorr', CORR_UPDATE, ['x', 'y'], CORR_EXTRA, CORR_TITLE, CORR_DESC, CORR_NOTE)


CD_TITLE = "en ? '\\uD83D\\uDCCF What this effect size actually means' : '\\uD83D\\uDCCF 这个效应量到底说明什么'"
CD_DESC = ("en ? 'Turns Cohen\\'s d into things you can picture: how much the two groups overlap, "
           "the chance one case beats another, the number needed to treat, and the sample size needed to detect it.' "
           ": '把 Cohen\\'s d 换成能想象的量：两组分布重叠多少、随机抽一个体胜出的概率、需治人数，"
           "以及要检出该效应所需的样本量。'")


def cd_section():
    return wrap('__charCohen', CD_UPDATE, ['m1', 'm2', 's1', 's2', 'n1', 'n2'], CD_EXTRA,
                CD_TITLE, CD_DESC, CD_NOTE)


CR_TITLE = "en ? '\\uD83D\\uDCCA How strong is this association' : '\\uD83D\\uDCCA 这个关联到底有多强'"
CR_DESC = ("en ? 'Puts Cramer\\'s V on the Cohen scale, explains the link to phi on a 2x2 table, "
           "and separates significant from strong.' "
           ": '把 Cramer\\'s V 放到 Cohen 分级上看，说明它在 2×2 表上与 phi 的关系，并区分显著与强。'")


def cr_section():
    return wrap('__charCram', CR_UPDATE, ['a', 'b', 'c', 'd'], CR_EXTRA, CR_TITLE, CR_DESC, CR_NOTE)


OR_TITLE = "en ? '⚕️ What this odds ratio actually means' : '⚕️ 这个比值比到底说明什么'"
OR_DESC = ("en ? 'Odds ratios are routinely misread as risk ratios. This converts your OR into the real "
           "risk ratio, the absolute risk difference and the number needed to treat.' "
           ": '比值比最常被误当成风险比。这里把 OR 换算成真实的风险比、绝对风险差与需治人数。'")


def or_section():
    return wrap('__charOr', OR_UPDATE, ['a', 'b', 'c', 'd'], OR_EXTRA, OR_TITLE, OR_DESC, OR_NOTE)


# ---- 第二批（F-CHAR-7）：相对风险 / 置信区间 / t 检验前提 / 方差分析效应量 ----
RR_TITLE = "en ? '📉 What this relative risk actually means' : '📉 这个相对风险到底说明什么'"
RR_DESC = ("en ? 'A relative risk without the baseline is easy to over-read. This adds the absolute difference, "
           "the number needed to treat, and what the same RR would mean at a different baseline.' "
           ": '脱离基线风险的相对风险最容易被夸大。这里补上绝对风险差、需治人数，"
           "以及同一个 RR 在另一基线风险下会是什么含义。'")

CI_TITLE = "en ? '📐 What this confidence interval actually means' : '📐 这个置信区间到底说明什么'"
CI_DESC = ("en ? 'Confidence intervals are the most misquoted number in statistics. This explains what the 95% does and does not say, "
           "checks the interval against Wilson, and shows what sample size buys you.' "
           ": '置信区间是统计学里被误读最多的数字。这里说明 95% 到底指什么、不指什么，"
           "与 Wilson 区间对照，并给出精度与样本量的关系。'")

TT_TITLE = "en ? '🔍 Are this test\\'s assumptions met' : '🔍 这个检验的前提成立吗'"
TT_DESC = ("en ? 'A t test is only as good as its assumptions. This checks equal variances, how much normality matters at your sample size, "
           "and gives the Welch alternative when variances differ.' "
           ": 't 检验的可信度取决于前提是否成立。这里检查方差齐性、当前样本量下正态性有多重要，"
           "并在方差不齐时给出 Welch 检验的替代结果。'")

AV_TITLE = "en ? '📊 How much do these groups really differ' : '📊 这些组到底差多少'"
AV_DESC = ("en ? 'A significant F does not say which group differs, nor how much. This adds eta-squared and omega-squared, "
           "explains the post-hoc step, and lists the assumptions behind the test.' "
           ": 'F 显著既不说明哪两组不同，也不说明差多少。这里补上 η² 与 ω² 效应量，"
           "说明事后比较这一步，并列出检验的前提。'")


def rr_section():
    return wrap('__charRr', RR_UPDATE, ['a', 'b', 'c', 'd'], RR_EXTRA, RR_TITLE, RR_DESC, RR_NOTE)


def ci_section():
    return wrap('__charCi', CI_UPDATE, ['x', 'n', 'z'], CI_EXTRA, CI_TITLE, CI_DESC, CI_NOTE)


def tt_section():
    return wrap('__charTt', TT_UPDATE, ['m1', 'm2', 's1', 's2', 'n1', 'n2'], TT_EXTRA, TT_TITLE, TT_DESC, TT_NOTE)


def av_section():
    return wrap('__charAv', AV_UPDATE, ['m1', 'm2', 'm3', 's1', 's2', 's3', 'n1', 'n2', 'n3'],
                AV_EXTRA, AV_TITLE, AV_DESC, AV_NOTE)


# ======================================== 9. 假设检验的两类错误（it/hypothesis-test）
# 该页主函数名为 calculate()（非 calcTool），故 hook_fn 需显式指定
HT_EXTRA = r'''
  // 二分法求正态分位数（z 使 Phi(z) = p），避免依赖页面内部函数
  function __stZ(p){
    if (!(p > 0 && p < 1)) return NaN;
    var lo = -12, hi = 12, i, mid;
    for (i = 0; i < 120; i++){ mid = (lo + hi) / 2; if (__stNcdf(mid) < p) lo = mid; else hi = mid; }
    return (lo + hi) / 2;
  }
  function __stTail(){
    var e = document.getElementById('tail');
    if (!e) return 'two';
    var v = String(e.value || '').toLowerCase();
    return (v.indexOf('one') >= 0 || v === '1' || v.indexOf('单') >= 0) ? 'one' : 'two';
  }
  function __stHT(){
    var mean = __stNum('mean'), mu0 = __stNum('mu0'), sigma = __stNum('sigma'),
        n = __stNum('n'), alpha = __stNum('alpha');
    if (!isFinite(mean) || !isFinite(mu0) || !isFinite(sigma) || !isFinite(n) || !isFinite(alpha)) return null;
    if (!(sigma > 0) || !(n > 0) || !(alpha > 0) || !(alpha < 1)) return null;
    var se = sigma / Math.sqrt(n);
    var z = (mean - mu0) / se;
    var tail = __stTail();
    var zc = tail === 'one' ? __stZ(1 - alpha) : __stZ(1 - alpha / 2);
    if (!isFinite(zc)) return null;
    var delta = Math.abs(mean - mu0) / se;                 // 以观测差作为效应量
    // 双尾：power = Phi(delta - zc) + Phi(-delta - zc)；单尾只取同向那一侧
    var power = tail === 'one' ? __stNcdf(delta - zc) : (__stNcdf(delta - zc) + __stNcdf(-delta - zc));
    // 可检出的最小效应（power = 80%）：(z_crit + z_0.80) * sigma / sqrt(n)
    var mde = (zc + 0.8416) * se;
    return { z: z, zc: zc, alpha: alpha, delta: delta, power: power, mde: mde,
             tail: tail, se: se, diff: mean - mu0, n: n, sigma: sigma };
  }
'''

HT_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charHtBadge');
    var val = document.getElementById('__charHtVal');
    var bar = document.getElementById('__charHtBar');
    var tb = document.getElementById('__charHtRows');
    var m = __stHT();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter the sample mean, the hypothesised mean, sigma, n and alpha to see the error rates behind this test.'
                                    : '请填写样本均值、假设均值、总体标准差 sigma、样本量 n 与 alpha，再看该检验背后的两类错误。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var rej = Math.abs(m.z) > m.zc;      // 是否落在拒绝域
    var beta = 1 - m.power;
    var lvl, color;
    if (rej && m.power >= 0.80){ lvl = en ? 'Rejected, well powered' : '拒绝且效能充足'; color = '#dc2626'; }
    else if (rej){ lvl = en ? 'Rejected, but power is low' : '拒绝但效能偏低'; color = '#ea580c'; }
    else if (m.power >= 0.80){ lvl = en ? 'Not rejected, well powered' : '未拒绝且效能充足'; color = '#0d9488'; }
    else { lvl = en ? 'Not rejected, power is low' : '未拒绝且效能不足'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color; badge.textContent = lvl; }
    if (val) val.textContent = (en ? 'z = ' : 'z = ') + m.z.toFixed(4)
      + (en ? '  critical ' : '  临界值 ') + (m.tail === 'one' ? '' : '±') + m.zc.toFixed(3)
      + (en ? '  (' : '（')
      + (m.tail === 'one' ? (en ? 'one-tailed' : '单尾') : (en ? 'two-tailed' : '双尾'))
      + (en ? ')' : '）');

    var rows = '';
    // 决策矩阵：四类结果的概率
    rows += __stRow(en ? 'The two error types' : '两类错误',
      en ? ('Alpha = ' + m.alpha.toFixed(3) + ' is the false-positive rate: if the null hypothesis were true, this test would still reject it that often. '
            + 'Beta is the false-negative rate: if the true effect equals the one observed here, this design misses it about ' + __stPct(beta)
            + ' of the time. Cutting alpha without adding data pushes beta up.')
        : ('α = ' + m.alpha.toFixed(3) + ' 是假阳性率：若原假设为真，该检验仍会有这么高的比例错误拒绝它。'
           + 'β 是假阴性率：若真实效应等于此处观测到的效应，该设计约有 ' + __stPct(beta) + ' 的概率漏掉它。'
           + '在样本不变时压低 α，会把 β 推高。'));

    rows += __stRow(en ? 'Power of this design' : '该设计的检验效能',
      (en ? 'Power = 1 - beta = ' : '效能 = 1 − β = ') + __stPct(m.power)
      + (en ? ' for an effect of the size observed here (|mean - mu0| = ' : '（对应此处观测到的效应 |x̄ − μ0| = ')
      + Math.abs(m.diff).toFixed(3) + (en ? '). ' : '）。')
      + (m.power >= 0.80
          ? (en ? 'At or above the usual 80% target, so a real effect of this size would usually be detected.'
            : '达到通常的 80% 目标，这么大的真实效应一般能被检出。')
          : (en ? 'Below the usual 80% target: a real effect of this size would often be missed, so a non-significant result here proves very little.'
            : '低于通常的 80% 目标：这么大的真实效应常常会被漏掉，因此此处"不显著"几乎说明不了什么。')));

    // 可检出的最小效应：不做事后效能也能说清样本够不够
    rows += __stRow(en ? 'Smallest effect you can detect' : '你能检出的最小效应',
      (en ? 'With n = ' : '在 n = ') + m.n + (en ? ' and alpha = ' : '、α = ') + m.alpha.toFixed(3)
      + (en ? ', the smallest difference detectable with 80% power is about ' : ' 下，效能 80% 时可检出的最小差值约 ')
      + m.mde.toFixed(3) + (en ? ' (MDE = (z_crit + 0.8416) * sigma / sqrt(n)). ' : '（MDE = (z_crit + 0.8416)·σ/√n）。')
      + (Math.abs(m.diff) >= m.mde
          ? (en ? 'The observed difference is above that, so the design can resolve it.' : '观测差值高于该值，设计足以分辨。')
          : (en ? 'The observed difference is below that threshold, which is why it may not reach significance.'
            : '观测差值低于该阈值，这也是它可能达不到显著的原因。')));

    rows += __stRow(en ? 'What "not significant" does not mean' : '"不显著"不等于什么',
      en ? 'Failing to reject is not the same as proving the null. It can mean the effect is small, or that the sample was too small to see it. '
          + 'To argue for "no effect" you need an equivalence test or a confidence interval narrow enough to rule out effects that matter.'
        : '未能拒绝并不等于证明了原假设。可能是效应很小，也可能是样本太小看不出来。'
          + '要主张"没有效应"，需要等价性检验，或给出窄到足以排除有意义效应的置信区间。');

    rows += __stRow(en ? 'Before you run the test' : '做检验之前先定好',
      en ? 'Fix alpha, the direction (one or two tailed) and the sample size in advance. Choosing a one-tailed test after seeing which way the result went '
          + 'roughly doubles the false-positive rate, and stopping as soon as p dips below 0.05 does the same.'
        : '提前定好 α、单尾还是双尾、以及样本量。看到结果方向后才改用单尾，会把假阳性率提高约一倍；'
          + '一看到 p 跌破 0.05 就停止收集数据，效果同样如此。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.power, m.power >= 0.80 ? '#16a34a' : '#ea580c')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Power = ' : '检验效能 = ') + __stPct(m.power)
        + (en ? '  (80% is the usual target)' : '（通常以 80% 为目标）')
        + '</div>';
    }
  }'''

HT_NOTE = (r"""en
      ? 'Power uses the normal approximation: for a two-tailed test power = Phi(delta - z_crit) + Phi(-delta - z_crit), for one-tailed power = Phi(delta - z_crit), with delta = |mean - mu0| / (sigma/sqrt(n)). The minimum detectable effect is (z_crit + z_0.80) * sigma / sqrt(n) at 80% power. Power computed from the observed effect is post hoc and only illustrative - plan a study from the effect you care about, not from the result you happened to get. Indicative reading aid.'
      : '效能采用正态近似：双尾 power = Φ(δ − z_crit) + Φ(−δ − z_crit)，单尾 power = Φ(δ − z_crit)，其中 δ = |x̄ − μ0|/(σ/√n)。可检出最小效应 MDE = (z_crit + z_0.80)·σ/√n（效能 80%）。依据观测效应反算的效能属事后效能，仅作示意 —— 研究设计应基于你关切的效应量，而不是碰巧得到的结果。以上为判读提示。'""")

# ======================================== 10. 卡方检验的效应量与残差定位
CH_EXTRA = r'''
  function __stChi(){
    var eo = document.getElementById('o'), ee = document.getElementById('e');
    if (!eo || !ee) return null;
    function arr(v){
      return String(v || '').split(',').map(function(s){ return parseFloat(s.trim()); })
               .filter(function(x){ return isFinite(x); });
    }
    var oa = arr(eo.value), ea = arr(ee.value);
    var n = Math.min(oa.length, ea.length);
    if (n < 1) return null;
    var chi = 0, N = 0, i, res = [], thin = 0, maxI = -1, maxV = -1;
    for (i = 0; i < n; i++){
      if (!(ea[i] > 0)) return null;
      chi += Math.pow(oa[i] - ea[i], 2) / ea[i];
      N += oa[i];
      var r = (oa[i] - ea[i]) / Math.sqrt(ea[i]);
      res.push(r);
      if (ea[i] < 5) thin++;
      if (Math.abs(r) > maxV){ maxV = Math.abs(r); maxI = i; }
    }
    if (!(N > 0)) return null;
    // Cohen's w：卡方族效应量，w = sqrt(chi-square / N)
    var w = Math.sqrt(chi / N);
    return { chi: chi, df: n - 1, N: N, w: w, res: res, thin: thin,
             maxI: maxI, maxV: maxV, o: oa, e: ea };
  }
'''

CH_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charChiBadge');
    var val = document.getElementById('__charChiVal');
    var bar = document.getElementById('__charChiBar');
    var tb = document.getElementById('__charChiRows');
    var m = __stChi();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter observed and expected values (comma separated) with every expected value positive.'
                                    : '请填写观测值与期望值（逗号分隔），且每个期望值都为正数。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var lvl, color;
    if (m.w >= 0.50){ lvl = en ? 'Large (Cohen w)' : '大效应（Cohen w）'; color = '#dc2626'; }
    else if (m.w >= 0.30){ lvl = en ? 'Medium (Cohen w)' : '中等效应（Cohen w）'; color = '#ea580c'; }
    else if (m.w >= 0.10){ lvl = en ? 'Small (Cohen w)' : '小效应（Cohen w）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen w)' : '可忽略（Cohen w）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'w = ' + m.w.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'chi-square = ' : 'χ² = ') + m.chi.toFixed(4)
      + (en ? '  (df = ' : '（df = ') + m.df + (en ? ')' : '）')
      + (en ? '   Cohen\'s w = ' : '   Cohen\'s w = ') + m.w.toFixed(4);

    var rows = '';
    // Cohen's w：卡方该配的效应量，绝大多数页面都漏了
    rows += __stRow(en ? 'Effect size w' : '效应量 w',
      (en ? 'Cohen\'s w = sqrt(chi-square / N) = ' : 'Cohen\'s w = √(χ²/N) = ') + m.w.toFixed(4)
      + (en ? ', the standard effect size for chi-square tests. Bands: 0.10 small, 0.30 medium, 0.50 large. '
            + 'A chi-square value alone cannot be compared across studies because it grows with N; w can.'
        : '，这是卡方检验的标准效应量。分级：0.10 小、0.30 中、0.50 大。'
          + '单独的 χ² 无法跨研究比较，因为它随 N 增大；w 可以。'));

    // 期望频数检查：卡方最常用的适用条件
    rows += __stRow(en ? 'Expected counts check' : '期望频数检查',
      (m.thin > 0
        ? (en ? m.thin + ' of the ' + m.res.length + ' cells have an expected value below 5. Chi-square becomes unreliable there: '
                + 'merge sparse categories, or use an exact test.'
          : '共 ' + m.res.length + ' 个格子中有 ' + m.thin + ' 个期望值低于 5。此时卡方不再可靠：'
            + '应合并稀疏类别，或改用精确检验。')
        : (en ? 'Every expected value is at least 5, which meets the usual requirement for the chi-square approximation.'
          : '所有期望值都不低于 5，满足卡方近似的通常要求。')));

    // 标准化残差：定位到底哪个格子在驱动结果
    var loc = '';
    if (m.maxI >= 0){
      var r = m.res[m.maxI];
      loc = (en ? 'The largest contribution comes from cell ' : '贡献最大的是第 ') + (m.maxI + 1)
        + (en ? ': observed ' : ' 格：观测 ') + m.o[m.maxI].toFixed(0)
        + (en ? ' vs expected ' : '，期望 ') + m.e[m.maxI].toFixed(2)
        + (en ? ', a standardised residual of ' : '，标准化残差 ') + r.toFixed(2)
        + (Math.abs(r) > 2
            ? (en ? ' (beyond about 2 in absolute value, so this cell is driving the result).'
              : '（绝对值超过约 2，说明正是这一格在驱动结果）。')
            : (en ? ' (within about 2, so no single cell stands out).' : '（未超过约 2，没有哪一格特别突出）。'));
    }
    rows += __stRow(en ? 'Where the difference comes from' : '差异来自哪一格', loc);

    rows += __stRow(en ? 'Which chi-square is this' : '这是哪一种卡方',
      en ? 'The same statistic serves two different questions. A goodness-of-fit test compares one variable against a known or theoretical distribution; '
          + 'a test of independence asks whether two variables in a contingency table are related. The degrees of freedom differ, and so does the interpretation.'
        : '同一个统计量回答两类不同问题：拟合优度检验把单个变量与已知或理论分布比较；'
          + '独立性检验则问列联表中两个变量是否相关。两者自由度不同，解读也不同。');

    rows += __stRow(en ? 'Significant vs important' : '显著 ≠ 重要',
      en ? 'Chi-square grows with N, so with a large sample even a trivial deviation becomes significant. Report w alongside the statistic, '
          + 'and check the standardised residuals so you can say where the deviation actually is.'
        : 'χ² 随 N 增大，样本很大时即便微小偏差也会显著。报告统计量时应一并给出 w，'
          + '并查看标准化残差，说明偏差究竟出在哪里。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, m.w), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Cohen\'s w = ' : 'Cohen\'s w = ') + m.w.toFixed(3)
        + (en ? '  (0.1 small / 0.3 medium / 0.5 large)' : '（0.1 小 / 0.3 中 / 0.5 大）')
        + '</div>';
    }
  }'''

CH_NOTE = (r"""en
      ? 'Effect size follows Cohen: w = sqrt(chi-square/N), with bands 0.10 small, 0.30 medium, 0.50 large. Standardised residuals are (observed - expected)/sqrt(expected); values beyond about 2 in absolute value flag the cells driving the statistic. The usual requirement is that expected counts are at least about 5. This module reconstructs the statistic from the observed and expected lists, so it reflects exactly the numbers entered above. Indicative reading aid.'
      : '效应量依据 Cohen：w = √(χ²/N)，分级 0.10 小、0.30 中、0.50 大。标准化残差 =（观测 − 期望）/√期望，绝对值超过约 2 即提示该格在驱动统计量。通常要求期望频数不低于约 5。本模块依据上方填入的观测与期望序列还原统计量，因此与所填数字完全一致。以上为判读提示。'""")

# ======================================== 11. 单样本 t 检验
OS_EXTRA = r'''
  function __stOne(){
    var xbar = __stNum('xbar'), mu0 = __stNum('mu0'), sd = __stNum('sd'), n = __stNum('n');
    if (!isFinite(xbar) || !isFinite(mu0) || !isFinite(sd) || !isFinite(n)) return null;
    if (!(sd > 0) || n < 2) return null;
    var se = sd / Math.sqrt(n);
    var t = (xbar - mu0) / se;
    var d = (xbar - mu0) / sd;                 // 单样本标准化效应量
    var tc = __stTcrit(n - 1);                 // 双尾 alpha = 0.05
    var crit = isFinite(tc) ? tc * se : NaN;
    return { t: t, d: d, se: se, n: n, df: n - 1, tc: tc, crit: crit, diff: xbar - mu0 };
  }
'''

OS_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charOsBadge');
    var val = document.getElementById('__charOsVal');
    var bar = document.getElementById('__charOsBar');
    var tb = document.getElementById('__charOsRows');
    var m = __stOne();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter the sample mean, the reference value, the SD (positive) and n (at least 2).'
                                    : '请填写样本均值、参照值、标准差（大于 0）与样本量 n（至少 2）。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var ad = Math.abs(m.d);
    var sig = isFinite(m.tc) && Math.abs(m.t) > m.tc;
    var lvl, color;
    if (ad >= 0.80){ lvl = en ? 'Large (Cohen)' : '大效应（Cohen）'; color = '#dc2626'; }
    else if (ad >= 0.50){ lvl = en ? 'Medium (Cohen)' : '中等效应（Cohen）'; color = '#ea580c'; }
    else if (ad >= 0.20){ lvl = en ? 'Small (Cohen)' : '小效应（Cohen）'; color = '#0d9488'; }
    else { lvl = en ? 'Negligible (Cohen)' : '可忽略（Cohen）'; color = '#16a34a'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = sig ? color : '#16a34a';
      badge.textContent = (en ? 'd = ' : 'd = ') + m.d.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 't = ' : 't = ') + m.t.toFixed(4)
      + (en ? '  (df = ' : '（df = ') + m.df + (en ? ')' : '）')
      + (en ? '   Cohen\'s d = ' : '   Cohen\'s d = ') + m.d.toFixed(3);

    var rows = '';
    rows += __stRow(en ? 'Is it significant' : '是否显著',
      (en ? 'At alpha = 0.05 two-tailed with ' : '在 α = 0.05 双尾、df = ') + m.df
      + (en ? ' degrees of freedom the critical value is about ' : ' 时临界值约 ') + (isFinite(m.tc) ? m.tc.toFixed(3) : '-')
      + (sig ? (en ? '; |t| = ' : '；|t| = ') + Math.abs(m.t).toFixed(3) + (en ? ' exceeds it, so the difference is significant.'
                                                                            : ' 超过临界值，差异显著。')
             : (en ? '; |t| = ' : '；|t| = ') + Math.abs(m.t).toFixed(3) + (en ? ' does not reach it, so the difference is not significant.'
                                                                            : ' 未达临界值，差异不显著。')));

    // 效应量：差值除以个体标准差，这才是"差多少"
    rows += __stRow(en ? 'How big is the gap' : '差距有多大',
      (en ? 'Cohen\'s d = (mean - reference) / SD = ' : 'Cohen\'s d =（均值 − 参照值）/ 标准差 = ') + m.d.toFixed(4)
      + (en ? ': the sample sits ' : '：样本均值比参照值高 ') + Math.abs(m.d).toFixed(2)
      + (en ? ' standard deviations away from the reference value (' : ' 个标准差（')
      + (ad >= 0.8 ? (en ? 'large' : '大') : (ad >= 0.5 ? (en ? 'medium' : '中') : (ad >= 0.2 ? (en ? 'small' : '小') : (en ? 'negligible' : '可忽略'))))
      + (en ? ' by Cohen).' : '效应）。')
      + (en ? ' Report this alongside t: a significant result on a huge sample can still be a trivial shift.'
        : ' 报告 t 时应一并给出它：大样本上的显著结果，实际位移仍可能微不足道。'));

    rows += __stRow(en ? 'The interval you should quote' : '该报告的区间',
      (en ? 'The standard error is ' : '标准误为 ') + m.se.toFixed(4)
      + (en ? ', so a 95% interval for the mean is roughly the mean plus or minus ' : '，因此均值的 95% 区间约为均值 ± ')
      + (isFinite(m.crit) ? m.crit.toFixed(4) : '-')
      + (en ? '. If that interval covers the reference value, the data are consistent with it - which is a stronger statement than a bare p value.'
        : '。若该区间覆盖参照值，说明数据与参照值相容 —— 这比单给一个 p 值信息量大得多。'));

    rows += __stRow(en ? 'Assumptions' : '前提',
      (m.n < 15
        ? (en ? 'With n = ' + m.n + ', the test depends on the data being roughly normal. Check a histogram or Q-Q plot; '
                + 'with clear skew use the Wilcoxon signed-rank test or a bootstrap.'
          : 'n = ' + m.n + ' 时，检验依赖数据近似正态。请查看直方图或 Q-Q 图；明显偏态时改用 Wilcoxon 符号秩检验或自助法。')
        : (en ? 'With n = ' + m.n + ' the central limit theorem carries most of the load, so mild non-normality is usually tolerable, '
                + 'but outliers and dependence between observations are not fixed by sample size.'
          : 'n = ' + m.n + ' 时中心极限定律足以支撑，轻度非正态通常可以容忍；'
            + '但离群点与观测不独立，无法靠增大样本解决。')));

    rows += __stRow(en ? 'One sample, one question' : '单样本只回答一个问题',
      en ? 'This test compares one group against a fixed reference value. If you are comparing two measurements on the same subjects use a paired test, '
          + 'and if you are comparing two separate groups use an independent-samples test - picking the wrong one changes the standard error and can flip the conclusion.'
        : '单样本检验把一组数据与固定参照值比较。若比较的是同一批受试者的两次测量，应使用配对检验；'
          + '若比较两组独立对象，则用独立样本检验 —— 选错会改变标准误，甚至翻转结论。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, ad / 2), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? '|d| = ' : '|d| = ') + ad.toFixed(3)
        + (en ? '  (0.2 small / 0.5 medium / 0.8 large)' : '（0.2 小 / 0.5 中 / 0.8 大）')
        + '</div>';
    }
  }'''

OS_NOTE = (r"""en
      ? 'Cohen\'s d for one sample is (mean - reference)/SD, with the usual bands 0.2 small, 0.5 medium, 0.8 large. The interval uses the sample mean plus or minus t_crit(df = n-1) times the standard error SD/sqrt(n) at alpha = 0.05 two-tailed. The test assumes independent observations and, at small n, roughly normal data; with clear skew use the Wilcoxon signed-rank test. Indicative reading aid, not a substitute for checking the assumptions on the real data.'
      : '单样本的 Cohen\'s d =（均值 − 参照值）/ 标准差，常用分级 0.2 小、0.5 中、0.8 大。区间取样本均值 ± t_crit(df = n−1)×标准误 SD/√n（α = 0.05 双尾）。检验假设观测独立，样本小时还要求数据近似正态；明显偏态时应改用 Wilcoxon 符号秩检验。以上为判读提示，不能替代对真实数据前提的检验。'""")


def ht_section():
    return wrap('__charHt', HT_UPDATE, ['mean', 'mu0', 'sigma', 'n', 'alpha', 'tail'], HT_EXTRA,
                HT_TITLE, HT_DESC, HT_NOTE, hook_fn='calculate')


def ch_section():
    return wrap('__charChi', CH_UPDATE, ['o', 'e'], CH_EXTRA, CH_TITLE, CH_DESC, CH_NOTE)


def os_section():
    return wrap('__charOs', OS_UPDATE, ['xbar', 'mu0', 'sd', 'n'], OS_EXTRA, OS_TITLE, OS_DESC, OS_NOTE)


# ---- 第三批（F-CHAR-8）：两类错误 / 卡方效应量 / 单样本 t ----
HT_TITLE = "en ? '⚖️ The errors behind this test' : '⚖️ 这个检验背后的两类错误'"
HT_DESC = ("en ? 'A hypothesis test can fail in two directions. This lays out the false-positive and false-negative rates, "
           "the power of your design, and the smallest effect it can actually detect.' "
           ": '假设检验会在两个方向上出错。这里给出假阳性与假阴性率、当前设计的检验效能，"
           "以及它实际能检出的最小效应。'")

CH_TITLE = "en ? '🔢 How big is this chi-square effect' : '🔢 这个卡方效应有多大'"
CH_DESC = ("en ? 'A chi-square value cannot be compared across sample sizes. This adds Cohen\\'s w, checks the expected counts, "
           "and points at the cell actually driving the result.' "
           ": '卡方值无法跨样本量比较。这里补上 Cohen\\'s w 效应量、检查期望频数，并指出真正驱动结果的那一格。'")

OS_TITLE = "en ? '🎯 What this one-sample test really says' : '🎯 这个单样本检验到底说明什么'"
OS_DESC = ("en ? 'Significance only answers whether the gap is real. This adds the effect size, the interval for the mean, "
           "and the assumptions the test is leaning on.' "
           ": '显著性只回答差距是否真实。这里补上效应量、均值的置信区间，以及检验所依赖的前提。'")

TARGETS3 = {
    'tools/it/hypothesis-test.html': (ht_section, '__charHt'),
    'tools/statistics/chi-square-test.html': (ch_section, '__charChi'),
    'tools/statistics/one-sample-t-test.html': (os_section, '__charOs'),
}

# ======================================== 12. 四分位距与离群点（Tukey 围栏）
IQ_EXTRA = r'''
  function __stIqr(){
    var q1 = __stNum('q1'), q3 = __stNum('q3'), med = __stNum('median_'),
        lo = __stNum('min_'), hi = __stNum('max_'), n = __stNum('data_count');
    if (!isFinite(q1) || !isFinite(q3)) return null;
    var iqr = q3 - q1;
    if (!(iqr >= 0)) return null;
    return { q1: q1, q3: q3, iqr: iqr, med: med, lo: lo, hi: hi, n: n,
             innerLo: q1 - 1.5 * iqr, innerHi: q3 + 1.5 * iqr,
             outerLo: q1 - 3 * iqr, outerHi: q3 + 3 * iqr };
  }
'''

IQ_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charIqBadge');
    var val = document.getElementById('__charIqVal');
    var bar = document.getElementById('__charIqBar');
    var tb = document.getElementById('__charIqRows');
    var m = __stIqr();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter Q1 and Q3 to get the outlier fences. Add the minimum and maximum to detect actual outliers.'
                                    : '请填写 Q1 与 Q3 得到离群点围栏；再填入最小值与最大值即可判定是否存在离群点。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    // 用五数概括判定是否越界
    var outMild = [], outExtreme = [];
    if (isFinite(m.lo)){
      if (m.lo < m.outerLo) outExtreme.push(en ? 'minimum' : '最小值');
      else if (m.lo < m.innerLo) outMild.push(en ? 'minimum' : '最小值');
    }
    if (isFinite(m.hi)){
      if (m.hi > m.outerHi) outExtreme.push(en ? 'maximum' : '最大值');
      else if (m.hi > m.innerHi) outMild.push(en ? 'maximum' : '最大值');
    }
    var lvl, color;
    if (outExtreme.length){ lvl = en ? 'Extreme outliers present' : '存在极端离群点'; color = '#dc2626'; }
    else if (outMild.length){ lvl = en ? 'Mild outliers present' : '存在温和离群点'; color = '#ea580c'; }
    else if (isFinite(m.lo) || isFinite(m.hi)){ lvl = en ? 'No outliers by the fences' : '按围栏无离群点'; color = '#16a34a'; }
    else { lvl = en ? 'Fences ready' : '围栏已算出'; color = '#0d9488'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color; badge.textContent = lvl; }
    if (val) val.textContent = (en ? 'IQR = Q3 - Q1 = ' : 'IQR = Q3 − Q1 = ') + m.iqr.toFixed(4);

    var rows = '';
    // Tukey 围栏：箱线图判定离群点的官方规则
    rows += __stRow(en ? 'Tukey fences' : 'Tukey 围栏',
      (en ? 'The usual fences sit at Q1 - 1.5*IQR and Q3 + 1.5*IQR, here ' : '常用围栏位于 Q1 − 1.5×IQR 与 Q3 + 1.5×IQR，此处为 ')
      + m.innerLo.toFixed(3) + (en ? ' and ' : ' 与 ') + m.innerHi.toFixed(3)
      + (en ? '. Points beyond 3*IQR (' : '。超出 3×IQR（') + m.outerLo.toFixed(3) + (en ? ' / ' : ' / ') + m.outerHi.toFixed(3)
      + (en ? ') are extreme outliers rather than mild ones.' : '）的属于极端离群点，而非温和离群点。'));

    // 实际判定
    var verdict;
    if (outExtreme.length){
      verdict = (en ? 'The ' : '') + outExtreme.join(en ? ' and ' : ' 与 ')
        + (en ? ' lies beyond the 3*IQR fence: an extreme outlier. ' : ' 超出 3×IQR 围栏，属极端离群点。')
        + (en ? 'Check whether it is a data-entry error before deciding to keep or drop it.'
          : ' 先核查是否为录入错误，再决定保留还是剔除。');
    } else if (outMild.length){
      verdict = (en ? 'The ' : '') + outMild.join(en ? ' and ' : ' 与 ')
        + (en ? ' falls outside the 1.5*IQR fence, so it is a mild outlier: worth a look, but not automatically wrong.'
          : ' 落在 1.5×IQR 围栏之外，属温和离群点：值得检查，但不等于一定有误。');
    } else if (isFinite(m.lo) && isFinite(m.hi)){
      verdict = en ? 'Minimum and maximum both sit inside the fences, so no value is flagged on this rule.'
                   : '最小值与最大值都在围栏之内，按该规则没有被标记的点。';
    } else {
      verdict = en ? 'Add the minimum and maximum above to apply the fences to your data.'
                   : '请在上方填入最小值与最大值，即可用围栏判定实际数据。';
    }
    rows += __stRow(en ? 'On your numbers' : '按你的数据', verdict);

    // 稳健的 σ 估计：正态下 IQR = 1.349 sigma
    rows += __stRow(en ? 'A robust scale estimate' : '一个稳健的离散估计',
      (en ? 'For a normal distribution IQR is about 1.349 sigma, so sigma is roughly IQR / 1.349 = '
        : '正态分布下 IQR ≈ 1.349σ，因此 σ 约为 IQR / 1.349 = ')
      + (m.iqr / 1.349).toFixed(4)
      + (en ? '. Unlike the plain standard deviation, this estimate is not dragged around by outliers.'
        : '。与普通标准差不同，这个估计不会被离群点带跑。'));

    // 箱子内部的位置 => 偏态方向
    var skewTxt;
    if (isFinite(m.med) && m.iqr > 0){
      var pos = (m.med - m.q1) / m.iqr;
      var dir = pos < 0.45 ? (en ? 'the upper half is longer, suggesting a right-skewed shape'
                                 : '上半部分更长，提示右偏（长尾在右）')
              : (pos > 0.55 ? (en ? 'the lower half is longer, suggesting a left-skewed shape'
                                 : '下半部分更长，提示左偏（长尾在左）')
                            : (en ? 'the median sits near the middle of the box, suggesting a roughly symmetric shape'
                                  : '中位数接近箱体中部，提示大致对称'));
      skewTxt = (en ? 'The median sits at ' : '中位数位于箱体的 ')
        + (pos * 100).toFixed(1) + '%' + (en ? ' of the box: ' : '：') + dir + (en ? '.' : '。');
    } else {
      skewTxt = en ? 'Add the median to read the shape of the box.' : '填入中位数即可判读箱体形状。';
    }
    rows += __stRow(en ? 'What the box says' : '箱体说明了什么', skewTxt);

    rows += __stRow(en ? 'Why IQR and not the range' : '为什么用 IQR 而不是极差',
      en ? 'The range depends entirely on the two most extreme values, so one bad measurement moves it. '
          + 'The IQR only uses the middle half of the data, which is why box plots and robust summaries are built on it.'
        : '极差完全取决于两个最极端的值，一个错误测量就能改变它。'
          + 'IQR 只用中间一半的数据，这正是箱线图与稳健统计以它为基础的原因。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      var span = (m.innerHi - m.innerLo) || 1;
      var posv = isFinite(m.med) ? (m.med - m.innerLo) / span : 0.5;
      bar.innerHTML = __stBar(Math.max(0, Math.min(1, posv)), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Fences ' : '围栏 ') + m.innerLo.toFixed(3) + (en ? ' to ' : ' 到 ') + m.innerHi.toFixed(3)
        + (en ? '  (1.5 x IQR rule)' : '（1.5×IQR 规则）')
        + '</div>';
    }
  }'''

IQ_NOTE = (r"""en
      ? 'Fences follow Tukey: mild outliers lie beyond Q1 - 1.5*IQR or Q3 + 1.5*IQR, extreme ones beyond Q1 - 3*IQR or Q3 + 3*IQR. The robust scale estimate uses IQR = 1.349*sigma for a normal distribution. Only the five-number summary is used here, so the fence verdict reflects whichever minimum and maximum you enter; it does not see the individual observations. Indicative reading aid, not a rule for automatically deleting data.'
      : '围栏依据 Tukey：温和离群点在 Q1 − 1.5×IQR 或 Q3 + 1.5×IQR 之外，极端离群点在 Q1 − 3×IQR 或 Q3 + 3×IQR 之外。稳健离散估计用正态分布下的 IQR = 1.349σ。本模块只使用五数概括，因此判定结果取决于你填入的最小值与最大值，看不到每一个观测值。以上为判读提示，不构成自动删除数据的依据。'""")

# ======================================== 13. 变异系数 CV
CV_EXTRA = r'''
  function __stCv(){
    var mu = __stNum('mu'), sigma = __stNum('sigma');
    if (!isFinite(mu) || !isFinite(sigma)) return null;
    if (!(sigma >= 0)) return null;
    var cv = mu !== 0 ? (sigma / Math.abs(mu)) * 100 : NaN;
    return { mu: mu, sigma: sigma, cv: cv, snr: sigma > 0 ? Math.abs(mu) / sigma : NaN };
  }
'''

CV_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charCvBadge');
    var val = document.getElementById('__charCvVal');
    var bar = document.getElementById('__charCvBar');
    var tb = document.getElementById('__charCvRows');
    var m = __stCv();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter the mean and the standard deviation (SD at least 0) to read the CV.'
                                    : '请填写均值与标准差（标准差不小于 0）以判读变异系数。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    if (m.mu === 0){
      if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#dc2626';
        badge.textContent = en ? 'Undefined at mean = 0' : '均值为 0 时无定义'; }
      if (val) val.textContent = en ? 'CV is not defined when the mean is 0 (division by zero).'
                                    : '均值为 0 时变异系数无定义（除以 0）。';
      if (bar) bar.innerHTML = '';
      var r0 = __stRow(en ? 'Why it breaks' : '为什么会失效',
        en ? 'The CV divides the spread by the mean, so it explodes as the mean approaches zero and is undefined at zero. '
            + 'Use the standard deviation instead when the mean is near zero.'
          : '变异系数用离散程度除以均值，因此均值趋近 0 时它会急剧放大，等于 0 时无定义。'
            + '均值接近 0 时应改用标准差。');
      var t0 = document.getElementById('__charCvRows');
      if (t0) t0.innerHTML = r0;
      return;
    }
    var cv = m.cv;
    var lvl, color;
    if (cv < 5){ lvl = en ? 'Very low spread' : '离散很小'; color = '#16a34a'; }
    else if (cv < 10){ lvl = en ? 'Low spread' : '离散较小'; color = '#0d9488'; }
    else if (cv < 20){ lvl = en ? 'Moderate spread' : '离散中等'; color = '#ea580c'; }
    else if (cv < 30){ lvl = en ? 'High spread' : '离散偏大'; color = '#dc2626'; }
    else { lvl = en ? 'Very high spread' : '离散很大'; color = '#7f1d1d'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'CV = ' + cv.toFixed(2) + '% · ' + lvl; }
    if (val) val.textContent = (en ? 'CV = ' : 'CV = ') + cv.toFixed(2) + '%'
      + (en ? '   (SD is ' : '（标准差为均值的 ') + (cv / 100).toFixed(4) + (en ? ' of the mean)' : ' 倍）');

    var rows = '';
    // 分级说明：明确这是行业惯例，不是统一标准
    rows += __stRow(en ? 'How to read the bands' : '怎么看这些分级',
      en ? 'There is no single universal cut-off. In laboratory and analytical work a CV under about 10% is often taken as acceptable '
          + 'and under 5% as good; in the social and biological sciences CVs well above 30% are common. '
          + 'Always judge it against the convention in your own field.'
        : '并不存在统一的阈值。实验室与分析化学工作中通常把 CV 低于约 10% 视为可接受、低于 5% 视为良好；'
          + '而在社会科学与生命科学里，CV 超过 30% 也很常见。判读时务必对照本领域的惯例。');

    // 头号陷阱：CV 只在比率尺度有意义
    rows += __stRow(en ? 'Only for ratio scales' : '只适用于比率尺度',
      en ? 'The CV is only meaningful when zero is a real, absolute zero - weight, length, counts, concentrations. '
          + 'For interval scales whose zero is arbitrary, such as temperature in degrees Celsius, a CV is meaningless: '
          + 'switch the same data to kelvin and the CV changes completely.'
        : '只有当"零"是真正的绝对零点时，变异系数才有意义 —— 例如重量、长度、计数、浓度。'
          + '对于零点人为设定的等距尺度（如摄氏度温度），CV 没有意义：把同一批数据换算成开尔文，CV 会完全不同。');

    rows += __stRow(en ? 'Mean near zero' : '均值接近 0',
      (en ? 'This mean is ' : '此处均值为 ') + m.mu.toFixed(4)
      + (Math.abs(m.mu) < Math.abs(m.sigma)
          ? (en ? ', which is smaller in magnitude than the SD: the CV is unstable here and should not be quoted.'
            : '，其绝对值小于标准差：此处的 CV 不稳定，不应引用。')
          : (en ? ', comfortably larger than the SD, so the CV is stable here.'
            : '，明显大于标准差，因此此处 CV 稳定。')));

    rows += __stRow(en ? 'CV or standard deviation' : '用 CV 还是标准差',
      en ? 'Use the SD when your reader knows the units and you are comparing groups measured on the same scale. '
          + 'Use the CV when the means differ by orders of magnitude or the units differ, because it is dimensionless.'
        : '当读者熟悉单位、且比较的是同一量纲上的各组时，用标准差。'
          + '当均值相差几个数量级或单位不同时，用 CV，因为它是无量纲的。');

    rows += __stRow(en ? 'Signal-to-noise view' : '换个角度看：信噪比',
      isFinite(m.snr)
        ? (en ? 'Mean / SD = ' : '均值 / 标准差 = ') + m.snr.toFixed(4)
          + (en ? ', the reciprocal of the CV: a CV of 10% means the mean is 10 times the spread.'
            : '，即 CV 的倒数：CV 为 10% 意味着均值是离散程度的 10 倍。')
        : (en ? 'Not available when the SD is 0.' : '标准差为 0 时不适用。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, cv / 50), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'CV = ' : 'CV = ') + cv.toFixed(2) + '%'
        + (en ? '  (5% / 10% / 20% are common reference points)' : '（常用参考点 5% / 10% / 20%）')
        + '</div>';
    }
  }'''

CV_NOTE = (r"""en
      ? 'CV = SD/|mean| x 100%, and it is only meaningful on a ratio scale where zero is absolute. It is undefined at a mean of zero and unstable when the mean is small relative to the SD. The bands used here (5% / 10% / 20% / 30%) are common working conventions, especially in laboratory and analytical work, not a universal standard - compare against the convention in your own field. Indicative reading aid.'
      : 'CV = 标准差/|均值|×100%，只在零点为绝对零的比率尺度上有意义。均值为 0 时无定义，均值相对标准差很小时不稳定。此处分级（5% / 10% / 20% / 30%）是常见的工作惯例，尤见于实验室与分析工作，并非统一标准 —— 请对照本领域惯例判读。以上为判读提示。'""")

# ======================================== 14. 样本偏度
SK_EXTRA = r'''
  function __stSk(){
    var e = document.getElementById('xs');
    if (!e) return null;
    var xs = String(e.value || '').split(/[\s,]+/).map(function(s){ return parseFloat(s); })
               .filter(function(v){ return isFinite(v); });
    var n = xs.length;
    if (n < 3) return null;
    var mean = 0, i;
    for (i = 0; i < n; i++) mean += xs[i];
    mean /= n;
    var ss = 0;
    for (i = 0; i < n; i++) ss += Math.pow(xs[i] - mean, 2);
    var s = Math.sqrt(ss / (n - 1));
    if (!(s > 0)) return null;
    var cu = 0;
    for (i = 0; i < n; i++) cu += Math.pow((xs[i] - mean) / s, 3);
    var g1 = (n / ((n - 1) * (n - 2))) * cu;
    // 大样本正态下样本偏度的标准误约 sqrt(6/n)
    var se = Math.sqrt(6 / n);
    return { g1: g1, n: n, se: se, mean: mean, sd: s };
  }
'''

SK_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charSkBadge');
    var val = document.getElementById('__charSkVal');
    var bar = document.getElementById('__charSkBar');
    var tb = document.getElementById('__charSkRows');
    var m = __stSk();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter at least 3 numbers with some spread to read the skewness.'
                                    : '请填入至少 3 个有差异的数值，以判读偏度。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var a = Math.abs(m.g1);
    var lvl, color;
    if (a < 0.5){ lvl = en ? 'Fairly symmetric (Bulmer)' : '大致对称（Bulmer）'; color = '#16a34a'; }
    else if (a < 1){ lvl = en ? 'Moderately skewed (Bulmer)' : '中等偏斜（Bulmer）'; color = '#ea580c'; }
    else { lvl = en ? 'Highly skewed (Bulmer)' : '高度偏斜（Bulmer）'; color = '#dc2626'; }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color;
      badge.textContent = 'g1 = ' + m.g1.toFixed(3) + ' · ' + lvl; }
    if (val) val.textContent = (en ? 'Sample skewness g1 = ' : '样本偏度 g₁ = ') + m.g1.toFixed(4)
      + (en ? '  (n = ' : '（n = ') + m.n + (en ? ')' : '）');

    var dir = m.g1 > 0
      ? (en ? 'Positive: the right tail is longer, so the mean usually sits above the median.'
        : '为正：右侧尾部更长，均值通常高于中位数。')
      : (m.g1 < 0 ? (en ? 'Negative: the left tail is longer, so the mean usually sits below the median.'
                      : '为负：左侧尾部更长，均值通常低于中位数。')
                  : (en ? 'Zero: the tails balance out on this measure.' : '为零：按该指标两侧尾部平衡。'));

    var rows = '';
    rows += __stRow(en ? 'Direction' : '方向', dir);

    rows += __stRow(en ? 'How skewed is skewed' : '多偏算偏',
      en ? 'A common rule of thumb (Bulmer, 1979): below about 0.5 in absolute value is fairly symmetric, '
          + '0.5 to 1 is moderate, above 1 is high. These are conventions, not a test.'
        : '常用经验规则（Bulmer, 1979）：绝对值低于约 0.5 大致对称，0.5 到 1 为中等偏斜，'
          + '高于 1 为高度偏斜。这些是惯例，不是检验。');

    // 是否显著偏离 0：用 SE = sqrt(6/n)
    var z = m.g1 / m.se;
    rows += __stRow(en ? 'Is it more than noise' : '是否超出噪声',
      (en ? 'For a normal sample this large, the standard error of skewness is about sqrt(6/n) = '
        : '正态样本在 n = ' + m.n + ' 时，偏度的标准误约为 √(6/n) = ')
      + m.se.toFixed(4) + (en ? ', giving z = ' : '，对应 z = ') + z.toFixed(3)
      + (Math.abs(z) > 2
          ? (en ? '. Beyond about 2 in absolute value, so the asymmetry is unlikely to be pure sampling noise.'
            : '。绝对值超过约 2，说明这种不对称不太可能只是抽样噪声。')
          : (en ? '. Within about 2, so with this sample size you cannot clearly separate real skew from sampling noise.'
            : '。未超过约 2，以当前样本量还无法把真实偏斜与抽样噪声区分开。')));

    rows += __stRow(en ? 'Why it matters' : '为什么重要',
      en ? 'Skew decides which summary is honest. With a long right tail the mean is pulled up and the median describes a typical case better; '
          + 'many common tests also assume roughly symmetric residuals, so strong skew points at a transform or a nonparametric test.'
        : '偏度决定该用哪个汇总量。右尾很长时均值被抬高，中位数更能代表"典型情况"；'
          + '许多常用检验还假设残差大致对称，因此强偏斜提示应做变量变换或改用非参数检验。');

    rows += __stRow(en ? 'Small samples are unreliable' : '小样本不可靠',
      (en ? 'Skewness is computed from cubed deviations, so a single far-out value can dominate it, and with n = '
        : '偏度由离差的三次方算得，单个很远的点就能主导结果；n = ')
      + m.n + (en ? ' the estimate is noisy. Treat the value as a rough signal here, and always look at the histogram as well.'
                  : ' 时估计噪声很大。此处应把它当作粗略信号，务必同时看直方图。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, a / 2), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? '|g1| = ' : '|g₁| = ') + a.toFixed(3)
        + (en ? '  (0.5 moderate / 1 high)' : '（0.5 中等 / 1 高度）')
        + '</div>';
    }
  }'''

SK_NOTE = (r"""en
      ? 'Sample skewness uses the adjusted Fisher-Pearson form g1 = n/((n-1)(n-2)) * sum(((x - mean)/s)^3), matching the page. Bands follow the common rule of thumb (Bulmer, 1979): 0.5 moderate, 1 high. For a normal sample the standard error of skewness is approximately sqrt(6/n), so |g1|/SE beyond about 2 is unlikely to be noise. Skewness is very sensitive to outliers and unstable in small samples - read it together with a histogram. Indicative reading aid.'
      : '样本偏度采用调整的 Fisher-Pearson 形式 g₁ = n/((n−1)(n−2))·Σ((x − x̄)/s)³，与页面一致。分级采用常用经验规则（Bulmer, 1979）：0.5 为中等、1 为高度。正态样本下偏度标准误约为 √(6/n)，故 |g₁|/SE 超过约 2 时不太可能只是噪声。偏度对离群点极敏感且在小样本下不稳定 —— 请结合直方图一起判读。以上为判读提示。'""")

# ======================================== 15. 方差齐性 F 检验
FT_EXTRA = r'''
  // 注意：本页 s1 / s2 填的是**方差**（页面表格标注为 s1^2 / s2^2），F = v1 / v2
  function __stFt(){
    var v1 = __stNum('s1'), v2 = __stNum('s2'), n1 = __stNum('n1'), n2 = __stNum('n2');
    if (!isFinite(v1) || !isFinite(v2) || !isFinite(n1) || !isFinite(n2)) return null;
    if (!(v1 > 0) || !(v2 > 0) || n1 < 2 || n2 < 2) return null;
    var F = v1 / v2;
    var ratioSd = Math.sqrt(Math.max(v1, v2) / Math.min(v1, v2));
    return { F: F, v1: v1, v2: v2, n1: n1, n2: n2, df1: n1 - 1, df2: n2 - 1, ratioSd: ratioSd };
  }
'''

FT_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charFtBadge');
    var val = document.getElementById('__charFtVal');
    var bar = document.getElementById('__charFtBar');
    var tb = document.getElementById('__charFtRows');
    var m = __stFt();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter both variances (positive) and both sample sizes (at least 2).'
                                    : '请填写两个方差（均为正数）与两个样本量（均至少 2）。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    // SD 比值：方差齐性的常用经验阈值
    var hetero = m.ratioSd > 2;
    var lvl = hetero ? (en ? 'SD ratio above 2' : '标准差比值超过 2') : (en ? 'SD ratio within 2' : '标准差比值在 2 以内');
    var color = hetero ? '#ea580c' : '#16a34a';
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = color; badge.textContent = lvl; }
    if (val) val.textContent = (en ? 'F = ' : 'F = ') + m.F.toFixed(4)
      + (en ? '  (df = ' : '（df = ') + m.df1 + ', ' + m.df2 + (en ? ')' : '）')
      + (en ? '   SD ratio = ' : '   标准差比值 = ') + m.ratioSd.toFixed(3);

    var rows = '';
    // 头号陷阱：别把它当作 t 检验的前置筛选
    rows += __stRow(en ? 'Do not use it as a gatekeeper' : '别把它当前置筛选',
      en ? 'The tempting routine is: run this test, and if it is not significant use the pooled t test, otherwise use Welch. '
          + 'That two-step habit is now discouraged: this F test is extremely sensitive to non-normality, so with skewed data it often '
          + 'reports unequal variances when the variances are in fact equal, and stays quiet when they are not. '
          + 'The safer default is to use the Welch test directly - it costs almost nothing when variances really are equal.'
        : '常见做法是：先跑这个检验，不显著就用合并方差 t 检验，显著就用 Welch。'
          + '这种两步流程如今已不推荐：该 F 检验对非正态极其敏感，数据偏态时常常在方差实际相等的情况下报错"不齐"，'
          + '而在方差真的不齐时反而静默。更稳妥的默认做法是直接用 Welch 检验 —— 当方差确实相等时，它几乎不损失效能。');

    rows += __stRow(en ? 'Read the ratio, not just p' : '看比值，不只看 p',
      (en ? 'The two SDs are ' : '两个标准差为 ') + Math.sqrt(m.v1).toFixed(4) + (en ? ' and ' : ' 与 ')
      + Math.sqrt(m.v2).toFixed(4) + (en ? ', a ratio of ' : '，比值 ') + m.ratioSd.toFixed(3)
      + (en ? 'x. With a large sample even a ratio near 1.1 can be significant, but such a small difference barely affects the t test. '
             + 'What matters is the size of the ratio, not whether it clears 0.05.'
        : ' 倍。样本很大时即便比值只有 1.1 也会显著，但这么小的差异对 t 检验几乎没有影响。'
          + '重要的是比值的大小，而不是它是否跨过 0.05。'));

    rows += __stRow(en ? 'Better alternatives' : '更好的替代',
      en ? 'If you do need a formal check of equal variances, Levene\'s test (based on absolute deviations from the group centre) '
          + 'or the Brown-Forsythe version using medians are far more robust to non-normality than this F test, which assumes normality quite strictly.'
        : '若确实需要正式的方差齐性检验，Levene 检验（基于相对组中心的绝对离差）或改用中位数的 Brown-Forsythe 版本，'
          + '对非正态的稳健性远高于这个 F 检验 —— 后者对正态性的假设相当严格。');

    rows += __stRow(en ? 'What to do with unequal variances' : '方差不齐该怎么办',
      en ? 'Use the Welch t test, or Welch ANOVA for more than two groups. If the spread grows with the level, a log or similar transform '
          + 'often stabilises it, and if the outcome is ordinal or strongly skewed consider a rank-based test instead.'
        : '使用 Welch t 检验，多组时用 Welch 方差分析。若离散程度随水平增大，取对数等变换常能稳定方差；'
          + '若结局是有序变量或严重偏态，可考虑秩和检验。');

    rows += __stRow(en ? 'Why variances matter at all' : '方差为什么重要',
      en ? 'The pooled two-sample test averages the two variances into one figure. When the groups really differ in spread, '
          + 'that pooled figure belongs to neither group, and the stated error rate drifts away from 5% - in either direction depending on group sizes.'
        : '合并方差的两样本检验把两个方差平均成一个数值。当两组离散程度真的不同时，'
          + '这个合并值不属于任何一组，名义 5% 的错误率也会偏离 —— 偏离方向取决于两组样本量的对比。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(Math.min(1, (m.ratioSd - 1) / 2), color)
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'SD ratio = ' : '标准差比值 = ') + m.ratioSd.toFixed(3)
        + (en ? '  (about 2 is the usual rule of thumb)' : '（经验阈值约 2）')
        + '</div>';
    }
  }'''

FT_NOTE = (r"""en
      ? 'This page takes variances, so F = v1/v2 with df1 = n1 - 1 and df2 = n2 - 1. The F test for equal variances assumes normality and is highly sensitive to departures from it, which is why using it as a screening step before a t test is now discouraged (see Zimmerman 2004 and Delacre et al. 2017); prefer Welch directly, or Levene / Brown-Forsythe for a formal check. The SD ratio is compared against the common rule of thumb of about 2. Indicative reading aid, not a substitute for inspecting the data.'
      : '本页填入的是方差，故 F = v1/v2，df1 = n1 − 1，df2 = n2 − 1。方差齐性的 F 检验假设正态且对偏离正态极敏感，因此如今不推荐把它当作 t 检验前的筛选步骤（参见 Zimmerman 2004 与 Delacre et al. 2017）；更建议直接用 Welch，或用 Levene / Brown-Forsythe 做正式检验。标准差比值与常用的约 2 倍经验阈值比较。以上为判读提示，不能替代对数据本身的查看。'""")


def iq_section():
    return wrap('__charIq', IQ_UPDATE, ['data_count', 'min_', 'q1', 'median_', 'q3', 'max_'],
                IQ_EXTRA, IQ_TITLE, IQ_DESC, IQ_NOTE, hook_fn='calc')


def cv_section():
    return wrap('__charCv', CV_UPDATE, ['mu', 'sigma'], CV_EXTRA, CV_TITLE, CV_DESC, CV_NOTE)


def sk_section():
    return wrap('__charSk', SK_UPDATE, ['xs'], SK_EXTRA, SK_TITLE, SK_DESC, SK_NOTE)


def ft_section():
    return wrap('__charFt', FT_UPDATE, ['s1', 's2', 'n1', 'n2'], FT_EXTRA, FT_TITLE, FT_DESC, FT_NOTE)


# ---- 第四批（F-CHAR-9）：四分位围栏 / 变异系数 / 偏度 / 方差齐性 ----
IQ_TITLE = "en ? '📦 Outliers and spread, the box-plot way' : '📦 离群点与离散：箱线图的判法'"
IQ_DESC = ("en ? 'Turns the quartiles into Tukey fences, flags mild and extreme outliers, and reads the shape of the box.' "
           ": '把四分位数换算成 Tukey 围栏，标出温和与极端离群点，并判读箱体的形状。'")

CV_TITLE = "en ? '📏 What this CV really tells you' : '📏 这个变异系数到底说明什么'"
CV_DESC = ("en ? 'The CV is dimensionless, which makes it easy to over-use. This explains when it is meaningful, "
           "when it breaks, and how to read the size of it.' "
           ": '变异系数无量纲，因而最容易被滥用。这里说明它何时有意义、何时失效，以及如何判读大小。'")

SK_TITLE = "en ? '📈 What this skewness means' : '📈 这个偏度说明什么'"
SK_DESC = ("en ? 'Skewness decides which average is honest. This gives the direction, the usual bands, "
           "and whether the asymmetry is bigger than sampling noise.' "
           ": '偏度决定用哪个均值才诚实。这里给出方向、常用分级，以及这种不对称是否超出抽样噪声。'")

FT_TITLE = "en ? '⚠️ Should you screen with this test' : '⚠️ 该不该用它做前置筛选'"
FT_DESC = ("en ? 'The F test for equal variances is widely used as a gatekeeper before a t test - and widely misused. "
           "This explains why, and what to do instead.' "
           ": '方差齐性的 F 检验常被当作 t 检验前的筛子 —— 而这正是它被误用的地方。这里说明原因与替代做法。'")

TARGETS4 = {
    'tools/statistics/iqr.html': (iq_section, '__charIq'),
    'tools/statistics/coefficient-of-variation.html': (cv_section, '__charCv'),
    'tools/statistics/skewness-sample.html': (sk_section, '__charSk'),
    'tools/statistics/f-test-variance.html': (ft_section, '__charFt'),
}

# ======================================== 16. 标准误 SE（最常被与 SD 混淆）
SE_EXTRA = r'''
  function __stSe(){
    var sigma = __stNum('sigma'), n = __stNum('n');
    if (!isFinite(sigma) || !isFinite(n)) return null;
    if (!(sigma > 0) || !(n > 0)) return null;
    var se = sigma / Math.sqrt(n);
    // 样本量翻到多少才能把 SE 减半：SE 正比于 1/sqrt(n)，故需 4 倍
    return { sigma: sigma, n: n, se: se, half: 1.96 * se };
  }
'''

SE_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charSeBadge');
    var val = document.getElementById('__charSeVal');
    var bar = document.getElementById('__charSeBar');
    var tb = document.getElementById('__charSeRows');
    var m = __stSe();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter a positive SD and a positive sample size to read the standard error.'
                                    : '请填写正的标准差与正的样本量，以判读标准误。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    var shrink = 1 - (m.se / m.sigma);
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#0d9488';
      badge.textContent = (en ? 'SE is ' : 'SE 为 SD 的 ') + __stPct(m.se / m.sigma)
        + (en ? ' of the SD' : ''); }
    if (val) val.textContent = (en ? 'SE = SD / sqrt(n) = ' : 'SE = SD / √n = ') + m.se.toFixed(4)
      + (en ? '   (SD = ' : '（SD = ') + m.sigma.toFixed(4) + (en ? ', n = ' : '，n = ') + m.n + (en ? ')' : '）');

    var rows = '';
    // 头号混淆：SE 说的是均值，SD 说的是个体
    rows += __stRow(en ? 'SE is not the SD' : 'SE 不是 SD',
      en ? 'The SD describes how spread out the individual observations are. The standard error describes how much the SAMPLE MEAN would '
          + 'move if you repeated the study. Here the SD is ' + m.sigma.toFixed(4) + ' but the SE is only ' + m.se.toFixed(4)
          + ': the same data, two different questions.'
        : '标准差描述单个观测值有多分散；标准误描述的是**样本均值**在重复研究时会波动多少。'
          + '此处 SD = ' + m.sigma.toFixed(4) + '，而 SE 只有 ' + m.se.toFixed(4) + '：同一批数据，两个不同的问题。');

    rows += __stRow(en ? 'Why it shrinks with n' : '为什么随 n 缩小',
      (en ? 'SE = SD / sqrt(' : 'SE = SD / √(') + m.n + (en ? '), so it falls as 1/sqrt(n): ' : ')，因此按 1/√n 下降：')
      + (en ? 'going from n = ' + m.n + ' to n = ' + (m.n * 4) + ' would halve it, not divide it by four. '
             + 'Quadrupling the sample only buys a factor of two in precision.'
        : '样本量由 n = ' + m.n + ' 增加到 n = ' + (m.n * 4) + ' 只能让它减半，而不是变成四分之一。'
          + '样本翻两番，精度只提高一倍。'));

    rows += __stRow(en ? 'The interval it gives' : '它给出的区间',
      (en ? 'A large-sample 95% interval for the mean is roughly the mean plus or minus 1.96 * SE = '
        : '大样本下均值的 95% 区间约为均值 ± 1.96×SE = ') + m.half.toFixed(4)
      + (en ? '. Note this is an interval for the mean, not a range containing 95% of the data - that would need the SD.'
        : '。注意这是均值的区间，不是"包含 95% 数据"的范围 —— 后者要用标准差。'));

    rows += __stRow(en ? 'How error bars mislead' : '误差棒怎么骗人',
      en ? 'Because the SE is always smaller than the SD, plotting SE bars instead of SD bars makes a result look more precise than it is, '
          + 'and readers routinely mistake them for the spread of the data. Say which one you are plotting.'
        : '由于 SE 总是小于 SD，用 SE 画误差棒会让结果看起来比实际更精确，'
          + '而读者常误以为它表示数据的离散范围。务必标明画的是哪一个。');

    rows += __stRow(en ? 'Which one to report' : '该报哪一个',
      en ? 'Report the SD when you are describing your sample - how much individuals vary. Report the SE when you are stating how precisely '
          + 'you have located a mean. Label it explicitly; "mean plus or minus X" is ambiguous on its own.'
        : '描述样本时用 SD（个体之间的差异有多大）；说明均值定位得有多准时用 SE。'
          + '并明确标注 —— 单独写"均值 ± X"是有歧义的。');
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.se / m.sigma, '#0d9488')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'SE shrinks the SD by ' : 'SE 相对 SD 缩小了 ') + __stPct(shrink)
        + (en ? '  at this sample size' : '（当前样本量下）')
        + '</div>';
    }
  }'''

SE_NOTE = (r"""en
      ? 'SE = SD/sqrt(n), so it shrinks as 1/sqrt(n): quadrupling n halves the SE. The SE describes the sampling variability of the mean, while the SD describes the spread of individual observations - they answer different questions and are frequently confused, especially in error bars. The 95% figure uses the large-sample approximation mean +/- 1.96*SE and assumes independent observations. Indicative reading aid.'
      : 'SE = SD/√n，按 1/√n 收缩：样本量翻两番，SE 减半。SE 描述均值的抽样变异，SD 描述单个观测值的离散 —— 两者回答不同问题，且常被混淆，误差棒尤甚。95% 区间用大样本近似 均值 ± 1.96×SE，并假设观测独立。以上为判读提示。'""")

# ======================================== 17. 调和平均
HM_EXTRA = r'''
  function __stHm(){
    var e = document.getElementById('data');
    if (!e) return null;
    var xs = String(e.value || '').split(/[\s,]+/).map(function(s){ return parseFloat(s); })
               .filter(function(v){ return isFinite(v); });
    var n = xs.length;
    if (n < 1) return null;
    var i, sumInv = 0, sum = 0, prod = 1, hasNonPos = false;
    for (i = 0; i < n; i++){
      if (xs[i] <= 0){ hasNonPos = true; break; }
      sumInv += 1 / xs[i];
      sum += xs[i];
      prod *= xs[i];
    }
    if (hasNonPos) return { xs: xs, n: n, bad: true };
    var hm = n / sumInv;
    var am = sum / n;
    var gm = Math.pow(prod, 1 / n);
    var mn = Math.min.apply(null, xs);
    return { xs: xs, n: n, hm: hm, am: am, gm: gm, min: mn, bad: false };
  }
'''

HM_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charHmBadge');
    var val = document.getElementById('__charHmVal');
    var bar = document.getElementById('__charHmBar');
    var tb = document.getElementById('__charHmRows');
    var m = __stHm();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter one or more numbers to read the harmonic mean.'
                                    : '请填入至少一个数值，以判读调和平均。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    if (m.bad){
      if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#dc2626';
        badge.textContent = en ? 'Undefined here' : '此处无定义'; }
      if (val) val.textContent = en ? 'The harmonic mean needs every value to be strictly positive.'
                                    : '调和平均要求每个数值都严格大于 0。';
      if (bar) bar.innerHTML = '';
      var tb2 = document.getElementById('__charHmRows');
      if (tb2) tb2.innerHTML = __stRow(en ? 'Why it fails' : '为什么失效',
        en ? 'The harmonic mean averages reciprocals, so a zero gives division by zero and a negative value breaks the interpretation. '
            + 'Rates and speeds must be positive for this average to make sense.'
          : '调和平均是对倒数取平均，因此出现 0 会导致除以零，出现负数则破坏其含义。'
            + '速率与速度必须为正，这个平均数才有意义。');
      return;
    }
    var gap = m.am - m.hm;
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#0d9488';
      badge.textContent = (en ? 'HM = ' : 'HM = ') + m.hm.toFixed(4); }
    if (val) val.textContent = (en ? 'Harmonic mean = ' : '调和平均 = ') + m.hm.toFixed(4)
      + (en ? '   vs arithmetic ' : '   算术平均 ') + m.am.toFixed(4)
      + (en ? ' and geometric ' : '，几何平均 ') + m.gm.toFixed(4);

    var rows = '';
    // 经典陷阱：往返平均速度
    rows += __stRow(en ? 'The round-trip trap' : '往返速度的陷阱',
      en ? 'Drive out at 60 and back at 40 over the same distance and the average speed is not 50. The trip is 2 units of distance, '
          + 'and the time is 1/60 + 1/40 hours per unit, so the average speed is the harmonic mean, 48. '
          + 'Whenever the quantity you hold fixed is the distance rather than the time, use the harmonic mean.'
        : '去程 60、回程 40，同样的距离，平均速度不是 50。总路程为 2 个单位，总时间为 1/60 + 1/40 小时每单位，'
          + '因此平均速度是调和平均 48。只要固定的量是"距离"而不是"时间"，就该用调和平均。');

    rows += __stRow(en ? 'When to reach for it' : '什么时候该用它',
      en ? 'Use the harmonic mean for rates and ratios - speeds over equal distances, unit prices when you spend a fixed amount each time, '
          + 'parallel resistances, or anything where the quantity in the denominator is what stays constant. '
          + 'Using the plain average in those cases systematically overstates the result.'
        : '速率与比率用调和平均 —— 等距离上的速度、每次花固定金额时的平均单价、并联电阻，'
          + '以及任何"分母固定"的情形。这些场合用普通平均会系统性地高估结果。');

    // AM >= GM >= HM
    rows += __stRow(en ? 'The three averages' : '三个平均数的关系',
      (en ? 'For positive numbers the ordering is always arithmetic >= geometric >= harmonic: here '
        : '对正数而言恒有 算术 ≥ 几何 ≥ 调和：此处 ')
      + m.am.toFixed(4) + ' >= ' + m.gm.toFixed(4) + ' >= ' + m.hm.toFixed(4)
      + (en ? '. They coincide only when every value is identical; the wider the spread, the further apart they sit.'
        : '。只有当所有数值相同时三者才相等；离散越大，它们相差越远。'));

    rows += __stRow(en ? 'It is dominated by small values' : '它受小值主导',
      (en ? 'The smallest value here is ' : '此处最小值为 ') + m.min.toFixed(4)
      + (en ? '. Because the harmonic mean works on reciprocals, one very small value pulls it down hard - '
             + 'much harder than it pulls down the arithmetic mean. Check for a genuine zero or a data-entry slip before trusting it.'
        : '。由于调和平均作用于倒数，一个很小的值会把它拉得很低 —— 远比它对算术平均的影响大。'
          + '采信之前请确认是否真有 0 或录入错误。'));

    rows += __stRow(en ? 'What the gap tells you' : '两者之差说明什么',
      (en ? 'Arithmetic minus harmonic here is ' : '此处算术平均减调和平均 = ') + gap.toFixed(4)
      + (gap > 0
          ? (en ? ', a sign the values are spread out: the closer the two averages, the more uniform the data.'
            : '，说明数值比较分散：两个平均数越接近，数据越均匀。')
          : (en ? ': zero, meaning all the values are the same.' : '，为 0，说明所有数值相同。')));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.am > 0 ? m.hm / m.am : 0, '#0d9488')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'HM / AM = ' : 'HM / AM = ') + (m.am > 0 ? (m.hm / m.am).toFixed(4) : '-')
        + (en ? '  (1 means all values are equal)' : '（为 1 表示所有数值相同）')
        + '</div>';
    }
  }'''

HM_NOTE = (r"""en
      ? 'The harmonic mean is n / sum(1/x) and requires every value to be strictly positive. It is the right average for rates when the denominator is held fixed - equal distances at different speeds, fixed spending at different prices, parallel resistances. For positive numbers, arithmetic >= geometric >= harmonic, with equality only when all values match. It is dominated by the smallest values, so check for zeros and entry errors. Indicative reading aid.'
      : '调和平均为 n / Σ(1/x)，要求每个数值严格大于 0。当分母固定时它是正确的平均 —— 等距离不同速度、固定花费不同单价、并联电阻。对正数恒有 算术 ≥ 几何 ≥ 调和，仅当所有数值相同时取等。它受最小值主导，请留意 0 与录入错误。以上为判读提示。'""")

# ======================================== 18. 百分位排名
PR_EXTRA = r'''
  function __stPr(){
    var de = document.getElementById('data'), ve = document.getElementById('val');
    if (!de || !ve) return null;
    var xs = String(de.value || '').split(/[\s,]+/).map(function(s){ return parseFloat(s); })
               .filter(function(v){ return isFinite(v); });
    var v = parseFloat(ve.value);
    if (!xs.length || !isFinite(v)) return null;
    var n = xs.length, below = 0, equal = 0, i;
    for (i = 0; i < n; i++){
      if (xs[i] < v) below++;
      else if (xs[i] === v) equal++;
    }
    // 常用定义：(低于该值的个数 + 0.5 * 等于的个数) / n
    var pr = (below + 0.5 * equal) / n * 100;
    var strict = below / n * 100;
    return { pr: pr, strict: strict, n: n, below: below, equal: equal, v: v,
             min: Math.min.apply(null, xs), max: Math.max.apply(null, xs) };
  }
'''

PR_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charPrBadge');
    var val = document.getElementById('__charPrVal');
    var bar = document.getElementById('__charPrBar');
    var tb = document.getElementById('__charPrRows');
    var m = __stPr();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter the data set and the value to locate its percentile rank.'
                                    : '请填入数据集与待定位的数值，以得到百分位排名。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#0d9488';
      badge.textContent = (en ? 'PR = ' : 'PR = ') + m.pr.toFixed(1) + (en ? 'th percentile' : ' 百分位'); }
    if (val) val.textContent = (en ? 'Percentile rank = ' : '百分位排名 = ') + m.pr.toFixed(2)
      + (en ? '  (' : '（') + m.below + (en ? ' below, ' : ' 个低于，') + m.equal
      + (en ? ' equal, out of ' : ' 个等于，共 ') + m.n + (en ? ')' : '）');

    var rows = '';
    // 头号误读：PR 不是"答对率"
    rows += __stRow(en ? 'It is not a score' : '它不是得分率',
      en ? 'A percentile rank of 90 does NOT mean "90% correct". It means this value sits at or above about 90% of the values in this particular set. '
          + 'It is a position within a comparison group, never an amount of knowledge or accuracy.'
        : '百分位排名 90 并不表示"答对 90%"，而是表示这个值不低于该数据集中约 90% 的值。'
          + '它是在某个比较组内的相对位置，绝不是正确率或掌握程度。');

    rows += __stRow(en ? 'Rank versus percentile' : '百分位排名 vs 百分位数',
      en ? 'The two directions are easy to swap: a percentile is a VALUE below which a given share of the data falls, '
          + 'while a percentile rank is the SHARE of data at or below a given value. This page computes the second one.'
        : '这两个方向很容易弄反：百分位数是"某个比例的数据落在其下的**数值**"，'
          + '而百分位排名是"某个数值所对应的**比例**"。本页算的是后者。');

    // 分辨率：小样本只能取离散档位
    var step = 100 / m.n;
    rows += __stRow(en ? 'Resolution depends on n' : '分辨率取决于样本量',
      (en ? 'With n = ' : 'n = ') + m.n + (en ? ' the rank can only move in steps of about ' : ' 时，排名只能以约 ')
      + step.toFixed(1) + (en ? ' percentage points, so small differences in rank carry little information. '
                                + 'Two people one place apart may differ by almost nothing.'
                          : ' 个百分点为步长变化，因此排名的细小差别信息量很低。'
                            + '名次相差一位，实际水平可能几乎没差别。')
      + (m.equal > 1
          ? (en ? ' Here ' + m.equal + ' values tie with yours; the 0.5 weighting used here splits the difference.'
            : ' 此处有 ' + m.equal + ' 个值与你的数值相同；本页采用的 0.5 加权把它分摊处理。')
          : ''));

    rows += __stRow(en ? 'It depends on the group' : '它取决于比较组',
      (en ? 'This rank is measured only against the ' : '这个排名只是相对你填入的 ') + m.n
      + (en ? ' numbers entered above, which span ' : ' 个数而言，其范围为 ') + m.min.toFixed(3)
      + (en ? ' to ' : ' 到 ') + m.max.toFixed(3)
      + (en ? '. Change the comparison group and the same value gets a different rank - so always state which group you used.'
        : '。换一个比较组，同一个值会得到不同的排名 —— 因此必须说明用的是哪一组。'));

    rows += __stRow(en ? 'Ties and the definition' : '并列与定义差异',
      (en ? 'Counting only strictly lower values gives ' : '只统计严格更小的数值时得到 ') + m.strict.toFixed(2)
      + (en ? '%, while the common "below plus half the ties" definition gives ' : '%，而常用的"低于者加一半并列者"定义给出 ')
      + m.pr.toFixed(2) + (en ? '%. Different textbooks and software pick different conventions, so quote the definition with the number.'
                               : '%。不同教材与软件采用不同约定，因此报数时应一并说明所用定义。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.pr / 100, '#0d9488')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'Position within this group: ' : '在本组中的相对位置：') + m.pr.toFixed(1) + '%'
        + '</div>';
    }
  }'''

PR_NOTE = (r"""en
      ? 'Percentile rank here uses the common definition (number below + 0.5 x number equal) / n x 100%; counting only strictly lower values would give the alternative shown in the table. A percentile rank is a position within a specific comparison group, not a percentage score or an accuracy figure. With small n the rank can only change in steps of 100/n, and different fields and software use different tie conventions, so state the definition and the group. Indicative reading aid.'
      : '本页百分位排名采用常用定义（低于的个数 + 0.5×并列的个数）/ n × 100%；只统计严格更小值则为表中所列的另一算法。百分位排名是特定比较组内的位置，不是得分率或正确率。样本量小时排名只能以 100/n 为步长变化，且不同领域与软件对并列的处理约定不同，因此报数时应说明定义与比较组。以上为判读提示。'""")

# ======================================== 19. 几何平均
GM_EXTRA = r'''
  function __stGm(){
    var e = document.getElementById('data');
    if (!e) return null;
    var xs = String(e.value || '').split(/[\s,]+/).map(function(s){ return parseFloat(s); })
               .filter(function(v){ return isFinite(v); });
    var n = xs.length;
    if (n < 1) return null;
    var i, sum = 0, hasNonPos = false, logSum = 0;
    for (i = 0; i < n; i++){
      sum += xs[i];
      if (xs[i] <= 0){ hasNonPos = true; break; }
      logSum += Math.log(xs[i]);
    }
    if (hasNonPos) return { xs: xs, n: n, bad: true, am: sum / n };
    var gm = Math.exp(logSum / n);
    return { xs: xs, n: n, gm: gm, am: sum / n, bad: false,
             min: Math.min.apply(null, xs), max: Math.max.apply(null, xs) };
  }
'''

GM_UPDATE = r'''{
    var en = __stIsEn();
    var badge = document.getElementById('__charGmBadge');
    var val = document.getElementById('__charGmVal');
    var bar = document.getElementById('__charGmBar');
    var tb = document.getElementById('__charGmRows');
    var m = __stGm();
    if (!m){
      if (badge) badge.style.display = 'none';
      if (val) val.textContent = en ? 'Enter one or more numbers to read the geometric mean.'
                                    : '请填入至少一个数值，以判读几何平均。';
      if (bar) bar.innerHTML = '';
      if (tb) tb.innerHTML = '';
      return;
    }
    if (m.bad){
      if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#dc2626';
        badge.textContent = en ? 'Undefined here' : '此处无定义'; }
      if (val) val.textContent = en ? 'The geometric mean needs every value to be strictly positive (a zero or a negative breaks it).'
                                    : '几何平均要求每个数值都严格大于 0（出现 0 或负数即失效）。';
      if (bar) bar.innerHTML = '';
      var tg = document.getElementById('__charGmRows');
      if (tg) tg.innerHTML = __stRow(en ? 'Why it fails' : '为什么失效',
        en ? 'The geometric mean multiplies the values and takes the nth root, so a single zero makes it zero and a negative value '
            + 'makes the root undefined for an even count. Add a constant only if the shift is meaningful, and say that you did.'
          : '几何平均先把数值相乘再开 n 次方，因此只要有一个 0 结果就是 0，出现负数时偶次根无定义。'
            + '只有在平移确实有意义时才加常数，且必须说明做过平移。');
      return;
    }
    if (badge){ badge.style.display = 'inline-block'; badge.style.background = '#0d9488';
      badge.textContent = (en ? 'GM = ' : 'GM = ') + m.gm.toFixed(4); }
    if (val) val.textContent = (en ? 'Geometric mean = ' : '几何平均 = ') + m.gm.toFixed(4)
      + (en ? '   vs arithmetic ' : '   算术平均 ') + m.am.toFixed(4);

    var rows = '';
    // 经典陷阱：平均增长率
    rows += __stRow(en ? 'The growth-rate trap' : '平均增长率的陷阱',
      en ? 'Gain 50% one year and lose 50% the next and the arithmetic average says 0%, but you end up with 0.75 of what you started - a 25% loss. '
          + 'The geometric mean of 1.5 and 0.5 is about ' + Math.sqrt(1.5 * 0.5).toFixed(4) + ', i.e. roughly a 13.4% loss per year. '
          + 'For anything that compounds - growth rates, returns, ratios - use the geometric mean.'
        : '一年涨 50%、次年跌 50%，算术平均说是 0%，但你的本金只剩 0.75 —— 实际亏了 25%。'
          + '1.5 与 0.5 的几何平均约为 ' + Math.sqrt(1.5 * 0.5).toFixed(4) + '，即每年约亏 13.4%。'
          + '凡是复利型的量 —— 增长率、收益率、比率 —— 都要用几何平均。');

    rows += __stRow(en ? 'When to use it' : '什么时候用',
      en ? 'Use it for data that combine by multiplication rather than addition: growth factors, index numbers, aspect ratios, '
          + 'or measurements spread over several orders of magnitude. Use the arithmetic mean when values add up.'
        : '适用于以"相乘"方式组合的数据：增长因子、指数、比率，或跨越几个数量级的测量值。'
          + '数值是相加关系时用算术平均。');

    rows += __stRow(en ? 'The gap between the two' : '两个平均的差距',
      (en ? 'Arithmetic is ' : '算术平均 ') + m.am.toFixed(4) + (en ? ', geometric is ' : '，几何平均 ') + m.gm.toFixed(4)
      + (en ? '. The arithmetic mean is always at least as large, and the gap grows with the spread: here the values run from '
        : '。算术平均恒不小于几何平均，且差距随离散程度增大：此处数值范围为 ')
      + m.min.toFixed(4) + (en ? ' to ' : ' 到 ') + m.max.toFixed(4)
      + (en ? '. A large gap is a signal that the data are skewed or spread across magnitudes.' : '。差距大即提示数据偏斜或跨量级。'));

    rows += __stRow(en ? 'Why it is gentler' : '为什么它更"温和"',
      en ? 'Because it works in logarithms, the geometric mean is pulled much less by one huge value than the arithmetic mean is. '
          + 'That is what makes it the honest centre for skewed, multiplicative data - but it also means it hides how large the biggest values are.'
        : '由于它在对数尺度上运算，几何平均受个别极大值的影响远小于算术平均。'
          + '这正是它适合偏斜、相乘型数据的原因 —— 但同时它也会掩盖最大值到底有多大。');

    rows += __stRow(en ? 'Zero and negative values' : '零与负值的处理',
      (en ? 'All ' : '此处 ') + m.n + (en ? ' values here are positive, so the geometric mean is well defined. '
                                       + 'If a series can contain zero or negative entries, the geometric mean cannot be used directly - '
                                       + 'consider working with log-transformed values or a different summary.'
                                     : ' 个数值都为正，因此几何平均有定义。'
                                       + '若序列中可能出现 0 或负数，则不能直接使用几何平均 —— '
                                       + '可考虑对数值取对数后处理，或改用其他汇总量。'));
    if (tb) tb.innerHTML = rows;

    if (bar){
      bar.innerHTML = __stBar(m.am > 0 ? m.gm / m.am : 0, '#0d9488')
        + '<div style="font-size:12px;color:var(--text-muted);">'
        + (en ? 'GM / AM = ' : 'GM / AM = ') + (m.am > 0 ? (m.gm / m.am).toFixed(4) : '-')
        + (en ? '  (1 means all values are equal)' : '（为 1 表示所有数值相同）')
        + '</div>';
    }
  }'''

GM_NOTE = (r"""en
      ? 'The geometric mean is exp(mean(log x)), i.e. the nth root of the product, and needs every value to be strictly positive. It is the correct centre for multiplicative or compounding quantities such as growth factors, returns and ratios; a 50% gain followed by a 50% loss is a 25% loss overall, not a wash. It is always at most the arithmetic mean, with equality only when all values match. Indicative reading aid.'
      : '几何平均为 exp(均值(log x))，即乘积开 n 次方，要求每个数值严格大于 0。对于相乘或复利型的量（增长因子、收益率、比率），它才是正确的中心；先涨 50% 再跌 50%，总体是亏 25% 而非持平。它恒不大于算术平均，仅当所有数值相同时取等。以上为判读提示。'""")


def se_section():
    return wrap('__charSe', SE_UPDATE, ['sigma', 'n'], SE_EXTRA, SE_TITLE, SE_DESC, SE_NOTE)


def hm_section():
    return wrap('__charHm', HM_UPDATE, ['data'], HM_EXTRA, HM_TITLE, HM_DESC, HM_NOTE)


def pr_section():
    return wrap('__charPr', PR_UPDATE, ['data', 'val'], PR_EXTRA, PR_TITLE, PR_DESC, PR_NOTE)


def gm_section():
    return wrap('__charGm', GM_UPDATE, ['data'], GM_EXTRA, GM_TITLE, GM_DESC, GM_NOTE)


# ---- 第五批（F-CHAR-10）：标准误 / 调和平均 / 百分位排名 / 几何平均 ----
SE_TITLE = "en ? '📐 SE is not the SD' : '📐 标准误不是标准差'"
SE_DESC = ("en ? 'The standard error and the standard deviation answer different questions and are constantly confused. "
           "This spells out which is which, and why error bars mislead.' "
           ": '标准误与标准差回答的是两个不同问题，却常被混为一谈。这里说清哪个是哪个，以及误差棒为什么会骗人。'")

HM_TITLE = "en ? '🚗 When the average speed is not the average' : '🚗 平均速度不等于速度的平均'"
HM_DESC = ("en ? 'The harmonic mean is the right average for rates. This shows the round-trip trap, when to use it, "
           "and why small values dominate it.' "
           ": '调和平均才是速率的正确平均。这里给出往返速度的陷阱、适用场合，以及它为何受小值主导。'")

PR_TITLE = "en ? '📊 What this percentile rank means' : '📊 这个百分位排名说明什么'"
PR_DESC = ("en ? 'A percentile rank is a position, not a score. This clears up the most common misreading, "
           "and shows how much the comparison group and the sample size matter.' "
           ": '百分位排名是位置，不是得分。这里澄清最常见的误读，并说明比较组与样本量有多大影响。'")

GM_TITLE = "en ? '📈 Why growth rates need this average' : '📈 为什么增长率要用这个平均'"
GM_DESC = ("en ? 'The arithmetic average quietly overstates anything that compounds. This shows the growth-rate trap, "
           "when the geometric mean is the honest centre, and where it fails.' "
           ": '算术平均会悄悄高估一切复利型的量。这里给出增长率陷阱、几何平均的正确场合，以及它的失效边界。'")

TARGETS5 = {
    'tools/statistics/standard-error.html': (se_section, '__charSe'),
    'tools/statistics/harmonic-mean.html': (hm_section, '__charHm'),
    'tools/statistics/percentile-rank.html': (pr_section, '__charPr'),
    'tools/statistics/geometric-mean.html': (gm_section, '__charGm'),
}

TARGETS = {
    'tools/statistics/correlation-coefficient.html': (corr_section, '__charCorr'),
    'tools/statistics/cohens-d.html': (cd_section, '__charCohen'),
    'tools/statistics/cramers-v.html': (cr_section, '__charCram'),
    'tools/statistics/odds-ratio.html': (or_section, '__charOr'),
}

# 第二批：默认不跑，需显式 `python3 scripts/_ux_char_stat.py --batch2`
TARGETS2 = {
    'tools/statistics/relative-risk.html': (rr_section, '__charRr'),
    'tools/statistics/confidence-proportion.html': (ci_section, '__charCi'),
    'tools/statistics/independent-t-test.html': (tt_section, '__charTt'),
    'tools/statistics/one-way-anova.html': (av_section, '__charAv'),
}


def inject(path, build, mark):
    s = open(path, encoding='utf-8').read()
    if 'id="%s"' % mark in s:
        return False
    sec = build()
    if '</body>' in s:
        s = s.replace('</body>', sec + '\n</body>', 1)
    else:
        s = s + sec
    open(path, 'w', encoding='utf-8').write(s)
    return True


def main():
    if '--batch5' in sys.argv:
        targets = TARGETS5
    elif '--batch4' in sys.argv:
        targets = TARGETS4
    elif '--batch3' in sys.argv:
        targets = TARGETS3
    elif '--batch2' in sys.argv:
        targets = TARGETS2
    else:
        targets = TARGETS
    done = skip = miss = 0
    for rel, (build, mark) in targets.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("MISS", rel); miss += 1; continue
        if inject(p, build, mark):
            done += 1; print("OK  ", rel)
        else:
            skip += 1; print("SKIP", rel)
    print("injected=%d skipped(already)=%d missing=%d" % (done, skip, miss))


if __name__ == '__main__':
    main()
