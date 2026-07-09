from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="LineSec Core API", lifespan=lifespan)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"database": "connected", "api": "healthy"}

@app.post("/api/ingest")
def ingest_findings(findings: List[schemas.FindingCreate], db: Session = Depends(get_db)):
    db_findings = []
    for finding in findings:
        finding_data = getattr(finding, "model_dump", finding.dict)()
        db_finding = models.Finding(**finding_data)
        db.add(db_finding)
        db_findings.append(db_finding)
    
    db.commit()
    
    for db_finding in db_findings:
        db.refresh(db_finding)
        
    return db_findings
