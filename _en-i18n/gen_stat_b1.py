#!/usr/bin/env python3
# statistics batch1 (10 tools)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'statistics')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'statistics')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'binomial-cdf': [
"Cumulative Probability from Trials, Success Probability and Upper Bound",
"Enter the number of trials n, the success probability p and the upper bound x to find P(X≤x).",
"Binomial CDF Calculator",
"/ Binomial CDF Calculator",
'📖 View the "Cumulative Probability from Trials, Success Probability and Upper Bound User Guide"',
"Upper bound x",
"Left-tail probability of the binomial distribution.",
"📚 In-depth: Cumulative Probability of the Binomial Distribution",
"Cumulative probability of successes ≤x (or ≥x).",
'Acceptance probability of "at most k defectives" in quality control.',
"At most 5 successes",
"n=10, p=0.5, x=5: CDF=P(X≤5)=Σ_{0}^{5}C(10,k)0.5^10≈0.6230 (covering every outcome from 0 to 5).",
"At least 8",
"P(X≥8)=1−P(X≤7)≈1−0.9453=0.0547 (a rare event).",
"How do CDF and PMF differ?",
"PMF is the point probability P(X=k) and CDF the cumulative P(X≤k); they differ by a summation.",
"Why is ≤x commonly used?",
"Cumulative distributions are left-closed by convention, and the right-tail probability is obtained as 1−CDF(x−1), matching statistical tables.",
],
'binomial-pmf': [
"Probability of exactly k successes in n independent trials.",
"Binomial Probability Calculator",
"/ Binomial Probability",
'📖 View the "Binomial Probability Calculator User Guide"',
"X=k)=C(n,k)p^k(1−p)^(n−k). 10 shots with 3 hits at p=0.5 give 0.1172.",
"Number of successes k",
"10 shots with 3 hits at p=0.5 give 0.1172.",
"📚 In-depth: Probability Mass of the Binomial Distribution",
"Probability of exactly k successes in n independent Bernoulli trials.",
"Quality sampling, shooting accuracy, click conversion and other counts.",
"5 hits in 10 shots",
"n=10, p=0.5, k=5: C(10,5)=252; P=252×0.5^10=252/1024≈0.2461, so five hits in ten shots occur about 24.6% of the time.",
"Defect rate",
"n=20, p=0.1, k=0 (all conforming): P=0.9^20≈0.1216; k=2: C(20,2)×0.1²×0.9^18=190×0.01×0.1652≈0.3139.",
"How is C(n,k) computed?",
"Combination",
" C(n,k)=n!/(k!(n−k)!), the number of ways to place the k successes.",
"Relation to the ",
"?",
"When n is large, p small and λ=np moderate, the binomial is approximated by the Poisson: P≈e^−λ·λ^k/k!.",
],
'chi-square-test': [
"Degree of deviation between observed and expected values.",
"Chi-Square Test Calculator",
"/ Chi-Square Goodness of Fit",
"Chi-Square Goodness of Fit",
'📖 View the "Chi-Square Test Calculator User Guide"',
"χ² = Σ(O−E)²/E. df = number of categories − 1.",
"Observed values O (comma separated)",
"Expected values E (comma separated)",
"df = number of categories − 1.",
"📚 In-depth: Chi-Square Goodness-of-Fit / Independence Test",
"Compares observed frequencies with expected frequencies: χ²=Σ(O−E)²/E.",
"Independence tests on contingency tables and goodness-of-fit tests.",
"df=(rows−1)(columns−1) for looking up the critical value.",
"2×2 independence",
"Observed O=[60,40;30,70] (all row and column totals 100), expected E=50 in every cell: χ²=(10²+10²+20²+20²)/50=(100+100+400+400)/50=1000/50=20. With df=1 this far exceeds the critical value 3.84, so the association is significant.",
"Goodness of fit",
"100 trials expected 50/50 and observed 60/40: χ²=(10²+10²)/50=4, df=1, p≈0.045, significant at the critical level.",
"How are the expected frequencies set?",
"For independence tests E_ij = row total_i × column total_j / grand total; for fit tests allocate by the theoretical proportions. Any expected count below 5 should be pooled or handled with Yates correction.",
"What does a larger χ² mean?",
"A large χ² means the observed values deviate greatly from expectation, so the null hypothesis (independence or fit) is more likely to be rejected.",
],
'coefficient-of-variation': [
"Coefficient of Variation from Mean and Standard Deviation",
"Enter the mean μ and standard deviation σ to get the coefficient of variation.",
"Coefficient of Variation Calculator",
"/ Coefficient of Variation Calculator",
'📖 View the "Coefficient of Variation from Mean and Standard Deviation User Guide"',
"Dimensionless, so dispersion can be compared across units.",
"📚 In-depth: Coefficient of Variation (CV)",
"CV=σ/μ×100%, a dimensionless measure of dispersion.",
"Comparability across data with different units or very different means.",
"CV below 10% is stable, 10%-30% moderate and above 30% highly variable.",
"Comparing two groups",
"Group A with μ=100, σ=15 gives CV=15%; group B with μ=50, σ=12 gives CV=24%. B fluctuates more in relative terms even though its σ is smaller.",
"Investment view",
"A fund returning 8% a year with σ=12% has CV=150%; low return with high volatility calls for caution.",
"Why divide by the mean?",
" carries units, and dividing by the mean removes them, so dispersion can be compared across variables such as height in cm and weight in kg.",
"What if the mean is close to 0?",
"CV becomes distorted or even diverges, so do not use it then; switch to an absolute measure of dispersion.",
],
'cohens-d': [
"Cohen's d Effect Size Calculator",
"Standardized effect size for the difference between two group means.",
"/ Cohen's d (effect size)",
"Cohen's d (effect size)",
'📖 View the "Cohen\'s d Effect Size Calculator User Guide"',
"Cohen's d divides the difference between two group means by the pooled standard deviation s_p, giving an effect size in standard deviation units that removes the original scale so magnitudes can be compared across experiments: |d| of about 0.2 is small, 0.5 medium and 0.8 large. s_p is obtained by weighting the two standard deviations by their sample sizes.",
"|d| ≈ 0.2 / 0.5 / 0.8 counts as small / medium / large.",
"Standardized by the pooled standard deviation.",
"📚 In-depth: Cohen's d Effect Size",
"Standardizing the difference between two means: d=(m1−m2)/sp.",
"Judges how large the difference is in practice, not just whether it is significant.",
"d ≈ 0.2 small, 0.5 medium and 0.8 large effect.",
"Two group means",
"m1=85, m2=80, s1=s2=10, n1=n2=30: the pooled sp=√(((29×100)+(29×100))/58)=√(5800/58)=√100=10; d=(85−80)/10=0.5 (a medium effect).",
"Large effect",
"A difference of 16 with sp=10 gives d=1.6, a large effect with clear clinical and practical significance.",
"Effect size",
" and its relation to the p-value?",
"The p-value depends on ",
" (a large sample can render even a small difference significant); the effect size d measures the magnitude, and the two complement each other.",
"Pooled ",
" sp formula?",
"sp=√(((n1−1)s1²+(n2−1)s2²)/(n1+n2−2)), i.e. the square root of the pooled variance.",
],
'confidence-proportion': [
"Interval estimation of a population proportion.",
"Confidence Interval for a Proportion Calculator",
"/ Confidence Interval for a Proportion",
"Confidence Interval for a Proportion",
'📖 View the "Confidence Interval for a Proportion Calculator User Guide"',
"Number of successes x",
"60/100 at 95% gives an interval of about [0.504,0.696].",
"The approximation is reasonable when np≥5.",
"📚 In-depth: Confidence Interval for a Proportion",
"Sample proportion p=x/n, CI=p±z·√(p(1−p)/n).",
"Interval estimation for survey approval rates and pass rates.",
"The interval is widest at p=0.5 (the most conservative case).",
"Approval rate survey",
"Conservative estimate",
"p=0.5, n=1000: SE=√(0.25/1000)=0.0158, half-width ≈0.031, so the interval is about ±3.1%.",
"Why is the interval widest at p=0.5?",
"Because p(1−p) is maximized at 0.5, giving the largest variance and the widest interval; it is the usual basis for ",
" planning.",
"What if n is not large enough?",
"The normal approximation requires both np and n(1−p) to be at least 5; otherwise use the exact binomial (Clopper-Pearson) interval.",
"How to Use the Confidence Interval for a Proportion Calculator",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does the Confidence Interval for a Proportion Calculator do?",
"Confidence Interval for a Proportion Calculator: enter the number of successes and the sample size (or the sample proportion) to obtain the population proportion interval at a chosen confidence level under the normal approximation, for surveys and medical estimation.",
"How do I use the Confidence Interval for a Proportion Calculator?",
"What scenarios is the Confidence Interval for a Proportion Calculator best for?",
],
'correlation-coefficient': [
"Pearson Correlation Coefficient Calculator",
"Strength of the linear relationship between two variables.",
"/ Pearson Correlation Coefficient",
"Pearson Correlation Coefficient",
'📖 View the "Pearson Correlation Coefficient Calculator User Guide"',
"The Pearson correlation coefficient r divides the sum of the cross-products of deviations by the square root of the product of the sums of squared deviations, measuring the strength and direction of the linear association: r ranges from −1 to 1, a larger absolute value means a stronger linear relationship and the sign shows whether the correlation is positive or negative. r = 0 means no linear correlation.",
"The closer |r| is to 1, the stronger the linear correlation.",
"📚 In-depth: Pearson Correlation Coefficient",
"Linear correlation between two variables: r=Σ(x−x̄)(y−ȳ)/√(Σ(x−x̄)²Σ(y−ȳ)²).",
"Determines the direction and strength of linear correlation (−1 to 1).",
"Correlation does not imply causation.",
"Strong positive correlation",
"x=[1,2,3,4], y=[2,4,5,7]: x̄=2.5, ȳ=4.5; Σ(x−x̄)(y−ȳ)=6.5 and √(Σ(x−x̄)²·Σ(y−ȳ)²)=√(5×14.75)=√73.75≈8.587; r≈6.5/8.587≈0.757 (a moderately strong positive correlation).",
"No correlation",
"r≈0 means no linear association, although a nonlinear relationship may still exist (check the plot).",
"Is r=0.8 considered strong?",
"As a rule of thumb |r|>0.7 is strong, 0.4-0.7 moderate and below 0.4 weak, though judgement also requires ",
" and domain knowledge.",
"Can correlation imply causation?",
"No. Ice cream sales correlate with drownings, yet both are driven by temperature: correlation is not causation.",
],
'correlation-r-squared': [
"Coefficient of Determination from the Correlation Coefficient",
"Enter the correlation coefficient r to get the coefficient of determination R².",
"Coefficient of Determination R² Calculator",
"/ Coefficient of Determination R² Calculator",
'📖 View the "Coefficient of Determination from the Correlation Coefficient User Guide"',
"Correlation coefficient r",
"R² is the proportion of variance explained.",
"📚 In-depth: Coefficient of Determination R²",
"R²=r², the proportion of variation in the dependent variable explained by the regression.",
"Evaluating the ",
" goodness of fit (0 to 1).",
"A high R² does not mean a good model (it may ",
"overfit",
"Regression explanatory power",
"r=0.757 gives R²=0.757²≈0.573, i.e. about 57.3% of the variation in y is explained linearly by x and the rest is residual.",
"Strong fit",
"r=0.95 gives R²=0.9025, so 90% of the variation is explained and the fit is excellent.",
"Is a larger R² always better?",
"On the training set R² rises as more predictors are added (even meaningless ones), so look at the adjusted R² or use cross-validation to avoid overfitting.",
"Can R² be negative?",
"R² can be negative when the model performs worse than simply predicting the mean, which means the model is useless.",
],
'cramers-v': [
"Cramér's V Calculator",
"Standardized effect size of association between categorical variables (2×2).",
"/ Cramér's V (association strength)",
"Cramér's V (association strength)",
'📖 View the "Cramér\'s V Calculator User Guide"',
"Cramér's V divides the chi-square statistic χ² by the sample size and the smallest dimension constraint, then takes the square root, standardizing chi-square to the 0-1 range to measure the association between two categorical variables: 0 means no association and 1 complete association, applicable to contingency tables of any size. This page computes it from the four frequencies of a 2×2 table.",
"For a 2×2 table min(r−1,c−1)=1.",
"V lies in [0,1]: the larger it is, the stronger the association.",
"📚 In-depth: Cramér's V Association Strength",
"Association strength in a contingency table: V=√(χ²/(n·min(r−1,c−1))).",
"Ranges from 0 to 1, standardized so different tables are comparable.",
"Used together with the ",
"chi-square test",
" to assess significance.",
"2×2 table",
"χ²=20, n=200, min(1,1)=1: V=√(20/200)=√0.1≈0.316, a moderate association.",
"Weak association",
"χ²=4, n=100: V=√(4/100)=0.2, a weak association.",
"How is V better than χ²?",
"χ² grows with ",
", whereas V is standardized by n and the dimensions, so association strength can be compared across tables.",
"Why is 1 the upper bound of V?",
"After dividing by n·min(r−1,c−1), perfect association gives V=1, so V always lies in [0,1].",
"How to Use Cramér's V Calculator",
"Computing statistical indicators, confidence intervals and sample sizes.",
"What does Cramér's V Calculator do?",
"Cramér's V Calculator: computes the Cramér's V effect size from the chi-square value of a contingency table together with sample size and degrees of freedom, measuring the association between two categorical variables for cross-tab analysis.",
"How do I use Cramér's V Calculator?",
"What scenarios is Cramér's V Calculator best for?",
],
'f-test-variance': [
"Tests whether two population variances are equal.",
"F-Test for Variances Calculator",
"/ F-test (homogeneity of variance)",
"F-test (homogeneity of variance)",
'📖 View the "F-Test for Variances Calculator User Guide"',
"p = 2·min(right tail, left tail).",
"Sample 1 variance s₁²",
"Sample 2 variance s₂²",
"Sample 1 size n₁",
"Sample 2 size n₂",
"The larger variance is usually used as the numerator.",
"Two-sided p = 2·min(right tail, left tail).",
"📚 In-depth: F-Test (Variance Ratio)",
"Testing homogeneity of two ",
"sample variances",
": F = variance₁ / variance₂ (the two inputs on this page are the sample variances s₁² and s₂²).",
"In ANOVA it is the ratio of between-group to within-group mean squares.",
"The F distribution has degrees of freedom (n1−1, n2−1).",
"Homogeneity of variance",
"Sample 1 variance 12 and sample 2 variance 10: F = 12/10 = 1.2, df=(n1−1, n2−1). The closer F is to 1, the more it suggests the two ",
"population variances",
" are equal.",
"Between-group MSB=30 and within-group MSW=15: F=2.0 with df=(2,27); the table critical value is about 3.35, so it is not significant.",
"Why put the larger variance in the numerator?",
"Putting the larger variance in the numerator keeps F≥1 for comparison with a one-tailed critical value, while homogeneity of variance tests use both tails.",
"Is the F-test sensitive to normality?",
"Yes. Homogeneity of variance tests are sensitive to non-normality, so the more robust Levene test may be preferable.",
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
    print('gen_stat_b1 done')
