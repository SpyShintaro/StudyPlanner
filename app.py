"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: User-Friendly GUI to interact with StudyTime functionality
"""

# GUI Handling
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QCalendarWidget, QTextEdit, QDialog,
                             QDateEdit, QTimeEdit, QComboBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont

import sys
from studytime.core import *

def get_data(file: str):
    """
    Creates a Save Instance object to interact with the user's data
    """
    data = SaveInstance(file)

    return data

class MainWindow(QMainWindow):
    """
    The main application window; will show the current view, as well as item data
    """
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout() # Parent Layout

        info_layout = QVBoxLayout() # Information Box Layout

        self.header_font = QFont("Helvetica", 15)
        self.header_font.setBold(True)
        
        self.date_header = QLabel(parent=self)
        self.date_header.setFont(self.header_font)

        self.info_box = QTextEdit(parent=self)
        self.info_box.setReadOnly(True)

        new_item_btn = QPushButton("Create New Item", self)
        new_item_btn.clicked.connect(self.open_item_dialog)

        info_layout.addWidget(self.date_header)
        info_layout.addWidget(new_item_btn)
        info_layout.addWidget(self.info_box)

        self.date = QCalendarWidget(self)
        self.date.selectionChanged.connect(self.data_clicked) # Calls whenever the user selects a different date

        info = QWidget()
        info.setLayout(info_layout)

        layout.addWidget(info)
        layout.addWidget(self.date)

        self.data_clicked() # Called in order to set the information sidebar to the current date

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.setWindowTitle("StudyTime")
        self.show()

    def open_item_dialog(self):
        """
        Creates and displays a dialog for the user to add a new item
        """
        dialog = NewItemDialog(self)
        dialog.exec()
    
    def data_clicked(self):
        """
        Slot function that updates the info sidebar whenever the user selects a new date
        """
        
        data = get_data("dates")

        date = self.date.selectedDate().toPyDate() # Converts the selected date of the calendar to a Datetime object

        self.update_info_box(date, data.search_date(date))
    
    def update_info_box(self, date, data):
        """
        Changes the information sidebar to display relevant date information
        """
        
        text = ""
        self.date_header.setText(f"Date: {date.strftime('%d/%m/%Y')}\n") # Displays the current date as text

        for item in data:
            text += f"{item['name']}: {item['time']}\n{item['type']}" # Shows most relevant item data

        self.info_box.setText(f"{text}")

class NewItemDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add Item")
        layout = QGridLayout()

        header = QLabel(self)
        header.setText("Add New Item")
        header.setFont(parent.header_font)
        
        name_text = QLabel("Name: ", self)
        name_input = QLineEdit(self)

        type_text = QLabel("Type: ", self)
        
        type_input = QComboBox(self)
        type_input.addItems(["Task", "Event", "Assignment"])

        date_text = QLabel("Date: ", self)

        date_input = QDateEdit(self)
        date_input.setDate(QDate.currentDate())
        date_input.setCalendarPopup(True)

        time_text = QLabel("Time: ", self)

        time_input = QTimeEdit(self)
        time_input.setTime(QTime.currentTime())

        # Header
        layout.addWidget(header, 0, 0)

        # Name Input
        layout.addWidget(name_text, 1, 0)
        layout.addWidget(name_input, 1, 1)

        # Type Input
        layout.addWidget(type_text, 2, 0)
        layout.addWidget(type_input, 2, 1)

        # Date Input
        layout.addWidget(date_text, 3, 0)
        layout.addWidget(date_input, 3, 1)

        # Time Input
        layout.addWidget(time_text, 4, 0)
        layout.addWidget(time_input, 4, 1)

        self.setLayout(layout)
    
    def add_item(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())