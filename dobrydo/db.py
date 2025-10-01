import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH: Path = Path.home() / ".dobrydo" / "dobrydo.db"


@contextmanager
def get_db():
    """Get database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database and create tables if missing."""
    with get_db() as conn:
        cur = conn.cursor()

        # Create tasks table
        _ = cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                tags TEXT
            );
        """
        )
