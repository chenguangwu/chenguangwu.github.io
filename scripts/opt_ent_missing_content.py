#!/usr/bin/env python3
# 补建 ent 批 2 个缺失的 content_deepdive key（工具页存在但无内容条目）
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CD = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

MISSING = {
    'ent/pure-tone-audiometry': {
        'title': '纯音听力筛查 · 听力图',
        'summary': '纯音听力筛查（听力图）工具。用 Web Audio 生成 125 / 250 / 500 / 1000 / 2000 / 4000 / 8000 Hz 共 8 个频率纯音，逐耳采用升法（从低到高）估算听阈，自动绘制标准听力图（频率对数轴 × dB 轴，标注正常 / 轻度 / 中度 / 重度 / 极重度区带），按 WHO 分级：正常 ≤25、轻度 26–40、中度 41–60、重度 61–80、极重度 >80 dB HL。',
        'scenarios': [
            '自测双耳各频率听阈，初步判断有无听力下降。',
            '对比左右耳听力图，发现单侧听力损失。',
            '按 WHO 分级了解下降程度（正常 / 轻 / 中 / 重 / 极重）。'
        ],
        'examples': [
            {
                'title': '右耳 4 kHz 听阈 35 dB',
                'body': '右耳 1000 Hz 听阈 20 dB、4000 Hz 听阈 35 dB，PTA≈28 dB，评级轻度，提示高频轻度下降，建议到医疗机构做专业纯音测听确认。'
            }
        ],
        'faqs': [
            {
                'q': '网页能替代专业纯音测听吗？',
                'a': '不能。网页未做 dB HL 硬件校准，音量随设备与耳机差异很大，仅供娱乐与科普，不能用于诊断或替代耳科检查。'
            },
            {
                'q': 'WHO 分级怎么算？',
                'a': '取 500 / 1000 / 2000 / 4000 Hz 平均听阈（PTA）：正常 ≤25、轻度 26–40、中度 41–60、重度 61–80、极重度 >80 dB HL。'
            }
        ]
    },
    'ent/temporal-resolution-hearing': {
        'title': '听觉时间分辨率测试',
        'summary': '听觉时间分辨率测试工具。包含「间隙检测」（Gap Detection Threshold，GDT）与「调制检测」（Amplitude Modulation Detection，AMD）两种范式，采用 2-IFC 自适应阶梯法估算毫秒级 / 百分比阈值，并对照儿童 / 青年 / 中年 / 老年参考范围，反映听觉系统对快速时间结构变化的察觉能力。',
        'scenarios': [
            '自测对短暂静默（间隙）的察觉能力，评估中枢听觉处理。',
            '评估对响度起伏（振幅调制）的追踪能力。',
            '对照年龄参考范围，了解时间分辨是否随年龄下降。'
        ],
        'examples': [
            {
                'title': '青年间隙阈值约 4 ms',
                'body': '25 岁受试者间隙检测阈值 4.2 ms、调制深度阈值 10%，均落在青年参考范围内，时间分辨基本正常。'
            }
        ],
        'faqs': [
            {
                'q': '间隙检测与调制检测有什么区别？',
                'a': '间隙检测判断两段噪声之间能否听出静默间断；调制检测判断纯音响度是否周期起伏，二者共同反映时间分辨能力。'
            },
            {
                'q': '结果能当诊断吗？',
                'a': '不能。受设备、耳机、环境噪声与个体差异影响很大，仅供娱乐对照，不能替代专业听力与耳科检查。'
            }
        ]
    }
}

cd = json.load(open(CD, encoding='utf-8'))
added = 0
for k, v in MISSING.items():
    if k in cd:
        print('EXISTS(skip):', k)
        continue
    cd[k] = v
    added += 1
    print('ADDED:', k)

if added:
    json.dump(cd, open(CD, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('saved, added', added)
else:
    print('nothing to add')
