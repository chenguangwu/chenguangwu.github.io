#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bing Webmaster 收录状态批量核查脚本（零外部依赖，仅标准库）
================================================================================
背景：
  后台「索引浏览器(Index Explorer)」只能逐一下载最末级目录数据，一个个点太慢。
  本脚本改用 Bing Webmaster API 批量拉取，直接产出「哪些页面被收录」的报告。

API 文档：
  GetUrlInfo         GET  https://ssl.bing.com/webmaster/api.svc/json/GetUrlInfo?apikey=KEY&siteUrl=..&url=..
  GetChildrenUrlInfo POST https://ssl.bing.com/webmaster/api.svc/json/GetChildrenUrlInfo?apikey=KEY
                         body: {"siteUrl","url","page":0,"filterProperties":{...}}

核心事实（务必理解，已实测验证 2026-08-27）：
  Bing 没有「已收录=true/false」的布尔字段！它返回的是抓取详情：
    - LastCrawledDate : 最后抓取时间（**判断收录最可靠的信号；非空=已被抓取**）
    - HttpStatus      : HTTP 状态码（实测已抓取页也返回 0，并非 200！不能据此判成功）
    - DiscoveryDate   : 发现时间
    - IsPage          : 是否页面（false=目录）
  推断规则：LastCrawledDate 非空 -> indexed(已抓取/收录)；为空 -> not_crawled(未抓取)；
            HttpStatus>=400 -> error。原始字段全量写入 JSON，供校准。
  注意：GetChildrenUrlInfo(按目录批量) 实测对本站一律返回空 {"d":[]}，不可用；
        实际可用的是 GetUrlInfo(单页)。故默认 --mode geturl。

用法：
  # 0) 先看规模（不需要 API key）
  python3 _check_bing_index.py --dry-run

  # 1) 单页精确核查（实际可用模式，调用次数=URL数；支持 --resume 续跑）
  BING_API_KEY=YOUR_KEY python3 _check_bing_index.py

  # 2) 分批跑（避免一次性太久/撞限额），跑完一批续跑下一批
  BING_API_KEY=YOUR_KEY python3 _check_bing_index.py --limit 500 --resume

  # 中断后续跑
  BING_API_KEY=YOUR_KEY python3 _check_bing_index.py --resume

输出：
  _bing_index_check.csv   每行一个 URL + 推断结果（可直接用 Excel 打开筛选）
  _bing_index_check.json  原始 UrlInfo 全量（供人工校准阈值）
  _bing_index_check_state.json  续跑状态（已完成的目录/URL，中断不丢进度）

注意：
  - apikey 与 _submit_bing_url_api.py 用的是同一个 Bing Webmaster API key
    （Bing Webmaster Tools → Settings → API Access 生成）
  - 若 GetUrlInfo 报 InvalidUrl 类错误，多半是 url 参数需 JSON 引号包裹，
    可把 _get_url_info 里 params 的 'url' 值改为 json.dumps(page_url) 再试。
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# ==================== 配置区 ====================
SITE_URL = 'https://chenguangwu.github.io/'
SITEMAP_FILE = 'sitemap.xml'
API_BASE = 'https://ssl.bing.com/webmaster/api.svc/json'
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
TIMEOUT = 20
MAX_RETRIES = 3
DELAY_DEFAULT = 1.0
OUT_CSV = '_bing_index_check.csv'
OUT_JSON = '_bing_index_check.json'
STATE_JSON = '_bing_index_check_state.json'
# ================================================

DATE_RE = re.compile(r'/Date\((-?\d+)([+-]\d{4})?\)/')


def parse_ms_date(s):
    """把 Bing 的 /Date(1315349995266-0700)/ 格式转成可读时间；普通日期原样返回。
    .NET DateTime.MinValue(约 -62135596800000，即 0001-01-01) 表示「从未抓取/无日期」，返回 None。"""
    if not s or not isinstance(s, str):
        return None
    m = DATE_RE.search(s)
    if not m:
        return s
    ms = int(m.group(1))
    # 极小值（含 MinValue 负值、或早于 2001 的噪声值）一律视为「无抓取时间」
    if ms < 1_000_000_000_000:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception:
        return None


def http_json(method, url, params=None, body=None):
    """发起 JSON 请求，统一把错误转成带响应体的 RuntimeError，便于诊断。"""
    if method == 'GET':
        full = url + ('?' + urllib.parse.urlencode(params) if params else '')
        data = None
        headers = {'Accept': 'application/json'}
    else:
        full = url
        data = json.dumps(body).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Accept': 'application/json'}

    req = urllib.request.Request(full, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else ''
        raise RuntimeError(f'HTTP {e.code}: {raw[:300]}') from e
    except Exception as e:
        raise RuntimeError(f'网络错误: {e}') from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f'非JSON响应: {raw[:300]}')


def call_with_retry(fn, retry=0):
    """限流/配额错误长退避重试（30s 起，避免密集撞 Bing 滑动窗口惩罚），其他错误指数退避。"""
    try:
        return fn()
    except Exception as e:
        msg = str(e)
        is_throttle = ('429' in msg or '503' in msg or 'Throttle' in msg or 'quota' in msg.lower())
        if is_throttle and retry < MAX_RETRIES:
            wait = 30 * (retry + 1)
            print(f'  ⏳ 限流/配额，等待 {wait}s 后重试({retry+1}/{MAX_RETRIES})...', flush=True)
            time.sleep(wait)
            return call_with_retry(fn, retry + 1)
        if not is_throttle and retry < MAX_RETRIES:
            time.sleep(2 ** retry)
            print(f'  ↻ 网络/其他错误，{2 ** retry}s 后重试({retry+1}/{MAX_RETRIES})', flush=True)
            return call_with_retry(fn, retry + 1)
        raise


def get_url_info(apikey, page_url):
    """单页索引详情（GET）。返回 UrlInfo dict 或 None。"""
    url = f'{API_BASE}/GetUrlInfo'
    params = {'apikey': apikey, 'siteUrl': SITE_URL, 'url': page_url}
    data = call_with_retry(lambda: http_json('GET', url, params=params))
    return data.get('d')


def get_children_info(apikey, dir_url, page):
    """目录索引详情（POST）。返回 UrlInfo 列表。"""
    url = f'{API_BASE}/GetChildrenUrlInfo?apikey={urllib.parse.quote(apikey)}'
    body = {
        'siteUrl': SITE_URL,
        'url': dir_url,
        'page': page,
        'filterProperties': {
            '__type': 'FilterProperties:#Microsoft.Bing.Webmaster.Api',
            'CrawlDateFilter': 0,        # 0=Any（拉全部，不限最近一周）
            'DiscoveredDateFilter': 0,
            'DocFlagsFilters': 0,
            'HttpCodeFilters': 0,
        },
    }
    data = call_with_retry(lambda: http_json('POST', url, body=body))
    return data.get('d', []) or []


def extract_urls(sitemap_path):
    if not os.path.exists(sitemap_path):
        print(f'错误: 找不到 {sitemap_path}')
        sys.exit(1)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = []
    for url_elem in root.findall(f'{NS}url'):
        loc = url_elem.find(f'{NS}loc')
        if loc is not None and loc.text:
            u = loc.text.strip()
            if u.startswith(SITE_URL):
                urls.append(u)
    return urls


def dir_of(url):
    """取 URL 的父目录（去掉末尾文件名，不带末尾斜杠）。"""
    if url.endswith('/'):
        return url.rstrip('/')
    idx = url.rfind('/')
    return url[:idx]


def classify(info):
    """根据 UrlInfo 启发式推断收录状态。返回 (guess, last, status, is_page, discovery)。
    实测结论：已抓取页的 HttpStatus 也是 0（非 200），故以 LastCrawledDate 为准。"""
    if not info:
        return 'no_data', None, None, None, None
    last = parse_ms_date(info.get('LastCrawledDate'))
    status = info.get('HttpStatus')
    is_page = info.get('IsPage')
    discovered = parse_ms_date(info.get('DiscoveryDate'))

    if last:
        guess = 'indexed'          # 有最后抓取时间 -> 已被抓取/收录
    elif isinstance(status, int) and status >= 400:
        guess = 'error'            # 4xx/5xx -> 抓取异常
    else:
        guess = 'not_crawled'      # 无抓取时间 -> 未抓取/未收录

    return guess, last, status, is_page, discovered


def write_outputs(results):
    """写出 CSV（可读报告）+ JSON（原始全量）。"""
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['url', 'last_crawled', 'http_status', 'is_page',
                    'discovery_date', 'indexed_guess'])
        for u in sorted(results.keys()):
            info = results[u]
            guess, last, status, is_page, disc = classify(info)
            w.writerow([
                u,
                last or '',
                '' if status is None else status,
                '' if is_page is None else is_page,
                disc or '',
                guess,
            ])

    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 汇总
    counts = {}
    for info in results.values():
        guess, *_ = classify(info)
        counts[guess] = counts.get(guess, 0) + 1
    print()
    print('=== 核查完成 ===')
    print(f'总条数: {len(results)}')
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')
    print(f'CSV 报告: {OUT_CSV}')
    print(f'JSON 原始: {OUT_JSON}')


def save_state(done_dirs, results):
    with open(STATE_JSON, 'w', encoding='utf-8') as f:
        json.dump({'done_dirs': list(done_dirs), 'results': results},
                  f, ensure_ascii=False)


def run_children(apikey, limit, delay, resume):
    """模式 children：按目录批量拉取。注意：实测对本站 GetChildrenUrlInfo 一律返回空，
    此模式实际不可用，保留仅为兼容；请用 --mode geturl。"""
    urls = extract_urls(SITEMAP_FILE)
    dirs = sorted(set(dir_of(u) for u in urls))
    if limit:
        dirs = dirs[:limit]

    state = {}
    if resume and os.path.exists(STATE_JSON):
        with open(STATE_JSON, encoding='utf-8') as f:
            state = json.load(f)
    done_dirs = set(state.get('done_dirs', []))
    results = state.get('results', {})

    total = len(dirs)
    remaining = [d for d in dirs if d not in done_dirs]
    print(f'目录总数: {total} | 待查: {len(remaining)} | 已完成: {len(done_dirs)}')
    print('（每目录分页拉全，调用次数≈目录数，远低于日配额）\n')

    for i, d in enumerate(remaining, start=1):
        page = 0
        while True:
            infos = get_children_info(apikey, d, page)
            if not infos:
                break
            for info in infos:
                u = info.get('Url')
                if u:
                    results[u] = info
            page += 1
            if page % 1 == 0:
                time.sleep(delay)
        done_dirs.add(d)
        save_state(done_dirs, results)
        if i % 10 == 0 or i == len(remaining):
            print(f'进度: {i}/{len(remaining)} 目录 | 已收集 {len(results)} 条', flush=True)
        time.sleep(delay)

    write_outputs(results)


def run_geturl(apikey, limit, delay, resume):
    """模式 geturl：单页精确核查（调用次数=URL数）。带自适应速率：遇限流自动翻倍降速，连续成功缓慢恢复。"""
    urls = extract_urls(SITEMAP_FILE)
    if limit:
        urls = urls[:limit]

    results = {}
    if resume and os.path.exists(STATE_JSON):
        with open(STATE_JSON, encoding='utf-8') as f:
            results = json.load(f).get('results', {})
    todo = [u for u in urls if u not in results]
    total = len(todo)
    print(f'待查 URL: {total} | 已完成: {len(results)}\n')

    cur_delay = max(delay, 4.0)  # 保守起手 4s，避开 Bing 速率限流
    consec_throttle = 0
    for i, u in enumerate(todo, start=1):
        info = None
        try:
            info = get_url_info(apikey, u)
            consec_throttle = 0
            if i % 80 == 0:
                cur_delay = max(3.0, cur_delay * 0.9)  # 连续顺利则缓慢回落
        except RuntimeError as e:
            msg = str(e)
            if '429' in msg or '503' in msg or 'Throttle' in msg or 'quota' in msg.lower():
                consec_throttle += 1
                cur_delay = min(cur_delay * 2, 30.0)
                # 连续多次限流 -> 主动长冷却，避免持续撞墙刷惩罚窗口
                cool = 60 if consec_throttle < 4 else 300
                print(f'  ⏳ 限流(连续{consec_throttle}次)，间隔 {cur_delay:.0f}s，冷却 {cool}s', flush=True)
                time.sleep(cool)
                try:
                    info = get_url_info(apikey, u)
                    consec_throttle = 0
                except RuntimeError:
                    info = None  # 实在限流：本次不记录，留待 --resume 重查
            else:
                raise

        if info is None:
            print(f'  ⚠️ {u} 本次限流未取到，跳过待续跑', flush=True)
        else:
            results[u] = info

        if i % 10 == 0 or i == total:
            c = {}
            for inf in results.values():
                g, *_ = classify(inf)
                c[g] = c.get(g, 0) + 1
            print(f'进度: {i}/{total} | 已查有效 {len(results)} | '
                  f'收录 {c.get("indexed", 0)} / 未抓取 {c.get("not_crawled", 0)} / '
                  f'异常 {c.get("error", 0)} / 无数据 {c.get("no_data", 0)} | delay {cur_delay:.1f}s', flush=True)
        if i % 50 == 0 or i == total:
            save_state(set(), results)
        time.sleep(cur_delay)

    write_outputs(results)


def main():
    p = argparse.ArgumentParser(description='Bing Webmaster 收录状态批量核查')
    p.add_argument('--apikey', help='Bing Webmaster API key')
    p.add_argument('--mode', choices=['geturl', 'children'], default='geturl',
                   help='geturl=单页精确(实际可用,默认); children=按目录批量(Bing 对本站返回空,备用)')
    p.add_argument('--limit', type=int, default=0, help='最多处理前 N 个目录/URL（0=全部）')
    p.add_argument('--delay', type=float, default=DELAY_DEFAULT, help='每次调用间隔秒数')
    p.add_argument('--resume', action='store_true', help='从状态文件续跑')
    p.add_argument('--dry-run', action='store_true',
                   help='只统计 URL/目录规模，不调用 API（无需 apikey）')
    args = p.parse_args()

    if args.dry_run:
        urls = extract_urls(SITEMAP_FILE)
        dirs = sorted(set(dir_of(u) for u in urls))
        print(f'URL 总数: {len(urls)}')
        print(f'目录总数(=children 模式 API 调用次数上限): {len(dirs)}')
        print('前 5 个目录示例:')
        for d in dirs[:5]:
            print('  ', d)
        return

    if not args.apikey:
        args.apikey = os.environ.get('BING_API_KEY')
    if not args.apikey:
        print('错误: 必须提供 --apikey 或设置环境变量 BING_API_KEY')
        sys.exit(1)

    if args.mode == 'children':
        run_children(args.apikey, args.limit, args.delay, args.resume)
    else:
        run_geturl(args.apikey, args.limit, args.delay, args.resume)


if __name__ == '__main__':
    main()
