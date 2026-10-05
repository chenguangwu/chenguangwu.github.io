// js/i18n.js — ToolBox 多语言国际化引擎（纯前端，localStorage 持久化）
//
// 用法：
//   <script src="js/i18n.js"></script> 放在 app.js / common.js 之前
//   HTML 元素加 data-i18n="key" 翻译文本，data-i18n-ph="key" 翻译 placeholder，data-i18n-title="key" 翻译 title
//   切换语言：I18n.set('en-US') / I18n.set('zh-CN') 或点击页面右上角语言下拉
//   动态渲染行业/分类名：I18n.indName(info, key) / I18n.catName(info, key)
//
// 规范见 docs/i18n-spec.md。zh-CN 为默认；繁体页为编译期静态页面，英文保留运行时切换。
(function () {
  'use strict';

// ===== 语言注册表（LANG_REGISTRY）=====
var LANG_REGISTRY = [
  { code: 'zh-CN', label: '中文',    dir: 'ltr', fallback: null,    isDefault: true },
  { code: 'zh-TW', label: '繁體中文', dir: 'ltr', fallback: null },
  { code: 'en-US', label: 'English', dir: 'ltr', fallback: null }
];

  var FALLBACK = 'en-US';

// ===== 地区子标签 → locale 映射（navigator.language 匹配用）=====
  var REGION_MAP = {
    'zh': 'zh-CN', 'cn': 'zh-CN', 'hk': 'zh-CN', 'tw': 'zh-CN', 'mo': 'zh-CN',
    'en': 'en-US', 'us': 'en-US', 'gb': 'en-US', 'au': 'en-US', 'ca': 'en-US', 'nz': 'en-US'
  };

  // ===== 时区 → locale 兜底（纯前端无 IP 地理时的次级判定）=====
  var TIMEZONE_MAP = {
    // 目前保留 en-US/zh-CN 两语，不依赖时区兜底到其他语种
  };

  // ===== 语言包（PACKS）=====
  // zh-CN 留空 => 通过 data-i18n-fb 回退页面原始中文
  // 其余语言包可在 i18n/<code>.json 加载或由构建注入；v1 先复用 en-US 回退
  var PACKS = {
    'zh-CN': {},
    'zh-TW': {},
    'en-US': {
      // 通用 UI
      'app.name': 'ToolBox',
      'nav.search': 'Search',
      'nav.theme': 'Toggle theme',
      'nav.hot': 'Hot tools',
      'nav.recent': 'Recent',
      'nav.fav': 'Favorites',
      'nav.guide': 'User Guide',
      // index.html 顶部用的是 nav.guides（复数），与 nav.guide 并存，
      // 否则 key 不匹配会回退到中文兜底「使用指南」
      'nav.guides': 'User Guide',
      'nav.cat': 'Categories',
      // nav-menu.js 移动端抽屉用（JS 调用 T()，无 data-i18n 属性，缺失会回退中文兜底）
      'nav.menu': 'Menu',
      'nav.no_tools': 'No tools',
      'hero.eyebrow': '5000+ tools · Runs in your browser',
      'hero.title': 'Free Online Tools',
      'hero.sub': '5000+ free tools, all running locally in your browser. No sign-up, your data stays private.',
      'hero.tags': 'Popular:',
      'hero.chain': 'Tool Chains: link multiple tools, output flows into the next input',
      'tab.hot': '🔥 Hot Tools',
      'tab.all': 'All Tools',
      'tab.fav': 'Favorites',
      'tab.recent': 'Recent',
      'section.why': 'Why ToolBox',
      'section.cat': 'Categories',
      'section.hotcat': 'Popular Categories',
      'section.hottools': 'Popular Tools',
      'section.comtools': 'Common Tools',
      'section.about': 'About',
      'btn.allHot': 'All hot tools →',
      // 工具页公共框架（chrome）
      'bc.home': 'Home',
      'tool.related': '🔗 Related Tools',
      'tool.notes': '⚠️ Usage Notes & Cautions',
      'tool.copy': '📋 Copy Result',
      'tool.download': '💾 Download',
      'tool.sample': '📦 Example',
      'tool.clear': '🗑️ Clear',
      'tool.waiting': 'Waiting for input...',
      'tool.fav': 'Favorites',
      'tool.fav_add': 'Add to favorites',
      'tool.fav_remove': 'Remove favorite',
      'tool.theme_toggle': 'Toggle theme',
      'tool.guide_link': '📖 User Guide',
      'tool.copy_ok': 'Copied',
      'tool.subscript': 'Subscript',
      'tool.superscript': 'Superscript',
      'tool.result_empty': 'Result is empty',
      'tool.device_mobile': 'mobile',
      'tool.device_pc': 'desktop',
      'nav.back': '← ToolBox',
      'cat.suffix_tools': 'Tools',
      'btn.allInd': 'View all industries →',
      'search.placeholder': 'Search tools, categories or features...',
      'search.mobile': 'Search tools...',
      'search.cmdk': 'Search 5000+ tools, categories or features...',
      'cmdk.title': 'Tool Search',
      'cmdk.select': 'Select',
      'cmdk.open': 'Open',
      'cmdk.close': 'Close',
      'cmdk.pure': 'Pure frontend · Data stays in your browser',
      'common.copy': 'Copy',
      'common.use': 'Use',
      'common.all': 'All',
      'lang.switch': 'Language',
      'quality.label': 'Quality',
      'quality.A': 'Professional Tools',
      'quality.A.desc': 'Formula explanations, charts & multi-parameter calculations',
      'quality.B': 'Standard Tools',
      'quality.B.desc': 'Full interaction and calculation logic',
      'quality.C': 'Lite Tools',
      'quality.C.desc': 'Quick reference / lookup pages',
      'explore.title': '🧭 Explore Tools',
      'explore.subtitle': 'Explore 5000+ free online tools',
      'explore.hint': 'Pick a category above, or search directly · Pure frontend, your data stays local',
      'explore.hot': 'Popular Industries',
      'footer.privacy': 'Pure frontend · Data never leaves your browser',
      // common.js 的 buildUnifiedFooter() 会动态注入 footer，缺这个键会回退中文
      'footer.desc': '5000+ cross-industry pure frontend tools. Your data never leaves your browser.',
      // 移动端底部 Tab
      'tabbar.home': 'Home',
      'tabbar.cat': 'Categories',
      'tabbar.search': 'Search',
      'breadcrumb.expand': 'Expand all {n} categories',
      'breadcrumb.collapse': 'Collapse categories',
      'tabbar.hot': 'Hot',
      'tabbar.fav': 'Favorites',
      'tabbar.guides': 'Guides',
      // 功能分类
      'cat_text': 'Text', 'cat_encode': 'Encode', 'cat_convert': 'Convert',
      'cat_generate': 'Generator', 'cat_dev': 'Developer', 'cat_design': 'Design',
      'cat_image': 'Image', 'cat_math': 'Math', 'cat_validator': 'Validator',
      'cat_reference': 'Reference', 'cat_game': 'Games', 'cat_finance': 'Finance',
      'cat_calculator': 'Calculator', 'cat_health': 'Health', 'cat_engineer': 'Engineering',
      // 行业英文名（权威源 i18n/industry-en.json，全量 279 条，供 sitemap/面包屑/分类标签 EN 态消费）
      'ind_it': 'IT Development', 'ind_ai': 'AI & Artificial Intelligence', 'ind_data': 'Data Analysis',
      'ind_engineering': 'Engineering Calculation', 'ind_electronics': 'Electronics & Circuits', 'ind_finance': 'Finance & Accounting',
      'ind_biz': 'Business & Office', 'ind_marketing': 'Marketing & Promotion', 'ind_sales': 'Sales Management',
      'ind_startup': 'Startup & Entrepreneurship', 'ind_design': 'Design & Creativity', 'ind_image': 'Image Processing',
      'ind_video': 'Video Processing', 'ind_music': 'Music & Arts', 'ind_writing': 'Writing & Creation',
      'ind_life': 'Daily Life', 'ind_health': 'Health & Medical', 'ind_travel': 'Travel',
      'ind_food': 'Food & Cooking', 'ind_home': 'Home & Renovation', 'ind_edu': 'Education & Learning',
      'ind_language': 'Language & Translation', 'ind_exam': 'Exam Preparation', 'ind_history': 'History & Culture',
      'ind_literature': 'Literature & Reading', 'ind_legal': 'Law & Compliance', 'ind_science': 'Scientific Research',
      'ind_math': 'Math Calculation', 'ind_stats': 'Statistical Analysis', 'ind_medical': 'Medical Professions',
      'ind_fun': 'Games & Entertainment', 'ind_entertainment': 'Film & Entertainment', 'ind_sports': 'Sports',
      'ind_chinese': 'Chinese Culture', 'ind_yi': 'I Ching & Bagua', 'ind_fengshui': 'Feng Shui',
      'ind_fortune': 'Fortune & Divination', 'ind_agriculture': 'Agriculture & Farming', 'ind_construction': 'Construction & Real Estate',
      'ind_manufacturing': 'Manufacturing', 'ind_logistics': 'Logistics & Transport', 'ind_energy': 'Energy & Power',
      'ind_environment': 'Environmental Protection', 'ind_automotive': 'Automotive & Transport', 'ind_beauty': 'Beauty & Skincare',
      'ind_pet': 'Pet Care', 'ind_parenting': 'Parenting & Kids', 'ind_gardening': 'Gardening',
      'ind_mining': 'Mining & Metallurgy', 'ind_textile': 'Textile & Apparel', 'ind_chemical': 'Chemical & Materials',
      'ind_fishery': 'Fisheries & Aquaculture', 'ind_forestry': 'Forestry', 'ind_livestock': 'Livestock Farming',
      'ind_accessibility': 'Accessibility', 'ind_accounting': 'Accounting & Audit', 'ind_acupuncture': 'Acupuncture & Tuina',
      'ind_admin': 'Administration', 'ind_advertising': 'Advertising & Design', 'ind_aerospace': 'Aerospace',
      'ind_antiques': 'Antiques & Appraisal', 'ind_aquaculture': 'Aquaculture', 'ind_archaeology': 'Archaeology & Museology',
      'ind_archive': 'Archive Management', 'ind_astronomy': 'Astronomy', 'ind_audio': 'Audio Tools',
      'ind_auto-beauty': 'Auto Detailing', 'ind_automation': 'Industrial Automation', 'ind_baking': 'Baking & Pastry',
      'ind_ballistics': 'Ballistics & Weapons', 'ind_beekeeping': 'Beekeeping', 'ind_beneficiation': 'Ore Beneficiation & Smelting',
      'ind_blasting': 'Blasting Engineering', 'ind_bonding': 'Bonding & Sealing', 'ind_brand': 'Brand Management',
      'ind_bridge': 'Bridge Engineering', 'ind_building-material': 'Building Materials', 'ind_cable': 'Cable & Wire',
      'ind_cardiology': 'Cardiology', 'ind_casting': 'Casting Engineering', 'ind_ceramics': 'Ceramics',
      'ind_chess': 'Chess Games', 'ind_chinese-cook': 'Chinese Cooking', 'ind_civil': 'Civil Engineering',
      'ind_cleaning': 'Cleaning & Sanitation', 'ind_clinical-lab': 'Clinical Laboratory', 'ind_clinical-nursing': 'Clinical Nursing',
      'ind_cnc': 'CNC Machining', 'ind_community': 'Community Management', 'ind_consulting': 'Consulting & Advisory',
      'ind_content': 'Content Creation', 'ind_convenience': 'Convenience Store', 'ind_cosmetic-derm': 'Cosmetic Dermatology',
      'ind_cosmetics': 'Cosmetics', 'ind_customer-service': 'Customer Service', 'ind_daily-goods': 'Daily Goods',
      'ind_dailychem': 'Daily Chemicals', 'ind_dance': 'Dance & Arts', 'ind_decor': 'Interior Decoration',
      'ind_defense': 'National Defense & Military', 'ind_dentistry': 'Dentistry', 'ind_dermatology': 'Dermatology & Venereology',
      'ind_discipline': 'Rules & Regulations', 'ind_domestic': 'Domestic Services', 'ind_dyeing': 'Dyeing & Printing',
      'ind_ecommerce': 'E-commerce', 'ind_elderly': 'Elderly Care', 'ind_electrical': 'Electrical Engineering',
      'ind_embedded': 'Embedded Systems', 'ind_endocrinology': 'Endocrinology', 'ind_ent': 'ENT (Otolaryngology)',
      'ind_event': 'Event Planning', 'ind_exhibition': 'Exhibition Services', 'ind_express': 'Express & Delivery',
      'ind_film': 'Film & Cinema', 'ind_fire': 'Fire Safety', 'ind_fire-rescue': 'Fire & Rescue',
      'ind_fitness': 'Fitness & Exercise', 'ind_floral': 'Floral Design', 'ind_food-processing': 'Food Processing',
      'ind_food-safety': 'Food Safety', 'ind_food-testing': 'Food Testing', 'ind_forensic-medicine': 'Forensic Medicine',
      'ind_forex': 'Forex Trading', 'ind_fresh': 'Fresh & Cold Chain', 'ind_funeral': 'Funeral Services',
      'ind_furniture': 'Furniture Manufacturing', 'ind_futures': 'Futures Trading', 'ind_gas': 'Gas Engineering',
      'ind_gastroenterology': 'Gastroenterology', 'ind_general': 'General Engineering', 'ind_geology': 'Geology & Exploration',
      'ind_gis': 'Geographic Information Systems', 'ind_glass': 'Glass Craft', 'ind_hardware': 'Hardware & Building Materials',
      'ind_healthcare': 'Healthcare', 'ind_heattreat': 'Heat Treatment', 'ind_hematology': 'Hematology',
      'ind_hotel': 'Hotel Management', 'ind_hr': 'Human Resources', 'ind_hvac': 'HVAC (Heating, Ventilation, Air Conditioning)',
      'ind_hydraulic': 'Hydraulic Engineering', 'ind_insurance': 'Insurance Calculation', 'ind_interior': 'Interior Decoration',
      'ind_jewelry': 'Jewelry', 'ind_knowledge': 'Knowledge Management', 'ind_labor-protection': 'Labor Protection',
      'ind_landscape': 'Landscaping & Gardening', 'ind_leather': 'Leather Processing', 'ind_livestream': 'Live-stream E-commerce',
      'ind_machinery': 'Machinery Manufacturing', 'ind_martial-arts': 'Martial Arts', 'ind_mechanical': 'Mechanical Engineering',
      'ind_media': 'Media & Communication', 'ind_metallurgy': 'Metallurgy & Materials', 'ind_metalwork': 'Metalworking',
      'ind_meteorology': 'Meteorology & Weather', 'ind_mold': 'Mold Engineering', 'ind_municipal': 'Municipal Engineering',
      'ind_nephrology': 'Nephrology', 'ind_network': 'Network Technology', 'ind_neurology': 'Neurology',
      'ind_niche': 'Niche', 'ind_nutrition': 'Nutrition & Diet', 'ind_obstetrics': 'Obstetrics',
      'ind_office': 'Office & Documents', 'ind_ophthalmology': 'Ophthalmology', 'ind_optical': 'Optometry & Vision Science',
      'ind_outdoor': 'Outdoor & Sports', 'ind_packaging': 'Packaging Engineering', 'ind_paint': 'Paint & Coatings',
      'ind_paper': 'Papermaking & Printing', 'ind_pediatrics': 'Pediatrics', 'ind_pharma': 'Pharmaceutical Engineering',
      'ind_pharmacy': 'Pharmacy', 'ind_photography': 'Photography', 'ind_pipe': 'Pipeline Engineering',
      'ind_plastic': 'Plastics & Rubber', 'ind_pneumatic': 'Pneumatics & Hydraulics', 'ind_port': 'Port Engineering',
      'ind_pr': 'Public Relations', 'ind_printing': 'Printing Technology', 'ind_procurement': 'Procurement & Supply',
      'ind_project': 'Project Management', 'ind_property': 'Property Management', 'ind_psychiatry': 'Psychiatry',
      'ind_psychology': 'Psychology & Counseling', 'ind_pulmonology': 'Pulmonology', 'ind_quality': 'Quality Management',
      'ind_railway': 'Railway Engineering', 'ind_realestate': 'Real Estate', 'ind_rehabilitation': 'Rehabilitation Medicine',
      'ind_rental': 'Rental Management', 'ind_reproductive-medicine': 'Reproductive Medicine', 'ind_research': 'Research & Academia',
      'ind_rheumatology': 'Rheumatology & Immunology', 'ind_road': 'Road Engineering', 'ind_rubber': 'Rubber Products',
      'ind_safety': 'Work Safety', 'ind_securities': 'Securities Investment', 'ind_security': 'Cybersecurity',
      'ind_security-guard': 'Security Guard Services', 'ind_seismology': 'Seismology', 'ind_shipping': 'Shipping & Marine',
      'ind_sports-event': 'Sports Events', 'ind_stage': 'Stage & Performance', 'ind_steel': 'Steel & Metallurgy',
      'ind_stone': 'Stone Processing', 'ind_supplychain': 'Supply Chain', 'ind_surface': 'Surface Treatment',
      'ind_surveying': 'Surveying & Mapping', 'ind_tcm-chemistry': 'TCM Chemistry', 'ind_tcm-diagnosis': 'TCM Diagnosis',
      'ind_tcm-pharmacy': 'TCM Pharmacy', 'ind_telecom': 'Telecommunications', 'ind_timber': 'Timber Processing',
      'ind_transport': 'Transportation', 'ind_tunnel': 'Tunnel Engineering', 'ind_uiux': 'UI/UX Design',
      'ind_unitedfront': 'United Front Work', 'ind_urban': 'Urban Planning', 'ind_urology': 'Urology',
      'ind_usedcar': 'Used Cars', 'ind_valve': 'Valve Engineering', 'ind_warehouse': 'Warehouse Management',
      'ind_water': 'Water Conservancy', 'ind_wedding': 'Wedding Planning', 'ind_welding': 'Welding Engineering',
      'ind_woodwork': 'Woodworking', 'ind_yoga': 'Yoga & Meditation', 'ind_acoustics': 'Acoustics',
      'ind_audit': 'Audit & Compliance', 'ind_banking': 'Banking', 'ind_chemistry': 'Chemistry',
      'ind_dynamics': 'Dynamics', 'ind_eco': 'Eco & Environment', 'ind_economics': 'Economics',
      'ind_edu2': 'Teaching Aids', 'ind_electromagnetism': 'Electromagnetism', 'ind_encode': 'Encoding & Conversion',
      'ind_fluid': 'Fluid Mechanics', 'ind_gardening2': 'Gardening Care', 'ind_geometry': 'Geometry',
      'ind_investment': 'Investment & Wealth Management', 'ind_kids': 'Kids & Growth', 'ind_kinematics': 'Kinematics',
      'ind_legal2': 'Labor Law', 'ind_library': 'Library & Archives', 'ind_logistics2': 'Warehousing & Logistics',
      'ind_maritime': 'Maritime & Shipping', 'ind_martial': 'Martial Sports', 'ind_materials': 'Materials Science',
      'ind_medical2': 'Medical Operations', 'ind_metrology': 'Metrology', 'ind_misc': 'General Calculation',
      'ind_misc2': 'Miscellaneous Life', 'ind_museum': 'Museum & Exhibition', 'ind_nuclear': 'Nuclear Physics',
      'ind_optics': 'Optics', 'ind_pet-training': 'Pet Training', 'ind_petrochem': 'Petrochemical',
      'ind_pets': 'Pet Care', 'ind_photo': 'Photography Parameters', 'ind_photo2': 'Photo Post-processing',
      'ind_process': 'Process Control', 'ind_quantum': 'Quantum Physics', 'ind_restaurant': 'Restaurant Management',
      'ind_robotics': 'Robotics', 'ind_service': 'Customer Service', 'ind_signal': 'Signals & Systems',
      'ind_statistics': 'Statistics', 'ind_structural': 'Structural Engineering', 'ind_tax': 'Taxation',
      'ind_text': 'Text Processing', 'ind_textile2': 'Textile & Dyeing', 'ind_thermodynamics': 'Thermodynamics',
      'ind_woodworking': 'Woodcraft', 'ind_cognition': 'Cognition & Brain Training', 'ind_colorvision': 'Color Vision & Accessibility',
      // embed.html（工具嵌入开发者文档）英文词典：data-i18n-html 保留 <code>/<strong> 内联标签
      'emb.h1': '🧩 Tool Embedding API',
      'emb.intro': 'All ToolBox tools are pure front-end. You can embed any of them into your website, blog, or document via an <code>&lt;iframe&gt;</code>. All data is processed locally in the visitor’s browser.',
      'emb.tag': 'Free · No backend · Data never leaves the browser',
      'emb.s1_title': '1. Recommended: with an attribution backlink',
      'emb.s1_body': '<strong>An iframe alone does not pass SEO weight</strong> — search engines see only the iframe’s <code>src</code> and give no ranking credit to the embedding site or to us. The real value is the <strong>clickable, crawlable attribution link</strong> below the iframe. Use the complete snippet below:',
      'emb.s1_note': 'No need to copy by hand: open <strong>any tool page</strong>, expand the “Share & Embed” block at the bottom, and one-click copy code adapted to the current tool (with optional height and light/dark theme).',
      'emb.s2_title': '2. Basic embedding (minimal)',
      'emb.s2_body': 'Put any tool-page URL into an iframe (note: this bare iframe has no backlink and passes no weight):',
      'emb.s3_title': '3. Embed parameters',
      'emb.th_param': 'Parameter', 'emb.th_desc': 'Description', 'emb.th_example': 'Example',
      'emb.param_embed': 'Enables embed mode: hides the navbar, breadcrumb, privacy badge and theme button automatically',
      'emb.param_theme': 'Force theme: <code>dark</code> or <code>light</code>',
      'emb.param_accent': 'Custom theme color (hex, including #)',
      'emb.s4_title': '4. Combined example',
      'emb.s5_title': '5. Live preview',
      'emb.s5_body': 'Below is an embed preview of the “Compound Interest Calculator” (dark theme + purple accent):',
      'emb.s6_title': '6. Notes & SEO explanation',
      'emb.li1': 'The embedded page is identical to the official site; all computation runs locally on the visitor’s device — your server bears no compute load.',
      'emb.li2': 'Set a fixed height appropriate to the content (tool-page height varies with input).',
      'emb.li3': 'If blocked by the browser (X-Frame-Options), this site already allows same-origin / cross-origin iframe embedding.',
      'emb.li4': '<strong>About weight:</strong> an iframe passes no link weight — only a real <code>&lt;a href&gt;</code> on the page passes it. If you want this embed to also count as a recommendation for ToolBox, keep the attribution backlink from Section 1 (don’t add <code>rel="nofollow"</code> to it). If you’d rather not show it, removing it is completely fine — the tool still works.',
      'emb.back': '← Back to ToolBox home',
      // 首页静态/动态渲染扩展键（批次2）
      'why.sub': 'Not just another skinned tool site — a toolbox that is truly on your side',
      'why.c1_title': 'Data never leaves your browser',
      'why.c1_desc': 'All computation happens locally. No server, no upload, no data collection. Handle sensitive files with peace of mind.',
      'why.c2_title': 'Instant pure-frontend load',
      'why.c2_desc': 'No backend wait, no loading spinners. Ready on open; speed depends on your device, not the server.',
      'why.c3_title': 'No login, free forever',
      'why.c3_desc': 'No popups, no forced sign-up, no limits. Use and go. Free forever.',
      'why.c4_title': '5000+ full coverage',
      'why.c4_desc': 'From developers to daily life, 200+ niche industries in one place. No jumping between a dozen sites.',
      // about.html 全文翻译（避免中英混排）
      'about.title': 'About ToolBox',
      'about.sub': 'Not just another skinned tool site — a toolbox that is truly on your side',
      'about.why_title': 'Why ToolBox',
      'about.story_title': 'Our Philosophy',
      'about.story_p1': 'ToolBox was built on a simple belief: tools should be tools.',
      'about.story_p2': 'No sign-up for a tiny feature, no ad pop-ups, no worrying about data collection. Open the page, get the job done, close the tab — that is it. We turned 5000+ everyday utilities into pure-frontend pages that run entirely in your browser; your data never leaves your device.',
      'about.story_p3': 'From IT development, design, business office to daily life, tools across 200+ niche industries are gathered here. We also provide tool chains, user guides and category navigation to help you connect standalone tools into an efficient workflow.',
      'about.stat_tools': 'Online Tools',
      'about.stat_industries': 'Industries',
      'about.stat_upload': 'Data Uploads',
      'about.stat_free': 'Free Forever',
      'hero.badge1': 'Runs pure-frontend',
      'hero.badge2': 'Data stays in browser',
      'hero.badge3': 'No login required',
      'hero.badge4': 'Free forever',
      // 首页「分类导航」主体区块标题（home-categories.js 渲染）
      'home.cats_title': 'Categories',
      // 顶栏 Logo 副标题
      'brand.sub': 'Tools Wiki',
      'breadcrumb.nav': 'Categories',
      'ad.label': '— Sponsored —',
      'ad.taobao_title': 'Taobao Picks',
      'ad.taobao_desc': 'Curated quality goods, limited-time offers',
      'ad.taobao_cta': 'Shop now →',
      'ad.taobao_desc_m': 'Curated quality goods',
      'ad.coupon_title': 'Coupon Center',
      'ad.coupon_desc': 'Grab official subsidies, claim coupons before checkout',
      'ad.coupon_cta': 'Get coupons →',
      'foot.tool_json': 'JSON Formatter',
      'foot.tool_qr': 'QR Code Generator',
      'foot.tool_pwd': 'Password Generator',
      'foot.tool_color': 'Color Picker',
      'foot.tool_regex': 'Regex Tester',
      'foot.tool_timestamp': 'Timestamp Converter',
      'foot.sitemap': 'Sitemap',
      'foot.contact': 'Contact & Feedback',
      'foot.manage_data': 'Manage Local Data',
      'foot.about': 'About Us',
      'foot.chains': 'Tool Chains',
      'ind.view_all': 'View all {n} industries →',
      'ind.collapse': 'Collapse ↑',
      'cat.empty': 'No tools in this category',
      'common.loading': 'Loading...',
      'state.loading': 'Loading...',
      'state.load_fail': 'Load failed, please refresh and try again',
      'quality.empty': 'No tools at this quality level',
      'view.empty_recent': 'No recent tools',
      'view.empty_fav': 'No favorite tools',
      'view.empty': 'No data',
      'search.results': '🔍 Search Results',
      'search.results_truncated': 'Found {n} tools, showing the {m} most relevant',
      'search.no_match': 'No matching tools found',
      'search.no_match_hint': 'Try other keywords, or check these related tools:',
      'search.placeholder_hint': 'Type keywords to start searching',
      'search.related': 'Related Tools',
      // 搜索页（search.html）专用
      'search.title': 'Search Tools',
      'search.title_icon': '🔍 Search Tools',
      'search.breadcrumb': '/ Search Tools',
      'search.hint_prefix': 'Search all',
      'search.hint_suffix': 'free online tools',
      'search.input_ph': 'e.g. JSON formatter, QR code, BMI calculator...',
      'search.try_these': 'Try:',
      'search.failed': 'Failed to load, please refresh',
      // 工具链组合页（chains.html）专用
      'chains.title': '🧩 Tool Chains',
      'chains.breadcrumb': '/ Tool Chains',
      'chains.desc': 'Chain multiple tools into a single pipeline: each step output is filled into the next input automatically. Fully client-side, data never leaves your browser.',
      'chains.privacy': '🔒 All data is processed locally; chain state is stored in your browser localStorage.',
      'chains.done': '✅ Chain finished! To run it again, click Start below.',
      'chains.preset': '✨ Preset Chains',
      'chains.custom': '🛠️ Custom Chain',
      'chains.name_ph': 'Name this chain, e.g. My text pipeline',
      'chains.search_ph': 'Search tools to add (e.g. URL, Base64, MD5)...',
      'chains.empty': 'No steps yet — search tools above and add them in order.',
      'chains.save': '💾 Save Custom Chain',
      'chains.tip': '💡 Tip: each step is filled automatically from the previous result; if a tool input is not auto-filled, copy and paste manually.',
      'chains.start': '▶ Start',
      'chains.delete': '🗑 Delete',
      'chains.steps_suffix': 'steps',
      'chains.no_match': 'No matching tools, try other keywords',
      'chains.index_failed': 'Failed to load the search index',
      'chains.alert_name': 'Please name the chain first',
      'chains.alert_step': 'Please add at least one tool step',
      'chains.saved_head': '✅ Custom chain "',
      'chains.saved_tail': '" saved. Click Start to run it.',
      'chains.custom_prefix': 'Custom chain (',
      // 404 页专用
      'err.title': 'Page not found',
      'err.desc': 'The page may have been moved or deleted. Try searching, or pick a popular tool below.',
      'err.search_ph': 'Search tools, e.g. JSON formatter, QR code...',
      'err.search_btn': 'Search',
      'err.hint': '5000+ free online tools · Runs client-side, no upload',
      'err.suggest': 'You might be looking for',
      'err.hot_tools': 'Popular Tools',
      'err.hot_cats': 'Popular Categories',
      'err.go_home': 'Go to Home Now',
      'err.sitemap': 'View Sitemap',
      'err.moved': 'Tool has moved',
      'err.moved_hint': 'Click to open the correct page',
      'err.redirecting': 'Redirecting to the correct page...',
      'err.redirect_home': 'Redirecting to home in {n} seconds...',
      'err.redirect_go': 'Redirecting in {n} seconds...',
      'err.related': ' related tools',
      'err.view': 'Click to view',
      'err.view_all_tools': 'Browse all 5000+ tools →',
      'err.footer': 'ToolBox - 5000+ free online tool wiki · Runs client-side, no upload',
      // 全站实时下拉搜索（js/tool-search.js）
      'search.searching': 'Loading tool index…',
      'search.view_all': 'View all search results',
      // 分类落地页（tools/<ind>/index.html）页头
      'cat.tools_suffix': ' Tools',
      'cat.total_prefix': 'Total',
      'cat.total_suffix': ' free online tools',
      'cat.about_prefix': 'About "',
      'cat.about_suffix': ' Tools"',
      'cat.h_about': 'Overview',
      'cat.h_feature': 'Key Features & Use Cases',
      'cat.h_faq': 'FAQ',
      'disc.title': '⚠️ Professional Tool Disclaimer',
      'disc.body': 'Results are for reference only. Always verify with an on-site assessment and follow the applicable standards.',
      // 站点地图（sitemap.html）
      'sitemap.back': '← Back to Home',
      'sitemap.subtitle_a': 'Sitemap · ',
      'sitemap.subtitle_b': ' free online tools · updated ',
      'sitemap.count_suffix': ' tools',
      'sitemap.back_home': 'Back to Home',
      'sitemap.copyright': '© 2026 ToolBox - Free Online Tools',
      'toast.copy_success': 'Copied to clipboard',
      'toast.copy_failed': 'Copy failed, please copy manually',
      'toast.copy_prompt': 'Please copy manually:',
      'toast.copy_target_missing': 'No copyable result found',
      'toast.element_not_found': 'Element not found',
      'toast.fav_added': 'Added to favorites ❤️',
      'toast.fav_removed': 'Removed from favorites',
      'toast.reset': 'Reset',
      'toast.cleared': 'Cleared',
      'toast.history_cleared': 'History cleared',
      'toast.history_restored': 'History restored',
      'toast.history_loaded': 'History loaded',
      'toast.deleted': 'Deleted',
      'toast.saved': 'Saved',
      'toast.loaded': 'Loaded',
      'toast.empty_data': 'No data',
      'toast.needs_calculation': 'Please calculate first',
      'toast.needs_generate': 'Please generate first',
      'toast.invalid_input': 'Please enter valid input',
      'toast.empty_source': 'No content to process',
      'toast.empty_export': 'No data to export',
      'toast.empty_download': 'No downloadable content',
      'toast.export_ok': 'Exported successfully',
      'toast.export_failed': 'Export failed',
      'toast.import_ok': 'Imported successfully',
      'toast.import_failed': 'Import failed',
      'toast.empty_favorite': 'No favorites yet',
      'validate.number': 'Please enter a valid number',
      'privacy.badge_title': 'This tool runs on pure frontend. Data is processed locally and never uploaded (click to manage local data)',
      'privacy.badge_text': 'Local Mode',
      'privacy.badge_aria': 'Local data management',
      'tool.file_upload_hint': 'Please upload an image first',
      'tool.image_load_error': 'Image failed to load',
      'tool.image_load_ok': 'Image loaded',
      'ad.label_promo': '— Sponsored —',
      'ad.label': '— Advertising —',
      // aria-label 专用（EN 态读屏不应念中文）：广告轮播圆点、footer 实时数据、about 页区块
      'ad.dot1_aria': 'Ad slide 1',
      'ad.dot2_aria': 'Ad slide 2',
      'nav.back_top': 'Back to top',
      'tool.pick_time': 'Pick a time',
      'tool.result_actions': 'Result actions',
      'foot.la_widget_aria': 'ToolBox real-time visit data',
      'about.stats_aria': 'Site statistics',
      'about.ad_section_aria': 'Sponsored',
      'ad.taobao_title': 'Taobao Picks',
      'ad.taobao_desc': 'Curated quality products, limited-time offers',
      'ad.taobao_cta': 'Check it out →',
      'ad.coupon_title': 'Coupon Center',
      'ad.coupon_desc': 'Grab official subsidies, claim coupons before checkout',
      'ad.coupon_cta': 'Get coupons →',
      'ad.track_event': 'Ad click',
      'ad.fallback_text': '⭐ Bookmark ToolBox: 5000+ free tools anytime · Pure frontend · Data stays in browser',
      // 页脚友情链接（淘宝客文字广告）
      'footer.friend_link': 'Friend link: Taobao Picks',
      'footer.friend_link2': 'Coupon Center: claim official subsidies',
      'footer.friend_tip': '(orders via this link support us)',
      // 关于页面 - 支持我们（淘宝客说明）
      'about.support_title': 'Support Us',
      'about.support_p1': 'ToolBox is free forever, no login, no sign-up. We keep the project running through small Taobao affiliate commissions.',
      'about.support_p2': 'When you find something nice on Taobao, just enter through the "Taobao Picks" link on our pages — the price is identical to opening Taobao directly, you pay nothing extra. We receive a small commission from that order.',
      'about.support_p3': 'If ToolBox has helped you, this is the best support you can offer. Thanks for every smooth experience.'
    }
  };

  var KEY = 'toolbox_lang';
  var current = 'zh-CN';

  // ===== 工具函数 =====
  function isValidLang(lang) {
    for (var i = 0; i < LANG_REGISTRY.length; i++) {
      if (LANG_REGISTRY[i].code === lang) return true;
    }
    return false;
  }

  // 规范化：兼容旧调用 set('en'/'zh')，en_US→en-US，未知→null
  function normalize(lang) {
    if (!lang) return null;
    if (lang === 'en') return 'en-US';
    if (lang === 'zh') return 'zh-CN';
    lang = String(lang).replace('_', '-');
    if (isValidLang(lang)) return lang;
    var lower = lang.toLowerCase();
    if (lower === 'zh-tw' || lower === 'zh-hant-tw') return 'zh-TW';
    // 香港浏览器与旧偏好统一使用保留的台湾繁体静态版本。
    if (lower === 'zh-hk' || lower === 'zh-hant-hk') return 'zh-TW';
    var base = lang.split('-')[0].toLowerCase();
    if (REGION_MAP[base]) return REGION_MAP[base];
    return null;
  }

  // 判定语言（优先级：URL 路径(/zh-tw) > ?lang > localStorage > 浏览器/页面默认）
  // 关键约束：zh-TW 是「静态站点语言」，只能由 URL 路径 /zh-tw/ 决定。
  // 非 /zh-tw 路径的页面(localStorage 里残留的 zh-TW 或 ?lang=zh-TW)一律无效，
  // 避免从繁体页点绝对链接跳回简体根后，切换器被 localStorage 污染误显示「繁体」。
  function detect() {
    var pathLocale = localeFromPath();
    if (pathLocale) return pathLocale;
    try {
      var params = new URLSearchParams(location.search);
      var u = normalize(params.get('lang'));
      if (u && u !== 'zh-TW') return u;
    } catch (e) {}
    try {
      var s = localStorage.getItem(KEY);
      var sn = normalize(s);
      if (sn && sn !== 'zh-TW') return sn;
    } catch (e) {}
    // 中文优先：未显式指定(?lang/localStorage)时，默认跟随页面 <html lang>（中文），
    // 确保中文搜索引擎(含 Googlebot, 其渲染 locale=en-US)渲染后索引中文；
    // 仅当用户浏览器语言含中文变体时才跟随浏览器。英文真实用户可点语言按钮或带 ?lang=en 显式切换。
    var htmlLang = (document.documentElement && document.documentElement.lang || '').toLowerCase();
    var pageDefault = normalize(htmlLang) || 'zh-CN';
    var langs = (navigator.languages && navigator.languages.length)
      ? navigator.languages : [navigator.language];
    for (var i = 0; i < langs.length; i++) {
      var n = normalize(langs[i]);
      if (n === 'zh-CN') return 'zh-CN';
    }
    return pageDefault;
  }

  function get() { return current; }
  function isEnglish() { return current === 'en-US'; }
  function isStaticTraditional() { return current === 'zh-TW'; }

  function localeFromPath() {
    var path = (location.pathname || '').replace(/^\/+/, '');
    if (path === 'zh-tw' || path.indexOf('zh-tw/') === 0) return 'zh-TW';
    return null;
  }

  function sourcePath() {
    var path = (location.pathname || '').replace(/^\/+/, '');
    return path.replace(/^zh-(?:tw|hk)\/?/i, '');
  }

  function assetUrl(url) {
    if (!url || /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(url)) return url;
    var prefix = current === 'zh-TW' ? '/zh-tw' : '';
    if (!prefix) return url;
    return prefix + (url.charAt(0) === '/' ? url : '/' + url);
  }

  function routeFor(lang) {
    var path = sourcePath();
    var prefix = lang === 'zh-TW' ? '/zh-tw/' : '/';
    var target = prefix + path;
    if (!path) target = prefix;
    var query = '';
    try {
      var params = new URLSearchParams(location.search);
      params.delete('lang');
      if (lang === 'en-US') params.set('lang', 'en-US');
      var rendered = params.toString();
      query = rendered ? '?' + rendered : '';
    } catch (e) {}
    return target + query + (location.hash || '');
  }

  // ===== 繁体静态站点：站内页面链接前缀修正 =====
  // 繁体页是独立静态路径 /zh-tw/，但部分注入的导航/卡片链接写死绝对路径
  // (/tools/...、/chains.html 等，无 /zh-tw 前缀)，点击会跳回简体根。
  // 此处把所有站内「页面」链接统一加 /zh-tw 前缀；资源(/js /css /json /logo 等)不动。
  var _anchorObserver = null;
  var RES_LINK_PREFIX = /^\/(?:zh-tw|js|css|json|i18n|images?|assets?|fonts?|libs?|vendor|\.well-known|wp-)/i;
  var RES_LINK_SUFFIX = /\.(?:png|jpe?g|gif|svg|ico|webp|avif|xml|txt|json|css|js|woff2?|ttf|eot|map|pdf|zip|gz|mp4|webm|mp3|webmanifest)$/i;
  function rewriteLocaleAnchors() {
    if (!isStaticTraditional()) return;
    var links = document.querySelectorAll('a[href^="/"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href');
      if (!href || href.indexOf('/zh-tw') === 0) continue;   // 已是繁体路径
      if (RES_LINK_PREFIX.test(href) || RES_LINK_SUFFIX.test(href)) continue;  // 资源不动
      a.setAttribute('href', '/zh-tw' + href);
    }
  }
  function startAnchorObserver() {
    if (_anchorObserver || !isStaticTraditional() || !window.MutationObserver) return;
    _anchorObserver = new MutationObserver(function () { rewriteLocaleAnchors(); });
    _anchorObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  // header/footer 由 js/common.js 在 DOMContentLoaded 之后才注入，比I18n.init 晚，
  // 初次 apply() 扫不到这些节点 ⇒ 英文态下它们的 aria-label 会停留在中文。
  // 这里对新注入的 [data-i18n*] 节点做增量翻译（含 snapshotFallback 快照，
  // 保证切回中文时能复原），只在当前语言非中文时启用，避免无谓开销。
  var _i18nAttrObserver = null;
  function startI18nAttrObserver() {
    if (_i18nAttrObserver || !window.MutationObserver) return;
    var pending = false;
    _i18nAttrObserver = new MutationObserver(function (records) {
      if (current === 'zh-CN' && !isStaticTraditional()) return;
      var hit = false;
      for (var i = 0; i < records.length; i++) {
        var added = records[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if (n.matches && n.matches('[data-i18n],[data-i18n-ph],[data-i18n-title],[data-i18n-aria],[data-i18n-alt],[data-i18n-html]')) { hit = true; break; }
          if (n.querySelector && n.querySelector('[data-i18n],[data-i18n-ph],[data-i18n-title],[data-i18n-aria],[data-i18n-alt],[data-i18n-html]')) { hit = true; break; }
        }
        if (hit) break;
      }
      if (!hit || pending) return;
      pending = true;
      // 合并同一帧的多次注入
      setTimeout(function () { pending = false; try { apply(document); } catch (e) {} }, 0);
    });
    _i18nAttrObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  // 回退链解析：current -> current.fallback -> ... -> en-US
  function resolve(key, fb) {
    var seen = {};
    var l = current;
    while (l && !seen[l]) {
      seen[l] = true;
      var pack = PACKS[l];
      if (pack && pack.hasOwnProperty(key)) return pack[key];
      var reg = null;
      for (var i = 0; i < LANG_REGISTRY.length; i++) {
        if (LANG_REGISTRY[i].code === l) reg = LANG_REGISTRY[i];
      }
      l = reg ? reg.fallback : null;
    }
    return (fb == null) ? key : fb;
  }

  function t(key, fallback) { return resolve(key, fallback); }

  // 行业/分类 key -> 可读英文名兜底（general -> General，auto-beauty -> Auto Beauty，ai -> AI）
  var KEY_ACRONYMS = {
    it: 'IT', ai: 'AI', ui: 'UI', ux: 'UX', uiux: 'UI/UX', api: 'API', seo: 'SEO',
    hr: 'HR', erp: 'ERP', crm: 'CRM', oa: 'OA', pdf: 'PDF', '3d': '3D', ar: 'AR',
    vr: 'VR', id: 'ID', iot: 'IoT', sql: 'SQL', b2b: 'B2B', b2c: 'B2C', cad: 'CAD',
    cpu: 'CPU', gpu: 'GPU', css: 'CSS', html: 'HTML', js: 'JavaScript', qc: 'QC',
    qa: 'QA', sms: 'SMS', gps: 'GPS'
  };

  function keyToEn(k) {
    var parts = String(k || '').split('-');
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      if (!parts[i]) continue;
      out.push(KEY_ACRONYMS[parts[i]] || parts[i].charAt(0).toUpperCase() + parts[i].slice(1));
    }
    return out.join(' ') || String(k || '');
  }

  function indName(info, key) {
    if (!info) return '';
    if (isEnglish()) {
      if (info.en) return info.en;
      var en = t('ind_' + (key || info.key), null);
      if (en && en.indexOf('ind_') !== 0) return en;
      // 兜底不要用中文：否则英文态会出现「通用工程」这类中文残留
      var k = key || info.key;
      return k ? keyToEn(k) : (info.name || '');
    }
    return info.name || '';
  }
  function catName(info, key) {
    if (!info) return '';
    if (isEnglish()) {
      if (info.en) return info.en;
      var en = t('cat_' + (key || info.key), null);
      if (en && en.indexOf('cat_') !== 0) return en;
      var k2 = key || info.key;
      return k2 ? keyToEn(k2) : (info.name || '');
    }
    return info.name || '';
  }

  // 注册/合并一个语言包（工具页 per-industry 字典用）
  function addPack(lang, dict) {
    if (!lang || !dict) return;
    if (!PACKS[lang]) PACKS[lang] = {};
    for (var k in dict) {
      if (Object.prototype.hasOwnProperty.call(dict, k)) PACKS[lang][k] = dict[k];
    }
  }

  function applyLangAttr() {
    try {
      if (!document.documentElement) return;
      document.documentElement.lang = current;
      var reg = null;
      for (var i = 0; i < LANG_REGISTRY.length; i++) {
        if (LANG_REGISTRY[i].code === current) reg = LANG_REGISTRY[i];
      }
      document.documentElement.dir = (reg && reg.dir === 'rtl') ? 'rtl' : 'ltr';
    } catch (e) {}
  }

  // 在首次渲染前，把placeholder / title / aria-label / alt 的「原始中文」快照到 *-fb 属性。
  // 否则切到英文后，这些属性值会被改成英文；再切回中文时fallback 取到的
  // 是已被污染的英文属性值，导致中文无法恢复（与 data-i18n 缺 fb 同理）。
  // 只对缺失 *-fb 的元素补快照，已显式配置的不覆盖。
  function snapshotFallback() {
    try {
      var nodes = document.querySelectorAll('[data-i18n-ph],[data-i18n-title],[data-i18n-aria],[data-i18n-alt],[data-i18n-html]');
      for (var i = 0; i < nodes.length; i++) {
        var el = nodes[i];
        if (el.hasAttribute('data-i18n-ph') && !el.hasAttribute('data-i18n-ph-fb')) {
          el.setAttribute('data-i18n-ph-fb', el.getAttribute('placeholder') || '');
        }
        if (el.hasAttribute('data-i18n-title') && !el.hasAttribute('data-i18n-title-fb')) {
          el.setAttribute('data-i18n-title-fb', el.getAttribute('title') || '');
        }
        if (el.hasAttribute('data-i18n-aria') && !el.hasAttribute('data-i18n-aria-fb')) {
          el.setAttribute('data-i18n-aria-fb', el.getAttribute('aria-label') || '');
        }
        if (el.hasAttribute('data-i18n-alt') && !el.hasAttribute('data-i18n-alt-fb')) {
          el.setAttribute('data-i18n-alt-fb', el.getAttribute('alt') || '');
        }
        if (el.hasAttribute('data-i18n-html') && !el.hasAttribute('data-i18n-html-fb')) {
          el.setAttribute('data-i18n-html-fb', el.innerHTML);
        }
      }
    } catch (e) {}
  }

  function apply(root) {
    root = root || document;
    snapshotFallback();
    var nodes = root.querySelectorAll('[data-i18n],[data-i18n-ph],[data-i18n-title],[data-i18n-aria],[data-i18n-alt],[data-i18n-html]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.hasAttribute('data-i18n')) {
        var k = el.getAttribute('data-i18n');
        var txt = t(k, el.getAttribute('data-i18n-fb') || el.textContent);
        if (txt) el.textContent = txt;
      }
      if (el.hasAttribute('data-i18n-ph')) {
        var phKey = el.getAttribute('data-i18n-ph');
        var phFb = el.getAttribute('data-i18n-ph-fb');
        if (phFb == null) phFb = el.getAttribute('placeholder') || '';
        el.setAttribute('placeholder', t(phKey, phFb));
      }
      if (el.hasAttribute('data-i18n-title')) {
        var ttKey = el.getAttribute('data-i18n-title');
        var ttFb = el.getAttribute('data-i18n-title-fb');
        if (ttFb == null) ttFb = el.getAttribute('title') || '';
        el.setAttribute('title', t(ttKey, ttFb));
      }
      // aria-label / alt 走同一回退链：EN 态未配 key 时保留原中文，
      // 故凡是 header/footer 注入的中文 aria-label 都必须补 data-i18n-aria，否则英文态读屏仍念中文。
      if (el.hasAttribute('data-i18n-aria')) {
        var arKey = el.getAttribute('data-i18n-aria');
        var arFb = el.getAttribute('data-i18n-aria-fb');
        if (arFb == null) arFb = el.getAttribute('aria-label') || '';
        el.setAttribute('aria-label', t(arKey, arFb));
      }
      if (el.hasAttribute('data-i18n-alt')) {
        var alKey = el.getAttribute('data-i18n-alt');
        var alFb = el.getAttribute('data-i18n-alt-fb');
        if (alFb == null) alFb = el.getAttribute('alt') || '';
        el.setAttribute('alt', t(alKey, alFb));
      }
      // data-i18n-html：整段 innerHTML 替换（保留 <code>/<strong> 等内联标签），
      // 用于含内联标签的混合段落；fb 为原始中文 HTML，切回中文时复原。
      if (el.hasAttribute('data-i18n-html')) {
        var hKey = el.getAttribute('data-i18n-html');
        var hFb = el.getAttribute('data-i18n-html-fb');
        if (hFb == null) hFb = el.innerHTML;
        var hv = t(hKey, hFb);
        if (hv != null) el.innerHTML = hv;
      }
    }
    updateSwitchers();
  }

  function updateSwitchers() {
    var sels = document.querySelectorAll('.lang-switcher select');
    for (var i = 0; i < sels.length; i++) {
      if (sels[i].value !== current) sels[i].value = current;
    }
  }

  // 注入语言下拉（替代原二进制 中/EN 按钮）
  function mountSwitcher(container) {
    if (!container || container.querySelector('.lang-switcher')) return;
    var wrap = document.createElement('div');
    wrap.className = 'lang-switcher nav-icon-btn';
    wrap.style.cssText = 'display:inline-flex;align-items:center;gap:6px;padding:0 10px;';
    var flag = document.createElement('span');
    flag.className = 'lang-flag-icon';
    flag.textContent = '\uD83C\uDF10'; // 🌐
    flag.style.cssText = 'font-size:16px;pointer-events:none;';
    var sel = document.createElement('select');
    sel.setAttribute('aria-label', 'Language / 语言');
    sel.title = 'Language / 语言';
    sel.style.cssText = 'background:transparent;border:none;color:inherit;font:inherit;cursor:pointer;outline:none;appearance:none;-webkit-appearance:none;';
    for (var i = 0; i < LANG_REGISTRY.length; i++) {
      var o = document.createElement('option');
      o.value = LANG_REGISTRY[i].code;
      o.textContent = LANG_REGISTRY[i].label;
      if (LANG_REGISTRY[i].code === current) o.selected = true;
      sel.appendChild(o);
    }
    sel.onchange = function () { set(sel.value); };
    var caret = document.createElement('span');
    caret.className = 'lang-caret';
    caret.textContent = '▾';
    caret.style.cssText = 'font-size:10px;opacity:.6;pointer-events:none;';
    wrap.appendChild(flag);
    wrap.appendChild(sel);
    wrap.appendChild(caret);

    // 图标 🌐 与箭头 ▾ 是 pointer-events:none，点击会穿透到外层 div，
    // 而外层原本没有点击处理 → 表现为"点图标没反应，只能点文字"。
    // 这里统一转发：优先展开原生下拉，浏览器不支持时直接切换语言
    //（当前只有中英两语，点图标即切换符合预期）。
    wrap.style.cursor = 'pointer';
    wrap.addEventListener('click', function (e) {
      if (e.target === sel) return;   // 点 select 自身交给原生处理
      e.preventDefault();
      try {
        if (typeof sel.showPicker === 'function') { sel.showPicker(); return; }
      } catch (err) { /* 不支持则走下面兜底 */ }
      for (var i = 0; i < LANG_REGISTRY.length; i++) {
        if (LANG_REGISTRY[i].code !== current) { set(LANG_REGISTRY[i].code); break; }
      }
    });

    container.appendChild(wrap);
  }

  function autoMount() {
    var a = document.querySelector('.nav-actions');
    if (a) mountSwitcher(a);
    var m = document.querySelector('.nav-mobile-actions');
    if (m) mountSwitcher(m);
    if (!a && !m) {
      var n = document.querySelector('.nav');
      if (n) mountSwitcher(n);
    }
  }

  // 工具页标题同步（P1）：构建期已将 <title> 预渲染为英文以优化国际 SEO 首抓，
  // 中文模式切回 <meta name="title-zh"> 保存的中文标题；英文/其他模式恢复 <title> 原值。
  var _descZh = '';
  function syncTitle() {
    try {
      var titleEl = document.querySelector('title');
      if (!titleEl) return;
      if (current === 'en-US') {
        var enMeta = document.querySelector('meta[name="title-en"]');
        if (enMeta && enMeta.getAttribute('content')) {
          document.title = enMeta.getAttribute('content');
        }
      } else {
        document.title = titleEl.textContent;
      }
    } catch (e) {}
  }
  function syncDesc() {
    try {
      var descEl = document.querySelector('meta[name="description"]');
      if (!descEl) return;
      if (current === 'en-US') {
        var enMeta = document.querySelector('meta[name="desc-en"]');
        if (enMeta && enMeta.getAttribute('content')) {
          descEl.setAttribute('content', enMeta.getAttribute('content'));
        }
      } else {
        descEl.setAttribute('content', _descZh);
      }
    } catch (e) {}
    syncKeywords();
    syncOg();
  }

  // keywords meta 同步：EN 态从 keywords-en 还原英文关键词（审计会扫描 meta:keywords 残留中文）
  function syncKeywords() {
    try {
      var kwEl = document.querySelector('meta[name="keywords"]');
      if (!kwEl) return;
      if (current === 'en-US') {
        var enMeta = document.querySelector('meta[name="keywords-en"]');
        if (enMeta && enMeta.getAttribute('content')) {
          kwEl.setAttribute('content', enMeta.getAttribute('content'));
        }
      } else {
        kwEl.setAttribute('content', _kwZh);
      }
    } catch (e) {}
  }

  // og:title / og:description 同步：社交分享与部分爬虫只读 og，不读 description。
  // 构建层已为每页写入 title-en / desc-en，EN 态必须同步到 og，否则分享卡片仍是中文。
  var _ogZh = null;
  function syncOg() {
    try {
      var ogT = document.querySelector('meta[property="og:title"]');
      var ogD = document.querySelector('meta[property="og:description"]');
      if (current === 'en-US') {
        var tEn = document.querySelector('meta[name="title-en"]');
        var dEn = document.querySelector('meta[name="desc-en"]');
        if (ogT && tEn && tEn.getAttribute('content')) ogT.setAttribute('content', tEn.getAttribute('content'));
        if (ogD && dEn && dEn.getAttribute('content')) ogD.setAttribute('content', dEn.getAttribute('content'));
      } else {
        if (ogT && _ogZh && _ogZh.t) ogT.setAttribute('content', _ogZh.t);
        if (ogD && _ogZh && _ogZh.d) ogD.setAttribute('content', _ogZh.d);
      }
    } catch (e) {}
  }

  function set(lang, opts) {
    opts = opts || {};
    var nl = normalize(lang);
    if (!nl) nl = FALLBACK;
    // 台湾繁体是独立静态 URL，切换时整页导航，确保搜索引擎与无 JS 客户端都拿到繁体 HTML。
    var target = routeFor(nl);
    if ((isStaticTraditional() || nl === 'zh-TW') && target !== location.pathname + location.search + location.hash) {
      if (opts.persist !== false) {
        try { localStorage.setItem(KEY, nl); } catch (e) {}
      }
      location.assign(target);
      return;
    }
    current = nl;
    if (opts.persist !== false) {
      try { localStorage.setItem(KEY, current); } catch (e) {}
    }
    try {
      var url = new URL(location.href);
      if (current === 'zh-CN') url.searchParams.delete('lang');
      else url.searchParams.set('lang', current);
      history.replaceState(null, '', url);
    } catch (e) {}
    applyLangAttr();
    apply(document);
    syncTitle();
    syncDesc();
    // 同时在 window 与 document 上派发：工具页的语言切换监听器多挂在 document
    // （window 上派发的事件不会传播到 document），此前切语言时工具动态内容不重渲染。
    if (window.dispatchEvent) window.dispatchEvent(new Event('toolbox:langchange'));
    if (document.dispatchEvent) document.dispatchEvent(new Event('toolbox:langchange'));
  }

  var _kwZh = '';
  function init() {
    try {
      var _dEl = document.querySelector('meta[name="description"]');
      if (_dEl) _descZh = _dEl.getAttribute('content') || '';
    } catch (e) {}
    try {
      var _kEl = document.querySelector('meta[name="keywords"]');
      if (_kEl) _kwZh = _kEl.getAttribute('content') || '';
    } catch (e) {}
    // 快照 og 原始中文值：syncOg 在切回中文时需要复原（social meta 不参与 data-i18n）
    try {
      var _ot = document.querySelector('meta[property="og:title"]');
      var _od = document.querySelector('meta[property="og:description"]');
      _ogZh = {
        t: _ot ? (_ot.getAttribute('content') || '') : '',
        d: _od ? (_od.getAttribute('content') || '') : ''
      };
    } catch (e) {}
    try {
      current = detect();
    } catch (e) { current = FALLBACK; }
    applyLangAttr();
    apply(document);
    syncTitle();
    syncDesc();
    autoMount();
    loadRegionalPack();
    // 启动站内链接前缀修正的 MutationObserver：捕获 nav-menu.js 等运行时动态注入的
    // 绝对路径站内链接(/tools/...、/chains.html)，在繁体页统一加 /zh-tw 前缀，避免点击跳回简体。
    startAnchorObserver();
    startI18nAttrObserver();
    // 初始语言就绪后派发一次 toolbox:langchange：工具页常在解析期（此刻 I18n 尚未 init、
    // current 仍为默认值）就渲染了动态内容，若不补发则该内容停留在默认语言、与 ?lang/localStorage
    // 指定的语言不一致。补发后工具按当前语言重渲染（window + document 双通道，覆盖两类监听口径）。
    if (window.dispatchEvent) window.dispatchEvent(new Event('toolbox:langchange'));
    if (document.dispatchEvent) document.dispatchEvent(new Event('toolbox:langchange'));
    injectGuideI18n();
  }

  // 指南页内容区英文：仅对 /guides/ 下的指南页动态注入 js/guide-i18n.js（不污染其他页面、
  // 不修改 3409 个指南 HTML）。guide-i18n.js 自身再按 slug 二次 guard。
  function injectGuideI18n() {
    try {
      var p = location.pathname.split('/');
      var last = p[p.length - 1] || '';
      if (p.indexOf('guides') === -1) return;
      if (!last.endsWith('.html')) return;
      if (last === 'index.html' || last.endsWith('.en.html')) return;
      if (document.getElementById('guide-i18n-script')) return;
      var s = document.createElement('script');
      s.src = '/js/guide-i18n.js';
      s.defer = true;
      s.id = 'guide-i18n-script';
      document.head.appendChild(s);
    } catch (e) {}
  }

  function loadRegionalPack() {
    if (!isStaticTraditional() || !window.fetch) return;
    var file = '/i18n/locale-zh-TW.json';
    fetch(file, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (pack) {
        if (!pack) return;
        addPack(current, pack);
        apply(document);
      })
      .catch(function () { /* 静态页面的 data-i18n-fb 已是繁体，可安全回退 */ });
  }

  window.I18n = {
    get: get, set: set, t: t,
    indName: indName, catName: catName, assetUrl: assetUrl,
    apply: apply, applyLangAttr: applyLangAttr, mountSwitcher: mountSwitcher, init: init,
    addPack: addPack,
    LANG_REGISTRY: LANG_REGISTRY, detect: detect, normalize: normalize,
    FALLBACK: FALLBACK, isEnglish: isEnglish, isStaticTraditional: isStaticTraditional
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 页面加载完成后，根据 URL ?lang 参数兜底自动对齐语言。
  // 临时覆盖语义：persist:false 不写 localStorage，避免覆盖用户手动选择的语言偏好。
  function ensureLangFromQuery() {
    try {
      var params = new URLSearchParams(location.search);
      var q = normalize(params.get('lang'));
      if (q && q !== current) set(q, { persist: false });
    } catch (e) {}
  }
  function onLoad() {
    ensureLangFromQuery();
    if (isStaticTraditional()) rewriteLocaleAnchors();
  }
  if (document.readyState === 'complete') {
    onLoad();
  } else {
    window.addEventListener('load', onLoad);
  }
})();
