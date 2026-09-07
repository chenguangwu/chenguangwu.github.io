#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""energy 分类英文 i18n 套话清理 + 补真实英文 en/ed。
更新 slug-en.json（{en,ed}）与 _en_override.json（{en,ed,ind}，保留 ind）的 energy/ key。
写回保持 ensure_ascii=False, indent=2 匹配原文件。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SL = os.path.join(ROOT, "i18n/tools/slug-en.json")
OV = os.path.join(ROOT, "i18n/tools/_en_override.json")

EN_I18N = {
"daily-irradiation": {"en":"Daily Solar Irradiation","ed":"Estimate daily/monthly solar irradiation (kWh/m²/day) from peak-sun hours, array area and tilt factor to size PV systems."},
"solar-panel-power": {"en":"Solar Panel Power","ed":"Estimate DC output and STC power of a PV array from module count, efficiency and temperature coefficient for inverter matching."},
"solar-calculator": {"en":"Solar Power Calculator","ed":"Estimate home PV system capacity, annual generation, payback period and lifetime savings from load, irradiation and tariff."},
"solar-output-physics": {"en":"Solar Output Physics","ed":"Estimate incident solar power on a tilted module from the solar constant, air mass and angle of incidence."},
"wind-power": {"en":"Wind Power Calculator","ed":"Estimate horizontal-axis turbine output with P=½ρAv³Cp from air density, swept area and wind speed."},
"wind-power-physics": {"en":"Wind Power Physics","ed":"Understand the kinetic-to-electric energy chain, Betz limit, tip-speed ratio and power curve of wind turbines."},
"wind-power-estimator": {"en":"Wind Power Estimator","ed":"Estimate annual generation and equivalent full-load hours of small/distributed turbines from capacity factor."},
"battery-capacity-wh": {"en":"Battery Capacity (Wh)","ed":"Convert Ah×V to watt-hours and compare energy capacity across cells and packs for sizing and runtime."},
"battery-life": {"en":"Battery Life Estimator","ed":"Estimate usable runtime from capacity and load current/power, accounting for depth of discharge and efficiency."},
"cop-heatpump": {"en":"Heat Pump COP","ed":"Compute coefficient of performance COP=Q/W for heat pumps and interpret SCOP and cold-weather drop."},
"heat-pump-cop": {"en":"Heat Pump Coefficient of Performance","ed":"Compute COP/EER for heating and cooling and compare seasonal efficiency ratings SCOP/SEER."},
"energy-efficiency": {"en":"Energy Efficiency","ed":"Compute efficiency η=output/input across appliances, motors, boilers and envelopes to find savings."},
"energy-payback": {"en":"Energy Payback Period","ed":"Compute energy payback time from embodied energy and annual generation for PV/wind systems."},
"lcoe": {"en":"LCOE Calculator","ed":"Compute levelized cost of electricity LCOE=(CAPEX·CRF+O&M)/annual generation to compare generation economics."},
"thermal-efficiency": {"en":"Thermal Efficiency","ed":"Compute thermal efficiency η=W/Q_in of heat engines and assess waste-heat recovery potential."},
"carnot-efficiency": {"en":"Carnot Efficiency","ed":"Compute the ideal Carnot efficiency η=1−Tc/Th as the upper bound for any heat engine."},
"power-factor": {"en":"Power Factor","ed":"Compute power factor cosφ=P/S and its impact on line loss, capacity and utility penalty."},
"r-value-insulation": {"en":"Insulation R-Value","ed":"Compute thermal resistance R=d/(k·A) and U-value to compare building envelope insulation."},
"conductive-heat-rate": {"en":"Conductive Heat Rate","ed":"Compute steady-state conduction Q=kAΔT/d from Fourier's law for insulation and heat-loss design."},
"joule-heating": {"en":"Joule Heating","ed":"Compute Joule heating P=I²R=UI for heating elements, wire heating and overload risk."},
"electrical-power": {"en":"Electrical Power","ed":"Compute electric power P=UI (AC: P=UIcosφ) and distinguish real from apparent power."},
"three-phase-power": {"en":"Three-Phase Power","ed":"Compute three-phase real power P=√3·U_L·I_L·cosφ for motors and distribution."},
"power-consumption": {"en":"Power Consumption","ed":"Compute energy (kWh) from power and time and estimate the electricity cost of devices."},
"energy-consumption": {"en":"Energy Consumption","ed":"Aggregate monthly/annual consumption across devices, locate heavy users and suggest savings."},
"energy-from-power": {"en":"Energy From Power","ed":"Compute energy E=P·t from power and duration to link power and electricity metrics."},
"energy-cost": {"en":"Energy Cost","ed":"Compute electricity cost from consumption and tariff (tiered/time-of-use) and compare savings."},
"fuel-cost": {"en":"Fuel Cost","ed":"Compute fuel cost from volume/mass and price, or per-unit-energy cost vs electricity."},
"standby-power-calculator": {"en":"Standby Power Calculator","ed":"Sum standby power of household appliances by typical wattage and estimate annual wasted electricity cost."},
"fridge-power-estimator": {"en":"Fridge Power Estimator","ed":"Estimate annual consumption and cost of a refrigerator from its rating and duty cycle."},
"estimate-time-current": {"en":"Charge/Discharge Time","ed":"Estimate charge or discharge time t=C/I from battery capacity and current, with efficiency."},
"estimate-area": {"en":"Area Estimator","ed":"Back-calculate required area from power density (PV W/m², CADR/height) for layout planning."},
"calculator-calc-power-usage": {"en":"Average Power From Energy","ed":"Compute average power P=E/t from energy and period for capacity planning (placeholder-named utility)."},
"calculator-calc-4": {"en":"Energy Converter","ed":"Convert among energy, power and time (E=P·t) for quick electricity estimates (placeholder-named utility)."},
"calculator-calc-5": {"en":"Energy Unit Calculator","ed":"Convert W/kW and Wh/kWh and estimate single-device monthly cost (placeholder-named utility)."},
"energy-calculator": {"en":"Energy Calculator","ed":"Aggregate home/shop monthly consumption and cost from a device list and suggest saving priorities."},
"kinetic-energy": {"en":"Kinetic Energy","ed":"Compute kinetic energy Ek=½mv² and its squared dependence on speed for braking and impact."},
"gravitational-potential": {"en":"Gravitational Potential Energy","ed":"Compute gravitational potential energy Ep=mgh for pumped storage and fall risk."},
"specific-energy": {"en":"Specific Energy","ed":"Compute specific energy (Wh/kg) to compare batteries and fuels by mass."},
"energy-density": {"en":"Energy Density","ed":"Compute energy density (Wh/L) to compare volume occupancy of batteries and fuels."},
"fuel-heat-value": {"en":"Fuel Calorific Value","ed":"Compute releasable heat from fuel mass/volume and LHV/HHV for boiler and cost estimates."},
"carbon-footprint": {"en":"Carbon Footprint","ed":"Compute GHG emissions (CO₂e) from activity data and emission factors for households/firms."},
"convert-emission": {"en":"Emission Unit Converter","ed":"Convert emission units (kg/t, CO₂/CO₂e) and GWP across gases for consistent accounting."},
"assessor-water-quality": {"en":"Water Quality Assessor","ed":"Assess water quality from pH, turbidity, chlorine and TDS against standards with treatment advice."},
"water-tds-evaluator": {"en":"Water TDS Evaluator","ed":"Evaluate drinking/purified water grade from TDS reading and temperature, with filter-change hints."},
"air-purifier-area": {"en":"Air Purifier Area","ed":"Estimate applicable room area from CADR, ceiling height and air-change rate for selection."},
"calc-area-air": {"en":"Ventilation Area Calculator","ed":"Back-calculate area from airflow, air-change rate and height for ventilation/purifier layout."},
"calculator-calc-power": {"en":"Power Calculator","ed":"Compute electric power P=UI (AC: P=UIcosφ) as a general wattage converter."},
"heat-energy-q": {"en":"Heat Energy (Q=mcΔT)","ed":"Compute heat Q=mcΔT for heating/cooling load and thermal storage estimates."},
}

def main():
    sl = json.load(open(SL, encoding="utf-8"), strict=False)
    ov = json.load(open(OV, encoding="utf-8"), strict=False)
    n_sl = n_ov = 0
    for k, v in EN_I18N.items():
        fk = "energy/" + k
        if fk in sl:
            sl[fk]["en"] = v["en"]; sl[fk]["ed"] = v["ed"]; n_sl += 1
        if fk in ov:
            ov[fk]["en"] = v["en"]; ov[fk]["ed"] = v["ed"]; n_ov += 1
    json.dump(sl, open(SL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(ov, open(OV, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    bad = 0
    for k in EN_I18N:
        for d in (sl.get(k, {}), ov.get(k, {})):
            ed = d.get("ed", "").lower()
            if "free online tool" in ed or "free and accurate" in ed or "calculate online, free" in ed:
                bad += 1
    print(f"updated slug={n_sl} override={n_ov} boilerplate_residual={bad}")

if __name__ == "__main__":
    main()
