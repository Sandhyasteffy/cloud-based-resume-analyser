import sqlite3
from config import Config

def get_connection():
    return sqlite3.connect(Config.DATABASE_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            role TEXT NOT NULL,
            match_score INTEGER NOT NULL,
            matched_skills TEXT,
            missing_skills TEXT,
            extra_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_analysis(file_name, role, match_score, matched_skills, missing_skills, extra_skills):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis_results (
            file_name, role, match_score, matched_skills, missing_skills, extra_skills
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        file_name,
        role,
        match_score,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        ", ".join(extra_skills)
    ))

    conn.commit()
    conn.close()

def get_all_results():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, file_name, role, match_score, matched_skills, missing_skills, extra_skills, created_at
        FROM analysis_results
        ORDER BY created_at DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results