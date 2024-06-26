from tensorflow.keras.models import load_model  #type:ignore
from PIL import Image
import numpy as np
import os

# Load the v2_model
model_path = './model/final_model_v3.h5'
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

v2_model = load_model(model_path)

# Analyzing the emotion
class Analyze:
    def __init__(self):
        pass
        
    def analyze_emotion(self, image_path):
        img_array = self.preprocess_image(image_path)
        v2_prediction = v2_model.predict(img_array)
        
        emotions = ['Happy', 'Sad', 'Neutral']
        predicted_emotion = emotions[np.argmax(v2_prediction)]
        return predicted_emotion
    
    def preprocess_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((48, 48))
        img = img.convert('L')  # Convert the image to grayscale
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
        return img_array
