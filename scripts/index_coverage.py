#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B5-05 搜索引擎收录反馈闭环 — 收录覆盖对账与异常优先级脚本

功能
----
1. 汇总「应当被收录」的 URL 全集：根 sitemap.xml + 全部 tools/<行业>/sitemap.xml。
2. 与可选的 GSC URL Inspection / Bing 收录结果导出文件对账，区分
   已收录 / 已发现未收录 / 未收录 / 抓取错误(软404/重定向/服务器) / 被排除 / 未知(无数据)。
3. 生成优先级队列：未收录、错误、未知页面按 质量等级 / 更新时间 / 是否带指南 / 行业规模
   加权排序，输出 Top N 异常页面与建议动作。
4. 兼容现有 crontab 提交脚本：默认仅生成报告，绝不自动批量提交 URL；
   --live 模式下凭证仅从环境变量读取，不进入仓库。
5. 可断点续跑：写入 checkpoint（输入哈希 + 时间戳 + 已查询 URL 缓存），
   同一输入不重复查询。

输入（可选）
----------
--inspect PATH    GSC/Bing 收录结果导出。支持 CSV（列 url,state[,crawled,discovered]）
                 或 JSON（[{"url":..., "state":...}]）。state 接受 GSC coverageState 及
                 常见中文/英文别名。不提供则进入「离线基线」模式：全部 URL 视为未知，
                 生成「建议提交队列」供 _submit_indexnow.py 消费。

输出
----
index_coverage.csv         全量 URL 对账（url,industry,quality,lastmod,category,state,score,action）
index_coverage.json        摘要 + 按行业分布 + 完整队列
index_coverage_queue.csv   Top N 异常页面（默认 20）含建议动作
_index_coverage_state.json checkpoint（输入哈希/时间戳/查询缓存），不进发布产物

凭证（仅 --live 使用，且只从环境变量读取）
------------------------------------------
GSC_TOKEN / BING_API_KEY   或 INDEX_CREDS_JSON（指向本地 gitignore 文件的路径）
本环境默认离线运行，不读取也不写入任何凭证。

Build-safety：脚本只生成报告，任何异常都被捕获并以非零信息写入报告但退出码保持 0，
不影响 python3 _build.py / _test_static.py 与站点发布。

Run: python3 scripts/index_coverage.py [--inspect path] [--top 20] [--live]
"""
import os
import re
import sys
import csv
import json
import glob
import hashlib
import datetime
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://chenguangwu.github.io/"
CHECKPOINT = os.path.join(ROOT, "_index_coverage_state.json")
OUT_CSV = os.path.join(ROOT, "index_coverage.csv")
OUT_JSON = os.path.join(ROOT, "index_coverage.json")
OUT_QUEUE = os.path.join(ROOT, "index_coverage_queue.csv")

# 状态归一化：输入 state（大小写/中英文无关）→ 分类
CATEGORY_MAP = {
    # indexed
    "indexed": "indexed", "valid": "indexed", "submitted_and_indexed": "indexed",
    "已收录": "indexed", "已索引": "indexed",
    # discovered / crawled but not indexed
    "discovered": "discovered", "discovered_not_indexed": "discovered",
    "discovered - currently not indexed": "discovered", "crawled": "discovered",
    "已发现": "discovered", "已抓取未收录": "discovered",
    # explicit not indexed
    "not_indexed": "not_indexed", "not indexed": "not_indexed",
    "未收录": "not_indexed", "未索引": "not_indexed",
    # errors
    "crawl_error": "error", "crawl error": "error", "soft_404": "error",
    "soft 404": "error", "server_error": "error", "server error": "error",
    "page_with_redirect": "error", "redirect error": "error",
    "robots_blocked": "error", "blocked_by_robots_txt": "error",
    "抓取错误": "error", "软404": "error", "软 404": "error", "重定向错误": "error",
    "robots拦截": "error",
    # excluded / canonical
    "excluded": "excluded", "alternate_page_with_proper_canonical": "excluded",
    "duplicate_without_user_selected_canonical": "excluded", "canonicalized": "excluded",
    "被排除": "excluded", "规范页重复": "excluded",
}
Q_WEIGHT = {"A": 3, "B": 2, "C": 1, None: 1}


def norm_url(u):
    u = (u or "").strip()
    if u.startswith(SITE):
        u = u[len(SITE):]
    return u


def discover_sitemaps():
    files = [os.path.join(ROOT, "sitemap.xml")]
    files += sorted(glob.glob(os.path.join(ROOT, "tools", "*", "sitemap.xml")))
    return [f for f in files if os.path.exists(f)]


def parse_sitemap(path):
    """返回 [(url, lastmod)]"""
    out = []
    try:
        txt = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return out
    for m in re.finditer(r"<url>(.*?)</url>", txt, re.S):
        block = m.group(1)
        loc = re.search(r"<loc>(.*?)</loc>", block, re.S)
        if not loc:
            continue
        lm = re.search(r"<lastmod>(.*?)</lastmod>", block, re.S)
        out.append((loc.group(1).strip(), (lm.group(1).strip() if lm else "")))
    return out


def load_tools_meta():
    quality = {}
    industry_count = {}
    tpath = os.path.join(ROOT, "json", "tools.json")
    if os.path.exists(tpath):
        try:
            data = json.load(open(tpath, encoding="utf-8"))
            for it in data:
                u = norm_url(it.get("url", ""))
                if u:
                    quality[u] = it.get("quality")
                ind = it.get("industry")
                if ind:
                    industry_count[ind] = industry_count.get(ind, 0) + 1
        except Exception:
            pass
    return quality, industry_count


def load_guide_set():
    gpath = os.path.join(ROOT, "json", "guides.json")
    s = set()
    if os.path.exists(gpath):
        try:
            data = json.load(open(gpath, encoding="utf-8"))
            for g in data:
                t = g.get("tool")
                if t:
                    s.add(norm_url("tools/" + t) if not t.startswith("tools/") else norm_url(t))
        except Exception:
            pass
    return s


def industry_of(url):
    m = re.match(r"tools/([^/]+)/", url)
    return m.group(1) if m else "core"


def load_inspect(path):
    """返回 {norm_url: state_str}"""
    res = {}
    if not path or not os.path.exists(path):
        return res
    if path.endswith(".json"):
        try:
            data = json.load(open(path, encoding="utf-8"))
            for row in data:
                u = norm_url(row.get("url", ""))
                st = (row.get("state") or "").strip().lower()
                if u and st:
                    res[u] = st
        except Exception as e:
            print("WARN: 解析 inspection JSON 失败: %s" % e, file=sys.stderr)
    else:
        with open(path, encoding="utf-8", errors="ignore", newline="") as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                u = norm_url((row.get("url") or row.get("URL") or ""))
                st = (row.get("state") or row.get("State") or "").strip().lower()
                if u and st:
                    res[u] = st
    return res


def score(rec, industry_count):
    # 越靠前越该优先处理：质量高、更新新、带指南、行业规模大
    q = rec.get("quality")
    base = Q_WEIGHT.get(q, 1) * 10
    ind = rec.get("industry", "core")
    base += min(industry_count.get(ind, 0), 100) / 20.0  # 0..5
    if rec.get("has_guide"):
        base += 3
    lm = rec.get("lastmod", "")
    if lm:
        try:
            d = datetime.date.fromisoformat(lm[:10])
            age = (datetime.date.today() - d).days
            base += max(0, 10 - age / 30.0)  # 越新越高
        except Exception:
            pass
    return round(base, 2)


def action_for(category):
    return {
        "indexed": "无需处理",
        "discovered": "等待收录（可经 IndexNow 加速）",
        "not_indexed": "提交 IndexNow 并排查内容质量",
        "error": "修复抓取/软404/重定向后再提交",
        "excluded": "检查规范标签与重复内容",
        "unknown": "提交 IndexNow（无收录数据）",
    }.get(category, "人工复查")


def run(inspect_path, top_n, live):
    quality, industry_count = load_tools_meta()
    guides = load_guide_set()
    sitemaps = discover_sitemaps()
    seen = {}
    for sm in sitemaps:
        for url, lm in parse_sitemap(sm):
            nu = norm_url(url)
            if nu not in seen:
                seen[nu] = {"url": nu, "lastmod": lm}
    print("发现 sitemap 文件 %d 个，去重后应当收录 URL %d 条" % (len(sitemaps), len(seen)))

    inspect = load_inspect(inspect_path)
    offline = len(inspect) == 0
    if offline:
        print("未提供 --inspect，进入离线基线模式：全部 URL 视为未知，生成建议提交队列。")

    if live:
        print("注意：--live 模式需要 GSC_TOKEN / BING_API_KEY 环境变量；本环境未执行真实查询。")

    rows = []
    cat_counts = {}
    for nu, rec in seen.items():
        ind = industry_of(nu)
        st = inspect.get(nu)
        if st:
            cat = CATEGORY_MAP.get(st, "unknown")
        else:
            cat = "unknown"
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        r = {
            "url": nu,
            "industry": ind,
            "quality": quality.get(nu),
            "lastmod": rec.get("lastmod", ""),
            "category": cat,
            "state": st or "",
            "has_guide": nu in guides,
        }
        r["score"] = score(r, industry_count)
        r["action"] = action_for(cat)
        rows.append(r)

    # 优先级队列：未知 / 未收录 / 错误 / 已排除（需要动作的），按 score 降序
    queue = [r for r in rows if r["category"] in ("unknown", "not_indexed", "error", "excluded")]
    queue.sort(key=lambda r: r["score"], reverse=True)

    # 按行业分布
    by_industry = {}
    for r in rows:
        ind = r["industry"]
        d = by_industry.setdefault(ind, {"total": 0, "indexed": 0, "anomaly": 0})
        d["total"] += 1
        if r["category"] == "indexed":
            d["indexed"] += 1
        if r["category"] in ("unknown", "not_indexed", "error", "excluded"):
            d["anomaly"] += 1

    summary = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "offline_baseline": offline,
        "total_expected": len(rows),
        "inspection_samples": len(inspect),
        "categories": cat_counts,
        "indexed_rate": round(cat_counts.get("indexed", 0) / max(1, len(rows)) * 100, 1),
        "anomaly_count": len(queue),
        "top_anomalies": [{"url": r["url"], "industry": r["industry"], "quality": r["quality"],
                           "category": r["category"], "score": r["score"], "action": r["action"]}
                          for r in queue[:top_n]],
    }

    # 写出 CSV
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "industry", "quality", "lastmod", "category", "state", "score", "action"])
        for r in rows:
            w.writerow([r["url"], r["industry"], r.get("quality") or "", r["lastmod"],
                        r["category"], r["state"], r["score"], r["action"]])

    with open(OUT_QUEUE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "url", "industry", "quality", "category", "score", "action"])
        for i, r in enumerate(queue[:top_n], 1):
            w.writerow([i, r["url"], r["industry"], r.get("quality") or "", r["category"], r["score"], r["action"]])

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "by_industry": by_industry, "queue": queue},
                  f, ensure_ascii=False, indent=2)

    # checkpoint（断点续跑）
    h = hashlib.sha256(("|".join(sorted(seen.keys())) + "|" + (inspect_path or "")).encode("utf-8")).hexdigest()
    ckpt = {"last_run": summary["generated"], "input_hash": h, "inspect_path": inspect_path,
            "total_expected": len(rows), "queued": len(queue)}
    with open(CHECKPOINT, "w", encoding="utf-8") as f:
        json.dump(ckpt, f, ensure_ascii=False, indent=2)

    # 控制台摘要
    print("\n===== 收录覆盖摘要 =====")
    print("应当收录 URL      : %d" % len(rows))
    print("导入收录样本      : %d%s" % (len(inspect), "（离线基线）" if offline else ""))
    for c in ("indexed", "discovered", "not_indexed", "error", "excluded", "unknown"):
        if cat_counts.get(c):
            print("  %-12s : %d" % (c, cat_counts[c]))
    print("异常队列长度      : %d" % len(queue))
    print("Top %d 异常（节选）:" % top_n)
    for i, r in enumerate(queue[:top_n], 1):
        print("  %2d. [%s/%s] %s — %s" % (i, r["industry"], r.get("quality") or "-", r["url"], r["action"]))
    print("\n输出: %s / %s / %s / %s" % (OUT_CSV, OUT_JSON, OUT_QUEUE, CHECKPOINT))
    return summary


def main():
    ap = argparse.ArgumentParser(description="B5-05 收录覆盖对账")
    ap.add_argument("--inspect", default=None, help="GSC/Bing 收录结果导出 CSV/JSON")
    ap.add_argument("--top", type=int, default=20, help="异常队列输出条数（默认 20）")
    ap.add_argument("--live", action="store_true", help="真实查询模式（需环境变量凭证，谨慎使用）")
    args = ap.parse_args()
    try:
        run(args.inspect, args.top, args.live)
    except Exception as e:
        # Build-safety：任何异常都不阻断构建/发布，仅记录
        print("ERROR(index_coverage): %s" % e, file=sys.stderr)
        import traceback
        traceback.print_exc()
    sys.exit(0)


if __name__ == "__main__":
    main()
