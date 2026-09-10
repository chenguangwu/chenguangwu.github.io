#!/usr/bin/env python3
"""realize(writing): 替换真占位键 writing/text-polisher（文本润色工具）为真实 deep-dive 内容。

诊断：原 deep-dive 正文为六型占位套话变体（"在writing场景下先确认Text Polisher口径与边界，再输出可复核
结论""适用于流程复用、异常复核、版本变更对照""降低追溯成本"等），且出现大写未替换变量名 "Text Polisher"；
scanner 精确指纹词（可复核输出/降低上手门槛）被同义变体（可复核结论/降低追溯成本）规避而漏报，经人工
通读确认仍为真占位。本脚本以真实文本润色工程内容覆盖，键数守恒（不删键），ci 5022。
"""
import json
import sys

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = f"{ROOT}/i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    data = json.load(f)

KEY = "writing/text-polisher"
assert KEY in data, f"键 {KEY} 不存在"

before = len(data)
assert before == 5022, f"键数异常: {before}"

data[KEY] = {
    "title": "文本润色工具",
    "scenarios": [
        "公文/邮件润色：把口语化、啰嗦的草稿调整为正式、简洁的书面表达，保留原意，避免歧义。",
        "论文/报告改写：做降重与语句通顺处理，规避生硬机翻腔，提升专业可读性。",
        "社媒文案打磨：在保持既定语气的前提下提升流畅度与吸引力，使表达更自然。"
    ],
    "examples": [
        {
            "title": "邮件润色示例",
            "body": "原文“那个事情你尽快看看弄一下” → 润色“烦请尽快跟进并处理该事项”。说明：去口语、补主语、明确动作，语气更正式且不失礼貌。"
        }
    ],
    "faqs": [
        {
            "q": "润色会改变原意吗？",
            "a": "默认只调整表达方式、不改变原意；遇到歧义句会保留原句并给出提示，由你最终确认。"
        },
        {
            "q": "支持哪些风格？",
            "a": "常见有正式、简洁、通顺、去口语等，可按场景选择；输出会附带主要修改要点，方便你逐条核对。"
        }
    ]
}

after = len(data)
assert after == 5022, f"键数守恒失败: {after}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"[OK] {KEY} 已替换为真实文本润色内容；键数守恒 {before} -> {after}")
