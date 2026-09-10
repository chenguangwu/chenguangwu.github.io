#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补清 §9 队列漏检：customer-service/random-script 的 deep-dive FAQ 占位六型残留。

背景：
- §9 主队列曾标注 "customer-service 零改动"，但全站六型复扫发现该键 FAQ1/FAQ2
  含六型⑥结构性泛化短语占位（可复核输出 / 沿用模板逐项核对 / 降低上手门槛），
  属漏检，本轮补清。
- 仅重写 faqs（FAQ1、FAQ2 去占位，FAQ3 真实保留），scenarios/examples 均为真实内容不动。
- 键数守恒 5022；六型纯占位三词（可复核输出 / 沿用模板逐项核对 / 降低上手门槛）全站清零。
"""
import json

P = "i18n/tools/content_deepdive.json"


def main():
    with open(P, encoding="utf-8") as f:
        d = json.load(f)
    assert len(d) == 5022, "键数漂移: %d" % len(d)

    k = "customer-service/random-script"
    assert k in d, "缺少键: %s" % k
    old = d[k]
    assert "faqs" in old and len(old["faqs"]) >= 2, "FAQ 结构异常"

    # 重写 FAQ：去六型占位，贴合工具真实功能
    # 工具能力：从本地话术库随机抽取 n 条生成对练清单；「复制」按钮复制结果；纯前端不采集数据。
    new_faqs = [
        {
            "q": "抽取结果可以保存或复用吗？",
            "a": "可以。点「复制」按钮即可把生成的对练清单复制到剪贴板，再粘贴到培训文档或群聊里留痕；坐席也能按同一份清单反复自测，主管则可把同一清单发给多名坐席做统一考核。",
        },
        {
            "q": "新成员如何使用它做岗前演练？",
            "a": "直接打开工具抽取一份清单，按「确认状态 → 说明影响 → 给出方案 → 留复核入口 → 礼貌收尾」的顺序逐条模拟应答并自评即可，无需自己从零准备对练材料；主管也能把同一份清单分发给团队统一练习。",
        },
        {
            "q": "随机抽取会泄露客户数据吗？",
            "a": "不会。仅从本地话术库抽取，不采集任何客户信息，符合隐私合规要求。",
        },
    ]
    old["faqs"] = new_faqs

    # 占位指纹断言（仅六型纯占位三词，须全站清零；统一口径/快速复核为合法真实用词，不纳入）
    txt = json.dumps(d, ensure_ascii=False)
    for fp in ["可复核输出", "沿用模板逐项核对", "降低上手门槛"]:
        c = txt.count(fp)
        assert c == 0, "残留占位: %s = %d" % (fp, c)

    with open(P, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))

    residual = sum(txt.count(fp) for fp in ["可复核输出", "沿用模板逐项核对", "降低上手门槛"])
    print("updated keys: 1 / total keys: %d / residual cliche: %d / OK" % (len(d), residual))


if __name__ == "__main__":
    main()
