import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  # Replace with your MySQL password
            database="iot_ca2"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.write(f"Error: {e}")
        return None

def get_user_details():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE id = 2;''')
        user_details = cursor.fetchone()  # Fetch one row
        conn.close()
        return user_details

# Function to calculate BMR
def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

# User Page Function
def user_page():
    st.title("User Page")
    user_data = get_user_details()

    if user_data:
        # Custom CSS to style the table
        st.markdown(
            """
            <style>
            .user-table {
                width: 100%;
                border-collapse: collapse;
                background-color: #f9f9f9; /* Table background color */
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            .user-table th, .user-table td {
                padding: 15px;
                text-align: left;
                border: none; /* Remove borders */
                font-size: 20px; /* Increase font size */
            }
            .user-table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            .user-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .user-table tr:nth-child(odd) {
                background-color: #ffffff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create the table with a background
        st.markdown(
            f"""
            <table class="user-table">
                <tr>
                    <td><strong>Name</strong></td>
                    <td>{user_data[1]}</td>
                </tr>
                <tr>
                    <td><strong>Age</strong></td>
                    <td>{user_data[2]}</td>
                </tr>
                <tr>
                    <td><strong>Gender</strong></td>
                    <td>{user_data[3]}</td>
                </tr>
                <tr>
                    <td><strong>Weight:</strong></td>
                    <td>{user_data[4]}</td>
                </tr>
                <tr>
                    <td><strong>Height</strong></td>
                    <td>{user_data[5]}</td>
                </tr>
                <tr>
                    <td><strong>BMR</strong></td>
                    <td>{int(calculate_bmr(user_data[3], user_data[4], user_data[5], user_data[2]))}</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("User not found or error retrieving data.")
