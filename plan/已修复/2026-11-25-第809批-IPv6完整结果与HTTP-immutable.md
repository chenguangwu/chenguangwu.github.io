# 第809批：IPv6 说明与完整结果，HTTP immutable 语义

关闭 `plan/it/` 3 项：

- IPv6转换-说明中的零压缩示例不是完整地址
- IPv6转换-历史和CSV截断完整转换结果
- HTTP缓存速查-immutable并非永不过期

## IPv6 转换（`tools/it/ipv6-converter.html`）

- 说明拆成两条独立规则：
  - 前导零省略仍保留 8 组：`2001:0db8:0000:0000:0000:0000:0000:0001 → 2001:db8:0:0:0:0:0:1`；
  - 连续全零组压缩：`2001:db8:0:0:0:0:0:1 → 2001:db8::1`；
  - 删除不合法示例 `1:0:0:0 写作 1::`，避免把「补零」和「压缩」混为一谈。
- 新增 `__ipv6LastFullText`：转换成功时由结构化字段拼出完整结果（展开、压缩、前缀、8 段），不再依赖结果区 DOM。
- `__ipv6_converterResText()` 优先返回完整文本，删除 `slice(0,80)`；历史与 CSV 导出不再截断 8 段/展开地址。
- 英文态通过 `i18n/tools/en/it/ipv6-converter.json` 同步两条新说明。

## HTTP 缓存速查（`tools/it/http-cache.html`）

- `immutable` 描述由「资源永不过期，无需验证」改为「在 max-age 新鲜期内不再发条件请求；新鲜期仍有限，过期后照常重新验证」。
- FAQ 正文与可见 FAQ 同步：说明它不会无限期有效，只适用于带内容哈希、内容不变的 URL；到期后仍重新验证。
- 英文态补充两条新文案的 `i18n/tools/en/it/http-cache.json` 映射。

## 验证

- 定向：IPv6 7/7、HTTP 5/5。
- 全量 IT：2409/2409。
- Puppeteer 真机：2/2，验证完整 IPv6 文本长度 171 且历史记录完整，HTTP 搜索 immutable 后列表显示新语义且不再出现旧「永不过期」文案。
- 门禁：static 0 失败 0 告警；links 0 死链；assets 0 死链 / 0 lang 缺失 / 0 重复 id；inline marker 通过。
