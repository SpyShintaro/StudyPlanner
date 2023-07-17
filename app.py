"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: User-Friendly GUI to interact with StudyTime functionality
"""

# GUI Handling
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCalendarWidget, QTextEdit

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
        
        self.date_header = QLineEdit(parent=self)
        self.date_header.setReadOnly(True)

        self.info_box = QTextEdit(parent=self)
        self.info_box.setReadOnly(True)

        info_layout.addWidget(self.date_header)
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())