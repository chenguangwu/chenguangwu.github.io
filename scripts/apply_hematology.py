# -*- coding: utf-8 -*-
"""真实化 hematology 分类 deep-dive 占位。键数守恒 5022。
hematology 28 键中仅 hematology/assessor-4 为 STY3 孤儿占位（无对应 HTML，真实工具
iron-overload.html 由 hematology/iron-overload 真实注入）；其余 27 键早已真实化。
本脚本仅替换该 1 孤儿键为真实血液学内容（不删键，保 5022）。
"""
import json
import os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
P = os.path.join(ROOT, "i18n/tools/content_deepdive.json")

d = json.load(open(P, encoding="utf-8"))
before = len(d)
assert "hematology/assessor-4" in d, "孤儿键缺失"

d["hematology/assessor-4"] = {
    "title": "铁过载（血清铁蛋白）评估",
    "scenarios": [
        "体检筛查：用血清铁蛋白结合转铁蛋白饱和度初筛铁过载，铁蛋白超过性别参考上限（男>300、女>200 ng/mL）或转铁蛋白饱和度>45% 时提示铁负荷异常，需进一步 HFE 基因检测或肝脏 MRI 铁沉积评估。",
        "遗传性血色病评估：对 HFE C282Y 突变携带者，按铁蛋白与转铁蛋白饱和度分级（铁蛋白>1000 ng/mL 为高负荷），制定治疗性放血或铁螯合疗程并监测脏器功能。",
        "输血依赖贫血监测：地中海贫血、MDS 等需定期输血者，监测铁蛋白累积（常>1000 ng/mL 需祛铁治疗），评估心脏、肝脏等器官铁沉积风险。"
    ],
    "examples": [
        {
            "title": "算例：男性血清铁蛋白 650 ng/mL 的铁过载评估",
            "body": "输入：男性、血清铁蛋白 650 ng/mL、转铁蛋白饱和度 52%。判定：铁蛋白 650 > 300 ng/mL（男性参考上限），且转铁蛋白饱和度 52% > 45%，符合铁过载（iron overload）标准，提示明显铁负荷增加；若铁蛋白 >1000 ng/mL 则属高负荷、需启动治疗性放血（目标铁蛋白 50–100 ng/mL）或铁螯合。结论：该例为中度铁过载，建议完善 HFE 基因检测与肝脏 MRI 铁定量。"
        }
    ],
    "faqs": [
        {
            "q": "铁蛋白多高算铁过载？",
            "a": "成人铁蛋白参考上限约为男性 300 ng/mL、女性 200 ng/mL；超过即为铁负荷增加。临床常将铁蛋白 >1000 ng/mL 视为显著铁过载（高负荷），常需祛铁治疗。但铁蛋白也受炎症、肝病、肿瘤影响而升高，需结合转铁蛋白饱和度（>45% 支持真性铁过载）与临床表现综合判断，不能单凭一次结果诊断。"
        },
        {
            "q": "铁过载怎么降下来？",
            "a": "遗传性血色病或部分输血依赖者以治疗性放血（静脉切放）为主，每周 1 次至铁蛋白降至 50–100 ng/mL 后改为维持；不能放血者（如贫血、心功能差）用铁螯合剂（去铁胺/地拉罗司）。同时限制膳食铁与维生素 C 摄入。具体方案须由血液科据铁蛋白、脏器功能与病因个体化制定。"
        }
    ]
}

after = len(d)
assert before == after, f"键数变化 {before}->{after}"
assert before == 5022, f"键数不为 5022: {before}"

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print(f"OK hematology 孤儿键真实化完成: 键数守恒 {before}（assessor-4 1 键已替换为真实内容）")
