# Finance manager research and replication notes

Reviewed: 2026-10-19

## Decision

Build a local-first, manual-entry finance tracker inspired by established product patterns, rather than copying a proprietary app. The target is a useful, private personal money workflow that works without bank connections or paid services. The repository already contains a Python CLI; the new static browser app in `site/` is a standalone browser interface and does not replace that CLI.

## Products reviewed

| Product | Strongest pattern | Trade-off / fit for this project |
|---|---|---|
| [Monarch Money](https://www.monarch.com/) | Unified net-worth, transaction, flexible budget, recurring-charge, reports and goals experience | Broad all-in-one reference; paid service and account syncing are outside this local-only first slice |
| [YNAB](https://www.ynab.com/)/[pricing](https://www.ynab.com/pricing) | Assign money intentionally, category budgets, savings goals and debt planning | Strong methodology, subscription; the app implements tracking and limits, not the full YNAB method |
| [Actual Budget](https://actualbudget.org/) | Open-source, privacy-conscious, envelope/zero-based budgeting | Closest philosophy for a private self-managed tool; richer budgeting and sync are not replicated here |
| [Quicken](https://www.quicken.com/) | Broad desktop finance, bills and investment management | Much wider scope than this lightweight browser app |

Independent comparison context: [Forbes Advisor's 2026 budgeting-app methodology](https://www.forbes.com/advisor/banking/best-budgeting-apps/) compares 24 apps using cost, budgeting, additional features, reporting/analytics and security. [NerdWallet's 2026 guide](https://www.nerdwallet.com/finance/learn/best-budget-apps) highlights transaction categorization, forward planning and bill reminders. Product pages are first-party claims; this note does not treat marketing copy as independent proof of quality.

## Scope and user flow

Core flow: open the page → add income/expense/savings record → review current-month totals and category spend → set category budget or savings goal → export a backup.

Included in this slice:
- Manual transaction entry with amount, category, date and note.
- Monthly income, expense, net cash-flow and savings-rate summary.
- Search and type filtering; delete confirmation.
- Category spend bars, monthly category budgets and savings goals.
- CSV transaction export; JSON backup/restore for transactions, budgets and goals.
- Browser-local persistence: IndexedDB for transactions, localStorage for budgets/goals/preferences.

Not included: bank aggregation, automatic subscription detection, multi-device sync, user accounts, financial advice, investments valuation, bill reminders, receipt OCR, encryption at rest, or multi-currency conversion. Browser storage is not a substitute for an encrypted vault; use a trusted device profile and export backups. Avoid storing bank credentials or account numbers.

## Implementation notes

This is a clean-room implementation of common finance workflows. It does not use another product's source, assets, or copied interface text. Existing Python CLI files are retained. The deployable browser app lives in `site/`; its CSS and JavaScript are separate files under `site/assets/`.

## Validation checklist

- [ ] Open `app.html` in a current browser.
- [ ] Add one income, expense and savings record; reload and confirm records persist.
- [ ] Confirm month summary and category totals using known amounts.
- [ ] Add and remove a budget and savings goal.
- [ ] Export CSV and JSON; restore JSON into a fresh browser profile.
- [ ] Verify invalid JSON and malformed transaction values are rejected.
- [ ] Test keyboard navigation and narrow viewport layout.
- [ ] Run the existing Python test suite separately; the browser app is not covered by it yet.

## Sources

- Monarch product overview: https://www.monarch.com/
- YNAB pricing and feature overview: https://www.ynab.com/pricing
- Actual Budget project: https://actualbudget.org/
- Quicken product overview: https://www.quicken.com/
- Forbes Advisor, Best Budgeting Apps: https://www.forbes.com/advisor/banking/best-budgeting-apps/
- NerdWallet, Best Budget Apps: https://www.nerdwallet.com/finance/learn/best-budget-apps
