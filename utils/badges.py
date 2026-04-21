"""
CarbonSnap – Badge & Achievement System
"""
from datetime import datetime, date

BADGE_CATALOGUE = {
    # Streak badges
    "streak_3":    {"emoji": "🔥", "title": "Green Streak",       "desc": "3 days of tracking",           "xp": 30},
    "streak_7":    {"emoji": "🌿", "title": "Week Warrior",        "desc": "7 consecutive days tracked",    "xp": 70},
    "streak_30":   {"emoji": "🏆", "title": "Eco Hero",            "desc": "30 days streak!",               "xp": 300},

    # Emission level badges
    "below_avg":   {"emoji": "🌱", "title": "Below Average",       "desc": "Footprint < India avg (4kg)",   "xp": 20},
    "eco_champ":   {"emoji": "🥇", "title": "Eco Champion",        "desc": "Daily footprint ≤ 2 kg",        "xp": 50},
    "net_zero_day":{"emoji": "⚡", "title": "Net Zero Day",        "desc": "Achieved 0 extra emissions",    "xp": 100},

    # Challenge badges
    "no_car_day":  {"emoji": "🚗", "title": "No-Car Day",          "desc": "Zero transport emissions",      "xp": 40},
    "vegan_day":   {"emoji": "🥗", "title": "Plant Power",         "desc": "Zero animal product emissions", "xp": 40},
    "zero_waste":  {"emoji": "♻️", "title": "Zero Waster",        "desc": "Zero landfill waste today",     "xp": 40},
    "solar_day":   {"emoji": "☀️", "title": "Sun Powered",         "desc": "Electricity < 0.5 kWh",         "xp": 40},

    # Reduction badges
    "reduced_10":  {"emoji": "📉", "title": "10% Reducer",         "desc": "Cut weekly avg by 10%",         "xp": 60},
    "reduced_20":  {"emoji": "📊", "title": "20% Reducer",         "desc": "Cut weekly avg by 20%",         "xp": 120},

    # Social
    "first_share": {"emoji": "📤", "title": "Eco Ambassador",      "desc": "Shared your report",            "xp": 25},
    "first_entry": {"emoji": "🌍", "title": "Carbon Tracker",      "desc": "First footprint calculation",   "xp": 10},
}


def award_badges(history: list, session_state) -> list[str]:
    """
    Evaluate history and award new badges.
    Returns list of newly awarded badge keys.
    """
    if not hasattr(session_state, "badges"):
        session_state.badges = set()
    if not hasattr(session_state, "xp"):
        session_state.xp = 0

    newly_awarded = []
    already = session_state.badges

    # First entry
    if history and "first_entry" not in already:
        newly_awarded.append("first_entry")

    # Streak calculation
    if len(history) >= 1:
        streak = _calculate_streak(history)
        if streak >= 3 and "streak_3" not in already:
            newly_awarded.append("streak_3")
        if streak >= 7 and "streak_7" not in already:
            newly_awarded.append("streak_7")
        if streak >= 30 and "streak_30" not in already:
            newly_awarded.append("streak_30")

    # Emission-based
    if history:
        last = history[-1]
        total = last.get("total_kg", 99)
        if total <= 4.0 and "below_avg" not in already:
            newly_awarded.append("below_avg")
        if total <= 2.0 and "eco_champ" not in already:
            newly_awarded.append("eco_champ")
        if total == 0.0 and "net_zero_day" not in already:
            newly_awarded.append("net_zero_day")

        # Category-specific
        transport_kg = last.get("transport_kg", 99)
        food_kg = last.get("food_kg", 99)
        waste_kg = last.get("waste_kg", 99)
        energy_kwh = last.get("electricity", 99)

        if transport_kg == 0 and "no_car_day" not in already:
            newly_awarded.append("no_car_day")
        if food_kg == 0.0 and "vegan_day" not in already:
            newly_awarded.append("vegan_day")
        if waste_kg == 0 and "zero_waste" not in already:
            newly_awarded.append("zero_waste")
        if energy_kwh <= 0.5 and "solar_day" not in already:
            newly_awarded.append("solar_day")

    # Reduction badges (compare weekly averages)
    if len(history) >= 14:
        recent_avg = sum(h["total_kg"] for h in history[-7:]) / 7
        prev_avg = sum(h["total_kg"] for h in history[-14:-7]) / 7
        if prev_avg > 0:
            pct_reduction = (prev_avg - recent_avg) / prev_avg * 100
            if pct_reduction >= 10 and "reduced_10" not in already:
                newly_awarded.append("reduced_10")
            if pct_reduction >= 20 and "reduced_20" not in already:
                newly_awarded.append("reduced_20")

    # Award
    for badge in newly_awarded:
        session_state.badges.add(badge)
        new_xp = getattr(session_state, "xp", 0) + BADGE_CATALOGUE[badge]["xp"]
        session_state.xp = new_xp

        user_id = session_state.get("user_id")
        if user_id:
            from utils.auth_db import save_badge_db, save_xp_db
            save_badge_db(user_id, badge)
            save_xp_db(user_id, new_xp)

    return newly_awarded


def get_level(xp: int) -> tuple[str, str, int]:
    """Return (level_name, emoji, next_level_xp)."""
    levels = [
        (0,   "Seedling",      "🌱", 100),
        (100, "Green Walker",  "🚶", 300),
        (300, "Eco Rider",     "🚲", 600),
        (600, "Green Warrior", "⚔️", 1000),
        (1000,"Planet Saver",  "🌍", 2000),
        (2000,"Carbon Hero",   "🦸", 9999),
    ]
    level_name, emoji, next_xp = "Seedling", "🌱", 100
    for threshold, name, em, nxt in levels:
        if xp >= threshold:
            level_name, emoji, next_xp = name, em, nxt
    return level_name, emoji, next_xp


def _calculate_streak(history: list) -> int:
    """Calculate current consecutive daily streak."""
    if not history:
        return 0
    dates = sorted(set(
        h["date"] if isinstance(h["date"], date) else datetime.strptime(h["date"], "%Y-%m-%d").date()
        for h in history
    ), reverse=True)
    streak = 1
    for i in range(1, len(dates)):
        delta = (dates[i - 1] - dates[i]).days
        if delta == 1:
            streak += 1
        else:
            break
    return streak
