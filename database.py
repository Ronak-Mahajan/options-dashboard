import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "calculations.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                spot_price REAL NOT NULL,
                strike_price REAL NOT NULL,
                time_to_expiry REAL NOT NULL,
                risk_free_rate REAL NOT NULL,
                volatility REAL NOT NULL,
                call_price REAL NOT NULL,
                put_price REAL NOT NULL
            )
        """)


def save_calculation(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call_price: float,
    put_price: float,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO calculations 
            (timestamp, spot_price, strike_price, time_to_expiry, risk_free_rate, volatility, call_price, put_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                S,
                K,
                T,
                r,
                sigma,
                call_price,
                put_price,
            ),
        )


def fetch_recent(limit: int = 10) -> list[dict]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            """
            SELECT timestamp, spot_price, strike_price, time_to_expiry, 
                   risk_free_rate, volatility, call_price, put_price
            FROM calculations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]


init_db()
