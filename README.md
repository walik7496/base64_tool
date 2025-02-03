# Base64 Image Converter

This is a Python-based application that allows you to easily convert images to Base64 strings and vice versa. It supports a variety of image formats and provides a simple graphical user interface (GUI) built using PyQt5.

## Features

- **Image to Base64**: Convert images (PNG, JPG, JPEG, BMP, GIF, TIFF) to Base64 encoded strings.
- **Base64 to Image**: Decode Base64 strings and save them as images in different formats.
- **Preview**: View images with adjustable scaling before conversion.
- **Drag-and-Drop**: Easily drag and drop images into the application for conversion.
- **Error handling**: The app will notify you of any errors (e.g., invalid Base64 or unsupported formats).

## Installation

### Requirements

Before running the application, make sure you have Python 3.x installed. You'll also need to install the necessary Python libraries.

1. Clone this repository:
    ```bash
    git clone https://github.com/walik7496/base64_tool.git
    ```
2. Navigate to the project folder:
    ```bash
    cd base64-image-converter
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Dependencies

The following Python libraries are required to run the application:
- `PyQt5`: For creating the GUI.
- `base64`: Built-in Python module for Base64 encoding/decoding.

These dependencies are automatically listed in `requirements.txt`, so you can install them using the command above.

## Usage

1. **Run the Application**:
   After installing the dependencies, you can run the application by executing:
   ```bash
   python convertbase64.py
