from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId): return v
        return ObjectId(str(v))

# Stored as documents
class Candidate(BaseModel):
    email: EmailStr
    password: str
    name: str
    resume_url: Optional[str] = None
    role: str = "candidate"

class Admin(BaseModel):
    email: EmailStr
    password: str
    role: str = "admin"

class Job(BaseModel):
    title: str
    description: str
    department: str
    location: str
    employment_type: str
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    required_skills: List[str]
    additional_info: Optional[str] = None
    status: str = "Open"   # Open | Closed | Filled

class Application(BaseModel):
    candidate_email: EmailStr
    job_id: str
    status: str = "Applied"   # Applied | Shortlisted | Rejected | Hired
    applied_at: datetime = Field(default_factory=datetime.utcnow)