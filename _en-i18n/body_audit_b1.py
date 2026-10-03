def main():
    # ---------------- audit-sample (14) ----------------
    write('audit-sample', build('audit-sample', [
        "🎲 Audit Sample Size Determination",
        "Compute the sample size for attribute sampling and variable sampling from the desired reliance, tolerable error and expected error",
        "📖 Read the \"Audit Sample Size Determination User Guide\"",
        "📚 Deep dive: Audit Sample Size Determination",
        "In a financial statement audit, for internal control testing (attribute sampling), determine how many transactions to draw to evaluate whether the deviation rate is acceptable.",
        "For substantive detail testing (variable sampling), compute the sample size from the tolerable error and the expected population deviation, controlling the risk of incorrect inference.",
        "When planning annual audit workload and staffing, use",
        "to back-derive the inspection hours, avoiding insufficient sampling that leaves the audit evidence inadequate.",
        "Attribute sampling",
        "Set the risk of over-reliance at 5%, the tolerable deviation rate at 5% and the expected population deviation rate at 1%. Consulting the attribute sampling sample size table (risk coefficient method): a 5% risk corresponds to a risk coefficient of about 3.0, so sample size n = risk coefficient ÷ tolerable deviation rate = 3.0 ÷ 5% = 60 items; if the expected deviation rises to 2%, the risk coefficient rises to 4.8, giving n = 4.8 ÷ 5% ≈ 96 items. The higher the expected deviation, the larger the sample required.",
        "How do you choose between attribute sampling and variable sampling?",
        "Attribute sampling focuses on \"whether a deviation exists\" (such as a missing approval or incomplete voucher), producing a deviation rate, and is used for internal control testing; variable sampling focuses on \"how large the misstatement is\" (such as overstated inventory cost), producing a misstatement amount range, and is used for substantive detail testing. The two have different sample size formulas and should match their respective test objectives.",
        "What happens if the tolerable error is set too large?",
        "The larger the tolerable error (or deviation rate), the smaller the required sample and the lower the inspection workload, but the precision of the audit conclusion also drops, which may let material misstatements slip through. It should be set below the materiality level of the financial statements and coordinated with the risk of detection and the risk of material misstatement under the audit risk model, and must not be loosened purely to save effort.",
    ]))

    # ---------------- depreciation-compare (24) ----------------
    write('depreciation-compare', build('depreciation-compare', [
        "📉 Depreciation Method Comparison",
        "Compares the straight-line method, the double-declining balance method and the sum-of-the-years'-digits method, showing the depreciation and book value of each year",
        "Core formulas (by input variable): depreciable×(life-y+1)÷sumYears; max(0,(bvD-salvage)÷remYears); m.dep÷maxDep×100",
        "📖 Read the \"Depreciation Method Comparison User Guide\"",
        ": (cost - salvage value) / useful life, the same depreciation amount each year",
        "Double-declining balance method",
        ": depreciation rate = 2 / useful life, computed on the opening net book value, with the last two years switched to the straight-line method",
        "Sum-of-the-years'-digits method",
        ": (cost - salvage value) × remaining useful life / sum of the years, more depreciation early and less later",
        "📚 Deep dive: Depreciation Method Comparison",
        "During tax planning and financial statement preparation, compare the straight-line method,",
        "double-declining balance",
        "method,",
        "on their effect on the depreciation and net book value of each year.",
        "Assess the effect of accelerated depreciation on early-stage profit and deferred income tax, judging whether the asset's early tax burden can reasonably be deferred.",
        "In the fixed asset management ledger, choose a matching depreciation policy per asset class and keep the basis consistent, making cross-period reconciliation easier.",
        "Cost 100000, useful life 5 years, salvage rate 5%",
        "Cost 100000 CNY, expected useful life 5 years, salvage rate 5% (salvage value 5000 CNY, depreciable amount 95000 CNY). Straight-line annual depreciation = 95000 ÷ 5 = 19000 CNY. Double-declining balance annual rate = 2 ÷ 5 = 40%, so year 1 depreciation = 100000 × 40% = 40000 CNY, year 2 = (100000 − 40000) × 40% = 24000 CNY, and the last two years split the remaining net value minus salvage evenly. For the sum-of-the-years'-digits method the annual rate denominator = 5+4+3+2+1 = 15, so year 1 depreciation = 95000 × 5/15 ≈ 31667 CNY and year 2 = 95000 × 4/15 ≈ 25333 CNY, decreasing year by year.",
        "Why does the double-declining balance method switch to straight line in the last two years?",
        "The double-declining balance method depreciates fast early and slow later, so if the rate is applied throughout, the cost cannot land exactly on the salvage value by the end. By convention, in the final two years before the depreciation period expires, the remaining net value minus the estimated net salvage value is averaged, ensuring the final net book value equals the salvage value.",
        "How do the three methods differ in their effect on income tax?",
        "The straight-line method spreads the expense evenly across years; accelerated depreciation methods (double-declining balance, sum-of-the-years'-digits) give large early depreciation, low early profit and relatively deferred taxable income, which is equivalent to gaining the time value of money, but the total depreciation over the whole life cycle is the same, only distributed with more early and less later.",
        "How to use the Depreciation Method Comparison tool",
        "During tax planning and financial statement preparation, compare the straight-line, double-declining balance and sum-of-the-years'-digits methods in terms of their effect on the depreciation and net book value of each year.",
    ]))

    # ---------------- index (18) ----------------
    write('index', build('index', [
        "📋 Audit Compliance Tools",
        "Audit compliance",
        "Audit Compliance Tools",
        "Discounts each period to compute the net present value, showing the present value, discount factor and cumulative present value of each period, supporting continuous / annuity modes",
        "Audit Sampling",
        "Based on the desired reliance, tolerable error and expected error, computes the sample size for attribute sampling and variable sampling, used for audit sampling plan design and inspection workload planning.",
        "Depreciation Comparison",
        "Compares the straight-line method, the double-declining balance method and the sum-of-the-years'-digits method, showing the depreciation and book value of each year",
        "Enter the cash flows of each period and scan NPV at different discount rates to precisely locate the internal rate of return (the threshold where NPV turns from positive to negative)",
        "Enter key data from the balance sheet and income statement to automatically compute solvency, operating and profitability ratios and give an assessment",
        "About \"Audit Compliance Tools\"",
        "The Audit Compliance Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of audit compliance scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The audit compliance tools listed on this page include (a few representative tools):",
        "These tools help you finish common audit compliance tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the audit compliance tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the audit compliance tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
