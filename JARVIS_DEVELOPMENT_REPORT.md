# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 27 August 2026  
**Current milestone:** v0.7 — Unified Task & Assignment Reminder System

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

reminder_service.py
 │
 ├── checks due tasks
 └── checks due assignments
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

### Assignments

A dedicated `assignments` table and `assignments.py` module separate academic assignments from ordinary tasks.

Each assignment stores:

- Unique ID
- Assignment title
- Subject
- Due date
- Due time
- Status
- Creation timestamp

Commands:

```text
assignment <title> for <subject> due <date> at <time>
assignments
pendingassignments
completeassignment <id>
```

### Unified Background Reminders — New in v0.7

`reminder_service.py` now checks both pending tasks and pending assignments every 30 seconds.

The service:

- Detects due and overdue tasks
- Detects due and overdue assignments
- Uses distinct reminder titles for tasks and assignments
- Includes the assignment subject in assignment notifications
- Uses the free `plyer` dependency for desktop notifications when supported
- Falls back to console output when desktop notifications are unavailable
- Avoids repeatedly notifying the same item during one service run

## Current Workflow

```text
Create task or assignment
        ↓
Store permanently in SQLite
        ↓
Optional date and time
        ↓
Unified reminder service checks deadlines
        ↓
JARVIS sends task/assignment reminder
        ↓
Complete item when finished
```

## Current Limitation

The reminder service must currently be started manually. Automatic operating-system startup and local notification testing are still pending.

The reminder service also needs to be running for continuous checks; running the service from Codespaces is useful for logic testing, while desktop notifications are best tested on a local computer.

## Development Roadmap

### Phase 1 — Core Student Assistant

- [x] Repository setup
- [x] SQLite database foundation
- [x] Task storage and completion
- [x] Date and time parsing
- [x] Due/overdue detection
- [x] Background reminder-service foundation
- [x] Unified reminders for tasks and assignments
- [ ] Automatic startup/background scheduling

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

The next practical development step is to add a Notes module so JARVIS can persist and retrieve student notes, while keeping the project modular before expanding into schedules and planning.

## Current Status

> **JARVIS v0.7 — Persistent Task, Assignment, and Unified Reminder Management Foundation**
