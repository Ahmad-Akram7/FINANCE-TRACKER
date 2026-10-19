# Finance Tracker — Product and Implementation Audit

Reviewed: 2026-10-20  
Scope: static browser app, Python CLI packaging, and automated checks.

## Product assessment

The core idea is useful as a **local-first personal finance tracker**: manual income/expense/savings entry, monthly overview, category budgets, savings goals, CSV import/export, JSON backup/restore, and a personal khata ledger. The static browser app is inexpensive to host and requires no server, bank integration, or account.

Do not position it as an encrypted vault or bank-grade financial system. Browser storage is not encrypted at rest, data stays in the current browser profile, and clearing browser data can erase the local copy. Users need regular backups.

## Issues addressed on this branch

| Priority | Finding | Change |
|---|---|---|
| High | Python CLI and tests imported `finance_tracker.*`, but the repository only contained root-level modules. The package was missing, so test collection failed and the declared CLI entry point could not install correctly. | Add the installable `finance_tracker` package, interface modules, package version, and root-level compatibility shims. |
| High | A render failure could be reported as a database-open failure, obscuring the cause of the browser storage warning. | Separate IndexedDB initialization from the initial render and display actionable technical detail. |
| High | CSV import and backup restore could fail after writing only some transactions. | Validate import data before writes and use one IndexedDB read/write transaction for transaction records. |
| High | Savings rate was calculated from income left after expenses rather than recorded savings transfers. | Define savings rate as explicit savings transfers divided by income and clarify the label. |
| Medium | Monthly insight ignored savings transfers while the net cash-flow KPI subtracted them. | Align insight calculations and empty-state messaging with the KPI. |
| Medium | Budget spending could fail to match a budget if the category's capitalization differed. | Match normalized category names. |
| Medium | Impossible dates could pass simple ISO date-shape checks. | Validate actual calendar dates. |
| Medium | Tabs lacked complete keyboard navigation and accessible selected-state behavior. | Add semantic tab/tabpanel relationships and arrow/Home/End navigation. |
| Medium | Responsive layouts, focus indicators, dark-mode contrast, and reduced-motion behavior needed attention. | Improve touch targets, focus states, responsive styling, and theme contrast. |
| Medium | The repository had no dedicated pull-request check for the browser app, and existing CLI tests required project dependencies. | Add CI that checks JS syntax, validates key static files, installs the package, and runs pytest. |

## Remaining limitations / release gates

1. **Browser E2E tests remain necessary.** Test Firefox and Chromium at desktop and mobile widths: transaction create/delete, budgets, goals, khata repayments, custom splits, CSV import/export, JSON restore, reload persistence, and dark mode.
2. **Backup restore is not atomic across storage engines.** Transactions are in IndexedDB; budgets, goals, and khata data are in localStorage. Transaction writes are atomic, but a quota failure while updating localStorage can still leave a partially restored backup.
3. **No encryption at rest.** Anyone with access to the same unlocked browser profile may be able to inspect records. Do not store bank credentials or full account numbers.
4. **No bank aggregation or multi-device sync.** These are excluded from the current static-app scope.
5. **Savings rate definition is explicit.** It means recorded savings transfers divided by recorded income; the app does not infer savings that the user has not entered.
6. **Python CLI and browser data are separate.** The CLI's SQLite database and browser IndexedDB/localStorage do not sync with each other.

## Manual verification checklist

- [ ] Confirm the pull-request CI passes, including editable installation and pytest.
- [ ] Load the browser app in normal Firefox and inspect Console for errors.
- [ ] Add income, expense, and savings-transfer records; reload and verify persistence.
- [ ] Verify savings rate equals savings transfers / income for the current month.
- [ ] Verify net cash flow subtracts expenses and savings transfers.
- [ ] Import valid CSV rows, duplicates, quoted commas, and impossible dates; confirm atomic writes.
- [ ] Export JSON; test valid restore and malformed transaction/list data.
- [ ] Test khata payments and custom 2–3-person splits to the cent.
- [ ] Navigate tabs with mouse, Tab, arrow keys, Home, and End.
- [ ] Check 200% zoom, a 320px viewport, visible focus, dark mode, and reduced motion.
- [ ] Verify package installation and CLI help after installing from the repository.

## Release recommendation

**Reasonable for a private/local-first MVP after manual browser verification. Not ready to advertise as a security-focused or production-grade financial product.** Before wider distribution, prioritize browser E2E tests, clearer cross-store backup recovery, and a documented privacy/threat model.
