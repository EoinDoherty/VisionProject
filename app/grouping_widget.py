from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem

class Grouping(QWidget):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups
        self.title = "Image Groupings"
        self.left = 10
        self.right = 10
        self.width = 500
        self.height = 500
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
            header_widget.setText(0, group)

            for name in self.groups[group]:
                thing = QTreeWidgetItem(header_widget)
                thing.setText(1, name)
        
        if "" in self.groups:
            for name in self.groups[""]:
                thing = QTreeWidgetItem(tree)
                thing.setText(0, name)

        self.layout.addWidget(tree)
        self.setLayout(self.layout)
