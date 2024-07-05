"""DDL for random names app."""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///names.db", echo=True)
Base = declarative_base()


class Rappers(Base):
    """Rappers class for orm."""

    __tablename__ = "rappers"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Simpsons(Base):
    """Simpsons class for orm."""

    __tablename__ = "simpsons"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


RAPPERS = [
    "lil-wayne",
    "weezy",
    "jay-z",
    "dmx",
    "kendrick",
    "k-dot",
    "childish-gambino",
    "asap-rocky",
    "j-cole",
    "bas",
    "smino",
]

SIMPSONS = [
    "maggie",
    "marge",
    "lisa",
    "homer",
    "bart",
    "grandpa",
    "selma",
    "patty",
    "jub-jub",
    "quimby",
    "chief-wiggum",
    "ralph",
    "milhouse",
    "nelson",
    "apu",
    "radioactive-man",
    "comicbook-guy",
    "dr-hibert",
    "dr-nick",
    "snake",
]


def main():
    """RUN DDL."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    rappers = [Rappers(name=name) for name in RAPPERS]
    simpsons = [Simpsons(name=name) for name in SIMPSONS]

    session.add_all(rappers)
    session.add_all(simpsons)
    session.commit()

    session.close()


if __name__ == "__main__":
    main()
