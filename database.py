import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="materna_db",    # your database name
            user="postgres",         # your postgres username
            password="Kr1sR00T_365", # your postgres password
            port="5432"              # default postgres port
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None