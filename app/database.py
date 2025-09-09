from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME
import certifi
import os

# Optional toggle for local dev if your network does TLS interception
ALLOW_INVALID_CERTS = os.getenv("ALLOW_INVALID_CERTS", "false").lower() == "true"

client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    # Prefer proper CA bundle
    tlsCAFile=None if ALLOW_INVALID_CERTS else certifi.where(),
    # As a last-resort local dev bypass (DON'T USE IN PROD)
    tlsAllowInvalidCertificates=ALLOW_INVALID_CERTS,
    serverSelectionTimeoutMS=20000,
)
db = client[DB_NAME]

async def ensure_indexes():
    # Fail fast but with a clear error printed
    try:
        await db.candidates.create_index("email", unique=True)
        await db.admins.create_index("email", unique=True)
        await db.jobs.create_index("status")
        await db.applications.create_index([("candidate_email", 1), ("job_id", 1)], unique=True)
    except Exception as e:
        print("Mongo index creation failed:", e)
        raise
