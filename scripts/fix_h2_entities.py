#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复首个 <h2> 标题的 HTML 实体多重转义损坏（历史遗留，跨分类）。

症状（2026-09-12 全站扫描命中 32 页 / 14 分类）：
    <h2 data-zh="&amp;#127908; 在线录音工具">&amp;#Audio Recorder</h2>
浏览器渲染为「&#Audio Recorder」—— emoji 实体 &#127908; 被吞掉数字部分，
只留下字面 '&'，同时 data-zh 被反复转义成 &amp;#127908;（应为 🎤）。

根因：早期某批量脚本在处理 `&#NNNNN;` 形式的 emoji 时正则失误，丢弃了数字段。

修法（幂等）：
- data-zh 做「深度反转义」（反复 html.unescape 直到稳定）还原出真实
  「emoji + 中文名」；emoji 与中文名按首个空格拆分（首字符非 emoji 时视为无 emoji）。
- 英文名取 i18n/tools/_en_override.json 的权威 en 值（含 EN_FIX 补丁表）。
- 重写为 <h2 data-zh="{emoji} {中文名}">{emoji} {英文名}</h2>，保留 h2 的其他属性。

用法：
    python3 scripts/fix_h2_entities.py --dry-run
    python3 scripts/fix_h2_entities.py --apply
    python3 scripts/fix_h2_entities.py --dry-run --industry science   # 仅限某分类
"""
import argparse
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OV_PATH = os.path.join(ROOT, "i18n", "tools", "_en_override.json")

# data-zh 深度反转义后仍与正确值不符的特殊条目（数据源本身损坏）
EN_FIX = {
    "it/case-converter": "Case Converter",   # 原 en = "Case Converter - &# 128296 ; Case Converter"
    "statistics/cohens-d": "Cohen's D",      # 原 en = "Cohens D"（丢撇号）
    "statistics/cramers-v": "Cramer's V",    # 原 en = "Cramers V"（丢撇号）
}

# 历史上的 emoji 实体数字本身写错（深度反转义后落到不相关的符号），按名称修正
EMOJI_FIX = {
    "design/image-mosaic": "🖼",            # 原 #12951 -> ㊗（应为图片类）
    "design/image-rounded-corners": "🔲",   # 原 #11099 -> ⭛
    "fun/pong": "🏓",                       # 原 #127936 -> 🏀（篮球）
    "music/piano-keyboard": "🎹",           # 原 #127930 -> 🎺（小号）
}

H2_RE = re.compile(r"<h2([^>]*)>([\s\S]*?)</h2>")
DZ_RE = re.compile(r'data-zh="([^"]*)"')


def deep_unescape(s, rounds=5):
    for _ in range(rounds):
        n = html.unescape(s)
        if n == s:
            break
        s = n
    return s


def looks_like_emoji(tok):
    """首 token 不含中日韩文字或拉丁字母数字时，视为 emoji / 符号图标。"""
    if not tok:
        return False
    if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", tok):
        return False
    if re.search(r"[A-Za-z0-9]", tok):
        return False
    return True


def split_emoji(text):
    """返回 (emoji/图标, 其余文字)。首 token 非图标时 emoji 为 ''。"""
    text = text.strip()
    if not text:
        return "", text
    parts = text.split(" ", 1)
    head = parts[0]
    if looks_like_emoji(head):
        return head, (parts[1].strip() if len(parts) > 1 else "")
    return "", text


def esc_attr(v):
    return v.replace("&", "&amp;").replace('"', "&quot;")


def esc_text(v):
    return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_broken(inner_raw, dz_raw):
    disp_inner = html.unescape(inner_raw.strip())
    if re.match(r"^&(#?[A-Za-z])", disp_inner):
        return True
    if re.search(r"&amp;amp;|&amp;#\d|&amp;#x[0-9A-Fa-f]", dz_raw):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--industry", default=None, help="仅处理该分类目录（默认全站）")
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        print("请指定 --dry-run 或 --apply")
        return 2

    ov = json.load(open(OV_PATH, encoding="utf-8"))
    pattern = "tools/%s/*.html" % (a.industry or "*")
    files = [f for f in sorted(glob.glob(os.path.join(ROOT, pattern)))
             if os.path.basename(f) != "index.html"]

    fixed, skipped = [], []
    for path in files:
        ind = os.path.basename(os.path.dirname(path))
        slug = os.path.basename(path)[:-5]
        src = open(path, encoding="utf-8").read()
        m = H2_RE.search(src)
        if not m:
            continue
        attrs, inner_raw = m.group(1), m.group(2)
        dzm = DZ_RE.search(attrs)
        dz_raw = dzm.group(1) if dzm else ""
        if not is_broken(inner_raw, dz_raw):
            continue

        key = "%s/%s" % (ind, slug)
        en = EN_FIX.get(key) or (ov.get(key, {}) or {}).get("en") or ""
        if not en:
            skipped.append((key, "无 en 数据源"))
            continue

        dz_deep = deep_unescape(dz_raw)
        emoji, zh = split_emoji(dz_deep)
        if not zh:
            skipped.append((key, "data-zh 无法解析: %r" % dz_deep))
            continue
        # emoji 实体数字历史写错的，用 EMOJI_FIX 修正（zh 已剥离错误符号）
        emoji = EMOJI_FIX.get(key, emoji)

        new_attrs = attrs
        new_dz = (emoji + " " + zh).strip()
        if dzm:
            new_attrs = attrs[:dzm.start(1)] + esc_attr(new_dz) + attrs[dzm.end(1):]
        else:
            new_attrs = attrs + ' data-zh="%s"' % esc_attr(new_dz)

        new_inner = esc_text((emoji + " " + en).strip())
        new_h2 = "<h2%s>%s</h2>" % (new_attrs, new_inner)
        new_src = src[:m.start()] + new_h2 + src[m.end():]
        if new_src == src:
            continue
        if a.apply:
            open(path, "w", encoding="utf-8").write(new_src)
        fixed.append((key, inner_raw.strip()[:40], new_inner[:40], dz_raw[:34], new_dz[:34]))

    print("扫描页面: %d；需修复: %d；跳过: %d" % (len(files), len(fixed), len(skipped)))
    for k, oi, ni, od, nd in fixed:
        print("  [%s]" % k)
        print("      inner : %r -> %r" % (oi, ni))
        print("      data-zh: %r -> %r" % (od, nd))
    for k, why in skipped:
        print("  ⚠️ 跳过 %s：%s" % (k, why))

    # 同步修正 i18n 数据源中损坏的 en 值（避免页面 h2 与分类页/搜索不一致）
    synced = []
    for key, en in EN_FIX.items():
        if key in ov and (ov[key].get("en") or "") != en:
            synced.append((key, ov[key].get("en"), en))
            ov[key]["en"] = en
    if synced and a.apply:
        json.dump(ov, open(OV_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if synced:
        print("\n数据源 en 同步修正 %d 条%s：" % (len(synced), "" if a.apply else "（dry-run 未写入）"))
        for k, old, new in synced:
            print("  [%s] %r -> %r" % (k, old, new))

    if a.dry_run:
        print("\n（dry-run，未写入；加 --apply 生效）")
    else:
        print("\n已写入 %d 个页面文件" % len(fixed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
