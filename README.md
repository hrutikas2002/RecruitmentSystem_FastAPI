**Recruitment System – FastAPI Backend**

A mini recruitment platform backend built with FastAPI, MongoDB (Atlas), and JWT authentication. It supports two roles—Admin and Candidate—with job postings, applications, and resume uploads.


** Problem Statement**

Build a backend for a recruitment system that allows:

**Candidates**

sign up & log in

browse jobs

upload resumes

apply to jobs

view their own applications

**Admins**

log in

create/update jobs

list all candidates

view candidate resumes

view all applications

**Requirements**

Role-based access control for routes

Secure password hashing and JWT-based auth

Persistent data storage (MongoDB)

Resume upload & serving

Clear, testable API with Swagger docs

**Features**

**Authentication**

Candidate signup

Admin seed & login

OAuth2 Password Flow with JWT

Role embedded in token (role: "admin" | "candidate")

**Jobs**

Create / Update (Admin only)

List & get by id (Public)

Status: Open | Closed | Filled

**Applications**

Candidate applies to job

Candidate lists their applications

Admin lists all applications

Unique constraint to prevent duplicate applications

**Candidates**

Upload resume (file) — saved locally & served via /static

Admin lists all candidates

Admin fetches resume URL for a candidate

**Architecture & Tech Stack**

FastAPI (web framework)

Motor (async MongoDB driver)

MongoDB Atlas (managed cloud database)

Passlib (bcrypt) for secure password hashing

python-jose for JWT creation/verification

python-multipart for file uploads

Starlette StaticFiles to serve uploaded resumes

**Endpoints Overview**

Explore and try them in Swagger UI: http://127.0.0.1:8000/docs

### Auth
| Method | Path          | Role              | Description            |
|:-----: | ------------- | ----------------- | ---------------------- |
| POST   | `/signup`     | Public            | Create candidate       |
| POST   | `/admin/seed` | Public (one-time) | Create an admin (seed) |
| POST   | `/token`      | Public            | Login, returns JWT     |

### Jobs
| Method | Path             | Role   | Description               |
|:-----: | ---------------- | ------ | ------------------------- |
| GET    | `/jobs`          | Public | List jobs                 |
| GET    | `/jobs/{job_id}` | Public | Get job by id             |
| POST   | `/jobs`          | Admin  | Create job                |
| PUT    | `/jobs/{job_id}` | Admin  | Update job (e.g., status) |

### Candidates
| Method | Path                        | Role                   | Description                                    |
|:-----: | --------------------------- | ---------------------- | ---------------------------------------------- |
| GET    | `/candidates/me`            | Candidate/Admin (self) | Get my profile                                 |
| POST   | `/candidates/upload-resume` | Candidate/Admin        | Upload resume (`email`, `file` as form fields) |

### Applications
| Method | Path                                | Role      | Description           |
|:-----: | ----------------------------------- | --------- | --------------------- |
| POST   | `/applications/jobs/{job_id}/apply` | Candidate | Apply to a job        |
| GET    | `/applications/me`                  | Candidate | List my applications  |
| GET    | `/applications/all`                 | Admin     | List all applications |

### Admin Utilities
| Method | Path                    | Role  | Description                  |
|:-----: | ----------------------- | ----- | ---------------------------- |
| GET    | `/admin/candidates`     | Admin | List all candidates          |
| GET    | `/admin/resume/{email}` | Admin | Get resume URL for candidate |


**Setup & Running Locally**

Create a virtual environment

Windows (PowerShell)

python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies

pip install -r requirements.txt

Configure environment
Create a .env file in the project root with:

MONGO_URI=mongodb+srv://<user>:<pass>@cluster0.xxxxx.mongodb.net/Recruitment?retryWrites=true&w=majority&appName=Cluster0

SECRET_KEY=change_me_to_a_long_random_string

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_NAME=Recruitment

UPLOAD_FOLDER=uploads

Run the server

If main.py is at the repo root:

uvicorn main:app --reload

If main.py is inside the app package:

uvicorn app.main:app --reload


Open Swagger

http://127.0.0.1:8000/docs
