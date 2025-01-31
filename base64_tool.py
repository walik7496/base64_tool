import sys
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QProgressBar, QTabWidget, QComboBox, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Base64ConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Base64 Image Converter")
        self.setGeometry(100, 100, 700, 500)

        self.supported_formats = ["png", "jpg", "jpeg", "bmp", "gif", "tiff"]  # supported formats

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget(self)
        self.tabs.addTab(self.createImageToBase64Tab(), "Image to Base64")
        self.tabs.addTab(self.createBase64ToImageTab(), "Base64 to Image")
        
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setAcceptDrops(True)  # Allow drag-and-drop

    def createImageToBase64Tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Text fields
        self.image_path_input = QLineEdit(self)
        self.image_path_input.setPlaceholderText("Image path here...")
        self.image_path_input.setReadOnly(True)

        # File selection button
        self.select_image_button = QPushButton("Select Image", self)
        self.select_image_button.clicked.connect(self.select_image)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)

        # Image preview
        self.image_label = QLabel(self)

        # Scaling before conversion
        self.scale_combo = QComboBox(self)
        self.scale_combo.addItems(["100%", "50%", "25%"])
        self.scale_combo.currentIndexChanged.connect(self.update_preview)

        # Button to convert to Base64
        self.encode_button = QPushButton("Convert Image to Base64", self)
        self.encode_button.clicked.connect(self.encode_image)

        # Base64 input field (we use QTextEdit instead of QLineEdit)
        self.base64_input = QTextEdit(self)
        self.base64_input.setPlaceholderText("Base64 string here...")
        self.base64_input.setReadOnly(True)

        # Layouts
        layout.addWidget(self.select_image_button)
        layout.addWidget(self.image_path_input)
        layout.addWidget(self.scale_combo)
        layout.addWidget(self.encode_button)
        layout.addWidget(self.base64_input)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.image_label)

        tab.setLayout(layout)
        return tab

    def createBase64ToImageTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Text fields for base64 (using QTextEdit)
        self.base64_input_image = QTextEdit(self)
        self.base64_input_image.setPlaceholderText("Base64 string here...")

        # Button for decoding base64
        self.decode_button = QPushButton("Convert Base64 to Image", self)
        self.decode_button.clicked.connect(self.decode_base64)

        # Selecting a format for saving
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(self.supported_formats)

        # Progress bar
        self.progress_bar_image = QProgressBar(self)
        self.progress_bar_image.setMaximum(100)

        # Image path field
        self.image_path_input_image = QLineEdit(self)
        self.image_path_input_image.setPlaceholderText("Save image path here...")

        # Button to copy image path from Image to Base64 tab
        self.copy_path_button = QPushButton("Copy Path from Image to Base64", self)
        self.copy_path_button.clicked.connect(self.copy_image_path)

        # Layouts
        layout.addWidget(self.base64_input_image)
        layout.addWidget(self.decode_button)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.progress_bar_image)
        layout.addWidget(self.image_path_input_image)
        layout.addWidget(self.copy_path_button)

        tab.setLayout(layout)
        return tab

    def select_image(self):
        # File selection dialog when clicking the Select Image button
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if file_path: # If the user has selected a file
            self.image_path_input.setText(file_path)  # Setting the path in the input field
            self.encode_image()  # Automatically start conversion

    def encode_image(self):
        image_path = self.image_path_input.text()
        if image_path:  # Checking if there is a way
            file_extension = image_path.split('.')[-1].lower()
            if file_extension not in self.supported_formats:
                self.show_error_message(f"Unsupported image format: {file_extension}")
                return

            self.progress_bar.setValue(0)

            # Scaling an image before conversion
            scale_factor = int(self.scale_combo.currentText().replace('%', '')) / 100
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(int(pixmap.width() * scale_factor), int(pixmap.height() * scale_factor))  # перетворено на int
            self.image_label.setPixmap(scaled_pixmap)

            # Convert image to base64
            try:
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    self.base64_input.setText(encoded_string)
                    self.progress_bar.setValue(100)
            except Exception as e:
                self.show_error_message(f"Error encoding image: {str(e)}")

    def decode_base64(self):
        base64_string = self.base64_input_image.toPlainText().strip()  # Clean up excess spaces

        if base64_string:
            try:
                print("Starting Base64 validation...")  # Logging

                # Clean up unnecessary spaces and add proper padding
                base64_string = self.fix_base64_padding(base64_string)

                if not self.is_valid_base64(base64_string):
                    self.show_error_message("Invalid Base64 string!")
                    print("Invalid Base64 string detected!")  # Logging
                    return

                print("Base64 decoded successfully.")  # Logging

                # Convert Base64 to Image
                image_data = base64.b64decode(base64_string)
                
                # Additional logging for image size after decoding
                print(f"Decoded image data length: {len(image_data)} bytes")

                # We get the path to save the file
                save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", f"Images (*.{self.format_combo.currentText().lower()})")
                if save_path:
                    with open(save_path, "wb") as image_file:
                        image_file.write(image_data)

                    print(f"Image successfully saved to: {save_path}")  # Logging

                    self.image_path_input_image.setText(save_path)
                    self.progress_bar_image.setValue(100)
                else:
                    self.show_error_message("No save path selected.")
            except Exception as e:
                self.show_error_message(f"Error decoding base64: {str(e)}")
                print(f"Error: {str(e)}")  # Error logging

    def fix_base64_padding(self, base64_string):
        # Add the necessary padding to the Base64 string if it is not enough
        missing_padding = len(base64_string) % 4
        if missing_padding:
            base64_string += '=' * (4 - missing_padding)
        return base64_string

    def update_preview(self):
        # Updating the image preview with the new scale
        image_path = self.image_path_input.text()
        if image_path:
            scale_factor = int(self.scale_combo.currentText().replace('%', '')) / 100
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(int(pixmap.width() * scale_factor), int(pixmap.height() * scale_factor))  # converted to int
            self.image_label.setPixmap(scaled_pixmap)

    def is_valid_base64(self, base64_string):
        try:
            base64.b64decode(base64_string, validate=True)
            return True
        except Exception:
            return False

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def copy_image_path(self):
        # Copy the path from the Image to Base64 tab to the Base64 to Image tab
        self.image_path_input_image.setText(self.image_path_input.text())

    # Adding drag-and-drop support
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_url = event.mimeData().urls()[0].toLocalFile()
        if file_url:
            self.image_path_input.setText(file_url)  # Setting the path to the image
            self.encode_image()  # We immediately convert

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Base64ConverterApp()
    window.show()
    sys.exit(app.exec_())
