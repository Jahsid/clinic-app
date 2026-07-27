-- Clinic Appointment & Patient Desk — raw schema (matches project documentation section 6.3)
-- Run this manually if you prefer explicit DDL instead of SQLAlchemy's create_all().

CREATE TABLE IF NOT EXISTS users (
    user_id         SERIAL PRIMARY KEY,
    username        VARCHAR(100) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(100) NOT NULL,
    role            VARCHAR(20) NOT NULL,          -- admin | receptionist | doctor
    email           VARCHAR(100) UNIQUE,
    phone           VARCHAR(15),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id       SERIAL PRIMARY KEY,
    doctor_name     VARCHAR(100) NOT NULL,
    specialization  VARCHAR(100) NOT NULL,
    phone           VARCHAR(15),
    email           VARCHAR(100) UNIQUE,
    experience      INT,
    availability    VARCHAR(50),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patients (
    patient_id      SERIAL PRIMARY KEY,
    patient_name    VARCHAR(100) NOT NULL,
    age             INT,
    gender          VARCHAR(10),
    phone           VARCHAR(15),
    email           VARCHAR(100),
    address         TEXT,
    blood_group     VARCHAR(5),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id     SERIAL PRIMARY KEY,
    patient_id         INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    doctor_id          INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    appointment_date   DATE NOT NULL,
    appointment_time   TIME NOT NULL,
    reason             TEXT,
    status             VARCHAR(20) DEFAULT 'Scheduled',   -- Scheduled | Completed | Cancelled
    remarks            TEXT,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes (section 6.4)
CREATE INDEX IF NOT EXISTS ix_patient_name       ON patients(patient_name);
CREATE INDEX IF NOT EXISTS ix_doctor_name        ON doctors(doctor_name);
CREATE INDEX IF NOT EXISTS ix_appointment_date   ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS ix_appointment_status ON appointments(status);
