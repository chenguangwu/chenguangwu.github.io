#!/usr/bin/env python3
"""436 独立证据：页面 description 隐私尾句清理 + 与卡片描述口径一致。

背景（2026-11-15 复核失败 436）：构建源把「纯前端运行、数据不上传、无需注册，
打开浏览器即可使用。」拼进每个工具页的 description/og/twitter/JSON-LD，而卡片
描述逻辑 tool_desc_source.clean_zh_candidate 早已把同一句当模板尾巴清掉，造成
4022 页 description 尾部雷同、两处口径不一致。本脚本锁三条口径：
  1. 工具页 meta/og/twitter/JSON-LD 不再含该隐私尾句；
  2. 卡片权威源 clean_zh_candidate 对含尾句/补句的输入都能截掉模板尾巴、保留有效描述；
  3. industry-groups.json 的 32 字导航描述不被补句污染（无「适合工程估…」截断残留）。
下划线前缀 = 独立专项证据，不入 gates_manifest.txt ratchet。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tool_desc_source as TDS

PRIVACY_TAIL = "纯前端运行、数据不上传、无需注册"
BOILER_TAIL = "适合工程估算、日常换算与快速复核，结果可一键复制"

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


# ① 扫描工具页四类载体，隐私尾句必须为 0
TOOLS_DIR = os.path.join(ROOT, "tools")
hit_pages = []
for dirpath, _dirs, files in os.walk(TOOLS_DIR):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(dirpath, fn)
        with open(fp, encoding="utf-8", errors="ignore") as f:
            head = f.read(12000)
        if PRIVACY_TAIL in head:
            hit_pages.append(os.path.relpath(fp, ROOT))
check(not hit_pages, "页面仍含隐私尾句（%d 页，例：%s）" % (len(hit_pages), hit_pages[:3]))

# ② 卡片/导航描述：隐私尾句 + 补句都能被截掉，有效功能描述保留
cases = [
    # 旧格式历史页（尚未重建）：core 后直接拼隐私尾句
    ("按原始大小估算 Base64 编码后的体积与换行开销，便于调试编码问题。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。", "按原始大小估算 Base64 编码后的体积与换行开销，便于调试编码问题"),
    # 新格式（本批 build 产出）：core 后是补句，隐私尾句已在 _build.py 阶段清掉
    ("在字符与码点之间互转，便于理解字符集与编码差异。适合工程估算、日常换算与快速复核，结果可一键复制。", "在字符与码点之间互转，便于理解字符集与编码差异"),
    ("电阻计算支持串并联等效电阻、分压与功率核算，是电路分析的基础工具。" + BOILER_TAIL + "。", "电阻计算支持串并联等效电阻、分压与功率核算，是电路分析的基础工具"),
    # 真隐私功能陈述（非模板尾巴）不误伤
    ("银行卡号仅做 Luhn 校验，数据不上传。", "银行卡号仅做 Luhn 校验，数据不上传。"),
]
for raw, want in cases:
    got = TDS.clean_zh_candidate(raw, "").rstrip("。")
    check(got == want.rstrip("。" ), "clean_zh_candidate：「%s」→「%s」，期望「%s」" % (raw[:30], got, want))

# ③ industry-groups.json 导航描述无补句截断残留
ig_path = os.path.join(ROOT, "json", "industry-groups.json")
with open(ig_path, encoding="utf-8") as f:
    ig_text = f.read()
check("适合工程估" not in ig_text, "industry-groups.json 含补句截断污染")

# ④ json/tools.json 卡片 d 字段无隐私尾句
tj_path = os.path.join(ROOT, "json", "tools.json")
with open(tj_path, encoding="utf-8") as f:
    tj_text = f.read()
check(PRIVACY_TAIL not in tj_text, "tools.json 卡片描述仍含隐私尾句")

total = 1 + len(cases) + 2
if fails:
    print("436 隐私尾句清理证据：%d/%d 通过，%d 失败" % (total - len(fails), total, len(fails)))
    for x in fails:
        print("  FAIL", x)
    sys.exit(1)
print("436 隐私尾句清理证据：%d/%d 全部通过" % (total, total))
print("  - 工具页隐私尾句：0 页")
print("  - 卡片/导航描述：尾句与补句均能截掉、真隐私功能不误伤")
print("  - industry-groups.json / tools.json：无模板尾巴残留")
