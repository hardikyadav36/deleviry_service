from fastapi import FastAPI
from app.database.database import SessionLocal, get_session, get_connection, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text 

app = FastAPI()
# logistic_env\scripts\activate

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

@app.get("/db-test")
def db_test():
    with get_session() as session:
        result = session.execute(text("SELECT 1"))
        return {"db_test": result.scalar()}

@app.get("/users")
def get_users():
    with get_session() as session:
        users = session.query(User).all()
        return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

# ------------------------------
# Get users via raw SQL
# ------------------------------
@app.get("/raw-users")
def get_raw_users():
    with get_connection() as conn:
        result = conn.execute(text("SELECT id, name, email FROM users"))
        return [dict(row) for row in result]