#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 photo2 分类 5 键 deep-dive（第四波模板变体占位）。
键数守恒 5022：只修改值，不增删键。JSON 仓库规范 indent=1 + separators=(",", ": ")。
"""
import json

P = "i18n/tools/content_deepdive.json"

with open(P, encoding="utf-8") as f:
    d = json.load(f)

new = {
    "photo2/exposure-triangle": {
        "title": "曝光三角形",
        "scenarios": [
            "逆光人像想用大光圈虚化背景时，需在曝光三角形中提高快门速度或降低 ISO，避免画面过曝。",
            "弱光手持拍摄为压低快门防抖，往往开大光圈或提升 ISO，但需权衡景深变浅与噪点增加。",
            "拍摄运动物体需高速快门定格瞬间，可用开大光圈或提高 ISO 补偿进光量，维持曝光不变。"
        ],
        "examples": [
            {
                "title": "默认参数下的曝光值",
                "body": "以 f/5.6、1/60s、ISO100 为例：EV100=log₂(5.6²÷0.0167)≈10.9，ISO 调整 0 档，实际 EV≈10.9，对应「晴天户外」场景；调整任一顶点（光圈/快门/ISO）一档，需用另两项反向补偿以保持等量曝光。"
            }
        ],
        "faqs": [
            {
                "q": "EV 值代表什么含义？",
                "a": "EV（曝光值）量化进光量，数值每加 1 表示进光量翻倍、减 1 表示减半；它是光圈、快门、ISO 三者的综合结果。"
            },
            {
                "q": "为什么改一档光圈要补偿其他参数？",
                "a": "三角形任一顶点改变都会改变总进光量，保持等量曝光须由另两个顶点反向补偿相同档数，画面亮度才不变化。"
            }
        ]
    },
    "photo2/focal-length": {
        "title": "焦距视场角",
        "scenarios": [
            "全画幅标镜装在 APS-C 机身上，等效焦距变长、取景视野变窄，构图需相应后撤。",
            "风光与建筑摄影常用 16mm 超广角获取宏大透视，但需注意边缘畸变与暗角。",
            "体育、生态摄影依赖 400mm 等长焦压缩空间、拉近远处主体，同时虚化杂乱背景。"
        ],
        "examples": [
            {
                "title": "等效焦距换算",
                "body": "以 50mm 镜头为例：装在全画幅（对角线 43.3mm）等效 50mm、视角 ×1.00；装在 APS-C（28.2mm）等效约 77mm、视角 ×0.65；装在 M4/3（21.6mm）等效 100mm、视角 ×0.50。换算公式：等效焦距=焦距×(参考画幅对角线÷当前画幅对角线)。"
            }
        ],
        "faqs": [
            {
                "q": "焦距转换系数怎么计算？",
                "a": "系数=当前画幅对角线÷参考画幅（通常相对全画幅）对角线；系数越小说明等效焦距越长、视角越窄。"
            },
            {
                "q": "视场角和焦距是什么关系？",
                "a": "焦距越长视场角越窄。水平视场角 FOV=2×arctan(传感器宽÷(2×焦距))，单位度。"
            }
        ]
    },
    "photo2/video-storage": {
        "title": "视频存储计算",
        "scenarios": [
            "婚礼、活动跟拍前估算 4K/30fps 一小时占用的存储卡容量，决定携带几张卡与备份策略。",
            "户外延时或长录制按码率与时长预算硬盘空间，避免录制中途容量耗尽。",
            "在画质与体积间权衡：选 H.265/HEVC 可省约一半空间，但需确认播放端兼容性。"
        ],
        "examples": [
            {
                "title": "1080P 一小时文件大小",
                "body": "以 1080P、30fps、视频码率 20Mbps、音频 128kbps、录制 1 小时、H.264 编码为例：文件大小=(20+0.128)×3600÷8÷1024≈8.85GB；一张 32GB 存储卡约可录制 3.6 小时。改用 H.265 约 4.42GB；若升级到 4K、100Mbps 则一小时约 44GB。"
            }
        ],
        "faqs": [
            {
                "q": "码率越高画质一定越好吗？",
                "a": "通常码率越高细节保留越多、文件越大，但受编码器效率与画面复杂度影响；过高码率收益递减。"
            },
            {
                "q": "H.265 为什么能省空间？",
                "a": "HEVC 在同画质下约比 H.264 节省 40%–50% 码率，但编码/解码算力开销更大，老旧设备可能不兼容。"
            }
        ]
    },
    "photo2/print-size": {
        "title": "打印尺寸对照",
        "scenarios": [
            "冲印 6 寸照片前检查原图是否达到 1205×1795 像素（300DPI），避免放大后模糊。",
            "制作 A4 画册需原图至少 2480×3508 像素，低于此值印刷会出现锯齿与软边。",
            "电商主图按 72–150DPI 输出，在清晰度与网页加载速度之间取得平衡。"
        ],
        "examples": [
            {
                "title": "3000×2000 像素照片的打印尺寸",
                "body": "以 3000×2000 像素（6MP）、300DPI 为例：宽度=3000÷300×25.4≈254mm，高度≈169mm，即约 10×6.7 英寸；宽高比 3:2，质量评级「优秀」。若降到 150DPI，物理尺寸翻倍但仅适合日常打印。"
            }
        ],
        "faqs": [
            {
                "q": "打印多少 DPI 算清晰？",
                "a": "照片冲印建议 ≥300DPI 达到专业级；屏幕显示 72DPI 即可；150DPI 适合一般文档打印。"
            },
            {
                "q": "打印尺寸和像素怎么换算？",
                "a": "物理尺寸(mm)=像素÷DPI×25.4；所需最小像素=目标尺寸(mm)÷25.4×目标DPI。DPI 越高单位面积像素越密、越清晰。"
            }
        ]
    },
    "photo2/color-temperature": {
        "title": "色温白平衡",
        "scenarios": [
            "室内钨丝灯下人像偏黄，可在相机白平衡设 3200K 或后期向蓝方向补偿校正。",
            "黄昏外拍保留暖调氛围时，用 5600K 标准基准而非强制去暖，避免过度冷调。",
            "混合光源（窗光+灯光）场景用灰卡自定义白平衡，避免画面局部偏色。"
        ],
        "examples": [
            {
                "title": "色温与 Mired 换算",
                "body": "以正午日光 5500K 为例：Mired=round(1000000÷5500)=182，对应 RGB 近似 (255,237,222)、HEX #ffedde，相机建议日光/闪光灯模式；暖光 3200K 的 Mired=313、RGB(255,184,123)；冷光 6500K 的 Mired=154、RGB(255,254,250)。"
            }
        ],
        "faqs": [
            {
                "q": "色温 K 值如何对应颜色？",
                "a": "低色温偏橙红（烛光/钨丝），高色温偏蓝白（阴影/蓝天），工具按黑体辐射近似换算 RGB。"
            },
            {
                "q": "Mired 是什么、有什么用？",
                "a": "Mired=1,000,000÷K，用于白平衡滤镜换算；与开尔文相反，Mired 数值越大光线越暖，便于滤镜档位换算。"
            }
        ]
    }
}

# 占位指纹（第四波模板变体 + 通用套话）
FP = ["在photo2场景下", "先使用", "建立输入边界", "后续再对关键指标拆分归因",
      "适合先做样本验证", "将异常样本与处理假设并列记录",
      "边界样本试跑", "挑选一组正常样本与一组异常样本并行计算",
      "如何避免误报？", "输出可否直接落地？"]

before = sum(1 for k in new for blob in (json.dumps(d[k], ensure_ascii=False) for _ in [0])
             if any(fp in json.dumps(d[k], ensure_ascii=False) for fp in FP))

for k, v in new.items():
    assert k in d, "missing key: " + k
    d[k] = v

after = sum(1 for k in new if any(fp in json.dumps(d[k], ensure_ascii=False) for fp in FP))

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1, separators=(",", ": "))

print("updated keys:", len(new))
print("total keys:", len(d))
print("residual cliche (before/after):", before, "/", after)
assert len(d) == 5022, "key count must stay 5022, got %d" % len(d)
assert after == 0, "residual cliche not cleared"
print("OK")
