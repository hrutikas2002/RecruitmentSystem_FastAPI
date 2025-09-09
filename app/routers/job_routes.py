from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.schemas import JobCreate, JobUpdate
from app.models import Job
from app.crud import create_job, update_job, get_all_jobs, get_job
from app.auth import require_role
from app.deps import to_str_list, to_str_id

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("", summary="List jobs (all)")
async def list_jobs():
    jobs = await get_all_jobs()
    return to_str_list(jobs)

@router.post("", dependencies=[Depends(require_role("admin"))], summary="Admin: create job")
async def post_job(job: JobCreate):
    # validate status
    if job.status and job.status not in ("Open", "Closed", "Filled"):
        raise HTTPException(status_code=422, detail="Invalid status")
    await create_job(Job(**job.dict()))
    return {"message": "Job created"}

@router.put("/{job_id}", dependencies=[Depends(require_role("admin"))], summary="Admin: update job")
async def update_job_endpoint(job_id: str, patch: JobUpdate):
    if patch.status and patch.status not in ("Open", "Closed", "Filled"):
        raise HTTPException(status_code=422, detail="Invalid status")
    if not ObjectId.is_valid(job_id):
        raise HTTPException(status_code=400, detail="Invalid job_id")
    await update_job(job_id, patch.dict(exclude_unset=True))
    return {"message": "Job updated"}

@router.get("/{job_id}", summary="Get a job by id")
async def get_job_by_id(job_id: str):
    job = await get_job(job_id)
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    return to_str_id(job)
