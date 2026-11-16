#!/usr/bin/env node
/**
 * 915 批复核失败重做的静态证据：社交尺寸页数据口径与官方核对入口。
 *
 * 判据：
 *   1) 微博客服公开说明的头像大尺寸 180×180 已落到页面数据；旧值 200×200 不再出现；
 *   2) 页面明确标注「2024-07 为社区整理快照，非平台官方发布」，不冒充官方规格表；
 *   3) 对已核对的公开说明（微博 / Instagram / YouTube）给出可追溯口径；
 *   4) 11 个平台均给出官方核对入口链接（规范变更时以平台后台为准）。
 *
 * 用法：node scripts/_verify_social_sizes_sources_915.mjs
 * 退出码：0 全通过；1 存在失败。
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FILE = path.join(ROOT, 'tools', 'marketing', 'social-media-image-sizes.html');
const html = fs.readFileSync(FILE, 'utf8');

const fails = [];
function check(cond, msg) {
  if (!cond) fails.push(msg);
}

const weiboStart = html.indexOf('weibo: {');
const weiboEnd = html.indexOf('douyin: {', weiboStart);
check(weiboStart >= 0 && weiboEnd > weiboStart, '未定位到微博数据块');
const weibo = weiboStart >= 0 && weiboEnd > weiboStart ? html.slice(weiboStart, weiboEnd) : '';
check(weibo.includes("{type:'头像', name:'头像', width: 180, height: 180, ratio: '1:1'}"),
  '微博客服口径 180×180 未落到页面数据');
check(!weibo.includes('width: 200, height: 200'), '微博数据块仍残留旧值 200×200');

check(html.includes('社区整理快照，非平台官方发布'), '未声明数据是社区整理快照（非官方规格表）');
check(html.includes('微博客服头像大尺寸 180×180'), '缺少微博客服 180×180 的已核对说明');
check(html.includes('Instagram 帮助中心图片宽度最高 1080px'), '缺少 Instagram 帮助中心的已核对说明');
check(html.includes('YouTube 帮助中心建议横幅至少 2560×1440'), '缺少 YouTube 帮助中心的已核对说明');

const official = [
  ['微信', 'https://mp.weixin.qq.com/'],
  ['微博', 'https://help.weibo.com/'],
  ['抖音', 'https://creator.douyin.com/help/contentStandard'],
  ['小红书', 'https://creator.xiaohongshu.com/'],
  ['哔哩哔哩', 'https://member.bilibili.com/platform/home'],
  ['知乎', 'https://www.zhihu.com/'],
  ['Meta', 'https://www.facebook.com/business/help/'],
  ['Instagram', 'https://help.instagram.com/1631821640426723'],
  ['X', 'https://help.x.com/'],
  ['LinkedIn', 'https://www.linkedin.com/help/linkedin'],
  ['YouTube', 'https://support.google.com/youtube/answer/10456525'],
];
for (const [name, url] of official) {
  check(html.includes(`href="${url}"`), `${name} 官方核对入口缺失：${url}`);
}

const total = 7 + official.length;
if (fails.length) {
  console.log(`社交尺寸来源证据：${total - fails.length}/${total} 通过，${fails.length} 失败`);
  for (const m of fails) console.log('  FAIL ' + m);
  process.exit(1);
}
console.log(`社交尺寸来源证据：${total}/${total} 全部通过`);
console.log('  - 微博头像对齐公开说明 180×180，旧值已清');
console.log('  - 明确 2024-07 为社区快照，列出 3 项已核对公开说明');
console.log('  - 11 个平台均给出官方核对入口');
