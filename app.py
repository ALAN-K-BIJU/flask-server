from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from werkzeug.utils import secure_filename  # Import secure_filename function
import torch
import urllib.request 
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
import os
import base64  # Import base64 module
from utils import classify_img, get_density_model, detection_img, get_pothole_model

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

classes = ['Empty', 'High', 'Low', 'Medium', 'Traffic Jam']
density_model = get_density_model()
density_model.eval()

pothole_classes = ['Background', 'Pothole']
pothole_model = get_pothole_model()
pothole_model.eval()

dirname = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(dirname, os.pardir)
upload_dir = os.path.join(root_dir, "uploads")

def process_density_image(file):
    img = Image.open(file)
    img = np.array(img)
    img = cv2.resize(img, (480, 480))
    label, probability = classify_img(density_model, img)
    return classes[label], probability

def process_pothole_image(file):
    img = Image.open(file)
    img = np.array(img)
    img = cv2.resize(img, (480, 480))
    detected_img = detection_img(pothole_model, img, pothole_classes, conf_threshold=0.5, iou_threshold=0.5)
    return detected_img

@app.route('/api/upload', methods=['POST'])
def upload_density_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)  # Use secure_filename function to secure the filename
        file.save(os.path.join(upload_dir, filename))

        # Process image for density classification
        label, probability = process_density_image(file)

        return jsonify({"traffic": label, "value": probability}), 200
    else:
        return jsonify({'error': 'Error processing image'}), 500

# @app.route('/api', methods=['POST'])
# def upload_pothole_image():
#     print("Request received for /api/anotherApi endpoint")
    
#     if 'file' not in request.files:
#         print("No file part in request")
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']

#     if file.filename == '':
#         print("No selected file")
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filename = secure_filename(file.filename)  # Use secure_filename function to secure the filename
#         print(f"Filename: {filename}")
#         file.save(os.path.join(upload_dir, filename))
#         print("File saved successfully")

#         # Process image for pothole detection
#         detected_img = process_pothole_image(file)

#         # Check if pothole is detected
#         if "Pothole" in detected_img:
#             print("Pothole detected")
#             return jsonify({'result': 'Yes its a pothole'}), 200
#         else:
#             print("No pothole detected")
#             return jsonify({'result': 'No pothole detected'}), 200
#     else:
#         print("Error processing image")
#         return jsonify({'error': 'Error processing image'}), 500
    

@app.route('/api/anotherApi', methods=['POST'])
def handle_another_api():
    if 'previousImageUrl' not in request.json:
        return jsonify({'error': 'No previousImageUrl provided'}), 400

    previous_image_url = request.json['previousImageUrl']

    # Process the image using your model
    #processed_image_url = process_image(previous_image_url)

    # Return the processed image URL
    return jsonify({"resultImageUrl":"Pothole Detected !!"})




if __name__ == '__main__':
    app.run(debug=True)
