from datetime import date, time, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Auth ----------
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    full_name: str
    role: str
    email: Optional[str] = None


# ---------- Doctor ----------
class DoctorBase(BaseModel):
    doctor_name: str
    specialization: str
    phone: Optional[str] = None
    email: Optional[str] = None
    experience: Optional[int] = None
    availability: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(DoctorBase):
    doctor_name: Optional[str] = None
    specialization: Optional[str] = None


class DoctorOut(DoctorBase):
    model_config = ConfigDict(from_attributes=True)
    doctor_id: int
    created_at: datetime


# ---------- Patient ----------
class PatientBase(BaseModel):
    patient_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    patient_name: Optional[str] = None


class PatientOut(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int
    created_at: datetime


# ---------- Appointment ----------
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: Optional[str] = None
    remarks: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class AppointmentOut(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: int
    status: str
    created_at: datetime
    doctor_name: Optional[str] = None
    patient_name: Optional[str] = None


# ---------- Dashboard ----------
class DashboardSummary(BaseModel):
    total_doctors: int
    total_patients: int
    total_appointments: int
    todays_appointments: int
    scheduled_count: int
    completed_count: int
    cancelled_count: int


class RecentAppointment(BaseModel):
    appointment_id: int
    patient_name: str
    doctor_name: str
    appointment_date: date
    appointment_time: time
    status: str
