import psycopg2

def fetch_trends_from_db(table_name="google_trends_now", limit=10):
    conn = psycopg2.connect(
        dbname="advantage_db2",
        user="pranav",
        password="2104",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT topic FROM {table_name}
        ORDER BY scraped_date DESC, id DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    # Convert list of tuples to list of strings
    return [r[0] for r in rows]
