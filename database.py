import sqlite3
from typing import Dict, Optional

DATABASE_NAME = "blackjack.db"

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_NAME)

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            ties INTEGER DEFAULT 0,
            total_games INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            winner TEXT,
            player_score INTEGER,
            dealer_score INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def get_player_stats(user_id: int) -> Dict[str, int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT wins, losses, ties, total_games FROM players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"wins": row[0], "losses": row[1], "ties": row[2], "total_games": row[3]}
    return {"wins": 0, "losses": 0, "ties": 0, "total_games": 0}

def update_player_stats(user_id: int, result: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE players SET total_games = total_games + 1 WHERE user_id = ?", (user_id,))

    field = "wins" if result == "win" else "losses" if result == "loss" else "ties"
    cursor.execute(f"UPDATE players SET {field} = {field} + 1 WHERE user_id = ?", (user_id,))

    if cursor.rowcount == 0:
        wins = 1 if result == "win" else 0
        losses = 1 if result == "loss" else 0
        ties = 1 if result == "tie" else 0
        cursor.execute(
            "INSERT INTO players (user_id, wins, losses, ties, total_games) VALUES (?, ?, ?, ?, ?)",
            (user_id, wins, losses, ties, 1)
        )

    conn.commit()
    conn.close()

def save_game_history(user_id: int, winner: str, player_score: int, dealer_score: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO games_history (user_id, winner, player_score, dealer_score) VALUES (?, ?, ?, ?)",
        (user_id, winner, player_score, dealer_score)
    )
    conn.commit()
    conn.close()

def get_history(user_id: int, limit: int = 5) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT winner, player_score, dealer_score, date FROM games_history WHERE user_id = ? ORDER BY date DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows