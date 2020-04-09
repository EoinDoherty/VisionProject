from os import getcwd
from sys import exit
import matplotlib.pyplot as plt
# from tkinter import Tk # That library is cursed
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog
from skimage import data
from skimage.io import imread

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Image Sorter"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.initUI()
        self.show()
        self.image = data.astronaut()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        image_button = QPushButton("Show image")
        image_button.clicked.connect(self.show_image)
        self.layout.addWidget(image_button)
        
        print_button = QPushButton("Print text")
        print_button.clicked.connect(lambda : print("clicked button"))
        self.layout.addWidget(print_button)

        file_nav_button = QPushButton("Select Image")
        file_nav_button.clicked.connect(self.file_nav)
        self.layout.addWidget(file_nav_button)

        self.setLayout(self.layout)
    
    def show_image(self):
        plt.imshow(self.image)
        plt.show()
    
    def file_nav(self):
        # file_dialog = QFileDialog(self)
        # file_dialog.setViewMode(QFileDialog.Detail)

        # if file_dialog.exec_():
        #     print(file_dialog.selectedFiles())

        # print(QFileDialog.getOpenFileNames(self, "select files", getcwd()))
        image_path, _ = QFileDialog.getOpenFileName(self, "Find a file", getcwd(), "Image files (*png *jpg *jpeg)")
        try:
            self.image = imread(image_path)
        except ValueError:
            pass

if __name__ == "__main__":
    # app = QApplication([])
    # ex = App()
    # exit(app.exec_())
    from app.visual_similarity.cluster_similar import group_images
    print("hello")
    print(group_images("data/"))