"""
🌿 CarbonSnap – Personal Carbon Footprint Tracker & Reducer
EcoHack 2025 | India-specific | Gamified | Auth-enabled

Run: streamlit run app.py
"""
import streamlit as st
import sys, os

# ── Path fix ─────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# Defer heavy imports
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarbonSnap – Personal Carbon Tracker",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "## 🌿 CarbonSnap\nPersonal Carbon Footprint Tracker · EcoHack 2025",
    },
)

# ── Session State Init ────────────────────────────────────────────────────────
_defaults = {
    "dark_mode":            True,
    "logged_in":            False,
    "user_id":              None,
    "user_name":            "",
    "user_email":           "",
    "username":             "",
    "user_city":            "Pune / Pimpri",
    "badges":               set(),
    "xp":                   0,
    "active_page":          "Dashboard",    # custom nav state
    "carbonsnap_history":   [],
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Restore persistent session ────────────────────────────────────────────────
if not st.session_state["logged_in"] and "login_token" in st.query_params:
    token = st.query_params["login_token"]
    try:
        from utils.auth_db import get_user_by_id
        user_row = get_user_by_id(int(token))
        if user_row:
            from src_pages.auth import _load_user_data
            _load_user_data(user_row)
    except Exception:
        pass

# ── DB Init (Deferred to first run) ───────────────────────────────────────────
if "db_initialized" not in st.session_state:
    from utils.auth_db import init_db
    init_db()
    st.session_state["db_initialized"] = True
    
    # Silently ensure a demo account exists
    try:
        from src_pages.auth import create_demo_account
        create_demo_account()
    except Exception:
        pass

# ── CSS ───────────────────────────────────────────────────────────────────────
from utils.styles import inject_css
dark = st.session_state["dark_mode"]
inject_css(dark)

# ═════════════════════════════════════════════════════════════════════════════
# AUTH GATE – show login/signup if not logged in
# ═════════════════════════════════════════════════════════════════════════════
if not st.session_state["logged_in"]:
    from src_pages.auth import render_auth_page
    render_auth_page(dark)
    st.stop()          # Don't render anything else

# ═════════════════════════════════════════════════════════════════════════════
# MAIN APP – only reached when logged in
# ═════════════════════════════════════════════════════════════════════════════

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center;padding:10px 0 16px">
            <div style="font-size:2.2rem">🌿</div>
            <div style="font-size:1.3rem;font-weight:900;color:#22c55e;letter-spacing:-0.03em">CarbonSnap</div>
            <div style="font-size:0.72rem;color:#64748b;margin-top:2px">Personal Carbon Tracker</div>
        </div>
    """, unsafe_allow_html=True)


# ── Sidebar Inputs (Dashboard) ────────────────────────────────────────────────
if st.session_state["active_page"] == "Dashboard":
    from src_pages.dashboard import render_sidebar
    inputs = render_sidebar()
else:
    inputs = {}

# ── Custom Top Nav Bar (styled buttons) ───────────────────────────────────────
active_page = st.session_state.get("active_page", "Dashboard")
user_name   = st.session_state.get("user_name", "User")
avatar_letter = (user_name[0] if user_name else "U").upper()

nav_pages = [("🏠 Dashboard", "Dashboard"), ("📅 Tracker", "Tracker"),
             ("⚔️ Challenges", "Challenges")]

# We use 5 columns: 3 for the nav buttons, 1 spacer, 1 for the user popover menu
cols = st.columns([1.5, 1.5, 1.5, 2, 2.5])
for i, (label, page) in enumerate(nav_pages):
    with cols[i]:
        is_active = (active_page == page)
        if st.button(label, key=f"nav_{page}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state["active_page"] = page
            st.rerun()

with cols[-1]:
    # Streamlit Popover for user dropdown
    with st.popover(f"👤 {user_name}", use_container_width=True):
        st.markdown(f"**Hello, {user_name}!**")
        if st.button("📝 Profile & Settings", use_container_width=True):
            st.session_state["active_page"] = "Profile"
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            if "login_token" in st.query_params:
                del st.query_params["login_token"]
            for k in ["logged_in", "user_id", "user_name", "user_email", "username",
                      "badges", "xp", "carbonsnap_history", "active_page"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

st.markdown("<hr style='border:none;border-top:1px solid rgba(34,197,94,0.12);margin:8px 0 20px'>",
            unsafe_allow_html=True)

# Redundant sync removed - handled in auth.py during login

# ── Page Routing ──────────────────────────────────────────────────────────────
page = st.session_state.get("active_page", "Dashboard")

if page == "Dashboard":
    from src_pages.dashboard import render_dashboard
    render_dashboard(inputs)

elif page == "Tracker":
    from src_pages.tracker import render_tracker
    render_tracker()

elif page == "Challenges":
    from src_pages.challenges import render_challenges
    render_challenges()

elif page == "Profile":
    from src_pages.profile import render_profile
    render_profile()

# ── Global Footer ─────────────────────────────────────────────────────────────
st.markdown("<br><hr style='border:none;border-top:1px solid rgba(148,163,184,0.1);margin:20px 0 10px'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#64748b; font-size:0.8rem; padding-bottom:20px; font-weight:600;'>"
    "Made by <span style='color:#22c55e;'>THRIVERS</span>"
    "</div>", 
    unsafe_allow_html=True
)
