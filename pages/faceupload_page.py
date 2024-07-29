import streamlit as st
import mysql.connector
import os
import json
import time
import subprocess

from mysql.connector import Error

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(parent_directory, 'tempData.json')

appmodel_script = parent_directory + "/ciot_app_model.py"

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='iot'
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None
    
# Function to check if user_id exists in the sleep table
def check_user_id_exists(connection, user_id):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM faceregister WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0

# Function to insert data into the sleep table
def insert_sleep_data(connection, user_id, status):
    cursor = connection.cursor()
    query = "INSERT INTO faceregister (user_id, status) VALUES (%s, %s)"
    cursor.execute(query, (user_id, status))
    connection.commit()
    cursor.close()

# Home Page Function
def faceupload_page():
    st.title("Face Upload Page")
    st.write("Please upload your photos to update your profile.")

    try:
        with open(temp_data_path, 'r') as file:
            data = json.load(file)
            user_id = data.get('user_id')
            username = data.get('username')
    except: 
        return 
    
    # Establish database connection
    connection = create_connection()
    if connection is None:
        return
    
    # Check if user_id exists in the sleep table
    if check_user_id_exists(connection, user_id):
        st.write("Data already exists for your user_id.")
        connection.close()
        return

    # Create the user-specific directory
    user_test_directory = os.path.join(parent_directory, 'datasets', 'test', username)
    os.makedirs(user_test_directory, exist_ok=True)

    user_train_directory = os.path.join(parent_directory, 'datasets', 'train', username)
    os.makedirs(user_train_directory, exist_ok=True)

    user_valid_directory = os.path.join(parent_directory, 'datasets', 'valid', username)
    os.makedirs(user_valid_directory, exist_ok=True)

    # File uploader for multiple photos
    uploaded_files = st.file_uploader("Choose photos...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Initialize session state for the button if it doesn't exist
    if "save_button_clicked" not in st.session_state:
        st.session_state.save_button_clicked = False
    
    if uploaded_files:
        if not st.session_state.save_button_clicked:
            if st.button("Save"):
                # Save each uploaded file to the user-specific directory
                for uploaded_file in uploaded_files:
                    file_path_test = os.path.join(user_test_directory, uploaded_file.name)
                    with open(file_path_test, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    file_path_train = os.path.join(user_train_directory, uploaded_file.name)
                    with open(file_path_train, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    file_path_valid = os.path.join(user_valid_directory, uploaded_file.name)
                    with open(file_path_valid, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    
                # Set session state to reflect upload completion
                st.session_state.save_button_clicked = True
                st.success("Files successfully uploaded.")

                subprocess.Popen(["python", appmodel_script])

                insert_sleep_data(connection, user_id, "Completed")
                connection.close()


                # Wait for 5 seconds before reloading the page
                time.sleep(5)
                st.rerun()
        else:
            st.button("Save", disabled=True)
    else:
        st.button("Save", disabled=True)

