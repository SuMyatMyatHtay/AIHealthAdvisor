from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import os

def image_gen_w_aug(train_parent_directory, test_parent_directory):
    train_datagen = ImageDataGenerator(
        rescale=1/255,
        rotation_range=30,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        validation_split=0.15
    )
    
    test_datagen = ImageDataGenerator(rescale=1/255)
    
    train_generator = train_datagen.flow_from_directory(
        train_parent_directory,
        target_size=(75, 75),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = train_datagen.flow_from_directory(
        train_parent_directory,
        target_size=(75, 75),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    
    test_generator = test_datagen.flow_from_directory(
        test_parent_directory,
        target_size=(75, 75),
        batch_size=32,
        class_mode='categorical'
    )
    
    return train_generator, val_generator, test_generator

def model_output_for_TL(pre_trained_model, last_output, num_classes):
    x = Flatten()(last_output)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(num_classes, activation='softmax')(x)
    
    model = Model(pre_trained_model.input, x)
    
    return model

train_dir = os.path.join('datasets/train/')
test_dir = os.path.join('datasets/test/')


train_generator, validation_generator, test_generator = image_gen_w_aug(train_dir, test_dir)

# Count the number of folders in the test directory to determine the number of classes
num_classes = len(next(os.walk(test_dir))[1])

pre_trained_model = InceptionV3(input_shape=(75, 75, 3), include_top=False, weights='imagenet')

for layer in pre_trained_model.layers:
    layer.trainable = False

last_layer = pre_trained_model.get_layer('mixed7')
last_output = last_layer.output

model_TL = model_output_for_TL(pre_trained_model, last_output, num_classes)
model_TL.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_TL = model_TL.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=100,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

tf.keras.models.save_model(model_TL, 'my_model.hdf5')
