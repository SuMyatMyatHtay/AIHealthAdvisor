import mysql.connector as mysql

def create_database_and_table():
    try:
        # Connect to MySQL without specifying a database
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd=""
        )

        cursor = db.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS IOT")
        print("Database checked/created successfully.")

        # Connect to the IOT database
        db.database = "iot"

        # Check if the table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        result = cursor.fetchone()

        if result:
            print("Table already exists.")
        else:
            cursor.execute("""
                CREATE TABLE users(
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(255) NOT NULL UNIQUE, 
                    password VARCHAR(255) NOT NULL 
                )
            """)
            print("Table created successfully.")

    except mysql.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    create_database_and_table()
