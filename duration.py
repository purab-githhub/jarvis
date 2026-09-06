from database import initialize_database
from effort_planner import clear_effort_override, set_effort_override


VALID_KINDS = {"task": "Task", "assignment": "Assignment", "event": "Event"}


def parse_minutes(value):
    """Accept a positive whole-number duration in minutes."""
    minutes = int(value)
    if minutes <= 0:
        raise ValueError
    return minutes


def set_duration(kind_text, item_id_text, minutes_text):
    kind = VALID_KINDS.get(kind_text.lower())
    if not kind:
        raise ValueError("kind must be task, assignment, or event")
    item_id = int(item_id_text)
    minutes = parse_minutes(minutes_text)
    set_effort_override(kind, item_id, minutes)


def clear_duration(kind_text, item_id_text):
    kind = VALID_KINDS.get(kind_text.lower())
    if not kind:
        raise ValueError("kind must be task, assignment, or event")
    item_id = int(item_id_text)
    return clear_effort_override(kind, item_id)


def main():
    initialize_database()
    print("\n========== JARVIS DURATION SETTINGS ==========")
    print("Set a real effort estimate for a task, assignment, or schedule event.")
    print("Examples:")
    print("  python duration.py task 3 60")
    print("  python duration.py assignment 2 120")
    print("  python duration.py event 4 90")
    print("  python duration.py clear task 3")


if __name__ == "__main__":
    import sys

    initialize_database()
    args = sys.argv[1:]
    try:
        if len(args) == 3 and args[0].lower() in VALID_KINDS:
            set_duration(*args)
            print(f"JARVIS: {args[0].title()} #{args[1]} effort set to {args[2]} minutes.")
        elif len(args) == 3 and args[0].lower() == "clear":
            removed = clear_duration(args[1], args[2])
            print("JARVIS: Effort override cleared." if removed else "JARVIS: No effort override was found.")
        else:
            main()
    except (ValueError, TypeError):
        print("JARVIS: Use task, assignment, or event with a positive duration in minutes.")
