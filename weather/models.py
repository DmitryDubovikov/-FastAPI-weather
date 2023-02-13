from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    Table,
    DateTime,
    Float,
)

metadata = MetaData()

city = Table(
    "city",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column("name", String, nullable=False),
)

weather = Table(
    "weather",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("city_id", ForeignKey("city.id"), nullable=False),
    Column("time", DateTime, server_default=func.now(), nullable=False),
    Column("temperature", Float),
    Column("pressure", Integer),
    Column("wind", Float),
)
