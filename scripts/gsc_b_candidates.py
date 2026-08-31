#!/usr/bin/env python3
"""GSC-B 高展示低点击筛选工具（本地执行，无外部依赖）。

用途：
1. 读取 GSC 查询导出 CSV（需含 query / page / impressions / clicks / ctr / position）
2. 按规则筛出高展示低点击样本（可配置）
3. 输出高优先级页面清单（按曝光降序），用于定向重写 description
"""

from __future__ import annotations

import argparse
import csv
import json
import io
import re
from pathlib import Path
from typing import Dict, List, Tuple


def canon(name: str) -> str:
    return re.sub(r"[\s\-_:.()（）]+", "", (name or "").strip().lower())


def normalize_fields(row: Dict[str, str]) -> Dict[str, str]:
    return {
        (k or "").lstrip("\ufeff").strip(): v for k, v in row.items()
    }


def parse_num(v: str) -> float:
    if v is None:
        return 0.0
    s = (v or "").strip()
    if not s:
        return 0.0
    if s.endswith("%"):
        try:
            return float(s[:-1].strip()) / 100.0
        except ValueError:
            return 0.0
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return 0.0


def open_csv_with_encoding(path: Path) -> Tuple[csv.DictReader, io.TextIOWrapper, str]:
    encodings = ("utf-8", "utf-8-sig", "gb18030")
    last_error = None
    for enc in encodings:
        try:
            f = path.open("r", encoding=enc, newline="")
            reader = csv.DictReader(f)
            _ = reader.fieldnames
            return reader, f, enc
        except UnicodeDecodeError as exc:
            last_error = exc
            try:
                f.close()
            except Exception:
                pass
            continue
        except Exception as exc:
            # 保留首个能复现根因的异常，避免静默吞掉非编码错误
            last_error = exc
            try:
                f.close()
            except Exception:
                pass
            continue
    raise SystemExit(f"CSV 打开失败（编码尝试: {', '.join(encodings)}），最后错误: {last_error}")

def detect_field(row: Dict[str, str], candidates: List[str], fallback: str = "") -> str:
    key_map = {canon(k): k for k in row.keys()}
    for k in candidates:
        ck = canon(k)
        if ck in key_map:
            v = row.get(key_map[ck], "")
            if v and v.strip():
                return v.strip()
    return fallback


def ensure_required_fields(headers: List[str]) -> None:
    keys = [canon(h) for h in headers if h]
    groups = {
        "query": {
            "query", "queries", "querytext", "searchquery", "searchterm",
            "搜索词", "查询", "查询词", "查询短语", "searchterm", "搜索查询", "关键词", "检索词", "关键词词组",
        },
        "page": {
            "page", "url", "landingpage", "dimensionurl", "destinationurl",
            "网页", "页面", "页面地址", "目标页面", "目标url", "url地址", "着陆页url", "页面url", "目标页面url", "网址",
        },
        "impressions": {
            "impressions", "queryimpressions", "queryimpression", "clicksimpressions", "impressionsclicks",
            "展示次数", "曝光次数", "曝光", "展现次数", "展示量", "展示", "展现量", "曝光量", "impressions",
        },
        "clicks": {
            "clicks", "queryclicks", "clickclicks",
            "点击次数", "点击数", "点击", "点击量",
        },
        "ctr": {
            "ctr", "clickratio", "queryctr",
            "点击率", "点击率（%）", "点击率百分比", "clickrate",
        },
        "position": {
            "position", "avgposition", "queryposition", "平均排名", "平均位次", "平均位置",
        },
    }

    missing = []
    for name, aliases in groups.items():
        if not (aliases & set(keys)):
            missing.append(name)
    if missing:
        print("警告: 未识别到部分关键字段，可能导致空结果：")
        print("  缺失: " + ", ".join(missing))
        print("  当前表头: " + ", ".join(headers[:60]))


def main() -> None:
    ap = argparse.ArgumentParser(description="高展示低点击候选页提取（GSC-B）")
    ap.add_argument("--csv", required=True, help="GSC 查询导出 CSV 文件路径")
    ap.add_argument("--out", default="gsc_b_candidates", help="输出文件前缀（默认: gsc_b_candidates）")
    ap.add_argument("--min-impressions", type=float, default=800, help="高展示下限（默认 800）")
    ap.add_argument("--max-ctr", type=float, default=0.04, help="CTR 上限（默认 0.04）")
    ap.add_argument("--max-position", type=float, default=None, help="可选：仅保留平均排名 <= 该值")
    ap.add_argument("--top", type=int, default=200, help="默认输出的 URL 数量（默认 200）")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    out_prefix = Path(args.out)

    if not csv_path.exists():
        raise SystemExit(f"CSV 文件不存在: {csv_path}")

    raw_rows: List[Dict[str, object]] = []
    reader, fobj, encoding = open_csv_with_encoding(csv_path)
    with fobj:
        if not reader.fieldnames:
            raise SystemExit(f"CSV 缺少表头: {csv_path}")
        # 按字段名宽松匹配：query/page/impressions/clicks/ctr/position
        print("检测到表头: "+", ".join(reader.fieldnames[:40]))
        print(f"使用编码: {encoding}")
        ensure_required_fields(reader.fieldnames)
        for row in reader:
            row = normalize_fields(row)
            query = detect_field(row, [
                "query", "queries", "querytext", "searchquery", "searchterm", "查询", "查询词", "搜索查询", "关键词", "搜索词", "检索词", "queryterm",
            ])
            page = detect_field(row, [
                "page", "url", "landingpage", "dimensionurl", "destinationurl", "目标页面", "着陆页url", "网页", "页面", "页面url", "目标url", "url地址"
            ])
            impressions = parse_num(detect_field(row, [
                "impressions", "queryimpressions", "queryimpression", "clicksimpressions", "impressionsclicks",
                "展示次数", "曝光次数", "曝光", "展现次数", "展示量", "展现量", "曝光量"
            ]))
            clicks = parse_num(detect_field(row, [
                "clicks", "queryclicks", "clickclicks", "点击次数", "点击数", "点击", "点击量"
            ]))
            ctr = parse_num(detect_field(row, ["ctr", "clickratio", "queryctr", "点击率", "点击率（%）", "点击率百分比", "clickrate"]))
            position = parse_num(detect_field(row, [
                "position", "avgposition", "queryposition", "平均排名", "平均位次", "平均位置"
            ]))

            if not (page and query):
                continue
            raw_rows.append({
                "query": query,
                "page": page,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr,
                "position": position,
            })

    candidates = []
    url_map: Dict[str, Dict[str, object]] = {}

    for r in raw_rows:
        if r["impressions"] < args.min_impressions:
            continue
        if r["ctr"] > args.max_ctr:
            continue
        if args.max_position is not None and r["position"] > args.max_position:
            continue

        candidates.append(r)
        info = url_map.setdefault(r["page"], {
            "page": r["page"],
            "impressions": 0.0,
            "clicks": 0.0,
            "position_sum": 0.0,
            "position_count": 0,
            "worst_ctr": 1.0,
            "worst_query": "",
            "worst_ctr_impr": 0.0,
            "queries": 0,
        })
        info["impressions"] = float(info["impressions"]) + r["impressions"]
        info["clicks"] = float(info["clicks"]) + r["clicks"]
        if r["position"] > 0:
            info["position_sum"] = float(info["position_sum"]) + r["position"]
            info["position_count"] = int(info["position_count"]) + 1
        if r["ctr"] < float(info["worst_ctr"]):
            info["worst_ctr"] = r["ctr"]
            info["worst_query"] = r["query"]
            info["worst_ctr_impr"] = r["impressions"]
        info["queries"] = int(info["queries"]) + 1

    aggregated = []
    for info in url_map.values():
        impressions = float(info["impressions"])
        clicks = float(info["clicks"])
        if impressions <= 0:
            continue
        pos_count = int(info["position_count"])
        avg_pos = (float(info["position_sum"]) / pos_count) if pos_count else 0.0
        agg_ctr = clicks / impressions if impressions else 0.0
        aggregated.append({
            "page": info["page"],
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round(agg_ctr, 6),
            "avg_position": round(avg_pos, 2),
            "queries": int(info["queries"]),
            "worst_ctr": float(info["worst_ctr"]),
            "worst_query": info["worst_query"],
            "worst_query_impressions": float(info["worst_ctr_impr"]),
        })

    aggregated.sort(key=lambda x: x["impressions"], reverse=True)
    top_urls = aggregated[: args.top]

    out_urls_csv = out_prefix.with_suffix(".urls.csv")
    with out_urls_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["page", "impressions", "clicks", "ctr", "avg_position", "queries", "worst_ctr", "worst_query", "worst_query_impressions"],
        )
        w.writeheader()
        for row in top_urls:
            w.writerow({
                "page": row["page"],
                "impressions": int(row["impressions"]),
                "clicks": int(row["clicks"]),
                "ctr": f"{row['ctr']:.4%}",
                "avg_position": row["avg_position"],
                "queries": row["queries"],
                "worst_ctr": f"{row['worst_ctr']:.4%}",
                "worst_query": row["worst_query"],
                "worst_query_impressions": int(row["worst_query_impressions"]),
            })

    out_rows_csv = out_prefix.with_suffix(".rows.csv")
    with out_rows_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["query", "page", "impressions", "clicks", "ctr", "position"])
        w.writeheader()
        for r in candidates:
            w.writerow({
                "query": r["query"],
                "page": r["page"],
                "impressions": int(r["impressions"]),
                "clicks": int(r["clicks"]),
                "ctr": f"{r['ctr']:.4%}",
                "position": round(r["position"], 2) if r["position"] else 0.0,
            })

    out_json = out_prefix.with_suffix(".json")
    with out_json.open("w", encoding="utf-8") as f:
        json.dump({
            "source_csv": str(csv_path),
            "filters": {
                "min_impressions": args.min_impressions,
                "max_ctr": args.max_ctr,
                "max_position": args.max_position,
                "top": args.top,
            },
            "totals": {
                "raw_rows": len(raw_rows),
                "candidate_rows": len(candidates),
                "candidate_urls": len(aggregated),
            },
            "urls": top_urls,
        }, f, ensure_ascii=False, indent=2)

    print(f"原始行数: {len(raw_rows)}")
    print(f"通过高展示低点击过滤: {len(candidates)} 行")
    print(f"涉及 URL 数: {len(aggregated)}")
    if len(raw_rows) == 0:
        print("提示: 未命中任何有效行。请确认 CSV 是否为 Query-level 导出，并检查字段名是否包含 query/page/impressions/clicks/ctr/position。")
    print("前几条: ")
    for row in top_urls[:20]:
        print(f"- {row['page']} | 曝光 {int(row['impressions'])} | CTR {row['ctr']:.2%} | 平均位次 {row['avg_position']:.2f}")

    print("已输出:")
    print(f"- {out_urls_csv}")
    print(f"- {out_rows_csv}")
    print(f"- {out_json}")


if __name__ == "__main__":
    main()
