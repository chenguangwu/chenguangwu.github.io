# 第303批 · url-parser 空域名生成畸形 URL（IT清单）

## 根因
`buildUrl()` 无条件以 `proto+'//'` 起拼，host 为空时直接拼上 path，生成 `https:///path` 畸形 URL；`copyBuiltUrl()` 会把该畸形串复制到剪贴板。清单第84行子问题之一。

## 改动
- `tools/it/url-parser.html`
  - `buildUrl()`：host 为空 → `builtUrl` 显示双语提示「请输入域名 / Please enter a hostname」并返回空串，不生成畸形 URL。
  - `copyBuiltUrl()`：先取 `buildUrl()` 返回值，为空串则不复制。
  - 提示用内联 helper `(typeof TBKit!=='undefined'&&TBKit.util&&TBKit.util.isEn&&TBKit.util.isEn())` 保证英文态零 CJK；不新增 i18n 词表 key。
  - 域名非空的正常构造路径完全不变。
- `scripts/verify_it_calc.js`：新增 1 条精确强锁用例 `URLHOST OK`（clicks 探针：host 为空、path=/path → buildUrl 返回空串且提示含「域名」且不含 /path）。

## 验证
- verify 单 slug：旧源码 6/7（真红，fullBlob 末尾 `BAD https:///path?query=value&foo=bar`，探针确实生效）；修复后 7/7。
- 全量 verify：1707/1707 通过（EXIT=0）。
- 旧源码差分：换回旧 buildUrl/copyBuiltUrl → 6/7 红；恢复修好版 → 7/7 绿。
- JSDOM 真机三态：
  - 中文态 host 为空 → 返回空串、`builtUrl=请输入域名`、copyText 调用 0 次（OK）
  - 中文态 host 非空 → `https://example.com/path?...` 合法构造、copyText 调用 1 次（OK，未误伤）
  - 英文态 host 为空 → 返回空串、`builtUrl=Please enter a hostname`、无 CJK（OK）
- 完整门禁：待跑（后台）。

## 备注
- 同清单条目的端口子问题（`type=number` 已挡非数字，1-65535 范围未校验）保留待裁断，未擅动。
- 仅本地 commit，不 push。
