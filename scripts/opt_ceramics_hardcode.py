#!/usr/bin/env python3
"""清理 ceramics 硬编码套话（formula-desc + tool-intro + opt-guide/opt-faq）。

范围判定（基于抽样读页）：
- 5 页 tool-intro 全套话：工具简介块误标「商业办公领域」+ 功能特点/使用场景通用科学套话，需全清为真实陶艺内容。
- formula-desc 占位仅 glaze-temp/kiln-firing：「本速查内容依据权威标准与公开资料整理…商业办公领域的在线工具」→ 真实陶艺说明，并修正「商业办公」为「陶瓷」。clay-shrinkage/glaze-ratio/wheel-speed 无 formula-desc 块。
- opt-guide/opt-faq 套话仅 glaze-ratio/kiln-firing：「工作与生活中的相关计算与查询」（JSON-LD + opt-guide <p> + opt-faq <dd> 三处）。
"""
import re, sys, json

PLACEHOLDER = '工作与生活中的相关计算与查询。'

# tool-intro 通用真实功能特点
FEATURES = '''      <li>陶瓷参数一键换算：收缩率、配比、温度、转速实时得出</li>
      <li>本地计算：数据不出浏览器，保护配方与工艺机密</li>
      <li>结果可复制导出：便于记录与复烧对照</li>
      <li>适配多种泥料与釉方：陶、炻、瓷均可用</li>'''

# 每页工具简介（真实陶瓷说明）与真实使用场景（取 content_deepdive scenarios）
INTRO = {
    'clay-shrinkage': {
        'brief': '泥料收缩率计算是一款面向陶艺与作坊的在线工具，按干燥与烧成尺寸计算收缩率并辅助坯体放尺，纯前端处理，数据本地计算保护隐私。',
        'scenes': ['坯体放尺设计：按总收缩率反推湿坯尺寸', '收缩率异常排查：批次波动预警开裂风险', '练泥与陈腐工艺评估：稳定出品率', '教学与试烧校样：快速换算参考'],
    },
    'glaze-ratio': {
        'brief': '釉料配比计算是一款面向陶艺与作坊的在线工具，按釉式百分比计算各原料称量并估算调浆加水量，纯前端处理，数据本地计算保护隐私。',
        'scenes': ['基础釉称量：按配方百分比算各原料克重', '水釉比估算：浸釉/淋釉/喷釉加水量', '小样缩放：大配方反推试烧小样', '色釉复配：保持比例验证呈色'],
    },
    'glaze-temp': {
        'brief': '釉料温度对照是一款面向陶艺与作坊的在线工具，给出低温/中温/高温釉推荐烧成区间并辅助坯釉匹配，纯前端处理，数据本地计算保护隐私。',
        'scenes': ['釉料烧成温度查对：避免过烧或欠烧', '坯釉匹配：减少剥釉与龟裂', '窑温均匀性核对：修正上下温差色差', '测温锥对照：判读实际窑温'],
    },
    'kiln-firing': {
        'brief': '窑炉烧成曲线是一款面向陶艺与作坊的在线工具，按坯体/釉料类型给出升温、保温与冷却曲线并估算总时长，纯前端处理，数据本地计算保护隐私。',
        'scenes': ['氧化焰烧成曲线：排胶排水与釉烧保温', '还原焰（瓷）曲线：还原时机与氧化保温', '素烧与釉烧分段：提升成品率', '升降温速率规划：防惊裂与变形'],
    },
    'wheel-speed': {
        'brief': '拉坯转速计算是一款面向陶艺与作坊的在线工具，按器型与阶段给出拉坯机推荐转速，纯前端处理，数据本地计算保护隐私。',
        'scenes': ['开坯定中心：低速稳妥找正', '提拉成型：中速拉高筒身', '修口收尾：精修口沿与圆润', '新手练手：从低速起步稳手感'],
    },
}

# formula-desc 真实说明（含领域修正）
FORMULA = {
    'glaze-temp': ('<p class="formula-desc">依据陶瓷烧成工艺，给出低温（约 900–1050℃）、中温（约 1100–1200℃）、'
                   '高温（约 1200–1300℃）釉的推荐烧成温度区间，并提示过烧流淌与欠烧无光的风险；'
                   '具体以釉方与测温锥为准。纯前端本地计算，数据不出浏览器。</p>'),
    'kiln-firing': ('<p class="formula-desc">依据坯体/釉料类型给出升温速率、保温温度与保温时间，'
                    '估算总烧成时长（含氧化焰、还原焰与素烧/釉烧分段）；原理为升温曲线积分与保温平衡。'
                    '纯前端本地计算，数据不出浏览器。</p>'),
}


def build_guide_scene(slug):
    d = json.load(open('i18n/tools/content_deepdive.json', encoding='utf-8'))
    sc = d[f'ceramics/{slug}'].get('scenarios', [])[:2]
    return '；'.join(s.strip().rstrip('。') for s in sc) + '。'


def process_page(slug, dry):
    f = f'tools/ceramics/{slug}.html'
    s = open(f, encoding='utf-8').read()
    cfg = INTRO[slug]
    brief = cfg['brief']
    scenes = '\n'.join(f'      <li>{x}</li>' for x in cfg['scenes'])
    # 工具简介块
    s2 = re.sub(r'<h4><span class="h4-icon">📝</span>工具简介</h4>\s*<p>.*?</p>',
                f'<h4><span class="h4-icon">📝</span>工具简介</h4>\n    <p>{brief}</p>', s, flags=re.S)
    # features / scenes ul
    s2 = re.sub(r'<ul class="intro-features">.*?</ul>',
                f'<ul class="intro-features">\n{FEATURES}\n    </ul>', s2, flags=re.S)
    s2 = re.sub(r'<ul class="intro-scenes">.*?</ul>',
                f'<ul class="intro-scenes">\n{scenes}\n    </ul>', s2, flags=re.S)
    # formula-desc
    if slug in FORMULA:
        s2 = re.sub(r'<p class="formula-desc">本速查内容依据权威标准与公开资料[^<]*</p>', FORMULA[slug], s2)
    # opt-guide/opt-faq 套话（三处）
    if PLACEHOLDER[:-1] in s2 or f'<p>{PLACEHOLDER}</p>' in s2:
        scene = build_guide_scene(slug)
        s2 = s2.replace(f'<p>{PLACEHOLDER}</p>', f'<p>{scene}</p>')
        s2 = s2.replace(f'"text": "{PLACEHOLDER}"', f'"text": "{scene}"')
        s2 = s2.replace(f'<dd>{PLACEHOLDER}</dd>', f'<dd>{scene}</dd>')
    n_opt = s.count(f'<p>{PLACEHOLDER}</p>')
    n_json = s.count(f'"text": "{PLACEHOLDER}"')
    n_dd = s.count(f'<dd>{PLACEHOLDER}</dd>')
    n_formula = s.count('本速查内容依据权威标准与公开资料')
    if dry:
        print(f'[dry] {slug}: intro {int(s2!=s)} + formula-desc {n_formula} + opt {n_opt}/{n_json}/{n_dd}')
        return
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2)
        print(f'[ok] {slug}: tool-intro 套话清 + formula-desc {n_formula} + opt {n_opt}/{n_json}/{n_dd}')
    else:
        print(f'[skip] {slug}: 无变化')


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    for slug in INTRO:
        process_page(slug, dry)
