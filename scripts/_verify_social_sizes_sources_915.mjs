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
  ['twitter', '带应用按钮图片广告', 800, 418, 'help.x.com/en/business-and-advertising/creative-ad-specifications', '推荐'],
  ['twitter', '横幅图片', 1500, 500, 'help.x.com/en/managing-your-account/how-to-customize-your-profile', '推荐'],
  ['linkedin', '个人头像', 400, 400, 'linkedin.com/help/linkedin/answer/a549049', '最小'],
  ['linkedin', '背景图片', 1584, 396, 'linkedin.com/help/linkedin/answer/a568217', '推荐'],
  ['linkedin', '主页帖子链接预览图', 1200, 627, 'linkedin.com/help/lms/answer/a567368', '建议'],
  ['linkedin', '单图广告', 1200, 628, 'single-image-ads/specs', '推荐'],
  ['linkedin', '轮播卡片', 1080, 1080, 'carousel-ads/specs', '至少'],
  ['bilibili', '课堂横版课程封面', 1146, 717, 'bilibili.com/cheese/cooperate/help', '至少'],
  ['youtube', '视频广告缩略图', 1280, 720, 'answer/13547298', '推荐'],
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
assert.deepEqual(Object.keys(data).sort(), ['bilibili', 'linkedin', 'twitter', 'weibo', 'youtube']);
const all = Object.values(data).flatMap(p => p.sizes);
assert.equal(all.length, items.length, '只保留逐项核实的尺寸');
for (const item of all) {
  assert.ok(item.source && item.sourceText && item.noteZh && item.noteEn, item.name);
  assert.doesNotMatch(item.noteZh, /未核验|社区快照/);
  assert.doesNotMatch(item.noteEn, /unverified|community snapshot/i);
}
for (const text of ['sizeSourceHtml(s,', 'sizeSourceText(s,', "s.source ? ' · ' + s.source"]) assert.ok(html.includes(text), text);
assert.doesNotMatch(html, /社区快照|像素尺寸未核验/);
console.log(`社媒尺寸来源专项：${items.length} 条官方口径、展示和导出标识通过`);
