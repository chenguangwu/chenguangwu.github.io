#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'electrical')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'electrical')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'electrical', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('wire-resistance', build('wire-resistance', [
        "⚡ Wire Resistance Calculation (Electrical)",
        "Computes the DC resistance of a conductor from material resistivity, length and cross-section.",
        "Wire Resistance Calculation",
        "Resistivity ρ (Ω·mm²/m)",
        "R = ρ·L/A (copper ρ≈0.0172, aluminium ≈0.0283 Ω·mm²/m)",
        "Resistance rises as temperature rises",
        "Long-distance transmission needs a voltage drop and heating check",
        "📚 Deep dive: Wire Resistance Calculation (Electrical)",
        "Distribution line loss calculation: 100m of 4mm² copper gives R ≈ 0.44Ω.",
        "Grounding resistance estimate: electrode plus soil",
        "resistivity",
        "to derive the grounding grid resistance.",
        "Motor winding copper loss: I²R and temperature rise.",
        "Precision measurement of low resistance: a four-wire method for milliohm-level resistance.",
        "100m of copper at a cross-section of 1.5mm²",
        "R = 1.724e-8 × 100 / 1.5e-6 ≈ 1.15Ω; at 10A that is an 11.5V drop and 115W of loss.",
        "Why is AC resistance larger than DC resistance?",
        "The skin effect (high-frequency current crowding to the conductor surface) and the proximity effect (magnetic interference from adjacent conductors) reduce the effective cross-section and raise AC resistance. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What is the effect of temperature on resistance?",
        "Metal resistance increases with temperature, R(T)=R0[1+α(T-T0)]; for copper α≈0.00393/℃, so a 50℃ rise in a copper conductor increases resistance by about 20%. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why do superconductors need extremely low temperatures?",
        "Below its critical temperature a metal's resistance approaches zero (for example niobium-titanium in the 4.2K liquid helium range), so it can carry large currents without loss, which is why it is used in MRI and accelerators. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

    write('voltage-divider', build('voltage-divider', [
        "🔌 Voltage Divider Calculation",
        "Two-resistor divider, output under load, and potentiometer",
        "Core formula (by input variable): |((Vout - Videal)| ÷ Videal × 100); R × (1 - pos÷100); R × pos÷100",
        "Voltage Divider Circuit",
        "/ Voltage Divider",
        "📚 Deep dive: Resistor Voltage Divider Calculation (Electrical)",
        "ADC front-end step-down: dropping a 0-12V signal to 0-3.3V to match an MCU ADC.",
        "Reference voltage: a low-current reference source (for example a TL431 set by a divider).",
        "Sensor bias: a resistor divider powering the sensor.",
        "Op-amp bias: when a dual supply is inconvenient, a resistor divider provides the midpoint.",
        "A 12V to 3.3V divider for an ADC",
        "R1=10kΩ, R2=3.9kΩ → Vout=12×3.9/13.9≈3.37V; a high-impedance divider reduces loading effects.",
        "Why pick the divider resistors larger?",
        "Larger resistors reduce quiescent current, but going too large lets loading and leakage pull the voltage away from the ideal; 10kΩ to 100kΩ is the usual range. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I compute it when the next stage draws a load?",
        "Connect the load",
        "resistor in parallel",
        "with R2 to get the equivalent R2L, then substitute that into the formula; an op-amp buffer can avoid the loading effect entirely. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why is a resistor divider worse than a voltage regulator?",
        "A divider's output follows input fluctuations and varies a lot with load, while a regulator (LDO or DC-DC) gives a stable, efficient output (switching types especially). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "About \"Voltage Divider\"",
        "The Voltage Divider computes the divider node and the loaded divider output from the input voltage and resistance ratio. It is a fundamental tool for bias and signal conditioning design, running entirely in the front end with no data uploaded.",
    ]))

    write('opamp-gain', build('opamp-gain', [
        "📡 Op-Amp Gain Calculation (Electrical)",
        "Computes the closed-loop voltage gain of inverting and non-inverting amplifier circuits.",
        "Op-Amp Gain Calculation",
        "A_v = -R_f/R_in inverting; A_v = 1+R_f/R_in non-inverting; ideal op-amp with deep negative feedback as the approximation, while in reality bandwidth and slew rate limit it",
        "Input resistor R_in (Ω)",
        "Feedback resistor R_f (Ω)",
        "Inverting: A_v = -R_f/R_in",
        "Non-inverting: A_v = 1+R_f/R_in",
        "Ideal op-amp with deep negative feedback as the approximation, while in reality bandwidth and slew rate limit it",
        "📚 Deep dive: Op-Amp Gain Calculation (Electrical)",
        "Inverting amplification: Av=-Rf/Rin, with Av=-1 to -100 being common.",
        "Non-inverting amplification: Av=1+Rf/Rg, with Av=1 to 1000 being common.",
        "Voltage follower: Av=1, offering high input impedance and low output impedance as a buffer.",
        "Differential amplification: the front stage of an instrumentation amplifier, with Av=Rf/Rin and common-mode rejection.",
        "Non-inverting amplifier with Rin=10kΩ and Rf=90kΩ",
        "Av=1+90/10=10; the balancing resistor Rin‖Rf=9kΩ; with GBW=1MHz, fT=100kHz.",
        "Why is a balancing resistor needed?",
        "The op-amp input bias current produces an offset voltage across the input impedance, and the balancing resistor makes both input impedances equal so the bias current effect cancels. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I trade off bandwidth against gain?",
        "The gain-bandwidth product GBW is constant, with Av×f-3dB=GBW; the higher the gain the narrower the usable bandwidth. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "What should I watch for with a single-supply op-amp?",
        "You need a midpoint bias (Vcc/2) for input and output coupling, keeping the DC bias path separate from the AC path. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

    write('current-divider', build('current-divider', [
        "⚡ Current Divider Calculation (Electrical)",
        "Computes the current taken by each of two parallel resistors.",
        "Current Divider Calculation",
        "Total current I_t (mA)",
        "Branch resistance R₁ (Ω)",
        "Branch resistance R₂ (Ω)",
        "Parallel division: I₁ = I_t·R₂/(R₁+R₂), I₂ = I_t·R₁/(R₁+R₂)",
        "The smaller the resistance, the larger the share of current",
        "The total should equal the input total current (for verification)",
        "📚 Deep dive: Current Divider Calculation (Electrical)",
        "Resistive division: R1=6Ω, R2=3Ω, I_total=6A → I1=2A, I2=4A.",
        "Shunt (manganin strip) design: when measuring large current, put a low-value resistance in parallel with the load and measure the voltage.",
        "Multiple parallel power resistors on a PCB: current sharing error ≤5%.",
        "Unbalanced load analysis: estimating the inter-phase unbalance rate and zero-sequence current.",
        "Two branches R1=10Ω, R2=20Ω in parallel with I=9A",
        "Where does the divider formula come from?",
        "Parallel branches share the same voltage Ui=I1·R1=I2·R2, so I1/I2=R2/R1 and I1=I_total·R₂/(R₁+R₂). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why measure the voltage across the shunt?",
        "Large current is hard to measure directly, so you measure the voltage across a low-value shunt (milliohm level) and convert: I=U/Rshunt. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do I do a quick calculation for multiple parallel branches?",
        "Req=1/(Σ1/R); the current in each branch is I_total·(Req/Ri), that is, the split follows the conductance ratios. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

    write('rlc-resonance', build('rlc-resonance', [
        "⚡ RLC Series Resonant Frequency Calculation (Electrical)",
        "Computes the resonant frequency of an RLC series circuit from its inductance and capacitance.",
        "RLC Series Resonant Frequency Calculation",
        "Series resonant frequency f₀ = 1 ÷ (2π√(LC)), where L is in henries and C in farads (1 mH = 10⁻³ H, 1 μF = 10⁻⁶ F); with L = 1 mH and C = 1 μF, f₀ is about 5033 Hz. At resonance the inductive reactance equals the capacitive reactance, the impedance is at its minimum of a pure resistance R, and the current is at its maximum; the quality factor Q = (1 ÷ R) × √(L ÷ C), and a higher Q gives sharper frequency selection with a bandwidth BW = f₀ ÷ Q.",
        "Inductance L (mH)",
        "At resonance the inductive and capacitive reactances are equal, so the circuit impedance is at its minimum",
        "Used for frequency selection, filtering and oscillator circuit design",
        "📚 Deep dive: RLC Series Resonant Frequency Calculation (Electrical)",
        "Wireless charging coil: 13.56MHz ISM resonant design.",
        "Radio tuning: a variable capacitor tunes to the target station frequency.",
        "Band-pass filter: LC resonance serves as the frequency-selective network.",
        "EMI suppression: an LC notch filter presents infinite impedance at a target frequency.",
        "Series resonance with L=100μH and C=100pF",
        "f0=1/(2π√LC)=1/(2π·√(1e-4·1e-10))≈1.59MHz; with R=10Ω, Q=100 and the bandwidth is about 16kHz.",
        "What is the impedance at resonance?",
        "In a series resonance the impedance is R (its minimum) and the current is at its maximum; in a parallel resonance the impedance is R·Q² (its maximum) and the voltage is at its maximum. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Is a high Q good or a low Q good?",
        "Frequency-selective circuits want a high Q (sharp selectivity), while wideband filtering and power supply LC filtering want a low Q (wide bandwidth, less prone to resonant over-voltage). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why is the measured resonant frequency different from the calculated one?",
        "Stray capacitance, lead inductance and component tolerances all shift it; at high frequencies you need a vector network analyzer to measure and calibrate. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

    write('rc-filter', build('rc-filter', [
        "📡 RC Low-Pass Cutoff Frequency Calculation (Electrical)",
        "Computes the cutoff frequency of a first-order RC low-pass filter from its resistance and capacitance.",
        "RC Low-Pass Cutoff Frequency Calculation",
        "f_c = 1/(2πRC); signals above f_c attenuate at -20dB per decade; commonly used for power supply decoupling and anti-aliasing input filtering",
        "Resistance R (kΩ)",
        "Signals above f_c attenuate at -20dB per decade",
        "Commonly used for power supply decoupling and anti-aliasing input filtering",
        "📚 Deep dive: RC Low-Pass Cutoff Frequency Calculation (Electrical)",
        "Audio low-pass: removing high-frequency noise at a 20kHz cutoff.",
        "Power supply decoupling: an RC filter stripping switching supply ripple.",
        "Signal conditioning: an anti-aliasing low-pass at the ADC input.",
        "Timing circuit: RC charge and discharge calculation (an NE555 monostable).",
        "First-order low-pass with R=10kΩ and C=10nF",
        "f-3dB=1/(2π·10k·10n)=1.59kHz; at 10f the attenuation is about -20dB and at 100f it is -40dB.",
        "What does the cutoff frequency mean?",
        "It is the frequency at which the gain falls to -3dB (≈0.707); a first-order RC roll-off loses 6dB per octave while a second-order one loses 12dB per octave. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "How do RC and RL filters differ?",
        "RC suits small-signal low-cost designs; RL suits high-current power supply filtering (such as an LC power filter), with cutoff frequency f=1/(2π√LC). This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
        "Why add an op-amp to make an active filter?",
        "A passive RC filter drives loads poorly and has a fixed Q; an active filter (Sallen-Key or MFB) has adjustable gain, isolates stages and lets you set Q. This tool is an aid for electrical engineering calculation; its results serve only scheme design, preliminary engineering study and teaching reference, and do not replace formal electrical design, IEC/NEC standards or the final judgement of a certified engineer.",
    ]))

if __name__ == '__main__':
    main()
