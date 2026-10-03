#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'security')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'security')
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
    out = {'slug': slug, 'industry': 'security', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('earthquake-escape', build('earthquake-escape', [
        "🔤 Earthquake Escape Route Planning",
        "Generate personalized earthquake escape advice based on living environment, including shelter locations, escape routes and post-quake notes.",
        "Select residence type",
        "Floor level",
        "Low floor (1-3 stories)",
        "Mid floor (4-10 stories)",
        "High floor (11 stories and above)",
        "Generate escape plan",
        "Escape action plan",
        "Shelter-area analysis",
        "✅ Recommended shelter location",
        "❌ Dangerous area (avoid)",
        "Post-quake shelter and self-rescue points",
        "General earthquake-emergency knowledge",
        "🌍 Earthquake warning and response",
        "Golden 12 seconds:",
        "From feeling the shaking to violent shaking is about 12 seconds, a precious escape/shelter time",
        "Drop, cover, hold on:",
        "Internationally used shelter mnemonic (Drop, Cover, Hold on)",
        "Don't take the elevator:",
        "Being trapped in an elevator during a power outage in an earthquake is extremely dangerous",
        "Don't jump off the building:",
        "Injuries from jumping off a building above the second floor often exceed the earthquake itself",
        "📦 Household earthquake preparedness",
        "Secure tall furniture to prevent tipping and injury",
        "Don't hang heavy objects above the bed; keep away from windows and glass",
        "Prepare a household emergency kit (water, food, medicine, flashlight, whistle)",
        "Agree on an emergency meeting point and contact method with family",
        "Know the location of emergency shelters in your community",
        "If buried: stay calm and conserve strength; tap pipes or walls with a stone to send a distress signal; don't shout loudly to avoid inhaling dust; clear dust near mouth and nose to keep breathing unobstructed.",
        "Tool introduction and usage",
        "The earthquake escape-route planning tool generates personalized earthquake shelter plans and escape advice based on different living environments.",
        "Generate escape plan by residence layout",
        "Post-quake shelter points",
        "Dangerous-location warning",
        "General earthquake-preparedness knowledge",
        "Household earthquake preparedness",
        "Workplace safety",
        "School safety education",
        "Community emergency drill",
        "📚 In-Depth Analysis: Earthquake Escape Route Planning",
        "After moving into a new home, office building or dorm, plan nearby shelter locations and two or more evacuation routes in advance by building type.",
        "When schools or employers organize emergency drills, generate targeted shelter and evacuation points by venue (classroom / office area / shared rental).",
        "In family safety education, explain the shelter location of different rooms to the elderly and children to avoid panic during a quake.",
        "Example: generate advice for a 'high-rise apartment'",
        "For shelter, prioritize corners of load-bearing walls and small rooms (bathroom, kitchen) that easily form triangular spaces, staying away from exterior walls, glass windows and chandeliers; during the main shock never take the elevator, shelter in place, and after the shaking weakens evacuate orderly by stairs to open ground; immediately after the quake check gas valves and circuits, and only use them after confirming safety. Detached houses or villas should keep away from tall furniture and walls; school classrooms follow instructions to quickly evacuate along the planned route to the playground.",
        "Should high-floor residents run downstairs during an earthquake?",
        "During strong shaking, first shelter in place (drop, cover, hold on) and don't run blindly - crowded stairs, falling objects and dizziness all increase danger; evacuate orderly after the main shock passes. In daily life, familiarize yourself with the nearest safe stairs and outdoor meeting point.",
        "What elements should escape-route planning consider?",
        "Prepare at least two independent safe exits, avoiding glass curtain walls, tall shelves and exterior walls; choose a meeting point in open ground away from buildings; also anticipate night and power-outage scenarios, and place flashlights and emergency kits at the door and bedside to ensure they are always accessible.",
    ]))

    write('emergency-contacts', build('emergency-contacts', [
        "🔒 Emergency Contacts Panel",
        "One-tap view of common emergency numbers, supports adding custom emergency contacts. Data is saved in the local browser, accessible anytime.",
        "In an emergency, stay calm, first call the corresponding emergency-rescue number, and clearly state your location and situation.",
        "🚨 Core emergency numbers",
        "🏥 Medical and health",
        "⚡ Public service and rights",
        "📌 My custom contacts",
        "Add family, friends or community emergency contacts, saved locally.",
        "Contact name",
        "Note (optional)",
        "Add contact",
        "📞 Notes for calling emergency numbers",
        "State location clearly:",
        "Accurately report your address, floor and landmark to help rescuers locate you",
        "Describe the situation:",
        "Briefly describe what happened, how many are injured and the severity",
        "Stay on the line:",
        "Don't hang up first; wait for the operator to confirm information before hanging up",
        "Leave someone to guide:",
        "Send someone to the intersection to guide rescuers to the scene",
        "Don't dial randomly:",
        "Don't occupy emergency lines for non-emergencies, to avoid affecting others' calls for help",
        "Prepare in advance:",
        "Set up emergency contacts and SOS function on your phone",
        "Tool introduction and usage",
        "The emergency contacts panel collects nationally universal emergency-rescue numbers and public-service hotlines, and supports adding personal emergency contacts.",
        "Quick lookup of core emergency numbers",
        "Medical-health hotline",
        "Public-service rights hotline",
        "Custom contact management",
        "One-tap dialing (mobile)",
        "Saved locally, not uploaded",
        "Quick number lookup in emergencies",
        "Household safety preparation",
        "Emergency for elderly and children",
        "Travel reference",
        "📚 In-Depth Analysis: Emergency Contacts Panel",
        "When an elderly person or child at home has a sudden condition, look up the corresponding emergency number with one tap, avoiding dialing the wrong number in panic.",
        "When an accident or vehicle breakdown occurs while driving, quickly find the 122 traffic-accident and 12122 highway-rescue numbers.",
        "Add family, property management and attending doctor as custom emergency contacts for centralized use in emergencies.",
        "Common emergency-number reference",
        "Core numbers: police 110, fire 119, medical emergency 120, traffic accident 122, maritime distress 12395, forest fire 12119; medical-specific: national public-health hotline 12320, psychological aid 400-161-9995, anti-drug 12348, Red Cross rescue 999 (some cities); public-service: consumer complaint 12315, mayor hotline 12345, labor rights 12333, legal aid 12348, weather forecast 12121, road rescue 12122. Users can also add custom contacts (such as property, family) in the panel, with data stored only in the browser locally.",
        "Where are my added custom contacts stored?",
        "Stored only in this machine's browser localStorage, not uploaded to any server; therefore when switching devices, clearing cache or using incognito mode the custom contacts will not sync and need to be re-added.",
        "Are these numbers universal nationwide?",
        "110/119/120/122 etc. are core nationwide universal emergency numbers; some specific numbers vary by region, e.g. Red Cross rescue 999 is only available in some cities, and the psychological-aid hotline follows the local health commission's announcement; when traveling it is advised to confirm the destination's applicable numbers in advance.",
    ]))

    write('first-aid-kit', build('first-aid-kit', [
        "🚑 First-Aid Kit List Generator",
        "Generate a professional first-aid item list by usage scenario, supporting check-off confirmation and export/print. Better prepared than sorry; it can save lives at critical moments.",
        "Uncheck",
        "Prepared",
        "items",
        "Tip: regularly check the expiry of medicines in the first-aid kit, and replace expired items every 3-6 months. Place the kit where the whole family knows and can easily reach.",
        "First-aid kit usage advice",
        "📦 Storage location",
        "Place where the whole family knows but children cannot easily reach",
        "Avoid hot and humid environments (e.g. bathroom); medicines need dry and cool storage",
        "Car first-aid kit in a fixed position in the trunk, avoiding scattering while driving",
        "Outdoor first-aid kit carried with you or placed in an easily accessible outer pocket of the backpack",
        "🔄 Regular maintenance",
        "Check medicine expiry every 3 months",
        "Replace soon-to-expire medicines and consumables every 6 months",
        "Replenish consumed items promptly after use",
        "Regularly learn first-aid knowledge to ensure family members can use it",
        "Tool introduction and usage",
        "The first-aid kit list generator generates a professional first-aid item list by different usage scenarios, helping you prepare for emergencies.",
        "4 scenario lists",
        "Items labeled by category use",
        "Check-off to confirm preparation progress",
        "Supports export and print",
        "Includes usage and maintenance advice",
        "Household emergency preparation",
        "Car safety configuration",
        "Outdoor hiking trip",
        "Workplace backup",
        "📚 In-Depth Analysis: First-Aid Kit List Generator",
        "When moving, buying a new car or setting up an office, generate a professional first-aid item list by usage scenario and purchase accordingly.",
        "Before planning hiking, camping and other outdoor activities, generate a more targeted outdoor first-aid kit configuration.",
        "Units or families take periodic inventory, check off against the list, export/print, then replenish missing items.",
        "Example: basic configuration of a 'home first-aid kit'",
        "Recommended basics: adhesive bandages, sterile gauze and medical tape, povidone-iodine swabs or alcohol pads, scissors, tweezers, thermometer, disposable gloves, emergency medicines (antipyretic, anti-diarrhea, anti-allergy, etc.), flashlight and spare batteries, first-aid manual. Car and outdoor scenarios need additional: reflective vest, safety hammer, emergency blanket, water-purification tablets, snake/insect-bite treatment supplies; office scenarios focus on trauma and fainting. The list supports check-off confirmation and export/print, but items are only the basics.",
        "How often should medicines in the kit be checked?",
        "It is recommended to verify expiry every 3-6 months and replace expired ones immediately; liquids and ointments should be protected from freezing and high heat; fragile items (e.g. thermometer) stored separately and fixed to avoid breakage in transport.",
        "Does a list mean you can handle emergencies?",
        "No. Items are only basic support; truly saving lives depends on correct first aid. It is recommended to attend first-aid training from institutions such as the Red Cross, master skills like bleeding control, bandaging, CPR (cardiopulmonary resuscitation) and the Heimlich maneuver, and memorize the 120 emergency number.",
    ]))


if __name__ == '__main__':
    main()
