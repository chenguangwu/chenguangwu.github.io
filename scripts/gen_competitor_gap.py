# -*- coding: utf-8 -*-
"""
gen_competitor_gap.py — 竞品工具覆盖率 Gap 分析器

比对「竞品站（it-tools.tech 等）工具清单」与「ToolBox 全站 5023 工具」，
输出：
  1. gap-report.md  —— 已覆盖 / 疑似缺失 清单（人工审核依据）
  2. gap-report.csv —— 逐工具明细（可 Excel 筛选）

匹配算法：
  竞品 slug 去掉通用停用词（to/and/the/converter/generator/parser/validator 等）
  得核心 token，在本地工具的 (url + name + desc) 中做「全部 token 共现」模糊匹配。

用法：python3 scripts/gen_competitor_gap.py
纯标准库，可复跑（幂等覆盖）。产物不影响站点、不被 _build.py 收录。
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_JSON = os.path.join(ROOT, "json", "tools.json")
OUT_MD = os.path.join(ROOT, "gap-report.md")
OUT_CSV = os.path.join(ROOT, "gap-report.csv")

# ---------------------------------------------------------------------------
# 1) 竞品站工具清单（it-tools.tech 官方仓库 src/tools 目录，2026-08 抓取）
#    每行: (竞品 slug, 中文名, 是否纯前端可实现, 备注)
# ---------------------------------------------------------------------------
COMPETITOR_TOOLS = [
    ("ascii-text-drawer", "ASCII 艺术字生成", 1, "纯算法"),
    ("base64-file-converter", "Base64 文件转换", 1, "FileReader"),
    ("base64-string-converter", "Base64 字符串转换", 1, ""),
    ("basic-auth-generator", "Basic Auth 生成", 1, ""),
    ("bcrypt", "Bcrypt 哈希", 1, "bcryptjs CDN"),
    ("benchmark-builder", "性能基准代码生成", 1, ""),
    ("bip39-generator", "BIP39 助记词", 1, ""),
    ("camera-recorder", "摄像头录制", 1, "getUserMedia"),
    ("case-converter", "大小写转换", 1, ""),
    ("chmod-calculator", "chmod 权限计算", 1, ""),
    ("chronometer", "秒表计时器", 1, ""),
    ("color-converter", "颜色格式转换", 1, ""),
    ("crontab-generator", "Crontab 表达式生成", 1, ""),
    ("date-time-converter", "日期时间转换", 1, ""),
    ("device-information", "设备信息检测", 1, "navigator API"),
    ("docker-run-to-docker-compose-converter", "docker run 转 compose", 1, ""),
    ("email-normalizer", "邮箱规范化", 1, ""),
    ("emoji-picker", "Emoji 选择器", 1, ""),
    ("encryption", "加密解密", 1, "WebCrypto"),
    ("eta-calculator", "ETA 预计到达计算", 1, ""),
    ("git-memo", "Git 备忘单", 1, ""),
    ("hash-text", "文本哈希", 1, ""),
    ("hmac-generator", "HMAC 生成", 1, ""),
    ("html-entities", "HTML 实体转义", 1, ""),
    ("html-wysiwyg-editor", "富文本编辑器", 1, "contentEditable"),
    ("http-status-codes", "HTTP 状态码速查", 1, ""),
    ("iban-validator-and-parser", "IBAN 校验解析", 1, ""),
    ("integer-base-converter", "进制转换", 1, ""),
    ("ipv4-address-converter", "IPv4 地址转换", 1, ""),
    ("ipv4-range-expander", "IPv4 范围展开", 1, ""),
    ("ipv4-subnet-calculator", "IPv4 子网计算", 1, ""),
    ("ipv6-ula-generator", "IPv6 ULA 生成", 1, ""),
    ("json-diff", "JSON 差异对比", 1, ""),
    ("json-minify", "JSON 压缩", 1, ""),
    ("json-to-csv", "JSON 转 CSV", 1, ""),
    ("json-to-toml", "JSON 转 TOML", 1, ""),
    ("json-to-xml", "JSON 转 XML", 1, ""),
    ("json-to-yaml-converter", "JSON 转 YAML", 1, ""),
    ("json-viewer", "JSON 可视化查看", 1, ""),
    ("jwt-parser", "JWT 解析", 1, ""),
    ("keycode-info", "按键 KeyCode 速查", 1, ""),
    ("list-converter", "列表格式转换", 1, ""),
    ("lorem-ipsum-generator", "Lorem 占位文生成", 1, ""),
    ("mac-address-generator", "MAC 地址生成", 1, ""),
    ("mac-address-lookup", "MAC 厂商查询", 1, "需内置 OUI 表"),
    ("markdown-to-html", "Markdown 转 HTML", 1, ""),
    ("math-evaluator", "数学表达式求值", 1, ""),
    ("meta-tag-generator", "Meta 标签生成", 1, ""),
    ("mime-types", "MIME 类型速查", 1, ""),
    ("numeronym-generator", "数字缩写生成(i18n)", 1, ""),
    ("otp-code-generator-and-validator", "OTP/TOTP 验证码", 1, "纯算法"),
    ("password-strength-analyser", "密码强度分析", 1, ""),
    ("pdf-signature-checker", "PDF 签名校验", 0, "需解析 PDF 签名结构，实现复杂"),
    ("percentage-calculator", "百分比计算", 1, ""),
    ("phone-parser-and-formatter", "电话号码解析格式化", 1, "需内置国家码表"),
    ("qr-code-generator", "二维码生成", 1, ""),
    ("random-port-generator", "随机端口生成", 1, ""),
    ("regex-memo", "正则备忘单", 1, ""),
    ("regex-tester", "正则在线测试", 1, ""),
    ("roman-numeral-converter", "罗马数字转换", 1, ""),
    ("rsa-key-pair-generator", "RSA 密钥对生成", 1, "WebCrypto"),
    ("safelink-decoder", "SafeLink 解码", 1, ""),
    ("slugify-string", "Slug 生成", 1, ""),
    ("sql-prettify", "SQL 格式化", 1, ""),
    ("string-obfuscator", "字符串混淆", 1, ""),
    ("svg-placeholder-generator", "SVG 占位图生成", 1, ""),
    ("temperature-converter", "温度换算", 1, ""),
    ("text-diff", "文本差异对比", 1, ""),
    ("text-statistics", "文本统计", 1, ""),
    ("text-to-binary", "文本转二进制", 1, ""),
    ("text-to-nato-alphabet", "北约音标字母转换", 1, ""),
    ("text-to-unicode", "文本转 Unicode", 1, ""),
    ("token-generator", "随机 Token 生成", 1, ""),
    ("toml-to-json", "TOML 转 JSON", 1, ""),
    ("toml-to-yaml", "TOML 转 YAML", 1, ""),
    ("ulid-generator", "ULID 生成", 1, ""),
    ("url-encoder", "URL 编解码", 1, ""),
    ("url-parser", "URL 解析", 1, ""),
    ("user-agent-parser", "User-Agent 解析", 1, ""),
    ("uuid-generator", "UUID 生成", 1, ""),
    ("wifi-qr-code-generator", "WiFi 二维码生成", 1, ""),
    ("xml-formatter", "XML 格式化", 1, ""),
    ("xml-to-json", "XML 转 JSON", 1, ""),
    ("yaml-to-json-converter", "YAML 转 JSON", 1, ""),
    ("yaml-to-toml", "YAML 转 TOML", 1, ""),
    ("yaml-viewer", "YAML 查看器", 1, ""),
]

# ---------------------------------------------------------------------------
# 2) 人工校准映射（MANUAL_MAP）
#    竞品命名与本站命名常不一致（chronometer↔stopwatch、git-memo↔git-cheatsheet、
#    sql-prettify↔sql-formatter、mime-types↔mime-type …），字符串相似度无法跨越
#    这层语义差异，会把「已覆盖」误报为「缺失」。此处固化人工核实结果，优先于自动匹配。
#    ⚠️ 新增/改名工具时如发现误报，优先来这里补一行。
# ---------------------------------------------------------------------------
MANUAL_MAP = {
    "ascii-text-drawer": "tools/it/ascii-art.html",            # ASCII 大字生成器
    "chronometer": "tools/it/stopwatch.html",                  # 秒表
    "date-time-converter": "tools/it/date-duration.html",      # 日期时长/换算
    "encryption": "tools/it/aes-encryptor.html",               # AES 加解密
    "git-memo": "tools/it/git-cheatsheet.html",                # Git 备忘单
    "html-wysiwyg-editor": "tools/it/rich-text-editor.html",   # 富文本编辑器（本站新增）
    "http-status-codes": "tools/it/http-status.html",          # HTTP 状态码
    "ipv4-address-converter": "tools/it/ip-calculator.html",   # IP 换算/子网
    "ipv4-subnet-calculator": "tools/it/ip-calculator.html",
    "mac-address-lookup": "tools/it/mac-lookup.html",          # MAC 厂商查询（含 OUI）
    "mime-types": "tools/it/mime-type.html",                   # MIME 速查
    "regex-memo": "tools/it/regex-cheatsheet.html",            # 正则备忘单
    "rsa-key-pair-generator": "tools/it/rsa.html",             # RSA（含密钥对生成）
    "sql-prettify": "tools/it/sql-formatter.html",             # SQL 格式化
    "temperature-converter": "tools/life/temperature-converter.html",  # 温度换算（含列氏度）
}

# 通用停用词：竞品 slug 里这些词不参与核心 token 匹配
STOP = {
    "to", "and", "the", "a", "an", "of", "for", "in", "on", "with", "or",
    "converter", "generator", "parser", "validator", "formatter", "checker",
    "analyser", "analyzer", "information", "viewer", "code", "text", "string",
    "online", "tool", "tools", "free", "builder", "creator", "maker",
}


def core_tokens(slug):
    """从竞品 slug 提取核心 token（去停用词 + 数字后缀）"""
    parts = re.split(r"[-_]+", slug.lower())
    toks = [p for p in parts if p and p not in STOP]
    return toks if toks else [slug.lower()]


def build_local_index():
    tools = json.load(open(TOOLS_JSON, encoding="utf-8"))
    idx = []
    for t in tools:
        url = (t.get("url") or "").lower()
        name = (t.get("name") or "").lower()
        desc = (t.get("desc") or "").lower()
        en = (t.get("en") or "").lower()
        hay = url + " " + name + " " + desc + " " + en
        idx.append((hay, t))
    return idx


def find_matches(toks, idx, slug="", limit=5):
    """在本地索引里找包含全部核心 token 的工具。

    注意：不能简单「取前 N 个命中」——tools.json 的顺序会让不相关的工具
    （命中同一个泛词，如 temperature）挤掉真正对标的那一个。
    因此改为：收集全部候选 → 按 (basename 与竞品 slug 的相似度, URL 长度)
    排序 → 取最相关的一个。
    """
    import difflib
    import os as _os
    cands = []
    for hay, t in idx:
        if all(tok in hay for tok in toks):
            cands.append(t)
    if not cands:
        return []
    def score(t):
        base = _os.path.splitext(_os.path.basename(t.get("url", "")))[0].lower()
        sim = difflib.SequenceMatcher(None, base, slug.lower()).ratio() if slug else 0.0
        # 相似度优先；相同时短 URL 优先（通常更精确）
        return (sim, -len(t.get("url", "")))
    cands.sort(key=score, reverse=True)
    return cands[:limit]


def main():
    idx = build_local_index()
    covered, missing = [], []
    for slug, cn, feasible, note in COMPETITOR_TOOLS:
        toks = core_tokens(slug)
        manual = MANUAL_MAP.get(slug)
        if manual:
            # 人工校准优先：直接按 URL 定位，绕过字符串匹配
            hits = [t for _, t in idx if t.get("url") == manual]
        else:
            hits = find_matches(toks, idx, slug)
        row = {
            "slug": slug, "cn": cn, "feasible": feasible, "note": note,
            "tokens": "|".join(toks),
            "hits": hits,
        }
        if hits:
            row["local_url"] = hits[0].get("url", "")
            row["local_name"] = hits[0].get("name", "")
            row["quality"] = hits[0].get("quality", "")
            covered.append(row)
        else:
            row["local_url"] = ""
            row["local_name"] = ""
            row["quality"] = ""
            missing.append(row)

    # ---- CSV ----
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["竞品slug", "中文名", "是否纯前端", "状态", "本地URL", "本地名称", "质量", "核心token", "备注"])
        for r in covered + missing:
            w.writerow([
                r["slug"], r["cn"], "是" if r["feasible"] else "否",
                "已覆盖" if r["hits"] else "缺失",
                r["local_url"], r["local_name"], r["quality"],
                r["tokens"], r["note"],
            ])

    # ---- MD ----
    total = len(COMPETITOR_TOOLS)
    doable_missing = [r for r in missing if r["feasible"]]
    skip_missing = [r for r in missing if not r["feasible"]]
    lines = []
    lines.append("# 竞品工具覆盖率 Gap 报告\n")
    lines.append("> 对标竞品：**it-tools.tech**（开源开发者工具聚合站，官方仓库 `src/tools` 目录 82 个工具）\n")
    lines.append("> 生成脚本：`scripts/gen_competitor_gap.py`（可复跑，产物不影响站点）\n")
    lines.append("\n## 一、总览\n")
    lines.append("| 指标 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    lines.append("| 竞品工具总数 | %d | 100%% |" % total)
    lines.append("| **已覆盖** | %d | %.1f%% |" % (len(covered), 100.0 * len(covered) / total))
    lines.append("| **缺失（纯前端可做）** | %d | %.1f%% |" % (len(doable_missing), 100.0 * len(doable_missing) / total))
    lines.append("| 缺失（不建议做） | %d | %.1f%% |" % (len(skip_missing), 100.0 * len(skip_missing) / total))
    lines.append("\n## 二、缺失且纯前端可做（待补齐）\n")
    if doable_missing:
        lines.append("| # | 竞品工具 | 中文名 | 核心 token | 说明 |")
        lines.append("|---|----------|--------|-----------|------|")
        for i, r in enumerate(doable_missing, 1):
            lines.append("| %d | `%s` | %s | `%s` | %s |" % (i, r["slug"], r["cn"], r["tokens"], r["note"] or "—"))
    else:
        lines.append("（无）")
    lines.append("\n## 三、缺失但不建议做\n")
    if skip_missing:
        lines.append("| 竞品工具 | 中文名 | 原因 |")
        lines.append("|----------|--------|------|")
        for r in skip_missing:
            lines.append("| `%s` | %s | %s |" % (r["slug"], r["cn"], r["note"]))
    else:
        lines.append("（无）")
    lines.append("\n## 四、已覆盖明细（供内容优化参考）\n")
    lines.append("| 竞品工具 | 本地工具 | 本地 URL | 质量 |")
    lines.append("|----------|----------|----------|------|")
    for r in covered:
        lines.append("| `%s` | %s | `%s` | %s |" % (r["slug"], r["local_name"], r["local_url"], r["quality"]))

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("竞品工具总数: %d" % total)
    print("已覆盖: %d (%.1f%%)" % (len(covered), 100.0 * len(covered) / total))
    print("缺失(纯前端可做): %d" % len(doable_missing))
    print("缺失(不建议): %d" % len(skip_missing))
    print("\n--- 缺失清单 ---")
    for r in doable_missing:
        print("  %-42s %s" % (r["slug"], r["cn"]))
    if skip_missing:
        print("\n--- 不建议 ---")
        for r in skip_missing:
            print("  %-42s %s (%s)" % (r["slug"], r["cn"], r["note"]))
    print("\n产物: %s / %s" % (OUT_MD, OUT_CSV))


if __name__ == "__main__":
    main()
