import holidays
from datetime import datetime

def get_next_federal_holiday():
    """
    Retrieve the next federal holiday in the US and its day of the week.

    Returns:
        str: The next federal holiday date, name, and day of the week.
    """
    # Get US federal holidays for the current year
    us_holidays = holidays.US(years=datetime.now().year)

    # Get today's date
    today = datetime.today().date()

    # Find the next holiday
    next_holiday = min(date for date in us_holidays.keys() if date > today)

    # Get the day of the week
    day_of_week = next_holiday.strftime('%A')

    return f"The next federal holiday is {next_holiday} ({day_of_week}) - {us_holidays[next_holiday]}"

def main():
    """
    Main function to print the next federal holiday and its day of the week.
    """
    print(get_next_federal_holiday())

if __name__ == "__main__":
    main()
