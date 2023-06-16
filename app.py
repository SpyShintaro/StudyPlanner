"""
StudyPlanner/app

Author: Jake Hickey
Date: 29/05/23
Description: The GUI that the user will use to interact with the rest of the program
"""

# GUI Handling
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

# Datetime handling
import calendar
from datetime import datetime

from studytime import core

class MainWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()

        self.initUI(view)
    
    def initUI(self, view):
        widget = QWidget()
        main_layout = QGridLayout()

        tab = QTabWidget()
        tab.addTab(view, "Calendar")

        main_layout.addWidget(QGroupBox("Item Information"), 1, 1, 4, 2)
        main_layout.addWidget(tab, 1, 2, 4, 7)

        main_layout.setHorizontalSpacing(25)

        widget.setLayout(main_layout)

        self.setCentralWidget(widget)
        self.show()

class CalendarView(QWidget): # Generates a calendar view containing 35 days
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        calendar_layout = QGridLayout()

        dates = self.map_dates() # A list of dates in the month, spaced with zeroes to start at the correct weekday

        for week in range(5): # Iterates through five rows (representing a week)
            for day in range(7): # Iterates through each day in the week, filling out columns
                day_box = QLabel()
                
                try:
                    date = str(dates.pop())

                    if date != "0":
                        day_box.setText(date)
                except IndexError:
                    pass

                calendar_layout.addWidget(day_box, week, day)
        
        self.setLayout(calendar_layout)
        self.updateGeometry()

class DateObject(QListWidget):
    """
    A widget template for all dates in the calendar
    """
    def __init__(self, date):
        super().__init__()

        self.header = QTextEdit(f"{date}")

    def initUI(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow(CalendarView())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()