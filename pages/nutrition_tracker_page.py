import streamlit as st
import mysql.connector as mysql
from datetime import date

# Function to create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="iot_ca2"
        )
        if conn.is_connected():
            return conn
    except mysql.Error as e:
        st.write(f"Error: {e}")
        return None

# Function to retrieve user details (including target BMR)
def get_user_details(user_id=2):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT bmr
        FROM users
        WHERE id = %s
        ''', (user_id,))
        user_details = cursor.fetchone()
        conn.close()
        return user_details
    return None

# Function to calculate total calorie intake for the current day
def get_total_calories():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(calories)
        FROM userMeals
        WHERE date = %s
        ''', (date.today(),))
        total_calories = cursor.fetchone()[0]
        conn.close()
        return total_calories if total_calories is not None else 0
    return 0

# Function to save meal data to the database
def save_meal(name, meal_type, calories):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO userMeals (name, meal_type, calories, date)
            VALUES (%s, %s, %s, %s)
        ''', (name, meal_type, calories, date.today()))
        conn.commit()
        conn.close()

# Function to retrieve foods from the database
def get_foods(meal_type):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT name, calories
        FROM foods
        WHERE meal_type = %s
        ''', (meal_type,))
        foods = cursor.fetchall()
        conn.close()
        return foods
    return []

# Function to retrieve user meals from the database
def get_user_meals(meal_type):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT name, calories
        FROM userMeals
        WHERE meal_type = %s AND date = %s
        ''', (meal_type, date.today()))
        meals = cursor.fetchall()
        conn.close()
        return meals
    return []

# Function to display the meal input form in an expander
def show_expander(meal_type):
    with st.expander(f"Add {meal_type.capitalize()} Meal", expanded=False):
        # Add new meal form
        meal_name = st.text_input(f"{meal_type.capitalize()} Meal Name", key=f"{meal_type}_name")
        calories = st.number_input("Calories", min_value=0, format="%f", key=f"{meal_type}_calories")
        if st.button(f"Add {meal_type.capitalize()} Meal", key=f"add_{meal_type}"):
            if meal_name and calories:
                save_meal(meal_name, meal_type, calories)
                st.success(f"{meal_type.capitalize()} meal added successfully!")
                st.experimental_rerun()  # Refresh the page to show the new meal
            else:
                st.error("Please provide both meal name and calories.")

# Nutrition Tracker Page Function
def nutrition_tracker_page():
    st.title("Nutrition Tracker")
    
    # Add CSS for styling
    st.markdown(
        """
        <style>
        .target-bmr-card {
            border: 1px solid #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: #DFF0D8;
        }
        .bmr-card {
            border: 1px solid #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: #D9EDF7;
        }
        .bmr-text {
            font-size: 26px;
            font-weight: bold;
            
        }
        .bmr-value {
            font-size: 22px;
            font-weight: bold;
            color: #333;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }
        .stExpander > div {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 16px;
        }
        .stMarkdown > div {
            background-color: #f8f9fa;
        }
        .meal-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #ffffff;
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

    # Get user details (including target BMR)
    user_details = get_user_details()
    if user_details:
        target_bmr = user_details[0]
        st.markdown(
            f"""
            <div class="target-bmr-card">
                <div class="bmr-text">Target BMR : {target_bmr} kcal/day</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Calculate total calorie intake
    total_calories = get_total_calories()
    
    st.markdown(
        f"""
        <div class="bmr-card">
            <div class="bmr-text">Current Total Caloric Intake : {total_calories} kcal</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Add Your Meals")

    # Show sections for each meal type with expanders closed by default
    meal_types = ["breakfast", "lunch", "dinner"]
    for meal_type in meal_types:
        st.markdown(f"#### {meal_type.capitalize()} Meals")
        # Display existing meals in card format
        meals = get_user_meals(meal_type)
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

if __name__ == "__main__":
    nutrition_tracker_page()
