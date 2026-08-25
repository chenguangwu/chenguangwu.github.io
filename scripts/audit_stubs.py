#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P0-1 跳转桩治理脚本（审计 + 可选清理）。"""

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"
SCRIPT_COMMENT = "TOOLBOX-REDIRECT"


class LinkCollector(HTMLParser):
    """提取 HTML 内部链接与 script 片段。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raw_script_chunks: List[str] = []
        self.links: List[str] = []
        self._script_open = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag.lower() in {"a", "link", "script", "img", "iframe", "source", "video", "audio", "embed", "object"}:
            for key in ("href", "src"):
                value = attrs.get(key)
                if isinstance(value, str) and value.strip():
                    self.links.append(value.strip())

        for key in ("action", "formaction"):
            value = attrs.get(key)
            if isinstance(value, str) and value.strip():
                self.links.append(value.strip())

        if tag.lower() == "script" and attrs.get("type") != "application/json":
            self._script_open = True

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self._script_open:
            self._script_open = False

    def handle_data(self, data):
        if self._script_open:
            self.raw_script_chunks.append(data)


REFRESH_RE = re.compile(
    r"<meta\s+[^>]*http-equiv=['\"]refresh['\"][^>]*content=['\"]([^'\"]*)['\"]",
    re.IGNORECASE,
)
CANON_RE = re.compile(
    r"<link\s+[^>]*rel=['\"]canonical['\"][^>]*href=['\"]([^'\"]+)",
    re.IGNORECASE,
)
LOCATION_RE = re.compile(
    r"location\.href\s*=\s*['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)
ABS_HTTP_RE = re.compile(r"^https?://", re.IGNORECASE)
TOOLBOX_TARGET_RE = re.compile(r"\n(?P<prefix><meta http-equiv=\"refresh\" content=\"0;url=)[^\">]+(?P<suffix>\">)")


@dataclass(frozen=True)
class StubItem:
    file: str
    target: str
    target_exists: bool
    target_type: str
    incoming: int = 0


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def all_html_files() -> List[Path]:
    return [p for p in TOOLS_DIR.rglob("*.html")]


def is_external(url: str) -> bool:
    return bool(ABS_HTTP_RE.match(url) or url.startswith("javascript:") or url.startswith("mailto:"))


def normalize_target(raw: str) -> str:
    if not raw:
        return ""
    return raw.strip().strip("'").strip('"').split("#", 1)[0].strip()


def resolve_local(raw: str, source: Path) -> str:
    if not raw:
        return ""
    url = normalize_target(raw)
    if not url or is_external(url) or url.startswith("#"):
        return url

    if url.startswith("//"):
        # 协议相对 URL；本项目通常用于站内跳转（如 //tools/xxx/index.html）
        url = url[2:]

    if url.startswith("tools/"):
        candidate = (ROOT / url).resolve()
    elif url.startswith("/"):
        candidate = (ROOT / url.lstrip("/")).resolve()
    else:
        candidate = (source.parent / url).resolve()

    if candidate.is_dir():
        candidate = candidate / "index.html"
    elif candidate.suffix != ".html" and candidate.with_suffix(candidate.suffix + ".html").exists():
        candidate = candidate.with_suffix(candidate.suffix + ".html")

    return candidate.relative_to(ROOT).as_posix()


def _canonicalize_target(target: str) -> str:
    if not target:
        return ""
    t = target.replace("\\", "/")
    if t.startswith("./"):
        t = t[2:]
    return t


def file_exists(rel: str) -> bool:
    if not rel or is_external(rel):
        return False
    abs_path = ROOT / rel
    if abs_path.exists():
        return True
    if abs_path.with_suffix(".html").exists():
        return True
    return False


def extract_redirect_target(content: str) -> Tuple[str, str]:
    m = CANON_RE.search(content)
    if m:
        return m.group(1).strip(), "canonical"

    m = REFRESH_RE.search(content)
    if m:
        payload = m.group(1)
        n = re.search(r"url=([^;]+)", payload, re.IGNORECASE)
        if n:
            return n.group(1).strip(" \"'"), "meta"

    collector = LinkCollector()
    collector.feed(content)
    for raw in collector.raw_script_chunks:
        for n in LOCATION_RE.finditer(raw):
            return n.group(1).strip(), "script"

    return "", "missing"


def scan_stubs() -> List[StubItem]:
    items: List[StubItem] = []
    for fp in all_html_files():
        rel = fp.relative_to(ROOT).as_posix()
        content = _read_text(fp)
        if SCRIPT_COMMENT not in content:
            continue
        raw_target, reason = extract_redirect_target(content)
        raw_target = _canonicalize_target(raw_target)
        if is_external(raw_target):
            target_exists = False
            target_type = "external"
            resolved_target = raw_target
        elif raw_target:
            resolved_target = resolve_local(raw_target, fp)
            target_exists = file_exists(resolved_target)
            target_type = "ok" if target_exists else "missing"
        else:
            resolved_target = ""
            target_type = reason
            target_exists = False
        items.append(StubItem(file=rel, target=resolved_target, target_exists=target_exists, target_type=target_type))
    return items


def incoming_count() -> Dict[str, int]:
    counts = defaultdict(int)
    for fp in all_html_files():
        try:
            content = _read_text(fp)
        except Exception:
            continue

        collector = LinkCollector()
        collector.feed(content)

        for raw in collector.links:
            target = normalize_target(raw)
            if not target:
                continue
            resolved = resolve_local(target, fp)
            if not resolved or is_external(resolved):
                continue
            counts[resolved] += 1

        for raw in collector.raw_script_chunks:
            for loc in LOCATION_RE.finditer(raw):
                resolved = resolve_local(loc.group(1), fp)
                if not resolved or is_external(resolved):
                    continue
                counts[resolved] += 1
    return counts


def is_redirect_file(fp: Path) -> bool:
    try:
        return SCRIPT_COMMENT in fp.read_text(encoding="utf-8")
    except Exception:
        return False


def make_stub_html(title: str, target_url: str) -> str:
    target_url = target_url.strip()
    return (
        "<!DOCTYPE html>\n"
        "<!-- TOOLBOX-REDIRECT -->\n"
        "<html lang=\"zh-CN\"><head><meta charset=\"UTF-8\">\n"
        f"<meta http-equiv=\"refresh\" content=\"0;url={target_url}\">\n"
        f"<link rel=\"canonical\" href=\"{target_url}\">\n"
        '<meta name="robots" content="noindex,follow">\n'
        f"<title>{title} - ToolBox</title>\n"
        '<script src="/js/clarity.js" defer></script>\n'
        "</head>\n"
        "<body>\n"
        f"<p>页面已迁移至 <a href=\"{target_url}\">新地址</a>。</p>\n"
        "<script>window.location.href='{0}';</script>\n"
        "</body></html>\n"
    ).format(target_url)


def read_stub_title(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.S)
        if m:
            t = m.group(1).strip()
            return t.replace(" - ToolBox", "").strip()
    except Exception:
        pass
    return path.stem


def dedupe_duplicates(duplicates, apply: bool = False):
    """将同目标重复桩并到首项；将其余桩指向首项，返回执行清单。"""
    plans = []
    for _, rows in duplicates:
        keeper = rows[0]
        keeper_fp = ROOT / keeper.file
        if not keeper_fp.exists():
            continue
        keeper_url = "/" + keeper.file
        for it in rows[1:]:
            fp = ROOT / it.file
            if not fp.exists():
                continue
            title = read_stub_title(fp)
            plans.append((it.file, keeper.file, "to-duplicate-keeper"))
            if apply:
                fp.write_text(make_stub_html(title, keeper_url), encoding="utf-8")
    return plans


def classify(items: List[StubItem], incoming: Dict[str, int]):
    # 重新注入入链数
    for i, it in enumerate(items):
        items[i] = StubItem(
            file=it.file,
            target=it.target,
            target_exists=it.target_exists,
            target_type=it.target_type,
            incoming=incoming.get(it.file, 0),
        )

    by_target: Dict[str, List[StubItem]] = defaultdict(list)
    for it in items:
        by_target[it.target].append(it)

    duplicates = []
    for target, rows in by_target.items():
        if not target:
            continue
        valid = [r for r in rows if r.target_type == "ok"]
        if len(valid) > 1:
            duplicates.append((target, sorted(valid, key=lambda x: x.file)))

    missing = [it for it in items if it.target_type in {"missing", "external", "missing_target", "no_target"}]
    orphans = [
        it for it in items
        if it.incoming <= 0 and it.target_type in {"missing", "external", "no_target", "missing_target"}
    ]

    return {
        "all": items,
        "duplicates": duplicates,
        "missing": missing,
        "orphans": orphans,
        "incoming": incoming,
        "healthy": len(items) - sum(len(rows) - 1 for _, rows in duplicates),
    }


def write_json(path: Path, payload: dict):
    path.write_text(
        json.dumps(
            {
                "stub_count": len(payload["all"]),
                "missing_target": len(payload["missing"]),
                "duplicate_target_count": len(payload["duplicates"]),
                "orphans_count": len(payload["orphans"]),
                "duplicates": [
                    {
                        "target": target,
                        "count": len(stubs),
                        "stubs": [s.file for s in stubs],
                    }
                    for target, stubs in payload["duplicates"]
                ],
                "orphans": [
                    {
                        "file": it.file,
                        "target": it.target,
                        "reason": it.target_type,
                        "incoming": it.incoming,
                    }
                    for it in payload["orphans"]
                ],
                "stubs": [
                    {
                        "file": it.file,
                        "target": it.target,
                        "target_type": it.target_type,
                        "target_exists": it.target_exists,
                        "incoming": it.incoming,
                    }
                    for it in payload["all"]
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def write_report(path: Path, payload: dict):
    lines = [
        "# 跳转桩治理审计报告",
        "",
        f"stub_count={len(payload['all'])}",
        f"missing_target={len(payload['missing'])}",
        f"duplicate_target_count={len(payload['duplicates'])}",
        f"orphans_count={len(payload['orphans'])}",
        "",
        "## 重复目标",
    ]

    if payload["duplicates"]:
        for target, rows in payload["duplicates"]:
            lines.append(f"- {target} ({len(rows)} 个桩)")
            for row in rows:
                lines.append(f"  - {row.file}")
    else:
        lines.append("- 无")

    lines.extend([
        "",
        "## 孤儿桩（无入链且目标异常）",
    ])
    if payload["orphans"]:
        for row in payload["orphans"]:
            lines.append(f"- {row.file} -> {row.target or '(no target)'} [{row.target_type}] 入链={row.incoming}")
    else:
        lines.append("- 无")

    lines.extend([
        "",
        "## 审计摘要",
        f"- 健康桩: {payload['healthy']}",
    ])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def delete_orphans(orphans: List[StubItem]):
    removed = []
    for it in orphans:
        fp = ROOT / it.file
        if fp.exists():
            fp.unlink()
            removed.append(it.file)
    return removed


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="", help="导出 JSON 报告路径")
    ap.add_argument("--report", default="", help="导出 markdown 报告路径")
    ap.add_argument("--list-orphans", action="store_true", help="仅输出孤儿桩清单")
    ap.add_argument("--delete-orphans", action="store_true", help="清理无入链且目标无效的桩")
    ap.add_argument("--dedupe-duplicates", action="store_true", help="将同目标重复桩并到第一条（默认仅 dry-run）")
    ap.add_argument("--apply", action="store_true", help="与 --dedupe-duplicates 配合：执行文件改写")
    ap.add_argument("--no-banner", action="store_true")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    items = scan_stubs()
    counts = incoming_count()
    payload = classify(items, counts)

    if not args.no_banner:
        print("--- stub-audit report ---")
        print(f"stub_count: {len(payload['all'])}")
        print(f"missing_target: {len(payload['missing'])}")
        print(f"duplicate_target_count: {len(payload['duplicates'])}")
        print(f"orphans_count: {len(payload['orphans'])}")

    if args.list_orphans:
        for row in payload["orphans"][:200]:
            print(f"{row.file}\t{row.target or '(no target)'}\t{row.target_type}\tincoming={row.incoming}")

    if args.delete_orphans:
        removed = delete_orphans(payload["orphans"])
        print(f"deleted_orphans: {len(removed)}")
        for fp in removed:
            print(fp)

    if args.dedupe_duplicates:
        plans = dedupe_duplicates(payload["duplicates"], apply=args.apply)
        print(f"dedupe_duplicates: {len(plans)}")
        for src, dst, mode in plans[:200]:
            print(f"{src} -> {dst} [{mode}]")

    if args.json:
        write_json(Path(args.json), payload)
        if not args.no_banner:
            print(f"json: {args.json}")

    if args.report:
        write_report(Path(args.report), payload)
        if not args.no_banner:
            print(f"report: {args.report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
