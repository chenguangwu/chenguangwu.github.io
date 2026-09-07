#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""event 批：同步行业 i18n 字典中的旧工具名 -> 新名。

- i18n/tools/event-phrases.json : 运行期 en-US 翻译字典（tool-i18n.js 加载），
  旧名键 "评估（效果/报告/改进）体系" 现已无对应可见文本，统一改为 "活动效果评估"。
- scripts/tool_desc_override.py : 未被构建引用的死字典，同步键名避免误导。
幂等可重跑。
"""
import json

OLD = '评估（效果/报告/改进）体系'
NEW = '活动效果评估'
OLD_E = 'Evaluation (Effect/Report/Improvement) System'
NEW_E = 'Event Effectiveness Assessment'

# 1) event-phrases.json
P = 'i18n/tools/event-phrases.json'
d = json.load(open(P, encoding='utf-8'))
nd = {}
for k, v in d.items():
    nk = k.replace(OLD, NEW)
    nv = v.replace(OLD_E, NEW_E) if isinstance(v, str) else v
    nd[nk] = nv
json.dump(nd, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
leftover = [k for k in nd if OLD in k] + [k for k, v in nd.items() if isinstance(v, str) and OLD_E in v]
print('event-phrases.json: leftover old keys/vals =', len(leftover))

# 2) tool_desc_override.py（纯字符串替换单行）
SP = 'scripts/tool_desc_override.py'
s = open(SP, encoding='utf-8').read()
old_line = "'%s': ('', 'Event evaluation and improvement')," % OLD
new_line = "'%s': ('', 'Event Effectiveness Assessment')," % NEW
if old_line in s:
    s = s.replace(old_line, new_line)
    open(SP, 'w', encoding='utf-8').write(s)
    print('tool_desc_override.py: updated key')
else:
    print('tool_desc_override.py: old line not found, skip')
