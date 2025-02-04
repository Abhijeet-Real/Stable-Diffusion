import random, sys, Config
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image, ImageFilter, ImageQt
from Prompt import prompt_list
from Connector import main

class ImageGenerationThread(QThread):
    # Signal to notify when the image generation is complete
    finished = pyqtSignal()

    def __init__(self, filename, prompt, num_inference_steps, guidance_scale, internet, fast):
        super().__init__()
        self.filename = filename
        self.prompt = prompt
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self.internet = internet
        self.fast = fast

    def run(self):
        # Call the main function for image generation with provided parameters
        main(object=[self.filename, self.prompt],
             num_inference_steps=self.num_inference_steps,
             guidance_scale=self.guidance_scale,
             internet=self.internet,
             fast=self.fast)
        # Emit the finished signal when done
        self.finished.emit()

class StableDiffusionGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Stable Diffusion Image Generator")
        self.setWindowIcon(QtGui.QIcon(r"D:\Stable Diffusion\Stable Diffusion Icon.ico"))
        self.setGeometry(100, 100, 500, 355)

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

        # Generate button
        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.clicked.connect(self.start_image_generation)
        form_layout.addRow(QtWidgets.QLabel(""), self.generate_button)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

    def set_random_prompt(self):
        random_prompt_data = random.choice(prompt_list)
        filename = random_prompt_data[0]
        random_prompt = random.choice(random_prompt_data[1:])  # Skip the first element (filename)
        self.filename_edit.setText(filename)
        self.prompt_edit.setPlainText(random_prompt)

    def showEvent(self, event):
        bg_image_path = r"D:\Stable Diffusion\Stable Diffusion Background.jpg"
        pil_image = Image.open(bg_image_path)
        blurred_image = pil_image.filter(ImageFilter.GaussianBlur(0))

        img_data = blurred_image.convert("RGBA").tobytes("raw", "RGBA")
        width, height = blurred_image.size
        qimage = QtGui.QImage(img_data, width, height, QtGui.QImage.Format_RGBA8888)

        pixmap = QtGui.QPixmap.fromImage(qimage)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.set_prompt_background_transparent()
        super().showEvent(event)

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def set_prompt_background_transparent(self):
        self.prompt_edit.setStyleSheet("background: rgba(255, 255, 255, 128);")

    def start_image_generation(self):
        filename = self.filename_edit.text()
        prompt = self.prompt_edit.toPlainText()
        inference_steps = self.inference_slider.value()
        guidance_scale = self.guidance_slider.value()

        # Disable the Generate button during generation
        self.generate_button.setEnabled(False)

        # Start a worker thread for image generation
        self.image_generation_thread = ImageGenerationThread(
            filename, prompt, inference_steps, guidance_scale, True, True
        )
        self.image_generation_thread.finished.connect(self.on_image_generation_finished)
        self.image_generation_thread.start()

    def on_image_generation_finished(self):
        QtWidgets.QMessageBox.information(self, "Image Generated", "The image has been successfully generated.")
        self.generate_button.setEnabled(True)  # Re-enable the Generate button

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = StableDiffusionGUI()
    gui.show()
    sys.exit(app.exec_())