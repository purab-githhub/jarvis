from datetime import date

from database import get_connection
from recurring_schedule import get_recurring_events_for_date


def get_daily_agenda(agenda_date=None):
    """Return pending tasks, assignments, and planned one-time/recurring events for one date."""
    agenda_date = agenda_date or date.today().isoformat()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, category, due_time
        FROM tasks
        WHERE status = 'Pending' AND due_date = ?
        ORDER BY due_time IS NULL, due_time, id
        """,
        (agenda_date,),
    )
    tasks = cursor.fetchall()

    cursor.execute(
        """
        SELECT id, title, subject, due_time
        FROM assignments
        WHERE status = 'Pending' AND due_date = ?
        ORDER BY due_time IS NULL, due_time, id
        """,
        (agenda_date,),
    )
    assignments = cursor.fetchall()

    cursor.execute(
        """
        SELECT id, title, event_time, event_type
        FROM schedule
        WHERE status = 'Planned' AND event_date = ?
        ORDER BY event_time IS NULL, event_time, id
        """,
        (agenda_date,),
    )
    events = cursor.fetchall()
    conn.close()

    events.extend(get_recurring_events_for_date(agenda_date))
    events.sort(key=lambda event: (event[2] is None, event[2] or "23:59", event[0]))
    return tasks, assignments, events


def get_agenda_counts(agenda_date=None):
    tasks, assignments, events = get_daily_agenda(agenda_date)
    return len(tasks), len(assignments), len(events)
