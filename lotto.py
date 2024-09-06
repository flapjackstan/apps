import argparse
import random
def parse_args() -> argparse.Namespace:
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Randomly select names from a list until all are selected.",
        epilog="Thank you for using the random name selector!",
        usage="python lottery.py -n method red rza gza ol'dirty ghostface",
    )

    # Define arguments (including the interactive mode flag)
    parser.add_argument("-n", "--names", help="List of names", type=str, nargs="*", metavar="NAME")
    parser.add_argument("-i", "--interactive", help="Enter interactive mode", action="store_true")
    parser.add_argument("-s", "--shuffle", help="Shuffle the list before selection", action="store_true")
    parser.add_argument("--version", action="version", version="1.0")

    # Parse the arguments
    return parser.parse_args()


def main():
    args = parse_args()
    # Check if we're in interactive mode
    if args.interactive or not args.names:
        print("Entering interactive mode...")
        names_input = input("Enter names separated by spaces: ")
        args.names = names_input.split()
        shuffle_input = input("Shuffle the list before selection? (y/n): ").lower() == 'y'
        args.shuffle = shuffle_input

    # Validate names input
    if not args.names:
        print("No names provided. Exiting.")
        return

    # Optionally shuffle the names
    if args.shuffle:
        random.shuffle(args.names)

    # Randomly select names one at a time
    print("\nRandomly selecting names...")
    selected_names = []
    while args.names:
        selected_name = random.choice(args.names)
        print(f"Selected: {selected_name}")
        selected_names.append(selected_name)
        args.names.remove(selected_name)
        input("Press Enter for next name.")
    
    print("\nAll names have been selected:")
    print(", ".join(selected_names))

if __name__ == "__main__":
    main()
