from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Date, Time,
    ForeignKey, TIMESTAMP, func, Index
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # admin | receptionist | doctor
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(15), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    experience = Column(Integer, nullable=True)
    availability = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    appointments = relationship("Appointment", back_populates="doctor")

    __table_args__ = (Index("ix_doctor_name", "doctor_name"),)


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    blood_group = Column(String(5), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    appointments = relationship("Appointment", back_populates="patient")

    __table_args__ = (Index("ix_patient_name", "patient_name"),)


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default="Scheduled")  # Scheduled | Completed | Cancelled
    remarks = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    __table_args__ = (
        Index("ix_appointment_date", "appointment_date"),
        Index("ix_appointment_status", "status"),
    )
