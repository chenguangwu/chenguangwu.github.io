#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""51.la 开放 API：访问明细 / 受访页面拉取（URL 级真实站内流量）。

用法（密钥仅从环境变量读取，绝不硬编码 / 不写仓库）：
    LA_ACCESS_KEY=... LA_SECRET_KEY=... [LA_MASK_ID=...] \\
        python3 scripts/fetch_51la_pagedetail.py [--endpoint page|visit] [--page 1]

端点：
    --endpoint page   -> /page/all      受访页面排行（url + pv + uv），SEO-C/D 主数据源
    --endpoint visit  -> /visit/detail  访问明细日志（逐条访问），备用

接口权限：概览 /overview/get 已验证 level-2 签名通过；URL 级明细 /page/all、
/visit/detail 在 API 应用未开通「页面分析/访问明细」权限前返回 5005，需在
51.la 控制台「数据开放平台」为该 API 应用开通对应接口权限后本脚本方可取到数据。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import string
import subprocess
import sys
import time
from pathlib import Path

API_URL = "https://v6-open.51.la/open"
DEFAULT_MASK_ID = "3R0rVW6KKmLfdAFz"  # 项目 51.la V6 统计 ID（analytics.js 中）
ROOT = Path(__file__).resolve().parent.parent
ENDPOINTS = {"page": "/page/all", "visit": "/visit/detail"}


def signed_payload(access_key: str, secret_key: str, extra: dict, level: int = 2) -> dict:
    payload = {
        "accessKey": access_key,
        "nonce": "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4)),
        "timestamp": int(time.time() * 1000),
        **extra,
    }
    if level == 1:
        payload["sign"] = access_key
    else:
        sign_params = {
            "accessKey": access_key,
            "nonce": payload["nonce"],
            "timestamp": payload["timestamp"],
            "secretKey": secret_key,
        }
        query = "&".join(f"{k}={sign_params[k]}" for k in sorted(sign_params))
        payload["sign"] = hashlib.sha256(query.encode("utf-8")).hexdigest().upper()
    return payload


def request_api(path: str, payload: dict) -> dict:
    body = json.dumps(payload)
    cmd = ["curl", "-s", "-X", "POST", API_URL + path,
           "-H", "Content-Type: application/json", "-d", body, "--max-time", "30"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=40).stdout
    except Exception as e:  # noqa: BLE001
        return {"_err": str(e)}
    try:
        return json.loads(out)
    except Exception:  # noqa: BLE001
        return {"_raw": out[:600]}


def _extract_rows(bean: object) -> list:
    if isinstance(bean, list):
        return bean
    if isinstance(bean, dict):
        for key in ("list", "data", "items", "records", "pageList"):
            if isinstance(bean.get(key), list):
                return bean[key]
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--endpoint", choices=ENDPOINTS, default="page")
    ap.add_argument("--page", type=int, default=1)
    args = ap.parse_args()

    ak = os.environ.get("LA_ACCESS_KEY", "").strip()
    sk = os.environ.get("LA_SECRET_KEY", "").strip()
    mid = os.environ.get("LA_MASK_ID", DEFAULT_MASK_ID).strip()
    if not ak or not sk:
        raise SystemExit("请设置 LA_ACCESS_KEY / LA_SECRET_KEY（从环境变量，勿硬编码）")

    path = ENDPOINTS[args.endpoint]
    payload = signed_payload(ak, sk, {"maskId": mid, "page": args.page}, level=2)
    resp = request_api(path, payload)
    print("原始返回:", json.dumps(resp, ensure_ascii=False)[:900])

    if not resp.get("success"):
        code = resp.get("code")
        msg = resp.get("message")
        if str(code) == "5005":
            print(f"\n[阻塞] 接口 {path} 返回 5005：需在 51.la 控制台「数据开放平台」为该 API 应用开通"
                  f"「页面分析/访问明细」接口权限后重试。脚本已就绪，权限一开即跑。")
        else:
            print(f"\n[失败] 接口 {path}：{code} {msg}")
        return 2

    rows = _extract_rows(resp.get("bean"))
    out = {
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "endpoint": args.endpoint,
        "mask_id": mid,
        "count": len(rows),
        "rows": rows,
    }
    fname = "analytics_51la_pagedetail.json" if args.endpoint == "page" else "analytics_51la_visitdetail.json"
    (ROOT / "json" / fname).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n已存档 json/{fname}（{len(rows)} 条）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
