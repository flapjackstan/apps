"""Tests for the tracts app."""

import pytest

from apps.tracts import CensusMiddleWare, Fips

# Format of national_county.txt: STATE,STATEFP,COUNTYFP,COUNTYNAME,CLASSFP
FAKE_COUNTY_FILE = "\n".join(
    [
        "AL,01,001,Autauga County,H1",
        "CA,06,037,Los Angeles County,H1",
        "CA,06,073,San Diego County,H1",
    ]
)


def test_fips_lookup_returns_state_and_county(mocker):
    """A known county name resolves to its state and county FIPS codes."""
    mocker.patch("apps.tracts.requests.get", return_value=mocker.Mock(text=FAKE_COUNTY_FILE))

    fips = CensusMiddleWare.get_state_county_fips_using_county_name("Los Angeles")

    assert fips == Fips(state="06", county="037")


def test_fips_lookup_raises_for_unknown_county(mocker):
    """An unrecognized county name raises a ValueError."""
    mocker.patch("apps.tracts.requests.get", return_value=mocker.Mock(text=FAKE_COUNTY_FILE))

    with pytest.raises(ValueError, match="Nonexistent"):
        CensusMiddleWare.get_state_county_fips_using_county_name("Nonexistent")
