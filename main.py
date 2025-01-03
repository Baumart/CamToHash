import cv2
import hashlib
from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%H_%M_%S")

def debug(frame):
    time = get_time()
    file_path = "captured_frame." + time

    # Bild anzeigen
    # cv2.imwrite(file_path + ".png", frame)
    # print(f"Bild wurde gespeichert unter: {file_path}")

    # Bild in bin
    with open(file_path + ".bin", "wb") as file:
        file.write(frame)
        file.close()
    print(f"Bitmap wurde gespeichert unter: {file_path}")

    return None

def capture_image_and_generate_random():
    # Öffne die Kamera (Kamera-ID 0 ist normalerweise die Standardkamera)
    # OBS ist 1
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!")
        return None

    # Warte kurz, damit die Kamera stabil ist
    cv2.waitKey(1000)  # Warte 1 Sekunde

    # Nimm ein einzelnes Bild auf
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Erfassen des Bildes!")
        cap.release()
        return None

    debug(frame)

    # Kamera freigeben
    cap.release()
    cv2.destroyAllWindows()

    # Generiere einen "zufälligen" Wert basierend auf den Bilddaten
    random_hash = hashlib.sha3_512(frame.tobytes()).hexdigest()

    print("Generierter zufälliger Wert:", random_hash)
    return random_hash


# Funktion aufrufen
random_value = capture_image_and_generate_random()
