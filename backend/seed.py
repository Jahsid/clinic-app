"""
Seed the database with an initial admin user and a couple of sample doctors.
Run with: python seed.py   (after the FastAPI app has created the tables once,
or after running init_db.sql)
"""
from app.database import SessionLocal, Base, engine
from app import models, auth

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if not db.query(models.User).filter(models.User.username == "admin").first():
        db.add(models.User(
            username="admin",
            password_hash=auth.hash_password("Admin@123"),
            full_name="System Administrator",
            role="admin",
            email="admin@clinic.local",
        ))

    if not db.query(models.User).filter(models.User.username == "reception1").first():
        db.add(models.User(
            username="reception1",
            password_hash=auth.hash_password("Reception@123"),
            full_name="Front Desk",
            role="receptionist",
            email="reception@clinic.local",
        ))

    if db.query(models.Doctor).count() == 0:
        db.add_all([
            models.Doctor(doctor_name="Dr. Asha Rao", specialization="General Medicine",
                          phone="9990001111", email="asha.rao@clinic.local",
                          experience=8, availability="Mon-Fri 9am-4pm"),
            models.Doctor(doctor_name="Dr. Vivek Shah", specialization="Pediatrics",
                          phone="9990002222", email="vivek.shah@clinic.local",
                          experience=12, availability="Mon-Sat 10am-2pm"),
        ])

    db.commit()
    print("Seed complete. Login with admin / Admin@123")
finally:
    db.close()
