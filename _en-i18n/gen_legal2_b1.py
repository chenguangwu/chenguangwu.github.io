#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'legal2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'legal2')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
# 与 gardening2/pruning-time 同类：术语内链（法条引用 / 高频词）被 per-tool 字典译掉后，
# 同一元素剩下的「：…」碎片脱离了行业 phrases 整串匹配，变残留。补进 EXTRA 兜底。
# ⚠️ 只补「该元素内 <strong> 标签已在 per-tool 字典里」的碎片；若 <strong> 本身没译
# （如 contract-dates 的 生效日/终止日），补碎片反而会让 phrases 整串失配、
# 把 <strong> 暴露成新残留 —— 那种情况交给 phrases 整节点命中，不要动。
EXTRA = {
    'keyword-extract': {
        '：识别《XX法》第X条等法条引用。':
            ': recognizes statutory citations such as Article X of the Law on XX.',
        '：统计文书中的高频实词（2字以上）。':
            ': counts frequent content words in the document (2 characters or more).',
        '：内置常见法律术语词典匹配，如违约、诉讼、判决、管辖等。':
            ': matches against a built-in dictionary of common legal terms, such as breach, litigation, judgment and jurisdiction.',
        '：识别「原告XX」「被告XX」「甲方XX」等主体称谓。':
            ': recognizes designations of parties such as Plaintiff XX, Defendant XX and Party A XX.',
    },
}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'legal2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('compensation-n1', build('compensation-n1', [
        '⚖️ N+1 Compensation Calculator',
        'Calculates severance compensation for terminating or ending a labor contract under the Labor Contract Law (N and N+1), supporting the monthly wage cap and personal income tax estimation.',
        'Core formula (by input variables): (leaveDate.getFullYear() - hireDate.getFullYear()) × 12 + (leaveDate.getMonth() - hireDate.getMonth()); 36000 × 0.03 + 108000 × 0.1 + 156000 × 0.2 + (taxableIncome - 300000) × 0.25; 36000 × 0.03 + 108000 × 0.1 + (taxableIncome - 144000) × 0.2',
        '/ N+1 Compensation',
        '📖 View the guide to N+1 compensation calculation',
        'Termination by mutual agreement / no-fault termination (N+1)',
        'Economic redundancy / contract not renewed on expiry (N)',
        'Unlawful termination (2N)',
        'Less than 6 months counts as half a month’s wage',
        '📚 In-depth: N+1 compensation calculation',
        'Mutual termination scenario: the employee joined on 2019-01-15 and leaves on 2022-09-10, with 3 years and 8 months of service; the average monthly wage over the 12 months before leaving is 15,000 CNY, and three times the local average monthly wage of the previous year is 30,000 CNY (so no cap applies). Years of service N = 4, N+1 compensation = 5 × 15,000 = 75,000 CNY, which is within the tax-free allowance and is received in full.',
        'High-income cap scenario: the employee has 12 years and 1 month of service with a monthly wage of 50,000 CNY, while the local three-times cap is 30,000 CNY. Since the wage exceeds three times the average, it is counted as 30,000, and the years are capped at 12, so N = 12 and N+1 compensation = 13 × 30,000 = 390,000 CNY; the part above the tax-free allowance of 30,000 CNY is subject to personal income tax of about 900 CNY.',
        'Unlawful termination 2N scenario: for the same high-income employee, if the employer terminates the contract unlawfully, compensation is twice the economic compensation standard: 2N = 2 × 12 × 30,000 = 720,000 CNY, with estimated tax of about 58,080 CNY and a net amount of about 661,920 CNY.',
        'Worked example: mutual termination after 3 years and 8 months',
        'Take hire date 2019-01-15 and leaving date 2022-09-10: total months = (2022 − 2019) × 12 + (9 − 1) = 44 months; because the leaving day (10) is earlier than the hire day (15) no extra month is added, giving 3 full years and 8 remaining months (6 months or more counts as 1 year), so N = 4. The monthly wage of 15,000 is below the three-times cap, so the calculation wage is 15,000 CNY and N+1 compensation = 4 × 15,000 + 15,000 = 75,000 CNY; the tax-free allowance = (30,000 ÷ 3 × 12) × 3 = 360,000 CNY, so 75,000 CNY falls within the allowance, no tax is due, and the net amount received is 75,000 CNY.',
        'How should the rule that six months or more but less than a year counts as one year be applied?',
        'Judge by full years plus the remaining months: 6 or more remaining months adds 1 year, while less than 6 months adds 0.5 years (turn off the option for less than 6 months counting as half a month to make it add 1 year instead). Example: 3 years and 8 months → N = 4.',
        'Why is service capped at 12 years once the monthly wage is capped?',
        'Under Article 47 of the Labor Contract Law, where an employee’s monthly wage exceeds three times the average monthly wage of employees in the region for the previous year, compensation is paid at three times that amount and the payment period may not exceed twelve years. High earners are capped on both the monthly wage and the number of years.',
        'About N+1 compensation calculation',
    ]))

    write('contract-dates', build('contract-dates', [
        '📅 Contract Date Validation',
        'Checks the logical consistency of the signing date, effective date and end date, computes the contract term and determines the current contract status.',
        '/ Contract Date Validation',
        '📖 View the guide to contract date validation',
        'Automatic renewal agreed',
        'Advance notice required to terminate',
        '📚 In-depth: contract date validation',
        'Standard performance period: signed 2024-01-10, effective 2024-02-01, ending 2025-01-31, a term of 365 days (about 1 year); while it is in performance the remaining days and progress can be shown.',
        'Effective date later than the signing date: signed 2024-03-01 and effective 2024-06-01, the tool notes that it takes effect 92 days after signing, avoiding effectiveness disputes caused by logical contradictions.',
        'Advance notice agreed for termination: with an end date of 2025-12-31 and 30 days advance notice required, the last notice date is 2025-12-01; missing it may make unilateral termination under the agreement impossible.',
        'Worked example: converting a one-year contract term',
        'Effective 2024-02-01 and ending 2025-01-31, so the term = 2025-01-31 − 2024-02-01 = 365 days. If today is 2024-06-10, then 130 days have been performed, 235 days remain and progress is about 35.6%; status: today falls within the interval [effective date, end date] → in performance. For the notice period, 30 days before the end date 2025-12-31 gives 2025-12-01 as the last notice date.',
        'What is the risk of an effective date earlier than the signing date?',
        'Unless the contract is agreed to take effect subject to a condition or a term, an effective date earlier than the signing date is logically contradictory and may affect when the contract takes effect; check the clauses before signing.',
        'How is an automatic renewal clause presented?',
        'Once you check automatic renewal agreed, the expiry status is shown as automatically renewed, and you should be prompted to verify the cap on the number of renewals and the renewal conditions to avoid disputes over indefinite renewal.',
        'About contract date validation',
    ]))

    write('ip-protection', build('ip-protection', [
        '©️ Intellectual Property Protection Period',
        'Computes the expiry date and remaining years of protection for patents, trademarks and copyrights, and flags renewal or fee payment deadlines.',
        '/ IP Protection Period',
        '📖 View the guide to intellectual property protection periods',
        '📚 In-depth: intellectual property protection periods',
        'Invention patent: filing date 2010-03-01, protection lasts 20 years counted from the filing date, expiring 2030-03-01; annual fees must be paid every year to maintain it, and the patent right lapses if the fees are not paid.',
        'Registered trademark: registration approved on 2018-06-15, protection lasts 10 years, expiring 2028-06-15; the renewal window is 2027-06-15 to 2028-06-15, with a grace period extending to 2028-12-15.',
        'Design: filed on 2022-01-01 (after 2021-06-01), protection lasts 15 years, expiring 2037-01-01; filings made before that date get 10 years.',
        'Worked example: the 20-year protection of an invention patent',
        'Filing date 2010-03-01, invention patent protection 20 years, so expiry = 2010-03-01 + 20 years = 2030-03-01. If today is 2024-06-10, about 2090 days remain (about 5.7 years). Trademarks differ: approval date 2018-06-15 + 10 years = expiry 2028-06-15, and renewal can be filed within the 12 months before expiry (from 2027-06-15), each renewal lasting 10 years.',
        'Why are designs protected for either 10 or 15 years?',
        'After the fourth amendment to the Patent Law took effect on June 1, 2021, design patents filed on or after that date are protected for 15 years, while those filed earlier are protected for 10 years; the dividing line is whether the filing date falls after 2021-06-01.',
        'What happens if a trademark is not renewed on expiry?',
        'If it is not renewed on expiry and the 6-month grace period is also missed, the registered trademark lapses and others may apply to register it; renewal should be handled within the 12 months before expiry, and can still be done with a surcharge during the grace period.',
        'About intellectual property protection periods',
    ]))

    write('keyword-extract', build('keyword-extract', [
        '⚖️ Legal Keyword Extraction',
        'Automatically extracts keywords from legal documents, including legal terms, dates, amounts, parties and statutory citations, to assist document search and analysis.',
        '/ Legal Keyword Extraction',
        '📖 View the guide to legal keyword extraction',
        'Legal terms',
        'Parties',
        'Statutory citations',
        'Frequent words',
        ': recognizes date formats such as yyyy-mm-dd, yyyy/mm/dd and yyyymmdd.',
        ': recognizes monetary expressions such as "CNY XX", "XX ten thousand CNY" and "XX CNY".',
        '📚 In-depth: legal keyword extraction',
        'Judgment on a sales contract: after pasting the document it extracts the plaintiff Zhang San and the defendant Li Si, the date 2024-03-15, the amount CNY 500,000, the statutory citations Article 577 and Article 585 of the Civil Code, and so on, helping to sort out the points in dispute quickly.',
        'Lease contract dispute: extracts frequent legal terms such as rent, deposit, breach and termination to locate the core obligation clauses and the breach points.',
        'Bulk document search: counts frequent words across several documents (frequency ≥ 2) to support clustering, comparison of key points and similar-case search.',
        'Worked example: extraction results on the built-in sample document',
        'The default sample is a judgment on a sales contract dispute. The tool identifies the parties Zhang San and Li Si, the dates 2024-03-15 and 2023-10-01 / 2023-12-31, the amounts CNY 500,000 and CNY 50,000, the statutory citations Article 577 and Article 585 of the Civil Code, and frequent words such as contract, breach and payment for goods; it outputs the total keyword count and displays them by category for easy search and archiving.',
        'Why do the extraction results need manual review?',
        'This tool works by rules and dictionary matching, so it may misjudge or miss complex sentence structures, ambiguous identical names (such as Manager Wang) or uncommon terms; verify key documents manually before relying on them.',
        'Will the document content be uploaded?',
        'No. All recognition happens locally in the browser; the text never leaves your device and is never uploaded to any server, in line with the pure front-end privacy principle.',
        'About legal keyword extraction',
        'Paste the content of a legal document, such as a judgment, contract or complaint...\n\nExample:\nIn the sales contract dispute between the plaintiff Zhang San and the defendant Li Si, this court registered the case on March 15, 2024. The plaintiff alleged that on October 1, 2023 the two parties signed a Purchase and Sale Contract under which the defendant would buy goods from the plaintiff for a total price of CNY 500,000. The defendant failed to pay for the goods on time, which constitutes a breach of contract. Pursuant to Article 577 of the Civil Code of the People’s Republic of China, the plaintiff requests a judgment ordering the defendant to pay CNY 500,000 for the goods plus CNY 50,000 in liquidated damages.',
    ]))

    write('statute-deadline', build('statute-deadline', [
        '🧮 Statute of Limitations Calculator',
        'Computes the expiry date of the limitation period from the date the right was infringed or the date the infringement became known, and shows how much time remains to assert the right.',
        '/ Statute of Limitations',
        '📖 View the guide to statute of limitations calculation',
        'Suspension of the limitation period applies',
        'Interruption of the limitation period applies',
        '📚 In-depth: statute of limitations calculation',
        'Ordinary period: the date of infringement or of becoming aware is 2021-01-01, the ordinary limitation period is 3 years, expiring 2024-01-01.',
        'Interruption: starting 2020-06-01, filing suit on 2022-06-01 interrupts the period; 3 years run again from the interruption date, expiring 2025-06-01.',
        'Suspension: starting 2021-01-01 (expiring 2024-01-01), force majeure occurs on 2023-10-01 and the obstacle is removed on 2024-02-01, suspending 123 days, so expiry is postponed to 2024-05-03.',
        'Worked example: the 3-year ordinary period and suspension',
        'Start date 2021-01-01, ordinary 3 years → expiry 2024-01-01. If force majeure occurs within the final 6 months (2023-10-01) and is removed on 2024-02-01, the suspended days = 2024-02-01 − 2023-10-01 = 123 days, and expiry is postponed to 2024-01-01 + 123 days = 2024-05-03. In the interruption case, 3 years run again from the interruption date (for example 2022-06-01).',
        'What is the difference between interruption and suspension?',
        'Interruption arises from filing suit, from one party making a demand, or from agreeing to perform, and the period starts running again from that moment; suspension arises when an obstacle such as force majeure occurs within the final 6 months, and the period expires 6 months after the obstacle is removed (this tool approximates it by postponing by the number of suspended days).',
        'How is the maximum 20-year protection period counted?',
        'It runs from the date the right was damaged and does not apply the knew or should have known rule; courts do not protect rights beyond 20 years, although an extension may be applied for in special circumstances.',
        'About statute of limitations calculation',
    ]))


if __name__ == '__main__':
    main()
