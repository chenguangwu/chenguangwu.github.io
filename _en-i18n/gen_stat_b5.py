#!/usr/bin/env python3
# statistics batch5 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'statistics')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'statistics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'statistics-4': [
"Confidence Interval Estimation",
"Computes the confidence interval of a population mean from the sample mean, standard deviation and sample size.",
'📖 View the "Confidence Interval Estimation User Guide"',
"CI = x̄ ± z · s / √n, with z inverted from the confidence level by the normal approximation (two-sided)",
"The confidence interval for a mean is centred on the sample mean x̄ plus or minus the z value times the standard error s/√n. The z value is inverted from the confidence level: taking the tail probability α = (1 − cl/100)/2 in the inverse standard normal approximation, 95% gives z ≈ 1.96 and 99% gives z ≈ 2.576. It applies to large samples or when the population standard deviation is known.",
"Use the z distribution for large samples or when the population standard deviation is known.",
"📚 In-depth: Z-Score Standardization",
"z=(x−μ)/σ turns a value into a standard score.",
"Comparison across units and outlier detection (|z|>3).",
"After standardization the mean is 0 and the ",
"exam score",
"x=115, μ=100, σ=15: z=1.0, i.e. one standard deviation above the mean (ahead of about 84% of test takers).",
"Outlier detection",
"z=3.2 lies beyond the usual ±3σ bounds and is flagged as a potential outlier.",
"What level is z=2?",
"It is 2σ above the mean, ahead of about 97.7% of the data under normality (upper tail 2.3%).",
"What does standardization achieve?",
"It removes units so data from different distributions can be compared, such as z-scores for height in cm against weight in kg.",
],
'statistics-5': [
"Sample Size Estimation",
"Estimates the minimum sample size required for a given error, confidence level and population standard deviation.",
'📖 View the "Sample Size Estimation User Guide"',
"Mean estimation n = ⌈(z·σ / e)²⌉; proportion estimation n = ⌈z²·p(1−p) / e²⌉",
"After inverting z from the confidence level, the minimum sample size is estimated as n = (z·σ/e)² for a mean, where σ is the estimated population standard deviation and e the tolerated error, and as n = z²·p(1−p)/e² for a proportion, where p is the expected proportion. Results are rounded up to whole observations for planning samples in surveys and experiments.",
"Tolerated error",
"Estimated population standard deviation",
"Proportion estimate",
"n = (Z · σ / ME)² (mean)",
"n = Z² · p(1−p) / ME² (proportion)",
"Results are rounded up.",
"📚 In-depth: Confidence Level and Critical Values",
"Looks up the critical z or t value from the confidence level.",
"The interval widens as the confidence level rises.",
"95% critical value",
"Two-tailed 95% corresponds to z=1.96 (2.5% in each tail); 99% corresponds to z=2.576 (0.5% per tail).",
"The trade-off",
"Raising confidence to 99% widens the interval (more conservative but vaguer), a trade-off between precision and assurance.",
"Is a higher confidence level always better?",
"A higher level means a wider and less precise interval; 95% is the conventional balance, with 99% or 90% used in specific fields.",
"How do z and t critical values differ?",
"Small samples or unknown σ call for t critical values (which vary with df and run slightly above z); with large samples t≈z.",
],
'statistics-7': [
"Skewness and Kurtosis",
"Computes the skewness and kurtosis of a data distribution.",
'📖 View the "Skewness and Kurtosis User Guide"',
"Skewness g₁ = m₃ / m₂^1.5; excess kurtosis = m₄ / m₂² − 3, where mₖ = Σ(xᵢ − x̄)ᵏ / n",
"Distribution shape is measured with population central moments: skewness g₁ = m₃/m₂^1.5, positive for right skew (a long tail to the right) and negative for left skew; excess kurtosis = m₄/m₂² − 3, positive when the distribution is more peaked and heavy-tailed than normal and negative when flatter. mₖ is the k-th central moment divided by n. This page computes population moments for exactly 10 observations.",
"Data 8",
"Data 9",
"Data 10",
"Excess kurtosis = m₄ / m₂² − 3",
"Skewness above 0 means right skew and below 0 left skew; kurtosis above 0 means sharper than normal.",
"📚 In-depth: Skewness and Kurtosis",
"Reports skewness (asymmetry) alongside excess kurtosis (tail weight).",
"Diagnoses the shape of a distribution.",
"Normal: skewness 0 and excess kurtosis 0.",
"Shape diagnosis",
"Skewness ≈0.8 (right-skewed) with excess kurtosis ≈0.5 (slightly peaked) means the distribution trails off to the right and is a touch sharper than normal.",
"Heavy tails",
"Excess kurtosis above 0 means the tails are heavier than normal and the extreme-value risk higher, as is common in finance.",
"Why subtract 3 to get excess kurtosis?",
"Normal kurtosis equals 3, so excess kurtosis = kurtosis − 3 puts normality at 0, making it easy to spot heavy tails (>0) or light tails (<0).",
"Can skewness and kurtosis identify a distribution?",
"Not uniquely, since they only describe moment features; combine them with QQ plots and goodness-of-fit tests.",
],
'statistics': [
"Normal Distribution Probability",
"Computes interval probabilities under a normal distribution given the mean, standard deviation and lower and upper bounds.",
'📖 View the "Normal Distribution Probability User Guide"',
"P(a ≤ X ≤ b) = [Φ((b−μ)/σ) − Φ((a−μ)/σ)] × 100%, where Φ is the standard normal cumulative distribution function",
"The bounds b and a are standardized to (b−μ)/σ and (a−μ)/σ and the difference of their standard normal cumulative probabilities gives the area under the normal curve over [a, b] (multiplied by 100 for a percentage). Entering a very large negative lower bound such as −1e9 approximates negative infinity and yields P(X ≤ b). The probability outside the interval is 1 minus this value.",
"Lower bound",
"Upper bound",
"Use a very large negative lower bound to approximate -∞.",
"📚 In-depth: Interval Probability of the Normal Distribution",
"Computes P(a<X<b)=Φ((b−μ)/σ)−Φ((a−μ)/σ).",
"The share of product quality measurements falling inside specification.",
"μ=0, σ=1 gives the standard normal.",
"±1σ interval",
"μ=0, σ=1, a=−1, b=1: Φ(1)−Φ(−1)=0.8413−0.1587=0.6826, i.e. 68.3% of the observations lie inside the interval.",
"Specification limits",
"μ=100, σ=5 and specification [90,110]: z1=−2, z2=2; P≈Φ(2)−Φ(−2)=0.9545, so about 95.5% conform.",
"Why use ±1/±2/±3σ so often?",
"Under normality they cover 68.3%, 95.4% and 99.7% respectively (the empirical rule), a quick way to gauge the normal range of variation.",
"Can it be applied to non-normal data?",
"No. The proportions then depart from the empirical values, so use the actual distribution or Chebyshev's inequality (at least 1−1/k²).",
],
'stddev-list': [
"Sample Standard Deviation from a Series of Values",
"Enter several values (separated by commas or spaces) to get the sample standard deviation.",
"Sample Standard Deviation Calculator",
"/ Sample Standard Deviation Calculator",
'📖 View the "Sample Standard Deviation from a Series of Values User Guide"',
"The standard deviation shares the units of the raw data.",
"📚 In-depth: Sample Standard Deviation",
"The most widely used measure of dispersion.",
"It keeps the original units, unlike the variance.",
"Data [2,4,6,8]",
"Consistency",
"[10,10,10,10]: s=0, because there is no variation at all.",
": which to use?",
"Variance suits formulas (such as ANOVA); the ",
" shares the units of the data and is easier to interpret, so report the standard deviation.",
"n−1 or n?",
"Use n−1 for sample estimates (unbiased); use n only when the data form the complete population (see ",
"population variance",
],
't-score': [
"t Value from Sample Mean, Hypothesized Mean and Standard Deviation",
"Enter the sample mean x̄, hypothesized mean μ, standard deviation s and sample size n to get the t statistic.",
"t Statistic Calculator",
"/ t Statistic Calculator",
'📖 View the "t Value from Sample Mean, Hypothesized Mean and Standard Deviation User Guide"',
"Hypothesized mean μ",
"The core quantity of the one-sample t-test.",
"📚 In-depth: t Score (One Sample)",
"t=(x̄−μ)/(s/√n), standardization for one sample.",
"The core quantity for testing means with small samples.",
"Look up the t distribution using df=n−1.",
"Testing the mean",
"Large t",
"With x̄=120: t=20/3≈6.67, far beyond the critical value and significant.",
"t scores versus z scores?",
"The form is identical, but t uses the sample s and follows the heavier-tailed t distribution, whereas z uses a known σ and follows the normal.",
"What does df do?",
"df sets the shape of the t distribution: small df gives thicker tails and larger critical values, making the test more conservative.",
],
't': [
"t-Test Statistic",
"Computes the one-sample t statistic to test the difference between the sample mean and a hypothesized mean.",
'📖 View the "t-Test Statistic User Guide"',
"t = (x̄ − μ₀) / (s / √n); degrees of freedom df = n − 1",
"The one-sample t statistic measures how far the sample mean x̄ departs from the hypothesized population mean μ₀ using the standard error s/√n as yardstick. A larger |t| means stronger evidence that the sample mean differs from the hypothesized value, and df = n − 1 is used to look up critical values of the t distribution. The raw difference x̄ − μ₀ is reported as well.",
"Hypothesized population mean",
"The larger |t| is, the stronger the evidence against the null hypothesis.",
"📚 In-depth: t Statistic (One Sample)",
"Hypothesis testing",
" relies on this statistic.",
"Outputs the t value and the degrees of freedom.",
"The test",
"|t| below the critical value t(0.05,24)=2.064 means the null hypothesis is not rejected (the difference is not significant).",
"How do t and p relate?",
"The further |t| exceeds the critical value, the smaller p becomes; t and df determine p uniquely.",
"Why is df equal to n−1?",
"Estimating s consumes one degree of freedom (through x̄), leaving df=n−1.",
],
'variance-list': [
"Sample Variance from a Series of Values",
"Enter several values (separated by commas or spaces) to get the sample variance.",
"/ Sample Variance Calculator",
'📖 View the "Sample Variance from a Series of Values User Guide"',
"Sample variance uses the denominator n−1 (unbiased).",
"📚 In-depth: Variance (Sample)",
"Dispersion measured in squared units.",
" interconverts with it.",
"Data [2,4,6,8]",
"x̄=5; s²=(9+1+1+9)/3=20/3≈6.667 (standard deviation s≈2.582).",
"Zero variance",
"Why does variance square the deviations?",
"Squaring stops positive and negative deviations cancelling out and penalizes outliers, but it also squares the units, which is why the root is usually taken to return to the standard deviation.",
"Sample or population?",
"This tool uses n−1 (",
"sample variance",
"); for the ",
"population variance",
" please use the population variance tool instead.",
],
'z-score-calc': [
"Z-Score Calculator",
"How many standard deviations a value lies from the mean.",
"/ Standard Score Z",
"Standard Score Z",
'📖 View the "Z-Score Calculator User Guide"',
"A z-score subtracts the mean μ from the raw value x and divides by the standard deviation σ, giving the distance from the mean in standard deviations. z > 0 lies above the mean and z < 0 below it; z-scores are used for standardization and outlier detection, where |z| > 2 or 3 is treated as unusual.",
"📚 In-depth: Computing Z-Scores",
"z=(x−μ)/σ standardizes a single value.",
"Outlier detection and comparison across distributions.",
"|z|>3 is usually judged anomalous.",
"x=190cm, μ=170, σ=10: z=2.0, i.e. 2σ above the mean (ahead of about 97.7% of observations).",
"A low value",
"x=140: z=−3.0, three standard deviations below the mean, which may indicate an anomaly or a distinct subgroup.",
"Can z-scores be negative?",
"Yes, they indicate values below the mean, while |z| gives the distance.",
"Should σ be the sample or population value?",
"Use the population σ when the parameters are known; under sampling use the sample s, which strictly speaking gives a t score.",
],
'z': [
"Z-Score Calculator with Percentile",
"Converts a raw score into a standard z-score and reports the percentile.",
'📖 View the "Z-Score Calculator User Guide"',
"Z = (x − μ) / σ; percentile = Φ(Z) × 100%; distance from the mean = |Z| standard deviations",
"The z-score standardizes a raw score x within its distribution by subtracting the mean μ and dividing by the standard deviation σ, giving the distance from the mean in standard deviations. The standard normal cumulative distribution Φ(Z) then converts it into a percentile rank, the share of data below that value. Z > 0 lies above the mean and Z < 0 below, so data from different distributions can be compared directly.",
"Population mean",
"Population standard deviation",
"The percentile Φ(Z) is approximated with the normal cumulative distribution function",
"Z>0 means above the mean and Z<0 below the mean.",
"📚 In-depth: Standard Normal Cumulative Probability",
"Computes P(Z<z)=Φ(z)×100 (",
"the left-tail area under the standard normal.",
"Φ(1)≈0.8413, i.e. about 84.13% of the data fall below z=1.",
"Φ(2.58)≈0.9951, so about 99.5% fall below this value (upper tail only 0.49%).",
"How does Φ(z) compare with table lookups?",
"Φ(z) is the standard normal CDF, available from tables and software alike; this tool computes it directly with a built-in erf.",
"How is the right tail found?",
"P(Z>z)=1−Φ(z), and both tails give 2(1−Φ(|z|)).",
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
    print('gen_stat_b5 done')
