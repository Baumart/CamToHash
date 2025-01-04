from flask import Flask, jsonify
from camCapture import capture_image_and_generate_random  # Importiere die Logik aus capture.py

app = Flask(__name__)
app.debug = False

# Flask-Route für den API-Endpunkt
@app.route('/', methods=['GET'])
def generate_random():
    with app.app_context():
        # Führe die Bildaufnahme und Hash-Generierung aus
        random_hash, error = capture_image_and_generate_random()
        if error:
            return jsonify({"error": error}), 500  # Rückgabe eines Fehlers bei Problemen

        # Rückgabe des generierten Hash-Werts im JSON-Format
        return jsonify({"random_hash": random_hash})

    # Starte den Flask-Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
