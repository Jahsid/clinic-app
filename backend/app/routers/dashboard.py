from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db),
                       current_user: models.User = Depends(auth.get_current_user)):
    total_doctors = db.query(func.count(models.Doctor.doctor_id)).scalar()
    total_patients = db.query(func.count(models.Patient.patient_id)).scalar()
    total_appointments = db.query(func.count(models.Appointment.appointment_id)).scalar()
    todays_appointments = (
        db.query(func.count(models.Appointment.appointment_id))
        .filter(models.Appointment.appointment_date == date.today())
        .scalar()
    )
    scheduled_count = db.query(func.count(models.Appointment.appointment_id)).filter(
        models.Appointment.status == "Scheduled"
    ).scalar()
    completed_count = db.query(func.count(models.Appointment.appointment_id)).filter(
        models.Appointment.status == "Completed"
    ).scalar()
    cancelled_count = db.query(func.count(models.Appointment.appointment_id)).filter(
        models.Appointment.status == "Cancelled"
    ).scalar()

    return schemas.DashboardSummary(
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_appointments=total_appointments,
        todays_appointments=todays_appointments,
        scheduled_count=scheduled_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
    )


@router.get("/today", response_model=list[schemas.RecentAppointment])
def todays_schedule(db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_user)):
    appts = (
        db.query(models.Appointment)
        .options(joinedload(models.Appointment.doctor), joinedload(models.Appointment.patient))
        .filter(models.Appointment.appointment_date == date.today())
        .order_by(models.Appointment.appointment_time)
        .all()
    )
    return [
        schemas.RecentAppointment(
            appointment_id=a.appointment_id,
            patient_name=a.patient.patient_name,
            doctor_name=a.doctor.doctor_name,
            appointment_date=a.appointment_date,
            appointment_time=a.appointment_time,
            status=a.status,
        )
        for a in appts
    ]
