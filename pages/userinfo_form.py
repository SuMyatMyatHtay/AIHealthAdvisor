import streamlit as st
import mysql.connector as mysql
from mysql.connector import Error
import os
import json
from datetime import datetime

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(parent_directory, 'tempData.json')

def load_user_id():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data.get("user_id")
    return None

# Function to create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connect(
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

def calculate_age(birthdate):
    today = datetime.today()
    birth_date = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def store_user_details(user_id, gender, birthdate, height, goal, weight, sleep_goal_hour):
    age = calculate_age(birthdate)
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO userinfo (user_id, gender, age, birthdate, height, goal, weight, sleep_goal_hour) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            gender = VALUES(gender),
            age = VALUES(age),
            birthdate = VALUES(birthdate),
            height = VALUES(height),
            goal = VALUES(goal),
            weight = VALUES(weight),
            sleep_goal_hour = VALUES(sleep_goal_hour)           
        ''', (user_id, gender, age, birthdate, height, goal, weight, sleep_goal_hour))
        conn.commit()
        conn.close()

def userinfo_form():
    # Check if tempData.json exists
    if not os.path.exists(temp_data_path):
        st.error("User not logged in. Redirect to the first app page for login.")
        return
    
    st.title("User Information Form")
    user_id = load_user_id()  # Load user ID from JSON file

    if user_id:
        with st.form(key='user_info_form'):
            gender = st.selectbox("Gender", ["Male", "Female"])
            birthdate = st.date_input("Birthdate", value=datetime.today().date(), min_value=datetime(1900, 1, 1))
            height = st.number_input("Height (cm)", min_value=0)
            goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Maintain Weight"])
            weight = st.number_input("Weight (kg)", min_value=0)
            sleep_goal_hour = st.number_input("Sleep Goal (hours)", min_value=1, max_value=12)
            submit_button = st.form_submit_button("Submit")
            
            if submit_button:
                store_user_details(user_id, gender, birthdate.strftime('%Y-%m-%d'), height, goal, weight, sleep_goal_hour)
                st.success("User details saved successfully!")
                st.rerun()
    else:
        st.error("User ID not found. Please make sure you are logged in.")

if __name__ == "__main__":
    userinfo_form()
