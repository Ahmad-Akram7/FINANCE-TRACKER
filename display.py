"""Rich-powered display helpers — all visual output lives here."""

from __future__ import annotations

from datetime import datetime
from typing import List

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from finance_tracker.core import FinanceSummary
from finance_tracker.models import Transaction, TransactionType

console = Console()

# ─── Colour palette ──────────────────────────────────────────────────────────
_TYPE_COLOUR = {
    TransactionType.INCOME:  "green",
    TransactionType.EXPENSE: "red",
    TransactionType.SAVINGS: "cyan",
}
_TYPE_ICON = {
    TransactionType.INCOME:  "↑",
    TransactionType.EXPENSE: "↓",
    TransactionType.SAVINGS: "⊛",
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _fmt_amount(amount: float, tx_type: TransactionType) -> Text:
    colour = _TYPE_COLOUR[tx_type]
    icon   = _TYPE_ICON[tx_type]
    return Text(f"{icon} ${amount:,.2f}", style=f"bold {colour}")


def _fmt_date(dt: datetime) -> str:
    return dt.strftime("%d %b %Y  %H:%M") if dt else "—"


# ─── Public display functions ────────────────────────────────────────────────

def print_transactions(transactions: List[Transaction], title: str = "Transactions") -> None:
    if not transactions:
        console.print(Panel("[dim]No transactions found.[/dim]", title=title))
        return

    table = Table(
        title=title,
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold white on grey23",
        border_style="grey42",
        expand=False,
        min_width=80,
    )
    table.add_column("ID",          style="dim",        width=5,  justify="right")
    table.add_column("Type",        style="bold",       width=9)
    table.add_column("Amount",      justify="right",    width=14)
    table.add_column("Category",    style="yellow",     width=20)
    table.add_column("Description", style="dim white",  width=26, no_wrap=False)
    table.add_column("Date",        style="dim",        width=18)

    for tx in transactions:
        colour = _TYPE_COLOUR[tx.type]
        table.add_row(
            str(tx.id),
            Text(tx.type.value.capitalize(), style=f"bold {colour}"),
            _fmt_amount(tx.amount, tx.type),
            tx.category,
            tx.description or "—",
            _fmt_date(tx.date),
        )

    console.print(table)


def print_summary(summary: FinanceSummary, period: str = "All time") -> None:
    table = Table(
        title=f"📊  Financial Summary  ·  {period}",
        box=box.DOUBLE_EDGE,
        show_header=False,
        border_style="cyan",
        min_width=52,
    )
    table.add_column("Metric", style="bold white",  width=34)
    table.add_column("Value",  justify="right",     width=16)

    table.add_row("Total Income",    Text(f"${summary.total_income:>12,.2f}", style="bold green"))
    table.add_row("Total Expenses",  Text(f"${summary.total_expenses:>12,.2f}", style="bold red"))
    table.add_row("Total Savings",   Text(f"${summary.total_savings:>12,.2f}", style="bold cyan"))
    table.add_row("─" * 34,          "─" * 16)
    net_colour = "green" if summary.net >= 0 else "red"
    table.add_row("Net  (Income − Expenses)", Text(f"${summary.net:>12,.2f}", style=f"bold {net_colour}"))
    table.add_row("Savings Rate",    Text(f"{summary.savings_rate:>11.1f}%",   style="bold cyan"))
    console.print(table)


def print_category_breakdown(breakdown: dict[str, float], tx_type: str) -> None:
    if not breakdown:
        console.print("[dim]No data.[/dim]")
        return

    total = sum(breakdown.values())
    table = Table(
        title=f"Category Breakdown  ·  {tx_type.capitalize()}",
        box=box.SIMPLE_HEAVY,
        header_style="bold white",
        border_style="grey42",
        min_width=52,
    )
    table.add_column("Category", style="yellow",     width=28)
    table.add_column("Amount",   justify="right",    width=14)
    table.add_column("Share",    justify="right",    width=8)

    for cat, amt in breakdown.items():
        pct = (amt / total * 100) if total else 0
        bar = "█" * int(pct / 5)
        table.add_row(cat, f"${amt:,.2f}", f"{pct:>5.1f}%  {bar}")

    console.print(table)


def print_success(msg: str) -> None:
    console.print(f"  [bold green]✓[/bold green]  {msg}")


def print_error(msg: str) -> None:
    console.print(f"  [bold red]✗[/bold red]  {msg}")


def print_info(msg: str) -> None:
    console.print(f"  [bold cyan]ℹ[/bold cyan]  {msg}")
