"""
CarbonSnap – SQLite Authentication Database
Handles user registration, login, and session persistence.
"""
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime

# DB file lives next to app.py
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "carbonsnap.db")


# ── Schema ────────────────────────────────────────────────────────────────────
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    UNIQUE NOT NULL,
    email       TEXT    UNIQUE NOT NULL,
    password_hash TEXT  NOT NULL,
    salt        TEXT    NOT NULL,
    full_name   TEXT    NOT NULL,
    city        TEXT    DEFAULT 'Pune / Pimpri',
    mobile      TEXT,
    created_at  TEXT    DEFAULT (datetime('now')),
    last_login  TEXT
);
"""

CREATE_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS carbon_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    date        TEXT    NOT NULL,
    total_kg    REAL    NOT NULL,
    transport_kg REAL   DEFAULT 0,
    energy_kg   REAL    DEFAULT 0,
    food_kg     REAL    DEFAULT 0,
    waste_kg    REAL    DEFAULT 0,
    electricity REAL    DEFAULT 0,
    car_petrol  REAL    DEFAULT 0,
    created_at  TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
);
"""

CREATE_BADGES_TABLE = """
CREATE TABLE IF NOT EXISTS user_badges (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    badge_key TEXT   NOT NULL,
    earned_at TEXT   DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, badge_key)
);
"""

CREATE_XP_TABLE = """
CREATE TABLE IF NOT EXISTS user_xp (
    user_id  INTEGER PRIMARY KEY,
    xp       INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


def get_connection() -> sqlite3.Connection:
    """Return a database connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables on first run."""
    with get_connection() as conn:
        conn.execute(CREATE_USERS_TABLE)
        conn.execute(CREATE_HISTORY_TABLE)
        conn.execute(CREATE_BADGES_TABLE)
        conn.execute(CREATE_XP_TABLE)
        
        # Migration: Add mobile column if not exists
        try:
            conn.execute("ALTER TABLE users ADD COLUMN mobile TEXT")
        except sqlite3.OperationalError:
            pass # Column already exists
            
        conn.commit()


# ── Password Hashing ──────────────────────────────────────────────────────────
def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def _generate_salt() -> str:
    return secrets.token_hex(16)


# ── User Operations ───────────────────────────────────────────────────────────
def register_user(username: str, email: str, password: str,
                  full_name: str, city: str = "Pune / Pimpri", mobile: str = "") -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str)
    """
    username = username.strip().lower()
    email    = email.strip().lower()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."

    salt = _generate_salt()
    pw_hash = _hash_password(password, salt)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, salt, full_name, city, mobile) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username, email, pw_hash, salt, full_name.strip(), city, mobile.strip())
            )
            # Get new user ID
            user = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
            if user:
                conn.execute("INSERT INTO user_xp (user_id, xp) VALUES (?, 0)", (user["id"],))
            conn.commit()
        return True, "Account created successfully! Welcome to CarbonSnap! 🌿"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already taken. Try another one."
        elif "email" in str(e):
            return False, "Email already registered. Please login instead."
        return False, "Registration failed. Please try again."


def login_user(username_or_email: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Authenticate a user.
    Returns (success: bool, message: str, user_dict | None)
    """
    identifier = username_or_email.strip().lower()

    with get_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=? OR email=?",
            (identifier, identifier)
        ).fetchone()

    if not user:
        return False, "User not found. Please sign up first.", None

    pw_hash = _hash_password(password, user["salt"])
    if pw_hash != user["password_hash"]:
        return False, "Incorrect password. Please try again.", None

    # Update last login
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET last_login=? WHERE id=?",
            (datetime.now().isoformat(), user["id"])
        )
        conn.commit()

    return True, f"Welcome back, {user['full_name']}! 🌿", dict(user)


def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else None


def update_user_profile(user_id: int, city: str, full_name: str):
    """Update user's basic profile details"""
    with get_connection() as conn:
        conn.execute("UPDATE users SET city=?, full_name=? WHERE id=?", (city, full_name, user_id))
        conn.commit()


# ── History (persisted per user) ──────────────────────────────────────────────
def save_history_db(user_id: int, entry: dict):
    """Upsert a daily history entry for a user."""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO carbon_history
                (user_id, date, total_kg, transport_kg, energy_kg, food_kg, waste_kg, electricity, car_petrol)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                total_kg     = excluded.total_kg,
                transport_kg = excluded.transport_kg,
                energy_kg    = excluded.energy_kg,
                food_kg      = excluded.food_kg,
                waste_kg     = excluded.waste_kg,
                electricity  = excluded.electricity,
                car_petrol   = excluded.car_petrol
        """, (
            user_id,
            entry.get("date"),
            entry.get("total_kg", 0),
            entry.get("transport_kg", 0),
            entry.get("energy_kg", 0),
            entry.get("food_kg", 0),
            entry.get("waste_kg", 0),
            entry.get("electricity", 0),
            entry.get("car_petrol", 0),
        ))
        conn.commit()


def load_history_db(user_id: int) -> list:
    """Load all history for a user, sorted by date."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM carbon_history WHERE user_id=? ORDER BY date ASC",
            (user_id,)
        ).fetchall()
    return [dict(r) for r in rows]


# ── Badges (persisted per user) ────────────────────────────────────────────────
def save_badge_db(user_id: int, badge_key: str):
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO user_badges (user_id, badge_key) VALUES (?,?)",
                (user_id, badge_key)
            )
            conn.commit()
        except sqlite3.Error:
            pass


def load_badges_db(user_id: int) -> set:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT badge_key FROM user_badges WHERE user_id=?",
            (user_id,)
        ).fetchall()
    return {r["badge_key"] for r in rows}


# ── XP (persisted per user) ────────────────────────────────────────────────────
def save_xp_db(user_id: int, xp: int):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO user_xp (user_id, xp) VALUES (?,?) "
            "ON CONFLICT(user_id) DO UPDATE SET xp=excluded.xp",
            (user_id, xp)
        )
        conn.commit()


def load_xp_db(user_id: int) -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT xp FROM user_xp WHERE user_id=?", (user_id,)).fetchone()
    return row["xp"] if row else 0
