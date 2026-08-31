#!/usr/bin/env python3
"""GSC-B 候选页筛选脚本（多源统一入口）

用途：
1. 读取查询级导出 CSV（GSC / 百度统计 / 51.la / Clarity）
2. 按统一规则抽取 query/page/impressions/clicks/ctr/position
3. 筛出高展示低点击候选页，输出三类文件：
   - {prefix}.urls.csv    按 page 维度聚合后前 N 条
   - {prefix}.rows.csv    原始明细
   - {prefix}.json        审计摘要

说明：
  - 通过 `--source` 选择预置映射；
  - 通过 `--map-json` 可覆盖或扩展字段映射；
  - 未命中 query 的场景可继续运行，输出时会写入空值并给出告警。
"""

from __future__ import annotations

import argparse
import csv
import json
import io
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any


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
    # 容忍千分位与空格
    s = s.replace(",", "").replace(" ", "")
    try:
        return float(s)
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
        except Exception as exc:
            last_error = exc
            try:
                f.close()
            except Exception:
                pass
    raise SystemExit(f"CSV 打开失败（编码尝试: {', '.join(encodings)}），最后错误: {last_error}")


def detect_field(
    row: Dict[str, str],
    candidates: List[str],
    fallback: str = "",
) -> str:
    if not row:
        return fallback
    key_map = {canon(k): k for k in row.keys()}
    for k in candidates:
        ck = canon(k)
        if ck in key_map:
            v = row.get(key_map[ck], "")
            if v is not None and str(v).strip():
                return str(v).strip()
    return fallback


def score_source(row_keys: List[str], aliases: Dict[str, List[str]]) -> int:
    ks = {canon(k): 1 for k in row_keys}
    score = 0
    for alias_list in aliases.values():
        for alias in alias_list:
            if canon(alias) in ks:
                score += 1
                break
    return score


def build_alias_profiles() -> Dict[str, Dict[str, List[str]]]:
    return {
        "gsc": {
            "query": [
                "query", "queries", "querytext", "searchquery", "searchterm", "searchterm", "queryterm",
                "查询", "查询词", "搜索查询", "关键词", "检索词",
            ],
            "page": [
                "page", "url", "landingpage", "dimensionurl", "destinationurl",
                "页面", "页面地址", "网页", "目标页面", "着陆页url", "页面url", "目标url", "url地址",
            ],
            "impressions": [
                "impressions", "queryimpressions", "queryimpression", "impressionscount",
                "展示次数", "曝光次数", "曝光", "展现次数", "展示量", "展现量", "曝光量",
            ],
            "clicks": [
                "clicks", "queryclicks", "clickclicks",
                "点击次数", "点击数", "点击量",
            ],
            "ctr": [
                "ctr", "clickratio", "queryctr",
                "点击率", "点击率（%）", "点击率百分比", "clickrate",
            ],
            "position": [
                "position", "avgposition", "queryposition",
                "平均排名", "平均位次", "平均位置",
            ],
        },
        "baidu": {
            "query": [
                "query", "keyword", "queryword", "searchword", "searchkey", "searchterm",
                "搜索词", "关键词", "查询词", "query_word", "keyword_name",
            ],
            "page": [
                "page", "url", "landingpage", "dimension_url", "targeturl", "dimensionurl",
                "页面", "页面名称", "页面地址", "着陆页", "目标页面", "页面URL", "网页",
            ],
            "impressions": [
                "impressions", "pv", "pageviews", "pv_count", "访问量", "展现量", "浏览量", "show",
            ],
            "clicks": [
                "clicks", "uv", "click", "访问次数", "点击次数", "点击量",
            ],
            "ctr": [
                "ctr", "ctr%",
                "点击率", "点击率（%）", "点击率百分比",
            ],
            "position": [
                "position", "avgposition", "avg_position", "avgpos", "平均排名", "平均位次",
            ],
        },
        "51la": {
            "query": [
                "query", "keyword", "searchword", "searchquery", "term", "keywords", "search_term",
                "搜索词", "关键词", "查询词", "查询",
            ],
            "page": [
                "page", "url", "landingpage", "path", "page_url", "pv_url", "目标页面",
                "页面", "页面地址", "网页", "着陆页", "入口页",
            ],
            "impressions": [
                "impressions", "pv", "pv_count", "visits", "visit_count", "页面访问", "浏览量",
                "访问次数", "访问量", "访客数", "uv",
            ],
            "clicks": [
                "clicks", "click_count", "点击量", "点击次数",
            ],
            "ctr": [
                "ctr", "clickrate", "点击率", "点击率（%）", "ctr%",
            ],
            "position": [
                "position", "avgposition", "avg_position", "avg_positioning", "平均排名", "排名",
            ],
        },
        "clarity": {
            "query": [
                "query", "keyword", "searchterm", "search query", "eventname", "tag",
                "event", "来源查询", "搜索词",
            ],
            "page": [
                "url", "page", "pagename", "path", "pathname", "页面", "页面url", "着陆页",
            ],
            "impressions": [
                "sessions", "traffic", "sessionCount", "totalSessionCount", "visitorCount", "visits", "访问量", "会话数",
                "impressions", "totalTraffic",
            ],
            "clicks": [
                "clicks", "deadClickCount", "excessiveScroll", "rageClickCount",
                "quickbackClick", "errorClickCount", "点击量",
            ],
            "ctr": [
                "ctr", "conversion", "clickRatio", "点击率", "点击率（%）",
            ],
            "position": [
                "position", "rank", "avgRank", "avg_position",
            ],
        },
    }


def build_default_profile() -> Dict[str, List[str]]:
    merged: Dict[str, List[str]] = {}
    for profile in build_alias_profiles().values():
        for k, v in profile.items():
            merged.setdefault(k, []).extend(v)
    # 去重，保留顺序
    return {k: sorted(set(v)) for k, v in merged.items()}


def merge_mapping(
    preset: str,
    map_json: Path | None,
) -> Dict[str, List[str]]:
    profiles = build_alias_profiles()
    if preset == "auto":
        aliases = build_default_profile()
    elif preset not in profiles:
        aliases = build_default_profile()
    else:
        aliases = {k: list(v) for k, v in profiles[preset].items()}

    if map_json:
        with map_json.open("r", encoding="utf-8") as f:
            custom = json.load(f)
        if not isinstance(custom, dict):
            raise SystemExit("map-json 必须是一个 JSON 对象，键是 query/page/impressions/clicks/ctr/position")
        for key, val in custom.items():
            if key not in {"query", "page", "impressions", "clicks", "ctr", "position"}:
                continue
            if isinstance(val, list):
                aliases[key] = val + aliases.get(key, [])
            elif isinstance(val, str):
                aliases[key] = [val] + aliases.get(key, [])
            else:
                raise SystemExit(f"map-json 中 {key} 配置应为字符串或字符串列表")
        aliases = {k: list(dict.fromkeys(v)) for k, v in aliases.items()}

    return aliases


def pick_required_fields(aliases: Dict[str, List[str]], headers: List[str]) -> None:
    keys = [canon(h) for h in headers if h]
    groups = {
        "query": aliases.get("query", []),
        "page": aliases.get("page", []),
        "impressions": aliases.get("impressions", []),
        "clicks": aliases.get("clicks", []),
        "ctr": aliases.get("ctr", []),
        "position": aliases.get("position", []),
    }
    missing = []
    for name, alias_list in groups.items():
        if not any(canon(a) in keys for a in alias_list):
            missing.append(name)
    if missing:
        print("警告: 未识别到部分关键字段，可能导致空结果：")
        print("  缺失: " + ", ".join(missing))
        print("  当前表头: " + ", ".join(headers[:60]))


def infer_source(aliases: Dict[str, Dict[str, List[str]]], headers: List[str]) -> str:
    best = "custom"
    best_score = -1
    for name, profile in aliases.items():
        score = score_source(headers, profile)
        if score > best_score:
            best = name
            best_score = score
    return best if best_score > 0 else "custom"


def main() -> None:
    ap = argparse.ArgumentParser(description="高展示低点击候选页提取（GSC-B 多源版）")
    ap.add_argument("--csv", required=True, help="查询级导出 CSV 文件路径")
    ap.add_argument("--out", default="gsc_b_candidates", help="输出文件前缀（默认: gsc_b_candidates）")
    ap.add_argument("--source", default="auto", choices=["auto", "gsc", "baidu", "51la", "clarity"], help="字段映射源（默认 auto）")
    ap.add_argument("--map-json", dest="map_json", help="可选自定义映射 JSON（覆盖字段别名）")
    ap.add_argument("--min-impressions", type=float, default=800, help="高展示下限（默认 800）")
    ap.add_argument("--max-ctr", type=float, default=0.04, help="CTR 上限（默认 0.04）")
    ap.add_argument("--max-position", type=float, default=None, help="可选：仅保留平均排名 <= 该值")
    ap.add_argument("--top", type=int, default=200, help="默认输出的 URL 数量（默认 200）")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    out_prefix = Path(args.out)
    if not csv_path.exists():
        raise SystemExit(f"CSV 文件不存在: {csv_path}")

    map_json = Path(args.map_json) if args.map_json else None
    if map_json and not map_json.exists():
        raise SystemExit(f"自定义映射文件不存在: {map_json}")

    # auto 模式下尝试自动判定来源，再按来源重建别名；否则直接使用指定来源
    if args.source == "auto":
        # 先用默认映射读头推断来源
        probe_reader, probe_fobj, _ = open_csv_with_encoding(csv_path)
        with probe_fobj:
            if not probe_reader.fieldnames:
                raise SystemExit(f"CSV 缺少表头: {csv_path}")
            guessed = infer_source(build_alias_profiles(), probe_reader.fieldnames)
        source = guessed if guessed in build_alias_profiles() else "custom"
        aliases = merge_mapping(source, map_json)
    else:
        source = args.source
        aliases = merge_mapping(source, map_json)
        # 打开一次拿 header 用于提示
        probe_reader, probe_fobj, _ = open_csv_with_encoding(csv_path)
        with probe_fobj:
            if not probe_reader.fieldnames:
                raise SystemExit(f"CSV 缺少表头: {csv_path}")

    # 正式读取
    reader, fobj, encoding = open_csv_with_encoding(csv_path)
    with fobj:
        if not reader.fieldnames:
            raise SystemExit(f"CSV 缺少表头: {csv_path}")
        print(f"检测到表头: {', '.join(reader.fieldnames[:40])}")
        print(f"使用编码: {encoding}")
        print(f"使用源映射: {source}")
        pick_required_fields(reader.fieldnames, aliases)

        raw_rows: List[Dict[str, Any]] = []
        missing_query = 0
        missing_page = 0

        for row in reader:
            row = normalize_fields(row)
            query = detect_field(row, aliases.get("query", []))
            page = detect_field(row, aliases.get("page", []))
            impressions = parse_num(detect_field(row, aliases.get("impressions", [])))
            clicks = parse_num(detect_field(row, aliases.get("clicks", [])))
            ctr_val = parse_num(detect_field(row, aliases.get("ctr", [])))
            if ctr_val == 0.0 and impressions > 0:
                derived_ctr = clicks / impressions
                # 明确来源于衍生，仍保留在 0 附近
                ctr_val = derived_ctr if derived_ctr <= 1 else 0.0
            position = parse_num(detect_field(row, aliases.get("position", [])))

            if not page:
                missing_page += 1
                continue
            if not query:
                missing_query += 1

            raw_rows.append({
                "query": query or "",
                "page": page,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr_val,
                "position": position,
            })

    if missing_query:
        print(f"提示: 有 {missing_query} 行缺少 query 字段（将保留空字符串并继续处理）")
    if missing_page:
        print(f"提示: 有 {missing_page} 行缺少 page 字段（已跳过）")

    candidates: List[Dict[str, Any]] = []
    url_map: Dict[str, Dict[str, Any]] = {}

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

    aggregated: List[Dict[str, Any]] = []
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
    top_urls = aggregated[:args.top]

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
            "source": source,
            "source_csv": str(csv_path),
            "mapping": {k: aliases.get(k, []) for k in ["query", "page", "impressions", "clicks", "ctr", "position"]},
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
        print("提示: 未命中任何有效行。请确认 CSV 为 query-level 导出，并检查字段映射是否匹配。")
    print("前几条: ")
    for row in top_urls[:20]:
        print(f"- {row['page']} | 曝光 {int(row['impressions'])} | CTR {row['ctr']:.2%} | 平均位次 {row['avg_position']:.2f}")

    print("已输出:")
    print(f"- {out_urls_csv}")
    print(f"- {out_rows_csv}")
    print(f"- {out_json}")


if __name__ == "__main__":
    main()
