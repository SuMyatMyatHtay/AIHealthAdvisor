from PIL import Image, ImageOps
import tensorflow as tf
import cv2
import numpy as np
import os
import sys
from time import sleep

label = ''
frame = None

def import_and_predict(image_data, model):
    size = (75,75)
    image = ImageOps.fit(image_data, size, Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
    image = image.convert('RGB')
    image = np.asarray(image)
    image = (image.astype(np.float32) / 255.0)
    img_reshape = image[np.newaxis,...]
    prediction = model.predict(img_reshape)
    return prediction

model = tf.keras.models.load_model(r'C:\Python\ciot\my_model.hdf5')  # Use raw string to handle backslashes

cap = cv2.VideoCapture(0)  # Open the default camera

if cap.isOpened():
    print("Camera OK")
else:
    print("Failed to open camera")
    cap.open()

while True:
    ret, original = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    frame = cv2.resize(original, (224, 224))
    cv2.imwrite(filename='img.jpg', img=original)
    image = Image.open('img.jpg')

    # Get prediction
    prediction = import_and_predict(image, model)
    print(f"Raw prediction values: {prediction}")
    # Determine the label based on the prediction
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
    
    # Display the label on the frame
    cv2.putText(original, predict, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Classification", original)

    print(predict)
    sleep(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
frame = None
cv2.destroyAllWindows()
sys.exit()
