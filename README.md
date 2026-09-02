# ToolBox

6000+ 个免费在线工具组成的纯前端工具百科。计算、转换、编码、文本处理、生成器、开发辅助和行业工具都在浏览器本地运行，用户数据不上传服务器。

## 项目特点

- 纯 HTML、CSS、原生 JavaScript 和 Python 构建脚本。
- 无账号、无后端业务接口，工具数据默认只在当前浏览器处理。
- 支持中英文界面、拼音搜索、模糊搜索、收藏、最近使用和深浅主题。
- 支持移动端布局、PWA 离线缓存和本地隐私管理。
- GitHub Pages 静态托管，构建产物直接发布。

## 实时统计

统计数据由 `python3 _build.py` 根据当前工具页面自动更新，禁止手工修改。

<!-- TOOLBOX_STATS_START -->
| 指标 | 实时值 |
|---|---:|
| 工具总数 | 4984 |
| 行业总数 | 267 |
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

## 目录说明

| 路径 | 用途 |
|---|---|
| `index.html` | 首页和行业导航 |
| `tools/<industry>/` | 工具页面，禁止直接放在 `tools/` 根目录 |
| `guides/` | 工具使用指南 |
| `css/` | 首页和工具页公共样式 |
| `js/` | 首页、工具页、i18n、PWA 和隐私功能 |
| `json/` | 构建生成的工具索引，不手工修改 |
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
3. 提交源文件和由构建产生的必要产物。
4. 推送到 `master`，等待 GitHub Actions 和 GitHub Pages 完成部署。
5. 索引提交由用户侧定时任务管理；不要在普通开发会话自动运行 `_submit_*` 脚本。

## 相关文档

- [开发规范](AGENTS.md)
- [i18n 规范](docs/i18n-spec.md)
- [UI 设计规范](ui/设计规范.md)
- [下一阶段开发计划](NEXT-DEV-PLAN.md)
