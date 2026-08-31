# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 31 August 2026  
**Current milestone:** v0.11 — Recurring Weekly Schedule Support

---

## Current Architecture

```text
YOU
 │
 ▼
main.py ───────────── command interface
 │
 ├── agenda.py ─────── unified daily view
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
`agenda.py` combines today's pending tasks, assignments, and planned schedule events into one student-focused view.

The agenda now also includes active recurring weekly events that match the current weekday.

### Recurring Weekly Schedule — New in v0.11
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

Recurring events are stored as weekly templates rather than duplicated into the one-time schedule table. The daily agenda checks the current weekday and includes matching active recurring events automatically.

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
- The daily agenda currently covers one date at a time and does not yet prioritize or intelligently reschedule work.

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
- [ ] Exam tracker
- [ ] Practical/lab tracker
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

The next practical step is to build the **Weekly Planner**, using the daily agenda, assignments, tasks, one-time schedule, and recurring schedule as inputs. This should provide a useful week-at-a-glance view before adding more advanced AI prioritization.

## Current Status

> **JARVIS v0.11 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, and Unified Daily Agenda**
