#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 content 分类 4 个 content_deepdive key（第十八种占位变体，summary 原 None）。
仅覆盖 content/ 段，不触碰其他分类。不覆盖 title。
"""
import json

SRC = 'i18n/tools/content_deepdive.json'

REAL = {
    "content/checker-5": {
        "summary": "对文本或文档做结构、格式与常见问题的批量检查（如标题层级、链接、重复段落），输出问题清单与定位，辅助发布前自查。结果为机器初检，最终以人工复核为准。",
        "scenarios": [
            "公众号/博客发布前，批量扫标题层级、图片 alt、外链有效性，避免排版与死链问题。",
            "把多版草稿放一起比对，用同一检查模板定位前后版本差异与遗漏项。",
            "批量稿件的重复段落与空标题检查，辅助编辑快速挑出待修处。"
        ],
        "examples": [
            {"title": "发布前自查", "code": "输入 10 篇草稿 → 输出问题清单：\n3 篇缺 img alt、2 篇标题跳级、1 篇重复段\n按定位逐篇修"}
        ],
        "faqs": [
            {"q": "能替代人工审校吗？", "a": "不能。只做规则化初检（层级/链接/重复），语文与事实错误需人工；结果供优先处理。"},
            {"q": "检查规则能自定义吗？", "a": "按本工具内置模板运行；如需特定规范，以你设定的口径为准，本工具不强制统一样式。"},
            {"q": "结果能直接改稿吗？", "a": "不直接改。输出定位与建议，修改在你的编辑器完成，避免误改原文。"}
        ]
    },
    "content/generator-33": {
        "summary": "按设定（题材/人物/冲突）生成小说大纲、人设与章节草稿，辅助网文或短篇起步。结果为创作灵感与初稿，版权与质量以作者打磨为准，非代写成品。",
        "scenarios": [
            "开新书前用模板填题材、主角目标、核心冲突，生成三幕式大纲与人设卡，打破空白页。",
            "卡章节时给定上章结尾与走向，生成 2–3 个续写选项，挑可用的扩写。",
            "批量生成配角小传（身份/动机/秘密），保持群像不扁平。"
        ],
        "examples": [
            {"title": "新书起步", "code": "输入：都市/重生/主角想还债\n输出：大纲(起承转合) + 人设(3 主角) + 第1章草稿 800 字"}
        ],
        "faqs": [
            {"q": "生成的是成品吗？", "a": "不是。是初稿与灵感，需作者重写打磨；直接发布雷同度高、质量不稳。"},
            {"q": "会侵权吗？", "a": "本工具按你输入要素组合，不抓取他人作品；最终成稿原创性由作者负责。"},
            {"q": "能定字数吗？", "a": "可指定章节目标字数区间，实际以生成结果为准，长文建议分段生成再拼。"}
        ]
    },
    "content/generator-34": {
        "summary": "按主题与页数生成 PPT 大纲、版式与要点文案，辅助汇报/课件快速成稿。结果为结构草稿，视觉与数据以你在 PowerPoint 中精修为准。",
        "scenarios": [
            "周报/立项汇报前输入要点，生成 8–12 页大纲（封面/目录/现状/方案/计划/结尾），少想结构。",
            "把长文压缩成演讲型 PPT 要点，每页一句核心 + 三支撑，避免字多。",
            "课件按章节生成知识卡片版式建议，配合图表占位。"
        ],
        "examples": [
            {"title": "汇报成稿", "code": "输入：季度复盘\n输出：大纲(6页) + 每页标题与 3 要点 + 图表建议(柱状/折线)"}
        ],
        "faqs": [
            {"q": "能直接出可编辑 PPT 吗？", "a": "本工具出大纲与文案草稿，导入 PPT 再排版；不带模板版权。"},
            {"q": "页数怎么控？", "a": "按你给的页数区间生成；内容多可拆分，少可合并，以演讲节奏为准。"},
            {"q": "数据图能生成吗？", "a": "只给图表类型建议（柱状/折线），真实数据在你源表，避免编造数字。"}
        ]
    },
    "content/generator-time-1": {
        "summary": "辅助字幕时间轴调整与格式转换（如 SRT 偏移、合并、语言标注），提升观看同步与多语对照。结果为时间轴处理，翻译质量以人工为准。",
        "scenarios": [
            "下载的字幕整体偏移（音画不同步）时，批量加减时间轴让对白归位。",
            "把长句字幕按停顿拆成两行，降低阅读压力、适配移动端。",
            "双语对照时给每句加原文/译文标注，便于语言学习。"
        ],
        "examples": [
            {"title": "音画同步修正", "code": "输入 SRT + 偏移 +1.2s\n输出：全轨时间轴后移 1.2 秒的 SRT"}
        ],
        "faqs": [
            {"q": "能自动翻译字幕吗？", "a": "本工具做时间轴与格式处理，不含翻译；译文需你提供或用翻译工具后并入。"},
            {"q": "偏移量怎么定？", "a": "用播放器看首句对白偏差秒数填入；批量后移/前移统一生效。"},
            {"q": "支持哪些格式？", "a": "常见 SRT 为主；特定格式先转 SRT 再处理，避免编码乱码。"}
        ]
    },
}


def main():
    d = json.load(open(SRC, encoding='utf-8'))
    n_total = len(REAL)
    n_applied = 0
    n_skip = 0
    for key, val in REAL.items():
        if key in d:
            d[key] = val
            n_applied += 1
        else:
            n_skip += 1
            print('  [warn] key 不在 JSON，跳过:', key)
    json.dump(d, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('applied:', n_applied, '/', n_total, '| skip:', n_skip)
    PHRASE = ['content 场景下', '先校准', '口径后再批量输出', '对重复场景采用同一模板', '降低口径误差风险', '建议固定其他输入', '在consulting场景下', '在community场景下', '核对']
    ph = 0
    ok = 0
    for key in REAL:
        if key in d:
            v = d[key]
            blob = ' '.join(v.get('scenarios', [])) + ' ' + ' '.join(x.get('title', '') for x in v.get('examples', []))
            faqs = ' '.join(x.get('q', '') + x.get('a', '') for x in v.get('faqs', []))
            if any(p in blob for p in PHRASE) or any(p in faqs for p in PHRASE):
                ph += 1
            if bool(v.get('summary')) and len(v.get('scenarios', [])) == 3 and len(v.get('examples', [])) == 1 and len(v.get('faqs', [])) == 3:
                ok += 1
    print('结构完整:', ok, '/', len(REAL), '| 占位残留:', ph)


if __name__ == '__main__':
    main()
