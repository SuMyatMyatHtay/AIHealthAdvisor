import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
import json
from datetime import datetime
from datetime import date

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

def get_user_details(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT gender, age, birthdate, height, weight FROM userinfo WHERE user_id = %s;''', (user_id,))
        user_details = cursor.fetchone()  
        conn.close()
        
        # Convert to appropriate types
        if user_details:
            return (user_details[0], float(user_details[1]), user_details[2], float(user_details[3]), float(user_details[4]))
        else:
            return None

def get_user_name(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username FROM users WHERE id = %s;''', (user_id,))
        user_name = cursor.fetchone() 
        conn.close()
        return user_name[0] if user_name else None

def update_user_details(user_id, name, age, gender, weight, height, birthdate):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # Update the user name in the users table
        cursor.execute('''UPDATE users SET username = %s WHERE id = %s;''', (name, user_id))
        # Update other details in the userinfo table
        cursor.execute('''UPDATE userinfo SET age = %s, gender = %s, weight = %s, height = %s, birthdate = %s WHERE id = %s;''',
                       (age, gender, weight, height, birthdate, user_id))
        conn.commit()
        cursor.close()
        conn.close()

def calculate_age(birthdate):
    today = datetime.today()
    birth_date = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Function to calculate BMR
def calculate_bmr(gender, weight, height, age):
    
    weight = float(weight)
    height = float(height)
    age = float(age)
    
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return bmr


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
        

# User Page Function
def user_page():
    
    st.markdown("""
    <style>
        .title {
            text-align: center;
        }
        .edit-button {
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .edit-button:hover {
            background-color: #0056b3; /* Darker shade on hover */
        }
        .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Center the title
    st.markdown('<h1 class="title">User Page</h1>', unsafe_allow_html=True)

    user_id = load_user_id()

    # Initialize session state for edit mode if not already present
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if user_id:
        user_data = get_user_details(user_id)
        user_name = get_user_name(user_id)
        sleep_goal, wake_ups, net_sleep_hours = get_sleep_data(user_id)

        if user_data and user_name:
            # Edit mode logic
            if st.session_state.edit_mode:
                st.text_input("Name", user_name, key='name')
                st.date_input("Birthdate", value=datetime.strptime(user_data[2], '%Y-%m-%d'), key='birthdate')
                st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(user_data[0]), key='gender')
                st.number_input("Weight (kg)", value=float(user_data[4]), key='weight')
                st.number_input("Height (cm)", value=float(user_data[3]), key='height')

                # Buttons to save changes or cancel editing
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Save Changes"):
                        name = st.session_state.name
                        birthdate = st.session_state.birthdate
                        gender = st.session_state.gender
                        weight = st.session_state.weight
                        height = st.session_state.height

                        # Calculate age from birthdate
                        age = calculate_age(birthdate.strftime('%Y-%m-%d'))

                        update_user_details(user_id, name, age, gender, weight, height, birthdate.strftime('%Y-%m-%d'))
                        st.success("Details updated successfully")
                        st.session_state.edit_mode = False
                        st.rerun()

                with col2:
                    if st.button("Cancel"):
                        st.session_state.edit_mode = False
                        st.rerun()

            else:
                showSleepHour = ""
                if wake_ups is None: 
                    wake_ups = 0 
                if net_sleep_hours is None: 
                    net_sleep_hours = 0 
                if(net_sleep_hours < 60): 
                    showSleepHour = str(net_sleep_hours) + " minutes"
                else: 
                    showSleepHour = str(net_sleep_hours/60) + " hours"
                
                st.markdown(
                    """
                    <style>
                    .user-table {
                        width: 100%;
                        border-collapse: collapse;      
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                        margin-bottom: 20px; /* Space below the table */
                        
                    }
                    .user-table th, .user-table td {
                        padding: 15px;
                        text-align: left;
                        border: none; /* Remove borders */
                        font-size: 20px; /* Increase font size */
                       
                    }
                    .user-table th {
                        font-weight: bold;
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
                            <td>{user_name}</td>
                        </tr>
                        <tr>
                            <td><strong>Age</strong></td>
                            <td>{user_data[1]}</td>
                        </tr>
                        <tr>
                            <td><strong>Gender</strong></td>
                            <td>{user_data[0]}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{user_data[4]}</td>
                        </tr>
                        <tr>
                            <td><strong>Height</strong></td>
                            <td>{user_data[3]}</td>
                        </tr>
                        <tr>
                            <td><strong>BMR</strong></td>
                            <td>{int(calculate_bmr(user_data[0], user_data[4], user_data[3], user_data[1]))}</td>
                        </tr>
                        <tr>
                            <td><strong>Sleep Goal (hours)</strong></td>
                            <td>{sleep_goal}</td>
                        </tr>
                        
                    </table>
                    """,
                    unsafe_allow_html=True
                )
                # "wake_ups" for wake up time, "showSleepHour" for net Sleep Hours minute and hours dynamic
                
                if st.button("Edit", key="edit-button"):
                    st.session_state.edit_mode = True
                    st.rerun()

        else:
            st.write("User not found or error retrieving data.")
    else:
        st.write("No user logged in.")


