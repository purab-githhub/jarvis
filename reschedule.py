"""Approval-based rescheduling for flexible tasks and assignments.

The optimizer only recommends moves. This module performs an explicit move
when the user supplies the item type, id, and new date. Existing due times are
preserved so a date change does not silently alter the planned time.
"""

from datetime import datetime

from database import get_connection


def _validate_date(new_date):
    try:
        return datetime.strptime(new_date, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return None


def reschedule_item(kind, item_id, new_date):
    """Move a pending task or assignment to a new date.

    Returns True when exactly one pending item was updated.
    """
    normalized_kind = kind.strip().lower()
    table = {"task": "tasks", "assignment": "assignments"}.get(normalized_kind)
    if table is None or not isinstance(item_id, int) or item_id <= 0:
        return False

    validated_date = _validate_date(new_date)
    if validated_date is None:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {table} SET due_date = ? WHERE id = ? AND status = 'Pending'",
        (validated_date, item_id),
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated == 1


def print_reschedule_result(kind, item_id, new_date):
    """Print a user-friendly result for an explicit reschedule request."""
    if reschedule_item(kind, item_id, new_date):
        print(f"JARVIS: {kind.title()} #{item_id} rescheduled to {new_date}.")
        return True
    print("JARVIS: Reschedule failed. Check the item type, ID, date (YYYY-MM-DD), and pending status.")
    return False


if __name__ == "__main__":
    from database import initialize_database

    initialize_database()
    print("Use the interactive JARVIS command: reschedule task <id> <YYYY-MM-DD>")
    print("or: reschedule assignment <id> <YYYY-MM-DD>")
