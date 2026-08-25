// B5-10 指标采集浏览器验证（仅本地，不进发布产物）
const { chromium } = require('/Users/cgw/node_modules/playwright');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  // 1) 首页打开隐私弹窗，确认指标区块存在且默认关闭
  await page.goto('http://localhost:8138/index.html', { waitUntil: 'load' });
  await page.waitForTimeout(400);
  await page.click('#footerPrivacyLink');
  await page.waitForTimeout(300);
  const hasMetricsBlock = await page.$('#tb-priv-metrics-toggle') !== null;
  const optinBefore = await page.evaluate(() => localStorage.getItem('toolbox_metrics_optin'));
  console.log('privacy modal metrics block present =', hasMetricsBlock);
  console.log('optin before toggle =', optinBefore);

  // 2) 开启指标开关
  await page.click('#tb-priv-metrics-toggle');
  await page.waitForTimeout(150);
  const optinAfter = await page.evaluate(() => localStorage.getItem('toolbox_metrics_optin'));
  console.log('optin after toggle =', optinAfter);

  // 关闭弹窗
  await page.click('#tb-priv-close');
  await page.waitForTimeout(150);

  // 3) 访问一个工具页，应触发 tool_launch 事件
  await page.goto('http://localhost:8138/tools/science/calculator.html', { waitUntil: 'load' });
  await page.waitForTimeout(600);
  const events = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('toolbox_metrics_events') || '[]'); } catch (e) { return []; }
  });
  console.log('events after tool page load =', JSON.stringify(events));

  // 4) 复制按钮（若有）应触发 copy 事件
  const copyBtn = await page.$('.auto-copy-btn, button:has-text("复制")');
  if (copyBtn) {
    await copyBtn.click().catch(() => {});
    await page.waitForTimeout(200);
  }
  const events2 = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('toolbox_metrics_events') || '[]'); } catch (e) { return []; }
  });
  console.log('events after copy attempt =', JSON.stringify(events2.map(e => e.e)));

  // 5) 指标事件不含用户输入/查询内容（仅匿名字段）
  const leaked = events2.some(e => e.q || e.query || e.input || e.url || e.text || e.content);
  console.log('no PII/input fields leaked =', !leaked);

  // 6) 关闭指标后再访问不应新增事件（opt-in 强约束）
  await page.evaluate(() => { window.ToolBox.Metrics.setEnabled(false); window.ToolBox.Metrics.clear(); });
  await page.goto('http://localhost:8138/tools/it/base64.html', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  const events3 = await page.evaluate(() => {
    try { return JSON.parse(localStorage.getItem('toolbox_metrics_events') || '[]'); } catch (e) { return []; }
  });
  console.log('events when disabled =', events3.length, '(expect 0)');

  console.log('pageerrors/console-errors =', errors.length, errors.slice(0, 3));
  await browser.close();
})();
