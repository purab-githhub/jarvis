from datetime import date
from database import get_connection

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def add_recurring_event(title, weekday, event_time=None, event_type="Study"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recurring_schedule (title, weekday, event_time, event_type) VALUES (?, ?, ?, ?)",
        (title, weekday, event_time, event_type),
    )
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


def view_recurring_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, weekday, event_time, event_type, status FROM recurring_schedule WHERE status = 'Active' ORDER BY weekday, COALESCE(event_time, '23:59'), id"
    )
    events = cursor.fetchall()
    conn.close()
    return events


def complete_recurring_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recurring_schedule SET status = 'Completed' WHERE id = ? AND status = 'Active'",
        (event_id,),
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0


def get_recurring_events_for_date(event_date=None):
    target_date = date.fromisoformat(event_date) if event_date else date.today()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, event_time, event_type
        FROM recurring_schedule
        WHERE status = 'Active' AND weekday = ?
        ORDER BY COALESCE(event_time, '23:59'), id
        """,
        (target_date.weekday(),),
    )
    events = cursor.fetchall()
    conn.close()
    return events
