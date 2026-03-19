💰 Finance Tracker
A production-grade personal finance CLI — built with Python, SQLAlchemy, Click & Rich.
      
🌐 Live Docs · 📋 Report Bug · 🤝 Contributing

Overview
Finance Tracker is a terminal-first personal finance manager. Track income, expenses, and savings with validated inputs, rich formatted output, visual PNG reports, and a clean modular codebase you can actually extend.
No cloud. No subscriptions. Your data stays on your machine.

✨ What's New in v2.0
    • breakdown command — Category-level spending breakdown with inline bar chart
    • search command — Full-text search across category and description
    • budget command — Set spending limits and get real-time progress bars
    • export command — Dump all transactions to CSV
    • 4-panel visual report — Summary, metrics, donut chart, and top-category bar
    • Savings rate — Calculated automatically in every report
    • Timestamped results — --period today|week|month|year|all on all commands
    • Pydantic v2 migration — Faster validation, cleaner errors

🚀 Quick Start
# 1. Clone
git clone https://github.com/Ahmad-Akram7/FINANCE-TRACKER.git
cd FINANCE-TRACKER

# 2. Virtual environment
python3 -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt
pip install -e .

# 4. Initialise DB and go
finance-tracker init
finance-tracker --help

📖 Commands
add — Record a transaction
# Income
finance-tracker add --type income --amount 3500 --category "Monthly Salary"

# Expense with note
finance-tracker add --type expense --amount 55.40 --category "Groceries" --description "Weekly shop"

# Savings
finance-tracker add --type savings --amount 500 --category "Emergency Fund"
list — Browse transactions
# All transactions (most recent first)
finance-tracker list

# Filter by type and category, limit rows
finance-tracker list --type expense --category food --limit 20
report — Financial summary
finance-tracker report                  # All time
finance-tracker report --period month   # This month
finance-tracker report --period week    # Last 7 days
Simulated output:
  ╔══════════════════════════════════════════════════════╗
  ║        📊  Financial Summary  ·  Month               ║
  ╠══════════════════════════════════════════════════════╣
  ║  Total Income                          $3,500.00     ║
  ║  Total Expenses                          $240.00     ║
  ║  Total Savings                           $500.00     ║
  ║  ────────────────────────────────────────────────    ║
  ║  Net  (Income − Expenses)              $3,260.00     ║
  ║  Savings Rate                             14.3%      ║
  ╚══════════════════════════════════════════════════════╝
breakdown — Category breakdown
finance-tracker breakdown --type expense   # defaults to expense
finance-tracker breakdown --type income
search — Find transactions
finance-tracker search amazon
finance-tracker search "monthly"
budget — Check spending against a limit
finance-tracker budget Groceries 400 --period month
# Output: ████████░░░░░░░░░░░░  57.5%
#         Spent $230.00  /  Budget $400.00
#   ✓  $170.00 remaining this month.
visual-report — PNG chart
finance-tracker visual-report
finance-tracker visual-report --output monthly_report.png --period month
Generates a 4-panel chart: summary bars, key metrics, expense donut, top category bar.
export — CSV export
finance-tracker export
finance-tracker export --output my_finances_2025.csv
delete — Remove a transaction
finance-tracker delete 42   # prompts for confirmation

🗂️ Project Structure
FINANCE-TRACKER/
├── finance_tracker/
│   ├── models/         # SQLAlchemy ORM + Pydantic v2 schemas
│   ├── database/       # Engine, session factory, init_db()
│   ├── core/           # Business logic (CRUD, summary, search, budget)
│   └── interfaces/
│       ├── cli.py      # Click commands
│       └── display.py  # Rich display helpers
├── tests/
│   └── test_core.py    # pytest unit + integration tests
├── docs/               # GitHub Pages site
├── requirements.txt
├── setup.py
└── CONTRIBUTING.md
The core layer has zero UI dependencies — you can layer a FastAPI backend or Django admin on top without touching any business logic.

🏗️ Architecture
┌─────────────────────┐
│   interfaces/cli.py │  ← Click commands, argument parsing
│   interfaces/       │
│   display.py        │  ← Rich tables, panels, colours
└────────┬────────────┘
         │ calls
┌────────▼────────────┐
│     core/           │  ← Pure business logic, no UI
│  add, list, delete  │
│  summary, breakdown │
│  search, budget     │
└────────┬────────────┘
         │ uses
┌────────▼────────────┐
│    database/        │  ← Engine, SessionLocal, get_session()
└────────┬────────────┘
         │ maps to
┌────────▼────────────┐
│     models/         │  ← Transaction ORM, Pydantic schemas
└─────────────────────┘

🧪 Running Tests
pip install pytest pytest-cov
pytest tests/ -v --cov=finance_tracker
The test suite uses an in-memory SQLite database — no disk I/O, no cleanup required.

⚙️ Configuration
Env var	Default	Description
FINANCE_DB_URL	~/.finance_tracker.db	SQLAlchemy database URL

Example — use a custom path:
export FINANCE_DB_URL="sqlite:///~/Documents/my_finances.db"

🤝 Contributing
Contributions welcome! See CONTRIBUTING.md for guidelines.
git checkout -b feature/your-feature
# make changes
pytest tests/ -v
git commit -m "feat: your change"
Ideas: recurring transactions, multi-currency support, TUI dashboard, FastAPI backend.

📄 License
MIT License — see LICENSE.

Built by Ahmad Akram · LinkedIn · Fiverr
⭐ Star the repo if it's useful!
