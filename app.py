import streamlit as st
import os

import pages.login_page as login
import pages.home_page as home
import pages.sleep_page as sleep
import pages.nutrition_planner_page as nutrition_planner
import pages.nutrition_tracker_page as nutrition_tracker
import pages.user_page as user_planner
import pages.statistics_page as statistics
import pages.exercises_page as exercises

#st.set_page_config(layout="wide")

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current directory
parent_directory = os.path.dirname(current_directory)
# Set temp_data_path to the parent directory, with the file name tempData.json
temp_data_path = os.path.join(current_directory, 'tempData.json')

if os.path.exists(temp_data_path):
    # Hide the default Streamlit sidebar elements
    hide_streamlit_style = """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stSidebarNavItems"] { display: none; }
        [data-testid="stSidebarNavSeparator"] { display: none; }
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Navigation
    def main():
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Sleep Optimization", "Nutrition Planner","Nutrition Tracker", "User Page", "Statistics Page", "Exercises Page"])

        
        if page == "Home":
            home.home_page()
        elif page == "Sleep Optimization": 
            print("Sleep Page")
            sleep.sleep_page()
        elif page == "Nutrition Planner":
            print("Nutrition Planner Page")
            nutrition_planner.nutrition_planner_page()
        elif page == "Nutrition Tracker":
            print("Nutrition Tracker Page")
            nutrition_tracker.nutrition_tracker_page()
        elif page == "User Page":
            print("User Page")
            user_planner.user_page()
        elif page == "Statistics Page":
            print("Statistics Page")
            statistics.statistics()
        elif page == "Exercises Page":
            print("Exercises Page")
            exercises.exercises_page()
        

    if __name__ == "__main__":
        main()
else:
    login.login_page()