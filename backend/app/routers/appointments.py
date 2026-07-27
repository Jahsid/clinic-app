from typing import List, Optional
from datetime import date as date_type
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


def _to_out(appt: models.Appointment) -> schemas.AppointmentOut:
    return schemas.AppointmentOut(
        appointment_id=appt.appointment_id,
        patient_id=appt.patient_id,
        doctor_id=appt.doctor_id,
        appointment_date=appt.appointment_date,
        appointment_time=appt.appointment_time,
        reason=appt.reason,
        status=appt.status,
        remarks=appt.remarks,
        created_at=appt.created_at,
        doctor_name=appt.doctor.doctor_name if appt.doctor else None,
        patient_name=appt.patient.patient_name if appt.patient else None,
    )


@router.get("", response_model=List[schemas.AppointmentOut])
def list_appointments(
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    appointment_date: Optional[date_type] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Appointment).options(
        joinedload(models.Appointment.doctor), joinedload(models.Appointment.patient)
    )
    if doctor_id:
        query = query.filter(models.Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(models.Appointment.patient_id == patient_id)
    if appointment_date:
        query = query.filter(models.Appointment.appointment_date == appointment_date)
    if status_filter:
        query = query.filter(models.Appointment.status == status_filter)

    results = query.order_by(
        models.Appointment.appointment_date.desc(), models.Appointment.appointment_time
    ).all()
    return [_to_out(a) for a in results]


@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_user)):
    appt = (
        db.query(models.Appointment)
        .options(joinedload(models.Appointment.doctor), joinedload(models.Appointment.patient))
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return _to_out(appt)


@router.post("", response_model=schemas.AppointmentOut, status_code=201)
def book_appointment(
    payload: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin", "receptionist")),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    patient = db.query(models.Patient).filter(models.Patient.patient_id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Slot validation: same doctor cannot have two active appointments at the same date/time
    clash = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == payload.doctor_id,
            models.Appointment.appointment_date == payload.appointment_date,
            models.Appointment.appointment_time == payload.appointment_time,
            models.Appointment.status != "Cancelled",
        )
        .first()
    )
    if clash:
        raise HTTPException(
            status_code=409,
            detail="This doctor already has an appointment booked at that date and time",
        )

    appt = models.Appointment(**payload.model_dump(), status="Scheduled")
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return _to_out(appt)


@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    appointment_id: int,
    payload: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin", "receptionist", "doctor")),
):
    appt = db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updates = payload.model_dump(exclude_unset=True)

    # Doctors may only update status/remarks, not reschedule
    if current_user.role == "doctor":
        updates = {k: v for k, v in updates.items() if k in ("status", "remarks")}

    if payload.status and payload.status not in ("Scheduled", "Completed", "Cancelled"):
        raise HTTPException(status_code=400, detail="Invalid status value")

    # Re-validate clash if date/time is changing
    new_date = updates.get("appointment_date", appt.appointment_date)
    new_time = updates.get("appointment_time", appt.appointment_time)
    if "appointment_date" in updates or "appointment_time" in updates:
        clash = (
            db.query(models.Appointment)
            .filter(
                models.Appointment.doctor_id == appt.doctor_id,
                models.Appointment.appointment_date == new_date,
                models.Appointment.appointment_time == new_time,
                models.Appointment.status != "Cancelled",
                models.Appointment.appointment_id != appointment_id,
            )
            .first()
        )
        if clash:
            raise HTTPException(status_code=409, detail="Doctor already booked at that date and time")

    for field, value in updates.items():
        setattr(appt, field, value)

    db.commit()
    db.refresh(appt)
    return _to_out(appt)


@router.delete("/{appointment_id}", status_code=200)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin", "receptionist")),
):
    appt = db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.status = "Cancelled"
    db.commit()
    return {"message": "Appointment cancelled"}
