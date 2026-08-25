/* ===== ToolBox UI 模板共享脚本 ===== */
(function(){
  'use strict';

  // 主题管理
  const ThemeManager = {
    init(){
      const saved = localStorage.getItem('toolbox-theme');
      if(saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)){
        document.body.classList.add('dark');
      }
      const btn = document.querySelector('.theme-toggle');
      if(btn){
        btn.addEventListener('click', () => this.toggle());
      }
    },
    toggle(){
      document.body.classList.toggle('dark');
      const isDark = document.body.classList.contains('dark');
      localStorage.setItem('toolbox-theme', isDark ? 'dark' : 'light');
    }
  };

  // Tab 切换
  function initTabs(){
    document.querySelectorAll('.tabs').forEach(tabGroup => {
      const btns = tabGroup.querySelectorAll('.tab-btn');
      btns.forEach(btn => {
        btn.addEventListener('click', () => {
          btns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const target = btn.getAttribute('data-tab');
          if(target){
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(c => {
              c.classList.toggle('active', c.getAttribute('data-tab') === target);
            });
          }
        });
      });
    });
  }

  // Toast
  function showToast(msg, type){
    type = type || 'success';
    let container = document.querySelector('.toast-container');
    if(!container){
      container = document.createElement('div');
      container.className = 'toast-container';
      container.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:9999;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none;';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.style.cssText = 'background:var(--text);color:var(--card);padding:10px 20px;border-radius:12px;font-size:14px;box-shadow:0 8px 24px rgba(0,0,0,0.2);animation:fadeIn 0.3s ease;pointer-events:auto;';
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s';
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  }

  // 复制文本
  function copyText(text){
    if(navigator.clipboard){
      navigator.clipboard.writeText(text).then(() => showToast('已复制到剪贴板'));
    } else {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try{ document.execCommand('copy'); showToast('已复制到剪贴板'); }catch(e){ showToast('复制失败','error'); }
      ta.remove();
    }
  }

  // DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    initTabs();
  });

  // 暴露
  window.Template = {
    toggleTheme: () => ThemeManager.toggle(),
    showToast,
    copyText
  };
})();
