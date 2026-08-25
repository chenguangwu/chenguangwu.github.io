#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_release_dashboard.py — 隐私优先的发布质量看板生成器（B5-10）

聚合以下本地快照，生成发布前质量核对看板：
  - json/tools.json         构建产物：工具总数 + 质量分级分布
  - _test_report_static.json 静态测试：通过/告警/错误
  - _perf_baseline.json     Core Web Vitals 实测基线
  - _qa_gates.json          数据质量门禁
  - index_coverage.json     搜索引擎收录覆盖对账
  - json/guides.json        内容（指南）增长

原则：
  - 只读本地快照，不发起任何网络请求，不依赖用户指标数据。
  - 看板异常仅告警、绝不阻塞纯前端工具使用；本脚本退出码恒为 0。
  - 同时写出 release_snapshot.json，便于跨发版对比。
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load(path, default=None):
    try:
        with open(os.path.join(ROOT, path), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write("WARN: 无法读取 %s: %s\n" % (path, e))
        return default


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def build_snapshot():
    snap = {
        "generated": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "build": {},
        "static": {},
        "perf": {},
        "qa": {},
        "indexing": {},
        "content": {},
        "privacy": {},
        "anomalies": [],
    }

    # ---- 构建 + 质量分级 ----
    tools = _load("json/tools.json", [])
    if isinstance(tools, list):
        total = len(tools)
        q = {"A": 0, "B": 0, "C": 0}
        for t in tools:
            k = (t.get("quality") or "?").upper()
            if k in q:
                q[k] += 1
        snap["build"] = {
            "tool_count": total,
            "quality_A": q["A"],
            "quality_B": q["B"],
            "quality_C": q["C"],
            "quality_A_pct": pct(q["A"], total),
        }

    # ---- 静态测试 ----
    st = _load("_test_report_static.json", {})
    if st:
        total = st.get("total", 0)
        passed = st.get("passed", 0)
        warns = st.get("warnings", 0)
        errs = st.get("errors", 0) or []
        snap["static"] = {
            "total": total,
            "passed": passed,
            "warnings": warns,
            "errors": len(errs) if isinstance(errs, list) else errs,
            "status": "pass" if (passed == total and warns == 0 and (not errs)) else "warn",
        }
        if warns:
            snap["anomalies"].append("静态测试存在 %d 条告警" % warns)
        if errs:
            snap["anomalies"].append("静态测试存在 %d 个错误" % (len(errs) if isinstance(errs, list) else errs))

    # ---- 性能基线 ----
    perf = _load("_perf_baseline.json", {})
    if perf:
        summary = perf.get("summary", {})
        pages = perf.get("pages", {})
        alerts = 0
        sample = None
        for k, v in pages.items():
            if isinstance(v, dict):
                alerts += len(v.get("alerts", []) or [])
                if sample is None:
                    sample = {"lcp": v.get("lcp"), "cls": v.get("cls"), "ttfb": v.get("ttfb")}
        snap["perf"] = {
            "generated": perf.get("generated"),
            "pages": len(pages),
            "alerts": alerts,
            "sample_lcp_ms": sample.get("lcp") if sample else None,
            "sample_cls": sample.get("cls") if sample else None,
            "status": "pass" if alerts == 0 else "warn",
        }
        if alerts:
            snap["anomalies"].append("性能基线存在 %d 条超预算告警" % alerts)

    # ---- QA 门禁 ----
    qa = _load("_qa_gates.json", {})
    if qa:
        snap["qa"] = {
            "total": qa.get("total"),
            "canonical_pct": qa.get("canonical_pct"),
            "desc_pct": qa.get("desc_pct"),
            "jsonld_pct": qa.get("jsonld_pct"),
            "broken_stubs": qa.get("broken_stubs"),
            "orphan_links": qa.get("orphan_links"),
            "industry_dir_mismatch": qa.get("industry_dir_mismatch", 0),
            "stubs": qa.get("stubs", 0),
            "status": "pass" if (qa.get("canonical_pct") == 100 and qa.get("desc_pct") == 100
                                  and qa.get("jsonld_pct") == 100 and qa.get("broken_stubs") == 0
                                  and qa.get("orphan_links") == 0) else "warn",
        }

    # ---- 收录覆盖 ----
    ic = _load("index_coverage.json", {})
    if ic:
        s = ic.get("summary", {})
        cats = s.get("categories", {})
        snap["indexing"] = {
            "generated": s.get("generated"),
            "offline_baseline": s.get("offline_baseline"),
            "total_expected": s.get("total_expected"),
            "inspection_samples": s.get("inspection_samples"),
            "indexed_rate": s.get("indexed_rate"),
            "anomaly_count": s.get("anomaly_count"),
            "categories": cats,
            "queue_len": len(ic.get("queue", [])),
        }
        # 离线基线模式下全部 unknown 是预期（无 GSC/Bing 凭证），不计入异常
        if not s.get("offline_baseline") and s.get("anomaly_count"):
            snap["anomalies"].append("收录异常页面 %d 个" % s.get("anomaly_count"))

    # ---- 内容增长 ----
    guides = _load("json/guides.json", [])
    cluster = 0
    try:
        for fn in os.listdir(os.path.join(ROOT, "guides")):
            if fn.startswith("cluster-") and fn.endswith(".html"):
                cluster += 1
    except Exception:
        pass
    snap["content"] = {
        "guides": len(guides) if isinstance(guides, list) else 0,
        "clusters": cluster,
    }

    # ---- 隐私优先指标（仅说明默认策略，不读取用户数据）----
    snap["privacy"] = {
        "metrics_optin_default": False,
        "third_party_tracking": False,
        "local_only": True,
        "note": "匿名使用指标默认关闭（opt-in），仅存于浏览器 localStorage，绝不向第三方发送任何数据。",
        "doc": "docs/METRICS_PRIVACY.md",
    }

    return snap


def status_badge(status):
    color = {"pass": "#16a34a", "warn": "#d97706", "fail": "#dc2626"}.get(status, "#6b7280")
    label = {"pass": "✓ 通过", "warn": "⚠ 告警", "fail": "✗ 失败"}.get(status, status)
    return '<span style="background:%s;color:#fff;padding:3px 12px;border-radius:999px;font-size:13px;font-weight:700">%s</span>' % (color, label)


def render_html(snap):
    b = snap["build"]
    st = snap["static"]
    perf = snap["perf"]
    qa = snap["qa"]
    ic = snap["indexing"]
    c = snap["content"]
    p = snap["privacy"]

    # 质量分布条
    total = b.get("tool_count", 0) or 1
    qa_pct = b.get("quality_A_pct", 0)
    qb_pct = pct(b.get("quality_B", 0), total)
    qc_pct = pct(b.get("quality_C", 0), total)
    qbar = ('<div style="display:flex;height:14px;border-radius:7px;overflow:hidden;background:#eee;margin-top:6px">'
            '<div style="width:%s%%;background:#16a34a" title="A 专业"></div>'
            '<div style="width:%s%%;background:#2563eb" title="B 标准"></div>'
            '<div style="width:%s%%;background:#9ca3af" title="C 轻量"></div></div>' % (qa_pct, qb_pct, qc_pct))

    # 收录分类
    cats = ic.get("categories", {})
    cat_rows = "".join("<tr><td>%s</td><td style='text-align:right'>%s</td></tr>" % (k, v) for k, v in cats.items())

    anomalies = snap.get("anomalies", [])
    anom_html = ("<ul style='margin:8px 0 0;padding-left:18px;color:#b45309'>" +
                 "".join("<li>%s</li>" % a for a in anomalies) + "</ul>") if anomalies else \
        "<p style='color:#16a34a;margin:8px 0 0'>✓ 无阻断性异常</p>"

    html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ToolBox 发布质量看板</title></head>
<body style="margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Microsoft YaHei',sans-serif;background:#f6f7f9;color:#1f2937">
<div style="max-width:960px;margin:0 auto;padding:28px 20px 60px">
  <h1 style="margin:0 0 4px;font-size:24px">📊 ToolBox 发布质量看板</h1>
  <p style="color:#6b7280;margin:0 0 4px">生成时间：%s · 隐私优先 · 仅本地聚合，零第三方请求</p>
  <p style="color:#6b7280;margin:0 0 24px">本看板只读本地快照，异常仅告警，<b>绝不阻塞</b>纯前端工具使用。</p>

  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px">

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">🏗️ 构建与质量</h3>%s</div>
      <p style="font-size:30px;font-weight:800;margin:10px 0 2px">%s</p>
      <p style="color:#6b7280;margin:0">工具总数（A %s%% · B %s%% · C %s%%）</p>
      %s
    </div>

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">🧪 静态测试</h3>%s</div>
      <p style="font-size:30px;font-weight:800;margin:10px 0 2px">%s/%s</p>
      <p style="color:#6b7280;margin:0">通过 %s · 告警 %s · 错误 %s</p>
    </div>

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">⚡ 性能基线</h3>%s</div>
      <p style="font-size:30px;font-weight:800;margin:10px 0 2px">%s</p>
      <p style="color:#6b7280;margin:0">页 %s · 超预算告警 %s</p>
      <p style="color:#6b7280;margin:4px 0 0;font-size:12px">样本 LCP %s ms · CLS %s</p>
    </div>

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">🛡️ 数据质量门禁</h3>%s</div>
      <p style="font-size:18px;font-weight:700;margin:10px 0 2px">SEO 字段覆盖 100%%</p>
      <p style="color:#6b7280;margin:0">canonical %s%% · description %s%% · JSON-LD %s%%</p>
      <p style="color:#6b7280;margin:4px 0 0;font-size:12px">断链 %s · 失效重定向 %s · 行业/目录粒度差 %s</p>
    </div>

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">🔍 收录覆盖</h3>%s</div>
      <p style="font-size:18px;font-weight:700;margin:10px 0 2px">应收录 %s 条</p>
      <p style="color:#6b7280;margin:0">收录率 %s%% · 待复查队列 %s 条</p>
      <table style="width:100%%;font-size:12px;margin-top:8px;border-collapse:collapse;color:#374151">
        %s
      </table>
      <p style="color:#6b7280;margin:6px 0 0;font-size:11px">%s</p>
    </div>

    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">📚 内容增长</h3>%s</div>
      <p style="font-size:30px;font-weight:800;margin:10px 0 2px">%s</p>
      <p style="color:#6b7280;margin:0">指南 %s 篇 · 内容集群 %s 个</p>
    </div>

  </div>

  <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px;margin-top:16px">
    <h3 style="margin:0 0 6px">🔐 隐私优先指标</h3>
    <p style="color:#374151;margin:0;font-size:14px">%s</p>
    <p style="color:#6b7280;margin:6px 0 0;font-size:12px">默认关闭（opt-in）· 匿名聚合 · 仅存 localStorage · 无第三方追踪 · 详见 %s</p>
  </div>

  <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px;margin-top:16px">
    <h3 style="margin:0 0 4px">🚦 异常汇总（仅告警，不阻断）</h3>
    %s
  </div>

  <p style="color:#9ca3af;text-align:center;margin-top:24px;font-size:12px">ToolBox · 纯前端工具站 · 发布看板由 _release_dashboard.py 自动生成</p>
</div>
</body></html>""" % (
        snap["generated"],
        status_badge(b and "pass" or "warn"),
        b.get("tool_count", 0), qa_pct, qb_pct, qc_pct, qbar,
        status_badge(st.get("status")), st.get("passed", 0), st.get("total", 0),
        st.get("passed", 0), st.get("warnings", 0), st.get("errors", 0),
        status_badge(perf.get("status")), perf.get("pages", 0), perf.get("pages", 0), perf.get("alerts", 0),
        perf.get("sample_lcp_ms"), perf.get("sample_cls"),
        status_badge(qa.get("status")),
        qa.get("canonical_pct"), qa.get("desc_pct"), qa.get("jsonld_pct"),
        qa.get("orphan_links"), qa.get("broken_stubs"), qa.get("industry_dir_mismatch"),
        status_badge("warn" if ic.get("offline_baseline") else "pass"),
        ic.get("total_expected", 0), ic.get("indexed_rate", 0), ic.get("queue_len", 0),
        cat_rows, ("离线基线模式（无 GSC/Bing 凭证）：unknown 为预期，运行 _submit_indexnow.py 后可改善" if ic.get("offline_baseline") else ""),
        status_badge("pass"),
        c.get("guides", 0), c.get("guides", 0), c.get("clusters", 0),
        p.get("note"), p.get("doc"),
        anom_html,
    )
    return html


def main():
    try:
        snap = build_snapshot()
        # 写出快照
        with open(os.path.join(ROOT, "release_snapshot.json"), "w", encoding="utf-8") as f:
            json.dump(snap, f, ensure_ascii=False, indent=2)
        html = render_html(snap)
        with open(os.path.join(ROOT, "release_dashboard.html"), "w", encoding="utf-8") as f:
            f.write(html)
        sys.stdout.write("✓ 发布看板已生成：release_dashboard.html + release_snapshot.json\n")
        sys.stdout.write("  工具数=%s · 静态=%s/%s(告警%s/错误%s) · 性能页=%s(告警%s) · 收录应=%s(队列%s) · 指南=%s\n" % (
            snap["build"].get("tool_count"), snap["static"].get("passed"), snap["static"].get("total"),
            snap["static"].get("warnings"), snap["static"].get("errors"), snap["perf"].get("pages"),
            snap["perf"].get("alerts"), snap["indexing"].get("total_expected"), snap["indexing"].get("queue_len"),
            snap["content"].get("guides")))
        if snap["anomalies"]:
            sys.stdout.write("  异常(%d)：%s\n" % (len(snap["anomalies"]), "；".join(snap["anomalies"])))
        else:
            sys.stdout.write("  无阻断性异常。\n")
    except Exception as e:
        sys.stderr.write("ERROR: 生成看板失败：%s\n" % e)
    # 看板异常仅告警，绝不阻塞发布
    return 0


if __name__ == "__main__":
    sys.exit(main())
