import signal
import sys
from PIL import Image, ImageOps
import tensorflow as tf
import cv2
import numpy as np
import os

# Variable to control the loop
running = True

def signal_handler(sig, frame):
    global running
    print('Signal received, stopping...')
    running = False

# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

label = ''
frame = None

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
temp_data_path = os.path.join(current_directory, 'my_model.hdf5')

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

# Initialize previous prediction variable
previous_predict = None

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

        if np.argmax(prediction) == 0:
            predict = "Andy"
        elif np.argmax(prediction) == 1:
            predict = "Ei"
        elif np.argmax(prediction) == 2:
            predict = "Joe"
        elif np.argmax(prediction) == 3:
            predict = "Su"
        else:
            predict = "Unknown"

    if predict != previous_predict:
        print(f"{predict}")
        previous_predict = predict

    cv2.putText(original, predict, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Classification", original)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
frame = None
cv2.destroyAllWindows()
sys.exit()
