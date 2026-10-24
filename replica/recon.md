# Ledger UX reconnaissance

## Scope
- Product: Ledger, a local-first personal finance tracker.
- Target platform: Android APK (Capacitor/WebView) and responsive static web app.
- Core slice: review the month at a glance, add a transaction without scrolling, explore spending trends, and drill into matching transactions.
- Audience: an individual recording income, expenses, savings transfers, budgets, goals, and informal shared expenses.
- Approach: clean-room use of common finance UX patterns; no third-party code, logos, or proprietary copy is reused.

## Public reference sources
| Source | URL | Patterns reviewed |
|---|---|---|
| Monarch Reports help | https://help.monarch.com/hc/en-us/articles/21846787088916-Reports | Date/category filters, cash flow, spending and income charts, drill-downs |
| Monarch tracking | https://www.monarch.com/features/tracking | Searchable transactions, reports, goals, recurring items |
| YNAB Spending Trends | https://support.ynab.com/en_us/spending-trends-H1inlhzAc | Left navigation, category-group charts, drill-down to transactions |
| YNAB income vs spending on mobile | https://www.ynab.com/whats-new/check-your-income-vs-spending-on-mobile | Six-month mobile comparison and quick insights |
| Copilot dashboard | https://help.copilot.money/en/articles/6045480-dashboard-tab-overview | Spending pace, budget context, review actions |
| Copilot cash flow | https://help.copilot.money/en/articles/9682232-cash-flow-tab-overview | Monthly income/spending/net comparisons and chart interaction |

## Screen inventory
| ID | Screen | Entry | Purpose | Key components | Important states |
|---|---|---|---|---|---|
| S01 | Overview | Home / initial load | Monthly status at a glance | Metric cards, cash-flow line, insight, category donut, recent activity | Empty, populated, negative net, storage error |
| S02 | Transactions | Sidebar, bottom nav, chart drill-down | Find and manage records | Search, type filter, table, delete confirmation | Empty, no match, long descriptions |
| S03 | Budgets | Navigation | Set category limits and monitor spend | Budget form, progress bars | Empty, under limit, over limit |
| S04 | Savings goals | Navigation | Track targets | Goal form, progress bars | Empty, partial, complete |
| S05 | Reports | Insights nav / chart link | Compare monthly cash flow and category spending | 6/12-month selector, grouped bars, donut, recent activity | No data, one month, negative net |
| S06 | Khata & splits | Navigation / quick CTA | Track who owes whom and split bills | People list, balances, IOU form, allocation editor | Empty, no people, custom split, repayment |
| S07 | Quick add | Fixed plus / desktop action | Create a transaction from any screen | Modal form, validation status, save feedback | Invalid amount, saving, failure, success |
| S08 | Data tools | Sidebar menu | Import/export and backup/restore | CSV picker/export, JSON backup/restore | Missing file, invalid file, successful export |

## Core flows
- F01 Add a transaction: any screen → fixed plus / Add transaction → enter type, amount, category, date → save → summary and reports refresh.
- F02 Explore a category: Overview/Reports → tap category legend → Transactions opens with expense filter and category search applied.
- F03 Inspect a month: Overview line point or Reports monthly bar → selected month totals show income, expenses, savings transfers, and net.
- F04 Navigate on a phone: fixed bottom nav → Home, Activity, Insights, or Khata; budgets and goals remain accessible from the desktop sidebar and the app's section controls.
- F05 Recover data: Data tools → export JSON → retain a local backup; restore only after reviewing the selected file and confirmation.

## Component inventory
- Persistent desktop sidebar and mobile bottom navigation.
- Compact metric card, surface panel, status chip, primary/secondary/destructive button.
- SVG cash-flow line chart with focusable monthly points.
- CSS conic-gradient donut with category legend and drill-down buttons.
- Monthly paired-bar chart with 6/12-month range selection.
- Quick-add dialog, labelled inputs, validation status, storage status, data-tools disclosure.
- Existing transaction table, budget progress bars, goal progress bars, khata people list, repayment and split-allocation controls.

## Data model and evidence
- Transaction: id, type (income/expense/savings), amount, category, date, description, createdAt. Evidence: existing form and IndexedDB record operations. Confidence: high.
- Budget: category, limit. Evidence: budget form and localStorage key. Confidence: high.
- Goal: id, name, target, saved, optional date. Evidence: goal form. Confidence: high.
- Khata entry: id, person, direction, amount, paid, date, optional dueDate/note. Evidence: IOU and repayment forms. Confidence: high.
- Person: display name. Evidence: people list and split selector. Confidence: high.
- Preferences: currency and theme. Evidence: existing localStorage settings. Confidence: high.

## Boundaries
- No bank connectivity, account system, cloud sync, push notifications, financial advice, or encryption-at-rest claim.
- Android WebView data, browser IndexedDB/localStorage, and CLI SQLite are separate stores.
- This is an original implementation informed by common interaction patterns, not a pixel-copy of any reference app.

## Size and risk
- Size: M. Navigation and SVG/CSS charts are small; validating file import/export and IndexedDB persistence in Android WebView is the harder part.
- Highest-risk validation: chart tap targets, keyboard interaction, dialog behavior on Android WebView, local persistence after app restart, and CSV/JSON file pickers.
