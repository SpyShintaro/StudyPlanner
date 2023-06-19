"""
studytime.time_class

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

    def prepare_dict(self) -> dict:
        """
        Maps out data into dictionary for storage in JSON format
        """
        data = {
            "name": self.name,
            "data": [date.prepare_dict() for date in self.dates]
        }

        return data

class Date:
    def __init__(self, date: datetime.day) -> None:
        self.name = f"{date}"
        self.items = {}
    
    def add_item(self, item):
        self.items[item["name"]] = {item}
    
    def prepare_dict(self) -> dict:
        data = {
            "name": self.name,
            "data": self.items
        }

        return data