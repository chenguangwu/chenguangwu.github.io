#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补全 design b 批（music-scale-reference~web-audio-metronome）faqs 至 3 条。
主脚本已写 summary + 3 scenarios + 1 example + 第1条真实 faqs；本脚本补第2条（工具特有真实问答，不与第1条重复）+ 第3条（隐私）。
"""
import json
P='i18n/tools/content_deepdive.json'
d=json.load(open(P,encoding='utf-8'))
DIS='结果以浏览器实时计算为准，纯前端本地处理、数据不上传；生成的样式与代码仅作快速产出参考，正式项目请以设计系统、规范与浏览器实测为准。'

BKEYS=['music-scale-reference','neomorphism-generator','palette-extractor','particle-effect-generator','pattern-generator','photo-aspect-ratio-calculator','photo-print-size','photo-storage-calculator','pixel-art','pixel-art-generator','png-to-svg','progress-bar-generator','px-to-rem','qr-code-styled','rem-to-px','ripple-effect','shadow-generator','shadow-generator-advanced','shutter-speed-calculator','signature-pad','skeleton-loader','spacing-scale','spectrum-visualizer','spinner-generator','stripe-pattern','svg-minifier','svg-to-png','svg-viewer','tailwind-colors','text-shadow-generator','toast-generator','typography-scale','vh-vw','waveform-visualizer','web-audio-metronome']

QA2={
 'music-scale-reference': dict(q='小调怎么看？', a='自然小调全半排列为全半全全半全全；和声小调升七级，旋律小调上行升六七十级。'),
 'neomorphism-generator': dict(q='光源方向怎么定？', a='由双向阴影的明暗决定，统一一个方向（如左上）更自然，避免双向矛盾。'),
 'palette-extractor': dict(q='色数限制多少？', a='取前 N 主色即可；色数越多越接近原图但越杂，一般 5~8 色够用。'),
 'particle-effect-generator': dict(q='能导出图片吗？', a='可导出当前帧 PNG 或动画代码，用于网页背景与活动页。'),
 'pattern-generator': dict(q='密度怎么调？', a='改周期与线宽即可；周期越大越疏，线宽越大越实。'),
 'photo-aspect-ratio-calculator': dict(q='留边还是裁切？', a='按比例取框，可裁切或加边留白；社媒多裁切、打印多留白，按需求选。'),
 'photo-print-size': dict(q='英寸和像素关系？', a='英寸×DPI=像素；想清晰先定 DPI 再反推所需像素。'),
 'photo-storage-calculator': dict(q='质量影响多大？', a='JPG 质量越低文件越小但越糊；按用途权衡，归档建议高质量。'),
 'pixel-art': dict(q='导出什么格式？', a='导出 PNG 保硬边；避免 JPG 引入噪点破坏像素感。'),
 'pixel-art-generator': dict(q='块大小怎么选？', a='块越大越像素化；小图用小块更细腻，大图可用大块出风格。'),
 'png-to-svg': dict(q='转后还能编辑吗？', a='SVG 为路径，可继续在矢量软件里缩放编辑，不失真。'),
 'progress-bar-generator': dict(q='不确定进度怎么做？', a='未知时长用 indeterminate 循环样式，已知百分比用 width 过渡。'),
 'px-to-rem': dict(q='为何推荐用 rem？', a='rem 随根字号整体缩放，利于无障碍缩放与响应式，px 固定不随。'),
 'qr-code-styled': dict(q='容错等级怎么选？', a='装饰会降低容错；关键场景降装饰、保 L/M 容错与静区。'),
 'rem-to-px': dict(q='为何要换算回 px？', a='调试时常用 px 核对真实渲染尺寸，便于与设计稿逐像素对齐。'),
 'ripple-effect': dict(q='涟漪色怎么定？', a='取半透明主题色，浅底上更明显；可随组件配色调整。'),
 'shadow-generator': dict(q='阴影方向怎么定？', a='由 x/y 偏移决定，正向右下、负向左上；调正负即改光源方向。'),
 'shadow-generator-advanced': dict(q='怎么做彩色阴影？', a='用多层不同色 shadow 叠加即可出彩色或发光效果，注意层数性能。'),
 'shutter-speed-calculator': dict(q='长曝要注意什么？', a='长曝需三脚架，即便防抖也难手持稳住，避免糊片。'),
 'signature-pad': dict(q='能重新签吗？', a='可清空重画；导出前确认无误，本工具只生成图像不认证。'),
 'skeleton-loader': dict(q='什么时候用？', a='内容加载预期长时用骨架屏；极短加载用 spinner 即可。'),
 'spacing-scale': dict(q='负间距怎么处理？', a='间距用正 token；需要重叠时用 margin 负值，不要借间距 token 表达。'),
 'spectrum-visualizer': dict(q='频段数怎么定？', a='FFT 大小决定频段数；越大越细但更耗算力，按设备取舍。'),
 'spinner-generator': dict(q='大小和速度怎么调？', a='调尺寸与 animation-duration；过大过慢都不适，中等最稳。'),
 'stripe-pattern': dict(q='能做双色吗？', a='可设双色与底色，调对比度即可得到醒目或柔和条纹。'),
 'svg-minifier': dict(q='能处理内联 SVG 吗？', a='支持粘贴 inline SVG；过大文件建议先分段再压缩。'),
 'svg-to-png': dict(q='透明能保留吗？', a='导出 PNG 支持透明通道；如需白底可自行垫底再导出。'),
 'svg-viewer': dict(q='能编辑吗？', a='本工具仅预览对照；编辑请用 SVG 编辑软件或直接改代码。'),
 'tailwind-colors': dict(q='类名怎么对应？', a='如 bg-orange-500 对应 500 档 HEX，可类名与变量混用。'),
 'text-shadow-generator': dict(q='发光色怎么选？', a='用主题色半透明做发光，深浅控制强度，深底上更明显。'),
 'toast-generator': dict(q='位置怎么定？', a='用 fixed 定位到顶/底/角，配合 transform 做入出场动画。'),
 'typography-scale': dict(q='基字号怎么定？', a='正文通常 16px 起；过小伤可读，按受众与设备调整。'),
 'vh-vw': dict(q='和 % 有什么区别？', a='% 相对父元素，vh/vw 相对视口；全屏布局用视口单位更直接。'),
 'waveform-visualizer': dict(q='精度够吗？', a='按采样与峰值显示，仅供查看定位；精确分析请用音频软件。'),
 'web-audio-metronome': dict(q='需要音频文件吗？', a='无需文件，Web Audio 直接发声；仅本地播放不上传。'),
}

for k in BKEYS:
    key='design/'+k
    v=d[key]
    faqs=list(v.get('faqs',[]))
    if len(faqs)<2:
        assert k in QA2, '缺 QA2: '+k
        faqs.append(QA2[k])
    if len(faqs)<3:
        faqs.append(dict(q='会保存或上传我的内容吗？', a=DIS))
    v['faqs']=faqs[:3]
    d[key]=v
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('design b 批 faqs 补全完成')
bad=[k for k in BKEYS if len(d['design/'+k].get('faqs',[]))!=3]
print('faqs!=3 的 key:', bad)
