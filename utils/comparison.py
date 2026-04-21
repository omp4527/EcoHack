"""
CarbonSnap – Regional Comparison Engine
India city-level benchmarks (kg CO₂e per day).
"""

CITY_AVERAGES = {
    "Mumbai":       4.8,
    "Delhi":        5.2,
    "Bangalore":    4.2,
    "Pune / Pimpri": 4.0,
    "Chennai":      3.9,
    "Hyderabad":    4.3,
    "Kolkata":      3.7,
    "Ahmedabad":    4.1,
    "India Avg":    4.0,
    "Global Avg":   11.5,
    "EU Avg":       8.2,
    "US Avg":       16.0,
}

GLOBAL_BENCHMARKS = {
    "1.5°C Target (Paris)": 2.5,
    "India Sustainable":    3.0,
    "India Average":        4.0,
    "Global Average":       11.5,
}


def compare_avg(user_total: float, city: str = "Pune / Pimpri") -> dict:
    """
    Compare user's daily total against city and national averages.
    Returns comparison dict.
    """
    city_avg = CITY_AVERAGES.get(city, 4.0)
    india_avg = CITY_AVERAGES["India Avg"]
    global_avg = CITY_AVERAGES["Global Avg"]
    paris_target = 2.5

    def pct(reference):
        if reference == 0:
            return 0
        return round((user_total - reference) / reference * 100, 1)

    def msg(reference, label):
        p = pct(reference)
        if p < 0:
            return f"You're **{abs(p):.1f}% greener** than {label}! Keep it up!"
        elif p == 0:
            return f"You're exactly at the {label}."
        else:
            return f"You're **{p:.1f}% above** {label}. Room to grow!"

    return {
        "user_total": user_total,
        "city": city,
        "city_avg": city_avg,
        "india_avg": india_avg,
        "global_avg": global_avg,
        "paris_target": paris_target,
        "vs_city": pct(city_avg),
        "vs_india": pct(india_avg),
        "vs_global": pct(global_avg),
        "vs_paris": pct(paris_target),
        "msg_city": msg(city_avg, f"{city} avg"),
        "msg_india": msg(india_avg, "India avg"),
        "msg_global": msg(global_avg, "Global avg"),
        "daily_savings_vs_global": round(global_avg - user_total, 2),
    }


def get_all_city_averages() -> dict:
    return CITY_AVERAGES


def get_global_benchmarks() -> dict:
    return GLOBAL_BENCHMARKS
