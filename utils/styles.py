"""
CarbonSnap – Custom CSS & Theme Injection
"""

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Reset ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── App Background ───────────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    min-height: 100vh;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid rgba(34,197,94,0.2);
}
[data-testid="stSidebar"] .stMarkdown h2 {
    color: #22c55e;
    font-weight: 800;
    letter-spacing: -0.02em;
}

/* ── Metric Cards ─────────────────────────────────────────────────────── */
.metric-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,0.9) 100%);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    backdrop-filter: blur(12px);
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 25px rgba(34,197,94,0.3);
    border-color: rgba(34,197,94,0.6);
}
.metric-value {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    font-weight: 600;
}
.metric-sub {
    font-size: 0.9rem;
    color: #94a3b8;
    margin-top: 8px;
}

/* ── Tip Cards ────────────────────────────────────────────────────────── */
.tip-card {
    background: linear-gradient(135deg, rgba(34,197,94,0.08) 0%, rgba(132,204,22,0.05) 100%);
    border: 1px solid rgba(34,197,94,0.2);
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: border-color 0.2s ease;
}
.tip-card:hover { 
    border-left-color: #84cc16; 
    box-shadow: 0 0 15px rgba(34,197,94,0.2);
    transform: translateX(2px);
}
.tip-emoji { font-size: 1.5rem; margin-right: 10px; }
.tip-text { color: #e2e8f0; font-size: 0.92rem; line-height: 1.5; }

/* ── Badge Cards ──────────────────────────────────────────────────────── */
.badge-card {
    background: linear-gradient(135deg, rgba(168,85,247,0.12) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(168,85,247,0.3);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    transition: transform 0.2s ease;
}
.badge-card:hover { 
    transform: scale(1.06) translateY(-5px); 
    box-shadow: 0 12px 30px rgba(168,85,247,0.3), 0 0 20px rgba(168,85,247,0.2);
    border-color: rgba(168,85,247,0.6);
}
.badge-emoji { font-size: 2.4rem; display: block; margin-bottom: 6px; }
.badge-title { font-size: 0.82rem; font-weight: 700; color: #c4b5fd; }
.badge-desc  { font-size: 0.72rem; color: #94a3b8; margin-top: 2px; }
.badge-xp    { font-size: 0.7rem; color: #f59e0b; font-weight: 600; margin-top: 4px; }

/* Locked badge */
.badge-card-locked {
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(100,116,139,0.2);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    opacity: 0.45;
}

/* ── Challenge Cards ──────────────────────────────────────────────────── */
.challenge-card {
    background: linear-gradient(135deg, rgba(245,158,11,0.1) 0%, rgba(234,88,12,0.06) 100%);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    transition: transform 0.2s;
}
.challenge-card:hover { 
    transform: translateY(-6px); 
    box-shadow: 0 15px 35px rgba(245,158,11,0.2), 0 0 25px rgba(245,158,11,0.15);
    border-color: rgba(245,158,11,0.5);
}
.challenge-title { font-size:1rem; font-weight:700; color:#f1f5f9; margin:6px 0 4px; }
.challenge-desc { font-size:0.85rem; color:#94a3b8; margin-bottom:10px; }
.challenge-reward { font-size:0.8rem; color:#f59e0b; margin-bottom:8px; }
.challenge-prog { font-size:0.72rem; color:#64748b; margin-top:4px; }
.challenge-difficulty {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 9999px;
    display: inline-block;
    margin-bottom: 6px;
}
.diff-easy   { background: rgba(34,197,94,0.2); color: #22c55e; }
.diff-medium { background: rgba(245,158,11,0.2); color: #f59e0b; }
.diff-hard   { background: rgba(239,68,68,0.2);  color: #ef4444; }

/* ── Progress Bar ─────────────────────────────────────────────────────── */
.xp-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 9999px;
    height: 10px;
    overflow: hidden;
    margin: 8px 0;
}
.xp-bar-fill {
    height: 10px;
    border-radius: 9999px;
    background: linear-gradient(90deg, #22c55e, #84cc16);
    transition: width 0.6s ease;
}

/* ── Section Headers ──────────────────────────────────────────────────── */
.section-header {
    font-size: 1.2rem;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* ── Hide default Streamlit tabs (we use custom nav) ─────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] { display: none !important; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 0 !important; }

/* ── Top Navigation Bar ───────────────────────────────────────────────── */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 4px 18px 4px;
    border-bottom: 1px solid rgba(34,197,94,0.15);
    margin-bottom: 24px;
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 9px 20px;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    border: 1.5px solid transparent;
    transition: all 0.2s ease;
    text-decoration: none;
    white-space: nowrap;
    background: rgba(30,41,59,0.6);
    color: #94a3b8;
    border-color: rgba(100,116,139,0.2);
}
.nav-btn:hover {
    background: rgba(34,197,94,0.18);
    border-color: rgba(34,197,94,0.6);
    color: #22c55e;
    transform: translateY(-2px);
    box-shadow: 0 0 15px rgba(34,197,94,0.3);
}
.nav-btn.active {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    border-color: transparent;
    color: white;
    box-shadow: 0 4px 15px rgba(34,197,94,0.35);
}
.nav-user {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(30,41,59,0.6);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 50px;
    padding: 6px 16px 6px 8px;
    transition: all 0.2s ease;
}
.nav-user:hover {
    border-color: rgba(34,197,94,0.5);
    background: rgba(30,41,59,0.8);
    box-shadow: 0 0 20px rgba(34,197,94,0.2);
}
.nav-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 900;
    color: white;
    flex-shrink: 0;
}
.nav-username {
    font-size: 0.85rem;
    font-weight: 700;
    color: #e2e8f0;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ── Streamlit Buttons (dark) ─────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(34,197,94,0.3) !important;
    white-space: nowrap !important;
    min-height: 44px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(34,197,94,0.4) !important;
}
/* Secondary button style (neutral) */
.stButton > button[kind="secondary"] {
    background: rgba(30,41,59,0.8) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(100,116,139,0.3) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(51,65,85,0.8) !important;
    color: #e2e8f0 !important;
}

/* ── Sliders ──────────────────────────────────────────────────────────── */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #22c55e, #84cc16) !important;
}

/* ── Input Fields ─────────────────────────────────────────────────────── */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid rgba(100,116,139,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.15) !important;
}

/* ── DataFrames ───────────────────────────────────────────────────────── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ── Expander ─────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(30,41,59,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}

/* ── Share Banner ─────────────────────────────────────────────────────── */
.share-banner {
    background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(132,204,22,0.08));
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    margin-top: 16px;
}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(100,116,139,0.4); border-radius: 9999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(34,197,94,0.5); }

/* ── Animations ───────────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
    50%       { box-shadow: 0 0 0 12px rgba(34,197,94,0); }
}
.animate-fade-up { animation: fadeInUp 0.5s ease forwards; }
.pulse-green { animation: pulse-green 2s infinite; }

/* ── Mobile Responsiveness ────────────────────────────────────────────── */
@media (max-width: 768px) {
    .metric-value { font-size: 2rem; }
    .metric-card  { padding: 14px 16px; }
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #f0fdf4 0%, #dcfce7 100%); border-right: 1px solid rgba(34,197,94,0.3); }
.metric-card { background: white; border: 1px solid rgba(34,197,94,0.3); border-radius: 16px; padding: 20px 24px; margin-bottom: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); transition: transform 0.2s; }
.metric-card:hover { transform: translateY(-2px); }
.metric-value { font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; }
.metric-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; font-weight: 600; }
.metric-sub { font-size: 0.9rem; color: #6b7280; margin-top: 8px; }
.tip-card { background: #f0fdf4; border: 1px solid rgba(34,197,94,0.3); border-left: 4px solid #22c55e; border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; }
.tip-text { color: #1e293b; font-size: 0.92rem; }
.badge-card { background: #faf5ff; border: 1px solid rgba(168,85,247,0.3); border-radius: 14px; padding: 16px; text-align: center; }
.badge-title { font-size: 0.82rem; font-weight: 700; color: #7c3aed; }
.badge-desc { font-size: 0.72rem; color: #6b7280; }
.badge-xp { font-size: 0.7rem; color: #d97706; font-weight: 600; }
.challenge-card { background: #fffbeb; border: 1px solid rgba(245,158,11,0.3); border-radius: 16px; padding: 20px; margin-bottom: 14px; }
.section-header { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #e2e8f0; }
/* LIGHT MODE: buttons must have dark/black text for readability */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #0f172a !important;          /* dark text in light mode */
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(34,197,94,0.25) !important;
    white-space: nowrap !important;
    min-height: 44px !important;
    padding: 10px 16px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    color: white !important;            /* white on hover when darker bg */
    box-shadow: 0 8px 20px rgba(34,197,94,0.4) !important;
}
/* Secondary buttons in light mode */
.stButton > button[kind="secondary"] {
    background: #f8fafc !important;
    color: #475569 !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
}
/* Link buttons */
[data-testid="stLinkButton"] > a {
    color: #0f172a !important;
    font-weight: 700 !important;
}
.share-banner { background: #f0fdf4; border: 1px solid rgba(34,197,94,0.3); border-radius: 16px; padding: 20px 24px; text-align: center; }
.badge-card-locked { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px; text-align: center; opacity: 0.45; }
.xp-bar-bg { background: #e2e8f0; border-radius: 9999px; height: 10px; overflow: hidden; }
.xp-bar-fill { height: 10px; border-radius: 9999px; background: linear-gradient(90deg, #22c55e, #84cc16); }
.diff-easy   { background: rgba(34,197,94,0.15); color: #16a34a; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; }
.diff-medium { background: rgba(245,158,11,0.15); color: #d97706; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; }
.diff-hard   { background: rgba(239,68,68,0.15);  color: #dc2626; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; }
/* Hardcode dark text on Streamlit native elements */
.stMarkdown, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p, .stMarkdown span { color: #0f172a !important; }
.stWidgetLabel p, .stWidgetLabel div, label { color: #0f172a !important; }
[data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] .stMarkdown h3 { color: #0f172a !important; }
[data-testid="stSidebar"] p { color: #0f172a !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #0f172a !important; }
[data-testid="stExpander"] details summary svg { fill: #0f172a !important; stroke: #0f172a !important; color: #0f172a !important; }
[data-testid="stExpander"] details summary span { color: #0f172a !important; }
[data-testid="stToggle"] p, [data-testid="stToggle"] span { color: #0f172a !important; }

/* Challenge cards text overrides for light mode */
.challenge-card { background: #fffbeb; border: 1px solid rgba(245,158,11,0.3); border-radius: 16px; padding: 20px; margin-bottom: 14px; }
.challenge-title { font-size:1rem; font-weight:700; color:#0f172a !important; margin:6px 0 4px; }
.challenge-desc { font-size:0.85rem; color:#475569 !important; margin-bottom:10px; }
.challenge-reward { font-size:0.8rem; color:#d97706 !important; margin-bottom:8px; }
.challenge-prog { font-size:0.72rem; color:#64748b !important; margin-top:4px; }

/* Light-mode nav buttons */
.nav-btn { background: white; color: #475569; border-color: #e2e8f0; }
.nav-btn:hover { background: #f0fdf4; border-color: rgba(34,197,94,0.4); color: #16a34a; }
.nav-btn.active { background: linear-gradient(135deg,#22c55e,#16a34a); color: white; border-color: transparent; }
.nav-user { background: white; border-color: rgba(34,197,94,0.3); }
.nav-username { color: #0f172a; }
</style>
"""


def inject_css(dark_mode: bool = True):
    import streamlit as st
    st.markdown(DARK_CSS if dark_mode else LIGHT_CSS, unsafe_allow_html=True)


def top_nav_html(active_page: str, user_name: str, dark: bool = True) -> str:
    """Render the custom top navigation bar HTML."""
    pages = ["Dashboard", "Tracker", "Challenges", "Profile"]
    nav_btns = ""
    for name in pages:
        is_active = active_page == name
        cls = "nav-btn active" if is_active else "nav-btn"
        nav_btns += f'<span class="{cls}" id="nav-{name.lower()}">{name}</span>\n'

    # User avatar: first letter of name
    avatar_letter = (user_name[0] if user_name else "U").upper()
    display_name  = user_name if len(user_name) <= 16 else user_name[:14] + "…"

    return f"""
    <div class="top-nav">
        <div class="nav-left">
            {nav_btns}
        </div>
        <div class="nav-user">
            <div class="nav-avatar">{avatar_letter}</div>
            <span class="nav-username">{display_name}</span>
        </div>
    </div>
    """


def metric_card_html(value: str, label: str, sub: str = "", color: str = "#22c55e") -> str:
    return f"""
    <div class="metric-card animate-fade-up">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        {f'<div class="metric-sub">{sub}</div>' if sub else ''}
    </div>
    """


def tip_card_html(tip: str) -> str:
    return f"""
    <div class="tip-card animate-fade-up">
        <span class="tip-text">{tip}</span>
    </div>
    """


def badge_card_html(title: str, desc: str, xp: int, locked: bool = False) -> str:
    cls = "badge-card-locked" if locked else "badge-card"
    return f"""
    <div class="{cls}">
        <div class="badge-title">{title}</div>
        <div class="badge-desc">{desc}</div>
        <div class="badge-xp">+{xp} XP</div>
    </div>
    """


def xp_bar_html(current_xp: int, next_level_xp: int) -> str:
    pct = min(100, int(current_xp / next_level_xp * 100))
    return f"""
    <div class="xp-bar-bg">
        <div class="xp-bar-fill" style="width:{pct}%"></div>
    </div>
    <small style="color:#94a3b8">{current_xp} / {next_level_xp} XP to next level</small>
    """


def challenge_card_html(title, desc, reward, difficulty, progress_pct=0, completed=False) -> str:
    diff_map = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}
    diff_cls = diff_map.get(difficulty, "easy")
    done_overlay = '<div style="color:#22c55e;font-weight:800;font-size:1.1rem;margin-top:8px">COMPLETED!</div>' if completed else ""
    return f"""
    <div class="challenge-card">
        <span class="challenge-difficulty diff-{diff_cls}">{difficulty}</span>
        <div class="challenge-title">{title}</div>
        <div class="challenge-desc">{desc}</div>
        <div class="challenge-reward">Reward: {reward}</div>
        <div class="xp-bar-bg">
            <div class="xp-bar-fill" style="width:{progress_pct}%"></div>
        </div>
        <div class="challenge-prog">{progress_pct}% complete</div>
        {done_overlay}
    </div>
    """
