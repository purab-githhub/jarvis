from database import initialize_database
from tasks import add_task, complete_task, view_tasks


def print_tasks(tasks):
    if not tasks:
        print("\nJARVIS: No tasks found.\n")
        return

    print()
    for task_id, title, category, due_date, status in tasks:
        due = due_date if due_date else "No deadline"
        print(f"[{task_id}] {title} | {category} | Due: {due} | {status}")
    print()


def show_help():
    print("""
Available commands:
  add <task>          Add a new task
  tasks               Show all tasks
  pending             Show pending tasks
  complete <id>       Mark a task as completed
  help                Show available commands
  exit                Close JARVIS
""")


def run_jarvis():
    initialize_database()

    print("\n================================")
    print("        JARVIS STUDENT v0.1")
    print("================================")
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

            task_id = add_task(parts[1])
            print(f"JARVIS: Task #{task_id} added successfully.")

        elif action == "tasks":
            print_tasks(view_tasks())

        elif action == "pending":
            print_tasks(view_tasks("Pending"))

        elif action == "complete":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use complete <task_id>")
                continue

            if complete_task(int(parts[1])):
                print(f"JARVIS: Task #{parts[1]} completed successfully.")
            else:
                print("JARVIS: Task not found.")

        elif action == "help":
            show_help()

        elif action in {"exit", "quit"}:
            print("JARVIS: Goodbye.")
            break

        else:
            print("JARVIS: I don't understand that command. Type 'help'.")


if __name__ == "__main__":
    run_jarvis()
