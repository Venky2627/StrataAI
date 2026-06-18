import sqlite3
import os
import datetime

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "progress.db")

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table for Quiz Results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            document TEXT,
            quiz_type TEXT,
            score REAL,
            max_score REAL
        )
    ''')
    
    # Create table for Study Plans generated
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            documents TEXT,
            days INTEGER,
            hours_per_day INTEGER,
            goal TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_quiz_result(document: str, quiz_type: str, score: float, max_score: float):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO quiz_results (document, quiz_type, score, max_score) VALUES (?, ?, ?, ?)',
        (document, quiz_type, score, max_score)
    )
    conn.commit()
    conn.close()

def log_study_plan(documents: str, days: int, hours_per_day: int, goal: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO study_plans (documents, days, hours_per_day, goal) VALUES (?, ?, ?, ?)',
        (documents, days, hours_per_day, goal)
    )
    conn.commit()
    conn.close()

def get_quiz_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, document, quiz_type, score, max_score FROM quiz_results ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_study_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, documents, days, hours_per_day, goal FROM study_plans ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize DB on import
init_db()
