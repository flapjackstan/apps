"""Test dates app."""

import pytest

from dates import calculate_days_between, get_date_from


def test_get_date_from_forward():
    """Test dates forward."""
    assert get_date_from("2024-05-28", 70, "forward") == "2024-08-06"
    assert get_date_from("2024-12-31", 1, "forward") == "2025-01-01"


def test_get_date_from_back():
    """Test dates back."""
    assert get_date_from("2024-05-28", 70, "back") == "2024-03-19"
    assert get_date_from("2024-01-01", 1, "back") == "2023-12-31"


def test_get_date_from_invalid_direction():
    """Test dates invalid."""
    with pytest.raises(
        ValueError, match="Invalid direction. Please use 'back' or 'forward'."
    ):
        get_date_from("2024-05-28", 70, "sideways")


def test_calculate_days_between():
    """Test dates between."""
    assert calculate_days_between("2024-05-28", "2024-08-06") == 70
    assert calculate_days_between("2024-08-06", "2024-05-28") == -70
    assert calculate_days_between("2024-01-01", "2024-01-01") == 0


if __name__ == "__main__":
    pytest.main()
