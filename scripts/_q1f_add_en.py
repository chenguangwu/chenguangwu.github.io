#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q1 二期（gen_q1f）英文同步：向 i18n/tools/slug-en.json（卡片名）与 i18n/tools/_en_override.json
（标题/简介，嵌套 {en,ed,ind}）插入 13 个工具的高质量语义化英文。
采用与一期 _q1e_add_en.py 一致的「在 { 后插入」范式，保持其余键格式不变。
用法：python3 scripts/_q1f_add_en.py
注意：_en_override.json 的值必须是 dict {en,ed,ind}，不能是字符串，否则 _build.py 的 apply_en_override 会报 AttributeError。
"""
import json

NEW = {
    "it/wifi-qr-generator": {"en": "WiFi QR Code Generator",
        "ed": "WiFi QR Code Generator - Generate a standard WIFI: provisioning string from SSID, password and encryption so phones join by scanning. Free, browser-only."},
    "it/docker-run-converter": {"en": "Docker Run to Compose Converter",
        "ed": "Docker Run to Compose Converter - Parse a docker run command into ports, volumes, env and restart as a docker-compose.yml snippet. Free, browser-only."},
    "design/gradient-generator": {"en": "CSS Gradient Generator",
        "ed": "CSS Gradient Generator - Produce copy-ready linear or radial gradient CSS with angle and color stops plus live preview. Free, browser-only."},
    "text/lorem-ipsum-generator": {"en": "Lorem Ipsum Generator",
        "ed": "Lorem Ipsum Generator - Generate placeholder paragraphs for layouts with selectable count and length. Free, browser-only."},
    "text/reading-time-estimator": {"en": "Reading Time Estimator",
        "ed": "Reading Time Estimator - Estimate reading time from Chinese/English text by average speed and count chars/words. Free, browser-only."},
    "accounting/split-bill": {"en": "Split Bill Calculator",
        "ed": "Split Bill Calculator - Split a bill evenly by total, people and tip percentage, with each share and tip. Free, browser-only."},
    "tax/gst-calculator": {"en": "GST Calculator",
        "ed": "GST Calculator - Convert between tax-inclusive and tax-exclusive amounts at any rate, separating tax from base. Free, browser-only."},
    "it/date-duration": {"en": "Date Duration Calculator",
        "ed": "Date Duration Calculator - Compute days and weeks between two dates with inclusive/exclusive end-date options. Free, browser-only."},
    "baking/recipe-scaler": {"en": "Recipe Scaler",
        "ed": "Recipe Scaler - Scale baking ingredients by a factor from name=amount lines in one pass. Free, browser-only."},
    "automotive/fuel-cost-calculator": {"en": "Fuel Cost Calculator",
        "ed": "Fuel Cost Calculator - Estimate fuel cost from distance, consumption and price, or cost per kilometer. Free, browser-only."},
    "daily-goods/parking-fee": {"en": "Parking Fee Calculator",
        "ed": "Parking Fee Calculator - Estimate parking fees from duration, rate, free period and daily cap. Free, browser-only."},
    "biz/unit-price-compare": {"en": "Unit Price Compare",
        "ed": "Unit Price Compare - Normalize two products to one base unit and compare price per unit. Free, browser-only."},
    "it/unit-converter-advanced": {"en": "Advanced Unit Converter",
        "ed": "Advanced Unit Converter - Convert across length, mass, temperature, area, volume, time, speed and data storage at once. Free, browser-only."},
}


def insert_after_brace(path, with_ind=False):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    parts = []
    for k, v in NEW.items():
        v2 = dict(v)
        if with_ind:
            v2["ind"] = k.split("/")[0]
        parts.append('"%s":%s' % (k, json.dumps(v2, ensure_ascii=False, separators=(",", ":"))))
    block = ",\n".join(parts)
    idx = s.index("{") + 1
    new_s = s[:idx] + "\n" + block + ",\n" + s[idx:]
    json.loads(new_s)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_s)
    print("updated", path)


if __name__ == "__main__":
    insert_after_brace("i18n/tools/slug-en.json", with_ind=False)
    insert_after_brace("i18n/tools/_en_override.json", with_ind=True)
    print("OK")
