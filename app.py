from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from werkzeug.utils import secure_filename
import torch
import urllib.request 
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
import os
import base64
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

def process_density_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (480, 480))
    label, probability = classify_img(density_model, img)
    return classes[label], probability

def process_pothole_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (480, 480))
    detected_img = detection_img(pothole_model, img, pothole_classes, conf_threshold=0.5, iou_threshold=0.5)
    return detected_img


@app.route('/api/lights', methods=['POST'])
def upload_density_images():
    if 'urls' not in request.json:
        return jsonify({'error': 'No URLs provided'}), 400

    urls = request.json['urls']

    results = []
    for url in urls:
        try:
            img_data = urllib.request.urlopen(url).read()
            img_filename = os.path.join(upload_dir, "cloudinary_img.jpg")
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
            
            label, probability = process_density_image(img_filename)
            results.append({"url": url, "traffic": label, "value": probability})
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
