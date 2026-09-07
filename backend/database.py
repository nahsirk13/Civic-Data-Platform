from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------------------------
# DATABASE_URL: the connection string SQLAlchemy uses to find and log
# into your Postgres database.
#
# Format:  postgresql://<username>:<password>@<host>:<port>/<database_name>
#
#   postgres   -> the username (Postgres superuser you connected as)
#   poop123    -> the password you set with ALTER USER
#   localhost  -> the database is running on your own machine
#   5432       -> Postgres's default port
#   civic_data -> the specific database you created with CREATE DATABASE
#
# NOTE: hardcoding a password directly in code like this is NOT best
# practice for real projects — normally this would come from an
# environment variable so secrets never live in your source code /
# git repo. Fine for a local learning project, worth mentioning you
# know this in an interview.
# --------------------------------------------------------------------
DATABASE_URL = "postgresql://postgres:poop123@localhost:5432/civic_data"

# --------------------------------------------------------------------
# engine: SQLAlchemy's core connection manager.
# It doesn't open a connection immediately — think of it as a
# reusable pipeline that knows HOW to connect whenever something
# actually needs to talk to the database.
# --------------------------------------------------------------------
engine = create_engine(DATABASE_URL)

# --------------------------------------------------------------------
# SessionLocal: a factory for creating "sessions."
# A session = one conversation with the database (run some queries,
# maybe insert/update data, then close it).
#
#   autocommit=False -> changes are NOT saved automatically; you must
#                        call .commit() yourself. Gives you control
#                        over exactly when writes actually happen.
#   autoflush=False   -> SQLAlchemy won't auto-sync pending changes to
#                        the DB before every query; again, more control,
#                        fewer surprise writes.
# --------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------------------------
# Base: the parent class all your models inherit from.
# e.g. `class Representative(Base):` in models/representative.py
# This is what tells SQLAlchemy "this Python class represents an
# actual table in the database."
# --------------------------------------------------------------------
Base = declarative_base()