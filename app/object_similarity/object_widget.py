from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QStackedLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from app.grouping_widget import Grouping
from app.image_io import load_images
from .object_detection import ObjectDetection
from os import getcwd

class External(QThread):

    count_changed = pyqtSignal(int)
    thread_exit = pyqtSignal(int)

    def __init__(self, obj_detector, images):
        super().__init__()
        self.processor = obj_detector
        self.images = images

    def run(self):
        n = len(self.images)
        self.classifications = []

        for i in range(n):
            self.count_changed.emit(i)
            # self.classifications.append(classify_image(self.images[i]))
            self.classifications.append(self.processor.classify_image(self.images[i]))
        self.thread_exit.emit(i+1)

    def get_classifications(self):
        return self.classifications

class ObjectWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Groupings"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.initUI()
        self.show()
        self.processor = ObjectDetection()
    
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

        self.names, self.images = self.processor.load_directory(self.image_path)

        n = len(self.images)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(n)
        analysis_layout.addWidget(self.progress_bar)

        self.calc = External(self.processor, self.images)
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
        classifications = self.calc.get_classifications()

        print(self.names)
        print(len(self.names), len(classifications))
        print(classifications)
        final_group = self.processor.group_labels(classifications, self.names)
        grouping = Grouping(final_group, self.image_path)
        self.central_widget = grouping
        self.setCentralWidget(grouping)
