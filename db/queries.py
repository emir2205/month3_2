tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        date TEXT
    )
"""

read_tasks = """
    SELECT id, task, date FROM tasks ORDER BY id DESC
"""

update_tasks = """
    UPDATE tasks SET task = ? WHERE id = ?
"""

delete_tasks = """
    DELETE FROM tasks WHERE id = ?
"""

insert_tasks = """
    INSERT INTO tasks (task, date) VALUES (?, ?)
"""
