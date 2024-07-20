from typing import Optional, Tuple

import yfinance as yf


def get_stock_dividend_info(ticker: str) -> Tuple[Optional[float], Optional[str]]:
    """
    Get the last dividend amount and payout frequency for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns
    -------
        Tuple[Optional[float], Optional[str]]: The last dividend amount and the payout frequency.
    """
    stock = yf.Ticker(ticker)
    dividends = stock.dividends

    if dividends.empty:
        return None, None

    dividends.index[-1]
    last_dividend_amount = dividends.iloc[-1]

    # Calculate payout frequency
    if len(dividends) > 1:
        dates_diff = dividends.index.to_series().diff().dropna()
        average_diff_days = dates_diff.mean().days

        if average_diff_days < 45:
            frequency = "Monthly"
        elif average_diff_days < 135:
            frequency = "Quarterly"
        elif average_diff_days < 225:
            frequency = "Semi-Annually"
        else:
            frequency = "Annually"
    else:
        frequency = "Unknown"  # Only one dividend in the dataset

    return last_dividend_amount, frequency


def main() -> None:
    """Main function to get user input for stock ticker and display dividend information."""
    ticker = input("Enter the stock ticker symbol: ").strip().upper()
    shares = float(input("Enter the number of shares you own: "))

    dividend, frequency = get_stock_dividend_info(ticker)

    if dividend is None:
        print(f"No dividend information available for {ticker}.")
    else:
        expected_payout = shares * dividend
        print(f"Last Dividend for {ticker}: {dividend}")
        print(f"Payout Frequency: {frequency}")
        print(f"Expected Dividend Payout: {expected_payout}")


if __name__ == "__main__":
    main()
