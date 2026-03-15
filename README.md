# Budget Tracker

A command-line app to track your monthly budget using SQLite. You can add records, view them (with filters and sorting), update amounts, and delete entries.

## Requirements

- Python 3 (uses the built-in `sqlite3` module — no pip install needed)

## Quick Start

From the project folder:

```bash
python3 main.py
```

The app creates the database and tables automatically on first run. Use the menu to create, view, update, or delete budget records.

## Menu Options

| Choice | Action |
|--------|--------|
| **1** | **Create** — Add a new monthly budget (year, month, income, budget amounts, spending, notes) |
| **2** | **Read** — View records. You can filter by year and sort by date (newest or oldest first) |
| **3** | **Update** — Edit one field of an existing record (e.g. change income or a spent amount) |
| **4** | **Delete** — Remove a record. You’ll be asked for the record id and to confirm |
| **5** | **Exit** — Quit the app |

## Database

- **File:** `budget.db` (created in the project root)
- **Main table:** `monthly_budgets` — one row per month, with:
  - `id` — unique row id (use this for Update and Delete)
  - `year`, `month`
  - `bank_balance`, `income`
  - Budget: `budget_needs`, `budget_food`, `budget_wants`, `budget_travel`, `budget_savings`, `budget_investments`
  - Spent: `spent_needs`, `spent_food`, `spent_wants`, `spent_travel`, `spent_savings`, `spent_investments`
  - `notes`, `created_at`, `updated_at`

To only (re)create the database and tables without running the menu:

```bash
python3 db/create_db.py
```

## Project Structure

```
budget_tracker/
├── main.py           # CLI menu and CRUD (run this)
├── budget.db         # SQLite database (created when you run the app)
├── schema.sql        # Table definitions (for reference)
└── db/
    ├── create_db.py  # Creates tables (init_db)
    └── add_budget.py # Create: prompt and INSERT logic
```

All database writes use **parameterized queries** (`?` placeholders) to avoid SQL injection.
