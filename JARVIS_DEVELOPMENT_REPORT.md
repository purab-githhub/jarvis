# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 26 August 2026  
**Current milestone:** v0.6 — Assignment Management Foundation

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
 └── database.py ──── SQLite setup
             │
             ▼
         jarvis.db

reminder_service.py ─ continuous task reminder checking
```

## Implemented Features

### Tasks

- Add tasks
- Store tasks permanently in SQLite
- Add due dates and due times
- Understand `today`, `tomorrow`, weekdays, `next monday`, standard dates, and common time formats
- View all or pending tasks
- Mark tasks completed
- Detect due and overdue tasks

### Background Reminders

`reminder_service.py` checks pending tasks continuously and uses the free `plyer` dependency for desktop notifications when supported, with a console fallback.

### Assignments — New in v0.6

A dedicated `assignments` table and `assignments.py` module now separate academic assignments from ordinary tasks.

Each assignment stores:

- Unique ID
- Assignment title
- Subject
- Due date
- Due time
- Status
- Creation timestamp

New commands:

```text
assignment <title> for <subject> due <date> at <time>
assignments
pendingassignments
completeassignment <id>
```

Example:

```text
assignment DSA linked list submission for Data Structures due next monday at 6 pm
```

Then:

```text
assignments
completeassignment 1
```

## Current Workflow

```text
Create task or assignment
        ↓
Store permanently in SQLite
        ↓
Optional date and time
        ↓
Check/manage from JARVIS
        ↓
Reminder service checks task deadlines
        ↓
Complete item when finished
```

## Current Limitation

The reminder service must currently be started manually. Automatic operating-system startup and local notification testing are still pending.

Assignments are currently managed as their own academic records, while the existing reminder service monitors the task table. Integrating assignment deadlines into the unified reminder service is a future improvement.

## Development Roadmap

### Phase 1 — Core Student Assistant

- [x] Repository setup
- [x] SQLite database foundation
- [x] Task storage and completion
- [x] Date and time parsing
- [x] Due/overdue detection
- [x] Background reminder-service foundation
- [ ] Automatic startup/background scheduling
- [ ] Unified reminders for tasks and assignments

### Phase 2 — Student Productivity

- [x] Assignments module foundation
- [ ] Notes module
- [ ] Schedule module
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Daily agenda
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

The next practical development step is to integrate assignment deadlines into the reminder service so tasks and assignments are handled by one unified reminder system.

## Current Status

> **JARVIS v0.6 — Persistent Task, Reminder, and Assignment Management Foundation**
