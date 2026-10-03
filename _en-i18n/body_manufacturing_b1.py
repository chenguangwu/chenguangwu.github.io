#!/usr/bin/env python3
from head_manufacturing import build, write


def main():
    write('capacity-planning', build('capacity-planning', [
        '📐 Capacity Planning Calculator',
        'Evaluates line capacity utilization and plans equipment, working hours and shifts',
        '/ Capacity Planning',
        '📖 View the guide to capacity planning calculation',
        'Theoretical capacity = number of machines × capacity per machine × number of shifts × working days × equipment efficiency; capacity utilization = demand ÷ theoretical capacity × 100%; capacity gap = demand − theoretical capacity (a positive value means a shortfall, requiring more equipment or extra shifts); required machines = demand ÷ (capacity per machine × shifts × days × efficiency), rounded up; a load rate above 90% means capacity is tight and below 60% means excess capacity, which can be used to adjust shifts or the production schedule.',
        '📚 In-depth: capacity planning calculation',
        'Before investing in a new production line or holding a scheduling meeting, use this tool to work out the minimum number of machines and shifts needed to meet monthly orders, avoiding blind expansion or leaving a capacity gap.',
        'When switching between low and high seasons, adjust the number of shifts (1 / 2 / 3) to evaluate capacity utilization and decide whether to add shifts or divert spare capacity to other orders.',
        'When an unexpected large order arrives, quickly check whether the current equipment configuration can deliver within the deadline, and locate the bottleneck process that should be expanded first.',
        'Workshop capacity calculation example',
        'A machining workshop has 5 CNC machines with a capacity of 200 pieces per machine per day, 2 shifts per day, 22 working days per month and monthly orders of 20,000 pieces. Theoretical monthly capacity = 5 × 200 × 22 × 2 = 44,000 pieces; capacity utilization = 20,000 ÷ 44,000 ≈ 45.5% (surplus); the minimum machines needed for this order = ⌈20,000 ÷ (200 × 22 × 2)⌉ = 3. Conclusion: the current 5 machines can take the order comfortably, or the 2 spare machines can be switched to other orders.',
        'What does it mean when capacity utilization shows more than 100%?',
        'It means the current equipment configuration cannot complete the order within the deadline; the gap = order quantity − theoretical monthly capacity. Add machines (⌈gap ÷ monthly capacity per machine⌉ machines) or outsource, and check the bottleneck process first.',
        'Is a higher utilization always better?',
        'No. Utilization close to 100% over the long term means there is no buffer, and any downtime or rush order will breach the commitment. A healthy range is 70% to 95%, leaving room for maintenance, changeovers and unexpected orders.',
        'About capacity planning calculation',
    ]))

    write('defect-rate', build('defect-rate', [
        '🧮 Defect Rate and Sigma Calculator',
        'Conversion between first-pass yield, DPMO, PPM, CPK and sigma level',
        'Core formula (by input variables): max(0, (sigma - 3) × 2 ÷ 3); (d ÷ t) × 1000000 ÷ p; (d ÷ t) × 1000000',
        '/ Defect Rate Calculation',
        '📖 View the guide to defect rate and sigma calculation',
        '📚 In-depth: defect rate and sigma calculation',
        'When compiling monthly quality reports on defect levels, use the defect rate, first-pass yield and',
        'PPM / sigma conversion to compare process capability across production lines or months.',
        'To assess the overall yield of a multi-process product, use rolled throughput yield RTY to reveal the accumulated loss at each process and locate the main failure step.',
        'When reporting for a customer audit or a Six Sigma project, convert the',
        'PPM/DPMO into the',
        'sigma level',
        'and CPK, presenting the quality grade intuitively.',
        'Assembly line quality analysis example',
        'An assembly line inputs 50,000 pieces, detects 250 defective pieces, across 2 processes in total. Defect rate = 250 ÷ 50,000 = 0.5%; single-process first-pass yield = 1 − 0.5% = 99.5%; rolled throughput yield RTY = 0.995² ≈ 99.00%; PPM = 0.5% × 10⁶ = 5000; DPMO = 5000 ÷ 2 = 2500; table lookup gives a sigma level of 3.5σ, and by this tool’s approximate conversion CPK ≈ 0.33 (low, indicating that process stability needs improvement and the sources of variation should be addressed first).',
        'What is the difference between RTY and the first-pass qualification rate?',
        'Single-process first-pass yield FTY only reflects the proportion passing that process at the first attempt; rolled throughput yield RTY multiplies the FTY of every process, revealing the accumulated loss across processes. RTY is often far below the single-process pass rate, making it the key indicator for exposing hidden losses.',
        'How should DPMO and sigma level be understood?',
        'DPMO is the number of defects per million opportunities, and the sigma level is converted from DPMO by table lookup: about 66807 → 3σ, 6210 → 3.5σ, 233 → 4σ, 3.4 → 5σ, 0.002 → 6σ. The higher the value, the more stable the process; the usual industry target is ≥ 4σ (about DPMO ≤ 6210).',
        'About defect rate / DPMO calculation',
    ]))

    write('inventory-calculator', build('inventory-calculator', [
        '🏬 Inventory Calculator',
        'EOQ economic order quantity, safety stock and reorder point',
        'Core formula (by input variables): √(2 × D × S ÷ H); √(2 × D × S × H); (EOQ ÷ 2) × H',
        '/ Inventory Calculation',
        '📖 View the guide to the inventory calculator',
        '📚 In-depth: inventory calculator',
        'When the purchasing department sets a replenishment strategy, it uses EOQ to balance ordering cost against holding cost and determine the optimal quantity per order.',
        'Facing demand fluctuation and uncertain lead times, use safety stock and the reorder point ROP to set the replenishment trigger line and prevent line stoppages from material shortages.',
        'At the annual inventory review, use the total inventory cost (ordering plus holding) to assess whether the current strategy is economical and to optimize order frequency.',
        'EOQ and safety stock example',
        'A part has annual demand 12,000 units, ordering cost 50 CNY per order, annual holding cost 2 CNY per unit, average daily demand 33 units, lead time 7 days, daily demand',
        'standard deviation 5, service level 95% (Z = 1.65). EOQ = √(2 × 12000 × 50 ÷ 2) ≈ 775 units; annual orders 12000 ÷ 775 ≈ 15.5 times (a cycle of about 24 days); average inventory ≈ 387 units; safety stock = 1.65 × 5 × √7 ≈ 22 units; reorder point ROP = 33 × 7 + 22 ≈ 253 units; minimum total inventory cost ≈ √(2 × 12000 × 50 × 2) ≈ 1549 CNY.',
        'Is a larger or a smaller EOQ better?',
        'EOQ is the point of lowest total cost: too large an order quantity raises holding cost, while too small a quantity raises order frequency and ordering cost. The EOQ formula √(2DS/H) already balances the two, and in practice safety stock must be added on top to absorb fluctuation.',
        'How is the reorder point ROP used?',
        'When inventory falls to the ROP (average daily demand × lead time + safety stock), an order is triggered, ensuring no stockout during the lead time. The higher the service level (larger Z) and the greater the demand fluctuation, the higher the safety stock and the ROP.',
        'About the inventory calculator - EOQ safety stock',
    ]))

    write('production-efficiency', build('production-efficiency', [
        '⚡ OEE Overall Equipment Effectiveness',
        'OEE = availability × performance × quality (world class ≥ 85%)',
        'Core formula (by input variables): (1 - min(performance,1)) × 100; min(O ÷ idealCount, 1.5); (runTime × 60) ÷ CT',
        '/ OEE Production Efficiency',
        '📖 View the guide to OEE overall equipment effectiveness',
        '⚡ Calculate OEE',
        '📚 In-depth: OEE overall equipment effectiveness',
        'When launching an equipment efficiency improvement project, use OEE to quantify the three major losses — availability, performance and quality — and locate the biggest loss.',
        'Set an OEE target at the pre-shift meeting (world class ≥ 85%), compare teams and lines, and drive TPM together with the elimination of minor stoppages.',
        'When accepting new equipment or before and after a process change, compare OEE before and after to verify the improvement.',
        'OEE measurement example',
        'A machine is planned to run 480 minutes (an 8-hour shift), with 60 minutes of unplanned downtime, a cycle time of 120 seconds per piece, 200 pieces produced and 195 good pieces. Availability = (480 − 60) ÷ 480 = 87.5%; theoretical output = 420 × 60 ÷ 120 = 210 pieces, performance = 200 ÷ 210 ≈ 95.2%; quality = 195 ÷ 200 = 97.5%; OEE = 87.5% × 95.2% × 97.5% ≈ 81.2% (close to the good level). The losses come mainly from downtime (12.5%) and small speed losses.',
        'Which of the three OEE factors should be improved first?',
        'Start with the factor that loses the most. Availability losses (downtime and changeover) usually offer the biggest room for improvement and can be addressed with TPM; performance losses mostly come from minor stoppages and reduced speed; quality losses depend on process control. World class OEE is ≥ 85% (availability ≥ 90%, performance ≥ 95%, quality ≥ 99%).',
        'What is the difference between OEE and capacity utilization?',
        'Capacity utilization only looks at output ÷ theoretical capacity and ignores downtime, speed and quality losses; OEE includes availability × performance × quality, reflecting effective output more truthfully, and is the more comprehensive efficiency indicator in manufacturing.',
        'About OEE production efficiency calculation',
    ]))

    write('quality-control', build('quality-control', [
        '⚖️ CPK Process Capability Index',
        'Evaluates process capability; CPK ≥ 1.33 counts as acceptable',
        'Core formula (by input variables): |(mean - M)| ÷ (T ÷ 2); min(CPU, CPL); (USL + LSL) ÷ 2',
        '/ CPK Process Capability',
        '📖 View the guide to the CPK process capability index',
        '⚖️ Calculate CPK',
        '📚 In-depth: CPK process capability index',
        'When judging incoming material or process quality, use CPK / CP to assess whether the process capability meets the specification, and decide whether to accept the lot or adjust the process.',
        'When checking process centring, use the CA offset coefficient to judge whether the mean deviates from the tolerance centre, guiding equipment or parameter adjustment.',
        'For long-term stability monitoring, compare PPK (long term) with CPK (short term) to identify special causes that drift over time.',
        'Shaft diameter process capability example',
        'A shaft diameter has a specification of 9.5-10.5 mm, a measured mean of 10.0 mm and',
        'standard deviation 0.1 mm, with a sample of 30 pieces. Tolerance T = 10.5 − 9.5 = 1.0 mm; CP = 1.0 ÷ (6 × 0.1) = 1.67; CPU = (10.5 − 10.0) ÷ (3 × 0.1) = 1.67, CPL = (10.0 − 9.5) ÷ 0.3 = 1.67, CPK = min = 1.67; the tolerance centre is 10.0 mm, CA = |10.0 − 10.0| ÷ (1.0 ÷ 2) = 0% (centred, no offset); allowing for the',
        'correction, the long-term PPK ≈ 1.66. Conclusion: CPK ≥ 1.33 means the capability is acceptable and the centring is good.',
        'What is the difference between CPK and CP?',
        'CP only looks at tolerance width and process spread (the potential) and ignores mean offset; CPK = min(CPU, CPL) also accounts for offset and better reflects actual capability. When the mean is centred CPK = CP, and the larger the offset the smaller the CPK.',
        'What value of CPK counts as acceptable?',
        'In general industry: CPK ≥ 1.33 is acceptable (recommended), ≥ 1.67 means excess capability so the tolerance can be relaxed, 1.0 to 1.33 is marginal and needs improvement, and below 1.0 is insufficient. Industries such as automotive often require ≥ 1.33 or even ≥ 1.67.',
        'About CPK process capability calculation',
    ]))


if __name__ == '__main__':
    main()
