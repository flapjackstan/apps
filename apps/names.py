
"""Generate a random themed string using Typer."""

from __future__ import annotations

import random
from typing import TypeVar
import os
from io import StringIO

from dotenv import load_dotenv
from ansible_vault import Vault
import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from assets.sqlite_models import Rappers, Simpsons

app = typer.Typer(help="Fetch random records from a themed SQLite database.")

Base = declarative_base()
T = TypeVar("T", bound=Base)


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


# named rando because calling it random confuses the python namespace
@app.command()
def rando(
    db_name: str = typer.Argument(
        ...,
        help="Name of the database to use (either 'rappers' or 'simpsons').",
    ),
    num_records: int = typer.Argument(
        ...,
        help="Number of records to return.",
    ),
    password: str = typer.Option(
        ...,
        prompt=True,
        help="Password for yaml",
    ),
) -> None:
    """
    Fetch random records from the specified database.

    Args:
        db_name (str): Name of the database (either 'rappers' or 'simpsons').
        num_records (int): Number of records to return.
    """
    vault = Vault(password)
    data = vault.load(open("env.yaml").read())
    engine = create_engine(data.get("SQLITE_CONNECTION_STRING"))
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    if db_name == "rappers":
        model = Rappers
    elif db_name == "simpsons":
        model = Simpsons
    else:
        typer.echo("❌ Invalid database name. Choose either 'rappers' or 'simpsons'.")
        raise typer.Exit(code=1)

    records = get_random_records(session, model, num_records)
    for record in records:
        typer.echo(record.name)

