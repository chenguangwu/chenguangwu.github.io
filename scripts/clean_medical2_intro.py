#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""替换 medical2 5 个 HTML 的 area4 intro-scenes 通用占位（4 条同款套话）
为各工具真实医疗运营场景。area4 不被 _build.py 重建，须手改源 HTML。
"""
import re

MAPPING = {
    "iv-drip-speed": [
        "住院输液滴速调节与巡视安排",
        "门诊输液完成时间预估",
        "儿科微量输液速度控制",
        "静脉治疗质量控制核查",
    ],
    "bed-occupancy": [
        "科室月度床位运营分析",
        "床位规模规划与扩容评估",
        "医保绩效考核指标核算",
        "应急与疫情床位调度",
    ],
    "medical-abbrev": [
        "医嘱缩写核对与误读防范",
        "英文文献术语检索",
        "实习医护缩写培训",
        "处方审核参考",
    ],
    "surgery-duration": [
        "手术室排程与排台",
        "连台手术接台安排",
        "麻醉复苏资源规划",
        "手术产能与效率评估",
    ],
    "drug-expiry": [
        "家庭药箱效期盘点",
        "药房近效期批次管理",
        "临床科室备药核查",
        "疫苗与生物制剂效期监控",
    ],
}

def main():
    for base, items in MAPPING.items():
        fp = "tools/medical2/%s.html" % base
        with open(fp, encoding="utf-8") as f:
            s = f.read()
        block = '<ul class="intro-scenes">\n' + "".join(
            "      <li>%s</li>\n" % x for x in items
        ) + "    </ul>"
        s2, n = re.subn(r'<ul class="intro-scenes">.*?</ul>', block, s, flags=re.S)
        if n != 1:
            raise SystemExit("FAIL %s replaced=%d" % (base, n))
        with open(fp, "w", encoding="utf-8") as f:
            f.write(s2)
        print("OK", base, "->", items[0])

if __name__ == "__main__":
    main()
