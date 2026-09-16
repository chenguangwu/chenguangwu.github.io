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
DEFAULT_LOG_FILE = ROOT / '.codex' / 'tasks' / 'google-indexing-api.log'
# 日志最多保留多少行；超过后只保留最新的 N 行（含头部新内容）
DEFAULT_MAX_LOG_LINES = 1000
DEFAULT_CREDENTIAL = os.path.expanduser(
    '~/.workbuddy/gsc_indexing_service_account.json')

SCOPE = 'https://www.googleapis.com/auth/indexing'
PUBLISH_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'
INSPECT_SCOPE = 'https://www.googleapis.com/auth/webmasters'
INSPECT_ENDPOINT = 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect'
# Search Console URL Inspection API 每日配额 10000，本地留一半安全余量
DEFAULT_INSPECT_DAILY_LIMIT = 5000
INSPECT_TIMEOUT = 30
TIMEZONE = 'America/Los_Angeles'
LOG_TIMEZONE = 'Asia/Shanghai'

# Google's current initial default is 200 publish requests/day/project. Keep
# 20 requests in reserve for another process or an untracked manual request.
DEFAULT_DAILY_LIMIT = 198
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


def beijing_now():
    """Return current time as aware datetime in Asia/Shanghai."""
    try:
        from zoneinfo import ZoneInfo
        return now_utc().astimezone(ZoneInfo(LOG_TIMEZONE))
    except (ImportError, KeyError):
        # Fallback: UTC+8 wall time when zoneinfo is unavailable.
        from datetime import timedelta
        return now_utc().astimezone(timezone(timedelta(hours=8)))


# Log file realtime-flush control (set by main() when args parsed)
_LOG_FILE_PATH = None
_LOG_MAX_LINES = 0
_LOG_BUFFER = []
_LAST_FLUSH_TS = 0.0
# Flush when batch threshold OR interval threshold reached
_LOG_FLUSH_BATCH = 5
_LOG_FLUSH_INTERVAL = 3.0


def log(msg=''):
    """Print + buffer for realtime prepend to log file.

    Flushing strategy: every _LOG_FLUSH_BATCH lines OR every
    _LOG_FLUSH_INTERVAL seconds, whichever comes first.
    Finally block flushes whatever is left as safety net.
    """
    stamp = beijing_now().strftime('%Y-%m-%d %H:%M:%S CST')
    line = f'[{stamp}] {msg}'
    print(line)
    _LOG_BUFFER.append(line)

    if not _LOG_FILE_PATH:
        return  # no log file configured (--no-log-file or before args parse)

    # Real-time flush decision
    now_ts = time.time()
    if (len(_LOG_BUFFER) >= _LOG_FLUSH_BATCH
            or now_ts - _LAST_FLUSH_TS >= _LOG_FLUSH_INTERVAL):
        _flush_log_buffer()


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
        log(f'⚠️ 读取热度文件失败，集合页改用字母顺序：{exc}')
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
    if status in ('submitted', 'indexed'):
        return 'done'
    if status == 'failed' and not retry_failed:
        return 'failed'
    return 'pending'




def inspect_url(creds, url, site_url):
    """Call Search Console URL Inspection API for one URL.

    Returns a dict: {coverage_state, error, http_status}
    coverage_state examples: Indexed | Not indexed | Not found | Blocked | 404
    On failure (network/quota/auth), coverage_state is None and error is set.
    """
    try:
        from google.oauth2 import service_account as _sa
        from google.auth.transport.requests import Request as _AuthRequest
        if not creds.valid:
            creds.refresh(_AuthRequest())
        # If the indexing creds don't carry the webmasters scope, get a fresh
        # token with the correct scope so we don't silently get 403.
        has_webmasters = INSPECT_SCOPE in (getattr(creds, 'scopes', None) or [])
        token_creds = creds
        if not has_webmasters:
            try:
                # service_account.Credentials has .with_scopes()
                token_creds = creds.with_scopes([INSPECT_SCOPE])
                token_creds.refresh(_AuthRequest())
            except Exception:
                token_creds = creds
                token_creds.refresh(_AuthRequest())
    except Exception as exc:
        return {'coverage_state': None, 'http_status': 0,
                'error': f'auth:{type(exc).__name__}'}

    try:
        import requests
        response = requests.post(
            INSPECT_ENDPOINT,
            headers={
                'Authorization': f'Bearer {token_creds.token}',
                'Content-Type': 'application/json',
            },
            json={'inspectionUrl': url, 'siteUrl': site_url},
            timeout=INSPECT_TIMEOUT,
        )
    except Exception as exc:
        return {'coverage_state': None, 'http_status': 0,
                'error': f'network:{type(exc).__name__}'}

    if response.status_code == 429:
        return {'coverage_state': None, 'http_status': 429, 'error': 'quota'}
    if response.status_code != 200:
        try:
            payload = response.json()
            err = payload.get('error', {}) if isinstance(payload, dict) else {}
            msg = err.get('message', response.text[:120]) if isinstance(err, dict) else str(err)
        except Exception:
            msg = response.text[:120]
        return {'coverage_state': None, 'http_status': response.status_code,
                'error': msg}

    try:
        payload = response.json()
    except Exception:
        return {'coverage_state': None, 'http_status': 200, 'error': 'bad json'}

    result = payload.get('inspectionResult', {}) or {}
    idx = result.get('indexStatusResult', {}) or {}
    coverage = idx.get('coverageState') or idx.get('coverage_state') or 'Unknown'
    return {
        'coverage_state': coverage,
        'http_status': 200,
        'error': '',
        'last_crawl': idx.get('lastCrawlTime', ''),
        'sitemap_state': idx.get('sitemapState', ''),
    }


def run_inspection(pending_urls, creds, state, state_path, args):
    """Run Search Console inspection on a batch of pending URLs.

    Returns (filtered_urls, stats) where stats is a dict of counters.
    If inspection is disabled or quota exhausted, returns original pending_urls
    and a skip flag so the main flow continues unaffected.
    """
    stats = {
        'checked': 0,
        'indexed': 0,
        'not_indexed': 0,
        'quota_hit': False,
        'auth_error': False,
        'network_error': False,
        'skipped_recent': 0,
    }

    if getattr(args, 'no_inspect', False):
        log('🔎 收录检查已跳过（--no-inspect）')
        return pending_urls, stats

    inspect_budget = getattr(args, 'inspect_limit', 500)
    if inspect_budget <= 0:
        log('🔎 收录检查禁用（inspect-limit <= 0）')
        return pending_urls, stats

    # Only inspect URLs we have submitted before (status=submitted), and
    # only those we haven't inspected in the last 7 days. Freshly-pending
    # URLs (status=pending never submitted) definitely aren't indexed yet,
    # so skip them to conserve the daily budget.
    from datetime import timedelta
    now = now_utc()

    def last_inspect_ok(record):
        """Return True if we inspected recently enough."""
        ts = record.get('inspected_at')
        if not ts:
            return False
        try:
            last = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return (now - last) < timedelta(days=7)
        except Exception:
            return False

    targets = []
    for u in pending_urls:
        rec = state['urls'].get(u, {})
        # Only inspect URLs that have been submitted at least once before,
        # AND haven't been inspected in the last 7 days.
        if rec.get('status') == 'submitted' and not last_inspect_ok(rec):
            targets.append(u)
        elif rec.get('status') == 'submitted':
            stats['skipped_recent'] += 1

    # Also cap by --inspect-limit
    targets = targets[:inspect_budget]
    if not targets:
        log('🔎 收录检查：没有需要检查的 URL（要么没提交过，要么 7 天内已检查过）')
        return pending_urls, stats

    log(f'🔎 开始收录检查：{len(targets)} 个待检查，{stats["skipped_recent"]} 个 7 天内已检查过跳过')
    filtered = []
    for url in pending_urls:
        if url not in set(targets):
            filtered.append(url)

    for idx, url in enumerate(targets, 1):
        if stats['quota_hit']:
            break
        result = inspect_url(creds, url, SITE_URL)
        stats['checked'] += 1
        rec = state['urls'].setdefault(url, {})
        rec['inspected_at'] = iso_now()
        rec['last_coverage_state'] = result.get('coverage_state')

        if result['http_status'] == 429:
            stats['quota_hit'] = True
            stats['quota_error'] = result.get('error', '429 quota')
            log(f'  ⏹️ Search Console 配额耗尽，停止收录检查（已检查 {stats["checked"]}/{len(targets)}）')
            break
        if result['http_status'] in (401, 403):
            stats['auth_error'] = True
            log(f'  ⏹️ Search Console 认证失败 HTTP {result["http_status"]}，跳过收录检查阶段')
            break
        if result['http_status'] == 0:
            # network-level failure
            stats['network_error'] = True
            log(f'  ⚠️ Search Console 网络异常（{result.get("error","?")}），继续尝试')
            filtered.append(url)
            if idx < len(targets):
                time.sleep(1.0)
            continue
        if result['http_status'] != 200:
            log(f'  ⚠️ Search Console HTTP {result["http_status"]}: {result.get("error","")[:100]}')
            filtered.append(url)
            continue

        state_ = result.get('coverage_state', '')
        if state_ == 'Indexed':
            stats['indexed'] += 1
            rec['status'] = 'indexed'
            log(f'  ⏭️ 已收录跳过 [{rec.get("phase","?")}] {url}')
        else:
            stats['not_indexed'] += 1
            log(f'  🔍 {state_} [{rec.get("phase","?")}] {url}')
            filtered.append(url)

        # Respect API rate limits – Search Console has per-minute limits too.
        if idx < len(targets):
            time.sleep(0.6)

    save_state(state_path, state)

    if stats['quota_hit']:
        log(f'⚠️ Search Console 配额耗尽，本轮收录检查中途停止，剩余 {len(targets) - stats["checked"]} 个未检查')
    elif stats['auth_error']:
        log(f'⚠️ Search Console 认证错误，本轮收录检查已跳过，仍有 {len(filtered) - stats["not_indexed"]} 个 pending 进入提交流程')

    return filtered, stats



def _flush_log_buffer():
    """Flush _LOG_BUFFER to the HEAD of _LOG_FILE_PATH.

    Only flushes the currently-buffered lines (not the whole run).
    Rotation applies each time: after merge with existing content,
    if over _LOG_MAX_LINES, truncate from the bottom.
    """
    global _LOG_BUFFER, _LAST_FLUSH_TS
    if not _LOG_BUFFER or not _LOG_FILE_PATH:
        return
    import tempfile as _tf
    target = Path(_LOG_FILE_PATH)
    try:
        new_lines = _LOG_BUFFER
        _LOG_BUFFER = []
        _LAST_FLUSH_TS = time.time()

        if target.exists():
            try:
                existing = target.read_text(encoding='utf-8', errors='replace').splitlines()
            except OSError:
                existing = []
        else:
            existing = []

        all_lines = new_lines + existing
        if _LOG_MAX_LINES and _LOG_MAX_LINES > 0 and len(all_lines) > _LOG_MAX_LINES:
            all_lines = all_lines[:_LOG_MAX_LINES]

        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = _tf.mkstemp(
            dir=target.parent, prefix=f'.{target.name}.', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_lines))
                if all_lines:
                    f.write('\n')
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
        os.replace(tmp_path, target)
    except Exception as exc:
        import sys
        print(f'⚠️ 写入日志文件失败 {target}: {exc}', file=sys.stderr)


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
    parser.add_argument(
        '--no-inspect', action='store_true',
        help='跳过 Search Console 收录检查，直接提交')
    parser.add_argument(
        '--inspect-limit', type=int, default=500,
        help=f'本轮收录检查最多检查多少 URL，默认 500；0 等于 --no-inspect')
    parser.add_argument(
        '--log-file', default=str(DEFAULT_LOG_FILE),
        help=f'日志文件路径（默认 {DEFAULT_LOG_FILE}，头部追加 + 自动轮转）')
    parser.add_argument(
        '--no-log-file', action='store_true',
        help='不写日志文件，只输出到 stdout')
    parser.add_argument(
        '--max-log-lines', type=int, default=DEFAULT_MAX_LOG_LINES,
        help=f'日志文件最多保留多少行（默认 {DEFAULT_MAX_LOG_LINES}，0=不限制）')
    args = parser.parse_args()

    # ── 日志文件配置（全局变量，log() 里要用）──────────────────────
    if not args.no_log_file and args.log_file:
        global _LOG_FILE_PATH, _LOG_MAX_LINES
        _LOG_FILE_PATH = str(Path(args.log_file).expanduser())
        _LOG_MAX_LINES = args.max_log_lines

    if args.daily_limit <= 0:
        parser.error('--daily-limit 必须大于 0；如需调整请显式设置一个正数')
    if args.limit < 0:
        parser.error('--limit 不能小于 0')

    state_path = Path(args.state).expanduser()
    lock = acquire_lock(state_path)
    if lock is False:
        log('已有另一轮提交任务运行，本轮退出，不重复提交。')
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

        log(f'站点: {SITE_URL}')
        log(f'sitemap URL: {sitemap_count} | 集合页: {collection_count} | '
              f'热门工具: {hot_count} | 队列总数: {len(queue)}')
        log(f'已提交: {sum(1 for v in state["urls"].values() if v.get("status") == "submitted")} | '
              f'已收录: {sum(1 for v in state["urls"].values() if v.get("status") == "indexed")} | '
              f'永久失败: {sum(1 for v in state["urls"].values() if v.get("status") == "failed")} | '
              f'待处理: {len(pending)}')
        log(f'配额日期(Pacific): {daily["quota_date_pacific"]} | '
              f'本地 publish 尝试: {daily["publish_attempts"]}/{args.daily_limit} | '
              f'本轮预算: {run_budget}')

        if args.dry_run:
            for url in pending[:20]:
                log(f'  [{phase_by_url.get(url, "unknown")}] {url}')
            return 0

        if daily.get('stopped_reason'):
            log(f'本日已停止：{daily["stopped_reason"]}')
            return 0
        if run_budget <= 0:
            log('本日没有剩余本地配额，明天按队列继续。')
            return 0
        if not pending:
            log('✅ 所有队列 URL 都已有处理记录。')
            return 0

        log('加载服务账号凭证 ...')
        try:
            creds = load_credentials(Path(args.credential).expanduser())
        except Exception as exc:
            # network/auth/credential errors surface here
            import requests.exceptions as _ReqExc
            try:
                from google.auth.exceptions import TransportError as _GAuthTransport
            except ImportError:
                _GAuthTransport = ()
            reason = ''
            if isinstance(exc, (_GAuthTransport,
                                 _ReqExc.ConnectTimeout,
                                 _ReqExc.ConnectionError,
                                 _ReqExc.Timeout,
                                 TimeoutError, OSError)):
                reason = '网络异常，无法连接 Google OAuth 服务'
            elif isinstance(exc, FileNotFoundError):
                reason = '凭证文件不存在'
            elif isinstance(exc, RuntimeError):
                reason = str(exc)
            else:
                reason = f'{type(exc).__name__}: {exc}'
            log(f'⚠️ 加载凭证失败：{reason}')
            state['daily']['stopped_reason'] = f'凭证加载失败: {reason}'
            save_state(state_path, state)
            log('本轮提前退出，等下一次 cron 再试')
            return 1

        # ── 收录检查阶段 ──────────────────────────────────────────────
        pending, insp_stats = run_inspection(pending, creds, state,
                                             state_path, args)
        if insp_stats['indexed']:
            log(f'📊 收录检查结果：检查 {insp_stats["checked"]}，已收录跳过 {insp_stats["indexed"]}，'
                  f'未收录 {insp_stats["not_indexed"]}，剩余待提交 {len(pending)}')
        elif insp_stats['checked']:
            log(f'📊 收录检查结果：检查 {insp_stats["checked"]}，全部未收录，剩余待提交 {len(pending)}')

        if not pending:
            log('✅ 所有待检查 URL 已收录，本轮无需提交。')
            return 0

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
                log(f'✅ [{phase}] HTTP 200 {url}')
            elif category == 'quota':
                reason = f'HTTP {status}: {message or "quota/rate limit"}'
                record.update({'status': 'pending', 'last_error': reason})
                state['daily']['stopped_reason'] = reason
                save_state(state_path, state)
                log(f'⏹️ 配额或限流，立即停止：{reason}')
                break
            elif category == 'budget':
                state['daily']['stopped_reason'] = '本轮本地预算已用完'
                record.update({'status': 'pending', 'last_error': message})
                save_state(state_path, state)
                log('⏹️ 本轮本地预算已用完，明天继续。')
                break
            elif category == 'auth':
                reason = f'HTTP {status}: {message or "authentication/permission error"}'
                record.update({'status': 'pending', 'last_error': reason})
                state['daily']['stopped_reason'] = reason
                save_state(state_path, state)
                log(f'⏹️ 权限/认证错误，停止整轮：{reason}')
                break
            elif category == 'transient':
                record.update({'status': 'pending', 'last_error': message})
                failed += 1
                consecutive_transient += 1
                log(f'⚠️ 临时错误，保留待重试 [{phase}] HTTP {status}: {url}')
                if consecutive_transient >= MAX_CONSECUTIVE_TRANSIENT_FAILURES:
                    reason = f'连续 {consecutive_transient} 个临时错误，主动停止'
                    state['daily']['stopped_reason'] = reason
                    save_state(state_path, state)
                    log(f'⏹️ {reason}')
                    break
            else:
                record.update({
                    'status': 'failed',
                    'failed_at': iso_now(),
                    'last_error': message,
                })
                failed += 1
                consecutive_transient = 0
                log(f'❌ 永久失败 [{phase}] HTTP {status}: {url}')

            save_state(state_path, state)
            if calls < run_budget:
                time.sleep(MIN_REQUEST_DELAY)

        elapsed = time.time() - started
        log(f'本轮完成：publish 尝试 {calls} 次 | 接收成功 {accepted} | '
              f'失败/待重试 {failed} | 耗时 {elapsed:.0f}s')
        log(f'状态已保存：{state_path}')
        return 0
    finally:
        if lock not in (None, False):
            lock.close()
        # ── 最终刷盘：清掉 buffer 里剩余的日志行 ────────────────────
        try:
            _flush_log_buffer()
        except Exception:
            pass


if __name__ == '__main__':
    sys.exit(main())
