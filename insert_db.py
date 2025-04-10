import psycopg2
from datetime import date

def insert_trends_to_db(trends, table_name="google_trends_now"):
    conn = psycopg2.connect(
        dbname="advantage_db",
        user="harsha",
        password="0317",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    for trend in trends:
        topic = trend["topic"]
        volume = trend["volume"]
        start_time = trend["start_time"]

        cursor.execute(f"""
            INSERT INTO {table_name} (topic, volume, start_time, scraped_date)
            VALUES (%s, %s, %s, %s)
        """, (topic, volume, start_time, date.today()))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(trends)} trends into table: {table_name}")
