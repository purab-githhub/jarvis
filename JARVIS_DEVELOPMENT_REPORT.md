# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 1 September 2026  
**Current milestone:** v0.12 — Weekly Planner Foundation

---

## Current Architecture

```text
YOU
 │
 ▼
main.py ───────────── command interface
 │
 ├── agenda.py ─────── unified daily view
 ├── weekly_planner.py ─ weekly Monday-Sunday planner
 ├── tasks.py ──────── task management
 ├── assignments.py ── assignment management
 ├── notes.py ──────── note management
 ├── schedule.py ───── one-time schedule management
 ├── recurring_schedule.py ─ weekly recurring schedule
 └── database.py ───── SQLite setup
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

Commands:

```text
note <title>: <content> for <subject>
notes
notes <subject>
readnote <id>
searchnotes <keyword>
```

### Schedule
A dedicated `schedule` table and `schedule.py` module allow JARVIS to store one-time classes, study sessions, and other events.

Commands:

```text
schedule <event> due tomorrow at 6 pm type Study
schedulelist
today
completeschedule <id>
```

### Daily Agenda
`agenda.py` combines today's pending tasks, assignments, and planned schedule events into one student-focused view. Active recurring weekly events matching the current weekday are included automatically.

### Recurring Weekly Schedule
A dedicated `recurring_schedule` table and `recurring_schedule.py` module allow regular events to repeat automatically by weekday.

Example:

```text
recurring DSA class every monday at 10 am type Class
```

Other commands:

```text
recurringlist
completerecurring <id>
```

Recurring events are stored as weekly templates rather than duplicated into the one-time schedule table.

### Weekly Planner — New in v0.12
A new `weekly_planner.py` module builds a Monday-Sunday plan by reusing the existing daily agenda for each date. This means the weekly view combines pending tasks, assignments, one-time schedule events, and matching recurring events without duplicating storage logic.

The module provides:

- `get_week_start()` — resolves the Monday of the selected week
- `get_weekly_plan()` — returns all seven daily agenda datasets
- `get_weekly_counts()` — summarizes weekly workload
- `print_weekly_plan()` — prints a human-readable week-at-a-glance view

The planner can currently be tested directly with:

```bash
python weekly_planner.py
```

The existing interactive `main.py` command interface remains on v0.11 while the weekly planner is validated before being wired into the main command loop.

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
Daily Agenda combines today's work and schedule
        ↓
Recurring schedule adds regular weekly events automatically
        ↓
Weekly Planner reuses each day's agenda across Monday-Sunday
        ↓
Notes can be listed, filtered, read, or searched
```

## Current Limitations
- Reminder service still requires manual startup; automatic OS startup is pending.
- Desktop notifications are best tested locally rather than in Codespaces.
- Recurring schedules currently support weekly weekday repetition only.
- Recurring schedule completion disables the recurring template rather than completing one occurrence.
- Schedule, task, assignment, and note commands are still structured rather than fully conversational.
- Note creation is command-based rather than conversational or multi-line.
- Search is basic keyword matching.
- Weekly planner currently prints the combined week but does not yet prioritize workload, detect conflicts, or intelligently reschedule work.
- The weekly planner is currently exposed as a standalone module while it is validated; main-command integration is the next small integration step.

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
- [x] Daily agenda
- [x] Recurring weekly schedule
- [x] Weekly planner foundation
- [ ] Weekly planner main-command integration
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Workload prioritization

### Later Phases
- Better natural-language understanding
- Context-aware commands
- Voice input/output
- AI reasoning layer
- Intelligent workload prioritization
- Calendar and other explicitly authorized integrations
- Dashboard and multi-device access

## Immediate Next Step

Validate the weekly planner and then integrate it into `main.py` as a simple `week` command. After that, the planner can be extended with workload priorities and conflict detection.

## Current Status

> **JARVIS v0.12 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, Unified Daily Agenda, and Weekly Planner Foundation**
