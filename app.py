from flask import Flask, jsonify
from camCapture import capture_image_and_generate_random  # Import logic from capture.py

app = Flask(__name__)
app.debug = False

# Flask route for the API endpoint
@app.route('/', methods=['GET'])
def generate_random():
    with app.app_context():
        # Execute image capture and hash generation
        random_hash, error = capture_image_and_generate_random()
        if error:
            return jsonify({"error": error}), 500  # Return error if something goes wrong

        # Return the generated hash value in JSON format
        return jsonify({"random_hash": random_hash})

# Start the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
