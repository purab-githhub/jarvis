# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 8 September 2026  
**Current milestone:** v0.19 — Unified Duration-Aware Planner

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
`planner.py` now combines all planner analysis into one workflow:

1. Weekly planner
2. Planner insights
3. Effort-aware workload plan
4. Duration-aware conflict detection

Run it with:

```bash
python planner.py
```

### User-Entered Effort Estimates
JARVIS supports persistent effort overrides for individual planner items.

Examples:

```bash
python duration.py task 3 60
python duration.py assignment 2 120
python duration.py event 4 90
python duration.py clear task 3
```

The override is stored in the SQLite `effort_overrides` table and takes precedence over the heuristic estimate used by `effort_planner.py`. Clearing an override returns the item to the automatic heuristic estimate.

### Duration-Aware Conflict Detection
`duration_conflicts.py` treats each timed planner item as a time range using its estimated or user-entered duration.

Instead of only detecting identical timestamps, JARVIS can detect overlaps such as:

```text
07:00–08:30  DSA Revision
08:00–09:00  CN Study
```

The module reports the actual overlap window and the two conflicting planner items. Untimed items are ignored because there is no reliable start time from which to construct a range.

Run it with:

```bash
python duration_conflicts.py
```

The unified `planner.py` now includes this analysis automatically, so personal duration overrides affect both workload totals and overlap detection.

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
Duration-aware conflict detection converts timed items into ranges
        ↓
Unified Planner presents all planning analysis together
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
- Duration-aware conflict detection depends on an explicit start time and estimated/user-entered duration; untimed items cannot be reliably checked for overlap.
- Daily capacity is currently a configurable fixed default of 240 minutes.
- Direct `week`/`insights`/`effort`/`planner` integration into the existing `main.py` command loop remains pending.

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

Safely integrate the planner and duration commands into the existing JARVIS command interface using small targeted changes. Then add user-configurable daily capacity so workload warnings reflect the student's real available study time.

## Current Status

> **JARVIS v0.19 — Persistent Tasks, Assignments, Notes, One-Time & Recurring Schedule, Reminders, Unified Daily Agenda, Weekly Planner, Explainable Planner Insights, Effort-Aware Workload Planning, Unified Planner Entry Point, User-Entered Effort Estimates, Duration-Aware Conflict Detection, and Unified Duration-Aware Planner Output**
