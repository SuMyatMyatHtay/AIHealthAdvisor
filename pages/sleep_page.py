import streamlit as st
import mysql.connector
import os
import json
import subprocess

from datetime import datetime
from datetime import date
from mysql.connector import Error
import pages.faceupload_page as faceupload

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
temp_data_path = os.path.join(parent_directory, 'tempData.json')
facedetect_script = os.path.join(parent_directory, "faceDetect.py")

start_sleep_time = ""
end_sleep_time = ""
facedetect_duration = 0 
sleep_duration = 0 
is_sleeping = False

def load_faceDetect_duration():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data.get("faceDetect_duration")
    return 0

def start_subprocess():
    return subprocess.Popen(["python", facedetect_script])

def terminate_subprocess(process):
    if process and process.poll() is None:
        print("Terminating the subprocess...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Killing the subprocess...")
            process.kill()
        st.rerun()

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot"
    )
    return connection

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  
            database="iot"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.write(f"Error: {e}")
        return None

def user_exists_in_db(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM userinfo WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    return False

def insert_sleep_data(user_id, facedetect_duration, sleep_duration):
    print("Insert Sleep Data")
    if sleep_duration < 1 and facedetect_duration < 1:
        print("Duration too short, not saving in db")
    else:
        print("Should be saved")
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO sleeptrack (user_id, start_time, end_time, sleep_minute, facedetected_minute, date) VALUES (%s, %s, %s, %s, %s, %s)',
                (user_id, start_sleep_time, end_sleep_time, sleep_duration, facedetect_duration, date.today().strftime("%Y-%m-%d"))
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                return False
            else:
                raise err
        finally:
            cursor.close()
            conn.close()

def sleep_page():
    if not os.path.exists(temp_data_path):
        st.error("User not logged in. Redirect to the first app page for login.")
        return
    global start_sleep_time, end_sleep_time, sleep_duration, facedetect_duration, is_sleeping

    st.title("Sleep Page")
    
    try:
        with open(temp_data_path, 'r') as file:
            data = json.load(file)
            user_id = data.get('user_id')
            username = data.get('username')
    except FileNotFoundError:
        st.error(f"File {temp_data_path} not found.")
        return
    except json.JSONDecodeError:
        st.error("Error decoding JSON from the file.")
        return

    if user_id is None:
        st.error("No user_id found in tempData.json.")
        return

    if username is None:
        st.error("No username found in tempData.json.")
        return

    if not user_exists_in_db(user_id): 
        st.error("User information not found. Please complete your profile.")
        return
    
    st.write("Welcome to the sleep optimization page! The camera will be opened once you decided to sleep and it will be closed once you wake up.")

    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT EXISTS(SELECT 1 FROM faceregister WHERE user_id = %s)"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result[0]:
                # st.success(f"user_id {user_id} exists in the sleep table.")

                if 'test_process' not in st.session_state:
                    st.session_state.test_process = None

                if is_sleeping == False: 
                    if st.button("Sleep"):
                        print("Sleep Button")
                        is_sleeping = True
                        st.write("The user is sleeping. Face Detection is On. Good Night!")
                        st.session_state.test_process = start_subprocess()
                        start_sleep_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if st.session_state.test_process is not None:
                    if st.button("Wake Up"):
                        print("Wake Up Button")
                        is_sleeping = False
                        facedetect_duration = load_faceDetect_duration()
                        if st.session_state.test_process is not None:
                            end_sleep_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            start_dt = datetime.strptime(start_sleep_time, '%Y-%m-%d %H:%M:%S')
                            end_dt = datetime.strptime(end_sleep_time, '%Y-%m-%d %H:%M:%S')
                            sleep_duration = ((end_dt - start_dt).total_seconds() / 60) - facedetect_duration
                            print(sleep_duration)
                            insert_sleep_data(user_id, facedetect_duration, sleep_duration)
                            terminate_subprocess(st.session_state.test_process)
                            st.session_state.test_process = None

            else:
                st.warning(f"username: {username} face is not registered yet to use this sleep optimization function.")
                faceupload.faceupload_page()

    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    sleep_page()
