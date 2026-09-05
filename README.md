# ToolBox

5000+ 个免费在线工具组成的纯前端工具百科。计算、转换、编码、文本处理、生成器、开发辅助和行业工具都在浏览器本地运行，用户数据不上传服务器。

## 项目特点

- 纯 HTML、CSS、原生 JavaScript 和 Python 构建脚本。
- 无账号、无后端业务接口，工具数据默认只在当前浏览器处理。
- 支持中英文界面、拼音搜索、模糊搜索、收藏、最近使用和深浅主题。
- 支持移动端布局、PWA 离线缓存和本地隐私管理。
- GitHub Actions 构建并通过 GitHub Pages 发布静态产物。

## 实时统计

统计数据由 `python3 _build.py` 根据当前工具页面自动更新，禁止手工修改。

<!-- TOOLBOX_STATS_START -->
| 指标 | 实时值 |
|---|---:|
| 工具总数 | 5004 |
| 行业总数 | 268 |
| A 级占比 | 100.0% |
| B 级占比 | 0.0% |
| C 级占比 | 0.0% |
<!-- TOOLBOX_STATS_END -->

## 本地运行

项目使用 `fetch` 加载索引 JSON，不能依赖 `file://` 协议直接打开首页。请在仓库根目录启动本地 HTTP 服务：

```bash
python3 -m http.server 8765
```

然后访问 <http://localhost:8765>。

### 台湾繁体页面

`zh-tw/` 是 `_build.py` 根据简体中文源页面生成的静态发布目录，已通过根目录 `.gitignore` 忽略：

- 本地调试时保留 `zh-tw/`，可直接访问 `http://localhost:8765/zh-tw/`；它不会出现在提交中。
- 首次克隆、主动删除目录或修改中文源页面后，先运行 `python3 _build.py` 重新生成。
- 不要使用 `git add -f zh-tw/`，繁体产物只由本地构建和 GitHub Actions 生成。
- 根 `sitemap.xml` 会始终包含简体与台湾繁体 URL，不以本地 `zh-tw/` 是否存在为判断条件；缺少该目录时，本地繁体链接会暂时返回 404，重新构建即可恢复。

## 构建与质量门禁

新增或修改工具后，运行统一门禁：

```bash
python3 scripts/run_gates.py
```

门禁包含：

- `python3 _build.py`：扫描工具页面并生成索引、行业数据、站点地图和 SEO 信息。
- `python3 _test_static.py`：检查静态页面结构、元数据和相关映射。
- `python3 _audit_links.py --check`：检查站内死链。
- `python3 _audit_assets.py --check`：检查局部资源、HTML 语言属性和重复 id。
- `node scripts/verify_calc.js`：执行计算工具回归用例。

GitHub Actions 会在 pull request 和推送到 `master` 时自动执行同一套门禁。
`master` 门禁通过后，Actions 会上传完整静态 artifact 并部署到 GitHub Pages。
`zh-tw/` 为构建期生成目录，不再提交到源码仓库。
发布前会运行 `scripts/check_pages_artifact.py`，产物达到 900MiB 安全阈值时停止部署。
仓库 Pages 的发布来源必须保持为 **GitHub Actions**，不要切回 `Deploy from a branch`。

## 目录说明

| 路径 | 用途 |
|---|---|
| `index.html` | 首页和行业导航 |
| `tools/<industry>/` | 工具页面，禁止直接放在 `tools/` 根目录 |
| `guides/` | 工具使用指南 |
| `css/` | 首页和工具页公共样式 |
| `js/` | 首页、工具页、i18n、PWA 和隐私功能 |
| `json/` | 构建生成的工具索引，不手工修改 |
| `zh-tw/` | 本地与 Actions 生成的台湾繁体静态站点，保留用于本地调试但不提交 |
| `scripts/` | 批量生成、审计和开发辅助脚本 |
| `_build.py` | 项目构建入口 |
| `AGENTS.md` | AI Agent 开发规范 |
| `DEV-PLAN.md` | i18n 专项开发计划 |
| `NEXT-DEV-PLAN.md` | 非 i18n 下一阶段任务计划 |

## 新增工具规则

1. 新工具必须放在对应的 `tools/<industry>/` 目录。
2. 页面必须声明 `meta name="toolbox"`，包含 `cat`、`industry`、`icon` 和 `bg` 等元数据。
3. 核心功能必须真实可用，不能使用静态假结果或占位逻辑。
4. 所有计算、转换和文件处理优先在浏览器本地完成。
5. 不新增后端服务、登录、支付、实时数据 API 或需要上传用户数据的功能。
6. 新页面遵守 `AGENTS.md`、`docs/i18n-spec.md` 和 `ui/设计规范.md`。
7. 不手工修改 `json/*.json`、`sitemap.xml` 或首页构建注入的工具统计。

## 发布流程

1. 在本地 HTTP 服务中验证首页、搜索、工具页和移动端布局。
2. 运行 `python3 scripts/run_gates.py`，确保五项门禁全部通过。
3. 提交源文件和需要版本化的构建产物；不提交 `zh-tw/`。
4. 推送到 `master`，等待 `ToolBox Build and Deploy` 完成门禁、artifact 上传和 Pages 部署。
5. 在 Actions 成功后验证简体首页、`/zh-tw/`、至少一个繁体工具页及根 `sitemap.xml`。
6. 索引提交由用户侧定时任务管理；不要在普通开发会话自动运行 `_submit_*` 脚本。

## 搜索引擎提交注意事项

- Bing URL API 保持小批量流式提交，脚本默认每批 10 条并按日期正序/倒序轮换，避免一次性批量提交 1 万条 URL。
- Bing 密钥通过 `BING_API_KEY` 环境变量提供，不要写进仓库、日志、命令行参数或 crontab 命令文本。
- `_submit_bing_url_api.py` 会先读取 Bing 当日/月度剩余额度并限制提交数量；额度查询失败时应停止，不能盲目全量提交。

## 相关文档

- [开发规范](AGENTS.md)
- [i18n 规范](docs/i18n-spec.md)
- [UI 设计规范](ui/设计规范.md)
- [下一阶段开发计划](NEXT-DEV-PLAN.md)
