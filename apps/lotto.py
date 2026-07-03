"""Random picker app."""

import random
from typing import List

import typer

app = typer.Typer(help="Randomly select names from a list until all are selected.")


def randomize_selection_order(names: List[str], shuffle: bool = False) -> List[str]:
    """Return names in the random order they'd be selected, one at a time."""
    pool = list(names)
    if shuffle:
        random.shuffle(pool)

    order = []
    while pool:
        chosen = random.choice(pool)
        order.append(chosen)
        pool.remove(chosen)

    return order


@app.command("pick")
def pick(
    names: List[str] = typer.Argument(..., help="Space separated names to choose from."),
    shuffle: bool = typer.Option(False, "--shuffle", "-s", help="Shuffle the list before selection."),
    pause: bool = typer.Option(True, help="Pause for Enter between each name."),
):
    """Randomly select names one at a time until all are selected."""
    order = randomize_selection_order(names, shuffle=shuffle)

    typer.echo("Randomly selecting names...")
    for name in order:
        typer.echo(f"Selected: {name}")
        if pause:
            typer.prompt("Press Enter for next name", default="", show_default=False)

    typer.echo("\nAll names have been selected:")
    typer.echo(", ".join(order))
