"""Main Typer CLI that groups all date-related tools."""

import typer
from apps.holiday import app as holiday_app
from apps.dates import app as dates_app
from apps.names import app as names_app

cli = typer.Typer(help="Collection of date utilities: date math and holiday info.")

# Register subcommands
cli.add_typer(dates_app, name="dates", help="Work with date calculations.")
cli.add_typer(holiday_app, name="holiday", help="View holiday information.")
cli.add_typer(names_app, name="names", help="Generate n random names from character pool")


def main():
    """CLI entrypoint."""
    cli()


if __name__ == "__main__":
    main()
