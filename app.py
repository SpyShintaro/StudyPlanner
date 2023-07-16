"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: The GUI that the user will use to interact with the rest of the program
"""

# GUI Handling
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QDialog, QCalendarWidget, QTextEdit

import sys
from studytime.core import *

def get_data(file: str):
    data = SaveInstance(file)

    return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.info_box = QTextEdit(parent=self)
        self.info_box.setReadOnly(True)

        self.date = QCalendarWidget(self)
        self.date.selectionChanged.connect(self.data_clicked)

        layout.addWidget(self.date)
        layout.addWidget(self.info_box)

        self.data_clicked()

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.show()
    
    def data_clicked(self):
        data = get_data("dates")

        date = self.date.selectedDate().toPyDate()

        self.update_info_box(date, data.search_date(date))
    
    def update_info_box(self, date, data):

        text = f"Date: {date.strftime('%d/%m/%Y')}\n"

        for item in data:
            text += f"{item['name']}: {item['time']}\n{item['type']}"

        self.info_box.setText(f"{text}")
        

class DataDialog(QDialog):
    def __init__(self, parent, date: datetime, data: list):
        super().__init__(parent)

        data_widget = QTextEdit(self)

        text = f"Date: {date.strftime('%d/%m/%Y')}\n"

        for item in data:
            text += f"{item['name']}: {item['time']}\n{item['type']}"

        data_widget.setText(text)

        layout = QHBoxLayout()
        layout.addWidget(data_widget)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())