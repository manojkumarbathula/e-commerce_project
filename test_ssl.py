import os
from dotenv import load_dotenv
from mysql.connector import connection

load_dotenv()

try:
    mydb = connection.MySQLConnection(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA"),
        ssl_verify_cert=True
    )

    print("Database connected:", mydb.is_connected())

    if mydb.is_connected():
        cursor = mydb.cursor()
        cursor.execute("SHOW TABLES")

        print("Tables in database:")
        for table in cursor:
            print(table[0])

        cursor.close()
        mydb.close()

except Exception as e:
    print("Connection failed:", type(e).__name__)
    print("Error:", e)