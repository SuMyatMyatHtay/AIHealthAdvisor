import subprocess

# Paths to your scripts
streamlit_script = "C:\python\CIOT\streamlit.py"
facedetect_script = "C:\python\ciot/faceDetect.py"

# Run Streamlit script
streamlit_process = subprocess.Popen(["streamlit", "run", streamlit_script])

# Run test script
# test_process = subprocess.Popen(["python", facedetect_script])

# Wait for both processes to complete
streamlit_process.wait()
# test_process.wait()
