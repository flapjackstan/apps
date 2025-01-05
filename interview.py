import argparse
import random

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Interactive or command-line interview question processor.",
        epilog="Thank you for trying out this interactive script!",
        usage="python app.py --difficulty R",
    )

    # Define arguments (including the new interactive mode flag)
    parser.add_argument("--version", action="version", version="1.0")
    parser.add_argument("-d", "--difficulty", choices=["E", "M", "H", "R"], help="Options: E for easy, M for medium, H for hard, R for random")

    return parser.parse_args()

def main():
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

    print("Behavioral Prompt: You are a non technical hiring manager. Please give me a random behavioral interview question.")
    print()
    print(f"Technical Question Prompt: You are an experienced data scientist. Please give me a {difficulty} difficulty interview question. Also give me what you would expect as a good answer.")
    print()
    print(f"Leetcode Question: Please walk through question {random.randint(1, 50)}")

if __name__ == "__main__":
    main()