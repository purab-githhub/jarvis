# JARVIS Development Report

**Project:** JARVIS — Personal AI Student Assistant  
**Repository:** `purab-githhub/jarvis`  
**Report date:** 23 August 2026  
**Current milestone:** v0.3 — Task, Deadline & Relative-Date Foundation

---

## 1. Project Vision

JARVIS is being developed as a personal AI assistant for an engineering student. The long-term goal is to create a practical assistant that can understand natural-language requests, remember important information, manage academic work, schedule reminders, and eventually interact through voice.

The project is being developed incrementally rather than attempting a full AI assistant immediately.

### Long-term capabilities planned

- Assignment and task management
- Deadlines and reminders
- Notes and persistent memory
- Daily and weekly schedules
- Exam and practical tracking
- Natural-language commands
- Voice input and voice responses
- Smart workload planning
- AI-powered reasoning
- Optional integration with multiple AI providers
- Background notifications
- Student-focused dashboard/interface

---

## 2. Cost Policy

The development strategy is **₹0-first**.

The core system is designed around free/open-source or locally available technologies such as:

- Python
- SQLite
- Open-source Python libraries where appropriate
- Local/system notification mechanisms
- GitHub repository for source-code management

Commercial AI APIs or services are **not required for the core task/reminder system**. If a future feature requires a paid API, subscription, billing account, or usage-based service, it must be explicitly reviewed before being added.

GitHub Codespaces usage can have plan-specific usage limits, so paid Codespaces usage must not be assumed to be unlimited or free.

---

## 3. Repository Safety Rule

All current JARVIS development is restricted to:

`purab-githhub/jarvis`

Other repositories must not be modified or accessed for this project unless explicitly requested by the user.

---

## 4. GitHub Integration

The JARVIS GitHub repository has been connected to ChatGPT with write access. Files can now be created and updated directly in the repository.

The development workflow is:

1. Review the current JARVIS repository state.
2. Implement the next small feature.
3. Commit the change to the JARVIS repository.
4. Pull the change into the Codespace.
5. Test it.
6. Fix issues before moving to the next milestone.

---

## 5. Current Repository Implementation

### `database.py`

The database foundation uses SQLite. It creates a local `jarvis.db` database and initializes a `tasks` table.

The task record currently contains:

- `id` — unique task identifier
- `title` — task description
- `category` — task category
- `due_date` — optional deadline
- `status` — Pending or Completed
- `created_at` — creation timestamp

### `tasks.py`

The task-management layer provides functions for:

- Adding tasks
- Viewing tasks
- Filtering pending tasks
- Marking tasks completed
- Working with task deadlines
- Checking due/overdue work

### `main.py`

The command-line JARVIS interface connects the database and task-management layer.

The initial commands include:

```text
add <task>
tasks
pending
complete <id>
help
exit
```

The system is being extended to support deadline-aware commands and relative dates such as `tomorrow` and `next monday`.

---

## 6. Current User Workflow

The intended workflow is:

```text
User adds task
       ↓
JARVIS stores task permanently
       ↓
Task has optional deadline
       ↓
JARVIS checks due/overdue tasks
       ↓
User completes work
       ↓
User marks task completed
       ↓
Task status becomes Completed
```

Example target interaction:

```text
User: Add my DSA work due next Monday.

JARVIS:
Task added.
Deadline: next Monday
Status: Pending
```

Later:

```text
JARVIS: Reminder — DSA work is due today.
```

After completion:

```text
User: Complete task 1

JARVIS: Task #1 completed successfully.
```

---

## 7. Important Current Limitation

The current reminder implementation is a **check-based reminder system**. JARVIS can identify due or overdue tasks when the application is running/checking the database.

A true notification while the JARVIS application is completely closed requires a background process or operating-system scheduling/notification mechanism.

That future background notification layer can still be implemented using free/local technologies, subject to the computer being available or the operating system's scheduling capabilities.

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
- [x] Relative date support foundation
- [ ] Specific reminder time support
- [ ] Background notifications

### Phase 2 — Student Productivity

- [ ] Assignments module
- [ ] Notes module
- [ ] Schedule module
- [ ] Exam tracker
- [ ] Practical/lab tracker
- [ ] Daily agenda
- [ ] Weekly planning

### Phase 3 — Natural Language

- [ ] Natural-language task creation
- [ ] Date/time extraction
- [ ] Intent detection
- [ ] Context-aware commands
- [ ] Conversational task management

Example:

> "JARVIS, I have to submit my DSA assignment next Monday at 6 PM."

Expected interpretation:

```text
Task: Submit DSA assignment
Date: Next Monday
Time: 6:00 PM
Category: Assignment
Status: Pending
```

### Phase 4 — Voice Assistant

- [ ] Voice input
- [ ] Speech-to-text
- [ ] Text-to-speech
- [ ] Wake-word/activation workflow
- [ ] Hands-free task creation

### Phase 5 — AI Brain

Potential AI providers/models can be integrated behind a common JARVIS orchestration layer. The architecture should avoid making JARVIS permanently dependent on one provider.

Potential roles include:

- Reasoning
- Natural-language understanding
- Summarization
- Planning
- Document understanding
- Multimodal tasks

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

The next implementation sequence should be:

1. Test the current task/deadline implementation in Codespaces.
2. Add reliable date parsing for common natural-language dates.
3. Add explicit reminder time support.
4. Build a free background notification mechanism.
5. Add assignments as a dedicated student feature.
6. Add notes and persistent memory.
7. Add natural-language understanding.

---

## 10. Development Principle

JARVIS should be built as a modular system rather than one large script.

The architecture should remain:

```text
                    JARVIS
                       │
          ┌────────────┼────────────┐
          │            │            │
       Memory        AI Brain      Tools
          │            │            │
       SQLite       AI Model      Tasks
                                  Reminders
                                  Schedule
                                  Notes
                                  Assignments
```

This allows individual components to be improved without rebuilding the entire assistant.

---

## 11. Current Status Summary

**JARVIS is no longer only a concept.** The first working software foundation exists in the GitHub repository.

Current milestone:

> **JARVIS v0.3 — Persistent Student Task Manager with Deadlines and Relative-Date Support**

The immediate objective is to make reminders reliable, then expand JARVIS into a complete student productivity assistant before adding more advanced AI and voice capabilities.
