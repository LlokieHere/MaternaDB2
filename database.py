import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="aws-1-ap-northeast-1.pooler.supabase.com",
            port=5432,
            database="postgres",
            user="postgres.vnygeyyyzrugzpgclvje",  # ← make sure this is exact
            password="MaternaDB789"
        )
        print("✅ Connected to Supabase successfully!")
        return conn
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None