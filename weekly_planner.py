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
