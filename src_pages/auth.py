"""
CarbonSnap – Login / Sign-Up Page
"""
import streamlit as st
from utils.auth_db import (
    register_user, login_user, init_db,
    load_history_db, load_badges_db, load_xp_db
)


def _load_user_data(user: dict):
    """After login, hydrate session state with persisted DB data."""
    uid = user["id"]
    # History
    history = load_history_db(uid)
    st.session_state["carbonsnap_history"] = history

    # Badges
    badges = load_badges_db(uid)
    st.session_state["badges"] = badges

    # XP
    st.session_state["xp"] = load_xp_db(uid)

    # Profile
    st.session_state["user_name"]  = user["full_name"]
    st.session_state["user_email"] = user["email"]
    st.session_state["user_city"]  = user.get("city", "Pune / Pimpri")
    st.session_state["user_mobile"]= user.get("mobile", "")
    st.session_state["user_id"]    = uid
    st.session_state["logged_in"]  = True
    st.session_state["username"]   = user["username"]


def render_auth_page(dark: bool = True):
    """
    Render the login/signup page.
    Sets st.session_state['logged_in'] = True on success.
    """
    # init_db is handled in app.py

    # ── Hero Banner ───────────────────────────────────────────────────────────
    bg   = "#0f172a" if dark else "#f0fdf4"
    card = "rgba(30,41,59,0.9)" if dark else "white"
    text = "#e2e8f0" if dark else "#0f172a"
    sub  = "#94a3b8" if dark else "#6b7280"
    bdr  = "rgba(34,197,94,0.25)" if dark else "rgba(34,197,94,0.3)"

    # ── Auth Layout (Title + Form Centered) ──────────────────────────────────
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        # Title very close to the form
        st.markdown(f"""
        <div style="text-align:center;margin-top:5vh;margin-bottom:16px">
            <div style="font-size:3.5rem;margin-bottom:4px">🌿</div>
            <div style="font-size:2.5rem;font-weight:900;color:#22c55e;letter-spacing:-0.04em;line-height:1.2">CarbonSnap</div>
            <div style="font-size:0.95rem;color:{sub};margin-top:2px">Personal Carbon Footprint Tracker</div>
        </div>
        """, unsafe_allow_html=True)
        # Tab selector
        auth_tab = st.radio(
            " ", ["Login", "Sign Up"],
            horizontal=True, label_visibility="collapsed",
            key="auth_mode"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── LOGIN FORM ────────────────────────────────────────────────────────
        if auth_tab == "Login":
            st.markdown(f"""
            <div style="background:{card};border:1px solid {bdr};border-radius:20px;
                        padding:32px;box-shadow:0 20px 60px rgba(0,0,0,0.3)">
                <h2 style="color:#22c55e;font-weight:900;margin-bottom:4px;font-size:1.6rem">Welcome back</h2>
                <p style="color:{sub};font-size:0.9rem;margin-bottom:24px">Log in to continue your eco journey</p>
            """, unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                login_id = st.text_input("Username or Email", placeholder="eco.hero@gmail.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    if not login_id or not password:
                        st.error("Please fill in all fields.")
                    else:
                        success, msg, user = login_user(login_id, password)
                        if success:
                            st.query_params["login_token"] = str(user["id"])
                            _load_user_data(user)
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown("</div>", unsafe_allow_html=True)


        # ── SIGN UP FORM ──────────────────────────────────────────────────────
        else:
            from utils.comparison import get_all_city_averages
            cities = list(get_all_city_averages().keys())

            st.markdown(f"""
            <div style="background:{card};border:1px solid {bdr};border-radius:20px;
                        padding:32px;box-shadow:0 20px 60px rgba(0,0,0,0.3)">
                <h2 style="color:#22c55e;font-weight:900;margin-bottom:4px;font-size:1.6rem">Join CarbonSnap 🌱</h2>
                <p style="color:{sub};font-size:0.9rem;margin-bottom:24px">Create your free account and start tracking</p>
            """, unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                full_name = st.text_input("Full Name", placeholder="Enter Your Name")
                username  = st.text_input("Username", placeholder="min 3 chars")
                email     = st.text_input("Email", placeholder="Enter Your Email")
                mobile    = st.text_input("Mobile No. (Optional)", placeholder="Enter Your Mobile No.")
                city      = st.selectbox("Your City", cities, index=3)
                password  = st.text_input("Password", type="password", placeholder="Min 6 characters")
                confirm   = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                submitted = st.form_submit_button("Create Account", use_container_width=True)

                if submitted:
                    if not all([full_name, username, email, password, confirm]):
                        st.error("Please fill in all required fields.")
                    elif any(char.isdigit() for char in full_name):
                        st.error("Name should not contain numbers!")
                    elif password != confirm:
                        st.error("Passwords don't match!")
                    else:
                        success, msg = register_user(username, email, password, full_name, city, mobile)
                        if success:
                            st.success(msg)
                            # Auto-login after signup
                            ok, login_msg, user = login_user(username, password)
                            if ok:
                                st.query_params["login_token"] = str(user["id"])
                                _load_user_data(user)
                                st.rerun()
                        else:
                            st.error(msg)

            st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center;margin-top:40px;color:{sub};font-size:0.8rem;font-weight:600">
        Made by <span style="color:#22c55e;">THRIVERS</span><br>
        <span style="font-weight:400;font-size:0.72rem;opacity:0.7">Built for EcoHack 2026</span>
    </div>
    """, unsafe_allow_html=True)

    
def create_demo_account():
    """Create a demo account if it doesn't exist (called on startup)."""
    init_db()
    # Try creating demo user silently
    register_user("demo", "demo@carbonsnap.app", "demo123",
                  "Demo User", "Pune / Pimpri")
    # Seed demo with some history
    from utils.auth_db import login_user as _lu, load_history_db, save_history_db
    ok, _, demo_user = _lu("demo", "demo123")
    if ok and demo_user:
        existing = load_history_db(demo_user["id"])
        if not existing:
            _seed_demo_db(demo_user["id"])


def _seed_demo_db(user_id: int):
    """Seed 14 days of realistic demo data into the DB."""
    import random
    from datetime import date, timedelta
    from utils.auth_db import save_history_db

    today = date.today()
    base  = 4.5
    with get_connection() as conn:
        for i in range(14):
            d = today - timedelta(days=13 - i)
            total     = max(0.5, base - i * 0.08 + random.uniform(-0.5, 0.5))
            transport = max(0, total * 0.40 + random.uniform(-0.2, 0.2))
            energy    = max(0, total * 0.25 + random.uniform(-0.1, 0.1))
            food      = max(0, total * 0.28 + random.uniform(-0.15, 0.15))
            waste     = max(0, total - transport - energy - food)
            
            conn.execute("""
                INSERT INTO carbon_history
                    (user_id, date, total_kg, transport_kg, energy_kg, food_kg, waste_kg, electricity, car_petrol)
                VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT(user_id, date) DO NOTHING
            """, (
                user_id,
                d.isoformat(),
                round(total, 3),
                round(transport, 3),
                round(energy, 3),
                round(food, 3),
                round(waste, 3),
                round(random.uniform(2, 8), 2),
                round(random.uniform(5, 20), 1),
            ))
        conn.commit()
