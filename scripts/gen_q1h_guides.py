# -*- coding: utf-8 -*-
"""N/Q1h 高价值指南扩容生成器：为 Q1 新增的高频核心工具补齐使用指南（第一批 20 篇）。
复用 scripts/gen_n8_guides.py 的范式：写指南 HTML + 合并 json/guides.json + 更新 guides/index.html + 导出英文包。
模板用 .replace() 规避 CSS 大括号被 format 误解析。
运行：python3 scripts/gen_q1h_guides.py

本批聚焦 Q1 工具中高频核心（it/ 转换校验开发类 + 少量日常高频）：
json-repair, xml-validator, csv-validator, css-minify, js-minify, markdown-lint,
hash-identifier, meta-tags-generator, docker-run-converter, dockerfile-generator,
gitignore-generator, nginx-config-generator, kubernetes-yaml-generator, sitemap-generator,
ipv4-range-expander, ipv6-converter, unit-converter-advanced, date-duration,
lorem-ipsum-generator, split-bill
"""
import os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

GUIDES = [
 {
  'slug': 'json-repair',
  'ind': 'it',
  'base': 'json-repair.html',
  'name': 'JSON 修复器',
  'desc': 'JSON 修复器使用指南：自动补全缺失的引号、括号与尾随逗号，把不规范的 JSON 修成可解析的合法 JSON。',
  'intro': '手写或接口返回的 JSON 常因漏括号、多逗号、用了单引号而报错。本工具尝试定位并修复常见格式问题，方便复制进代码或配置。纯前端，数据不上传。',
  'features': ['补全缺失的括号与引号', '去除尾随逗号', '单引号转双引号', '错误位置提示', '本地处理'],
  'scenarios': ['接口返回的 JSON 被截断', '从网页复制的 JSON 漏了符号', '调试 JSON.parse 报错'],
  'steps': ['粘贴疑似出错的 JSON', '点击修复', '复制修正后的结果'],
  'tips': ['修复后仍建议再校验一次', '嵌套深时优先检查最内层', '单引号是最常见的一个坑'],
  'faqs': [('能修复所有错误吗？', '不能，仅处理常见格式问题；字段语义错误仍需人工核对。'), ('能给个例子吗？', '{"a":1,} 去掉尾随逗号得到 {"a":1}。')],
  'en_name': 'JSON Repair',
  'en_desc': 'JSON Repair Guide: auto-complete missing quotes, brackets and trailing commas so malformed JSON becomes parseable.',
  'en_intro': 'Hand-written or API-returned JSON often breaks from missing brackets, trailing commas or single quotes. This tool locates and fixes common formatting issues so you can copy it into code or config. Pure front-end, nothing uploaded.',
  'en_features': ['Complete missing brackets and quotes', 'Strip trailing commas', 'Convert single quotes to double', 'Point out the error position', 'Local processing'],
  'en_scenarios': ['JSON from an API got truncated', 'JSON copied from a web page lost symbols', 'Debug a JSON.parse error'],
  'en_steps': ['Paste the likely-broken JSON', 'Click repair', 'Copy the fixed result'],
  'en_tips': ['Validate again after repair', 'For deep nesting, check the innermost level first', 'Single quotes are the most common pitfall'],
  'en_faqs': [('Can it fix every error?', 'No, only common formatting issues; field-semantic errors still need a human check.'), ('Can you show an example?', '{"a":1,} with the trailing comma removed becomes {"a":1}.')],
 },
 {
  'slug': 'xml-validator',
  'ind': 'it',
  'base': 'xml-validator.html',
  'name': 'XML 校验器',
  'desc': 'XML 校验器使用指南：检查 XML 是否格式良好（标签闭合、属性引号、嵌套正确），定位错误行与原因。',
  'intro': 'XML 常用于配置与数据交换。本工具解析并校验格式良好性（well-formed），指出未闭合标签或非法字符的位置。纯前端，数据不上传。',
  'features': ['标签闭合校验', '属性引号检查', '嵌套层级检查', '错误行定位', '本地处理'],
  'scenarios': ['排查配置文件报错', '校验接口返回的 XML', '检查 RSS / SVG 合法性'],
  'steps': ['粘贴 XML', '点击校验', '查看通过提示或错误位置'],
  'tips': ['格式良好不等于 schema 合法', 'CDATA 内文本不被解析', '注意大小写敏感'],
  'faqs': [('格式良好和合法有什么不同？', '格式良好只检查语法；合法还需符合 DTD/XSD 约束。'), ('能给个例子吗？', '<a><b>1</a> 缺 b 闭合，会报未闭合标签。')],
  'en_name': 'XML Validator',
  'en_desc': 'XML Validator Guide: check whether XML is well-formed (closed tags, quoted attributes, correct nesting) and locate errors.',
  'en_intro': 'XML is common in config and data exchange. This tool parses and validates well-formedness, pointing out unclosed tags or illegal characters. Pure front-end, nothing uploaded.',
  'en_features': ['Tag-closing validation', 'Quoted-attribute check', 'Nesting-level check', 'Error line location', 'Local processing'],
  'en_scenarios': ['Troubleshoot a config error', 'Validate XML returned by an API', 'Check RSS / SVG validity'],
  'en_steps': ['Paste the XML', 'Click validate', 'See the pass message or error position'],
  'en_tips': ['Well-formed is not the same as schema-valid', 'Text inside CDATA is not parsed', 'Note case sensitivity'],
  'en_faqs': [('What is the difference between well-formed and valid?', 'Well-formed checks syntax only; valid also needs a DTD/XSD contract.'), ('Can you show an example?', '<a><b>1</a> misses the b close tag and reports an unclosed tag.')],
 },
 {
  'slug': 'csv-validator',
  'ind': 'it',
  'base': 'csv-validator.html',
  'name': 'CSV 校验器',
  'desc': 'CSV 校验器使用指南：检查 CSV 的分隔符、引号包裹与列数一致性，定位错位与截断行。',
  'intro': 'CSV 看似简单却常在引号内出现逗号、换行而错位。本工具按 RFC4180 思路解析，报告列数不一致或引号不匹配的行。本地处理不上传。',
  'features': ['列数一致性检查', '引号包裹校验', '分隔符自动识别', '异常行定位', '本地处理'],
  'scenarios': ['导入前核对表格', '排查 Excel 导出的脏数据', '校验批量数据文件'],
  'steps': ['上传或粘贴 CSV', '选分隔符', '点击校验看告警'],
  'tips': ['引号内的逗号不会被拆列', '换行出现在引号内是合法的', '表头列数应等于数据列数'],
  'faqs': [('为什么我的行被拆开了？', '多半是某字段引号未闭合，导致后续换行被当作新行。'), ('能给个例子吗？', '"say ""hi""" 表示含转义引号的字段。')],
  'en_name': 'CSV Validator',
  'en_desc': 'CSV Validator Guide: check CSV delimiters, quote wrapping and column consistency, locating misaligned or truncated rows.',
  'en_intro': 'CSV looks simple but often breaks when a comma or newline appears inside quotes. This tool parses with RFC4180 in mind and reports rows with inconsistent columns or unmatched quotes. Local, nothing uploaded.',
  'en_features': ['Column-count consistency check', 'Quote-wrapping validation', 'Auto-detect delimiter', 'Abnormal-row location', 'Local processing'],
  'en_scenarios': ['Verify a table before import', 'Troubleshoot dirty Excel exports', 'Validate a bulk data file'],
  'en_steps': ['Upload or paste the CSV', 'Pick the delimiter', 'Click validate to see warnings'],
  'en_tips': ['A comma inside quotes is not a column split', 'A newline inside quotes is legal', 'Header column count should equal data column count'],
  'en_faqs': [('Why is my row split?', 'Usually an unclosed quote makes later newlines count as new rows.'), ('Can you show an example?', '"say ""hi""" denotes a field containing an escaped quote.')],
 },
 {
  'slug': 'css-minify',
  'ind': 'it',
  'base': 'css-minify.html',
  'name': 'CSS 压缩器',
  'desc': 'CSS 压缩器使用指南：删除注释、空白与多余分号，缩小样式文件体积以加速加载。',
  'intro': '压缩后的 CSS 去掉无用字符但保留语义，适合直接上线或合并进构建产物。本工具本地压缩不上传源码。',
  'features': ['删除注释与空白', '合并多余规则', '去除末尾分号', '体积对比展示', '本地处理'],
  'scenarios': ['上线前压缩样式', '合并多个 CSS 文件', '减小静态资源体积'],
  'steps': ['粘贴 CSS', '点击压缩', '复制结果或看压缩比'],
  'tips': ['压缩不改视觉效果', '建议保留一份未压缩源', '配合 Gzip 更佳'],
  'faqs': [('会改样式吗？', '不会，仅去除空白与注释。'), ('能给个例子吗？', '/* a */ .x{color:red;} 变为 .x{color:red}。')],
  'en_name': 'CSS Minifier',
  'en_desc': 'CSS Minifier Guide: strip comments, whitespace and trailing semicolons to shrink stylesheet size for faster loading.',
  'en_intro': 'Minified CSS removes useless characters while keeping semantics, ready to ship or merge into build output. This tool minifies locally, source not uploaded.',
  'en_features': ['Strip comments and whitespace', 'Merge redundant rules', 'Drop trailing semicolons', 'Show size comparison', 'Local processing'],
  'en_scenarios': ['Minify styles before release', 'Combine multiple CSS files', 'Reduce static asset size'],
  'en_steps': ['Paste the CSS', 'Click minify', 'Copy the result or see the ratio'],
  'en_tips': ['Minify does not change visuals', 'Keep an unminified source copy', 'Pair with Gzip for best results'],
  'en_faqs': [('Does it change styles?', 'No, only whitespace and comments are removed.'), ('Can you show an example?', '/* a */ .x{color:red;} becomes .x{color:red}.')],
 },
 {
  'slug': 'js-minify',
  'ind': 'it',
  'base': 'js-minify.html',
  'name': 'JS 压缩器',
  'desc': 'JS 压缩器使用指南：去除 JavaScript 中的空白、注释与冗余，缩小脚本体积加速加载。',
  'intro': '压缩后的 JS 去掉无关字符但保持可执行，适合上线前处理。本工具本地压缩不上传源码，且不混淆变量名以免引入风险。',
  'features': ['去除注释与空白', '简化字面量', '体积对比', '保留可执行性', '本地处理'],
  'scenarios': ['上线前压缩脚本', '减小第三方 JS 体积', '预览压缩比'],
  'steps': ['粘贴 JS', '点击压缩', '复制或看体积变化'],
  'tips': ['压缩不等于混淆', '保留源文件便于维护', '大文件留意浏览器上限'],
  'faqs': [('压缩后能跑吗？', '能，语义不变。'), ('能给个例子吗？', 'var a = 1; 压缩为 var a=1;。')],
  'en_name': 'JS Minifier',
  'en_desc': 'JS Minifier Guide: strip whitespace, comments and redundancy from JavaScript to shrink script size for faster loads.',
  'en_intro': 'Minified JS keeps executing while dropping irrelevant characters, ideal before release. This tool minifies locally, source not uploaded, and does not rename variables to avoid risk.',
  'en_features': ['Strip comments and whitespace', 'Simplify literals', 'Size comparison', 'Keeps executability', 'Local processing'],
  'en_scenarios': ['Minify scripts before release', 'Shrink third-party JS', 'Preview the compression ratio'],
  'en_steps': ['Paste the JS', 'Click minify', 'Copy or watch the size change'],
  'en_tips': ['Minify is not obfuscation', 'Keep the source for maintenance', 'Watch browser limits on large files'],
  'en_faqs': [('Does it still run after minify?', 'Yes, semantics are unchanged.'), ('Can you show an example?', 'var a = 1; becomes var a=1;.')],
 },
 {
  'slug': 'markdown-lint',
  'ind': 'it',
  'base': 'markdown-lint.html',
  'name': 'Markdown 检查器',
  'desc': 'Markdown 检查器使用指南：检查 Markdown 的标题层级、列表、链接与代码块常见写法问题，提升可读性。',
  'intro': 'Markdown 渲染依赖约定（如标题#后空格、列表缩进）。本工具按常见规范提示可疑写法，帮助你写出更一致的文档。本地处理不上传。',
  'features': ['标题层级检查', '列表与缩进提示', '链接格式校验', '代码块围栏检查', '本地处理'],
  'scenarios': ['写 README 前自查', '统一团队文档风格', '排查渲染异常'],
  'steps': ['粘贴 Markdown', '点击检查', '按提示修正'],
  'tips': ['标题 # 后留空格', '列表项对齐缩进', '代码块用成对围栏'],
  'faqs': [('会改我的内容吗？', '不会，仅给出提示。'), ('能给个例子吗？', '"#标题" 建议改为 "# 标题"。')],
  'en_name': 'Markdown Linter',
  'en_desc': 'Markdown Linter Guide: check heading levels, lists, links and code fences for common Markdown style issues to improve readability.',
  'en_intro': 'Markdown rendering relies on conventions (space after #, list indentation). This tool hints at suspicious writing by common rules so your docs stay consistent. Local, nothing uploaded.',
  'en_features': ['Heading-level check', 'List and indentation hints', 'Link format check', 'Code-fence check', 'Local processing'],
  'en_scenarios': ['Self-check before writing a README', 'Unify team doc style', 'Troubleshoot odd rendering'],
  'en_steps': ['Paste the Markdown', 'Click check', 'Fix per the hints'],
  'en_tips': ['Put a space after the heading #', 'Align list-item indentation', 'Use paired fences for code blocks'],
  'en_faqs': [('Does it change my content?', 'No, it only gives hints.'), ('Can you show an example?', '"#标题" is better as "# 标题".')],
 },
 {
  'slug': 'hash-identifier',
  'ind': 'it',
  'base': 'hash-identifier.html',
  'name': '哈希识别器',
  'desc': '哈希识别器使用指南：根据哈希字符串的长度与字符集，推断它可能是 MD5/SHA1/SHA256 等哪种摘要算法。',
  'intro': '不同哈希算法输出长度固定（MD5 32 位、SHA1 40 位、SHA256 64 位十六进制）。本工具输入一串哈希，给出最可能的算法与长度。本地识别不上传。',
  'features': ['按长度推断算法', '识别 MD5/SHA1/SHA256 等', '显示输出长度', '字符集判断', '本地处理'],
  'scenarios': ['排查数据库存的是哪种哈希', 'CTF / 安全学习', '确认摘要算法类型'],
  'steps': ['粘贴哈希串', '点击识别', '查看候选算法'],
  'tips': ['长度只是线索非绝对', '加盐哈希无法反推原文', 'NTLM 也是 32 位十六进制'],
  'faqs': [('能反解哈希吗？', '不能，哈希单向；只能识别类型。'), ('能给个例子吗？', '32 位十六进制可能是 MD5 或 NTLM。')],
  'en_name': 'Hash Identifier',
  'en_desc': 'Hash Identifier Guide: infer whether a hash string is likely MD5/SHA1/SHA256 etc. from its length and charset.',
  'en_intro': 'Different hash algorithms have fixed output lengths (MD5 32, SHA1 40, SHA256 64 hex chars). Paste a hash and this tool shows the most likely algorithm and length. Local identification, nothing uploaded.',
  'en_features': ['Infer algorithm by length', 'Recognize MD5/SHA1/SHA256', 'Show output length', 'Charset judgment', 'Local processing'],
  'en_scenarios': ['Find which hash a DB stored', 'CTF / security study', 'Confirm a digest algorithm'],
  'en_steps': ['Paste the hash', 'Click identify', 'See candidate algorithms'],
  'en_tips': ['Length is a clue, not proof', 'Salted hashes cannot be reversed', 'NTLM is also 32 hex chars'],
  'en_faqs': [('Can it reverse a hash?', 'No, hashing is one-way; it only identifies the type.'), ('Can you show an example?', 'A 32-hex string could be MD5 or NTLM.')],
 },
 {
  'slug': 'meta-tags-generator',
  'ind': 'it',
  'base': 'meta-tags-generator.html',
  'name': 'Meta 标签生成器',
  'desc': 'Meta 标签生成器使用指南：生成标题、描述、Open Graph 与 Twitter 卡片等社交分享标签，复制进页面 head。',
  'intro': '完整的 meta 标签影响搜索摘要与社交分享卡片。本工具按输入生成标准标签片段，含 og:/twitter: 与 canonical。本地生成不上传。',
  'features': ['生成 title/description', '生成 Open Graph 标签', '生成 Twitter 卡片', '输出 canonical', '本地处理'],
  'scenarios': ['新页面 SEO 基础', '配置社交分享卡片', '统一站点元信息'],
  'steps': ['填写标题与描述', '填图片与 URL', '复制 head 片段'],
  'tips': ['描述控制在 70–160 字', 'og:image 建议 1200x630', 'canonical 避免重复收录'],
  'faqs': [('OG 和 Twitter 都要吗？', '建议都加，覆盖不同平台。'), ('能给个例子吗？', '输出含 <meta property="og:title" ...>。')],
  'en_name': 'Meta Tags Generator',
  'en_desc': 'Meta Tags Generator Guide: generate title, description, Open Graph and Twitter Card tags to paste into your page head.',
  'en_intro': 'Complete meta tags affect search snippets and social share cards. This tool generates standard snippets including og:/twitter: and canonical. Local generation, nothing uploaded.',
  'en_features': ['Generate title/description', 'Generate Open Graph tags', 'Generate Twitter Card', 'Output canonical', 'Local processing'],
  'en_scenarios': ['SEO basics for a new page', 'Configure social share cards', 'Unify site meta info'],
  'en_steps': ['Fill title and description', 'Fill image and URL', 'Copy the head snippet'],
  'en_tips': ['Keep description 70–160 chars', 'og:image ideally 1200x630', 'canonical avoids duplicate indexing'],
  'en_faqs': [('Do I need both OG and Twitter?', 'Yes, to cover different platforms.'), ('Can you show an example?', 'Output includes <meta property="og:title" ...>.')],
 },
 {
  'slug': 'docker-run-converter',
  'ind': 'it',
  'base': 'docker-run-converter.html',
  'name': 'Docker Run 转 Compose',
  'desc': 'Docker Run 转 Compose 使用指南：把 docker run 命令解析为等价的 docker-compose.yml，便于多容器管理。',
  'intro': 'docker run 参数一长串难维护。本工具解析镜像、端口、挂载、环境变量等，生成结构化的 compose 文件。本地解析不上传。',
  'features': ['解析镜像与命令', '提取端口/挂载/环境变量', '生成 compose 结构', '保留常用参数', '本地处理'],
  'scenarios': ['把临时容器固化为配置', '多服务统一管理', '迁移单机命令到 compose'],
  'steps': ['粘贴 docker run 命令', '点击转换', '复制 docker-compose.yml'],
  'tips': ['卷挂载注意宿主机路径', '端口格式 主机:容器', '环境变量用 environment 段'],
  'faqs': [('compose 和 run 等价吗？', '语义一致，compose 更易维护。'), ('能给个例子吗？', '-p 8080:80 转为 ports: ["8080:80"]。')],
  'en_name': 'Docker Run to Compose',
  'en_desc': 'Docker Run to Compose Guide: turn a docker run command into an equivalent docker-compose.yml for multi-container management.',
  'en_intro': 'A long docker run line is hard to maintain. This tool parses image, ports, mounts and env vars into a structured compose file. Local parsing, nothing uploaded.',
  'en_features': ['Parse image and command', 'Extract ports/mounts/env', 'Generate compose structure', 'Keep common flags', 'Local processing'],
  'en_scenarios': ['Freeze an ad-hoc container into config', 'Manage multiple services together', 'Migrate a single command to compose'],
  'en_steps': ['Paste the docker run command', 'Click convert', 'Copy the docker-compose.yml'],
  'en_tips': ['Mind host paths in volume mounts', 'Port format is host:container', 'Use the environment section for vars'],
  'en_faqs': [('Is compose equivalent to run?', 'Semantics match; compose is easier to maintain.'), ('Can you show an example?', '-p 8080:80 becomes ports: ["8080:80"].')],
 },
 {
  'slug': 'dockerfile-generator',
  'ind': 'it',
  'base': 'dockerfile-generator.html',
  'name': 'Dockerfile 生成器',
  'desc': 'Dockerfile 生成器使用指南：按基础镜像、端口、命令等选项生成可运行的 Dockerfile 模板。',
  'intro': 'Dockerfile 写法固定却易写错。本工具按常见选项（基础镜像、暴露端口、启动命令、工作目录）生成标准 Dockerfile。本地生成不上传。',
  'features': ['选择基础镜像', '设置暴露端口', '配置启动命令', '设置工作目录', '本地处理'],
  'scenarios': ['新项目快速起容器', '标准化构建文件', '教学 Docker 基础'],
  'steps': ['选基础镜像与端口', '填启动命令', '点击生成复制'],
  'tips': ['优先小体积镜像', '用多阶段构建减小体积', 'CMD 用 exec 形式'],
  'faqs': [('基础镜像怎么选？', '按语言与体积，如 node:20-alpine。'), ('能给个例子吗？', '输出含 FROM / EXPOSE / CMD 指令。')],
  'en_name': 'Dockerfile Generator',
  'en_desc': 'Dockerfile Generator Guide: generate a runnable Dockerfile template from options like base image, ports and commands.',
  'en_intro': 'Dockerfiles follow a fixed shape but are easy to get wrong. This tool generates a standard Dockerfile from common options (base image, exposed port, start command, workdir). Local generation, nothing uploaded.',
  'en_features': ['Pick a base image', 'Set exposed ports', 'Configure start command', 'Set work directory', 'Local processing'],
  'en_scenarios': ['Spin up a container for a new project', 'Standardize build files', 'Teach Docker basics'],
  'en_steps': ['Pick base image and ports', 'Fill the start command', 'Click generate and copy'],
  'en_tips': ['Prefer small images', 'Use multi-stage builds to shrink size', 'Use exec form for CMD'],
  'en_faqs': [('How to pick a base image?', 'By language and size, e.g. node:20-alpine.'), ('Can you show an example?', 'Output includes FROM / EXPOSE / CMD instructions.')],
 },
 {
  'slug': 'gitignore-generator',
  'ind': 'it',
  'base': 'gitignore-generator.html',
  'name': '.gitignore 生成器',
  'desc': '.gitignore 生成器使用指南：按语言与框架勾选，生成标准 .gitignore 模板，避免把依赖与密钥提交进仓库。',
  'intro': '不同技术栈要忽略的文件不同（node_modules、__pycache__、.env 等）。本工具勾选后生成合并的 .gitignore。本地生成不上传。',
  'features': ['按语言/框架勾选', '合并常用规则', '包含密钥文件忽略', '标准模板', '本地处理'],
  'scenarios': ['新仓库初始化', '多语言项目合一', '防止误提交密钥'],
  'steps': ['勾选所用技术栈', '点击生成', '复制 .gitignore'],
  'tips': ['务必忽略 .env', '已跟踪文件需 git rm --cached', '全局忽略用 git config'],
  'faqs': [('已提交的文件还能忽略吗？', '需先 git rm --cached 取消跟踪。'), ('能给个例子吗？', '勾选 Node 生成 node_modules/ 规则。')],
  'en_name': '.gitignore Generator',
  'en_desc': '.gitignore Generator Guide: pick languages and frameworks to generate a standard .gitignore so deps and secrets stay out of the repo.',
  'en_intro': 'Different stacks ignore different files (node_modules, __pycache__, .env). Tick what you use and this tool merges a standard .gitignore. Local generation, nothing uploaded.',
  'en_features': ['Pick by language/framework', 'Merge common rules', 'Include secret-file ignores', 'Standard template', 'Local processing'],
  'en_scenarios': ['Initialize a new repo', 'Combine multi-language projects', 'Prevent committing secrets'],
  'en_steps': ['Tick your stacks', 'Click generate', 'Copy the .gitignore'],
  'en_tips': ['Always ignore .env', 'Tracked files need git rm --cached', 'Use git config for global ignores'],
  'en_faqs': [('Can an already-committed file be ignored?', 'First git rm --cached to untrack it.'), ('Can you show an example?', 'Tick Node to generate node_modules/ rules.')],
 },
 {
  'slug': 'nginx-config-generator',
  'ind': 'it',
  'base': 'nginx-config-generator.html',
  'name': 'Nginx 配置生成器',
  'desc': 'Nginx 配置生成器使用指南：按反向代理、静态站点、HTTPS 等场景生成 nginx.conf 片段。',
  'intro': 'Nginx 配置块多易错。本工具按常见场景（反向代理、静态目录、重定向、HTTPS）产出可用的 server 块。本地生成不上传。',
  'features': ['反向代理片段', '静态站点配置', '301 重定向', 'HTTPS/证书占位', '本地处理'],
  'scenarios': ['部署前端静态站', '给后端加反向代理', '配置域名重定向'],
  'steps': ['选场景填域名/端口', '点击生成', '复制 server 块'],
  'tips': ['proxy_pass 末尾斜杠注意', '静态站用 root+try_files', '改完 nginx -t 校验'],
  'faqs': [('怎么生效配置？', '保存后 nginx -s reload。'), ('能给个例子吗？', '反向代理生成 location / { proxy_pass http://127.0.0.1:3000; }。')],
  'en_name': 'Nginx Config Generator',
  'en_desc': 'Nginx Config Generator Guide: generate nginx.conf snippets for reverse proxy, static sites, HTTPS and more.',
  'en_intro': 'Nginx config has many blocks and is error-prone. This tool emits a usable server block for common cases (reverse proxy, static dir, redirect, HTTPS). Local generation, nothing uploaded.',
  'en_features': ['Reverse-proxy snippet', 'Static-site config', '301 redirect', 'HTTPS/cert placeholder', 'Local processing'],
  'en_scenarios': ['Deploy a static front-end', 'Add a reverse proxy to back-end', 'Set up domain redirect'],
  'en_steps': ['Pick a scenario, fill domain/port', 'Click generate', 'Copy the server block'],
  'en_tips': ['Mind the trailing slash on proxy_pass', 'Static sites use root + try_files', 'Run nginx -t after editing'],
  'en_faqs': [('How to apply config?', 'Save then nginx -s reload.'), ('Can you show an example?', 'Reverse proxy yields location / { proxy_pass http://127.0.0.1:3000; }.')],
 },
 {
  'slug': 'kubernetes-yaml-generator',
  'ind': 'it',
  'base': 'kubernetes-yaml-generator.html',
  'name': 'Kubernetes YAML 生成器',
  'desc': 'Kubernetes YAML 生成器使用指南：按Deployment/Service 等选项生成可用的 K8s 清单片段。',
  'intro': 'K8s 清单字段多、缩进敏感。本工具按副本数、镜像、端口、服务类型生成标准 YAML，便于 kubectl apply。本地生成不上传。',
  'features': ['生成 Deployment', '生成 Service', '设置副本与端口', 'NodePort/ClusterIP', '本地处理'],
  'scenarios': ['快速起一个服务', '教学 K8s 清单', '标准化部署模板'],
  'steps': ['填镜像与副本数', '选服务类型与端口', '点击生成复制'],
  'tips': ['缩进必须用空格', 'imagePullPolicy 设 IfNotPresent', '用 kubectl apply -f'],
  'faqs': [('Deployment 和 Service 区别？', '前者管副本，后者管访问入口。'), ('能给个例子吗？', '输出含 apiVersion/kind/metadata/spec。')],
  'en_name': 'Kubernetes YAML Generator',
  'en_desc': 'Kubernetes YAML Generator Guide: generate usable K8s manifest snippets (Deployment/Service) from simple options.',
  'en_intro': 'K8s manifests have many fields and indentation is sensitive. This tool generates standard YAML from replicas, image, ports and service type for kubectl apply. Local generation, nothing uploaded.',
  'en_features': ['Generate Deployment', 'Generate Service', 'Set replicas and ports', 'NodePort/ClusterIP', 'Local processing'],
  'en_scenarios': ['Quickly launch a service', 'Teach K8s manifests', 'Standardize deploy templates'],
  'en_steps': ['Fill image and replicas', 'Pick service type and port', 'Click generate and copy'],
  'en_tips': ['Indent with spaces only', 'Set imagePullPolicy IfNotPresent', 'Use kubectl apply -f'],
  'en_faqs': [('Deployment vs Service?', 'One manages replicas, the other the access entry.'), ('Can you show an example?', 'Output includes apiVersion/kind/metadata/spec.')],
 },
 {
  'slug': 'sitemap-generator',
  'ind': 'it',
  'base': 'sitemap-generator.html',
  'name': 'Sitemap 生成器',
  'desc': 'Sitemap 生成器使用指南：把一组 URL 生成标准 sitemap.xml，便于提交搜索引擎。',
  'intro': 'sitemap.xml 帮助爬虫发现页面。本工具输入多行 URL 与可选优先级/更新频率，生成符合协议的 XML。本地生成不上传。',
  'features': ['批量 URL 转 XML', '可选优先级/频率', '符合 sitemap 协议', '直接可提交', '本地处理'],
  'scenarios': ['新站提交索引', '整理需收录的页面', '子目录单独地图'],
  'steps': ['每行粘贴一个 URL', '选可选参数', '点击生成复制'],
  'tips': ['每行一个 URL', '大站用 Sitemap 索引', '提交到 Search Console'],
  'faqs': [('多少个 URL 合适？', '单文件上限 5 万或 50MB。'), ('能给个例子吗？', '输出含 <url><loc>...</loc></url>。')],
  'en_name': 'Sitemap Generator',
  'en_desc': 'Sitemap Generator Guide: turn a list of URLs into a standard sitemap.xml for search-engine submission.',
  'en_intro': 'sitemap.xml helps crawlers discover pages. Enter multiple URLs plus optional priority/freq and this tool emits protocol-compliant XML. Local generation, nothing uploaded.',
  'en_features': ['Batch URLs to XML', 'Optional priority/freq', 'sitemap-protocol compliant', 'Ready to submit', 'Local processing'],
  'en_scenarios': ['Submit a new site', 'Organize pages to index', 'Per-subdir map'],
  'en_steps': ['Paste one URL per line', 'Pick optional params', 'Click generate and copy'],
  'en_tips': ['One URL per line', 'Use a Sitemap index for big sites', 'Submit to Search Console'],
  'en_faqs': [('How many URLs is ok?', 'Up to 50k URLs or 50MB per file.'), ('Can you show an example?', 'Output includes <url><loc>...</loc></url>.')],
 },
 {
  'slug': 'ipv4-range-expander',
  'ind': 'it',
  'base': 'ipv4-range-expander.html',
  'name': 'IPv4 网段展开器',
  'desc': 'IPv4 网段展开器使用指南：输入 CIDR 计算网络地址、广播地址、可用主机数与首尾 IP。',
  'intro': 'CIDR（如 192.168.1.0/24）表示一段连续地址。本工具解析后给出网段关键信息，常用于子网划分与防火墙核对。本地计算不上传。',
  'features': ['CIDR 解析', '网络/广播地址', '可用主机数', '首尾可用 IP', '本地处理'],
  'scenarios': ['子网划分规划', '防火墙规则核对', '排查地址冲突'],
  'steps': ['输入 CIDR', '点击展开', '查看网段信息'],
  'tips': ['/24 有 254 个可用主机', '网络地址不可分配', '广播地址不可分配'],
  'faqs': [('/31 能用吗？', '常用于点对点链路，无可用主机范围。'), ('能给个例子吗？', '192.168.1.0/24 可用 192.168.1.1–254。')],
  'en_name': 'IPv4 Range Expander',
  'en_desc': 'IPv4 Range Expander Guide: enter a CIDR to compute network address, broadcast address, usable host count and first/last IP.',
  'en_intro': 'A CIDR like 192.168.1.0/24 denotes a contiguous block. This tool parses it into key subnet info, useful for subnetting and firewall checks. Local computation, nothing uploaded.',
  'en_features': ['CIDR parsing', 'Network/broadcast address', 'Usable host count', 'First/last usable IP', 'Local processing'],
  'en_scenarios': ['Subnet planning', 'Firewall rule check', 'Troubleshoot address conflicts'],
  'en_steps': ['Enter a CIDR', 'Click expand', 'View subnet info'],
  'en_tips': ['/24 has 254 usable hosts', 'Network address is not assignable', 'Broadcast address is not assignable'],
  'en_faqs': [('Is /31 usable?', 'Common for point-to-point links; no usable host range.'), ('Can you show an example?', '192.168.1.0/24 usable is 192.168.1.1–254.')],
 },
 {
  'slug': 'ipv6-converter',
  'ind': 'it',
  'base': 'ipv6-converter.html',
  'name': 'IPv6 转换器',
  'desc': 'IPv6 转换器使用指南：在压缩（::）与完整（8 组 16 位）形式之间互转，并拆分段。',
  'intro': 'IPv6 用冒号分隔 8 组十六进制，连续全 0 段可压缩为 ::。本工具标准化输入并给出完整展开与各段。本地解析不上传。',
  'features': ['压缩↔完整互转', '拆分为 8 段', '格式校验', '大小写规范', '本地处理'],
  'scenarios': ['核对 IPv6 地址', '填写配置表单', '教学地址结构'],
  'steps': ['输入 IPv6', '点击转换', '查看完整式与分段'],
  'tips': [':: 只能出现一次', '每组 4 位十六进制', '字母大小写均可'],
  'faqs': [('为什么用 ::？', '压缩连续全 0 段，缩短书写。'), ('能给个例子吗？', '::1 是环回地址，等同 0:0:0:0:0:0:0:1。')],
  'en_name': 'IPv6 Converter',
  'en_desc': 'IPv6 Converter Guide: convert between compressed (::) and full (8 groups of 16 bits) forms and split into segments.',
  'en_intro': 'IPv6 uses colon-separated 8 groups of hex; runs of all-zero groups compress to ::. This tool normalizes input and shows the full expansion and segments. Local parsing, nothing uploaded.',
  'en_features': ['Compressed to full both ways', 'Split into 8 segments', 'Format validation', 'Case normalization', 'Local processing'],
  'en_scenarios': ['Verify an IPv6 address', 'Fill a config form', 'Teach address structure'],
  'en_steps': ['Enter the IPv6', 'Click convert', 'View full form and segments'],
  'en_tips': [':: may appear only once', 'Each group is 4 hex digits', 'Letter case is accepted'],
  'en_faqs': [('Why use ::?', 'It compresses runs of zero groups for shorter writing.'), ('Can you show an example?', '::1 is loopback, equal to 0:0:0:0:0:0:0:1.')],
 },
 {
  'slug': 'unit-converter-advanced',
  'ind': 'it',
  'base': 'unit-converter-advanced.html',
  'name': '高级单位转换器',
  'desc': '高级单位转换器使用指南：在长度、质量、体积、温度等多类单位间批量互转，支持自定义精度。',
  'intro': '覆盖常见物理量单位（米/英尺、千克/磅、升/加仑、摄氏度/华氏度等）。本工具一次选类目与单位即得结果。本地换算不上传。',
  'features': ['多类目切换', '温度特殊换算', '批量单位', '精度可调', '本地处理'],
  'scenarios': ['跨境购物换算', '食谱单位转换', '工程数据核对'],
  'steps': ['选类目与单位', '输入数值', '查看目标结果'],
  'tips': ['温度非十进制比例', '注意英制美式差异', '小数位按需调整'],
  'faqs': [('华氏怎么算？', 'F = C×9/5 + 32。'), ('能给个例子吗？', '100 摄氏度 = 212 华氏度。')],
  'en_name': 'Advanced Unit Converter',
  'en_desc': 'Advanced Unit Converter Guide: convert across length, mass, volume, temperature and more, with adjustable precision.',
  'en_intro': 'Covers common physical units (meter/foot, kg/lb, liter/gallon, C/F). Pick a category and units and get the result. Local conversion, nothing uploaded.',
  'en_features': ['Switch categories', 'Special temperature math', 'Bulk units', 'Adjustable precision', 'Local processing'],
  'en_scenarios': ['Cross-border shopping', 'Recipe unit conversion', 'Engineering data check'],
  'en_steps': ['Pick category and units', 'Enter a value', 'View the target result'],
  'en_tips': ['Temperature is not a decimal ratio', 'Mind US vs UK imperial', 'Adjust decimals as needed'],
  'en_faqs': [('How is Fahrenheit computed?', 'F = C×9/5 + 32.'), ('Can you show an example?', '100 °C = 212 °F.')],
 },
 {
  'slug': 'date-duration',
  'ind': 'it',
  'base': 'date-duration.html',
  'name': '日期时长计算器',
  'desc': '日期时长计算器使用指南：计算两个日期之间相差的天数、周数或月数，也支持加減天数。',
  'intro': '常用于项目排期、租期、纪念日倒计时。本工具输入起止日期即得间隔，或给定日期加 N 天求结果。本地计算不上传。',
  'features': ['两日期差值', '加/减天数', '含/不含端点可选', '工作日提示', '本地处理'],
  'scenarios': ['项目工期核算', '租约/订阅周期', '纪念日倒计时'],
  'steps': ['选起止日期或基准日', '点计算', '查看间隔或结果日'],
  'tips': ['注意是否含当天', '跨月按日历天数', '时区默认本地'],
  'faqs': [('包含起始日吗？', '可切换含/不含端点。'), ('能给个例子吗？', '2026-01-01 到 2026-01-31 相差 30 天。')],
  'en_name': 'Date Duration Calculator',
  'en_desc': 'Date Duration Calculator Guide: compute days/weeks/months between two dates, or add/subtract days from a date.',
  'en_intro': 'Useful for project scheduling, leases and anniversary countdowns. Enter start/end dates for the gap, or add N days to a date. Local computation, nothing uploaded.',
  'en_features': ['Gap between two dates', 'Add/subtract days', 'Inclusive/exclusive toggle', 'Workday hint', 'Local processing'],
  'en_scenarios': ['Project duration', 'Lease/subscription period', 'Anniversary countdown'],
  'en_steps': ['Pick start/end or a base date', 'Click calculate', 'View the gap or result date'],
  'en_tips': ['Mind whether to include the start day', 'Cross-month uses calendar days', 'Timezone defaults to local'],
  'en_faqs': [('Include the start day?', 'You can toggle inclusive/exclusive ends.'), ('Can you show an example?', '2026-01-01 to 2026-01-31 is 30 days apart.')],
 },
 {
  'slug': 'lorem-ipsum-generator',
  'ind': 'text',
  'base': 'lorem-ipsum-generator.html',
  'name': 'Lorem 占位文本生成器',
  'desc': 'Lorem 占位文本生成器使用指南：生成 Lorem ipsum 段落/句子/单词，用于排版与原型设计占位。',
  'intro': '设计稿与模板常用 Lorem ipsum 占位，避免被真实内容干扰。本工具按段数/句数/字数生成，可带经典开头。本地生成不上传。',
  'features': ['按段/句/词生成', '可调长度', '经典开头开关', '纯文本输出', '本地处理'],
  'scenarios': ['网页原型占位', '设计稿排版', '文档模板示例'],
  'steps': ['选数量与单位', '点生成', '复制占位文本'],
  'tips': ['仅作占位不要当正文', '长度按需控制', '可去掉经典开头'],
  'faqs': [('Lorem ipsum 什么意思？', '源自拉丁文，无实际语义的排版占位。'), ('能给个例子吗？', '经典开头 "Lorem ipsum dolor sit amet..."。')],
  'en_name': 'Lorem Ipsum Generator',
  'en_desc': 'Lorem Ipsum Generator Guide: generate Lorem ipsum paragraphs/sentences/words for layout and prototyping placeholders.',
  'en_intro': 'Design drafts and templates use Lorem ipsum to avoid distraction from real content. Generate by paragraphs/sentences/words, optionally with the classic opener. Local generation, nothing uploaded.',
  'en_features': ['Generate by para/sentence/word', 'Adjustable length', 'Classic opener toggle', 'Plain-text output', 'Local processing'],
  'en_scenarios': ['Web prototype placeholder', 'Design layout', 'Doc template sample'],
  'en_steps': ['Pick count and unit', 'Click generate', 'Copy the placeholder text'],
  'en_tips': ['Use only as placeholder, not real text', 'Control length as needed', 'Can drop the classic opener'],
  'en_faqs': [('What does Lorem ipsum mean?', 'Latin-derived, semantically empty layout placeholder.'), ('Can you show an example?', 'Classic opener "Lorem ipsum dolor sit amet...".')],
 },
 {
  'slug': 'split-bill',
  'ind': 'accounting',
  'base': 'split-bill.html',
  'name': '分账计算器',
  'desc': '分账计算器使用指南：输入账单总额、人数与小费比例，计算每人应付及小费金额，支持均摊。',
  'intro': '聚餐、合租、团购后常需平摊费用并加小费。填入总额、人数与小费比例，即得每人应付与总小费。本地计算不上传。',
  'features': ['总额平摊', '小费按比例', '每人应付计算', '人均四舍五入', '本地处理'],
  'scenarios': ['聚餐 AA', '合租分摊', '团购费用结算'],
  'steps': ['填总额与人数', '填小费比例', '点计算看每人'],
  'tips': ['小费按当地习惯', '人数含自己', '零头协商处理'],
  'faqs': [('小费一般多少？', '常见 10%–15%，看地区。'), ('能给个例子吗？', '480 元 4 人 10% 小费，每人约 132 元。')],
  'en_name': 'Split Bill Calculator',
  'en_desc': 'Split Bill Calculator Guide: enter total, headcount and tip percentage to compute each person’s share and the tip amount.',
  'en_intro': 'After a meal, shared rent or group buy, costs are split and a tip added. Enter total, people and tip to get each person’s share and total tip. Local computation, nothing uploaded.',
  'en_features': ['Split the total', 'Tip by percentage', 'Per-person amount', 'Per-person rounding', 'Local processing'],
  'en_scenarios': ['Dinner AA', 'Shared rent split', 'Group-buy settlement'],
  'en_steps': ['Fill total and people', 'Fill tip percentage', 'Click calculate for per-person'],
  'en_tips': ['Tip by local custom', 'Headcount includes yourself', 'Settle the odd change by agreement'],
  'en_faqs': [('How much tip?', 'Commonly 10%–15%, by region.'), ('Can you show an example?', '480 yuan, 4 people, 10% tip ≈ 132 each.')],
 },
]

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title{head_title_attr}>{title}使用指南 - ToolBox</title>
<meta name="description"{head_desc_attr} content="{desc}">
<meta property="og:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description"{head_desc_attr} content="{desc}">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta name="twitter:description"{head_desc_attr} content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh-CN" href="{canonical}">
<link rel="alternate" hreflang="en-US" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{"@type":"Organization","name":"ToolBox"},"inLanguage":"zh-CN"}
</script>
<script defer src="https://chenguangwu.github.io/js/i18n.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-en-pack.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-i18n.js"></script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
header{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:780px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:6px 0;}
dl{margin:0;}
dt{font-weight:700;margin-top:12px;}
dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
footer{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides"{nav_guides}>{nav_guides_fb}使用指南</a> / <span{title_attr}>{title}</span></nav></header>
<main>
<h1{title_attr}>{title} 使用指南</h1>
<p class="lead"{intro_attr}>{intro}</p>
<h2{sec_features}>核心功能</h2>
<ul>{features}</ul>
<h2{sec_scenarios}>适用场景</h2>
<ul>{scenarios}</ul>
<h2{sec_steps}>使用步骤</h2>
<ol>{steps}</ol>
<h2{sec_tips}>实用技巧</h2>
<ul>{tips}</ul>
<h2{sec_faqs}>常见问题</h2>
<dl>{faqs}</dl>
<div class="back"><a href="{tool_url}">→ 去使用 {title}（免费 · 纯前端 · 数据不上传）</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端在线工具 · 数据不上传，安全可靠</footer>
</body>
</html>
'''

def li(items, slug, field, en_items=None):
    out = []
    for i, x in enumerate(items):
        if en_items and i < len(en_items) and en_items[i]:
            key = 'guide.%s.%s.%d' % (slug, field, i)
            out.append('<li data-i18n="%s" data-i18n-fb="%s">%s</li>'
                       % (key, html.escape(str(x)), html.escape(str(x))))
        else:
            out.append('<li>%s</li>' % html.escape(str(x)))
    return ''.join(out)

def render_faqs(g):
    out = []
    en = g.get('en_faqs')
    for i, (q, a) in enumerate(g['faqs']):
        if en and i < len(en) and en[i]:
            qk = 'guide.%s.faqs.%d.q' % (g['slug'], i)
            ak = 'guide.%s.faqs.%d.a' % (g['slug'], i)
            out.append('<dt data-i18n="%s" data-i18n-fb="%s">%s</dt><dd data-i18n="%s" data-i18n-fb="%s">%s</dd>'
                       % (qk, html.escape(q), html.escape(q), ak, html.escape(a), html.escape(a)))
        else:
            out.append('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)))
    return ''.join(out)

GUIDE_EN_PACK = {
    'guide._section.features': 'Key Features',
    'guide._section.scenarios': 'Use Cases',
    'guide._section.steps': 'How to Use',
    'guide._section.tips': 'Pro Tips',
    'guide._section.faqs': 'FAQ',
    'guide._nav.guides': 'Guides',
}

def render(g):
    fn = '%s-guide.html' % g['slug']
    canonical = '%s/guides/%s' % (SITE, fn)
    has_en = 'en_name' in g
    if has_en:
        for fld in ('name', 'desc', 'intro', 'features', 'scenarios', 'steps', 'tips', 'faqs'):
            ek = 'en_' + fld
            if ek not in g:
                continue
            if fld in ('features', 'scenarios', 'steps', 'tips'):
                for i, v in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.%s.%d' % (g['slug'], fld, i)] = v
            elif fld == 'faqs':
                for i, (q, a) in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.faqs.%d.q' % (g['slug'], i)] = q
                    GUIDE_EN_PACK['guide.%s.faqs.%d.a' % (g['slug'], i)] = a
            elif fld == 'name':
                GUIDE_EN_PACK['guide.%s.title' % g['slug']] = g[ek]
                GUIDE_EN_PACK['guide.%s.back' % g['slug']] = 'Open %s (Free · client-side · no upload)' % g[ek]
            else:
                GUIDE_EN_PACK['guide.%s.%s' % (g['slug'], fld)] = g[ek]
        title_attr = ' data-i18n="guide.%s.title" data-i18n-fb="%s 使用指南"' % (g['slug'], html.escape(g['name']))
        intro_attr = ' data-i18n="guide.%s.intro" data-i18n-fb="%s"' % (g['slug'], html.escape(g['intro']))
        nav_guides = ' data-i18n="guide._nav.guides" data-i18n-fb="'
        nav_guides_fb = ' '
        back_attr = ' data-i18n="guide.%s.back" data-i18n-fb="→ 去使用 %s（免费 · 纯前端 · 数据不上传）"' % (g['slug'], html.escape(g['name']))
        sec_features = ' data-i18n="guide._section.features" data-i18n-fb="核心功能"'
        sec_scenarios = ' data-i18n="guide._section.scenarios" data-i18n-fb="适用场景"'
        sec_steps = ' data-i18n="guide._section.steps" data-i18n-fb="使用步骤"'
        sec_tips = ' data-i18n="guide._section.tips" data-i18n-fb="实用技巧"'
        sec_faqs = ' data-i18n="guide._section.faqs" data-i18n-fb="常见问题"'
        head_title_attr = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox"' % (g['slug'], html.escape(g['name']))
        head_title_attr2 = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox" data-attr="content"' % (g['slug'], html.escape(g['name']))
        head_desc_attr = ' data-i18n-head="guide.%s.desc" data-i18n-head-fb="%s" data-attr="content"' % (g['slug'], html.escape(g['desc']))
    else:
        title_attr = intro_attr = nav_guides = nav_guides_fb = back_attr = ''
        sec_features = sec_scenarios = sec_steps = sec_tips = sec_faqs = ''
        head_title_attr = head_title_attr2 = head_desc_attr = ''
    page = (TPL
        .replace('{title}', html.escape(g['name']))
        .replace('{desc}', html.escape(g['desc']))
        .replace('{canonical}', canonical)
        .replace('{intro}', html.escape(g['intro']))
        .replace('{features}', li(g['features'], g['slug'], 'features', g.get('en_features')))
        .replace('{scenarios}', li(g['scenarios'], g['slug'], 'scenarios', g.get('en_scenarios')))
        .replace('{steps}', li(g['steps'], g['slug'], 'steps', g.get('en_steps')))
        .replace('{tips}', li(g['tips'], g['slug'], 'tips', g.get('en_tips')))
        .replace('{faqs}', render_faqs(g))
        .replace('{tool_url}', SITE + '/tools/%s/%s' % (g['ind'], g['base']))
        .replace('{home}', SITE + '/')
        .replace('{title_attr}', title_attr)
        .replace('{intro_attr}', intro_attr)
        .replace('{nav_guides}', nav_guides)
        .replace('{nav_guides_fb}', nav_guides_fb)
        .replace('{back_attr}', back_attr)
        .replace('{sec_features}', sec_features)
        .replace('{sec_scenarios}', sec_scenarios)
        .replace('{sec_steps}', sec_steps)
        .replace('{sec_tips}', sec_tips)
        .replace('{sec_faqs}', sec_faqs)
        .replace('{head_title_attr}', head_title_attr)
        .replace('{head_title_attr2}', head_title_attr2)
        .replace('{head_desc_attr}', head_desc_attr))
    return fn, page

def main():
    os.makedirs(GUIDES_DIR, exist_ok=True)
    guide_map = []
    for g in GUIDES:
        fn, page = render(g)
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': g['base'], 'guide': '../../guides/%s' % fn, 'title': g['name'] + '使用指南'})
        print('OK: guides/%s' % fn)
    export_js(GUIDE_EN_PACK)
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.exists(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（本批 +%d）' % (len(merged), len(guide_map)))
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.exists(ip):
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join(
            '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a><span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
            % (g['slug'], html.escape(g['name']), html.escape(g['desc'])) for g in GUIDES)
        if '</ul>' in s:
            s = s.replace('</ul>', new_li + '</ul>', 1)
            open(ip, 'w', encoding='utf-8').write(s)
            print('guides/index.html 追加 %d 条' % len(GUIDES))

def export_js(pack):
    path = os.path.join(ROOT, 'js', 'guide-en-pack.js')
    merged = {}
    if os.path.exists(path):
        try:
            txt = open(path, encoding='utf-8').read()
            m = txt.find('window.GUIDE_EN_PACK')
            if m >= 0:
                js_part = txt[txt.index('=', m) + 1:].strip()
                if js_part.endswith(';'):
                    js_part = js_part[:-1]
                existing = json.loads(js_part)
                if isinstance(existing, dict):
                    merged.update(existing)
        except Exception:
            pass
    merged.update(pack)
    header = "/* Auto-generated by scripts/gen_*_guides.py — merged EN dictionary for guide pages. Do not edit by hand. */\n"
    open(path, 'w', encoding='utf-8').write(header + 'window.GUIDE_EN_PACK = ' + json.dumps(merged, ensure_ascii=False, indent=2) + ';\n')
    print('js/guide-en-pack.js 字典导出 %d 条(本批 %d)' % (len(merged), len(pack)))

if __name__ == '__main__':
    main()
