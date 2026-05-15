import sqlite3

DB_PATH = "tracker.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            coin          TEXT NOT NULL,
            days          INTEGER NOT NULL,
            current_price REAL NOT NULL,
            high          REAL NOT NULL,
            low           REAL NOT NULL,
            change_pct    REAL NOT NULL,
            avg_price     REAL NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_snapshot(coin, days, current_price, high, low, change_pct, avg_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO snapshots (coin, days, current_price, high, low, change_pct, avg_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (coin, days, current_price, high, low, change_pct, avg_price),
    )
    conn.commit()
    conn.close()


def get_snapshots():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM snapshots
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
