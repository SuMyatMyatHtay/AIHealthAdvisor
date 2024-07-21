import streamlit as st
import pandas as pd
import mysql.connector
import json
import os
import hashlib

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
temp_data_path = os.path.join(current_directory, 'tempData.json')

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_id(user_id):
    with open(temp_data_path, 'w') as f:
        json.dump({"user_id": user_id}, f)

def load_user_id():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data.get("user_id")
    return None

def delete_user_id():
    if os.path.exists(temp_data_path):
        os.remove(temp_data_path)

# Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot"
    )
    return connection

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hash_password(password)))
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

# Function to authenticate a user
def authenticate(username, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT id FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hash_password(password)))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return result[0]  # Return user ID
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to handle the main page
def main_page():
    st.title("Main Page")
    st.write("Welcome to the main page!")
    if st.button("Logout"):
        delete_user_id()
        st.session_state.page = "login"
        st.experimental_rerun()

    if st.button("Sleep Optimization"):
        st.session_state.page = "sleep"
        st.experimental_rerun()

# Function to handle the sleep optimization page
def sleep_optimization_page():
    st.title("Sleep Optimization Page")
    st.write("Welcome to the sleep optimization page!")
    if st.button("Go to Main Page"):
        st.session_state.page = "main"
        st.experimental_rerun()

# Function to extract the value of the 'page' query parameter
def get_page_query_param():
    return st.session_state.get('page', 'login')

# Main logic to switch between pages based on query parameter
if 'page' not in st.session_state:
    st.session_state.page = 'login'

page = get_page_query_param()

user_id = load_user_id()

if user_id:
    if page == "main":
        main_page()
    elif page == "sleep":
        sleep_optimization_page()
    else:
        st.session_state.page = "main"
        st.experimental_rerun()
else:
    # Create login and register tabs
    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user_id = authenticate(login_username, login_password)
            if user_id:
                save_user_id(user_id)
                st.success("Login successful!")
                st.session_state.page = "main"
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    with tabs[1]:
        st.header("Register")
        register_username = st.text_input("Username", key="register_username")
        register_password = st.text_input("Password", type="password", key="register_password")
        register_password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")
        if st.button("Register"):
            if register_password != register_password_confirm:
                st.error("Passwords do not match")
            elif register_user(register_username, register_password):
                st.success("Registration successful!")
            else:
                st.error("Username already exists")
