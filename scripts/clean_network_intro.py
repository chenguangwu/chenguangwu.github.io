#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 network 分类 3 个工具页 tool-intro-body 的 intro-scenes 通用默认占位
（日常办公与学习/开发调试与数据处理/快速计算与格式转换/信息查询与参考），
替换为各自真实的网络工程使用场景。calc-subnet 的 intro-scenes 已是真实场景，不处理。
_build.py 不重建该区块，需手动清理。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = """      <li>日常办公与学习</li>
      <li>开发调试与数据处理</li>
      <li>快速计算与格式转换</li>
      <li>信息查询与参考</li>"""

REPL = {
    "tools/network/convert-11.html": """      <li>网络抓包与报文分析</li>
      <li>IP 地址规划与排障</li>
      <li>子网划分与 VLAN 设计</li>
      <li>脚本批量 IP 处理</li>""",
    "tools/network/analysis-manager-1.html": """      <li>内部工具使用统计</li>
      <li>系统监控指标对比</li>
      <li>管理报表数据校验</li>
      <li>资源投入与产出分析</li>""",
    "tools/network/analysis-66.html": """      <li>优化前后效果量化</li>
      <li>A/B 多版本指标评测</li>
      <li>监测数据异常筛查</li>
      <li>增长与转化归因分析</li>""",
}

def main():
    for rel, new in REPL.items():
        p = os.path.join(ROOT, rel)
        with open(p, "r", encoding="utf-8") as f:
            s = f.read()
        if OLD not in s:
            print("SKIP (无占位):", rel); continue
        s = s.replace(OLD, new, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(s)
        print("OK 已清理:", rel)

if __name__ == "__main__":
    main()
