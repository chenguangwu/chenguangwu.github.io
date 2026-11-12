# 网络诊断工具（13 项独立工具）

纯前端网络诊断工具集，位于 `tools/telecom/`，每项工具一个独立页面（`data-tool="tX"`）。不引入后端、不需要 API Key、不埋点、不上报；结果只写当前页，最近一次成功结果另存于本机浏览器 `localStorage`，不上传。

> 历史说明：早期版本是 `tools/it/network-toolbox.html` 单页聚合 13 张卡片。因信息密度过高、显示 `[object Object]` 等问题，已按用户要求拆分为 13 个独立页并移入 `telecom` 分类；旧 URL 直接删除并提死链，不再维护聚合页。

## 工具清单

| 页面 | 工具 | 说明 |
|---|---|---|
| `public-ip-lookup.html` | T1 多源 IP 查询 | 公网出口 IP / 归属 / ISP / ASN / 时区，多源自动回退 |
| `ip-geolocation.html` | T2 任意 IP 查询 | 指定 IP 归属查询，先本地校验格式 |
| `local-ip-address.html` | T3 本机内网 IP | WebRTC host candidate 读取，无 STUN |
| `site-reachability.html` | T4 站点可达性 | 主流站点 favicon 启发式探测 |
| `url-reachability.html` | T5 自定义 URL | `fetch no-cors` + favicon 双重判断 |
| `webrtc-leak-test.html` | T6 WebRTC 泄露 | STUN 下的本机/公网候选对比 |
| `nat-type-test.html` | T7 NAT 类型推断 | 3 个公共 STUN 的映射行为推断 |
| `dns-egress-lookup.html` | T8 DNS 出口查询 | 需自有域名，**默认不配置、不伪造结果** |
| `cdn-edge-check.html` | T9 CDN 边缘节点 | 静态资源响应头 cf-ray / x-served-by 等 |
| `proxy-routing-test.html` | T10 代理分流规则 | 国内外站点 favicon 对比，启发式 |
| `network-speed-test.html` | T11 下行 + 延迟测速 | Cloudflare 测速端点，单轮失败跳过 |
| `browser-fingerprint.html` | T12 浏览器指纹 | 本地 Canvas/WebGL + WebCrypto，无 WebCrypto 降级 FNV-1a |
| `service-status.html` | T13 服务状态看板 | Statuspage API，失败显示 unknown |

## 架构与权威源

| 文件 | 说明 |
|---|---|
| `scripts/_gen_net_tools.py` | **页面权威源**：13 个页面的文案、字段、FAQ、模板；改页面先改这里再重跑 |
| `scripts/_gen_net_en.py` | 英文映射权威源：`i18n/tools/en/telecom/<slug>.json`、`telecom-body.json`、`_en_override.json`、`slug-en.json` |
| `js/network-toolbox.js` | 共享核心：13 项工具逻辑、统一超时/错误分类/复制/状态机/历史对比；一处实现，13 页复用 |
| `scripts/_verify_net_tools.mjs` | JSDOM 验证（66 项），含 `data-tool`、结果容器、按钮、字段表/FAQ、`[object Object]` 哨兵、T1 时区取值 |
| `docs/network-toolbox.md` | 本文档 |

页面内的 `<script>` 提供本页独立的本机存储适配层 `window.__ntStorage`，key 为 `ntHist_v1:tX`；共享 JS 通过它读写，缺失时退回统一 key。这样既保证各工具历史互不覆盖，也让存储逻辑在页面自身可见、可独立验证。

## 工具与外部端点

| 工具 | 端点 | 降级行为 |
|---|---|---|
| T1 | ipwho.is → ipapi.co/json → api.ip.sb/geoip → api64.ipify.org；v6.ident.me | 全失败显示失败原因；IPv6 失败静默跳过 |
| T2 | ipwho.is/{ip} → ipapi.co/{ip}/json | 非法 IP 不发请求；主源失败回退备源 |
| T3 | WebRTC（无 STUN）host candidate | 无候选/浏览器禁用显示说明 |
| T4 | Google/GitHub/Cloudflare/OpenAI favicon | onerror/超时分类，favicon 改版可能误判 |
| T5 | fetch no-cors → favicon Image | no-cors 不读状态码 |
| T6 | STUN（默认 `stun.l.google.com:19302`，可 `?stun=` 覆盖） | 无候选显示说明 |
| T7 | 3 个公共 STUN | 少于 2 个映射则「无法判断」 |
| T8 | **需自有域名**（未配置） | 明确降级，不伪造结果 |
| T9 | 可配置静态资源 URL，读 cf-ray/x-served-by/x-cache | 读不到头退化为最小 RTT |
| T10 | 国内/国外各 3 站 favicon | 启发式，非读取系统代理配置 |
| T11 | speed.cloudflare.com/\_\_down | 单轮失败跳过，全失败报错；保持前台 |
| T12 | 本地 Canvas/WebGL + crypto.subtle | 无 WebCrypto 降级 FNV-1a |
| T13 | GitHub/Cloudflare/Vercel/npm Statuspage API | 失败/CORS 显示 unknown |

## 统一约定

- 所有外部请求 6–8 秒超时（测速 30 秒），用 `AbortController` 取消；WebRTC 3–5 秒关闭连接。
- 错误分类：`超时` / `网络错误` / `接口限流` / `格式错误`，附原因与重试按钮。
- 每项工具独立「复制结果」；复制失败回退 `document.execCommand('copy')`。
- 结果区 `aria-live="polite"`；移动端单列自适应。
- **运行记录与对比**：最近一次成功结果（含时间戳）存本机 `localStorage`，页面底部汇总表展示状态、最近成功时间与上次结果摘要；点「对比上次」逐行显示 `- 上次 / + 本次` 差异。存储不可用（隐私模式）时静默跳过。
- **快捷预设**：带输入项的工具（T2/T5/T9）提供常用地址一键填充；无输入项工具提供「立即刷新」按钮，真实触发本页工具重新执行。
- T8 是唯一功能降级项：页面默认不配置任何自有域名接口，不产出假数据。

## 本地预览与验证

```bash
python3 -m http.server 8765
# 打开 http://127.0.0.1:8765/tools/telecom/public-ip-lookup.html
```

```bash
python3 scripts/_gen_net_tools.py   # 改文案/字段/FAQ 后重跑（会覆盖 13 个页面）
python3 scripts/_gen_net_en.py      # 同步英文映射
python3 _build.py                   # 重建 sitemap / 分类索引 / 繁体 / sw
env -u NODE_OPTIONS node scripts/_verify_net_tools.mjs
python3 scripts/_ux_baseline.py telecom --slug
```

## 已知限制

- `no-cors` 无法读取 HTTP 状态码，可达性只能判断网络层是否接受请求。
- 免费公共 API 的 CORS 策略与限流可能变化；失败会显示原因，不会伪装成功。
- 浏览器隐私设置（禁用 WebRTC、mDNS 混淆、限制 Canvas/WebGL）会影响 T3/T6/T7/T12 的结果精度。
- 核心逻辑放在共享 JS，构建脚本的 `own_len` 只统计页面自身内联代码，因此 13 页质量分级为 C；这是共享架构与分级口径的差异，不代表功能缺失。
