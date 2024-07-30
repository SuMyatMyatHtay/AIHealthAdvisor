import signal
import sys
from PIL import Image, ImageOps
import tensorflow as tf
import cv2
import numpy as np
import os
import streamlit as st
import json
import time

# Variable to control the loop
running = True

# Initialize previous prediction variable
previous_predict = None
start_time = None 
record_break = 0 

def signal_handler(sig, frame):
    global running
    print('Signal received, stopping...')
    running = False

# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

label = ''
frame = None

def save_user_id(user_id, username):
    jsontempData = {
        "user_id": user_id,
        "username" : username

    }
    with open(temp_data_path, 'w') as f:
        json.dump(jsontempData, f)

def load_user_id():
    if os.path.exists(temp_data_path):
        with open(temp_data_path, 'r') as f:
            data = json.load(f)
            return data
    return {}

def save_faceDetect_duration(record_break): 
    data = load_user_id()

    data['faceDetect_duration'] = record_break/60

    # Save updated data 
    with open(temp_data_path, 'w') as f: 
        json.dump(data, f, indent=4)


def import_and_predict(image_data, model):
    try:
        size = (75, 75)
        image = ImageOps.fit(image_data, size, Image.LANCZOS)
        image = image.convert('RGB')
        image = np.asarray(image)
        image = (image.astype(np.float32) / 255.0)
        img_reshape = image[np.newaxis, ...]
        prediction = model(img_reshape, training=False)
        return prediction.numpy()
    except Exception as e:
        return None

current_directory = os.path.dirname(os.path.abspath(__file__))
# temp_data_path = os.path.join(current_directory, 'my_model.hdf5')
temp_data_path = os.path.join(current_directory, 'tempData.json')
test_folder_path = os.path.join(current_directory, 'datasets/test')

# Get folder names dynamically
folder_names = sorted(os.listdir(test_folder_path))

try:
    with open(temp_data_path, 'r') as file:
        data = json.load(file)
        user_id = data.get('user_id')
        username = data.get('username')
except:
    st.error(f"File {temp_data_path} not found.")
    sys.exit(1)

try:
    model = tf.keras.models.load_model(r'C:\Python\AIHealthAdvisor\my_model.hdf5')
except Exception as e:
    sys.exit(1)

cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("Camera OK")
else:
    print("Failed to open camera")
    cap.open()

# Load the OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while running:
    ret, original = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        predict = "None"
    else:
        frame = cv2.resize(original, (224, 224))
        cv2.imwrite(filename='img.jpg', img=original)
        image = Image.open('img.jpg')

        prediction = import_and_predict(image, model)
        if prediction is None:
            print("Prediction failed")
            break

        # Map prediction to folder names
        predicted_index = np.argmax(prediction)
        if predicted_index < len(folder_names):
            predict = folder_names[predicted_index]
        else:
            predict = "IDK"

        # if np.argmax(prediction) == 0:
        #     predict = "Andy"
        # elif np.argmax(prediction) == 1:
        #     predict = "Ei"
        # elif np.argmax(prediction) == 2:
        #     predict = "Joe"
        # elif np.argmax(prediction) == 3:
        #     predict = "Su"
        # else:
        #     predict = "Unknown"

    if predict != previous_predict:
        # print(f"{predict}")
        if(predict == username): 
            print("Correct User Face")
            start_time = time.time() 

        else: 
            if(previous_predict == username): 
                elapsed_time = time.time() - start_time
                # print(f"Correct User was predicted for {elapsed_time} seconds")
                record_break += elapsed_time 
                print(f"{record_break} seconds")
                save_faceDetect_duration(record_break)

        previous_predict = predict

    cv2.putText(original, predict, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Classification", original)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
frame = None
cv2.destroyAllWindows()
sys.exit()
