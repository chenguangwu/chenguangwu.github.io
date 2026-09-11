#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校正 wear-brake 的 i18n 源数据（刹车片 → 刹车盘口径）。

背景：页面 <title>/<h1> 的权威来源是 i18n/tools/automotive.json 的 zh-CN 块（build 据此
渲染），而 body 由 auto_shell_lib 重建脚本生成。此前只改了页面 head 与 body，未改 i18n 源，
导致 build 后 <title> 又被重置回「刹车片磨损限度」，与 body h1「刹车盘磨损与更换」不一致。

同时更新 i18n/tools/automotive-phrases.json 的标题短语映射（中→英），保证英文页标题同步。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND_PATH = os.path.join(ROOT, 'i18n', 'tools', 'automotive.json')
PHRASE_PATH = os.path.join(ROOT, 'i18n', 'tools', 'automotive-phrases.json')

SLUG = 'wear-brake'
NEW_TITLE = '刹车盘磨损与更换'
NEW_INTRO = '按盘厚、MIN 极限与跳动量判断刹车盘能否继续使用，并估算剩余可磨寿命。'
NEW_NOTES = [
    '刹车盘厚度须多点实测取最小值，低于 MIN 标记必须更换',
    '制动抖动多因盘面跳动量超差（>0.05 mm），需车削或更换',
    '盘与片应配套评估，只换其一会加剧偏磨与异响',
]
NEW_EN_TITLE = 'Brake Disc Wear & Replacement'
NEW_EN_INTRO = ('Estimate remaining service life of a brake disc from its thickness, '
                'MIN limit and lateral runout.')

LEGACY_TITLE = '刹车片磨损限度'
LEGACY_INTRO = '输入刹车片当前厚度、新品厚度、磨损极限与使用里程，评估安全状态与剩余使用寿命。'
LEGACY_NOTES = [
    '前刹车片磨损通常比后轮快 2~3 倍',
    '激烈驾驶（频繁急刹）会大幅缩短刹车片寿命',
    '听到金属摩擦声说明已到极限，必须立即更换',
    '本工具纯前端运行，数据不会上传到服务器',
]


def main():
    # 1) i18n/tools/automotive.json
    with open(IND_PATH, encoding='utf-8') as f:
        d = json.load(f)
    blk = d[SLUG]
    zc = blk.setdefault('zh-CN', {})
    print('旧 zh-CN.title : %s' % zc.get('title'))
    zc['h1'] = NEW_TITLE
    zc['title'] = NEW_TITLE
    zc['desc'] = NEW_TITLE
    zc['intro'] = NEW_INTRO
    zc['note'] = NEW_NOTES + ['本工具纯前端运行，数据不会上传到服务器']
    blk['note'] = zc['note']
    en = blk.setdefault('en-US', {})
    en['title'] = NEW_EN_TITLE
    en['h1'] = NEW_EN_TITLE
    en['intro'] = NEW_EN_INTRO
    if LEGACY_INTRO in json.dumps(blk, ensure_ascii=False):
        print('⚠️ 旧 intro 仍有残留，请检查')
    with open(IND_PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('automotive.json 已更新 → zh-CN.title = %s' % NEW_TITLE)

    # 2) phrases 短语映射
    with open(PHRASE_PATH, encoding='utf-8') as f:
        p = json.load(f)
    cnt = 0
    for old, new, en in [
        (LEGACY_TITLE, NEW_TITLE, NEW_EN_TITLE),
        ('/ ' + LEGACY_TITLE, '/ ' + NEW_TITLE, '/ ' + NEW_EN_TITLE),
    ]:
        if old in p:
            del p[old]
            p[new] = en
            cnt += 1
    # 旧的「Wear Brake」映射若仍存在，替换为新英文
    for k, v in list(p.items()):
        if v == 'Wear Brake' and k not in (NEW_TITLE, '/ ' + NEW_TITLE):
            p[k] = NEW_EN_TITLE
            cnt += 1
    with open(PHRASE_PATH, 'w', encoding='utf-8') as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('automotive-phrases.json 更新 %d 条映射' % cnt)
    print('新映射: %r → %r' % (NEW_TITLE, p.get(NEW_TITLE)))


if __name__ == '__main__':
    main()
