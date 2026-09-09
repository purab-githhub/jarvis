from database import initialize_database
from duration_conflicts import print_duration_conflicts
from effort_planner import print_effort_plan
from planner_insights import print_planner_insights
from weekly_planner import print_weekly_plan


def run_planner():
    initialize_database()
    print("\n========== JARVIS PLANNER v0.21 ==========")
    print_weekly_plan()
    print_planner_insights()
    print_effort_plan()
    print_duration_conflicts()


if __name__ == "__main__":
    run_planner()
