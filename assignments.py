from database import get_connection


def add_assignment(title, subject="General", due_date=None, due_time=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO assignments (title, subject, due_date, due_time)
        VALUES (?, ?, ?, ?)
        """,
        (title, subject, due_date, due_time),
    )
    conn.commit()
    assignment_id = cursor.lastrowid
    conn.close()
    return assignment_id


def view_assignments(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT id, title, subject, due_date, due_time, status FROM assignments"
    params = ()
    if status:
        query += " WHERE status = ?"
        params = (status,)
    query += " ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date, due_time, id"
    cursor.execute(query, params)
    assignments = cursor.fetchall()
    conn.close()
    return assignments


def complete_assignment(assignment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE assignments SET status = 'Completed' WHERE id = ? AND status != 'Completed'",
        (assignment_id,),
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0
