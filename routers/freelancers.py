# routers/freelancers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/freelancers", tags=["Freelancers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.FreelancerOut)
def create_freelancer(f: schemas.FreelancerCreate, db: Session = Depends(get_db)):
    freelancer = models.Freelancer(
        full_name=f.full_name,
        phone_number=f.phone_number,
        skills=",".join(f.skills),
        status=f.status
    )
    db.add(freelancer)
    db.commit()
    db.refresh(freelancer)
    return freelancer

@router.get("/", response_model=list[schemas.FreelancerOut])
def list_freelancers(db: Session = Depends(get_db)):
    data = db.query(models.Freelancer).all()
    for f in data:
        f.skills = f.skills.split(",")
    return data

@router.get("/{id}", response_model=schemas.FreelancerOut)
def get_freelancer(id: int, db: Session = Depends(get_db)):
    f = db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Topilmadi")
    f.skills = f.skills.split(",")
    return f

@router.get("/skill/{skill}", response_model=list[schemas.FreelancerOut])
def filter_by_skill(skill: str, db: Session = Depends(get_db)):
    data = db.query(models.Freelancer).filter(models.Freelancer.skills.like(f"%{skill}%")).all()
    for f in data:
        f.skills = f.skills.split(",")
    return data

@router.put("/{id}/status", response_model=schemas.FreelancerOut)
def update_status(id: int, update: schemas.FreelancerStatusUpdate, db: Session = Depends(get_db)):
    f = db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Topilmadi")
    f.status = update.status
    db.commit()
    db.refresh(f)
    f.skills = f.skills.split(",")
    return f

@router.put("/{id}", response_model=schemas.FreelancerOut)
def update_freelancer(id: int, update: schemas.FreelancerUpdate, db: Session = Depends(get_db)):
    f = db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Topilmadi")
    f.full_name = update.full_name
    f.phone_number = update.phone_number
    f.skills = ",".join(update.skills)
    f.status = update.status
    db.commit()
    db.refresh(f)
    f.skills = f.skills.split(",")
    return f

@router.delete("/{id}")
def delete_freelancer(id: int, db: Session = Depends(get_db)):
    f = db.query(models.Freelancer).filter(models.Freelancer.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Topilmadi")
    db.delete(f)
    db.commit()
    return {"message": "Freelancer o‘chirildi"}
