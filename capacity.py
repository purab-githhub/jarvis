import sys

from database import initialize_database
from settings import DEFAULT_DAILY_CAPACITY_MINUTES, get_daily_capacity, set_daily_capacity


def print_capacity():
    minutes = get_daily_capacity()
    hours = minutes / 60
    print("\n========== JARVIS DAILY CAPACITY ==========")
    print(f"Current capacity: {minutes} min ({hours:.1f} hr/day)")
    print(f"Default capacity: {DEFAULT_DAILY_CAPACITY_MINUTES} min (4.0 hr/day)")
    print("To change it: python capacity.py <minutes>")
    print()


def main():
    initialize_database()

    if len(sys.argv) == 1:
        print_capacity()
        return

    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("JARVIS: Use python capacity.py <positive_minutes>.")
        return

    minutes = int(sys.argv[1])
    if minutes <= 0:
        print("JARVIS: Capacity must be greater than 0 minutes.")
        return

    set_daily_capacity(minutes)
    print(f"JARVIS: Daily planning capacity saved as {minutes} min ({minutes / 60:.1f} hr/day).")


if __name__ == "__main__":
    main()
