from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QStackedLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from app.grouping_widget import Grouping
from app.image_io import load_images
from .feature_analysis import FeatureAnalyzer, group_from_matrix
from os import getcwd
import numpy as np

class External(QThread):

    count_changed = pyqtSignal(int)
    thread_exit = pyqtSignal(int)

    def __init__(self, analyzer, images):
        super().__init__()
        self.analyzer = analyzer
        self.images = images

    def run(self):
        n = len(self.images)
        descs = []
        self.classifications = []
        counter = 0

        for i in range(n):
            self.count_changed.emit(counter)
            counter += 1
            # self.classifications.append(classify_image(self.images[i]))
            # self.classifications.append(self.processor.classify_image(self.images[i]))
            descs.append(self.analyzer.get_descriptors(self.images[i]))
        
        self.distance_matrix = np.ones([n,n]) * np.inf

        for i in range(n):
            for j in range(i+1, n):
                self.count_changed.emit(counter)
                counter += 1
                distance = self.analyzer.mean_distance(descs[i], descs[j])
                self.distance_matrix[i,j] = distance
                self.distance_matrix[j,i] = distance
        self.thread_exit.emit(counter + 1)

    def get_matrix(self):
        return self.distance_matrix


class FeatureWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Groupings"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.initUI()
        self.show()
        self.analyzer = FeatureAnalyzer()
    
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

        self.names, self.images = load_images(self.image_path)

        n = len(self.images)

        self.progress_bar = QProgressBar(self)
        bar_size = n + (n**2 - n) / 2
        self.progress_bar.setMaximum(bar_size)
        analysis_layout.addWidget(self.progress_bar)

        self.calc = External(self.analyzer, self.images)
        self.calc.count_changed.connect(self.on_count_changed)
        self.calc.thread_exit.connect(self.on_thread_exit)
        self.calc.start()
    
    def on_count_changed(self, value):
        self.progress_bar.setValue(value)
    
    def on_thread_exit(self, value):
        self.progress_bar.setValue(value)
        classifications = self.calc.get_matrix()

        final_group = group_from_matrix(self.calc.get_matrix(), self.names)
        grouping = Grouping(final_group, self.image_path)
        self.central_widget = grouping
        self.setCentralWidget(grouping)