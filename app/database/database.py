from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# -------------------------
# Database connection URL
# -------------------------
DATABASE_URL = "postgresql://localuser:mypass@localhost:5433/logistics_db"

# -------------------------
# Engine & Base setup
# -------------------------
engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------
# Context manager for safe connections
# -------------------------
@contextmanager
def get_connection():
    """Yields a DB connection and ensures it is closed after use"""
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()

# -------------------------
# Context manager for sessions (ORM)
# -------------------------
@contextmanager
def get_session():
    """Yields a SQLAlchemy session and ensures it is closed after use"""
    print("starting session")
    session = SessionLocal()
    print("seesion is initaied")
    try:
        print("seesion is starting")
        yield session
        session.commit()  # commits changes if everything is fine
    except Exception:
        session.rollback()  # rollback on error
        raise
    finally:
        session.close()