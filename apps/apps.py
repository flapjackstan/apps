"""Main Typer CLI that groups all date-related tools."""

import typer
from apps.holiday import app as holiday_app
from apps.dates import app as dates_app
from apps.interview import app as interview_app
from apps.lotto import app as lotto_app
from apps.names import app as names_app
from apps.savings import app as savings_app
from apps.timer import app as timer_app
from apps.tracts import app as tracts_app

cli = typer.Typer(help="Collection of date utilities: date math and holiday info.")

# Register subcommands
cli.add_typer(dates_app, name="dates", help="Work with date calculations.")
cli.add_typer(holiday_app, name="holiday", help="View holiday information.")
cli.add_typer(interview_app, name="interview", help="Generate interview prep prompts and a random Leetcode question.")
cli.add_typer(lotto_app, name="lotto", help="Randomly select names from a list until all are selected.")
cli.add_typer(names_app, name="names", help="Generate n random names from character pool")
cli.add_typer(savings_app, name="savings", help="Calculate savings needed for a period of unemployment.")
cli.add_typer(timer_app, name="timer", help="Run a timer with optional sub-timer notifications.")
cli.add_typer(tracts_app, name="tracts", help="Download census tract data to a GeoJSON file.")


def main():
    """CLI entrypoint."""
    cli()


if __name__ == "__main__":
    main()
