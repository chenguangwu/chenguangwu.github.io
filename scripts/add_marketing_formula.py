#!/usr/bin/env python3
"""marketing 分类 formula 补框：给 6 个计算类缺框页加 class="card formula-box" 公式说明。

用法: python3 scripts/add_marketing_formula.py [--apply]
公式文本取自各页真实计算逻辑；插入锚点按优先级自动匹配（tip-box / tabs / input-row 之前）。
"""
import os, re, sys

TOOLS = os.path.join(os.path.dirname(__file__), '..', 'tools', 'marketing')

FB_TPL = ('<div class="card formula-box">\n'
          '  <div class="formula-title">📐 计算方式</div>\n'
          '  <p>%s</p>\n'
          '</div>\n')

FORMULAS = {
  'ad-roi': '广告 ROI 模拟：CPC 模式 点击数=预算÷CPC、展示=点击÷CTR；CPM 模式 展示=预算÷CPM×1000、点击=展示×CTR。收入=点击×CVR×客单价，毛利=收入×(1−成本率)−固定成本，ROI=毛利÷预算。调整出价 / CTR / CVR 即可比较不同投放方案盈亏。',
  'calc-price-elasticity': '弧弹性（中点法）：需求变化率=(q2−q1)/[(q1+q2)/2]，价格变化率=(p2−p1)/[(p1+p2)/2]，Ed=需求变化率÷价格变化率（带符号）。|Ed|>1 富有弹性、<1 缺乏弹性；收入变化率=(p2×q2−p1×q1)/(p1×q1)，用于判断调价方向。',
  'cpc-calculator': 'CPC=花费÷点击；CPM=花费÷(展示÷1000)；CPA=花费÷转化。三者可相互换算：给定任意两项即可反推第三项与可购买的量，便于统一比较不同采买方式的单价。',
  'estimate-sample-size-confidence': 'Cochran 公式 n₀=z²·p(1−p)/e²（z 为置信水平对应分位数，e 为误差限度）；有限总体校正 n=n₀/(1+(n₀−1)/N)。预期比例 p 取 0.5 时样本量最大，已知更接近真实比例时可取更小值。',
  'marketing-roi': '营销 ROI=(收入−营销投入)÷营销投入；ROAS=收入÷广告投入。叠加复购时 总收入=首单转化量×客单价+复购量×客单价。多渠道可把自然流量与付费流量分别核算，避免高估或低估单渠道贡献。',
  'price-elasticity': '中点法弧弹性 Ed=(ΔQ/均价Q)÷(ΔP/均价P)。|Ed|>1 富有弹性（降价增收入）、<1 缺乏弹性（涨价增收入）、≈1 单位弹性。结果带符号，负号表示价格上升需求下降，符合常规需求规律。',
}

ANCHORS = [
  r'(<div class="tip-box")',
  r'(<div class="tabs")',
  r'(<div class="scale-row")',
  r'(<div class="set-row")',
  r'(<div[^>]*class="[^"]*tool-result[^"]*"[^>]*>)',
  r'(<div class="input-row")',
  r'(<div class="subject-row")',
]


def add_one(slug, apply):
    fp = os.path.join(TOOLS, slug + '.html')
    s = open(fp, encoding='utf-8').read()
    if 'class="formula-box"' in s:
        print('  skip %s (已有框)' % slug)
        return False
    if slug not in FORMULAS:
        print('  skip %s (无公式定义)' % slug)
        return False
    fb = FB_TPL % FORMULAS[slug]
    used = None
    for pat in ANCHORS:
        m = re.search(pat, s)
        if m:
            used = pat
            s2 = s[:m.start()] + fb + s[m.start():]
            break
    if used is None:
        print('  WARN %s (无可用锚点)' % slug)
        return False
    if apply:
        open(fp, 'w', encoding='utf-8').write(s2)
    print('  + %s (锚点:%s%s)' % (slug, used, ' [已写]' if apply else ''))
    return True


def main():
    apply = '--apply' in sys.argv
    n = 0
    for slug in FORMULAS:
        if add_one(slug, apply):
            n += 1
    print('==== %s %d 页 ====' % ('已应用' if apply else '预演', n))


if __name__ == '__main__':
    main()
