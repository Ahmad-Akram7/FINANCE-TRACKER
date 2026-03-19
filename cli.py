"""Click-based CLI — the user-facing entry point for Finance Tracker."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import click
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from finance_tracker import __version__
from finance_tracker.core import (
    add_transaction,
    delete_transaction,
    get_category_breakdown,
    get_summary,
    list_transactions,
    search_transactions,
)
from finance_tracker.database import get_session, init_db
from finance_tracker.interfaces.display import (
    console,
    print_category_breakdown,
    print_error,
    print_info,
    print_success,
    print_summary,
    print_transactions,
)
from finance_tracker.models import TransactionCreate, TransactionType

# ─── ANSI banner ─────────────────────────────────────────────────────────────

BANNER = r"""
  ███████╗██╗███╗  ██╗ █████╗ ███╗  ██╗ ██████╗███████╗
  ██╔════╝██║████╗ ██║██╔══██╗████╗ ██║██╔════╝██╔════╝
  █████╗  ██║██╔██╗██║███████║██╔██╗██║██║     █████╗
  ██╔══╝  ██║██║╚████║██╔══██║██║╚████║██║     ██╔══╝
  ██║     ██║██║ ╚███║██║  ██║██║ ╚███║╚██████╗███████╗
  ╚═╝     ╚═╝╚═╝  ╚══╝╚═╝  ╚═╝╚═╝  ╚══╝ ╚═════╝╚══════╝
         ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗
         ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
            ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
            ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
            ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
            ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

# ─── Helpers ─────────────────────────────────────────────────────────────────

_PERIOD_MAP = {
    "today":  timedelta(days=1),
    "week":   timedelta(weeks=1),
    "month":  timedelta(days=30),
    "year":   timedelta(days=365),
    "all":    None,
}


def _resolve_since(period: str) -> Optional[datetime]:
    delta = _PERIOD_MAP.get(period.lower())
    return (datetime.utcnow() - delta) if delta else None


# ─── Root group ───────────────────────────────────────────────────────────────

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "-V", "--version", prog_name="finance-tracker")
def cli() -> None:
    """
    \b
    💰  Finance Tracker v{version}
    Personal finance management from your terminal.
    """.format(version=__version__)


# ─── init ─────────────────────────────────────────────────────────────────────

@cli.command()
def init() -> None:
    """Initialise the SQLite database (safe to run multiple times)."""
    console.print(Panel(Text(BANNER, style="bold green"), border_style="green", padding=0))
    init_db()
    print_success("Database initialised successfully.")
    print_info("Run [bold]finance-tracker --help[/bold] to get started.")


# ─── add ──────────────────────────────────────────────────────────────────────

@cli.command()
@click.option(
    "--type", "-t", "tx_type",
    required=True,
    type=click.Choice(["income", "expense", "savings"], case_sensitive=False),
    help="Transaction type.",
)
@click.option("--amount", "-a", required=True, type=float, help="Amount (must be > 0).")
@click.option("--category", "-c", required=True, type=str, help="Category label.")
@click.option("--description", "-d", default=None, type=str, help="Optional note.")
def add(tx_type: str, amount: float, category: str, description: Optional[str]) -> None:
    """Add a new transaction (income, expense, or savings)."""
    try:
        data = TransactionCreate(
            type=TransactionType(tx_type.lower()),
            amount=amount,
            category=category,
            description=description,
        )
    except ValidationError as e:
        for err in e.errors():
            print_error(err["msg"])
        sys.exit(1)

    with get_session() as session:
        tx = add_transaction(session, data)
        print_success(
            f"[{tx_type.upper()}] ${tx.amount:,.2f}  ·  {tx.category}"
            + (f"  ·  {tx.description}" if tx.description else "")
            + f"  [dim](id={tx.id})[/dim]"
        )


# ─── list ─────────────────────────────────────────────────────────────────────

@cli.command("list")
@click.option(
    "--type", "-t", "tx_type", default=None,
    type=click.Choice(["income", "expense", "savings"], case_sensitive=False),
    help="Filter by transaction type.",
)
@click.option("--category", "-c", default=None, help="Filter by category (partial match).")
@click.option("--limit",    "-n", default=50,   type=int, help="Max rows to show (default 50).")
def list_cmd(tx_type: Optional[str], category: Optional[str], limit: int) -> None:
    """List transactions, with optional filters."""
    with get_session() as session:
        txs = list_transactions(
            session,
            tx_type=TransactionType(tx_type) if tx_type else None,
            category=category,
            limit=limit,
        )
    title = "All Transactions"
    if tx_type:
        title = f"{tx_type.capitalize()} Transactions"
    if category:
        title += f"  ·  category: {category}"
    print_transactions(txs, title=title)
    print_info(f"{len(txs)} record(s) shown.")


# ─── delete ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("transaction_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this transaction?")
def delete(transaction_id: int) -> None:
    """Delete a transaction by ID."""
    with get_session() as session:
        ok = delete_transaction(session, transaction_id)
    if ok:
        print_success(f"Transaction #{transaction_id} deleted.")
    else:
        print_error(f"Transaction #{transaction_id} not found.")
        sys.exit(1)


# ─── report ───────────────────────────────────────────────────────────────────

@cli.command()
@click.option(
    "--period", "-p", default="all",
    type=click.Choice(list(_PERIOD_MAP.keys()), case_sensitive=False),
    help="Time window for the report (default: all).",
    show_default=True,
)
def report(period: str) -> None:
    """Print a financial summary table."""
    since = _resolve_since(period)
    with get_session() as session:
        summary = get_summary(session, since=since)
    period_label = period.capitalize() if period != "all" else "All time"
    print_summary(summary, period=period_label)


# ─── breakdown ────────────────────────────────────────────────────────────────

@cli.command()
@click.option(
    "--type", "-t", "tx_type", default="expense",
    type=click.Choice(["income", "expense", "savings"], case_sensitive=False),
    help="Which transaction type to break down (default: expense).",
    show_default=True,
)
def breakdown(tx_type: str) -> None:
    """Show spending/income breakdown by category."""
    with get_session() as session:
        data = get_category_breakdown(session, tx_type=TransactionType(tx_type))
    print_category_breakdown(data, tx_type)


# ─── search ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("keyword")
def search(keyword: str) -> None:
    """Search transactions by keyword (category or description)."""
    with get_session() as session:
        results = search_transactions(session, keyword)
    print_transactions(results, title=f'Search: "{keyword}"')
    print_info(f"{len(results)} result(s).")


# ─── visual-report ────────────────────────────────────────────────────────────

@cli.command("visual-report")
@click.option(
    "--output", "-o", default="finance_report.png",
    type=click.Path(),
    help="Output PNG path.",
    show_default=True,
)
@click.option(
    "--period", "-p", default="all",
    type=click.Choice(list(_PERIOD_MAP.keys()), case_sensitive=False),
    show_default=True,
)
def visual_report(output: str, period: str) -> None:
    """Generate a bar-chart PNG of your financial summary."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print_error("matplotlib is not installed. Run: pip install matplotlib")
        sys.exit(1)

    since = _resolve_since(period)
    with get_session() as session:
        summary = get_summary(session, since=since)
        breakdown_data = get_category_breakdown(session, tx_type=TransactionType.EXPENSE)

    # ── Style ──
    BG       = "#0d1117"
    CARD_BG  = "#161b22"
    GREEN    = "#3fb950"
    RED      = "#f85149"
    CYAN     = "#58a6ff"
    GOLD     = "#d29922"
    TEXT     = "#c9d1d9"
    MUTED    = "#8b949e"

    fig = plt.figure(figsize=(14, 9), facecolor=BG)
    fig.suptitle(
        f"Finance Tracker  ·  {period.capitalize() if period != 'all' else 'All Time'}",
        fontsize=16, fontweight="bold", color=TEXT, y=0.97,
        fontfamily="monospace",
    )

    gs = fig.add_gridspec(2, 2, hspace=0.45, wspace=0.35,
                          left=0.08, right=0.95, top=0.90, bottom=0.08)

    # ── Panel 1: Summary bar ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(CARD_BG)
    labels  = ["Income", "Expenses", "Savings", "Net"]
    values  = [summary.total_income, summary.total_expenses, summary.total_savings, summary.net]
    colours = [GREEN, RED, CYAN, GREEN if summary.net >= 0 else RED]
    bars = ax1.bar(labels, values, color=colours, edgecolor=BG, linewidth=1.5)
    ax1.set_title("Summary", color=TEXT, fontsize=11, pad=8)
    ax1.set_ylabel("USD ($)", color=MUTED, fontsize=9)
    ax1.tick_params(colors=MUTED, labelsize=8)
    ax1.spines[:].set_color("#30363d")
    for bar, val in zip(bars, values):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.01,
            f"${val:,.0f}", ha="center", va="bottom",
            color=TEXT, fontsize=7.5, fontfamily="monospace",
        )

    # ── Panel 2: Metrics cards ──
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(CARD_BG)
    ax2.axis("off")
    metrics = [
        ("Total Income",   f"${summary.total_income:,.2f}",   GREEN),
        ("Total Expenses", f"${summary.total_expenses:,.2f}", RED),
        ("Total Savings",  f"${summary.total_savings:,.2f}",  CYAN),
        ("Net Balance",    f"${summary.net:,.2f}",            GREEN if summary.net >= 0 else RED),
        ("Savings Rate",   f"{summary.savings_rate:.1f}%",    GOLD),
    ]
    for i, (label, value, colour) in enumerate(metrics):
        y = 0.88 - i * 0.18
        ax2.text(0.05, y, label, transform=ax2.transAxes,
                 fontsize=9, color=MUTED)
        ax2.text(0.95, y, value, transform=ax2.transAxes,
                 fontsize=11, color=colour, fontweight="bold",
                 fontfamily="monospace", ha="right")
        ax2.axhline(y - 0.04, color="#30363d", linewidth=0.5, xmin=0.03, xmax=0.97,
                    transform=ax2.transAxes)
    ax2.set_title("Key Metrics", color=TEXT, fontsize=11, pad=8)

    # ── Panel 3: Expense donut ──
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(CARD_BG)
    if breakdown_data:
        cats   = list(breakdown_data.keys())[:7]
        vals   = [breakdown_data[c] for c in cats]
        pie_colours = [GREEN, RED, CYAN, GOLD, "#79c0ff", "#ffab70", "#ffa657"]
        wedges, texts, autotexts = ax3.pie(
            vals, labels=None, autopct="%1.1f%%",
            colors=pie_colours[:len(cats)],
            startangle=140, pctdistance=0.82,
            wedgeprops=dict(edgecolor=BG, linewidth=2),
        )
        for t in autotexts:
            t.set_color(BG)
            t.set_fontsize(7.5)
            t.set_fontweight("bold")
        # donut
        centre = plt.Circle((0, 0), 0.55, color=CARD_BG)
        ax3.add_patch(centre)
        ax3.legend(
            [mpatches.Patch(color=pie_colours[i]) for i in range(len(cats))],
            cats, loc="lower center", bbox_to_anchor=(0.5, -0.22),
            ncol=3, fontsize=7, labelcolor=MUTED, frameon=False,
        )
    else:
        ax3.text(0.5, 0.5, "No expense data", ha="center", va="center",
                 color=MUTED, transform=ax3.transAxes)
    ax3.set_title("Expenses by Category", color=TEXT, fontsize=11, pad=8)

    # ── Panel 4: Category bar ──
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(CARD_BG)
    if breakdown_data:
        top_cats = list(breakdown_data.keys())[:8]
        top_vals = [breakdown_data[c] for c in top_cats]
        ax4.barh(top_cats[::-1], top_vals[::-1], color=RED, edgecolor=BG, linewidth=1)
        ax4.tick_params(colors=MUTED, labelsize=8)
        ax4.spines[:].set_color("#30363d")
        ax4.set_xlabel("Amount ($)", color=MUTED, fontsize=8)
    else:
        ax4.text(0.5, 0.5, "No data", ha="center", va="center",
                 color=MUTED, transform=ax4.transAxes)
    ax4.set_title("Top Expense Categories", color=TEXT, fontsize=11, pad=8)

    out_path = Path(output)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print_success(f"Visual report saved → [bold]{out_path.resolve()}[/bold]")


# ─── export ───────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--output", "-o", default="transactions.csv",
              type=click.Path(), help="Output CSV file.", show_default=True)
def export(output: str) -> None:
    """Export all transactions to a CSV file."""
    import csv

    with get_session() as session:
        txs = list_transactions(session)

    out = Path(output)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "type", "amount", "category", "description", "date"])
        for tx in txs:
            writer.writerow([
                tx.id, tx.type.value, tx.amount,
                tx.category, tx.description or "",
                tx.date.strftime("%Y-%m-%d %H:%M:%S") if tx.date else "",
            ])

    print_success(f"Exported {len(txs)} transaction(s) → [bold]{out.resolve()}[/bold]")


# ─── budget ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("category")
@click.argument("limit", type=float)
@click.option("--period", "-p", default="month",
              type=click.Choice(list(_PERIOD_MAP.keys()), case_sensitive=False),
              show_default=True)
def budget(category: str, limit: float, period: str) -> None:
    """Check spending against a budget limit for a category."""
    since = _resolve_since(period)
    with get_session() as session:
        txs = list_transactions(
            session,
            tx_type=TransactionType.EXPENSE,
            category=category,
        )
    if since:
        txs = [t for t in txs if t.date and t.date >= since]

    spent = sum(t.amount for t in txs)
    remaining = limit - spent
    pct = (spent / limit * 100) if limit else 0
    bar_filled = int(pct / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    colour  = "green" if pct < 70 else ("yellow" if pct < 90 else "red")
    console.print(f"\n  Budget Check  ·  [bold]{category}[/bold]  ·  {period.capitalize()}\n")
    console.print(f"  [{colour}]{bar}[/{colour}]  {pct:.1f}%")
    console.print(f"  Spent    [bold red]${spent:,.2f}[/bold red]  /  Budget [bold]${limit:,.2f}[/bold]")
    if remaining >= 0:
        print_success(f"${remaining:,.2f} remaining this {period}.")
    else:
        print_error(f"Over budget by ${abs(remaining):,.2f}!")


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
