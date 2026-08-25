# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 25 August 2026  
**Current milestone:** v0.5 — Background Reminder Service Foundation

---

## 1. Project Vision

JARVIS is being developed as a personal AI assistant for an engineering student. The long-term goal is to create a practical assistant that can understand natural-language requests, remember important information, manage academic work, schedule reminders, and eventually interact through voice.

The project is being developed incrementally rather than attempting a full AI assistant immediately.

---

## 2. Cost Policy

The development strategy is **₹0-first**.

The current core uses free/open-source or locally available technologies:

- Python
- SQLite
- Open-source Python libraries
- Local/system notification mechanisms
- GitHub for source-code management

No paid API is required for the current task and reminder system. Any future paid service must be explicitly identified before being added.

---

## 3. Repository Safety Rule

All current JARVIS development is restricted to:

`purab-githhub/jarvis`

Other repositories must not be modified for this project unless explicitly requested.

---

## 4. Current Architecture

```text
                 YOU
                  │
                  ▼
             ┌─────────┐
             │ main.py │  ← command interface
             └────┬────┘
                  │
                  ▼
             ┌──────────┐
             │ tasks.py │  ← task logic
             └────┬─────┘
                  │
                  ▼
           ┌──────────────┐
           │ database.py  │  ← SQLite connection/setup
           └──────┬───────┘
                  │
                  ▼
              jarvis.db

             ┌─────────────────────┐
             │ reminder_service.py │
             └──────────┬──────────┘
                        ▼
                System notification
                or console fallback
```

---

## 5. Implemented Features

### Database (`database.py`)

The SQLite database stores tasks with:

- Unique ID
- Title
- Category
- Due date
- Due time
- Status
- Creation timestamp

The initialization code also supports migration for the newer `due_time` column.

### Task Logic (`tasks.py`)

Implemented operations:

- Add task
- View all tasks
- View pending tasks
- Mark task completed
- Sort tasks by deadline
- Detect due and overdue pending tasks

### Command Interface (`main.py`)

Current commands include:

```text
add <task> due tomorrow
add <task> due next monday at 6 pm
add <task> due 2026-08-24 at 18:00
tasks
pending
reminders
complete <id>
help
exit
```

### Date and Time Understanding

JARVIS can currently understand:

- `today`
- `tomorrow`
- `monday`, `tuesday`, etc.
- `next monday`, etc.
- `YYYY-MM-DD`
- `24 Aug 2026`
- `24 August 2026`
- Times such as `6 pm`, `6:30 pm`, and `18:30`

### Background Reminder Service (`reminder_service.py`)

A dedicated reminder process now checks the database every 30 seconds.

When a pending task becomes due, the service:

1. Detects the task using the existing deadline logic.
2. Sends a desktop notification through `plyer` when the operating system supports it.
3. Falls back to a visible console reminder if desktop notification support is unavailable.
4. Avoids repeatedly notifying the same task during the same service session.

The service can be started with:

```bash
python reminder_service.py
```

The notification dependency is listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 6. Current User Workflow

```text
Add task with date/time
        ↓
JARVIS stores it in SQLite
        ↓
Run JARVIS normally for task management
        ↓
Run reminder_service.py for continuous checking
        ↓
Deadline arrives
        ↓
Desktop/console reminder appears
        ↓
User finishes work
        ↓
complete <id>
        ↓
Status becomes Completed
```

Example:

```text
add Complete DSA assignment due next monday at 6 pm
```

Later:

```text
JARVIS REMINDER
Complete DSA assignment
Due: 2026-08-31 at 18:00
```

Then:

```text
complete 1
```

---

## 7. Important Limitation

The new service is a **background process foundation**, not yet an operating-system startup service.

For reminders to be checked continuously, `reminder_service.py` must be running. If JARVIS/the reminder service is stopped, no process is available to check the database.

The next notification milestone is to integrate this service with operating-system startup or scheduling so it can launch automatically when the user logs in. This can be done using free, built-in operating-system scheduling tools.

GitHub Codespaces is useful for development and testing, but desktop notifications are expected to work best when the service is run on the user's local computer rather than inside a cloud Codespace.

---

## 8. Development Roadmap

### Phase 1 — Core Student Assistant

- [x] Repository setup
- [x] SQLite database foundation
- [x] Task storage
- [x] Task listing
- [x] Pending-task filtering
- [x] Task completion
- [x] Basic deadlines
- [x] Relative date support
- [x] Specific reminder time support
- [x] Background reminder service foundation
- [ ] Automatic startup/background scheduling
- [ ] Notification reliability testing on local OS

### Phase 2 — Student Productivity

- [ ] Assignments module
- [ ] Notes module
- [ ] Schedule module
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Daily agenda
- [ ] Weekly planning

### Phase 3 — Natural Language

- [ ] Better natural-language task creation
- [ ] More flexible date/time extraction
- [ ] Intent detection
- [ ] Context-aware commands
- [ ] Conversational task management

### Phase 4 — Voice Assistant

- [ ] Voice input
- [ ] Speech-to-text
- [ ] Text-to-speech
- [ ] Wake-word/activation workflow
- [ ] Hands-free task creation

### Phase 5 — AI Brain

Potential AI providers/models can be integrated behind a common JARVIS orchestration layer. The architecture should avoid permanent dependence on one provider.

### Phase 6 — Advanced JARVIS

- [ ] Intelligent workload prioritization
- [ ] Automatic study-plan generation
- [ ] Calendar integration
- [ ] Email/task extraction where explicitly authorized
- [ ] Project management
- [ ] Desktop automation
- [ ] Web research tools
- [ ] Personal knowledge/memory system
- [ ] Dashboard
- [ ] Multi-device access

---

## 9. Immediate Next Steps

1. Pull the latest repository changes.
2. Install the free notification dependency.
3. Test task creation with a deadline a few minutes ahead.
4. Run `reminder_service.py` and verify the reminder behavior.
5. Add automatic startup/scheduling for the user's local operating system.
6. After reminders are reliable, begin the assignments module.

---

## 10. Current Status Summary

**JARVIS now has a working task system, persistent SQLite storage, deadline/date/time parsing, due/overdue detection, and a dedicated background reminder-service foundation.**

Current milestone:

> **JARVIS v0.5 — Background Reminder Service Foundation**

The next practical objective is automatic startup and local notification testing, followed by expansion into assignments, notes, schedules, and broader student productivity features.
