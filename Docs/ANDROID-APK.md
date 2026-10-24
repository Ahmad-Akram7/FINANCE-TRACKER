# Android APK

The Android package wraps the existing `site/` application with Capacitor and bundles the web assets inside the APK. It does not depend on the Cloudflare Pages URL to load the UI, so the phishing warning on the hosted website does not itself prevent the bundled interface from opening.

## Build and release

The workflow at `.github/workflows/android-apk-release.yml` builds the APK on GitHub Actions and attaches `Ledger-Finance-Tracker.apk` to the GitHub Release `android-v1.0.0`. It can also be run manually from **Actions → Build Android APK and publish GitHub Release → Run workflow** with a release tag.

Release page: https://github.com/Ahmad-Akram7/FINANCE-TRACKER/releases

## Install

1. Download `Ledger-Finance-Tracker.apk` from the release assets on your Android phone.
2. Open the downloaded APK and approve installation for your browser or file manager if Android asks.
3. Open Ledger and add a disposable test transaction first. Close and reopen the app to confirm that it persists.
4. Export a JSON backup after confirming storage works.

Android may display a warning for apps installed outside Google Play. Install only the APK attached to this repository's release.

## Data and security notes

- The UI and its assets are bundled in the APK; it does not need to fetch the hosted website to render.
- App storage is separate from browser storage and the Python CLI's SQLite database. Existing browser transactions will not automatically appear in the Android app.
- Records use the Android WebView's local browser storage. The app does not provide encryption at rest, account sign-in, or cloud synchronization.
- Keep JSON backups in a secure place and do not enter bank passwords or full account numbers.
- The initial APK is debug-signed for installation/testing. It is not a production signing setup, and a future APK signed with another key may not upgrade over this installation.

## Limitations

This is a Capacitor wrapper around the existing responsive web interface, not a separately rewritten native Android UI. Validate transaction creation, IndexedDB persistence, CSV import/export, JSON backup/restore, file pickers, and khata features on a real device before relying on it for important records.