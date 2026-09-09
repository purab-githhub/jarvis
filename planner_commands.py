"""Small command-layer helpers for exposing planner features from JARVIS CLI."""

from duration_conflicts import print_duration_conflicts
from effort_planner import print_effort_plan
from planner_insights import print_planner_insights
from weekly_planner import print_weekly_plan


def run_week_command():
    """Print the Monday-Sunday planner."""
    print_weekly_plan()


def run_insights_command():
    """Print explainable planner priorities and conflicts."""
    print_planner_insights()


def run_effort_command():
    """Print estimated workload and capacity warnings."""
    print_effort_plan()


def run_conflicts_command():
    """Print duration-aware schedule conflicts."""
    print_duration_conflicts()


def run_planner_command():
    """Print the complete planning analysis in one place."""
    print("\n========== JARVIS PLANNER v0.21 ==========")
    run_week_command()
    run_insights_command()
    run_effort_command()
    run_conflicts_command()
