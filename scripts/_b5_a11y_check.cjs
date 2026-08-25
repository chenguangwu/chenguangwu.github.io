// B5-07 无障碍键盘快速校验（仅本地，不进入发布产物）
const { chromium } = require('/Users/cgw/node_modules/playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));

  await page.goto('http://localhost:8137/index.html', { waitUntil: 'load' });

  // 1) 首页图标按钮是否都有可访问名称
  const navBtns = await page.$$eval('.nav-icon-btn', els => els.map(e => ({
    label: e.getAttribute('aria-label'),
    title: e.getAttribute('title'),
    name: e.getAttribute('aria-label') || e.getAttribute('title') || e.textContent.trim()
  })));
  const missing = navBtns.filter(b => !b.label);
  console.log('nav-icon-btn count =', navBtns.length);
  console.log('nav-icon-btn missing aria-label =', missing.length);
  navBtns.forEach(b => console.log('  -', JSON.stringify(b)));

  // 2) 键盘 Tab 能否聚焦主题/收藏类按钮（焦点环用 focus-visible，仅校验可聚焦+有名称）
  await page.keyboard.press('Tab');
  let focusedName = 'none';
  for (let i = 0; i < 12; i++) {
    const info = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return null;
      const name = el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent.trim();
      return { tag: el.tagName, name: name };
    });
    if (info && /主题|热门|最近|收藏|搜索/.test(info.name || '')) { focusedName = info.name; break; }
    await page.keyboard.press('Tab');
  }
  console.log('reached icon button by Tab =', focusedName);

  // 3) 命令面板键盘可用（Ctrl+K 打开，Esc 关闭）—— 可见性由 .open 类控制
  await page.keyboard.press('Control+K');
  await page.waitForTimeout(200);
  const cmdVisible = await page.evaluate(() => {
    const o = document.getElementById('cmdkOverlay');
    return !!o && o.classList.contains('open');
  });
  console.log('cmdk opens via Ctrl+K =', cmdVisible);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(150);
  const cmdClosed = await page.evaluate(() => {
    const o = document.getElementById('cmdkOverlay');
    return !o || !o.classList.contains('open');
  });
  console.log('cmdk closes via Esc =', cmdClosed);

  // 4) 工具页主题按钮可访问名称（取一个工具页）
  await page.goto('http://localhost:8137/tools/science/calculator.html', { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const themeA11y = await page.$eval('.theme-btn', el => ({
    label: el.getAttribute('aria-label'),
    title: el.getAttribute('title')
  })).catch(() => null);
  console.log('tool page .theme-btn a11y =', JSON.stringify(themeA11y));

  console.log('pageerrors =', errors.length, errors);
  await browser.close();
})();
