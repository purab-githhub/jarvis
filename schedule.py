from datetime import date
from database import get_connection


def add_event(title, event_date, event_time=None, event_type="Study"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schedule (title, event_date, event_time, event_type) VALUES (?, ?, ?, ?)",
        (title, event_date, event_time, event_type),
    )
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


def view_events(event_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    if event_date:
        cursor.execute(
            "SELECT id, title, event_date, event_time, event_type, status FROM schedule WHERE event_date = ? ORDER BY COALESCE(event_time, '23:59'), id",
            (event_date,),
        )
    else:
        cursor.execute(
            "SELECT id, title, event_date, event_time, event_type, status FROM schedule WHERE status = 'Planned' ORDER BY event_date, COALESCE(event_time, '23:59'), id"
        )
    events = cursor.fetchall()
    conn.close()
    return events


def complete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE schedule SET status = 'Completed' WHERE id = ? AND status = 'Planned'", (event_id,))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0


def get_today_events():
    return view_events(date.today().isoformat())
