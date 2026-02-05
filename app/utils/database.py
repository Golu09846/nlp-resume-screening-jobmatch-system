# FILE: app/utils/database.py

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), "resume_system.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # RESUMES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filedata BLOB,
            clean_text TEXT,
            skills TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            education TEXT,
            experience TEXT,
            projects TEXT,
            uploaded_at TIMESTAMP
        );
    """)

    # JD TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_jd TEXT,
            clean_jd TEXT,
            skills TEXT,
            role TEXT,
            uploaded_at TIMESTAMP
        );
    """)

    # RESULTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            jd_id INTEGER,
            semantic_score REAL,
            final_score REAL,
            matched_at TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


# ---------------- SAVE RESUME ----------------
def save_resume(filename, filedata, clean_text, skills,
                name, email, phone, education, experience, projects):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumes 
        (filename, filedata, clean_text, skills,
         name, email, phone, education, experience, projects, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        filedata,
        clean_text,
        ",".join(skills),
        name,
        email,
        phone,
        education,
        experience,
        projects,
        datetime.now()
    ))

    conn.commit()
    conn.close()


# ---------------- SAVE JD ----------------
def save_jd(raw_jd, clean_jd, skills, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO job_descriptions 
        (raw_jd, clean_jd, skills, role, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        raw_jd,
        clean_jd,
        ",".join(skills),
        role,
        datetime.now()
    ))

    conn.commit()
    conn.close()


# ---------------- SAVE MATCH RESULT ----------------
def save_result(resume_id, jd_id, semantic_score, final_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results
        (resume_id, jd_id, semantic_score, final_score, matched_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        resume_id,
        jd_id,
        semantic_score,
        final_score,
        datetime.now()
    ))

    conn.commit()
    conn.close()


# ---------------- FETCH RESUMES ----------------
def get_all_resumes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes ORDER BY uploaded_at DESC")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]   # FIX


# ---------------- FETCH JDs ----------------
def get_all_jds():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_descriptions ORDER BY uploaded_at DESC")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]   # FIX


# ---------------- FETCH MATCH RESULTS ----------------
def get_all_results():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT res.id as id,
               r.filename as filename,
               r.name as name,
               j.role as role,
               res.semantic_score,
               res.final_score,
               res.matched_at
        FROM results res
        JOIN resumes r ON res.resume_id = r.id
        JOIN job_descriptions j ON res.jd_id = j.id
        ORDER BY res.matched_at DESC
    """)
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]   # FIX
