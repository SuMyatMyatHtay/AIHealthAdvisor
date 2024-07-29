# How to run the streamlit for now

streamlit run streamlit.py

# How to run both streamlit and camera

python runscript.py

# How to set up (Su's Part)

- run "python mysql_createdb.py"
- inside the mysql, run the file which is under the "MySQL Database" folder
- run "python ciot_app_model.py" file

# What will be in next release

- I will make the python file to install all the data and all the necessary thingys in one shot.
- I will combine setup part in one shot (Sorry I lazy to do rn)
- One main file to handle the database connection rather than putting details in everything.

# The Database Info that we will be using

host="localhost",
user="root",
password="",
database="iot"

# Filenames

- ciot_app_model => In Use (To train the AI)
- ciot_detect => Not in Use (currently using faceDetect.py)
- faceDetect => In Use (To detect the face in camera)
- mysql_createdb.py => In Use (To create the things in advance before starting anything)
- mysqlcheck => To Test (To test our database connection)
- runscript => To Test (To run two files at the same time)
- app.py => In Use (The streamlit app)
- suTest.py => To Test
- tempData.json => System Create File (To store temp data. For example, the login id)
- pages folder => different pages streamlit files
- datasets folder => pictures to train the model for the face recognition
- Node-RED => exported Node Red flow.

# Bugs Left to Fix

- Login button needs to click twice to login
- Face Upload Page needs to click twice to disable (but do not crash the server)
- Wake Up button needs to click thrice to disable (but do not crash the server)

# Minor Flag Outs

- This version haven't tested out yet for the Node-RED so please ignore the Node-RED folder for now.
