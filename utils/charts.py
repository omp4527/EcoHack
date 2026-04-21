"""
CarbonSnap – Chart Builder (Plotly)
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

CATEGORY_COLORS = {
    "Transport": "#3b82f6",
    "Energy":    "#f59e0b",
    "Food":      "#22c55e",
    "Waste":     "#a855f7",
}

def get_layout():
    import streamlit as st
    is_dark = st.session_state.get("dark_mode", True)
    font_color = "#e2e8f0" if is_dark else "#0f172a"
    
    return dict(
        template="plotly_dark" if is_dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=font_color),
        margin=dict(l=10, r=10, t=50, b=30),
        legend=dict(
            orientation="h", yanchor="top", y=-0.1,
            xanchor="center", x=0.5,
        )
    )


def get_breakdown(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """
    Returns (pie_fig, bar_fig) from breakdown DataFrame.
    """
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(**get_layout(), height=320)
        return empty_fig, empty_fig

    cat_df = df.groupby("Category", as_index=False)["kg_CO2e"].sum()
    colors = [CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_df["Category"]]

    # ── Pie Chart ────────────────────────────────────────────────────────────
    pie_fig = go.Figure(go.Pie(
        labels=cat_df["Category"],
        values=cat_df["kg_CO2e"],
        hole=0.52,
        marker=dict(colors=colors, line=dict(color="#1e293b", width=2)),
        textinfo="label+percent",
        textfont=dict(size=13),
        hovertemplate="<b>%{label}</b><br>%{value:.3f} kg CO₂e<br>%{percent}<extra></extra>",
        pull=[0.05 if cat_df["kg_CO2e"].idxmax() == i else 0 for i in cat_df.index],
    ))
    pie_fig.update_layout(
        **get_layout(),
        height=340,
        showlegend=True,
        title=dict(text="Emissions by Category", x=0.5, xanchor="center"),
        annotations=[dict(
            text=f"<b>{cat_df['kg_CO2e'].sum():.2f}</b><br>kg CO₂e",
            x=0.5, y=0.5, font_size=16, showarrow=False,
            font_color="#94a3b8"
        )]
    )

    # ── Horizontal Bar Chart (subcategory) ───────────────────────────────────
    sub_df = df.sort_values("kg_CO2e", ascending=True).copy()
    sub_df["label"] = sub_df["emoji"].fillna("") + " " + sub_df["Subcategory"]
    bar_colors = [CATEGORY_COLORS.get(c, "#94a3b8") for c in sub_df["Category"]]

    bar_fig = go.Figure(go.Bar(
        x=sub_df["kg_CO2e"],
        y=sub_df["label"],
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0.2)", width=1)),
        text=[f"{v:.3f} kg" for v in sub_df["kg_CO2e"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.4f} kg CO₂e<extra></extra>",
    ))
    bar_fig.update_layout(
        **get_layout(),
        height=max(300, 40 * len(sub_df) + 80),
        title=dict(text="Emissions by Source", x=0.5, xanchor="center"),
        xaxis_title="kg CO₂e",
        yaxis_title=None,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(showgrid=False),
    )
    return pie_fig, bar_fig


def comparison_bar(user_total: float, comparisons: dict) -> go.Figure:
    """Horizontal bar chart comparing user vs cities/averages."""
    from utils.comparison import CITY_AVERAGES, GLOBAL_BENCHMARKS

    labels, vals, bar_colors = [], [], []

    # Add global benchmarks first
    for name, val in GLOBAL_BENCHMARKS.items():
        labels.append(name)
        vals.append(val)
        bar_colors.append("#64748b")

    # User
    labels.append(f"You ({user_total:.2f} kg)")
    vals.append(user_total)
    from utils.calculations import score_rating
    _, _, color = score_rating(user_total)
    bar_colors.append(color)

    fig = go.Figure(go.Bar(
        x=vals, y=labels,
        orientation="h",
        marker=dict(color=bar_colors),
        text=[f"{v:.1f} kg" for v in vals],
        textposition="outside",
        hovertemplate="%{y}<br>%{x:.2f} kg CO₂e/day<extra></extra>",
    ))
    fig.update_layout(
        **get_layout(),
        height=300,
        title=dict(text="How You Compare", x=0.5, xanchor="center"),
        xaxis_title="kg CO₂e / day",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(showgrid=False),
    )
    return fig
