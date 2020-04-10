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
        group_counter = 1

        self.groups.sort(key=lambda x: 0 if type(x) == tuple else 1)

        for i in range(len(self.groups)):
            entry = self.groups[i]

            if type(entry) == tuple:
                header = f"Group {group_counter}"
                header_widget = QTreeWidgetItem(tree)
                header_widget.setText(0, header)

                for name in entry:
                    thing = QTreeWidgetItem(header_widget)
                    thing.setText(1, name)
                group_counter += 1
            else:
                thing = QTreeWidgetItem(tree)
                thing.setText(0, str(self.groups[i]))

        self.layout.addWidget(tree)
        self.setLayout(self.layout)
