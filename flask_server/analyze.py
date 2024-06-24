from tensorflow.keras.models import load_model # type: ignore
from PIL import Image
import numpy as np
import os

# Load the v2_model
v2_model = load_model('final_model_v3.h5')
v2_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Analyzing the emotion
class Analyze:
    def __init__(self,image_path):
        self.image_path = image_path
        

    def analyze_emotion(self):
        img_array = self.preprocess_image(self.image_path)
        v2_prediction = v2_model.predict(img_array)

        # Assuming the model returns class probabilities, you can map them to human-readable emotions
        emotions = ['Happy', 'Sad', 'Neutral']
        predicted_emotion = emotions[np.argmax(v2_prediction)]
        print(predicted_emotion)
        return predicted_emotion
    def preprocess_image(image_path):
        img = Image.open(image_path)
        img = img.resize((48, 48))
        img = img.convert('L')  # Convert the image to grayscale
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
        return img_array



