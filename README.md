# CamToHash

CamToHash is a Python project that captures a single image from a network webcam stream, generates entropy from the image and system state, and returns this entropy in multiple formats (raw bytes, Base64, SHA3-512, SHAKE-256). A lightweight Flask API allows you to trigger the capture and retrieve the generated values.

---

## Table of Contents

1. Overview  
2. Features  
3. Requirements  
4. Installation  
5. Usage  
6. API Endpoints  
7. Examples  
8. Troubleshooting  
9. License  
10. Notes  

---

## Overview

CamToHash connects to a network webcam stream, captures a single frame, and combines it with system entropy sources such as:

- CPU usage  
- RAM usage
- Timestamps  
- OS random bytes  

The resulting entropy blob can be:
 
- hashed using SHA3-512 (fixed 64-byte digest)  
- hashed using SHAKE-256 (extendable output, e.g. 2048 bytes)

This makes the project useful for random value generation or demonstrating the combination of camera and system entropy.

---

## Features

- Captures a single frame from a network webcam  
- Collects system entropy from multiple sources  
- XORs image quadrants to increase entropy  
- Multiple output formats:
  - SHA3-512 hash  
  - SHAKE-256 hash (custom length)  
- REST API via Flask  
- Optional debug mode to save captured images and logs  

---
## Testing
![test_plot.png](img%2Ftest_plot.png)

---
## Requirements

- Python 3.8+  
- opencv-python  
- FastAPI 
- psutil  

Install dependencies:

pip install requirements.txt

---

## Installation

1. Clone the repository:  
   git clone https://github.com/Baumart/CamToHash.git  

2. Navigate to the project directory.

---

## Usage

1. Ensure your webcam stream is accessible or update the URL in camCapture.py.  
2. Start the fastapi server.  
3. The server will be available at:  
   https://0.0.0.0:443/

---

## API Endpoints

**GET /sha3-512**  
→ Returns a SHA3-512 hash.

**GET /**  
→ Returns a SHAKE-256 hash (default: 2048 bytes; length can be configured).

---

## Examples

### Example: SHA3-512 (Fixed Length)
JSON response:
```json
{
  "random_hash": "4d2c5ff1e8e33f6352db3b7a9df9f8b49b9f365fa4c9b26a73772b8e529ec6b7..."
}
```

SHA3-512 always produces exactly 64 bytes (128 hex characters).

---

## Troubleshooting

- **Camera not found**: Verify the stream URL.  
- **Port already in use**: Ensure port 443 is free or change it in app.py.  
- **Debug mode**: Enable app.debug = True to store captured frames and logs.

---

## License

MIT License © 2025 Baum

Provided “as is”, without warranty of any kind. Use at your own risk.

---

## Notes

- For issues or feature requests, please open an issue in the GitHub repository.  
- This project is intended for educational and demonstration purposes.
