// 游戏介绍页真机验证：tools/fun/jimao-3a-game.html + games/ 游戏文件。
// 校验：介绍页结构/版权声明/新窗口跳转 href 指向真实游戏文件；游戏文件未被 build 注入篡改（MD5）。
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'fs';
import { createHash } from 'crypto';
import { execFileSync } from 'child_process';

const ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io';
const GAME_REL = '/games/%E5%87%A0%E7%8C%AB%E5%9B%BD%E4%BA%A73A%E5%A4%A7%E4%BD%9C_V1.html';
const EXPECTED_MD5 = '63c937aeec2e0989e10901d327749dd0';
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' :: ' + String(detail).slice(0, 200) : '')); }
}

function main() {
  const html = readFileSync(`${ROOT}/tools/fun/jimao-3a-game.html`, 'utf8');
  let jsErr = '';
  const vc = new VirtualConsole();
  vc.on('jsdomError', e => { jsErr += String(e.message).slice(0, 200) + ' | '; });
  const dom = new JSDOM(html, {
    url: 'https://x.test/tools/fun/jimao-3a-game.html', runScripts: 'outside-only',
    pretendToBeVisual: true, virtualConsole: vc,
  });
  const doc = dom.window.document;
  check('介绍页加载无异常', jsErr === '', jsErr);
  check('标题正确', /几猫 3A 大作/.test(doc.title), doc.title);
  check('含 meta toolbox cat=game', /cat=game,industry=fun/.test(doc.querySelector('meta[name=toolbox]')?.content || ''));

  const cta = [...doc.querySelectorAll('a')].find(a => /开始试玩/.test(a.textContent || ''));
  check('存在开始试玩按钮', !!cta);
  check('按钮 target=_blank（新窗口）', cta?.getAttribute('target') === '_blank', cta?.getAttribute('target'));
  check('按钮带 noopener noreferrer', /noopener/.test(cta?.getAttribute('rel') || '') && /noreferrer/.test(cta?.getAttribute('rel') || ''), cta?.getAttribute('rel'));
  check('按钮 href 指向 games 游戏文件', cta?.getAttribute('href') === GAME_REL, cta?.getAttribute('href'));

  const body = doc.body.textContent || '';
  check('含版权声明', /版权与免责声明/.test(body));
  check('声明版权归原作者', /归原作者或原权利人所有/.test(body));
  check('声明本站不主张权利', /不主张对该游戏享有任何权利/.test(body));
  check('声明仅供试玩学习/非商业', /个人试玩与学习交流/.test(body) && /请勿用于任何商业用途/.test(body));
  check('含侵权联系处理说明', /存在侵权/.test(body) && /核实后及时处理/.test(body));
  check('介绍玩法/操作', /游戏简介/.test(body) && /玩法特色/.test(body) && /基本操作/.test(body));

  // 游戏文件：存在、MD5 与移动前一致、未被 build 注入统计/安全脚本
  const gamePath = `${ROOT}/games/几猫国产3A大作_V1.html`;
  const game = readFileSync(gamePath);
  const md5 = createHash('md5').update(game).digest('hex');
  check('游戏文件存在', game.length > 1000000, game.length);
  check('游戏文件 MD5 未变（内容零改动）', md5 === EXPECTED_MD5, md5);
  const gs = game.toString('utf8');
  check('游戏文件未被注入 ttzz 统计', !/lf1-cdn-tos\.bytegoofy\.com/.test(gs));
  check('游戏文件未被注入 secmeta', !/X-Content-Type-Options/.test(gs));

  // 索引注册
  const toolsJson = JSON.parse(readFileSync(`${ROOT}/json/tools.json`, 'utf8'));
  check('tools.json 已注册介绍页', toolsJson.some(t => t.url === 'tools/fun/jimao-3a-game.html'));
  const sitemap = readFileSync(`${ROOT}/sitemap.xml`, 'utf8');
  check('sitemap 已含介绍页', sitemap.includes('tools/fun/jimao-3a-game.html'));
  const funIdx = JSON.parse(readFileSync(`${ROOT}/i18n/tools/en/fun/_index.json`, 'utf8'));
  check('英文索引已含新 slug', funIdx.tools.includes('jimao-3a-game'));

  console.log(`\nGAME_INTRO ${fail === 0 ? 'ALL PASS' : 'FAILED'} | ${pass + fail} checks | pass=${pass} fail=${fail}`);
  if (fail) process.exitCode = 1;
}
main();
