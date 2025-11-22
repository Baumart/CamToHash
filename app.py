from flask import Flask, jsonify
from camCapture import capture_entropy_blob_sha3_512, capture_entropy_blob_shake_256_1024   # Import logic from capture.py

app = Flask(__name__)
app.debug = False

# Flask route for the API endpoint
@app.route('/sha3-512', methods=['GET'])
def generate_random_512():
    with app.app_context():
        # Execute image capture and hash generation
        random_hash, error = capture_entropy_blob_sha3_512()
        if error:
            return jsonify({"error": error}), 500  # Return error if something goes wrong

        # Return the generated hash value in JSON format
        return jsonify({"random_hash": random_hash})

@app.route('/', methods=['GET'])
def generate_random_1024():
    with app.app_context():
        # Execute image capture and hash generation
        random_hash, error = capture_entropy_blob_shake_256_1024()
        if error:
            return jsonify({"error": error}), 500  # Return error if something goes wrong

        # Return the generated hash value in JSON format
        return jsonify({"random_hash": random_hash})

# Start the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
