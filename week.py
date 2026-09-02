"""Convenience entry point for the JARVIS weekly planner.

This keeps weekly-planner execution available without changing the existing
interactive CLI until the main command loop can be safely updated.
"""

from database import initialize_database
from weekly_planner import print_weekly_plan


if __name__ == "__main__":
    initialize_database()
    print_weekly_plan()
