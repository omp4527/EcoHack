"""
CarbonSnap – Forecast & Projection Engine
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import date, timedelta


INDIA_AVG_DAILY_KG = 4.0


def weekly_forecast(history: list, today_total: float) -> go.Figure:
    """
    Build a 7-day trailing + 7-day forward forecast line chart.
    History items: {date, total_kg}
    """
    today = date.today()

    # ── Historical Data ────────────────────────────────────────────────────
    hist_dates, hist_vals = [], []
    if history:
        last_14 = history[-14:]
        for h in last_14:
            d = h["date"] if isinstance(h["date"], date) else \
                __import__("datetime").datetime.strptime(h["date"], "%Y-%m-%d").date()
            hist_dates.append(d)
            hist_vals.append(h["total_kg"])
    # Add today
    hist_dates.append(today)
    hist_vals.append(today_total)

    # ── Forecast: next 7 days (simple moving avg) ──────────────────────────
    window = hist_vals[-7:] if len(hist_vals) >= 7 else hist_vals
    trend_slope = 0.0
    if len(window) >= 3:
        x = np.arange(len(window))
        coeffs = np.polyfit(x, window, 1)
        trend_slope = coeffs[0]

    forecast_dates, forecast_vals, optimistic_vals = [], [], []
    for i in range(1, 8):
        fd = today + timedelta(days=i)
        fv = max(0, today_total + trend_slope * i)
        ov = max(0, today_total * (1 - 0.05 * i))   # 5% daily reduction scenario
        forecast_dates.append(fd)
        forecast_vals.append(round(fv, 3))
        optimistic_vals.append(round(ov, 3))

    # ── India avg reference ────────────────────────────────────────────────
    all_dates = hist_dates + forecast_dates
    avg_line = [INDIA_AVG_DAILY_KG] * len(all_dates)

    fig = go.Figure()

    # Historical trace
    fig.add_trace(go.Scatter(
        x=hist_dates, y=hist_vals,
        mode="lines+markers",
        name="Your Footprint",
        line=dict(color="#22c55e", width=3),
        marker=dict(size=8, symbol="circle"),
        hovertemplate="%{x|%d %b}<br>%{y:.2f} kg CO₂e<extra></extra>",
    ))

    # Forecast trace
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=forecast_vals,
        mode="lines+markers",
        name="Forecast (trend)",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        marker=dict(size=6, symbol="diamond"),
        hovertemplate="%{x|%d %b}<br>%{y:.2f} kg CO₂e<extra></extra>",
    ))

    # Optimistic scenario
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=optimistic_vals,
        mode="lines",
        name="If you reduce 5%/day",
        line=dict(color="#84cc16", width=2, dash="dot"),
        hovertemplate="%{x|%d %b}<br>%{y:.2f} kg CO₂e<extra></extra>",
    ))

    # India avg reference
    fig.add_trace(go.Scatter(
        x=all_dates, y=avg_line,
        mode="lines",
        name="India Avg (4 kg)",
        line=dict(color="#ef4444", width=1, dash="longdash"),
        hoverinfo="skip",
    ))

    # Shade forecast region
    fig.add_vrect(
        x0=str(today + timedelta(days=1)),
        x1=str(today + timedelta(days=7)),
        fillcolor="rgba(245,158,11,0.08)",
        line_width=0,
        annotation_text="Forecast →",
        annotation_position="top left",
    )

    fig.update_layout(
        title="📈 Emissions Trend & 7-Day Forecast",
        xaxis_title="Date",
        yaxis_title="kg CO₂e",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380,
        margin=dict(l=10, r=10, t=60, b=40),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
    return fig


def yearly_projection_stats(today_total: float, history: list) -> dict:
    """Return dict of yearly projection stats."""
    if history and len(history) >= 7:
        avg = sum(h["total_kg"] for h in history[-7:]) / 7
    else:
        avg = today_total

    yearly_kg = avg * 365
    yearly_tonnes = yearly_kg / 1000
    trees_needed = round(yearly_kg / 21)          # 1 tree absorbs ~21 kg/year
    india_avg_yearly = INDIA_AVG_DAILY_KG * 365
    pct_vs_avg = round((yearly_kg - india_avg_yearly) / india_avg_yearly * 100, 1)

    return {
        "yearly_kg": round(yearly_kg, 1),
        "yearly_tonnes": round(yearly_tonnes, 2),
        "trees_needed": trees_needed,
        "pct_vs_avg": pct_vs_avg,
        "weekly_kg": round(avg * 7, 2),
        "monthly_kg": round(avg * 30, 2),
    }
