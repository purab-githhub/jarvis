from datetime import datetime

from database import get_connection


def add_task(title, category="General", due_date=None, due_time=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (title, category, due_date, due_time)
        VALUES (?, ?, ?, ?)
        """,
        (title, category, due_date, due_time),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def view_tasks(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, title, category, due_date, due_time, status FROM tasks"
    params = ()
    if status:
        query += " WHERE status = ?"
        params = (status,)
    query += " ORDER BY due_date IS NULL, due_date, due_time IS NULL, due_time, id"
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def get_due_tasks(now=None):
    now = now or datetime.now()
    current_date = now.date().isoformat()
    current_time = now.strftime("%H:%M")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, due_date, due_time
        FROM tasks
        WHERE status = 'Pending'
          AND due_date IS NOT NULL
          AND (
              due_date < ?
              OR (due_date = ? AND (due_time IS NULL OR due_time <= ?))
          )
        ORDER BY due_date, due_time IS NULL, due_time, id
        """,
        (current_date, current_date, current_time),
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ? AND status != 'Completed'",
        (task_id,),
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0
