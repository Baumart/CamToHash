---

# Project CamToEnrcyption

A brief description of your project goes here. Explain what the project does and why it's useful.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [License](#license)

---

## Overview

Provide a brief overview of the project. For example:
- This project captures images from a USB camera and generates a SHA3-512 hash from the image data.
- The hash can be used for cryptographic purposes or as a random value generator.
- Designed for educational purposes or as a base for further development.

---

## Features

- Captures images from a USB camera or uses a stored image.
- Converts the image into a byte array for processing.
- Generates a SHA3-512 hash from the image data.
- Allows consistent and random hash generation from image data.

---

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Libraries:
  - OpenCV (`opencv-python`)
  - hashlib (built-in)

Install the required libraries with:

```bash
pip install opencv-python
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Baumart/CamToEnrcyption.git
   ```
2. Navigate to the project directory:
   ```bash
   cd CamToEnrcyption
   ```

---

## Usage

### Capture an Image and Generate a Hash
1. Run the Python script:
   ```bash
   python capture_and_hash.py
   ```
2. The script will:
   - Capture an image from the USB camera.
   - Generate a SHA3-512 hash from the image data.
   - Display the hash in the console.


### Example Output
```plaintext
Generated random hash: 4d2c5ff1e8e33f6352db3b7a9df9f8b49b9f365fa4c9b26a73772b8e529ec6b7
```

---

## License


Copyright <2025> <Baum>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
.

---

## Notes

If you encounter any issues or bugs, feel free to open an issue in the repository. 

---

