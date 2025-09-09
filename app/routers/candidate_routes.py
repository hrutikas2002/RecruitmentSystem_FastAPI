import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from pydantic import EmailStr
from app.auth import get_current_user
from app.schemas import ResumeUpload
from app.crud import update_candidate_resume
from app.config import UPLOAD_FOLDER

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("/me", summary="Get my profile")
async def me(current=Depends(get_current_user)):
    return {"email": current["email"], "name": current.get("name"), "role": current.get("role"), "resume_url": current.get("resume_url")}

@router.post("/upload-resume", summary="Upload my resume")
async def upload_resume(
    email: EmailStr = Form(...),
    file: UploadFile = File(...),
    current=Depends(get_current_user)
):
    # Only the owner or an admin can upload for this email
    if current["email"] != email and current.get("role") != "admin":
        raise HTTPException(status_code=403, detail="You can upload only your own resume")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    safe_name = file.filename.replace("..", "_")
    fp = os.path.join(UPLOAD_FOLDER, safe_name)
    with open(fp, "wb") as f:
        f.write(await file.read())

    resume_url = f"/static/{safe_name}"  # served by StaticFiles
    await update_candidate_resume(email, resume_url)
    return {"message": "Resume uploaded", "resume_url": resume_url}