/*
 * 已下线工具页的旧路径只保留给搜索引擎及外部历史链接使用。
 * 首页会在读取 localStorage 的收藏和最近使用记录时调用 resolve()，确保站内
 * 点击始终直达最终规范页面，不再经过静态跳转桩。
 */
(function (global) {
  'use strict';

  var aliases = Object.freeze({
    '/tools/agriculture/calc-14.html': '/tools/agriculture/crop-water-requirement.html',
    '/tools/agriculture/calc-3.html': '/tools/agriculture/continuous-cropping-index.html',
    '/tools/agriculture/calc-4.html': '/tools/agriculture/greenhouse-rolling-time.html',
    '/tools/agriculture/calc-5.html': '/tools/agriculture/greenhouse-ventilation.html',
    '/tools/beauty/self-assess-1.html': '/tools/beauty/skin-tewl.html',
    '/tools/cardiology/calc-2.html': '/tools/cardiology/chads2-vasc.html',
    '/tools/construction/estimate-area-dosage-1.html': '/tools/construction/soundproof-material.html',
    '/tools/construction/estimate-volume-load.html': '/tools/construction/radiator-calculator.html',
    '/tools/daily-goods/classify-32.html': '/tools/daily-goods/index.html',
    '/tools/dailychem/classify-36.html': '/tools/dailychem/index.html',
    '/tools/dailychem/huanbao-tianranyugongxiaoduibijisuanqi.html': '/tools/dailychem/index.html',
    '/tools/dailychem/manager-classify-6.html': '/tools/dailychem/index.html',
    '/tools/dentistry/estimate-27.html': '/tools/dentistry/bruxism-force.html',
    '/tools/dentistry/kouqiangkuiyang-afuta-fenqi.html': '/tools/dentistry/oral-ulcer.html',
    '/tools/dentistry/quankouyichi-heweiguanxi-zhuanyi.html': '/tools/dentistry/complete-denture.html',
    '/tools/dentistry/ratio-13.html': '/tools/dentistry/alveolar-bone-loss.html',
    '/tools/design/color-scheme-generator.html': '/tools/design/color-palette.html',
    '/tools/encode/utf8-bytes.html': '/tools/encode/utf-8.html',
    '/tools/energy/calc-area-air.html': '/tools/energy/air-purifier-area.html',
    '/tools/energy/calculator-calc-power.html': '/tools/energy/standby-power-calculator.html',
    '/tools/fire/classify-121.html': '/tools/fire/index.html',
    '/tools/food-processing/tester-5.html': '/tools/food-processing/emulsion-stability.html',
    '/tools/food-safety/compare-11.html': '/tools/food-safety/index.html',
    '/tools/food-testing/rater-risk.html': '/tools/food-testing/allergen-cross-risk.html',
    '/tools/gastroenterology/assessor-9.html': '/tools/gastroenterology/intestinal-metaplasia.html',
    '/tools/general/analysis-temp-pressure.html': '/tools/general/index.html',
    '/tools/general/bolt-classify.html': '/tools/general/index.html',
    '/tools/general/carbon-classify-1.html': '/tools/general/index.html',
    '/tools/general/carbon-classify.html': '/tools/general/index.html',
    '/tools/general/classify-100.html': '/tools/general/index.html',
    '/tools/general/classify-101.html': '/tools/general/index.html',
    '/tools/general/classify-102.html': '/tools/general/index.html',
    '/tools/general/classify-103.html': '/tools/general/index.html',
    '/tools/hematology/assessor-4.html': '/tools/hematology/iron-overload.html',
    '/tools/hydraulic/estimate-18.html': '/tools/hydraulic/calc-54.html',
    '/tools/it/calc-6.html': '/tools/it/regex.html',
    '/tools/it/git-cheatsheet.html': '/tools/it/git-commands.html',
    '/tools/it/qrcode-generator.html': '/tools/it/qrcode.html',
    '/tools/it/sn-generator.html': '/tools/it/serial-key-generator.html',
    '/tools/legal/estimate-accident.html': '/tools/legal/traffic-accident-compensation.html',
    '/tools/life/todo-list.html': '/tools/life/index.html',
    '/tools/meteorology/wind-beaufort.html': '/tools/meteorology/beaufort-scale.html',
    '/tools/nephrology/rater-15.html': '/tools/nephrology/vascular-calcification.html',
    '/tools/pet/pet-food.html': '/tools/pet/pet-feeding-calc.html',
    '/tools/procurement/calc-15.html': '/tools/procurement/eoq.html',
    '/tools/sales/calc-1.html': '/tools/sales/commission-calculator.html',
    '/tools/urology/niaodaoxiazhai-niaoliulv-yupan.html': '/tools/urology/index.html',
    '/tools/valve/tool-004-111.html': '/tools/valve/index.html',
    '/tools/welding/jietou-sheji-pokou-jianxi-xingshi.html': '/tools/welding/index.html',
    '/tools/woodwork/paoxue-damoshazhimushuxuanzezhinan.html': '/tools/woodwork/index.html'
  });

  function resolve(url) {
    if (typeof url !== 'string') return url;
    var match = url.match(/^(https?:\/\/chenguangwu\.github\.io)?(\/tools\/[^?#]+)([?#].*)?$/i);
    if (!match || !aliases[match[2]]) return url;
    return (match[1] || '') + aliases[match[2]] + (match[3] || '');
  }

  global.ToolPathAliases = Object.freeze({ resolve: resolve });
})(window);
