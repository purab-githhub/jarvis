from datetime import date, datetime

from weekly_planner import get_weekly_plan


def _minutes(value):
    if not value:
        return None
    try:
        hour, minute = map(int, value.split(":", 1))
        return hour * 60 + minute
    except (TypeError, ValueError):
        return None


def _priority(item_kind, due_date, due_time=None):
    """Return a simple explainable priority score and label."""
    score = 0
    if item_kind == "Assignment":
        score += 30
    elif item_kind == "Task":
        score += 20
    else:
        score += 10

    try:
        days = (date.fromisoformat(due_date) - date.today()).days
    except (TypeError, ValueError):
        days = 7

    if days < 0:
        score += 60
    elif days == 0:
        score += 50
    elif days == 1:
        score += 40
    elif days <= 3:
        score += 25
    elif days <= 7:
        score += 10

    if due_time:
        score += 5

    if score >= 80:
        label = "HIGH"
    elif score >= 45:
        label = "MEDIUM"
    else:
        label = "LOW"
    return score, label


def get_weekly_items(target_date=None):
    """Flatten the weekly planner into normalized items with priority metadata."""
    items = []
    for current_date, tasks, assignments, events in get_weekly_plan(target_date):
        day = current_date.isoformat()
        for task_id, title, category, due_time in tasks:
            score, label = _priority("Task", day, due_time)
            items.append({"kind": "Task", "id": task_id, "title": title, "detail": category,
                          "date": day, "time": due_time, "score": score, "priority": label})
        for assignment_id, title, subject, due_time in assignments:
            score, label = _priority("Assignment", day, due_time)
            items.append({"kind": "Assignment", "id": assignment_id, "title": title, "detail": subject,
                          "date": day, "time": due_time, "score": score, "priority": label})
        for event_id, title, event_time, event_type in events:
            score, label = _priority("Event", day, event_time)
            items.append({"kind": "Event", "id": event_id, "title": title, "detail": event_type,
                          "date": day, "time": event_time, "score": score, "priority": label})
    return items


def get_priority_items(target_date=None):
    """Return weekly work ordered from highest to lowest priority."""
    return sorted(get_weekly_items(target_date), key=lambda item: (-item["score"], item["date"], item["time"] or "23:59"))


def get_conflicts(target_date=None):
    """Find items scheduled at the same explicit date/time."""
    timed = [item for item in get_weekly_items(target_date) if item["time"]]
    groups = {}
    for item in timed:
        groups.setdefault((item["date"], item["time"]), []).append(item)
    return [group for group in groups.values() if len(group) > 1]


def get_daily_load(target_date=None):
    """Return item counts by date for simple overload detection."""
    load = {}
    for item in get_weekly_items(target_date):
        load[item["date"]] = load.get(item["date"], 0) + 1
    return load


def print_planner_insights(target_date=None):
    items = get_weekly_items(target_date)
    print("\n========== JARVIS PLANNER INSIGHTS ==========")
    if not items:
        print("\nJARVIS: No planned work found for this week.\n")
        return

    print("\n[PRIORITIES]")
    for item in get_priority_items(target_date):
        when = f" {item['date']}" + (f" at {item['time']}" if item['time'] else "")
        print(f"  [{item['priority']}] {item['kind']} #{item['id']}: {item['title']} —{when}")

    conflicts = get_conflicts(target_date)
    print("\n[CONFLICTS]")
    if conflicts:
        for group in conflicts:
            first = group[0]
            print(f"  ⚠ {first['date']} at {first['time']}: " + " | ".join(f"{x['kind']} #{x['id']} {x['title']}" for x in group))
    else:
        print("  No exact time conflicts detected.")

    load = get_daily_load(target_date)
    print("\n[DAILY LOAD]")
    for day in sorted(load):
        marker = "  ⚠" if load[day] >= 5 else "   "
        print(f"{marker} {day}: {load[day]} item(s)")
    print()


if __name__ == "__main__":
    from database import initialize_database
    initialize_database()
    print_planner_insights()
