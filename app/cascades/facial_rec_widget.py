from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QFileDialog, QApplication, QMainWindow, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from os import getcwd
from .facial_recognition import group_faces_binary, group_faces_count, detect_face
from app.grouping_widget import Grouping
from app.image_io import load_images

class External(QThread):

    count_changed = pyqtSignal(int)
    thread_exit = pyqtSignal(int)

    def __init__(self, images):
        super().__init__()
        self.faces = []
        self.images = images

    def run(self):
        for i in range(len(self.images)):
            self.count_changed.emit(i)
            # print(i)
            self.faces.append(detect_face(self.images[i]))
        self.thread_exit.emit(i+1)

    def get_faces(self):
        return self.faces


class Facial(QMainWindow):
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
        self.image_path = QFileDialog.getExistingDirectory(self, "Find a directory", getcwd())
        
        if self.image_path == "":
            return

        self.select_layout.addWidget(QLabel(self.image_path))

        run_btn = QPushButton("Analyze")
        run_btn.clicked.connect(self.process)
        self.select_layout.addWidget(run_btn)
    
    def process(self):

        analysis_layout = QVBoxLayout()
        progress_text = QLabel("Processing")
        analysis_layout.addWidget(progress_text)
        self.central_widget = QWidget()
        self.central_widget.setLayout(analysis_layout)
        self.setCentralWidget(self.central_widget)

        self.names, images = load_images(self.image_path)

        n = len(images)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(n)
        analysis_layout.addWidget(self.progress_bar)

        self.calc = External(images)
        self.calc.count_changed.connect(self.on_count_changed)
        self.calc.thread_exit.connect(self.on_thread_exit)
        self.calc.start()

        # groups = group_faces_binary(image_path)
        # grouping = Grouping(groups)
        # self.central_widget = grouping
        # self.setCentralWidget(grouping)
    
    def on_count_changed(self, value):
        self.progress_bar.setValue(value)
    
    def on_thread_exit(self, value):
        self.progress_bar.setValue(value)
        self.faces = self.calc.get_faces()
        # print(self.faces)
        
        self.post_processing_layout = QVBoxLayout()

        count_button = QPushButton("Group by number of faces")
        count_button.clicked.connect(self.count_group)
        self.post_processing_layout.addWidget(count_button)

        binary_button = QPushButton("Find portraits")
        binary_button.clicked.connect(self.binary_group)
        self.post_processing_layout.addWidget(binary_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.post_processing_layout)
        self.setCentralWidget(self.central_widget)
    
    def count_group(self):
        grouping = Grouping(group_faces_count(self.faces, self.names), self.image_path)
        self.central_widget = grouping
        self.setCentralWidget(grouping)
    
    def binary_group(self):
        grouping = Grouping(group_faces_binary(self.faces, self.names), self.image_path)
        self.central_widget = grouping
        self.setCentralWidget(grouping)

if __name__ == "__main__":
    app = QApplication([])
    ex = Facial()
    exit(app.exec_())