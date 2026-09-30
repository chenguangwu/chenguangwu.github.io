#!/usr/bin/env python3
# statistics batch4 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'statistics')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'statistics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'sample-size-proportion': [
"Estimates the sample size required for a given confidence level and error bound.",
"Sample Size for a Proportion Calculator",
"/ Sample Size (Proportion)",
"Sample Size (Proportion)",
'📖 View the "Sample Size for a Proportion Calculator User Guide"',
"Sample size peaks at p=0.5. Use z=1.96 for 95% confidence.",
"Sample size peaks at p=0.5.",
"Use z=1.96 for 95% confidence.",
"📚 In-depth: Sample Size for a Proportion",
"Planning the required ",
"p=0.5 is the most conservative choice (largest n).",
"Approval rate survey",
"z=1.96, p=0.5, e=0.05: n=1.96²×0.25/0.0025=0.9604/0.0025=384.16→385, the classic 385 respondents.",
"Known p=0.3",
"n=1.96²×0.3×0.7/0.0025=0.9604×0.21/0.0025≈322, so the sample size is smaller.",
"Why is p=0.5 the most conservative?",
"Because p(1−p) is maximized at 0.5, which maximizes n; planning on that basis guarantees enough observations when p is unknown.",
"Is this the minimum sample?",
"It assumes no response bias and simple random sampling; stratification or non-response require inflating it further.",
"How to Use the Sample Size for a Proportion Calculator",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does the Sample Size for a Proportion Calculator do?",
"Sample Size for a Proportion Calculator: given the confidence level, error bound and expected proportion, estimates the sample size needed for a population proportion, for the design of sample surveys.",
"How do I use the Sample Size for a Proportion Calculator?",
"What scenarios is the Sample Size for a Proportion Calculator best for?",
],
'sample-variance': [
"Sample variance with n−1 degrees of freedom.",
"/ Sample Variance",
"Sample Variance",
'📖 View the "Sample Variance Calculator User Guide"',
"s² = Σ(xᵢ−x̄)²/(n−1). The denominator is n−1 (unbiased).",
"The denominator is n−1 (unbiased).",
"📚 In-depth: Sample Variance",
"s²=Σ(x−x̄)²/(n−1) (dividing by n−1).",
"An unbiased estimate of dispersion under sampling.",
"population variance",
" distinction.",
"Data [2,4,6,8]",
"A set of values",
"Why divide by n−1 rather than n?",
"Using the sample mean x̄ underestimates the true variance; dividing by the degrees of freedom n−1 gives the unbiased Bessel-corrected estimate.",
"s² versus the ",
"The standard deviation s=√s² restores the original units and is easier to interpret.",
"How to Use the Sample Variance Calculator",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does the Sample Variance Calculator do?",
"Sample Variance Calculator: enter a data set to compute the sample variance with n−1 degrees of freedom, measuring dispersion for inferential statistics and hypothesis testing.",
"How do I use the Sample Variance Calculator?",
"What scenarios is the Sample Variance Calculator best for?",
"🧮 Reading the Results",
"Sample variance s²=Σ(xᵢ−x̄)²/(n−1) is the dispersion of the sample data about the mean; using the denominator n−1 gives the unbiased Bessel-corrected estimate.",
"Variance carries the square of the original units, so taking the square root recovers the sample standard deviation s with the original scale. Only population variance uses n as its denominator.",
],
'skewness-sample': [
"Sample Skewness from a Series of Values",
"Enter several values (separated by commas or spaces) to get the sample skewness.",
"Sample Skewness Calculator",
"/ Sample Skewness Calculator",
'📖 View the "Sample Skewness from a Series of Values User Guide"',
"Sample skewness g₁ measures the asymmetry of a distribution through the bias-corrected standardized third moment: positive values mean right skew (a long tail to the right), negative values left skew and values near 0 approximate symmetry. The denominator applies n − 1 and n − 2 as small-sample corrections, where n is the sample size and s the sample standard deviation.",
"Positive skewness means a longer right tail.",
"The example gives about 0.82.",
"📚 In-depth: Skewness",
"Skewness g1 measures the direction and degree of asymmetry in a distribution.",
"Positive skew (long right tail) and negative skew (long left tail).",
"A normal distribution has skewness ≈0.",
"Right-skewed",
"Data [1,2,2,3,10]: the mean of 3.6 far exceeds the median of 2 and skewness ≈1.3 (clearly right-skewed), because the extreme value pulls the mean up.",
"Sample skewness is close to 0 for near-normal data (within ±0.5 counts as roughly symmetric).",
"What do the signs of skewness mean?",
"Positive skew means a long right tail with mean > median; negative skew means a long left tail with mean < median.",
"Should large skewness be addressed?",
"Consider a log transform, removing or winsorizing extreme values, or switching to the ",
" and IQR description.",
],
'standard-error-proportion': [
"Standard Error from Sample Proportion and Sample Size",
"Enter the sample proportion p and the sample size n to get the standard error of a proportion.",
"Standard Error of a Proportion Calculator",
"/ Standard Error of a Proportion Calculator",
'📖 View the "Standard Error from Sample Proportion and Sample Size User Guide"',
"The basis for a confidence interval of a proportion.",
"📚 In-depth: Standard Error of a Proportion",
"SE=√(p(1−p)/n), the sampling variability of a sample proportion.",
"Building ",
"confidence intervals for proportions",
" and running z-tests.",
"A larger n gives a smaller SE.",
"SE=√(0.5×0.5/100)=√0.0025=0.05, so the proportion estimate varies by about ±5%.",
"SE=√(0.25/400)=0.025, halved when n is quadrupled.",
"Standard error versus the ",
"The standard deviation describes the spread of the data itself; the standard error of a ",
"descriptive statistic",
" measures sampling variability (for example of a proportion) and shrinks as n grows.",
"Use the sample p or the true value?",
"Usually the sample p is plugged in to estimate SE; at the planning stage p=0.5 gives the largest SE.",
],
'standard-error': [
"Standard deviation of the sampling distribution of the mean.",
"Standard Error of the Mean Calculator",
"/ Standard Error",
'📖 View the "Standard Error of the Mean Calculator User Guide"',
"A larger sample gives a smaller standard error.",
"📚 In-depth: Standard Error of the Mean",
"SE=σ/√n (or s/√n), the sampling variability of the mean.",
" and the denominator of t/z tests.",
"SE shrinks with √n.",
"SE=15/5=3, so the mean estimate varies by about ±3 (the half-width of the 95% CI is roughly 1.96×3≈5.88).",
"SE=15/10=1.5 gives a narrower interval.",
"Why divide by √n?",
"The variance of the mean of independent samples equals the ",
"population variance",
" divided by n, hence SE=σ/√n; more observations make the mean more stable.",
"What if σ is unknown?",
"Estimate SE from the sample s; with small samples the t distribution is more accurate.",
],
'statistics-10': [
"Comparing Coefficients of Variation",
"Checks whether two data sets have similar dispersion.",
'📖 View the "Comparing Coefficients of Variation User Guide"',
"The coefficient of variation CV divides the standard deviation by the absolute mean, removing units so the relative dispersion of two groups can be compared. A larger CV means relatively stronger fluctuation; when the units or magnitudes differ, CV is more appropriate than comparing standard deviations directly.",
"Mean of A",
"Standard deviation of A",
"Mean of B",
"Standard deviation of B",
"CV = (standard deviation / |mean|) × 100%",
"CV removes the effect of units, so data measured on different scales can be compared.",
"📚 In-depth: Comparing Coefficients of Variation",
"Compares the relative dispersion of two data sets (CV=σ/|μ|).",
'Judges which group is less stable when the means differ sharply.',
"The larger CV fluctuates more in relative terms.",
"Comparing two groups",
"Group 1 with μ=100, σ=10 gives CV=10%; group 2 with μ=50, σ=8 gives CV=16%, so group 2 fluctuates more relatively despite the smaller σ.",
"Investment comparison",
"A returns 10% a year with σ 12% (CV 120%); B returns 5% with σ 6% (CV 120%). The CVs match, so the risk-return trade-off is the same.",
"Why use |μ|?",
"It prevents CV from taking the wrong sign when the mean is negative; the absolute value measures relative volatility.",
"Versus the ",
"?",
"The standard deviation measures absolute dispersion and CV relative dispersion, so comparisons across units or across very different means must use CV.",
],
'statistics-11': [
"Weighted Mean",
"Computes a weighted mean from a set of values and their weights.",
'📖 View the "Weighted Mean User Guide"',
"Weighted mean x̄_w = (v₁w₁ + v₂w₂ + v₃w₃) / (w₁ + w₂ + w₃)",
"The weighted mean sums each value multiplied by its weight and divides by the total weight, so weights are normalized automatically and need not be converted to percentages. It is used for weighted grades and composite indicators: the result stays correct even when the weights do not add up to 1 or 100.",
"Weight A",
"Weight B",
"Value C",
"Weight C",
"Weighted mean = Σ(xᵢ · wᵢ) / Σwᵢ",
"The weights need not sum to 1; they are normalized automatically.",
"📚 In-depth: Summary of Descriptive Statistics",
"One click gives the count, mean and ",
" as well as the extremes.",
"Initial exploration of data and quick checks for anomalies.",
"Best used together with visualizations.",
"Sample summary",
"Data [12,15,14,10,18,13,16]: n=7, Σ=98, mean ≈14.0, median 14, min=10, max=18, sd ≈2.65.",
"Skewness hint",
"A mean far above the median suggests right skew, so examine the distribution further.",
"Descriptive statistics",
": is that enough?",
"Only an initial look, since inferential conclusions need ",
"hypothesis testing",
"; description cannot replace inference.",
"When should the median be used?",
"With skewed data or outliers, the median plus IQR is more robust than the mean plus standard deviation.",
],
'statistics-12': [
"Mean, Median and Mode",
"Enter a set of data to compute the mean, median, mode, range and total quickly.",
'📖 View the "Mean, Median and Mode User Guide"',
"Mean = (Σ dᵢ)/7; median = the 4th value after sorting; range = max − min; total = Σ dᵢ",
"Gives central tendency and dispersion quickly for exactly 7 values: the mean is the total divided by 7, the median is the 4th (middle) value after sorting ascending, the range is the maximum minus the minimum, and the sum of all values is shown as well. Handy for classrooms or for describing a set of data quickly.",
"Median: the middle value after sorting",
"Range = maximum − minimum",
"This version uses 7 fixed inputs for fast computation.",
"📚 In-depth: Quantiles and Percentiles",
"Computes any quantile (quartiles, deciles and so on).",
"data distribution",
" for bucketing and baseline lines.",
"Interpolation handles non-integer positions.",
"Versus quartiles",
"Sorted [1,2,3,4,5,6,7,8]: Q1(25%)=2.25, median(50%)=4.5, Q3(75%)=6.75 (linear interpolation).",
"On the same data P90 sits at position 7.2 with a value of about 7.2, meaning 90% of the data fall below roughly 7.2.",
"How are quantiles interpolated?",
"Non-integer positions usually take linear interpolation (NumPy's default), although Excel, TI calculators and other software differ slightly.",
"Why are quantiles not unique?",
"Several definitions exist (types 1-9) and they can differ by 0.1-0.5, so state the method whenever you report them.",
],
'statistics-13': [
"Standard Deviation and Variance",
"Computes the sample or population standard deviation, variance and coefficient of variation (CV).",
'📖 View the "Standard Deviation and Variance User Guide"',
"Variance s² = Σ(xᵢ − x̄)² / (n − 1 or n); standard deviation s = √s²; CV = s / |x̄| × 100%",
"Compute the mean x̄ first, then the sum of squared deviations, and divide by the degrees of freedom to get the variance: a sample uses n − 1 (unbiased) and a population uses n. The standard deviation is the square root of the variance and shares the units of the original data; the coefficient of variation divides the standard deviation by the absolute mean as a percentage, allowing comparison across units. Here n is fixed at 7, so samples use a denominator of 6 and populations a denominator of 7.",
"Type: 1 = sample, 2 = population",
"Variance s² = Σ(x − x̄)² / (n − 1) (sample) or n (population)",
"Standard deviation = √variance",
"Enter 1 for the sample standard deviation and 2 for the population standard deviation.",
"📚 In-depth: Normality and Distribution Tests",
"Tests whether the data are approximately normal (Shapiro-Wilk / Kolmogorov-Smirnov approach).",
"Verifies the assumptions behind parametric tests.",
"Switch to nonparametric methods when the data are not normal.",
"Judging normality by skewness and kurtosis",
"Sample skewness",
" with values near 0 and excess kurtosis near 0, plus a roughly straight QQ plot, the data can be treated as normal so a t-test is appropriate.",
"Clear departure",
"Skewness of 1.5 and kurtosis of 4 point to non-normality, so nonparametric tests such as Wilcoxon or Mann-Whitney are preferable.",
"Does p>0.05 in a normality test mean the data are normal?",
"No. It only means no departure was detected: large samples flag even slight departures while small samples are insensitive, so judge alongside plots.",
"Must you change methods if the data are not normal?",
"Many tests tolerate departures in large samples thanks to the CLT; alternatively transform the data (log / Box-Cox) and use a parametric method.",
],
'statistics-16': [
"Linear Regression Fit",
"Fits y = ax + b by least squares and reports the slope, intercept and prediction.",
'📖 View the "Linear Regression Fit User Guide"',
"Slope a = (nΣxy − ΣxΣy) / (nΣx² − (Σx)²); intercept b = (Σy − aΣx) / n; prediction ŷ = a·x + b",
"The line y = ax + b is fitted to 5 pairs of (x, y) by least squares: the slope a comes from the ratio of the covariance of x and y to the variance of x, and the intercept b places the line through the sample means (x̄, ȳ). Substituting any x yields the prediction ŷ, for trend analysis and data modelling.",
"Predict X",
"Enter paired data and specify any x to predict y.",
"📚 In-depth: Statistical Power and Effect Size",
"Given the effect size, ",
" and α, compute the power (1−β).",
"Planning the assurance level of an experiment.",
"Low power risks missing a real effect.",
"Power estimation",
"With α=0.05, n=30 per group and d=0.5, power ≈0.48: too low, since real effects are easily missed; raising n to 64 per group gives power ≈0.80, meeting the usual target.",
"Larger effects give higher power",
"With d=0.8 and n=30, power ≈0.86, which is sufficient.",
"What is statistical power?",
"The probability of correctly rejecting the null hypothesis when a real effect exists (1−β); at least 0.8 is normally required.",
"How do α, n, d and power relate?",
"Any three determine the fourth; a design usually fixes α and the target power, then solves for the required n or the detectable effect d.",
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
    print('gen_stat_b4 done')
