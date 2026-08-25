/* B4-04 Freemium：AI 工具每日免费次数 + 付费解锁
 * 规则：
 *  - 基础工具全免费；仅 AI 工具（tools/ai/*.html）按次计费
 *  - 每日免费 N 次（默认 5），localStorage 按日期计数（toolbox_ai_quota_YYYYMMDD）
 *  - 付费解锁：toolbox_ai_unlocked = '1'，之后无限使用
 *  - 支付跳转：window.TOOLBOX_PAY_URL（Stripe Payment Link / GitHub Sponsors），默认 GitHub Sponsors
 *  - 红线：限制提示为轻提示（非弹窗、不打断、不水印、不出现在核心工具上）
 * 接入：AI 工具页 head 加载本文件；common.js 无关。runAI 在 module 脚本中定义为
 *       window.runAI，本文件在 DOMContentLoaded 时包装它加入配额门禁（module 先于
 *       DOMContentLoaded 执行，保证拿到已定义的原函数）。
 */
window.Freemium = (function(){
  'use strict';
  var LS_UNLOCK = 'toolbox_ai_unlocked';
  var LS_QUOTA = 'toolbox_ai_quota_';
  var DAILY_FREE = 5;
  var PAY_URL = window.TOOLBOX_PAY_URL || 'https://github.com/sponsors/chenguangwu';

  function pad(n){ return n < 10 ? '0' + n : String(n); }
  function todayKey(){
    var d = new Date();
    return LS_QUOTA + d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate());
  }
  function getCount(){
    try { return parseInt(localStorage.getItem(todayKey()) || '0', 10) || 0; } catch(e){ return 0; }
  }
  function isUnlocked(){
    try { return localStorage.getItem(LS_UNLOCK) === '1'; } catch(e){ return false; }
  }
  function remaining(){
    return isUnlocked() ? Infinity : Math.max(0, DAILY_FREE - getCount());
  }
  // 消耗一次配额：返回 {ok, remaining, unlocked}
  function consume(){
    if (isUnlocked()) return { ok: true, remaining: Infinity, unlocked: true };
    var c = getCount();
    if (c >= DAILY_FREE) return { ok: false, remaining: 0, unlocked: false };
    try { localStorage.setItem(todayKey(), String(c + 1)); } catch(e){}
    return { ok: true, remaining: DAILY_FREE - c - 1, unlocked: false };
  }
  function unlock(){
    try { localStorage.setItem(LS_UNLOCK, '1'); } catch(e){}
  }
  // 轻提示（底部居中浮条，可关闭，不打断操作）
  function showLimit(){
    try {
      var div = document.getElementById('toolboxFreemiumTip');
      if (div) return;
      div = document.createElement('div');
      div.id = 'toolboxFreemiumTip';
      div.setAttribute('style',
        'position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:9999;' +
        'background:#fff;border:1px solid #E5E7EB;border-radius:14px;' +
        'box-shadow:0 8px 30px rgba(0,0,0,.15);padding:16px 20px;max-width:340px;' +
        'text-align:center;font-size:13.5px;color:#1F2937;');
      div.innerHTML =
        '<div style="font-size:26px;margin-bottom:6px;">🔋</div>' +
        '<div style="font-weight:700;margin-bottom:4px;">今日免费次数已用完</div>' +
        '<div style="color:#6B7280;margin-bottom:12px;">每天 ' + DAILY_FREE + ' 次免费 AI 使用 · 解锁后无限使用全部 AI 工具</div>' +
        '<div style="display:flex;gap:8px;justify-content:center;">' +
        '<a href="' + PAY_URL + '" target="_blank" rel="noopener" style="background:linear-gradient(135deg,#FF6B35,#7C3AED);color:#fff;border:0;border-radius:10px;padding:9px 18px;font-size:13px;font-weight:700;text-decoration:none;cursor:pointer;">⚡ 解锁无限使用</a>' +
        '<button onclick="this.parentNode.parentNode.remove()" style="background:#f3f4f6;color:#374151;border:0;border-radius:10px;padding:9px 16px;font-size:13px;cursor:pointer;">知道了</button>' +
        '</div>';
      document.body.appendChild(div);
    } catch(e){}
  }
  // 包装 window.runAI：消耗配额，超额拦截并提示
  function patch(){
    try {
      if (!window.runAI || window.__runAI_patched) return;
      window.__runAI_patched = true;
      var orig = window.runAI;
      window.runAI = function(){
        var r = consume();
        if (!r.ok) { showLimit(); return; }
        return orig.apply(this, arguments);
      };
    } catch(e){}
  }
  document.addEventListener('DOMContentLoaded', patch);

  return {
    DAILY_FREE: DAILY_FREE,
    PAY_URL: PAY_URL,
    remaining: remaining,
    consume: consume,
    isUnlocked: isUnlocked,
    unlock: unlock,
    showLimit: showLimit
  };
})();
