# -*- coding: utf-8 -*-
"""清理 dermatology A/B/C 三类硬编码套话。
A 类：assessor-14/rater-28/rater-29（错配"本校验工具…"）+ seborrheic-dermatitis/vss-scar
     （医疗通用"本健康工具…"）替换为真实领域 formula-desc；其余标准数学/速查变体语义相符保留。
B 类：chilblain-grading 的「工作与生活中的相关计算与查询」占位（JSON-LD FAQ + 旧 deep-dive dd）→ 真实场景。
C 类：assessor-14/rater-28/rater-29 的 tool-intro-body 块内 6 类通用套话（简介尾随/功能特点/使用场景）→ 真实内容。
"""
import re, sys, os

DRY = '--dry' in sys.argv

# ---------- A 类 formula-desc ----------
A_REPL = {
 'assessor-14': ('本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。',
                 '本工具按头皮与面部脂溢性皮炎的鳞屑、油腻、红斑与瘙痒表现进行严重程度分级，结果实时显示；纯前端评估，数据不上传服务器。'),
 'rater-28': ('本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。',
              '本工具按温哥华瘢痕量表(VSS)对瘢痕的血管性、色素、柔韧性、厚度及疼痛瘙痒进行分级评分，结果实时显示；纯前端评估，数据不上传服务器。'),
 'rater-29': ('本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。',
              '本工具按虫咬(皮炎)反应的红斑范围、水肿、丘疹水疱与瘙痒强度进行评分分级，结果实时显示；纯前端评估，数据不上传服务器。'),
 'seborrheic-dermatitis': ('本健康工具基于通用生理常数与经验公式估算，结果仅供参考，不替代专业医疗诊断与建议。',
              '本工具按脂溢性皮炎的受累部位、鳞屑与红斑程度、油腻及瘙痒进行严重度评估，结果实时显示；纯前端评估，数据不上传服务器。'),
 'vss-scar': ('本健康工具基于通用生理常数与经验公式估算，结果仅供参考，不替代专业医疗诊断与建议。',
              '本工具按温哥华瘢痕量表(VSS)对瘢痕的血管性、色素、柔韧性、厚度及疼痛瘙痒进行分级评分，结果实时显示；纯前端评估，数据不上传服务器。'),
}

# ---------- B 类 ----------
B_OLD = '工作与生活中的相关计算与查询'
B_NEW = '用于寒冷暴露后手指、足趾、耳廓等肢端冻疮的分度判断与保暖护理指导，帮助识别需就医的破溃坏死。'

# ---------- C 类 tool-intro-body ----------
JUNK_TAIL = '免费在线工具，纯前端处理，数据不上传，保护隐私安全。'
C_REPL = {
 'assessor-14': dict(
   intro_tail_strip='脂溢性皮炎（头皮屑）评估。',
   feat_replace=('操作简单，一键完成', '按头皮与面部鳞屑、油腻、红斑、瘙痒分级'),
   scenes=['头皮屑与脂溢性皮炎自我监测', '药用洗发剂使用频率参考', '疗效随访与护理调整', '就医前初步评估']),
 'rater-28': dict(
   intro_tail_strip='疤痕（VSS）温哥华评分。',
   feat_replace=('操作简单，一键完成', '按血管性/色素/柔韧性/厚度/疼痛瘙痒多维评分'),
   scenes=['瘢痕严重度客观量化', '激光注射等治疗前后随访', '烧伤或术后瘢痕评估', '就医前初步评级']),
 'rater-29': dict(
   intro_tail_strip='虫咬（皮炎）反应评分。',
   feat_replace=('操作简单，一键完成', '按红斑范围/水肿/丘疹水疱/瘙痒分级'),
   scenes=['虫咬皮炎反应分度', '居家护理与止痒指导', '过敏或感染预警', '就医前初步评估']),
}


def fix_a(n):
    p = 'tools/dermatology/%s.html' % n
    s = open(p, encoding='utf-8').read()
    old, new = A_REPL[n]
    if old not in s:
        return s, s, 'OLD未命中'
    new_s = s.replace(old, new, 1)
    return s, new_s, 'OK' if new_s != s else '无变化'


def fix_b(n):
    p = 'tools/dermatology/%s.html' % n
    s = open(p, encoding='utf-8').read()
    if B_OLD not in s:
        return s, s, 'OLD未命中'
    new_s = s.replace(B_OLD + '。', B_NEW + '。').replace(B_OLD, B_NEW)
    return s, new_s, 'OK' if new_s != s else '无变化'


def fix_c(n):
    p = 'tools/dermatology/%s.html' % n
    s = open(p, encoding='utf-8').read()
    r = C_REPL[n]
    new = s
    # 1) 简介尾随语
    pat_intro = re.compile(r'(<h4><span class="h4-icon">📝</span>工具简介</h4>\s*<p>' + re.escape(r['intro_tail_strip']) + r')' + re.escape(JUNK_TAIL))
    new = pat_intro.sub(lambda m: m.group(1), new)
    # 2) 功能特点
    new = new.replace('<li>%s</li>' % r['feat_replace'][0], '<li>%s</li>' % r['feat_replace'][1])
    # 3) 使用场景
    new = re.sub(r'(<ul class="intro-scenes">).*?(</ul>)',
                 lambda m: m.group(1) + ''.join('<li>%s</li>' % x for x in r['scenes']) + m.group(2),
                 new, flags=re.S)
    return s, new, 'OK' if new != s else '无变化'


def main():
    print('=== dermatology A/B/C 清理 ===')
    for n in A_REPL:
        _, after, st = fix_a(n)
        print('(A)[%s] %s 残留:%s' % (n, st, A_REPL[n][0][:10] in after))
    _, after_b, st_b = fix_b('chilblain-grading')
    print('(B)[chilblain-grading] %s 残留:%s' % (st_b, B_OLD in after_b))
    for n in C_REPL:
        _, after, st = fix_c(n)
        tail_left = JUNK_TAIL in after
        feat_left = C_REPL[n]['feat_replace'][0] in after
        print('(C)[%s] %s 尾随残留:%s 套话li残留:%s' % (n, st, tail_left, feat_left))
    if DRY:
        print('DRY 完成，未写入')
        return
    # 写入
    for n in A_REPL:
        _, after, _ = fix_a(n)
        open('tools/dermatology/%s.html' % n, 'w', encoding='utf-8').write(after)
    _, after_b, _ = fix_b('chilblain-grading')
    open('tools/dermatology/chilblain-grading.html', 'w', encoding='utf-8').write(after_b)
    for n in C_REPL:
        _, after, _ = fix_c(n)
        open('tools/dermatology/%s.html' % n, 'w', encoding='utf-8').write(after)
    print('写入完成')


if __name__ == '__main__':
    main()
