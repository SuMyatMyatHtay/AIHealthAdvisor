import streamlit as st
import mysql.connector
from mysql.connector import Error

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

# Connect to MySQL database
def get_exercises():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
        cursor.execute("SELECT exercise_name, exercise_description, photo_url FROM exercises")
        exercises = cursor.fetchall()
        cursor.close()
        conn.close()  # Fixed variable name
        return exercises
    return []

# Streamlit app
def exercises_page():
    st.title("Exercises")
    
    exercises = get_exercises()
    
    for exercise in exercises:
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin-bottom: 20px; 
                    box-shadow: 0px 0px 15px rgba(0,0,0,0.2); 
                    display: flex; 
                    align-items: flex-start;
                    max-width: 1500px; 
                    width: 110%;
                ">
                    <div style="flex: 1; padding-right: 15px;">
                        <img src="{exercise['photo_url']}" style="width: 100%; border-radius: 10px;" />
                    </div>
                    <div style="flex: 2;">
                        <h3 style="margin-top: 0; font-size: 1.5em;">{exercise['exercise_name']}</h3>
                        <p style="font-size: 1.1em;">{exercise['exercise_description']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    exercises_page()
