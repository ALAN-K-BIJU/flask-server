from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
import os
import utils
from utils import classify_img, get_density_model

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

classes = ['Empty', 'High', 'Low', 'Medium', 'Traffic Jam']
model = get_density_model()
model.eval()

dirname = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(dirname, os.pardir)
density_img_dir = os.path.join(root_dir, "images", "density_img")


def process_image(file):
    img = Image.open(file)
    img = np.array(img)
    img = cv2.resize(img, (480, 480))
    label, probability = classify_img(model, img)
    return classes[label], probability


@app.route('/upload', methods=['POST'])
def upload_files():
    lane_urls = {}
    response_data = []

    for key, file in request.files.items():
        file.save(f"uploads/{file.filename}")
        label, probability = process_image(file)
        response_data.append({"traffic": label, "value": probability})

    for key, value in request.form.items():
        if key.startswith('lane'):
            lane_number = int(key[4:])
            lane_urls[f"lane{lane_number}"] = value

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
