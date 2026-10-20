# Product research and scope notes

**Last reviewed:** 2026-10-20

## Product decision

Build a local-first, manual-entry finance tracker rather than connecting bank accounts or copying a proprietary app. The browser experience should be useful without an account, backend, paid API, or build step. The repository also maintains a separate Python CLI.

## Reference products

| Product | Publicly documented pattern | Fit / trade-off |
|---|---|---|
| [Monarch Money](https://www.monarch.com/) | Unified personal finance overview, budgets, reports, and goals | Broad reference; account syncing and paid-service assumptions are outside this scope |
| [YNAB](https://www.ynab.com/pricing) | Intentional category budgeting and goal planning | Useful budgeting ideas; Ledger does not implement the full YNAB method |
| [Actual Budget](https://actualbudget.org/) | Open-source, privacy-conscious budgeting | Closest philosophy for self-managed finance; richer budgeting and sync are not implemented |
| [Quicken](https://www.quicken.com/) | Broad desktop finance and reporting | Wider scope than this lightweight app |

Independent comparison context: [Forbes Advisor](https://www.forbes.com/advisor/banking/best-budgeting-apps/) and [NerdWallet](https://www.nerdwallet.com/finance/learn/best-budget-apps) discuss budgeting, categorization, reporting, and security. Product pages are first-party claims, not independent proof of product quality.

## Current browser scope

- Manual income, expense, and savings-transfer entry.
- Current-month totals, net cash flow, recorded savings rate, category spending, and six-month trend.
- Transaction search/filter and confirmed deletion.
- Category budgets and savings goals.
- Person-based khata entries, repayments, and custom 2–3-person splits.
- CSV transaction import/export.
- JSON backup/restore for transactions, budgets, goals, khata entries, people, and currency preference.
- Responsive light/dark UI.

## Data and boundaries

- Transactions use IndexedDB.
- Budgets, goals, khata entries, people, and preferences use localStorage.
- The Python CLI uses a separate SQLite database.
- No data syncs between the browser and CLI or between devices.
- Browser storage and plaintext JSON backups are not encrypted by this application.

Not included: bank aggregation, multi-device sync, login, automatic subscription detection, bill reminders, receipt OCR, investment valuation, encrypted storage, multi-currency conversion, or financial advice.

## Validation checklist

- [ ] Open `site/index.html` or serve the repository root with `python -m http.server 8000` and visit `/site/`.
- [ ] Add income, expense, and savings records; reload and verify persistence.
- [ ] Validate current-month totals, savings-rate definition, category spending, and budgets.
- [ ] Add/remove goals and test empty states.
- [ ] Record khata entries in both directions, repayments, and custom splits.
- [ ] Import CSV with quoted commas/newlines, duplicates, invalid rows, and impossible dates.
- [ ] Export and restore JSON; verify malformed backups are rejected.
- [ ] Test keyboard navigation, dark mode, small screens, and storage errors.
- [ ] Run `node --check site/assets/js/app.js` and `python -m pytest -q`.

## Sources

- https://www.monarch.com/
- https://www.ynab.com/pricing
- https://actualbudget.org/
- https://www.quicken.com/
- https://www.forbes.com/advisor/banking/best-budgeting-apps/
- https://www.nerdwallet.com/finance/learn/best-budget-apps/
