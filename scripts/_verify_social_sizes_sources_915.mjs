#!/usr/bin/env node
// 专项：逐条核对来源性质、链接、筛选与导出共用口径。
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html = fs.readFileSync('tools/marketing/social-media-image-sizes.html', 'utf8');
const dataText = html.match(/const platformData = (\{[\s\S]*?\n\});\n\nlet currentPlatform/);
assert.ok(dataText, 'platformData 缺失');
const data = vm.runInNewContext('(' + dataText[1] + ')');
const items = [
  ['weibo', '头像', 100, 100, 'kefu.weibo.com/faqdetail?id=20908', '生成'],
  ['twitter', '头像', 400, 400, 'help.x.com/en/managing-your-account/how-to-customize-your-profile', '推荐'],
  ['twitter', '横幅图片', 1500, 500, 'help.x.com/en/managing-your-account/how-to-customize-your-profile', '推荐'],
  ['linkedin', '个人头像', 400, 400, 'linkedin.com/help/linkedin/answer/a549049', '最小'],
  ['linkedin', '背景图片', 1584, 396, 'linkedin.com/help/linkedin/answer/a568217', '推荐'],
  ['linkedin', '单图广告', 1200, 628, 'single-image-ads/specs', '推荐'],
  ['linkedin', '轮播卡片', 1080, 1080, 'carousel-ads/specs', '至少'],
  ['youtube', '频道封面', 2560, 1440, 'answer/10456525', '推荐'],
  ['youtube', '视频缩略图', 3840, 2160, 'answer/72431', '推荐'],
];
for (const [platform, name, width, height, url, nature] of items) {
  const item = data[platform].sizes.find(x => x.name === name);
  assert.ok(item, platform + ' ' + name);
  assert.equal(item.width, width); assert.equal(item.height, height);
  assert.ok(item.source.includes(url)); assert.ok(item.noteZh.includes(nature));
  assert.ok(item.noteEn && item.noteZh.includes('2026-11-18') && item.noteEn.includes('2026-11-18'));
}
for (const p of Object.values(data)) for (const item of p.sizes) {
  if (item.source) assert.ok(item.sourceText && item.noteZh && item.noteEn, item.name);
}
for (const text of ['社区快照，此项未核验', 'Community snapshot; this item has not been verified', 'sizeSourceHtml(s,', 'sizeSourceText(s,', 's.source ? \' · \' + s.source']) assert.ok(html.includes(text), text);
for (const name of ['竖版帖子', '横版帖子']) assert.ok(data.instagram.sizes.find(s => s.name === name).noteZh.includes('未核验'));
console.log(`社媒尺寸来源专项：${items.length} 条官方口径及未核验、展示和导出标识通过`);
