import time
from datetime import datetime

try:
    from plyer import notification
except ImportError:
    notification = None

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
    notified_tasks = set()

    print("JARVIS reminder service started.")
    print("Checking for due tasks every 30 seconds. Press Ctrl+C to stop.\n")

    try:
        while True:
            due_tasks = get_due_tasks(datetime.now())
            current_ids = set()

            for task_id, title, due_date, due_time in due_tasks:
                current_ids.add(task_id)
                if task_id not in notified_tasks:
                    send_notification(
                        "JARVIS REMINDER",
                        f"{title}\nDue: {format_due(due_date, due_time)}",
                    )
                    notified_tasks.add(task_id)

            notified_tasks.intersection_update(current_ids)
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nJARVIS reminder service stopped.")


if __name__ == "__main__":
    run_reminder_service()
