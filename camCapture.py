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
        app.logger.debug(f"Saving image to: {file_path}.bin")

        # Show image
        cv2.imwrite(file_path + ".png", frame)
        print(f"Image saved to: {file_path}")

        # Image to bin
        with open(file_path + ".bin", "wb") as file:
            file.write(frame)
            file.close()
            app.logger.debug(f"Bitmap saved to: {file_path}.bin")
    return None

def capture_image_and_generate_random():
    # Open the camera (camera ID 0 is usually the default camera)
    # OBS is 1
    cap = cv2.VideoCapture("http://10.0.11.85/webcam/?action=stream")
    if not cap.isOpened():
        print("Could not open camera!")
        return None, "Could not open camera!"

    # Capture a single image
    ret, frame = cap.read()
    if not ret:
        print("Error capturing image!")
        cap.release()
        return None, "Error capturing image!"

    debug(frame)

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

    # Generate a "random" value based on the image data
    random_hash = hashlib.sha3_512(frame.tobytes()).hexdigest()

    print("Generated random value:", random_hash)
    return random_hash, None

