import streamlit as st
import mysql.connector
import os
import json
import requests
from mysql.connector import Error
from datetime import datetime, date

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

def load_username():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data.get("username")
    return None

# Function to create a connection to the MySQL database
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

def delete_user_id():
    if os.path.exists(temp_data_path):
        os.remove(temp_data_path)

def get_sleep_data(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT sleep_goal_hour FROM userinfo WHERE user_id = %s;''', (user_id,))
        sleep_goal = cursor.fetchone()
        
        cursor.execute('''SELECT SUM(facedetected_minute), SUM(sleep_minute) FROM sleeptrack WHERE user_id = %s AND date = %s;''', (user_id,  date.today().strftime("%Y-%m-%d")))
        sleep_data = cursor.fetchone()
        
        conn.close()
            
        # If sleep_goal is not None, use its value; otherwise, return None
        sleep_goal_value = float(sleep_goal[0]) if sleep_goal and sleep_goal[0] is not None else None

        if sleep_data:
            facedetected_minute = int(sleep_data[0]) if sleep_data[0] is not None else None
            sleep_minute = float(sleep_data[1]) if sleep_data[1] is not None else None
        else:
            facedetected_minute = None
            sleep_minute = None

        return sleep_goal_value, facedetected_minute, sleep_minute
    else:
        return None, None, None

def create_card(title, content, background_color):
    st.markdown(
        f"""
        <div style="
            background-color: {background_color};
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 10px;
            width: 100%;
            max-width: 450px;
            height: 200px;
            overflow: auto;
            display: inline-block;
            vertical-align: top;
        ">
            <h4 style="margin-top: 0;">{title}</h4>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Home Page Function
def home_page():
    st.title("Home Page")
    st.write("Welcome to the main page!")

    user_id = load_user_id()
    username = load_username() 

    if user_id: 
        sleep_goal, wake_ups, net_sleep_hours = get_sleep_data(user_id)
        if wake_ups is None: 
            wake_ups = 0 
        if net_sleep_hours is None: 
            net_sleep_hours = 0 
        showSleepHour = ""
        if net_sleep_hours < 60: 
            showSleepHour = str(net_sleep_hours) + " minutes"
        else: 
            showSleepHour = str(net_sleep_hours/60) + " hours"

        col1, col2 = st.columns(2)

        with col1:
            create_card('Good Sleep is Good Health ', f'Dear {username}, Today you have slept for {showSleepHour}', '#a83263')  

        with col2:
            create_card('Oh no! What is disturbing to your sleep?!', f'Dear {username}, you have woke up {wake_ups} times today (last night).', '#8732a8')  


        try:
            response = requests.get("http://127.0.0.1:1880/steps")
            data = response.json()
            steps_today = data['steps']
        except Exception as e:
            steps_today = "Error fetching data"

        col3, col4 = st.columns(2)

        with col3: 
            create_card('One Step Far From Your Dreams', f'Dear {username}, Today you have walked for {steps_today} steps', '#002869')  

    if st.button("Logout"):
        delete_user_id()
        st.rerun()
