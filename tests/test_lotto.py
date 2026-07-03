"""Tests for the lotto app."""

from apps.lotto import randomize_selection_order


def test_randomize_selection_order_includes_all_names_once():
    """Every name is selected exactly once, in some order."""
    names = ["red", "rza", "gza", "ol'dirty", "ghostface"]

    order = randomize_selection_order(names)

    assert sorted(order) == sorted(names)
    assert len(order) == len(names)


def test_randomize_selection_order_does_not_mutate_input():
    """The input list is left untouched."""
    names = ["red", "rza", "gza"]

    randomize_selection_order(names, shuffle=True)

    assert names == ["red", "rza", "gza"]
