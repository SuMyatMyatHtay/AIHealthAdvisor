import streamlit as st
import mysql.connector
import os

from mysql.connector import Error

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(parent_directory, 'tempData.json')

def delete_user_id():
    if os.path.exists(temp_data_path):
        os.remove(temp_data_path)


# Home Page Function
def home_page():
    st.title("Home Page")
    st.write("Welcome to the main page!")
    if st.button("Logout"):
        delete_user_id()
        # st.session_state.page = "login"
        st.rerun()
