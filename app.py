"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: User-Friendly GUI to interact with StudyTime functionality
"""

# GUI Handling
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLineEdit, QCalendarWidget, QTextEdit, QDialog, QDateEdit, QTimeEdit,
                             QComboBox, QGroupBox, QScrollArea, QTableWidget, QTableWidgetItem)
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

        self.info_box = QGroupBox("What's On") # Aesthetic grouping for the sidebar

        self.date_header = QLabel(parent=self)
        self.date_header.setFont(self.header_font)

        self.info_scroll = InfoWrapper(parent=self)

        #self.info_text = QLabel(parent=self)
        #self.info_text.setAlignment(Qt.AlignmentFlag.AlignTop)

        new_item_btn = QPushButton("Create New Item", self)
        new_item_btn.clicked.connect(self.create_item_dialog) # Opens a new dialog on button click

        info_layout.addWidget(self.date_header)
        info_layout.addWidget(new_item_btn)
        info_layout.addWidget(self.info_scroll)

        info_layout.setStretch(2, 4)
        self.info_box.setLayout(info_layout)

        self.date = QCalendarWidget(self)
        self.date.selectionChanged.connect(self.data_clicked) # Calls whenever the user selects a different date
        self.date.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat(0))

        layout.addWidget(self.info_box, 0, 0, 1, 1)
        layout.addWidget(self.date, 0, 1, 1, 1)

        self.data = self.data_clicked() # Called in order to set the information sidebar to the current date

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.setWindowTitle("StudyTime")
        self.showMaximized()

    def create_item_dialog(self):
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

        self.info_scroll.update(data)

    def open_item_details(self, item: dict):
        pass

class InfoWrapper(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.table = QTableWidget(0, 2, self)
        self.table.setShowGrid(False)

        self.parent = parent
    
    def update(self, data):

        self.table.clear()
        self.table.setRowCount(len(data))

        for idx, item in enumerate(data):
            self.table.setItem(idx, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(idx, 1, QTableWidgetItem(item["time"]))



class ItemDetailDialog(QDialog):
    def __init__(self, parent, item):
        super().__init__(parent)

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
        self.type_input.currentIndexChanged.connect(self.event_toggle)

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

        # Error Message Box
        self.error_message = QTextEdit("", self)

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

        # Error Dialog
        layout.addWidget(self.error_message, 6, 0, 1, 2)
        
        # Form Buttons
        layout.addWidget(submit_btn, 7, 0)
        layout.addWidget(cancel_btn, 7, 1)

        self.setLayout(layout)
    
    def get_inputs(self):
        """
        Returns all of the user inputted data from the GUI as a dictionary
        """
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

    def event_toggle(self):
        """
        Checks the type of item entered into the dialog box. If "Event" is selected, the subject is greyed out
        """
        if self.type_input.currentIndex() == 1: # Checks if the type_input has the "Event" index chosen
            self.class_input.setEnabled(False)
        elif not self.class_input.isEnabled:
            self.class_input.setEnabled(True)

    def add_item(self):
        """
        Gets data from dialog inputs and creates a new item accordingly
        """
        item_data = self.get_inputs()

        if item_data["name"] == "":
            self.error_message.setText("Please input a name and try again.")
        else:
            date = item_data["date"].toPyDate()
            time = item_data["time"].toPyTime()

            item_datetime = datetime(date.year, date.month, date.day, time.hour, time.minute, 0)

            func = [
                partial(self.window.data.add_task, subject = item_data["subject"]), # Subject is a necessary argument for this function, but it's not needed for all versions so it's passed here
                partial(self.window.data.add_event),
                partial(self.window.data.add_assignment, subject = item_data["subject"]) # See above
            ]

            func[item_data["type"]](item_data["name"], item_datetime) # Selects the relevant add function from studytime.core, and passes arguments

            self.window.update_info_text(item_datetime, self.window.data.search_date(item_datetime))
            self.window.date.setSelectedDate(item_data["date"])
            self.close()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())