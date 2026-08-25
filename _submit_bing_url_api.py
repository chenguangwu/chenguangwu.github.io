#!/usr/bin/env python3
"""
Bing Webmaster URL Submission API 流式批量提交脚本
用法:
  手动:  python3 _submit_bing_url_api.py --apikey YOUR_BING_API_KEY [--limit N]
  cron:  python3 _submit_bing_url_api.py --apikey YOUR_BING_API_KEY --yes >> _bing_submit.log 2>&1

功能:
  1. 从 sitemap.xml 提取所有URL
  2. 使用 Bing Webmaster URL Submission API **批量接口 SubmitUrlbatch** 分批流式提交
     （每批 10 条、间隔 3 秒，与 _submit_indexnow.py 的流式分批风格一致，避免限流）
  3. 实时显示进度，支持失败重试

Bing API 文档:
  https://www.bing.com/webmasters/help/URL-Submission-62f2860b
  批量端点: POST https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=xxx
  单批上限: 500 URL（本脚本用 10，对齐 IndexNow 的流式分批节奏）
  限额: 每域名每天 10,000 URL

注意:
  - 本脚本使用的 API key 是 Bing Webmaster Tools 的 API key（Settings → API Access 生成），
    与 IndexNow key 是两个不同的 key。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# ==================== 配置区 ====================
HOST = 'chenguangwu.github.io'
SITE_URL = 'https://chenguangwu.github.io/'
SITEMAP_FILE = 'sitemap.xml'
API_ENDPOINT = 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch'
BATCH_SIZE = 10         # 每批提交的URL数量（对齐 IndexNow 的流式分批节奏）
BATCH_DELAY = 3.0       # 每批之间的间隔秒数（流式，避免 ThrottleHost 限流）
TIMEOUT = 15            # 单个请求超时秒数
MAX_RETRIES = 5         # 失败重试次数（含 ThrottleHost 限流长退避）
# ================================================

NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'


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
            url = loc.text.strip()
            if url.startswith('https://chenguangwu.github.io/'):
                urls.append(url)

    return urls


def submit_batch(apikey, batch, retry=0):
    """批量提交一批URL到 Bing URL Submission API"""
    payload = {
        'siteUrl': SITE_URL,
        'urlList': batch,
    }
    data = json.dumps(payload).encode('utf-8')

    req_url = f'{API_ENDPOINT}?apikey={apikey}'
    req = urllib.request.Request(
        req_url,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
            return True, resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else ''
        # ThrottleHost = 主机级限流，需长退避等待后重试
        if 'ThrottleHost' in body and retry < MAX_RETRIES:
            wait = 30 * (retry + 1)
            print(f'  ⏳ 限流(ThrottleHost)，等待 {wait}s 后重试本批({len(batch)}条) ...')
            time.sleep(wait)
            return submit_batch(apikey, batch, retry + 1)
        if retry < MAX_RETRIES:
            time.sleep(2 ** retry)
            return submit_batch(apikey, batch, retry + 1)
        return False, e.code, body
    except Exception as e:
        if retry < MAX_RETRIES:
            time.sleep(2 ** retry)
            return submit_batch(apikey, batch, retry + 1)
        return False, 0, str(e)


def main():
    parser = argparse.ArgumentParser(description='Bing URL Submission API 流式批量提交')
    parser.add_argument('--apikey', required=True, help='Bing Webmaster API key')
    parser.add_argument('--limit', type=int, default=0, help='最多提交前 N 个URL（0=全部）')
    parser.add_argument('--dry-run', action='store_true', help='只打印URL数量，不实际提交')
    parser.add_argument('--yes', action='store_true',
                        help='跳过确认（cron 等非交互环境必加）')
    args = parser.parse_args()

    print('正在读取 sitemap.xml ...')
    urls = extract_urls(SITEMAP_FILE)

    if args.limit > 0:
        urls = urls[:args.limit]

    total = len(urls)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    print(f'总URL数: {total}')
    print(f'提交模式: 流式批量（每批{BATCH_SIZE}条，间隔{BATCH_DELAY}秒，SubmitUrlbatch）')
    print(f'总批次: {total_batches}')
    print(f'每日限额: 10,000 URL')
    print()

    if args.dry_run:
        print('干运行模式，不实际提交')
        print('前5个URL示例:')
        for u in urls[:5]:
            print(' ', u)
        return

    # 非交互确认（cron 用 --yes 跳过）
    if not args.yes:
        confirm = input(f'确认要向 Bing 提交 {total} 个URL吗？ [y/N] ')
        if confirm.lower() not in ('y', 'yes'):
            print('已取消')
            return

    success = 0
    fail = 0
    failed_urls = []
    start_time = time.time()

    for i in range(0, total, BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1

        ok, status, body = submit_batch(args.apikey, batch)
        if ok:
            success += len(batch)
        else:
            fail += len(batch)
            failed_urls.extend(batch)
            print(f'  ⚠️ 第 {batch_num} 批失败 (HTTP {status}): {body[:200]}')

        if batch_num % 30 == 0 or batch_num == total_batches:
            elapsed = time.time() - start_time
            print(
                f'进度: {batch_num}/{total_batches} '
                f'({i + len(batch)}/{total}) | 成功: {success} | 失败: {fail} | '
                f'耗时: {elapsed:.0f}s',
                flush=True,
            )

        time.sleep(BATCH_DELAY)

    elapsed = time.time() - start_time
    print()
    print(f'提交完成！成功: {success}，失败: {fail}，总耗时: {elapsed:.0f}s')

    if failed_urls:
        failed_file = '_bing_url_submission_failed.json'
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_urls, f, ensure_ascii=False, indent=2)
        print(f'失败 URL 已保存到: {failed_file}')
        sys.exit(1)


if __name__ == '__main__':
    main()
