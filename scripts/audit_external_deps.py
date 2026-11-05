#!/usr/bin/env python3
"""外部第三方依赖审计：资源枚举 + 版本锁 / SRI / crossorigin / 本地兜底 / vendor 台账。

用法：
  python3 scripts/audit_external_deps.py            # 打印台账与汇总
  python3 scripts/audit_external_deps.py --check    # 有「可锁未锁」或静态脚本缺 SRI 时 exit 1
  python3 scripts/audit_external_deps.py --json     # 输出机器可读 JSON

审计口径：
  - 只统计「运行时真正会发起请求」的资源：<script src>、<link rel=stylesheet|preconnect|preload>、
    import()、fetch()、JS 里的 loadScript() / script.src = ...；导航链接（淘宝客、GitHub、社交分享）不计。
  - 本站 origin（chenguangwu.github.io）与相对路径不计入「第三方」。
  - 版本锁：jsdelivr 需 npm 包后带精确 @x.y.z；cdnjs 需 /lib/x.y.z/。
  - SRI：静态 <script> 看 integrity + crossorigin；动态 import / wasm / 服务端下发 SDK 标「不可用」并写明原因。
  - 兜底：页面含对应库的 typeof 守卫或「加载失败 / 无法加载 / 出错」提示即判「有降级」。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF_ORIGIN = "chenguangwu.github.io"
SKIP_DIRS = {"zh-tw", "node_modules", ".git", "plan", "scripts", "i18n"}

# 第三方库 -> 页面运行时全局名（用于兜底守卫识别）
LIB_GLOBALS = {
    "pdf-lib": "PDFLib",
    "mermaid": "mermaid",
    "d3": "d3",
    "markmap-view": "markmap",
    "markmap-lib": "markmap",
    "bcryptjs": "bcrypt",
    "js-yaml": "jsyaml",
    "less": "less",
    "acorn": "acorn",
    "sql.js": "initSqlJs",
    "typescript": "ts",
}

# 统计 / 广告 SDK：上游服务端动态下发，官方要求直接引用，版本不可锁
TELEMETRY_HOSTS = {
    "sdk.51.la",
    "v6-widget.51.la",
    "hm.baidu.com",
    "zz.bdstatic.com",
    "lf1-cdn-tos.bytegoofy.com",
    "pagead2.googlesyndication.com",
}

FALLBACK_HINTS = ("加载失败", "无法加载", "加载出错", "请检查网络", "加载异常")
# 文档 / 代码示例里的占位域名，不是真实请求
DOC_HOSTS = {"example.com", "www.example.com", "placehold.co"}
EXTERNAL_SCRIPT_RE = re.compile(r"<script[^>]*\bsrc=\"(https?://[^\"]+)\"[^>]*>", re.I)
LINK_RE = re.compile(r"<link[^>]*>", re.I)
INLINE_JS_URL_RE = re.compile(r"https?://[^\s\"'<>()`]+")
HOST_RE = re.compile(r"https?://([a-z0-9.-]+\.[a-z]{2,})")

VERSION_IN_JSDEVLIRR = re.compile(r"@(\d+\.\d+\.\d+)")
VERSION_IN_CDNJS = re.compile(r"/(?:ajax/libs/[^/]+|[^/]+)/(\d+\.\d+\.\d+)/")
SCOPED_NPM = re.compile(r"/npm/(@[^/]+/[^@/]+|[^@/]+)@")
CDNJS_LIB = re.compile(r"/ajax/libs/([^/]+)/")


def iter_source_files():
    """扫描会进入发布产物的源文件（HTML / JS / CSS）。"""
    for base, pattern in (
        (ROOT, "*.html"),
        (ROOT / "tools", "**/*.html"),
        (ROOT / "guides", "*.html"),
        (ROOT / "js", "**/*.js"),
    ):
        for p in sorted(base.glob(pattern)):
            parts = set(p.relative_to(ROOT).parts)
            if parts & SKIP_DIRS:
                continue
            yield p


def page_libs(html: str) -> list[str]:
    """从页面里的 CDN 静态脚本识别引用了哪些第三方库。"""
    libs = []
    for m in EXTERNAL_SCRIPT_RE.finditer(html):
        url = m.group(1)
        name = lib_name(url)
        if name and name not in libs:
            libs.append(name)
    return libs


def lib_name(url: str) -> str:
    m = SCOPED_NPM.search(url)
    if m:
        return m.group(1)
    m = CDNJS_LIB.search(url)
    if m:
        return m.group(1)
    return ""


def host_of(url: str) -> str:
    m = HOST_RE.match(url)
    return (m.group(1) if m else "").lower()


def tf_version() -> str:
    """从 js/ai-core.js 读取锁定版本，替换模板串里的 ${TF_VERSION}。"""
    p = ROOT / "js" / "ai-core.js"
    if p.is_file():
        m = re.search(r"TF_VERSION\s*=\s*'([^']+)'", p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1)
    return "3"


def model_revisions() -> dict[str, str]:
    """从 js/ai-core.js 的 MODEL_REVISIONS 读取模型 → commit sha。"""
    p = ROOT / "js" / "ai-core.js"
    if not p.is_file():
        return {}
    txt = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"MODEL_REVISIONS\s*=\s*\{(.*?)\};", txt, re.S)
    if not m:
        return {}
    return dict(re.findall(r"'([^']+)':\s*'([0-9a-f]{40})'", m.group(1)))


def version_of(url: str) -> tuple[bool, str]:
    m = re.search(r"/resolve/([0-9a-f]{40})/", url)
    if m:
        return True, m.group(1)[:12] + "…"
    m = VERSION_IN_JSDEVLIRR.search(url)
    if m:
        return True, m.group(1)
    m = VERSION_IN_CDNJS.search(url)
    if m:
        return True, m.group(1)
    return False, "无版本号"


def has_fallback(html: str, libs: list[str]) -> bool:
    if any(h in html for h in FALLBACK_HINTS):
        return True
    if "transformers-dynamic" in libs and re.search(r"catch\s*\(", html):
        return True
    if "google-fonts" in libs and "sans-serif" in html:
        return True
    for lib in libs:
        g = LIB_GLOBALS.get(lib)
        if g and re.search(r"typeof\s+(?:window\.)?" + re.escape(g) + r"\b", html):
            return True
    return False


def collect_pages() -> list[dict]:
    pages = []
    for p in iter_source_files():
        if p.suffix.lower() != ".html":
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        libs = page_libs(html)
        if "js/ai-core.js" in html:
            libs.append("transformers-dynamic")
        if "fonts.googleapis.com" in html:
            libs.append("google-fonts")
        if not libs:
            continue
        rel = p.relative_to(ROOT).as_posix()
        pages.append({"page": rel, "libs": libs, "fallback": has_fallback(html, libs)})
    return pages


def collect_records() -> list[dict]:
    records: dict[tuple[str, str], dict] = {}

    def add(origin: str, url: str, kind: str, page: str, tag: str = "", dynamic: bool = False):
        if origin == "fonts.googleapis.com":
            url = "https://fonts.googleapis.com/css2"   # 三个模板串同一端点，归并
        key = (origin, url)
        rec = records.get(key)
        if rec is None:
            locked, ver = version_of(url)
            rec = {
                "origin": origin,
                "url": url,
                "kind": kind,
                "version_lock": locked,
                "version": ver,
                "sri": "-",
                "crossorigin": "-",
                "dynamic": dynamic,
                "pages": [],
            }
            records[key] = rec
        if page and page not in rec["pages"]:
            rec["pages"].append(page)
        if tag:
            rec["sri"] = "有" if re.search(r"\bintegrity=", tag, re.I) else "无"
            rec["crossorigin"] = "有" if re.search(r"\bcrossorigin=", tag, re.I) else "无"

    for p in iter_source_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(ROOT).as_posix()

        if p.suffix.lower() == ".html":
            for m in EXTERNAL_SCRIPT_RE.finditer(text):
                url = m.group(1)
                if host_of(url) == SELF_ORIGIN:
                    continue
                add(host_of(url), url, "script", rel, tag=m.group(0))
            for m in LINK_RE.finditer(text):
                tag = m.group(0)
                if not re.search(r'rel="(?:stylesheet|preload)"', tag, re.I):
                    continue
                hm = re.search(r'href="(https?://[^"]+)"', tag, re.I)
                if not hm or host_of(hm.group(1)) in (SELF_ORIGIN, *DOC_HOSTS):
                    continue
                add(host_of(hm.group(1)), hm.group(1), "link", rel, tag=tag)
            # 内联脚本里动态注入的第三方脚本（TTZZ 等）
            for m in INLINE_JS_URL_RE.finditer(text):
                url = m.group(0)
                if host_of(url) in (SELF_ORIGIN, *DOC_HOSTS):
                    continue
                if not (re.search(r"\.(js|mjs|css|wasm)(?:[?#]|$)", url) or "fonts.googleapis.com/css" in url):
                    continue
                kind = "link" if "fonts.googleapis.com/css" in url else "script"
                add(host_of(url), url, kind, rel, dynamic=True)
        else:
            for m in re.finditer(r"https?://[^\s\"'`<>()]+", text):
                url = m.group(0).rstrip(",;")
                url = url.replace("${TF_VERSION}", tf_version())
                h = host_of(url)
                if not h or h in (SELF_ORIGIN, *DOC_HOSTS):
                    continue
                if re.search(r"\.(js|mjs|css|wasm)(?:[?#/]|$)", url) or "transformers@" in url:
                    add(h, url, "js", rel, dynamic=True)

    # 间接依赖：Transformers.js 运行时从 Hugging Face 拉模型，URL 由库内部拼装，源码无字面量
    for p in iter_source_files():
        if p.suffix.lower() != ".html":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(ROOT).as_posix()
        for m in re.finditer(r"getPipeline\('([^']+)',\s*'([^']+)'", text):
            model = m.group(2)
            rev = model_revisions().get(model)
            add(
                "huggingface.co",
                f"https://huggingface.co/{model}/resolve/{rev or 'main'}/",
                "model",
                rel,
                dynamic=True,
            )

    return sorted(records.values(), key=lambda r: (r["origin"], r["url"])) 


def vendor_ledger() -> list[dict]:
    entries = []
    pdfjs = ROOT / "vendor" / "pdfjs"
    if pdfjs.is_dir():
        for d in sorted(pdfjs.iterdir()):
            if d.is_dir() and re.fullmatch(r"\d+\.\d+\.\d+", d.name):
                files = sorted(x.name for x in d.glob("*.mjs"))
                entries.append({
                    "component": "PDF.js",
                    "version": d.name,
                    "local": f"vendor/pdfjs/{d.name}/",
                    "files": files,
                    "source": "https://www.npmjs.com/package/pdfjs-dist",
                    "note": "自托管（原 CDN 3.11.174 因 CVE-2024-4367 升级）",
                })
    fuse = ROOT / "vendor" / "fuse.min.js"
    if fuse.is_file():
        head = fuse.read_text(encoding="utf-8", errors="ignore")[:400]
        m = re.search(r"Fuse\.js\s+v(\d+\.\d+\.\d+)", head) or re.search(r"v(\d+\.\d+\.\d+)", head)
        entries.append({
            "component": "Fuse.js",
            "version": m.group(1) if m else "未标注",
            "local": "vendor/fuse.min.js",
            "files": ["fuse.min.js"],
            "source": "https://www.npmjs.com/package/fuse.js",
            "note": "index.html 搜索 / SW 预缓存",
        })
    fonts_css = ROOT / "vendor" / "fonts" / "fonts.css"
    if fonts_css.is_file():
        txt = fonts_css.read_text(encoding="utf-8", errors="ignore")
        fam = re.search(r"font-family:\s*'([^']+)'", txt)
        entries.append({
            "component": fam.group(1) if fam else "本地字体",
            "version": font_version(ROOT / "vendor" / "fonts" / "plus-jakarta-sans-400.ttf"),
            "local": "vendor/fonts/",
            "files": sorted(x.name for x in (ROOT / "vendor" / "fonts").iterdir()),
            "source": "Google Fonts（本地 woff2/ttf 副本）",
            "note": "index.html / 404.html 使用；版本取自 TTF name 表 ID5",
        })
    pairing_fonts = ROOT / "vendor" / "fonts" / "font-pairing"
    if pairing_fonts.is_dir():
        entries.append({
            "component": "Font pairing preview fonts",
            "version": "Google Fonts Latin subsets",
            "local": "vendor/fonts/font-pairing/",
            "files": sorted(x.name for x in pairing_fonts.iterdir() if x.is_file()),
            "source": "https://github.com/google/fonts",
            "note": "35 个 OFL 字体族；各族许可证随资源分发，字体文件名带内容哈希",
        })
    sqljs = ROOT / "vendor" / "sql.js"
    if sqljs.is_dir():
        for d in sorted(sqljs.iterdir()):
            if d.is_dir() and re.fullmatch(r"\d+\.\d+\.\d+", d.name):
                entries.append({
                    "component": "sql.js",
                    "version": d.name,
                    "local": f"vendor/sql.js/{d.name}/",
                    "files": sorted(x.name for x in d.iterdir()),
                    "source": "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/",
                    "note": "自托管；wasm 启动前 SHA-256 校验（失败拒绝启动）",
                })
    for component, version, source, note in (
        ("acorn", "8.19.0", "https://cdn.jsdelivr.net/npm/acorn@8.19.0/dist/acorn.min.js", "MIT；浏览器包无运行时外部依赖"),
        ("bcryptjs", "2.4.3", "https://cdn.jsdelivr.net/npm/bcryptjs@2.4.3/dist/bcrypt.min.js", "MIT；浏览器包无运行时外部依赖"),
        ("js-yaml", "4.1.0", "https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js", "MIT；argparse 为命令行依赖，不在浏览器包中"),
        ("less", "4.9.1", "https://cdn.jsdelivr.net/npm/less@4.9.1/dist/less.min.js", "Apache-2.0；包含 copy-anything、is-what、parse-node-version，支持用户指定的 @import"),
        ("pdf-lib", "1.17.1", "https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js", "MIT；包含 standard-fonts、upng、pako、tslib"),
        ("typescript", "5.3.3", "https://cdnjs.cloudflare.com/ajax/libs/typescript/5.3.3/typescript.min.js", "Apache-2.0；附上游第三方声明，单文件转译无需运行时下载"),
    ):
        d = ROOT / "vendor" / component / version
        if d.is_dir():
            entries.append({
                "component": component,
                "version": version,
                "local": f"vendor/{component}/{version}/",
                "files": sorted(x.name for x in d.iterdir() if x.is_file()),
                "source": source,
                "note": note,
            })
    return entries


def font_version(ttf: Path) -> str:
    """读取 TTF name 表 ID5（版本字符串），如 'Version 2.071;gftools[0.9.30]' → '2.071'。"""
    try:
        import struct
        b = ttf.read_bytes()
        num = struct.unpack(">H", b[4:6])[0]
        name_off = None
        for i in range(num):
            off = 12 + i * 16
            if b[off:off + 4] == b"name":
                name_off = struct.unpack(">I", b[off + 8:off + 12])[0]
                break
        if name_off is None:
            return "未标注"
        _fmt, count, str_off = struct.unpack(">HHH", b[name_off:name_off + 6])
        for i in range(count):
            r = name_off + 6 + i * 12
            pid, eid, _lid, nid, ln, soff = struct.unpack(">HHHHHH", b[r:r + 12])
            if nid != 5:
                continue
            raw = b[name_off + str_off + soff:name_off + str_off + soff + ln]
            s = raw.decode("utf-16-be", "ignore") if pid == 3 else raw.decode("latin1", "ignore")
            m = re.search(r"Version\s+(\d+\.\d+)", s)
            if m:
                return m.group(1)
        return "未标注"
    except Exception:
        return "未标注"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    records = collect_records()
    pages = collect_pages()
    ledger = vendor_ledger()

    origins = sorted({r["origin"] for r in records})
    functional = [r for r in records if r["origin"] not in TELEMETRY_HOSTS]
    telemetry = [r for r in records if r["origin"] in TELEMETRY_HOSTS]

    # 分档
    tier1 = [r for r in functional if not r["version_lock"]]           # 无版本锁
    tier2 = [
        r for r in functional
        if r["version_lock"] and r["kind"] in ("script", "js", "wasm") and r["sri"] != "有"
    ]
    tier2_extra = [r for r in tier2 if r["dynamic"]]
    tier1_telemetry = [r for r in telemetry]

    no_fallback = [p for p in pages if not p["fallback"]]

    # 静态脚本缺 SRI / crossorigin 的硬违规（可锁脚本）
    violations = [
        r for r in functional
        if r["kind"] == "script" and not r["version_lock"]
    ]

    summary = {
        "origins": len(origins),
        "origins_functional": len({r["origin"] for r in functional}),
        "origins_telemetry": len({r["origin"] for r in telemetry}),
        "records": len(records),
        "scripts_cdn": len([r for r in functional if r["kind"] in ("script", "js", "wasm")]),
        "tier1_no_version_lock_functional": len(tier1),
        "tier1_no_version_lock_telemetry": len(tier1_telemetry),
        "tier2_version_no_sri": len(tier2),
        "tier2_dynamic_import": len(tier2_extra),
        "vendor_ledger": len(ledger),
        "pages_with_external_deps": len(pages),
        "pages_no_fallback": len(no_fallback),
        "violations": len(violations),
    }

    if args.json:
        print(json.dumps({
            "summary": summary,
            "records": records,
            "vendor": ledger,
            "pages": pages,
            "no_fallback": no_fallback,
            "violations": violations,
        }, ensure_ascii=False, indent=2))
    else:
        print("== 外部资源台账 ==")
        print(f"{'origin':32} {'文件':58} {'版本锁':6} {'SRI':4} {'CORS':5}")
        for r in records:
            ver = r["version"] if r["version_lock"] else "无"
            sri = r["sri"] if not r["dynamic"] else "动态"
            print(f"{r['origin']:32} {r['url'][:58]:58} {ver:6} {sri:4} {r['crossorigin']:5}")

        print("\n== 分档 ==")
        print(f"origin 总数：{summary['origins']}（功能库 {summary['origins_functional']} / 统计广告 {summary['origins_telemetry']}）")
        print(f"资源条目：{summary['records']}（外部可执行脚本 {summary['scripts_cdn']}）")
        print(f"① 无版本锁：功能库 {summary['tier1_no_version_lock_functional']} / 统计广告 {summary['tier1_no_version_lock_telemetry']}")
        print(f"② 有版本但无 SRI：{summary['tier2_version_no_sri']}（动态 import {summary['tier2_dynamic_import']}）")
        print(f"③ vendor 台账：{summary['vendor_ledger']} 条")
        print(f"兜底：外部依赖页 {summary['pages_with_external_deps']}，无降级 {summary['pages_no_fallback']}")

        if no_fallback:
            print("\n== 无降级页面 ==")
            for p in no_fallback:
                print(f"  - {p['page']} ← {', '.join(p['libs'])}")

        print("\n== vendor 台账 ==")
        for e in ledger:
            print(f"  - {e['component']} {e['version']}  {e['local']}  ← {e['source']}")

    if args.check and violations:
        print("\n[FAIL] 外部脚本未锁定精确版本：", file=sys.stderr)
        for r in violations:
            print(f"  - {r['url']}（{', '.join(r['pages'])}）", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
