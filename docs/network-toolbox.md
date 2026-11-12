# 网络工具箱（Network Toolbox）

纯前端网络诊断工具集，集成于 `tools/it/network-toolbox.html`（分类：IT 开发）。不引入后端、不需要 API Key、不埋点、不上报；结果只保留在当前页面内存中，最近一次成功结果另存于本机浏览器 `localStorage`（键 `ntHist_v1`），不上传。

## 新增/修改文件

| 文件 | 说明 |
|---|---|
| `tools/it/network-toolbox.html` | 13 个工具的聚合页面（卡片分区，静态结构） |
| `js/network-toolbox.js` | 全部工具逻辑、统一超时/错误分类/复制/状态机 |
| `i18n/tools/en/it/network-toolbox.json` | 英文映射（166 键，英文值 0 CJK） |
| `i18n/tools/_en_override.json` | 新增 `it/network-toolbox` 标题/描述英文覆盖，供构建注入 `title-en`/`desc-en` meta |
| `i18n/tools/slug-en.json` | 新增 `it/network-toolbox` 键，满足行业工具↔英文映射一致性门禁 |
| `i18n/tools/en/it/_index.json` | 注册 slug，`tool-i18n.js` 才会加载该页字典 |
| `i18n/tools/it-body.json` | 标题/简介英文映射 |
| `json/tools.json` | 工具总表新增条目 |
| `json/industry-groups.json` | IT 分类导航新增入口 |
| `scripts/_verify_network_toolbox.mjs` | JSDOM 全链路验证（25 项） |

## 工具与外部端点

| 工具 | 端点 | 降级行为 |
|---|---|---|
| T1 多源 IP | ipwho.is → ipapi.co/json → api.ip.sb/geoip → api64.ipify.org；v6.ident.me | 全失败显示失败原因；IPv6 失败静默跳过 |
| T2 任意 IP | ipwho.is/{ip} → ipapi.co/{ip}/json | 非法 IP 不发请求；主源失败回退备源 |
| T3 本机内网 IP | WebRTC（无 STUN）host candidate | 无候选/浏览器禁用显示说明 |
| T4 站点可达性 | Google/GitHub/Cloudflare/OpenAI favicon | onerror/超时分类，favicon 改版可能误判 |
| T5 自定义 URL | fetch no-cors → favicon Image | no-cors 不读状态码 |
| T6 WebRTC 泄露 | STUN（默认 stun.l.google.com:19302，可 `?stun=` 覆盖） | 无候选显示说明 |
| T7 NAT 推断 | 3 个公共 STUN | 少于 2 个映射则「无法判断」 |
| T8 DNS 出口 | **需自有域名**（未配置） | 明确降级，不伪造结果 |
| T9 CDN 边缘 | 可配置静态资源 URL，读 cf-ray/x-served-by/x-cache | 读不到头退化为最小 RTT |
| T10 代理分流 | 国内/国外各 3 站 favicon | 启发式，非读取系统代理配置 |
| T11 测速 | speed.cloudflare.com/\_\_down | 单轮失败跳过，全失败报错；保持前台 |
| T12 浏览器指纹 | 本地 Canvas/WebGL + crypto.subtle | 无 WebCrypto 降级 FNV-1a |
| T13 服务状态 | GitHub/Cloudflare/Vercel/npm Statuspage API | 失败/CORS 显示 unknown |

## 统一约定

- 所有外部请求 6–8 秒超时（测速 30 秒），用 `AbortController` 取消；WebRTC 3–5 秒关闭连接。
- 错误分类：`超时` / `网络错误` / `接口限流` / `格式错误`，附原因与重试按钮。
- 每个工具有独立「复制结果」，顶部有「复制全部结果」；复制失败回退 `document.execCommand('copy')`。
- 结果区 `aria-live="polite"`；移动端单列自适应。
- **运行记录与对比**：每个工具最近一次成功结果（含时间戳）存本机 `localStorage`，不上传；页面底部汇总表展示状态、最近成功时间与上次结果摘要，点「对比上次」逐行显示 `- 上次 / + 本次` 差异。存储不可用（隐私模式）时静默跳过，不影响工具；换浏览器/清除站点数据后记录消失。
- T8 是唯一功能降级项：页面默认不配置任何自有域名接口，不产出假数据。

## 本地预览

```bash
python3 -m http.server 8765
# 打开 http://127.0.0.1:8765/tools/it/network-toolbox.html
```

验证：

```bash
env -u NODE_OPTIONS node scripts/_verify_network_toolbox.mjs
```

## 已知限制

- `no-cors` 无法读取 HTTP 状态码，可达性只能判断网络层是否接受请求。
- 免费公共 API 的 CORS 策略与限流可能变化；失败会显示原因，不会伪装成功。
- 浏览器隐私设置（禁用 WebRTC、mDNS 混淆、限制 Canvas/WebGL）会影响 T3/T6/T7/T12 的结果精度。
