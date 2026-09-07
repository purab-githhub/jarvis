from datetime import datetime, timedelta

from effort_planner import get_effort_items


def _parse_start(date_value, time_value):
    if not date_value or not time_value:
        return None
    try:
        return datetime.fromisoformat(f"{date_value}T{time_value}")
    except ValueError:
        return None


def get_duration_conflicts(target_date=None):
    """Find overlapping timed planner items using their estimated/user-entered duration."""
    timed = []
    for item in get_effort_items(target_date):
        start = _parse_start(item.get("date"), item.get("time"))
        if start is None:
            continue
        end = start + timedelta(minutes=item["estimated_minutes"])
        timed.append((start, end, item))

    conflicts = []
    timed.sort(key=lambda entry: entry[0])
    for index, current in enumerate(timed):
        start_a, end_a, item_a = current
        for start_b, end_b, item_b in timed[index + 1:]:
            if start_b >= end_a:
                break
            if start_b < end_a and start_a < end_b:
                conflicts.append((item_a, item_b, max(start_a, start_b), min(end_a, end_b)))
    return conflicts


def print_duration_conflicts(target_date=None):
    conflicts = get_duration_conflicts(target_date)
    print("\n========== JARVIS DURATION CONFLICTS ==========")
    if not conflicts:
        print("\nJARVIS: No overlapping timed items detected.\n")
        return

    print("\n[OVERLAPPING TIME RANGES]")
    for first, second, overlap_start, overlap_end in conflicts:
        print(
            f"  ⚠ {overlap_start.strftime('%Y-%m-%d %H:%M')}–{overlap_end.strftime('%H:%M')}: "
            f"{first['kind']} #{first['id']} {first['title']} "
            f"({first['estimated_minutes']} min) overlaps "
            f"{second['kind']} #{second['id']} {second['title']} "
            f"({second['estimated_minutes']} min)"
        )
    print()


if __name__ == "__main__":
    from database import initialize_database
    initialize_database()
    print_duration_conflicts()
