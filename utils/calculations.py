"""
CarbonSnap – Core Calculation Engine
India-specific emission factors.
"""
import pandas as pd

# ── Emission Factors (kg CO₂e per unit) ────────────────────────────────────
FACTORS = {
    # Transport (per km)
    "car_petrol":     0.25,
    "car_diesel":     0.27,
    "two_wheeler":    0.113,
    "bus":            0.089,
    "metro_train":    0.031,
    "auto_rickshaw":  0.103,
    "flight_domestic": 0.255,   # per km

    # Energy (per unit)
    "electricity":    0.75,     # per kWh – India grid 2024
    "lpg":            2.983,    # per kg
    "natural_gas":    2.204,    # per m³

    # Food (per kg consumed)
    "beef":           27.0,
    "lamb":           39.2,
    "pork":           12.1,
    "chicken":         6.9,
    "fish":            6.1,
    "eggs":            4.8,
    "dairy":           3.2,
    "rice":            2.7,
    "vegetables":      0.7,
    "fruits":          0.8,
    "pulses_legumes":  0.9,

    # Waste (per kg)
    "mixed_waste":    0.50,
    "recycled":       0.02,
    "composted":      0.10,
}

INDIA_AVG_DAILY_KG = 4.0       # kg CO₂e/day India average


def calculate_footprint(inputs: dict) -> tuple[float, pd.DataFrame]:
    """
    Calculate daily carbon footprint across all categories.

    Parameters
    ----------
    inputs : dict
        Keys should match the categories below.

    Returns
    -------
    total_kg : float
    df       : pd.DataFrame  columns=[Category, Subcategory, kg_CO2e, emoji]
    """
    rows = []

    # ── Transport ──────────────────────────────────────────────────────────
    transport_map = {
        "car_petrol":      ("Car (Petrol)",       "km"),
        "car_diesel":      ("Car (Diesel)",       "km"),
        "two_wheeler":     ("Two-Wheeler",        "km"),
        "bus":             ("Bus",                "km"),
        "metro_train":     ("Metro / Train",      "km"),
        "auto_rickshaw":   ("Auto Rickshaw",      "km"),
        "flight_domestic": ("Domestic Flight",   "km"),
    }
    for key, (label, unit) in transport_map.items():
        emoji = ""
        val = inputs.get(key, 0.0)
        if val:
            rows.append({
                "Category": "Transport",
                "Subcategory": label,
                "Value": val,
                "Unit": unit,
                "Factor": FACTORS[key],
                "kg_CO2e": round(val * FACTORS[key], 4),
                "emoji": emoji,
            })

    # ── Energy ─────────────────────────────────────────────────────────────
    energy_map = {
        "electricity": ("Electricity",    "kWh"),
        "lpg":         ("LPG",            "kg"),
        "natural_gas": ("Natural Gas",    "m³"),
    }
    for key, (label, unit) in energy_map.items():
        emoji = ""
        val = inputs.get(key, 0.0)
        if val:
            rows.append({
                "Category": "Energy",
                "Subcategory": label,
                "Value": val,
                "Unit": unit,
                "Factor": FACTORS[key],
                "kg_CO2e": round(val * FACTORS[key], 4),
                "emoji": emoji,
            })

    # ── Food ───────────────────────────────────────────────────────────────
    food_map = {
        "beef":            ("Beef"),
        "lamb":            ("Lamb / Mutton"),
        "pork":            ("Pork"),
        "chicken":         ("Chicken"),
        "fish":            ("Fish / Seafood"),
        "eggs":            ("Eggs"),
        "dairy":           ("Dairy"),
        "rice":            ("Rice"),
        "vegetables":      ("Vegetables"),
        "fruits":          ("Fruits"),
        "pulses_legumes":  ("Pulses / Legumes"),
    }
    for key, label in food_map.items():
        emoji = ""
        val = inputs.get(key, 0.0)
        if val:
            rows.append({
                "Category": "Food",
                "Subcategory": label,
                "Value": val,
                "Unit": "kg",
                "Factor": FACTORS[key],
                "kg_CO2e": round(val * FACTORS[key], 4),
                "emoji": emoji,
            })

    # ── Waste ──────────────────────────────────────────────────────────────
    waste_map = {
        "mixed_waste": ("Mixed Waste",  "kg"),
        "recycled":    ("Recycled",     "kg"),
        "composted":   ("Composted",    "kg"),
    }
    for key, (label, unit) in waste_map.items():
        emoji = ""
        val = inputs.get(key, 0.0)
        if val:
            rows.append({
                "Category": "Waste",
                "Subcategory": label,
                "Value": val,
                "Unit": unit,
                "Factor": FACTORS[key],
                "kg_CO2e": round(val * FACTORS[key], 4),
                "emoji": emoji,
            })

    if not rows:
        df = pd.DataFrame(columns=["Category","Subcategory","Value","Unit","Factor","kg_CO2e","emoji"])
        return 0.0, df

    df = pd.DataFrame(rows)
    total_kg = round(df["kg_CO2e"].sum(), 3)
    return total_kg, df


def get_category_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate kg_CO2e by Category."""
    if df.empty:
        return df
    return df.groupby("Category", as_index=False)["kg_CO2e"].sum()


def score_rating(total_kg: float) -> tuple[str, str, str]:
    """Return (grade, label, color) based on daily total."""
    if total_kg <= 2.0:
        return "A+", "Eco Champion", "#22c55e"
    elif total_kg <= 3.5:
        return "A", "Green Warrior", "#84cc16"
    elif total_kg <= 5.0:
        return "B", "Average Joe", "#f59e0b"
    elif total_kg <= 7.0:
        return "C", "High Emitter", "#f97316"
    else:
        return "D", "Carbon Heavy", "#ef4444"
