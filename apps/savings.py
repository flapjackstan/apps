from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Calculate savings needed for a period of unemployment.")
console = Console()


@app.command()
def calculate(
    monthly_cost: Annotated[
        float,
        typer.Argument(help="Your monthly expenses.")
    ],
):
    """
    Generate a 20-year savings table.
    """

    annual_cost = monthly_cost * 12

    table = Table(title="Savings Needed to Cover Living Expenses")

    table.add_column("Years", justify="right")
    table.add_column("Annual Cost", justify="right")
    table.add_column("Savings Needed", justify="right")

    for years in range(1, 21):
        table.add_row(
            str(years),
            f"${annual_cost:,.2f}",
            f"${annual_cost * years:,.2f}",
        )

    console.print(table)


if __name__ == "__main__":
    app()
