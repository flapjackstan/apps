"""Main Typer CLI that groups all date-related tools."""

import typer
import apps.holiday
import apps.dates
import apps.names

app = typer.Typer(help="Collection of date utilities: date math and holiday info.")

# Register subcommands
app.add_typer(apps.dates.app, name="dates", help="Work with date calculations.")
app.add_typer(apps.holiday.app, name="holiday", help="View holiday information.")
app.add_typer(apps.names.app, name="names", help="Generate n random names from character pool")


def main():
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()
