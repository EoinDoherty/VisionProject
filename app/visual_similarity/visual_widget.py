from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QStackedLayout
from os import getcwd
from .group_similar import group_images
from app.grouping_widget import Grouping

class Visual(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Groupings"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.initUI()
        self.show()
    
    def initUI(self):
        self.select_layout = QVBoxLayout()

        path_button = QPushButton("Select a directory to analyze")
        path_button.clicked.connect(self.file_nav)

        self.select_layout.addWidget(path_button)
        
        # self.layout = QStackedLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.select_layout)
        self.setCentralWidget(self.central_widget)
    
    def file_nav(self):
        image_path = QFileDialog.getExistingDirectory(self, "Find a directory", getcwd())
        
        if image_path == "":
            return

        groups = group_images(image_path)
        grouping = Grouping(groups)
        self.central_widget = grouping
        self.setCentralWidget(grouping)

if __name__ == "__main__":
    app = QApplication([])
    ex = Visual()
    exit(app.exec_())