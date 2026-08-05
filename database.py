import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
async def get_connection():
    conn = await asyncpg.connect()
    return conn

async def create_tables(conn):
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        major TEXT NOT NULL,
        year INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS courses(
        id SERIAL PRIMARY KEY,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        credits INTEGER NOT NULL,
        semester TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS enrollments (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS assessments (
        id SERIAL PRIMARY KEY,
        course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        max_score INTEGER NOT NULL,
        date DATE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS scores (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        assessment_id INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
        score INTEGER NOT NULL,
        submitted BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        date DATE NOT NULL,
        present BOOLEAN NOT NULL
    );
    """)


async def seed_data(conn):
    await conn.execute("""
    INSERT INTO users (name, email, major, year) VALUES
    ('Alex Rivera', 'alex.rivera@univ.edu', 'Computer Science', 2),
    ('Maya Patel', 'maya.patel@univ.edu', 'Electrical Engineering', 1),
    ('Jordan Lee', 'jordan.lee@univ.edu', 'Computer Science', 3),
    ('Sam Chen', 'sam.chen@univ.edu', 'Mechanical Engineering', 4),
    ('Taylor Swift', 'taylor.swift@univ.edu', 'Software Engineering', 2);
    """)

    await conn.execute("""
    INSERT INTO courses (code, name, credits, semester) VALUES
    ('MATH101', 'Calculus I', 4, 'Fall 2026'),
    ('MATH201', 'Linear Algebra', 3, 'Fall 2026'),
    ('CS102', 'Data Structures & Algorithms', 4, 'Fall 2026'),
    ('PHYS105', 'University Physics I', 4, 'Fall 2026');
    """)

    await conn.execute("""
    INSERT INTO enrollments (student_id, course_id) VALUES
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 4),
    (3, 2), (3, 3), (3, 4),
    (4, 1), (4, 3), (4, 4),
    (5, 2), (5, 3);
    """)

    await conn.execute("""
    INSERT INTO assessments (course_id, title, type, max_score, date) VALUES
    (1, 'Quiz 1: Limits & Integration Intro', 'quiz', 20, '2026-09-15'),
    (1, 'Quiz 2: Definite Integrals', 'quiz', 20, '2026-10-05'),
    (1, 'Midterm Exam', 'midterm', 100, '2026-10-25'),
    (1, 'Final Exam', 'final', 100, '2026-12-15'),

    (2, 'Quiz 1: Matrix Operations', 'quiz', 20, '2026-09-18'),
    (2, 'Quiz 2: Vector Spaces', 'quiz', 20, '2026-10-08'),
    (2, 'Midterm Exam', 'midterm', 100, '2026-10-28'),
    (2, 'Final Exam', 'final', 100, '2026-12-18'),

    (3, 'Quiz 1: Arrays & Pointers', 'quiz', 20, '2026-09-20'),
    (3, 'Quiz 2: Trees & Graphs', 'quiz', 20, '2026-10-10'),
    (3, 'Midterm Exam', 'midterm', 100, '2026-10-30'),
    (3, 'Final Exam', 'final', 100, '2026-12-20'),

    (4, 'Quiz 1: Kinematics', 'quiz', 20, '2026-09-22'),
    (4, 'Quiz 2: Dynamics & Work', 'quiz', 20, '2026-10-12'),
    (4, 'Midterm Exam', 'midterm', 100, '2026-11-02'),
    (4, 'Final Exam', 'final', 100, '2026-12-22');
    """)

    await conn.execute("""
    INSERT INTO scores (student_id, assessment_id, score, submitted) VALUES
    (1, 1, 6, TRUE),
    (1, 2, 5, TRUE),
    (1, 3, 72, TRUE),
    (1, 4, 75, TRUE),
    (1, 5, 7, TRUE),
    (1, 6, 8, TRUE),
    (1, 7, 78, TRUE),
    (1, 8, 80, TRUE),
    (1, 9, 19, TRUE),
    (1, 10, 18, TRUE),
    (1, 11, 92, TRUE),
    (1, 12, 95, TRUE),

    (2, 1, 17, TRUE),
    (2, 2, 16, TRUE),
    (2, 3, 85, TRUE),
    (2, 4, 88, TRUE),
    (2, 13, 18, TRUE),
    (2, 14, 19, TRUE),
    (2, 15, 91, TRUE),
    (2, 16, 94, TRUE),

    (3, 5, 18, TRUE),
    (3, 6, 17, TRUE),
    (3, 7, 88, TRUE),
    (3, 8, 86, TRUE),
    (3, 9, 20, TRUE),
    (3, 10, 20, TRUE),
    (3, 11, 98, TRUE),
    (3, 12, 99, TRUE),
    (3, 13, 10, TRUE),
    (3, 14, 11, TRUE),
    (3, 15, 58, TRUE),
    (3, 16, 55, TRUE),

    (4, 1, 15, TRUE),
    (4, 2, 14, TRUE),
    (4, 3, 79, TRUE),
    (4, 4, 82, TRUE),
    (4, 9, 16, TRUE),
    (4, 10, 17, TRUE),
    (4, 11, 84, TRUE),
    (4, 12, 86, TRUE),
    (4, 13, 17, TRUE),
    (4, 14, 16, TRUE),
    (4, 15, 83, TRUE),
    (4, 16, 85, TRUE),

    (5, 5, 19, TRUE),
    (5, 6, 20, TRUE),
    (5, 7, 95, TRUE),
    (5, 8, 92, TRUE),
    (5, 9, 18, TRUE),
    (5, 10, 19, TRUE),
    (5, 11, 90, TRUE),
    (5, 12, 91, TRUE);
    """)

    await conn.execute("""
    INSERT INTO attendance (student_id, course_id, date, present) VALUES
    (1, 1, '2026-09-14', TRUE),
    (1, 1, '2026-09-16', TRUE),
    (1, 1, '2026-09-21', TRUE),
    (1, 1, '2026-09-23', TRUE),
    (1, 1, '2026-09-28', TRUE),
    (1, 1, '2026-09-30', TRUE),
    (1, 1, '2026-10-02', FALSE),
    (1, 1, '2026-10-05', FALSE),
    (1, 1, '2026-10-07', FALSE),
    (1, 1, '2026-10-12', TRUE),

    (2, 1, '2026-09-14', TRUE),
    (2, 1, '2026-09-16', TRUE),
    (2, 1, '2026-09-21', TRUE),
    (2, 1, '2026-09-23', TRUE),
    (2, 1, '2026-09-28', TRUE),
    (2, 1, '2026-09-30', TRUE),
    (2, 1, '2026-10-02', TRUE),
    (2, 1, '2026-10-05', TRUE),
    (2, 1, '2026-10-07', TRUE),
    (2, 1, '2026-10-12', TRUE),

    (4, 1, '2026-09-14', TRUE),
    (4, 1, '2026-09-16', TRUE),
    (4, 1, '2026-09-21', FALSE),
    (4, 1, '2026-09-23', TRUE),
    (4, 1, '2026-09-28', TRUE),
    (4, 1, '2026-09-30', TRUE),
    (4, 1, '2026-10-02', TRUE),
    (4, 1, '2026-10-05', TRUE),
    (4, 1, '2026-10-07', TRUE),
    (4, 1, '2026-10-12', TRUE),

    (1, 2, '2026-09-15', TRUE),
    (1, 2, '2026-09-17', TRUE),
    (1, 2, '2026-09-22', TRUE),
    (1, 2, '2026-09-24', TRUE),
    (1, 2, '2026-09-29', TRUE),
    (1, 2, '2026-10-01', TRUE),
    (1, 2, '2026-10-06', TRUE),
    (1, 2, '2026-10-08', TRUE),
    (1, 2, '2026-10-13', TRUE),
    (1, 2, '2026-10-15', TRUE),

    (3, 2, '2026-09-15', TRUE),
    (3, 2, '2026-09-17', TRUE),
    (3, 2, '2026-09-22', TRUE),
    (3, 2, '2026-09-24', TRUE),
    (3, 2, '2026-09-29', FALSE),
    (3, 2, '2026-10-01', TRUE),
    (3, 2, '2026-10-06', TRUE),
    (3, 2, '2026-10-08', TRUE),
    (3, 2, '2026-10-13', TRUE),
    (3, 2, '2026-10-15', TRUE),

    (5, 2, '2026-09-15', TRUE),
    (5, 2, '2026-09-17', TRUE),
    (5, 2, '2026-09-22', TRUE),
    (5, 2, '2026-09-24', TRUE),
    (5, 2, '2026-09-29', TRUE),
    (5, 2, '2026-10-01', TRUE),
    (5, 2, '2026-10-06', TRUE),
    (5, 2, '2026-10-08', TRUE),
    (5, 2, '2026-10-13', TRUE),
    (5, 2, '2026-10-15', TRUE),

    (1, 3, '2026-09-14', TRUE),
    (1, 3, '2026-09-16', TRUE),
    (1, 3, '2026-09-21', TRUE),
    (1, 3, '2026-09-23', TRUE),
    (1, 3, '2026-09-28', TRUE),
    (1, 3, '2026-09-30', TRUE),
    (1, 3, '2026-10-02', TRUE),
    (1, 3, '2026-10-05', TRUE),
    (1, 3, '2026-10-07', TRUE),
    (1, 3, '2026-10-12', TRUE),

    (3, 3, '2026-09-14', TRUE),
    (3, 3, '2026-09-16', TRUE),
    (3, 3, '2026-09-21', TRUE),
    (3, 3, '2026-09-23', TRUE),
    (3, 3, '2026-09-28', TRUE),
    (3, 3, '2026-09-30', TRUE),
    (3, 3, '2026-10-02', TRUE),
    (3, 3, '2026-10-05', TRUE),
    (3, 3, '2026-10-07', TRUE),
    (3, 3, '2026-10-12', TRUE),

    (4, 3, '2026-09-14', TRUE),
    (4, 3, '2026-09-16', TRUE),
    (4, 3, '2026-09-21', TRUE),
    (4, 3, '2026-09-23', FALSE),
    (4, 3, '2026-09-28', TRUE),
    (4, 3, '2026-09-30', TRUE),
    (4, 3, '2026-10-02', TRUE),
    (4, 3, '2026-10-05', TRUE),
    (4, 3, '2026-10-07', TRUE),
    (4, 3, '2026-10-12', TRUE),

    (5, 3, '2026-09-14', TRUE),
    (5, 3, '2026-09-16', TRUE),
    (5, 3, '2026-09-21', TRUE),
    (5, 3, '2026-09-23', TRUE),
    (5, 3, '2026-09-28', TRUE),
    (5, 3, '2026-09-30', TRUE),
    (5, 3, '2026-10-02', TRUE),
    (5, 3, '2026-10-05', TRUE),
    (5, 3, '2026-10-07', TRUE),
    (5, 3, '2026-10-12', TRUE),

    (2, 4, '2026-09-15', TRUE),
    (2, 4, '2026-09-17', TRUE),
    (2, 4, '2026-09-22', TRUE),
    (2, 4, '2026-09-24', TRUE),
    (2, 4, '2026-09-29', TRUE),
    (2, 4, '2026-10-01', TRUE),
    (2, 4, '2026-10-06', TRUE),
    (2, 4, '2026-10-08', TRUE),
    (2, 4, '2026-10-13', TRUE),
    (2, 4, '2026-10-15', TRUE),

    (3, 4, '2026-09-15', FALSE),
    (3, 4, '2026-09-17', TRUE),
    (3, 4, '2026-09-22', FALSE),
    (3, 4, '2026-09-24', TRUE),
    (3, 4, '2026-09-29', TRUE),
    (3, 4, '2026-10-01', FALSE),
    (3, 4, '2026-10-06', TRUE),
    (3, 4, '2026-10-08', TRUE),
    (3, 4, '2026-10-13', TRUE),
    (3, 4, '2026-10-15', TRUE),

    (4, 4, '2026-09-15', TRUE),
    (4, 4, '2026-09-17', TRUE),
    (4, 4, '2026-09-22', TRUE),
    (4, 4, '2026-09-24', TRUE),
    (4, 4, '2026-09-29', TRUE),
    (4, 4, '2026-10-01', TRUE),
    (4, 4, '2026-10-06', TRUE),
    (4, 4, '2026-10-08', TRUE),
    (4, 4, '2026-10-13', TRUE),
    (4, 4, '2026-10-15', TRUE);
    """)


async def main():
    conn = await asyncpg.connect(DATABASE_URL)

    await create_tables(conn)
    await seed_data(conn)

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())