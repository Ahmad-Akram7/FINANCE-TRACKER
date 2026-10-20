# Finance Tracker — Python CLI

The CLI records and reviews personal finances from a terminal. It uses a local SQLite database and is separate from the browser app.

## Install

Python 3.9 or newer is required.

```powershell
git clone https://github.com/Ahmad-Akram7/FINANCE-TRACKER.git
Set-Location FINANCE-TRACKER
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements_finance.txt
python -m pip install -e .
finance-tracker --help
```

On Linux/macOS, activate with `source .venv/bin/activate`.

## Common commands

```bash
finance-tracker add --type income --amount 3500 --category "Salary"
finance-tracker add --type expense --amount 55.40 --category "Groceries" --description "Weekly shop"
finance-tracker add --type savings --amount 500 --category "Emergency Fund"

finance-tracker list
finance-tracker list --type expense --category food --limit 20
finance-tracker search "monthly"

finance-tracker report --period month
finance-tracker breakdown --type expense
finance-tracker budget Groceries 400 --period month
finance-tracker export --output transactions.csv
finance-tracker visual-report --period month --output monthly_report.png

# Check the record ID before deleting
finance-tracker delete 42
```

Use `finance-tracker --help` and each command's `--help` as the source of truth for the installed version.

## Storage

The CLI uses SQLite at `~/.finance_tracker.db` by default. Set `FINANCE_DB_URL` to select another SQLAlchemy-compatible database URL. Protect and back up the database file.

The browser app stores data separately in IndexedDB/localStorage. There is no automatic sync between the interfaces.

## Tests

```powershell
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
```

Tests use an in-memory SQLite database and should not modify your personal CLI database.

## Data and security

This is a personal tracking tool, not financial, investment, tax, or accounting advice. Neither interface connects to a bank. Neither database is encrypted by this application; do not store passwords or full account numbers. Export a browser JSON backup before clearing site data or moving devices.

See [main README](README.md) and [product audit](Docs/PRODUCT_AUDIT.md).
