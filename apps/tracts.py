"""
Tool to download census tract data to a GeoJSON file.

Uses the TIGER geography files and the Census API. Requires a CENSUS_API_KEY
in the environment (loaded from a .env file via python-dotenv).

Good Census Related Reads
https://www2.census.gov/geo/tiger/
https://pypi.org/project/census/
https://www.census.gov/data/developers/data-sets/acs-5year.html
https://api.census.gov/data/2022/acs/acs5/variables.html
"""

import csv
import os
from dataclasses import dataclass, field

import requests
import typer
from census import Census
from dotenv import load_dotenv
from geopandas import GeoDataFrame, read_file
from pandas import DataFrame, merge

load_dotenv()

app = typer.Typer(help="Download census tract data to a GeoJSON file.")

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
class TractRequest:
    """User-supplied inputs describing which tracts to download."""

    state: str
    county: str
    year: str


@dataclass
class Fips:
    """Simple dataclass for easy access to FIPS."""

    state: str
    county: str


@dataclass
class CensusMiddleWare:
    """Middleware between the CLI inputs and the actual census app."""

    raw_input: TractRequest
    variables: dict

    key: str = CENSUS_API_KEY

    fips: Fips = field(init=False)

    def __post_init__(self):
        """Clean, validate, and make calculated variables."""
        self.fips = self.get_state_county_fips_using_county_name(self.raw_input.county)

    # static because it doesnt need access to class attributes or instance attributes
    # but still used in context of Census stuff.
    @staticmethod
    def get_state_county_fips_using_county_name(county: str) -> Fips:
        """
        Return the FIPS codes for a U.S. county given its name.

        https://gist.github.com/cjwinchester/a8ff5dee9c07d161bdf4
        """
        r = requests.get("http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt")
        reader = csv.reader(r.text.splitlines(), delimiter=",")
        for line in reader:
            if county == line[3].replace(" County", ""):
                return Fips(state=line[1], county=line[2])

        raise ValueError(f"County '{county}' not found.")


class CensusDownloader:
    """Download census data and geography information and write it to GeoJSON."""

    def __init__(self, app_input: CensusMiddleWare) -> None:
        self.api = Census(app_input.key)
        self.app_input = app_input

    def get_geography(self) -> GeoDataFrame:
        """Retrieve the geography (tract polygons) for the requested county."""
        ca_tracts = read_file(
            f"https://www2.census.gov/geo/tiger/TIGER{self.app_input.raw_input.year}/TRACT/"
            f"tl_{self.app_input.raw_input.year}_{self.app_input.fips.state}_tract.zip"
        )
        county_tracts = ca_tracts.query("COUNTYFP == @self.app_input.fips.county")  # using @ is like f-strings

        county_tracts["TOTAL_AREA_SQMETER"] = county_tracts["ALAND"] + county_tracts["AWATER"]
        county_tracts["CENTROID_LONG"] = county_tracts.centroid.x
        county_tracts["CENTROID_LAT"] = county_tracts.centroid.y

        return county_tracts

    def get_census(self) -> DataFrame:
        """Fetch census data for the requested variables and return a DataFrame."""
        for key, value in self.app_input.variables.items():
            if key == "ACS":
                print("Fetching ACS Data")
                variables = [v for k, v in value.items()]
                acs_data = DataFrame(
                    self.api.acs5.state_county_tract(
                        fields=variables,
                        state_fips=self.app_input.fips.state,
                        county_fips=self.app_input.fips.county,
                        tract="*",
                        year=int(self.app_input.raw_input.year),
                    )
                )

            if key == "Subject":
                print("Fetching Subject Data")
                variables = [v for k, v in value.items()]
                subject_data = DataFrame(
                    self.api.acs5st.state_county_tract(
                        fields=variables,
                        state_fips=self.app_input.fips.state,
                        county_fips=self.app_input.fips.county,
                        tract="*",
                        year=self.app_input.raw_input.year,
                    )
                )

        data = merge(acs_data, subject_data, on=["state", "county", "tract"])
        snake_names = [key for inner_dict in CENSUS_VARIABLES.values() for key in inner_dict.keys()]
        source_names = [key for inner_dict in CENSUS_VARIABLES.values() for key in inner_dict.values()]
        rename_dict = dict(zip(source_names, snake_names))
        return data.rename(columns=rename_dict)

    def get_data(self, output: str = "output.geojson") -> None:
        """Retrieve geography and census data, merge them, and save as GeoJSON."""
        geography = self.get_geography()
        census_data = self.get_census()

        join = merge(geography, census_data, left_on="TRACTCE", right_on="tract", how="inner")
        join = GeoDataFrame(join)
        join.to_file(output, driver="GeoJSON")


@app.command("download")
def download(
    state: str = typer.Option(..., help="State the tracts are in, e.g. 'CA'."),
    county: str = typer.Option(..., help="County the tracts are in, e.g. 'Los Angeles'."),
    year: str = typer.Option(..., help="Year for BOTH data and geography, e.g. '2021'."),
    output: str = typer.Option("output.geojson", help="Path to write the GeoJSON file."),
):
    """Download census tract data for a county to a GeoJSON file."""
    if not CENSUS_API_KEY:
        typer.echo("❌ CENSUS_API_KEY not set. Add it to your .env file.")
        raise typer.Exit(code=1)

    request = TractRequest(state=state, county=county, year=year)
    middleware = CensusMiddleWare(raw_input=request, variables=CENSUS_VARIABLES)
    downloader = CensusDownloader(middleware)
    downloader.get_data(output)
    typer.echo(f"✅ Wrote tract data to {output}")
