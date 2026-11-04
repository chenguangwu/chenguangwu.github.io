#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tax 计算页空值守卫（幂等）。

根因同族：calcTool() 直接 num()（空值→0）后无条件 dataGrid 渲染，
导致「清空输入仍输出结构化零值」。本脚本在 calcTool 顶部插入
「是否填写」守卫（空串 / parseFloat→NaN），不判非 0，
因此 debt=0 / r=0 这类合法 0 不受影响。

幂等判据：脚本标记 /* TOOLBOX-REQ-GUARD */ 已存在则整页跳过；
可重复运行，第二次起零改动。

用法：
  python3 scripts/apply_tax_req_guard.py            # 默认处理 BATCH1 十页
  python3 scripts/apply_tax_req_guard.py --all      # 处理 BATCH 全部 16 页
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = "/* TOOLBOX-REQ-GUARD */"

BATCH1 = [
    "ad-valorem-duty", "break-even-taxable", "capital-gains-tax", "customs-duty",
    "excise-tax", "foreign-tax-credit", "gift-tax", "interest-income-tax",
    "payroll-tax", "property-tax",
]
BATCH2 = [
    "sales-tax-addon", "social-security-tax", "specific-duty", "tax-on-discount",
    "vat-from-exclusive", "withholding-tax",
]

HELPER = (
    MARK + "function __tbReq(ids,names){"
    "for(var i=0;i<ids.length;i++){"
    "var el=document.getElementById(ids[i]);var v=el?el.value:'';"
    "if(v===''||v==null||!isFinite(parseFloat(v))){"
    "ToolBox.setResult('result','<p class=\"tip-error\">请填写「'+names[i]+'」后再计算。</p>');"
    "return false;}}return true;}"
)


def clean_label(txt):
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = re.sub(r"\s*[（(][^）)]*[）)]\s*", "", txt)
    return txt.strip()


def required_fields(html):
    """按页面出现顺序取 number 输入及其 label。"""
    labels = {}
    for m in re.finditer(r'<label[^>]*for="([^"]+)"[^>]*>([\s\S]*?)</label>', html):
        labels[m.group(1)] = clean_label(m.group(2))
    out = []
    for m in re.finditer(r"<input[^>]*>", html):
        tag = m.group(0)
        idm = re.search(r'id="([^"]+)"', tag)
        typ = (re.search(r'type="([^"]*)"', tag) or [None, "text"])[1].lower()
        if not idm or typ != "number":
            continue
        out.append((idm.group(1), labels.get(idm.group(1), idm.group(1))))
    return out


def patch(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if MARK in html:
        return "skip(已改)"
    fields = required_fields(html)
    if not fields:
        return "skip(无 number 输入)"
    sig = "function calcTool(){"
    if sig not in html:
        return "skip(无 calcTool)"
    ids = "[" + ",".join("'%s'" % i for i, _ in fields) + "]"
    names = "[" + ",".join("'%s'" % n.replace("'", "\\'") for _, n in fields) + "]"
    guard = sig + "\n   if(!__tbReq(%s,%s))return;" % (ids, names)
    html = html.replace(sig, HELPER + "\n" + guard, 1)
    path.write_text(html, encoding="utf-8")
    return "patched(%d fields: %s)" % (len(fields), ", ".join(i for i, _ in fields))


def main():
    targets = BATCH1 + BATCH2 if "--all" in sys.argv else BATCH1
    for slug in targets:
        p = ROOT / "tools" / "tax" / (slug + ".html")
        if not p.exists():
            print("%-26s MISSING" % slug)
            continue
        print("%-26s %s" % (slug, patch(p)))


if __name__ == "__main__":
    main()
