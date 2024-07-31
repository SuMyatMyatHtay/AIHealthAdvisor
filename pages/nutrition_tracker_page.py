import streamlit as st
import mysql.connector as mysql
from mysql.connector import Error
import os
import json
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

def get_user_details(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT gender, age, birthdate, height, weight FROM userinfo WHERE user_id = %s;''', (user_id,))
        user_details = cursor.fetchone()  
        conn.close()
        
        if user_details:
            return (user_details[0], float(user_details[1]), user_details[2], float(user_details[3]), float(user_details[4]))
        else:
            return None

def calculate_bmr(gender, weight, height, age):
    weight = float(weight)
    height = float(height)
    age = float(age)
    
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return bmr

def get_total_calories(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(calories)
        FROM userMeals
        WHERE date = %s and user_id = %s 
        ''', (date.today(),user_id,))
        total_calories = cursor.fetchone()[0]
        conn.close()
        return total_calories if total_calories is not None else 0
    return 0

def save_meal(name, meal_type, calories, user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO userMeals (name, meal_type, calories, date, user_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, meal_type, calories, date.today(), user_id))
        conn.commit()
        conn.close()

def get_user_meals(meal_type, user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT name, calories
        FROM userMeals
        WHERE meal_type = %s AND date = %s AND user_id = %s
        ''', (meal_type, date.today(), user_id))
        meals = cursor.fetchall()
        conn.close()
        return meals
    return []

def show_expander(meal_type):
    user_id = load_user_id()
    with st.expander(f"Add {meal_type.capitalize()} Meal", expanded=False):
        meal_name = st.text_input(f"{meal_type.capitalize()} Meal Name", key=f"{meal_type}_name")
        calories = st.number_input("Calories", min_value=0, format="%f", key=f"{meal_type}_calories")
        if st.button(f"Add {meal_type.capitalize()} Meal", key=f"add_{meal_type}"):
            if meal_name and calories and user_id:
                save_meal(meal_name, meal_type, calories, user_id)
                st.success(f"{meal_type.capitalize()} meal added successfully!")
                st.rerun()
            else:
                st.error("Please provide both meal name and calories.")

def nutrition_tracker_page():
    st.title("Nutrition Tracker")
    user_id = load_user_id()
    if user_id:
        st.markdown(
            """
            <style>
            .target-bmr-card {
                border: 1px solid #ffffff;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .bmr-card {
                border: 1px solid #ffffff;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .bmr-text {
                font-size: 26px;
                font-weight: bold;
            }
            .bmr-value {
                font-size: 22px;
                font-weight: bold;
            }
            .stButton > button {
                font-weight: bold;
            }
            .stExpander > div {
                border-radius: 8px;
                padding: 16px;
            }
            .meal-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .meal-title {
                font-size: 20px;
                font-weight: bold;
                margin: 0;
            }
            .meal-calories {
                margin: 4px 0;
                font-size: 16px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        user_details = get_user_details(user_id)
        if user_details:
            target_bmr = calculate_bmr(user_details[0], user_details[4], user_details[3], user_details[1])
            st.markdown(
                f"""
                <div class="target-bmr-card">
                    <div class="bmr-text">Target BMR : {int(target_bmr)} kcal/day</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        total_calories = get_total_calories(user_id)
        
        st.markdown(
            f"""
            <div class="bmr-card">
                <div class="bmr-text">Current Total Caloric Intake : {total_calories} kcal</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### Add Your Meals")

        meal_types = ["breakfast", "lunch", "dinner","snack"]
        for meal_type in meal_types:
            st.markdown(f"#### {meal_type.capitalize()} Meals")
            meals = get_user_meals(meal_type, user_id)
            if meals:
                for meal in meals:
                    st.markdown(
                        f"""
                        <div class="meal-card">
                            <h4 class="meal-title">{meal[0]}</h4>
                            <p class="meal-calories"><strong>Calories:</strong> {meal[1]} kcal</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            show_expander(meal_type)
    else:
        st.error("No user ID found. Please ensure you are logged in.")

if __name__ == "__main__":
    nutrition_tracker_page()
