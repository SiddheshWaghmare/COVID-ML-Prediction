from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model('models/covid_detection_model.h5')

# Define the image dimensions expected by the model
img_width, img_height = 150, 150

# Define the class labels
class_labels = {0: 'Covid-19', 1: 'Normal', 2: 'Viral Pneumonia'}

def preprocess_image(image):
    image = image.resize((img_width, img_height))
    image = image.convert('RGB')
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/')
def index():
    return render_template('index.html', prediction_result=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        image = Image.open(file)
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction)
        predicted_label = class_labels[predicted_class]
        return render_template('index.html', prediction_result=predicted_label)

if __name__ == '__main__':
    app.run(debug=True,port=121)
