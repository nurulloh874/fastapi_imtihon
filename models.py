# models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Freelancer(Base):
    __tablename__ = "freelancers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    skills = Column(String, nullable=False)  # ["Python,Django"] ko‘rinishida saqlanadi
    status = Column(String, default="available")
    joined_at = Column(DateTime, default=datetime.utcnow)
