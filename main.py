from datetime import date, datetime, timedelta
import re

from database import initialize_database
from tasks import add_task, complete_task, get_due_tasks, view_tasks


def parse_due_date(command):
    match = re.search(r"\s+due\s+(.+)$", command, re.IGNORECASE)
    if not match:
        return command.strip(), None, None

    title = command[:match.start()].strip()
    due_text = match.group(1).strip()
    time_match = re.search(r"\s+at\s+(.+)$", due_text, re.IGNORECASE)
    time_text = None
    if time_match:
        due_text = due_text[:time_match.start()].strip()
        time_text = time_match.group(1).strip().lower()

    date_text = due_text.lower()
    today = date.today()
    relative_dates = {"today": today, "tomorrow": today + timedelta(days=1)}

    due_date = None
    if date_text in relative_dates:
        due_date = relative_dates[date_text]
    else:
        weekday_names = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6,
        }
        weekday_match = re.fullmatch(r"(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", date_text)
        if weekday_match:
            is_next = bool(weekday_match.group(1))
            target = weekday_names[weekday_match.group(2)]
            days_ahead = (target - today.weekday()) % 7
            if is_next:
                days_ahead = days_ahead + 7 if days_ahead else 7
            elif days_ahead == 0:
                days_ahead = 7
            due_date = today + timedelta(days=days_ahead)
        else:
            for fmt in ("%Y-%m-%d", "%d %b %Y", "%d %B %Y"):
                try:
                    due_date = datetime.strptime(date_text, fmt).date()
                    break
                except ValueError:
                    pass

    if due_date is None:
        return title, "INVALID", None

    due_time = None
    if time_text:
        normalized = re.sub(r"\s+", " ", time_text)
        for fmt in ("%I %p", "%I:%M %p", "%H:%M"):
            try:
                due_time = datetime.strptime(normalized.upper(), fmt).strftime("%H:%M")
                break
            except ValueError:
                pass
        if due_time is None:
            return title, due_date.isoformat(), "INVALID"

    return title, due_date.isoformat(), due_time


def print_tasks(tasks):
    if not tasks:
        print("\nJARVIS: No tasks found.\n")
        return
    print()
    for task_id, title, category, due_date, due_time, status in tasks:
        due = due_date if due_date else "No deadline"
        if due_time:
            due += f" at {due_time}"
        print(f"[{task_id}] {title} | {category} | Due: {due} | {status}")
    print()


def show_due_alerts():
    tasks = get_due_tasks()
    if not tasks:
        print("\nJARVIS: No tasks are due right now.\n")
        return
    now = datetime.now()
    today = now.date().isoformat()
    print("\n! JARVIS REMINDERS")
    for task_id, title, due_date, due_time in tasks:
        when = f"{due_date} {due_time}" if due_time else due_date
        if due_date < today or (due_date == today and due_time and due_time < now.strftime("%H:%M")):
            print(f"  [{task_id}] OVERDUE: {title} (due {when})")
        else:
            print(f"  [{task_id}] DUE NOW: {title} ({when})")
    print()


def show_help():
    print("""
Available commands:
  add <task> due tomorrow
  add <task> due next monday at 6 pm
  add <task> due 2026-08-24 at 18:00
  tasks
  pending
  reminders
  complete <id>
  help
  exit
""")


def run_jarvis():
    initialize_database()
    print("\n================================")
    print("        JARVIS STUDENT v0.4")
    print("================================")
    show_due_alerts()
    print("Type 'help' to see commands.\n")

    while True:
        command = input("JARVIS > ").strip()
        if not command:
            continue
        parts = command.split(maxsplit=1)
        action = parts[0].lower()

        if action == "add":
            if len(parts) < 2:
                print("JARVIS: Please provide a task title.")
                continue
            title, due_date, due_time = parse_due_date(parts[1])
            if due_date == "INVALID":
                print("JARVIS: I could not understand the date.")
                continue
            if due_time == "INVALID":
                print("JARVIS: I could not understand the time. Try 6 pm, 6:30 pm, or 18:30.")
                continue
            if not title:
                print("JARVIS: Please provide a task title.")
                continue
            task_id = add_task(title, due_date=due_date, due_time=due_time)
            if due_date:
                when = due_date + (f" at {due_time}" if due_time else "")
                print(f"JARVIS: Task #{task_id} added. Due: {when}.")
            else:
                print(f"JARVIS: Task #{task_id} added successfully.")
        elif action == "tasks":
            print_tasks(view_tasks())
        elif action == "pending":
            print_tasks(view_tasks("Pending"))
        elif action == "reminders":
            show_due_alerts()
        elif action == "complete":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use complete <task_id>")
                continue
            if complete_task(int(parts[1])):
                print(f"JARVIS: Task #{parts[1]} completed successfully.")
            else:
                print("JARVIS: Task not found or already completed.")
        elif action == "help":
            show_help()
        elif action in {"exit", "quit"}:
            print("JARVIS: Goodbye.")
            break
        else:
            print("JARVIS: I don't understand that command. Type 'help'.")


if __name__ == "__main__":
    run_jarvis()
