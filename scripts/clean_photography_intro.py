#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 photography 的第四处占位残留：convert-focal.html 与 capacity-fps.html 的 intro-scenes 仍是通用默认占位。
calc-exposure-aperture.html 的 intro-scenes 已是真实摄影场景，不动。"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = """    <ul class="intro-scenes">
      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>
    </ul>"""

NEW_CONVERT = """    <ul class="intro-scenes">
      <li>镜头焦距与视场角的单位换算</li>
      <li>多支镜头画幅适配对比</li>
      <li>焦段规划与取景范围估算</li>
      <li>镜头库参数统一整理</li>
    </ul>"""

NEW_CAP = """    <ul class="intro-scenes">
      <li>录制帧率与存储容量规划</li>
      <li>多机位素材容量评估</li>
      <li>慢动作/高帧率方案取舍</li>
      <li>外录设备存储预留</li>
    </ul>"""

for fn, new in [("convert-focal.html", NEW_CONVERT), ("capacity-fps.html", NEW_CAP)]:
    P = os.path.join(BASE, "tools", "photography", fn)
    s = open(P, encoding="utf-8").read()
    if OLD in s:
        s = s.replace(OLD, new)
        open(P, "w", encoding="utf-8").write(s)
        print(f"{fn} intro-scenes 已替换为真实摄影场景")
    else:
        print(f"{fn} 未找到通用占位块，请人工核对")
