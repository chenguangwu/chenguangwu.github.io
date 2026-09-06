#!/usr/bin/env python3
"""清理 chess 硬编码套话。

清理范围（逐页探查确认）：
  1) formula-desc 占位仅 2 页：gomoku-forbidden / xiangqi-endgame
     占位模板「本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。 工具名称：…」
     → 整块替换为真实棋类说明。
  2) opt-guide/opt-faq 通用套话仅 1 页：bridge-scoring
     「工作与生活中的相关计算与查询。」出现在 JSON-LD FAQ + opt-guide <p> + opt-faq <dd> 三处
     → 同步替换为真实桥牌场景。
  3) tool-intro 5 页（bridge-scoring/elo-rating/go-territory/gomoku-forbidden/xiangqi-endgame）简介/功能/场景均为真实棋类内容，保留不清。
  4) formula-desc bridge-scoring/elo-rating/go-territory 无块（已真实或无需），保留。
"""
import re
import sys

PLACEHOLDER_OPT = '工作与生活中的相关计算与查询。'
PLACEHOLDER_FD = '本速查内容依据权威标准与公开资料整理，供快速查阅参考；具体数值以官方最新发布为准。'

FD_REAL = {
    'gomoku-forbidden': '依据中国五子棋竞赛规则判断黑棋禁手（三三、四四、长连），落子后自动识别活三、冲四与连五，辅助规则判定、对局复核与禁手战术练习。',
    'xiangqi-endgame': '依据中国象棋规则收录一步杀、两步杀与经典江湖残局，点击展开解法步骤，演示马后炮、重炮、闷宫等常见杀法，辅助杀法学习与残局训练。',
}

BRIDGE_OPT_REAL = '适用于桥牌比赛计分与复盘：由定约阶数、花色、加倍状态与局况核算定约分、满贯/超墩/局况奖与宕墩罚分，辅助牌手核对得分、分析叫牌策略与学习计分规则。'

FILES_FD = {name: f'tools/chess/{name}.html' for name in FD_REAL}
BRIDGE_FILE = 'tools/chess/bridge-scoring.html'


def process(dry=False):
    # 1) formula-desc 占位清理
    for name, real in FD_REAL.items():
        path = FILES_FD[name]
        s = open(path, encoding='utf-8').read()
        if PLACEHOLDER_FD not in s:
            print(f'[skip] {name}: formula-desc 未找到速查占位（可能已清理）')
            continue
        new = re.sub(r'<p class="formula-desc">.*?</p>',
                     f'<p class="formula-desc">{real}</p>', s, count=1, flags=re.S)
        if dry:
            print(f'[dry] {name}: 将替换 formula-desc 占位为真实棋类说明')
        else:
            open(path, 'w', encoding='utf-8').write(new)
            print(f'[ok] {name}: formula-desc 已替换为真实棋类说明')

    # 2) bridge-scoring opt-guide/opt-faq 套话清理
    s = open(BRIDGE_FILE, encoding='utf-8').read()
    n = s.count(PLACEHOLDER_OPT)
    if n == 0:
        print(f'[skip] bridge-scoring: 未找到 opt 套话')
    else:
        new = s.replace(PLACEHOLDER_OPT, BRIDGE_OPT_REAL)
        if dry:
            print(f'[dry] bridge-scoring: 将替换 {n} 处 opt 套话（每页应 3 处）')
        else:
            open(BRIDGE_FILE, 'w', encoding='utf-8').write(new)
            print(f'[ok] bridge-scoring: 已替换 {n} 处 opt 套话为真实桥牌场景')


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    process(dry=dry)
