def main():
    # ---------------- irr-table (16) ----------------
    write('irr-table', build('irr-table', [
        "🏦 IRR Trial Table",
        "Enter the cash flows of each period and scan NPV at different discount rates to precisely locate the internal rate of return (the threshold where NPV turns from positive to negative)",
        "\"Enter the cash flows of each period and scan NPV at different discount rates to precisely locate the internal rate of return (the threshold where NPV turns from positive to negative)\" is professionally computed from the input parameters and outputs the result.",
        "📖 Read the \"IRR Trial Table User Guide\"",
        ": IRR is the discount rate that makes NPV = 0. In the scan table, the IRR lies between the two adjacent rows where NPV turns from positive to negative (or from negative to positive), and the tool computes it precisely with linear interpolation.",
        "📚 Deep dive: IRR Trial Table",
        "In investment decisions, scanning",
        "at multiple discount rates locates the threshold where NPV turns from positive to negative, that is,",
        "When comparing different projects, use the same set of cash flows to plot a trial table of NPV against the discount rate, giving an intuitive comparison of return levels.",
        "When doing project feasibility studies or comparing financing plans, compare IRR against the cost of capital or the benchmark return to judge whether the target is met.",
        "Trial table for the internal rate of return of a five-year cash flow",
        "Initial investment −100000 CNY, with year 1~5 cash flows of 25000, 30000, 35000, 30000 and 20000 CNY. At a discount rate of 8% NPV ≈ 12312 CNY (positive), and at 12% NPV ≈ −1414 CNY (negative), so the IRR lies between 8% and 12%; with linear interpolation IRR ≈ 8% + (12312 ÷ (12312 + 1414)) × 4% ≈ 11.6%, which is above the cost of capital, so the plan is feasible.",
        "Should I look at IRR or NPV?",
        "NPV directly gives the absolute amount of return, while IRR gives a relative rate convenient for comparing projects of different sizes. For mutually exclusive projects of very different sizes, prioritize NPV; to judge purely whether the rate of return meets a target, look at IRR. When cash flows alternate sign multiple times, IRR may not be unique, so NPV should govern.",
        "Why does the trial table scan multiple discount rates?",
        "IRR is defined as the discount rate that makes NPV zero and cannot be solved analytically in one step, so it must be trial-computed step by step: first find two adjacent discount rates where NPV has opposite signs, then approximate with linear interpolation. The finer the scan density, the more precise the located internal rate of return.",
    ]))

    # ---------------- npv-discount (21) ----------------
    write('npv-discount', build('npv-discount', [
        "🏦 NPV Discount Calculation",
        "Discounts each period to compute the net present value, showing the present value, discount factor and cumulative present value of each period, supporting continuous / annuity modes",
        "Core formulas (by input variable): 1÷(1+rate)^t+1",
        "📖 Read the \"NPV Discount Calculation User Guide\"",
        "Initial investment (CNY, period 0 outflow)",
        "Custom cash flows",
        "Equal annuity mode",
        "NPV > 0 the project is feasible; NPV < 0 the project is not feasible. The higher the discount rate, the lower the present value of the distant cash flows.",
        "📚 Deep dive: NPV Discount Calculation",
        "When evaluating an investment project or equipment purchase, discount each period's net cash flow at the discount rate to convert it to present value, and judge whether it",
        "is greater than zero.",
        "When comparing mutually exclusive plans, compute the cumulative present value at the same discount rate for each and choose the one with the higher net present value.",
        "For lease-versus-buy decisions and installment-receivable valuation, align the basis with the annuity or per-period discount mode before comparing side by side.",
        "Net present value of a five-year investment",
        "Initial investment 100000 CNY, with year 1~5 net cash flows of 25000, 30000, 35000, 30000 and 20000 CNY, discounted at 8%. The present value factors 1/(1.08)^t are 0.9259, 0.8573, 0.7938, 0.7350 and 0.6806 in turn; the total present value is about 25000×0.9259 + 30000×0.8573 + 35000×0.7938 + 30000×0.7350 + 20000×0.6806 = 23148 + 25719 + 27783 + 22050 + 13612 = 112312 CNY; net present value NPV = 112312 − 100000 = 12312 CNY, greater than zero, so the plan is feasible.",
        "What discount rate should be used?",
        "The discount rate can reference the firm's weighted average cost of capital (WACC), an industry benchmark return, or the opportunity cost of capital; the higher the risk, the larger the value. When comparing a batch of plans, the same discount rate must be used for comparability.",
        "What is the difference between annuity mode and per-period mode?",
        "Annuity mode assumes each period's cash flow is equal, using the",
        "annuity present value",
        "factor P/A(r,n)=(1−(1+r)^−n)/r to discount in one step; per-period mode takes each cash flow individually, suiting irregular amounts. Results should be governed by per-period mode, with annuity mode only for equal-payment deposit estimates.",
    ]))

    # ---------------- ratio-analysis (20) ----------------
    write('ratio-analysis', build('ratio-analysis', [
        "📊 Financial Ratio Analysis",
        "Enter key data from the balance sheet and income statement to automatically compute solvency, operating and profitability ratios and give an assessment",
        "\"Enter key data from the balance sheet and income statement to automatically compute solvency, operating and profitability ratios and give an assessment\" is professionally computed from the input parameters and outputs the result.",
        "📖 Read the \"Financial Ratio Analysis User Guide\"",
        "📚 Deep dive: Financial Ratio Analysis",
        "Before credit approval or supplier credit granting, use",
        "the quick ratio",
        "and the debt-to-asset ratio",
        "to assess the firm's short-term and long-term solvency.",
        "In operational review meetings, use",
        "inventory turnover",
        "and accounts receivable turnover to measure asset operating efficiency and locate slow-moving inventory or collection risk.",
        "In post-investment management or annual report interpretation, use",
        "and return on equity (ROE) to assess earnings quality and shareholder returns.",
        "A typical set of financial statement ratio calculations",
        "Current assets of 2 million CNY, inventory of 500000 CNY and current liabilities of 1 million CNY give current ratio = 200 ÷ 100 = 2.0 and quick ratio = (200 − 50) ÷ 100 = 1.5; a quick ratio of at least 1 is generally considered safer. If annual revenue is 8 million CNY and average accounts receivable is 1.6 million CNY, accounts receivable turnover = 800 ÷ 160 = 5 times, and the average collection period ≈ 365 ÷ 5 = 73 days. If net profit is 800000 CNY and average net assets are 4 million CNY, ROE = 80 ÷ 400 = 20%.",
        "Is a high current ratio always safe?",
        "Not necessarily. A high current ratio may simply mean inventory or accounts receivable have piled up; what can actually repay debts immediately is quick assets (current assets minus inventory). You should judge it together with the quick ratio, the cash ratio, and the aging of receivables and inventory turnover, avoiding liquidity risk being masked by inflated current assets.",
        "Does a high ROE mean the company is good?",
        "A high ROE may come from high profitability, or from high leverage (a lot of borrowing amplifying shareholder returns). DuPont analysis can decompose it into net profit margin × total asset turnover × equity multiplier, distinguishing operating efficiency from returns built on debt, and guarding against understated solvency risk.",
    ]))


if __name__ == '__main__':
    main()
