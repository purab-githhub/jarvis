# JARVIS

A modular, extensible personal AI assistant inspired by JARVIS.

## Current project

JARVIS is currently being built as a free-first personal student assistant. It includes persistent task, assignment, notes, scheduling, reminders, and workload-planning foundations.

## Quick start in GitHub Codespaces

Pull the latest repository changes:

```bash
git pull origin main
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Verify/compile the project:

```bash
python verify.py
```

Run the interactive assistant:

```bash
python main.py
```

Run the unified planner:

```bash
python planner.py
```

Run the standalone weekly planner:

```bash
python week.py
```

Run planner insights:

```bash
python insights.py
```

Run effort analysis:

```bash
python effort.py
```

View or change your daily planning capacity:

```bash
python capacity.py
python capacity.py 300
```

Run duration-aware conflict detection:

```bash
python duration_conflicts.py
```

Preview safe workload redistribution recommendations:

```bash
python optimize.py
```

Run the approval workflow for recommended moves:

```bash
python optimize_and_reschedule.py
```

The approval workflow shows each proposed move and asks for explicit `y` confirmation. Only approved pending tasks or assignments are rescheduled, and their existing due times are preserved. The optimizer itself never changes data automatically.

For a direct, one-item move without the recommendation workflow:

```bash
python reschedule.py task 3 2026-09-15
python reschedule.py assignment 2 2026-09-16
```

These commands change only the selected pending item's due date and preserve its existing due time.

Run the reminder service:

```bash
python reminder_service.py
```

## Project verification

`verify.py` compiles the Python source, initializes the SQLite database, and imports the major JARVIS modules without starting the interactive command loop. It covers the settings, optimizer, command bridge, explicit rescheduling, and approval workflow modules.

GitHub Actions also runs the same verification automatically on pushes and pull requests targeting `main`.

## Current capabilities

- Persistent tasks and assignments
- Deadlines and reminder times
- Relative-date support
- Notes and keyword search
- One-time and recurring schedules
- Daily and weekly planning
- Priority and conflict analysis
- Effort estimation and user-entered duration overrides
- Persistent user-configurable daily planning capacity
- Duration-aware scheduling conflict detection
- Recommendation-only workload redistribution across lighter days
- Explicit approval-based rescheduling for pending tasks and assignments
- Interactive approval workflow for optimizer recommendations
- Desktop reminder-service foundation

See [`JARVIS_DEVELOPMENT_REPORT.md`](JARVIS_DEVELOPMENT_REPORT.md) for the complete development history and roadmap.
