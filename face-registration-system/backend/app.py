from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import face_recognition
import base64
import pymongo
import io

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['faces']
users = db["users"]

def encode_images(img_data):
    """Decode base64 image and return face encoding."""
    try:
        img_bytes = io.BytesIO(img_data)  # Convert binary to a file-like object
        img = face_recognition.load_image_file(img_bytes)
        encodings = face_recognition.face_encodings(img)
        return encodings[0] if encodings else None
    except Exception as e:
        print("Encoding error:", str(e))
        return None

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # Corrected from request.json()
    username = data.get('username')
    img_data = base64.b64decode(data.get('image'))  # Decode base64 image

    encodings = encode_images(img_data)
    if encodings is None:
        return jsonify({"error": "No Face Detected"}), 400

    users.insert_one({"username": username, "encodings": encodings.tolist()})  # Convert to list for MongoDB
    return jsonify({"message": "User Registered Successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    img_data = base64.b64decode(data.get('image'))

    encodings = encode_images(img_data)
    if encodings is None:
        return jsonify({"error": "No Face Detected"}), 400

    for user in users.find():
        stored = np.array(user['encodings'])  # Corrected field name
        result = face_recognition.compare_faces([stored], encodings)

        if result[0]:  # If face matches
            return jsonify({"message": f"{user['username']} logged in successfully"})

    return jsonify({"error": "Face Not Recognized"}), 401

if __name__ == "__main__":
    app.run(debug=True)
