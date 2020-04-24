from os import getcwd
from sys import exit
import matplotlib.pyplot as plt
# from tkinter import Tk # That library is cursed
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMainWindow
from skimage import data
from skimage.io import imread
from app.visual_similarity.visual_widget import Visual
from app.grouping_widget import Grouping
from app.cascades.facial_rec_widget import Facial
from app.object_similarity.object_widget import ObjectWidget
from app.feature_similarity.feature_widget import FeatureWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Sorter"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.initUI()
        self.show()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        
        print_button = QPushButton("Print text")
        print_button.clicked.connect(lambda : print("clicked button"))
        # self.layout.addWidget(print_button)

        visual_grp_button = QPushButton("Group by visual features")
        visual_grp_button.clicked.connect(self.visual_group)
        self.layout.addWidget(visual_grp_button)

        test_grp = QPushButton("Debug grouping view")
        test_grp.clicked.connect(self.test_grp_view)
        # self.layout.addWidget(test_grp)

        facial_grp_button = QPushButton("Group using facial recognition")
        facial_grp_button.clicked.connect(self.facial_group)
        self.layout.addWidget(facial_grp_button)

        object_grp_button = QPushButton("Group using object recognition")
        object_grp_button.clicked.connect(self.object_group)
        self.layout.addWidget(object_grp_button)

        feat_grp_button = QPushButton("Group using SIFT feature comparison (very slow)")
        feat_grp_button.clicked.connect(self.feature_group)
        self.layout.addWidget(feat_grp_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        # self.setCentralWidget(self.layout)
    
    def visual_group(self):
        # print("Showing visual?")
        self.visual = Visual()
    
    def test_grp_view(self):
        self.grp_view = Grouping({"group 1": ["asdf", "qwe"], "": ["one", "another"]}, "~/github/VisionProject")
    
    def facial_group(self):
        self.facial = Facial()
    
    def object_group(self):
        self.object = ObjectWidget()
    
    def feature_group(self):
        self.feature = FeatureWidget()

if __name__ == "__main__":
    app = QApplication([])
    ex = App()
    exit(app.exec_())