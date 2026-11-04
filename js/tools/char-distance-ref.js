/* 距离量级感知模块（horizon-distance / length-pipeline / speed-distance 三页共用一份实现）
 * 页面内联 oninput 调用 __charDistUpdate，必须显式挂到 window 上。 */
(function(){
  var REFS = [
    ['标准跑道一圈', 'Standard track lap', 400],
    ['足球场长度', 'Soccer field length', 105],
    ['一层楼高', 'One floor height', 3],
    ['成年人身高', 'Adult height', 1.7],
    ['珠穆朗玛峰', 'Mount Everest', 8848.86],
    ['马拉松', 'Marathon', 42195],
    ['赤道周长', 'Earth equator', 40075000],
    ['地月距离', 'Earth–Moon', 384400000],
    ['日地距离', 'Earth–Sun', 149600000000]
  ];
  function __charFmt(n, en){
    if(n>=1e8) return (en? (n/1e9).toFixed(2)+' billion m' : (n/1e8).toFixed(2)+' 亿米');
    if(n>=1e4) return (n/1000).toFixed(n>=1e6?0:1)+' km';
    if(n>=1000) return (n/1000).toFixed(2)+' km';
    if(n>=1) return n.toFixed(n<10?2:0)+' m';
    return (n*100).toFixed(1)+' cm';
  }
  function __charIsEn(){
    try { return new URLSearchParams(location.search).get('lang')==='en-US'; } catch(e){ return false; }
  }
  function __charDistUpdate(){
    var en = __charIsEn();
    var v = parseFloat(document.getElementById('__charDistVal').value);
    var out = document.getElementById('__charDistOut');
    if(!isFinite(v)||v<=0){ out.textContent=''; return; }
    var below=null, above=null;
    for(var i=0;i<REFS.length;i++){
      if(REFS[i][2]<=v) below=REFS[i];
      if(REFS[i][2]>=v && above===null) above=REFS[i];
    }
    var parts=[];
    if(below) parts.push((v/below[2]).toFixed(2)+' × '+(en?below[1]:below[0]));
    if(above && above!==below) parts.push((v/above[2]).toFixed(3)+' × '+(en?above[1]:above[0]));
    out.textContent = (en?'≈ ':'约 ')+parts.join(' / ');
    var tb=document.getElementById('__charDistRef');
    if(tb && !tb.dataset.filled){
      var rows='';
      for(var j=0;j<REFS.length;j++){
        rows+='<tr><td style="padding:4px 6px;border-bottom:1px solid var(--border);">'+(en?REFS[j][1]:REFS[j][0])+'</td><td style="text-align:right;padding:4px 6px;border-bottom:1px solid var(--border);">'+__charFmt(REFS[j][2], en)+'</td></tr>';
      }
      tb.innerHTML=rows; tb.dataset.filled='1';
    }
  }
  window.__charDistUpdate = __charDistUpdate;
  function __charInit(){
    var en = __charIsEn();
    document.getElementById('__charDistTitle').textContent = en?'📏 Distance Magnitude Sense':'📏 距离量级感知';
    document.getElementById('__charDistDesc').textContent = en?'Enter a length or distance in meters to compare against common references.':'输入一个长度或距离（米），直观对照常见参照物，建立量级概念。';
    document.getElementById('__charDistSum').textContent = en?'Common distance references':'常见距离参照';
    document.getElementById('__charDistUnit').textContent = en?'meters (m)':'米 (m)';
    document.getElementById('__charDistTh1').textContent = en?'Reference':'参照物';
    document.getElementById('__charDistTh2').textContent = en?'Length':'长度';
    __charDistUpdate();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',__charInit);
  else __charInit();
})();
