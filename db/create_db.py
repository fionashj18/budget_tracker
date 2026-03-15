import sqlite3
import os

# Path to database (project root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "budget.db")

# Connect to (or create) a database file
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Create your table (if it doesn't already exist)
cur.execute("""
    CREATE TABLE IF NOT EXISTS monthly_budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
        bank_balance REAL DEFAULT 0,
        income REAL DEFAULT 0,
        budget_needs REAL DEFAULT 0,
        budget_food REAL DEFAULT 0,
        budget_wants REAL DEFAULT 0,
        budget_travel REAL DEFAULT 0,
        budget_savings REAL DEFAULT 0,
        budget_investments REAL DEFAULT 0,
        spent_needs REAL DEFAULT 0,
        spent_food REAL DEFAULT 0,
        spent_wants REAL DEFAULT 0,
        spent_travel REAL DEFAULT 0,
        spent_savings REAL DEFAULT 0,
        spent_investments REAL DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now')),
        notes TEXT,
        UNIQUE(year, month)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        balance REAL DEFAULT 0,
        updated_at TEXT DEFAULT (datetime('now'))
    )
""")

con.commit()
con.close()

print(f"Database ready: {DB_PATH}")
