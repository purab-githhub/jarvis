# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 29 August 2026  
**Current milestone:** v0.9 — Tasks, Assignments, Notes, Reminders & Schedule

---

## Current Architecture

```text
YOU
 │
 ▼
main.py ─────── command interface
 │
 ├── tasks.py ─────── task management
 ├── assignments.py ─ assignment management
 ├── notes.py ─────── note management
 ├── schedule.py ──── schedule management
 └── database.py ──── SQLite setup
             │
             ▼
         jarvis.db

reminder_service.py
 ├── checks due tasks
 └── checks due assignments
```

## Implemented Features

### Tasks
- Persistent SQLite storage
- Due dates and due times
- Relative dates such as today, tomorrow, weekdays, and next Monday
- Common 12-hour and 24-hour time formats
- View pending/all tasks and mark tasks completed
- Due/overdue detection

### Assignments
- Separate assignments table and module
- Subject, deadline, time, status, and creation timestamp
- View pending/all assignments and mark assignments completed

### Unified Background Reminders
- Checks tasks and assignments every 30 seconds
- Desktop notifications through free `plyer` where supported
- Console fallback
- Prevents repeated notifications during the same service run

### Notes
A dedicated `notes` table and `notes.py` module allow JARVIS to persist study notes.

Each note stores:
- Unique ID
- Title
- Full content
- Subject/category
- Creation timestamp

Commands:

```text
note <title>: <content> for <subject>
notes
notes <subject>
readnote <id>
searchnotes <keyword>
```

### Schedule — New in v0.9
A dedicated `schedule` table and `schedule.py` module now allow JARVIS to store planned classes, study sessions, and other events.

Each schedule event stores:
- Unique ID
- Event title
- Date
- Optional time
- Event type
- Planned/Completed status
- Creation timestamp

Commands:

```text
schedule <event> due tomorrow at 6 pm type Study
schedulelist
today
completeschedule <id>
```

Example:

```text
schedule DSA revision due tomorrow at 7 pm type Study
```

Then:

```text
today
```

shows the events scheduled for today, while:

```text
schedulelist
```

shows planned upcoming events.

## Current Workflow

```text
Create task / assignment / note / schedule event
        ↓
Store permanently in SQLite
        ↓
Tasks and assignments may include deadlines
        ↓
Reminder service checks task/assignment deadlines
        ↓
Schedule provides planned daily events
        ↓
Notes can be listed, filtered, read, or searched
```

## Current Limitations
- Reminder service still requires manual startup; automatic OS startup is pending.
- Desktop notifications are best tested locally rather than in Codespaces.
- Schedule events are currently one-time events; recurring weekly schedules are not yet implemented.
- Schedule commands are currently structured rather than fully conversational.
- Note creation is command-based rather than conversational or multi-line.
- Search is basic keyword matching.

## Development Roadmap

### Phase 1 — Core Student Assistant
- [x] SQLite database foundation
- [x] Task storage and completion
- [x] Date/time parsing
- [x] Due/overdue detection
- [x] Background reminder-service foundation
- [x] Unified reminders for tasks and assignments
- [ ] Automatic startup/background scheduling

### Phase 2 — Student Productivity
- [x] Assignments module
- [x] Notes module
- [x] Schedule module
- [ ] Recurring weekly schedule
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Daily agenda combining tasks, assignments, and schedule
- [ ] Weekly planning

### Later Phases
- Better natural-language understanding
- Context-aware commands
- Voice input/output
- AI reasoning layer
- Intelligent workload prioritization
- Calendar and other explicitly authorized integrations
- Dashboard and multi-device access

## Immediate Next Step

The next practical step is to build a **Daily Agenda** that combines today's schedule events, due tasks, due assignments, and important reminders into one JARVIS view. After that, recurring weekly schedule support can be added.

## Current Status

> **JARVIS v0.9 — Persistent Task, Assignment, Notes, Schedule, and Reminder Foundation**
