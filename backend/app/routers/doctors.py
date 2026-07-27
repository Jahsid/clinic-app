from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.get("", response_model=List[schemas.DoctorOut])
def list_doctors(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Doctor)
    if search:
        query = query.filter(models.Doctor.doctor_name.ilike(f"%{search}%"))
    return query.order_by(models.Doctor.doctor_name).all()


@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("", response_model=schemas.DoctorOut, status_code=201)
def create_doctor(
    payload: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin")),
):
    doctor = models.Doctor(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.put("/{doctor_id}", response_model=schemas.DoctorOut)
def update_doctor(
    doctor_id: int,
    payload: schemas.DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin")),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_roles("admin")),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return None
