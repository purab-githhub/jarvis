from collections import defaultdict

from database import get_connection
from planner_insights import get_weekly_items


DEFAULT_MINUTES = {
    "Assignment": 90,
    "Task": 45,
    "Event": 60,
}

KEYWORD_MINUTES = {
    "exam": 120,
    "revision": 90,
    "study": 60,
    "assignment": 90,
    "project": 120,
    "practical": 90,
    "lab": 90,
    "reading": 45,
    "read": 45,
    "practice": 60,
    "quiz": 45,
    "test": 90,
}


def get_effort_override(kind, item_id):
    """Return a user-entered effort value, or None when no override exists."""
    conn = get_connection()
    row = conn.execute(
        "SELECT minutes FROM effort_overrides WHERE kind = ? AND item_id = ?",
        (kind, item_id),
    ).fetchone()
    conn.close()
    return row[0] if row else None


def estimate_minutes(item):
    """Return a user override when available, otherwise a transparent estimate."""
    override = get_effort_override(item.get("kind"), item.get("id"))
    if override is not None:
        return override

    title = item.get("title", "").lower()
    detail = item.get("detail", "").lower()
    text = f"{title} {detail}"
    for keyword, minutes in KEYWORD_MINUTES.items():
        if keyword in text:
            return minutes
    return DEFAULT_MINUTES.get(item.get("kind"), 45)


def set_effort_override(kind, item_id, minutes):
    """Persist a user-entered effort estimate for a planner item."""
    if kind not in DEFAULT_MINUTES:
        raise ValueError("kind must be Task, Assignment, or Event")
    if not isinstance(item_id, int) or item_id <= 0:
        raise ValueError("item_id must be a positive integer")
    if not isinstance(minutes, int) or minutes <= 0:
        raise ValueError("minutes must be a positive integer")

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO effort_overrides (kind, item_id, minutes, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(kind, item_id) DO UPDATE SET
            minutes = excluded.minutes,
            updated_at = CURRENT_TIMESTAMP
        """,
        (kind, item_id, minutes),
    )
    conn.commit()
    conn.close()


def clear_effort_override(kind, item_id):
    """Remove a user-entered effort value so the heuristic estimate is used again."""
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM effort_overrides WHERE kind = ? AND item_id = ?",
        (kind, item_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def get_effort_items(target_date=None):
    """Attach an estimated effort value to each weekly planner item."""
    items = []
    for item in get_weekly_items(target_date):
        enriched = dict(item)
        enriched["estimated_minutes"] = estimate_minutes(item)
        items.append(enriched)
    return items


def get_daily_effort(target_date=None):
    """Return estimated effort totals by date."""
    totals = defaultdict(int)
    for item in get_effort_items(target_date):
        totals[item["date"]] += item["estimated_minutes"]
    return dict(totals)


def get_effort_warnings(target_date=None, daily_capacity_minutes=240):
    """Return days whose estimated work exceeds the configured daily capacity."""
    totals = get_daily_effort(target_date)
    return {
        day: minutes
        for day, minutes in totals.items()
        if minutes > daily_capacity_minutes
    }


def print_effort_plan(target_date=None, daily_capacity_minutes=240):
    items = get_effort_items(target_date)
    print("\n========== JARVIS EFFORT PLAN ==========")
    if not items:
        print("\nJARVIS: No planned work found for this week.\n")
        return

    print("\n[ESTIMATED EFFORT]")
    for item in sorted(items, key=lambda x: (x["date"], x["time"] or "23:59")):
        when = f"{item['date']}" + (f" at {item['time']}" if item['time'] else "")
        print(f"  {when} | {item['kind']} #{item['id']} | {item['title']} | ~{item['estimated_minutes']} min")

    print(f"\n[DAILY CAPACITY: {daily_capacity_minutes} min]")
    totals = get_daily_effort(target_date)
    for day in sorted(totals):
        minutes = totals[day]
        hours = minutes / 60
        marker = "  ⚠" if minutes > daily_capacity_minutes else "   "
        print(f"{marker} {day}: ~{minutes} min ({hours:.1f} hr)")

    warnings = get_effort_warnings(target_date, daily_capacity_minutes)
    print("\n[EFFORT WARNINGS]")
    if warnings:
        for day, minutes in sorted(warnings.items()):
            excess = minutes - daily_capacity_minutes
            print(f"  ⚠ {day}: estimated load exceeds capacity by ~{excess} min")
    else:
        print("  No estimated capacity overloads detected.")
    print()


if __name__ == "__main__":
    from database import initialize_database
    initialize_database()
    print_effort_plan()
