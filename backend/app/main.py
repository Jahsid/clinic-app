from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth_routes, doctors, patients, appointments, dashboard

# Level 1: create tables automatically for local dev.
# For production, use Alembic migrations instead (see init_db.sql for the raw schema).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Appointment & Patient Desk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000","https://clinic-appointment-portal.onrender.com/login"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Clinic Appointment & Patient Desk API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
