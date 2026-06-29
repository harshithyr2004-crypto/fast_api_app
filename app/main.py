from fastapi import FastAPI

from routers import company, job
from database import Base, engine, SessionLocal
from models import company as company_model, job as job_model

app = FastAPI()
print("engine is:", engine)

def seed_company_data():
    with SessionLocal() as db:
        if not db.query(company_model.Company).filter(company_model.Company.id == 10).first():
            db_company = company_model.Company(
                id=10,
                name="Seed Company 10",
                email="seed10@example.com",
                phone="0000000000",
            )
            db.add(db_company)
            db.commit()

try:
    Base.metadata.create_all(bind=engine)
    seed_company_data()
except Exception as e:
    print("Warning: could not create database tables at startup:", e)
app.include_router(company.router)
app.include_router(job.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def read_about():
    return {"about": "This is about page"}

@app.get("/contact")
def read_contact():
    return {"contact": "This is contact page"}