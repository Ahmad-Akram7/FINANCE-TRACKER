# Android APK

The Android package wraps the responsive `site/` app with Capacitor and bundles the interface and chart logic inside the APK. It does not depend on the Cloudflare Pages URL to render the app.

## Latest release

Open [GitHub Releases](https://github.com/Ahmad-Akram7/FINANCE-TRACKER/releases) and download `Ledger-Finance-Tracker.apk` from the newest Android release.

The Android workflow runs when the app UI changes on `main`. Each automatic build creates a new `android-v1.1.N` release; a manual run can use a custom tag.

## Android UX

- Persistent bottom navigation for Home, Activity, Insights, and Khata on small screens.
- A transaction-entry dialog opened by the centre plus button, so adding a record does not require scrolling to a form.
- Desktop sidebar navigation for wider displays.
- Cash-flow line chart with selectable monthly points.
- Category donut chart with tap-through to matching expense transactions.
- Reports view with 6- or 12-month income/expense bars and monthly totals.

## Install

1. Download the APK from the latest GitHub Release on your Android phone.
2. Open it and approve installation for your browser or file manager if Android asks.
3. Open Ledger and add a disposable test transaction.
4. Close and reopen the app to verify that the record persists.
5. Export a JSON backup after confirming storage works.

Android may display a warning for apps installed outside Google Play. Install only the APK attached to this repository's release.

## Data and security notes

- The UI and assets are bundled locally; the app does not need to fetch the hosted website to render.
- App storage is separate from browser storage and the Python CLI's SQLite database. Existing browser transactions do not automatically appear in Android.
- Records use Android WebView local storage. This app does not provide encryption at rest, account sign-in, or cloud synchronization.
- Keep JSON backups in a secure place. Do not store banking passwords or full account numbers.
- The APK is debug-signed for testing, not production distribution. Future APKs signed with another key may not upgrade over this installation.

## Validation

The automated workflow checks JavaScript syntax and builds the Android APK. Test transaction creation, IndexedDB persistence, CSV import/export, JSON backup/restore, chart tap targets, navigation, and khata flows on a real Android device before relying on it for important records.
