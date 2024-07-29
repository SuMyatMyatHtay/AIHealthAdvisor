import streamlit as st
import mysql.connector
import os
import json
import subprocess

from mysql.connector import Error

import pages.faceupload_page as faceupload

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(parent_directory, 'tempData.json')

facedetect_script = os.path.join(parent_directory, "faceDetect.py")

# Function to start the subprocess
def start_subprocess():
    return subprocess.Popen(["python", facedetect_script])

# Function to terminate the subprocess
def terminate_subprocess(process):
    if process.poll() is None:  # Check if the process is still running
        print("Terminating the subprocess...")
        process.terminate()
        try:
            # Wait for the process to terminate gracefully
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If the process does not terminate in the given time, kill it
            print("Killing the subprocess...")
            process.kill()
        st.rerun()

# Home Page Function
def sleep_page():
    st.title("Sleep Page")
    st.write("Welcome to the sleep optimization page!")

    # Load user_id from tempData.json
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

    # Connect to the MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="iot"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Check if user_id exists in the sleep table
            query = "SELECT EXISTS(SELECT 1 FROM faceregister WHERE user_id = %s)"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result[0]:
                st.success(f"user_id {user_id} exists in the sleep table.")

                # Initialize session state if it doesn't exist
                if 'test_process' not in st.session_state:
                    st.session_state.test_process = None

                if st.button("Sleep"):
                    st.write("The user is sleeping. Face Detection is On. Good Night!")
                    
                    # Start the subprocess
                    st.session_state.test_process = start_subprocess()

                # Display the "Wake Up" button only if the process is running
                if st.session_state.test_process is not None:
                    if st.button("Wake Up"):
                        # Terminate the subprocess if it's running
                        if st.session_state.test_process is not None:
                            terminate_subprocess(st.session_state.test_process)
                            st.session_state.test_process = None  # Reset the state
            else:
                st.warning(f"user_id {user_id} does not exist in the faceregister table.")
                faceupload.faceupload_page() 

    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    sleep_page()
