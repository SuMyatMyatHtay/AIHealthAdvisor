import streamlit as st
import os
import json
import mysql.connector as mysql
from mysql.connector import Error

import pages.login_page as login
import pages.home_page as home
import pages.sleep_page as sleep
import pages.nutrition_planner_page as nutrition_planner
import pages.nutrition_tracker_page as nutrition_tracker
import pages.user_page as user_planner
import pages.statistics_page as statistics
import pages.exercises_page as exercises
import pages.userinfo_form as userinfoform

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(current_directory, 'tempData.json')

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

def load_user_id():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data.get("user_id")
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

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Sleep Optimization", "Nutrition Planner","Nutrition Tracker", "User Page", "Statistics Page", "Exercises Page"])

    if page == "Home":
        home.home_page()
    elif page == "Sleep Optimization": 
        sleep.sleep_page()
    elif page == "Nutrition Planner":
        nutrition_planner.nutrition_planner_page()
    elif page == "Nutrition Tracker":
        nutrition_tracker.nutrition_tracker_page()
    elif page == "User Page":
        user_planner.user_page()
    elif page == "Statistics Page":
        statistics.statistics()
    elif page == "Exercises Page":
        exercises.exercises_page()

hide_streamlit_style = """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebarNavItems"] { display: none; }
    [data-testid="stSidebarNavSeparator"] { display: none; }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if os.path.exists(temp_data_path):
    user_id = load_user_id()

    # Hide the default Streamlit sidebar elements
    

    if user_id and user_exists_in_db(user_id):
        main()
    else:
        st.error("User information not found. Please complete your profile.")
        userinfoform.userinfo_form()  # Redirect to user info form page
else:
    login.login_page()
