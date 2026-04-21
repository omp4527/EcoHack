"""
CarbonSnap – Session-state based history persistence.
Also provides CSV export/import for demo purposes.
"""
import json
import pandas as pd
from datetime import date, datetime
import streamlit as st


HISTORY_KEY = "carbonsnap_history"
MAX_HISTORY = 365   # Keep 1 year max


def save_history(entry: dict):
    """
    Save a daily entry to session_state history.
    entry must contain: {date, total_kg, transport_kg, energy_kg, food_kg, waste_kg}
    """
    # Ensure date is serialisable string
    if isinstance(entry.get("date"), date):
        entry["date"] = entry["date"].isoformat()

    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []

    # Avoid duplicate for same date
    history = st.session_state[HISTORY_KEY]
    history = [h for h in history if h.get("date") != entry["date"]]
    history.append(entry)
    history = sorted(history, key=lambda x: x["date"])[-MAX_HISTORY:]
    st.session_state[HISTORY_KEY] = history


def load_history() -> list:
    """Load history from session_state."""
    return st.session_state.get(HISTORY_KEY, [])


def get_history_df() -> pd.DataFrame:
    """Return history as a DataFrame for display."""
    history = load_history()
    if not history:
        return pd.DataFrame()
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False)
    return df


def history_to_csv() -> bytes:
    """Export history to CSV bytes."""
    df = get_history_df()
    if df.empty:
        return b""
    return df.to_csv(index=False).encode("utf-8")


def seed_demo_history():
    """Seed realistic 14-day demo data for demo mode."""
    import random
    import numpy as np
    from datetime import timedelta

    demo = []
    today = date.today()
    base = 4.5
    for i in range(14):
        d = today - timedelta(days=13 - i)
        # Slightly declining trend + noise
        total = max(0.5, base - i * 0.08 + random.uniform(-0.5, 0.5))
        transport = total * 0.40 + random.uniform(-0.2, 0.2)
        energy = total * 0.25 + random.uniform(-0.1, 0.1)
        food = total * 0.28 + random.uniform(-0.15, 0.15)
        waste = max(0, total - transport - energy - food)
        demo.append({
            "date": d.isoformat(),
            "total_kg": round(total, 3),
            "transport_kg": round(max(0, transport), 3),
            "energy_kg": round(max(0, energy), 3),
            "food_kg": round(max(0, food), 3),
            "waste_kg": round(max(0, waste), 3),
            "electricity": round(random.uniform(2, 8), 2),
            "car_petrol": round(random.uniform(5, 20), 1),
        })
    st.session_state[HISTORY_KEY] = demo

    # If logged in, update the DB as well!
    user_id = st.session_state.get("user_id")
    if user_id:
        from utils.auth_db import save_history_db
        for entry in demo:
            save_history_db(user_id, entry)

