"""Generate a random themed string."""

from __future__ import annotations

import argparse
import random
from typing import TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from assets.sqlite_models import Rappers, Simpsons

Base = declarative_base()
T = TypeVar("T", bound=Base)


def parse_args() -> argparse.Namespace:
    """Parse args."""
    parser = argparse.ArgumentParser(
        description="Fetch random records from the database."
    )
    parser.add_argument(
        "db_name",
        type=str,
        help="Name of the database to use (either 'rappers' or 'simpsons').",
    )
    parser.add_argument("num_records", type=int, help="Number of records to return.")
    return parser.parse_args()


def get_random_records(session: Session, model: type[T], num_records: int) -> list[T]:
    """
    Get random records from the specified model.

    Args:
        session (Session): SQLAlchemy session.
        model (Type[T]): SQLAlchemy model class.
        num_records (int): Number of records to return.

    Returns
    -------
        List[T]: List of random records.
    """
    records = session.query(model).all()
    return random.sample(records, min(num_records, len(records)))


def main(db_name: str, num_records: int) -> None:
    """
    Fetch random records from the specified database.

    Args:
        db_name (str): Name of the database (either 'rappers' or 'simpsons').
        num_records (int): Number of records to return.
    """
    engine = create_engine("sqlite:////Users/elmer/Documents/dev/apps/assets/names.db")
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    if db_name == "rappers":
        model = Rappers
    elif db_name == "simpsons":
        model = Simpsons
    else:
        raise ValueError(
            "Invalid database name. Choose either 'rappers' or 'simpsons'."
        )

    records = get_random_records(session, model, num_records)
    for record in records:
        print(record.name)


if __name__ == "__main__":
    args = parse_args()
    main(args.db_name, args.num_records)
