#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

(async () => {
  const page = fs.readFileSync(path.join(__dirname, '../tools/tcm-diagnosis/ten-questions.html'), 'utf8');
  const script = page.match(/var questions=\[[\s\S]*?renderQuestionnaire\(\);[\s\S]*?<\/script>/)[0].replace(/<\/script>$/, '');
  const dom = new JSDOM(page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ''), { runScripts: 'dangerously', url: 'https://example.test/' });
  const { window } = dom;
  let toasts = 0;
  window.ToolBox = { showToast: () => { toasts++; } };
  window.i18nText = () => '';
  window.eval(script);
  const doc = window.document;
  const input = (el, value) => { el.value = value; el.dispatchEvent(new window.Event('input', { bubbles: true })); };
  input(doc.getElementById('pName'), '测试患者');
  await new Promise(resolve => setTimeout(resolve, 350));
  assert(doc.getElementById('result').textContent.includes('测试患者'), '输入姓名后应实时生成问诊记录');
  assert.strictEqual(toasts, 0, '实时生成不应弹窗');
  input(doc.getElementById('head'), '头痛');
  await new Promise(resolve => setTimeout(resolve, 350));
  assert(doc.getElementById('result').textContent.includes('头痛'), '问诊字段应实时更新');
  const radio = doc.querySelector('[data-id="hanre_type"] input');
  radio.checked = true;
  radio.dispatchEvent(new window.Event('change', { bubbles: true }));
  await new Promise(resolve => setTimeout(resolve, 350));
  assert(doc.getElementById('result').textContent.includes('无寒热'), '选择选项应实时更新');
  assert.strictEqual(window.localStorage.length, 0, '实时生成不得保存病例');
  input(doc.getElementById('pName'), '待清空');
  window.resetForm();
  await new Promise(resolve => setTimeout(resolve, 350));
  assert(doc.getElementById('result').textContent.includes('填写问诊内容后点击'), '重置后待执行的实时生成不得覆盖提示');
  window.generate();
  assert.strictEqual(toasts, 2, '手动生成仍应提示');
  console.log('PASS 问诊实时生成、选项、隐私及重置');
  window.close();
})().catch(err => { console.error(err); process.exitCode = 1; });
