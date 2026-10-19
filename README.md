# Finance Tracker

A private, local-first personal finance toolkit. It includes a browser-based tracker for everyday use and a Python command-line interface for terminal workflows.

## Browser tracker

Open [app.html](app.html) in a current browser. No build step, account, server, bank connection, or third-party JavaScript dependency is required.

Features:
- Record income, expenses and savings transfers.
- Review current-month income, expenses, net cash flow and savings rate.
- Search and filter transactions; delete with confirmation.
- See expense totals by category and track monthly category budgets.
- Set savings goals and track progress.
- Export transactions as CSV and export/restore a JSON backup.

Transactions use IndexedDB. Budgets and goals use browser local storage. The data remains in that browser profile; it does not sync to another device. Browser storage can be cleared or lost, so export backups regularly. This is not an encrypted password vault and should not hold bank credentials or full account numbers.

The currency defaults to PKR. Display formatting follows the browser's locale; this is a display setting, not currency conversion.

## Python CLI

The existing Python CLI is retained. See [FINANCE_README.md](FINANCE_README.md) for its commands and setup. It uses a local SQLite database by default.

## Research and design

The product comparison, scope decisions and validation checklist are in [Docs/finance-manager-research.md](Docs/finance-manager-research.md). The replica flow map and feature matrix are in [replica/](replica/).

## Quick start

For the browser app, open app.html.

For the CLI, create a virtual environment, install the project dependencies, then run the installed finance-tracker command. Follow the current CLI documentation for the exact installation path.

## License

See [LICENSE](LICENSE).
