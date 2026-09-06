#!/usr/bin/env python3
"""清理 tools/blasting/ 下 3 个工具的 formula-desc 占位套话。

对齐 agriculture 范本格式：依据标准 + 真实原理/公式 + 工具用途 + 数据不出浏览器，
去除「本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。」
通用免责套话，保留并提炼真实工具信息。

幂等：仅当命中套话前缀才替换；已替换过的文件再次运行不变。
"""
import re
import sys

BASE = "tools/blasting"

# 文件名 -> 真实 formula-desc 文案（对齐 agriculture 范本）
REPLACE = {
    "blast-monitoring.html": (
        "依据 GB 6722《爆破安全规程》查询质点振动速度安全允许标准与监测要求；"
        "本工具输入爆心距、单段装药量等参数，按萨道夫斯基公式估算质点峰值振动速度，"
        "辅助判定是否超出安全允许值；纯前端计算，数据不出浏览器。"
    ),
    "demolition-method.html": (
        "依据结构类型、环境敏感性与工程规模推荐拆除方法；本工具按素混凝土、钢筋混凝土、"
        "砖砌体、钢结构、混合结构等输入，结合周边环境给出机械拆除、人工拆除、静力破碎或"
        "控制爆破的选型建议；纯前端计算，数据不出浏览器。"
    ),
    "structural-weakening.html": (
        "依据构件类型与几何参数定位拆除爆破薄弱点与切缝位置；本工具按立柱、梁、墙、板等"
        "构件输入截面与高度，给出预处理切口布置与最小抵抗线建议，辅助控制倒塌方向；"
        "纯前端计算，数据不出浏览器。"
    ),
}

PAT = re.compile(r'<p class="formula-desc">.*?</p>', re.S)


def main():
    dry = "--dry" in sys.argv
    for fn, new_desc in REPLACE.items():
        p = f"{BASE}/{fn}"
        html = open(p, encoding="utf-8").read()
        m = PAT.search(html)
        if not m:
            print(f"[SKIP] {fn}: 未找到 formula-desc 块")
            continue
        old = m.group(0)
        if "本速查内容依据权威标准" not in old:
            print(f"[SKIP] {fn}: 已是真实说明，无需替换")
            continue
        new = f'<p class="formula-desc">{new_desc}</p>'
        if dry:
            print(f"[DRY] {fn}:\n  - {old[:60]}...\n  + {new[:60]}...")
            continue
        html2 = PAT.sub(new, html, count=1)
        open(p, "w", encoding="utf-8").write(html2)
        print(f"[DONE] {fn}: formula-desc 已替换为真实说明")


if __name__ == "__main__":
    main()
