# 461 · 安全-哈希页 MD5 不可用与 IT-json-to-tsv 旧输出残留

## 问题 1（真缺陷）：哈希校验页 MD5 永远报错
`tools/safety/haxijisuan.html` 默认算法是 **MD5**，但实现走 `crypto.subtle.digest('MD5', ...)`。
WebCrypto 规范不支持 MD5，任何输入都抛
`Failed to execute 'digest' on 'SubtleCrypto'`；且在非安全上下文（`file://`、非 HTTPS）连 SHA 也整体不可用。

### 修复
在页面内内置纯 JS 实现 `__hashHex(algo, text)`：UTF-8 编码 + MD5 / SHA-1 / SHA-256，
`process()` 改为同步取值，彻底摆脱 `crypto.subtle` 与安全上下文限制。
验证：
- 已知向量：`MD5('hello')=5d41402abc…`、`SHA-1('hello')=aaf4c61d…`、`SHA-256('hello')=2cf24dba…` 全部一致；
- 与 Node `crypto.createHash` 对「中文串 / 长串 1000 字符 / 空串」三算法逐一比对，无差异；
- 页面脚本 `node --check` 通过，模拟 DOM 调用 `process()` 正常渲染。

## 问题 2（G10 同源）：json-to-tsv 空/非法输入残留旧输出
`tools/it/json-to-tsv.html` 输入清空或 JSON 解析失败时只清 `#j2tStats`，`#tsvOutput` 仍保留上一次结果，
用户会把旧 TSV 当成当前输入的结果（与 G10「输入失效后旧结果残留」同类）。

### 修复
输入事件里空值 / 解析异常 / 非数组三条分支统一清空 `#j2tStats` 与 `#tsvOutput`。

## 清单滞后销账
`plan/no-effect-recheck.md` A 节另两页经源码核验已修好，不重复改：
- `tools/stats/regression-analysis.html:395` 已绑定 `pred-x` input；
- `tools/stats/statistical-tests.html:692` 已绑定 `one-mu` input。

## 验证
- 两页脚本 `node --check` 通过；`python3 _build.py` 通过。
- `plan/no-effect-recheck.md` 顶部加收口说明，A 节 4 页全部关闭。
