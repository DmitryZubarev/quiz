from sqlalchemy.orm import registry
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey

engine = create_engine("postgresql+psycopg2://postgres:Dc028ed7_@localhost/quiz")
mapper_registry = registry()

session_table = Table(
    "session",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)
