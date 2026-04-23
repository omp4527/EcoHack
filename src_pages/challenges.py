"""
CarbonSnap – Page 3: Gamified Challenges
"""
import streamlit as st
from datetime import date, timedelta
from utils.styles import challenge_card_html, metric_card_html
from utils.storage import load_history
from utils.badges import BADGE_CATALOGUE, get_level


CHALLENGE_CATALOGUE = [
    {
        "id": "no_beef_week",
        "emoji": "🥩",
        "title": "No Beef Week",
        "desc": "Avoid beef for 7 consecutive days and help save 27 kg CO₂e per kg avoided.",
        "category": "Food",
        "difficulty": "Medium",
        "duration_days": 7,
        "reward": "Plant Power Badge + 40 XP",
        "badge_id": "vegan_day",
        "impact": "Save up to ~190 kg CO₂e",
        "tips": ["Try dal, paneer, or tofu as protein sources",
                 "Rajma or chole are excellent high-protein alternatives",
                 "A veggie biryani can be just as satisfying!"],
    },
    {
        "id": "no_car_week",
        "emoji": "🚗",
        "title": "Car-Free Week",
        "desc": "Use metro, bus, or cycle for all commutes for 7 days.",
        "category": "Transport",
        "difficulty": "Hard",
        "duration_days": 7,
        "reward": "Eco Rider Badge + 70 XP",
        "badge_id": "no_car_day",
        "impact": "Save 2–5 kg CO₂e/day (14–35 kg total)",
        "tips": ["Plan your metro route the night before",
                 "Rent a cycle for short distances",
                 "Auto-rickshaw still beats car by 60%"],
    },
    {
        "id": "vegan_day",
        "emoji": "🌱",
        "title": "Vegan Monday",
        "desc": "Go completely plant-based for 1 day (no meat, eggs, or dairy).",
        "category": "Food",
        "difficulty": "Easy",
        "duration_days": 1,
        "reward": "Plant Power Badge + 40 XP",
        "badge_id": "vegan_day",
        "impact": "Save 3–5 kg CO₂e in 1 day!",
        "tips": ["Oat milk chai instead of dairy chai",
                 "Chana masala or dal makhani for lunch",
                 "Avocado toast or poha for breakfast"],
    },
    {
        "id": "energy_saver",
        "emoji": "⚡",
        "title": "Energy Minimalist",
        "desc": "Keep electricity use below 3 kWh/day for 5 days.",
        "category": "Energy",
        "difficulty": "Medium",
        "duration_days": 5,
        "reward": "Sun Powered Badge + 50 XP",
        "badge_id": "solar_day",
        "impact": "Save ~3.75 kg CO₂e",
        "tips": ["Set AC to 26°C instead of 18°C",
                 "Switch to LED bulbs this week",
                 "Unplug device chargers when not in use"],
    },
    {
        "id": "waste_warrior",
        "emoji": "♻️",
        "title": "Zero Landfill Week",
        "desc": "Sort all waste into wet/dry and compost kitchen scraps for 7 days.",
        "category": "Waste",
        "difficulty": "Easy",
        "duration_days": 7,
        "reward": "Zero Waster Badge + 40 XP",
        "badge_id": "zero_waste",
        "impact": "Divert 3–5 kg from landfill",
        "tips": ["Get a small compost bin for kitchen",
                 "Use cloth bag for shopping",
                 "Flatten cardboard for recycling"],
    },
    {
        "id": "cycle_commuter",
        "emoji": "🚲",
        "title": "Cycle Commuter",
        "desc": "Cycle at least 5 km every day for 5 days.",
        "category": "Transport",
        "difficulty": "Medium",
        "duration_days": 5,
        "reward": "Eco Rider Badge + 50 XP",
        "impact": "Save ~6 kg CO₂e + improve health!",
        "tips": ["Wake 15 min earlier to account for cycling time",
                 "Podcast or music makes the ride fly by",
                 "Keep a change of clothes at work"],
    },
    {
        "id": "digital_detox",
        "emoji": "📱",
        "title": "Digital Low-Power Day",
        "desc": "Keep screen-on time to <3 hours and unplug all devices at night for 3 days.",
        "category": "Energy",
        "difficulty": "Easy",
        "duration_days": 3,
        "reward": "Energy Saver Badge + 30 XP",
        "impact": "Save ~0.5 kWh/day",
        "tips": ["Read a physical book instead",
                 "Go for a walk in the evening",
                 "Have chai without the scroll session"],
    },
    {
        "id": "local_food",
        "emoji": "🌾",
        "title": "Local Food Week",
        "desc": "Buy only locally grown, seasonal produce from your nearest sabziwala for 7 days.",
        "category": "Food",
        "difficulty": "Easy",
        "duration_days": 7,
        "reward": "Local Hero Badge + 35 XP",
        "impact": "Cut food transport emissions by 50%",
        "tips": ["Seasonal veggies are cheaper AND greener",
                 "Find your local vegetable market map",
                 "Plan a weekly meal around seasonal produce"],
    },
]


def _get_challenge_state(challenge_id: str) -> dict:
    """Get or init challenge progress from session state."""
    key = f"challenge_{challenge_id}"
    if key not in st.session_state:
        st.session_state[key] = {
            "status": "not_started",  # not_started, active, completed
            "start_date": None,
            "last_logged_date": None,
            "days_done": 0,
        }
    return st.session_state[key]


def _update_challenge(challenge_id: str, updates: dict):
    key = f"challenge_{challenge_id}"
    st.session_state[key].update(updates)


def render_challenges():
    st.markdown('<div class="section-header">Eco Challenges</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#94a3b8;font-size:0.9rem;margin-bottom:20px">
        Take on real-world sustainability challenges. Complete them to earn XP, unlock badges, 
        and make a measurable impact. 
    </div>
    """, unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────────────────────
    active_count    = sum(1 for c in CHALLENGE_CATALOGUE
                          if _get_challenge_state(c["id"])["status"] == "active")
    completed_count = sum(1 for c in CHALLENGE_CATALOGUE
                          if _get_challenge_state(c["id"])["status"] == "completed")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card_html(str(active_count), "Active Challenges", "Currently in progress", "#f59e0b"),
                    unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card_html(str(completed_count), "Completed", "Great work!", "#22c55e"),
                    unsafe_allow_html=True)
    with col3:
        total_xp_challenges = sum(
            int(c["reward"].split("+")[-1].replace("XP","").strip())
            for c in CHALLENGE_CATALOGUE
            if _get_challenge_state(c["id"])["status"] == "completed"
        )
        st.markdown(metric_card_html(f"{total_xp_challenges} XP", "Earned from Challenges", "Keep going!", "#a855f7"),
                    unsafe_allow_html=True)

    st.markdown("---")

    # ── Filter ────────────────────────────────────────────────────────────
    filter_col, sort_col = st.columns([2, 1])
    with filter_col:
        cat_filter = st.multiselect(
            "Filter by Category",
            ["All", "Food", "Transport", "Energy", "Waste"],
            default=["All"],
        )
    with sort_col:
        diff_filter = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])

    # Apply filters
    visible = CHALLENGE_CATALOGUE.copy()
    if "All" not in cat_filter and cat_filter:
        visible = [c for c in visible if c["category"] in cat_filter]
    if diff_filter != "All":
        visible = [c for c in visible if c["difficulty"] == diff_filter]

    # ── Challenge Cards ───────────────────────────────────────────────────
    for i in range(0, len(visible), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(visible):
                break
            challenge = visible[i + j]
            cid = challenge["id"]
            state = _get_challenge_state(cid)
            status = state["status"]
            days_done = state.get("days_done", 0)
            duration = challenge["duration_days"]
            progress_pct = int(days_done / duration * 100) if status != "not_started" else 0

            with col:
                st.markdown(challenge_card_html(
                    challenge["title"], challenge["desc"],
                    challenge["reward"], challenge["difficulty"],
                    progress_pct, status == "completed"
                ), unsafe_allow_html=True)

                # Action buttons
                if status == "not_started":
                    if st.button(f"Start Challenge", key=f"start_{cid}", use_container_width=True):
                        _update_challenge(cid, {"status": "active",
                                                "start_date": date.today().isoformat(),
                                                "days_done": 0})
                        st.success(f"Challenge started! {challenge['emoji']} {challenge['title']}")
                        st.rerun()

                elif status == "active":
                    btn_col1, btn_col2 = st.columns(2)
                    last_date = state.get("last_logged_date")
                    can_log = last_date != date.today().isoformat()
                    
                    with btn_col1:
                        if st.button(f"Log Day {days_done+1}", key=f"log_{cid}", 
                                     use_container_width=True, disabled=not can_log,
                                     help="You can only log one day per calendar day" if not can_log else ""):
                            new_days = days_done + 1
                            today_str = date.today().isoformat()
                            if new_days >= duration:
                                _update_challenge(cid, {"status": "completed", "days_done": new_days, "last_logged_date": today_str})
                                xp_gain = int(challenge["reward"].split("+")[-1].replace("XP","").strip())
                                if "xp" not in st.session_state:
                                    st.session_state.xp = 0
                                st.session_state.xp = st.session_state.get("xp", 0) + xp_gain
                                
                                # Award badge
                                badge_id = challenge.get("badge_id")
                                if badge_id:
                                    if "badges" not in st.session_state:
                                        st.session_state.badges = set()
                                    st.session_state.badges.add(badge_id)
                                    # Persist badge
                                    uid = st.session_state.get("user_id")
                                    if uid:
                                        from utils.auth_db import save_badge_db
                                        save_badge_db(uid, badge_id)

                                st.balloons()
                                st.success(f"🏆 Challenge COMPLETED! +{xp_gain} XP earned!")
                            else:
                                _update_challenge(cid, {"days_done": new_days, "last_logged_date": today_str})
                                st.success(f"Day {new_days}/{duration} done! See you tomorrow!")
                            st.rerun()
                        
                        if not can_log:
                            st.info("Next day available tomorrow!")
                    with btn_col2:
                        if st.button("Abandon", key=f"abandon_{cid}", use_container_width=True):
                            _update_challenge(cid, {"status": "not_started", "days_done": 0})
                            st.warning("Challenge abandoned. You can restart anytime!")
                            st.rerun()

                    # Tips expander
                    with st.expander("Tips for this challenge"):
                        for tip in challenge.get("tips", []):
                            st.markdown(f"• {tip}")

                elif status == "completed":
                    st.success("COMPLETED! Amazing work!")
                    if st.button("Redo Challenge", key=f"redo_{cid}", use_container_width=True):
                        _update_challenge(cid, {"status": "not_started", "days_done": 0})
                        st.rerun()

    # ── Impact Summary ────────────────────────────────────────────────────
    if completed_count > 0:
        st.markdown("---")
        st.markdown('<div class="section-header">Your Challenge Impact</div>', unsafe_allow_html=True)
        st.success(f"""
        You've completed **{completed_count} challenge(s)** and earned **{total_xp_challenges} XP**!
        
        Your eco-actions have the potential to inspire others.  
        **Share your achievements** on WhatsApp to multiply your impact! 
        """)
        share_msg = f"I've completed {completed_count} eco challenges on CarbonSnap and earned {total_xp_challenges} XP! Join me in reducing carbon footprints! #CarbonSnap #EcoHack"
        st.link_button("Share Achievements", f"https://wa.me/?text={share_msg.replace(' ','%20')}")
