"""
CarbonSnap – Personalized Tip Generator
"""

TIPS_DB = {
    "Transport": [
        ("🚲", "Bike 10 km instead of driving → save **2.5 kg CO₂e/day**"),
        ("🚌", "Take the bus instead of a petrol car → cut emissions by **65%** per trip"),
        ("🚇", "Switch one car trip to metro → save up to **3 kg** per 10 km"),
        ("🛵", "Carpool with 1 friend → halve your transport footprint instantly"),
        ("✈️", "Replace 1 domestic flight with a train → save **~150 kg CO₂e**"),
        ("🌿", "Inflate tyres properly → improve fuel efficiency by **3%**"),
        ("🅿️", "Work from home just 2 days/week → cut weekly transport by **40%**"),
    ],
    "Energy": [
        ("💡", "Switch to LED bulbs → save **0.05 kg CO₂e per hour** of lighting"),
        ("❄️", "Set AC at 24°C instead of 20°C → reduce electricity use by **24%**"),
        ("🌞", "Install a 1 kW solar panel → offset **0.75 kg CO₂e/kWh** generated"),
        ("🔌", "Unplug standby devices → save **0.3 kWh/day** (~225 g CO₂e)"),
        ("🪟", "Use natural ventilation before turning on AC → save 1–2 kWh/day"),
        ("🔥", "Use induction cooktop instead of LPG → cut cooking emissions by **30%**"),
        ("🌬️", "Dry clothes in sun instead of dryer → save **1.8 kg CO₂e** per load"),
    ],
    "Food": [
        ("🥗", "One meat-free day/week → save **~1 kg CO₂e** per meal"),
        ("🐄", "Replace beef with chicken → reduce food emissions by **75%**"),
        ("🌱", "Go plant-based 3 days/week → save up to **5 kg CO₂e/week**"),
        ("🛒", "Buy local & seasonal produce → reduce food miles by **50%**"),
        ("🥦", "Add one extra veg serving daily → save **0.3 kg CO₂e**"),
        ("♻️", "Reduce food waste by 30% → save **~0.45 kg CO₂e/day**"),
        ("🫘", "Swap rice for millets twice a week → cut grain emissions by **60%**"),
    ],
    "Waste": [
        ("♻️", "Recycle 1 kg plastic → save **1.5 kg CO₂e** vs landfill"),
        ("🌱", "Compost kitchen scraps → divert 2 kg/week, save **1 kg CO₂e**"),
        ("🛍️", "Use a reusable bag → avoid **0.02 kg CO₂e** per plastic bag"),
        ("🧴", "Buy refillable products → reduce packaging waste by **70%**"),
        ("📱", "Donate old electronics → avoid **80 kg CO₂e** of e-waste per device"),
        ("💧", "Fix leaking taps → save water heating energy = **0.1 kg CO₂e/day**"),
    ],
    "General": [
        ("🌳", "Plant 1 tree → offset **~21 kg CO₂** per year"),
        ("🏠", "Switch to green electricity tariff → zero grid emissions"),
        ("📊", "Track your footprint daily → awareness alone reduces by **15%**"),
        ("👥", "Share this app with 3 friends → multiply your impact by 4x"),
    ],
}


def generate_tips(total: float, top_category: str, n: int = 4) -> list[dict]:
    """
    Generate personalized tips based on total footprint and top category.

    Returns list of dicts: {emoji, tip, savings_hint}
    """
    tips = []

    # Category-specific tips first
    cat_tips = TIPS_DB.get(top_category, [])
    for emoji, tip in cat_tips[:n]:
        tips.append({"emoji": emoji, "tip": tip, "category": top_category})

    # Fill remaining from General
    remaining = n - len(tips)
    for emoji, tip in TIPS_DB["General"][:remaining]:
        tips.append({"emoji": emoji, "tip": tip, "category": "General"})

    # Severity-based headline message
    if total <= 2.0:
        headline = "🎉 Amazing! You're well below the India average (4 kg/day). Keep it up!"
    elif total <= 4.0:
        headline = f"🌍 You're at the India average. Small changes can make you **Eco Champion**!"
    elif total <= 7.0:
        headline = f"⚠️ Your {top_category} is the biggest contributor. Focus here for max impact!"
    else:
        headline = f"🔥 High emissions detected! Start with **{top_category}** — biggest win possible."

    return {"headline": headline, "tips": tips}


def get_quick_win(top_category: str) -> str:
    """Return a single high-impact quick win for the top category."""
    quick_wins = {
        "Transport": "🚲 Bike or take metro for 1 trip today → save 1–3 kg instantly!",
        "Energy":    "❄️ Raise AC by 2°C right now → save 0.15 kg CO₂e per hour!",
        "Food":      "🥗 Skip meat at your next meal → save 1–5 kg CO₂e!",
        "Waste":     "♻️ Sort your waste into wet/dry bags today → easy impact!",
    }
    return quick_wins.get(top_category, "🌱 Track consistently for 7 days to unlock Green Streak badge!")
