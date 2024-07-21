import os
import subprocess

current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"current_directory values: {current_directory}")
# Paths to your scripts
streamlit_script = current_directory + "/streamlit.py"
facedetect_script = current_directory + "/faceDetect.py"

# Run Streamlit script
streamlit_process = subprocess.Popen(["streamlit", "run", streamlit_script])

# Run test script
# test_process = subprocess.Popen(["python", facedetect_script])

# Wait for both processes to complete
streamlit_process.wait()
# test_process.wait()
