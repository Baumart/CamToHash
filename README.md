---

# CamToHash

CamToHash is a Python project that captures an image from a network webcam stream and generates a SHA3-512 hash from the image data. This hash can be used as a source of randomness or for cryptographic purposes. The project provides a simple Flask API endpoint to trigger the image capture and retrieve the generated hash.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoint](#api-endpoint)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)
9. [Notes](#notes)

---

## Overview

CamToHash connects to a network webcam (default stream: `http://10.0.11.85/webcam/?action=stream`), captures a single frame, and computes a SHA3-512 hash from the raw image bytes. The hash is returned via a REST API endpoint. This can be used for generating random values or as a demonstration of using camera entropy in applications.

---

## Features

- Captures a single frame from a network webcam stream.
- Generates a SHA3-512 hash from the captured image data.
- Provides a REST API endpoint using Flask to trigger the process and retrieve the hash.
- Optional debug mode to save captured images and logs for development.

---

## Requirements

- Python 3.8 or higher
- [OpenCV](https://pypi.org/project/opencv-python/) (`opencv-python`)
- [Flask](https://pypi.org/project/Flask/`)

Install the required libraries with:

```bash
pip install opencv-python flask
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Baumart/CamToHash.git
   ```
2. Navigate to the project directory:
   ```bash
   cd CamToHash
   ```

---

## Usage

1. Make sure your network webcam is accessible at the default URL (`http://10.0.11.85/webcam/?action=stream`) or modify the URL in `camCapture.py` if needed.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. The server will run on `http://0.0.0.0:5000/`.


---

## API Endpoint

- **GET /**  
  Triggers the image capture and hash generation.

  **Response Example:**
  ```json
  {
    "random_hash": "4d2c5ff1e8e33f6352db3b7a9df9f8b49b9f365fa4c9b26a73772b8e529ec6b7..."
  }
  ```

  If an error occurs (e.g., camera not available):
  ```json
  {
    "error": "Could not open camera!"
  }
  ```

---

## Troubleshooting

- **Camera not found:**  
  Ensure the webcam stream URL in `camCapture.py` is correct and accessible from your machine.
- **Port already in use:**  
  Make sure nothing else is running on port 5000 or change the port in `app.py`.
- **Debugging:**  
  Set `app.debug = True` in `app.py` to enable debug mode, which saves captured images and logs.

---

## License

MIT License

Copyright (c) 2025 Baum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Notes

- For any issues or feature requests, please open an issue in the repository.
- This project is intended for educational and demonstration purposes.

