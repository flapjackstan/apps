"""Calculate days between dates or the date forward or back from a specific date."""

import argparse
import datetime


def get_date_from(date, days, direction):
    """
    Get date days back or forward from input date.

    Parameters
    ----------
    - date (str): String of the date to calculate from
    - days (int): Number of days to go back or forward from the input date
    - direction (str): String indicating whether to move "back" or "forward" from the input date

    Returns
    -------
    - str: Date that is 'days' days before or after the input date, based on the direction
    """
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

    if direction == "back":
        delta = datetime.timedelta(days=-days)
    elif direction == "forward":
        delta = datetime.timedelta(days=days)
    else:
        raise ValueError("Invalid direction. Please use 'back' or 'forward'.")

    new_date = date_obj + delta
    new_date_str = new_date.strftime("%Y-%m-%d")

    return new_date_str


def calculate_days_between(date1, date2):
    """
    Calculate the number of days between two dates.

    Parameters
    ----------
    - date1 (str): The first date in the format YYYY-MM-DD
    - date2 (str): The second date in the format YYYY-MM-DD

    Returns
    -------
    - int: Number of days between date1 and date2
    """
    date_obj1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date_obj2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    delta = date_obj2 - date_obj1

    return delta.days


def main():
    """Calculate days between dates."""
    parser = argparse.ArgumentParser(
        description="Calculate date back or forward from input date or calculate days between two dates",
        epilog='Example: python dates.py "2024-05-28" 70 "forward" OR python dates.py "2024-05-28" "2024-06-28"',
    )
    parser.add_argument("date1", type=str, help="Input date in the format YYYY-MM-DD")
    parser.add_argument(
        "days_or_date2", help="Number of days to go back or forward, or the second date in the format YYYY-MM-DD"
    )
    parser.add_argument(
        "direction", type=str, nargs="?", choices=["back", "forward"], help="Direction to move from the input date"
    )

    args = parser.parse_args()

    try:
        days = int(args.days_or_date2)
        if not args.direction:
            parser.error("Direction must be specified when providing number of days.")
        result_date = get_date_from(args.date1, days, args.direction)
        print(f"{days} days {args.direction} from {args.date1} is: {result_date}")
    except ValueError:
        date2 = args.days_or_date2
        days_between = calculate_days_between(args.date1, date2)
        print(f"The number of days between {args.date1} and {date2} is: {days_between}")


if __name__ == "__main__":
    main()
