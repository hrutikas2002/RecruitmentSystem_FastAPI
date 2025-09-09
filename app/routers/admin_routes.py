from fastapi import APIRouter, Depends, HTTPException
from app.auth import require_role
from app.crud import get_all_candidates
from app.deps import to_str_list
from app.database import db

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role("admin"))])

@router.get("/candidates", summary="Admin: list all candidates")
async def list_candidates():
    cand = await get_all_candidates()
    return to_str_list(cand)

@router.get("/resume/{candidate_email}", summary="Admin: get a candidate resume URL")
async def view_resume(candidate_email: str):
    candidate = await db.candidates.find_one({"email": candidate_email})
    if not candidate or not candidate.get("resume_url"):
        raise HTTPException(status_code=404, detail="Candidate or resume not found")
    return {"candidate_email": candidate_email, "resume_url": candidate["resume_url"]}
