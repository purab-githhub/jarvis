"""Suggest safe workload redistribution across the current planning week.

The optimizer is recommendation-only: it never changes tasks, assignments, or
schedule entries. Timed items and events are left in place because moving them
could create new schedule conflicts or change commitments.
"""

from collections import defaultdict

from effort_planner import get_effort_items
from settings import get_daily_capacity


def get_redistribution_suggestions(target_date=None, daily_capacity_minutes=None):
    """Return recommendation dictionaries for moving flexible work to lighter days."""
    if daily_capacity_minutes is None:
        daily_capacity_minutes = get_daily_capacity()

    items = get_effort_items(target_date)
    totals = defaultdict(int)
    by_day = defaultdict(list)
    for item in items:
        totals[item["date"]] += item["estimated_minutes"]
        by_day[item["date"]].append(item)

    if not totals:
        return []

    candidates = {
        day: [
            item for item in day_items
            if item["kind"] in {"Task", "Assignment"} and not item["time"]
        ]
        for day, day_items in by_day.items()
    }

    suggestions = []
    working_totals = dict(totals)

    for source_day in sorted(working_totals):
        excess = working_totals[source_day] - daily_capacity_minutes
        if excess <= 0:
            continue

        source_items = sorted(
            candidates.get(source_day, []),
            key=lambda item: (-item["estimated_minutes"], -item["score"], item["title"].lower()),
        )

        while excess > 0 and source_items:
            target_days = [
                day for day in sorted(working_totals)
                if day != source_day and working_totals[day] < daily_capacity_minutes
            ]
            if not target_days:
                break

            target_day = max(
                target_days,
                key=lambda day: daily_capacity_minutes - working_totals[day],
            )
            available = daily_capacity_minutes - working_totals[target_day]

            fitting = [
                item for item in source_items
                if item["estimated_minutes"] <= min(excess, available)
            ]
            if fitting:
                item = max(fitting, key=lambda value: value["estimated_minutes"])
            else:
                fitting = [
                    item for item in source_items
                    if item["estimated_minutes"] <= available
                ]
                if not fitting:
                    break
                item = min(fitting, key=lambda value: value["estimated_minutes"])

            minutes = item["estimated_minutes"]
            suggestions.append({
                "kind": item["kind"],
                "id": item["id"],
                "title": item["title"],
                "minutes": minutes,
                "from_date": source_day,
                "to_date": target_day,
            })
            working_totals[source_day] -= minutes
            working_totals[target_day] += minutes
            excess -= minutes
            source_items.remove(item)

    return suggestions


def print_redistribution_plan(target_date=None, daily_capacity_minutes=None):
    """Print safe workload redistribution recommendations."""
    if daily_capacity_minutes is None:
        daily_capacity_minutes = get_daily_capacity()

    print("\n========== JARVIS WORKLOAD OPTIMIZER ==========")
    print(f"\n[DAILY CAPACITY: {daily_capacity_minutes} min]")

    suggestions = get_redistribution_suggestions(target_date, daily_capacity_minutes)
    if not suggestions:
        print("  No safe redistribution suggestions are needed.")
        print("  Either the workload fits capacity or only fixed/timed items are overloaded.")
        print()
        return

    print("\n[RECOMMENDED MOVES]")
    for suggestion in suggestions:
        print(
            f"  {suggestion['kind']} #{suggestion['id']} '{suggestion['title']}' "
            f"(~{suggestion['minutes']} min): {suggestion['from_date']} -> {suggestion['to_date']}"
        )

    print("\nJARVIS: These are recommendations only; no calendar or task data was changed.\n")


if __name__ == "__main__":
    from database import initialize_database

    initialize_database()
    print_redistribution_plan()
