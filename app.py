"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: The GUI that the user will use to interact with the rest of the program
"""

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()
        self.view = view

        self.initUI()
    
    def initUI(self):
        widget = QWidget()
        main_layout = QGridLayout()

        main_layout.addWidget(QGroupBox("Item Information"), 1, 1, 4, 2)
        main_layout.addWidget(self.view, 1, 3, 4, 7)

        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.show()

class CalendarView(QWidget):
    def __init__(self):
        super().__init__()

        calendar_layout = QGridLayout()

        for week in range(4):
            for day in range(7):
                calendar_layout.addWidget(QMessageBox(), week, day)
        
        self.setLayout(calendar_layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow(CalendarView())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()