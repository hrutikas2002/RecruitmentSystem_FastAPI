from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth / common
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Candidate
class CandidateCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class CandidateLogin(BaseModel):
    email: EmailStr
    password: str

class CandidateResponse(BaseModel):
    email: EmailStr
    name: str
    resume_url: Optional[str] = None
    role: str

class ResumeUpload(BaseModel):
    email: EmailStr

# Admin
class AdminCreate(BaseModel):
    email: EmailStr
    password: str

# Jobs
class JobCreate(BaseModel):
    title: str
    description: str
    department: str
    location: str
    employment_type: str
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: List[str]
    additional_info: Optional[str] = None
    status: Optional[str] = "Open"

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: Optional[List[str]] = None
    additional_info: Optional[str] = None
    status: Optional[str] = None

# Applications
class ApplicationResponse(BaseModel):
    candidate_email: EmailStr
    job_id: str
    status: str
    applied_at: datetime
