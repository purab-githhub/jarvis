from database import get_connection


def add_note(title, content, subject="General"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, subject) VALUES (?, ?, ?)", (title, content, subject))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id


def view_notes(subject=None):
    conn = get_connection()
    cursor = conn.cursor()
    if subject:
        cursor.execute("SELECT id, title, subject, created_at FROM notes WHERE LOWER(subject) = LOWER(?) ORDER BY id DESC", (subject,))
    else:
        cursor.execute("SELECT id, title, subject, created_at FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()
    conn.close()
    return notes


def get_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, subject, created_at FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note


def search_notes(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute("SELECT id, title, subject, created_at FROM notes WHERE title LIKE ? OR content LIKE ? OR subject LIKE ? ORDER BY id DESC", (pattern, pattern, pattern))
    notes = cursor.fetchall()
    conn.close()
    return notes
