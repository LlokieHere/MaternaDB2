import psycopg2
#NOTE: If you want to connect to Supabase, uncomment the following function and comment 
#out the local connection function. Make sure to replace the credentials with your actual 
#Supabase credentials.


# def get_connection():
#     try:
#         conn = psycopg2.connect(
#             host="aws-1-ap-northeast-1.pooler.supabase.com",
#             port=5432,
#             database="postgres",
#             user="postgres.vnygeyyyzrugzpgclvje",  # ← make sure this is exact
#             password="MaternaDB789"
#         )
#         print("✅ Connected to Supabase successfully!")
#         return conn
#     except Exception as e:
#         print(f"❌ Connection error: {e}")
#         return None

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="materna_db",    # ← your local DB name
            user="postgres",          # ← your local username
            password="Kr1sR00T_365"  # ← your local password
        )
        print("✅ Connected to local DB successfully!")
        return conn
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None