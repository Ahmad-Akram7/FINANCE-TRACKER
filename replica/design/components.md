# Ledger component specifications

## Navigation
- Desktop sidebar: fixed 248 px rail; icon and text labels; active destination has an accent indicator; data tools stay below primary destinations.
- Mobile bottom bar: fixed to viewport bottom with safe-area padding; Home, Activity, Insights, Khata and a visually prominent add action. Targets remain at least 44 px where practical.
- States: default, active, keyboard focus, disabled. Active state is conveyed by background and text, not color alone.

## Metric card
- Shows label, prominent numeric value, and period/definition.
- Uses tabular numerals; negative net cash flow uses danger role and positive uses success role.
- At narrow widths cards use a two-column grid; values wrap rather than overflow.

## Charts
- Cash-flow line: inline SVG, visible grid and legend, accessible name, focusable data points with keyboard activation and tooltips.
- Category donut: CSS conic gradient computed from actual local expense records; central total equals the displayed category sum; legend buttons are keyboard-accessible and open filtered transactions.
- Monthly comparison bars: native buttons with paired income/expense bars, six/twelve month selection, visible selected state, and a monthly detail panel.
- Never use fabricated sample values in user totals; empty states explain how to populate charts.

## Quick-add dialog
- Native dialog with labelled fields, close control, click-outside close, validation feedback and pending/success/error states.
- The same save operation is used by the dashboard form and dialog to keep validation and persistence behavior consistent.

## Data tools
- CSV import, CSV export, JSON backup and JSON restore remain available through the Data tools disclosure.
- Preserve existing IndexedDB/localStorage behavior; do not migrate or clear data as part of a visual refresh.

## Accessibility
- Semantic buttons for actions; labels for every input; visible focus; chart points support Enter/Space.
- Reduced-motion preference is respected by the stylesheet.
- Verify text/background contrast and test at 390 px and 1440 px. Automated syntax checks do not constitute end-to-end validation.
