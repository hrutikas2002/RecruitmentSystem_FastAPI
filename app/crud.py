from typing import List, Optional
from bson import ObjectId
from app.database import db
from app.models import Candidate, Admin, Job, Application

# Users
async def get_user_by_email(email: str) -> Optional[dict]:
    user = await db.candidates.find_one({"email": email})
    if user: return user
    return await db.admins.find_one({"email": email})

async def create_candidate(candidate: Candidate):
    return await db.candidates.insert_one(candidate.dict())

async def create_admin(admin: Admin):
    return await db.admins.insert_one(admin.dict())

# Jobs
async def create_job(job: Job):
    return await db.jobs.insert_one(job.dict())

async def update_job(job_id: str, patch: dict):
    return await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": patch})

async def get_job(job_id: str) -> Optional[dict]:
    return await db.jobs.find_one({"_id": ObjectId(job_id)})

async def get_all_jobs(limit: int = 100) -> List[dict]:
    return await db.jobs.find().to_list(limit)

# Candidates
async def get_all_candidates(limit: int = 200) -> List[dict]:
    return await db.candidates.find().to_list(limit)

async def update_candidate_resume(email: str, resume_url: str):
    return await db.candidates.update_one({"email": email}, {"$set": {"resume_url": resume_url}})

# Applications
async def create_application(app: Application):
    return await db.applications.insert_one(app.dict())

async def list_my_applications(candidate_email: str) -> List[dict]:
    return await db.applications.find({"candidate_email": candidate_email}).to_list(200)

async def list_all_applications() -> List[dict]:
    return await db.applications.find().to_list(500)
