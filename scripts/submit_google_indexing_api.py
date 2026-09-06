#!/usr/bin/env python3
"""Submit site URLs to Google's Web Search Indexing API in a safe daily queue.

This is a notification API, not a Search Console URL Inspection replacement.
Google's documented supported content types are JobPosting and BroadcastEvent
embedded in VideoObject. A successful HTTP 200 means Google accepted the
notification; it does not mean that the URL is indexed.

Queue order:
  1. tools/<industry>/index.html collection pages, ranked by local traffic
  2. json/hot-tools.json editorial hot tools
  3. every remaining URL from sitemap.xml

The state file is deliberately outside Git's tracked files by default:
  .codex/tasks/google-indexing-api-state.json

Dependencies (already used by the existing GSC scripts):
  google-auth, requests
  /Users/cgw/.workbuddy/binaries/python/envs/default/bin/python

Example cron command (run from any directory):
  30 16 * * * cd /Users/cgw/project/cgw/chenguangwu.github.io && \
    /Users/cgw/.workbuddy/binaries/python/envs/default/bin/python \
    scripts/submit_google_indexing_api.py \
    --credential /Users/cgw/Downloads/github-page-504803-8abe6b800932.json \
    --yes >> .codex/tasks/google-indexing-api.log 2>&1

The credential path is accepted as an argument so the private key is never
put in this repository, a command payload, or a log line.
"""

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

try:
    import requests
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account
except ImportError as exc:
    raise SystemExit(
        '缺少依赖，请使用项目已有 managed venv：'
        '/Users/cgw/.workbuddy/binaries/python/envs/default/bin/python'
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = 'https://chenguangwu.github.io/'
SITEMAP_FILE = ROOT / 'sitemap.xml'
HOT_TOOLS_FILE = ROOT / 'json' / 'hot-tools.json'
TRAFFIC_FILE = ROOT / 'analytics_traffic_merged.csv'
DEFAULT_STATE_FILE = ROOT / '.codex' / 'tasks' / 'google-indexing-api-state.json'
DEFAULT_CREDENTIAL = os.path.expanduser(
    '~/.workbuddy/gsc_indexing_service_account.json')

SCOPE = 'https://www.googleapis.com/auth/indexing'
PUBLISH_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
TIMEZONE = 'America/Los_Angeles'

# Google's current initial default is 200 publish requests/day/project. Keep
# 20 requests in reserve for another process or an untracked manual request.
DEFAULT_DAILY_LIMIT = 180
TIMEOUT = 45
MAX_RETRIES = 2
RETRY_BACKOFF = 5
MIN_REQUEST_DELAY = 1.0
MAX_CONSECUTIVE_TRANSIENT_FAILURES = 3
SITEMAP_NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

REDACT_EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+')
REDACT_BEARER = re.compile(r'Bearer\s+[A-Za-z0-9._-]+', re.IGNORECASE)


def now_utc():
    return datetime.now(timezone.utc)


def pacific_date():
    """Return Google's daily quota date without requiring pytz."""
    try:
        from zoneinfo import ZoneInfo
        return now_utc().astimezone(ZoneInfo(TIMEZONE)).date().isoformat()
    except (ImportError, KeyError):
        # macOS/Python 3.9+ has zoneinfo. UTC is a safe fallback for a rare
        # stripped runtime; it may reset a few hours earlier/later only.
        return now_utc().date().isoformat()


def iso_now():
    return now_utc().isoformat(timespec='seconds')


def redact(text):
    """Keep API errors useful without leaking account identifiers or tokens."""
    text = REDACT_EMAIL.sub('[redacted-email]', str(text))
    text = REDACT_BEARER.sub('Bearer [redacted-token]', text)
    return text[:500]


def error_summary(response):
    try:
        payload = response.json()
        err = payload.get('error', payload)
        if isinstance(err, dict):
            parts = [str(err[key]) for key in ('status', 'message', 'reason')
                     if err.get(key)]
            if parts:
                return redact(' | '.join(parts))
    except (ValueError, TypeError):
        pass
    return redact(response.text)


def extract_urls(path):
    if not path.exists():
        raise RuntimeError(f'找不到 sitemap：{path}')
    root = ET.parse(path).getroot()
    urls = []
    seen = set()
    for elem in root.findall(f'{SITEMAP_NS}url'):
        loc = elem.find(f'{SITEMAP_NS}loc')
        if loc is None or not loc.text:
            continue
        url = loc.text.strip()
        if url.startswith(SITE_URL) and url not in seen:
            urls.append(url)
            seen.add(url)
    return urls


def relative_url(url):
    parsed = urlparse(url)
    return parsed.path.lstrip('/')


def absolute_url(value):
    value = str(value or '').strip()
    if not value:
        return ''
    return value if value.startswith('http') else urljoin(SITE_URL, value)


def load_hot_tools(path):
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f'读取热门工具清单失败：{path}: {exc}') from exc
    if not isinstance(payload, list):
        raise RuntimeError(f'热门工具清单不是数组：{path}')
    result = []
    seen = set()
    for item in payload:
        value = item.get('u') if isinstance(item, dict) else item
        url = absolute_url(value)
        if url.startswith(SITE_URL) and url not in seen:
            result.append(url)
            seen.add(url)
    return result


def traffic_scores(path):
    """Aggregate tool-page traffic by industry for collection-page ranking."""
    scores = {}
    if not path.exists():
        return scores
    try:
        with path.open(newline='', encoding='utf-8') as source:
            for row in csv.DictReader(source):
                page = row.get('page', '')
                parts = urlparse(page).path.strip('/').split('/')
                if len(parts) < 3 or parts[0] != 'tools' or parts[2] == 'index.html':
                    continue
                industry = parts[1]
                try:
                    impressions = float(row.get('impressions') or 0)
                except ValueError:
                    impressions = 0.0
                try:
                    clicks = float(row.get('clicks') or 0)
                except ValueError:
                    clicks = 0.0
                score = scores.setdefault(industry, [0.0, 0.0, 0])
                score[0] += impressions
                score[1] += clicks
                score[2] += 1
    except OSError as exc:
        print(f'⚠️ 读取热度文件失败，集合页改用字母顺序：{exc}')
    return scores


def collection_urls(all_urls):
    scores = traffic_scores(TRAFFIC_FILE)
    discovered = {}
    for url in all_urls:
        rel = relative_url(url)
        match = re.fullmatch(r'tools/([^/]+)/index\.html', rel)
        if match:
            discovered[match.group(1)] = url

    # Protect against a stale sitemap: category landing pages are also
    # discovered from the checked-out site itself.
    for path in sorted((ROOT / 'tools').glob('*/index.html')):
        industry = path.parent.name
        discovered.setdefault(industry, urljoin(SITE_URL, f'tools/{industry}/index.html'))

    def rank(item):
        industry, url = item
        impressions, clicks, page_count = scores.get(industry, (0, 0, 0))
        return (-impressions, -clicks, -page_count, industry)

    return [url for _, url in sorted(discovered.items(), key=rank)]


def build_queue():
    sitemap_urls = extract_urls(SITEMAP_FILE)
    sitemap_set = set(sitemap_urls)
    collections = collection_urls(sitemap_urls)
    hot = [url for url in load_hot_tools(HOT_TOOLS_FILE)
           if url not in set(collections)]

    # Keep priority URLs even when the local sitemap has not caught up yet.
    ordered = []
    phase_by_url = {}
    for phase, values in (('collection', collections), ('hot', hot),
                          ('sitemap', sitemap_urls)):
        for url in values:
            if not url.startswith(SITE_URL) or url in phase_by_url:
                continue
            ordered.append(url)
            phase_by_url[url] = phase

    return ordered, phase_by_url, len(sitemap_set), len(collections), len(hot)


def empty_state():
    return {
        'version': 1,
        'site_url': SITE_URL,
        'updated_at': iso_now(),
        'daily': {
            'quota_date_pacific': pacific_date(),
            'publish_attempts': 0,
            'accepted': 0,
            'stopped_reason': '',
        },
        'urls': {},
    }


def load_state(path):
    if not path.exists():
        return empty_state()
    try:
        state = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f'读取状态文件失败：{path}: {exc}') from exc
    if not isinstance(state, dict):
        raise RuntimeError(f'状态文件格式错误：{path}')
    state.setdefault('version', 1)
    state.setdefault('site_url', SITE_URL)
    state.setdefault('urls', {})
    state.setdefault('daily', {})
    reset_daily_state(state)
    return state


def reset_daily_state(state):
    today = pacific_date()
    daily = state.setdefault('daily', {})
    if daily.get('quota_date_pacific') != today:
        state['daily'] = {
            'quota_date_pacific': today,
            'publish_attempts': 0,
            'accepted': 0,
            'stopped_reason': '',
        }
    else:
        daily.setdefault('publish_attempts', 0)
        daily.setdefault('accepted', 0)
        daily.setdefault('stopped_reason', '')


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    state['updated_at'] = iso_now()
    temp = path.with_name(f'.{path.name}.{os.getpid()}.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8')
    os.replace(temp, path)


def acquire_lock(state_path):
    """Prevent overlapping cron runs from double-submitting the same URL."""
    try:
        import fcntl
    except ImportError:
        return None
    lock_path = state_path.with_suffix(state_path.suffix + '.lock')
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open('a+', encoding='utf-8')
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return False
    handle.seek(0)
    handle.truncate()
    handle.write(f'pid={os.getpid()} started_at={iso_now()}\n')
    handle.flush()
    return handle


def load_credentials(path):
    if not path.exists():
        raise RuntimeError(
            f'找不到凭证文件：{path}\n'
            '请通过 --credential 指定 JSON，或设置 GOOGLE_INDEXING_CREDENTIAL')
    creds = service_account.Credentials.from_service_account_file(
        str(path), scopes=[SCOPE])
    creds.refresh(Request())
    return creds


def valid_token(creds):
    if not creds.valid:
        creds.refresh(Request())
    return creds.token


def parse_error_reason(response):
    try:
        payload = response.json()
        err = payload.get('error', {})
        if isinstance(err, dict):
            reasons = []
            if err.get('status'):
                reasons.append(str(err['status']))
            for detail in err.get('details', []):
                if isinstance(detail, dict) and detail.get('reason'):
                    reasons.append(str(detail['reason']))
            return '|'.join(reasons).lower()
    except (ValueError, TypeError):
        pass
    return ''


def publish_url(creds, url, on_attempt):
    """Return (status, category, attempts, error).

    category is one of accepted, quota, auth, transient, permanent, budget.
    """
    last_error = ''
    for attempt in range(1, MAX_RETRIES + 2):
        if on_attempt() is False:
            return 0, 'budget', attempt - 1, '本轮本地预算已用完'
        try:
            token = valid_token(creds)
            response = requests.post(
                PUBLISH_ENDPOINT,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                },
                json={'url': url, 'type': 'URL_UPDATED'},
                timeout=TIMEOUT,
            )
        except requests.exceptions.RequestException as exc:
            last_error = redact(f'{type(exc).__name__}: {exc}')
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
                continue
            return 0, 'transient', attempt, last_error

        if response.status_code == 200:
            return response.status_code, 'accepted', attempt, ''

        last_error = error_summary(response)
        reason = parse_error_reason(response)

        if response.status_code == 401:
            try:
                creds.refresh(Request())
            except Exception as exc:  # token refresh will be retried next cron
                last_error = redact(f'token refresh failed: {type(exc).__name__}')
            if attempt <= MAX_RETRIES:
                continue
            return response.status_code, 'auth', attempt, last_error

        # Any 429 is a deliberate hard stop. It may be per-minute or daily
        # quota, and continuing would turn a safe cron into a quota hammer.
        if response.status_code == 429 or 'quota' in reason:
            return response.status_code, 'quota', attempt, last_error

        if response.status_code in (500, 502, 503, 504):
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
                continue
            return response.status_code, 'transient', attempt, last_error

        if response.status_code == 403:
            return response.status_code, 'auth', attempt, last_error
        return response.status_code, 'permanent', attempt, last_error

    return 0, 'transient', MAX_RETRIES + 1, last_error


def url_status(state, url, retry_failed):
    record = state.get('urls', {}).get(url, {})
    status = record.get('status')
    if status == 'submitted':
        return 'done'
    if status == 'failed' and not retry_failed:
        return 'failed'
    return 'pending'


def main():
    parser = argparse.ArgumentParser(
        description='Google Web Search Indexing API 安全队列提交')
    parser.add_argument(
        '--credential',
        default=os.environ.get('GOOGLE_INDEXING_CREDENTIAL', DEFAULT_CREDENTIAL),
        help='服务账号 JSON 路径（也可用 GOOGLE_INDEXING_CREDENTIAL）')
    parser.add_argument(
        '--state',
        default=str(DEFAULT_STATE_FILE),
        help=f'状态文件路径（默认 {DEFAULT_STATE_FILE}）')
    parser.add_argument(
        '--daily-limit', type=int, default=DEFAULT_DAILY_LIMIT,
        help=f'本地每日 publish 上限，默认 {DEFAULT_DAILY_LIMIT}，0 不建议使用')
    parser.add_argument(
        '--limit', type=int, default=0,
        help='本轮最多提交 URL 数，0=受每日上限控制')
    parser.add_argument(
        '--retry-failed', action='store_true',
        help='重试此前记录为永久失败的 URL')
    parser.add_argument(
        '--dry-run', action='store_true', help='只显示队列，不请求 Google')
    parser.add_argument(
        '--yes', action='store_true', help='兼容 cron；保留参数但不会交互确认')
    args = parser.parse_args()

    if args.daily_limit <= 0:
        parser.error('--daily-limit 必须大于 0；如需调整请显式设置一个正数')
    if args.limit < 0:
        parser.error('--limit 不能小于 0')

    state_path = Path(args.state).expanduser()
    lock = acquire_lock(state_path)
    if lock is False:
        print('已有另一轮提交任务运行，本轮退出，不重复提交。')
        return 0

    try:
        queue, phase_by_url, sitemap_count, collection_count, hot_count = build_queue()
        state = load_state(state_path)
        save_state(state_path, state)

        pending = [url for url in queue
                   if url_status(state, url, args.retry_failed) == 'pending']
        daily = state['daily']
        remaining_daily = max(0, args.daily_limit - daily['publish_attempts'])
        run_budget = remaining_daily
        if args.limit:
            run_budget = min(run_budget, args.limit)

        print(f'站点: {SITE_URL}')
        print(f'sitemap URL: {sitemap_count} | 集合页: {collection_count} | '
              f'热门工具: {hot_count} | 队列总数: {len(queue)}')
        print(f'已成功记录: {sum(1 for v in state["urls"].values() if v.get("status") == "submitted")} | '
              f'永久失败: {sum(1 for v in state["urls"].values() if v.get("status") == "failed")} | '
              f'待处理: {len(pending)}')
        print(f'配额日期(Pacific): {daily["quota_date_pacific"]} | '
              f'本地 publish 尝试: {daily["publish_attempts"]}/{args.daily_limit} | '
              f'本轮预算: {run_budget}')

        if args.dry_run:
            for url in pending[:20]:
                print(f'  [{phase_by_url.get(url, "unknown")}] {url}')
            return 0

        if daily.get('stopped_reason'):
            print(f'本日已停止：{daily["stopped_reason"]}')
            return 0
        if run_budget <= 0:
            print('本日没有剩余本地配额，明天按队列继续。')
            return 0
        if not pending:
            print('✅ 所有队列 URL 都已有处理记录。')
            return 0

        print('加载服务账号凭证 ...')
        creds = load_credentials(Path(args.credential).expanduser())
        accepted = 0
        failed = 0
        calls = 0
        consecutive_transient = 0
        started = time.time()

        for url in pending:
            if calls >= run_budget:
                break

            def on_attempt():
                nonlocal calls
                if calls >= run_budget:
                    return False
                calls += 1
                state['daily']['publish_attempts'] += 1
                save_state(state_path, state)
                return True

            phase = phase_by_url.get(url, 'unknown')
            status, category, attempts, message = publish_url(creds, url, on_attempt)
            record = state['urls'].setdefault(url, {})
            record.update({
                'phase': phase,
                'last_attempt_at': iso_now(),
                'attempts': record.get('attempts', 0) + attempts,
                'last_http_status': status,
            })

            if category == 'accepted':
                record.update({
                    'status': 'submitted',
                    'submitted_at': iso_now(),
                    'last_error': '',
                })
                state['daily']['accepted'] += 1
                accepted += 1
                consecutive_transient = 0
                print(f'✅ [{phase}] HTTP 200 {url}')
            elif category == 'quota':
                reason = f'HTTP {status}: {message or "quota/rate limit"}'
                record.update({'status': 'pending', 'last_error': reason})
                state['daily']['stopped_reason'] = reason
                save_state(state_path, state)
                print(f'⏹️ 配额或限流，立即停止：{reason}')
                break
            elif category == 'budget':
                state['daily']['stopped_reason'] = '本轮本地预算已用完'
                record.update({'status': 'pending', 'last_error': message})
                save_state(state_path, state)
                print('⏹️ 本轮本地预算已用完，明天继续。')
                break
            elif category == 'auth':
                reason = f'HTTP {status}: {message or "authentication/permission error"}'
                record.update({'status': 'pending', 'last_error': reason})
                state['daily']['stopped_reason'] = reason
                save_state(state_path, state)
                print(f'⏹️ 权限/认证错误，停止整轮：{reason}')
                break
            elif category == 'transient':
                record.update({'status': 'pending', 'last_error': message})
                failed += 1
                consecutive_transient += 1
                print(f'⚠️ 临时错误，保留待重试 [{phase}] HTTP {status}: {url}')
                if consecutive_transient >= MAX_CONSECUTIVE_TRANSIENT_FAILURES:
                    reason = f'连续 {consecutive_transient} 个临时错误，主动停止'
                    state['daily']['stopped_reason'] = reason
                    save_state(state_path, state)
                    print(f'⏹️ {reason}')
                    break
            else:
                record.update({
                    'status': 'failed',
                    'failed_at': iso_now(),
                    'last_error': message,
                })
                failed += 1
                consecutive_transient = 0
                print(f'❌ 永久失败 [{phase}] HTTP {status}: {url}')

            save_state(state_path, state)
            if calls < run_budget:
                time.sleep(MIN_REQUEST_DELAY)

        elapsed = time.time() - started
        print(f'本轮完成：publish 尝试 {calls} 次 | 接收成功 {accepted} | '
              f'失败/待重试 {failed} | 耗时 {elapsed:.0f}s')
        print(f'状态已保存：{state_path}')
        return 0
    finally:
        if lock not in (None, False):
            lock.close()


if __name__ == '__main__':
    sys.exit(main())
