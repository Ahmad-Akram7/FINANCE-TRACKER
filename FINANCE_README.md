# Finance Tracker: Python CLI guide

The Python command-line interface records income, expenses and savings in a local SQLite database. Use it when you prefer terminal workflows, scripted exports or reports.

For a browser interface with budgets, savings goals and local CSV/JSON backup, open [browser app](site/index.html). The browser app and CLI keep separate data stores; they do not sync.

## Install

```bash
git clone https://github.com/Ahmad-Akram7/FINANCE-TRACKER.git
cd FINANCE-TRACKER
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements_finance.txt
pip install -e .
finance-tracker --help
```

If the editable install does not expose the command, inspect setup.py and the installed entry points before changing the environment.

## Common commands

Add income, expenses or a savings transfer:

```bash
finance-tracker add --type income --amount 3500 --category "Salary"
finance-tracker add --type expense --amount 55.40 --category "Groceries" --description "Weekly shop"
finance-tracker add --type savings --amount 500 --category "Emergency Fund"
```

List and filter transactions:

```bash
finance-tracker list
finance-tracker list --type expense --category food --limit 20
finance-tracker search "monthly"
```

Review totals and category spending:

```bash
finance-tracker report --period month
finance-tracker breakdown --type expense
finance-tracker budget Groceries 400 --period month
```

Create a chart report or export transactions:

```bash
finance-tracker visual-report --period month --output monthly_report.png
finance-tracker export --output transactions.csv
```

Delete a transaction by its ID after checking the displayed record:

```bash
finance-tracker delete 42
```

Use `finance-tracker --help` and each command's `--help` output as the source of truth for the installed version.

## Local database

The CLI uses SQLite by default, stored at `~/.finance_tracker.db`. Set `FINANCE_DB_URL` to choose another SQLAlchemy-compatible database URL. Keep the database file private and make regular backups.

## Tests

Install the test dependencies and run the suite:

```bash
pip install pytest pytest-cov
pytest -v
```

The project includes tests for transaction validation, CRUD operations, summaries, category totals and search. Run them after changing core calculations or persistence.

## Data and security

- The CLI stores data locally by default. Protect your operating-system account and database file.
- The browser app stores transactions in IndexedDB and budgets/goals in localStorage. Browser data may be cleared and does not sync between devices.
- Export backups before changing devices or clearing browser data.
- Neither interface connects to banks or provides investment, tax or financial advice.

## Project notes

The product research and scope decisions are documented in [Docs/finance-manager-research.md](Docs/finance-manager-research.md). The browser screen map and feature checklist live in [replication map](Docs/replica-map.md) and [feature matrix](Docs/feature-matrix.csv).

## License

See [LICENSE](LICENSE).
