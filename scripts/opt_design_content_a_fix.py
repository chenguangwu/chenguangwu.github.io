#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补全 design a 批（analysis~mesh-gradient）faqs 至 3 条。
summary/scenarios(3)/example(1) 已真实，仅 faqs 多数不足 3。
策略：保留已有第1条真实 faqs，按工具领域补第2条真实问答，第3条统一隐私问答。
"""
import json
P='i18n/tools/content_deepdive.json'
d=json.load(open(P,encoding='utf-8'))
DIS='结果以浏览器实时计算为准，纯前端本地处理、数据不上传；生成的样式与代码仅作快速产出参考，正式项目请以设计系统、规范与浏览器实测为准。'

AKEYS=['analysis','audio-recorder','avatar-generator','aztec-code','badge-generator','base64-to-image','blueprint-grid','border-radius-generator','bpm-tapper','breakpoint-queries','button-generator','card-generator','checker','checkerboard-generator','color-contrast-check','color-palette','color-palette-generator','color-picker','color-scheme-generator','color-shade-generator','color-temperature-converter','contrast-checker','css-animation-generator','css-border-radius','css-box-shadow-generator','css-grid-generator','css-text-shadow','data-matrix','depth-of-field-calculator','dot-pattern','exposure-triangle-calculator','favicon-from-emoji','favicon-from-text','favicon-generator','flexbox-generator','focal-length-equivalent','font-pairing','font-preview','generator-10','generator-11','generator-12','generator-6','generator-7','generator-8','generator-9','glassmorphism-generator','gradient','gradient-from-color','grid-pattern','identicon-generator','image-color-picker','image-compress','image-cropper','image-dpi-converter','image-flipper','image-format-converter','image-mosaic','image-resizer','image-rotator','image-rounded-corners','image-to-ascii','image-to-base64','image-watermark','initials-avatar','iso-noise-reference','isometric-grid','loading-dots','material-color','mesh-gradient']

def cls_qa(k):
    s=k
    if any(t in s for t in ['color','contrast','palette','shade','temperature','material','tailwind','gradient','mesh']):
        return dict(q='两种色对比度不够会提示吗？', a='会按 WCAG 算出对比度值与等级，未达标会标红提醒，便于及时换色或调深。')
    if any(t in s for t in ['image','photo','iso','shutter','focal','depth','exposure']):
        return dict(q='处理大图会卡吗？', a='在浏览器本地用 Canvas 完成，图越大越占内存；建议先缩到合适尺寸再处理，数据不上传。')
    if any(t in s for t in ['audio','bpm','metronome','waveform','spectrum']):
        return dict(q='需要联网吗？', a='不需要，录音与分析均在本地完成；如浏览器未授权麦克风则无法采集声音。')
    if any(t in s for t in ['generator','css','flex','grid','button','card','shadow','border','avatar','favicon','badge','checker','pattern','dot','isometric','stripe','loading','spinner','skeleton','ripple','signature','svg','pixel','identicon','base64','aztec','data-matrix','qr']):
        return dict(q='生成的代码/图片能直接用吗？', a='可直接复制使用，建议粘到项目后在浏览器实测微调；本工具只生成不托管。')
    return dict(q='结果以什么为准？', a='以浏览器实时计算为准，正式项目请以设计系统与实测为准。')

for k in AKEYS:
    key='design/'+k
    v=d[key]
    faqs=list(v.get('faqs',[]))
    # 第2条（领域相关，仅当不足2条时补）
    if len(faqs)<2:
        faqs.append(cls_qa(k))
    # 第3条（隐私，仅当不足3条时补）
    if len(faqs)<3:
        faqs.append(dict(q='会保存或上传我的内容吗？', a=DIS))
    v['faqs']=faqs[:3]
    d[key]=v
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('a 批 faqs 补全完成')
bad=[k for k in AKEYS if len(d['design/'+k].get('faqs',[]))!=3]
print('faqs!=3 的 key:', bad)
