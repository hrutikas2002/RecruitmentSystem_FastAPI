import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.config import UPLOAD_FOLDER
from app.database import ensure_indexes
from app.routers.auth_routes import router as auth_router
from app.routers.job_routes import router as job_router
from app.routers.candidate_routes import router as candidate_router
from app.routers.admin_routes import router as admin_router
from app.routers.application_routes import router as application_router

app = FastAPI(title="Recruitment System API")

# CORS (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static serving for resumes
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")

@app.on_event("startup")
async def on_startup():
    await ensure_indexes()

@app.get("/")
def welcome_message():
    return {"message": "Welcome to the Recruitment System API!"}

# Routers
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(candidate_router)
app.include_router(admin_router)
app.include_router(application_router)
