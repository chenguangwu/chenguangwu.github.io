#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""替换 photo2 分类 5 个工具页 tool-intro-body 中的静态套话（area4）。
原模板为「设计创意/CSS」错位内容，替换为摄影真实内容：简介、功能特点、使用场景。
正则仅替换 <ul class="intro-features"> / <ul class="intro-scenes"> 整段及简介 <p>。
"""
import re
import os

BASE = "tools/photo2"

# 每个文件：intro 简介、features 功能特点、scenes 使用场景
DATA = {
    "exposure-triangle.html": {
        "intro": "曝光三角形是一款面向摄影爱好者的在线曝光计算工具，帮助理解光圈、快门、ISO 三者此消彼长的关系，在不改变亮度前提下控制景深与运动模糊。",
        "features": [
            "三角联动计算，任一参数变化即时换算另两项",
            "实时可视化曝光值与适用场景分级",
            "一键生成等量曝光组合对照表",
            "纯前端运行，数据不上传"
        ],
        "scenes": [
            "逆光人像虚化背景时控制曝光",
            "弱光手持防抖权衡景深与噪点",
            "运动物体高速快门定格",
            "风光夜景长曝光参数规划"
        ]
    },
    "focal-length.html": {
        "intro": "焦距视场角是一款摄影构图辅助工具，按镜头焦距与传感器画幅计算视场角，对比不同焦段取景范围，辅助镜头选择与构图。",
        "features": [
            "多画幅传感器一键切换（全画幅/APS-C/M4/3 等）",
            "水平/垂直/对角视场角实时换算",
            "等效焦距与焦距转换系数计算",
            "纯前端运行，数据不上传"
        ],
        "scenes": [
            "全画幅镜头转接 APS-C 机身取景评估",
            "风光超广角透视与畸变预判",
            "体育生态长焦空间压缩与拉近",
            "镜头采购前焦段覆盖规划"
        ]
    },
    "video-storage.html": {
        "intro": "视频存储计算是一款视频拍摄规划工具，按分辨率、帧率、码率与时长估算文件大小，辅助存储卡、硬盘与云存储的采购与备份规划。",
        "features": [
            "多种分辨率/帧率预设（720P–8K）",
            "视频+音频码率与编码系数综合估算",
            "存储卡容量可录时长对照",
            "纯前端运行，数据不上传"
        ],
        "scenes": [
            "婚礼活动跟拍存储卡容量规划",
            "户外延时长录制硬盘预算",
            "编码格式画质与体积权衡",
            "多机位素材备份空间评估"
        ]
    },
    "print-size.html": {
        "intro": "打印尺寸对照是一款摄影输出辅助工具，按图像像素与打印 DPI 换算物理尺寸，并列出常见照片规格的像素要求，判断照片能否满足清晰冲印。",
        "features": [
            "像素与物理尺寸双向换算",
            "多种 DPI 档位（72–600）质量评级",
            "6 寸/A4 等标准照片规格像素对照表",
            "纯前端运行，数据不上传"
        ],
        "scenes": [
            "冲印 6 寸前清晰度核查",
            "A4 画册原图像素门槛确认",
            "电商主图 DPI 与加载平衡",
            "证件照尺寸与像素匹配"
        ]
    },
    "color-temperature.html": {
        "intro": "色温白平衡是一款摄影校色参考工具，按色温 Kelvin 值换算 Mired 与近似 RGB，提供常见光源预设，辅助理解白平衡与画面冷暖。",
        "features": [
            "色温 K 值与 Mired 互转",
            "常见光源预设一键查询（烛光–蓝天）",
            "黑体辐射近似 RGB/HEX 预览",
            "纯前端运行，数据不上传"
        ],
        "scenes": [
            "室内钨丝灯偏黄校正",
            "黄昏暖调氛围保留",
            "混合光源灰卡自定义白平衡",
            "后期校色冷暖方向判断"
        ]
    }
}


def build_ul(items):
    return "<ul class=\"intro-features\">\n" + "\n".join(
        "      <li>%s</li>" % it for it in items) + "\n    </ul>"


def build_scenes(items):
    return "<ul class=\"intro-scenes\">\n" + "\n".join(
        "      <li>%s</li>" % it for it in items) + "\n    </ul>"


CLICHE_INTRO = "是一款设计创意领域的在线工具。设计创意工具，可视化操作，一键生成 CSS 代码。"

total_repl = 0
for fn, cfg in DATA.items():
    path = os.path.join(BASE, fn)
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # 1. 简介 <p>...</p>（匹配含设计创意套话的段落，整段替换）
    new_intro = "<p>%s</p>" % cfg["intro"]
    html2, n1 = re.subn(
        r"<p>[^<]*?是一款设计创意领域的在线工具。设计创意工具，可视化操作，一键生成 CSS 代码。</p>",
        new_intro, html, flags=re.S)
    # 2. features
    html3, n2 = re.subn(r"<ul class=\"intro-features\">.*?</ul>",
                        build_ul(cfg["features"]), html2, flags=re.S)
    # 3. scenes
    html4, n3 = re.subn(r"<ul class=\"intro-scenes\">.*?</ul>",
                        build_scenes(cfg["scenes"]), html3, flags=re.S)

    if (n1, n2, n3) != (1, 1, 1):
        print("WARN %s: intro=%d features=%d scenes=%d (expected 1,1,1)" % (fn, n1, n2, n3))
    with open(path, "w", encoding="utf-8") as f:
        f.write(html4)
    total_repl += n1 + n2 + n3
    print("cleaned %s: intro=%d features=%d scenes=%d" % (fn, n1, n2, n3))

# 复核：全站不应再出现设计创意套话
leftover = 0
for fn in DATA:
    with open(os.path.join(BASE, fn), encoding="utf-8") as f:
        if CLICHE_INTRO in f.read():
            leftover += 1
            print("RESIDUAL cliche in", fn)
print("total replacements:", total_repl, "| residual files:", leftover)
assert leftover == 0, "cliche not fully cleared"
print("OK")
