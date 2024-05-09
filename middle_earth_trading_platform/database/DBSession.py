# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from middle_earth_trading_platform.Configuration import *

# Database configuration
# SQLALCHEMY_DATABASE_URL = "mysql://root:root123@localhost/market"
SQLALCHEMY_DATABASE_URL = f"{db_name}://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_schema}"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker object
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()
