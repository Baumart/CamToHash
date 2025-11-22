# camCapture.py
import cv2
import psutil
import struct
import os
import threading
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

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def xor_quadrants(frame):
    h, w, _ = frame.shape
    half_h, half_w = h // 2, w // 2
    q1 = frame[0:half_h, 0:half_w].tobytes()
    q2 = frame[0:half_h, half_w:w].tobytes()
    q3 = frame[half_h:h, 0:half_w].tobytes()
    q4 = frame[half_h:h, half_w:w].tobytes()

    m = min(len(q1), len(q2), len(q3), len(q4))
    x = bytearray(q1[:m])
    for region in (q2[:m], q3[:m], q4[:m]):
        x = bytearray(xor(region, x))
    return bytes(x)

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
        frame = capture_img(camera_id)
        if frame is not None:
            mixed.extend(xor_quadrants(frame))
        mixed.extend(os.urandom(128))
    return bytes(mixed)

def _whiten(raw):
    return hashlib.shake_256(raw).digest(2048)

def capture_entropy_blob_sha3_512(camera_id=1):
    sys_bytes = get_system_entropy_bytes()
    cam_mix = _capture_multi_frame_mix(camera_id)
    raw = xor(sys_bytes, os.urandom(2048)) + cam_mix
    whitened = _whiten(raw)
    random_hash = hashlib.sha3_512(whitened).hexdigest()
    return random_hash, None

def capture_entropy_blob_shake_256_1024(camera_id=1):
    sys_bytes = get_system_entropy_bytes()
    cam_mix = _capture_multi_frame_mix(camera_id)
    raw = xor(sys_bytes, os.urandom(2048)) + cam_mix
    whitened = _whiten(raw)
    random_hash = hashlib.shake_256(whitened).hexdigest(1024)
    return random_hash, None
