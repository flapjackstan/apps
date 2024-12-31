"""Analyze a dividend stock."""
import argparse

import pandas as pd
import yfinance as yf


def parse_args() -> argparse.Namespace:
    """Parse args base."""
    parser = argparse.ArgumentParser(
        description="Get up to the last 20 years of annual dividend amounts and growth rates.",
        epilog="Useful for evaluating a stock for a mid to long term trade.",
        usage="python dividends.py TGT",
    )

    # Define arguments
    parser.add_argument("ticker", type=str, help="The stock ticker symbol")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("--version", action="version", version="1.0")

    return parser.parse_args()


def get_annual_dividends(ticker: str) -> dict[int, float]:
    """
    Get the annual dividend amounts for the last 20 years for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns
    -------
        Dict[int, float]: A dictionary with years as keys and aggregated annual dividend amounts as values.
    """
    stock = yf.Ticker(ticker)
    dividends = stock.dividends

    if dividends.empty:
        return {}

    # Ensure last_20_years is timezone-aware to match dividends index
    last_20_years = pd.Timestamp.now(tz=dividends.index.tz) - pd.DateOffset(years=20)
    dividends = dividends[dividends.index >= last_20_years]

    # Aggregate dividends by year
    annual_dividends = dividends.groupby(dividends.index.year).sum().to_dict()

    return annual_dividends


def calculate_growth_rate(annual_dividends: dict[int, float]) -> dict[int, float]:
    """
    Calculate the year-by-year growth rate of annual dividends.

    Args:
    annual_dividends (Dict[int, float]): A dict with years as keys and aggregated annual dividend amounts as values.

    Returns
    -------
    Dict[int, float]: A dictionary with years as keys and growth rates as values.
    """
    years = sorted(annual_dividends.keys())
    growth_rates = {}

    for i in range(1, len(years)):
        previous_year = years[i - 1]
        current_year = years[i]
        previous_amount = annual_dividends[previous_year]
        current_amount = annual_dividends[current_year]

        if previous_amount > 0:
            growth_rate = ((current_amount - previous_amount) / previous_amount) * 100
        else:
            growth_rate = None

        growth_rates[current_year] = growth_rate

    return growth_rates


def format_output(annual_dividends: dict[int, float], growth_rates: dict[int, float]) -> None:
    """
    Format and print the annual dividends and growth rates with custom formatting.

    Args:
    annual_dividends (Dict[int, float]): A dict with years as keys and aggregated annual dividend amounts as values.
    growth_rates (Dict[int, float]): A dict with years as keys and growth rates as values.
    """
    for year in sorted(annual_dividends.keys()):
        dividend = annual_dividends[year]
        growth_rate = growth_rates.get(year)

        # Format dividend
        dividend_str = f"${dividend:.2f}"

        # Format growth rate
        if growth_rate is not None:
            growth_rate_str = f"{growth_rate:.2f}%"
            if growth_rate > 0:
                growth_rate_str = f"\033[92m{growth_rate_str}\033[0m"  # Green for positive
            elif growth_rate < 0:
                growth_rate_str = f"\033[91m{growth_rate_str}\033[0m"  # Red for negative
        else:
            growth_rate_str = "N/A"

        print(f"Year: {year}, Dividend: {dividend_str}, Growth Rate: {growth_rate_str}")


def main() -> None:
    """Run main script."""
    args = parse_args()

    ticker = args.ticker

    annual_dividends = get_annual_dividends(ticker)

    if not annual_dividends:
        print(f"No dividend information available for {ticker}.")
    else:
        growth_rates = calculate_growth_rate(annual_dividends)
        format_output(annual_dividends, growth_rates)


if __name__ == "__main__":
    main()
