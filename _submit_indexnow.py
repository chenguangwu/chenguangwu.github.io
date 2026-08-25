#!/usr/bin/env python3
"""
IndexNow URL 提交脚本
用法: python3 _submit_indexnow.py

功能:
  1. 从 sitemap.xml 提取所有URL
  2. 以流式模式（每批10个URL，间隔1秒）提交到 IndexNow API
  3. 实时显示进度

依赖: 仅需 Python 3 标准库，无需安装任何第三方包
"""

import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

# ==================== 配置区 ====================
API_URL = 'https://api.indexnow.org/IndexNow'
KEY = 'c355d2d375dc40469dc213f2f28e2d76'
KEY_LOCATION = 'https://chenguangwu.github.io/c355d2d375dc40469dc213f2f28e2d76.txt'
HOST = 'chenguangwu.github.io'
SITEMAP_FILE = 'sitemap.xml'
BATCH_SIZE = 10       # 每批提交的URL数量（小批次=流式模式）
BATCH_DELAY = 1       # 每批之间的间隔秒数（避免限流）
TIMEOUT = 15          # 单个请求超时秒数
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
            urls.append(loc.text.strip())

    return urls


def submit_batch(batch):
    """提交一批URL到 IndexNow API"""
    payload = {
        'host': HOST,
        'key': KEY,
        'keyLocation': KEY_LOCATION,
        'urlList': batch,
    }
    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status in (200, 202)
    except Exception:
        return False


def main():
    # 1. 提取URL
    print('正在读取 sitemap.xml ...')
    urls = extract_urls(SITEMAP_FILE)

    total = len(urls)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    print(f'总URL数: {total}')
    print(f'提交模式: 流式（每批{BATCH_SIZE}个URL，间隔{BATCH_DELAY}秒）')
    print(f'总批次: {total_batches}')
    print()

    # 2. 逐批提交
    success = 0
    fail = 0
    start_time = time.time()

    for i in range(0, total, BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1

        ok = submit_batch(batch)
        if ok:
            success += len(batch)
        else:
            fail += len(batch)

        # 每50批打印一次进度
        if batch_num % 50 == 0:
            elapsed = time.time() - start_time
            print(
                f'进度: {batch_num}/{total_batches} '
                f'({batch_num * BATCH_SIZE}/{total}) | '
                f'成功: {success} | 失败: {fail} | '
                f'耗时: {elapsed:.0f}s',
                flush=True,
            )

        time.sleep(BATCH_DELAY)

    # 3. 结果汇总
    elapsed = time.time() - start_time
    print()
    print(f'提交完成！成功: {success}，失败: {fail}，总耗时: {elapsed:.0f}s')

    # 4. 如果有失败的URL，保存到文件方便重试
    if fail > 0:
        print(f'提示: {fail} 个URL提交失败，建议稍后重新运行本脚本')


if __name__ == '__main__':
    main()
