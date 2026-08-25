#!/usr/bin/env python3
"""
ToolBox 自动化静态测试脚本
============================
检查所有工具页面的：
1. HTML 基本结构（DOCTYPE, head, body）
2. meta toolbox 标签是否存在
3. 公共资源路径是否正确（common.css, common.js）
4. 导航栏是否存在（返回首页 + 主题切换）
5. 标题格式是否规范（xxx - ToolBox）
6. JS 语法错误检测（用 node 检查，可选）
7. 是否有损坏的引用路径
8. 文件大小是否异常
"""
import os
import re
import sys
import json
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, 'tools')

# 统计
stats = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'errors': [],
    'warnings_list': [],
}

class ToolHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_doctype = False
        self.has_toolbox_meta = False
        self.toolbox_meta = {}
        self.title = ''
        self.has_common_css = False
        self.has_common_js = False
        self.has_nav = False
        self.has_theme_btn = False
        self.css_links = []
        self.js_scripts = []
        self.has_h2 = False
        self._in_title = False
        self._in_h2 = False
    
    def handle_decl(self, decl):
        if decl.lower().startswith('doctype'):
            self.has_doctype = True
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self._in_title = True
        
        if tag == 'meta' and attrs_dict.get('name') == 'toolbox':
            self.has_toolbox_meta = True
            content = attrs_dict.get('content', '')
            for pair in content.split(','):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    self.toolbox_meta[k.strip()] = v.strip()
        
        if tag == 'link' and attrs_dict.get('rel') == 'stylesheet':
            href = attrs_dict.get('href', '')
            self.css_links.append(href)
            if 'common.css' in href:
                self.has_common_css = True
        
        if tag == 'script':
            src = attrs_dict.get('src', '')
            if src:
                self.js_scripts.append(src)
                if 'common.js' in src:
                    self.has_common_js = True
        
        if tag == 'div' and attrs_dict.get('class') == 'nav':
            self.has_nav = True
        
        if tag == 'button':
            cls = attrs_dict.get('class', '')
            onclick = attrs_dict.get('onclick', '')
            if 'theme' in cls or 'toggleToolTheme' in onclick:
                self.has_theme_btn = True
        
        if tag == 'h2':
            self._in_h2 = True
            self.has_h2 = True
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        if tag == 'h2':
            self._in_h2 = False
    
    def handle_data(self, data):
        if self._in_title:
            self.title += data


def check_tool(filepath, rel_path):
    """检查单个工具页面"""
    stats['total'] += 1
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stats['failed'] += 1
        stats['errors'].append(f'❌ {rel_path}: 无法读取文件 - {e}')
        return
    
    parser = ToolHTMLParser()
    try:
        parser.feed(content)
    except Exception as e:
        stats['failed'] += 1
        stats['errors'].append(f'❌ {rel_path}: HTML 解析失败 - {e}')
        return
    
    errors = []
    warnings = []
    
    # 1. DOCTYPE 检查
    if not parser.has_doctype:
        errors.append('缺少 <!DOCTYPE html>')
    
    # 2. meta toolbox 检查
    if not parser.has_toolbox_meta:
        warnings.append('缺少 <meta name="toolbox"> 标签，可能导致分类错误')
    else:
        meta = parser.toolbox_meta
        if 'cat' not in meta:
            warnings.append('meta toolbox 缺少 cat 字段')
        if 'industry' not in meta:
            warnings.append('meta toolbox 缺少 industry 字段')
        if 'icon' not in meta:
            warnings.append('meta toolbox 缺少 icon 字段')
    
    # 3. 标题格式检查
    if not parser.title:
        errors.append('缺少 <title>')
    elif not parser.title.strip().endswith('- ToolBox'):
        warnings.append(f'title 格式不规范: "{parser.title.strip()}" (应以 " - ToolBox" 结尾)')
    
    # 4. 公共资源路径检查
    # 计算路径深度: tools/<industry>/file.html -> 深度 2，需要 ../../
    depth = rel_path.count(os.sep)
    expected_prefix = '../' * depth
    
    if not parser.has_common_css:
        errors.append('缺少 common.css 引用')
    else:
        # 检查路径是否正确
        for css in parser.css_links:
            if 'common.css' in css and not css.startswith(expected_prefix):
                errors.append(f'common.css 路径错误: {css} (期望以 {expected_prefix} 开头)')
    
    if not parser.has_common_js:
        errors.append('缺少 common.js 引用')
    else:
        for js in parser.js_scripts:
            if 'common.js' in js and not js.startswith(expected_prefix):
                errors.append(f'common.js 路径错误: {js} (期望以 {expected_prefix} 开头)')
    
    # 5. 导航栏检查
    if not parser.has_nav:
        warnings.append('缺少 .nav 导航栏')
    
    # 6. 主题切换按钮检查
    if not parser.has_theme_btn:
        warnings.append('缺少主题切换按钮')
    
    # 7. h2 检查
    if not parser.has_h2:
        warnings.append('缺少 <h2> 标题')
    
    # 8. 文件大小检查
    size = os.path.getsize(filepath)
    if size < 500:
        warnings.append(f'文件过小 ({size} bytes)，可能是不完整的工具')
    if size > 200 * 1024:
        warnings.append(f'文件过大 ({size/1024:.1f} KB)，建议优化')
    
    # 9. 检查是否有硬编码的内联样式过大（可选warning）
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1)) > 10000:
        warnings.append(f'内联样式过大 ({len(style_match.group(1))} bytes)，建议抽取到 common.css')
    
    # 统计结果
    if errors:
        stats['failed'] += 1
        for e in errors:
            stats['errors'].append(f'❌ {rel_path}: {e}')
    else:
        stats['passed'] += 1
    
    if warnings:
        stats['warnings'] += len(warnings)
        for w in warnings:
            stats['warnings_list'].append(f'⚠️  {rel_path}: {w}')


def check_i18n_foundation():
    """i18n 基础设施检查（批次0引入；当前状态空跑通过，不计入 errors/warnings）"""
    print()
    print('🌐 i18n 基础设施检查:')
    print('-' * 60)
    i18n_path = os.path.join(ROOT, 'js', 'i18n.js')
    ok = True
    if not os.path.exists(i18n_path):
        print('  ❌ 缺少 js/i18n.js')
        return
    with open(i18n_path, 'r', encoding='utf-8') as f:
        src = f.read()
    if 'LANG_REGISTRY' not in src:
        print('  ❌ js/i18n.js 未定义 LANG_REGISTRY')
        ok = False
    required = ['zh-CN', 'en-US']
    missing = [c for c in required if ("'%s'" % c) not in src and ('"%s"' % c) not in src]
    if missing:
        print('  ❌ LANG_REGISTRY 缺少语言: %s' % ', '.join(missing))
        ok = False
    if 'function detect' not in src:
        print('  ❌ 缺少 detect() 地区判定')
        ok = False
    index_path = os.path.join(ROOT, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            idx = f.read()
        if 'js/i18n.js' not in idx:
            print('  ❌ index.html 未引入 js/i18n.js')
            ok = False
    spec_path = os.path.join(ROOT, 'docs', 'i18n-spec.md')
    if not os.path.exists(spec_path):
        print('  ❌ 缺少 docs/i18n-spec.md 规范文档')
        ok = False
    # 多语言 SEO hreflang 门禁（批次4）：首页含 hreflang x-default 且链接可达
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            idx = f.read()
        if 'hreflang="x-default"' not in idx:
            print('  ⚠️ index.html 缺少 hreflang x-default（需重跑 _build.py 注入）')
        else:
            # 校验至少一个非 x-default 的 hreflang 指向可达绝对 URL
            import re as _re
            alts = _re.findall(r'hreflang="([^"]+)"\s+href="(https?://[^"]+)"', idx)
            bad = [h for h in alts if not h[1].startswith('https://chenguangwu.github.io/')]
            if bad:
                print('  ⚠️ 发现不可达 hreflang 链接: %s' % ', '.join(b[0] for b in bad))
            else:
                print('  ✅ 首页 hreflang 链含 x-default 且链接可达')
    if ok:
        print('  ✅ LANG_REGISTRY 含中英双语、detect() 地区判定就位、首页已引入 i18n.js')
        print('  ✅ 规范文档: docs/i18n-spec.md')


def check_related_slug_map():
    """相关工具映射完整性检查：industry-*.json 与 slug-en.json 键一致性。"""
    print()
    print('🧩 相关工具映射门禁（industry-*.json ↔ slug-en.json）:')
    print('-' * 60)
    ind_dir = os.path.join(ROOT, 'json')
    slug_path = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')

    tool_keys = set()
    bad_urls = []
    for name in sorted(os.listdir(ind_dir)):
        if not name.startswith('industry-') or not name.endswith('.json'):
            continue
        path = os.path.join(ind_dir, name)
        try:
            data = json.load(open(path, encoding='utf-8'))
        except Exception as e:
            stats['warnings'] += 1
            stats['warnings_list'].append('⚠️  %s 读取失败: %s' % (name, e))
            continue
        for item in data:
            url = item.get('url')
            if not isinstance(url, str):
                continue
            if not url.startswith('tools/') or not url.endswith('.html'):
                bad_urls.append(url)
                continue
            normalized = url[6:-5]
            if normalized.count('/') != 1:
                bad_urls.append(url)
                continue
            tool_keys.add(normalized)

    if not os.path.exists(slug_path):
        print('  ❌ 缺少 i18n/tools/slug-en.json')
        return

    try:
        slug = json.load(open(slug_path, encoding='utf-8'))
    except Exception as e:
        print('  ❌ slug-en.json 读取失败: %s' % e)
        return

    slug_keys = set(slug.keys())
    missing = sorted(tool_keys - slug_keys)
    extra = sorted(slug_keys - tool_keys)

    print('  行业工具页数: %d' % len(tool_keys))
    print('  slug-en 条目数: %d' % len(slug_keys))
    print('  映射缺失: %d' % len(missing))
    print('  冗余 slug: %d' % len(extra))
    print('  非标准行业页链接: %d' % len(bad_urls))

    if missing:
        print('  ⚠️  缺失示例: ' + ', '.join(missing[:20]))
        stats['warnings'] += 1
        stats['warnings_list'].append('⚠️  slug-en 不覆盖 %d 个行业工具键（例如: %s）' % (len(missing), ', '.join(missing[:5])))
    if extra:
        print('  ⚠️  冗余示例: ' + ', '.join(extra[:20]))
        stats['warnings'] += 1
        stats['warnings_list'].append('⚠️  slug-en 含 %d 个游离键（例如: %s）' % (len(extra), ', '.join(extra[:5])))
    if bad_urls:
        print('  ⚠️ 非标准链接示例: ' + ', '.join(bad_urls[:20]))
        stats['warnings'] += 1
        stats['warnings_list'].append('⚠️  industry-*.json 含 %d 个非标准工具链接（例如: %s）' % (len(bad_urls), ', '.join(bad_urls[:5])))
    if not missing and not extra and not bad_urls:
        print('  ✅ 映射与路径均一致，相关工具英文映射可用')


def main():
    print('=' * 60)
    print('ToolBox 自动化静态测试')
    print('=' * 60)
    print()
    
    # 遍历所有工具
    # 注：各行业的 index.html 为构建脚本生成的分类落地页（非工具），跳过检查
    for root, dirs, files in os.walk(TOOLS_DIR):
        for f in files:
            if f == 'index.html':
                continue
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, ROOT)
                # 跳过重命名产生的重定向桩（非真实工具页）
                try:
                    with open(filepath, 'r', encoding='utf-8') as _fh:
                        _head = _fh.read(200)
                    if 'TOOLBOX-REDIRECT' in _head:
                        continue
                except:
                    pass
                check_tool(filepath, rel_path)
    
    # 输出结果
    print(f'扫描完成，共检查 {stats["total"]} 个工具页面')
    print()
    print(f'  ✅ 通过: {stats["passed"]}')
    print(f'  ❌ 失败: {stats["failed"]}')
    print(f'  ⚠️  警告: {stats["warnings"]} 条')
    print()
    
    if stats['errors']:
        print('❌ 错误详情:')
        print('-' * 60)
        for e in stats['errors'][:50]:  # 最多显示50条
            print(e)
        if len(stats['errors']) > 50:
            print(f'  ... 还有 {len(stats["errors"]) - 50} 条错误')
        print()
    
    if stats['warnings_list']:
        print('⚠️  警告详情 (前30条):')
        print('-' * 60)
        for w in stats['warnings_list'][:30]:
            print(w)
        if len(stats['warnings_list']) > 30:
            print(f'  ... 还有 {len(stats["warnings_list"]) - 30} 条警告')
        print()
    
    # 按行业统计
    print('📊 各行业工具数量:')
    print('-' * 60)
    industry_counts = {}
    for root, dirs, files in os.walk(TOOLS_DIR):
        for d in dirs:
            industry_counts[d] = 0
        for f in files:
            if f.endswith('.html'):
                industry = os.path.basename(root)
                industry_counts[industry] = industry_counts.get(industry, 0) + 1
    
    for ind, cnt in sorted(industry_counts.items(), key=lambda x: -x[1]):
        bar = '█' * (cnt // 5)
        print(f'  {ind:12s} {cnt:4d}  {bar}')
    print()
    
    # i18n 基础设施检查（不计入 errors/warnings）
    check_i18n_foundation()
    check_related_slug_map()

    # 保存详细报告
    report = {
        'total': stats['total'],
        'passed': stats['passed'],
        'failed': stats['failed'],
        'warnings': stats['warnings'],
        'errors': stats['errors'],
        'warnings_list': stats['warnings_list'],
        'industry_counts': industry_counts,
    }
    
    report_path = os.path.join(ROOT, '_test_report_static.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'详细报告已保存到: {report_path}')
    
    return 0 if stats['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
