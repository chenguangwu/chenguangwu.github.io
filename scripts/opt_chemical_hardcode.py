#!/usr/bin/env python3
"""清理 chemical 硬编码套话（formula-desc + tool-intro，无 opt-guide 区块）。

范围判定（基于逐页提取 tool-intro + formula-desc 全文）：
- 10 页 tool-intro 全套话：工具简介块误标「化工材料工具，帮助计算化学配方与参数」（或「X是一款化工材料领域的在线工具。化工材料工具…」）+ 功能特点/使用场景通用科学套话，需全清为真实内容。
  套话页：analysis-cost-7 / calc-pipeline-pressure-drop / convert-capacity-tank / convert-density-crude / miaomu-guige-zhiliang-yanshou-biaozhun / mixture-ratio / molar-mass / ph-calculator / reaction-yield / solution-concentration
  已真实保留（不动）：checker-15（化工质量体系自查）、detector-39（化工产品纯度，滴定/重量法）
- formula-desc 占位仅 2 页（标准占位模板）：
  analysis-cost-7 = 本计算依据通用财务与货币规则 → 真实预算成本说明
  molar-mass       = 本工程计算基于标准物理与材料公式 → 真实摩尔质量说明（IUPAC 原子量）
  其余 formula-desc 已真实（calc-pipeline-pressure-drop/checker-15/convert-capacity-tank/convert-density-crude/miaomu 的「输入两个参数…」/SI 说明）保留。
- 12 页均 [opt区块]: 无 → 无 opt-guide/opt-faq 套话，不需清理。
"""
import re, sys, json

# tool-intro 通用真实功能特点（化工/苗木均适用）
FEATURES = '''      <li>规格/参数一键换算：按公式实时得出结果</li>
      <li>本地计算：数据不出浏览器，保护业务数据</li>
      <li>结果可复制导出：便于记录与复核</li>
      <li>支持常用单位切换：减少人工换算误差</li>'''

# 每页工具简介（真实说明）与真实使用场景（取 content_deepdive scenarios）
INTRO = {
    'analysis-cost-7': {
        'brief': '面向化工企业的预算（成本/控制/优化）分析工具：按装置投资、生产成本与工艺方案做成本测算与偏差分析，辅助预算编制与降本决策。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['装置投资预算编制：汇总分项估算形成总投资', '生产成本控制与偏差分析：定位超支环节', '工艺优化方案成本对比：筛选更优路线', '预算与立项报告附证：快速测算支撑比选'],
    },
    'calc-pipeline-pressure-drop': {
        'brief': '管道沿程压降计算工具：基于达西–魏斯巴赫公式估算沿程阻力损失，辅助泵选型与管网设计。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['厂区输料管道沿程阻力核算', '泵选型扬程余量评估', '管网改造压降对比', '雷诺数流态判定'],
    },
    'convert-capacity-tank': {
        'brief': '储罐容量与液位换算工具：按罐型由液位高度反算容积或反之，辅助库存盘点与安全液位管理。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['液位→体积盘点：收发存核对', '收发作业目标液位核算', '安全液位红线设定', '卧式/立式罐型适配'],
    },
    'convert-density-crude': {
        'brief': '原油 API 度与密度换算工具：按标准公式互算并判定轻/重质油，辅助贸易计量与炼化配料。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['API 度↔密度互算', '轻/重质油分类判定', '贸易计量密度温度校正', '计价与加工路线参考'],
    },
    'miaomu-guige-zhiliang-yanshou-biaozhun': {
        'brief': '苗木（规格/质量/验收）标准工具：按地径、胸径、苗高与冠幅核查规格等级，辅助出圃检验与绿化工程验收。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['规格等级核查：匹配设计要求', '出圃质量判定：根系与病虫害', '绿化工程验收：逐株核规格', '不达标株整改计量'],
    },
    'mixture-ratio': {
        'brief': '混合配比计算工具：按比例换算各组分投料量，支持多元配料与溶液配制，辅助配方复配与小试。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['多元配料质量比换算', '溶液配制体积比', '反应物料配比核算', '小试配方缩放'],
    },
    'molar-mass': {
        'brief': '摩尔质量计算工具：按化学式解析原子量求和得到摩尔质量，支持水合物与常见离子，辅助溶液配制与反应计量。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['化学式摩尔质量解析', '溶液配制物质的量换算', '反应计量比核算', '水合物与括号处理'],
    },
    'ph-calculator': {
        'brief': 'pH/pOH 计算工具：按浓度换算酸碱度并支持缓冲体系估算，辅助水质与工艺调控。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['强酸/强碱 pH 换算', '缓冲溶液 pH 估算', '工艺水合规阈值判定', '稀释对 pH 的影响'],
    },
    'reaction-yield': {
        'brief': '反应产率计算工具：按理论产量与实际产量核算收率并支持多步总收率分析，辅助工艺优化。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['理论产量计算', '实际产率核算', '收率偏低环节排查', '多步反应总收率'],
    },
    'solution-concentration': {
        'brief': '溶液浓度换算工具：在质量分数、物质的量浓度、ppm/mg·L 间互算并支持稀释配制，辅助化验与投料。纯前端处理，数据本地计算保护隐私。',
        'scenes': ['质量分数↔物质的量浓度', 'ppm 与 mg/L 换算', '稀释配制加水量核算', '浓酸稀释安全提示'],
    },
}

# formula-desc 真实说明（仅标准占位 2 页）
FORMULA = {
    'analysis-cost-7': ('<p class="formula-desc">依据化工企业成本管理常用口径，按投资、原料、能耗、人工与制造费用分项测算并汇总，'
                        '结果随口径与价格假设变化；正式预算以内部核算制度与最新税法为准。纯前端本地计算，数据不出浏览器。</p>'),
    'molar-mass': ('<p class="formula-desc">依据 IUPAC 相对原子质量，按化学式各元素原子量求和得到摩尔质量（g/mol），'
                   '支持带括号水合物与常见离子；原子量以标准值计，结果可用于溶液配制与反应计量参考。纯前端本地计算，数据不出浏览器。</p>'),
}


def main():
    dry = '--dry' in sys.argv
    for slug, cfg in INTRO.items():
        f = f'tools/chemical/{slug}.html'
        s = open(f, encoding='utf-8').read()
        brief = cfg['brief']
        scenes = '\n'.join(f'      <li>{x}</li>' for x in cfg['scenes'])
        s2 = re.sub(r'<h4><span class="h4-icon">📝</span>工具简介</h4>\s*<p>.*?</p>',
                    f'<h4><span class="h4-icon">📝</span>工具简介</h4>\n    <p>{brief}</p>', s, flags=re.S)
        s2 = re.sub(r'<ul class="intro-features">.*?</ul>',
                    f'<ul class="intro-features">\n{FEATURES}\n    </ul>', s2, flags=re.S)
        s2 = re.sub(r'<ul class="intro-scenes">.*?</ul>',
                    f'<ul class="intro-scenes">\n{scenes}\n    </ul>', s2, flags=re.S)
        n_formula = 0
        if slug in FORMULA:
            for pat in [r'<p class="formula-desc">本计算依据通用财务与货币规则[^<]*</p>',
                        r'<p class="formula-desc">本工程计算基于标准物理与材料公式[^<]*</p>']:
                if re.search(pat, s2):
                    s2 = re.sub(pat, FORMULA[slug], s2)
                    n_formula += 1
        if dry:
            print(f'[dry] {slug}: intro {int(s2!=s)} + formula-desc {n_formula}')
            continue
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
            print(f'[ok] {slug}: tool-intro 套话清 + formula-desc {n_formula}')
        else:
            print(f'[skip] {slug}: 无变化')


if __name__ == '__main__':
    main()
