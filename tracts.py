"""
Tool to download census tract data with the assumption that data gets put on postgres and is overwritten when a new variable is included.

Good Census Related Reads
https://www2.census.gov/geo/tiger/
https://pypi.org/project/census/
https://learn.arcgis.com/en/related-concepts/united-states-census-geography.htm
https://www.census.gov/newsroom/blogs/random-samplings/2014/07/understanding-geographic-relationships-counties-places-tracts-and-more.html
https://www.census.gov/data/developers/data-sets/acs-5year.html
https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
https://api.census.gov/data/2022/acs/acs5/variables.html

TODO:
- argparse only takes in year, state, and county
- hardcoded census variables with intuitive way on how to add to it
- double check if theres a way to add like a post_init to argparse.Namespace creation that can do so cleaning and transformations

"""

import argparse
import csv
import os
from dataclasses import dataclass, field

import requests
from census import Census
from dotenv import load_dotenv
from geopandas import GeoDataFrame, read_file
from pandas import DataFrame, merge

load_dotenv()

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")
CENSUS_VARIABLES = {
    "ACS": {
        "median_age": "B01002_001E",
        "total_population": "B01003_001E",
    },
    "Subject": {
        "median_income": "S1901_C01_012E",
    },
}


@dataclass
class Fips:
    state: str
    county: str


@dataclass
class CensusMiddleWare:
    raw_input: argparse.Namespace
    variables: dict

    key: str = CENSUS_API_KEY

    fips: Fips = field(init=False)

    def __post_init__(self):
        # clean and validate
        pass
        # derived
        self.fips = self.get_state_county_fips_using_county_name(self.raw_input.county)

    # static because it doesnt need access to class attributes or instance attributes but still used in context of Census stuff.
    @staticmethod
    def get_state_county_fips_using_county_name(county: str) -> Fips:
        """
        Function to return a dict of FIPS codes (keys) of U.S. counties (values).

        https://gist.github.com/cjwinchester/a8ff5dee9c07d161bdf4
        """
        r = requests.get("http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt")
        reader = csv.reader(r.text.splitlines(), delimiter=",")
        for line in reader:
            if county == line[3].replace(" County", ""):
                return Fips(state=line[1], county=line[2])

        raise Exception("County Not Found.")


class CensusDownloader:
    """
    A class for downloading census data and geography information.

    Args:
        input (CensusMiddleWare): An instance of the CensusMiddleWare class.

    Attributes
    ----------
        api (Census): An instance of the Census class.
        input (CensusMiddleWare): The input object.

    Methods
    -------
        get_geography(): Retrieves the geography data for a specific county.
        get_census(): Fetches census data based on the specified variables and returns a DataFrame.
        get_data(): Retrieves data from geography and census sources, merges them, and saves the result as a GeoJSON file.
    """

    def __init__(self, input: CensusMiddleWare) -> None:
        self.api = Census(input.key)
        self.input = input

    def get_geography(self) -> GeoDataFrame:
        """
        Retrieve the geography data for a specific county.

        Returns
        -------
            GeoDataFrame: The geography data for the county.
        """
        ca_tracts = read_file(
            f"https://www2.census.gov/geo/tiger/TIGER{self.input.raw_input.year}/TRACT/tl_{self.input.raw_input.year}_{self.input.fips.state}_tract.zip"
        )
        county_tracts = ca_tracts.query("COUNTYFP == @self.input.fips.county")  # using @ is like f-strings

        county_tracts["TOTAL_AREA_SQMETER"] = county_tracts["ALAND"] + county_tracts["AWATER"]
        county_tracts["CENTROID_LONG"] = county_tracts.centroid.x
        county_tracts["CENTROID_LAT"] = county_tracts.centroid.y

        return county_tracts

    def get_census(self) -> DataFrame:
        """
        Fetch census data based on the specified variables and returns a DataFrame.

        Returns
        -------
            DataFrame: The census data as a pandas DataFrame.
        """
        for key, value in self.input.variables.items():
            if key == "ACS":
                print("Fetching ACS Data")
                variables = [v for k, v in value.items()]
                acs_data = DataFrame(
                    self.api.acs5.state_county_tract(
                        fields=variables,
                        state_fips=self.input.fips.state,
                        county_fips=self.input.fips.county,
                        tract="*",
                        year=int(self.input.raw_input.year),
                    )
                )

            if key == "Subject":
                print("Fetching Subject Data")
                variables = [v for k, v in value.items()]
                subject_data = DataFrame(
                    self.api.acs5st.state_county_tract(
                        fields=variables,
                        state_fips=self.input.fips.state,
                        county_fips=self.input.fips.county,
                        tract="*",
                        year=self.input.raw_input.year,
                    )
                )

        data = merge(acs_data, subject_data, on=["state", "county", "tract"])
        snake_names = [key for inner_dict in CENSUS_VARIABLES.values() for key in inner_dict.keys()]
        source_names = [key for inner_dict in CENSUS_VARIABLES.values() for key in inner_dict.values()]
        rename_dict = dict(zip(source_names, snake_names))
        return data.rename(columns=rename_dict)

    def get_data(self) -> None:
        """
        Retrieve data from the geography and census sources, merges them, and saves the result as a GeoJSON file.

        Returns
        -------
            None
        """
        geography = self.get_geography()
        census_data = self.get_census()

        join = merge(geography, census_data, left_on="TRACTCE", right_on="tract", how="inner")
        join = GeoDataFrame(join)
        join.to_file(
            "output.geojson",
            driver="GeoJSON",
        )


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    p = argparse.ArgumentParser(
        description="Download census tract data to a geojson file.",
        usage="python tracts.py --state 'CA' --county 'Los Angeles' --year 2021",
        epilog="Uses Tiger and Census API",
    )
    p.add_argument("--state", type=str, required=True, help="state in which tracts are in.")
    p.add_argument("--county", type=str, required=True, help="county in which tracts are in.")
    p.add_argument("--year", type=str, required=True, help="year for BOTH data and geography.")
    return p.parse_args()


def main():
    """Run script as an app."""
    args = parse_args()
    cm = CensusMiddleWare(raw_input=args, variables=CENSUS_VARIABLES)
    downloader = CensusDownloader(cm)
    downloader.get_data()


if __name__ == "__main__":
    main()
