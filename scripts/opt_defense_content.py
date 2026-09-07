#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 content_deepdive 中 defense 2 key（第二十六种占位变体）为真实国防/军事评分场景。
占位变体：在defense场景下，先对 <Title> 建模统一口径，再输出可复核结论…
仅改 defense/ 前缀的 key；summary 原 None、faqs 仅 2 条。补 summary+3 scenarios+1 example(body)+3 faqs。
射击/军体类结果为估算参考，不替代实弹校枪、专业训练指导与正式考核裁判；标准以现役官方版本为准。
幂等：已含真实 summary 的 key 跳过。
"""
import json, os, sys

JSON_PATH = 'i18n/tools/content_deepdive.json'

DATA = {
 'calc-rater': {
  'title': '射击弹道与修正计算',
  'summary': '基于简化质点弹道模型，输入射击距离、初速、弹道系数、横风与风角、归零距离等，估算弹丸飞行时间、弹道降与横风偏移，换算瞄准修正量（MOA/密位），并按落点偏差折算靶环评分，辅助射击预习与弹道理解。',
  'scenarios': [
   '步枪精度预习：输入已知初速与弹道系数，按目标距离与归零距离预估弹道降，给出需抬高的密位/MOA 修正，帮助校枪前心中有数。',
   '横风修正：给定侧风风速与风角，估算横向偏移量并换算为风偏密位，实弹前做修正预案。',
   '靶环评分：按落点相对靶心偏差与靶环间距，折算命中环数，用于训练成绩快速估算。',
  ],
  'example': {'title': '300m 横风修正估算', 'body': '示例：距离 300m、初速 850m/s、BC 0.45、横风 3m/s 正横风（风角 90）、归零 100m、靶环间距 5cm。\n• 弹道降（相对归零）按简化模型估算，得需抬高的密位/MOA 修正\n• 横风偏移按风偏公式得横向偏差，再折算风偏密位\n• 落点偏差 8cm → 靶环评分 ≈ 中心 − 8÷5 ≈ 1.6 环\n（注：简化质点模型不含科里奥利、湿度、温度梯度等高阶项）'},
  'faqs': [
   {'q': '结果准吗？', 'a': '采用简化质点弹道模型，忽略气温、湿度、海拔、科里奥利力等，仅作预习量级参考；精确射击以实弹校枪为准。'},
   {'q': 'MOA 和密位怎么换？', 'a': '1 密位≈3.44 MOA，工具内统一换算；具体以所用瞄具分划为准。'},
   {'q': '能当训练评分依据吗？', 'a': '靶环评分为按偏差的折算估算，不替代正式考核计时与裁判；仅助理解落点与成绩关系。'},
  ],
 },
 'rater-38': {
  'title': '军事体育训练考核评分',
  'summary': '依据《军事体育训练大纲》参考标准，按性别与年龄段对引体向上、双杠臂屈伸、仰卧起坐、俯卧撑、3000米跑等单项成绩评分（0–100 分档），辅助军体考核自测与成绩记录。',
  'scenarios': [
   '单项目自测：选性别+年龄段+项目（如 3000米跑 13分30秒），查对应标准得单项分。',
   '多项汇总：逐项评分后按权重汇总体能总分，看是否达及格/良好/优秀线。',
   '阶段对比：训练前后两次成绩同屏对比，看进步幅度与薄弱项。',
  ],
  'example': {'title': '男 20–24 岁体能自测', 'body': '示例：男、20–24岁、3000米跑 13′30″、引体向上 12 个、仰卧起坐 70 个/分。\n• 按大纲参考标准各得单项分（如 3000米 85、引体 80、仰卧 90）\n• 按权重汇总体能总分，判达良好区间\n（注：标准依公开《军事体育训练大纲》参考值，具体以现役最新版本与单位细则为准）'},
  'faqs': [
   {'q': '标准按哪一版？', 'a': '参考公开《军事体育训练大纲》分年龄性别标准；现役最新版本与单位细则可能调整，请以官方为准。'},
   {'q': '分数怎么算？', 'a': '按各单项实测值映射到标准分档（通常 0–100），再按大纲权重汇总；具体权重以规定为准。'},
   {'q': '能替代正式考核吗？', 'a': '不能，仅作自测与记录参考；正式考核以单位组织计时与裁判结果为准。'},
  ],
 },
}

def main():
    if not os.path.exists(JSON_PATH):
        print('ERROR: %s 不存在' % JSON_PATH); sys.exit(1)
    d = json.load(open(JSON_PATH, encoding='utf-8'))
    cnt = 0; skip = 0
    for k, v in DATA.items():
        key = 'defense/' + k
        if key not in d:
            print('  WARN 未找到 key:', key); continue
        old = d[key]
        blob = ' '.join(old.get('scenarios', []))
        if old.get('summary') and '在defense场景下' not in blob:
            skip += 1; continue
        d[key] = {
            'summary': v['summary'],
            'scenarios': v['scenarios'],
            'examples': [{'title': v['example']['title'], 'body': v['example']['body']}],
            'faqs': v['faqs'],
        }
        cnt += 1
    json.dump(d, open(JSON_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('defense 真实化完成：更新 %d 个 key，跳过 %d 个（已真实）' % (cnt, skip))

if __name__ == '__main__':
    main()
