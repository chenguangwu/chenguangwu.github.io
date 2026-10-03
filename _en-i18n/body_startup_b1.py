def main():
    # ---------------- burn-rate (15) ----------------
    write('burn-rate', build('burn-rate', [
        "💰 Burn Rate Calculator",
        "Startup cash consumption analysis: computes monthly net burn, cash runway and the date funds run out",
        "Core formula (by input variable): netBurn x 18",
        "/ Burn Rate Calculator",
        "📚 Deep dive: Burn Rate Calculator",
        "Total monthly spending (salaries + rent + marketing + other) is the gross burn rate; the net burn rate = monthly spending - monthly revenue, and a negative value means cash flow has turned positive.",
        "Runway = cash on hand / net burn rate; use the runway length for alerts: under 6 months is high risk, under 9 months means accelerate fundraising, under 12 months means plan the raise.",
        "Work backwards from \"keep an 18-month runway\": funding needed = net burn rate x 18 - current cash (a financing round is needed only when this is positive).",
        "Reproducible example (cash 500,000 CNY, monthly income 20,000 CNY, monthly spending 125,000 CNY)",
        "Monthly spending = 80,000 + 15,000 + 20,000 + 10,000 = 125,000 CNY; net burn = 125,000 - 20,000 = 105,000 CNY per month; gross burn = 125,000 CNY.\nRunway = 500,000 / 105,000 = 4.8 months → below 6 months, triggering the high-risk alert, so raise funds now or cut non-essential spending.\n18-month target cash = 105,000 x 18 = 1,890,000 CNY; suggested raise = 1,890,000 - 500,000 = 1,390,000 CNY (including buffer).",
        "What is the difference between gross and net burn?",
        "Gross burn rate = total monthly spending (excluding revenue); net burn rate = spending - revenue. Once there is revenue, net burn measures the real consumption, and the runway is computed on net burn too - the higher the revenue, the longer the runway.",
        "Why is an 18-month runway recommended?",
        "Raising funds often takes 3-9 months from launch to money in the bank, and an 18-month buffer covers the fundraising period plus execution variance, avoiding forced low-priced financing at the trough. The formula is net burn x 18, and the shortfall is the suggested round size.",
        "About \"Burn Rate Calculator\"",
    ]))

    # ---------------- business-plan (15) ----------------
    write('business-plan', build('business-plan', [
        "✨ Business Plan Generator",
        "Guided entry across nine sections to generate a complete business plan, with export and local save support",
        "/ Business Plan Generator",
        "📚 Deep dive: Business Plan Generator",
        "Fill in each item following the standard BP structure (executive summary, company overview, market analysis, product and service, business model, competitive analysis, team, financial forecast, fundraising plan, risks), which avoids missing items and guarantees every module investors care about is covered.",
        "Different rounds emphasize different things: angel rounds highlight the team and product validation, Series A emphasizes growth and unit economics, and Series B focuses on scale and the path to profitability; the same structure adapts to different funding stages.",
        "Consolidate the key numbers (TAM/SAM/SOM, average order value,",
        ", monthly growth, burn rate) into the executive summary and financial forecast so investors can grasp them quickly.",
        "Reproducible example: key numbers for a SaaS startup BP",
        "The tool generates a standard 10-section outline: the executive summary states \"target market SOM of 500,000 SMEs, average order value 12,000 CNY per year, gross margin 75%\"; the financial forecast gives 3 years of revenue (Y1 6,000,000 CNY, Y2 18,000,000 CNY, Y3 45,000,000 CNY) with the corresponding burn rate; the fundraising plan states this round of 20,000,000 CNY for 15% dilution, with use of proceeds (R&D 40% / sales 35% / operations 25%). The tool renders these numbers into a complete BP outline by section, ready to export as a pitch base draft and DD material.",
        "Which modules does a BP usually include?",
        "The mainstream structure covers executive summary, company overview, market and opportunity (TAM/SAM/SOM), product/service, business model, competitive analysis, team, financial forecast, fundraising plan, and risks with mitigations. Seed and angel rounds can streamline team and product, while growth-stage companies must add unit economics and the scaling path.",
        "How many years should the financial forecast cover?",
        "For an early-stage company 3 years (12 quarters) is enough, focused on each quarter of year 1 and each year for the following two years; build the forecast bottom-up (average order value x customer count x gross margin) rather than guessing, and label the key assumptions (retention, CAC, payback period) so investors can review them.",
        "About \"Business Plan Generator\"",
    ]))

    # ---------------- calc-1 (14) ----------------
    write('calc-1', build('calc-1', [
        "💰 Startup Cost Estimate",
        "Enter startup one-off investment and monthly operating expenses by category to estimate total initial funding",
        "Startup one-off investment and monthly operating expenses entered by category estimate the total initial funding by professional calculation from the input parameters.",
        "/ Startup Cost Estimate",
        "📚 Deep dive: Startup Cost Estimate",
        "Split startup costs into one-off investment (registration, venue, equipment, first inventory, branding/development) and monthly operations (salaries, rent, marketing, sundry), accumulating each separately so nothing is missed.",
        "Operating capital = monthly cost x number of months, then add the emergency reserve (usually 3 months) to get the total recommended initial funding.",
        "Divide the total by the monthly cost to get how many months the funding supports (the runway); below 12 months you need more financing or lower costs.",
        "Reproducible example (default parameters)",
        "One-off: registration 3,000 + venue 20,000 + equipment 30,000 + inventory 20,000 + branding 15,000 + other 5,000 = 93,000 CNY.\nMonthly operations: salaries 30,000 + rent 5,000 + marketing 5,000 + sundry 3,000 = 43,000 CNY.\nOperating capital = 43,000 x 12 = 516,000 CNY; emergency reserve = 43,000 x 3 = 129,000 CNY.\nRecommended initial funding = 93,000 + 516,000 + 129,000 = 738,000 CNY; the funding supports 738,000 / 43,000 = 17.2 months.",
        "How many months of emergency reserve should be kept?",
        "Keep 3 months of operating cash as a rule; if the fundraising cycle is long or revenue is uncertain, 6 months is safer. The reserve counts toward initial funding, directly lengthening the runway and lowering the risk of running out of cash.",
        "At what runway should I worry?",
        "Start fundraising planning when the runway is under 12 months, accelerate when it is under 9 months, and treat under 6 months as high risk requiring an immediate raise or spending cuts. Formula: runway = initial funding / monthly cost.",
    ]))

    # ---------------- equity-calculator (15) ----------------
    write('equity-calculator', build('equity-calculator', [
        "🧮 Equity Split Calculator",
        "Startup team equity allocation with weighted contribution, option pool reservation and multi-round dilution",
        "Core formula (by input variable): amount / (pre + amount) x 100; max(0, min(100, t.initPct))",
        "/ Equity Split Calculator",
        "📚 Deep dive: Equity Split Calculator",
        "Score each founder's contribution to the idea, capital, time and resources, then equity = individual score / total score x (100% - option pool), avoiding an arbitrary even split or shares based only on capital contributed.",
        "Deduct the option pool (such as 10%) first, then allocate founder shares, so the pool sits above the founders and dilutes proportionally with them in later funding rounds.",
        "Each round dilutes existing shareholders via \"retained percentage = pre-money / (pre-money + new amount)\", and the investor stake = new amount / (pre-money + new amount), so multi-round structures can be derived step by step.",
        "Reproducible example (A60/B40 split, 10% option pool, round 1 pre=10,000,000 CNY, amount=5,000,000 CNY)",
        "Distributable to founders = 100% - 10% = 90%: A = 60/100 x 90% = 54.0%, B = 36.0%, option pool 10% (total 100%).\nRound 1: post-money = 10,000,000 + 5,000,000 = 15,000,000 CNY, retained percentage = 10,000,000/15,000,000 = 0.6667, investor stake = 5,000,000/15,000,000 x 100% = 33.33%.\nAfter dilution: A = 54 x 0.6667 = 36.00%, B = 24.00%, pool = 6.67%, investor 33.33% (total 100%). Further rounds can be layered on.",
        "Which level should the option pool sit at?",
        "Place it before founder allocation (deduct the 10% pool first, distribute the remaining 90% to founders). That way later financing dilutes the pool and the founders proportionally, avoiding a separately reserved pool that would dilute founders twice.",
        "How is equity computed after multiple rounds?",
        "In each round multiply every existing party's percentage by \"retained percentage = pre-money valuation / (pre-money + new amount)\", then add the investors at \"new amount / post-money\". Stacking rounds one by one shows the final structure of founders, pool and each round of investors.",
        "About \"Equity Split Calculator\"",
    ]))

    # ---------------- pitch-deck (15) ----------------
    write('pitch-deck', build('pitch-deck', [
        "✨ Pitch Deck Outline Generator",
        "Based on a standard 10-page structure, guides you through filling in each page and generates a complete pitch outline, with export and local save support",
        "Based on a standard 10-page structure, guides you page by page through every slide, generating a complete pitch outline with export and local save support",
        "/ Pitch Deck Outline Generator",
        "📚 Deep dive: Pitch Deck Outline Generator",
        "Follows a standard 10-page structure (problem, solution, market opportunity, product demo, business model, competitive advantage, team, financials, fundraising, vision) and guides you page by page, ensuring a complete narrative and closed logic.",
        "Keep the information density per page low: one core argument plus one supporting number per page to avoid walls of text; use the three-part hook \"problem → solution → why now\" to capture investors.",
        "Fine-tune the order for different audiences: move business model and financials earlier for finance-focused investors, and move the product demo earlier for product-focused investors, using the same structure.",
        "Reproducible example: standard 10-page pitch outline",
        "The tool generates the outline: (1) Problem (a SaaS pain point costing the market 20 billion CNY a year) (2) Solution (one-click automation, deployed in 1 day) (3) Market opportunity (TAM 80 billion / SAM 12 billion / SOM 800 million CNY) (4) Product demo (screenshots of 3 core features) (5) Business model (subscription, average order value 12,000 CNY per year, NRR 120%) (6) Competitive advantage (compared with 3 rivals, 5x faster implementation) (7) Team (2 co-founders from major companies, 10 years of experience) (8) Financials (ARR Y1 6,000,000 CNY → Y3 45,000,000 CNY, 75%) (9) Fundraising (this round 20,000,000 CNY for 15% dilution) (10) Vision (become the segment leader within 3 years). Each page carries data, and the export is ready to use as the pitch master.",
        "How many pages should a pitch deck have?",
        "The standard 10-12 pages is safest: cover + problem + solution + market + product + model + advantage + team + financials + fundraising + closing vision. Early-stage projects struggle to get through more pages; the core is nailing five things: problem, solution, market, team, and how the money will be used.",
        "Which metrics should the financials page show?",
        "Early stage looks at ARR/MRR, monthly growth, gross margin, net revenue retention (NRR), CAC and payback period; growth stage adds LTV/CAC, burn rate and runway. Keep the metrics traceable and consistent with the BP so the pitch and the documents do not contradict each other.",
        "About \"Pitch Deck Outline Generator\"",
    ]))

    # ---------------- valuation-calculator (15) ----------------
    write('valuation-calculator', build('valuation-calculator', [
        "📈 Startup Valuation Calculator",
        "Five methods to estimate a startup's valuation (pre-money), outputting a combined valuation range. Amounts in units of 10,000 CNY",
        "Five methods to estimate a startup's valuation (pre-money) and output a combined range by professional calculation from the input parameters.",
        "/ Startup Valuation Calculator",
        "📚 Deep dive: Startup Valuation Calculator",
        "Cross-validate with several methods: Berkus (5 factors each at most 5,000,000 CNY, total cap 25,000,000 CNY), scorecard (base valuation x weighted deviation), venture capital method (back out pre-money/post-money), DCF (discounted cash flow plus perpetual terminal value), and transaction comparables (PS multiples / value per user).",
        "A single method has large error for early-stage projects, so run 2-3 methods and take a range to avoid being anchored by one basis; DCF is sensitive to assumptions and suits growth-stage companies with stable cash flow.",
        "The venture capital method works backwards from an exit multiple: post-money = exit value / (1 + annualized return)^years, pre-money = post-money - this round's investment, and it also computes the investor's stake.",
        "Reproducible example (all 5 methods run together)",
        "Berkus: 5 factors at 3,000,000 CNY each → 15,000,000 CNY (cap 25,000,000 CNY).\nScorecard: base 20,000,000 CNY, 7 factors deviation weighted +5% → 21,000,000 CNY.\nVenture capital method: exit 80,000,000 CNY, return multiple 1.4, 4 years, this round 15,000,000 CNY → annualized rate 0.4, post-money = 80,000,000/1.4^4 = 20,825,000 CNY, pre-money = 5,825,000 CNY, investor stake = 72.0%.\nDCF: 5-year cash flow (5,000,000 → 12,440,000 CNY, g=20%), discounted at 12%, perpetual growth 3% → present value of each period totals 30,895,000 CNY plus present value of terminal value 80,794,000 CNY = 111,690,000 CNY.\nTransaction comparables: revenue 20,000,000 CNY x PS(3~8) = 60,000,000-160,000,000 CNY; the per-user method (monthly active users 3,000,000 x 30~80 CNY) serves as a cross-check giving 0.9-2.4 (10,000 CNY units).\nThe combined range is about 5,820,000-160,000,000 CNY; use the multi-method average as the starting point for negotiations.",
        "Which valuation method suits an early-stage project?",
        "For very early stages Berkus or the scorecard (team and factor scoring) is most reliable; once there is revenue, use the venture capital method to back out; at growth stage add DCF and PS comparables. Every single method skews one way, so run at least two for cross-validation.",
        "How is the return rate set in the venture capital method?",
        "Return rate = exit multiple - 1 (for example a 10x exit gives an annualized 9, which is too aggressive). In practice an annualized return of 20%~40% over 3-5 years is common for early stages (that is, a multiple of 1.2~1.4); a multiple that is too high back-solves to a negative pre-money valuation, so revisit the parameters.",
        "About \"Startup Valuation Calculator\"",
    ]))


if __name__ == '__main__':
    main()
