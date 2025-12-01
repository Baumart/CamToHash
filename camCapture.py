import cv2
import psutil
import struct
import os
from datetime import datetime
import hashlib

def get_time():
    now = datetime.now()
    millis = int(now.microsecond / 1000)
    return now.strftime(f"%H_%M_%S_{millis:03d}")

def get_system_entropy_bytes():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    cpu_freq = psutil.cpu_freq().current

    sys_bytes = struct.pack("fff", cpu_usage, ram_usage, cpu_freq,)
    sys_bytes += get_time().encode("utf-32")
    sys_bytes += os.urandom(2048)

    return sys_bytes

def capture_img(camera_id):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    if not ret:
        return None
    return frame

def _capture_multi_frame_mix(camera_id, frames=32):
    mixed = bytearray()
    for _ in range(frames):
        img = capture_img(camera_id)
        if img is not None:
            mixed.extend(img)
            mixed.extend(os.urandom(128))
        else:
            return None
    return bytes(mixed)

def capture_entropy_blob_sha3_512(camera_id=1):
    sys_bytes = get_system_entropy_bytes()
    cam_mix = _capture_multi_frame_mix(camera_id)
    if cam_mix is None:
        return None, True
    _ = sys_bytes + cam_mix + os.urandom(4096)
    random_hash = hashlib.sha3_512(_).hexdigest()
    return random_hash, None

def capture_entropy_blob_shake_256_1024(camera_id=1):
    sys_bytes = get_system_entropy_bytes()
    cam_mix = _capture_multi_frame_mix(camera_id)
    if cam_mix is None:
        return None, True
    _ = sys_bytes + cam_mix + os.urandom(4096)
    random_hash = hashlib.shake_256(_).hexdigest(1024)
    return random_hash, None
