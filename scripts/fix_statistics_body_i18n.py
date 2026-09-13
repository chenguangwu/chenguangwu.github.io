#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""statistics (51) 分类英文态数据源根治：同步三端 + 清孤儿键。

三处数据源（与 science/sports/fun/ai/biz/life/agriculture/hydraulic 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/statistics-body.json  -> build `_prerender_tool_body` 预渲染 h1 + 首个 <p>
  ② i18n/tools/statistics.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json     -> 运行时 en（h2/h1）与 ed

本轮缺口：
  - 51 页 en-US / body / ov 三端英文为占位或代号（如 "Statistics 7" / "P" / "T" / "Iqr"）
  - 孤儿键清理：body 10 个（跨行业残留 bayes-theorem / confidence-interval / margin-of-error
    已迁 it；已下架 odds-to-probability；旧命名残留 statistics-2/3/6/8/9/15）、
    ov 4 个、gis 4 个

用法：
  python3 scripts/fix_statistics_body_i18n.py --dry-run
  python3 scripts/fix_statistics_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'statistics')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'statistics-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'statistics.json')

# NAME = 英文名（h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
NAME = {
    'binomial-cdf': 'Binomial CDF Calculator',
    'binomial-pmf': 'Binomial PMF Calculator',
    'chi-square-test': 'Chi-Square Test Calculator',
    'coefficient-of-variation': 'Coefficient of Variation Calculator',
    'cohens-d': "Cohen's d Effect Size Calculator",
    'confidence-proportion': 'Proportion Confidence Interval Calculator',
    'correlation-coefficient': 'Pearson Correlation Coefficient Calculator',
    'correlation-r-squared': 'Coefficient of Determination (R-squared) Calculator',
    'cramers-v': "Cramer's V Calculator",
    'f-test-variance': 'F-Test for Equal Variances Calculator',
    'geometric-mean': 'Geometric Mean Calculator',
    'harmonic-mean': 'Harmonic Mean Calculator',
    'independent-t-test': 'Independent Two-Sample t-Test Calculator',
    'iqr': 'Interquartile Range (IQR) Calculator',
    'linear-regression': 'Least-Squares Linear Regression Calculator',
    'mean-absolute-deviation': 'Mean Absolute Deviation (MAD) Calculator',
    'normal-cdf': 'Standard Normal CDF Calculator',
    'odds-ratio': 'Odds Ratio Calculator',
    'one-sample-t-test': 'One-Sample t-Test Calculator',
    'one-sample-z-test': 'One-Sample z-Test Calculator',
    'one-way-anova': 'One-Way ANOVA Calculator',
    'p': 'P-Value from z-Score Estimator',
    'paired-t-test': 'Paired t-Test Calculator',
    'percentile-rank': 'Percentile Rank Calculator',
    'poisson-pmf': 'Poisson PMF Calculator',
    'pooled-variance': 'Pooled Variance Calculator',
    'population-variance': 'Population Variance Calculator',
    'probability-complement': 'Complementary Probability Calculator',
    'range-stat': 'Range Calculator',
    'relative-risk': 'Relative Risk (RR) Calculator',
    'sample-size-mean': 'Sample Size for Estimating a Mean',
    'sample-size-proportion': 'Sample Size for Estimating a Proportion',
    'sample-variance': 'Sample Variance Calculator',
    'skewness-sample': 'Sample Skewness Calculator',
    'standard-error': 'Standard Error of the Mean Calculator',
    'standard-error-proportion': 'Standard Error of a Proportion Calculator',
    'statistics': 'Normal Distribution Probability Calculator',
    'statistics-10': 'Coefficient of Variation Comparison',
    'statistics-11': 'Weighted Mean Calculator',
    'statistics-12': 'Mean, Median and Mode Calculator',
    'statistics-13': 'Standard Deviation and Variance Calculator',
    'statistics-16': 'Linear Regression Fit Calculator',
    'statistics-4': 'Confidence Interval for a Mean Calculator',
    'statistics-5': 'Sample Size Estimator',
    'statistics-7': 'Skewness and Kurtosis Calculator',
    'stddev-list': 'Sample Standard Deviation Calculator',
    't': 'One-Sample t Statistic Calculator',
    't-score': 't-Statistic Calculator',
    'variance-list': 'Sample Variance Calculator (Data List)',
    'z': 'Z-Score Calculator (with Percentile)',
    'z-score-calc': 'Z-Score Calculator',
}

INTRO = {
    'binomial-cdf': 'Enter the number of trials n, success probability p and upper bound x to get the cumulative probability P(X<=x) of a binomial distribution, for acceptance sampling, reliability and cumulative binomial analysis.',
    'binomial-pmf': 'Enter trials n, success count k and success probability p to compute the probability of exactly k successes in n independent Bernoulli trials, for discrete distributions and risk modelling.',
    'chi-square-test': 'Enter observed and expected frequencies to compute the chi-square statistic and judge whether the deviation is significant, for goodness-of-fit and independence tests.',
    'coefficient-of-variation': 'Enter the mean and standard deviation to compute CV = sigma/mu x 100%, comparing dispersion across data sets measured in different units.',
    'cohens-d': "Enter two group means and pooled standard deviation (or group SDs and sizes) to compute Cohen's d and measure effect size for comparing experimental results.",
    'confidence-proportion': 'Enter the number of successes and sample size (or the sample proportion) to get the confidence interval for a population proportion by normal approximation, for surveys and medical estimation.',
    'correlation-coefficient': 'Enter paired X and Y data to compute the Pearson correlation coefficient r, measuring the strength and direction of a linear relationship, with a significance check.',
    'correlation-r-squared': 'Enter the correlation coefficient r to compute the coefficient of determination R-squared, the share of variance in the dependent variable explained by a regression model.',
    'cramers-v': "From the chi-square value, sample size and degrees of freedom of a contingency table, compute Cramer's V to measure the association strength between two categorical variables.",
    'f-test-variance': 'Enter two sample variances and their degrees of freedom to compute the F statistic and critical value and test whether two population variances are equal.',
    'geometric-mean': 'Enter a set of positive numbers to compute the geometric mean as the n-th root of their product, suited to growth rates and ratio-type data.',
    'harmonic-mean': 'Enter a set of numbers to compute the harmonic mean as the reciprocal of the arithmetic mean of reciprocals, suited to rates and unit prices.',
    'independent-t-test': 'Enter two independent samples (means, standard deviations and sizes) to compute the t value and p value and test whether the two population means differ significantly.',
    'iqr': 'Enter a data set (or count, minimum, Q1, median, Q3 and maximum) to compute Q1, Q2, Q3 and the interquartile range, and mark outlier bounds by the 1.5 x IQR rule for box plots.',
    'linear-regression': 'Enter paired (x, y) data to fit the best-fit line by least squares and get the slope, intercept and R-squared, for trend prediction and variable-relationship modelling.',
    'mean-absolute-deviation': 'Enter a series of values to compute the mean absolute deviation MAD = sum|x - xbar| / n, measuring average dispersion for forecast error and robustness checks.',
    'normal-cdf': 'Enter the mean, standard deviation and a value x, or a standard score z, to compute the standard normal cumulative probability P(X <= x) for probability and quantile estimates.',
    'odds-ratio': 'Enter the four frequencies of a 2x2 contingency table to compute the odds ratio and its confidence interval, measuring exposure-outcome association in epidemiology.',
    'one-sample-t-test': 'Enter sample data (or mean, standard deviation and size) to test a sample mean against a hypothesised population mean when the population SD is unknown, returning t, df and p.',
    'one-sample-z-test': 'Enter the sample mean, sample size and known population standard deviation to test the sample mean against a hypothesised value, returning the z statistic and one/two-sided p values.',
    'one-way-anova': 'Enter two or more group means, standard deviations and sizes to compute between-group and within-group sums of squares, the F value and p value for one-way analysis of variance.',
    'p': 'Enter a z statistic to approximate the two-sided p value using the normal distribution, with a note that p below 0.05 usually rejects the null hypothesis at the 5% level.',
    'paired-t-test': 'Enter paired measurements of the same subjects (e.g. before and after treatment) to compute the mean and SD of differences and test whether the difference is non-zero, returning t, df and p.',
    'percentile-rank': 'Enter a data set and a target value to compute the percentile rank, i.e. the percentage of the data below that value, for score and ranking evaluation.',
    'poisson-pmf': 'Enter the average event rate lambda per unit time or space and the target count k to compute the Poisson probability mass P(X=k), for rare-event modelling such as call arrivals or failures.',
    'pooled-variance': 'Enter two sample sizes and standard deviations to compute the pooled variance as a weighted average, used for the equal-variance assumption before a two-sample t-test.',
    'population-variance': 'Enter a complete data set to compute the population variance as the average squared deviation from the mean, measuring dispersion with results computed locally.',
    'probability-complement': 'Enter the probability of an event p to compute the complementary probability P(Ac) = 1 - P(A), a basic probability operation.',
    'range-stat': 'Enter a series of values to compute the range R = max - min, a quick measure of the spread of a data set.',
    'relative-risk': 'Enter the outcome rates of an exposed and an unexposed group to compute the relative risk RR and its confidence interval, measuring exposure-outcome association in cohort studies.',
    'sample-size-mean': 'Given a confidence level, margin of error and population standard deviation, estimate the minimum sample size needed to estimate a population mean, for experiment design.',
    'sample-size-proportion': 'Given a confidence level, margin of error and expected proportion, estimate the minimum sample size needed to estimate a population proportion, for survey design.',
    'sample-variance': 'Enter a data set to compute the sample variance using n - 1 degrees of freedom, measuring dispersion for inferential statistics and hypothesis testing.',
    'skewness-sample': 'Enter a series of values to compute the sample skewness g1 from the third standardised central moment, judging left/right skew and symmetry of a distribution.',
    'standard-error': 'Enter the sample standard deviation and sample size to compute the standard error of the mean SE = s / sqrt(n), used in confidence intervals and significance tests.',
    'standard-error-proportion': 'Enter the sample proportion p and sample size n to compute SE = sqrt[p(1-p)/n], the sampling variability of a proportion estimate, for proportion confidence intervals and tests.',
    'statistics': 'Enter the mean, standard deviation and lower/upper bounds to compute the probability (area under the normal curve) for that interval, useful for cumulative probabilities and quantile ranges.',
    'statistics-10': 'Enter the mean and standard deviation of two data sets to compare their coefficients of variation CV, removing the effect of units when comparing dispersion.',
    'statistics-11': 'Enter values together with their weights to compute a weighted mean with automatic weight normalisation, for weighted scores and indicators.',
    'statistics-12': 'Enter up to seven values to quickly compute the arithmetic mean, median, mode and range and the total, a fast way to describe central tendency and spread of a data set.',
    'statistics-13': 'Enter a set of values and choose sample or population to compute standard deviation, variance and the coefficient of variation, comparing dispersion across different units.',
    'statistics-16': 'Enter paired (x, y) sample data to fit the line y = ax + b by least squares, output the slope a, intercept b, correlation and goodness of fit, and predict y for any x.',
    'statistics-4': 'Enter the sample mean, standard deviation, sample size and a confidence level (e.g. 95%) to estimate the confidence interval for the population mean with a z value, for large samples or known population SD.',
    'statistics-5': 'Enter the acceptable margin of error, confidence level and population standard deviation to estimate the minimum sample size for a mean, planning sample counts with sufficient precision.',
    'statistics-7': 'Enter a data set to compute skewness and kurtosis and judge whether the distribution is left- or right-skewed and more peaked or flatter than normal, spotting tail features.',
    'stddev-list': 'Enter a comma- or space-separated list of numbers to compute the sample standard deviation s with n - 1 denominator, assessing how spread out the observations are.',
    't': 'Enter the sample mean, hypothesised population mean, sample standard deviation and sample size to compute the one-sample t statistic (xbar - mu)/(s/sqrt(n)) and its degrees of freedom.',
    't-score': 'Enter the sample mean, hypothesised mean, standard deviation and sample size to compute the t statistic for a mean hypothesis test.',
    'variance-list': 'Enter a comma- or space-separated list of numbers to compute the sample variance s2 = sum(x - xbar)2 / (n - 1), the squared standard deviation used in statistical description and ANOVA.',
    'z': 'Enter a raw score, population mean and population standard deviation to standardise the score as z = (x - mu)/sigma and get its percentile rank, comparing values across distributions.',
    'z-score-calc': 'Enter a raw value, mean and standard deviation to compute the z score (x - mu)/sigma, for standardisation and outlier detection.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


_CANDIDATES = (
    dict(indent=0, separators=(',', ':')),
    dict(indent=1, separators=(',', ':')),
    dict(indent=1),
    dict(indent=2, separators=(',', ':')),
    dict(indent=2),
    dict(indent=None, separators=(',', ':')),
    dict(indent=None),
)


def dump_like(path, data, orig_raw):
    """按文件原有 JSON 格式回写：逐一尝试候选格式，取能无损还原原串的那个。"""
    body_raw = orig_raw.rstrip('\n')
    trailing = '\n' if orig_raw.endswith('\n') else ''
    try:
        orig = json.loads(orig_raw)
    except Exception:
        orig = None
    if orig is not None:
        for c in _CANDIDATES:
            try:
                if json.dumps(orig, ensure_ascii=False, **c) == body_raw:
                    return json.dumps(data, ensure_ascii=False, **c) + trailing
            except Exception:
                continue
    return json.dumps(data, ensure_ascii=False, indent=2) + trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov_raw = open(OV, encoding='utf-8').read()
    body_raw = open(BODY, encoding='utf-8').read()
    gis_raw = open(GIS, encoding='utf-8').read()
    ov = json.loads(ov_raw)
    body = json.loads(body_raw)
    gis = json.loads(gis_raw)

    chg_en = chg_ed = chg_body = added_body = added_gis = chg_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'statistics/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'statistics'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'statistics')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + statistics-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + statistics.json 新增条目:', slug)
        z = g.get('zh-CN')
        if not isinstance(z, dict):
            z = {}
        # statistics 中文态齐全，不写英文进中文位；仅当缺失时告警（由 ZH 字典补，本批无缺）
        if not (z.get('title') or '').strip():
            print('  !! zh-CN title 缺失（需人工补中文）:', slug)
        g['zh-CN'] = z
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿/跨行业残留键清理：本行业数据源中不属于 statistics 工具页的键一律删除。
    st_slugs = set(slugs)
    orph_body = [k for k in list(body.keys()) if k not in st_slugs]
    for k in orph_body:
        del body[k]
    orph_ov = [k for k in list(ov.keys())
               if k.startswith('statistics/') and k.split('/', 1)[1] not in st_slugs]
    for k in orph_ov:
        del ov[k]
    orph_gis = [k for k in list(gis.keys()) if k not in st_slugs]
    for k in orph_gis:
        del gis[k]

    print('\n--- 汇总 ---')
    print('statistics 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('statistics-body 更新:', chg_body, ' 新增:', added_body)
    print('statistics.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title 补齐:', chg_zh)
    print('孤儿键删除  body:', len(orph_body), ' _en_override:', len(orph_ov), ' statistics.json:', len(orph_gis))
    if orph_body:
        print('   body:', orph_body)
    if orph_ov:
        print('   ov  :', orph_ov)
    if orph_gis:
        print('   gis :', orph_gis)

    if a.dry_run:
        print('\n[dry-run] 未写盘')
        return 0

    open(OV, 'w', encoding='utf-8').write(dump_like(OV, ov, ov_raw))
    open(BODY, 'w', encoding='utf-8').write(dump_like(BODY, body, body_raw))
    open(GIS, 'w', encoding='utf-8').write(dump_like(GIS, gis, gis_raw))
    print('\n已写盘:', OV, BODY, GIS)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
