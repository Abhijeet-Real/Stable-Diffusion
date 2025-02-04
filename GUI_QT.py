import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageFilter, ImageQt
from Prompt import prompt_list  # Importing the prompt list from Prompt.py
from Connector import main

class StableDiffusionGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Stable Diffusion Image Generator")
        self.setWindowIcon(QtGui.QIcon(r"D:\Stable Diffusion\Stable Diffusion Icon.ico"))
        self.setGeometry(100, 100, 500, 300)

        # Background label for displaying the image
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # Send background to the back

        # Layout setup
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()

        # Filename input
        filename_label = QtWidgets.QLabel("Filename:")
        filename_label.setStyleSheet("color: white; font-weight: bold;")
        self.filename_edit = QtWidgets.QLineEdit()
        form_layout.addRow(filename_label, self.filename_edit)

        # Prompt input
        prompt_label = QtWidgets.QLabel("Prompt:")
        prompt_label.setStyleSheet("color: white; font-weight: bold;")
        self.prompt_edit = QtWidgets.QTextEdit()
        self.prompt_edit.setPlaceholderText("Enter the prompt here...")
        form_layout.addRow(prompt_label, self.prompt_edit)

        # Random Prompt Button
        random_prompt_button = QtWidgets.QPushButton("Random Prompt")
        random_prompt_button.clicked.connect(self.set_random_prompt)
        form_layout.addRow(QtWidgets.QLabel(""), random_prompt_button)

        # Inference steps slider
        inference_label = QtWidgets.QLabel("Inference Steps:")
        inference_label.setStyleSheet("color: white; font-weight: bold;")
        self.inference_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.inference_slider.setRange(1, 100)
        self.inference_slider.setValue(40)
        form_layout.addRow(inference_label, self.inference_slider)

        # Guidance scale slider
        guidance_label = QtWidgets.QLabel("Guidance Scale:")
        guidance_label.setStyleSheet("color: white; font-weight: bold;")
        self.guidance_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.guidance_slider.setRange(1, 25)
        self.guidance_slider.setValue(15)
        form_layout.addRow(guidance_label, self.guidance_slider)

        # Internet toggle button
        self.internet_button = QtWidgets.QPushButton("Internet Off")
        self.internet_button.setCheckable(True)
        self.internet_button.clicked.connect(self.toggle_internet)
        form_layout.addRow(QtWidgets.QLabel(""), self.internet_button)

        # Fast mode toggle button
        self.fast_button = QtWidgets.QPushButton("Fast Disabled")
        self.fast_button.setCheckable(True)
        self.fast_button.clicked.connect(self.toggle_fast_mode)
        form_layout.addRow(QtWidgets.QLabel(""), self.fast_button)

        # Generate button
        generate_button = QtWidgets.QPushButton("Generate")
        generate_button.clicked.connect(self.generate_image)
        form_layout.addRow(QtWidgets.QLabel(""), generate_button)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

    def set_random_prompt(self):
        # Select a random sublist from prompt_list and skip the filename (index 0)
        random_prompt_data = random.choice(prompt_list)
        filename = random_prompt_data[0]
        random_prompt = random.choice(random_prompt_data[1:])  # Skip the first element (filename)
        
        # Set the filename and prompt fields
        self.filename_edit.setText(filename)
        self.prompt_edit.setPlainText(random_prompt)

    def showEvent(self, event):
        # Load and blur the background image here
        bg_image_path = r"D:\Stable Diffusion\Stable Diffusion Background.jpg"  # Ensure this path is correct
        pil_image = Image.open(bg_image_path)
        blurred_image = pil_image.filter(ImageFilter.GaussianBlur(0))  # Adjust blur radius if needed

        # Convert the PIL Image directly to a QImage
        img_data = blurred_image.convert("RGBA").tobytes("raw", "RGBA")
        width, height = blurred_image.size
        qimage = QtGui.QImage(img_data, width, height, QtGui.QImage.Format_RGBA8888)

        # Convert QImage to QPixmap and set to background label
        pixmap = QtGui.QPixmap.fromImage(qimage)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # Set the background to cover the whole window

        # Update the prompt input background with the corresponding area of the blurred background
        self.set_prompt_background_transparent()

        super().showEvent(event)

    def resizeEvent(self, event):
        # Adjust background label size on window resize
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def toggle_internet(self):
        if self.internet_button.isChecked():
            self.internet_button.setText("Internet On")
            self.internet_button.setStyleSheet("border: 2px solid green; color: green;")
        else:
            self.internet_button.setText("Internet Off")
            self.internet_button.setStyleSheet("")

    def toggle_fast_mode(self):
        if self.fast_button.isChecked():
            self.fast_button.setText("Fast Enabled")
            self.fast_button.setStyleSheet("border: 2px solid blue; color: blue;")
        else:
            self.fast_button.setText("Fast Disabled")
            self.fast_button.setStyleSheet("")

    def set_prompt_background_transparent(self):
        # Set the QTextEdit (prompt_edit) to transparent
        self.prompt_edit.setStyleSheet("background: rgba(255, 255, 255, 128);")

    def generate_image(self):
        # main function of connector
        main(object=[str(self.filename_edit.text()), str(self.prompt_edit.toPlainText())], \
            num_inference_steps=int(self.inference_slider.value()), \
            guidance_scale=int(self.guidance_slider.value()),\
            internet = self.internet_button.isChecked(),\
            fast = self.fast_button.isChecked())
        filename = self.filename_edit.text()
        prompt = self.prompt_edit.toPlainText()
        inference_steps = self.inference_slider.value()
        guidance_scale = self.guidance_slider.value()
        internet_on = self.internet_button.isChecked()
        fast_mode = self.fast_button.isChecked()

        # Placeholder for generation logic
        QtWidgets.QMessageBox.information(self, "Image Generated", f"Filename: {filename}\nPrompt: {prompt}\nInference Steps: {inference_steps}\nGuidance Scale: {guidance_scale}\nInternet: {internet_on}\nFast Mode: {fast_mode}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = StableDiffusionGUI()
    gui.show()
    sys.exit(app.exec_())