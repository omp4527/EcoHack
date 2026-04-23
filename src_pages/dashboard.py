"""
CarbonSnap – Page 1: Dashboard
"""
import streamlit as st
from datetime import date
import time

from utils.calculations import calculate_footprint, score_rating, INDIA_AVG_DAILY_KG
from utils.charts import get_breakdown, comparison_bar
from utils.tips import generate_tips, get_quick_win
from utils.badges import award_badges, BADGE_CATALOGUE, get_level
from utils.forecast import weekly_forecast, yearly_projection_stats
from utils.comparison import compare_avg, get_all_city_averages
from utils.storage import save_history, load_history
from utils.export import export_report
from utils.styles import (
    inject_css, metric_card_html, tip_card_html,
    badge_card_html, xp_bar_html
)


def render_sidebar() -> dict:
    """Render sidebar inputs and return inputs dict."""
    # ── Transport ──────────────────────────────────────────────────────────
    st.sidebar.markdown("### Transport (km today)")
    car_petrol    = st.sidebar.number_input("Car (Petrol)", 0.0, 500.0, 0.0, 1.0)
    car_diesel    = st.sidebar.number_input("Car (Diesel)", 0.0, 500.0, 0.0, 1.0)
    two_wheeler   = st.sidebar.number_input("Two-Wheeler",  0.0, 200.0, 0.0, 1.0)
    bus           = st.sidebar.number_input("Bus",          0.0, 200.0, 0.0, 1.0)
    metro_train   = st.sidebar.number_input("Metro/Train",  0.0, 500.0, 0.0, 1.0)
    auto_rickshaw = st.sidebar.number_input("Auto Rickshaw",0.0, 100.0, 0.0, 1.0)
    flight_domestic= st.sidebar.number_input("Flight (km)", 0.0, 5000.0, 0.0, 50.0)

    st.sidebar.markdown("### Energy (today's usage)")
    electricity   = st.sidebar.number_input("Electricity (kWh)", 0.0, 50.0, 0.0, 0.5)
    lpg           = st.sidebar.number_input("LPG (kg)",          0.0, 10.0, 0.0, 0.1)
    natural_gas   = st.sidebar.number_input("Natural Gas (m³)",  0.0, 20.0, 0.0, 0.5)

    st.sidebar.markdown("### Food (kg consumed today)")
    with st.sidebar.expander("Meat & Fish", expanded=False):
        beef    = st.number_input("Beef (kg)",    0.0, 2.0, 0.0, 0.05,  key="f_beef")
        lamb    = st.number_input("Lamb (kg)",    0.0, 2.0, 0.0, 0.05,  key="f_lamb")
        pork    = st.number_input("Pork (kg)",    0.0, 2.0, 0.0, 0.05,  key="f_pork")
        chicken = st.number_input("Chicken (kg)", 0.0, 2.0, 0.0, 0.05, key="f_chk")
        fish    = st.number_input("Fish (kg)",    0.0, 2.0, 0.0, 0.05,  key="f_fish")
    with st.sidebar.expander("Dairy, Grains & Veg", expanded=False):
        eggs       = st.number_input("Eggs (kg)",       0.0, 1.0, 0.0, 0.05, key="f_eggs")
        dairy      = st.number_input("Dairy (kg)",      0.0, 2.0, 0.0,  0.05, key="f_dairy")
        rice       = st.number_input("Rice (kg)",       0.0, 1.0, 0.0,  0.05, key="f_rice")
        vegetables = st.number_input("Vegetables (kg)", 0.0, 2.0, 0.0,  0.05, key="f_veg")
        fruits     = st.number_input("Fruits (kg)",     0.0, 2.0, 0.0,  0.05, key="f_fruit")
        pulses     = st.number_input("Pulses (kg)",     0.0, 1.0, 0.0,  0.05, key="f_pulse")

    st.sidebar.markdown("### Waste (kg today)")
    mixed_waste = st.sidebar.number_input("Mixed Waste (kg)", 0.0, 10.0, 0.0, 0.1)
    recycled    = st.sidebar.number_input("Recycled (kg)",    0.0, 10.0, 0.0, 0.1)
    composted   = st.sidebar.number_input("Composted (kg)",   0.0, 5.0,  0.0, 0.1)

    # Demo mode
    st.sidebar.markdown("---")
    if st.sidebar.button("Load Demo Data", help="Populate with realistic sample data"):
        from utils.storage import seed_demo_history
        seed_demo_history()
        st.rerun()

    return {
        "car_petrol": car_petrol, "car_diesel": car_diesel,
        "two_wheeler": two_wheeler, "bus": bus, "metro_train": metro_train,
        "auto_rickshaw": auto_rickshaw, "flight_domestic": flight_domestic,
        "electricity": electricity, "lpg": lpg, "natural_gas": natural_gas,
        "beef": beef, "lamb": lamb, "pork": pork, "chicken": chicken, "fish": fish,
        "eggs": eggs, "dairy": dairy, "rice": rice,
        "vegetables": vegetables, "fruits": fruits, "pulses_legumes": pulses,
        "mixed_waste": mixed_waste, "recycled": recycled, "composted": composted,
    }


def render_dashboard(inputs: dict):
    """Main dashboard content."""
    total_kg, df = calculate_footprint(inputs)
    _, label, color = score_rating(total_kg)
    history = load_history()
    city = st.session_state.get("user_city", "Pune / Pimpri")

    # ── Hero Section ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])

    india_diff = total_kg - INDIA_AVG_DAILY_KG
    vs_india = f"{'↑' if india_diff >= 0 else '↓'} {abs(india_diff):.2f} kg vs India avg"

    with col1:
        st.markdown(metric_card_html(
            f"{total_kg:.2f} kg",
            "Daily CO₂e Footprint",
            vs_india,
            color
        ), unsafe_allow_html=True)

    with col2:
        proj = yearly_projection_stats(total_kg, history)
        st.markdown(metric_card_html(
            f"{proj['yearly_tonnes']} t",
            "Yearly Projection",
            f"Trees needed: {proj['trees_needed']}/yr",
            "#f59e0b"
        ), unsafe_allow_html=True)

    with col3:
        xp = getattr(st.session_state, "xp", 0) if hasattr(st.session_state, "xp") else st.session_state.get("xp", 0)
        level_name, level_emoji, _ = get_level(xp)
        st.markdown(metric_card_html(
            f"{level_emoji} {level_name}",
            "Your Eco Level",
            f"{xp} XP earned · {len(getattr(st.session_state, 'badges', set()))} badges",
            "#a855f7"
        ), unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────
    if not df.empty:
        pie_fig, bar_fig = get_breakdown(df)
        col_a, col_b = st.columns([1.1, 0.9])
        with col_a:
            st.plotly_chart(pie_fig, use_container_width=True, key="pie")
        with col_b:
            comp = compare_avg(total_kg, city)
            comp_fig = comparison_bar(total_kg, comp)
            st.plotly_chart(comp_fig, use_container_width=True, key="comp")

        st.plotly_chart(bar_fig, use_container_width=True, key="bar")
    else:
        st.info("Enter your activities in the sidebar to see your carbon footprint breakdown!")

    # ── Tips & Quick Wins ─────────────────────────────────────────────────
    if not df.empty:
        top_cat_row = df.groupby("Category")["kg_CO2e"].sum().idxmax()
        tips_data = generate_tips(total_kg, top_cat_row)

        st.markdown('<div class="section-header">Personalized Reduction Tips</div>', unsafe_allow_html=True)
        st.info(tips_data["headline"])

        tip_cols = st.columns(2)
        for i, tip in enumerate(tips_data["tips"]):
            with tip_cols[i % 2]:
                st.markdown(tip_card_html(tip["tip"]), unsafe_allow_html=True)

        quick_win = get_quick_win(top_cat_row)
        st.success(f"**⚡ Quick Win:** {quick_win}")

    # ── Badges Section ────────────────────────────────────────────────────
    new_badges = award_badges(history, st.session_state)

    if new_badges:
        badge_names = [f"{BADGE_CATALOGUE[b]['emoji']} {BADGE_CATALOGUE[b]['title']}" for b in new_badges]
        st.success(f"🎉 New badge{'s' if len(new_badges) > 1 else ''} unlocked: {', '.join(badge_names)}")
        st.balloons()

    earned = getattr(st.session_state, "badges", set()) or st.session_state.get("badges", set())
    if earned:
        st.markdown('<div class="section-header">Your Badges</div>', unsafe_allow_html=True)
        badge_cols = st.columns(min(len(earned), 5))
        for i, badge_key in enumerate(list(earned)[:10]):
            if badge_key in BADGE_CATALOGUE:
                b = BADGE_CATALOGUE[badge_key]
                with badge_cols[i % min(len(earned), 5)]:
                    st.markdown(badge_card_html(b["title"], b["desc"], b["xp"]),
                                unsafe_allow_html=True)

    # ── Save & Export ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Save & Share</div>', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if st.button("Save Today's Entry", use_container_width=True):
            cat_totals = df.groupby("Category")["kg_CO2e"].sum() if not df.empty else {}
            entry = {
                "date": date.today().isoformat(),
                "total_kg": total_kg,
                "transport_kg": float(cat_totals.get("Transport", 0)),
                "energy_kg":    float(cat_totals.get("Energy", 0)),
                "food_kg":      float(cat_totals.get("Food", 0)),
                "waste_kg":     float(cat_totals.get("Waste", 0)),
                "electricity":  inputs.get("electricity", 0),
                "car_petrol":   inputs.get("car_petrol", 0),
            }
            save_history(entry)

            # Persist to DB if logged in
            user_id = st.session_state.get("user_id")
            if user_id:
                from utils.auth_db import save_history_db
                save_history_db(user_id, entry)

            st.success("Saved! Keep tracking daily for streaks & badges!")
            st.rerun()

    with col_s2:
        if st.button("Download PDF Report", use_container_width=True):
            if df.empty:
                st.warning("Enter some data first!")
            else:
                badges_set = st.session_state.get("badges", set())
                pdf_bytes = export_report(
                    df, total_kg, badges_set, city,
                    st.session_state.get("user_name", "EcoSnapper")
                )
                st.download_button(
                    "Click to Download PDF",
                    pdf_bytes,
                    file_name=f"CarbonSnap_{date.today()}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

    with col_s3:
        share_text = (
            f"My carbon footprint today is {total_kg:.2f} kg CO₂e "
            f"({label}) – tracked with #CarbonSnap! "
            f"India avg is 4 kg/day. Join me in going green!"
        )
        whatsapp_url = f"https://wa.me/?text={share_text.replace(' ', '%20')}"
        st.link_button("Share on WhatsApp", whatsapp_url, use_container_width=True)

    # Comparison text
    if not df.empty:
        comp = compare_avg(total_kg, city)
        st.markdown(f"""
        <div class="share-banner">
            <div style="font-size:1.1rem;font-weight:700;color:#22c55e;margin-bottom:8px">{comp['msg_india']}</div>
            <div style="font-size:0.85rem;color:#94a3b8">{comp['msg_global']}</div>
        </div>
        """, unsafe_allow_html=True)

    return total_kg, df
