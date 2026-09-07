#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 encode 分类 B类套话 "工作与生活中的相关计算与查询。"
出现在两页（encode-5 二维码版本容量 / binary-to-ascii Binary·Hex to ASCII）的
FAQ JSON-LD text、opt-guide 适用场景 <p>、opt-faq <dd> 三处，统一替换为真实编码场景描述。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 每文件对应的真实适用场景描述（同一段文本用于三处位置）
REAL = {
    "tools/encode/encode-5.html": (
        "规划二维码印刷内容时确定所需版本与容量，例如产品包装、名片、"
        "海报与票务上的二维码；在容量受限时权衡编码模式（数字/字母/字节/汉字）"
        "与纠错等级，避免内容超出版本上限导致生成失败。"
    ),
    "tools/encode/binary-to-ascii.html": (
        "解析网络或串口通信报文中的 ASCII 载荷；排查嵌入式设备或日志里以二进制、"
        "十六进制形式打印的字符数据；教学演示二进制、十六进制与 ASCII 字符之间的映射关系。"
    ),
}

OLD = "工作与生活中的相关计算与查询。"

def main():
    total = 0
    for rel, real in REAL.items():
        fp = os.path.join(ROOT, rel)
        s = open(fp, encoding="utf-8").read()
        n = s.count(OLD)
        if n == 0:
            print(f"  [skip] {rel}: 无套话残留")
            continue
        s = s.replace(OLD, real)
        assert s.count(OLD) == 0, f"{rel} 替换后仍有残留"
        open(fp, "w", encoding="utf-8").write(s)
        total += n
        print(f"  [ok] {rel}: 替换 {n} 处")
    print(f"完成，共清理 {total} 处 B类套话")

if __name__ == "__main__":
    main()
