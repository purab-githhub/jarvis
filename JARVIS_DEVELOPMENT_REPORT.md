# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 3 September 2026  
**Current milestone:** v0.14 — Weekly Planner Insights

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
 ├── week.py ───────── standalone weekly-planner entry point
 ├── planner_insights.py ─ priorities, conflicts, daily load
 ├── insights.py ───── standalone insights entry point
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
- Persistent study notes in a dedicated SQLite table
- List, subject-filter, read, and keyword-search commands

### Schedule
- One-time classes, study sessions, and other events
- Date, time, type, and completion status

### Daily Agenda
- Combines pending tasks, assignments, one-time schedule events, and matching recurring events for a date

### Recurring Weekly Schedule
- Weekly weekday templates
- Recurring event listing and disabling
- Matching events appear automatically in the daily agenda

### Weekly Planner
`weekly_planner.py` builds a Monday-Sunday plan by reusing the daily agenda. It combines pending tasks, assignments, one-time schedule events, and matching recurring events.

`week.py` provides a standalone command-line entry point:

```bash
python week.py
```

### Weekly Planner Insights — New in v0.14
`planner_insights.py` adds a simple, explainable planning layer on top of the existing weekly planner.

It provides:

- Priority scoring for tasks, assignments, and events
- Higher urgency for overdue and near-term work
- Higher base priority for assignments than ordinary tasks/events
- Exact date/time conflict detection when multiple items share the same explicit slot
- Daily workload counts
- A warning marker for days containing five or more planned items

The standalone entry point is:

```bash
python insights.py
```

The priority system is intentionally rule-based and transparent at this stage. It is not yet an AI prediction system.

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
Planner Insights ranks urgency and detects exact time conflicts
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
- Weekly planner insights use simple rules rather than AI-based prioritization.
- Conflict detection currently catches only exact matches on an explicit date and time; it does not yet know event duration or detect overlapping time ranges.
- Daily overload detection uses a simple five-item threshold rather than estimated study effort.
- The weekly planner is available through `weekly_planner.py` and `week.py`; direct `week` integration into the existing `main.py` command loop remains pending.

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
- [x] Standalone weekly planner entry point
- [x] Workload prioritization foundation
- [x] Exact conflict detection foundation
- [ ] Weekly planner main-command integration
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Duration-aware conflict detection
- [ ] Effort-based workload planning

### Later Phases
- Better natural-language understanding
- Context-aware commands
- Voice input/output
- AI reasoning layer
- Intelligent workload prioritization
- Calendar and other explicitly authorized integrations
- Dashboard and multi-device access

## Immediate Next Step

Safely integrate planner insights into the existing JARVIS command interface, preferably with `week` and an `insights` command. Then improve conflict detection using event durations and build effort-aware workload planning. Avoid replacing the full CLI when a targeted patch is possible.

## Current Status

> **JARVIS v0.14 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, Unified Daily Agenda, Weekly Planner, and Explainable Planner Insights**
