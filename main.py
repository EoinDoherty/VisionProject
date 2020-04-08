import matplotlib.pyplot as plt
# from tkinter import Tk # That library is cursed
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from skimage import data

def show_image():
    img = data.astronaut()
    plt.imshow(img)
    plt.show()

def main():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    image_button = QPushButton("Show image")
    image_button.clicked.connect(show_image)

    layout.addWidget(image_button)

    text_button = QPushButton("Print text")
    text_button.clicked.connect(lambda : print("clicked"))

    layout.addWidget(text_button)

    window.setLayout(layout)
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()