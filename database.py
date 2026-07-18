import sqlite3
from sqlite3 import Connection
from typing import List, Dict, Any
import os
import hashlib

DB_DIR = os.path.join(os.path.dirname(__file__), 'data')
DB_PATH = os.path.join(DB_DIR, 'prepstr.db')

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    subject TEXT,
    time_limit INTEGER,
    negative_marking REAL DEFAULT 0.0,
    total_questions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_option INTEGER,
    explanation TEXT,
    FOREIGN KEY(test_id) REFERENCES tests(test_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    test_id INTEGER,
    score REAL,
    correct INTEGER,
    wrong INTEGER,
    accuracy REAL,
    time_taken INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(test_id) REFERENCES tests(test_id)
);
"""


def get_conn() -> Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()


def add_user(name, username, email, password_hash, is_admin=0):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (name, username, email, password_hash, is_admin) VALUES (?, ?, ?, ?, ?)",
                    (name, username, email, password_hash, is_admin))
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        return None
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_test(title, subject, time_limit, negative_marking):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tests (title, subject, time_limit, negative_marking) VALUES (?, ?, ?, ?)",
                (title, subject, time_limit, negative_marking))
    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return tid


def get_tests():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tests ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_test(test_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tests WHERE test_id = ?", (test_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_question(test_id, question, opt1, opt2, opt3, opt4, correct_option, explanation):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (test_id, question, option1, option2, option3, option4, correct_option, explanation) VALUES (?,?,?,?,?,?,?,?)",
        (test_id, question, opt1, opt2, opt3, opt4, correct_option, explanation))
    conn.commit()
    qid = cur.lastrowid
    conn.close()
    return qid


def get_questions_for_test(test_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE test_id = ? ORDER BY id", (test_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def save_result(user_id, test_id, score, correct, wrong, accuracy, time_taken):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (user_id, test_id, score, correct, wrong, accuracy, time_taken) VALUES (?,?,?,?,?,?,?)",
        (user_id, test_id, score, correct, wrong, accuracy, time_taken))
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid


def get_results_by_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT r.*, t.title FROM results r LEFT JOIN tests t ON r.test_id = t.test_id WHERE user_id = ? ORDER BY date DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_overview_stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as users FROM users")
    users = cur.fetchone()['users']
    cur.execute("SELECT COUNT(*) as tests FROM tests")
    tests = cur.fetchone()['tests']
    cur.execute("SELECT COUNT(*) as questions FROM questions")
    questions = cur.fetchone()['questions']
    cur.execute("SELECT COUNT(*) as attempts FROM results")
    attempts = cur.fetchone()['attempts']
    conn.close()
    return {'users': users, 'tests': tests, 'questions': questions, 'attempts': attempts}

if __name__ == '__main__':
    init_db()
    print('Initialized DB at', DB_PATH)
