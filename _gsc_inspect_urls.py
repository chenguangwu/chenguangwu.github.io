#!/usr/bin/env python3
"""
GSC URL Inspection API 收录监控脚本（v3：token 运行期续期版）
功能: 批量查询 URL 的收录状态，输出「未收录」清单（发现未抓取/抓取未收录/被排除）

用法:
  手动:  python3 _gsc_inspect_urls.py [--limit 1900] [--credential PATH]
  cron:  python3 _gsc_inspect_urls.py >> _gsc_inspect.log 2>&1

依赖: google-auth + requests（已安装到 managed venv）
  /Users/cgw/.workbuddy/binaries/python/envs/default/bin/pip install google-auth requests

前置条件（一次性配置）:
  1. Google Cloud Console 创建项目，启用 "Google Search Console API"
  2. 创建服务账号并下载 JSON 凭证
  3. 在 GSC → 设置 → 用户和权限，把服务账号邮箱添加为「所有者」
  4. 把凭证 JSON 放到默认路径（或 --credential 指定）

配额:
  URL Inspection API: 约 2000 次/天/站点，600 次/分钟
  limit 控制「本轮 API 调用上限（含重试）」，默认 1900 留余量；0=不限

v2→v3 关键修复（针对 8/11~8/20 运行暴露的根本问题）:
  - 8/11 误判为「国内网络超时导致低成功率」，实测失败 100% 是 401（NETERR/429/5xx 全为 0）。
  - 根因: Google 服务账号 OAuth token 有效期约 1 小时，旧版只在脚本开头 refresh 一次，
    但脚本单次运行可达 90+ 分钟 → 60 分钟后 token 过期，后半程请求全部 401。
  - v3: 传入 creds 对象（非静态 token），inspect_url 遇 401 自动 creds.refresh() 续期并重试；
    另加 get_token() 在每次调用前校验有效性，确保长运行全程 token 有效。
  - 续跑仍基于「成功结果集合」（v2 已修的游标跳过 bug 保留）。

输出:
  _gsc_inspect_progress.json  断点进度（results=已成功集合，calls_total=累计调用）
  _gsc_unindexed.csv          未收录 URL 清单（verdict != PASS，含状态原因）
"""

import argparse
import csv
import json
import os
import sys
import time
import xml.etree.ElementTree as ET

from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

# ==================== 配置区 ====================
SITE_HINT = 'chenguangwu.github.io'
SITEMAP_FILE = 'sitemap.xml'
DEFAULT_CREDENTIAL = os.path.expanduser('~/.workbuddy/gsc_service_account.json')
SCOPE = 'https://www.googleapis.com/auth/webmasters'
INSPECT_ENDPOINT = 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect'
API_BASE = 'https://www.googleapis.com/webmasters/v3'
PROGRESS_FILE = '_gsc_inspect_progress.json'
OUTPUT_CSV = '_gsc_unindexed.csv'
DELAY = 0.3                # 每条间隔（300ms，远低于 600/min 限制）
TIMEOUT = 90               # 单请求超时（国内访问 Google 易慢，提至 90s）
MAX_RETRIES = 2            # 可重试错误/网络异常的额外重试次数（共 1+MAX_RETRIES 次）
BACKOFF = 3                # 重试退避基数（秒），第 n 次退避 = BACKOFF*(n+1)
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
# ================================================


def load_credentials(path):
    """加载服务账号凭证，返回已初始刷新的 creds 对象"""
    if not os.path.exists(path):
        print(f'错误: 找不到凭证文件 {path}')
        print('请先完成配置（见脚本头部说明），凭证默认放 ~/.workbuddy/gsc_service_account.json')
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        path, scopes=[SCOPE])
    creds.refresh(Request())
    return creds


def get_token(creds):
    """返回有效 token，必要时刷新（Google SA token 有效期约 1 小时）"""
    if not creds.valid:
        creds.refresh(Request())
    return creds.token


def get_site_url(token):
    """自动检测 GSC 中的站点 property"""
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(f'{API_BASE}/sites', headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()

    sites = [s['siteUrl'] for s in resp.json().get('siteEntry', [])
             if SITE_HINT in s['siteUrl']]
    if not sites:
        print(f'错误: GSC 中未找到包含 "{SITE_HINT}" 的已验证站点')
        sys.exit(1)
    for s in sites:
        if s.startswith('http'):
            return s
    return sites[0]


def extract_urls(sitemap_path):
    """从 sitemap.xml 提取所有URL"""
    if not os.path.exists(sitemap_path):
        print(f'错误: 找不到文件 {sitemap_path}')
        sys.exit(1)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = []
    for url_elem in root.findall(f'{NS}url'):
        loc = url_elem.find(f'{NS}loc')
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
    return urls


def load_progress():
    """加载断点进度（兼容旧版字段）"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            d = json.load(f)
        d.setdefault('checked', 0)
        d.setdefault('results', {})
        d.setdefault('calls_total', 0)
        return d
    return {'checked': 0, 'results': {}, 'calls_total': 0}


def save_progress(progress):
    """保存断点进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def inspect_url(creds, site_url, url):
    """查询单个 URL 的收录状态（token 运行期续期 + 超时重试 + 网络异常兜底）

    返回 (result_or_None, status_or_err)
      - 成功: (dict, 200)
      - 失败: (None, HTTP状态码 或 'NETERR:xxx')
    """
    body = {'inspectionUrl': url, 'siteUrl': site_url}
    last_status = 'ERR'
    for attempt in range(MAX_RETRIES + 1):
        try:
            token = get_token(creds)
            headers = {'Authorization': f'Bearer {token}'}
            resp = requests.post(INSPECT_ENDPOINT, json=body,
                                 headers=headers, timeout=TIMEOUT)
        except requests.exceptions.RequestException as e:
            last_status = f'NETERR:{type(e).__name__}'
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF * (attempt + 1))
                continue
            return None, last_status

        if resp.status_code == 200:
            data = resp.json()
            result = data.get('inspectionResult', {})
            idx = result.get('indexStatusResult', {})
            return {
                'url': url,
                'verdict': idx.get('verdict', 'UNKNOWN'),   # PASS / NEUTRAL / FAIL
                'coverage': idx.get('coverageState', ''),    # 收录状态
                'last_crawl': idx.get('lastCrawlTime', ''),
                'robots': idx.get('robotsTxtState', ''),
                'page_fetch': idx.get('pageFetchState', ''),
            }, 200

        # 401: token 过期/失效，刷新后重试（脚本长运行必触发，否则后半程全 401）
        if resp.status_code == 401:
            last_status = 401
            try:
                creds.refresh(Request())
            except Exception:
                pass
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF * (attempt + 1))
                continue
            return None, 401

        # 可重试的服务器/限流错误
        if resp.status_code in RETRYABLE_HTTP:
            last_status = resp.status_code
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF * (attempt + 1))
                continue
            return None, resp.status_code

        # 硬错误（4xx 非重试类）直接返回，不重试
        return None, resp.status_code

    return None, last_status


def main():
    parser = argparse.ArgumentParser(description='GSC URL Inspection 收录监控 v3')
    parser.add_argument('--limit', type=int, default=1900,
                        help='本轮最多 API 调用 N 次（含重试，默认 1900，留配额余量；0=不限）')
    parser.add_argument('--credential', default=DEFAULT_CREDENTIAL,
                        help=f'服务账号凭证 JSON 路径（默认 {DEFAULT_CREDENTIAL}）')
    parser.add_argument('--dry-run', action='store_true', help='只打印计划不查询')
    args = parser.parse_args()

    print('正在加载凭证 ...')
    creds = load_credentials(args.credential)

    print('正在检测 GSC 站点 ...')
    site_url = get_site_url(get_token(creds))
    print(f'目标站点: {site_url}')

    print('正在读取 sitemap ...')
    urls = extract_urls(SITEMAP_FILE)
    total = len(urls)

    progress = load_progress()
    results = progress['results']
    done = len(results)
    pending = [u for u in urls if u not in results]

    print(f'总URL数: {total} | 已成功记录: {done} | 待查: {len(pending)}')
    if args.dry_run:
        return

    budget = args.limit if args.limit > 0 else len(pending)
    budget = min(budget, len(pending))
    print(f'本轮调用上限: {budget}（覆盖待查URL，失败的明天自动重试）')
    print()

    if budget <= 0:
        print('✅ 无待查 URL，全部已成功覆盖')
        return

    ok = 0
    fail = 0
    calls = 0
    start_time = time.time()

    for url in pending:
        if calls >= budget:
            break
        result, status = inspect_url(creds, site_url, url)
        calls += 1
        progress['calls_total'] = progress.get('calls_total', 0) + 1
        if result:
            results[url] = result
            ok += 1
        else:
            fail += 1
            print(f'  ⚠️ 失败 ({status}): {url}')

        if calls % 100 == 0 or calls == budget:
            save_progress(progress)
            elapsed = time.time() - start_time
            print(
                f'进度: 调用 {calls}/{budget} | 成功: {ok} | 失败: {fail} | '
                f'待查剩余: {total - len(results)} | 耗时: {elapsed:.0f}s',
                flush=True,
            )
        time.sleep(DELAY)

    progress['checked'] = len(results)
    save_progress(progress)
    elapsed = time.time() - start_time
    print()
    print(f'本轮完成！调用 {calls} 次 | 新增成功: {ok} | 失败: {fail} | 耗时: {elapsed:.0f}s')

    # 汇总未收录清单（全部 results 中 verdict != PASS 的）
    if results:
        unindexed = [r for r in results.values() if r['verdict'] != 'PASS']
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', '判定', '收录状态', '上次抓取', 'robots', '页面抓取'])
            for r in unindexed:
                writer.writerow([r['url'], r['verdict'], r['coverage'],
                                 r['last_crawl'], r['robots'], r['page_fetch']])
        print(f'未收录清单: {OUTPUT_CSV}（共 {len(unindexed)} 条 / 累计成功 {len(results)} 条）')

    remaining = total - len(results)
    if remaining > 0:
        print(f'还有 {remaining} 个 URL 未成功查询，明天继续跑本脚本即可（自动重试失败的）')
    else:
        print('✅ 全量检查完成！')


if __name__ == '__main__':
    main()
