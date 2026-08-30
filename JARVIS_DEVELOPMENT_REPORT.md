# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 30 August 2026  
**Current milestone:** v0.10 — Unified Daily Agenda

---

## Current Architecture

```text
YOU
 │
 ▼
main.py ─────── command interface
 │
 ├── agenda.py ─────── unified daily view
 ├── tasks.py ──────── task management
 ├── assignments.py ── assignment management
 ├── notes.py ──────── note management
 ├── schedule.py ───── schedule management
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
A dedicated `schedule` table and `schedule.py` module allow JARVIS to store planned classes, study sessions, and other events.

Commands:

```text
schedule <event> due tomorrow at 6 pm type Study
schedulelist
today
completeschedule <id>
```

### Daily Agenda — New in v0.10
A new `agenda.py` module combines today's pending tasks, assignments, and planned schedule events into a single view.

The `today` command now provides one student-focused daily overview instead of showing only schedule events.

Example:

```text
JARVIS > today

========== JARVIS DAILY AGENDA (2026-08-30) ==========

[STUDY / TASKS]
  [Task #1] Complete DSA revision | General at 10:00

[ASSIGNMENTS]
  [Assignment #2] Submit CN assignment | Computer Networks at 18:00

[SCHEDULE]
  [Event #3] OSI revision | Study at 20:00

JARVIS: 3 item(s) planned for today.
```

The agenda reads directly from SQLite and only includes pending tasks, pending assignments, and planned schedule events for the selected day.

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
Notes can be listed, filtered, read, or searched
```

## Current Limitations
- Reminder service still requires manual startup; automatic OS startup is pending.
- Desktop notifications are best tested locally rather than in Codespaces.
- Schedule events are currently one-time events; recurring weekly schedules are not yet implemented.
- Schedule and task commands are currently structured rather than fully conversational.
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
- [ ] Recurring weekly schedule
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

The next practical step is to add **recurring weekly schedule support**, allowing classes and regular study sessions to repeat automatically without entering them every week. After that, the agenda can become the foundation for weekly planning and workload prioritization.

## Current Status

> **JARVIS v0.10 — Persistent Tasks, Assignments, Notes, Schedule, Reminders, and Unified Daily Agenda**
