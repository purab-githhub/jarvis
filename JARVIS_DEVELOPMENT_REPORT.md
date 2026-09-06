# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 6 September 2026  
**Current milestone:** v0.17 — User-Entered Effort Estimates

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
 ├── effort_planner.py ─ effort estimates, overrides, capacity warnings
 ├── effort.py ─────── standalone effort-planner entry point
 ├── duration.py ────── standalone effort-duration override command
 ├── planner.py ────── unified planner entry point
 ├── tasks.py ──────── task management
 ├── assignments.py ── assignment management
 ├── notes.py ──────── note management
 ├── schedule.py ───── one-time schedule management
 ├── recurring_schedule.py ─ weekly recurring schedule
 └── database.py ───── SQLite setup + effort override storage
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
- Monday-Sunday view built by reusing the daily agenda
- Combines pending tasks, assignments, one-time schedule events, and recurring events
- Standalone `week.py` entry point

### Weekly Planner Insights
- Explainable priority scoring
- Higher urgency for overdue and near-term work
- Assignment/task/event base priorities
- Exact date/time conflict detection
- Daily item-load warnings
- Standalone `insights.py` entry point

### Effort-Aware Workload Planning
- Transparent estimated minutes based on item type and keywords
- Daily estimated workload totals
- Configurable daily capacity, default 240 minutes
- Capacity overload warnings
- Standalone `effort.py` entry point

### Unified Planner Entry Point
`planner.py` combines the three planner views into one safe standalone workflow:

1. Weekly planner
2. Planner insights
3. Effort-aware workload plan

Run it with:

```bash
python planner.py
```

### User-Entered Effort Estimates — New in v0.17
JARVIS now supports persistent effort overrides for individual planner items.

Examples:

```bash
python duration.py task 3 60
python duration.py assignment 2 120
python duration.py event 4 90
python duration.py clear task 3
```

The override is stored in the SQLite `effort_overrides` table and takes precedence over the heuristic estimate used by `effort_planner.py`. Clearing an override returns the item to the automatic heuristic estimate.

This keeps the planner useful out of the box while allowing the user to gradually personalize estimates.

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
Effort Planner estimates workload
        ↓
User duration overrides can replace heuristic estimates
        ↓
Capacity warnings use the personalized effort values
        ↓
Unified Planner presents all three planning views together
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
- Effort estimates now support user overrides, but new items still start with heuristic defaults until personalized.
- Daily capacity is currently a configurable fixed default of 240 minutes.
- The unified planner is currently a standalone entry point; direct `week`/`insights`/`effort` integration into the existing `main.py` command loop remains pending.

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
- [x] Effort-aware workload planning foundation
- [x] Unified planner entry point
- [x] User-entered effort overrides
- [ ] Weekly planner main-command integration
- [ ] Duration-aware conflict detection
- [ ] User-configurable daily capacity
- [ ] Exam tracker
- [ ] Practical/lab tracker

### Later Phases
- Better natural-language understanding
- Context-aware commands
- Voice input/output
- AI reasoning layer
- Intelligent workload prioritization
- Calendar and other explicitly authorized integrations
- Dashboard and multi-device access

## Immediate Next Step

Safely integrate the unified planner and duration controls into the existing JARVIS command interface using small targeted changes. Then upgrade conflict detection from exact timestamp matching to duration-aware overlapping time ranges.

## Current Status

> **JARVIS v0.17 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, Unified Daily Agenda, Weekly Planner, Explainable Planner Insights, Effort-Aware Workload Planning, Unified Planner Entry Point, and User-Entered Effort Estimates**
