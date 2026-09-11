from database import get_connection

DEFAULT_DAILY_CAPACITY_MINUTES = 240
DAILY_CAPACITY_KEY = "daily_capacity_minutes"


def get_daily_capacity(default=DEFAULT_DAILY_CAPACITY_MINUTES):
    """Return the user's saved daily planning capacity in minutes."""
    conn = get_connection()
    row = conn.execute(
        "SELECT setting_value FROM user_settings WHERE setting_key = ?",
        (DAILY_CAPACITY_KEY,),
    ).fetchone()
    conn.close()

    if not row:
        return default

    try:
        value = int(row[0])
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def set_daily_capacity(minutes):
    """Persist the user's daily planning capacity in minutes."""
    if not isinstance(minutes, int) or minutes <= 0:
        raise ValueError("daily capacity must be a positive integer")

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO user_settings (setting_key, setting_value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(setting_key) DO UPDATE SET
            setting_value = excluded.setting_value,
            updated_at = CURRENT_TIMESTAMP
        """,
        (DAILY_CAPACITY_KEY, str(minutes)),
    )
    conn.commit()
    conn.close()

    return minutes
