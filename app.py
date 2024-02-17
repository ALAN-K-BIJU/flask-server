from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_files():
    lane_urls = {}

    for key, file in request.files.items():
        file.save(f"uploads/{file.filename}")

    for key, value in request.form.items():
        
        if key.startswith('lane'):
            lane_number = int(key[4:])
            lane_urls[f"lane{lane_number}"] = value

    response_data = [
        {"traffic": "LOW", "value": 0.876},
        {"traffic": "EMPTY", "value": 0.876},
        {"traffic": "MEDIUM", "value": 0.876},
        {"traffic": "JAM", "value": 0.876},
        {"traffic": "HIGH", "value": 0.208}
    ]

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
