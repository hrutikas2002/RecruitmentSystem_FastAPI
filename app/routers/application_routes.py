from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.auth import get_current_user, require_role
from app.models import Application
from app.crud import get_job, create_application, list_my_applications, list_all_applications
from app.deps import to_str_list

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/jobs/{job_id}/apply", summary="Candidate: apply to a job")
async def apply(job_id: str, current=Depends(get_current_user)):
    if current.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")
    if not ObjectId.is_valid(job_id):
        raise HTTPException(status_code=400, detail="Invalid job_id")
    job = await get_job(job_id)
    if not job or job.get("status") != "Open":
        raise HTTPException(status_code=400, detail="Job not open or not found")
    await create_application(Application(candidate_email=current["email"], job_id=str(job["_id"])))
    return {"message": "Application submitted"}

@router.get("/me", summary="Candidate: my applications")
async def my_apps(current=Depends(get_current_user)):
    if current.get("role") != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates")
    apps = await list_my_applications(current["email"])
    return to_str_list(apps)

@router.get("/all", dependencies=[Depends(require_role("admin"))], summary="Admin: all applications")
async def all_apps():
    apps = await list_all_applications()
    return to_str_list(apps)
