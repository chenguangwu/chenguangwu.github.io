#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agriculture (63) 分类 deep-dive 补齐：3 个空条页面写入完整内容达 §4.5。

未达标 3 页（2026-09-13 审计，scenarios=0/faqs=0/examples=0，全空）：
  cycle-honey / detector-13 / detector-nutrition（蜂业相关，三端亦缺中文名/简介）
标准：scenarios ≥2 且 examples ≥1 且 faqs ≥2 且 无套话。
内容逐条对照页面功能与实现撰写。文件格式 indent=1（与源一致，零格式 churn）。

用法：
  python3 scripts/fill_agriculture_deepdive.py --dry-run
  python3 scripts/fill_agriculture_deepdive.py --apply
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CD = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

ENTRIES = {
    'agriculture/cycle-honey': {
        'title': '采蜜期（摇蜜周期）安排',
        'scenarios': [
            '按蜂箱登记流蜜周期（7~14 天）与起始日期，推算每个蜂箱的下次摇蜜（取蜜）日期。',
            '多箱排期：汇总各箱摇蜜日生成日历，协调人手与摇蜜机，避免同一天多箱挤占。',
            '跟踪取蜜记录与产量，按箱统计累计取蜜量，评估蜜源期供给与蜂群产能。',
        ],
        'examples': [
            {
                'title': '荆条花期单箱摇蜜排期',
                'body': '5 月 20 日入场，流蜜周期设 10 天，则下次摇蜜为 5 月 30 日，依次递推 6 月 9 日、6 月 19 日。'
                        '若封盖率不足，人工延后 2~3 天再取，避免取到未成熟蜜导致发酵。',
            },
        ],
        'faqs': [
            {
                'q': '流蜜周期设几天合适？',
                'a': '以蜜源植物泌蜜节奏与封盖情况为准，常见 7~14 天。大流蜜期宜偏短（7~10 天），零星蜜源可偏长；'
                     '工具要求落在 7~14 天区间内。',
            },
            {
                'q': '为什么要按箱分别排期？',
                'a': '各箱群势、王龄、入场时间不同，泌蜜与封盖进度并不一致。按箱排期可避免「一刀切」，'
                     '减少取未熟蜜与伤子的风险。',
            },
            {
                'q': '数据会保存到服务器吗？',
                'a': '蜂箱与取蜜记录存于浏览器本地存储（localStorage），不上传服务器；清除浏览器数据会一并清空。'
                     '建议定期把取蜜记录另存备份。',
            },
        ],
    },
    'agriculture/detector-13': {
        'title': '蜂螨（寄生率）检测',
        'scenarios': [
            '按糖粉摇落法或酒精冲洗法采集样本工蜂，统计检出螨数并计算寄生率。',
            '对比不同蜂群、不同时期的寄生率，判断是否达到需要治螨的阈值。',
        ],
        'examples': [
            {
                'title': '酒精冲洗法测定寄生率',
                'body': '取 300 只工蜂样本，冲洗检出蜂螨 9 只，寄生率 = 9 ÷ 300 × 100% = 3.0%，'
                        '已超过 2%~3% 的防治参考线，建议结合群势与季节安排治螨。',
            },
        ],
        'faqs': [
            {
                'q': '采样多少只工蜂比较准？',
                'a': '常用 200~300 只工蜂，样本越大估算越稳定。建议多点取样（子脾边角与外勤蜂），'
                     '避免用单一位置代表整群。',
            },
            {
                'q': '寄生率多少需要治螨？',
                'a': '成年蜂寄生率一般超过 2%~3%，或巢房检出率明显上升时即需安排防治；'
                     '还需结合群势、蜜源期与封盖情况综合判断，避免流蜜期用药污染蜂蜜。',
            },
            {
                'q': '检测时要注意什么？',
                'a': '不同方法（糖粉、酒精、CO₂ 麻醉）测得的效率不同，应固定同一方法做纵向对比；'
                     '检测后及时还蜂，避免低温时段操作造成蜂群损失。',
            },
        ],
    },
    'agriculture/detector-nutrition': {
        'title': '花粉（发酵）全营养检测',
        'scenarios': [
            '录入（发酵）蜂花粉的蛋白质、脂肪、还原糖、水分、灰分与乳酸含量，逐项判级。',
            '按合格项与达优项数量评定综合等级，辅助原料收购定价与发酵工艺改进。',
        ],
        'examples': [
            {
                'title': '一批发酵花粉评级',
                'body': '蛋白质 18%、脂肪 4%、还原糖 16%、水分 7%、灰分 3.5%、乳酸 1.2%：'
                        '蛋白质、还原糖、乳酸达标，脂肪落在 1%~7% 适宜区间，水分 ≤8%、灰分 ≤4%，'
                        '6 项全部合格且蛋白质、还原糖达优，综合评为一级。',
            },
        ],
        'faqs': [
            {
                'q': '为什么要检测乳酸？',
                'a': '乳酸是蜂花粉发酵程度的指标：含量升高说明发酵较充分、更易消化吸收；'
                     '过低表示发酵不足，过高则可能已酸败，需结合气味与外观判断。',
            },
            {
                'q': '水分和灰分为什么越低越好？',
                'a': '水分高易霉变、缩短保质期；灰分高说明泥沙等杂质多。两者属「越低越好」型指标，'
                     '超过标准即判不合格，用于快速筛查原料洁净度与干燥程度。',
            },
            {
                'q': '综合等级是怎么定的？',
                'a': '按 6 项指标的合格数与达优数分级：达优 ≥5 项为特级；合格 ≥5 项为一级；'
                     '合格 ≥4 项为二级；否则为不合格。等级结果仅供参考，实际收购还需结合产地与检测报告。',
            },
        ],
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    raw = open(CD, encoding='utf-8').read()
    data = json.loads(raw)

    added = updated = 0
    for k, v in ENTRIES.items():
        cur = data.get(k)
        if cur is None:
            added += 1
            print('  + 新增', k, '| scenarios=%d examples=%d faqs=%d'
                  % (len(v['scenarios']), len(v['examples']), len(v['faqs'])))
        else:
            updated += 1
            print('  ~ 覆盖', k, '| 旧 scenarios=%d examples=%d faqs=%d'
                  % (len(cur.get('scenarios') or []), len(cur.get('examples') or []), len(cur.get('faqs') or [])))
        data[k] = v

    print('\n新增 %d / 覆盖 %d' % (added, updated))
    if a.dry_run:
        print('[dry-run] 未写盘')
        return 0
    out = json.dumps(data, ensure_ascii=False, indent=1)
    if raw.endswith('\n'):
        out += '\n'
    open(CD, 'w', encoding='utf-8').write(out)
    print('已写盘:', CD)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
