# Finance Tracker replication map

## Scope
- Platform: browser-based web app, usable as a standalone local file.
- Audience: individual managing personal cash flow without linking bank accounts.
- Core loop: record transactions → understand monthly cash flow → set category limits and savings goals → export a backup.
- Reference products: Monarch Money (all-in-one overview), YNAB (intentional budgeting), Actual Budget (local-first/open-source budgeting), Quicken (broad finance feature set). Only public product pages and independent comparisons were consulted.

## Screen inventory

| ID | Screen | Entry | Purpose | Main components / states |
|---|---|---|---|---|
| S01 | Overview | Open app | Show current-month totals, recent records and category spending | KPI cards, recent transactions, category bars; empty/filled |
| S02 | Transactions | Transactions tab | Search, filter, inspect and delete records | Search, type filter, table; empty/matching/no-match |
| S03 | Add transaction | Overview form | Save an income, expense or savings transfer | Type, amount, category, date, description; validation/success |
| S04 | Budgets | Budgets tab | Set monthly category caps and compare spend | Budget form, progress bars, over-limit state |
| S05 | Savings goals | Goals tab | Track saved amount against target | Goal form, progress bars, optional target date |
| S06 | Backup | Header actions | Export CSV/JSON and restore a JSON backup | Download controls, file picker, validation/confirmation |

## Flows
- F01 Add and review: S01 → S03 → S01/S02. Validate positive amount and required category/date.
- F02 Investigate spending: S02 → search/type filter → delete with confirmation.
- F03 Budget: S04 → save category limit → compare current-month expense total.
- F04 Save toward target: S05 → create goal → review progress.
- F05 Backup and restore: S06 → export JSON → restore file with validation and confirmation.

## Data model
- Transaction: id, type (income|expense|savings), positive amount, category, date (YYYY-MM-DD), description, createdAt.
- Budget: category, positive monthly limit.
- Goal: id, name, positive target, non-negative saved amount, optional target date.
- Transactions are stored in IndexedDB. Budgets and goals are stored in localStorage. This split is a known limitation; backup combines all three.

## Feature matrix
See features.csv. The browser app is a fresh implementation of common patterns, not a copy of another product's code, assets or wording.

## Deliberate exclusions
Bank sync, multi-device sync, account login, automatic subscription detection, bills/alerts, investment valuation, encryption at rest, multi-currency conversion and financial advice are out of scope. These require additional infrastructure, security work or data providers.

## Next
Run the browser validation checklist in ../Docs/finance-manager-research.md. Do not describe the app as production-ready until restore/import and cross-browser tests have been run.
