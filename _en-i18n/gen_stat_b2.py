#!/usr/bin/env python3
# statistics batch2 (11 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'statistics')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'statistics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'geometric-mean': [
"The n-th root of the product, suited to ratio data.",
"Geometric Mean Calculator",
"/ Geometric Mean",
'📖 View the "Geometric Mean Calculator User Guide"',
"Suited to averaging growth rates.",
"📚 In-depth: Geometric Mean",
"The n-th root of the product of n values: g=(Πx_i)^(1/n).",
"Growth rates, ratios and log-normal data.",
"More robust to extreme values than the arithmetic mean.",
"Average growth rate",
"Annual growth rates of 5%, 10% and −2% convert to 1.05, 1.10 and 0.98; g=(1.05×1.10×0.98)^(1/3)≈(1.1319)^(0.333)≈1.0423, i.e. about 4.23% compound annual growth.",
"Simple data",
"Why use the geometric mean for growth rates?",
"Growth rates compound multiplicatively, so the geometric mean gives the compound average; the arithmetic mean overstates it (a rise of 50% followed by a fall of 50% is not a zero return).",
"What about negative values or zero?",
"The geometric mean requires every value to be positive; with zeros or negatives it is undefined (or requires shifting the data). For ratios, take logarithms, average them and exponentiate.",
],
'harmonic-mean': [
"The reciprocal of the arithmetic mean of the reciprocals, suited to rates.",
"Harmonic Mean Calculator",
"/ Harmonic Mean",
"Harmonic Mean",
'📖 View the "Harmonic Mean Calculator User Guide"',
"Round-trip average speed uses the harmonic mean.",
"📚 In-depth: Harmonic Mean",
"n/Σ(1/x_i), used for rates, average prices and other reciprocal averages.",
"Average speed over legs of equal distance travelled at different ",
"speeds",
"Harmonic mean ≤ geometric mean ≤ arithmetic mean.",
"Round-trip average speed",
"60 km/h outbound and 40 km/h on the return (equal distances): H=2/(1/60+1/40)=2/(0.01667+0.025)=2/0.04167=48 km/h (not 50).",
"Average of two rates",
"Why is a round trip not the arithmetic mean?",
"Slower legs take longer and carry more weight; the harmonic mean weights by time and therefore reflects the true total duration.",
"Is the harmonic mean the smallest?",
"Yes. For positive values H≤G≤A always holds, and extreme values (very small denominators) pull the harmonic mean down.",
],
'independent-t-test': [
"Independent Two-Sample t-Test Calculator",
"Comparing the means of two independent groups, assuming equal variances.",
"/ Independent Samples t-Test (pooled variance)",
"Independent Samples t-Test (pooled variance)",
'📖 View the "Independent Two-Sample t-Test Calculator User Guide"',
"The independent two-sample t statistic divides the difference between the two group means by the pooled standard error to test whether the population means differ significantly. The pooled variance s_p² is the weighted average of the two variances by sample size, with df = n₁ + n₂ − 2. The larger |t| is, the stronger the evidence against the null hypothesis of equal group means.",
"The two groups must have equal variances.",
"Unequal variances call for the Welch correction.",
"📚 In-depth: Independent Samples t-Test",
"Difference between two independent group means: t=(m1−m2)/√(sp²(1/n1+1/n2)).",
"df=n1+n2−2 decides whether the difference is significant.",
"Assumes homogeneity of variance (otherwise use Welch).",
"Comparing two groups",
"m1=85, m2=80, sp=10, n1=n2=30: t=5/√(100×(2/30))=5/√6.667=5/2.582≈1.936, df=58. Significance requires |t| above the critical value of 2.00, so this case is borderline.",
"A larger difference",
"With m1−m2=10: t=10/2.582≈3.87, df=58, significant (p<0.001).",
"What if the variances are unequal?",
"Use Welch's t-test (with the Welch-Satterthwaite df correction), which is more robust and the default in most software.",
"How do t-tests and z-tests differ?",
"Use the t-test for small samples when σ is unknown (relying on s and the t distribution); use z when σ is known or the sample is large.",
],
'iqr': [
"📊 Interquartile Range IQR",
"Computes the quartiles and interquartile range of a data set for outlier detection.",
'📖 View the "Interquartile Range IQR User Guide"',
"IQR = Q3 − Q1; outlier lower bound = Q1 − 1.5×IQR; outlier upper bound = Q3 + 1.5×IQR",
"The interquartile range IQR is the difference between the third and first quartiles, describing the span of the middle 50% of the data and proving more robust than the range. Under Tukey's 1.5×IQR rule, observations below Q1−1.5×IQR or above Q3+1.5×IQR count as outliers, which is how boxplot whiskers and outliers are identified.",
"Outlier bounds: [Q1 − 1.5·IQR, Q3 + 1.5·IQR]",
"Data points outside the bounds can be treated as outliers.",
"📚 In-depth: Interquartile Range (IQR)",
"IQR=Q3−Q1, the span of the middle 50% of the data.",
"Boxplots and outlier detection (the 1.5×IQR rule).",
"More robust than the range when the data are skewed.",
"Data [1..9]",
"Q1=25th percentile=3, Q3=75th percentile=7: IQR=4. The outlier bounds run from Q1−1.5IQR=−3 to Q3+1.5IQR=13, so there are no outliers.",
"Skewed data",
"[1,2,3,4,5,6,7,8,100]: Q1=3, Q3=7, IQR=4; 100 exceeds the upper bound of 13 and is flagged as an outlier.",
"Where does the 1.5×IQR rule come from?",
"Tukey's rule of thumb, standard for boxplots and roughly ±2.7σ under normality, though not a strict ",
"statistical test",
"IQR versus the ",
"IQR is quantile-based and resistant to outliers; the standard deviation uses every value and is heavily influenced by extremes.",
],
'linear-regression': [
"y = a + b·x (least squares)",
"Fits the best straight line to the data.",
"Least-Squares Regression Calculator",
"/ Simple Linear Regression",
"Simple Linear Regression",
'📖 View the "Least-Squares Regression Calculator User Guide"',
"Least squares: b=Σ(x−x̄)(y−ȳ)/Σ(x−x̄)².",
"📚 In-depth: Simple Linear Regression",
"Fitting y=a+bx: b=(nΣxy−ΣxΣy)/(nΣx²−(Σx)²).",
"Prediction and slope significance.",
"Residual diagnostics verify the linearity assumption.",
"Fitting a line",
"x=[1,2,3,4], y=[2,4,5,7]: b=(4×50−10×18)/(4×30−100)=(200−180)/(120−100)=20/20=1.0; a=(18−1.0×10)/4=2.0; y=2+1.0x. (With this data b=1.0 and a=2.0.)",
"What does the slope b mean?",
"For each unit increase in x, y changes by b units on average; its significance and ",
" come from a t-test.",
"How do R² and regression relate?",
"In simple regression R²=r², so the explanatory power is the square of the ",
"correlation coefficient",
".",
"How to Use the Least-Squares Regression Calculator",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does the Least-Squares Regression Calculator do?",
"Least-Squares Regression Calculator: enter paired (x, y) data to fit the best-fitting line and obtain the slope, intercept and coefficient of determination R², for trend forecasting and modelling relationships between variables.",
"How do I use the Least-Squares Regression Calculator?",
"What scenarios is the Least-Squares Regression Calculator best for?",
"Simple linear regression y=a+b·x fits a straight line by least squares, where b is the slope (the average change in y per unit increase in x) and a is the intercept.",
"Results support prediction and trend assessment; goodness of fit should be judged together with the correlation coefficient and R², and extrapolation beyond the observed range is unreliable.",
],
'mean-absolute-deviation': [
"Mean Absolute Deviation from a Series of Values",
"Enter several values (separated by commas or spaces) to get the mean absolute deviation.",
"Mean Absolute Deviation Calculator",
"/ Mean Absolute Deviation Calculator",
'📖 View the "Mean Absolute Deviation from a Series of Values User Guide"',
"More robust to outliers than the variance.",
"📚 In-depth: Mean Absolute Deviation (MAD)",
"MAD=Σ|x−μ|/n, the average distance.",
"Easier to interpret than the ",
" (same units as the data).",
"A robust measure of dispersion.",
"Data [2,4,6,8]",
"μ=5; MAD=(|2−5|+|4−5|+|6−5|+|8−5|)/4=(3+1+1+3)/4=2, so each value lies 2 units from the mean on average.",
"Versus the standard deviation",
"Here σ=√5≈2.236, slightly above MAD=2 because extreme values are not magnified by squaring.",
"How do MAD and the standard deviation differ?",
"MAD averages absolute deviations while the standard deviation squares them and then takes the root (magnifying outliers); MAD is more robust and easier to interpret.",
" absolute deviation?",
"There is also MAD=median(|x−median|), which resists outliers even more; the two are different measures, so keep them apart.",
"How to Use Mean Absolute Deviation from a Series of Values",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does Mean Absolute Deviation from a Series of Values do?",
"Enter a set of values and compute MAD = Σ|xᵢ − x̄|/n to measure average dispersion, for forecast error and robustness assessment.",
"How do I use Mean Absolute Deviation from a Series of Values?",
"What scenarios is Mean Absolute Deviation from a Series of Values best for?",
"Mean absolute deviation MAD=mean(|xᵢ−x̄|) is the average of the absolute deviations from the mean, measuring how spread out the data are.",
"How it differs from the standard deviation",
"MAD is less sensitive to outliers than the standard deviation (it does not square) and stays in the original units, which makes it easier to grasp. The units match the source data.",
],
'normal-cdf': [
"Normal Distribution CDF Calculator",
"Standard normal cumulative distribution function (erf approximation).",
"/ Normal Cumulative Probability",
"Normal Cumulative Probability",
'📖 View the "Normal Distribution CDF Calculator User Guide"',
"The standard normal cumulative distribution function Φ(z) gives the probability that a standard normal variable is less than or equal to z, i.e. the area under the curve to the left. Any normal distribution is first standardized as z = (x − μ)/σ and the cumulative probability then follows from Φ(z). Used for normal tables and quantile assessment.",
"Standard score z",
"The erf approximation is accurate to about 1e-7.",
"📚 In-depth: Cumulative Probability of the Normal Distribution",
"Finds P(Z≤z) or interval probabilities.",
"One-tailed probability",
"z=1: Φ(1)≈0.8413, i.e. 84.13% of the data lie below mean+1σ. z=1.96 gives ≈0.9750.",
"Interval probability",
"P(−1<Z<1)=Φ(1)−Φ(−1)=0.8413−0.1587=0.6826 (the 68.3% rule); P(−1.96<Z<1.96)≈95%.",
"What is erf?",
"The error function used to express the normal CDF; most languages and calculators provide it, so Φ(z) can be used directly.",
"Why memorize 1.96 and 2.58?",
"They are the two-tailed critical z values for 95% and 99% confidence, used constantly in tables and tools.",
],
'odds-ratio': [
"Strength of association between exposure and outcome in a 2×2 table.",
"Odds Ratio Calculator",
"/ Odds Ratio (OR)",
"Odds Ratio (OR)",
'📖 View the "Odds Ratio Calculator User Guide"',
"OR>1 means the risk is elevated.",
"📚 In-depth: Odds Ratio (OR)",
"OR=(a·d)/(b·c), the association strength in case-control studies.",
"OR=1 means no association, above 1 higher risk and below 1 a protective effect.",
"For rare diseases OR≈RR.",
"Exposure and disease",
"a=40 (exposed with the disease), b=20 (exposed without), c=30 (unexposed with the disease), d=60 (unexposed without): OR=(40×60)/(20×30)=2400/600=4. The odds in the exposed group are four times those in the control group.",
"Protective factor",
"OR=0.5 means exposure halves the odds (a protective effect).",
"How do OR and RR differ?",
"RR compares incidence rates (cohort studies) while OR compares odds (case-control studies). For rare diseases OR≈RR; for common ones OR overstates RR.",
"Can OR be read directly as a risk multiple?",
"Only approximately for rare diseases; otherwise OR exceeds RR and must be interpreted with care.",
],
'one-sample-t-test': [
"When the population standard deviation is unknown, the sample standard deviation is used to test departures of the mean.",
"One-Sample t-Test Calculator",
"/ One-Sample t-Test",
"One-Sample t-Test",
'📖 View the "One-Sample t-Test Calculator User Guide"',
"Use a t-test when σ is unknown.",
"📚 In-depth: One-Sample t-Test",
"Tests whether the sample mean equals a known value: t=(x̄−m0)/(s/√n).",
"df=n−1; the t distribution applies to small samples.",
"Judges whether the deviation is statistically meaningful.",
"Testing the mean",
"x̄=105, m0=100, s=15, n=25: t=5/(15/5)=5/3≈1.667, df=24. The critical value t(0.05,24)≈2.064 is not reached, so the result is not significant (p≈0.108).",
"A significant case",
"With x̄=112: t=12/3=4.0, far beyond the critical value and significant (p<0.001).",
"Why use t rather than z?",
"With σ unknown it is estimated by the sample s; in small samples the variability of s gives the t distribution heavier tails, making it more conservative than z.",
"How is the p-value obtained?",
"Look up the t distribution using t and df; the two-tailed p=2×P(T>|t|). This tool computes it with built-in erf and betai functions.",
],
'one-sample-z-test': [
"When the population standard deviation is known, tests whether the sample mean departs from a hypothesized value.",
"One-Sample z-Test Calculator",
"/ One-Sample z-Test",
'📖 View the "One-Sample z-Test Calculator User Guide"',
"Two-tailed p = 2(1−Φ(|z|)); at z=2 the two-tailed p≈0.046. Use the z-test when σ is known.",
"Two-tailed p = 2(1−Φ(|z|)); at z=2 the two-tailed p≈0.046 (H₀ correctly rejected).",
"Use the z-test when σ is known.",
"📚 In-depth: One-Sample z-Test",
"Testing the mean when σ is known: z=(x̄−m0)/(σ/√n).",
"Also common as a large-sample approximation.",
"p=2(1−Φ(|z|)) for two tails.",
"Testing the mean",
"x̄=105, m0=100, σ=15, n=25: z=5/(15/5)=1.667; p=2(1−Φ(1.667))≈2×0.0477≈0.095, which does not reach significance at 0.05.",
"Significant with a large sample",
"With n=100: z=5/(15/10)=3.333, p≈0.0009, highly significant.",
"How do z and t test results differ?",
"The z-test with known σ or large samples is more liberal; the t-test for unknown σ in small samples is more conservative, and the gap closes as n grows.",
"One-tailed or two-tailed?",
"Two-tailed by default (testing whether they are equal); with a directional hypothesis (> or <) use one tail and halve p.",
],
'one-way-anova': [
"Tests whether several group means differ significantly.",
"One-Way ANOVA Calculator",
"/ One-Way Analysis of Variance (ANOVA)",
"One-Way Analysis of Variance (ANOVA)",
'📖 View the "One-Way ANOVA Calculator User Guide"',
"One-way analysis of variance splits the total variation into between-group variation (caused by the factor) and within-group variation (random error): MS_between = SS_between/(k−1) and MS_within = SS_within/(N−k), with F as their ratio. A larger F means the between-group differences stand out more against the within-group noise, which tests whether several means are equal.",
"Group 3 mean",
"Group 3 standard deviation",
"Group 3 sample size",
"Compares the means of three or more groups.",
"Homogeneity of variance is a prerequisite.",
"📚 In-depth: One-Way Analysis of Variance",
"Comparing several means: F=MSB/MSW.",
"The null hypothesis is that all group means are equal.",
"Follow a significant result with pairwise comparisons (Tukey and others).",
"Comparing three groups",
"Between-group SSB and within-group SSW give MSB=SSB/dfB and MSW=SSW/dfW; with MSB=30 and MSW=15 the result is F=2.0, df=(2,27). The critical value F(0.05;2,27)≈3.35 is not reached, so it is not significant.",
"Significant",
"F=5.0 exceeds the critical value, so equality of means is rejected and at least one group differs.",
"What comes after a significant ANOVA?",
"Post-hoc tests (Tukey HSD, Bonferroni) locate which pair differs, guarding against false positives from multiple comparisons.",
"Does a large F always matter?",
"A large F with a small p means significant differences between groups, but only the effect size (η²) reflects practical importance.",
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
    print('gen_stat_b2 done')
