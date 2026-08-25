// ============================================================================
// ToolBox 新工具批量开发编排（workflow script body）
// 关联：PLAN-TOOLS.md（候选池）· ROADMAP.md §P3-1（新工具批量开发）
// 用法：将本文件内容作为 workflow 工具的 script 参数；
//       args 传 { batches: [{ id, tools: [{slug, name, industry, cat, icon, bg, desc, spec}] }] }
//       不传 args 时回退到下方 DEFAULT_BATCHES（批次1+2 去重后的首批候选）。
// 两阶段：verify（轻量）→ develop（单模型串行）
// ============================================================================

// ---------- 默认候选（已剔除对话校验确认的重复项） ----------
const DEFAULT_BATCHES = [
  {
    id: 'batch1-common',
    tools: [
      { slug: 'html-to-markdown', name: 'HTML 转 Markdown', industry: 'it', cat: 'convert', icon: '🔁', bg: '#e3f2fd', desc: '粘贴 HTML 片段一键转为 Markdown，保留标题/列表/表格/链接/代码结构。', spec: '文本转换：h1-6/p/ul/ol/table/a/img/code 转 markdown；实时转换 + 一键复制' },
      { slug: 'significant-figures', name: '有效数字计算器', industry: 'science', cat: 'math', icon: '🔢', bg: '#e8f5e9', desc: '按四舍六入五成双规则保留有效数字，支持科学计数法。', spec: '输入数值+目标有效位数，输出舍入结果与科学计数法形式' },
      { slug: 'robots-txt-generator', name: 'Robots.txt 生成器', industry: 'it', cat: 'dev', icon: '🤖', bg: '#f3e5f5', desc: '可视化勾选 User-agent/Allow/Disallow/Sitemap 生成 robots.txt。', spec: '多规则增删，实时预览 robots.txt 文本，一键复制' },
      { slug: 'rot13-encoder', name: 'ROT13 编码器', industry: 'it', cat: 'encode', icon: '🔤', bg: '#fff3e0', desc: '字母旋转 13 位编码/解码（对称），支持批量文本。', spec: '大小写字母 ROT13 互转，非字母字符原样保留' },
    ],
  },
  {
    id: 'batch2-image-content',
    tools: [
      { slug: 'id-photo-crop', name: '证件照裁剪器', industry: 'image', cat: 'image', icon: '📸', bg: '#e0f7fa', desc: '上传照片选 1 寸/2 寸/护照规格裁剪，支持背景色替换导出 PNG。', spec: 'canvas 裁剪 + 蓝/白/红背景替换，按规格像素尺寸导出' },
      { slug: 'nine-grid-cutter', name: '九宫格切图', industry: 'image', cat: 'image', icon: '🔲', bg: '#e8eaf6', desc: '图片切成 3×3 九张，自动适配社交平台尺寸，逐张下载。', spec: 'canvas 均分 3×3，逐格导出 PNG，支持整图/单格下载' },
      { slug: 'wechat-cover-maker', name: '公众号封面生成器', industry: 'image', cat: 'image', icon: '🖼️', bg: '#fce4ec', desc: '900×383 画布：背景/渐变 + 标题排版生成公众号封面图。', spec: 'canvas 绘制 900×383，背景色/渐变 + 标题文字，导出 PNG' },
      { slug: 'xiaohongshu-counter', name: '小红书文案计数器', industry: 'marketing', cat: 'text', icon: '📕', bg: '#ffebee', desc: '统计字数/行数/话题数，提示 1000 字上限与换行规则。', spec: '实时统计字符数/行数/#话题数，emoji 单独计数，超限提示' },
      { slug: 'sensitive-word-filter', name: '敏感词检测器', industry: 'text', cat: 'text', icon: '🛡️', bg: '#f1f8e9', desc: '内置通用敏感词表 + 自定义词表，高亮标记并替换为*。', spec: '本地词表匹配，高亮 + 替换，支持导入自定义词表' },
      { slug: 'excel-formula-reference', name: 'Excel 公式速查表', industry: 'office', cat: 'reference', icon: '📊', bg: '#e0f2f1', desc: '100+ 常用 Excel 公式分类速查，含语法与示例。', spec: '分类搜索速查表（VLOOKUP/SUMIFS/INDEX-MATCH 等），含语法+示例' },
      { slug: 'loan-comparison', name: '贷款方案对比器', industry: 'finance', cat: 'finance', icon: '💰', bg: '#fff8e1', desc: '多贷款方案并列对比总利息/月供/还款曲线。', spec: '多方案并列（等额本息/等额本金/不同利率期限），对比总利息与月供' },
      { slug: 'mortgage-prepayment', name: '提前还款计算器', industry: 'finance', cat: 'finance', icon: '🏠', bg: '#efebe9', desc: '对比提前还款「缩短年限 vs 减少月供」两种模式的省息差异。', spec: '部分/全额提前还款，两种模式省息对比，含剩余本金重算' },
    ],
  },
];

const batches = (args && Array.isArray(args.batches) && args.batches.length) ? args.batches : DEFAULT_BATCHES;

// ---------- 工具页手写最小模板（SEO/JSON-LD/hreflang/相关工具由 _build.py 自动注入） ----------
function toolTemplate(t) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=${t.cat},industry=${t.industry},icon=${t.icon},bg=${t.bg}">
<meta name="description" content="${t.name} - 专为在线工具打造的纯前端工具，数据不上传，免费使用">
<title>${t.name} - ToolBox</title>
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>
</head>
<body>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ ${t.name}</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<div class="container">
  <div class="card">
    <h2>${t.icon} ${t.name}</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">${t.desc}</p>
    <!-- 在此实现工具 UI：input-row / toolbar / result-box 等 -->
  </div>
</div>
<script>
// 在此实现 ${t.spec} 的核心逻辑（纯前端，禁用网络请求）
</script>
</body>
</html>`;
}

const interGapMs = 900;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ---------- 阶段 1：重复校验（轻量模型，结构化返回） ----------
function verifyPrompt(batch) {
  const list = batch.tools.map(t => `- ${t.slug}（${t.name}）`).join('\n');
  return `你是 ToolBox 项目的工具重复校验员。项目根目录 /Users/cgw/project/cgw/chenguangwu.github.io 有 5254 个现有工具（json/tools.json + tools/ 目录）。

请对下面这批候选工具逐一判断是否与现有工具重复：
${list}

判定方法（必须实际执行，不能空想）：
1. 用 grep 在 tools/ 目录搜索候选工具的中文名关键词（如「证件照」「九宫格」「贷款对比」）
2. 对照 json/tools.json 的工具名与 file 字段
3. 功能实质相同即判 duplicate（即使名字不同）

返回 JSON：
{ "keep": ["确认为新工具、无重复的 slug..."], "duplicate": ["与现有工具重复的 slug..."] }
注意：宁可多 keep 让后续开发，也不要误删有差异化价值的新工具。`;
}

// ---------- 阶段 2：开发（单阶段串行） ----------
function devPrompt(t) {
  return `你是 ToolBox 项目的前端工具开发员。在 /Users/cgw/project/cgw/chenguangwu.github.io 工作目录下，创建新工具页面。

【项目硬约束（必须遵守）】
- 纯前端 HTML5 + 原生 ES6 JS + CSS 变量主题；禁止任何后端/API/网络请求
- 禁止引入 npm 构建工具链；只能引用已存在的公共资源

【任务】创建文件 tools/${t.industry}/${t.slug}.html，实现「${t.name}」工具：
- 功能规格：${t.spec}
- 一句话描述：${t.desc}

【文件模板（严格遵守，SEO/结构化数据/相关工具/面包屑由 _build.py 自动注入，不要手写这些）】
${toolTemplate(t)}

【关键要求】
1. <meta name="toolbox" content="cat=${t.cat},industry=${t.industry},icon=${t.icon},bg=${t.bg}"> 必须原样保留
2. 使用公共样式类：.nav .container .card .btn .btn.primary .toolbar .result-box .input-row .tool-notes
3. 使用公共方法：ToolBox.showToast() / ToolBox.copyText() / ToolBox.downloadText() / ToolBox.toggleToolTheme()
4. 主题切换按钮必须有（onclick="ToolBox.toggleToolTheme()"）
5. 工具功能代码必须真实可运行（真实计算/转换逻辑），禁止占位符或空壳
6. 移动端可用（响应式），CSS 变量优先，不硬编码颜色
7. 若需要图片处理（canvas），上传/导出均走浏览器本地 FileReader + canvas.toBlob，不上传服务器

完成后返回：文件路径 + 3 句话说明实现的功能与交互方式。`;
}

// ---------- 编排主流程 ----------
log('开始编排：' + batches.length + ' 个批次，共 ' + batches.reduce((s, b) => s + b.tools.length, 0) + ' 个候选工具');

// 阶段 1：校验（每批一个轻量 agent）
phase('verify');
const verified = await pipeline(batches, async (batch, item, i) => {
  const r = await agent(verifyPrompt(batch), {
    label: 'verify-' + batch.id,
    phase: 'verify',
    schema: {
      type: 'object',
      properties: {
        keep: { type: 'array', items: { type: 'string' } },
        duplicate: { type: 'array', items: { type: 'string' } },
      },
      required: ['keep', 'duplicate'],
    },
  });
  const keep = new Set((r && r.keep) || batch.tools.map(t => t.slug));
  const keptTools = batch.tools.filter(t => keep.has(t.slug));
  log('批次 ' + batch.id + '：校验通过 ' + keptTools.length + ' / ' + batch.tools.length);
  await sleep(interGapMs);
  return { batch, keptTools };
});

// 阶段 2：开发（每个工具单次调用，按工具顺序串行）
phase('develop');
const developed = await pipeline(verified, async (v, item, i) => {
  if (!v.keptTools.length) { log('批次 ' + v.batch.id + ' 无待开发工具，跳过'); return []; }
  // 逐个开发，降低并发，避免模型突发容量告警
  const results = [];
  for (const t of v.keptTools) {
    const r = await agent(devPrompt(t), {
      label: 'dev-' + t.slug,
      phase: 'develop',
    });
    results.push(r);
    await sleep(interGapMs);
  }
  return results;
});

// 汇总（供主 agent 随后统一跑 _build.py + 四道门禁）
return {
  candidates: batches.reduce((s, b) => s + b.tools.length, 0),
  developed: developed.reduce((s, d) => s + (d || []).filter(Boolean).length, 0),
  verified: verified.map(item => ({ batch: item.batch.id, keep: item.keptTools.length, total: item.batch.tools.length })),
  next: '由主 agent 运行 python3 _build.py 后执行 _test_static.py / _audit_links.py --check / _audit_assets.py --check 四道门禁',
};
