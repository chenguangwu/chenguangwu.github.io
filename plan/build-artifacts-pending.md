# 主工作区待集成入库清单（构建产物快照）

> 快照：2026-11-05 11:45（Asia/Shanghai）｜HEAD `29c04d8392`（= origin）｜已跟踪变更 **157** 条
>
> 本轮已 push `498b41383b..29c04d8392`（36 笔），CI run `41963140091`：
> `Build and test` **success**、`Deploy to GitHub Pages` **success**（线上已切到本批）。
>
> 构建：主工作区 `_build.py` 1 次（HEAD `e7e01841f8`），产物 **223** 条（`json/**` 221 + guides 纯 TTZ 2）。
> 门禁：干净 worktree @`840020995e` 全量 **229/229 PASS**，wall clock **4m28.8s**。
>
> 未纳入产物的脏文件一律不进本批：工具页 78、i18n 65、scripts 6、guides 3、plan 2、共享单点 4。

## 0. 本轮产物（已入库）

```text
index.html  sitemap.xml  sitemap.html  sw.js  js/industry-info.js
json/**（tools/industry-*/guides 等 216 个）
guides/{detector-134,detector-155,detector-159,detector-hardness-torque,detector-stretch,rebar-anchorage,two-way-slab}-guide.html（纯 TTZ）
```

## 1. 明确排除

- `tools/<cat>/<slug>.html` 工具页（构建期 meta 刷新不属产物；84 页错改批一律不 add）
- `i18n/**`、`scripts/**`、`plan/**`、`css/**`、`js/**`、`_build.py`（在途线/共享单点）
- `guides/{calc-39,ratio-hormone,tongue-twister}-guide.html`（非纯 TTZ，夹带正文改动）

## 2. 取证

- 构建前 mtime：`/tmp/int5-prebuild-mtime.txt`；add 清单：`/tmp/int5-add.txt`（223）
- 门禁日志：`/tmp/int5-gates.log`（含各项耗时）
- 线上抽样：`/tmp/chk-json_tools.json`、`/tmp/chk-json_guides.json`、`/tmp/chk-guides_index.html`
