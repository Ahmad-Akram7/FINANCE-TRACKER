# Finance Tracker audit — 2026-10-20

## Product assessment

Ledger is a useful local-first personal finance tracker: it avoids account creation and bank connections, supports transaction tracking, budgets, goals, CSV workflows, JSON backups, and a personal khata ledger. The strongest product promise is privacy by locality and a low-friction manual workflow.

It should be described as a **personal tracking tool**, not a bank-grade financial system. Browser storage is not encrypted at rest and does not sync across devices. Users can lose their only copy if they clear site data, use another browser profile, or lose the device. Keep that limitation visible.

## Issues addressed in this branch

- **Dashboard render could fail on malformed local settings.** Budget, goal, khata, and people lists now validate both their array shape and basic record structure. The dashboard can still render while displaying a warning, and relevant edits/backup export stop instead of overwriting unreadable data. Category aggregation uses prototype-safe objects.
- **Backup export could silently produce an incomplete or fail with an unhandled JSON parse error.** Export now validates budget and goal settings and presents a clear failure message if either list cannot be read.
- **Expense summary had a misleading “Selected period” label despite no period selector.** It now says “Current month,” matching the actual calculation.
- **Savings rate could imply a valid 0% when income was zero.** It now shows an em dash until there is income to use as the denominator.
- **Legacy/imported savings goals without a saved amount could produce `NaN` progress.** Progress rendering now normalizes the missing amount to zero.
- **Dark-mode primary button contrast was weak.** Standard primary actions now use dark text on the light-green dark-mode primary surface; special tabs, person selectors, secondary buttons, and destructive buttons keep their semantic styling.
- **Visual hierarchy was inconsistent.** Added a restrained responsive visual system, clearer heading hierarchy, softer panel surfaces, stronger focus states, and responsive refinements without adding dependencies.
- **Privacy/backup documentation was incomplete.** README now documents local storage boundaries and the actual JSON backup contents, including khata data and currency preference.

## Remaining product risks / next priorities

1. **No encryption at rest.** Browser-profile access means anyone with access to the unlocked device/profile may access records. If the product is marketed as a privacy tool, document this clearly; optional client-side encrypted exports/vault protection would be a separate feature.
2. **No cross-device sync or recovery service.** This is a deliberate trade-off, but onboarding should explain it and encourage backups before importing/restoring or clearing browser data.
3. **Financial semantics need explicit wording.** “Savings rate” currently means savings transfers divided by income, not a standardized personal-finance metric. Keep that definition visible and handle values above 100% intentionally if desired.
4. **Manual browser testing is still required.** Validate IndexedDB in Firefox normal/private windows, multiple tabs, quota/storage denial, CSV import with quoted commas/newlines and duplicate rows, JSON restore, dark-mode contrast, keyboard-only navigation, and mobile layouts.
5. **No automated browser end-to-end tests yet.** The existing workflow syntax-checks JavaScript, but does not simulate storage failures, validate calculations, or exercise the UI.
6. **No authentication is not equivalent to encryption.** Do not store credentials, complete account numbers, or other highly sensitive identifiers.
7. **Data integrity across stores.** Transactions use IndexedDB while budgets/goals/khata use localStorage. A JSON restore spans separate storage systems and is not atomic; keep the confirmation and backup-before-restore guidance.
8. **Financial calculations require regression tests.** Add unit tests for monthly totals, savings-rate semantics, net cash flow, khata direction/repayments, split rounding, and import validation before calling the app production-grade.

## Verification performed for this change

- Reviewed current HTML, CSS, JavaScript storage/backup flows, README, and deployment workflow.
- JavaScript syntax must be checked with `node --check site/assets/js/app.js` in CI after the branch is pushed.
- This remote edit has not been exercised in a real browser in this task. Do not describe it as a complete WCAG certification or an end-to-end verified release.
