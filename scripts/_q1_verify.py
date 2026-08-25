#!/usr/bin/env python3
"""Q1 真实缺口核验：对每个候选给多个中英文同义词，全站 name/desc/en/ed 任一命中即判存在。
只输出真正缺失（全部同义词均未命中）的候选，并打印命中名供透明核对。
"""
import json

PATH = "json/tools.json"

# 候选 -> 同义词列表（小写）
CANDIDATES = {
    "json-minify": ["json 压缩", "json minif", "json 最小化", "压缩 json", "json压缩"],
    "json-validate": ["json 校验", "json valid", "json 验证", "校验 json", "json验证"],
    "json-diff": ["json 比对", "json diff", "json 对比", "比对 json", "json比对"],
    "yaml-to-toml": ["yaml 转 toml", "yaml to toml", "yaml转toml"],
    "toml-to-yaml": ["toml 转 yaml", "toml to yaml", "toml转yaml"],
    "yaml-to-json": ["yaml 转 json", "yaml to json"],
    "toml-to-json": ["toml 转 json", "toml to json"],
    "flexbox-generator": ["flexbox", "flex 布局生成", "弹性布局生成", "flex生成"],
    "border-radius": ["圆角生成", "border-radius", "css 圆角生成"],
    "slugify": ["slug", "slugify"],
    "mac-generator": ["mac 地址生成", "mac address generator", "随机 mac", "mac生成"],
    "ipv6-ula": ["ipv6", "ipv6 ula", "ula 生成"],
    "chmod": ["chmod"],
    "css-minify": ["css 压缩", "css minif", "css压缩"],
    "html-minify": ["html 压缩", "html minif", "html压缩"],
    "xml-to-json": ["xml 转 json", "xml to json"],
    "json-to-xml": ["json 转 xml", "json to xml"],
    "device-info": ["浏览器信息", "device information", "设备信息", "浏览器检测"],
    "ua-parser": ["user agent", "ua 解析", "user-agent", "ua解析"],
    "ulid": ["ulid"],
    "git-cheatsheet": ["git 速查", "git cheatsheet", "git 备忘"],
    "shuffle": ["洗牌", "shuffle"],
    "draw-lot": ["抽签", "随机抽选", "抽奖", "随机抽"],
    "px-to-rem": ["px 转 rem", "px to rem", "px转rem"],
    "rem-to-px": ["rem 转 px", "rem to px"],
    "vh-vw": ["vh", "vw", "视口单位", "viewport"],
    "svg-optimize": ["svg 压缩", "svg optim", "svg 优化", "svg压缩"],
    "aes-text": ["aes", "加密文本", "encrypt text", "文本加密"],
    "text-ascii": ["ascii 二进制", "ascii binary", "文本转 ascii", "ascii码"],
    "emoji-picker": ["emoji 选择", "emoji picker", "emoji 搜索", "emoji选择"],
    "numeronym": ["numeronym", "数字缩写"],
    "phone-parser": ["电话解析", "phone parser", "电话号码格式化", "手机格式化"],
    "eta": ["eta", "到达时间", "eta计算"],
    "keycode": ["keycode", "键码", "按键码"],
    "basic-auth": ["basic auth", "basicauth"],
    "otp": ["otp", "totp", "动态码"],
    "wifi-qr": ["wifi", "wifi qr", "wifi二维码"],
    "http-headers": ["http 头", "http header", "http 头信息", "http头"],
    "string-obfuscator": ["字符串混淆", "obfuscator", "字符串加密"],
    "latex": ["latex"],
    "markdown-preview": ["markdown 预览", "markdown preview", "md 预览"],
    "csv-to-yaml": ["csv 转 yaml", "csv to yaml", "csv转yaml"],
    "base64-file": ["base64 文件", "base64 file", "文件 base64"],
    "yaml-to-toml2": ["yaml转toml"],
    # 第四轮：it-tools 其余缺口
    "text-nato": ["nato", "北约字母", "字母表 拼写"],
    "text-unicode": ["文本转 unicode", "text to unicode", "unicode 转换", "unicode 编码"],
    "list-converter": ["list converter", "列表转换", "列表互转", "列表格式化"],
    "ipv4-subnet": ["子网", "subnet", "子网计算", "子网划分"],
    "ipv4-address": ["ipv4 地址", "ipv4 address", "ip 地址转换", "ip地址换算"],
    "ipv4-range": ["ipv4 范围", "ip 范围", "range expand", "ip段展开"],
    "random-port": ["随机端口", "random port", "端口生成"],
    "email-normalizer": ["邮件规范化", "email normalizer", "邮箱规范化", "邮箱标准化"],
    "bip39": ["bip39", "助记词", "助记词生成"],
    "svg-placeholder": ["svg 占位", "svg placeholder", "占位图", "占位 svg"],
    "docker-compose": ["docker compose", "docker run", "compose 转换", "compose 生成"],
    "color-converter": ["颜色转换", "color converter", "颜色值转换", "hex rgb 转换", "hex转rgb"],
    "html-wysiwyg": ["富文本", "wysiwyg", "html 编辑器", "可视化编辑"],
    "benchmark": ["基准测试", "benchmark"],
}


def main():
    with open(PATH, encoding="utf-8") as f:
        tools = json.load(f)
    corpus = []
    for t in tools:
        s = " ".join([t.get("name", ""), t.get("desc", ""), t.get("en", ""), t.get("ed", "")]).lower()
        corpus.append((t.get("name", ""), s))
    present, absent = {}, []
    for label, toks in CANDIDATES.items():
        hits = []
        for name, s in corpus:
            if any(tok.lower() in s for tok in toks):
                hits.append(name)
        if hits:
            present[label] = hits[0]
        else:
            absent.append(label)
    print(f"工具总数: {len(tools)}")
    print(f"\n=== 真正缺失（{len(absent)}）===")
    for a in absent:
        print(f"  + {a}")
    print(f"\n=== 已存在（{len(present)}）===")
    for k, v in present.items():
        print(f"  - {k}  =>  {v}")


if __name__ == "__main__":
    main()
