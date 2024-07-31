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

        # Check if the users table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        result_users = cursor.fetchone()

        if result_users:
            print("Users table already exists.")
        else:
            cursor.execute("""
                CREATE TABLE users(
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(255) NOT NULL UNIQUE, 
                    password VARCHAR(255) NOT NULL 
                )
            """)
            print("Users table created successfully.")

        # Check if the sensor table exists 
        cursor.execute("SHOW TABLES LIKE 'sensor'")
        result_sensor = cursor.fetchone()

        if result_sensor: 
            print("Sensor table already exists.")
        else: 
            cursor.execute("""
                           CREATE TABLE `sensor` (
                                `datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
                                `sensor` text NOT NULL,
                                `value` text NOT NULL
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                           """)

        # Check if the faceregister table exists
        cursor.execute("SHOW TABLES LIKE 'faceregister'")
        result_faceregister = cursor.fetchone()

        if result_faceregister:
            print("faceregister table already exists.")
        else:
            cursor.execute("""
                CREATE TABLE faceregister(
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11),
                    status VARCHAR(255) NOT NULL
                )
            """)
            print("faceregister table created successfully.")


        # Check if the sleeptrack table exists
        cursor.execute("SHOW TABLES LIKE 'sleeptrack'")
        result_sleeptrack = cursor.fetchone()

        if result_sleeptrack: 
            print("sleeptrack table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE sleeptrack ( 
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11), 
                    start_time VARCHAR(255) NOT NULL, 
                    end_time VARCHAR(255) NOT NULL, 
                    sleep_minute INT(11) NOT NULL,
                    facedetected_minute INT(11) NOT NULL
                )
            """)
            print("sleeptrack table created successfully.")


        # Check if the userinfo table exists
        cursor.execute("SHOW TABLES LIKE 'userinfo'")
        result_userinfo = cursor.fetchone()

        if result_userinfo: 
            print("userinfo table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE userinfo ( 
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11) NOT NULL, 
                    gender VARCHAR(255), 
                    age INT(11), 
                    birthdate VARCHAR(255), 
                    height INT(11),
                    weight DECIMAL(10, 2),
                    goal VARCHAR(255)
                )
            """)
            print("userinfo table created successfully.")

        # Check if the usermeals table exists
        cursor.execute("SHOW TABLES LIKE 'usermeals'")
        result_usermeals = cursor.fetchone()

        if result_usermeals: 
            print("usermeals table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE usermeals ( 
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
                    calories INT NOT NULL,
                    date DATE NOT NULL,
                    user_id INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES userinfo(id)
                )
            """)
            print("usermeals table created successfully.")

    except mysql.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    create_database_and_table()
