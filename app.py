"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: The GUI that the user will use to interact with the rest of the program
"""

# GUI Handling
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCalendarWidget, QTextEdit

import sys
from studytime.core import *

def get_data(file: str):
    data = SaveInstance(file)

    return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() # Parent Layout

        info_layout = QVBoxLayout() # Information Box Layout
        
        self.date_header = QLineEdit(parent=self)
        self.date_header.setReadOnly(True)

        self.info_box = QTextEdit(parent=self)
        self.info_box.setReadOnly(True)

        info_layout.addWidget(self.date_header)
        info_layout.addWidget(self.info_box)

        self.date = QCalendarWidget(self)
        self.date.selectionChanged.connect(self.data_clicked)

        info = QWidget()
        info.setLayout(info_layout)

        layout.addWidget(info)
        layout.addWidget(self.date)

        self.data_clicked()

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.setWindowTitle("StudyTime")
        self.show()
    
    def data_clicked(self):
        data = get_data("dates")

        date = self.date.selectedDate().toPyDate()

        self.update_info_box(date, data.search_date(date))
    
    def update_info_box(self, date, data):

        text = ""
        self.date_header.setText(f"Date: {date.strftime('%d/%m/%Y')}\n")

        for item in data:
            text += f"{item['name']}: {item['time']}\n{item['type']}"

        self.info_box.setText(f"{text}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())