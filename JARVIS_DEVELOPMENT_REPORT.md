# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 8 September 2026  
**Current milestone:** v0.20 — Verification & Reproducible Run Foundation

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
 ├── planner_insights.py ─ priorities, exact conflicts, daily load
 ├── insights.py ───── standalone insights entry point
 ├── effort_planner.py ─ effort estimates, overrides, capacity warnings
 ├── effort.py ─────── standalone effort-planner entry point
 ├── duration.py ────── standalone effort-duration override command
 ├── duration_conflicts.py ─ duration-aware overlapping conflict detection
 ├── planner.py ────── unified planner + duration conflict entry point
 ├── tasks.py ──────── task management
 ├── assignments.py ── assignment management
 ├── notes.py ──────── note management
 ├── schedule.py ───── one-time schedule management
 ├── recurring_schedule.py ─ weekly recurring schedule
 ├── verify.py ─────── project compilation/import verification
 └── database.py ───── SQLite setup + effort override storage
             │
             ▼
         jarvis.db

reminder_service.py
 ├── checks due tasks
 └── checks due assignments

.github/workflows/verify.yml
 └── automatically verifies the project on pushes/PRs to main
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
`planner.py` combines:

1. Weekly planner
2. Planner insights
3. Effort-aware workload plan
4. Duration-aware conflict detection

Run it with:

```bash
python planner.py
```

### User-Entered Effort Estimates
Persistent effort overrides can be set for individual planner items:

```bash
python duration.py task 3 60
python duration.py assignment 2 120
python duration.py event 4 90
python duration.py clear task 3
```

Overrides take precedence over heuristic estimates.

### Duration-Aware Conflict Detection
Timed planner items are converted into ranges using estimated or user-entered durations. Overlaps such as `07:00–08:30` and `08:00–09:00` are detected. Untimed items are skipped because their range cannot be inferred reliably.

### Project Verification
`verify.py` provides a repeatable local verification command:

```bash
python verify.py
```

It:

1. Compiles the Python source tree.
2. Initializes the SQLite database.
3. Imports the major JARVIS modules without launching the interactive CLI.
4. Reports PASS/FAIL results.

A GitHub Actions workflow at `.github/workflows/verify.yml` runs this verification automatically on pushes and pull requests targeting `main`.

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
Capacity warnings use personalized effort values
        ↓
Duration-aware conflict detection converts timed items into ranges
        ↓
Unified Planner presents planning analysis together
        ↓
verify.py / GitHub Actions verifies the codebase
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
- Duration-aware conflict detection depends on an explicit start time and estimated/user-entered duration.
- Daily capacity is currently a configurable fixed default of 240 minutes.
- Direct `week`/`insights`/`effort`/`planner` integration into the existing `main.py` command loop remains pending.
- Automated verification confirms compilation/imports; it does not replace full behavioral testing with realistic user data.

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
- [x] Duration-aware conflict detection
- [x] Unified duration-aware planner output
- [x] Local project verification utility
- [x] GitHub Actions verification workflow
- [ ] Weekly planner main-command integration
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

Pull the latest `main` branch in Codespaces and run `python verify.py` to confirm the environment is healthy. Then integrate the planner commands into the existing JARVIS CLI using small targeted changes, followed by user-configurable daily capacity and workload redistribution.

## Current Status

> **JARVIS v0.20 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, Daily Agenda, Weekly Planner, Explainable Planner Insights, Effort-Aware Workload Planning, Unified Planner, User-Entered Effort Estimates, Duration-Aware Conflict Detection, and Automated Project Verification**
