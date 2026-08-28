# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 28 August 2026  
**Current milestone:** v0.8 — Tasks, Assignments, Notes & Unified Reminders

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
- `today`, `tomorrow`, weekdays, `next monday`, standard dates, and common time formats
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

### Notes — New in v0.8
A dedicated `notes` table and `notes.py` module now allow JARVIS to persist study notes.

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

Example:

```text
note OSI Layers: Application, Presentation, Session, Transport, Network, Data Link, Physical for Computer Networks
```

Then:

```text
notes Computer Networks
readnote 1
searchnotes transport
```

## Current Workflow

```text
Create task / assignment / note
        ↓
Store permanently in SQLite
        ↓
Tasks and assignments may include deadlines
        ↓
Reminder service checks deadlines
        ↓
Notes can be listed, filtered, read, or searched
```

## Current Limitations
- Reminder service still requires manual startup; automatic OS startup is pending.
- Desktop notifications are best tested locally rather than in Codespaces.
- Note creation is currently command-based rather than conversational or multi-line.
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

The next practical step is a **Schedule module** for classes, study sessions, and recurring weekly events. That will let JARVIS answer questions such as what is scheduled today and will provide the foundation for daily agendas and weekly planning.

## Current Status

> **JARVIS v0.8 — Persistent Task, Assignment, Notes, and Unified Reminder Foundation**
