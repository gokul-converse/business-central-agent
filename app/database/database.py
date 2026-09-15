from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.settings import settings

DATABASE_URL = (                    # We're telling SQLAlchemy: This is the PostgreSQL database I want you to connect to
    f"postgresql+psycopg://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

engine = create_engine(DATABASE_URL)                                        # creates the SQLAlchemy engine. Think of the engine as the connection manager between: SQL ALCHEMY and the Postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass