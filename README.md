# Clinic Appointment & Patient Desk

Full-stack implementation (React + FastAPI + PostgreSQL) matching the project documentation
(sections 6 and 7: Database Design and API Design) and the 11-day Level 1 build plan.

## What's implemented (Level 1 — Days 1–8 of the plan)

- **Auth**: JWT login/logout/profile, role-based access (admin, receptionist, doctor)
- **Doctors**: full CRUD (admin only writes; everyone can view), search by name
- **Patients**: full CRUD (admin + receptionist can write), search by name
- **Appointments**: booking, reschedule, cancel, status update, double-booking prevention
  (a doctor can't have two active appointments at the same date/time)
- **Dashboard**: summary counts + today's schedule
- **Database**: matches the exact schema in section 6.3 (users, doctors, patients, appointments)

## Project layout

```
clinic-app/
  backend/
    app/
      main.py            # FastAPI app + router registration + CORS
      database.py         # SQLAlchemy engine/session
      models.py           # ORM models (users, doctors, patients, appointments)
      schemas.py           # Pydantic request/response schemas
      auth.py               # JWT + bcrypt password hashing + role guard
      routers/
        auth_routes.py     # POST /api/login, /api/logout, GET /api/profile
        doctors.py          # /api/doctors CRUD
        patients.py         # /api/patients CRUD
        appointments.py    # /api/appointments CRUD + slot validation
        dashboard.py        # /api/dashboard, /api/dashboard/today
    init_db.sql            # raw DDL matching section 6.3 (optional, alternative to ORM create_all)
    seed.py                # creates admin/receptionist users + 2 sample doctors
    requirements.txt
    .env.example
  frontend/
    src/
      api/client.js         # fetch wrapper, attaches JWT, handles 401
      context/AuthContext.jsx
      components/Navbar.jsx, ProtectedRoute.jsx
      pages/Login.jsx, Dashboard.jsx, Doctors.jsx, Patients.jsx, Appointments.jsx
      App.jsx, main.jsx, index.css
    package.json, vite.config.js, index.html
    .env.example
```

## Step-by-step: how to run it

### 1. Database (Day 3, Session 1)
```bash
createdb clinic_db
# option A: let SQLAlchemy create tables automatically (default, see step 3)
# option B: run the raw schema yourself
psql -d clinic_db -f backend/init_db.sql
```

### 2. Backend setup
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # edit DATABASE_URL and SECRET_KEY
```

### 3. Seed an admin user (Day 3, Session 2 — auth foundation)
```bash
python seed.py
# creates: admin / Admin@123   and   reception1 / Reception@123
```

### 4. Run the backend
```bash
uvicorn app.main:app --reload --port 8000
# Swagger docs: http://localhost:8000/docs
```

### 5. Frontend setup
```bash
cd ../frontend
npm install
cp .env.example .env   # points VITE_API_URL at the backend
npm run dev
# App: http://localhost:5173
```

### 6. Log in
Use `admin / Admin@123` or `reception1 / Reception@123` (from seed.py).

## Mapping back to the 11-day plan

| Day | Plan focus | Code delivering it |
|---|---|---|
| 1–2 | Architecture, DB & API freeze | `models.py`, `schemas.py`, section 6/7 of docs mirrored 1:1 |
| 3 | Setup + auth foundation | `auth.py`, `routers/auth_routes.py`, `Login.jsx`, `AuthContext.jsx` |
| 4 | Doctor module, patient module start | `routers/doctors.py`, `Doctors.jsx`; `routers/patients.py` scaffolds |
| 5 | Patient module complete, appointment start | `Patients.jsx` full CRUD; `AppointmentCreate` schema |
| 6 | Appointment desk UI + backend persistence + slot validation | `Appointments.jsx`, `routers/appointments.py` (clash check) |
| 7 | Schedule/history view + dashboard | `dashboard()` / `todays_schedule()`, `Dashboard.jsx` |
| 8 | Stabilize Level 1 | smoke-tested end to end (auth, CRUD, booking, clash, dashboard, role checks) |

## Known limitations / Level 2+ ideas (documented honestly, per Day 8/11 checkpoints)
- No password reset flow, no refresh tokens (access token expires after 8h by default)
- No pagination on list endpoints yet (fine for a clinic desk's typical row counts, but worth adding for Level 2)
- Reports endpoints from section 7.7 (`/api/reports/*`) are in the docs but not yet built — good Level 2/3 target
- No automated test suite included (project was verified with manual smoke tests during this session)
- Frontend has no client-side field validation beyond `required`; server-side validation via Pydantic is the source of truth
