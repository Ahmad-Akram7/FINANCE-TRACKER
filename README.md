# Finance Tracker

A local-first personal finance tracker plus a Python CLI. The browser app is a static site and can be hosted on GitHub Pages or Cloudflare Pages without a server, build step, paid API, or account.

## Browser app

- **Live locally:** open [site/index.html](site/index.html) in a modern browser.
- **GitHub Pages:** the included Actions workflow deploys the `site/` directory on pushes to `main`. In repository Settings → Pages, select **GitHub Actions** as the build/deployment source.
- **Cloudflare Pages:** create a Pages project connected to this repository. Set the build command to none (leave it blank) and the build output directory to `site`. No environment variables are required.

Features: income/expense/savings transactions, monthly cash-flow summary, category spending, budgets, savings goals, search/filter, CSV export and JSON backup/restore.

## Project layout

```text
.
├── site/                    # Deployable static web app
│   ├── index.html
│   ├── assets/
│   │   ├── css/app.css
│   │   └── js/app.js
│   └── _headers             # Cloudflare Pages response headers
├── .github/workflows/
│   └── pages.yml            # GitHub Pages deployment
├── Docs/                    # Research and implementation notes
├── cli.py, core.py, ...     # Existing Python CLI
├── tests (test_core.py)     # CLI tests
└── setup.py
```

## Privacy and storage

The browser app stores transactions in IndexedDB and budgets/goals in localStorage in the current browser profile. It does not sync across devices or connect to banks. Browser storage is **not encrypted at rest**; do not enter bank credentials or full account numbers. Export backups regularly. CSV export contains transactions; JSON backup includes transactions, budgets and goals.

The currency display defaults to PKR; this formats values but does not convert currencies.

## Python CLI

See [FINANCE_README.md](FINANCE_README.md) for installation and terminal commands. The CLI uses a local SQLite database by default and remains independent of the browser app.

## Documentation

- [Finance manager research](Docs/finance-manager-research.md)
- [Replication map](Docs/replica-map.md)
- [Feature matrix](Docs/feature-matrix.csv)

## License

See [LICENSE](LICENSE).
