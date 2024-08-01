import streamlit as st
import pandas as pd
import mysql.connector
import json
import os
import hashlib
import re

from mysql.connector import Error
from time import sleep

# Home Page Function
def login_page():
    st.title("Login Page")
    rundata()
    
# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(parent_directory, 'tempData.json')


# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_id(user_id, username):
    jsontempData = {
        "user_id": user_id,
        "username" : username

    }
    with open(temp_data_path, 'w') as f:
        json.dump(jsontempData, f)

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
    
def is_password_strong(password):
    """Check if the password is strong."""
    if (re.search(r'[a-zA-Z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False


def rundata(): 
    tabs = st.tabs(["Login", "Register"])
    with tabs[0]:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user_id = authenticate(login_username, login_password)
            if user_id:
                save_user_id(user_id, login_username)
                st.success("Login successful!")
                # st.session_state.page = "main"
                st.rerun()
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
            elif len(register_password) < 6:
                st.error("Password must be at least 6 characters long")
            elif not is_password_strong(register_password):
                st.error("Password must contain at least one letter, one number, and one special character")
        
            elif register_user(register_username, register_password):
                st.success("Registration successful!")
                sleep(3)
                # st.session_state.selected_tab = "Login"
                st.rerun() 
                
            else:
                st.error("Username already exists")

