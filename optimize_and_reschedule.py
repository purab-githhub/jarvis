"""Interactive approval workflow for JARVIS workload redistribution.

The optimizer proposes safe moves. This module lets the student review each
proposal and explicitly approve it before changing a task or assignment date.
No move is applied without a clear 'y' confirmation.
"""

from database import initialize_database
from reschedule import reschedule_item
from workload_optimizer import get_redistribution_suggestions


def run_approval_workflow(target_date=None):
    """Show optimizer suggestions and apply only explicitly approved moves."""
    suggestions = get_redistribution_suggestions(target_date)

    print("\n========== JARVIS APPROVAL WORKFLOW ==========")
    if not suggestions:
        print("JARVIS: No safe redistribution suggestions are available.")
        return 0

    print("\nReview each proposed move. Nothing changes unless you enter 'y'.\n")
    applied = 0
    skipped = 0

    for index, suggestion in enumerate(suggestions, start=1):
        print(
            f"[{index}] {suggestion['kind']} #{suggestion['id']} "
            f"'{suggestion['title']}' (~{suggestion['minutes']} min)"
        )
        print(f"    Move: {suggestion['from_date']} -> {suggestion['to_date']}")
        answer = input("    Approve this move? [y/N]: ").strip().lower()

        if answer != "y":
            print("    JARVIS: Skipped.\n")
            skipped += 1
            continue

        success = reschedule_item(
            suggestion["kind"],
            suggestion["id"],
            suggestion["to_date"],
        )
        if success:
            print("    JARVIS: Move applied successfully.\n")
            applied += 1
        else:
            print("    JARVIS: Move could not be applied; no change was made.\n")
            skipped += 1

    print(
        f"JARVIS: Workflow complete — {applied} move(s) applied, "
        f"{skipped} skipped."
    )
    return 0


if __name__ == "__main__":
    initialize_database()
    raise SystemExit(run_approval_workflow())
