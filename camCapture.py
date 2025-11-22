import cv2
import psutil
import struct
import os
import threading
from datetime import datetime
import base64
import hashlib

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

def get_system_entropy_bytes():
    """
    Collects system entropy as raw bytes (no hashing).
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    cpu_freq = psutil.cpu_freq().current
    pid = os.getpid()
    tid = threading.get_ident()

    # Pack numeric values into bytes
    sys_bytes = struct.pack(
        "fffII",  # 3 floats + 2 ints
        cpu_usage, ram_usage, cpu_freq,
        pid, tid
    )

    # Add time string as bytes
    sys_bytes += get_time().encode("utf-32")

    # Mix in OS randomness directly
    sys_bytes += os.urandom(128)

    return sys_bytes

def get_time():
    """
    Returns current time as string including milliseconds.
    """
    now = datetime.now()
    # %f gives microseconds → divide by 1000 to get milliseconds
    millis = int(now.microsecond / 1000)
    return now.strftime(f"%H_%M_%S_{millis:03d}")

def xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

def xor_quadrants(frame):
    """
    XOR all 4 image quadrants to produce a compact mix from the image.
    """
    h, w, _ = frame.shape
    half_h, half_w = h // 2, w // 2
    q1 = frame[0:half_h,     0:half_w    ].tobytes()
    q2 = frame[0:half_h,     half_w:w    ].tobytes()
    q3 = frame[half_h:h,     0:half_w    ].tobytes()
    q4 = frame[half_h:h,     half_w:w    ].tobytes()

    # XOR q1 ⊕ q2 ⊕ q3 ⊕ q4 (truncate to shortest length for safety)
    m = min(len(q1), len(q2), len(q3), len(q4))
    x = bytearray(q1[:m])
    for region in (q2[:m], q3[:m], q4[:m]):
        x = bytearray(xor(region,x))
    return bytes(x)

def capture_img(camera_id):
    """
    captures images from camera
    """
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        return None, "Could not open camera!"
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    if not ret:
        return None, "Error capturing image!"
    return frame

def capture_entropy_blob_base64(camera_id=1, as_base64=True):
    """
    builds entropy blob in base64 no max length
    """
    # Build entropy components
    sys_bytes = get_system_entropy_bytes()
    xor_bytes = xor_quadrants(capture_img(camera_id))

    # Final entropy bundle (no hash, no compression)
    entropy_blob = xor(sys_bytes,os.urandom(512)) + xor_bytes
    # Optional: return Base64 for portability
    if as_base64:
        return base64.b64encode(entropy_blob).decode("ascii"), None

    return entropy_blob, None

def capture_entropy_blob_sha3_512(camera_id=1,):
    """
    builds entropy blob in sha3-512 max length 128 bytes
    """
    # Build entropy components
    sys_bytes = get_system_entropy_bytes()
    xor_bytes = xor_quadrants(capture_img(camera_id))

    # Final entropy bundle (no hash, no compression)
    entropy_blob = xor(sys_bytes,os.urandom(512)) + xor_bytes

    random_hash = hashlib.sha3_512(entropy_blob).hexdigest()
    return random_hash, None

def capture_entropy_blob_shake_256_2048(camera_id=1,):
    """
    builds entropy blob in shake_256 max length 2048 bytes
    """
    # Build entropy components
    sys_bytes = get_system_entropy_bytes()
    xor_bytes = xor_quadrants(capture_img(camera_id))

    # Final entropy bundle (no hash, no compression)
    entropy_blob = xor(sys_bytes,os.urandom(512)) + xor_bytes

    random_hash = hashlib.shake_256(entropy_blob).hexdigest(2048)
    return random_hash, None

