from datetime import date, timedelta

from agenda import get_daily_agenda


def get_week_start(target_date=None):
    target = date.fromisoformat(target_date) if target_date else date.today()
    return target - timedelta(days=target.weekday())


def get_weekly_plan(target_date=None):
    """Return the unified daily agenda for each day in the Monday-Sunday week."""
    week_start = get_week_start(target_date)
    plan = []
    for offset in range(7):
        current = week_start + timedelta(days=offset)
        tasks, assignments, events = get_daily_agenda(current.isoformat())
        plan.append((current, tasks, assignments, events))
    return plan


def get_weekly_counts(target_date=None):
    plan = get_weekly_plan(target_date)
    return {
        "tasks": sum(len(day[1]) for day in plan),
        "assignments": sum(len(day[2]) for day in plan),
        "events": sum(len(day[3]) for day in plan),
    }


def print_weekly_plan(target_date=None):
    plan = get_weekly_plan(target_date)
    week_start = plan[0][0]
    week_end = plan[-1][0]
    print(f"\n========== JARVIS WEEKLY PLANNER ({week_start.isoformat()} to {week_end.isoformat()}) ==========")
    total = 0
    for current_date, tasks, assignments, events in plan:
        day_total = len(tasks) + len(assignments) + len(events)
        total += day_total
        print(f"\n{current_date.strftime('%A, %d %b %Y')} — {day_total} item(s)")
        if not day_total:
            print("  No planned items.")
            continue
        for task_id, title, category, due_time in tasks:
            when = f" at {due_time}" if due_time else ""
            print(f"  [Task #{task_id}] {title} | {category}{when}")
        for assignment_id, title, subject, due_time in assignments:
            when = f" at {due_time}" if due_time else ""
            print(f"  [Assignment #{assignment_id}] {title} | {subject}{when}")
        for event_id, title, event_time, event_type in events:
            when = f" at {event_time}" if event_time else ""
            print(f"  [Event #{event_id}] {title} | {event_type}{when}")
    print(f"\nJARVIS: {total} item(s) planned this week.\n")


if __name__ == "__main__":
    from database import initialize_database
    initialize_database()
    print_weekly_plan()
