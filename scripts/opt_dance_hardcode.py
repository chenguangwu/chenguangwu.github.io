#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 dance 3 页 opt 套话（B 类）。

仅 assessor-csat-1 / tester-4 / partner-distance 三页含「工作与生活中的相关计算与查询。」
每页出现 3 处：① JSON-LD 的 Answer.text；② <h2>适用场景</h2> 段；③ FAQ 的 <dd>。
统一替换为真实舞蹈场景短句（纯中文+标点，JSON-LD 合法）。

(A) FD 变体 0 页：dance 7 页均无 formula-desc 段，无需处理。
(C) 块内 6 类通用套话 0 页：dance 页 tool-intro-body 块内不含通用套话，无需处理。
幂等：仅当短语存在时替换；含 opt 回灌检测与 JSON-LD 合法性校验。
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "dance")

OPT_JUNK = "工作与生活中的相关计算与查询。"

REAL_SCENE = {
    "assessor-csat-1": "用于舞蹈培训机构的教学质量复盘、学员进步跟踪与多班级横向对比",
    "partner-distance": "用于双人舞配合走位规划、旋转轨迹半径估算与身高差补偿",
    "tester-4": "用于坐位体前屈体测评级、训练前后柔韧进步跟踪与群体体能筛查",
}


def check_jsonld(s, fname):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not m:
        return True
    try:
        json.loads(m.group(1))
        return True
    except Exception as e:
        print("  [JSON-LD] %s 非法: %s" % (fname, e))
        return False


def main():
    dry = "--dry" in sys.argv
    changed = []
    for fname, scene in REAL_SCENE.items():
        fp = os.path.join(TOOLS, fname + ".html")
        if not os.path.exists(fp):
            print("  SKIP 未找到:", fname)
            continue
        s = open(fp, encoding="utf-8").read()
        orig = s
        cnt = s.count(OPT_JUNK)
        if cnt == 0:
            print("  %s: 无 opt 套话(已处理)" % fname)
            continue
        s = s.replace(OPT_JUNK, scene + "。", cnt)
        if not check_jsonld(s, fname):
            print("  %s: JSON-LD 校验失败，跳过写入" % fname)
            continue
        if s != orig:
            changed.append(fname)
            if not dry:
                open(fp, "w", encoding="utf-8").write(s)
            print("  %s: %s (%d 处)" % (fname, "待写" if dry else "已改", cnt))
        else:
            print("  %s: 无变化" % fname)
    # 回灌检测
    print("\n=== 回灌检测 ===")
    for fname in REAL_SCENE:
        fp = os.path.join(TOOLS, fname + ".html")
        s = open(fp, encoding="utf-8").read()
        print("  %s opt 残留: %s" % (fname, OPT_JUNK in s))
    print("完成：改动 %d 页" % len(changed))


if __name__ == "__main__":
    main()
