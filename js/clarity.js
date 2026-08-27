(function(c,l,a,r,i,t,y){
  if (c.__tbClarityLoaded) return;
  c.__tbClarityLoaded = true;
  c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
  t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i+'?ref=bwt';
  y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, 'clarity', 'script', 'y48102uvzx');

// 51.la 站点统计（第三方分析，统一从此共享脚本动态注入，避免逐页内联重复）
(function () {
  if (window.__laLoaded) return;
  window.__laLoaded = true;
  var s = document.createElement('script');
  s.charset = 'UTF-8';
  s.id = 'LA_COLLECT';
  s.src = '//sdk.51.la/js-sdk-pro.min.js';
  s.onload = function () {
    if (window.LA) {
      window.LA.init({id:"3R0rVW6KKmLfdAFz",ck:"3R0rVW6KKmLfdAFz",autoTrack:true,hashMode:true,screenRecord:true});
    }
  };
  var first = document.getElementsByTagName('script')[0];
  if (first && first.parentNode) {
    first.parentNode.insertBefore(s, first);
  } else if (document.head) {
    document.head.appendChild(s);
  }
})();
