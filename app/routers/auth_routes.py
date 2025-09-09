from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import CandidateCreate, AdminCreate, Token
from app.models import Candidate, Admin
from app.crud import create_candidate, create_admin, get_user_by_email
from app.auth import get_password_hash, verify_password, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["auth"])

@router.post("/signup", summary="Candidate signup")
async def signup(candidate: CandidateCreate):
    exists = await get_user_by_email(candidate.email)
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    cand = Candidate(email=candidate.email, password=get_password_hash(candidate.password), name=candidate.name)
    await create_candidate(cand)
    return {"message": "Candidate created"}

@router.post("/admin/seed", summary="Create an admin (one-time use)")
async def seed_admin(admin: AdminCreate):
    exists = await get_user_by_email(admin.email)
    if exists:
        raise HTTPException(status_code=400, detail="Admin already exists")
    adm = Admin(email=admin.email, password=get_password_hash(admin.password))
    await create_admin(adm)
    return {"message": "Admin created"}

@router.post("/token", response_model=Token, summary="Login to get JWT")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2 form_data.username = email
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    role = user.get("role", "candidate")
    access_token = create_access_token(data={"sub": user["email"], "role": role}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
