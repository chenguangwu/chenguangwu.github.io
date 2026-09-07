# -*- coding: utf-8 -*-
"""清理 domestic 2 页 tool-intro-body 块内 6 类通用套话（C 类）。
A 类 FD 为生成器标准变体（语义相符）保留；B 类 opt 套话「工作与生活中的相关计算与查询」0 命中。
"""
import re, sys, os

DRY = '--dry' in sys.argv

# 简介尾随通用语（含全站真实特性「纯前端处理/数据不上传」，但作为旧模板尾随套话整体清除，真实特性在功能特点 li 保留）
JUNK_TAIL = '免费在线工具，纯前端处理，数据不上传，保护隐私安全。'

# 各页真实替换文本
REPL = {
 'generator-price': dict(
   intro_tail_strip='合同（服务/价格/条款）生成。',  # 保留前缀
   feat_replace=('操作简单，一键完成', '按服务内容、价格与关键条款生成规范合同草稿'),
   scenes=['家政与劳务协议快速起草', '服务范围与价格条款固化留存', '多版本合同方案比对', '合同草稿复制存档']),
 'recommender-8': dict(
   intro_tail_strip='保险（责任/意外/雇主）推荐。',
   feat_replace=('操作简单，一键完成', '按企业规模与用工类型推荐险种组合'),
   scenes=['雇主责任险保额初筛', '意外险与责任险组合比对', '投保方案内部讨论', '保障要点清单导出']),
}

# 保留的真实功能特点（不删）
KEEP_FEATS = ['纯前端处理，数据不上传服务器', '支持复制和下载结果', '实时显示结果，所见即所得']

# B 类检测
OPT = '工作与生活中的相关计算与查询。'
# A 类生成器变体（语义相符，保留不处理）
FD_KEEP = '本生成器依据指定格式规范在前端按规则随机或确定性生成内容'

def fix_page(n):
    p = 'tools/domestic/%s.html' % n
    s = open(p, encoding='utf-8').read()
    r = REPL[n]
    new = s
    # 1) 简介尾随语：把「<真实前缀>JUNK_TAIL」改为「<真实前缀>」
    pat_intro = re.compile(r'(<h4><span class="h4-icon">📝</span>工具简介</h4>\s*<p>' + re.escape(r['intro_tail_strip']) + r')' + re.escape(JUNK_TAIL))
    new = pat_intro.sub(lambda m: m.group(1), new)
    # 2) 功能特点：替换套话 li 为真实功能
    new = new.replace('<li>%s</li>' % r['feat_replace'][0], '<li>%s</li>' % r['feat_replace'][1])
    # 3) 使用场景：整段替换 4 项通用为真实场景
    new = re.sub(r'(<h4><span class="h4-icon">🎯</span>使用场景</h4>\s*<ul class="intro-scenes">).*?(</ul>)',
                 lambda m: m.group(1) + ''.join('<li>%s</li>' % x for x in r['scenes']) + m.group(2),
                 new, flags=re.S)
    if DRY:
        return s, new
    open(p, 'w', encoding='utf-8').write(new)
    return s, new

def main():
    print('=== domestic 三类检测/清理 ===')
    # A 类：生成器变体语义相符，仅报告
    a_files = [f for f in os.listdir('tools/domestic') if f.endswith('.html') and f != 'index.html']
    a_hit = [f[:-5] for f in a_files if FD_KEEP in open('tools/domestic/%s' % f, encoding='utf-8').read()]
    print('(A) 生成器 FD 语义相符(保留):', a_hit if a_hit else '无')
    # B 类
    b_hit = [f[:-5] for f in a_files if OPT in open('tools/domestic/%s' % f, encoding='utf-8').read()]
    print('(B) opt 套话命中:', b_hit if b_hit else '无')
    # C 类清理
    for n in REPL:
        before, after = fix_page(n)
        tail_left = JUNK_TAIL in after
        feat_left = REPL[n]['feat_replace'][0] in after
        scenes_left = '日常办公与学习' in after
        print('(C)[%s] 尾随语残留:%s 套话li残留:%s 通用场景残留:%s' % (n, tail_left, feat_left, scenes_left))
    print('完成' if not DRY else 'DRY完成')

if __name__ == '__main__':
    main()
