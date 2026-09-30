#!/usr/bin/env python3
# statistics batch3 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'statistics')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'statistics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'p': [
"p-Value Approximation for Hypothesis Testing",
"Estimates the two-tailed p-value of a z-test by normal approximation.",
'📖 View the "p-Value Approximation for Hypothesis Testing User Guide"',
"Two-tailed p = 2 · (1 − Φ(|Z|))",
"p < 0.05 is usually taken as significant at the 5% level.",
"📚 In-depth: Two-Tailed p-Value (Standard Normal)",
"Given z, the two-tailed p=2(1−Φ(|z|)).",
"Hypothesis testing",
" for significance decisions.",
"p<0.05 is usually judged significant.",
"p=2(1−Φ(1.96))=2×0.025=0.05, exactly the 5% significance boundary.",
"p=2(1−Φ(2.58))≈2×0.0049≈0.0098, significant at about the 1% level.",
"What does the p-value mean?",
"The probability of observing the current result or a more extreme one if the null hypothesis holds. A small p does not mean a large effect, only that the result looks unlikely to be random.",
"Why two tails?",
"Without a directional hypothesis both extremes count as unusual, so the two-tailed p is twice the one-tailed value and therefore more conservative.",
],
'paired-t-test': [
"Tests the differences from before-and-after or paired measurements on the same subjects.",
"Paired t-Test Calculator",
"/ Paired Samples t-Test",
"Paired Samples t-Test",
'📖 View the "Paired t-Test Calculator User Guide"',
"Mean difference d̄",
"Standard deviation of the differences s_d",
"Number of pairs n",
"Used for before-and-after controlled experiments.",
"📚 In-depth: Paired Samples t-Test",
"Pre-post differences within subjects: t=d̄/(sd/√n), df=n−1.",
"Removes variation between subjects and increases sensitivity.",
"For example blood pressure before and after medication.",
"Pre-test and post-test",
"Mean difference d̄=3, sd of the differences=4, n=20: t=3/(4/√20)=3/0.894≈3.354, df=19. The critical value of ≈2.093 is exceeded, so it is significant (p<0.01) and the intervention works.",
"No effect",
"With d̄=0.5: t=0.5/0.894≈0.56, not significant.",
"Why use a paired rather than an independent t-test?",
"Pairing controls for baseline differences between subjects, giving smaller error and higher power; it requires pre-post measurements on the same subjects or a paired design.",
"Must the differences be normal?",
"The differences should be approximately normal, though with large n the central limit theorem relaxes this.",
],
'percentile-rank': [
"The proportion of data in the group that falls below a given value.",
"Percentile Rank Calculator",
"/ Percentile Rank",
"Percentile Rank",
'📖 View the "Percentile Rank Calculator User Guide"',
"PR = (Below+0.5·Equal)/N×100. It describes relative position.",
"Describes relative position.",
"📚 In-depth: Percentile Rank",
"PR=(number below+0.5×number equal)/N×100.",
"Relative position of a score within a group.",
'"What percentage am I above" for exam scores and heights.',
"An exam score of 80",
"Among 30 people, 12 score below 80 and 3 equal 80: PR=(12+0.5×3)/30×100=(13.5)/30×100=45, i.e. ahead of roughly 45% of the group (the 45th percentile).",
"If nobody scores higher: PR=(29+0.5×1)/30×100≈98.3.",
"Percentile versus percentile rank?",
"The percentile P_k is the score below which k% of people fall; the percentile rank is the k matching a given score, so the two are inverse functions.",
"Why add 0.5?",
"It counts half of the tied cases, avoiding treating one's own score as below itself; a standard empirical correction.",
],
'poisson-pmf': [
"Probability of observing k events within a unit of time or space.",
"Poisson Probability Calculator",
"/ Poisson Probability",
"Poisson Probability",
'📖 View the "Poisson Probability Calculator User Guide"',
"Number of events k",
"📚 In-depth: Poisson Probability",
"Event counts per unit of time or space: P(X=k)=λ^k·e^−λ/k!.",
"λ is the average rate (mean = variance).",
"Counts of rare events such as calls or failures.",
"λ=3 with 2 hits",
"P(X=2)=3²·e^−3/2!=9×0.04979/2≈0.2240, about 22.4%.",
"λ=3 with no hits",
"P(X=0)=e^−3≈0.0498, so there is about a 5% chance nobody arrives.",
"When does the Poisson approximate the binomial?",
"With large n, small p and a moderate np=λ, the binomial is approximately Poisson, the standard model for rare events.",
"Can λ be a decimal?",
"Yes. λ is an average rate (for example 2.5 per hour) and need not be a whole number.",
],
'pooled-variance': [
"Pooled Variance from Two Sample Variances",
"Enter the two sample sizes n₁ and n₂ together with the variances s₁² and s₂² to get the pooled variance.",
"Pooled Variance Calculator",
"/ Pooled Variance Calculator",
'📖 View the "Pooled Variance from Two Sample Variances User Guide"',
"Used when the two-sample t-test assumes equal variances.",
"📚 In-depth: Pooled Variance",
"A common variance estimate for the two-sample t-test.",
"More precise when the variances are assumed equal.",
"Equal sample sizes",
"Unequal variances",
"Why is the pooled variance a weighted average?",
"It is weighted by degrees of freedom (n−1), so the larger sample carries more weight; this gives an unbiased pooling.",
"Can unequal variances still be pooled?",
"No. Use Welch's t-test directly, which does not pool variances and corrects the degrees of freedom.",
],
'population-variance': [
"Population Variance Calculator",
"Variance with the population size N as the denominator.",
"/ Population Variance",
"Population Variance",
'📖 View the "Population Variance Calculator User Guide"',
"Population variance divides the sum of squared deviations of every observation from the population mean μ by the population size N, describing the dispersion of the entire data set. Unlike sample variance its denominator is N rather than n − 1, so it applies when the complete population is known.",
"The denominator is N (population).",
"📚 In-depth: Population Variance",
"σ²=Σ(x−μ)²/N (dividing by N).",
"Used when the entire population is known.",
"sample variance",
" differs, since that one divides by n−1.",
"Data [2,4,6,8]",
"Versus sample variance",
"For the same data the sample s²=20/3≈6.667, larger than the population variance because of the degrees-of-freedom correction.",
"Why does sample variance divide by n−1?",
"Estimating from the sample mean systematically underestimates the true variance; dividing by n−1 gives the unbiased Bessel correction.",
"When is population variance used?",
"Only when the data form the complete population rather than a sample; any survey estimate uses sample variance.",
],
'probability-complement': [
"Probability of the Complement from an Event Probability",
"Enter the event probability p to get the probability of the complementary event.",
"Complementary Event Probability Calculator",
"/ Complementary Event Probability Calculator",
'📖 View the "Probability of the Complement from an Event Probability User Guide"',
"The probability of the complementary event equals 1 minus the event probability, and the two always add to 1. It gives a quick route to problems such as at least one occurrence or none occurring: when computing an event directly is cumbersome, take the complement instead.",
"Probability P(A)",
"The probabilities of all possible events sum to 1.",
"📚 In-depth: Probability of Complementary Events",
"P(not A)=1−P(A).",
'"At least once" is simpler as 1 minus none occurring.',
"A basic axiom of probability.",
"At least once",
"With single-trial success p=0.3, at least one success in three trials is 1−0.7³=1−0.343=0.657, simpler than adding up the separate terms.",
"Complementary event",
"P(rain)=0.2 gives P(no rain)=0.8.",
"When should complements be used?",
"When a direct calculation has many terms (such as at least 1 meaning 1 or 2 or ... or n), the complement none occurring usually settles it in a single term.",
"Does it require mutually exclusive events?",
"No. The complement formula holds for any event and does not require mutual exclusivity, which belongs to the addition rule.",
],
'range-stat': [
"Range of a Series of Values",
"Enter several values (separated by commas or spaces) to get the range.",
"Range Calculator",
'📖 View the "Range of a Series of Values User Guide"',
"The range is the difference between the largest and smallest values in a data set: the simplest measure of dispersion, reflecting the overall span. It is quick to compute but depends only on the two endpoints, so outliers distort it, which is why it usually serves as a first screening statistic.",
"The range is the easiest to compute but sensitive to extreme values.",
"📚 In-depth: Range",
"R=max−min, the simplest measure of dispersion.",
"Quickly describes the span of the data.",
"Highly sensitive to outliers.",
"Data [3,7,2,9]",
"Effect of outliers",
"[3,7,2,9,100]: R=98, dominated by a single extreme value, which is why the IQR is usually reported alongside.",
"Limitations of the range?",
"It uses only the two extremes and ignores the middle of the distribution and the ",
", so a single outlier distorts it; in large samples the range also inflates with n.",
"When should the range be used?",
"For quick screening and quality control (R charts); formal analysis should be backed up by the ",
],
'relative-risk': [
"Comparing outcome rates between an exposed group and an unexposed group.",
"Relative Risk Calculator",
"/ Relative Risk (RR)",
"Relative Risk (RR)",
'📖 View the "Relative Risk Calculator User Guide"',
"a=40, b=60 gives an incidence rate of 0.4.",
"RR>1 means exposure carries higher risk.",
"📚 In-depth: Relative Risk (RR)",
"RR = incidence in the exposed group / incidence in the unexposed group.",
"Effect strength in cohort studies.",
"RR=1 means no effect, above 1 higher risk and below 1 protection.",
"Exposure and disease",
"40/60 cases in the exposed group and 30/90 in the unexposed group give RR=(40/60)/(30/90)=0.667/0.333=2.0, so exposure carries twice the risk of the control group.",
"Protection",
"RR=0.5 means incidence in the exposed group is half that of the controls (a protective effect).",
"How do RR and OR differ?",
"RR compares incidence rates (requiring a cohort and known denominators), while OR compares odds (case-control studies). For rare diseases OR≈RR.",
"Can RR greatly exceed 1?",
"Yes, indicating strong risk, but when the ",
" is wide a large sample is needed before the estimate is reliable.",
],
'sample-size-mean': [
"Sample Size for a Mean Calculator",
"Sample size required to estimate a population mean.",
"/ Sample Size (Mean)",
"Sample Size (Mean)",
'📖 View the "Sample Size for a Mean Calculator User Guide"',
"The minimum sample size needed to estimate a population mean follows from the tolerated error e, the population standard deviation σ and the z value for the chosen confidence level: a smaller error, a larger σ or a higher confidence level all increase the required size. The z value can be entered by hand (95% corresponds to 1.96 and 99% to 2.576) and the result is rounded up.",
"If σ is unknown, use a historical estimate.",
"A smaller e means a larger sample size.",
"📚 In-depth: Sample Size for a Mean",
"n=(z·σ/e)² for a given precision e and confidence level.",
"Planning the required ",
"z=1.96 corresponds to 95%.",
"Precision ±2",
"z=1.96, σ=10, e=2: n=(1.96×10/2)²=(9.8)²=96.04→97, so at least 97 observations are required.",
"Tighter precision",
"With e=1: n=(19.6)²=384.16→385, since halving the error quadruples the sample size.",
"What is e?",
"e is the tolerated margin of error (ME), i.e. the upper bound on the ",
" half-width; a smaller e requires a larger n (a quadratic relation).",
"How do you set σ when it is unknown?",
"Estimate it from a pilot study or the literature, or use a conservative maximum variability; otherwise adopt two-stage sampling.",
],
}

def build(slug, en_list):
    path = os.path.join(WORK, slug + '.json')
    wj = json.load(open(path, encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('!! %s length mismatch %d vs %d' % (slug, len(en_list), len(items)))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src'):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if not en or not isinstance(en, str):
            print('!! %s empty translation' % slug)
            sys.exit(1)
        if CJK.search(en) or CNP.search(en):
            print('!! %s CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    name = ''
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'statistics', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

if __name__ == '__main__':
    for slug, en_list in EN.items():
        mp = build(slug, en_list)
        write(slug, mp)
    print('gen_stat_b3 done')
