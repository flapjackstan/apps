"""Get next federal holiday."""

from datetime import datetime

import holidays


def get_next_federal_holiday() -> str:
    """
    Retrieve the next federal holiday in the US.

    Its day of the week, and the number of days until that date.
    """
    # Get US federal holidays for the current year
    us_holidays = holidays.US(years=datetime.now().year)

    # Get today's date
    today = datetime.today().date()

    # Find the next holiday
    next_holiday = min(date for date in us_holidays.keys() if date > today)

    # Get the day of the week
    day_of_week = next_holiday.strftime("%A")

    # Calculate the number of days until the next holiday
    days_until_holiday = (next_holiday - today).days

    return (
        f"The next federal holiday is {next_holiday} ({day_of_week}) - "
        f"{us_holidays[next_holiday]}. It is in {days_until_holiday} days."
    )


def main():
    """
    Print the next federal holiday.

    Its day of the week and the number of days until that date.
    """
    print(get_next_federal_holiday())


if __name__ == "__main__":
    main()
