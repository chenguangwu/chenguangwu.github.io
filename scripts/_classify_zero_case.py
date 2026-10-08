#!/usr/bin/env python3
"""对零用例页做「可补用例性」分类，避免对结构性不可能的页面做无用功。
分类（按能否构造出「有判别力的派生输出锚点」）：
  A 确定性·有输入   —— 最高价值，优先补
  B 随机·有输入     —— 输出含随机，但可锚结构/统计/长度，需专门设计
  C 随机·无输入     —— 结构性难覆盖
  D 无输入·无随机   —— 可能是纯参考表/文本工具（textarea 另计）
  E 纯展示/无脚本逻辑
用法: python3 scripts/_classify_zero_case.py
"""
import os, re, json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

zero = [l for l in open("/tmp/zero_case_all.txt").read().split("\n") if l]

RAND = re.compile(r"Math\.random|crypto\.getRandomValues|Math\.floor\(Math\.random")
INPUT_RE = re.compile(r"<input\b", re.I)
SEL_RE = re.compile(r"<select\b", re.I)
TA_RE = re.compile(r"<textarea\b", re.I)
CANVAS_RE = re.compile(r"<canvas\b", re.I)

buckets = defaultdict(list)
rows = []
for slug in zero:
    p = os.path.join(TOOLS, slug + ".html")
    try:
        html = open(p, encoding="utf8", errors="ignore").read()
    except OSError:
        buckets["E"].append(slug)
        continue
    ni = len(INPUT_RE.findall(html))
    ns = len(SEL_RE.findall(html))
    nt = len(TA_RE.findall(html))
    inputs = ni + ns + nt
    rand = bool(RAND.search(html))
    canvas = bool(CANVAS_RE.search(html))
    if rand and inputs >= 1:
        k = "B"
    elif rand and inputs == 0:
        k = "C"
    elif inputs >= 1:
        k = "A"
    elif nt >= 1:
        k = "D"
    else:
        k = "E"
    buckets[k].append(slug)
    rows.append((slug, k, inputs, rand, canvas))

DESC = {
    "A": "确定性·有输入（最高价值，优先补）",
    "B": "随机·有输入（锚结构/长度，需专门设计）",
    "C": "随机·无输入（结构性难覆盖）",
    "D": "无输入·无随机（参考表/文本类）",
    "E": "纯展示/无输入无脚本逻辑",
}
print("=" * 70)
tot = len(zero)
for k in "ABCDE":
    n = len(buckets[k])
    print(f"  {k}  {DESC[k]:34} {n:4}  ({n/tot*100:.1f}%)")
print("=" * 70)
print(f"  合计 {tot}")
print("\nA 类行业分布 TOP20：")
by = defaultdict(list)
for slug in buckets["A"]:
    by[slug.split("/")[0]].append(slug)
for ind, ps in sorted(by.items(), key=lambda kv: -len(kv[1]))[:20]:
    print(f"  {ind:22} {len(ps)}")

# 输出 A 类清单（按行业分组，便于分批）
for k in ("A", "B", "D"):
    open(f"/tmp/zero_{k}.txt", "w").write("\n".join(buckets[k]))
print("\n清单已写出: /tmp/zero_A.txt /tmp/zero_B.txt /tmp/zero_D.txt")
json.dump({k: v for k, v in buckets.items()}, open("/tmp/zero_buckets.json", "w"), ensure_ascii=False)
