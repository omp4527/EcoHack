"""
CarbonSnap – Page 4: Profile, Badges & Yearly Stats
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date

from utils.badges import BADGE_CATALOGUE, get_level, _calculate_streak
from utils.storage import load_history, get_history_df
from utils.forecast import yearly_projection_stats
from utils.comparison import CITY_AVERAGES, GLOBAL_BENCHMARKS
from utils.styles import metric_card_html, badge_card_html, xp_bar_html

@st.dialog("Edit Profile")
def edit_profile_dialog():
    st.write("Update your profile details below:")
    new_name = st.text_input("Full Name", value=st.session_state.get("user_name", ""))
    
    from utils.comparison import get_all_city_averages
    cities = list(get_all_city_averages().keys())
    current_city = st.session_state.get("user_city", "Pune / Pimpri")
    city_idx = cities.index(current_city) if current_city in cities else 3
    new_city = st.selectbox("Your City", cities, index=city_idx)
    
    if st.button("Save Changes", type="primary", use_container_width=True):
        if any(char.isdigit() for char in new_name):
            st.error("Name should not contain numbers!")
        elif not new_name.strip():
            st.error("Name cannot be empty.")
        else:
            user_id = st.session_state.get("user_id")
            if user_id:
                from utils.auth_db import update_user_profile
                update_user_profile(user_id, new_city, new_name.strip())
            st.session_state["user_name"] = new_name.strip()
            st.session_state["user_city"] = new_city
            st.rerun()

def render_profile():
    # ── User Header ───────────────────────────────────────────────────────
    user_name = st.session_state.get("user_name", "EcoSnapper")
    user_email = st.session_state.get("user_email", "N/A")
    user_mobile = st.session_state.get("user_mobile", "")
    city = st.session_state.get("user_city", "Pune / Pimpri")
    xp = st.session_state.get("xp", 0)
    badges = st.session_state.get("badges", set())
    history = load_history()
    streak = _calculate_streak(history)
    level_name, level_emoji, next_level_xp = get_level(xp)

    col1, col2 = st.columns([3, 1])
    with col1:
        mobile_html = f'<div style="font-size:0.9rem;color:#94a3b8;margin-top:2px">📱 {user_mobile}</div>' if user_mobile else ''
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(34,197,94,0.12),rgba(132,204,22,0.06));
                    border:1px solid rgba(34,197,94,0.25);border-radius:20px;padding:28px 32px;
                    display:flex;align-items:center;gap:24px">
            <div style="font-size:4rem">{level_emoji}</div>
            <div>
                <div style="font-size:1.8rem;font-weight:900;color:#22c55e;letter-spacing:-0.03em">{user_name}</div>
                <div style="font-size:0.9rem;color:#94a3b8;margin-top:4px">{user_email}</div>{mobile_html}
                <div style="font-size:0.9rem;color:#94a3b8;margin-top:2px">{city} · Level: {level_name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Edit Profile", use_container_width=True):
            edit_profile_dialog()
            
    st.markdown("<br>", unsafe_allow_html=True)

    # XP progress bar
    st.markdown(xp_bar_html(xp, next_level_xp), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────────────────
    today_total = history[-1]["total_kg"] if history else 0.0
    proj = yearly_projection_stats(today_total, history)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card_html(f"{streak}", "Day Streak", "Track daily to grow!","#f59e0b"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card_html(f"{len(history)}", "Days Logged", "Building your story","#3b82f6"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card_html(f"{proj['yearly_tonnes']} t", "Yearly Projection","CO₂e based on recent avg","#f97316"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card_html(f"{proj['trees_needed']}", "Trees to Offset","Per year to go carbon neutral","#22c55e"), unsafe_allow_html=True)

    # ── Badge Wall ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:28px">Badge Wall</div>', unsafe_allow_html=True)

    all_badge_keys = list(BADGE_CATALOGUE.keys())
    earned_badges = badges or set()
    cols_per_row = 5
    rows = [all_badge_keys[i:i+cols_per_row] for i in range(0, len(all_badge_keys), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for j, bkey in enumerate(row):
            b = BADGE_CATALOGUE[bkey]
            locked = bkey not in earned_badges
            with cols[j]:
                st.markdown(badge_card_html(b["title"], b["desc"], b["xp"], locked=locked),
                            unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style="font-size:0.75rem;color:#64748b;margin-top:12px">
        Locked badges appear dimmed. Complete challenges and track daily to unlock all badges!
    </div>
    """, unsafe_allow_html=True)

    # ── Yearly Projection Chart ───────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:28px">Yearly Emission Projection</div>',
                unsafe_allow_html=True)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    current_month = date.today().month - 1

    # Simulated monthly data
    if history and len(history) >= 7:
        recent_avg = sum(h["total_kg"] for h in history[-7:]) / 7
    else:
        recent_avg = today_total if today_total > 0 else 4.0

    # Generate projected yearly data with realistic seasonal variation
    import math
    projected_monthly = []
    for m in range(12):
        seasonal_factor = 1 + 0.08 * math.sin((m - 5) * math.pi / 6)
        projected_monthly.append(round(recent_avg * 30 * seasonal_factor, 1))

    india_monthly = [4.0 * 30] * 12

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months, y=projected_monthly,
        name="Your Projection",
        marker=dict(
            color=["#22c55e" if i <= current_month else "rgba(34,197,94,0.25)" for i in range(12)],
        ),
        hovertemplate="%{x}: <b>%{y:.1f} kg</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=months, y=india_monthly,
        mode="lines+markers", name="India Avg",
        line=dict(color="#ef4444", dash="dash", width=2),
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        font=dict(family="Inter", color="#e2e8f0"),
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis_title="kg CO₂e / month",
        legend=dict(orientation="h"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)"),
    )
    st.plotly_chart(fig, use_container_width=True, key="yearly_proj")

    # ── Global Comparison Gauge ───────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:28px">Global Context</div>',
                unsafe_allow_html=True)

    today_val = today_total if today_total > 0 else recent_avg
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=today_val,
        title={"text": "Your Daily Footprint (kg CO₂e)", "font": {"color": "#e2e8f0", "size": 14}},
        delta={"reference": 4.0, "suffix": " vs India avg"},
        gauge={
            "axis": {"range": [0, 16], "tickcolor": "#94a3b8"},
            "bar": {"color": "#22c55e"},
            "steps": [
                {"range": [0, 2.5],  "color": "rgba(34,197,94,0.15)"},
                {"range": [2.5, 4.0], "color": "rgba(245,158,11,0.1)"},
                {"range": [4.0, 8.0], "color": "rgba(239,68,68,0.1)"},
                {"range": [8.0, 16],  "color": "rgba(127,29,29,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#22c55e", "width": 3},
                "value": 2.5,
            },
        },
        number={"suffix": " kg", "font": {"color": "#22c55e", "size": 36}},
    ))
    fig_gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        font=dict(family="Inter", color="#e2e8f0"),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    col_g1, col_g2 = st.columns([1.2, 0.8])
    with col_g1:
        st.plotly_chart(fig_gauge, use_container_width=True, key="gauge")
    with col_g2:
        st.markdown("""
        <div style="padding-top:20px">
        """, unsafe_allow_html=True)
        benchmarks = {
            "Paris 1.5°C": ("2.5 kg/day", "#22c55e"),
            "India Sustainable": ("3.0 kg/day", "#84cc16"),
            "India Average": ("4.0 kg/day", "#f59e0b"),
            "Global Average": ("11.5 kg/day", "#f97316"),
            "US Average": ("16.0 kg/day", "#ef4444"),
        }
        for name, (val, color) in benchmarks.items():
            is_you = (name == "Paris 1.5°C" and today_val <= 2.5) or \
                     (name == "India Sustainable" and today_val <= 3.0) or \
                     (name == "India Average" and today_val <= 4.0)
            indicator = " ← You're here! ✓" if is_you else ""
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:8px 12px;border-radius:8px;margin-bottom:6px;
                        background:rgba(255,255,255,0.03);border-left:3px solid {color}">
                <span style="font-size:0.85rem;color:#e2e8f0">{name}</span>
                <span style="font-size:0.85rem;font-weight:700;color:{color}">{val}{indicator}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Share Profile ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:28px">Share Your Progress</div>',
                unsafe_allow_html=True)

    badge_emoji_str = " ".join([BADGE_CATALOGUE[b]["emoji"] for b in earned_badges if b in BADGE_CATALOGUE][:5])
    share_text = (
        f"CarbonSnap Profile: {user_name} | {level_emoji} {level_name} | "
        f"{today_val:.1f} kg CO₂e today | {streak}-day streak | {len(earned_badges)} badges {badge_emoji_str} | "
        f"Join me! #CarbonSnap #EcoHack #ClimateAction"
    )

    st.markdown(f"""
    <div class="share-banner">
        <div style="font-size:1.5rem;margin-bottom:12px">🌟</div>
        <div style="font-size:0.95rem;color:#e2e8f0;line-height:1.6;margin-bottom:16px">
            <em>"{share_text}"</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_share1, col_share2 = st.columns(2)
    with col_share1:
        st.link_button("WhatsApp",
                       f"https://wa.me/?text={share_text.replace(' ','%20')}",
                       use_container_width=True)
    with col_share2:
        twitter_text = share_text[:240]
        st.link_button("Twitter / X",
                       f"https://twitter.com/intent/tweet?text={twitter_text.replace(' ','%20')}",
                       use_container_width=True)

    # ── Tips for gaining more XP ──────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:28px">Unlock More Badges</div>',
                unsafe_allow_html=True)
    locked_badges = [k for k in BADGE_CATALOGUE if k not in earned_badges]
    if locked_badges:
        cols = st.columns(min(3, len(locked_badges)))
        for i, bkey in enumerate(locked_badges[:3]):
            b = BADGE_CATALOGUE[bkey]
            with cols[i]:
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.5);border:1px solid rgba(100,116,139,0.2);
                            border-radius:12px;padding:14px;text-align:center;">
                    <div style="font-size:2rem;opacity:0.4"></div>
                    <div style="font-size:0.85rem;font-weight:700;color:#64748b">{b['title']}</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:4px">{b['desc']}</div>
                    <div style="font-size:0.7rem;color:#f59e0b;margin-top:6px">+{b['xp']} XP</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.balloons()
        st.success("WOW! You've unlocked ALL badges! You are a true Carbon Hero!")
