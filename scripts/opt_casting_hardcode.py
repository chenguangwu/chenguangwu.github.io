#!/usr/bin/env python3
"""清理 casting 硬编码套话（detector-24 formula-desc + opt-guide/opt-faq；analysis-36 tool-intro）。

范围判定（基于抽样读页）：
- analysis-36: formula-desc 已真实(保留); tool-intro 功能特点/使用场景为通用科学套话,需清;
              tool-intro 工具简介块与注意事项(隐私声明)已真实,保留。
- detector-24: formula-desc 占位(本校验工具依据...)需清; tool-intro 已真实(保留);
              opt-guide/opt-faq 的「工作与生活中的相关计算与查询」套话需清(JSON-LD+opt-guide<p>+opt-faq<dd>三处)。
"""
import re, sys

PLACEHOLDER = '工作与生活中的相关计算与查询。'

# analysis-36 tool-intro 真实替换
ANALYSIS_FEATURES = '''      <li>缺陷数据描述统计：均值、标准差、极差一键算出</li>
      <li>工艺稳定性评估：缺陷率与控制界限辅助判定批次合格性</li>
      <li>批次缺陷溯源：按浇道、型腔定位高发位置</li>
      <li>本地处理：数据不出浏览器，保护工艺机密</li>'''
ANALYSIS_SCENES = '''      <li>气孔缺陷率统计：批量抽检评估工艺稳定性</li>
      <li>缩松评级复核：厚大断面缩松面积占比判定</li>
      <li>夹渣缺陷溯源：批次夹渣位置与尺寸分析</li>
      <li>质量改进参考：为补缩、冷铁与浇注系统优化提供依据</li>'''

# detector-24 formula-desc 真实说明
DETECTOR_FORMULA = ('<p class="formula-desc">依据 GB/T 3323（射线）、GB/T 11345（超声焊缝）、'
                    'GB/T 9443（渗透）等国家标准，对输入的探伤方法、缺陷长度、母材厚度等参数'
                    '进行质量等级评定；原理为缺陷尺寸与板厚比对照等级限值，结果实时输出。'
                    '纯前端本地计算，数据不出浏览器。</p>')


def build_guide_scene():
    import json
    d = json.load(open('i18n/tools/content_deepdive.json', encoding='utf-8'))
    sc = d['casting/detector-24'].get('scenarios', [])[:2]
    return '；'.join(s.strip().rstrip('。') for s in sc) + '。'


def process_analysis(dry):
    f = 'tools/casting/analysis-36.html'
    s = open(f, encoding='utf-8').read()
    s2 = re.sub(r'<ul class="intro-features">.*?</ul>',
                f'<ul class="intro-features">\n{ANALYSIS_FEATURES}\n    </ul>', s, flags=re.S)
    s2 = re.sub(r'<ul class="intro-scenes">.*?</ul>',
                f'<ul class="intro-scenes">\n{ANALYSIS_SCENES}\n    </ul>', s2, flags=re.S)
    if dry:
        print(f'[dry] analysis-36: features/scenes 套话替换 {int(s2!=s)} 处')
        return
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2)
        print('[ok] analysis-36: tool-intro 功能特点/使用场景套话已清')


def process_detector(dry):
    f = 'tools/casting/detector-24.html'
    s = open(f, encoding='utf-8').read()
    scene = build_guide_scene()
    # formula-desc 占位
    s2 = re.sub(r'<p class="formula-desc">本校验工具依据对应数据格式与语法规范[^<]*</p>',
                DETECTOR_FORMULA, s)
    n_formula = s.count('本校验工具依据对应数据格式与语法规范')
    # opt-guide <p> 套话
    s2 = s2.replace(f'<p>{PLACEHOLDER}</p>', f'<p>{scene}</p>')
    # JSON-LD FAQ 套话
    s2 = s2.replace(f'"text": "{PLACEHOLDER}"', f'"text": "{scene}"')
    # opt-faq <dd> 套话
    s2 = s2.replace(f'<dd>{PLACEHOLDER}</dd>', f'<dd>{scene}</dd>')
    n_opt = s.count(f'<p>{PLACEHOLDER}</p>')
    n_json = s.count(f'"text": "{PLACEHOLDER}"')
    n_dd = s.count(f'<dd>{PLACEHOLDER}</dd>')
    if dry:
        print(f'[dry] detector-24: formula-desc {n_formula} + opt-guide {n_opt} + JSON-LD {n_json} + opt-faq {n_dd} -> 场景: {scene[:36]}...')
        return
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2)
        print(f'[ok] detector-24: 清 formula-desc {n_formula} + opt-guide {n_opt} + JSON-LD {n_json} + opt-faq {n_dd} 处套话')
    else:
        print('[skip] detector-24: 未匹配')


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    process_analysis(dry)
    process_detector(dry)
