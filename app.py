"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: User-Friendly GUI to interact with StudyTime functionality
"""

# GUI Handling
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLineEdit, QCalendarWidget, QTextEdit, QDialog, QDateEdit, QTimeEdit,
                             QComboBox, QGroupBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont

import sys
from functools import partial
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

        layout = QGridLayout() # Parent Layout
        layout.setColumnStretch(1, 2)

        info_layout = QVBoxLayout() # Information Box Layout

        self.header_font = QFont("Helvetica", 13)
        self.header_font.setBold(True)

        self.info_box = QGroupBox("What's On")

        self.date_header = QLabel(parent=self)
        self.date_header.setFont(self.header_font)

        self.info_text = QLabel(parent=self)

        new_item_btn = QPushButton("Create New Item", self)
        new_item_btn.clicked.connect(self.open_item_dialog)

        info_layout.addWidget(self.date_header)
        info_layout.addWidget(new_item_btn)
        info_layout.addWidget(self.info_text)

        #self.info_text.setLayout(info_layout)
        info_layout.setStretch(2, 4)
        self.date = QCalendarWidget(self)
        self.date.selectionChanged.connect(self.data_clicked) # Calls whenever the user selects a different date

        layout.addLayout(info_layout, 0, 0, 1, 1)
        layout.addWidget(self.date, 0, 1, 1, 1)

        self.data = self.data_clicked() # Called in order to set the information sidebar to the current date

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.setWindowTitle("StudyTime")
        self.showMaximized()

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

        self.update_info_text(date, data.search_date(date))
        return data
    
    def update_info_text(self, date, data):
        """
        Changes the information sidebar to display relevant date information
        """
        
        text = ""
        self.date_header.setText(f"Date: {date.strftime('%d/%m/%Y')}\n") # Displays the current date as text

        for item in data:
            text += f"{item['name']}: {item['time']}\n{item['type']}\n" # Shows most relevant item data

        self.info_text.setText(f"{text}")

class NewItemDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = self.parentWidget()
        self.setWindowTitle("Add Item")
        layout = QGridLayout()

        # Header
        header = QLabel(self)
        header.setText("Add New Item")
        header.setFont(parent.header_font)
        
        # Name
        name_text = QLabel("Name: ", self)
        self.name_input = QLineEdit(self)
        
        # Item Type
        type_text = QLabel("Type: ", self)
        
        self.type_input = QComboBox(self)
        self.type_input.addItems(["Task", "Event", "Assignment"])
        self.type_input.currentIndexChanged.connect(self.check_type)

        # Date
        date_text = QLabel("Date: ", self)

        self.date_input = QDateEdit(self)
        self.date_input.setDate(self.window.date.selectedDate())
        self.date_input.setCalendarPopup(True)

        # Time
        time_text = QLabel("Time: ", self)

        self.time_input = QTimeEdit(self)
        self.time_input.setTime(QTime.currentTime())

        # Subject
        class_text = QLabel("Subject: ", self)

        self.class_input = QComboBox(self)
        self.class_input.addItems(["Applied Computing", "Maths Methods", "Maths Specialist", "Chemistry", "English"])

        # Buttons
        submit_btn = QPushButton("Submit", self, clicked=self.add_item)
        cancel_btn = QPushButton("Cancel", self, clicked=self.close)

        # Header
        layout.addWidget(header, 0, 0)

        # Name Input
        layout.addWidget(name_text, 1, 0)
        layout.addWidget(self.name_input, 1, 1)

        # Type Input
        layout.addWidget(type_text, 2, 0)
        layout.addWidget(self.type_input, 2, 1)

        # Date Input
        layout.addWidget(date_text, 3, 0)
        layout.addWidget(self.date_input, 3, 1)

        # Time Input
        layout.addWidget(time_text, 4, 0)
        layout.addWidget(self.time_input, 4, 1)

        # Class Input
        layout.addWidget(class_text, 5, 0)
        layout.addWidget(self.class_input, 5, 1)

        # Form Buttons
        layout.addWidget(submit_btn, 6, 0)
        layout.addWidget(cancel_btn, 6, 1)

        self.setLayout(layout)
    
    def get_inputs(self):
        name = self.name_input.text()
        type = self.type_input.currentIndex()
        date = self.date_input.date()
        time = self.time_input.time()
        subject = self.class_input.currentText()

        data = {
            "name": name,
            "type": type,
            "date": date,
            "time": time,
            "subject": subject
        }

        return data

    def check_type(self):
        """
        Checks the type of item entered into the dialog box. If "Event" is selected, the subject is greyed out
        """
        if self.type_input.currentIndex() == 1:
            self.class_input.setEnabled(False)
        elif not self.class_input.isEnabled:
            self.class_input.setEnabled(True)

    def add_item(self):
        """
        Gets data from dialog inputs and creates a new item accordingly
        """
        item_data = self.get_inputs()
        date = item_data["date"].toPyDate()
        time = item_data["time"].toPyTime()

        item_datetime = datetime(date.year, date.month, date.day, time.hour, time.minute, 0)

        func = [
            partial(self.window.data.add_task, subject = item_data["subject"]),
            partial(self.window.data.add_event),
            partial(self.window.data.add_assignment, subject = item_data["subject"])
        ]

        func[item_data["type"]](item_data["name"], item_datetime)

        self.window.update_info_text(item_datetime, self.window.data.search_date(item_datetime))
        self.window.date.setSelectedDate(item_data["date"])
        self.close()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())