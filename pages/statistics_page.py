import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
import json
from datetime import date, timedelta
import pandas as pd
import decimal
import plotly.graph_objects as go

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

def get_calories_last_seven_days(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = '''
        SELECT date, COALESCE(SUM(calories), 0) as total_calories
        FROM userMeals
        WHERE user_id = %s AND date >= %s
        GROUP BY date
        ORDER BY date ASC
        '''
        start_date = date.today() - timedelta(days=6)
        cursor.execute(query, (user_id, start_date))
        result = cursor.fetchall()
        conn.close()

        # Fill missing days with zero calories
        date_calories_dict = {start_date + timedelta(days=i): 0 for i in range(7)}
        for row in result:
            date_calories_dict[row[0]] = row[1]

        # Prepare final result
        final_result = [(d.strftime('%Y-%m-%d'), c) for d, c in date_calories_dict.items()]
        return final_result
    return []

def get_user_details(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT gender, age, birthdate, height, weight FROM userinfo WHERE id = %s;''', (user_id,))
        user_details = cursor.fetchone()  
        conn.close()
        
        # Convert to appropriate types
        if user_details:
            return (user_details[0], float(user_details[1]), user_details[2], float(user_details[3]), float(user_details[4]))
        else:
            return None

def calculate_bmr(gender, weight, height, age):
    # Ensure weight, height, and age are float
    weight = float(weight)
    height = float(height)
    age = float(age)
    
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return bmr

def statistics():
    st.title("Caloric Intake Overview: Last 7 Days")
    user_id = load_user_id()
    
    if user_id:
        # Extract data
        result = get_calories_last_seven_days(user_id)
        
        # Convert Decimals to floats and handle date formatting
        dates = [x[0] for x in result]
        values = [float(x[1]) if isinstance(x[1], decimal.Decimal) else float(x[1]) for x in result]

        # Create DataFrame
        data = pd.DataFrame({
            'Date': pd.to_datetime(dates),
            'Value': values
        })

        # Get user details
        user_details = get_user_details(user_id)
        
        if user_details:
            gender, age, _, height, weight = user_details
            target_calories = calculate_bmr(gender, weight, height, age)
            
            # Create a list for the second line 
            second_line_values = [target_calories] * len(dates) 

            # Create DataFrame for the second line
            second_line_data = pd.DataFrame({
                'Date': pd.to_datetime(dates),
                'Value': second_line_values
            })

            # Create a line chart with Plotly
            fig = go.Figure()

            # Add first line trace
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Value'], mode='lines+markers', name='Caloric Intake'))

            # Add second line trace
            fig.add_trace(go.Scatter(x=second_line_data['Date'], y=second_line_data['Value'], mode='lines+markers', name='Target Calories'))

            # Update layout with custom width, height, and y-axis minimum value
            fig.update_layout(
                title='',
                xaxis_title='Date',
                yaxis_title='Calories',
                yaxis=dict(range=[0, None]),  
                width=800,  
                height=400  
            )

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig)

if __name__ == "__main__":
    statistics()
