from datetime import date, datetime, timedelta
import re

from assignments import add_assignment, complete_assignment, view_assignments
from database import initialize_database
from notes import add_note, get_note, search_notes, view_notes
from schedule import add_event, complete_event, get_today_events, view_events
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
        weekday_names = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
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


def parse_assignment(command):
    title, due_date, due_time = parse_due_date(command)
    if due_date == "INVALID" or due_time == "INVALID":
        return title, "General", due_date, due_time
    subject = "General"
    subject_match = re.search(r"\s+for\s+(.+)$", title, re.IGNORECASE)
    if subject_match:
        subject = subject_match.group(1).strip()
        title = title[:subject_match.start()].strip()
    return title, subject, due_date, due_time


def parse_note(command):
    subject = "General"
    subject_match = re.search(r"\s+for\s+(.+)$", command, re.IGNORECASE)
    if subject_match:
        subject = subject_match.group(1).strip()
        command = command[:subject_match.start()].strip()
    if ":" not in command:
        return None, None, subject
    title, content = command.split(":", 1)
    title, content = title.strip(), content.strip()
    if not title or not content:
        return None, None, subject
    return title, content, subject


def parse_schedule(command):
    event_type = "Study"
    type_match = re.search(r"\s+type\s+(.+)$", command, re.IGNORECASE)
    if type_match:
        event_type = type_match.group(1).strip()
        command = command[:type_match.start()].strip()
    title, event_date, event_time = parse_due_date(command)
    return title, event_date, event_time, event_type


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


def print_assignments(assignments):
    if not assignments:
        print("\nJARVIS: No assignments found.\n")
        return
    print()
    for assignment_id, title, subject, due_date, due_time, status in assignments:
        due = due_date if due_date else "No deadline"
        if due_time:
            due += f" at {due_time}"
        print(f"[{assignment_id}] {title} | Subject: {subject} | Due: {due} | {status}")
    print()


def print_notes(notes):
    if not notes:
        print("\nJARVIS: No notes found.\n")
        return
    print()
    for note_id, title, subject, created_at in notes:
        print(f"[{note_id}] {title} | Subject: {subject} | Created: {created_at}")
    print()


def print_schedule(events):
    if not events:
        print("\nJARVIS: No schedule events found.\n")
        return
    print()
    for event_id, title, event_date, event_time, event_type, status in events:
        when = event_date + (f" at {event_time}" if event_time else "")
        print(f"[{event_id}] {title} | {event_type} | {when} | {status}")
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
  assignment <title> for <subject> due next monday at 6 pm
  assignments
  pendingassignments
  completeassignment <id>
  note <title>: <content> for <subject>
  notes
  notes <subject>
  readnote <id>
  searchnotes <keyword>
  schedule <event> due tomorrow at 6 pm type Study
  schedulelist
  today
  completeschedule <id>
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
    print("        JARVIS STUDENT v0.9")
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
            task_id = add_task(title, due_date=due_date, due_time=due_time)
            print(f"JARVIS: Task #{task_id} added successfully.")
        elif action == "assignment":
            if len(parts) < 2:
                print("JARVIS: Use assignment <title> for <subject> due <date> at <time>.")
                continue
            title, subject, due_date, due_time = parse_assignment(parts[1])
            if due_date == "INVALID" or due_time == "INVALID":
                print("JARVIS: I could not understand the assignment deadline.")
                continue
            assignment_id = add_assignment(title, subject, due_date, due_time)
            print(f"JARVIS: Assignment #{assignment_id} added successfully.")
        elif action == "note":
            if len(parts) < 2:
                print("JARVIS: Use note <title>: <content> for <subject>.")
                continue
            title, content, subject = parse_note(parts[1])
            if not title:
                print("JARVIS: Use note <title>: <content> for <subject>.")
                continue
            note_id = add_note(title, content, subject)
            print(f"JARVIS: Note #{note_id} saved successfully.")
        elif action == "schedule":
            if len(parts) < 2:
                print("JARVIS: Use schedule <event> due <date> at <time> type <type>.")
                continue
            title, event_date, event_time, event_type = parse_schedule(parts[1])
            if event_date == "INVALID" or event_time == "INVALID" or not event_date:
                print("JARVIS: I could not understand the schedule date/time.")
                continue
            event_id = add_event(title, event_date, event_time, event_type)
            print(f"JARVIS: Schedule event #{event_id} added successfully.")
        elif action == "schedulelist":
            print_schedule(view_events())
        elif action == "today":
            print_schedule(get_today_events())
        elif action == "completeschedule":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use completeschedule <event_id>")
                continue
            print(f"JARVIS: {'Schedule event completed successfully.' if complete_event(int(parts[1])) else 'Schedule event not found or already completed.'}")
        elif action == "tasks":
            print_tasks(view_tasks())
        elif action == "pending":
            print_tasks(view_tasks("Pending"))
        elif action == "assignments":
            print_assignments(view_assignments())
        elif action == "pendingassignments":
            print_assignments(view_assignments("Pending"))
        elif action == "notes":
            subject = parts[1] if len(parts) > 1 else None
            print_notes(view_notes(subject))
        elif action == "readnote":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use readnote <note_id>.")
                continue
            note = get_note(int(parts[1]))
            if note:
                note_id, title, content, subject, created_at = note
                print(f"\n[{note_id}] {title}\nSubject: {subject}\nCreated: {created_at}\n\n{content}\n")
            else:
                print("JARVIS: Note not found.")
        elif action == "searchnotes":
            if len(parts) < 2:
                print("JARVIS: Use searchnotes <keyword>.")
                continue
            print_notes(search_notes(parts[1]))
        elif action == "reminders":
            show_due_alerts()
        elif action == "complete":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use complete <task_id>")
                continue
            print(f"JARVIS: {'Task completed successfully.' if complete_task(int(parts[1])) else 'Task not found or already completed.'}")
        elif action == "completeassignment":
            if len(parts) < 2 or not parts[1].isdigit():
                print("JARVIS: Use completeassignment <assignment_id>")
                continue
            print(f"JARVIS: {'Assignment completed successfully.' if complete_assignment(int(parts[1])) else 'Assignment not found or already completed.'}")
        elif action == "help":
            show_help()
        elif action in {"exit", "quit"}:
            print("JARVIS: Goodbye.")
            break
        else:
            print("JARVIS: I don't understand that command. Type 'help'.")


if __name__ == "__main__":
    run_jarvis()
