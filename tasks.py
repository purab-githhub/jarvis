from database import get_connection


def add_task(title, category="General", due_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, category, due_date)
        VALUES (?, ?, ?)
        """,
        (title, category, due_date),
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return task_id


def view_tasks(status=None):
    conn = get_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute(
            "SELECT id, title, category, due_date, status FROM tasks WHERE status = ? ORDER BY id",
            (status,),
        )
    else:
        cursor.execute(
            "SELECT id, title, category, due_date, status FROM tasks ORDER BY id"
        )

    tasks = cursor.fetchall()
    conn.close()

    return tasks


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,),
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0
