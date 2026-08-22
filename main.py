from datetime import date, datetime
import re

from database import initialize_database
from tasks import add_task, complete_task, get_due_tasks, view_tasks


def parse_due_date(command):
    match = re.search(r"\s+due\s+(.+)$", command, re.IGNORECASE)
    if not match:
        return command.strip(), None

    title = command[:match.start()].strip()
    date_text = match.group(1).strip()

    formats = ["%Y-%m-%d", "%d %b %Y", "%d %B %Y"]
    for fmt in formats:
        try:
            return title, datetime.strptime(date_text, fmt).date().isoformat()
        except ValueError:
            pass

    return title, "INVALID"


def print_tasks(tasks):
    if not tasks:
        print("\nJARVIS: No tasks found.\n")
        return

    print()
    for task_id, title, category, due_date, status in tasks:
        due = due_date if due_date else "No deadline"
        print(f"[{task_id}] {title} | {category} | Due: {due} | {status}")
    print()


def show_due_alerts():
    tasks = get_due_tasks()
    if not tasks:
        return

    today = date.today().isoformat()
    print("\n! JARVIS REMINDERS")
    for task_id, title, due_date in tasks:
        if due_date < today:
            print(f"  [{task_id}] OVERDUE: {title} (was due {due_date})")
        else:
            print(f"  [{task_id}] DUE TODAY: {title}")
    print()


def show_help():
    print("""
Available commands:
  add <task>                       Add a task without a deadline
  add <task> due 2026-08-24        Add a task with a deadline
  add <task> due 24 Aug 2026       Add a task with a deadline
  tasks                            Show all tasks
  pending                          Show pending tasks
  reminders                        Show due and overdue tasks
  complete <id>                    Mark a task as completed
  help                             Show available commands
  exit                             Close JARVIS
""")


def run_jarvis():
    initialize_database()

    print("\n================================")
    print("        JARVIS STUDENT v0.2")
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

            title, due_date = parse_due_date(parts[1])
            if due_date == "INVALID":
                print("JARVIS: I could not understand the date. Try 2026-08-24 or 24 Aug 2026.")
                continue
            if not title:
                print("JARVIS: Please provide a task title.")
                continue

            task_id = add_task(title, due_date=due_date)
            if due_date:
                print(f"JARVIS: Task #{task_id} added. Due: {due_date}.")
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
