#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""英文元数据退化门禁（2026-11-05）。

背景：`scripts/gen_en_override.py` 曾用 slug title-case / 单通用词 / 固定套话兜底，
造成 674 页 `title-en` 退化（`generator-35` -> `Generator 35`、`财务模型` -> `Finance`）。
本门禁扫描 `i18n/tools/_en_override.json` 的英文值，六类成因各自判红：

  P1 numbered_slug     编号 slug 直接 title-case（Generator 35 / Detector 173）
  P2 single_generic    单个通用词或纯动作词（Finance / Detect / Quality）
  P3 paren_template    括号模板碎片（`- ( A / B / C )`）
  P4 hyphen_fragment   连字符拼接碎片（`X - ( ... )` 等）
  P5 slug_word_salad   slug 词堆砌、语序错乱（Assessor Water Quality）
  P6 duplicate_word    机翻相邻重复词（AST AST / Reference Reference）

用法：
  python3 scripts/audit_en_meta_degenerate.py --check            # 门禁：新退化即 exit 1
  python3 scripts/audit_en_meta_degenerate.py --report           # 只打印，不判红
  python3 scripts/audit_en_meta_degenerate.py --update-baseline  # 存量债转基线（人工确认后）
  python3 scripts/audit_en_meta_degenerate.py --self-test        # 判据自测（六类必红、合法名不红）
  python3 scripts/audit_en_meta_degenerate.py --input /tmp/x.json # 指定待扫文件（自测/演练）

基线（存量债）`scripts/en_meta_degenerate_baseline.json`：只允许减少、不允许新增；
新增条目必须修数据或登记 allowlist，禁止用 --update-baseline 掩盖回归。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERRIDE_PATH = ROOT / "i18n" / "tools" / "_en_override.json"
BASELINE_PATH = ROOT / "scripts" / "en_meta_degenerate_baseline.json"
ALLOWLIST_PATH = ROOT / "scripts" / "en_meta_allowlist.json"

# 合法单词型名称（缩写/专名），逐条在 allowlist 里登记原因
DEFAULT_ACRONYMS = {
    "bmi", "pdf", "ocr", "ip", "uuid", "json", "yaml", "csv", "qr", "sha", "md5",
    "aes", "rsa", "jwt", "base64", "regex", "cron", "utm", "emi", "sip", "roi",
    "npv", "irr", "gpa", "psqi", "gcs", "apgar", "inr", "egfr", "tds", "ppi",
    "dpi", "px", "bpm", "hrv", "ldl", "hdl", "hba1c", "ast", "alt", "bun", "crp",
    "esr", "ph", "db", "hz", "khz", "mhz", "xml", "html", "css", "url", "uri",
}

# slug 里的通用角色/设备词：出现在词首且 ≥2 段 → 语序错乱
GENERIC_ROLE = {
    "generator", "calculator", "converter", "convert", "checker", "detector",
    "analyzer", "analyser", "estimator", "assessor", "rater", "evaluator",
    "planner", "tracker", "tool", "maker", "parser", "formatter", "builder",
    "finder", "editor", "viewer", "reader", "printer", "sorter", "splitter",
    "filter", "simulator", "renderer", "mapper", "scanner", "cleaner", "counter",
    "timer", "comparator", "provider", "recommender", "analysis", "assess",
    "random", "temp", "util", "app", "template", "report", "process",
}

# 单通用词判据只认「角色词 + 抽象通用词」，避免把 Timer / Stopwatch 这类合法单词名误杀
GENERIC_SINGLE = GENERIC_ROLE | {
    "finance", "quality", "cost", "risk", "price", "budget", "density", "speed",
    "time", "value", "values", "data", "result", "results", "content", "effect",
    "activity", "flow", "guide", "support", "service", "management", "standard",
    "improvement", "optimization", "maintenance", "logistics", "payment", "tax",
    "salary", "loan", "interest", "rate", "ratio", "percent", "fraction", "score",
    "grade", "level", "size", "weight", "height", "length", "area", "volume",
    "distance", "duration", "temperature", "pressure", "energy", "power", "force",
    "torque", "transport", "competitor", "detect", "evaluate", "measure",
    "compare", "compute", "calculate", "generate", "analyze", "check", "format",
    "view", "preview", "pick", "select", "track", "estimate", "convert",
}

# 可作合法修饰语、不应触发「词堆砌」的词首词
MODIFIER_OK = {
    "random", "temp", "auto", "data", "text", "image", "color", "time", "date",
    "unit", "file", "url", "number", "json", "hex", "base64", "password", "hash",
    "code", "html", "css", "xml", "csv", "yaml", "pdf", "qr", "regex", "ip",
    "uuid", "emi", "sip", "roi", "npv", "irr", "gpa", "bmi", "app", "util",
}

BOILER = (
    "produce results instantly in your browser",
    "online utility on toolbox",
    "compute values online with accurate results",
    "convert values online with instant results",
    "check and validate inputs online",
    "compare values online with clear output",
    "run and process online in your browser",
    "format text online with instant output",
    "pick and choose options online",
    "view and preview content online",
    "encode and decode securely in your browser",
    "obfuscate and minify code online",
    "generate results online for free and instantly",
    "generate results online, free and instant",
)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def load_allowlist() -> tuple[set[str], dict[str, str]]:
    """返回 (缩写白名单, key 级豁免 {key: reason})；缩写支持 list 或 {缩写: 原因}。"""
    acronyms = set(DEFAULT_ACRONYMS)
    keys: dict[str, str] = {}
    if ALLOWLIST_PATH.exists():
        data = json.load(open(ALLOWLIST_PATH, encoding="utf-8"))
        raw = data.get("acronyms", {})
        if isinstance(raw, dict):
            acronyms |= {str(x).lower() for x in raw}
        else:
            acronyms |= {str(x).lower() for x in raw}
        keys = {str(k): str(v) for k, v in data.get("keys", {}).items()}
    return acronyms, keys


def detect(slug: str, name: str, acronyms: set[str]) -> list[str]:
    """返回命中的退化成因（空列表 = 正常）。"""
    reasons: list[str] = []
    if not name:
        return reasons
    words = [w for w in re.split(r"[-_]", slug) if w]
    # P6 机翻相邻重复词
    if re.search(r"\b([A-Za-z]{2,})(\s+\1\b)+", name, flags=re.IGNORECASE):
        reasons.append("duplicate_word")
    # P3 括号模板碎片
    if re.search(r"-\s*\(", name) or re.search(r"\(\s*[A-Za-z][A-Za-z /]*\s*\)\s*$", name):
        reasons.append("paren_template")
    # P4 连字符拼接碎片（`X - ( ... )` / 尾部 ` ) `
    if re.search(r"\s+-\s+", name) and "(" in name:
        reasons.append("hyphen_fragment")
    # P1 编号 slug 直接 title-case
    if any(re.fullmatch(r"\d+", w) for w in words) and norm(name) == norm(slug):
        reasons.append("numbered_slug")
    # P2 单个通用词（只认角色词/抽象通用词；全大写 2-6 位视为缩写专名，如 EBIT/CAGR/PSQI）
    name_words = re.findall(r"[A-Za-z]+", name)
    if len(name_words) == 1 and name_words[0].lower() in GENERIC_SINGLE:
        w = name_words[0]
        if not (w.isupper() and 2 <= len(w) <= 6) and w.lower() not in acronyms:
            reasons.append("single_generic")
    # P5 slug 词堆砌：与 slug 同形 + 词首为通用角色词 + ≥2 段（合法的修饰语词首除外）
    if norm(name) == norm(slug) and len(words) >= 2 \
            and words[0] in GENERIC_ROLE and words[0] not in MODIFIER_OK:
        reasons.append("slug_word_salad")
    return reasons


def collect(path: Path, acronyms: set[str]) -> dict[str, str]:
    data = json.load(open(path, encoding="utf-8"))
    problems: dict[str, str] = {}
    for key, val in data.items():
        if not isinstance(val, dict):
            problems[key] = "value_not_dict"
            continue
        slug = key.split("/", 1)[-1]
        reasons = detect(slug, val.get("en", ""), acronyms)
        if reasons:
            problems[key] = ",".join(sorted(set(reasons)))
    return problems


def load_baseline() -> dict[str, str]:
    if not BASELINE_PATH.exists():
        return {}
    data = json.load(open(BASELINE_PATH, encoding="utf-8"))
    return {str(k): str(v) for k, v in data.get("items", {}).items()}


def write_baseline(items: dict[str, str]) -> None:
    payload = {
        "generated_at": "2026-11-05",
        "note": "英文元数据退化存量债基线：只允许减少不允许新增；新增必须修数据或登记 allowlist。",
        "count": len(items),
        "items": dict(sorted(items.items())),
    }
    json.dump(payload, open(BASELINE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[en-meta] 基线已更新：{len(items)} 条 -> {BASELINE_PATH}")


def self_test() -> int:
    """六类判据 + 合法短名反向用例。"""
    acr = set(DEFAULT_ACRONYMS)
    cases = [
        ("generator-35", "Generator 35", ["numbered_slug"]),
        ("detector-173", "Detector 173", ["numbered_slug"]),
        ("fin", "Finance", ["single_generic"]),
        ("detect", "Detect", ["single_generic"]),
        ("psqi", "Quality - ( Check / Evaluate / Improvement ) Mechanism", ["paren_template", "hyphen_fragment"]),
        ("assessor-water-quality", "Assessor Water Quality", ["slug_word_salad"]),
        ("ast-view-device", "AST AST View Device", ["duplicate_word"]),
        ("reference-format-convert", "Reference Reference Format Convert", ["duplicate_word"]),
        # 反向用例：合法名不得判红
        ("it/bmi", "BMI", []),
        ("it/pdf-merge", "PDF Merge", []),
        ("it/json-diff", "JSON Diff Compare", []),
        ("accounting/asset-turnover", "Asset Turnover", []),
        ("design/base64-to-image", "Base64 to Image", []),
        ("accounting/ebit", "EBIT", []),
        ("accounting/ebitda", "EBITDA", []),
    ]
    bad = 0
    for slug, name, want in cases:
        got = detect(slug.split("/")[-1], name, acr)
        got_set, want_set = set(got), set(want)
        if want_set and not want_set.issubset(got_set):
            bad += 1
            print(f"FAIL {slug}: {name!r} -> got {got}, want at least {want}")
        elif not want_set and got_set:
            bad += 1
            print(f"FAIL {slug}: {name!r} 合法名被误判 -> {got}")
    print(f"[en-meta] self-test: {len(cases) - bad}/{len(cases)} passed")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="英文元数据退化门禁")
    ap.add_argument("--check", action="store_true", help="发现新增退化即 exit 1")
    ap.add_argument("--report", action="store_true", help="只打印报告，不判红")
    ap.add_argument("--update-baseline", action="store_true", help="把当前存量写入基线")
    ap.add_argument("--self-test", action="store_true", help="判据自测")
    ap.add_argument("--input", type=Path, default=OVERRIDE_PATH, help="待扫 JSON（默认 _en_override.json）")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if not args.input.exists():
        print(f"ERROR: 待扫文件不存在：{args.input}")
        return 2

    acronyms, allow_keys = load_allowlist()
    current = collect(args.input, acronyms)
    # allowlist 优先（逐条写原因才允许豁免）
    for key in list(current):
        if key in allow_keys:
            current.pop(key)
    baseline = load_baseline()

    if args.update_baseline:
        write_baseline(current)
        return 0

    added = {k: v for k, v in current.items() if k not in baseline}
    fixed = [k for k in baseline if k not in current]
    counts: dict[str, int] = {}
    for reasons in current.values():
        for r in reasons.split(","):
            counts[r] = counts.get(r, 0) + 1
    inds: dict[str, int] = {}
    for key in current:
        inds[key.split("/", 1)[0]] = inds.get(key.split("/", 1)[0], 0) + 1

    print(f"[en-meta] 存量退化 {len(current)} 条 / 基线 {len(baseline)} 条 / 新增 {len(added)} 条 / 已修复 {len(fixed)} 条")
    print("[en-meta] 成因分布：" + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])))
    print("[en-meta] 行业前 10：" + ", ".join(f"{k}={v}" for k, v in sorted(inds.items(), key=lambda x: -x[1])[:10]))

    if args.report:
        for key, reasons in sorted(current.items())[:50]:
            print(f"  - {key}: {reasons}")
        return 0

    if added:
        print("ERROR: 检测到新增英文元数据退化（禁止新增，必须修数据或登记 allowlist）：")
        for key, reasons in sorted(added.items()):
            print(f"  - {key}: {reasons}")
        return 1

    if fixed:
        print("[en-meta] 提示：以下基线条目已修复，可运行 --update-baseline 收缩基线：")
        print("  " + ", ".join(fixed[:20]) + (" ..." if len(fixed) > 20 else ""))
    print("[en-meta] OK：无新增退化")
    return 0


if __name__ == "__main__":
    sys.exit(main())
