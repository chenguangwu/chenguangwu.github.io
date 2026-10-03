#!/usr/bin/env python3
from head_maritime import build, write


def main():
    write('anchorage-capacity', build('anchorage-capacity', [
        '🧊 Anchorage Capacity Design',
        'Computes the swinging radius of a single vessel at anchor, the anchoring area required and the number of vessels an anchorage can hold',
        'Core formula (by input variables): π × swingRadius × swingRadius; anchorageKm2 × 1000000',
        '/ Anchorage Capacity Design',
        '📖 View the guide to anchorage capacity design',
        '📖 Anchoring design notes',
        '📚 In-depth: anchorage capacity design',
        'When planning an anchorage or assessing a port expansion, use this tool to derive the swinging radius and footprint of a single vessel from ship length, water depth, cable scope factor and safety margin, and to estimate how many vessels the anchorage can hold.',
        'Choose the cable scope factor for open or sheltered waters (usually 4 to 7 times the depth), and assess whether the safety margin is sufficient in strong wind or current and whether dragging is likely.',
        'Comparing the two layouts, circular swinging anchorage and square fixed berths: the former lets every vessel swing independently without interference but takes more space, while the latter packs berths tightly but requires strict control so no swinging radius crosses a boundary.',
        'Example: number of vessels an anchorage can hold',
        'An anchorage of 10 km², ship length 200 m, depth 20 m, cable scope 5 times, safety margin 50 m and a circular layout. Cable length = 20 × 5 = 100 m; swinging radius = 100 + 200 + 50 = 350 m; area per vessel = π × 350² ≈ 384,845 m²; vessels held = ⌊10 × 10⁶ ÷ 384,845⌋ = 25. With a square layout instead (berth spacing 2 × 350 = 700 m), the area per vessel is 700² = 490,000 m², holding ⌊10 × 10⁶ ÷ 490,000⌋ = 20 — the circular layout saves space, but anchor chains must be kept from tangling.',
        'What cable scope factor is appropriate?',
        'Sheltered waters can go as low as 3 to 4 times the depth, while open or windy waters suggest at least 6 times (this tool treats more than 7 times as suited to severe conditions). Too short a scope gives an insufficient swinging radius and the vessel drags in strong wind; too long takes more room and increases chain wear.',
        'How do you choose between the circular and square layouts?',
        'In a circular swinging anchorage each vessel swings independently around its own anchor without interfering with others, occupying πR² per vessel (R being the swinging radius); square fixed berths pack vessels tightly (spacing 2R) but require that no vessel’s swing crosses its boundary, suiting well-ordered fixed-berth anchorages.',
        'About anchorage capacity design',
    ]))

    write('compass-correction', build('compass-correction', [
        '⚓ Magnetic Compass Correction',
        'Magnetic compass deviation correction: conversion between true heading, magnetic heading and compass heading, plus deviation table generation',
        'Computes magnetic compass deviation correction, the conversion between true heading, magnetic heading and compass heading, and the generation of the deviation table from the inputs, then outputs the result.',
        '/ Magnetic Compass Correction',
        '📖 View the guide to magnetic compass correction',
        '📋 Compass deviation correction table',
        '📖 Compass correction principles',
        '📚 In-depth: magnetic compass correction',
        'In dead reckoning, convert between compass heading (CH), magnetic heading (MH) and true heading (TH) using variation (Var) and deviation (Dev), to meet passage planning and collision avoidance needs.',
        'After a compass self-check or a newly installed compass, use the five-coefficient method (A/B/C/D/E) to draw up a deviation table and quantify the deviation correction for each compass heading.',
        'When working on charts or comparing GPS offsets, correct the compass reading to a true north basis to remove the heading error caused by compass error (Dev + Var).',
        'Example: finding the true heading from the compass heading',
        'In an area with variation Var = 5°E and deviation Dev = 3°E, with compass heading CH = 090°, find the true heading. Compass error = Dev + Var = 3 + 5 = 8°E; magnetic heading MH = 090 + 3 = 093°; true heading TH = 093 + 5 = 098°. In reverse (true to compass), subtract the corrections in turn: CH = TH − Var − Dev.',
        'What is the difference between variation and deviation?',
        'Variation is the angle between magnetic north and true north (it changes by area and by year), while deviation is the interference of the ship’s magnetic materials with the compass (it changes with the ship’s heading); compass error = Dev + Var is the total difference between the compass reading and true north. At sea, looking up the deviation table by the ship’s heading and applying the correction cancels it out.',
        'How is the five-coefficient deviation table used?',
        'Deviation Dev = A + B·sin(CH) + C·cos(CH) + D·sin(2CH) + E·cos(2CH), with the coefficients fitted from measured compass headings. Each compass heading CH in the table has a matching correction; at sea, look up the value for the current heading, add or subtract it to get the magnetic heading, then add the variation to get the true heading.',
        'About magnetic compass correction',
    ]))

    write('speed-distance', build('speed-distance', [
        '🏎️ Speed and Distance Conversion',
        'Converts the three quantities of nautical speed, distance and time, supporting knots, km/h and m/s',
        'Core formula (by input variables): Math.floor((totalMin % 1440) ÷ 60); Math.floor(totalMin ÷ 1440); Math.round(totalMin % 60)',
        '/ Speed and Distance Conversion',
        '📖 View the guide to speed and distance conversion',
        '📖 Nautical unit notes',
        'Time = distance ÷ speed',
        '📚 In-depth: speed and distance conversion',
        'When drawing up a passage plan, find the distance from a known speed and time (or the speed or time needed for a known distance), and schedule the arrival time and fuel budget.',
        'Convert between different units (knots/kn, km/h, m/s; nautical miles/nm, km, m; hours/days/minutes) so that the logbook and chart annotations are consistent.',
        'When estimating ETA or deciding whether to avoid a tropical storm or reroute, quickly assess how a speed change affects the arrival time.',
        'Distance and multi-unit',
        'A vessel sails at 12 knots for 10 hours. Distance = 12 × 10 = 120 nautical miles = 120 × 1.852 ≈ 222.24 km (≈ 222,240 m); the speed in other units is 12 kn ≈ 22.224 km/h ≈ 6.17 m/s. To reach a port 300 nautical miles away within 24 hours, the required speed = 300 ÷ 24 ≈ 12.5 knots.',
        'How do knots convert to km/h?',
        '1 knot = 1 nautical mile per hour = 1.852 km/h ≈ 0.5144 m/s; a distance of 1 nautical mile = 1.852 km = 1852 m. The tool has these constants built in and converts any input unit automatically into nautical miles, knots and hours.',
        'Why does navigation use nautical miles rather than kilometres?',
        'A nautical mile is based on one minute of latitude arc, so it corresponds directly to latitude and longitude and fits charts and track plotting naturally; kilometres suit land better. This tool handles the cross-domain conversion and avoids manual conversion errors.',
        'About speed and distance conversion',
    ]))

    write('stowage-factor', build('stowage-factor', [
        '🧮 Stowage Factor Calculator',
        'Calculates the cargo stowage factor (SF) and checks hold capacity: judges whether a cargo is heavy or light and works out the hold capacity required',
        'Core formula (by input variables): min(maxByCapacity, maxByWeight); sf × 35.88',
        '/ Stowage Factor Calculation',
        '📖 View the guide to stowage factor calculation',
        '📖 Stowage factor notes',
        'Cement: 0.7-0.9 m³/t',
        '📚 In-depth: stowage factor calculation',
        'Before stowage planning, use the stowage factor SF (volume / weight) to judge whether a cargo is heavy (capacity-limited) or light (deadweight-limited), guiding the allocation of space and weight.',
        'Given the total cargo quantity and SF, work back to the hold capacity required and the capacity and deadweight utilization, and judge whether capacity or deadweight will be exceeded.',
        'For bulk cargoes or container stowage, compare the maximum load allowed by capacity with that allowed by deadweight to identify the binding constraint (capacity or deadweight).',
        'Example: cargo classification and maximum load',
        'A cargo has volume 150 m³ and weight 100 t, so SF = 150 ÷ 100 = 1.5 m³/t (≈ 53.82 ft³/LT) and density = 100 ÷ 150 ≈ 0.67 t/m³, making it a light cargo (capacity-limited, 1.3 ≤ SF < 2.0). For a load of 5000 t with SF = 1.5, hold capacity 8000 m³ and deadweight 10000 t: required capacity = 5000 × 1.5 = 7500 m³, capacity utilization 93.75%, deadweight utilization 50%; the maximum load allowed by capacity = 8000 ÷ 1.5 ≈ 5333 t, below the deadweight of 10000 t, so capacity is the bottleneck and at most 5333 t can be loaded.',
        'What does a large stowage factor SF mean?',
        'SF = volume / weight; the larger the value the more bulky the cargo (a light cargo), so capacity fills before deadweight; the smaller the SF the denser the cargo (a heavy cargo), so deadweight fills before capacity. Rule of thumb: below 0.6 heavy, 0.6 to 1.3 medium, 1.3 to 2.0 light, 2.0 or above extremely light.',
        'How do you judge whether capacity or deadweight is the constraint?',
        'Maximum load = min(capacity ÷ SF, deadweight). If capacity ÷ SF ≤ deadweight it is capacity-limited (light cargo), otherwise deadweight-limited (heavy cargo). When stowing, make sure the actual cargo quantity does not exceed the smaller of the two, so neither capacity nor deadweight is exceeded.',
        'About stowage factor calculation',
    ]))

    write('tide-window', build('tide-window', [
        '⛅ Tidal Window Estimation',
        'Estimates the navigable tidal window from high and low water times and the tidal range, helping a vessel ride the tide in and out of port',
        'Core formula (by input variables): bestWindow.start + transitMin ÷ 2; bestWindow.end - transitMin ÷ 2; w.start + transitMin ÷ 2',
        '/ Tidal Window Estimation',
        '📖 View the guide to tidal window estimation',
        '📖 Principles of riding the tide',
        '📚 In-depth: tidal window estimation',
        'Before a large vessel enters port or crosses a shallow section, use a cosine tide model to work out the navigable period that meets the tide height required by draft plus UKC (the tidal window), and schedule the entry and exit times.',
        'Given the charted depth, the vessel draft and the under-keel clearance UKC, work back to the required tide height and search for a continuous window around high water where the tide level qualifies.',
        'When the transit time is insufficient, assess whether the passage time can be shortened (more speed or less load) or the trip rescheduled, avoiding the risk of touching bottom or running aground.',
        'Example: tidal window for riding the tide',
        'A port has high water at 12:00 (4.0 m), low water at 06:00 (1.0 m) and the next low water at 18:00 (1.2 m); charted depth 8 m, draft 9 m, UKC 0.5 m, transit time 60 minutes. Required tide height = 9 + 0.5 − 8 = 1.5 m; searching the whole tidal cycle with the cosine model, the continuous window with tide height ≥ 1.5 m is about 07:37-16:44 (547 minutes), with the best entry at 08:07 and the latest departure at 16:14. If the charted depth is already at least draft + UKC (required tide height ≤ 0), there is no need to ride the tide and passage is possible at any time.',
        'Why is the required tide height draft + UKC − charted depth?',
        'Actual depth = charted depth + tide height, and it must be at least draft + UKC (under-keel clearance); rearranging gives tide height ≥ draft + UKC − charted depth. UKC guards against squat, shallow-water effect and grounding, and is generally at least 0.5 to 1.0 m for merchant ships.',
        'Is a cosine tide model reasonable?',
        'A semidiurnal tide varies approximately as a cosine within one high-water to low-water half cycle, with cos = 1 at high water and cos = −1 at low water, which is enough for quick engineering pre-planning; precise operations should rely on the port authority tide tables or measurements. This tool is for rough window estimation and timing before a voyage.',
        'About tidal window estimation',
    ]))


if __name__ == '__main__':
    main()
