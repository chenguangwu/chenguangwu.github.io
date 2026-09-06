# -*- coding: utf-8 -*-
"""清理 cnc 分类硬编码套话：仅 1 工具 detector-23。

- tool-intro 三段块已真实（CNC 加工尺寸检测功能/场景，无套话、块完整），无需清。
- opt-guide <p> 套话 0 页，无需清。
- formula-desc 校验变体 1 页（detector-23）：替换为真实 CNC 尺寸检测说明。
  meta description 已真实（"选择检测方式...计算偏差并判定IT公差等级"），无回灌，仅清 formula-desc 块。
"""
import re
import os

TOOLS = "tools/cnc"
DRY = "--dry" in __import__("sys").argv

FD_MAP = {
    "detector-23": "本工具按 CNC 加工尺寸检测规范，输入实测尺寸与理论值计算偏差并对照 IT 公差等级判定合格性，给出刀具补偿与加工调整建议；纯前端运行，数据不上传。",
}


def clean_fd(name, real):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r'<p class="formula-desc">.*?</p>',
                 '<p class="formula-desc">' + real + '</p>', s, flags=re.S)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


total = 0
for name, real in FD_MAP.items():
    c = clean_fd(name, real)
    if c:
        total += c
        print((("DRY " if DRY else "") + "fd " + name))
print("total changed:", total)
