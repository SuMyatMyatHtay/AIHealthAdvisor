import streamlit as st
import mysql.connector
from mysql.connector import Error
import json
import os
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
        
        if user_details:
            return (user_details[0], float(user_details[1]), user_details[2], float(user_details[3]), float(user_details[4]))
        else:
            return None

# Function to calculate BMR
def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

# Function to distribute calories among meals
def distribute_calories(bmr):
    breakfast = bmr * 0.25
    lunch = bmr * 0.30
    dinner = bmr * 0.30
    snacks = bmr * 0.15
    return breakfast, lunch, dinner, snacks

# Function to retrieve meals from the database
def get_meals(meal_type, target_calories):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
            id,
            name,    
            calories,    
            ingredients,
            recipes
        FROM meals
        WHERE meal_type = %s
        ORDER BY ABS(calories - %s) ASC
        LIMIT 1;''', (meal_type, target_calories))
        meals = cursor.fetchall()
        conn.close()
        return meals

# Function to store meal plan in the database
def store_meal_plan(meal_plan):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        today = date.today().strftime("%Y-%m-%d")
        for meal_type, meals in meal_plan.items():
            if meals:  # Check if there are meals for the type
                # Extract details from the meal tuple
                for meal in meals:
                    meal_id, meal_name, calories, ingredients, recipes = meal
                    cursor.execute('''
                    INSERT INTO meal_plan (meal_name, meal_type, date, calories, ingredients, recipes) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (meal_name, meal_type, today, calories, ingredients, recipes))
        conn.commit()
        conn.close()

# Function to retrieve meal plan for today from the database
def get_meal_plan_for_today():
    conn = create_connection()
    if conn:
        today = date.today().strftime("%Y-%m-%d")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT meal_name, meal_type, calories, ingredients, recipes 
        FROM meal_plan 
        WHERE date = %s
        ''', (today,))
        meal_plan_data = cursor.fetchall()
        conn.close()
        # Organize meals by type
        meal_plan = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snack': []
        }
        for meal_name, meal_type, calories, ingredients, recipes in meal_plan_data:
            meal_plan[meal_type].append((None, meal_name, calories, ingredients, recipes))  # None for id, as it's not used here
        return meal_plan
    return None

# Function to generate a daily meal plan
def generate_daily_meal_plan(bmr):
    breakfast_calories, lunch_calories, dinner_calories, snack_calories = distribute_calories(bmr)
    breakfast_options = get_meals('breakfast', breakfast_calories)
    lunch_options = get_meals('lunch', lunch_calories)
    dinner_options = get_meals('dinner', dinner_calories)
    snack_options = get_meals('snack', snack_calories)
    
    daily_meal_plan = {
        'breakfast': select_meal(breakfast_options, breakfast_calories),
        'lunch': select_meal(lunch_options, lunch_calories),
        'dinner': select_meal(dinner_options, dinner_calories),
        'snack': select_meal(snack_options, snack_calories)
    }
    return daily_meal_plan

def select_meal(meal_options, target_calories):
    # Select the closest meal option to the target calories
    return meal_options

def nutrition_planner_page():
    if not os.path.exists(temp_data_path):
        st.error("User not logged in. Redirect to the first app page for login.")
        return
    st.title("Nutrition Planner")
    st.markdown("### Today's Meal Plan")

    user_id = load_user_id()
    user_data = get_user_details(user_id)
    if user_data:
        weight = user_data[4]
        height = user_data[3]
        age = user_data[1]
        gender = user_data[0]

        # Check if a meal plan for today exists in the database
        meal_plan = get_meal_plan_for_today()
        
        if not meal_plan or all(not meals for meals in meal_plan.values()):
            user_bmr = calculate_bmr(gender, weight, height, age)
            daily_plan = generate_daily_meal_plan(user_bmr)
            store_meal_plan(daily_plan)
        else:
            daily_plan = meal_plan

        # Custom CSS for card layout using inline styles
        def create_card(title, meals, background_color):
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
                    height: 300px; /* Fixed height */
                    overflow: auto; /* Scroll if content overflows */
                    display: inline-block;
                    vertical-align: top;
                ">
                    <h4 style="margin-top: 0;">{title}</h4>
                    {"".join([
                        f"<div style='margin-bottom: 10px;'><p style='margin: 0;'><strong>{meal[1]}</strong></p><p style='margin: 0;'><em>{meal[2]} kcal</em></p><p style='margin: 0;'><strong>Ingredients:</strong> {meal[3]}</p><p style='margin: 0;'><strong>Recipe:</strong> {meal[4]}</p></div>"
                        for meal in meals
                    ])}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Create card layout
        col1, col2 = st.columns(2)

        with col1:
            create_card('Breakfast', daily_plan['breakfast'], '#a83263')  

        with col2:
            create_card('Lunch', daily_plan['lunch'], '#8732a8')  
        
        col3, col4 = st.columns(2)
        
        with col3:
            create_card('Dinner', daily_plan['dinner'], '#a86132')  

        with col4:
            create_card('Snacks', daily_plan['snack'], '#32a86d') 

    else:
        st.write("User not found or error retrieving data.")
