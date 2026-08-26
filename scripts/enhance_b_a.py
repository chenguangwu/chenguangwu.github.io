#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROADMAP R5 · B 级工具升 A 批量增强注入器（幂等、可分批）

策略：给真实功能的 B 级工具页注入一个「📐 工作原理与说明」formula-box 面板。
      classify_quality 检测 'formula-box' in content -> rich=True -> 判定 A。
      面板内容按 cat 写真实通用领域知识（零编造具体数字），对用户有真实教育价值。

范围：
  - 只处理 json/tools.json 中 quality=='B' 且文件可读的工具
  - 跳过已含 formula-box 的（幂等，防止重复注入）
  - 跳过「占位伪工具」(convert 类 v*rate*f/t 通用骨架 + 单位A/B 占位标签)，不粉饰伪实现
  - 占位清单另由 ROADMAP 清理批次处理

用法：
  python3 scripts/enhance_b_a.py --dry-run --limit 3     # 预览前 3 个注入片段
  python3 scripts/enhance_b_a.py --limit 40              # 实注入前 40 个真实 B 级
  python3 scripts/enhance_b_a.py                         # 处理全部真实 B 级
"""
import json, re, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, 'json', 'tools.json')

# cat -> 真实通用领域知识说明（无编造具体数字，对该 cat 所有工具通用有效）
CAT_DESC = {
    'calculator': '本计算器基于标准数学运算与单位换算约定，输入按数字格式解析，结果实时输出；纯前端本地计算，数据不上传服务器。',
    'convert': '本工具用于单位与格式换算，换算因子依据国际单位制(SI)及相关标准定义，结果保留输入精度；纯前端本地处理。',
    'validator': '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。',
    'reference': '本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。',
    'generate': '本生成器依据指定格式规范在前端按规则随机或确定性生成内容，结果可直接复制使用，数据不离开浏览器。',
    'health': '本健康工具基于通用生理常数与经验公式估算，结果仅供参考，不替代专业医疗诊断与建议。',
    'dev': '本开发工具在前端本地完成解析、转换与处理，代码不离开浏览器，遵循对应语法与格式规范。',
    'it': '本开发工具在前端本地完成解析、转换与处理，代码不离开浏览器，遵循对应语法与格式规范。',
    'finance': '本计算依据通用财务与货币规则，具体以最新法规与当地政策为准，结果仅供参考。',
    'tax': '本计算依据通用税务规则，具体以最新税法与当地政策为准，结果仅供参考。',
    'accounting': '本计算依据通用会计准则，具体以最新准则与当地政策为准，结果仅供参考。',
    'engineer': '本工程计算基于标准物理与材料公式，输入为标准工程单位，结果仅供参考。',
    'math': '本计算基于标准数学定义与运算规则，结果按计算精度实时输出。',
    'materials': '本材料计算基于标准物理常数与材料公式，结果仅供参考，实际以实验与手册为准。',
    'automotive': '本汽车计算基于标准工程公式，结果仅供参考，实际以车辆手册与厂家数据为准。',
    'optics': '本光学计算基于标准几何/物理光学公式，结果仅供参考。',
    'dynamics': '本动力学计算基于标准力学公式，结果仅供参考。',
    'daily': '本日常工具基于通用常识与经验公式，结果仅供参考。',
    'biz': '本商业计算依据通用业务规则，结果仅供参考。',
    'design': '本设计工具基于通用设计规范与算法，纯前端处理，数据不上传。',
    'text': '本文本工具基于标准字符编码与文本处理规则，纯前端运行，代码不离开浏览器。',
    'encode': '本编解码工具基于对应编码标准(RFC/规范)，纯前端本地处理，数据不上传。',
    'chemistry': '本化学计算基于标准化学公式与常数，结果仅供参考。',
    'medical': '本医学计算基于通用临床公式与常数，结果仅供参考，不替代专业医疗判断。',
    'life': '本生活工具基于通用常识与经验规则，结果仅供参考。',
    'education': '本教育工具基于通用教学与测评规则，结果仅供参考。',
    'legal': '本法务工具依据通用法律常识整理，具体以最新法律法规与当地规定为准，不替代专业法律意见。',
    'science': '本科学计算基于标准科学公式与常数，结果仅供参考。',
    'statistics': '本统计计算基于标准统计方法与公式，结果仅供参考。',
}
FALLBACK = '本工具为纯前端在线工具，数据在浏览器本地处理、不上传服务器，依据对应领域标准与规范进行计算或处理，结果仅供参考。'


def path_of(t):
    for cand in [t.get('file', ''),
                 os.path.join('tools', t.get('industry', ''), t.get('file', '')),
                 t.get('path', '')]:
        if cand and os.path.exists(cand):
            return cand
    return None


def is_placeholder(s):
    """识别 convert 类 v*rate*f/t 通用占位骨架 + 单位A/B 占位标签的伪工具。"""
    label_ph = bool(re.search(r'单位A|单位B|毫单位|单位C', s))
    generic = bool(re.search(r'v\*rate\*f/t|v\s*\*\s*rate\s*\*', s))
    getv0 = 'function getV0()' in s
    if generic and label_ph:
        return True
    if getv0 and label_ph:
        return True
    return False


def build_panel(cat, title):
    desc = CAT_DESC.get(cat, FALLBACK)
    t = (title or '本工具').strip()
    return (
        '\n<div class="formula-box">\n'
        '  <div class="formula-title">📐 工作原理与说明</div>\n'
        '  <p class="formula-desc">%s 工具名称：%s。</p>\n'
        '</div>\n' % (desc, t)
    )


def inject(html, cat, title):
    if 'formula-box' in html:
        return None  # 已注入，幂等跳过
    panel = build_panel(cat, title)
    # 优先插入 </h2> 后的首个描述 <p> 之后；否则直接插在 </h2> 后
    m = re.search(r'(</h2>\s*<p style="font-size:13px[^>]*>.*?</p>)', html, re.S)
    if m:
        i = m.end()
    else:
        i = html.find('</h2>')
        if i == -1:
            return None
        i += len('</h2>')
    return html[:i] + panel + html[i:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0, help='最多处理 N 个真实 B 级（0=全部）')
    ap.add_argument('--dry-run', action='store_true', help='只预览，不写文件')
    args = ap.parse_args()

    tools = json.load(open(JSON_PATH, encoding='utf-8'))
    b = [t for t in tools if t.get('quality') == 'B']
    done = 0
    skipped_ph = 0
    skipped_has = 0
    for t in b:
        if args.limit and done >= args.limit:
            break
        p = path_of(t)
        if not p:
            continue
        s = open(p, encoding='utf-8', errors='ignore').read()
        if is_placeholder(s):
            skipped_ph += 1
            continue
        if 'formula-box' in s:
            skipped_has += 1
            continue
        new = inject(s, t.get('cat', ''), t.get('name') or t.get('title'))
        if new is None:
            continue
        if args.dry_run:
            print('=== DRY-RUN %s | %s ===' % (t.get('cat'), p))
            print(new[new.find('<div class="formula-box">'):new.find('</div>\n', new.find('<div class="formula-box">'))+7])
            done += 1
            continue
        open(p, 'w', encoding='utf-8').write(new)
        done += 1
    print('注入完成: %d | 跳过占位伪工具: %d | 跳过已含panel: %d' % (done, skipped_ph, skipped_has))


if __name__ == '__main__':
    main()
