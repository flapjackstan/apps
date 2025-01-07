"""Interview with a friend."""

import argparse
import random

from bs4 import BeautifulSoup


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Interactive or command-line interview question processor.",
        epilog="Thank you for trying out this interactive script!",
        usage="python app.py --difficulty R",
    )

    # Define arguments (including the new interactive mode flag)
    parser.add_argument("--version", action="version", version="1.0")
    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["E", "M", "H", "R"],
        help="Options: E for easy, M for medium, H for hard, R for random",
    )

    return parser.parse_args()


def main():
    """Run script."""
    args = parse_args()

    difficulty = args.difficulty

    if difficulty == "R":
        difficulty = random.choice(["E", "M", "H"])

    if difficulty == "E":
        difficulty = "easy"
    if difficulty == "M":
        difficulty = "medium"
    if difficulty == "H":
        difficulty = "hard"

    print(
        "Behavioral Prompt: You are a non-technical hiring manager. Please give me a random behavioral interview question."  #  noqa: E501
    )
    print()
    print(
        f"Technical Question Prompt: You are an experienced data scientist. Please give me a {difficulty} difficulty interview question. Also give me what you would expect as a good answer."  #  noqa: E501
    )
    print()

    # copied and pasted html and then formatted here
    # https://www.freeformatter.com/html-formatter.html
    # not sure why but requests wasnt working for me
    with open("./assets/formatted_leetcode.html") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    problem_containers = soup.find_all(
        "div",
        class_="flex flex-col border-b-[1.5px] duration-300 last:border-b-0 border-lc-fill-02 dark:border-dark-lc-fill-02 hover:bg-lc-fill-02 dark:hover:bg-dark-lc-fill-02 cursor-pointer",  #  noqa: E501
    )

    problem_dict = {}
    for i, container in enumerate(problem_containers, start=1):
        title_div = container.find("div", class_="truncate")
        title = title_div.text if title_div else "No title found"

        problem_dict[i] = {"Title": title}

    print(f"Leetcode Question: Please walk through question {problem_dict[random.randint(1, 50)]}")


if __name__ == "__main__":
    main()
