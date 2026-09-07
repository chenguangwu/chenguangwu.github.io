# -*- coding: utf-8 -*-
"""opt_cosmetics_content.py — 真实化 cosmetics 唯一 key assessor-67 的 content_deepdive 占位内容。

占位变体（第二十一种）：「在cosmetics场景中先确认Assessor 67口径与边界…」summary=None。
真实化：summary + 3 scenarios + 1 example(body) + 3 faqs，覆盖化妆品注册备案合规评估真实场景。
合规：补「本工具不替代监管决定/官方检测报告，以最新法规为准」免责（不覆盖 title）。
example 沿用 body 字段（与占位一致，_build.py 渲染读 body）。
"""
import json, os

PATH = 'i18n/tools/content_deepdive.json'

DATA = {
    'cosmetics/assessor-67': {
        'summary': '按《化妆品安全技术规范》等公开限值，对输入的重金属（铅/汞/砷/镉）、甲醇、微生物（菌落总数/致病菌）等检测值逐项比对，判定各项是否达标并给出整体备案/注册合规初筛结论，提示留样与报告归档。',
        'scenarios': [
            '新品备案前自筛：把第三方送检报告数值逐项比对限值，提前发现超标项、避免退审返工。',
            '工厂来料与出厂管控：对原料、半成品、成品定期检测并建立合规台账，便于批次追溯。',
            '客诉与监管应对：出现超标质疑时快速定位是哪个指标、哪批货、偏离限值多少。',
        ],
        'examples': [{'title': '普通化妆品合规初筛', 'body': '输入：铅 0.8mg/kg（限值 10）、汞 0.1mg/kg（限值 1）、甲醇 50mg/kg（限值 2000）、菌落总数 120CFU/g（限值 500）、无致病菌 → 各项达标，整体判定「可备案」，提示保留检测报告与留样。'}],
        'faqs': [
            {'q': '本工具能代替官方检测报告吗？', 'a': '不能。仅为限值比对初筛，备案须具资质机构出具的检测报告，本工具不替代第三方检验。'},
            {'q': '限值按哪个标准？', 'a': '常用《化妆品安全技术规范》（2015 版）及后续公告，具体以产品类别与最新法规为准，标准更新以官方发布为准。'},
            {'q': '初筛通过就能上市吗？', 'a': '不自筛通过即代表合规上市。仍须走完整备案/注册流程并审核资料，本工具不替代监管决定。'},
        ],
    },
}

def main():
    assert os.path.exists(PATH), PATH
    d = json.load(open(PATH, encoding='utf-8'))
    n = 0
    for k, v in DATA.items():
        assert k in d, 'key 缺失: ' + k
        d[k]['summary'] = v['summary']
        d[k]['scenarios'] = v['scenarios']
        d[k]['examples'] = v['examples']
        d[k]['faqs'] = v['faqs']
        n += 1
    json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('已真实化 %d 个 cosmetics key（含法规免责，example 用 body 字段）' % n)

if __name__ == '__main__':
    main()
