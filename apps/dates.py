"""CLI app for working with dates using Typer."""

import datetime
import typer

app = typer.Typer(help="Calculate days between dates or move forward/back by N days.")


def get_date_from(date: str, days: int, direction: str) -> str:
    """Get date days back or forward from input date."""
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

    if direction == "back":
        delta = datetime.timedelta(days=-days)
    elif direction == "forward":
        delta = datetime.timedelta(days=days)
    else:
        raise ValueError("Invalid direction. Please use 'back' or 'forward'.")

    return (date_obj + delta).strftime("%Y-%m-%d")


def calculate_days_between(date1: str, date2: str) -> int:
    """Calculate the number of days between two dates."""
    date_obj1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date_obj2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    return (date_obj2 - date_obj1).days


@app.command("between")
def days_between(
    date1: str = typer.Argument(..., help="Start date in YYYY-MM-DD format."),
    date2: str = typer.Argument(..., help="End date in YYYY-MM-DD format."),
):
    """Calculate number of days between two dates."""
    days = calculate_days_between(date1, date2)
    typer.echo(f"The number of days between {date1} and {date2} is: {days}")


@app.command("shift")
def date_shift(
    date: str = typer.Argument(..., help="Input date in YYYY-MM-DD format."),
    days: int = typer.Argument(..., help="Number of days to move."),
    direction: str = typer.Argument(..., help="Direction: 'back' or 'forward'."),
):
    """Get the date N days forward or back from a given date."""
    result = get_date_from(date, days, direction)
    typer.echo(f"{days} days {direction} from {date} is: {result}")
