#!/usr/bin/env python3
"""Fetch a 51.la V6 overview snapshot without storing credentials."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import string
import time
import urllib.request
from pathlib import Path


API_URL = "https://v6-open.51.la/open"


def signed_payload(access_key: str, secret_key: str, extra: dict[str, str]) -> dict[str, object]:
    payload: dict[str, object] = {
        "accessKey": access_key,
        "nonce": "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4)),
        "timestamp": int(time.time() * 1000),
        **extra,
    }
    sign_params = {
        "accessKey": access_key,
        "nonce": payload["nonce"],
        "timestamp": payload["timestamp"],
        "secretKey": secret_key,
    }
    query = "&".join(f"{key}={sign_params[key]}" for key in sorted(sign_params))
    payload["sign"] = hashlib.sha256(query.encode("utf-8")).hexdigest().upper()
    return payload


def request_api(path: str, payload: dict[str, object]) -> dict:
    request = urllib.request.Request(
        API_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mask-id", help="51.la 统计 ID; omit to list available sites")
    parser.add_argument("--output", type=Path, default=Path("51la_overview.json"))
    args = parser.parse_args()

    access_key = os.environ.get("51LA_ACCESS_KEY", "").strip()
    secret_key = os.environ.get("51LA_SECRET_KEY", "").strip()
    if not access_key or not secret_key:
        raise SystemExit("请先设置 51LA_ACCESS_KEY 和 51LA_SECRET_KEY")

    if args.mask_id:
        result = request_api("/overview/get", signed_payload(access_key, secret_key, {"maskId": args.mask_id}))
    else:
        result = request_api("/sitegroup/list", signed_payload(access_key, secret_key, {}))

    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写入 {args.output}")


if __name__ == "__main__":
    main()
