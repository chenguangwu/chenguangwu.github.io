#!/usr/bin/env python3
"""412 独立证据：fake-tools 清单不得再宣称「全站全量销账完成」。

复核失败 412 核心：part-01 旧结论称「全部不再成立 / 当前待修页 0 / 全量复核完毕」，
但同期 plan/复核失败/ 仍有多项未闭环 —— 以「本清单已清」误报「全站全部完成」不成立。
918 批据实修正：本清单页面层面已清，但明确列出全站仍存在的未闭环失败项，
不再出现绝对化「全量销账/全部完成/待修页 0」结论文案。
下划线前缀 = 独立专项证据，不入 ratchet。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "plan", "fake-tools", "part-01.md")
text = open(p, encoding="utf-8").read()

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


# ① 旧的绝对化全量销账措辞必须消失（「全站全部销账」允许出现在否定句「不成立…」里）
for bad in ["当前待修页 0", "全部不再成立", "全量复核完毕"]:
    check(bad not in text, "仍含绝对化销账措辞：「%s」" % bad)
for line in text.splitlines():
    if "全站全部销账" in line:
        check("不成立" in line or "不等于" in line or "不等于" in line,
              "「全站全部销账」出现在非否定语境：%s" % line.strip()[:60])

# ② 新结论必须点明「本清单清 ≠ 全站完成」
check("不等于「全站全部完成」" in text or "不成立「全站全部销账」结论" in text,
      "未声明本清单清不等于全站完成")
check("plan/复核失败/" in text, "未指向仍存在的失败项目录")

# ③ 清单指向实时目录，不复制会随着迁移失真的数量或名单。
import re
fail_dir = os.path.join(ROOT, "plan", "复核失败")
remain = sorted(fn for fn in os.listdir(fail_dir) if fn.endswith(".md"))
check("实时目录为准" in text, "未说明以失败目录实时内容为准")
check(not re.search(r"仍有\s*\*\*?\d+\s*项", text), "仍有静态失败数量")
check(not re.search(r"未闭环：[0-9０-９]", text), "仍有静态失败编号列表")

if fails:
    print("412 结论真实性检查失败：")
    for x in fails:
        print("  FAIL", x)
    sys.exit(1)
print("412 结论真实性检查通过；失败目录当前 %d 项（实时读取）" % len(remain))
