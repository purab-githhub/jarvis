"""Standalone entry point for JARVIS workload redistribution recommendations."""

from database import initialize_database
from workload_optimizer import print_redistribution_plan


if __name__ == "__main__":
    initialize_database()
    print_redistribution_plan()
