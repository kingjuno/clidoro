import os
import sqlite3


def save_to_db(dates, cache_dir):
    conn = sqlite3.connect(f"{cache_dir}/clidoro.sqlite")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS random_data (
            id INTEGER PRIMARY KEY,
            date TEXT,
            amount INTEGER
        )
    """
    )
    cursor.executemany("INSERT INTO random_data (date, amount) VALUES (?, ?)", dates)
    conn.commit()
    conn.close()


def clear_db(cache_dir):
    db_path = os.path.join(cache_dir, "clidoro.sqlite")
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except:
        ...
