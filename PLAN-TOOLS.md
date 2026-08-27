# ToolBox 新增工具候选池（Q1）

> **方向**：新建工具候选池 + 分批开发上线（A 级质量）。
> **依据**：忽略 GSC，基于 it-tools.tech 竞品缺口 + 自身判断拟定（计算/转换/速查/生成器优先）。
> **去重**：反查现有 5031 工具，排除已覆盖项；`keycode-lookup`(=存量 keycode-info)、`text-to-nato`(=存量 nato-alphabet) 功能重叠，已排除。
> **质量门槛**：每批工具 A 级达标（own_len≥6000 或 ≥3000 且 inputs≥3），靠真实功能模块（参考表/明细/计算）而非代码膨胀。
> **英文**：每批开发后必同步 `i18n/tools/_en_override.json`(标题/简介) + `slug-en.json`(卡片)，高质量语义化，禁止 slug 直译；跑 `python3 _build.py` 后验证英文无残留。
> **门禁**：每批 `scripts/run_gates.py` 5/5 + `_build.py` 重建，独立 commit+push。

## 一期（13，转换器/编码/速查）— 开发批次 gen_q1e ✅ 已上线
| slug | industry | 定位 |
|---|---|---|
| roman-numeral-converter | it | 罗马数字 ↔ 阿拉伯数字互转 |
| mime-type-lookup | it | 文件扩展名 ↔ MIME 类型速查 |
| http-methods-reference | it | HTTP 方法语义/安全/幂等速查 |
| json-repair | it | 粘贴损坏 JSON 一键修复并校验 |
| text-to-braille | text | 文本转盲文 Unicode 点字 |
| text-to-1337 | text | 文本转 Leet 语（多强度） |
| binary-to-ascii | encode | 二进制/十六进制串转 ASCII 文本 |
| text-to-ascii-art | text | 文本转 ASCII 大字艺术字 |
| triangle-calculator | it | 三角形边长/角度/面积/周长计算 |
| prime-checker | it | 质数检测 + 因数分解 |
| color-shade-generator | design | 基色生成明暗梯度（tint/shade） |
| ipv4-range-expander | it | CIDR/范围展开网络地址与可用数 |
| ipv6-converter | it | IPv6 地址压缩/展开标准化 |

## 二期（13，生成器/计算/生活）— 开发批次 gen_q1f ✅ 已上线
| slug | industry | 定位 |
|---|---|---|
| wifi-qr-generator | it | WiFi 配置生成二维码文本 |
| docker-run-converter | it | docker run 命令 ↔ compose 互转 |
| gradient-generator | design | CSS 渐变生成器（线性/径向） |
| lorem-ipsum-generator | text | 占位文本生成器 |
| reading-time-estimator | text | 文章阅读时长估算 |
| split-bill | accounting | 多人分账/小费计算 |
| gst-calculator | tax | 增值税（含税/不含税）计算 |
| date-duration | it | 两日期相差天数/工作日 |
| recipe-scaler | baking | 配方按份量缩放 |
| fuel-cost-calculator | automotive | 油费/百公里成本估算 |
| parking-fee | daily-goods | 停车费阶梯计算 |
| unit-price-compare | biz | 不同规格单价对比 |
| unit-converter-advanced | it | 进阶单位换算（多类目） |

## 三期（13，校验/配置生成）— 开发批次 gen_q1g ✅ 已上线（实际行业 it/design，因 data/security/seo 目录未建）
| slug | industry | 定位 |
|---|---|---|
| xml-validator | it | XML 格式校验 + 美化 |
| csv-validator | data | CSV 表头/列数校验 |
| css-minify | it | CSS 压缩 |
| js-minify | it | JS 压缩（安全去空白/注释） |
| markdown-lint | text | Markdown 常见规范检查 |
| hash-identifier | security | 哈希类型识别 |
| gitignore-generator | it | .gitignore 模板生成 |
| dockerfile-generator | it | Dockerfile 模板生成 |
| sitemap-generator | seo 或 it | 简易 sitemap.xml 生成 |
| color-blindness-sim | design | 色盲模拟预览 |
| nginx-config-generator | it | Nginx server 块配置生成 |
| kubernetes-yaml-generator | it | K8s Deployment YAML 生成 |
| meta-tags-generator | seo 或 it | SEO meta 标签生成 |

## 已排除候选（DUPLICATE / REJECTED）
- keycode-lookup → 存量 `keycode-info` 等价
- text-to-nato → 存量 `nato-alphabet` 等价
- （其余 it-tools 缺口 angle/energy/sql-formatter/git-cheatsheet/xml-formatter 等已在更早批次上线）
