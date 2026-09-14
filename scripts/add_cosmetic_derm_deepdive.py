#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 content_deepdive.json 的 cosmetic-derm 段补 1 个缺失键。

缺失页：assessor-67（历史上未纳入 i18n 管道，故无 deep-dive 键）。

保持该文件自定义格式（顶层键 1 空格缩进），用精确文本插入，不做 json.dump 重写。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "i18n/tools/content_deepdive.json")
ANCHOR = ' "cosmetic-derm/aging-1": {'

ENTRIES = [
    (
        "cosmetic-derm/assessor-67",
        {
            "title": "注册（备案/检验/安全评估）流程",
            "scenarios": [
                "备案前自查：把第三方检验报告里的铅、砷、汞、甲醇与菌落总数录进来，先判断这批配方能不能过备案。",
                "配方微调：某项卡在限值边缘时，先算清各项余量再改配方与工艺，避免反复送检。",
                "特殊/普通分流：按类别换用不同菌落总数限值，看清该走 NMPA 注册还是备案流程。",
            ],
            "examples": [
                {
                    "title": "可复现算例：普通化妆品五项全达标",
                    "body": "输入：类别=普通化妆品，铅 5、砷 2、汞 0.5、甲醇 0.1、菌落总数 100。\n内置限值：铅 ≤10、砷 ≤4、汞 ≤1、甲醇 ≤0.2、菌落总数（普通）≤1000。\n逐项判定 5/5 全为 ✓ → 结论「符合备案/注册要求」，提示普通化妆品在 NMPA 平台备案后即可上市。\n若把类别切到「特殊化妆品」，菌落总数限值收紧为 ≤500，其余四项限值不变。",
                },
                {
                    "title": "可复现算例：汞超标被拦下",
                    "body": "输入：汞 1.5（限值 ≤1）→ 该项判定 ✗，整体结论「不符合要求」，页面提示存在超标项目、不得上市销售，需调整配方或工艺并重新检测合格后方可备案/注册。",
                },
            ],
            "faqs": [
                {
                    "q": "限值是从哪里来的？可以改吗？",
                    "a": "按《化妆品安全技术规范》《化妆品监督管理条例》及 GB 7918、GB 7917 等公开限值内置在页面里（铅 ≤10、砷 ≤4、汞 ≤1、甲醇 ≤0.2、菌落总数 普通 ≤1000 / 特殊 ≤500，单位 mg/kg，菌落总数 CFU/g）。工具纯前端运行、不联网、不上传数据，因此限值是固定口径；法规更新时以官方最新文本为准。",
                },
                {
                    "q": "特殊化妆品和普通化妆品的差别在哪里？",
                    "a": "本工具里主要体现在两点：一是菌落总数限值（特殊 ≤500，普通 ≤1000）；二是上市路径——特殊化妆品（染发、烫发、祛斑美白、防晒、防脱发、宣称新功效等）须向 NMPA 申请注册，审批周期约 6–12 个月；普通化妆品只需在 NMPA 平台备案，备案后可上市。",
                },
                {
                    "q": "能替代第三方检验或官方审评吗？",
                    "a": "不能。本工具只做「录入值 vs 公开限值」的逐项对照，用于送检前的自查与配方预判；法定结论必须以有资质检验机构出具的检测报告和药监部门的审评结果为准。",
                },
            ],
            "summary": "把铅、砷、汞、甲醇与菌落总数的实测值逐项对照公开限值，输出达标矩阵与备案/注册结论，便于送检前自查。",
        },
    ),
]


def dump_entry(key, obj) -> str:
    """按文件既有缩进（键 1 空格、字段 2 空格、数组项 3、内层对象 4…）生成文本。"""
    out = [' "%s": {' % key]
    out.append('  "title": %s,' % json.dumps(obj["title"], ensure_ascii=False))
    out.append('  "scenarios": [')
    for i, s in enumerate(obj["scenarios"]):
        out.append('   %s%s' % (json.dumps(s, ensure_ascii=False), ',' if i < len(obj["scenarios"]) - 1 else ''))
    out.append('  ],')
    out.append('  "examples": [')
    for i, e in enumerate(obj["examples"]):
        out.append('   {')
        out.append('    "title": %s,' % json.dumps(e["title"], ensure_ascii=False))
        out.append('    "body": %s' % json.dumps(e["body"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["examples"]) - 1 else ''))
    out.append('  ],')
    out.append('  "faqs": [')
    for i, f in enumerate(obj["faqs"]):
        out.append('   {')
        out.append('    "q": %s,' % json.dumps(f["q"], ensure_ascii=False))
        out.append('    "a": %s' % json.dumps(f["a"], ensure_ascii=False))
        out.append('   }%s' % (',' if i < len(obj["faqs"]) - 1 else ''))
    out.append('  ],')
    out.append('  "summary": %s' % json.dumps(obj["summary"], ensure_ascii=False))
    out.append(' },')
    return '\n'.join(out)


def main() -> int:
    apply = "--apply" in sys.argv
    raw = open(P, encoding="utf-8").read()
    data = json.loads(raw)
    existing = [k for k, _ in ENTRIES if k in data]
    if existing:
        print("已存在，跳过:", existing)

    block = "\n".join(dump_entry(k, v) for k, v in ENTRIES if k not in data)
    if not block:
        print("无需写入")
        return 0

    idx = raw.find(ANCHOR)
    if idx < 0:
        print("未找到锚点，终止")
        return 1
    new = raw[:idx] + block + "\n" + raw[idx:]

    chk = json.loads(new)
    for k, v in ENTRIES:
        assert chk.get(k) == v, "内容不一致: " + k
    print("新增键: %s | cosmetic-derm 段旧键 %d -> 新键 %d | 非本段键数不变: %s" % (
        ", ".join(k for k, _ in ENTRIES if k not in data),
        len([k for k in data if k.startswith("cosmetic-derm/")]),
        len([k for k in chk if k.startswith("cosmetic-derm/")]),
        len([k for k in data if not k.startswith("cosmetic-derm/")]) == len([k for k in chk if not k.startswith("cosmetic-derm/")]),
    ))
    if apply:
        open(P, "w", encoding="utf-8").write(new)
        print("已落盘")
    else:
        print("预览（加 --apply 落盘）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
