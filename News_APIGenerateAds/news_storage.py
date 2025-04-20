# news_storage.py

import sqlite3

def create_news_table():
    conn = sqlite3.connect("news_ads.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pincode TEXT,
            product TEXT,
            location TEXT,
            headline TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_news(pincode, product, location, headlines):
    conn = sqlite3.connect("news_ads.db")
    cursor = conn.cursor()
    for headline in headlines:
        cursor.execute("""
            INSERT INTO news_data (pincode, product, location, headline)
            VALUES (?, ?, ?, ?)
        """, (pincode, product, location, headline))
    conn.commit()
    conn.close()

def fetch_news_from_db(pincode, product):
    conn = sqlite3.connect("news_ads.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT location, headline FROM news_data
        WHERE pincode = ? AND product = ?
    """, (pincode, product))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return None, []
    location = rows[0][0]
    headlines = [row[1] for row in rows]
    return location, headlines
