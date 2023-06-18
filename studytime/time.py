"""
studytime.time

Author: Jake Hickey
Description: A library containing definitions for time classes in studytime 
"""

# Imports
from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


class Year:
    def __init__(self, year_data):
        self.year = year_data

class Month:
    def __init__(self, month: datetime.month, year: datetime.year, date_objects):
        self.name = f"{months[month - 1]} {year}"
        self.dates = date_objects

class Date:
    def __init__(self, date: datetime) -> None:
        pass