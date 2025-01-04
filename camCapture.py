import cv2
import hashlib
from datetime import datetime



def get_time():
    now = datetime.now()
    return now.strftime("%H_%M_%S")

def debug(frame):
    from app import app
    if app.debug:
        file_path = "captured_frame." + get_time()
        app.logger.debug(f"Speichere Bild unter: {file_path}.bin")

        # Bild anzeigen
        cv2.imwrite(file_path + ".png", frame)
        print(f"Bild wurde gespeichert unter: {file_path}")

        # Bild in bin
        with open(file_path + ".bin", "wb") as file:
            file.write(frame)
            file.close()
            app.logger.debug(f"Bitmap wurde gespeichert unter: {file_path}.bin")
    return None

def capture_image_and_generate_random():
    # Öffne die Kamera (Kamera-ID 0 ist normalerweise die Standardkamera)
    # OBS ist 1
    cap = cv2.VideoCapture("http://10.0.11.85/webcam/?action=stream")
    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!")
        return None, "Kamera konnte nicht geöffnet werden!"

    # Nimm ein einzelnes Bild auf
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Erfassen des Bildes!")
        cap.release()
        return None, "Fehler beim Erfassen des Bildes!"

    debug(frame)

    # Kamera freigeben
    cap.release()
    cv2.destroyAllWindows()

    # Generiere einen "zufälligen" Wert basierend auf den Bilddaten
    random_hash = hashlib.sha3_512(frame.tobytes()).hexdigest()

    print("Generierter zufälliger Wert:", random_hash)
    return random_hash, None

