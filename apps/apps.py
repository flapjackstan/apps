"""Main Typer CLI that groups all date-related tools."""

import typer
import apps.holiday
import apps.dates

app = typer.Typer(help="Collection of date utilities: date math and holiday info.")

# Register subcommands
app.add_typer(apps.dates.app, name="dates", help="Work with date calculations.")
app.add_typer(apps.holiday.app, name="holiday", help="View holiday information.")


def main():
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()
