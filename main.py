"""
Budget Tracker CLI — full CRUD for monthly_budgets.
Run: python main.py
"""

import sqlite3
from typing import Optional

from db.create_db import DB_PATH, init_db
from db.add_budget import add_monthly_budget


def _prompt_int(prompt: str, default: Optional[int] = None) -> Optional[int]:
    s = input(prompt).strip()
    if not s:
        return default
    try:
        return int(s)
    except ValueError:
        return None


def _prompt_float(prompt: str, default: Optional[float] = None) -> Optional[float]:
    s = input(prompt).strip()
    if not s:
        return default
    try:
        return float(s)
    except ValueError:
        return None


# ---------- Read ----------
def list_budgets(filter_year: Optional[int] = None, sort_newest_first: bool = True):
    """
    Read records from monthly_budgets.
    Filter by year (optional) and sort by date (newest or oldest first).
    """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Parameterized: filter by year if provided
    if filter_year is not None:
        cur.execute(
            """
            SELECT id, year, month, bank_balance, income,
                   budget_needs, budget_food, budget_wants, budget_travel,
                   budget_savings, budget_investments,
                   spent_needs, spent_food, spent_wants, spent_travel,
                   spent_savings, spent_investments, notes
            FROM monthly_budgets
            WHERE year = ?
            ORDER BY year DESC, month DESC
            """,
            (filter_year,),
        )
    else:
        cur.execute(
            """
            SELECT id, year, month, bank_balance, income,
                   budget_needs, budget_food, budget_wants, budget_travel,
                   budget_savings, budget_investments,
                   spent_needs, spent_food, spent_wants, spent_travel,
                   spent_savings, spent_investments, notes
            FROM monthly_budgets
            ORDER BY year DESC, month DESC
            """
        )

    rows = cur.fetchall()
    con.close()

    if sort_newest_first:
        # already newest first from ORDER BY
        pass
    else:
        rows = list(reversed(rows))

    return rows


def do_read():
    """Interactive Read: ask for filter/sort, then display records."""
    print("\n--- View monthly budgets ---")
    year_str = input("Filter by year (leave blank for all): ").strip()
    filter_year = int(year_str) if year_str else None

    sort_str = input("Sort by date: 1 = newest first, 2 = oldest first [1]: ").strip() or "1"
    sort_newest_first = sort_str != "2"

    rows = list_budgets(filter_year=filter_year, sort_newest_first=sort_newest_first)
    if not rows:
        print("No records found.")
        return

    for r in rows:
        total_budget = (
            (r["budget_needs"] or 0)
            + (r["budget_food"] or 0)
            + (r["budget_wants"] or 0)
            + (r["budget_travel"] or 0)
            + (r["budget_savings"] or 0)
            + (r["budget_investments"] or 0)
        )
        total_spent = (
            (r["spent_needs"] or 0)
            + (r["spent_food"] or 0)
            + (r["spent_wants"] or 0)
            + (r["spent_travel"] or 0)
            + (r["spent_savings"] or 0)
            + (r["spent_investments"] or 0)
        )
        print(f"\n  id={r['id']}  {r['year']}-{r['month']:02d}  "
              f"income={r['income']}  bank={r['bank_balance']}  "
              f"budget total={total_budget}  spent={total_spent}")
        if r["notes"]:
            print(f"      notes: {r['notes']}")
    print()


# ---------- Update ----------
# Editable columns (excluding id, created_at)
UPDATEABLE_COLUMNS = [
    "bank_balance", "income",
    "budget_needs", "budget_food", "budget_wants", "budget_travel",
    "budget_savings", "budget_investments",
    "spent_needs", "spent_food", "spent_wants", "spent_travel",
    "spent_savings", "spent_investments",
    "notes",
]


def do_update():
    """Interactive Update: pick record by id, then choose field and new value."""
    print("\n--- Update a monthly budget ---")
    row_id = _prompt_int("Record id to update: ")
    if row_id is None:
        print("Invalid id.")
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, year, month FROM monthly_budgets WHERE id = ?", (row_id,))
    row = cur.fetchone()
    if not row:
        print(f"No record with id={row_id}.")
        con.close()
        return

    print(f"Editing {row[1]}-{row[2]:02d} (id={row_id}).")
    print("Fields:", ", ".join(UPDATEABLE_COLUMNS))
    field = input("Field to update: ").strip().lower()
    if field not in UPDATEABLE_COLUMNS:
        print("Unknown field.")
        con.close()
        return

    if field == "notes":
        new_val = input("New value (text): ").strip() or None
    else:
        val_str = input("New value (number): ").strip()
        if not val_str:
            print("No change.")
            con.close()
            return
        try:
            new_val = float(val_str)
        except ValueError:
            print("Invalid number.")
            con.close()
            return

    # Parameterized UPDATE
    cur.execute(
        "UPDATE monthly_budgets SET updated_at = datetime('now'), " + field + " = ? WHERE id = ?",
        (new_val, row_id),
    )
    con.commit()
    con.close()
    print(f"Updated {field} for id={row_id}.")


# ---------- Delete ----------
def do_delete():
    """Interactive Delete: pick record by id, confirm, then remove."""
    print("\n--- Delete a monthly budget ---")
    row_id = _prompt_int("Record id to delete: ")
    if row_id is None:
        print("Invalid id.")
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, year, month FROM monthly_budgets WHERE id = ?", (row_id,))
    row = cur.fetchone()
    if not row:
        print(f"No record with id={row_id}.")
        con.close()
        return

    confirm = input(f"Delete {row[1]}-{row[2]:02d} (id={row_id})? [y/N]: ").strip().lower()
    if confirm != "y" and confirm != "yes":
        print("Cancelled.")
        con.close()
        return

    cur.execute("DELETE FROM monthly_budgets WHERE id = ?", (row_id,))
    con.commit()
    con.close()
    print("Deleted.")


# ---------- Menu ----------
def main():
    init_db()
    while True:
        print("\n=== Budget Tracker ===")
        print("1. Create — Add a new monthly budget")
        print("2. Read   — View records (filter by year, sort by date)")
        print("3. Update — Edit an existing record")
        print("4. Delete — Remove a record")
        print("5. Exit")
        choice = input("Choice [1-5]: ").strip() or "5"

        if choice == "1":
            add_monthly_budget()
        elif choice == "2":
            do_read()
        elif choice == "3":
            do_update()
        elif choice == "4":
            do_delete()
        elif choice == "5":
            print("Bye.")
            break
        else:
            print("Enter 1–5.")


if __name__ == "__main__":
    main()
