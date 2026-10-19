# Finance Tracker usability and reliability audit

**Scope:** static browser app under `site/` (HTML, CSS, JavaScript). This is a code review and static validation, not a full browser/assistive-technology certification.

## Findings addressed in this change

| Severity | Finding | Change |
|---|---|---|
| High | IndexedDB startup errors were swallowed behind a generic banner, so users could not distinguish a blocked database from a browser/storage error. | Preserve the actual error name/message in an accessible alert; handle blocked opens and close the connection on version changes. The original runtime cause still needs confirmation in a deployed browser. |
| High | CSV import and JSON restore wrote transactions one at a time, so a mid-import failure could leave a partial transaction set. | Add a single read-write IndexedDB transaction for bulk writes; CSV imports and restored transaction records now commit together or abort together. |
| High | JSON backup validation happened while writing, allowing earlier transactions to be written before a later invalid row was found. | Validate transaction dates, amounts, types and required fields before writing; validate optional budgets, goals, khata entries, people, and currency values before restore. |
| Medium | Dates generated through UTC ISO strings could show the previous/next day relative to the user's local date. | Generate current dates from local calendar fields and validate calendar dates instead of accepting impossible dates such as 30 February. |
| Medium | CSV date parsing could accept impossible dates and used UTC conversion for fallback date strings. | Validate ISO and day/month/year dates and keep fallback parsing in local calendar time. |
| Medium | Currency codes restored from JSON were not constrained and could break number formatting. | Accept only three-letter uppercase currency codes; otherwise fall back to PKR. |
| Medium | Section navigation did not expose tab selection state or keyboard arrow navigation to assistive technology. | Add tab/tabpanel semantics, selected state, arrow/Home/End navigation, and transaction filter labels. |
| Medium | Keyboard focus and reduced-motion behavior were not explicitly styled. | Add visible focus indicators, larger touch targets, responsive mobile action layout, and reduced-motion overrides. |

## Product / idea review

The product is a viable **local-first personal finance and informal-ledger tool** for an individual who values privacy and does not need bank synchronization. Its clearest differentiators are no account requirement, browser-local records, CSV import/export, JSON backup, and a khata ledger for shared debts.

It should not yet be marketed as a secure financial-data vault or a multi-device accounting system. The current architecture deliberately keeps data in browser storage, which is not encrypted at rest and does not synchronize across devices.

## Remaining risks and verification gates

1. **Root cause of the user's IndexedDB error is not yet known.** The updated banner will expose the browser's error name/message after deployment. Do not clear browser/site data as a diagnostic step.
2. **Browser end-to-end tests have not been run.** Test on current Firefox and Chromium, including a normal window, private browsing, blocked database/open-tab scenarios, import/export, repayment, and reload persistence.
3. **Backup restore spans two storage systems.** Transaction writes are atomic in IndexedDB, but localStorage settings/khata updates cannot participate in the same transaction. A storage quota/security failure during those later writes can leave a partially restored backup.
4. **Backups are plaintext JSON.** Users should store backup files securely. There is no encryption-at-rest or recovery key.
5. **No multi-device sync, bank integration, user accounts, or shared ledger collaboration.** These are product-scope limitations, not bugs in a local-only app.
6. **Date formats can be ambiguous.** Slash/dot dates are interpreted as day/month/year. For broad public CSV compatibility, add an explicit date-format choice in the import UI.
7. **No automated browser test suite exists for the static app.** The current verification includes JavaScript syntax validation and targeted date-parser checks only.

## Manual regression checklist

- Open the deployed app and confirm the storage status reads “Saved on this device.”
- If IndexedDB fails, verify the alert includes the technical error detail and does not suggest clearing site data.
- Add a transaction, reload, and verify it remains.
- Import a CSV containing valid dates, invalid dates, duplicate rows, quoted commas, and a malformed row; verify no partial import occurs on failure.
- Restore a valid backup and a deliberately invalid backup; verify invalid transaction data is rejected before transaction writes.
- Verify local dates around midnight and month/year boundaries.
- Navigate tabs with mouse, Tab, arrow keys, Home, and End; verify focus is visible.
- Test narrow mobile widths and 200% browser zoom.
- Verify the dark-mode toggle still works and persists where localStorage is available.

## Semantic contrast spot-check

The light-theme semantic text pairs were checked using the WCAG relative-luminance formula. Normal text pairs pass 4.5:1: foreground on background (14.74:1), surface (15.91:1), and muted surface (13.76:1); muted foreground on background (5.84:1), surface (6.31:1), and muted surface (5.46:1); primary on background (5.99:1); white primary text on primary (6.47:1); and secondary foreground on secondary (10.73:1). The original light border token failed the 3:1 non-text contrast spot-check, so it was darkened to `#75877A` (3.82:1 against white, 3.54:1 against the page background, 3.30:1 against muted surface). The dark border token was adjusted to `#617268` (3.19:1 against the card surface, 3.48:1 against input surfaces, 3.59:1 against the page background).

This is a semantic color-pair spot-check, not a complete WCAG conformance audit. Focus visibility, keyboard behavior, responsive layout, screen-reader output, and actual browser rendering still require manual testing.
