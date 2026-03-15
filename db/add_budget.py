"""
Add a new monthly budget record via CLI.
Uses parameterized queries (?) to avoid SQL injection.
"""

import sqlite3
import os
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "budget.db")


def _prompt_float(prompt: str, default: float = 0.0) -> float:
    """Ask for a float; use default if user presses Enter."""
    s = input(prompt).strip()
    if not s:
        return default
    try:
        return float(s)
    except ValueError:
        print("  Invalid number, using 0.")
        return default


def _prompt_int(prompt: str, default: Optional[int] = None) -> int:
    """Ask for an int; use default if provided and user presses Enter."""
    s = input(prompt).strip()
    if not s and default is not None:
        return default
    try:
        return int(s)
    except ValueError:
        raise ValueError(f"Invalid integer: {s!r}")


def add_monthly_budget() -> None:
    """
    Ask the user for each field and insert a new row into the monthly_budgets
    table using parameterized queries.
    """
    print("Enter monthly budget (press Enter for 0 where applicable):\n")

    year = _prompt_int("Year (e.g. 2025): ")
    month = _prompt_int("Month (1-12): ")
    if not (1 <= month <= 12):
        print("Month must be 1-12. Aborting.")
        return

    bank_balance = _prompt_float("Bank balance: ")
    income = _prompt_float("Income: ")

    print("\nBudget allocations:")
    budget_needs = _prompt_float("  Needs: ")
    budget_food = _prompt_float("  Food: ")
    budget_wants = _prompt_float("  Wants: ")
    budget_travel = _prompt_float("  Travel: ")
    budget_savings = _prompt_float("  Savings: ")
    budget_investments = _prompt_float("  Investments: ")

    print("\nSpent so far this month:")
    spent_needs = _prompt_float("  Needs: ")
    spent_food = _prompt_float("  Food: ")
    spent_wants = _prompt_float("  Wants: ")
    spent_travel = _prompt_float("  Travel: ")
    spent_savings = _prompt_float("  Savings: ")
    spent_investments = _prompt_float("  Investments: ")

    notes = input("\nNotes (optional): ").strip() or None

    # Parameterized query: ? placeholders; values passed as a tuple.
    # This prevents SQL injection—never concatenate user input into SQL.
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO monthly_budgets (
            year, month, bank_balance, income,
            budget_needs, budget_food, budget_wants, budget_travel,
            budget_savings, budget_investments,
            spent_needs, spent_food, spent_wants, spent_travel,
            spent_savings, spent_investments,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            year,
            month,
            bank_balance,
            income,
            budget_needs,
            budget_food,
            budget_wants,
            budget_travel,
            budget_savings,
            budget_investments,
            spent_needs,
            spent_food,
            spent_wants,
            spent_travel,
            spent_savings,
            spent_investments,
            notes,
        ),
    )
    row_id = cur.lastrowid
    con.commit()
    con.close()

    print(f"\nInserted row for {year}-{month:02d} (id={row_id}).")


if __name__ == "__main__":
    add_monthly_budget()
