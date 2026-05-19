-- ============================================================
-- MaternaDB  –  Full Database Setup
-- Run this entire file in pgAdmin Query Tool on materna_db
-- Safe to run multiple times (IF NOT EXISTS everywhere)
-- ============================================================


-- ============================================================
-- 1. USERS  (login & signup)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id      SERIAL PRIMARY KEY,
    name         TEXT        NOT NULL,
    email        TEXT        UNIQUE NOT NULL,
    password     TEXT        NOT NULL,
    role         TEXT        DEFAULT 'Staff',
    contact      TEXT,
    profile_pic  BYTEA,
    date_joined  TIMESTAMPTZ DEFAULT NOW()
);

-- Add missing columns if table already existed without them
ALTER TABLE users ADD COLUMN IF NOT EXISTS role        TEXT        DEFAULT 'Staff';
ALTER TABLE users ADD COLUMN IF NOT EXISTS contact     TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_pic BYTEA;
ALTER TABLE users ADD COLUMN IF NOT EXISTS date_joined TIMESTAMPTZ DEFAULT NOW();


-- ============================================================
-- 2. STAFF  (referenced by prescriptions etc.)
-- ============================================================
CREATE TABLE IF NOT EXISTS staff (
    staff_id    SERIAL PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    role        TEXT DEFAULT 'Midwife',
    contact     TEXT
);


-- ============================================================
-- 3. PATIENT PROFILE
-- ============================================================
CREATE TABLE IF NOT EXISTS patient_profile (
    patient_id      SERIAL PRIMARY KEY,
    first_name      TEXT    NOT NULL,
    middle_name     TEXT,
    last_name       TEXT    NOT NULL,
    date_of_birth   DATE,
    age             INTEGER,
    blood_type      TEXT,
    philhealth_no   TEXT,
    contact_no      TEXT,
    address         TEXT,
    patient_type    TEXT    DEFAULT 'Maternal',
    date_registered DATE    DEFAULT CURRENT_DATE
);


-- ============================================================
-- 4. APPOINTMENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id   SERIAL PRIMARY KEY,
    patient_id       INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    appointment_date DATE    NOT NULL,
    appointment_time TIME,
    purpose          TEXT,
    status           TEXT    DEFAULT 'Scheduled',
    notes            TEXT
);


-- ============================================================
-- 5. MEDICAL HISTORY
-- ============================================================
CREATE TABLE IF NOT EXISTS medical_history (
    history_id      SERIAL PRIMARY KEY,
    patient_id      INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    condition       TEXT    NOT NULL,
    diagnosis_date  DATE,
    status          TEXT    DEFAULT 'Active',
    remarks         TEXT
);


-- ============================================================
-- 6. FAMILY PLANNING
-- ============================================================
CREATE TABLE IF NOT EXISTS family_planning (
    planning_id     SERIAL PRIMARY KEY,
    patient_id      INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    method          TEXT    NOT NULL,
    start_date      DATE,
    end_date        DATE,
    prescribed_by   INTEGER REFERENCES staff(staff_id),
    next_followup   DATE,
    status          TEXT    DEFAULT 'Active',
    notes           TEXT
);


-- ============================================================
-- 7. PRESCRIPTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS prescription (
    prescription_id   SERIAL PRIMARY KEY,
    patient_id        INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    prescribed_by     INTEGER REFERENCES staff(staff_id),
    prescription_date DATE    DEFAULT CURRENT_DATE,
    medicine_name     TEXT    NOT NULL,
    dosage            TEXT,
    frequency         TEXT,
    duration          TEXT,
    route             TEXT,
    timing            TEXT,
    notes             TEXT
);


-- ============================================================
-- 8. PREGNANCY  (one row per pregnancy per patient)
-- ============================================================
CREATE TABLE IF NOT EXISTS pregnancy (
    pregnancy_id  SERIAL PRIMARY KEY,
    patient_id    INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    pregnancy_num INTEGER NOT NULL,
    edd           DATE,
    start_date    DATE    DEFAULT CURRENT_DATE,
    status        TEXT    DEFAULT 'Active'   -- 'Active', 'Delivered', 'Lost'
);


-- ============================================================
-- 9. PRENATAL VISIT  (many per pregnancy)
-- ============================================================
CREATE TABLE IF NOT EXISTS prenatal_visit (
    visit_id        SERIAL PRIMARY KEY,
    pregnancy_id    INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    visit_num       INTEGER NOT NULL,
    visit_date      DATE    NOT NULL,
    aog_weeks       INTEGER NOT NULL,
    staff           TEXT    NOT NULL,
    bp              TEXT    NOT NULL,
    weight_kg       DECIMAL(5, 2),
    fht_bpm         INTEGER,
    fh_cm           DECIMAL(4, 1),
    presentation    TEXT    DEFAULT 'Cephalic',
    risk_assessment TEXT    DEFAULT 'Low Risk'
);

-- if you had an old version with patient_id directly on prenatal_visit, keep it nullable
ALTER TABLE prenatal_visit ADD COLUMN IF NOT EXISTS pregnancy_id INTEGER REFERENCES pregnancy(pregnancy_id);


-- ============================================================
-- 10. LAB & REFERRALS  (per pregnancy)
-- ============================================================
CREATE TABLE IF NOT EXISTS lab_referral (
    lab_id        SERIAL PRIMARY KEY,
    pregnancy_id  INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    lab_date      DATE    NOT NULL,
    lab_type      TEXT    NOT NULL,
    result        TEXT    DEFAULT 'Pending',
    notes         TEXT
);


-- ============================================================
-- 11. PREGNANCY MEDICATIONS  (per pregnancy)
-- ============================================================
CREATE TABLE IF NOT EXISTS pregnancy_medication (
    med_id        SERIAL PRIMARY KEY,
    pregnancy_id  INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    medicine_name TEXT    NOT NULL,
    dosage        TEXT    NOT NULL,
    frequency     TEXT    NOT NULL,
    route         TEXT    DEFAULT 'Oral',
    start_date    DATE,
    end_date      DATE,
    notes         TEXT
);


-- ============================================================
-- 12. DELIVERY RECORD  (per pregnancy, usually one)
-- ============================================================
CREATE TABLE IF NOT EXISTS delivery_record (
    delivery_id       SERIAL PRIMARY KEY,
    pregnancy_id      INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    delivery_date     DATE    NOT NULL,
    delivery_type     TEXT    NOT NULL,
    outcome           TEXT    NOT NULL,
    attendant         TEXT    NOT NULL,
    place_of_delivery TEXT,
    complications     TEXT,
    notes             TEXT
);


-- ============================================================
-- 13. NEWBORN RECORD  (per pregnancy, may be multiple for twins etc.)
-- ============================================================
CREATE TABLE IF NOT EXISTS newborn_record (
    newborn_id       SERIAL PRIMARY KEY,
    pregnancy_id     INTEGER REFERENCES pregnancy(pregnancy_id) ON DELETE CASCADE,
    baby_name        TEXT,
    date_of_birth    DATE,
    sex              TEXT    DEFAULT 'Female',
    birth_weight_kg  DECIMAL(4, 2),
    birth_length_cm  DECIMAL(4, 1),
    apgar_1min       INTEGER,
    apgar_5min       INTEGER,
    notes            TEXT
);


-- ============================================================
-- 14. PAST PREGNANCY  (patient's history before this system)
-- ============================================================
CREATE TABLE IF NOT EXISTS past_pregnancy (
    past_preg_id    SERIAL PRIMARY KEY,
    patient_id      INTEGER REFERENCES patient_profile(patient_id) ON DELETE CASCADE,
    year            INTEGER,
    outcome         TEXT,
    delivery_type   TEXT,
    complications   TEXT,
    notes           TEXT
);


-- ============================================================
-- SEED DATA — one admin user so you can log in immediately
-- Skip if a user already exists with this email.
-- ============================================================
INSERT INTO users (name, email, password, role)
VALUES ('Admin', 'admin@materna.com', 'admin123', 'Admin')
ON CONFLICT (email) DO NOTHING;


-- ============================================================
-- QUICK VERIFICATION
-- Run these after the above to confirm everything exists:
--
--   SELECT table_name FROM information_schema.tables
--   WHERE table_schema = 'public'
--   ORDER BY table_name;
--
-- You should see 14 tables listed.
-- ============================================================
