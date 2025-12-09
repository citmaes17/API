import sqlite3

DB_PATH = "leadflow.db"

def get_db():
    """
    Dependencia para FastAPI.
    Abre una conexión a SQLite, la cede con yield y luego la cierra.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def row_to_dict(row):
    return dict(row) if row is not None else None
