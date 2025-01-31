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

        self.supported_formats = ["png", "jpg", "jpeg", "bmp", "gif", "tiff"]  # підтримувані формати

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget(self)
        self.tabs.addTab(self.createImageToBase64Tab(), "Image to Base64")
        self.tabs.addTab(self.createBase64ToImageTab(), "Base64 to Image")
        
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setAcceptDrops(True)  # Дозволяємо drag-and-drop

    def createImageToBase64Tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Текстові поля
        self.image_path_input = QLineEdit(self)
        self.image_path_input.setPlaceholderText("Image path here...")
        self.image_path_input.setReadOnly(True)

        # Кнопка вибору файлу
        self.select_image_button = QPushButton("Select Image", self)
        self.select_image_button.clicked.connect(self.select_image)

        # Прогресбар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)

        # Попередній перегляд зображення
        self.image_label = QLabel(self)

        # Масштабування перед перетворенням
        self.scale_combo = QComboBox(self)
        self.scale_combo.addItems(["100%", "50%", "25%"])
        self.scale_combo.currentIndexChanged.connect(self.update_preview)

        # Кнопка для перетворення в Base64
        self.encode_button = QPushButton("Convert Image to Base64", self)
        self.encode_button.clicked.connect(self.encode_image)

        # Поле для вводу base64 (використовуємо QTextEdit замість QLineEdit)
        self.base64_input = QTextEdit(self)
        self.base64_input.setPlaceholderText("Base64 string here...")
        self.base64_input.setReadOnly(True)

        # Лейаути
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

        # Текстові поля для base64 (використовуємо QTextEdit)
        self.base64_input_image = QTextEdit(self)
        self.base64_input_image.setPlaceholderText("Base64 string here...")

        # Кнопка для декодування base64
        self.decode_button = QPushButton("Convert Base64 to Image", self)
        self.decode_button.clicked.connect(self.decode_base64)

        # Вибір формату для збереження
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(self.supported_formats)

        # Прогресбар
        self.progress_bar_image = QProgressBar(self)
        self.progress_bar_image.setMaximum(100)

        # Поле для шляху зображення
        self.image_path_input_image = QLineEdit(self)
        self.image_path_input_image.setPlaceholderText("Save image path here...")

        # Кнопка для копіювання шляху зображення з вкладки Image to Base64
        self.copy_path_button = QPushButton("Copy Path from Image to Base64", self)
        self.copy_path_button.clicked.connect(self.copy_image_path)

        # Лейаути
        layout.addWidget(self.base64_input_image)
        layout.addWidget(self.decode_button)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.progress_bar_image)
        layout.addWidget(self.image_path_input_image)
        layout.addWidget(self.copy_path_button)

        tab.setLayout(layout)
        return tab

    def select_image(self):
        # Діалог вибору файлу при натисканні кнопки Select Image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if file_path:  # Якщо користувач вибрав файл
            self.image_path_input.setText(file_path)  # Встановлюємо шлях у поле вводу
            self.encode_image()  # Автоматично починаємо перетворення

    def encode_image(self):
        image_path = self.image_path_input.text()
        if image_path:  # Перевіряємо, чи є шлях
            file_extension = image_path.split('.')[-1].lower()
            if file_extension not in self.supported_formats:
                self.show_error_message(f"Unsupported image format: {file_extension}")
                return

            self.progress_bar.setValue(0)

            # Масштабування зображення перед перетворенням
            scale_factor = int(self.scale_combo.currentText().replace('%', '')) / 100
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(int(pixmap.width() * scale_factor), int(pixmap.height() * scale_factor))  # перетворено на int
            self.image_label.setPixmap(scaled_pixmap)

            # Перетворення зображення в base64
            try:
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    self.base64_input.setText(encoded_string)
                    self.progress_bar.setValue(100)
            except Exception as e:
                self.show_error_message(f"Error encoding image: {str(e)}")

    def decode_base64(self):
        base64_string = self.base64_input_image.toPlainText().strip()  # Очищаємо від зайвих пробілів

        if base64_string:
            try:
                print("Starting Base64 validation...")  # Логування

                # Очищаємо непотрібні пробіли та додаємо правильний padding
                base64_string = self.fix_base64_padding(base64_string)

                if not self.is_valid_base64(base64_string):
                    self.show_error_message("Invalid Base64 string!")
                    print("Invalid Base64 string detected!")  # Логування
                    return

                print("Base64 decoded successfully.")  # Логування

                # Перетворення Base64 у зображення
                image_data = base64.b64decode(base64_string)
                
                # Додаткове логування для розміру зображення після декодування
                print(f"Decoded image data length: {len(image_data)} bytes")

                # Отримуємо шлях для збереження файлу
                save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", f"Images (*.{self.format_combo.currentText().lower()})")
                if save_path:
                    with open(save_path, "wb") as image_file:
                        image_file.write(image_data)

                    print(f"Image successfully saved to: {save_path}")  # Логування

                    self.image_path_input_image.setText(save_path)
                    self.progress_bar_image.setValue(100)
                else:
                    self.show_error_message("No save path selected.")
            except Exception as e:
                self.show_error_message(f"Error decoding base64: {str(e)}")
                print(f"Error: {str(e)}")  # Логування помилки

    def fix_base64_padding(self, base64_string):
        # Додаємо необхідний padding до Base64 рядка, якщо його не вистачає
        missing_padding = len(base64_string) % 4
        if missing_padding:
            base64_string += '=' * (4 - missing_padding)
        return base64_string

    def update_preview(self):
        # Оновлюємо попередній перегляд зображення з новим масштабом
        image_path = self.image_path_input.text()
        if image_path:
            scale_factor = int(self.scale_combo.currentText().replace('%', '')) / 100
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(int(pixmap.width() * scale_factor), int(pixmap.height() * scale_factor))  # перетворено на int
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
        # Копіюємо шлях з вкладки Image to Base64 на вкладку Base64 to Image
        self.image_path_input_image.setText(self.image_path_input.text())

    # Додаємо підтримку drag-and-drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_url = event.mimeData().urls()[0].toLocalFile()
        if file_url:
            self.image_path_input.setText(file_url)  # Встановлюємо шлях до зображення
            self.encode_image()  # Одразу перетворюємо

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Base64ConverterApp()
    window.show()
    sys.exit(app.exec_())
