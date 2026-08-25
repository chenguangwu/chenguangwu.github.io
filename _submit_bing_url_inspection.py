#!/usr/bin/env python3
"""
Bing Webmaster URL Inspection 页面自动化提交脚本
用法:
  1. 先安装依赖: /Users/cgw/.workbuddy/binaries/python/versions/3.13.12/bin/python3 -m venv /Users/cgw/.workbuddy/binaries/python/envs/default
     /Users/cgw/.workbuddy/binaries/python/envs/default/bin/pip install playwright
     /Users/cgw/.workbuddy/binaries/python/envs/default/bin/playwright install msedge
  2. 在 Edge 浏览器中登录 Bing Webmaster Tools (https://www.bing.com/webmasters)
  3. 运行: python3 _submit_bing_url_inspection.py --start 0 --limit 100

注意:
  - 本脚本控制真实 Edge 浏览器窗口操作
  - 每天限额约 10,000 URL
  - 6295 个 URL 全部提交预计需要数小时
  - 仅建议用于小批量或特殊需求
"""

import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ==================== 配置区 ====================
SITEMAP_FILE = 'sitemap.xml'
SITE_URL = 'https://chenguangwu.github.io/'
INSPECTION_URL = f'https://www.bing.com/webmasters/urlinspection?siteUrl={SITE_URL}'
DEFAULT_WAIT_MS = 5000
LONG_WAIT_MS = 8000
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
# ================================================


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
            if url.startswith(SITE_URL):
                urls.append(url)

    return urls


def inspect_and_submit(page, url, index, total):
    """在 URL Inspection 页面检查并请求索引一个 URL"""
    print(f'[{index}/{total}] {url}', end=' ', flush=True)

    try:
        # 1. 找到 URL 输入框并输入
        # Bing 页面输入框 placeholder 通常包含 "输入 URL" 或 "Enter URL"
        input_selector = 'input[type="url"], input[placeholder*="URL" i], input[placeholder*="url" i]'
        page.wait_for_selector(input_selector, timeout=DEFAULT_WAIT_MS)

        # 清空并输入
        page.fill(input_selector, '')
        page.fill(input_selector, url)

        # 2. 点击检查按钮
        # 按钮文字可能是"检查"或"Inspect"
        inspect_btn = 'button:has-text("检查"), button:has-text("Inspect")'
        page.click(inspect_btn)

        # 3. 等待结果加载
        page.wait_for_timeout(2000)

        # 4. 查找"请求编制索引"按钮
        # 可能的文字: "请求编制索引", "Request indexing", "请求索引"
        request_btn_selectors = [
            'button:has-text("请求编制索引")',
            'button:has-text("Request indexing")',
            'button:has-text("请求索引")',
        ]

        request_btn = None
        for selector in request_btn_selectors:
            try:
                request_btn = page.wait_for_selector(selector, timeout=3000)
                if request_btn and request_btn.is_visible():
                    break
            except PlaywrightTimeout:
                continue

        if not request_btn:
            print('→ 无需提交或页面状态不可提交')
            return True

        # 5. 点击请求编制索引
        request_btn.click()
        page.wait_for_timeout(1000)

        # 6. 在弹窗中点击"提交"
        submit_selectors = [
            'button:has-text("提交")',
            'button:has-text("Submit")',
        ]
        submitted = False
        for selector in submit_selectors:
            try:
                submit_btn = page.wait_for_selector(selector, timeout=3000)
                if submit_btn and submit_btn.is_visible():
                    submit_btn.click()
                    submitted = True
                    break
            except PlaywrightTimeout:
                continue

        # 7. 等待弹窗关闭
        page.wait_for_timeout(1500)

        # 8. 按 Escape 关闭可能的弹窗
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)

        if submitted:
            print('→ 已提交')
        else:
            print('→ 未找到提交按钮')

        return submitted

    except Exception as e:
        print(f'→ 失败: {e}')
        return False


def main():
    parser = argparse.ArgumentParser(description='Bing URL Inspection 浏览器自动化提交')
    parser.add_argument('--start', type=int, default=0, help='从第 N 个 URL 开始')
    parser.add_argument('--limit', type=int, default=10, help='最多提交 N 个 URL')
    parser.add_argument('--headless', action='store_true', help='无头模式（不显示窗口）')
    parser.add_argument('--delay', type=float, default=3.0, help='每个 URL 间隔秒数')
    args = parser.parse_args()

    urls = extract_urls(SITEMAP_FILE)
    urls = urls[args.start:args.start + args.limit]
    total = len(urls)

    print(f'准备提交 {total} 个 URL')
    print(f'起始位置: {args.start}')
    print('请确保 Edge 已登录 Bing Webmaster Tools')
    print()

    failed = []

    with sync_playwright() as p:
        # 使用本机 Edge
        browser = p.chromium.launch(
            channel='msedge',
            headless=args.headless,
        )
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()

        page.goto(INSPECTION_URL)
        print('已打开 Bing URL Inspection 页面')
        print('请在 20 秒内完成任何人工验证...')
        time.sleep(20)

        for i, url in enumerate(urls, start=1):
            ok = inspect_and_submit(page, url, i, total)
            if not ok:
                failed.append(url)

            if i < total:
                time.sleep(args.delay)

        browser.close()

    print()
    print(f'完成。成功: {total - len(failed)}，失败: {len(failed)}')
    if failed:
        failed_file = '_bing_url_inspection_failed.json'
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)
        print(f'失败 URL 已保存到: {failed_file}')


if __name__ == '__main__':
    main()
