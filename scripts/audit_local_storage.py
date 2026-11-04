#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全站本地存储审计（localStorage / sessionStorage / Cookie / IndexedDB）。

口径（与 plan/local-storage-audit.md 一致）：
  · 扫描范围：根目录 *.html、tools/**/*.html、guides/*.html、js/**/*.js
  · 违规判定（硬违规，必须修）：
      1) document.cookie 写入（`document.cookie =`，排除教学示例字符串）
      2) indexedDB 打开/使用
      3) 明文凭证落盘（密码/口令/token/私钥 等字段写入 storage）
      4) 跨页共享同一字面量键（不同工具页写读同一 key，互相覆盖）
  · 风险分档（只出清单，不改文案）：
      1 高风险：持久化字段含个人身份 / 健康 / 财务语义
      2 中风险：持久化业务中间态（草稿、历史记录、队列），字段无身份语义
      3 低风险：纯偏好（主题/语言/收藏/最近使用）或与个人无关的本地统计（最高分/计数器）

用法：
  python3 scripts/audit_local_storage.py            # 终端摘要
  python3 scripts/audit_local_storage.py --json out.json
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 敏感字段语义词表 ──────────────────────────────────────────────
# strong_cn：中文语义无歧义，命中即高敏（无论行业）
STRONG_CN = {
    "identity": ["姓名", "真实姓名", "联系人姓名", "患者姓名", "病人姓名", "户主姓名",
                 "员工姓名", "学生姓名", "身份证", "证件号码", "护照号", "车牌号",
                 "手机号码", "手机号", "联系电话", "电话号码", "电子邮箱", "邮箱地址",
                 "家庭住址", "通讯地址", "学号", "工号"],
    "health": ["病史", "既往史", "症状", "诊断", "用药", "药物名称", "病历",
               "过敏史", "手术史", "患者编号", "病历号"],
    "finance": ["年收入", "月收入", "个人收入", "工资", "薪资", "月薪", "年薪",
                "贷款金额", "房贷", "车贷", "月供", "首付", "存款", "负债", "债务",
                "公积金", "税前工资", "税后工资"],
}

# 身体指标中文词：在农业/地质/林业/畜牧等非人体上下文里同样存在（作物重量、岩体高度），
# 仅当页面上下文属于健康域时才计为个人信息。
STRONG_CN_CONTEXT = {
    "health": ["体重", "身高", "心率", "血压", "血糖", "体温", "孕周"],
}

# strong_en：英文语义基本无歧义（但仍排除少数“生成类”上下文）
STRONG_EN = {
    "identity": ["fullname", "full_name", "realname", "real_name", "idcard", "id_card",
                 "passport", "patientname", "patient_name", "patientid", "patient_id",
                 "studentid", "employeeid",
                 "contactname", "contact_name", "phonenumber", "phone_number",
                 "mobilephone", "emailaddress", "homeaddress"],
    "health": ["medicalhistory", "diagnosis", "medication", "bloodpressure", "bmi"],
    "finance": ["annualincome", "monthlyincome", "grossincome", "netincome",
                "salary", "mortgageamount", "loanamount", "downpayment"],
}

# weak_en：泛化英文词，仅当页面上下文属于对应语义域时才计入
WEAK_EN = {
    "identity": ["name", "contact", "owner", "patient", "student", "staff",
                 "employee", "phone", "mobile", "tel", "email", "mail", "address",
                 "username", "plate"],
    "health": ["weight", "height", "history", "allergy", "dose", "blood",
               "pressure", "symptom", "medicine"],
    "finance": ["income", "wage", "loan", "mortgage", "debt", "asset",
                "deposit", "principal"],
}

# 人体健康类工具目录（身体指标只在这些目录里视为个人信息；
# 农业/畜牧/林业/地质/纺织等目录里的 weight/height 是作物、岩体、织物参数）
HUMAN_DIRS = {
    "health", "healthcare", "medical", "medical2", "fitness", "sports", "nutrition",
    "rehabilitation", "cardiology", "nephrology", "dermatology", "cosmetic-derm",
    "tcm-diagnosis", "psychiatry", "psychology", "neurology", "pulmonology",
    "rheumatology", "ent", "ophthalmology", "dentistry", "urology", "obstetrics",
    "reproductive-medicine", "clinical-lab", "clinical-nursing", "pediatrics",
    "endocrinology", "gastroenterology", "hematology", "elderly", "parenting",
    "forensic-medicine", "acupuncture", "cognition", "beauty", "accessibility",
}

# 页面上下文语义域（title + h1 + meta description）
CTX_WORDS = {
    "health": ["健康", "医疗", "医学", "患者", "病人", "诊断", "临床", "护理", "康复",
               "体检", "用药", "病史", "bmi", "孕", "胎儿", "疾病",
               "医院", "药品", "剂量", "血压", "血糖", "症状", "量表",
               "health", "medical", "bmi", "patient", "clinical", "diagnosis"],
    "finance": ["收入", "工资", "薪资", "贷款", "房贷", "月供", "首付", "存款",
                "理财", "税", "公积金", "负债", "资产", "预算", "投资", "复利",
                "income", "salary", "loan", "mortgage", "tax", "finance"],
    "identity": ["简历", "名单", "通讯录", "员工", "学生", "患者", "报名", "客户",
                 "人事", "档案", "名片", "resume", "contact", "roster"],
}

# ── 低风险共享基础设施键（跨页共用是设计如此，不算冲突）──────────────────
SHARED_KEYS = {
    "theme", "toolbox_theme", "lang", "toolbox_lang", "i18n_lang",
    "favTools", "recentTools", "tb_chain_custom", "toolbox_chain_run",
    "toolbox_chain_payload", "toolbox_metrics_optin", "toolbox_metrics_log",
    "tb_ai_unlock", "toolbox_ai_unlock",
}
SHARED_KEY_PREFIXES = ("toolbox_ai_quota_", "tb_ux_", "tb_uxp_", "tbk_hist_", "pk:ans:")

# 写入动作：localStorage.setItem / sessionStorage.setItem / localStorage[key]=
STORE_WRITE_RE = re.compile(
    r"(?:window\.)?(localStorage|sessionStorage)\s*\.\s*setItem\s*\(", re.I)
STORE_READ_RE = re.compile(
    r"(?:window\.)?(localStorage|sessionStorage)\s*\.\s*getItem\s*\(", re.I)
STORE_BRACKET_RE = re.compile(
    r"(?:window\.)?(localStorage|sessionStorage)\s*\[\s*['\"`]([^'\"`]+)['\"`]\s*\]")
STORAGE_MENTION_RE = re.compile(r"(?:window\.)?(localStorage|sessionStorage)", re.I)
COOKIE_WRITE_RE = re.compile(r"document\.cookie\s*=")
IDB_RE = re.compile(r"\bindexedDB\b|\.open\s*\(\s*['\"`][^'\"`]*['\"`]\s*[,)]\s*"
                    r"(?:version|onupgradeneeded|objectStore)")

# 明文凭证：写入变量名/键名带这些词
CRED_RE = re.compile(
    r"(passw|password|passwd|pwd|secret|token|apikey|api_key|privatekey|private_key|"
    r"凭据|口令|密码|私钥|令牌)", re.I)
# 仅用于「键名即凭证」判定：不含裸 `pwd`，避免把 `tb_pwd_master`（加密派生值）误判为明文
CRED_STRONG_RE = re.compile(
    r"(passw|password|passwd|secret|apikey|api_key|privatekey|private_key|"
    r"credential|凭据|口令|密码|私钥|令牌)", re.I)

STRING_ARG_RE = re.compile(r"[`'\"]((?:[^`'\"\\]|\\.)*)[`'\"]")


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def read(p):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def html_files():
    out = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html"):
            out.append(os.path.join(ROOT, name))
    for sub in ("tools", "guides"):
        base = os.path.join(ROOT, sub)
        for dirpath, _, files in os.walk(base):
            for fn in sorted(files):
                if fn.endswith(".html"):
                    out.append(os.path.join(dirpath, fn))
    return out


def js_files():
    out = []
    base = os.path.join(ROOT, "js")
    for dirpath, _, files in os.walk(base):
        for fn in sorted(files):
            if fn.endswith(".js"):
                out.append(os.path.join(dirpath, fn))
    return out


def strip_script_strings(src):
    """粗略剔除 JS 字符串内容，避免把教学示例里的 `document.cookie =` 当成真写入。"""
    return re.sub(r"(?<!\\)'[^'\n]*'|\"[^\"\n]*\"|`[^`]*`", "''", src)


INPUT_RE = re.compile(r"<(input|textarea|select)\b[^>]*>", re.I)
ATTR_RE = re.compile(r"([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(\"[^\"]*\"|'[^']*')")
LABEL_RE = re.compile(r"<label\b[^>]*>(.*?)</label>", re.I | re.S)


def norm(s):
    return re.sub(r"<[^>]+>", " ", s or "").replace("&nbsp;", " ").strip()


def field_texts(html):
    """提取所有输入控件的可读字段名（id/name/placeholder/aria-label/关联 label 文本）。"""
    texts = []
    labels_by_for = {}
    for m in LABEL_RE.finditer(html):
        tag = m.group(0)
        fm = re.search(r"for\s*=\s*(\"[^\"]*\"|'[^']*')", tag, re.I)
        if fm:
            labels_by_for[fm.group(1).strip("'\"")] = norm(m.group(1))
    for m in INPUT_RE.finditer(html):
        attrs = {k.lower(): v.strip("'\"") for k, v in ATTR_RE.findall(m.group(0))}
        ftype = attrs.get("type", "").lower()
        if ftype in ("hidden", "button", "submit", "reset", "file", "image"):
            continue
        parts = [attrs.get("id", ""), attrs.get("name", ""), attrs.get("placeholder", ""),
                 attrs.get("aria-label", "")]
        fid = attrs.get("id", "")
        if fid and fid in labels_by_for:
            parts.append(labels_by_for[fid])
        texts.append(" ".join(p for p in parts if p).strip())
    return [t for t in texts if t]


def page_context(html):
    """页面语义域上下文：title + 第一个 h1 + meta description。"""
    parts = []
    for pat in (r"<title[^>]*>(.*?)</title>",
                r"<h1[^>]*>(.*?)</h1>",
                r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)'):
        m = re.search(pat, html, re.I | re.S)
        if m:
            parts.append(norm(m.group(1)))
    return " ".join(parts).lower()


def context_domains(ctx):
    doms = set()
    for dom, words in CTX_WORDS.items():
        for w in words:
            if w.lower() in ctx:
                doms.add(dom)
                break
    return doms


def classify_sensitive(field_strs, html, rp=""):
    hits = {}
    ctx = page_context(html)
    doms = context_domains(ctx)
    parts = rp.split("/")
    human_dir = len(parts) > 2 and parts[0] == "tools" and parts[1] in HUMAN_DIRS
    for cat, words in STRONG_CN.items():
        for w in words:
            if any(w in s for s in field_strs):
                hits.setdefault(cat, set()).add(w)
    for cat, words in STRONG_CN_CONTEXT.items():
        if not human_dir:
            continue
        for w in words:
            if any(w in s for s in field_strs):
                hits.setdefault(cat, set()).add(w)
    for cat, words in STRONG_EN.items():
        if cat == "health" and not human_dir:
            continue
        for w in words:
            for s in field_strs:
                sl = s.lower()
                if w in sl:
                    hits.setdefault(cat, set()).add(w)
    for cat, words in WEAK_EN.items():
        if cat == "health":
            if not human_dir:
                continue
        elif cat not in doms:
            continue
        for w in words:
            for s in field_strs:
                sl = s.lower()
                # 完整单词匹配，避免 "username" 被 "name" 命中
                if re.search(r"\b%s\b" % re.escape(w), sl):
                    hits.setdefault(cat, set()).add(w)
    return {k: sorted(v) for k, v in hits.items()}


ALIAS_DECL_RE = re.compile(
    r"\b([A-Za-z_$][\w$]*)\s*=\s*(?:window\.)?(localStorage|sessionStorage)\b")


def storage_aliases(src):
    """`const HISTORY_STORE = sessionStorage` 之类的别名。"""
    return {name: kind for name, kind in ALIAS_DECL_RE.findall(src)}


def iter_storage_writes(src):
    """遍历所有 storage 写入（含别名），产出 (start, call_snippet, kind)。"""
    for m in STORE_WRITE_RE.finditer(src):
        yield m.start(), src[m.start():m.start() + 400], m.group(1)
    for name, kind in storage_aliases(src).items():
        for m in re.finditer(r"\b%s\s*\.\s*setItem\s*\(" % re.escape(name), src):
            yield m.start(), src[m.start():m.start() + 400], kind


def resolve_key_expr(src, expr):
    """把 storage 调用的第一个参数解析成字面量键（支持常量回查/模板前缀）。"""
    expr = expr.strip()
    lit = re.match(r"[`'\"]([^`'\"]+)[`'\"]$", expr)
    if lit:
        return lit.group(1)
    ident = re.match(r"([A-Za-z_$][\w$]*)$", expr)
    if ident:
        decl = re.search(r"\b%s\s*=\s*[`'\"]([^`'\"]+)[`'\"]" % re.escape(ident.group(1)), src)
        if decl:
            return decl.group(1)
    return None


def extract_literal_keys(src, stype=None):
    """从 setItem/getItem/removeItem/方括号 提取字面量键（含别名与常量）。"""
    keys = set()
    aliases = storage_aliases(src)
    stores = ["localStorage", "sessionStorage"] + list(aliases)
    pat = r"\b(%s)\s*\.\s*(?:setItem|getItem|removeItem)\s*\(\s*([^,)]+)" % \
          "|".join(re.escape(s) for s in stores)
    for m in re.finditer(pat, src):
        raw_store, expr = m.group(1), m.group(2)
        kind = raw_store if raw_store in ("localStorage", "sessionStorage") \
            else aliases.get(raw_store, "localStorage")
        val = resolve_key_expr(src, expr)
        if not val or "$" in val or "+" in val:
            continue
        keys.add((kind, val))
    for m in STORE_BRACKET_RE.finditer(src):
        keys.add((m.group(1), m.group(2)))
    return keys


def extract_dynamic_prefixes(src):
    """提取 `'prefix' + var` 形式的动态键前缀。"""
    out = set()
    for m in re.finditer(
            r"(?:window\.)?(?:localStorage|sessionStorage)\s*\.\s*setItem\s*\(\s*"
            r"([`'\"][^`'\"]+[`'\"])\s*\+", src):
        out.add(m.group(1).strip("`'\""))
    return out


def detect_export(src):
    return bool(re.search(r"downloadText|downloadBlob|Blob\(|createObjectURL|toCSV|"
                          r"导出|download=", src, re.I))


# 业务中间态键：草稿 / 历史 / 记录 / 队列 / 名单
BUSINESS_KEY_RE = re.compile(
    r"(hist|history|draft|record|records|list|queue|save|patients|meds|contacts|"
    r"staff|customers|leases|orders|cart|results|notes|messages|schedule|roster|"
    r"inventory|log|logs)", re.I)

HASH_LIKE_RE = re.compile(r"hash|sha\w*\s*\(|digest|enc\w*\s*\(|btoa|subtle\.digest", re.I)
PASSWORD_INPUT_RE = re.compile(r"<input[^>]*>", re.I)
TYPE_PASSWORD_RE = re.compile(r'type\s*=\s*["\']?password', re.I)


def credential_violation(src):
    """检测「明文凭证落盘」：密码字段值 / 密码类键 / token 变量直接写入 storage。"""
    pwd_ids = set()
    for m in PASSWORD_INPUT_RE.finditer(src):
        tag = m.group(0)
        if not TYPE_PASSWORD_RE.search(tag):
            continue
        for pat in (r'\bid\s*=\s*["\']([^"\']+)', r'\bname\s*=\s*["\']([^"\']+)'):
            mm = re.search(pat, tag, re.I)
            if mm:
                pwd_ids.add(mm.group(1))

    for start, call, _kind in iter_storage_writes(src):
        window = src[max(0, start - 700):start + 500]
        km = re.search(r"setItem\s*\(\s*[`'\"]([^`'\"]+)[`'\"]", call)
        key = km.group(1) if km else ""
        if not key:
            # 键为常量变量：回查声明处的字面量（如 const HISTORY_KEY = 'password_generator_session_history'）
            idm = re.search(r"setItem\s*\(\s*([A-Za-z_$][\w$]*)\s*,", call)
            if idm:
                decl = re.search(r"\b%s\s*=\s*[`'\"]([^`'\"]+)[`'\"]" % re.escape(idm.group(1)), src)
                if decl:
                    key = decl.group(1)
        vm = re.search(r"setItem\s*\(\s*(?:[`'\"][^`'\"]*[`'\"]|[^,\n]+)\s*,\s*([^;\n]{0,220})",
                       call)
        value = vm.group(1) if vm else ""
        hash_like = bool(HASH_LIKE_RE.search(value))

        # 1) 直接把 type=password 控件的值写盘（哈希/加密后落盘不算明文凭证）
        if (not hash_like and pwd_ids and re.search(r"\.value\b", value)
                and any(pid in window for pid in pwd_ids)):
            return {"kind": "password-field", "key": key or "?", "field": sorted(pwd_ids)[0]}
        # 2) 键名即凭证语义（password_generator_session_history 等）
        if key and CRED_STRONG_RE.search(key) and not hash_like:
            return {"kind": "credential-key", "key": key}
        # 3) 值表达式直接是密码/令牌变量
        if not hash_like:
            vm2 = re.search(r"\b(password|passwd|pwd|secret|apiKey|api_key|token|"
                            r"privateKey|private_key)\b", value, re.I)
            if vm2:
                return {"kind": "credential-value", "key": key or "?", "var": vm2.group(1)}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    ap.add_argument("--check", action="store_true",
                    help="存在硬违规（Cookie/IndexedDB/明文凭证/跨页键冲突）或 0 页面时退出码 1")
    args = ap.parse_args()

    pages = html_files() + js_files()
    records = []
    violations_cookie = []
    violations_idb = []
    violations_cred = []
    key_users = {}

    for p in pages:
        src = read(p)
        rp = rel(p)
        is_js = rp.startswith("js/")
        stripped = strip_script_strings(src) if not is_js else src

        ls_use = len(re.findall(r"(?:window\.)?localStorage", src))
        ss_use = len(re.findall(r"(?:window\.)?sessionStorage", src))
        cookie_w = len(COOKIE_WRITE_RE.findall(stripped))
        idb = bool(IDB_RE.search(stripped))

        literal_keys = extract_literal_keys(src)
        dynamic_prefixes = extract_dynamic_prefixes(src)
        fields = [] if is_js else field_texts(src)
        sens = classify_sensitive(fields, src, rel(p))

        # data-no-persist：tool-ux 自动持久化关闭（显式保存仍可能生效）
        no_persist = bool(re.search(r"data-no-persist", src))
        uses_ux = bool(re.search(r"tool-ux\.js|/js/tool-ux\.js", src))
        uses_kit = bool(re.search(r"tool-kit\.js|/js/tool-kit\.js", src))
        uses_history = bool(re.search(r"TBKit\.history|ToolKit\.history|history\.record\s*\(", src))

        cred_hit = credential_violation(src)

        # 显式自定义键（非共享基础设施）
        custom_keys = []
        for stype, k in sorted(literal_keys):
            if k in SHARED_KEYS or any(k.startswith(pre) for pre in SHARED_KEY_PREFIXES):
                continue
            if k.startswith("toolbox_theme") or k == "theme":
                continue
            custom_keys.append((stype, k))
        for pre in sorted(dynamic_prefixes):
            if pre in SHARED_KEYS or any(pre.startswith(s) for s in SHARED_KEY_PREFIXES):
                continue
            custom_keys.append(("dynamic", pre + "*"))

        # 持久化是否实际生效（data-no-persist 只关闭 tool-ux 自动回填）
        persist_active = (uses_ux and not no_persist) or bool(custom_keys) or uses_history

        # 风险分档
        tier = 0
        reason = []
        business_keys = [k for _, k in custom_keys if BUSINESS_KEY_RE.search(k)]
        if not (ls_use or ss_use or cookie_w or idb):
            tier = 0
        elif sens and persist_active:
            tier = 1
            reason.append("敏感字段:" + "/".join("%s(%s)" % (k, ",".join(v)) for k, v in sens.items()))
        elif business_keys or (uses_history and not is_js):
            tier = 2
            reason.append("业务中间态:" + (",".join(business_keys[:5]) or "history"))
        elif custom_keys:
            tier = 3
            reason.append("本地统计/设置:" + ",".join(k for _, k in custom_keys[:5]))
        elif sens:
            tier = 3
            reason.append("敏感字段但已由 data-no-persist 关闭自动保存")
        else:
            tier = 3
            reason.append("仅偏好/本地统计")

        rec = {
            "path": rp,
            "kind": "js" if is_js else "page",
            "localStorage_refs": ls_use,
            "sessionStorage_refs": ss_use,
            "cookie_writes": cookie_w,
            "indexeddb": idb,
            "literal_keys": sorted(k for _, k in literal_keys),
            "dynamic_prefixes": sorted(dynamic_prefixes),
            "custom_keys": [{"store": s, "key": k} for s, k in custom_keys],
            "sensitive": sens,
            "fields_sampled": fields[:8],
            "tier": tier,
            "reason": reason,
            "uses_tool_ux": uses_ux,
            "uses_tool_kit": uses_kit,
            "data_no_persist": no_persist,
            "export": detect_export(src),
            "cred_hit": cred_hit,
        }
        records.append(rec)

        if cookie_w:
            violations_cookie.append({"path": rp, "count": cookie_w})
        if idb:
            violations_idb.append({"path": rp})
        if cred_hit:
            violations_cred.append({"path": rp, **cred_hit})

        for stype, k in literal_keys:
            if k in SHARED_KEYS or any(k.startswith(pre) for pre in SHARED_KEY_PREFIXES):
                continue
            if k == "theme" or k.startswith("toolbox_theme"):
                continue
            key_users.setdefault((stype, k), []).append(rp)

    conflicts = []
    for (stype, k), users in sorted(key_users.items()):
        page_users = [u for u in users if not u.startswith("js/")]
        if len(page_users) >= 2:
            conflicts.append({"store": stype, "key": k, "users": sorted(page_users)})

    summary = {
        "scanned": len(records),
        "pages": sum(1 for r in records if r["kind"] == "page"),
        "js": sum(1 for r in records if r["kind"] == "js"),
        "tier1": [r for r in records if r["tier"] == 1],
        "tier2": [r for r in records if r["tier"] == 2],
        "tier3": [r for r in records if r["tier"] == 3],
        "tier0": [r for r in records if r["tier"] == 0],
        "violations": {
            "cookie_write": violations_cookie,
            "indexeddb": violations_idb,
            "plaintext_credential": violations_cred,
            "cross_page_conflicts": conflicts,
        },
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"summary_counts": {k: len(v) if isinstance(v, list) else v
                                          for k, v in summary.items() if k != "tier0"},
                       "records": records}, f, ensure_ascii=False, indent=1)

    page_recs = [r for r in records if r["kind"] == "page"]
    print("扫描文件：%d（页面 %d / JS %d）" % (summary["scanned"], summary["pages"], summary["js"]))
    print("分档（页面口径）：Tier1 高风险 %d，Tier2 中风险 %d，Tier3 低风险 %d，无存储 %d"
          % (sum(1 for r in page_recs if r["tier"] == 1),
             sum(1 for r in page_recs if r["tier"] == 2),
             sum(1 for r in page_recs if r["tier"] == 3),
             sum(1 for r in page_recs if r["tier"] == 0)))
    print("违规：Cookie 写入 %d，IndexedDB %d，明文凭证 %d，跨页键冲突 %d"
          % (len(violations_cookie), len(violations_idb), len(violations_cred), len(conflicts)))

    if args.check:
        if summary["pages"] == 0:
            print("❌ 0 个页面被扫描，拒绝判绿")
            return 1
        if violations_cookie or violations_idb or violations_cred or conflicts:
            print("❌ 存在硬违规，拒绝判绿")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
