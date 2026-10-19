# Browser Finance Tracker — Product and Implementation Audit

Reviewed: 2026-10-20  
Scope: `site/index.html`, `site/assets/css/app.css`, `site/assets/js/app.js`, and the existing Python CLI test workflow.

## Product assessment

The core idea is sound as a **local-first personal money tracker**: manual income/expense/savings entry, current-month overview, category budgets, savings goals, CSV import/export, JSON backup/restore, and a personal khata ledger. It is inexpensive to host because the browser app is static and requires no server or API.

It should not be positioned as an encrypted vault, bank-grade financial system, or multi-device product. Browser storage is not encrypted at rest, records stay in the current browser profile, and clearing browser data can erase the local copy. Users need an explicit backup habit.

## Issues found and addressed in this branch

| Priority | Finding | Change |
|---|---|---|
| High | A rendering failure was reported as an IndexedDB-open failure, hiding the actual cause. | Separate database initialization from initial render; display the actual error and log it to the console. |
| High | Database upgrade blocking and stale connections were not handled. | Handle blocked open requests and close the connection on `versionchange`. |
| High | CSV and backup date checks accepted impossible ISO calendar dates. | Validate real calendar dates, not just the string shape. |
| High | CSV import wrote one row at a time and could leave a partial import. | Use one IndexedDB read/write transaction for all imported rows. |
| High | JSON restore validated and wrote records in the same loop, so a malformed later row could leave a partial restore. | Validate the complete payload before the transaction write and make transaction writes atomic. |
| High | The savings-rate figure was derived from unspent income rather than explicit savings transfers. | Define it as savings transfers divided by income and update the supporting label. |
| Medium | Monthly insight ignored savings transfers while the net cash-flow KPI included them. | Align the insight calculation with the KPI. |
| Medium | The interface said “Selected period” without providing a period selector. | Label the displayed period accurately as the current month. |
| Medium | Tabs lacked complete tab/tabpanel semantics and keyboard arrow navigation. | Add accessible relationships, selected state, focus management, and arrow/Home/End navigation. |
| Medium | Focus visibility, small touch controls, narrow layouts, and dark-mode button contrast needed improvement. | Add responsive styling, visible focus rings, larger targets, and explicit dark-mode button colors. |
| Medium | No PR validation workflow covered the static app. The old CLI tests also require pytest. | Add a dedicated pull-request workflow for JavaScript syntax, static references, and pytest. |

## Remaining limitations and release gates

1. **Browser E2E tests are still required.** Test in Firefox and Chromium at desktop and mobile widths, including transaction creation/editing/deletion, budgets, goals, khata payments, split allocations, CSV import/export, JSON restore, reload persistence, and dark mode.
2. **Cross-store restore is not a single atomic transaction.** Transactions live in IndexedDB while budgets, goals, and khata data live in localStorage. The backup is validated before writes, and transaction writes are atomic, but a storage/quota failure while updating localStorage can still leave a partially restored backup.
3. **No encryption at rest.** Anyone with access to the same unlocked browser profile may be able to inspect local records. Do not store bank credentials, full account numbers, or secrets.
4. **No multi-device sync or bank aggregation.** These are product-scope decisions, not bugs in the static deployment.
5. **Financial model scope is basic.** This is a tracker, not tax/accounting software or financial advice. Savings rate currently means explicit savings-transfer amount divided by recorded income; it does not infer unrecorded savings.
6. **Data recovery depends on exports.** Users should export JSON before restoring a backup or clearing browser data. The app cannot recover records already removed by the browser.

## Manual verification checklist

- [ ] Load the live site in a normal Firefox window and inspect Console for errors.
- [ ] Add income, expense, and savings-transfer records; reload and confirm they persist.
- [ ] Confirm savings rate equals savings transfers / income for the current month.
- [ ] Confirm monthly net cash flow subtracts expenses and savings transfers.
- [ ] Import CSV with valid rows, duplicates, quoted commas, and impossible dates; verify all-or-nothing writes.
- [ ] Export JSON; test a valid restore, a malformed row, and a malformed optional list.
- [ ] Test khata repayments and custom 2–3-person splits with exact-cent allocation.
- [ ] Navigate tabs using mouse, Tab, arrow keys, Home, and End.
- [ ] Test light/dark contrast, visible focus, 200% zoom, reduced-motion preference, and 320px viewport.
- [ ] Verify the PR workflow passes before merging and deploy the approved branch only after browser checks.

## Release recommendation

**Suitable for a private/local-first MVP after manual browser verification. Not yet ready to advertise as a security-focused or production-grade financial product.** Prioritize encrypted storage or a clearly scoped threat model, recovery UX, automated browser tests, and a documented restore contract before broader distribution.
