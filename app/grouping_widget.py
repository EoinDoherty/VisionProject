from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from app.image_io import save_group

class External(QThread):

    thread_exit = pyqtSignal(int)

    def __init__(self, grouping, src_path, dest_path):
        super().__init__()
        self.grouping = grouping
        self.src_path = src_path
        self.dest_path = dest_path

    def run(self):
        save_group(self.grouping, self.src_path, self.dest_path)
        self.thread_exit.emit(1)

class Grouping(QWidget):
    def __init__(self, groups, src_path):
        super().__init__()
        self.groups = groups
        self.title = "Image Groupings"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
        self.src_path = src_path
        self.initUI()
        self.show()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        # list = QListWidget()

        # for i in range(len(self.groups)):
        #     QListWidgetItem(f"{i}: {self.groups[i]}", list)
        
        # self.layout.addWidget(list)
        tree = QTreeWidget()
        tree.setColumnCount(2)

        for group in self.groups:
            if group == "":
                continue
            
            header_widget = QTreeWidgetItem(tree)
            header_widget.setText(0, str(group))

            for name in self.groups[group]:
                thing = QTreeWidgetItem(header_widget)
                thing.setText(1, str(name))
        
        if "" in self.groups:
            for name in self.groups[""]:
                thing = QTreeWidgetItem(tree)
                thing.setText(0, str(name))

        self.layout.addWidget(tree)

        save_btn = QPushButton("Save grouping to disk")
        save_btn.clicked.connect(self.save_grouping)
        self.layout.addWidget(save_btn)

        self.setLayout(self.layout)
    
    def save_grouping(self):
        save_dir = QFileDialog.getExistingDirectory(self, "Find a directory", self.src_path)
        
        self.ex = External(self.groups, self.src_path, save_dir)
        self.ex.start()
        self.ex.thread_exit.connect(self.on_thread_exit)
        # save_group(self.groups, self.src_path, save_dir)
    
    def on_thread_exit(self):
        self.layout.addWidget(QLabel("Saved"))
