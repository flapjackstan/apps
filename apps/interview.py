"""Interview prep prompt generator."""

import random
from pathlib import Path
from typing import List

import typer
from bs4 import BeautifulSoup

app = typer.Typer(help="Generate interview prep prompts and a random Leetcode question.")

LEETCODE_HTML = Path(__file__).parent / "assets" / "formatted_leetcode.html"
PROBLEM_CONTAINER_CLASS = (
    "flex flex-col border-b-[1.5px] duration-300 last:border-b-0 border-lc-fill-02 "
    "dark:border-dark-lc-fill-02 hover:bg-lc-fill-02 dark:hover:bg-dark-lc-fill-02 cursor-pointer"
)

DIFFICULTY_NAMES = {"E": "easy", "M": "medium", "H": "hard"}


def resolve_difficulty(difficulty: str) -> str:
    """Map a difficulty code (E, M, H, or R for random) to its full name."""
    if difficulty == "R":
        difficulty = random.choice(["E", "M", "H"])
    return DIFFICULTY_NAMES[difficulty]


def get_problem_titles() -> List[str]:
    """Parse the bundled Leetcode HTML export and return all problem titles."""
    html_content = LEETCODE_HTML.read_text()
    soup = BeautifulSoup(html_content, "html.parser")
    containers = soup.find_all("div", class_=PROBLEM_CONTAINER_CLASS)

    titles = []
    for container in containers:
        title_div = container.find("div", class_="truncate")
        titles.append(title_div.text if title_div else "No title found")

    return titles


@app.command("prep")
def prep(
    difficulty: str = typer.Option(
        "R", "--difficulty", "-d", help="Difficulty: E (easy), M (medium), H (hard), or R (random)."
    ),
):
    """Print a behavioral prompt, a technical prompt, and a random Leetcode question."""
    difficulty = difficulty.upper()
    if difficulty not in {"E", "M", "H", "R"}:
        typer.echo("❌ Invalid difficulty. Choose one of: E, M, H, R.")
        raise typer.Exit(code=1)

    resolved_difficulty = resolve_difficulty(difficulty)

    typer.echo(
        "Behavioral Prompt: You are a non-technical hiring manager. "
        "Please give me a random behavioral interview question."
    )
    typer.echo()
    typer.echo(
        "Technical Question Prompt: You are an experienced data engineering. "
        f"Please give me a {resolved_difficulty} difficulty interview question. "
        "Also give me what you would expect as a good answer."
    )
    typer.echo()

    titles = get_problem_titles()
    title = random.choice(titles)
    typer.echo(f"Leetcode Question: Please walk through question {title}")
