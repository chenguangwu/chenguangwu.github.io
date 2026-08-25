# -*- coding: utf-8 -*-
"""P3b/P2 共用：把无意义的"存记录"工具替换为重定向桩（指向本行业索引页）。

机制（同 P2 去重桩，已验证零死链）：
- 文件替换为含 `<!-- TOOLBOX-REDIRECT -->` 的桩，HTTP-refresh + canonical + JS 跳转。
- `_build.py`/`_audit_links` 均跳过桩文件 → 旧 URL 不丢、索引/搜索自动剔除。
- 幂等：已是桩则跳过；不存在则报 missing。

用法：
  python3 scripts/delete_tool_stub.py --list '[["optical","analysis-82"],["yoga","analysis-retention"]]'
  （--list 为 JSON 数组，元素可为 [ind, slug] 或 {"ind":,"slug":,"target":}）
"""
import os, re, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")


def make_stub(title, url):
    return (
        '<!DOCTYPE html>\n'
        '<!-- TOOLBOX-REDIRECT -->\n'
        '<html lang="zh-CN"><head><meta charset="UTF-8">\n'
        '<meta http-equiv="refresh" content="0;url=%s">\n'
        '<link rel="canonical" href="%s">\n'
        '<meta name="robots" content="noindex,follow">\n'
        '<script src="/js/clarity.js" defer></script>\n'
        "<title>%s</title></head>\n"
        '<body><p>该工具已整合至 <a href="%s">对应分类页</a>。</p>\n'
        "<script>window.location.href='%s';</script></body></html>"
        % (url, url, title, url, url)
    )


def delete(ind, slug, target=None):
    fp = os.path.join(TOOLS_DIR, ind, slug + ".html")
    if not os.path.exists(fp):
        return "missing"
    c = open(fp, encoding="utf-8").read()
    if "TOOLBOX-REDIRECT" in c:
        return "skip"
    m = re.search(r"<title>(.*?)</title>", c)
    title = m.group(1) if m else slug
    url = target or ("/tools/%s/index.html" % ind)
    open(fp, "w", encoding="utf-8").write(make_stub(title, url))
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", required=True, help="JSON 数组：[[ind,slug],...] 或 [{ind,slug,target}]")
    args = ap.parse_args()
    items = json.loads(args.list)
    stats = {}
    for it in items:
        if isinstance(it, dict):
            ind, slug = it["ind"], it["slug"]
            tgt = it.get("target")
        else:
            ind, slug = it[0], it[1]
            tgt = None
        r = delete(ind, slug, tgt)
        stats[r] = stats.get(r, 0) + 1
    print("删除桩结果:", stats)


if __name__ == "__main__":
    main()
