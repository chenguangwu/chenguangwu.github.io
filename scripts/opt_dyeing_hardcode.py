# -*- coding: utf-8 -*-
"""清理 dyeing 1 页 opt 套话（B 类）。

仅 temp-time-humidity-1 含「工作与生活中的相关计算与查询。」（3 处：
① JSON-LD 的 Answer.text；② <h2>适用场景</h2> 段 <p>；③ FAQ 的 <dd>）。
直接改 html 源文件（该区块不在 _build.py 的 JSON 重建范围，dance 等分类已验证有效）。
替换为真实汽蒸场景短句（纯中文+标点，JSON-LD 合法）。

(A) FD 变体 0 页：dyeing 13 页均无 formula-desc 段。
(C) 块内 6 类通用套话 0 页：各页 tool-intro-body 已是真实专业内容，无需处理。
幂等：仅当短语存在时替换；含 opt 回灌检测与 JSON-LD 合法性校验。
"""
import os, re, sys, json

ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io'
TOOLS = os.path.join(ROOT, 'tools', 'dyeing')

OPT_JUNK = '工作与生活中的相关计算与查询。'
REAL_SCENE = '用于还原/活性/涂料印花蒸化固色工序的参数复核、蒸化工艺条件核对与印染工艺教学演示'

FILES = ['temp-time-humidity-1']


def check_jsonld(s, fname):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not m:
        return True
    try:
        json.loads(m.group(1))
        return True
    except Exception as e:
        print('  [JSON-LD] %s 非法: %s' % (fname, e))
        return False


def main():
    dry = '--dry' in sys.argv
    for fname in FILES:
        fp = os.path.join(TOOLS, fname + '.html')
        if not os.path.exists(fp):
            print('  SKIP 未找到:', fname)
            continue
        s = open(fp, encoding='utf-8').read()
        cnt = s.count(OPT_JUNK)
        if cnt == 0:
            print('  %s: 无 opt 套话(已处理)' % fname)
            continue
        new = s.replace(OPT_JUNK, REAL_SCENE + '。', cnt)
        if not check_jsonld(new, fname):
            print('  %s: JSON-LD 校验失败，跳过写入' % fname)
            continue
        if s != new:
            if not dry:
                open(fp, 'w', encoding='utf-8').write(new)
            print('  %s: %s (%d 处)' % (fname, '待写' if dry else '已改', cnt))
        else:
            print('  %s: 无变化' % fname)
    # 回灌检测
    print('\n=== 回灌检测 ===')
    for fname in FILES:
        fp = os.path.join(TOOLS, fname + '.html')
        if os.path.exists(fp):
            t = open(fp, encoding='utf-8').read()
            print('  %s opt 残留: %s' % (fname, OPT_JUNK in t))


if __name__ == '__main__':
    main()
