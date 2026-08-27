import time
from datetime import datetime

try:
    from plyer import notification
except ImportError:
    notification = None

from assignments import get_due_assignments
from database import initialize_database
from tasks import get_due_tasks

CHECK_INTERVAL_SECONDS = 30


def format_due(due_date, due_time):
    return f"{due_date} at {due_time}" if due_time else due_date


def send_notification(title, message):
    if notification:
        notification.notify(
            title=title,
            message=message,
            app_name="JARVIS Student Assistant",
            timeout=10,
        )
    else:
        print(f"\n🔔 {title}\n{message}\n")


def run_reminder_service():
    initialize_database()
    notified_items = set()

    print("JARVIS reminder service started.")
    print("Checking for due tasks and assignments every 30 seconds. Press Ctrl+C to stop.\n")

    try:
        while True:
            now = datetime.now()
            due_tasks = get_due_tasks(now)
            due_assignments = get_due_assignments(now)
            current_items = set()

            for task_id, title, due_date, due_time in due_tasks:
                item_key = ("task", task_id)
                current_items.add(item_key)
                if item_key not in notified_items:
                    send_notification(
                        "JARVIS TASK REMINDER",
                        f"{title}\nDue: {format_due(due_date, due_time)}",
                    )
                    notified_items.add(item_key)

            for assignment_id, title, subject, due_date, due_time in due_assignments:
                item_key = ("assignment", assignment_id)
                current_items.add(item_key)
                if item_key not in notified_items:
                    send_notification(
                        "JARVIS ASSIGNMENT REMINDER",
                        f"{title}\nSubject: {subject}\nDue: {format_due(due_date, due_time)}",
                    )
                    notified_items.add(item_key)

            notified_items.intersection_update(current_items)
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nJARVIS reminder service stopped.")


if __name__ == "__main__":
    run_reminder_service()
