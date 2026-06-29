from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import make_url

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/student_db"

# If the Postgres database doesn't exist, try to create it using the 'postgres' maintenance DB.
try:
    url = make_url(SQLALCHEMY_DATABASE_URL)
    target_db = url.database
    admin_url = url.set(database="postgres")
    admin_engine = create_engine(admin_url)
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": target_db}
        ).scalar()
        if not exists:
            # CREATE DATABASE must run outside a transaction: open a separate
            # autocommit connection for the CREATE DATABASE statement.
            with admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn2:
                conn2.execute(text(f'CREATE DATABASE "{target_db}"'))
            print(f"Created database: {target_db}")
    admin_engine.dispose()
except Exception as e:
    # If we can't reach Postgres or can't create the DB, warn and continue.
    print("Warning: could not verify/create database:", e)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()