"""CLI app to get next US federal holiday."""

from datetime import datetime
import holidays
import typer

app = typer.Typer(help="Get information about US federal holidays.")


def get_next_federal_holiday() -> str:
    """Retrieve the next federal holiday in the US."""
    us_holidays = holidays.US(years=datetime.now().year)
    today = datetime.today().date()
    next_holiday = min(date for date in us_holidays.keys() if date > today)
    day_of_week = next_holiday.strftime("%A")
    days_until = (next_holiday - today).days

    return (
        f"The next federal holiday is {next_holiday} ({day_of_week}) - "
        f"{us_holidays[next_holiday]}. It is in {days_until} days."
    )


@app.command("next")
def next_holiday():
    """Print the next federal holiday."""
    typer.echo(get_next_federal_holiday())
