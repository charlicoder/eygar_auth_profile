import psycopg2
from psycopg2 import sql, OperationalError

# === AWS RDS connection settings ===
RDS_HOST = "eygar.cnyaamgc24kg.eu-west-1.rds.amazonaws.com"  # e.g., mydb.xxxxxx.us-east-1.rds.amazonaws.com
RDS_PORT = 5432
RDS_USER = "postgres"
RDS_PASSWORD = "u8aJPXQtTZgMkECn0DZ0"
NEW_DATABASE_NAME = "eygarprofile"


def create_connection():
    """Create a connection to the RDS PostgreSQL instance"""
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            dbname="postgres",  # connect to default database first
            sslmode="require",  # RDS usually requires SSL
        )
        print("✅ Connection to RDS successful.")
        return conn
    except OperationalError as e:
        print(f"❌ Error connecting to RDS: {e}")
        return None


def create_database(conn, db_name):
    """Create a new PostgreSQL database on RDS"""
    try:
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [db_name]
        )
        exists = cursor.fetchone()
        if exists:
            print(f"⚠️ Database '{db_name}' already exists.")
        else:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"✅ Database '{db_name}' created successfully.")

        cursor.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_database(connection, NEW_DATABASE_NAME)
