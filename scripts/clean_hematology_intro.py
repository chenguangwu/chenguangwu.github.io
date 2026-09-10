#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 hematology 分类 2 个文件 tool-intro-body 的 intro-scenes 第四处通用默认占位
（"日常办公与学习/开发调试与数据处理/快速计算与格式转换/信息查询与参考"）。
命中文件：quetie-juyou-rongxue-shiyanshijianbie.html（缺铁/巨幼/溶血实验室鉴别）、
generator-analysis.html（凝血酶生成 TG 曲线分析）。"""
import os

ROOT = "/Users/cgw/project/cgw/chenguangwu.github.io"
OLD = """    <ul class="intro-scenes">
      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>
    </ul>"""

REPL = {
    "quetie-juyou-rongxue-shiyanshijianbie.html": """    <ul class="intro-scenes">
      <li>血常规与网织红细胞区分增生性贫血与增生低下（缺铁/慢性病 vs 再生障碍）</li>
      <li>铁代谢四项（血清铁、铁蛋白、总铁结合力、转铁蛋白饱和度）定位缺铁或利用障碍</li>
      <li>叶酸/维生素 B12 与红细胞形态学检查鉴别巨幼细胞性贫血</li>
      <li>溶血指标（胆红素、LDH、结合珠蛋白、Coombs）判定溶血及免疫/非免疫分型</li>
    </ul>""",
    "generator-analysis.html": """    <ul class="intro-scenes">
      <li>按组织因子浓度与时间绘制凝血酶生成曲线，读取峰浓度、滞后时间、达峰时间与 ETP</li>
      <li>评估抗凝/止血平衡：峰值过高提示血栓风险、过低提示出血倾向</li>
      <li>监测抗凝药物（肝素、直接口服抗凝药 DOAC）对凝血酶生成参数的影响</li>
      <li>结合狼疮抗凝物、蛋白 C/S 缺陷等解读获得性易栓状态</li>
    </ul>""",
}

for fname, new in REPL.items():
    p = os.path.join(ROOT, "tools", "hematology", fname)
    assert os.path.exists(p), p
    s = open(p, encoding="utf-8").read()
    assert OLD in s, f"{fname} 未找到 intro-scenes 通用占位"
    s = s.replace(OLD, new)
    open(p, "w", encoding="utf-8").write(s)
    print(f"{fname} intro-scenes 第四处占位已清理")
