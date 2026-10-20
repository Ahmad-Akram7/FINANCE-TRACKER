# Product and implementation audit

**Reviewed:** 2026-10-20  
**Scope:** browser app, Python CLI, repository structure, documentation, and CI.  
**Status:** automated static checks are in place; browser end-to-end and assistive-technology verification remain release gates.

## Executive summary

Ledger is a useful local-first personal finance tool for manual transaction tracking and informal shared-debt accounting. It provides a static browser app, no account requirement, category budgets, savings goals, CSV import/export, JSON backup/restore, and a person-based khata ledger.

The repository contains two separate applications:
- **Browser app:** static files in `site/`; transactions in IndexedDB, settings and khata lists in localStorage.
- **Python CLI:** installable package in `finance_tracker/`; records in local SQLite.

They do not sync. The browser app is not an encrypted vault and should not be marketed as a bank-grade or security-critical financial system.

## Repository cleanup decisions

| Path | Purpose | Decision |
|---|---|---|
| `site/` | Browser app and static deployment output | Keep |
| `finance_tracker/` | Installable Python CLI package | Keep |
| Root Python wrappers | Backwards-compatible imports and launchers | Keep; not abandoned duplicates |
| `.github/workflows/browser-checks.yml` | JavaScript and Python CI | Keep |
| `.github/workflows/pages.yml` | GitHub Pages deployment | Keep if GitHub Pages is a desired target |
| `Docs/PRODUCT_AUDIT.md` | Canonical audit and release checklist | Keep |
| `Docs/finance-manager-research.md` | Product research and scope | Keep |
| `Docs/feature-matrix.csv` | Current feature inventory | Keep |
| `Docs/architecture.svg`, `Docs/browser-preview.svg` | Documentation diagrams; UI preview is illustrative | Keep |
| Duplicate audit files and older replica map | Overlapping or stale documentation | Consolidated into the canonical docs and removed |

## Findings and mitigations

| Priority | Finding | Mitigation / status |
|---|---|---|
| High | Browser storage may be unavailable or blocked in a particular browser context. | Header exposes storage status and startup errors should be read in DevTools. Close duplicate tabs if the database is blocked; do not clear data as a first diagnostic step. |
| High | Green CI does not prove every browser interaction works. | CI checks JS syntax, key static references, package installation, and Python tests. Manual browser regression remains required. |
| High | Browser data is not encrypted at rest and can be lost when site data is cleared. | Documented prominently; users should keep secure JSON backups and avoid storing credentials or full account numbers. |
| High | Restore spans IndexedDB and localStorage, which cannot share one atomic transaction. | Transaction records are validated and written in an IndexedDB transaction; localStorage failure can still leave a cross-store restore partially applied. |
| Medium | CLI and browser app use separate stores. | Documented; no sync is implied. |
| Medium | GitHub Pages does not deploy to the separately managed Cloudflare project. | Documented as separate deployment paths; Cloudflare can be deployed with Wrangler from the local `site/` directory. |
| Medium | Savings-rate meaning can be misunderstood. | It means recorded savings transfers divided by recorded income, not inferred surplus or a recommendation. |
| Medium | CSV date formats can be ambiguous. | Prefer ISO `YYYY-MM-DD` dates; slash/dot formats can be ambiguous. An explicit date-format selector remains a potential improvement. |
| Medium | Root Python files look duplicated. | They are compatibility shims; deleting them could break old imports and scripts. |

## Automated verification

`.github/workflows/browser-checks.yml` runs JavaScript syntax/static checks, installs the Python package, and runs `pytest`. `.github/workflows/pages.yml` separately validates JS syntax and publishes `site/` to GitHub Pages. Neither is a full browser E2E suite. A green GitHub Pages workflow does not confirm a separate Cloudflare project was updated.

## Manual release checklist

- [ ] Open the intended URL in Firefox and Chromium in a normal (non-private) window.
- [ ] Confirm storage status; add a transaction, reload, and verify persistence.
- [ ] Add income, expense, and savings records; verify totals and savings-rate definition.
- [ ] Test category spending and budget matching with case differences.
- [ ] Create/remove goals; test zero saved amount and optional target date.
- [ ] Test khata directions, repayments, balances, and custom 2–3-person splits down to the cent.
- [ ] Import CSV containing quoted commas/newlines, duplicates, malformed rows, and impossible dates.
- [ ] Export JSON and restore valid/invalid backups; ensure invalid transactions are rejected before writes.
- [ ] Navigate tabs with mouse, Tab, arrows, Home, and End.
- [ ] Check a 320px viewport, 200% zoom, visible focus, dark mode, and reduced motion.
- [ ] Confirm the intended hosting target; GitHub Pages and Cloudflare Pages are separate.
- [ ] Keep a known-good JSON backup before testing storage recovery.

## Product scope

**Included:** manual tracking, monthly overview, budgets, savings goals, search/filter, CSV workflows, JSON backup/restore, and personal khata entries.

**Not included:** bank aggregation, login, multi-device sync, encrypted-at-rest storage, shared cloud ledger, automatic subscription detection, bill reminders, investment valuation, multi-currency conversion, or financial advice.

## Recommendation

Treat Ledger as a **local-first MVP**. Do not claim production-grade reliability until browser regression tests cover storage, import/restore, and calculations. The highest-value next step is repeatable Firefox/Chromium end-to-end tests, including storage failure and backup recovery.
