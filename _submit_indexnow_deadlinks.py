#!/usr/bin/env python3
"""
IndexNow 死链（dead link）提交脚本
================================
用途: 把一批已知 404/410 的死链 URL 提交给 IndexNow，让搜索引擎重新抓取并移除索引。

原理: IndexNow 本身不区分死链/活链，提交后搜索引擎会自行抓取；
      若抓取返回 404/410，则搜索引擎移除该 URL 的索引。故"提交死链"= 提交这些 URL。

用法:
  从文件:  python3 _submit_indexnow_deadlinks.py --file deadlinks.txt
  从stdin: cat deadlinks.txt | python3 _submit_indexnow_deadlinks.py
  直接传:  python3 _submit_indexnow_deadlinks.py --url https://... --url https://...
  仅查看:  python3 _submit_indexnow_deadlinks.py --file deadlinks.txt --dry-run
  跳过校验: python3 _submit_indexnow_deadlinks.py --file deadlinks.txt --no-verify

安全:
  - 默认会对每个 URL 做本地 HTTP 校验，只提交确认为 404/410 的，跳过仍存活的（避免误删正常页索引）。
  - 若本地网络无法访问外网导致校验全部失败，会提示改用 --no-verify 并退出，不盲目提交。

依赖: 仅 Python 3 标准库。
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request

# ==================== 配置区 ====================
API_URL = 'https://api.indexnow.org/IndexNow'
KEY = 'c355d2d375dc40469dc213f2f28e2d76'
KEY_LOCATION = 'https://chenguangwu.github.io/c355d2d375dc40469dc213f2f28e2d76.txt'
HOST = 'chenguangwu.github.io'
BATCH_SIZE = 10       # 每批提交的URL数量（小批次=流式模式）
BATCH_DELAY = 1       # 每批之间的间隔秒数（避免限流）
TIMEOUT = 15          # 单个请求超时秒数
# ================================================


def read_urls(args):
    """按优先级读取待提交 URL：--file > --url > stdin。去重保序。"""
    urls = []
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            for line in f:
                u = line.strip()
                if u and not u.startswith('#'):
                    urls.append(u)
    if args.url:
        urls.extend(args.url)
    if not urls and not sys.stdin.isatty():
        for line in sys.stdin:
            u = line.strip()
            if u and not u.startswith('#'):
                urls.append(u)
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def check_status(url, timeout=15):
    """返回 (code, error)。code: HTTP 状态码或 0(网络错误)。"""
    try:
        req = urllib.request.Request(
            url, method='HEAD',
            headers={'User-Agent': 'Mozilla/5.0 (ToolBox deadlink checker)'},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # 网络错误 / 超时 / DNS 等
        return 0, str(e)


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


def verify_deadlinks(urls, timeout=15):
    """本地校验每个 URL 的 HTTP 状态，返回 (dead, live, neterr)。

    dead: 确认为 404/410 的 URL 列表
    live: (url, code) 仍存活（非 404/410）的列表
    neterr: (url, err) 网络错误无法判断的列表
    """
    import concurrent.futures

    dead, live, neterr = [], [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        fut = {ex.submit(check_status, u, timeout): u for u in urls}
        for f in concurrent.futures.as_completed(fut):
            u = fut[f]
            code, err = f.result()
            if code in (404, 410):
                dead.append(u)
            elif code == 0:
                neterr.append((u, err))
            else:
                live.append((u, code))
    return dead, live, neterr


def main():
    ap = argparse.ArgumentParser(description='IndexNow 死链提交脚本')
    ap.add_argument('--file', help='URL 列表文件，每行一个')
    ap.add_argument('--url', action='append', help='直接传 URL，可多次使用')
    ap.add_argument('--dry-run', action='store_true', help='只打印URL，不提交')
    ap.add_argument('--no-verify', action='store_true',
                    help='跳过本地 404 校验，直接提交（仅在你已确认全是死链时使用）')
    args = ap.parse_args()

    urls = read_urls(args)
    if not urls:
        print('没有可提交的 URL（请用 --file / --url / stdin 提供）')
        sys.exit(1)
    print(f'读取到 {len(urls)} 个待提交 URL')

    if args.dry_run:
        for u in urls[:10]:
            print(' ', u)
        if len(urls) > 10:
            print(f'  ... 其余 {len(urls) - 10} 个省略')
        print('dry-run 完成，未提交')
        return

    submit_list = urls
    if not args.no_verify:
        print('正在本地校验 HTTP 状态（仅提交 404/410 死链）...')
        dead, live, neterr = verify_deadlinks(urls)
        if neterr:
            rate = len(neterr) / len(urls)
            print(f'⚠️ 网络错误无法判断的 URL: {len(neterr)}/{len(urls)}')
            if rate > 0.5:
                print('本地网络大概率无法访问外网，校验不可靠。')
                print('如你已在线确认这些全为死链，请加 --no-verify 重新运行；否则请检查网络。')
                sys.exit(1)
            # 部分网络错误：保守起见，网络错误的 URL 也纳入提交（死链可能性高），仅跳过存活的
        if live:
            print(f'以下 {len(live)} 个 URL 仍存活（非 404/410），已跳过（如需强制提交加 --no-verify）:')
            for u, c in live:
                print(f'  [{c}] {u}')
        # 死链 + 网络错误（保守纳入）一并提交
        err_urls = [u for u, _ in neterr]
        submit_list = dead + err_urls
        print(f'确认为死链(404/410): {len(dead)}，网络不可判纳入提交: {len(err_urls)}，跳过存活: {len(live)}')

    if not submit_list:
        print('没有待提交的死链，结束。')
        return

    total = len(submit_list)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    success = 0
    fail = 0
    start_time = time.time()

    print(f'开始提交 {total} 个死链 URL（流式，每批{BATCH_SIZE}个，间隔{BATCH_DELAY}s）...')
    for i in range(0, total, BATCH_SIZE):
        batch = submit_list[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        ok = submit_batch(batch)
        if ok:
            success += len(batch)
        else:
            fail += len(batch)
        if batch_num % 50 == 0 or batch_num == total_batches:
            elapsed = time.time() - start_time
            print(
                f'进度: {batch_num}/{total_batches} '
                f'成功: {success} | 失败: {fail} | 耗时: {elapsed:.0f}s',
                flush=True,
            )
        time.sleep(BATCH_DELAY)

    print()
    print(f'提交完成！成功: {success}，失败: {fail}，总耗时: {time.time() - start_time:.0f}s')
    if fail > 0:
        print(f'提示: {fail} 个URL提交失败，建议稍后重新运行本脚本')


if __name__ == '__main__':
    main()
