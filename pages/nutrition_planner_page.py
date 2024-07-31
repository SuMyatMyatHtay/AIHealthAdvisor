import streamlit as st
import mysql.connector
from mysql.connector import Error
import random
from datetime import date

# Function to create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",  # Replace with your MySQL password
            database="iot"
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
        SELECT id, name, calories, carbs, protein, fat
        FROM foods
        WHERE meal_type = %s AND calories <= %s''', (meal_type, target_calories))
        meals = cursor.fetchall()
        conn.close()
        return meals

def select_meal(meal_options, target_calories):
    # Shuffle meals to introduce variability
    random.shuffle(meal_options)
    selected_meals = []
    current_calories = 0

    for meal in meal_options:
        meal_calories = meal[2]
        if current_calories + meal_calories <= target_calories:
            selected_meals.append(meal)
            current_calories += meal_calories
            if current_calories >= target_calories:
                break

    return selected_meals

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
    return daily_meal_plan, breakfast_calories, lunch_calories, dinner_calories, snack_calories

# Nutrition Planner Page Function
def nutrition_planner_page():
    st.title("Nutrition Planner")
    st.markdown("### Today's Meal Plan")

    user_data = get_user_details()
    if user_data:
        weight = user_data[4]
        height = user_data[5]
        age = user_data[2]
        gender = user_data[3]

        # Check if a meal plan for today exists in session_state
        today = date.today().strftime("%Y-%m-%d")
        if "meal_plan_date" not in st.session_state or st.session_state.meal_plan_date != today:
            user_bmr = calculate_bmr(gender, weight, height, age)
            daily_plan, breakfast_calories, lunch_calories, dinner_calories, snack_calories = generate_daily_meal_plan(user_bmr)
            st.session_state.meal_plan = daily_plan
            st.session_state.meal_plan_date = today
        else:
            daily_plan = st.session_state.meal_plan

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
                    display: inline-block;
                    vertical-align: top;
                ">
                    <h4 style="margin-top: 0;">{title}</h4>
                    {"".join([
                        f"<div style='margin-bottom: 10px;'><p style='margin: 0;'><strong>{meal[1]}</strong></p><p style='margin: 0;'><em>{meal[2]} kcal</em></p></div>"
                        for meal in meals
                    ])}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Create card layout
        col1, col2 = st.columns(2)

        with col1:
            create_card('Breakfast', daily_plan['breakfast'], '#FFDDC1')

        with col2:
            create_card('Lunch', daily_plan['lunch'], '#D1E2FF')
        
        col3, col4 = st.columns(2)
        
        with col3:
            create_card('Dinner', daily_plan['dinner'], '#D2F6E0')

        with col4:
            create_card('Snacks', daily_plan['snack'], '#F3F3F3')

    else:
        st.write("User not found or error retrieving data.")
