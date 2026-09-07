#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 discipline 分类硬编码套话（A 类 FD 错配 + C 类块内 6 类通用套话）。

A 类：assessor-risk-7 / tester-training-hr / assessor-28 挂「本校验工具依据对应数据格式
与语法规范进行合法性检查…」校验变体，实际是廉政/纪律/政治生态评估类，非数据格式校验，
属错配 → 替换为真实描述，保留「工具名称：」后缀与「纯前端运行，数据不离开浏览器。」真实特性。
stats-analysis 无 formula-desc，A 类不涉及。

C 类：4 页 tool-intro-body 块内 6 类通用套话全中（简介尾随语 + 功能特点 1 项 + 使用场景 4 项），
→ 替换为真实党建纪检场景文本，保留「纯前端处理/数据不上传」真实特性。

B 类 opt 套话「工作与生活中的相关计算与查询」：0 命中，跳过。

用法：默认正式替换；--dry 仅打印命中数与样例。
"""
import os, re, json, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A 类 FD 错配替换（仅替换校验变体前缀，保留工具名称后缀与纯前端真实特性句）
FD_OLD_PREFIX = '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；'
FD_NEW = {
    'assessor-risk-7': '廉政风险评估器依据纪法要求，对 5 个维度的风险识别项量化评分，输出风险等级与防控重点；',
    'tester-training-hr': '纪律教育测试题库依据纪律教育学习要点设题，作答后自动判分并给出解析；',
    'assessor-28': '政治生态画像评估器依据政治生态分析通用维度（每项 1-5 分）量化评分，构建画像并输出总分与风险等级；',
}
# C 类块内：每页真实文本
C_INTRO_TAIL = '免费在线工具，纯前端处理，数据不上传，保护隐私安全。'  # 简介尾随套话
C_FEATURE_JUNK = '操作简单，一键完成'  # 功能特点套话
C_SCENES_OLD = ['日常办公与学习', '开发调试与数据处理', '快速计算与格式转换', '信息查询与参考']
C_TEXT = {
    'assessor-risk-7': dict(
        intro_new='廉政（风险/防控/评估）体系。按 5 个维度风险识别项量化评分，输出风险等级与防控重点，用于纪检风险排查。',
        feature_new='按统一维度评分，结果可导出复核',
        scenes=['岗位廉政风险排查与自查自纠', '专项监督前的风险排序与资源安排', '年度防控清单动态更新与台账管理', '巡察考核前的自我测评与短板定位']),
    'tester-training-hr': dict(
        intro_new='纪律（教育/培训/测试）题库。提供纪律教育测试题，作答后自动判分并给出解析，用于廉政教育培训随堂测验。',
        feature_new='答完即时判分并附条款解析',
        scenes=['廉政教育培训尾声的随堂测验', '新入职或新提任人员纪律常识摸底', '支部集中学习后的前后测对比', '上岗前纪律教育效果检验']),
    'assessor-28': dict(
        intro_new='政治（生态/画像/评估）模型。按 6 个维度（每项 1-5 分）录入评分，构建政治生态画像并输出总分与风险等级。',
        feature_new='六维度统一口径，横向可比',
        scenes=['单位年度政治生态分析', '巡察或考核前的自我测评', '多部门政治生态横向对比', '整改成效的动态跟踪评估']),
    'stats-analysis': dict(
        intro_new='监督（四种形态/统计）分析。按监督执纪四种形态录入线索与处置，统计各层级占比与趋势，生成汇总表。',
        feature_new='按形态口径汇总，自动出占比',
        scenes=['季度纪检台账的占比与累计汇总', '巡视整改中各形态趋势跟踪', '多下属单位横向口径对齐', '常态化监督数据的可视化分析']),
}

def process_file(n, dry=False):
    p = os.path.join(D, 'tools', 'discipline', n + '.html')
    s = open(p, encoding='utf-8').read()
    orig = s
    log = []
    # A 类
    if n in FD_NEW:
        if FD_OLD_PREFIX in s:
            s = s.replace(FD_OLD_PREFIX, FD_NEW[n], 1)
            log.append('A:FD错配替换')
    # C 类 简介尾随
    if C_INTRO_TAIL in s:
        # 简介句形如 <p>工具名。免费在线工具，纯前端处理，数据不上传，保护隐私安全。</p>
        # 用真实 intro 替换整句（保留 <p> 标签与工具名前缀）
        new_intro = C_TEXT[n]['intro_new']
        s = re.sub(r'<p>[^<]*' + re.escape(C_INTRO_TAIL) + r'</p>',
                   '<p>' + new_intro + '</p>', s, count=1)
        log.append('C:简介尾随套话替换')
    # C 类 功能特点
    if C_FEATURE_JUNK in s:
        s = s.replace(C_FEATURE_JUNK, C_TEXT[n]['feature_new'], 1)
        log.append('C:功能特点套话替换')
    # C 类 使用场景 4 项
    sc = C_TEXT[n]['scenes']
    # 顺序替换（4 项都在 intro-scenes 内，按出现顺序）
    tmp = s
    for old_s, new_s in zip(C_SCENES_OLD, sc):
        tmp = tmp.replace('<li>' + old_s + '</li>', '<li>' + new_s + '</li>', 1)
    if tmp != s:
        s = tmp
        log.append('C:使用场景 4 项替换')
    if dry:
        return log, orig != s
    if s != orig:
        open(p, 'w', encoding='utf-8').write(s)
    return log, orig != s

def main():
    dry = '--dry' in sys.argv
    pages = ['assessor-28', 'assessor-risk-7', 'stats-analysis', 'tester-training-hr']
    total_changes = 0
    for n in pages:
        log, changed = process_file(n, dry)
        if changed:
            total_changes += 1
            print('[%s] %s' % (n, ' | '.join(log) if log else 'changed'))
        else:
            print('[%s] 无变化' % n)
    print('---')
    print('处理页数:', len(pages), '| 有改动:', total_changes, '| 模式: %s' % ('DRY' if dry else 'WRITE'))
    # JSON-LD 合法性抽检
    bad = []
    for n in pages:
        ss = open(os.path.join(D, 'tools', 'discipline', n + '.html'), encoding='utf-8').read()
        j = re.search(r'<script type="application/ld\+json">(.*?)</script>', ss, re.S)
        if j:
            try:
                json.loads(j.group(1))
            except Exception:
                bad.append(n)
    print('JSON-LD 非法页:', bad if bad else '无')

if __name__ == '__main__':
    main()
