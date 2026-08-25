#!/usr/bin/env python3
"""
GSC Sitemaps API 定时提交脚本
功能: 把根 sitemap.xml 重新提交给 Google Search Console，通知 Google 抓取最新 sitemap

用法:
  手动:  python3 _gsc_submit_sitemap.py [--credential PATH]
  cron:  python3 _gsc_submit_sitemap.py >> _gsc_submit.log 2>&1

依赖: google-auth + requests（已安装到 managed venv）
  /Users/cgw/.workbuddy/binaries/python/envs/default/bin/pip install google-auth requests

前置条件（一次性配置）:
  1. Google Cloud Console 创建项目，启用 "Google Search Console API"
  2. 创建服务账号并下载 JSON 凭证
  3. 在 GSC → 设置 → 用户和权限，把服务账号邮箱添加为「所有者」
  4. 把凭证 JSON 放到默认路径（或 --credential 指定）

API 文档:
  https://developers.google.com/webmaster-tools/v3/sitemaps/submit
  提交端点: PUT https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
  配额: 25,000 请求/天（远够用）
"""

import argparse
import json
import os
import sys
import urllib.parse

from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

# ==================== 配置区 ====================
SITE_HINT = 'chenguangwu.github.io'
SITEMAP_REL_PATH = 'sitemap.xml'          # 项目根目录下的 sitemap 文件名
DEFAULT_CREDENTIAL = os.path.expanduser('~/.workbuddy/gsc_service_account.json')
SCOPE = 'https://www.googleapis.com/auth/webmasters'
API_BASE = 'https://www.googleapis.com/webmasters/v3'
TIMEOUT = 30
# ================================================


def load_credentials(path):
    """加载服务账号凭证"""
    if not os.path.exists(path):
        print(f'错误: 找不到凭证文件 {path}')
        print('请先完成配置（见脚本头部说明），凭证默认放 ~/.workbuddy/gsc_service_account.json')
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        path, scopes=[SCOPE])
    creds.refresh(Request())
    return creds.token


def get_site_url(token):
    """自动检测 GSC 中的站点 property（优先 URL prefix，兼容 domain）"""
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(f'{API_BASE}/sites', headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()

    sites = [s['siteUrl'] for s in resp.json().get('siteEntry', [])
             if SITE_HINT in s['siteUrl']]
    if not sites:
        print(f'错误: GSC 中未找到包含 "{SITE_HINT}" 的已验证站点')
        sys.exit(1)

    # 优先 URL prefix 形式（https://.../），其次 domain 形式
    for s in sites:
        if s.startswith('http'):
            return s
    return sites[0]


def submit_sitemap(token, site_url, sitemap_url):
    """提交 sitemap 到 GSC"""
    feedpath = urllib.parse.quote(sitemap_url, safe='')
    url = f'{API_BASE}/sites/{urllib.parse.quote(site_url, safe="")}/sitemaps/{feedpath}'
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.put(url, headers=headers, timeout=TIMEOUT)
    return resp


def main():
    parser = argparse.ArgumentParser(description='GSC Sitemaps API 定时提交')
    parser.add_argument('--credential', default=DEFAULT_CREDENTIAL,
                        help=f'服务账号凭证 JSON 路径（默认 {DEFAULT_CREDENTIAL}）')
    args = parser.parse_args()

    print('正在加载凭证 ...')
    token = load_credentials(args.credential)

    print('正在检测 GSC 站点 ...')
    site_url = get_site_url(token)
    print(f'目标站点: {site_url}')

    # 读取 sitemap 文件名（与项目根目录一致）
    if not os.path.exists(SITEMAP_REL_PATH):
        print(f'错误: 找不到 {SITEMAP_REL_PATH}，请在项目根目录运行')
        sys.exit(1)
    sitemap_url = f'{site_url.rstrip("/")}/{SITEMAP_REL_PATH}'
    print(f'提交 sitemap: {sitemap_url}')

    resp = submit_sitemap(token, site_url, sitemap_url)
    # Google Sitemaps API 成功时返回 204 No Content（提交已受理）
    if resp.status_code in (200, 204):
        print(f'✅ 提交成功 (HTTP {resp.status_code})：{sitemap_url}')
        print('GSC 已收到通知，将异步抓取最新 sitemap')
    else:
        print(f'❌ 提交失败 (HTTP {resp.status_code})')
        print(resp.text[:500])
        sys.exit(1)


if __name__ == '__main__':
    main()
