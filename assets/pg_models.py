import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Float, ForeignKey, Computed, Index, Integer, String, create_engine, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()


class BaseMixin(BASE):
    """
    Anything that inherits from this will have access to these features.
    @classmethods:   Can be called from the child class template and has access to class attributes.
    @staticmethods:  Can also be called from the child class template but does not have access to class attributes.
    regular methods: Only callable from the class object itself.
    """

    __abstract__ = True  # make it so a user cannot instantiate this as an object

    @classmethod
    def create_from_csv_row(cls, row: dict) -> None:
        """Create address object for instances where we get csv records instead of SnowFlake."""
        pass

    @staticmethod
    def clean_address_component() -> None:
        """Remove unwanted characters or decode stuff."""
        pass

    def to_dict(self):
        """Put field/column as key and content as value."""
        return {field.name: getattr(self, field.name) for field in self.__table__.c}

    def get_field_names(self) -> list:
        """Get a list of field/column names for a table."""
        return self.__table__.c


# Alternative is we can define based on this type of address specs https://usaddress.readthedocs.io/en/latest/
class Address(BaseMixin):
    """
    Declarative DDL for `addresses` table.
    This is the DDL
    """
    __tablename__ = "addresses"
    __table_args__ = (
        Index(
            "unique_address_components",
            func.coalesce(Column("STREET_ADDRESS"), ""),
            func.coalesce(Column("CITY"), ""),
            func.coalesce(Column("STATE"), ""),
            func.coalesce(Column("ZIP"), ""),
            unique=True,
        ),
        {
            "comment": "Address table to store various types of addresses",
            "schema": "public",
        },
    )

    ID = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for the table. Made in house and not from an external source.",
    )
    STREET_ADDRESS = Column(String, nullable=True, comment="Street address component")
    CITY = Column(String, nullable=True, comment="City component")
    STATE = Column(String, nullable=True, comment="State component")
    ZIP = Column(String, nullable=True, comment="Zipcode component")
    SOURCE = Column(
        String,
        nullable=False,
        comment="Source where data is pulled.",
    )
    RAW_CONCAT_ADDRESS = Column(
        String,
        Computed(
            "COALESCE(\"STREET_ADDRESS\", '') || "
            + "COALESCE(\"CITY\", '') || ', ' || COALESCE(\"STATE\", '') || COALESCE(' ' || \"ZIP\", '')",
            persisted=True,
        ),
    )
    
    # an address has a geocoded_address that comes from the GeocodedAddress definition
    geocoded_address = relationship("GeocodedAddress", back_populates="address", uselist=False)


class GeocodedAddress(Address):
    """ORM class for the geocoded_addresses table."""

    __tablename__ = "geocoded_addresses"
    __table_args__ = (
        {
            "comment": "One to one relationship with an address.",
            "schema": "public",
        },
    )

    ID = Column(
        Integer,
        ForeignKey("public.addresses.ID"),
        primary_key=True,
        comment="Same ID as in the addresses table.",
    )

    LATITUDE = Column(Float, nullable=True, comment="Y coordinate.")
    LONGITUDE = Column(Float, nullable=True, comment="X coordinate.")
    GEOCODE_SOURCE = Column(String, nullable=False, comment="Source of the lat longs. Geocoder, Other")

    # A geocoded_address is tied to the Address definition and fills in its geocoded_address
    address = relationship("Address", back_populates="geocoded_address")
#
def main():
    load_dotenv()
    PG_CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')
    engine = create_engine(PG_CONNECTION_STRING, echo=True)
    try:
        engine.connect()
    except SQLAlchemyError as err:
        print("Check if docker is up!", err.__cause__)
    Address.metadata.create_all(engine)


if __name__ == "__main__":
    main()