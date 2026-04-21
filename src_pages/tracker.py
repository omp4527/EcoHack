"""
CarbonSnap – Page 2: Tracker (History & Trends)
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

from utils.storage import load_history, get_history_df, history_to_csv
from utils.styles import metric_card_html


def render_tracker():
    st.markdown('<div class="section-header">Your Carbon History</div>', unsafe_allow_html=True)

    history = load_history()
    if not history:
        st.info("No history yet! Go to Dashboard, log your data and hit **Save Today's Entry**.")
        st.markdown("""
        <div style="text-align:center;padding:40px;opacity:0.5">
            <div style="font-size:4rem"></div>
            <div style="font-size:1rem;margin-top:12px;color:#94a3b8">
                Your journey of 1,000 km starts with one step. Log your first day!
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df = get_history_df()
    df_disp = df.copy()
    df_disp["date"] = df_disp["date"].dt.strftime("%d %b %Y")

    # ── Summary Stats ─────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    avg_7 = df["total_kg"].tail(7).mean() if len(df) >= 1 else 0
    best  = df["total_kg"].min()
    worst = df["total_kg"].max()
    days_tracked = len(df)

    with col1:
        st.markdown(metric_card_html(
            f"{days_tracked}", "Days Tracked", "Keep it up!", "#22c55e"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card_html(
            f"{avg_7:.2f} kg", "7-Day Avg", "vs India: 4 kg/day", "#3b82f6"
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card_html(
            f"{best:.2f} kg", "Best Day", "Personal record!", "#22c55e"
        ), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card_html(
            f"{worst:.2f} kg", "Highest Day", "Room to improve", "#f97316"
        ), unsafe_allow_html=True)

    # ── Trend Chart ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:24px">Historical Trend</div>', unsafe_allow_html=True)

    fig = go.Figure()

    # Daily line
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["total_kg"],
        mode="lines+markers", name="Daily",
        line=dict(color="#22c55e", width=2),
        marker=dict(size=7),
        fill="tozeroy", fillcolor="rgba(34,197,94,0.07)",
        hovertemplate="%{x|%d %b %Y}<br><b>%{y:.2f} kg CO₂e</b><extra></extra>",
    ))

    # 7-day rolling avg
    if len(df) >= 3:
        roll = df["total_kg"].rolling(min(7, len(df))).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=roll,
            mode="lines", name=f"{min(7,len(df))}-day avg",
            line=dict(color="#f59e0b", width=2, dash="dot"),
        ))

    # India avg
    fig.add_hline(y=4.0, line_dash="dash", line_color="#ef4444",
                  annotation_text="India Avg (4 kg)", annotation_position="bottom right")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        font=dict(family="Inter", color="#e2e8f0"),
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h"),
        hovermode="x unified",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="kg CO₂e"),
    )
    st.plotly_chart(fig, use_container_width=True, key="hist_trend")

    # ── Category Stacked Area ─────────────────────────────────────────────
    cats = ["transport_kg", "energy_kg", "food_kg", "waste_kg"]
    cat_colors = {"transport_kg": "#3b82f6", "energy_kg": "#f59e0b",
                  "food_kg": "#22c55e",      "waste_kg": "#a855f7"}
    cat_fill_colors = {
        "transport_kg": "rgba(59,130,246,0.5)",
        "energy_kg":    "rgba(245,158,11,0.5)",
        "food_kg":      "rgba(34,197,94,0.5)",
        "waste_kg":     "rgba(168,85,247,0.5)",
    }
    cat_labels = {"transport_kg": "Transport", "energy_kg": "Energy",
                  "food_kg": "Food",         "waste_kg": "Waste"}

    available_cats = [c for c in cats if c in df.columns]
    if available_cats:
        st.markdown('<div class="section-header" style="margin-top:24px">Category Breakdown Over Time</div>',
                    unsafe_allow_html=True)
        area_fig = go.Figure()
        for cat in available_cats:
            area_fig.add_trace(go.Scatter(
                x=df["date"], y=df[cat].fillna(0),
                mode="lines", name=cat_labels[cat],
                stackgroup="one",
                line=dict(color=cat_colors[cat], width=0.5),
                fillcolor=cat_fill_colors[cat],
                hovertemplate=f"<b>{cat_labels[cat]}</b>: %{{y:.2f}} kg<extra></extra>",
            ))
        area_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            font=dict(family="Inter", color="#e2e8f0"),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h"),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(area_fig, use_container_width=True, key="area_trend")

    # ── History Table ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:24px">Daily Log</div>', unsafe_allow_html=True)

    display_cols = {
        "date": "Date",
        "total_kg": "Total (kg)",
        "transport_kg": "Transport",
        "energy_kg": "Energy",
        "food_kg": "Food",
        "waste_kg": "Waste",
    }
    visible = [c for c in display_cols if c in df_disp.columns]
    df_show = df_disp[visible].rename(columns={k: v for k, v in display_cols.items() if k in visible})

    st.dataframe(
        df_show.style.format({
            col: "{:.3f}" for col in df_show.columns if "Date" not in col
        }).background_gradient(
            cmap="RdYlGn_r",
            subset=[c for c in df_show.columns if "Total" in c or "Transport" in c],
        ),
        use_container_width=True,
        height=300,
    )

    # ── Export CSV ────────────────────────────────────────────────────────
    csv_bytes = history_to_csv()
    if csv_bytes:
        st.download_button(
            "Download History as CSV",
            csv_bytes,
            file_name=f"carbonsnap_history_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── Reduction Progress ────────────────────────────────────────────────
    if len(df) >= 7:
        st.markdown('<div class="section-header" style="margin-top:24px">Reduction Progress</div>',
                    unsafe_allow_html=True)
        first_week = df["total_kg"].head(7).mean()
        last_week  = df["total_kg"].tail(7).mean()
        reduction  = (first_week - last_week) / first_week * 100 if first_week > 0 else 0

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if reduction > 0:
                st.success(f"You've reduced emissions by **{reduction:.1f}%** compared to your first week!")
            elif reduction < 0:
                st.warning(f"Emissions up by **{abs(reduction):.1f}%** vs first week. Let's turn this around!")
            else:
                st.info("Consistent emissions. Try one of the challenges to drive reduction!")

        with col_r2:
            target = 2.5  # Paris target
            pct_to_target = min(100, max(0, (first_week - last_week) / max(first_week - target, 0.1) * 100)) if first_week > target else 100
            st.markdown(f"""
            <div style="color:#94a3b8;font-size:0.85rem;margin-bottom:6px">Progress to Paris Target (2.5 kg/day)</div>
            <div style="background:rgba(255,255,255,0.08);border-radius:9999px;height:12px;overflow:hidden">
                <div style="width:{pct_to_target:.0f}%;height:12px;border-radius:9999px;
                            background:linear-gradient(90deg,#22c55e,#84cc16);transition:width 0.8s ease">
                </div>
            </div>
            <div style="font-size:0.75rem;color:#64748b;margin-top:4px">{pct_to_target:.0f}% of the way there</div>
            """, unsafe_allow_html=True)
