"""Tests for the interview app."""

from apps.interview import get_problem_titles, resolve_difficulty


def test_resolve_difficulty_maps_codes_to_names():
    """Fixed difficulty codes map to their full name."""
    assert resolve_difficulty("E") == "easy"
    assert resolve_difficulty("M") == "medium"
    assert resolve_difficulty("H") == "hard"


def test_resolve_difficulty_random_picks_a_real_difficulty(mocker):
    """Random difficulty resolves through random.choice to a real difficulty."""
    mocker.patch("apps.interview.random.choice", return_value="H")

    assert resolve_difficulty("R") == "hard"


def test_get_problem_titles_parses_bundled_asset():
    """The bundled Leetcode export yields 50 non-empty problem titles."""
    titles = get_problem_titles()

    assert len(titles) == 50
    assert all(title and title != "No title found" for title in titles)
