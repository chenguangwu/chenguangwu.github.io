# 2026-11-11 第191批 · IT-N104/N105 HTTP 请求头速查：删编造字段 + 补常用头

## 清单项
- **IT-N104**：凭空编造 `Range-Unit` 请求头并单列「范围」分类（中，参考结果错误）
- **IT-N105**：缺最常用的缓存与安全头，「缓存」分类只剩 Vary（中，参考结果缺失）

## 根因
- `Range-Unit: <unit>` / `Range-Unit: bytes` 在 RFC 9110 中不存在；范围单位由 `Range: bytes=…` 与 `Accept-Ranges: bytes` 表达。页面为不存在的字段单开一个分类，会误导用户照抄后被服务端/代理拒绝。
- 91 条条目中 `Cache-Control`、`ETag`、`Last-Modified`、`Expires`、`Strict-Transport-Security`、`Content-Security-Policy`、`Permissions-Policy` 均无独立词条（`ETag` 仅作为 `If-Match`/`If-None-Match` 参数出现），「缓存」分类只有 `Vary` 一条，最常查阅的缓存协商/安全头查不到。

## 改动
`tools/it/http-headers.html` 的 `COMMANDS`：
1. 删除 `Range-Unit` 条目及其独有的「范围」分类（`Range`/`Accept-Ranges` 原有 `params: "bytes"` 已正确表达单位，无需另立字段）；
2. 新增 7 条独立词条并归入已有分类，避免改变既有分类首次出现顺序：
   - 缓存（+4）：`Cache-Control`（no-store/max-age/s-maxage/immutable）、`ETag`（W/ 弱验证）、`Last-Modified`、`Expires`
   - 安全（+3）：`Strict-Transport-Security`（max-age/includeSubDomains/preload）、`Content-Security-Policy`（default-src 等）、`Permissions-Policy`（`<feature>=<allowlist>`）
3. 总数 91 → 97，分类 21 → 20（「范围」消失），缓存 1 → 5、安全 5 → 8；分类明细表与图表统计随 `hdAgg()` 自动更正。
4. `i18n/tools/en/it/http-headers.json`：删除编造字段残留键 `支持的范围单位`，新增 8 条英译映射（7 条 desc + `W/ 表示弱验证`）。
5. `scripts/verify_it_calc.js` 新增 5 条强锁：结构（RU=0/total=97/cats=20）、7 头齐全、分类计数（cache=5/sec=8）、搜索 `Cache-Control` 命中 1 项、搜索 `Range-Unit` 零命中。

## 验证证据
- **真机** `scripts/_verify_it_batch191.mjs`（JSDOM）：**29/29**——数据层编造字段清零/7 头齐全/无重复/总数与分类结构、RFC 示例内容校验（no-store+immutable、HSTS max-age+includeSubDomains、CSP default-src+'self'、Permissions-Policy allowlist）、默认渲染 97 卡片、搜索行为、状态链、分类切换、明细表 20 行且各类之和 97、英文态 Caching/Security、per-tool en JSON 映射完整且旧键已删。
  **旧源码 5/29**（读 `/tmp/http-headers.N104N105.before.html` 与旧 en JSON）——差分成立。
- **verify 用例级旧源码差分**：修好版 **1530/1530**；临时换入旧源码后 **1525/1530**，5 条新锁全红；恢复后页面 MD5 与修好版一致（`97e1463bff5ccb761d510b4dfc23f266`）。全程 `/tmp` 备份往返，未用 `git checkout --`。
- audit 注入键 **30840**、用例 10326、僵尸 id 0；单文件判别力正确变红 1528/1529，唯一逃生 `it/vector-magnitude` 为既有基线、跳过 1 为既有；i18n `--check` 0 残留、`--roundtrip` 0 不一致。

## 备注
- **踩坑一**：初始 `HDRNEED 7|` 断言存在前缀逃生——旧态输出 `HDRNEED 7|Cache-Control,ETag,…` 仍命中前缀 `HDRNEED 7|`，旧源码差分只红 4/5。改为显式 `HDRNEED OK/BAD 7|…` 后旧态 5/5 全红。**教训：探针断言空列表时不要在可变内容前放固定的尾随分隔符，必须加显式状态标记。**
- **踩坑二**：搜索 `ETag` 命中 4 项（`If-Match`/`If-None-Match` 等条件请求条目的 desc/params 也含 ETag），是正常检索行为；断言改为检查渲染出的 `.cmd-name` 是否含独立 `ETag` 词条，旧态无该词条 ⇒ 差分仍强。
- **IT-N106 仍未处理**：中文标题只写「请求头」但收录响应头，需单独一批统一 title/h1/面包屑/JSON-LD 与方向标签，本批未动，留清单。
- 只本地提交、不 push。
