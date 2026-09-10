#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用清理：删除工具页源 html 中的 opt-guide / opt-faq 套话可见区块（DEV-PLAN §4.5.2）。

背景：早期 opt_content.py 批量生成的可见内容含通用套话（"在对应的输入框或选项中填写、
选择所需参数""点击「计算」或「生成」按钮""工作与生活中的相关计算与查询"等），
非构建产物、_build.py 不会覆盖，须手改源 html。

策略（§4.5.2）：整段删除 <section class="opt-guide">…</section> 与
<section class="opt-faq">…</section>，目标「前 N 后 0」。

用法:
    python3 scripts/opt_cleanup_opt_blocks.py --cat mechanical          # 清理整个分类
    python3 scripts/opt_cleanup_opt_blocks.py --cat mechanical --dry    # 只报数不改
    python3 scripts/opt_cleanup_opt_blocks.py --files a.html b.html     # 指定文件
"""
import re, glob, os, sys

CLASSES = ("opt-guide", "opt-faq")


def clean(text):
    """返回 (新文本, 删除块数)。非贪婪配对到最近的 </section>，避免误伤后续结构。"""
    removed = 0
    for cls in CLASSES:
        pattern = re.compile(r'<section class="%s">.*?</section>\s*' % cls, re.S)
        text, n = pattern.subn("", text)
        removed += n
    return text, removed


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    files = []
    if "--cat" in args:
        cat = args[args.index("--cat") + 1]
        files = [f for f in glob.glob("tools/%s/*.html" % cat)
                 if not f.endswith("index.html")]
    elif "--files" in args:
        i = args.index("--files") + 1
        files = [a for a in args[i:] if not a.startswith("--")]
    else:
        print("需要 --cat <分类> 或 --files <文件...>")
        return 1

    total_before = total_after = 0
    touched = []
    for f in sorted(files):
        t = open(f, encoding="utf-8").read()
        before = sum(len(re.findall(r'<section class="%s">' % c, t)) for c in CLASSES)
        if before == 0:
            continue
        new, removed = clean(t)
        after = sum(len(re.findall(r'<section class="%s">' % c, new)) for c in CLASSES)
        total_before += before
        total_after += after
        touched.append((f, before, after))
        if not dry:
            open(f, "w", encoding="utf-8").write(new)
    for f, b, a in touched:
        print("  %-46s 前 %d -> 后 %d" % (f, b, a))
    print("合计 前 %d -> 后 %d%s" % (total_before, total_after, "（dry-run 未落盘）" if dry else ""))
    return 0 if total_after == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
