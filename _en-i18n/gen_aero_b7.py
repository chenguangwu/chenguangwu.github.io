#!/usr/bin/env python3
# aerospace batch7 (4 slugs + index)
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'aerospace')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'aerospace')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EN = {
'mach-number': [
"Mach Number",
"/ Mach Number",
'📖 View the "Mach Number Guide"',
"At 15°C sea level the speed of sound is about 340 m/s.",
"M>1 is supersonic.",
"📚 In-Depth Analysis: Mach Number",
"Compute the Mach number M=V/a from the speed V and the local speed of sound a=√(γRT) to judge subsonic/transonic/supersonic.",
"Compare the speed of sound at different temperatures/altitudes to see the Mach number for the same true speed.",
"Assess the risk of the transonic drag rise (sound barrier).",
"Mach number at 15°C sea level",
"Temperature T=15°C=288 K, ",
"=1.4 and gas constant R=287 J/(kg·K). Speed of sound a=√(1.4×287×288)≈340 m/s. If the flight speed V=340 m/s, then M=1.0 (exactly the speed of sound).",
"Why does the speed of sound change with temperature?",
"a=√(γRT), so the higher the temperature, the greater the speed of sound. The upper atmosphere is thin but colder, so the speed of sound is actually slightly lower; hence the same true speed corresponds to a higher Mach number at altitude, which is why transonic conditions are defined by Mach rather than true speed.",
"Is M=1 necessarily the sound barrier?",
"M=1 is the speed-of-sound point, but the sharp drag rise occurs in the transonic region M≈0.8-1.2 (local shock waves). Modern airliners cruise at M≈0.78-0.85, deliberately avoiding the strong shock region to save fuel.",
],
'escape-velocity': [
"Escape Velocity from Gravitational Parameter and Radius",
"Enter the gravitational parameter μ and body radius r to find the escape velocity.",
"/ Escape Velocity Calculator",
'📖 View the "Escape Velocity from Gravitational Parameter and Radius Guide"',
"The escape velocity is √2 times the circular orbital velocity.",
"📚 In-Depth Analysis: Escape Velocity from Gravitational Parameter and Radius",
"Compute the escape velocity v_e=√(2μ/r) from the gravitational parameter μ and the surface (or starting) radius r.",
"Compare the escape velocities of Earth/Moon/Mars to assess the probe launch difficulty.",
"Given the escape velocity, back-calculate the minimum orbital-altitude kinetic energy required.",
"Earth escape velocity",
"Earth gravitational parameter μ=3.986×10¹⁴ m³/s² and radius r=6.371×10⁶ m. v_e=√(2×3.986e14/6.371e6)=√(1.251e8)≈11186 m/s ≈ 11.2 km/s. That is, the second cosmic velocity.",
"What is the relationship between escape velocity and the first cosmic velocity?",
"The first cosmic velocity (circular orbit) v_c=√(μ/r) and the escape velocity v_e=√2·v_c. For Earth v_c≈7.9 km/s and v_e≈11.2 km/s, differing by a factor of √2.",
"How much speed is needed to escape at orbital altitude?",
"The larger the starting radius r (the higher), the smaller v_e. Escaping from geosynchronous altitude needs far less additional speed than the 11.2 at the surface, because part of the orbital velocity is already available. This tool computes with the given r.",
],
'dynamic-pressure': [
"Dynamic Pressure from Air Density and Speed",
"Enter the air density ρ and speed v to find the dynamic pressure.",
"/ Dynamic Pressure Calculator",
'📖 View the "Dynamic Pressure Guide"',
"Dynamic pressure is the basis of aerodynamic forces.",
"📚 In-Depth Analysis: Dynamic Pressure from Air Density and Speed",
"A core aerodynamic load quantity: q=½ρv², used for lift, drag and control-surface load calculations.",
"Compare the dynamic pressure at different altitudes (density falls) to see how control effectiveness changes.",
"Given the structural dynamic-pressure limit, back-calculate the maximum allowable airspeed.",
"Sea-level dynamic pressure",
"Air density ρ=1.225 kg/m³ and speed v=100 m/s, so dynamic pressure q=½×1.225×100²=6125 Pa (≈0.061 atmosphere). The greater the dynamic pressure, the higher the aerodynamic load and control effectiveness.",
"What is the relationship between dynamic pressure and airspeed?",
"Dynamic pressure is proportional to the square of the true airspeed and proportional to density. The same indicated airspeed gives a lower dynamic pressure at altitude (low density), which is why controls feel softer at altitude and the stall true speed is higher.",
"Why do aircraft have a dynamic-pressure limit?",
"Structures (control surfaces, fuselage) and aeroelasticity (flutter) are all constrained by a dynamic-pressure ceiling; exceeding it may cause structural or control problems at some altitude/speed combination, so the flight envelope is defined jointly by dynamic pressure and Mach number.",
],
'centripetal-accel': [
"Centripetal Acceleration from Speed and Turn Radius",
"Enter the speed v and turn radius r to find the centripetal acceleration.",
"/ Centripetal Acceleration Calculator",
'📖 View the "Centripetal Acceleration from Speed and Turn Radius Guide"',
"The source of manoeuvring flight loads.",
"📚 In-Depth Analysis: Centripetal Acceleration from Speed and Turn Radius",
"In manoeuvring flight or a ground turn, compute the centripetal acceleration a=v²/r from the speed v and turn radius r.",
"Divide a by g to get the equivalent g-load and judge whether it exceeds occupant comfort or structural limits.",
"Given the allowable centripetal acceleration, back-calculate the safe turn radius.",
"Coordinated turn centripetal acceleration",
"Speed v=100 m/s and turn radius r=500 m, so centripetal acceleration a=v²/r=10000/500=20 m/s²≈2.04g. The occupants feel a load of about 2g, and both comfort and structure need assessment.",
"What is the relationship between centripetal acceleration and load factor?",
"In a manoeuvre the total load factor n≈√(1+(a/g)²) (in a level turn the horizontal centripetal component adds to gravity), with a small-angle approximation n≈1+a/g. This tool computes the pure centripetal component a, to be used together with the bank-angle and load-factor tools.",
"Does a ground turn count too?",
"Yes; cars, trains and aircraft taxiing on the ground all use the same formula for turns. Aviation focuses more on the occupants g sensation and the structure, while ground vehicles focus more on sideslip and wheel track.",
],
'index': [
"🚀 Aerospace Tools",
"Aerospace",
"Aerospace Tools",
"Bank-Angle Load Factor Calculator",
"Enter the manoeuvre bank angle φ (degrees) and compute the load factor as n=1/cos(φ) to assess the effect of turn g-load on structure and occupants, suitable for flight mechanics analysis and manoeuvre-envelope checks.",
"Wing Area from Wing Loading Calculator",
"Required wing area from weight and wing loading",
"Centripetal acceleration from speed and turn radius",
"Velocity from gravitational parameter and orbital radius",
"Rocket Delta-v Calculator",
"Delta-v from specific-impulse equivalent velocity and mass ratio",
"Orbital Period Calculator",
"Orbital period calculator: enter the central body gravitational parameter μ and orbital radius r to find the orbital period by T=2pi·√(r³/μ), used for satellite and spacecraft orbit design.",
"Escape velocity from gravitational parameter and radius",
"Dynamic pressure calculator: enter the air density ρ and speed v to find the dynamic pressure by q=½·ρ·v², used for aerodynamic load and aircraft force analysis.",
"Aspect Ratio Calculator",
"Wing aspect ratio calculator: enter the wingspan b and wing area S to find the aspect ratio by AR=b²/S, used for aerodynamic efficiency and wing configuration analysis.",
"Reynolds number from density, speed, characteristic length and viscosity",
"Lift Equation Calculator",
"Lift from dynamic pressure, lift coefficient and area",
"Drag Calculator",
"Drag from dynamic pressure, drag coefficient and area",
"Cross-time-zone flight time conversion: enter the departure and arrival local times to automatically compute the actual flight duration and the time difference",
"Correct the baseline takeoff length for airport elevation, air temperature and runway slope to compute the actual required runway length, used for flight performance assessment.",
"Aircraft weight and balance: compute the center of gravity from the station loads and arms and check whether it is within the allowed range",
"Look up and convert the dimensions, load and volume specifications of air cargo unit load devices (ULDs), aiding load planning and container selection, suitable for freight forwarders, flight loading and ground handling.",
"Based on elevation, air temperature and type performance parameters, correct and compute the takeoff/landing runway length required, suitable for flight planning, airport operation assessment and performance-limited analysis.",
"Estimate sector fuel burn from the type cruise fuel flow and flight distance or time, including taxi and reserve fuel, suitable for flight fuel accounting.",
"Enter the terminal area, number of security lanes and other parameters to assess passenger handling capacity and security throughput, aiding airport operations and resource allocation.",
"Summarise the baggage piece count and total weight of a flight or task, with statistics grouped by class or person, and check whether the load limit is exceeded, for air loading and baggage management accounting.",
"Lift-to-drag ratio (L/D) online calculator: enter the lift and drag to find the aerodynamic efficiency, used for glide-ratio and range optimisation analysis, running fully in the front end.",
"T/W = Thrust / Weight",
"Enter the engine thrust and aircraft weight to compute the thrust-to-weight ratio T/W, measuring acceleration and climb capability, suitable for aircraft preliminary design, powerplant selection and performance benchmarking.",
"Turn Rate",
"Turn rate online calculator: enter the speed and turn radius (or bank) to find the angular velocity, used for manoeuvre analysis and trajectory planning, running fully in the front end.",
"Lift coefficient Cl versus angle of attack α for an airfoil, plotting stall behaviour with a thin-airfoil model, and computing lift",
"Compute the rocket velocity increment by the Tsiolkovsky equation Δv=Ve·ln(m0/mf): enter the specific impulse and initial and final mass to assess orbit-insertion and orbit-change capability, suitable for rocket preliminary design and orbital manoeuvre estimation.",
"Payload fraction = (m0 − mf) / m0",
"Payload fraction calculator: enter the initial mass m0 and final mass mf to find the payload fraction by (m0−mf)/m0, assessing launch vehicle transport efficiency.",
"Wing lift online calculator: enter the dynamic pressure (or air density and speed) with the lift coefficient and wing area to find the aerodynamic lift, used for aircraft design and performance estimation, fully in the front end.",
"Specific Impulse Isp",
"Specific impulse (Isp) calculator: enter the thrust, mass flow rate and standard gravity to find the specific impulse by Isp=thrust/(mass flow rate×g0), measuring rocket engine propulsion efficiency.",
"Rate of Climb (ROC)",
"Compute the rate of climb ROC from the excess power (thrust minus drag times speed) to assess aircraft climb performance, suitable for flight performance analysis, trajectory planning and takeoff-climb checks.",
"Wing Loading W/S",
"Enter the weight and wing reference area to compute the wing loading W/S, assessing manoeuvrability, takeoff/landing speed and structural load, suitable for aircraft aerodynamic layout design, performance estimation and type comparison.",
"Descent Rate",
"Descent rate calculator: enter the true airspeed and flight path angle to find the aircraft descent vertical speed by descent rate=true airspeed×sin(flight path angle), aiding approach profile planning.",
"Coordinated Turn Radius",
"Coordinated turn radius online calculator: enter the speed and bank angle (load factor) to find the turn radius, used for trajectory planning and manoeuvre analysis, running fully in the front end.",
"Stall speed online calculator: enter the wing loading and maximum lift coefficient to find the critical stall speed, used for flight safety and performance assessment, running fully in the front end.",
"Breguet range online calculator: estimate the aircraft range from the fuel fraction, lift-to-drag ratio and cruise speed, used for aircraft performance and mission planning, running fully in the front end.",
"Thrust Required",
"Level-flight thrust-required online calculator: enter the lift and drag coefficients (or drag) to find the thrust needed to maintain level flight, used for range and performance analysis, fully in the front end.",
"Load Factor n",
"Coordinated turn load factor calculator: enter the bank angle φ to find the load factor by n=1/cosφ, used for aircraft structural design loads and manoeuvre-envelope analysis.",
"Mach Number",
"Mach number online calculator: enter the flight speed and local speed of sound to find the Mach number and judge subsonic/supersonic, suitable for aerodynamics teaching, running fully in the front end.",
'About "Aerospace Tools"',
"The Aerospace Tools collection includes 37 free online tools covering common calculation, conversion and lookup needs in aerospace scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find practical tools here that are ready to use. All tools run fully in the front end, no data is uploaded to a server and your privacy is protected.",
"The aerospace tools included on this page include (some representative tools):",
"These tools help you quickly complete common aerospace tasks without memorising complex formulas or doing manual conversions; just enter the values to get the result.",
"Do the aerospace tools require a download or registration?",
"No. All the aerospace tools on this page are pure front-end online tools that work as soon as you open the page, with no software to install, no account to register and no data uploaded.",
"Are the calculation results of the aerospace tools accurate? Is the data safe?",
"The tools compute locally in your browser based on public mathematical formulas and common industry standards, with instant results. All calculations are done locally on your device and data is not uploaded to a server, so privacy is safeguarded.",
],
}

# term-link nodes missed by extract: zh -> en
EXTRA = {
'mach-number': {'比热比 γ': 'specific heat ratio γ'},
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
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
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
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('!! %s EXTRA CJK/CNP violation: %s' % (slug, en[:60]))
            sys.exit(1)
        mp[z] = en
    return mp

def write(slug, mp):
    os.makedirs(OUT, exist_ok=True)
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('name', slug)
    out = {'slug': slug, 'industry': 'aerospace', 'name': name, 'map': mp}
    p = os.path.join(OUT, slug + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a', encoding='utf-8').write('\n')
    print('WROTE %s (+%d)' % (slug, len(mp)))

for slug, en_list in EN.items():
    write(slug, build(slug, en_list))
