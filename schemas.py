# schemas.py
from pydantic import BaseModel, validator
from typing import List
from datetime import datetime

class FreelancerBase(BaseModel):
    full_name: str
    phone_number: str
    skills: List[str]
    status: str = "available"

    @validator("phone_number")
    def check_phone(cls, v):
        if not v.startswith("+998"):
            raise ValueError("Telefon raqam +998 bilan boshlanishi kerak")
        return v

    @validator("skills")
    def check_skills(cls, v):
        if not v:
            raise ValueError("Kamida bitta skill bo‘lishi kerak")
        return v

    @validator("status")
    def check_status(cls, v):
        if v not in ["available", "busy", "on_leave"]:
            raise ValueError("Noto‘g‘ri status")
        return v

class FreelancerCreate(FreelancerBase):
    pass

class FreelancerUpdate(FreelancerBase):
    pass

class FreelancerStatusUpdate(BaseModel):
    status: str

    @validator("status")
    def check_status(cls, v):
        if v not in ["available", "busy", "on_leave"]:
            raise ValueError("Noto‘g‘ri status")
        return v

class FreelancerOut(FreelancerBase):
    id: int
    joined_at: datetime

    class Config:
        orm_mode = True
