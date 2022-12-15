import psycopg2
from Quiz_DAL.config import *

try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    # the cursor for perfoming database operations
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"server version - {cursor.fetchone()}")

except Exception as _ex:
    print("[INFO] Error - ", _ex)
    print(connection)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
