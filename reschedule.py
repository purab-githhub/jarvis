"""Approval-based rescheduling for flexible tasks and assignments.

The workload optimizer only recommends moves. This module performs an explicit
move when the user supplies the item type, id, and new date. Existing due times
are preserved so a date change does not silently alter the planned time.
"""

import argparse
from datetime import datetime

from database import get_connection, initialize_database


def _validate_date(new_date):
    try:
        return datetime.strptime(new_date, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return None


def reschedule_item(kind, item_id, new_date):
    """Move a pending task or assignment to a new date."""
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


def main():
    parser = argparse.ArgumentParser(
        description="Explicitly reschedule one pending JARVIS task or assignment."
    )
    parser.add_argument("kind", choices=("task", "assignment"))
    parser.add_argument("item_id", type=int)
    parser.add_argument("new_date", help="New due date in YYYY-MM-DD format")
    args = parser.parse_args()

    initialize_database()
    if reschedule_item(args.kind, args.item_id, args.new_date):
        print(f"JARVIS: {args.kind.title()} #{args.item_id} rescheduled to {args.new_date}.")
        return 0

    print(
        "JARVIS: Reschedule failed. Check the item type, ID, date "
        "(YYYY-MM-DD), and pending status."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
