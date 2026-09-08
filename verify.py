"""JARVIS project verification utility.

Run this from the repository root with:
    python verify.py

It compiles all Python modules, initializes the database, and verifies that
all major JARVIS modules can be imported without executing the interactive CLI.
"""

import compileall
import importlib
import sys

from database import initialize_database

MODULES = [
    "database",
    "tasks",
    "assignments",
    "notes",
    "schedule",
    "recurring_schedule",
    "agenda",
    "weekly_planner",
    "planner_insights",
    "effort_planner",
    "duration_conflicts",
    "planner",
    "reminder_service",
]


def main():
    print("========== JARVIS PROJECT VERIFICATION ==========")

    print("\n[1/3] Compiling Python files...")
    compiled = compileall.compile_dir(".", quiet=1, maxlevels=2)
    if not compiled:
        print("FAIL: Python compilation failed.")
        return 1
    print("PASS: Python compilation completed successfully.")

    print("\n[2/3] Initializing database...")
    initialize_database()
    print("PASS: Database initialization completed.")

    print("\n[3/3] Importing JARVIS modules...")
    for module_name in MODULES:
        try:
            importlib.import_module(module_name)
            print(f"PASS: {module_name}")
        except Exception as exc:
            print(f"FAIL: {module_name} -> {exc}")
            return 1

    print("\n========== VERIFICATION PASSED ==========")
    print("JARVIS Python modules compile and import successfully.")
    print("Next: run 'python main.py' to use the interactive assistant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
