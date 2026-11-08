# IT-N365 json-to-xml 根为数组时输出多个并列根元素 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/json-to-xml.html`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

`toXml()` 对数组按同一标签逐项平铺，且不区分 depth。根级数组因此得到多个并列根元素：

```
<?xml version="1.0" encoding="UTF-8"?>
<root>1</root>
<root>2</root>
```

XML 只允许单一根元素，任何解析器都会报 `junk after document element`，合法 JSON 数组转出的产物必然不可用。

## 修复

`toXml()` 数组分支增加深度 0 的特判：

```js
if(Array.isArray(v)){
  if(depth === 0){
    const innerRoot = v.map(item => toXml(item, 'item', indent, 1)).join(indent ? '\n' : '');
    if(indent) return '<' + t + '>\n' + innerRoot + '\n</' + t + '>';
    return '<' + t + '>' + innerRoot + '</' + t + '>';
  }
  ...（原有分支不变）
}
```

根名仍取用户填写的 `#root`，子项统一用 `<item>`。

## 判别力实测（jsdom 真机）

```
--- [1,2] 美化 ---            --- {"a":[1,2]} 美化（嵌套数组不受影响）---
<?xml version="1.0"?>         <?xml version="1.0"?>
<root>                        <root>
  <item>1</item>                <a>1</a>
  <item>2</item>                <a>2</a>
</root>                       </root>
```

修复前 `[1,2]` 输出两个并列 `<root>`，本用例即为回归判据。

## 为什么没有新增门禁用例（harness 限制，请复核方知悉）

该页 `loadSample()` 是无参顶层函数，harness 的兜底循环会在注入之后重跑它，把 `#input` 重置为内置样例并重新 `doBeautify()` ⇒ 注入的 `[1,2]` 在采集时已被覆盖。此外 `#output` 用 `textContent` 承载 XML，harness 的 `collectStrings` 会剥掉所有 `<...>` 标签，XML 结构在 blob 里不可见。
两者叠加使本页无法构造稳定的注入型断言，故以 jsdom 真机取证（上面三段输出）。
