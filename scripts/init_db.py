from app.database import engine, Base
from app.models.user import User

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    init()